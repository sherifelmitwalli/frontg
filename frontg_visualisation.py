#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
frontg_visualisation.py
=======================

High-resolution (300 dpi) figures for one scenario. All figures use a consistent
per-class colour + marker-shape scheme and grade-styled edges. Every caption
states that all entities and relationships are synthetic. Figures are visual aids
for expert review only; they assert nothing about any real person or organisation.

Figures produced:
  1 workflow_diagram.png                       (conceptual HITL workflow)
  2 synthetic_network_full.png
  3 synthetic_network_highlighted_paths.png
  4 synthetic_network_negative_controls.png    (isolated + embedded controls)
  5 synthetic_network_entity_resolution.png    (three-zone decisions)
  6 triage_score_distribution.png
  7 score_band_truth_summary.png
  8 robustness_threshold_sweep.png             (threshold sweep + weight sensitivity)
"""
from __future__ import annotations

import math
from pathlib import Path
from typing import Dict, List

import numpy as np
import networkx as nx
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

from frontg_config import (NODE_COLORS, NODE_SHAPES, EDGE_GRADE_STYLES, NODE_CLASSES,
                           TRIAGE_THRESHOLD, DISCLAIMER)

DPI = 300

# Publication mode: when the environment variable FRONTG_PUBLICATION is set to a
# truthy value, figure-level titles and the disclaimer footer are suppressed so
# figures can be embedded in a document whose captions carry that text.
# Panel labels ("(a)", "(b)") and per-subplot titles are kept. Default: off,
# so standalone repository figures remain self-describing.
import os
PUBLICATION_MODE = os.environ.get("FRONTG_PUBLICATION", "0").lower() not in ("0", "", "false", "no")


def _maybe_title(ax, *args, **kwargs):
    if not PUBLICATION_MODE:
        ax.set_title(*args, **kwargs)


def _maybe_suptitle(fig, *args, **kwargs):
    if not PUBLICATION_MODE:
        fig.suptitle(*args, **kwargs)


def _simple(G):
    s = nx.DiGraph()
    for n, d in G.nodes(data=True):
        s.add_node(n, **d)
    grade = {}
    for u, v, d in G.edges(data=True):
        if not s.has_edge(u, v) or d["evidence_grade"] > grade.get((u, v), -1):
            grade[(u, v)] = d["evidence_grade"]
        s.add_edge(u, v)
    nx.set_edge_attributes(s, grade, "evidence_grade")
    return s


def _layout(s, seed):
    n = s.number_of_nodes()
    k = 1.6 / math.sqrt(max(n, 1))
    iters = 200 if n <= 120 else (80 if n <= 300 else 45)
    return nx.spring_layout(s, seed=seed, k=k, iterations=iters)


def _draw_nodes(ax, s, pos, nodelist=None, size=260, edgecolor="#333333", lw=0.6, alpha=1.0):
    nodes = nodelist if nodelist is not None else list(s.nodes())
    for cls in NODE_CLASSES:
        sub = [n for n in nodes if s.nodes[n]["node_class"] == cls]
        if not sub:
            continue
        nx.draw_networkx_nodes(s, pos, nodelist=sub, ax=ax, node_color=NODE_COLORS[cls],
                               node_shape=NODE_SHAPES[cls], node_size=size,
                               edgecolors=edgecolor, linewidths=lw, alpha=alpha)


def _draw_edges_by_grade(ax, s, pos, edgelist=None, alpha=0.9, scale=1.0):
    edges = edgelist if edgelist is not None else list(s.edges())
    by_grade: Dict[int, List] = {}
    for u, v in edges:
        g = s.edges[u, v].get("evidence_grade", 1)
        by_grade.setdefault(g, []).append((u, v))
    for g in sorted(by_grade):
        st = EDGE_GRADE_STYLES[g]
        nx.draw_networkx_edges(s, pos, edgelist=by_grade[g], ax=ax, edge_color=st["color"],
                               style=st["style"], width=st["width"] * scale, alpha=alpha,
                               arrows=True, arrowsize=7, connectionstyle="arc3,rad=0.04")


def _class_legend(ax, classes, loc="upper left", anchor=(1.01, 1.0)):
    handles = [Line2D([0], [0], marker=NODE_SHAPES[c], color="w", markerfacecolor=NODE_COLORS[c],
               markeredgecolor="#333", markersize=9, label=c) for c in classes]
    return ax.legend(handles=handles, loc=loc, bbox_to_anchor=anchor, fontsize=7,
                     frameon=True, title="Node class", title_fontsize=8)


def _grade_legend(ax, loc="lower left", anchor=(1.01, 0.0)):
    handles = [Line2D([0], [0], color=EDGE_GRADE_STYLES[g]["color"], lw=EDGE_GRADE_STYLES[g]["width"],
               linestyle=EDGE_GRADE_STYLES[g]["style"], label=EDGE_GRADE_STYLES[g]["label"])
               for g in sorted(EDGE_GRADE_STYLES)]
    leg = ax.legend(handles=handles, loc=loc, bbox_to_anchor=anchor, fontsize=6.5,
                    frameon=True, title="Edge by evidence grade", title_fontsize=7)
    return leg


def _footer(ax, fig):
    if PUBLICATION_MODE:
        return
    fig.text(0.5, 0.015, DISCLAIMER, ha="center", va="bottom", fontsize=7, color="#555555", wrap=True)


def _present_classes(s, nodes=None):
    nodes = nodes if nodes is not None else list(s.nodes())
    return [c for c in NODE_CLASSES if any(s.nodes[n]["node_class"] == c for n in nodes)]


# --------------------------------------------------------------------------- #
# Figure - conceptual six-stage human-in-the-loop workflow
# --------------------------------------------------------------------------- #
def fig_workflow(out: Path):
    """Journal-style conceptual figure: public signals -> synthetic validation
    (this study) -> expert human review -> (dashed) future governed pilot.
    Minimal text, no internal title; the caption carries the explanation."""
    from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

    BLUE, AMBER, GREY, GREEN = "#1F3864", "#B9770E", "#6E6E6E", "#1b7837"
    fig, ax = plt.subplots(figsize=(13.4, 4.5))
    ax.set_xlim(0, 13.4); ax.set_ylim(0, 4.5); ax.axis("off")

    def box(x, w, header, hcolor, ec, dashed=False, fill="#FFFFFF"):
        ax.add_patch(FancyBboxPatch((x, 1.05), w, 2.75, boxstyle="round,pad=0.05",
                                    fc=fill, ec=ec, lw=1.4,
                                    linestyle=(0, (5, 3)) if dashed else "solid"))
        ax.text(x + w / 2, 3.52, header, ha="center", va="center",
                fontsize=10, weight="bold", color=hcolor)
        ax.plot([x + 0.18, x + w - 0.18], [3.32, 3.32], color=ec, lw=0.8, alpha=0.6)

    def arrow(x0, x1, label="", dashed=False):
        ax.add_patch(FancyArrowPatch((x0, 2.42), (x1, 2.42), arrowstyle="-|>",
                                     mutation_scale=18, color=GREY, lw=1.6,
                                     linestyle=(0, (4, 3)) if dashed else "solid"))
        if label:
            ax.text((x0 + x1) / 2, 2.66, label, ha="center", fontsize=7.6,
                    color=GREY, style="italic")

    # 1. public signals
    box(0.25, 2.95, "Public signals", BLUE, GREY)
    ax.text(0.50, 3.05, "Documentary", fontsize=8.6, weight="bold", color=BLUE)
    for i, t in enumerate(["funding records", "reports & publications",
                           "events & partnerships"]):
        ax.text(0.62, 2.78 - 0.27 * i, t, fontsize=8.4, color="#333333")
    ax.text(0.50, 1.92, "Weak", fontsize=8.6, weight="bold", color=AMBER)
    for i, t in enumerate(["shared links / reposts", "similar language",
                           "co-occurrence & timing"]):
        ax.text(0.62, 1.65 - 0.27 * i, t, fontsize=8.4, color="#333333")
    arrow(3.28, 3.92)

    # 2. synthetic validation
    box(3.98, 4.05, "Synthetic validation  (this study)", BLUE, BLUE, fill="#F4F7FC")
    checks = ["Finds seeded funder \u2192 intermediary \u2192 campaign pathways",
              "Never auto-merges look-alike organisations",
              "Leaves unrelated bystanders unflagged",
              "Weak signals alone can never trigger review",
              "Evaluated across network sizes and fixed seeds"]
    for i, t in enumerate(checks):
        y = 3.05 - 0.34 * i
        ax.text(4.22, y, "\u2713", fontsize=9.5, weight="bold", color=GREEN)
        ax.text(4.48, y, t, fontsize=8.4, color="#333333")
    ax.text(6.0, 1.22, "abstract entities \u00b7 known ground truth \u00b7 fixed seeds",
            ha="center", fontsize=7.4, color=GREY, style="italic")
    arrow(8.11, 8.75)

    # 3. human review
    box(8.81, 2.05, "Expert human review", "#7E5109", AMBER, fill="#FDF6EC")
    ax.text(9.835, 2.30, "every flag is a prompt\nfor confidential review \u2014\n"
            "never a finding\nof wrongdoing", ha="center", va="center",
            fontsize=8.3, color="#5A4A1F")
    arrow(10.94, 11.38, dashed=True)

    # 4. future governed pilot
    box(11.44, 1.75, "Future application", GREY, GREY, dashed=True, fill="#FAFAFA")
    ax.text(12.315, 2.30, "future work \u2014\nconditional on\nethics, legal &\n"
            "data-protection\nreview; FCTC\nArt. 5.3 governance", ha="center", va="center",
            fontsize=8.0, color="#555555")

    if not PUBLICATION_MODE:
        ax.text(6.7, 0.42, "All entities are synthetic and abstract \u2014 no real people or "
            "organisations, no live data collection. Outputs are triage indicators for "
            "expert review, never findings of wrongdoing.",
            ha="center", fontsize=7.6, color=GREY)
    fig.tight_layout()
    fig.savefig(out / "workflow_diagram.png", dpi=DPI, bbox_inches="tight"); plt.close(fig)


# --------------------------------------------------------------------------- #
# Figure - full network
# --------------------------------------------------------------------------- #
def fig_full(res, out: Path):
    s = _simple(res.G); pos = _layout(s, res.spec.seed)
    n = s.number_of_nodes()
    size = 320 if n <= 60 else (90 if n <= 220 else 36)
    fig, ax = plt.subplots(figsize=(11, 8.2))
    _draw_edges_by_grade(ax, s, pos, alpha=0.5, scale=0.8 if n > 120 else 1.0)
    _draw_nodes(ax, s, pos, size=size, lw=0.5)
    if n <= 60:
        nx.draw_networkx_labels(s, pos, ax=ax, font_size=5.2)
    leg1 = _class_legend(ax, _present_classes(s)); ax.add_artist(leg1)
    _grade_legend(ax)
    _maybe_title(ax, "Full synthetic network - %s (%d nodes, %d edges)\n"
                 "node classes by colour and shape; edges styled by synthetic evidence grade"
                 % (res.spec.name, res.G.number_of_nodes(), res.G.number_of_edges()), fontsize=11)
    ax.axis("off"); _footer(ax, fig)
    fig.tight_layout(rect=[0, 0.03, 1, 1])
    fig.savefig(out / "synthetic_network_full.png", dpi=DPI, bbox_inches="tight"); plt.close(fig)


# --------------------------------------------------------------------------- #
# Figure - highlighted seeded proxy paths
# --------------------------------------------------------------------------- #
def fig_paths(res, out: Path):
    G = res.G; s = _simple(G); pos = _layout(s, res.spec.seed)
    gt_edges = [(u, v) for u, v, d in G.edges(data=True) if d.get("is_ground_truth")]
    gt_nodes = set()
    for p in res.gen.ground_truth_paths:
        gt_nodes.update(x.strip() for x in p["node_sequence"].split("->"))
    n = s.number_of_nodes()
    bg_size = 120 if n <= 60 else (40 if n <= 220 else 16)
    hl_size = 360 if n <= 60 else (130 if n <= 220 else 60)
    fig, ax = plt.subplots(figsize=(11, 8.2))
    nx.draw_networkx_edges(s, pos, ax=ax, edge_color="#e6e6e6", width=0.7, arrows=False, alpha=0.7)
    bg = [x for x in s.nodes() if x not in gt_nodes]
    nx.draw_networkx_nodes(s, pos, nodelist=bg, ax=ax, node_color="#e9e9e9", node_size=bg_size,
                           edgecolors="#cccccc", linewidths=0.4)
    nx.draw_networkx_edges(s, pos, edgelist=gt_edges, ax=ax, edge_color="#b2182b", width=2.6,
                           arrows=True, arrowsize=13, connectionstyle="arc3,rad=0.04")
    _draw_nodes(ax, s, pos, nodelist=list(gt_nodes), size=hl_size, edgecolor="#b2182b", lw=1.5)
    if len(gt_nodes) <= 80:
        nx.draw_networkx_labels(s, pos, ax=ax, labels={x: x for x in gt_nodes}, font_size=6.8 if PUBLICATION_MODE else 5.6)
    handles = [Line2D([0], [0], marker=NODE_SHAPES[c], color="w", markerfacecolor=NODE_COLORS[c],
               markeredgecolor="#b2182b", markersize=9, label=c) for c in _present_classes(s, gt_nodes)]
    handles.append(Line2D([0], [0], color="#b2182b", lw=2.6, label="seeded proxy-path edge"))
    handles.append(Line2D([0], [0], marker="o", color="w", markerfacecolor="#e9e9e9",
                   markeredgecolor="#ccc", markersize=8, label="non-path node (faded)"))
    ax.legend(handles=handles, loc="upper left", bbox_to_anchor=(1.01, 1.0), fontsize=7, frameon=True)
    _maybe_title(ax, "Seeded proxy-path recovery - %s\n%d seeded paths highlighted; "
                 "non-path nodes faded (recall %s)"
                 % (res.spec.name, len(res.gen.ground_truth_paths),
                    res.metrics["rq1_path_recovery"]["path_recovery_recall"]), fontsize=11)
    ax.axis("off"); _footer(ax, fig)
    fig.tight_layout(rect=[0, 0.03, 1, 1])
    fig.savefig(out / "synthetic_network_highlighted_paths.png", dpi=DPI, bbox_inches="tight"); plt.close(fig)


# --------------------------------------------------------------------------- #
# Figure - negative-control subgraphs (isolated + embedded)
# --------------------------------------------------------------------------- #
def fig_negative_controls(res, out: Path):
    """Two panels: (a) isolated controls, disconnected from the seeded structure;
    (b) embedded controls, weakly attached to the active graph and therefore
    reachable from funders - the non-trivial negative-control test."""
    G = res.G; nc = res.nc_audit
    iso = nc[nc["control_type"] == "isolated"]
    emb = nc[nc["control_type"] == "embedded"]

    fig, (axL, axR) = plt.subplots(1, 2, figsize=(13.5, 7.0),
                                   gridspec_kw={"width_ratios": [1.15, 1.0]})

    def _panel(ax, rows, include_attach: bool, title: str):
        nodes = []
        for _, r in rows.iterrows():
            nodes += [x.strip() for x in str(r["nodes"]).split(";")]
            if include_attach and r.get("attached_to"):
                nodes.append(str(r["attached_to"]).strip())
        nodes = [n for n in dict.fromkeys(nodes) if n]
        if not nodes:
            ax.axis("off"); ax.set_title(title, fontsize=10); return
        sub = _simple(G).subgraph(nodes).copy()
        pos = nx.spring_layout(sub, seed=res.spec.seed,
                               k=2.2 / math.sqrt(max(len(nodes), 1)),
                               iterations=120 if len(nodes) <= 120 else 60)
        n = len(nodes)
        size = 300 if n <= 40 else (110 if n <= 120 else 45)
        _draw_edges_by_grade(ax, sub, pos, alpha=0.85)
        _draw_nodes(ax, sub, pos, size=size, edgecolor="#1f78b4", lw=1.1)
        if n <= 60:
            nx.draw_networkx_labels(sub, pos, ax=ax, font_size=5.4)
        show = rows if len(rows) <= 12 else rows.head(12)
        for _, r in show.iterrows():
            first = str(r["nodes"]).split(";")[0].strip()
            if first in pos:
                x, y = pos[first]
                ax.annotate("%s | %.1f | %s" % (r["control_id"], r["review_priority_score"],
                            "NOT flagged" if not r["flagged"] else "FLAGGED"),
                            (x, y), textcoords="offset points", xytext=(0, 14), ha="center",
                            fontsize=5.6, color="#1f78b4",
                            bbox=dict(boxstyle="round,pad=0.18", fc="#eef5fb", ec="#1f78b4", lw=0.5))
        ax.set_title(title, fontsize=9.5)
        ax.axis("off")

    r3 = res.metrics["rq3_negative_controls"]
    _panel(axL, iso, False,
           "(a) Isolated controls (n=%d): disconnected from the seeded structure;\n"
           "specificity %s, max score %s" % (len(iso), r3["negative_control_specificity"],
                                             r3["max_control_score"]))
    _panel(axR, emb, True,
           "(b) Embedded controls (n=%d): weakly attached, funder-reachable;\n"
           "%d candidate paths through them, none flagged (max score %s)"
           % (len(emb), r3["n_embedded_control_candidates"], r3["max_embedded_candidate_score"]))
    _grade_legend(axR, loc="lower left", anchor=(0.99, 0.0))
    _maybe_suptitle(fig, "Negative-control subgraphs - %s\nisolated controls test non-association; embedded "
                 "controls test that weak attachment to the active graph does not create priority"
                 % res.spec.name, fontsize=11)
    _footer(axR, fig)
    fig.tight_layout(rect=[0, 0.035, 1, 0.90])
    fig.savefig(out / "synthetic_network_negative_controls.png", dpi=DPI, bbox_inches="tight"); plt.close(fig)


# --------------------------------------------------------------------------- #
# Figure - entity resolution (three-zone decisions)
# --------------------------------------------------------------------------- #
def fig_entity_resolution(res, out: Path):
    rows = res.gen.entity_resolution_rows
    er = res.er_decisions
    prop = {}
    for _, r in er.iterrows():
        prop[(r["surface_a"], r["surface_b"])] = r["decision_zone"]
        prop[(r["surface_b"], r["surface_a"])] = r["decision_zone"]

    alias_groups: Dict[str, List[str]] = {}
    ff_by_canon: Dict[str, List[str]] = {}
    for r in rows:
        if r["is_true_alias"]:
            alias_groups.setdefault(r["canonical_id"], []).append(r["surface_form"])
        else:
            ff_by_canon.setdefault(r["canonical_id"][:-2], []).append(r["surface_form"])
    ff_pairs = [v for v in ff_by_canon.values() if len(v) >= 2]

    max_ff, max_grp = 6, 4
    show_ff = ff_pairs[:max_ff]; show_grp = list(alias_groups.items())[:max_grp]

    fig, ax = plt.subplots(figsize=(11.5, 7.6))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    ax.text(0.23, 0.99, "False friends (distinct identities)", ha="center", fontsize=10,
            weight="bold", color="#b22222")
    ax.text(0.75, 0.99, "True aliases (same canonical ID)", ha="center", fontsize=10,
            weight="bold", color="#1b7837")

    def node(x, y, label, ec):
        ax.scatter([x], [y], s=540, c="#7570b3", edgecolors=ec, linewidths=1.4, zorder=3)
        ax.annotate(label, (x, y), textcoords="offset points", xytext=(0, -15),
                    ha="center", fontsize=6.4, zorder=4)

    ZONE_STYLE = {
        "auto_merge": {"color": "#1b7837", "ls": "-", "label": "auto-merged"},
        "refer_to_human": {"color": "#e08214", "ls": (0, (2, 2)), "label": "referred to human queue"},
        "keep_separate": {"color": "#b22222", "ls": (0, (4, 3)), "label": "kept separate"},
    }

    ys = np.linspace(0.86, 0.12, max(len(show_ff), 1))
    for i, pair in enumerate(show_ff):
        a, b = pair[0], pair[1]; y = ys[i]; xa, xb = 0.08, 0.40
        node(xa, y, a, "#b22222"); node(xb, y, b, "#b22222")
        z = prop.get((a, b), "keep_separate")
        st = ZONE_STYLE[z]
        ax.plot([xa + 0.03, xb - 0.03], [y, y], color=st["color"], lw=1.8, ls=st["ls"], zorder=2)
        lab = ("-> referred to human queue (never auto-merged)" if z == "refer_to_human"
               else "x  kept separate")
        ax.annotate(lab, ((xa + xb) / 2, y), textcoords="offset points",
                    xytext=(0, 9), ha="center", fontsize=6.0, color=st["color"])

    centers_y = np.linspace(0.80, 0.20, max(len(show_grp), 1))
    for gi, (canon, members) in enumerate(show_grp):
        cx, cy = 0.76, centers_y[gi]; nM = len(members); R = 0.10
        coords = {}
        for k, mname in enumerate(members):
            ang = math.pi / 2 + 2 * math.pi * k / nM
            coords[mname] = (cx + R * math.cos(ang) * 1.5, cy + R * math.sin(ang))
        for i in range(nM):
            for j in range(i + 1, nM):
                a, b = members[i], members[j]
                z = prop.get((a, b), "keep_separate")
                st = ZONE_STYLE[z]
                (xa, ya), (xb, yb) = coords[a], coords[b]
                ax.plot([xa, xb], [ya, yb], color=st["color"], lw=1.8, ls=st["ls"], zorder=2)
        for mname, (x, y) in coords.items():
            node(x, y, mname, "#1b7837")
        ax.annotate(canon, (cx, cy), ha="center", fontsize=6.6, color="#1b7837", weight="bold")

    r2m = res.metrics["rq2_entity_resolution"]
    legend = [Line2D([0], [0], color="#1b7837", lw=2, label="auto-merged (true alias, similarity >= %s)" % r2m["auto_merge_threshold"]),
              Line2D([0], [0], color="#e08214", lw=2, ls=(0, (2, 2)),
                     label="ambiguous band -> referred to human review queue"),
              Line2D([0], [0], color="#b22222", lw=1.8, ls=(0, (4, 3)), label="kept separate (below referral band)")]
    ax.legend(handles=legend, loc="lower center", bbox_to_anchor=(0.5, -0.08), ncol=3, fontsize=7, frameon=True)
    note = ("showing first %d of %d false-friend pairs and first %d of %d alias groups"
            % (len(show_ff), len(ff_pairs), len(show_grp), len(alias_groups))) \
        if (len(ff_pairs) > max_ff or len(alias_groups) > max_grp) else ""
    _maybe_title(ax, "Entity-resolution test (three-zone rule) - %s\nauto-merge precision %s; no false "
                 "friend auto-merged; potential perfect-adjudication recall %s%s"
                 % (res.spec.name, r2m["entity_resolution_precision"],
                    r2m["potential_recall_if_all_referred_true_aliases_are_correctly_confirmed"],
                    ("\n" + note) if note else ""), fontsize=11)
    _footer(ax, fig)
    fig.tight_layout(rect=[0, 0.03, 1, 1])
    fig.savefig(out / "synthetic_network_entity_resolution.png", dpi=DPI, bbox_inches="tight"); plt.close(fig)


# --------------------------------------------------------------------------- #
# Figure - triage score distribution by group
# --------------------------------------------------------------------------- #
def fig_score_distribution(res, out: Path):
    cand = res.cand_df
    is_true = cand["ground_truth_label"] == 1
    is_wc = cand["is_weak_chain"] == 1
    is_emb = cand["touches_embedded_control"] == 1
    true_scores = cand[is_true]["review_priority_score"].tolist()
    wc_scores = cand[is_wc]["review_priority_score"].tolist()
    emb_scores = cand[is_emb & ~is_wc]["review_priority_score"].tolist()
    false_scores = cand[~is_true & ~is_wc & ~is_emb]["review_priority_score"].tolist()
    nc_scores = res.nc_audit[res.nc_audit["control_type"] == "isolated"]["review_priority_score"].tolist()
    bins = np.arange(0, 101, 5)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(nc_scores, bins=bins, alpha=0.65, color="#1f78b4", label="isolated controls (n=%d)" % len(nc_scores))
    ax.hist(wc_scores, bins=bins, alpha=0.6, color="#7570b3", label="weak-signal chains (n=%d)" % len(wc_scores))
    ax.hist(emb_scores, bins=bins, alpha=0.6, color="#66a61e", label="embedded-control paths (n=%d)" % len(emb_scores))
    ax.hist(false_scores, bins=bins, alpha=0.6, color="#e08214", label="false leads (n=%d)" % len(false_scores))
    ax.hist(true_scores, bins=bins, alpha=0.6, color="#1b7837", label="true seeded paths (n=%d)" % len(true_scores))
    ax.axvline(TRIAGE_THRESHOLD, color="#b22222", lw=2, ls="--",
               label="triage threshold = %.0f" % TRIAGE_THRESHOLD)
    ax.set_xlabel("Review-priority score (0-100)"); ax.set_ylabel("Count of synthetic structures")
    _maybe_title(ax, "Review-priority score distribution by group - %s\n"
                 "true seeded paths score above the threshold; weak-signal structures and controls below"
                 % res.spec.name, fontsize=11)
    ax.legend(fontsize=8, frameon=True)
    ax.grid(axis="y", alpha=0.3)
    _footer(ax, fig)
    fig.tight_layout(rect=[0, 0.04, 1, 1])
    fig.savefig(out / "triage_score_distribution.png", dpi=DPI, bbox_inches="tight"); plt.close(fig)


# --------------------------------------------------------------------------- #
# Figure - descriptive score-band truth summary
# --------------------------------------------------------------------------- #
def fig_score_band_truth_summary(res, out: Path):
    buckets = res.metrics["rq4_review_priority"]["score_band_truth_summary"]
    labels = ["%g-%g" % (b["bucket_low"], b["bucket_high"]) for b in buckets]
    rates = [b["planted_positive_proportion"] for b in buckets]
    counts = [b["n_candidates"] for b in buckets]
    fig, ax = plt.subplots(figsize=(9.5, 6))
    bars = ax.bar(labels, rates, color="#3182bd", edgecolor="#1F3864", width=0.6)
    for bar, c in zip(bars, counts):
        ax.annotate("n=%d" % c, (bar.get_x() + bar.get_width() / 2, bar.get_height()),
                    textcoords="offset points", xytext=(0, 4), ha="center", fontsize=8)
    ax.axhline(0.5, color="#999999", lw=0.8, ls=":")
    ax.set_ylim(0, 1.08); ax.set_xlabel("Review-priority score bucket")
    ax.set_ylabel("Ground-truth rate (fraction seeded)")
    _maybe_title(ax, "Score-band truth summary - %s\nplanted-positive proportions by synthetic score bucket"
                 % res.spec.name, fontsize=11)
    ax.grid(axis="y", alpha=0.3)
    _footer(ax, fig)
    fig.tight_layout(rect=[0, 0.04, 1, 1])
    fig.savefig(out / "score_band_truth_summary.png", dpi=DPI, bbox_inches="tight"); plt.close(fig)


# --------------------------------------------------------------------------- #
# Figure - robustness: threshold sweep + weight-perturbation stability
# --------------------------------------------------------------------------- #
def fig_robustness(res, out: Path):
    if res.sweep_df is None or res.sensitivity_draws is None:
        return
    sw, sd = res.sweep_df, res.sensitivity_draws
    fig, (axA, axB) = plt.subplots(1, 2, figsize=(12.5, 5.4))

    axA.plot(sw["threshold"], sw["recall"], color="#1b7837", lw=2, marker="o", ms=3.2, label="recall")
    axA.plot(sw["threshold"], sw["precision"], color="#e08214", lw=2, marker="s", ms=3.2, label="precision")
    axA.plot(sw["threshold"], sw["specificity"], color="#1f78b4", lw=2, marker="^", ms=3.2, label="specificity")
    axA.axvline(TRIAGE_THRESHOLD, color="#b22222", lw=1.8, ls="--",
                label="chosen threshold = %.0f" % TRIAGE_THRESHOLD)
    axA.set_xlabel("Triage threshold"); axA.set_ylabel("Metric value")
    axA.set_ylim(-0.04, 1.06); axA.grid(alpha=0.3)
    axA.set_title("(a)" if PUBLICATION_MODE else
                  "(a) Threshold sweep: triage metrics at every cut-off", fontsize=10, loc="left" if PUBLICATION_MODE else "center", weight="bold" if PUBLICATION_MODE else "normal")
    axA.legend(fontsize=8, frameon=True, loc="center left")

    data = [sd["spearman_rho"], sd["kendall_tau_b"], sd["topk_jaccard"],
            sd["flagged_set_jaccard"], sd["recall"], sd["precision"]]
    bp = axB.boxplot(data, tick_labels=["Spearman\nrho", "Kendall\ntau-b", "top-k\nJaccard",
                                        "flagged-set\nJaccard", "recall@%.0f" % TRIAGE_THRESHOLD,
                                        "precision@%.0f" % TRIAGE_THRESHOLD],
                     patch_artist=True, widths=0.55, showfliers=True,
                     flierprops=dict(marker=".", ms=4, alpha=0.5))
    colors = ["#1b7837", "#7570b3", "#4d9221", "#5ab4ac", "#e08214", "#1f78b4"]
    for patch, color in zip(bp["boxes"], colors):
        patch.set_facecolor(color); patch.set_alpha(0.55)
    # Jittered points retain visibility when a metric is constant across draws.
    _rng = np.random.default_rng(0)
    for i, (col, color) in enumerate(zip(data, colors)):
        x = i + 1 + _rng.uniform(-0.16, 0.16, size=len(col))
        axB.scatter(x, col, s=4, color=color, alpha=0.25, zorder=3, linewidths=0)
    if not PUBLICATION_MODE:
        axB.text(0.02, 0.035, "Spearman and Kendall quantify complete-ranking stability; top-k and\n"
                 "threshold metrics describe membership and cut-off sensitivity",
                 transform=axB.transAxes, fontsize=7, color="#555555")
    axB.set_ylim(-0.04, 1.06); axB.grid(axis="y", alpha=0.3)
    axB.set_ylabel("Metric value across perturbed weightings")
    n_d = len(sd)
    axB.set_title("(b)" if PUBLICATION_MODE else
                  "(b) Weight perturbation: %d draws, each weight x U(0.8, 1.2)" % n_d, fontsize=10, loc="left" if PUBLICATION_MODE else "center", weight="bold" if PUBLICATION_MODE else "normal")

    _maybe_suptitle(fig, "Robustness of the review-priority triage rule - %s\nconclusions do not hinge on "
                 "the exact threshold or weight values" % res.spec.name, fontsize=11)
    _footer(axB, fig)
    fig.tight_layout(rect=[0, 0.045, 1, 0.92])
    fig.savefig(out / "robustness_threshold_sweep.png", dpi=DPI, bbox_inches="tight"); plt.close(fig)


def fig_active_noise_challenge(res, out: Path):
    """Visualise the observed burden created by connected active-network noise."""
    active = res.metrics.get("active_noise_validation", {})
    if not active.get("n_active_noise_edges", 0):
        return
    r1 = res.metrics["rq1_path_recovery"]
    before = active["candidate_paths_before_active_noise"]
    after = active["candidate_paths_after_active_noise"]
    active_candidates = active["n_candidate_paths_using_active_noise"]
    active_false_positives = active["n_high_priority_active_noise_false_positives"]

    fig, (ax_a, ax_b) = plt.subplots(1, 2, figsize=(11.5, 5.2))
    bars = ax_a.bar(["before\nactive noise", "after\nactive noise"], [before, after],
                    color=["#9ecae1", "#3182bd"], edgecolor="#1f4e79")
    for bar, value in zip(bars, [before, after]):
        ax_a.text(bar.get_x() + bar.get_width() / 2, value, str(value), ha="center", va="bottom", fontsize=9)
    ax_a.set_ylabel("Enumerated funder-to-terminal candidates")
    ax_a.set_title("(a)" if PUBLICATION_MODE else "(a) Candidate burden after connected active noise",
                   fontsize=10, loc="left" if PUBLICATION_MODE else "center",
                   weight="bold" if PUBLICATION_MODE else "normal")
    ax_a.grid(axis="y", alpha=0.3)

    labels = ["seeded\ntrue paths", "active-noise\ncandidates", "active-noise\nhigh-priority FPs"]
    values = [int(r1["tp"]), active_candidates, active_false_positives]
    colors = ["#1b7837", "#5ab4ac", "#d95f02"]
    bars = ax_b.bar(labels, values, color=colors, edgecolor="#444444")
    for bar, value in zip(bars, values):
        ax_b.text(bar.get_x() + bar.get_width() / 2, value, str(value), ha="center", va="bottom", fontsize=9)
    ax_b.set_ylabel("Candidate count")
    ax_b.set_title("(b)" if PUBLICATION_MODE else "(b) Retained adverse challenge result",
                   fontsize=10, loc="left" if PUBLICATION_MODE else "center",
                   weight="bold" if PUBLICATION_MODE else "normal")
    ax_b.grid(axis="y", alpha=0.3)
    if not PUBLICATION_MODE:
        ax_b.text(0.02, 0.02, "final high-priority precision = %.4f; active-noise edges = %d" %
                  (r1["precision"], active["n_active_noise_edges"]), transform=ax_b.transAxes,
                  fontsize=7, color="#555555")
    _maybe_suptitle(fig, "Connected active-network noise challenge - %s" % res.spec.name, fontsize=11)
    _footer(ax_b, fig)
    fig.tight_layout(rect=[0, 0.045, 1, 0.92])
    fig.savefig(out / "active_noise_challenge.png", dpi=DPI, bbox_inches="tight")
    plt.close(fig)

def generate_all_figures(res, path_audit, out: Path) -> None:
    fig_workflow(out)
    fig_full(res, out)
    fig_paths(res, out)
    fig_negative_controls(res, out)
    fig_entity_resolution(res, out)
    fig_score_distribution(res, out)
    fig_score_band_truth_summary(res, out)
    fig_robustness(res, out)
    fig_active_noise_challenge(res, out)
