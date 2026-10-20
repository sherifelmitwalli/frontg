#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
frontg_v2_methods.py
====================

Candidate extraction, comparison methods, and per-instance evaluation for
Benchmark B. Synthetic data only.

Methods compared (all operate on the same enumerated Funder->terminal candidate
pathways):

* ``frontg``               published rule: gated score >= 60 AND eligibility
                           (funding edge AND min grade >= 2). Fixed; never tuned.
* ``frontg_no_elig``       ablation: gated score >= 60, eligibility rule removed.
* ``frontg_no_elig_no_gate`` ablation: ungated score >= 60, no eligibility.
* ``frontg_tuned``         FrontG score + eligibility, threshold tuned on base
                           validation instances (tests whether 60 is the issue).
* ``mean_grade``           mean evidence grade along the path (tuned threshold).
* ``centrality``           mean PageRank of the path's interior nodes (tuned).
* ``logreg``               logistic regression on path + structural features.
* ``gbm``                  gradient-boosted trees on the same features.
* ``gbm_elig``             gbm wrapped by the FrontG eligibility rule (the
                           safety layer applied to a learned ranker).
* ``gbm_oracle``           gbm trained on labelled data from the *target*
                           regime (reference upper bound; not deployable).

Learned models and tuned thresholds use only base-regime training/validation
instances unless stated otherwise, so the other regimes are distribution shifts.
"""
from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional, Tuple

import networkx as nx
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

import frontg_metrics as MET
import generate_synthetic_graph as G1
from frontg_config import TRIAGE_THRESHOLD, ScoreWeights
from frontg_v2_generator import RegimeV2, generate_instance

PATH_FEATURES = ["has_funding_edge", "mean_grade", "min_grade", "n_evidence_types",
                 "temporal_clustering", "semantic_similarity", "amplification",
                 "cooccurrence", "path_length"]
STRUCT_FEATURES = ["interior_mean_degree", "interior_max_degree", "interior_mean_pagerank",
                   "terminal_in_degree", "n_parallel_edges", "max_grade"]
LEARNED_FEATURES = PATH_FEATURES + STRUCT_FEATURES
# Pure topology features (no evidence content): used by the structural-leakage probe.
STRUCT_ONLY = ["interior_mean_degree", "interior_max_degree", "interior_mean_pagerank",
               "terminal_in_degree", "n_parallel_edges"]

METHOD_ORDER = ["frontg", "frontg_no_elig", "frontg_no_elig_no_gate", "frontg_tuned",
                "mean_grade", "centrality", "logreg_path", "logreg", "gbm", "gbm_elig", "gbm_oracle"]
METHOD_LABELS = {
    "frontg": "FrontG (published rule)",
    "frontg_no_elig": "FrontG without eligibility rule",
    "frontg_no_elig_no_gate": "FrontG without eligibility or gate",
    "frontg_tuned": "FrontG, tuned threshold",
    "mean_grade": "Mean evidence grade",
    "centrality": "Path PageRank centrality",
    "logreg_path": "Logistic regression (FrontG features only)",
    "logreg": "Logistic regression",
    "gbm": "Gradient boosting",
    "gbm_elig": "Gradient boosting + eligibility rule",
    "gbm_oracle": "Gradient boosting, in-regime (reference)",
}


# --------------------------------------------------------------------------- #
# Candidate extraction
# --------------------------------------------------------------------------- #
def extract_candidates(regime: RegimeV2, seed: int) -> pd.DataFrame:
    """Generate one Benchmark-B instance and return its scored candidate table."""
    gen = generate_instance(regime, seed)
    Gm = gen.to_multidigraph()
    scorer = G1.ReviewPriorityScorer(Gm, ScoreWeights())
    df, feats = G1.enumerate_candidate_paths(Gm, scorer, gen.ground_truth_paths,
                                             embedded_nodes=set(gen.bystander_nodes))
    if df.empty:
        return df
    fdf = pd.DataFrame(feats)
    for c in PATH_FEATURES + ["max_grade"]:
        df[c] = fdf[c].values
    # structural features on the simple directed graph
    S = nx.DiGraph()
    S.add_nodes_from(Gm.nodes())
    S.add_edges_from((u, v) for u, v, _ in Gm.edges(keys=True))
    pr = nx.pagerank(S, alpha=0.85)
    deg = dict(S.degree())
    indeg = dict(S.in_degree())
    mult: Dict[Tuple[str, str], int] = {}
    for u, v, _ in Gm.edges(keys=True):
        mult[(u, v)] = mult.get((u, v), 0) + 1
    rows = []
    for seq in df["node_sequence"]:
        nodes = seq.split(" -> ")
        interior = nodes[1:-1] or nodes[:1]
        rows.append({
            "interior_mean_degree": float(np.mean([deg[n] for n in interior])),
            "interior_max_degree": float(np.max([deg[n] for n in interior])),
            "interior_mean_pagerank": float(np.mean([pr[n] for n in interior])),
            "terminal_in_degree": float(indeg[nodes[-1]]),
            "n_parallel_edges": float(sum(mult[(a, b)] for a, b in zip(nodes[:-1], nodes[1:]))),
            "bystander_stratum": max([gen.bystander_nodes.get(n, 0) for n in nodes]),
        })
    df = pd.concat([df.reset_index(drop=True), pd.DataFrame(rows)], axis=1)
    # property-defined evidence classes (independent of labels)
    df["weak_evidence_only"] = ((df["has_funding_edge"] == 0) & (df["max_grade"] <= 2)).astype(int)
    df["low_floor"] = (df["min_grade"] <= 1).astype(int)
    df["eligible"] = df["eligible_for_high_priority"].astype(int)
    meta = gen.path_meta
    df["planted_kind"] = [meta.get(s, {}).get("kind", "derived") for s in df["node_sequence"]]
    df["true_funding_observed"] = [meta.get(s, {}).get("funding_observed", -1) if l == 1 else -1
                                   for s, l in zip(df["node_sequence"], df["ground_truth_label"])]
    df["regime"] = regime.name
    df["seed"] = seed
    df.attrs["n_planted"] = len(gen.ground_truth_paths)
    return df


def build_pool(regime: RegimeV2, seeds) -> pd.DataFrame:
    frames = [extract_candidates(regime, s) for s in seeds]
    frames = [f for f in frames if not f.empty]
    return pd.concat(frames, ignore_index=True)


# --------------------------------------------------------------------------- #
# Method fitting
# --------------------------------------------------------------------------- #
def _best_f1_threshold(scores: np.ndarray, y: np.ndarray) -> float:
    best_t, best_f1 = float(np.max(scores)) + 1.0, -1.0
    for t in np.unique(scores):
        pred = scores >= t
        tp = int(np.sum(pred & (y == 1)))
        if tp == 0:
            continue
        prec, rec = tp / pred.sum(), tp / max(1, y.sum())
        f1 = 2 * prec * rec / (prec + rec)
        if f1 > best_f1:
            best_f1, best_t = f1, float(t)
    return best_t


def frontg_rank_score(df: pd.DataFrame) -> np.ndarray:
    """Continuous ranking key for the gated FrontG rule: ineligible paths below all eligible."""
    return df["review_priority_score"].values - 100.0 * (1 - df["eligible"].values)


def _gbm(seed: int = 0) -> GradientBoostingClassifier:
    """Gradient-boosted trees (scikit-learn defaults except a fixed random state)."""
    return GradientBoostingClassifier(random_state=seed)


def fit_methods(train: pd.DataFrame, valid: pd.DataFrame) -> Dict[str, Any]:
    """Fit learned models on base-regime training data; tune thresholds on validation."""
    Xtr, ytr = train[LEARNED_FEATURES].values, train["ground_truth_label"].values
    Xva, yva = valid[LEARNED_FEATURES].values, valid["ground_truth_label"].values
    lr = make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000, C=1.0))
    lr.fit(Xtr, ytr)
    gb = _gbm().fit(Xtr, ytr)
    lrp = make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000, C=1.0))
    lrp.fit(train[PATH_FEATURES].values, ytr)
    fitted = {"logreg": lr, "gbm": gb, "logreg_path": lrp, "thresholds": {}}
    th = fitted["thresholds"]
    th["frontg_tuned"] = _best_f1_threshold(frontg_rank_score(valid), yva)
    th["mean_grade"] = _best_f1_threshold(valid["mean_grade"].values, yva)
    th["centrality"] = _best_f1_threshold(valid["interior_mean_pagerank"].values, yva)
    th["logreg"] = _best_f1_threshold(lr.predict_proba(Xva)[:, 1], yva)
    th["logreg_path"] = _best_f1_threshold(lrp.predict_proba(valid[PATH_FEATURES].values)[:, 1], yva)
    th["gbm"] = _best_f1_threshold(gb.predict_proba(Xva)[:, 1], yva)
    p_va = gb.predict_proba(Xva)[:, 1]
    elig_va = valid["eligible"].values
    th["gbm_elig"] = _best_f1_threshold(p_va - 2.0 * (1 - elig_va), yva)
    return fitted


def fit_oracle(train: pd.DataFrame, valid: pd.DataFrame) -> Dict[str, Any]:
    gb = _gbm().fit(train[LEARNED_FEATURES].values, train["ground_truth_label"].values)
    t = _best_f1_threshold(gb.predict_proba(valid[LEARNED_FEATURES].values)[:, 1],
                           valid["ground_truth_label"].values)
    return {"model": gb, "threshold": t}


def method_scores(df: pd.DataFrame, fitted: Dict[str, Any],
                  oracle: Optional[Dict[str, Any]] = None) -> Dict[str, Tuple[np.ndarray, np.ndarray]]:
    """Return {method: (continuous ranking score, binary decision)} for one candidate table."""
    out: Dict[str, Tuple[np.ndarray, np.ndarray]] = {}
    s = df["review_priority_score"].values
    s_ung = df["score_ungated_ablation"].values
    elig = df["eligible"].values.astype(bool)
    rk = frontg_rank_score(df)
    th = fitted["thresholds"]
    out["frontg"] = (rk, (s >= TRIAGE_THRESHOLD) & elig)
    out["frontg_no_elig"] = (s, s >= TRIAGE_THRESHOLD)
    out["frontg_no_elig_no_gate"] = (s_ung, s_ung >= TRIAGE_THRESHOLD)
    out["frontg_tuned"] = (rk, rk >= th["frontg_tuned"])
    mg = df["mean_grade"].values
    out["mean_grade"] = (mg, mg >= th["mean_grade"])
    c = df["interior_mean_pagerank"].values
    out["centrality"] = (c, c >= th["centrality"])
    X = df[LEARNED_FEATURES].values
    p_lr = fitted["logreg"].predict_proba(X)[:, 1]
    out["logreg"] = (p_lr, p_lr >= th["logreg"])
    p_lp = fitted["logreg_path"].predict_proba(df[PATH_FEATURES].values)[:, 1]
    out["logreg_path"] = (p_lp, p_lp >= th["logreg_path"])
    p_gb = fitted["gbm"].predict_proba(X)[:, 1]
    out["gbm"] = (p_gb, p_gb >= th["gbm"])
    k = p_gb - 2.0 * (1 - elig)
    out["gbm_elig"] = (k, k >= th["gbm_elig"])
    if oracle is not None:
        p_o = oracle["model"].predict_proba(X)[:, 1]
        out["gbm_oracle"] = (p_o, p_o >= oracle["threshold"])
    return out


# --------------------------------------------------------------------------- #
# Per-instance evaluation
# --------------------------------------------------------------------------- #
def evaluate_instance(df: pd.DataFrame, scores: Dict[str, Tuple[np.ndarray, np.ndarray]]) -> List[Dict[str, Any]]:
    y = df["ground_truth_label"].values.astype(int)
    n_planted = int(df.attrs.get("n_planted", y.sum()))
    rows = []
    for m, (cont, dec) in scores.items():
        dec = np.asarray(dec, dtype=bool)
        tp = int(np.sum(dec & (y == 1)))
        fp = int(np.sum(dec & (y == 0)))
        nflag = int(dec.sum())
        prec = tp / nflag if nflag else np.nan
        rec = tp / n_planted if n_planted else np.nan
        f1 = (2 * prec * rec / (prec + rec)) if (nflag and tp) else 0.0
        ap = float(average_precision_score(y, cont)) if 0 < y.sum() < len(y) else np.nan
        row = {"method": m, "regime": df["regime"].iloc[0], "seed": int(df["seed"].iloc[0]),
               "n_candidates": len(df), "n_planted": n_planted, "n_flagged": nflag,
               "tp": tp, "fp": fp, "precision": prec, "recall": rec, "f1": f1, "auprc": ap,
               "prevalence": y.mean()}
        # safety properties (label-independent evidence classes)
        weak = df["weak_evidence_only"].values == 1
        low = df["low_floor"].values == 1
        row["n_weak_evidence_flags"] = int(np.sum(dec & weak))
        row["n_weak_evidence_false_flags"] = int(np.sum(dec & weak & (y == 0)))
        row["n_low_floor_flags"] = int(np.sum(dec & low))
        for st in (1, 2, 3):
            mask = df["bystander_stratum"].values == st
            row[f"n_bystander_g{st}_paths"] = int(mask.sum())
            row[f"n_bystander_g{st}_flags"] = int(np.sum(dec & mask))
        # recall split by whether the true pathway's funding was observed
        tf = df["true_funding_observed"].values
        for flag, name in ((1, "funding_observed"), (0, "funding_hidden")):
            mask = (y == 1) & (tf == flag)
            row[f"n_true_{name}"] = int(mask.sum())
            row[f"tp_{name}"] = int(np.sum(dec & mask))
        rows.append(row)
    return rows


def bootstrap_ci(values, n_boot: int = 2000, seed: int = 7, stat: Callable = np.mean) -> Tuple[float, float, float]:
    v = np.asarray([x for x in values if not (isinstance(x, float) and np.isnan(x))], dtype=float)
    if len(v) == 0:
        return (np.nan, np.nan, np.nan)
    rng = np.random.default_rng(seed)
    boots = [stat(v[rng.integers(0, len(v), len(v))]) for _ in range(n_boot)]
    return (float(stat(v)), float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5)))
