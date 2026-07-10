#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
frontg_audit.py
===============

Builds the enriched, human-readable audit trail for one scenario:
  * path-recovery audit (per candidate path, with edge provenance, evidence
    snippets, classification, plain-language reason and a recommended action);
  * triage-score audit (per-term decomposition of every review-priority score,
    including the ungated ablation score and the gate contribution);
  * entity-resolution audit (three-zone decisions for every relevant pair);
  * negative-control audit (each isolated/embedded control with its outcome).

Every table is built from the synthetic ground truth only. All scores are triage
indicators for expert human review - never proof of wrongdoing.
"""
from __future__ import annotations

from typing import Dict, List, Tuple, Any

import pandas as pd

from frontg_config import TRIAGE_THRESHOLD


def _seq_to_nodes(seq: str) -> List[str]:
    return [s.strip() for s in seq.split("->")]


def _path_edges(G, nodes: List[str]) -> List[Dict[str, Any]]:
    """Highest-grade edge per hop, with provenance flags."""
    out = []
    for s, t in zip(nodes[:-1], nodes[1:]):
        best = None
        for _k, d in G.get_edge_data(s, t, default={}).items():
            if best is None or d["evidence_grade"] > best["evidence_grade"]:
                best = d
        if best is not None:
            if best.get("is_negative_control"):
                prov = "negative-control"
            elif best.get("is_ground_truth"):
                prov = "ground-truth"
            elif best.get("is_distractor"):
                prov = "distractor"
            else:
                prov = "background"
            out.append({"source": s, "target": t, "edge_type": best["edge_type"],
                        "grade": best["evidence_grade"], "snippet": best["evidence_snippet"],
                        "provenance": prov})
    return out


def _explain(feats: Dict[str, Any], score: float, high_priority_review: bool,
             score_threshold_crossed: bool, eligible: bool, ineligible_reason: str,
             is_weak_chain: bool = False, touches_embedded: bool = False) -> str:
    """Explain raw-score and high-priority decisions without conflating them."""
    bits = []
    bits.append("includes a direct synthetic funding edge (grade 4)"
                if feats.get("has_funding_edge") else "no direct funding edge")
    mn = int(feats["min_grade"])
    bits.append("weakest hop grade %d, mean grade %.2f" % (mn, feats["mean_grade"]))
    if mn >= 3:
        bits.append("documentary continuity maintained across all hops")
    elif mn == 2:
        bits.append("drops to a grade-2 shared-link/amplification hop")
    else:
        bits.append("drops to a grade-0/1 hop and is ineligible for high-priority review")
    if is_weak_chain:
        bits.append("weak-signal-only chain (RQ5): no documentary hop anywhere")
    if touches_embedded:
        bits.append("passes through an embedded control actor connected only by weak co-occurrence")
    if high_priority_review:
        head = "HIGH-PRIORITY REVIEW (raw score %.2f >= threshold %.1f and eligible)" % (score, TRIAGE_THRESHOLD)
    elif score_threshold_crossed:
        head = "not high priority: raw score %.2f reaches threshold %.1f but is ineligible (%s)" % (
            score, TRIAGE_THRESHOLD, ineligible_reason or "eligibility rule")
    else:
        head = "not high priority: raw score %.2f is below threshold %.1f" % (score, TRIAGE_THRESHOLD)
    return head + ": " + "; ".join(bits) + "."


def _action(cls: str, min_grade: int) -> str:
    if cls == "true_positive":
        return ("Prioritise for expert review: inspect the underlying synthetic records and "
                "confirm each link independently before drawing any inference.")
    if cls == "false_positive":
        if min_grade >= 3:
            return ("Queue for expert review; every hop carries documentary-grade evidence, so "
                    "this false lead is not separable from a true pathway on grades alone and "
                    "requires full manual verification of each underlying record.")
        return ("Queue for expert review as a possible lead only; the weakest hop is low grade "
                "(grade %d), so it may be set aside on inspection of that hop." % min_grade)
    if cls == "false_negative":
        return ("Review the threshold and seeded structure: a known path scored below the cut-off.")
    return "No review action required; retain in the audit log for completeness."


def build_audit_tables(res) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    G, scorer, cand_df = res.G, res.scorer, res.cand_df
    seeded = {p["node_sequence"]: p["path_id"] for p in res.gen.ground_truth_paths}
    seeded_set = set(seeded)

    path_rows, score_rows = [], []
    for _, row in cand_df.iterrows():
        nodes = _seq_to_nodes(row["node_sequence"])
        feats = scorer.features(nodes)
        _, _, comps = scorer.score(nodes)
        score = float(row["review_priority_score"])
        flagged = bool(row["high_priority_review"])
        score_threshold_crossed = bool(row["score_threshold_crossed"])
        eligible = bool(row["eligible_for_high_priority"])
        ineligible_reason = str(row.get("ineligible_reason", ""))
        is_seeded = row["node_sequence"] in seeded_set
        if flagged and is_seeded:
            cls = "true_positive"
        elif flagged and not is_seeded:
            cls = "false_positive"
        elif not flagged and is_seeded:
            cls = "false_negative"
        else:
            cls = "true_negative"
        edges = _path_edges(G, nodes)
        is_wc = bool(row.get("is_weak_chain", 0))
        is_emb = bool(row.get("touches_embedded_control", 0))
        score_ungated = float(row.get("score_ungated_ablation", score))
        path_rows.append({
            "id": seeded.get(row["node_sequence"], row["candidate_id"]),
            "candidate_id": row["candidate_id"],
            "node_sequence": row["node_sequence"],
            "edge_sequence": " -> ".join(e["edge_type"] for e in edges),
            "evidence_grades": " -> ".join(str(e["grade"]) for e in edges),
            "edge_provenance": " -> ".join(e["provenance"] for e in edges),
            "evidence_snippets": " || ".join(e["snippet"] for e in edges),
            "review_priority_score": score, "triage_threshold": TRIAGE_THRESHOLD,
            "score_threshold_crossed": int(score_threshold_crossed),
            "eligible_for_high_priority": int(eligible),
            "eligibility_rule_version": row["eligibility_rule_version"],
            "ineligible_reason": ineligible_reason,
            "high_priority_review": int(flagged),
            "flagged": int(flagged), "ground_truth_label": int(is_seeded),
            "is_weak_chain": int(is_wc), "touches_embedded_control": int(is_emb),
            "classification": cls,
            "explanation": _explain(feats, score, flagged, score_threshold_crossed, eligible,
                                    ineligible_reason, is_wc, is_emb),
            "recommended_action": _action(cls, int(feats["min_grade"]))})
        score_rows.append({
            "candidate_id": row["candidate_id"], "node_sequence": row["node_sequence"],
            "has_funding_edge": int(feats["has_funding_edge"]),
            "mean_grade": round(feats["mean_grade"], 3), "min_grade": int(feats["min_grade"]),
            "n_evidence_types": feats["n_evidence_types"],
            "temporal_clustering": feats["temporal_clustering"],
            "semantic_similarity": int(feats["semantic_similarity"]),
            "amplification": int(feats["amplification"]), "cooccurrence": int(feats["cooccurrence"]),
            "support_factor": comps["support_factor"], "term_funding": comps["term_funding"],
            "term_mean_grade": comps["term_mean_grade"], "term_min_grade": comps["term_min_grade"],
            "term_evidence_types": comps["term_evidence_types"], "term_temporal": comps["term_temporal"],
            "term_supporting": comps["term_supporting"], "penalty_length": comps["penalty_length"],
            "raw_score": comps["raw_score"], "final_score": comps["score"],
            "score_ungated_ablation": round(score_ungated, 2),
            "gate_contribution": round(score_ungated - comps["score"], 2),
            "triage_threshold": TRIAGE_THRESHOLD,
            "score_threshold_crossed": int(score_threshold_crossed),
            "eligible_for_high_priority": int(eligible),
            "eligibility_rule_version": row["eligibility_rule_version"],
            "ineligible_reason": ineligible_reason,
            "high_priority_review": int(flagged), "flagged": int(flagged)})

    # missed seeded paths not enumerated as candidates
    enumerated = set(cand_df["node_sequence"])
    for seq, pid in seeded.items():
        if seq not in enumerated:
            path_rows.append({
                "id": pid, "candidate_id": "", "node_sequence": seq, "edge_sequence": "",
                "evidence_grades": "", "edge_provenance": "", "evidence_snippets": "",
                "review_priority_score": float("nan"), "triage_threshold": TRIAGE_THRESHOLD,
                "flagged": 0,
                "ground_truth_label": 1, "is_weak_chain": 0, "touches_embedded_control": 0,
                "classification": "false_negative",
                "explanation": "Seeded proxy path not enumerated as a candidate.",
                "recommended_action": _action("false_negative", 0)})

    path_audit = pd.DataFrame(path_rows).sort_values(
        ["ground_truth_label", "review_priority_score"],
        ascending=[False, False], na_position="last") if path_rows else pd.DataFrame(path_rows)
    triage_audit = pd.DataFrame(score_rows).sort_values("final_score", ascending=False) \
        if score_rows else pd.DataFrame(score_rows)

    # entity-resolution audit (three-zone decisions)
    er = res.er_decisions.copy()
    er_audit = er[(er["pair_type"] == "true_alias") | (er["token_similarity"] >= 0.30)].copy()
    def er_expl(r):
        sim = r["token_similarity"]
        zone = r["decision_zone"]
        if zone == "auto_merge":
            if r["pair_type"] == "true_alias":
                return ("token similarity %.2f reaches the auto-merge threshold; the aliases "
                        "are linked (correct_auto_merge)." % sim)
            return ("token similarity %.2f reached the auto-merge threshold for a DISTINCT "
                    "pair (FALSE_MERGE - must be fixed before any further use)." % sim)
        if zone == "refer_to_human":
            kind = ("a true-alias pair" if r["pair_type"] == "true_alias"
                    else "a distinct (false-friend) pair")
            return ("token similarity %.2f falls in the ambiguous band, so the pair - %s - "
                    "is referred to the human review queue rather than decided automatically "
                    "(referred)." % (sim, kind))
        if r["pair_type"] == "true_alias":
            return ("token similarity %.2f is below the referral band; this alias pair is "
                    "conservatively kept separate (conservative_miss - recoverable by a "
                    "human reviewer)." % sim)
        return ("token similarity %.2f is below the referral band; these distinct synthetic "
                "entities are correctly kept separate (correct_keep_separate)." % sim)
    if len(er_audit):
        er_audit["expected_merge_decision"] = er_audit["ground_truth_decision"]
        er_audit["explanation"] = er_audit.apply(er_expl, axis=1)
        er_audit = er_audit.sort_values(["pair_type", "token_similarity"], ascending=[True, False])

    # negative-control audit
    nc = res.nc_audit.copy()
    if len(nc):
        nc["correctly_not_flagged"] = (nc["flagged"] == 0).astype(int)
        def _nc_expl(r):
            kind = ("embedded control (weakly attached to the active graph, reachable from "
                    "a funder)" if r.get("control_type") == "embedded"
                    else "isolated control (disconnected from the seeded structure)")
            if not r["flagged"]:
                return ("score %.2f is below the threshold of %.1f; this %s is correctly "
                        "not flagged" % (r["review_priority_score"], TRIAGE_THRESHOLD, kind))
            return ("score %.2f reached the threshold - inspect (unexpected for a %s)"
                    % (r["review_priority_score"], kind))
        nc["explanation"] = nc.apply(_nc_expl, axis=1)
    return path_audit, triage_audit, er_audit, nc
