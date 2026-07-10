#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
frontg_metrics.py
=================

Evaluation metrics and the transparent review-priority score computation for the
synthetic validation harness. This module is the single source of truth for the
scoring formula so that the harness and audit trail use the same computation.

It also implements the RQ5 robustness analyses:
  * exact analytic score bounds for structurally constrained path families
    (proving that weak-signal-only chains can never reach the triage threshold);
  * a full threshold sweep (precision/recall/specificity at every cut-off);
  * a weight-perturbation sensitivity analysis (deterministic seed).
"""
from __future__ import annotations

from typing import Dict, List, Any

import numpy as np
import pandas as pd
from scipy.stats import kendalltau, spearmanr

from frontg_config import EDGE_TYPE_GRADE, ScoreWeights, TRIAGE_THRESHOLD

ELIGIBILITY_RULE_VERSION = 'funding_and_min_grade_2_v1'


# --------------------------------------------------------------------------- #
# Review-priority score (RQ4)
# --------------------------------------------------------------------------- #
def score_components(features: Dict[str, Any], weights: ScoreWeights,
                     gated: bool = True) -> Dict[str, float]:
    """Return the per-term decomposition of the review-priority score.

    The score is a bounded weighted sum in [0, 100]:

        support           = min_grade / grade_max
        supporting_signal = w_sem*semantic + w_amp*amplification + w_cooc*cooccurrence
        raw  = w_fund*funding_edge
             + w_mean*(mean_grade/grade_max)
             + w_min *(min_grade/grade_max)
             + w_types*(n_evidence_types/types_norm)
             + w_temp*temporal_clustering
             + support*supporting_signal           # supporting signals are gated
             - length_penalty*max(0, path_length-3)
        score = clip(raw, 0, 100)

    Semantic-similarity and amplification are SUPPORTING signals only: they are
    multiplied by ``support`` (the normalised weakest-hop grade), so a path that
    drops to a low-grade hop cannot be pushed to high priority by these signals
    alone.

    ``gated=False`` computes the ABLATED score in which the support gate is
    removed (supporting signals enter at full weight). This is used only for the
    gate-ablation robustness analysis, never for triage decisions.
    """
    w = weights
    f = features
    support = (f["min_grade"] / w.grade_max) if gated else 1.0
    supporting_signal = (w.w_semantic * f["semantic_similarity"]
                         + w.w_amplification * f["amplification"]
                         + w.w_cooccurrence * f["cooccurrence"])
    t_funding = w.w_funding_edge * f["has_funding_edge"]
    t_mean = w.w_mean_grade * (f["mean_grade"] / w.grade_max)
    t_min = w.w_min_grade * (f["min_grade"] / w.grade_max)
    t_types = w.w_evidence_types * (f["n_evidence_types"] / w.types_norm)
    t_temporal = w.w_temporal * f["temporal_clustering"]
    t_supporting = support * supporting_signal
    penalty = w.length_penalty * max(0, f["path_length"] - 3)
    raw = (t_funding + t_mean + t_min + t_types + t_temporal + t_supporting - penalty)
    score = float(max(0.0, min(100.0, raw)))
    return {
        "support_factor": round(support, 3),
        "term_funding": round(t_funding, 3),
        "term_mean_grade": round(t_mean, 3),
        "term_min_grade": round(t_min, 3),
        "term_evidence_types": round(t_types, 3),
        "term_temporal": round(t_temporal, 3),
        "term_supporting": round(t_supporting, 3),
        "penalty_length": round(-penalty, 3),
        "raw_score": round(raw, 3),
        "score": round(score, 2),
    }


# --------------------------------------------------------------------------- #
# Classification metrics
# --------------------------------------------------------------------------- #
def binary_metrics(y_true: List[int], y_pred: List[int]) -> Dict[str, float]:
    """Precision, recall, F1, FPR, FNR, specificity from binary labels."""
    yt = np.asarray(y_true, dtype=int)
    yp = np.asarray(y_pred, dtype=int)
    tp = int(np.sum((yt == 1) & (yp == 1)))
    fp = int(np.sum((yt == 0) & (yp == 1)))
    fn = int(np.sum((yt == 1) & (yp == 0)))
    tn = int(np.sum((yt == 0) & (yp == 0)))

    def safe(n, d):
        return float(n) / float(d) if d else 0.0

    precision = safe(tp, tp + fp)
    recall = safe(tp, tp + fn)
    f1 = safe(2 * precision * recall, precision + recall) if (precision + recall) else 0.0
    return {
        "tp": tp, "fp": fp, "fn": fn, "tn": tn,
        "precision": round(precision, 4), "recall": round(recall, 4), "f1": round(f1, 4),
        "false_positive_rate": round(safe(fp, fp + tn), 4),
        "false_negative_rate": round(safe(fn, fn + tp), 4),
        "specificity": round(safe(tn, tn + fp), 4),
    }


def score_band_truth_summary(df: pd.DataFrame, score_col: str = "review_priority_score",
                             label_col: str = "ground_truth_label",
                             n_bins: int = 5) -> List[Dict[str, Any]]:
    """Describe planted-positive proportions by score band.

    This is a descriptive synthetic truth summary, not a probability
    estimate and not an estimate of real-world risk.
    """
    if df.empty:
        return []
    bins = np.linspace(0, 100, n_bins + 1)
    d = df.copy()
    d["_bucket"] = pd.cut(d[score_col], bins=bins, include_lowest=True)
    out = []
    for bucket, sub in d.groupby("_bucket", observed=True):
        lo, hi = float(bucket.left), float(bucket.right)
        out.append({"score_bucket": str(bucket), "bucket_low": lo, "bucket_high": hi,
                    "n_candidates": int(len(sub)), "mean_score": round(float(sub[score_col].mean()), 2),
                    "planted_positive_proportion": round(float(sub[label_col].mean()), 4),
                    "interpretation": "descriptive synthetic truth summary; not a probability estimate"})
    return out


def high_priority_eligibility(features: Dict[str, Any]) -> Dict[str, Any]:
    """Apply the pre-specified safety gate separately from the raw score."""
    reasons = []
    if not features.get("has_funding_edge"):
        reasons.append("missing_funding_edge")
    if float(features.get("min_grade", 0.0)) < 2.0:
        reasons.append("minimum_evidence_grade_below_2")
    return {
        "eligible_for_high_priority": not reasons,
        "eligibility_rule_version": ELIGIBILITY_RULE_VERSION,
        "ineligible_reason": ";".join(reasons),
    }


# --------------------------------------------------------------------------- #
# RQ5 robustness analyses
# --------------------------------------------------------------------------- #
def attainable_score_bounds(weights: ScoreWeights, threshold: float) -> pd.DataFrame:
    """Enumerate exact maxima in the implemented controlled edge-type space.

    Every sequence of two to four edge types from ``EDGE_TYPE_GRADE`` is
    evaluated. Score features are derived from those actual edge types, rather
    than inferred generously from grade patterns. The result is exact for this
    controlled vocabulary and scoring rule; it is not a claim about arbitrary
    real-world networks.
    """
    families = [
        ("weak_only_no_funding", "No funding edge; every hop grade <= 2", lambda et, gr: "funds" not in et and max(gr) <= 2),
        ("funding_with_grade0_floor", "Funding edge present; weakest hop grade 0", lambda et, gr: "funds" in et and min(gr) == 0),
        ("funding_with_grade1_floor", "Funding edge present; weakest hop grade 1", lambda et, gr: "funds" in et and min(gr) == 1),
        ("funding_with_grade2_floor", "Funding edge present; weakest hop grade 2", lambda et, gr: "funds" in et and min(gr) == 2),
        ("fully_documentary_min_grade3", "Funding edge present; every hop grade >= 3", lambda et, gr: "funds" in et and min(gr) >= 3),
    ]
    import itertools as _it
    edge_types = tuple(EDGE_TYPE_GRADE)
    rows = []
    for family, constraint, is_member in families:
        best_gated = best_ungated = None
        for n_hops in (2, 3, 4):
            for types in _it.product(edge_types, repeat=n_hops):
                grades = tuple(EDGE_TYPE_GRADE[edge_type] for edge_type in types)
                if not is_member(types, grades):
                    continue
                features = {
                    "has_funding_edge": 1.0 if "funds" in types else 0.0,
                    "mean_grade": float(np.mean(grades)), "min_grade": float(min(grades)),
                    "n_evidence_types": len(set(types)), "temporal_clustering": 1.0,
                    "semantic_similarity": 1.0 if "uses_similar_language" in types else 0.0,
                    "amplification": 1.0 if "amplifies" in types else 0.0,
                    "cooccurrence": 1.0 if sum(t in {"co_occurs_with", "shares_link"} for t in types) >= 2 else 0.0,
                    "path_length": n_hops,
                }
                gated = score_components(features, weights, gated=True)["score"]
                ungated = score_components(features, weights, gated=False)["score"]
                candidate = {"types": types, "grades": grades, "features": features,
                             "gated": gated, "ungated": ungated}
                if best_gated is None or gated > best_gated["gated"]:
                    best_gated = candidate
                if best_ungated is None or ungated > best_ungated["ungated"]:
                    best_ungated = candidate
        if best_gated is None or best_ungated is None:
            raise ValueError("No edge-type sequence found for bound family %s" % family)
        eligibility = high_priority_eligibility(best_gated["features"])
        rows.append({
            "family": family, "constraint": constraint,
            "max_score_gated": round(best_gated["gated"], 2),
            "max_score_ungated": round(best_ungated["ungated"], 2),
            "edge_type_sequence_gated": " -> ".join(best_gated["types"]),
            "evidence_grade_sequence_gated": " -> ".join(str(g) for g in best_gated["grades"]),
            "edge_type_sequence_ungated": " -> ".join(best_ungated["types"]),
            "evidence_grade_sequence_ungated": " -> ".join(str(g) for g in best_ungated["grades"]),
            "triage_threshold": threshold,
            "score_threshold_crossed_gated": bool(best_gated["gated"] >= threshold),
            "score_threshold_crossed_ungated": bool(best_ungated["ungated"] >= threshold),
            "eligible_for_high_priority": bool(eligibility["eligible_for_high_priority"]),
            "high_priority_review_gated": bool(best_gated["gated"] >= threshold and eligibility["eligible_for_high_priority"]),
        })
    return pd.DataFrame(rows)


def threshold_sweep(cand_df: pd.DataFrame, step: int = 1,
                    score_col: str = "review_priority_score",
                    label_col: str = "ground_truth_label") -> pd.DataFrame:
    """Precision / recall / specificity / flag count at every candidate threshold."""
    rows = []
    for thr in range(0, 101, step):
        pred = (cand_df[score_col] >= thr).astype(int).tolist()
        m = binary_metrics(cand_df[label_col].tolist(), pred)
        rows.append({"threshold": thr, "n_flagged": int(sum(pred)),
                     "precision": m["precision"], "recall": m["recall"], "f1": m["f1"],
                     "specificity": m["specificity"],
                     "false_positive_rate": m["false_positive_rate"]})
    return pd.DataFrame(rows)


def _rank_correlations(baseline_scores: List[float], perturbed_scores: List[float]) -> Dict[str, float]:
    """Return full-ranking correlations with average-rank and tau-b tie handling.

    SciPy assigns average ranks for ties in Spearman correlation and Kendall's
    tau-b corrects for tied pairs. Identical constant vectors are defined as
    perfectly stable; non-identical vectors with a constant ranking receive 0.
    """
    base = np.asarray(baseline_scores, dtype=float)
    perturbed = np.asarray(perturbed_scores, dtype=float)
    if np.array_equal(base, perturbed):
        return {"spearman_rho": 1.0, "kendall_tau_b": 1.0}
    if np.ptp(base) == 0 or np.ptp(perturbed) == 0:
        return {"spearman_rho": 0.0, "kendall_tau_b": 0.0}
    rho = float(spearmanr(base, perturbed).statistic)
    tau = float(kendalltau(base, perturbed, variant="b").statistic)
    return {
        "spearman_rho": 0.0 if np.isnan(rho) else rho,
        "kendall_tau_b": 0.0 if np.isnan(tau) else tau,
    }

def weight_sensitivity(features_list: List[Dict[str, Any]], labels: List[int],
                       base_weights: ScoreWeights, threshold: float,
                       n_draws: int = 200, rel_range: float = 0.20,
                       seed: int = 4242) -> Dict[str, Any]:
    """Perturb every score weight by U(1-r, 1+r) and re-evaluate triage.

    Reports, per draw: recall, precision, and the Jaccard overlap between the
    perturbed flagged set and the baseline flagged set. A triage rule whose
    behaviour collapses under +/-20% weight changes would be over-tuned; stable
    behaviour shows the conclusions do not hinge on the exact weight values.
    """
    rng = np.random.default_rng(seed)
    base_scores = [score_components(f, base_weights)["score"] for f in features_list]
    base_flagged = {i for i, s in enumerate(base_scores) if s >= threshold}
    k = len(base_flagged)
    base_order = sorted(range(len(base_scores)), key=lambda i: -base_scores[i])
    base_topk = set(base_order[:k]) if k else set()
    weight_fields = ["w_funding_edge", "w_mean_grade", "w_min_grade", "w_evidence_types",
                     "w_temporal", "w_semantic", "w_amplification", "w_cooccurrence",
                     "length_penalty"]
    draws = []
    for d in range(n_draws):
        mult = {f_: float(rng.uniform(1 - rel_range, 1 + rel_range)) for f_ in weight_fields}
        kw = {f_: getattr(base_weights, f_) * mult[f_] for f_ in weight_fields}
        w = ScoreWeights(**kw)
        scores = [score_components(f, w)["score"] for f in features_list]
        flagged = {i for i, s in enumerate(scores) if s >= threshold}
        m = binary_metrics(labels, [1 if i in flagged else 0 for i in range(len(labels))])
        inter, union = len(flagged & base_flagged), len(flagged | base_flagged)
        rank_corr = _rank_correlations(base_scores, scores)
        # rank-based stability: a triage tool RANKS candidates, so the primary
        # stability question is whether the ordering survives perturbation.
        # (Threshold metrics are also reported, but an absolute cut-off is, by
        # construction, sensitive to a global rescaling of all weights.)
        order = sorted(range(len(scores)), key=lambda i: -scores[i])
        topk = set(order[:k]) if k else set()
        n_true = max(1, sum(labels))
        rank_recall = sum(1 for i in topk if labels[i] == 1) / n_true
        tk_inter, tk_union = len(topk & base_topk), len(topk | base_topk)
        draws.append({"draw": d, "recall": m["recall"], "precision": m["precision"],
                      "specificity": m["specificity"], "n_flagged": len(flagged),
                      "flagged_set_jaccard": round(inter / union, 4) if union else 1.0,
                      "rank_recall_topk": round(rank_recall, 4),
                      "topk_jaccard": round(tk_inter / tk_union, 4) if tk_union else 1.0,
                      "spearman_rho": round(rank_corr["spearman_rho"], 4),
                      "kendall_tau_b": round(rank_corr["kendall_tau_b"], 4)})
    df = pd.DataFrame(draws)
    summary = {
        "n_draws": n_draws, "rel_range": rel_range, "seed": seed,
        "top_k": k,
        "tie_handling": "Spearman average ranks; Kendall tau-b tie correction",
        "spearman_rho_min": round(float(df["spearman_rho"].min()), 4),
        "spearman_rho_median": round(float(df["spearman_rho"].median()), 4),
        "kendall_tau_b_min": round(float(df["kendall_tau_b"].min()), 4),
        "kendall_tau_b_median": round(float(df["kendall_tau_b"].median()), 4),
        "rank_recall_topk_min": round(float(df["rank_recall_topk"].min()), 4),
        "rank_recall_topk_median": round(float(df["rank_recall_topk"].median()), 4),
        "topk_jaccard_min": round(float(df["topk_jaccard"].min()), 4),
        "topk_jaccard_median": round(float(df["topk_jaccard"].median()), 4),
        "recall_min": round(float(df["recall"].min()), 4),
        "recall_median": round(float(df["recall"].median()), 4),
        "precision_min": round(float(df["precision"].min()), 4),
        "precision_median": round(float(df["precision"].median()), 4),
        "specificity_min": round(float(df["specificity"].min()), 4),
        "flagged_set_jaccard_min": round(float(df["flagged_set_jaccard"].min()), 4),
        "flagged_set_jaccard_median": round(float(df["flagged_set_jaccard"].median()), 4),
        "pct_draws_recall_1": round(float((df["recall"] == 1.0).mean()), 4),
        "pct_draws_rank_recall_1": round(float((df["rank_recall_topk"] == 1.0).mean()), 4),
    }
    return {"draws": df, "summary": summary}


def formula_table(weights: ScoreWeights, threshold: float) -> pd.DataFrame:
    """Machine-written copy of the exact score formula (single source of truth)."""
    w = weights
    rows = [
        ("funding_edge", "w_fund * funding_edge", w.w_funding_edge,
         "1 if the path contains a direct synthetic funding edge (grade 4), else 0",
         "binary {0,1}", "primary - a documentary funding origin is the strongest single proxy indicator"),
        ("mean_grade", "w_mean * (mean_grade / 4)", w.w_mean_grade,
         "mean synthetic evidence grade across the hops on the path", "/4 (grades 0..4)",
         "primary - overall documentary strength of the chain"),
        ("min_grade", "w_min * (min_grade / 4)", w.w_min_grade,
         "weakest (minimum) evidence grade on the path - documentary continuity",
         "/4 (grades 0..4)", "primary - penalises chains that drop to a weak hop"),
        ("evidence_types", "w_types * (n_evidence_types / 5)", w.w_evidence_types,
         "number of distinct relationship types along the path", "/5",
         "secondary - diversity of independent evidence"),
        ("temporal_clustering", "w_temp * temporal_clustering", w.w_temporal,
         "fraction of hops sharing the modal campaign phase", "[0,1]",
         "secondary - temporal coherence of the chain"),
        ("semantic_similarity", "support * w_sem * semantic", w.w_semantic,
         "1 if a similar-language hop is present, else 0", "binary, gated by support",
         "supporting only - cannot raise priority without documentary support"),
        ("amplification", "support * w_amp * amplification", w.w_amplification,
         "1 if an amplification hop is present, else 0", "binary, gated by support",
         "supporting only - cannot raise priority without documentary support"),
        ("cooccurrence", "support * w_cooc * cooccurrence", w.w_cooccurrence,
         "1 if >= 2 weak co-occurrence / shared-link hops are present, else 0",
         "binary, gated by support", "supporting only - repeated weak co-presence"),
        ("length_penalty", "- pen * max(0, path_length - 3)", w.length_penalty,
         "gentle penalty per hop beyond three", "per extra hop",
         "control - long chains accumulate uncertainty"),
        ("support_factor", "support = min_grade / 4", float("nan"),
         "gate multiplying every supporting signal", "/4 (grades 0..4)",
         "gate - weak-signal-only chains receive almost no supporting contribution"),
        ("triage_threshold", "flag if score >= threshold", threshold,
         "transparent review cut-off", "score in [0,100]",
         "decision boundary - flags are queue entries for expert review, not conclusions"),
    ]
    return pd.DataFrame(rows, columns=["component", "term", "weight", "description",
                                       "normalisation", "role"])
