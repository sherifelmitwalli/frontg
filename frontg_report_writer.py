#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
frontg_report_writer.py
=======================

Writes the validation tracking report (Markdown + standalone HTML) for one
scenario from the enriched audit tables. The report is a transparent,
path-by-path audit trail intended to support expert human review. It repeatedly
states that all scores are triage indicators for expert review only - never proof
of misconduct, undisclosed conflicts, hidden funding or wrongdoing.
"""
from __future__ import annotations

import html as _html
from pathlib import Path
from typing import List

import pandas as pd

from frontg_config import TRIAGE_THRESHOLD, DISCLAIMER

FIGURES = [
    ("workflow_diagram.png", "Figure 1. Study design: public signals -> synthetic validation -> human review -> (future) governed pilot."),
    ("synthetic_network_full.png", "Figure 2. Full synthetic network (node classes by colour and shape)."),
    ("synthetic_network_highlighted_paths.png", "Figure 3. Seeded proxy-path recovery (non-path nodes faded)."),
    ("synthetic_network_negative_controls.png", "Figure 4. Negative-control subgraphs: isolated and embedded controls."),
    ("synthetic_network_entity_resolution.png", "Figure 5. Entity-resolution test (auto-merge / refer / keep-separate)."),
    ("triage_score_distribution.png", "Figure 6. Review-priority score distribution by group."),
    ("score_band_truth_summary.png", "Figure 7. Descriptive score-band truth summary (planted-positive proportion by score bucket)."),
    ("robustness_threshold_sweep.png", "Figure 8. Robustness: threshold sweep and weight-perturbation stability."),
]


def _md_table(rows: List[list], headers: List[str]) -> str:
    out = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for r in rows:
        out.append("| " + " | ".join(str(c).replace("|", "/") for c in r) + " |")
    return "\n".join(out)


def write_tracking_report(res, path_audit: pd.DataFrame, triage_audit: pd.DataFrame,
                          er_audit: pd.DataFrame, nc_audit: pd.DataFrame, out: Path) -> None:
    m = res.metrics
    ns, r1, r2, r3 = (m["network_summary"], m["rq1_path_recovery"],
                      m["rq2_entity_resolution"], m["rq3_negative_controls"])
    gt = res.gen.ground_truth_paths
    recovered = path_audit[path_audit["classification"] == "true_positive"]
    fps = path_audit[path_audit["classification"] == "false_positive"]
    missed = path_audit[path_audit["classification"] == "false_negative"]
    disc = "**" + DISCLAIMER + "**"

    md = []
    md.append("# Validation Tracking Report - %s" % res.spec.name)
    md.append("_Synthetic validation harness (seed = %d)._" % res.spec.seed)
    md.append(disc)

    md.append("## 1. Network summary")
    md.append(_md_table([
        ["Total nodes", ns["n_nodes"]], ["Total edges", ns["n_edges"]],
        ["Node classes", ns["n_node_classes"]], ["Relationship types", ns["n_edge_types"]],
        ["Seeded proxy paths", ns["n_seeded_proxy_paths"]],
        ["Candidate paths", ns["n_candidate_paths"]],
        ["False-friend entities", ns["n_false_friend_entities"]],
        ["True-alias groups", ns["n_true_alias_groups"]],
        ["Negative-control subgraphs (isolated + embedded)", ns["n_negative_control_subgraphs"]],
        ["Weak-signal chains (RQ5)", ns["n_weak_chains"]],
    ], ["Quantity", "Value"]))
    md.append("**Triage threshold (review-priority cut-off): %.1f / 100.** Scores are triage "
              "indicators for expert review only." % TRIAGE_THRESHOLD)

    md.append("## 2. Seeded ground-truth proxy paths (answer key)")
    md.append(_md_table([[p["path_id"], p["node_sequence"], p["edge_types"], p["evidence_grades"]]
                         for p in gt], ["Path ID", "Node sequence", "Relationship types", "Grades"]))

    md.append("## 3. Recovered candidate paths (flagged true positives)")
    md.append(_md_table([[r["id"], r["node_sequence"], "%.2f" % r["review_priority_score"]]
                         for _, r in recovered.iterrows()], ["ID", "Node sequence", "Score"]))
    md.append("Path-recovery recall **%s**; precision **%s**." %
              (r1["path_recovery_recall"], r1["path_recovery_precision"]))

    md.append("## 4. Missed paths (seeded but not flagged)")
    md.append("None - all seeded proxy paths were recovered." if missed.empty else
              _md_table([[r["id"], r["node_sequence"]] for _, r in missed.iterrows()],
                        ["ID", "Node sequence"]))

    md.append("## 5. False-positive paths (flagged but not seeded)")
    if fps.empty:
        md.append("None.")
    else:
        fp_mins = fps["evidence_grades"].apply(
            lambda g: min(int(x) for x in str(g).split("->")) if str(g).strip() else 0)
        note = ("\n\nThese are passed to a human reviewer as possible leads only. "
                "%d contain a weak (grade <= 2) hop that inspection may set aside; "
                "%d consist entirely of documentary-grade (>= 3) hops and are not separable "
                "from true pathways on grades alone, so they require full manual verification."
                % (int((fp_mins <= 2).sum()), int((fp_mins >= 3).sum())))
        md.append(_md_table([[r["candidate_id"], r["node_sequence"], "%.2f" % r["review_priority_score"]]
                             for _, r in fps.iterrows()], ["Candidate ID", "Node sequence", "Score"]) + note)

    md.append("## 6. Negative-control results (isolated and embedded)")
    md.append(_md_table([[r["control_id"], r.get("control_type", "isolated"), r["nodes"],
                          "%.2f" % r["review_priority_score"],
                          "NOT flagged" if not r["flagged"] else "FLAGGED", r["explanation"]]
                         for _, r in nc_audit.iterrows()],
                        ["Control ID", "Type", "Nodes", "Score", "Outcome", "Explanation"]))
    md.append("Isolated-control specificity **%s**; highest control score **%s**. "
              "Embedded-control specificity **%s** over %s funder-reachable candidate paths "
              "through embedded controls (max candidate score **%s**)." %
              (r3["negative_control_specificity"], r3["max_control_score"],
               r3["embedded_control_specificity"], r3["n_embedded_control_candidates"],
               r3["max_embedded_candidate_score"]))

    md.append("## 7. Entity-resolution decisions (three-zone rule)")
    md.append("Decisions: auto_merge (similarity >= %s), refer_to_human (%s-%s), keep_separate "
              "(< %s). The automated rule never merges in the ambiguous band; referred pairs "
              "go to the human review queue." %
              (r2["auto_merge_threshold"], r2["refer_threshold"], r2["auto_merge_threshold"],
               r2["refer_threshold"]))
    if len(er_audit):
        md.append(_md_table([[r["surface_a"], r["surface_b"], r["pair_type"], "%.2f" % r["token_similarity"],
                              r["decision_zone"], r["outcome"]]
                             for _, r in er_audit.iterrows()],
                            ["Surface A", "Surface B", "Pair type", "Sim.", "Zone", "Outcome"]))
    md.append("Auto-merge precision **%s**; auto-merge recall **%s**; potential recall if all referred true-alias pairs are correctly confirmed **%s** (assumption, not observed human performance). False merges: **%s**. Referral queue: %s pairs (%s true aliases, %s distinct pairs)." %
              (r2["entity_resolution_precision"], r2["entity_resolution_recall"],
               r2["potential_recall_if_all_referred_true_aliases_are_correctly_confirmed"], r2["n_false_merges"],
               r2["n_referred_pairs"], r2["n_referred_true_alias"], r2["n_referred_distinct"]))

    r5 = m["rq5_robustness"]
    md.append("## 7b. Robustness checks (weak-signal chains, gate ablation, sensitivity)")
    md.append(_md_table([
        ["Seeded weak-signal chains", r5["n_weak_chains_seeded"]],
        ["Weak-chain candidate paths", r5["n_weak_chain_candidates"]],
        ["Weak-chain candidates entering high-priority review", r5["n_weak_chain_high_priority_review"]],
        ["Weak-chain candidates flagged (gate REMOVED)", r5["n_weak_chain_flagged_ungated"]],
        ["Max weak-chain score (gated)", r5["max_weak_chain_score_gated"]],
        ["Max weak-chain score (gate removed)", r5["max_weak_chain_score_ungated"]],
        ["Max attainable weak-signal-only score (exact controlled-vocabulary enumeration, gate removed)",
         r5.get("weak_signal_only_max_attainable_ungated", "n/a")],
    ], ["Robustness check", "Value"]))
    if "weight_sensitivity" in r5:
        ws = r5["weight_sensitivity"]
        md.append("Weight-perturbation stability (%s draws, +/-%.0f%%): Spearman rho min/median **%s / %s**; Kendall tau-b min/median **%s / %s**; top-k Jaccard min **%s**; threshold-based recall median **%s**. Ties use average ranks for Spearman and tau-b correction for Kendall. See sensitivity_analysis.csv and threshold_sweep.csv." %
                  (ws["n_draws"], 100 * ws["rel_range"], ws["spearman_rho_min"], ws["spearman_rho_median"],
                   ws["kendall_tau_b_min"], ws["kendall_tau_b_median"], ws["topk_jaccard_min"], ws["recall_median"]))

    active = m.get("active_noise_validation", {})
    if active.get("n_active_noise_edges", 0):
        md.append("## 7c. Connected active-network noise challenge")
        md.append("%s connected active-noise edges increased candidate-path enumeration from **%s** to **%s**. The scenario contained **%s** candidate paths using active noise and **%s** high-priority active-noise false positives. These false positives are retained as an adverse result; candidate enumeration did%s reach the cap of %s." %
                  (active["n_active_noise_edges"], active["candidate_paths_before_active_noise"],
                   active["candidate_paths_after_active_noise"], active["n_candidate_paths_using_active_noise"],
                   active["n_high_priority_active_noise_false_positives"],
                   "" if active["candidate_cap_reached"] else " not", active["candidate_cap"]))

    md.append("## 8. Path-by-path audit trail")
    md.append("Each candidate path is shown with its edge provenance, evidence snippets, triage "
              "decision and a recommended human-review action. Scores are triage indicators only.")
    for _, r in path_audit.iterrows():
        md.append("### %s (%s)" % (r["id"], r["classification"]))
        md.append("- **Node sequence:** %s" % r["node_sequence"])
        md.append("- **Edge sequence:** %s" % (r["edge_sequence"] or "n/a"))
        md.append("- **Evidence grades:** %s" % (r["evidence_grades"] or "n/a"))
        md.append("- **Edge provenance:** %s" % (r["edge_provenance"] or "n/a"))
        md.append("- **Evidence snippets:** %s" % (r["evidence_snippets"] or "n/a"))
        md.append("- **Review-priority score:** %s (threshold %.1f) -> %s" %
                  (r["review_priority_score"], TRIAGE_THRESHOLD,
                   "FLAGGED" if r["flagged"] else "not flagged"))
        md.append("- **Ground-truth label:** %s" % ("seeded proxy path" if r["ground_truth_label"] else "not seeded"))
        md.append("- **Why:** %s" % r["explanation"])
        md.append("- **Recommended action:** %s" % r["recommended_action"])

    md.append("## 9. Visual validation")
    figures = list(FIGURES)
    if (out / "active_noise_challenge.png").exists():
        figures.append(("active_noise_challenge.png", "Figure 9. Connected active-network noise challenge."))
    for fn, cap in figures:
        md.append("![%s](%s)" % (cap, fn))

    md.append("## 10. Interpretation statement")
    md.append("This report is a transparent, path-by-path audit trail. The framework is designed to "
              "prioritise manual expert review, not to automate accusation or attribution. " + disc)

    (out / "validation_tracking_report.md").write_text("\n\n".join(md), encoding="utf-8")

    # ---------------- HTML ---------------- #
    def df_html(df, cols, headers):
        d = df[cols].copy(); d.columns = headers
        return d.to_html(index=False, border=0, classes="tbl", escape=True)

    parts = []
    parts.append("<h1>Validation Tracking Report - %s</h1>" % _html.escape(res.spec.name))
    parts.append("<p class='sub'>Synthetic validation harness (seed = %d).</p>" % res.spec.seed)
    parts.append("<div class='disc'>%s</div>" % _html.escape(DISCLAIMER))

    parts.append("<h2>1. Network summary</h2>")
    summ = pd.DataFrame({"Quantity": ["Total nodes", "Total edges", "Node classes", "Relationship types",
        "Seeded proxy paths", "Candidate paths", "False-friend entities", "True-alias groups",
        "Negative-control subgraphs", "Weak-signal chains"],
        "Value": [ns["n_nodes"], ns["n_edges"], ns["n_node_classes"], ns["n_edge_types"],
        ns["n_seeded_proxy_paths"], ns["n_candidate_paths"], ns["n_false_friend_entities"],
        ns["n_true_alias_groups"], ns["n_negative_control_subgraphs"], ns["n_weak_chains"]]})
    parts.append(summ.to_html(index=False, border=0, classes="tbl", escape=True))
    parts.append("<p class='note'>Triage threshold: <b>%.1f / 100</b>. Scores are triage indicators "
                 "for expert review only.</p>" % TRIAGE_THRESHOLD)

    parts.append("<h2>2. Seeded ground-truth proxy paths</h2>")
    parts.append(df_html(pd.DataFrame(gt), ["path_id", "node_sequence", "edge_types", "evidence_grades"],
                         ["Path ID", "Node sequence", "Relationship types", "Grades"]))

    parts.append("<h2>3. Recovered candidate paths (true positives)</h2>")
    parts.append(df_html(recovered, ["id", "node_sequence", "review_priority_score"],
                         ["ID", "Node sequence", "Score"]) if len(recovered) else "<p>None.</p>")
    parts.append("<p class='note'>Path-recovery recall <b>%s</b>; precision <b>%s</b>.</p>" %
                 (r1["path_recovery_recall"], r1["path_recovery_precision"]))

    parts.append("<h2>4. Missed paths</h2>")
    parts.append("<p>None - all seeded proxy paths were recovered.</p>" if missed.empty else
                 df_html(missed, ["id", "node_sequence"], ["ID", "Node sequence"]))

    parts.append("<h2>5. False-positive paths</h2>")
    if fps.empty:
        parts.append("<p>None.</p>")
    else:
        fp_mins_h = fps["evidence_grades"].apply(
            lambda g: min(int(x) for x in str(g).split("->")) if str(g).strip() else 0)
        parts.append(df_html(fps, ["candidate_id", "node_sequence", "review_priority_score"],
                             ["Candidate ID", "Node sequence", "Score"]) +
                     "<p class='note'>Passed to human review as possible leads only. "
                     "%d contain a weak (grade &le; 2) hop; %d consist entirely of "
                     "documentary-grade (&ge; 3) hops and require full manual verification.</p>"
                     % (int((fp_mins_h <= 2).sum()), int((fp_mins_h >= 3).sum())))

    parts.append("<h2>6. Negative-control results (isolated and embedded)</h2>")
    parts.append(df_html(nc_audit, ["control_id", "control_type", "nodes", "review_priority_score",
                                    "flagged", "explanation"],
                         ["Control ID", "Type", "Nodes", "Score", "Flagged", "Explanation"]))
    parts.append("<p class='note'>Isolated-control specificity <b>%s</b>; embedded-control "
                 "specificity <b>%s</b> over %s funder-reachable candidate paths (max candidate "
                 "score %s).</p>" %
                 (r3["negative_control_specificity"], r3["embedded_control_specificity"],
                  r3["n_embedded_control_candidates"], r3["max_embedded_candidate_score"]))

    parts.append("<h2>7. Entity-resolution decisions (three-zone rule)</h2>")
    if len(er_audit):
        parts.append(df_html(er_audit, ["surface_a", "surface_b", "pair_type", "token_similarity",
                     "decision_zone", "outcome", "explanation"],
                     ["Surface A", "Surface B", "Type", "Sim.", "Zone", "Outcome", "Explanation"]))
    parts.append("<p class='note'>Auto-merge precision <b>%s</b>; auto-merge recall <b>%s</b>; "
                 "potential recall if all referred true-alias pairs are correctly confirmed <b>%s</b> (assumption, not observed human performance); false "
                 "merges <b>%s</b>; referral queue <b>%s</b> pairs.</p>" %
                 (r2["entity_resolution_precision"], r2["entity_resolution_recall"],
                  r2["potential_recall_if_all_referred_true_aliases_are_correctly_confirmed"], r2["n_false_merges"],
                  r2["n_referred_pairs"]))

    r5h = m["rq5_robustness"]
    parts.append("<h2>7b. Robustness checks</h2>")
    rob = pd.DataFrame({"Check": ["Weak-chain candidates entering high-priority review",
                                  "Weak-chain candidates flagged (gate removed)",
                                  "Max weak-chain score (gated)",
                                  "Max weak-chain score (gate removed)",
                                  "Max attainable weak-signal-only score (analytic, gate removed)"],
                        "Value": [r5h["n_weak_chain_high_priority_review"],
                                  r5h["n_weak_chain_flagged_ungated"],
                                  r5h["max_weak_chain_score_gated"],
                                  r5h["max_weak_chain_score_ungated"],
                                  r5h.get("weak_signal_only_max_attainable_ungated", "n/a")]})
    parts.append(rob.to_html(index=False, border=0, classes="tbl", escape=True))
    if "weight_sensitivity" in r5h:
        ws = r5h["weight_sensitivity"]
        parts.append("<p class='note'>Weight-perturbation stability (%s draws, +/-%.0f%%): Spearman rho min/median <b>%s / %s</b>; Kendall tau-b min/median <b>%s / %s</b>. Ties use average ranks for Spearman and tau-b correction for Kendall.</p>" %
                     (ws["n_draws"], 100 * ws["rel_range"], ws["spearman_rho_min"], ws["spearman_rho_median"],
                      ws["kendall_tau_b_min"], ws["kendall_tau_b_median"]))
    active = m.get("active_noise_validation", {})
    if active.get("n_active_noise_edges", 0):
        active_table = pd.DataFrame({"Check": ["Connected active-noise edges", "Candidate paths before -> after active noise", "Candidate paths using active noise", "High-priority active-noise false positives", "Candidate cap reached"],
                                     "Value": [active["n_active_noise_edges"], "%s -> %s" % (active["candidate_paths_before_active_noise"], active["candidate_paths_after_active_noise"]), active["n_candidate_paths_using_active_noise"], active["n_high_priority_active_noise_false_positives"], active["candidate_cap_reached"]]})
        parts.append("<h2>7c. Connected active-network noise challenge</h2>")
        parts.append(active_table.to_html(index=False, border=0, classes="tbl", escape=True))

    parts.append("<h2>8. Path-by-path audit trail</h2>")
    parts.append(df_html(path_audit, ["id", "node_sequence", "edge_sequence", "evidence_grades",
                 "edge_provenance", "review_priority_score", "flagged", "classification",
                 "explanation", "recommended_action"],
                 ["ID", "Node sequence", "Edge sequence", "Grades", "Provenance", "Score", "Flagged",
                  "Class", "Why", "Recommended action"]))

    parts.append("<h2>9. Visual validation</h2>")
    figures = list(FIGURES)
    if (out / "active_noise_challenge.png").exists():
        figures.append(("active_noise_challenge.png", "Figure 9. Connected active-network noise challenge."))
    for fn, cap in figures:
        parts.append("<figure><img src='%s' alt='%s'><figcaption>%s</figcaption></figure>" %
                     (fn, _html.escape(cap), _html.escape(cap)))

    parts.append("<h2>10. Interpretation statement</h2>")
    parts.append("<div class='disc'>This report is a transparent, path-by-path audit trail. The "
                 "framework is designed to prioritise manual expert review, not to automate accusation "
                 "or attribution. " + _html.escape(DISCLAIMER) + "</div>")

    css = """
    body{font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif;max-width:1040px;margin:24px auto;padding:0 18px;color:#1a1a1a;line-height:1.5}
    h1{color:#1F3864;margin-bottom:2px} h2{color:#2E4D7B;border-bottom:2px solid #D9E2F3;padding-bottom:4px;margin-top:28px}
    .sub{color:#666;margin-top:0} .note{color:#444;font-size:.92em}
    .disc{background:#D9E2F3;border:1px solid #1F3864;border-radius:6px;padding:12px 14px;margin:14px 0;font-size:.95em}
    table.tbl{border-collapse:collapse;width:100%;margin:10px 0;font-size:.82em}
    table.tbl th{background:#1F3864;color:#fff;text-align:left;padding:7px 9px}
    table.tbl td{border:1px solid #cfd8e8;padding:6px 9px;vertical-align:top}
    table.tbl tr:nth-child(even){background:#F2F5FB}
    figure{margin:16px 0;text-align:center} figure img{max-width:100%;border:1px solid #ccc;border-radius:4px}
    figcaption{font-size:.85em;color:#555;margin-top:4px}
    """
    doc = ("<!DOCTYPE html><html lang='en'><head><meta charset='utf-8'>"
           "<meta name='viewport' content='width=device-width,initial-scale=1'>"
           "<title>Validation Tracking Report - %s</title><style>%s</style></head><body>%s</body></html>"
           % (_html.escape(res.spec.name), css, "\n".join(parts)))
    (out / "validation_tracking_report.html").write_text(doc, encoding="utf-8")
