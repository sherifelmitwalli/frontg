#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_benchmark_B.py
===================

Self-checks for Benchmark B, the comparators, and the entity-resolution
challenge set. Plain asserts, no pytest required:

    python test_benchmark_B.py

Runs a reduced ("quick") benchmark in a temporary folder. Synthetic data only.
"""
from __future__ import annotations

import tempfile
from pathlib import Path

import numpy as np
import pandas as pd

import frontg_er_challenge as ER
import frontg_metrics as MET
import frontg_v2_methods as M
import run_v2_benchmark as RB
from frontg_config import ScoreWeights, TRIAGE_THRESHOLD
from frontg_v2_generator import REGIMES, generate_instance

BANNED = ["philip morris", "british american", "japan tobacco", "imperial brands", "marlboro",
          "university of bath", "who fctc", "http://", "https://", "google", "nestle", "coca"]
PASSED, FAILED = [], []


def check(name, cond):
    (PASSED if cond else FAILED).append(name)
    print(("PASS " if cond else "FAIL ") + name)


def main():
    # 1. exact bounds: the eligibility rule is non-binding at the published weights
    b = MET.attainable_score_bounds(ScoreWeights(), TRIAGE_THRESHOLD).set_index("family")
    check("bounds: every ineligible path scores below the threshold (gated)",
          float(b.loc["ineligible_any", "max_score_gated"]) < TRIAGE_THRESHOLD)
    check("bounds: no-funding paths cannot reach the threshold even ungated",
          float(b.loc["no_funding_any_grade", "max_score_ungated"]) < TRIAGE_THRESHOLD)

    # 2. generator determinism and neutrality
    a = M.extract_candidates(REGIMES["base"], 123)
    a2 = M.extract_candidates(REGIMES["base"], 123)
    check("v2 reproducibility: identical candidate tables for a fixed seed",
          a.drop(columns=[]).equals(a2))
    gen = generate_instance(REGIMES["hub_background"], 7)
    txt = " ".join(gen.nodes).lower() + " " + " ".join(e.evidence_snippet for e in gen.edges).lower()
    check("v2: no real-world names in node ids or snippets", not any(t in txt for t in BANNED))
    check("v2: node ids do not encode role (no 'decoy'/'true'/'bystander' tokens)",
          not any(t in " ".join(gen.nodes).lower() for t in ("decoy", "true", "bystander", "control", "weak")))
    check("v2: planted pathways all enumerated as candidates",
          int(a["ground_truth_label"].sum()) == a.attrs["n_planted"])

    # 3. quick end-to-end run
    with tempfile.TemporaryDirectory() as td:
        res = RB.run(quick=True, out=Path(td))
        inst = res["instances"]
        f = inst[inst["method"] == "frontg"]
        check("FrontG: zero flags containing a grade <=1 hop (all regimes)", int(f["n_low_floor_flags"].sum()) == 0)
        check("FrontG: zero weak-evidence-only flags (all regimes)", int(f["n_weak_evidence_flags"].sum()) == 0)
        check("FrontG: zero grade-1-attached bystander flags (all regimes)", int(f["n_bystander_g1_flags"].sum()) == 0)
        ne = inst[inst["method"] == "frontg_no_elig"].reset_index(drop=True)
        check("eligibility rule non-binding: FrontG and FrontG-without-eligibility flag identically",
              (f.reset_index(drop=True)[["tp", "fp"]].values == ne[["tp", "fp"]].values).all())
        ge = inst[inst["method"] == "gbm_elig"]
        check("eligibility wrapper: learned ranker inherits zero low-floor flags",
              int(ge["n_low_floor_flags"].sum()) == 0 and int(ge["n_weak_evidence_flags"].sum()) == 0)
        check("all methods evaluated in all regimes",
              inst.groupby("regime")["method"].nunique().min() == len(M.METHOD_ORDER))
        d = res["diagnostic"]
        dA = d[d["benchmark"].str.startswith("A")]
        check("diagnostic: Benchmark A answer key is learnable from templates (AUPRC = 1)",
              bool((dA["auprc"] >= 0.999).all()))
        dB = d[(d["benchmark"].str.startswith("B")) & (~d["model"].str.contains("topology"))]
        check("diagnostic: Benchmark B is not trivially learnable (AUPRC < 0.9)", bool((dB["auprc"] < 0.9).all()))
        for fn in ["instance_metrics.csv", "summary_by_regime_method.csv", "diagnostic_learnability.csv",
                   "separability_summary.csv", "er_challenge_overall.csv", "thresholds.json", "regimes.csv"]:
            check(f"output written: {fn}", (Path(td) / fn).exists())

    # 4. entity-resolution challenge set
    er = ER.evaluate(out=Path(tempfile.mkdtemp()))
    ov = er["overall"].set_index("rule")
    bc = er["by_category"].set_index(["rule", "category"])
    check("ER challenge: published v1 rule false-merges sibling-qualifier pairs (documented failure)",
          bc.loc[("token_jaccard_v1", "sibling_qualifier"), "auto_merge"] > 0)
    check("ER challenge: all calibrated rules have zero false merges on the held-out set",
          int(ov.drop(index="token_jaccard_v1")["false_merges"].sum()) == 0)
    check("ER challenge: acronym referral never auto-merges an acronym pair",
          bc.loc[("normalised_token_acronym", "acronym"), "auto_merge"] == 0
          and bc.loc[("normalised_token_acronym", "shared_acronym"), "auto_merge"] == 0)
    names = " ".join(er["test_pairs"]["name_a"]).lower() + " ".join(er["test_pairs"]["name_b"]).lower()
    check("ER challenge: no real-world names", not any(t in names for t in BANNED))

    print(f"\n{len(PASSED)} passed, {len(FAILED)} failed.")
    if FAILED:
        raise SystemExit(1)
    print("All Benchmark-B self-checks passed. Synthetic data only.")


if __name__ == "__main__":
    main()
