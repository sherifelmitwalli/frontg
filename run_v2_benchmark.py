#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_v2_benchmark.py
===================

Runs Benchmark B (stochastic latent-truth benchmark) and the Benchmark-A
learnability diagnostic. Synthetic data only; no network access.

    python run_v2_benchmark.py                 # full run (default sizes)
    python run_v2_benchmark.py --quick         # small smoke run used by the tests

Outputs (folder ``benchmark_B/``):
  instance_metrics.csv          one row per (regime, test instance, method)
  summary_by_regime_method.csv  means with 95% bootstrap CIs + pooled safety counts
  thresholds.json               tuned thresholds for the non-FrontG decision rules
  diagnostic_learnability.csv   template-learnability diagnostic (Benchmark A vs B)
  regimes.csv                   the generator parameters of every regime
"""
from __future__ import annotations

import argparse
import dataclasses
import json
import time
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import average_precision_score

import frontg_v2_methods as M
import generate_synthetic_graph as G1
from frontg_config import SCENARIOS
from frontg_v2_generator import REGIMES, REGIME_ORDER, SEPARABILITY_LAMBDAS, separability_regime

OUT = Path(__file__).resolve().parent / "benchmark_B"

SEEDS = {
    "train": range(10000, 10100),
    "valid": range(15000, 15050),
    "test": range(20000, 20100),
    "oracle_train": range(30000, 30100),
    "oracle_valid": range(35000, 35050),
}
QUICK = {k: range(v.start, v.start + (6 if "valid" not in k else 4)) for k, v in SEEDS.items()}

SUMMARY_METRICS = ["precision", "recall", "f1", "auprc", "n_flagged"]
POOLED = ["n_weak_evidence_flags", "n_weak_evidence_false_flags", "n_low_floor_flags",
          "n_bystander_g1_paths", "n_bystander_g1_flags", "n_bystander_g2_paths",
          "n_bystander_g2_flags", "n_bystander_g3_paths", "n_bystander_g3_flags",
          "n_true_funding_observed", "tp_funding_observed", "n_true_funding_hidden",
          "tp_funding_hidden", "tp", "fp", "n_planted"]


def summarise(inst: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for (reg, meth), g in inst.groupby(["regime", "method"], sort=False):
        row = {"regime": reg, "method": meth, "method_label": M.METHOD_LABELS[meth],
               "n_instances": len(g), "mean_candidates": round(g["n_candidates"].mean(), 1),
               "mean_prevalence": round(g["prevalence"].mean(), 4)}
        for m in SUMMARY_METRICS:
            est, lo, hi = M.bootstrap_ci(g[m].values)
            row[f"{m}_mean"], row[f"{m}_lo"], row[f"{m}_hi"] = (round(est, 4), round(lo, 4), round(hi, 4))
        for c in POOLED:
            row[c] = int(g[c].sum())
        for st in (1, 2, 3):
            n = row[f"n_bystander_g{st}_paths"]
            row[f"bystander_g{st}_flag_rate"] = round(row[f"n_bystander_g{st}_flags"] / n, 4) if n else np.nan
        for name in ("funding_observed", "funding_hidden"):
            n = row[f"n_true_{name}"]
            row[f"recall_{name}"] = round(row[f"tp_{name}"] / n, 4) if n else np.nan
        row["pooled_precision"] = round(row["tp"] / max(1, row["tp"] + row["fp"]), 4)
        row["pooled_recall"] = round(row["tp"] / max(1, row["n_planted"]), 4)
        rows.append(row)
    return pd.DataFrame(rows)


def ambiguity_rate(df: pd.DataFrame, cols) -> float:
    """Share of candidates whose feature vector also occurs with the opposite label."""
    key = df[cols].round(6).astype(str).agg("|".join, axis=1)
    mix = df.groupby(key)["ground_truth_label"].agg(lambda s: 0 < s.mean() < 1)
    return round(float(key.map(mix).mean()), 4)


def diagnostic(test_base: pd.DataFrame, oracle_train: pd.DataFrame) -> pd.DataFrame:
    """Template-learnability diagnostic: can a learner reproduce each answer key?"""
    rows = []
    # Benchmark A: leave-one-scenario-out over the three fixed-template scenarios
    A = {}
    for k in ("small", "medium", "stress"):
        r = G1.compute_scenario(SCENARIOS[k], robustness=False)
        d = pd.DataFrame(r.features_list)[M.PATH_FEATURES].copy()
        d["ground_truth_label"] = r.cand_df["ground_truth_label"].values
        d["frontg_high_priority"] = r.cand_df["high_priority_review"].values
        A[k] = d
    for tr, te in [("medium", "stress"), ("stress", "medium"), ("medium", "small"), ("stress", "small")]:
        gb = M._gbm().fit(A[tr][M.PATH_FEATURES].values, A[tr]["ground_truth_label"].values)
        p = gb.predict_proba(A[te][M.PATH_FEATURES].values)[:, 1]
        y = A[te]["ground_truth_label"].values
        pred = p >= 0.5
        tp = int(np.sum(pred & (y == 1)))
        fy = A[te]["frontg_high_priority"].values.astype(bool)
        rows.append({"benchmark": "A (fixed templates)", "train": tr, "test": te,
                     "prevalence": round(float(y.mean()), 4),
                     "model": "gradient boosting (path features)",
                     "auprc": round(float(average_precision_score(y, p)), 4),
                     "precision_at_0.5": round(tp / max(1, pred.sum()), 4),
                     "recall_at_0.5": round(tp / max(1, y.sum()), 4),
                     "frontg_precision": round(int(np.sum(fy & (y == 1))) / max(1, fy.sum()), 4),
                     "frontg_recall": round(int(np.sum(fy & (y == 1))) / max(1, y.sum()), 4),
                     "feature_ambiguity_rate": ambiguity_rate(A[te], M.PATH_FEATURES)})
    # Benchmark B (base regime): train on independent instances, test on held-out instances
    gb = M._gbm().fit(oracle_train[M.PATH_FEATURES].values, oracle_train["ground_truth_label"].values)
    p = gb.predict_proba(test_base[M.PATH_FEATURES].values)[:, 1]
    y = test_base["ground_truth_label"].values
    pred = p >= 0.5
    tp = int(np.sum(pred & (y == 1)))
    fy = ((test_base["review_priority_score"] >= 60) & (test_base["eligible"] == 1)).values
    rows.append({"benchmark": "B (latent truth, base regime)", "train": "base train instances",
                 "test": "base test instances (pooled)", "model": "gradient boosting (path features)",
                 "auprc": round(float(average_precision_score(y, p)), 4),
                 "precision_at_0.5": round(tp / max(1, pred.sum()), 4),
                 "recall_at_0.5": round(tp / max(1, y.sum()), 4),
                 "frontg_precision": round(int(np.sum(fy & (y == 1))) / max(1, fy.sum()), 4),
                 "frontg_recall": round(int(np.sum(fy & (y == 1))) / max(1, y.sum()), 4),
                 "feature_ambiguity_rate": ambiguity_rate(test_base, M.PATH_FEATURES)})
    # Structural-leakage probe: a learner given topology only (no evidence features)
    # should be close to the prevalence baseline if the generator does not leak labels.
    gs = M._gbm().fit(oracle_train[M.STRUCT_ONLY].values, oracle_train["ground_truth_label"].values)
    ps = gs.predict_proba(test_base[M.STRUCT_ONLY].values)[:, 1]
    rows.append({"benchmark": "B (latent truth, base regime)", "train": "base train instances",
                 "test": "base test instances (pooled)",
                 "model": "gradient boosting (topology-only leakage probe)",
                 "auprc": round(float(average_precision_score(y, ps)), 4),
                 "precision_at_0.5": np.nan, "recall_at_0.5": np.nan,
                 "frontg_precision": np.nan, "frontg_recall": np.nan,
                 "feature_ambiguity_rate": ambiguity_rate(test_base, M.STRUCT_ONLY)})
    rows[-2]["prevalence"] = rows[-1]["prevalence"] = round(float(y.mean()), 4)
    return pd.DataFrame(rows)


SWEEP_METHODS = ["frontg", "frontg_no_elig_no_gate", "mean_grade", "logreg_path", "logreg", "gbm", "gbm_elig"]


def separability_sweep(seeds, out: Path) -> pd.DataFrame:
    """Train, tune, and test within each separability level (in-distribution)."""
    rows = []
    for lam in SEPARABILITY_LAMBDAS:
        reg = separability_regime(lam)
        train = M.build_pool(reg, seeds["train"])
        valid = M.build_pool(reg, seeds["valid"])
        fitted = M.fit_methods(train, valid)
        for sd in seeds["test"]:
            df = M.extract_candidates(reg, sd)
            if df.empty:
                continue
            sc = {k: v for k, v in M.method_scores(df, fitted).items() if k in SWEEP_METHODS}
            for r in M.evaluate_instance(df, sc):
                r["lambda"] = lam
                rows.append(r)
        print(f"[separability] lambda={lam:.2f} done")
    inst = pd.DataFrame(rows)
    inst.to_csv(out / "separability_instances.csv", index=False)
    summ = summarise(inst)
    summ.insert(0, "lambda", [float(r.split("_")[1]) for r in summ["regime"]])
    summ.to_csv(out / "separability_summary.csv", index=False)
    return summ


def run(quick: bool = False, out: Path = OUT) -> dict:
    seeds = QUICK if quick else SEEDS
    out.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    base = REGIMES["base"]
    train = M.build_pool(base, seeds["train"])
    valid = M.build_pool(base, seeds["valid"])
    fitted = M.fit_methods(train, valid)
    inst_rows, test_pools = [], {}
    for name in REGIME_ORDER:
        reg = REGIMES[name]
        o_train = M.build_pool(reg, seeds["oracle_train"])
        o_valid = M.build_pool(reg, seeds["oracle_valid"])
        oracle = M.fit_oracle(o_train, o_valid)
        frames = []
        for sd in seeds["test"]:
            df = M.extract_candidates(reg, sd)
            if df.empty:
                continue
            frames.append(df)
            inst_rows += M.evaluate_instance(df, M.method_scores(df, fitted, oracle))
        test_pools[name] = pd.concat(frames, ignore_index=True)
        if name == "base":
            base_oracle_train = o_train
        print(f"[benchmark B] regime={name} instances={len(frames)} "
              f"mean candidates={np.mean([len(f) for f in frames]):.1f} ({time.time() - t0:.0f}s)")
    inst = pd.DataFrame(inst_rows)
    inst["method"] = pd.Categorical(inst["method"], categories=M.METHOD_ORDER, ordered=True)
    inst = inst.sort_values(["regime", "method", "seed"], key=lambda c: c.map(
        {r: i for i, r in enumerate(REGIME_ORDER)}) if c.name == "regime" else c, kind="stable")
    inst["method"] = inst["method"].astype(str)
    inst.to_csv(out / "instance_metrics.csv", index=False)
    summ = summarise(inst)
    summ.to_csv(out / "summary_by_regime_method.csv", index=False)
    diag = diagnostic(test_pools["base"], base_oracle_train)
    diag.to_csv(out / "diagnostic_learnability.csv", index=False)
    pd.DataFrame([dataclasses.asdict(REGIMES[n]) for n in REGIME_ORDER]).to_csv(out / "regimes.csv", index=False)
    meta = {"thresholds": {k: round(float(v), 10) for k, v in fitted["thresholds"].items()}, "seeds": {k: [v.start, v.stop - 1] for k, v in seeds.items()},
            "n_train_candidates": int(len(train)), "n_valid_candidates": int(len(valid)),
            "train_prevalence": round(float(train["ground_truth_label"].mean()), 4),
            "learned_features": M.LEARNED_FEATURES, "quick": quick}
    (out / "thresholds.json").write_text(json.dumps(meta, indent=2))
    sweep = separability_sweep(seeds, out)
    import frontg_er_challenge as ER
    er = ER.evaluate(out=out)
    print(f"[benchmark B] done in {time.time() - t0:.0f}s -> {out}")
    return {"instances": inst, "summary": summ, "diagnostic": diag, "meta": meta, "pools": test_pools,
            "sweep": sweep, "er": er}


def main(argv=None):
    ap = argparse.ArgumentParser(description="Benchmark B (synthetic data only).")
    ap.add_argument("--quick", action="store_true", help="small smoke run")
    ap.add_argument("--output-dir", default=str(OUT))
    a = ap.parse_args(argv)
    run(quick=a.quick, out=Path(a.output_dir))


if __name__ == "__main__":
    main()
