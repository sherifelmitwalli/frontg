#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_synthetic_harness.py
=========================

Lightweight self-checks for the synthetic validation harness. Runs with plain
asserts (no pytest required):

    python test_synthetic_harness.py

Checks: output generation; fixed-seed reproducibility; absence of real-world
entity names; isolated AND embedded negative controls below threshold; three-zone
entity resolution (no false friend auto-merged; referred aliases recoverable);
ground-truth paths recovered; weak-signal chains never flagged (gated and
ungated, plus the analytic bound); weight-perturbation stability; and all
validation outputs written.
"""
from __future__ import annotations

import json
import tempfile
from pathlib import Path

import generate_synthetic_graph as G
from frontg_config import SCENARIOS, TRIAGE_THRESHOLD

# A small blocklist of real-world tokens that must never appear in synthetic ids.
BANNED = ["brave", "serper", "google", "consensus", "semantic scholar",
          "philip morris", "british american", "gilmore", "university of bath",
          "nestle", "coca", "pepsi", "marlboro", "http://", "https://", "api_key"]
PASSED, FAILED = [], []


def check(name, cond):
    (PASSED if cond else FAILED).append(name)
    print(("PASS " if cond else "FAIL ") + name)


def main():
    spec = SCENARIOS["small"]

    # 1. fixed-seed reproducibility (metrics + candidate scores identical)
    r1 = G.compute_scenario(spec)
    r2 = G.compute_scenario(spec)
    check("reproducibility: metrics identical", r1.metrics == r2.metrics)
    check("reproducibility: candidate scores identical",
          r1.cand_df["review_priority_score"].tolist() == r2.cand_df["review_priority_score"].tolist())

    # 2. no real-world entity names anywhere in the graph
    text = " ".join(list(r1.G.nodes())).lower()
    text += " " + " ".join(d.get("evidence_snippet", "") for *_e, d in r1.G.edges(data=True)).lower()
    check("no real-world entity names present", not any(b in text for b in BANNED))

    # 3. negative controls remain below threshold (isolated AND embedded)
    check("isolated negative controls below threshold",
          bool(r1.metrics["rq3_negative_controls"]["all_controls_below_threshold"]))
    check("embedded controls present and funder-reachable",
          r1.metrics["rq3_negative_controls"]["n_embedded_control_candidates"] >= 1)
    check("embedded-control candidate paths never flagged",
          bool(r1.metrics["rq3_negative_controls"]["all_embedded_below_threshold"]))

    # 4. three-zone entity resolution: never auto-merge a false friend;
    #    referred true-alias pairs define an assumed perfect-adjudication upper bound
    check("no false friend auto-merged (ER auto precision == 1.0)",
          r1.metrics["rq2_entity_resolution"]["entity_resolution_precision"] == 1.0)
    check("zero false merges",
          r1.metrics["rq2_entity_resolution"]["n_false_merges"] == 0)
    check("potential ER recall under perfect adjudication == 1.0",
          r1.metrics["rq2_entity_resolution"]["potential_recall_if_all_referred_true_aliases_are_correctly_confirmed"] == 1.0)
    check("human adjudication recall is not observed",
          r1.metrics["rq2_entity_resolution"]["observed_human_adjudication_recall"] is None)

    # 5. ground-truth paths present in the answer key and recovered
    check("ground-truth paths present", len(r1.gen.ground_truth_paths) >= 1)
    check("ground-truth paths recovered (recall == 1.0)",
          r1.metrics["rq1_path_recovery"]["path_recovery_recall"] == 1.0)

    # 5b. RQ5 robustness: weak-signal-only chains can never be flagged,
    #     with or without the support gate
    r5 = r1.metrics["rq5_robustness"]
    check("weak-signal chains seeded and enumerated",
          r5["n_weak_chain_candidates"] >= 1)
    check("weak-signal chains never enter high-priority review",
          r5["n_weak_chain_high_priority_review"] == 0)
    check("weak-signal chains never flagged (gate removed)",
          r5["n_weak_chain_flagged_ungated"] == 0)
    check("analytic bound: weak-signal-only score cannot reach threshold even ungated",
          not r5["weak_signal_only_raw_can_reach_threshold"])
    check("weight sensitivity: top-k ranking stable under +/-20% perturbation",
          r5["weight_sensitivity"]["rank_recall_topk_min"] >= 0.99)

    ws = r5["weight_sensitivity"]
    check("full-ranking Spearman correlations are reported", -1.0 <= ws["spearman_rho_min"] <= 1.0)
    check("full-ranking Kendall tau-b correlations are reported", -1.0 <= ws["kendall_tau_b_min"] <= 1.0)

    # 5c. Connected active-network noise creates real alternative candidates.
    medium = G.compute_scenario(SCENARIOS["medium"])
    active = medium.metrics["active_noise_validation"]

    # 5c-bis. Audit-trail claim correctness: recommended actions must reflect the
    # actual weakest-hop grade, and audit scores must stay numeric (NaN-safe).
    from frontg_audit import build_audit_tables
    pa, _ta, _ea, _na = build_audit_tables(medium)
    fp_rows = pa[pa["classification"] == "false_positive"]
    def _min_grade(g):
        return min(int(x) for x in str(g).split("->")) if str(g).strip() else 0
    wording_ok = all(
        ("documentary-grade" in r["recommended_action"]
         and "low grade" not in r["recommended_action"])
        if _min_grade(r["evidence_grades"]) >= 3
        else "low grade" in r["recommended_action"]
        for _, r in fp_rows.iterrows())
    check("false-positive actions reflect actual weakest-hop grade", wording_ok)
    import pandas as _pd
    check("path-audit scores are numeric (false negatives NaN-safe)",
          _pd.api.types.is_numeric_dtype(pa["review_priority_score"]))
    check("connected active-noise edges are present", active["n_active_noise_edges"] > 0)
    check("active noise increases candidate-path enumeration",
          active["candidate_paths_after_active_noise"] > active["candidate_paths_before_active_noise"])
    check("active-noise candidates are enumerated", active["n_candidate_paths_using_active_noise"] > 0)
    check("active-noise false positives are retained", active["n_high_priority_active_noise_false_positives"] > 0)
    check("reported scenarios do not hit the candidate cap", not active["candidate_cap_reached"])

    # 5d. Claim-correctness checks for the integer sweep and safety gate
    thresholds = r1.sweep_df["threshold"].tolist()
    check("threshold sweep contains every integer 0..100",
          len(thresholds) == 101 and thresholds == list(range(101)))
    grade1_bound = r1.bounds_df[r1.bounds_df["family"] == "funding_with_grade1_floor"].iloc[0]
    check("grade-1-floor path cannot enter high-priority review",
          bool(grade1_bound["score_threshold_crossed_ungated"])
          and not bool(grade1_bound["high_priority_review_gated"]))
    check("exact bounds include edge-type witness sequences",
          bool(grade1_bound["edge_type_sequence_gated"])
          and bool(grade1_bound["evidence_grade_sequence_gated"]))

    # 6. outputs are generated and metrics written
    with tempfile.TemporaryDirectory() as td:
        base = Path(td)
        G.run_scenario(spec, base, make_figures=False)
        out = base / spec.folder
        expected = ["synthetic_network.graphml", "synthetic_network.json",
                    "ground_truth_paths.csv", "ground_truth_entity_resolution.csv",
                    "negative_control_subgraphs.csv", "candidate_paths.csv",
                    "entity_resolution_decisions.csv", "path_recovery_audit.csv",
                    "triage_score_audit.csv", "validation_metrics.csv",
                    "validation_metrics.json", "validation_tracking_report.md",
                    "validation_tracking_report.html", "weak_signal_chains.csv",
                    "score_bounds.csv", "threshold_sweep.csv",
                    "sensitivity_analysis.csv", "review_priority_formula.csv"]
        missing = [f for f in expected if not (out / f).exists()]
        check("all core outputs generated", not missing)
        mj = json.loads((out / "validation_metrics.json").read_text())
        check("validation metrics written", "rq1_path_recovery" in mj)

    print("\n%d passed, %d failed." % (len(PASSED), len(FAILED)))
    if FAILED:
        raise SystemExit("FAILED: " + ", ".join(FAILED))
    print("All synthetic-harness self-checks passed. Synthetic data only.")


if __name__ == "__main__":
    main()
