#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
make_v2_figures.py
==================

Builds the manuscript figures (Frontiers format: 180 mm wide, 300 dpi, RGB,
PNG + TIFF) from the machine-written outputs of Benchmark A and Benchmark B.
Synthetic data only. Run after ``generate_synthetic_graph.py --all`` and
``run_v2_benchmark.py``.

    python make_v2_figures.py
"""
from __future__ import annotations

import shutil
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import numpy as np
import pandas as pd
from PIL import Image

import frontg_v2_methods as M
from frontg_v2_generator import REGIME_ORDER

ROOT = Path(__file__).resolve().parent
B = ROOT / "benchmark_B"
OUT = ROOT / "figures_for_submission"
W = 180 / 25.4                         # 180 mm in inches

# Reference categorical palette (validated order; see dataviz palette): colour = method family
FAMILY = {"frontg": "#2a78d6", "heuristic": "#8a8984", "learned": "#eb6834", "hybrid": "#1baf7a"}
METHOD_FAMILY = {"frontg": "frontg", "frontg_no_elig_no_gate": "frontg", "frontg_tuned": "frontg",
                 "frontg_no_elig": "frontg", "mean_grade": "heuristic", "centrality": "heuristic",
                 "logreg_path": "learned", "logreg": "learned", "gbm": "learned",
                 "gbm_oracle": "learned", "gbm_elig": "hybrid"}
SHORT = {"frontg": "FrontG (published)", "frontg_no_elig": "FrontG − eligibility",
         "frontg_no_elig_no_gate": "FrontG − eligibility − gate", "frontg_tuned": "FrontG, tuned threshold",
         "mean_grade": "Mean evidence grade", "centrality": "Path centrality",
         "logreg_path": "Log. regression (FrontG features)", "logreg": "Log. regression (all features)",
         "gbm": "Gradient boosting", "gbm_elig": "Gradient boosting + eligibility",
         "gbm_oracle": "Gradient boosting, in-regime*"}
REGIME_LABEL = {"base": "Base", "hidden_funding": "Hidden funding", "weak_coordination": "Weak-signal coordination",
                "documentary_decoys": "Documentary decoys", "hub_background": "Hub background",
                "community_background": "Community background"}
SHOW = ["frontg", "frontg_no_elig_no_gate", "frontg_tuned", "mean_grade", "centrality",
        "logreg_path", "logreg", "gbm", "gbm_elig", "gbm_oracle"]
INK, INK2, GRID = "#0b0b0b", "#52514e", "#e4e3df"

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 8, "axes.titlesize": 8.5, "axes.labelsize": 8,
    "xtick.labelsize": 7.5, "ytick.labelsize": 7.5, "legend.fontsize": 7.5,
    "axes.edgecolor": INK2, "axes.labelcolor": INK, "xtick.color": INK2, "ytick.color": INK2,
    "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True,
    "grid.color": GRID, "grid.linewidth": 0.6, "axes.axisbelow": True, "savefig.dpi": 300,
})


def save(fig, n: int) -> None:
    OUT.mkdir(exist_ok=True)
    png = OUT / f"Figure_{n}.png"
    fig.savefig(png, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    Image.open(png).convert("RGB").save(OUT / f"Figure_{n}.tif", dpi=(300, 300), compression="tiff_lzw")


def copy_as(src: Path, n: int) -> None:
    OUT.mkdir(exist_ok=True)
    shutil.copy(src, OUT / f"Figure_{n}.png")
    Image.open(src).convert("RGB").save(OUT / f"Figure_{n}.tif", dpi=(300, 300), compression="tiff_lzw")


def panel(ax, letter: str) -> None:
    ax.text(-0.02, 1.04, letter, transform=ax.transAxes, fontsize=10, fontweight="bold",
            va="bottom", ha="right", color=INK)


# --------------------------------------------------------------------------- #
def fig1_design() -> None:
    fig, ax = plt.subplots(figsize=(W, 3.6))
    ax.set_xlim(0, 101); ax.set_ylim(0, 56); ax.axis("off")

    def box(x, y, w, h, title, lines, edge, face, dashed=False):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3,rounding_size=1.0",
                                    lw=1.1, ec=edge, fc=face, ls="--" if dashed else "-"))
        ax.text(x + 1.2, y + h - 1.6, title, ha="left", va="top", fontsize=7.4, fontweight="bold", color=edge)
        for i, ln in enumerate(lines):
            ax.text(x + 1.2, y + h - 6.4 - i * 3.6, ln, ha="left", va="top", fontsize=6.0, color=INK)

    def arrow(x0, y0, x1, y1, dashed=False):
        ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                    arrowprops=dict(arrowstyle="-|>", lw=1.0, color=INK2, ls="--" if dashed else "-"))

    box(0.5, 6, 21, 46, "FrontG (method)",
        ["Path score, 0–100,", "fixed expert weights", "Supporting-signal gate", "Threshold 60",
         "Eligibility rule: funding", "edge and weakest hop", "grade ≥ 2", "Three-zone entity", "resolution", "Per-term audit trail"],
        "#1b3a6b", "#f3f6fb")
    box(26, 30, 33, 22, "Benchmark A: specification",
        ["Fixed planted templates, three scales", "Five acceptance criteria",
         "Exact score bounds by enumeration", "Threshold sweep; weight perturbation"], "#2a78d6", "#f3f6fb")
    box(26, 2, 33, 25, "Benchmark B: latent truth",
        ["True and decoy pathways drawn from", "overlapping evidence distributions",
         "Six regimes (hidden funding, hubs, ...)", "Separability sweep; nine comparators",
         "Adversarial entity-resolution set"], "#b8560f", "#fdf5ef")
    box(63.5, 14, 17, 26, "Expert review",
        ["Confidential queue;", "every flag is a", "prompt for review,", "never a finding"], "#7a5a00", "#fdf8ec")
    box(84, 14, 15.8, 26, "Future use",
        ["Only after ethics,", "legal and data-", "protection review", "and Article 5.3", "governance"],
        "#6b6a66", "#fafaf9", dashed=True)
    arrow(22, 41, 25.6, 41); arrow(22, 14.5, 25.6, 14.5)
    arrow(59.4, 27, 63.1, 27); arrow(80.9, 27, 83.6, 27, dashed=True)
    ax.text(99.5, 0.5, "All entities, relations and names are synthetic.", ha="right", va="bottom",
            fontsize=6.2, style="italic", color=INK2)
    save(fig, 1)


# --------------------------------------------------------------------------- #
def fig4_learnability() -> None:
    d = pd.read_csv(B / "diagnostic_learnability.csv")
    rows = []
    for _, r in d.iterrows():
        if r["benchmark"].startswith("A"):
            lab = f"A: train {r['train']} → test {r['test']}"
        elif "topology" in r["model"]:
            lab = "B: topology-only probe"
        else:
            lab = "B: evidence features"
        rows.append((lab, r["auprc"], r["prevalence"], r["benchmark"].startswith("A")))
    fig, ax = plt.subplots(figsize=(W * 0.62, 2.4))
    y = np.arange(len(rows))[::-1]
    for yi, (lab, a, p, isA) in zip(y, rows):
        ax.barh(yi, a, height=0.55, color="#2a78d6" if isA else "#eb6834", zorder=2)
        ax.plot([p, p], [yi - 0.36, yi + 0.36], color=INK, lw=1.4, zorder=3)
        ax.text(a + 0.015, yi, f"{a:.2f}", va="center", fontsize=7, color=INK)
    ax.set_yticks(y); ax.set_yticklabels([r[0] for r in rows])
    ax.set_xlim(0, 1.1); ax.set_xlabel("AUPRC of a gradient-boosting learner on held-out data")
    ax.plot([], [], color=INK, lw=1.4, label="prevalence (chance AUPRC)")
    ax.legend(loc="lower right", frameon=False)
    ax.grid(axis="y", visible=False)
    save(fig, 4)


# --------------------------------------------------------------------------- #
def fig5_auprc() -> None:
    s = pd.read_csv(B / "summary_by_regime_method.csv")
    fig, axes = plt.subplots(2, 3, figsize=(W, 4.6), sharex=True, sharey=True)
    for ax, reg, letter in zip(axes.flat, REGIME_ORDER, "ABCDEF"):
        sub = s[s["regime"] == reg].set_index("method")
        y = np.arange(len(SHOW))[::-1]
        for yi, m in zip(y, SHOW):
            r = sub.loc[m]
            c = FAMILY[METHOD_FAMILY[m]]
            ax.plot([r["auprc_lo"], r["auprc_hi"]], [yi, yi], color=c, lw=1.6, solid_capstyle="butt")
            ax.plot(r["auprc_mean"], yi, "o", ms=4, color=c, zorder=3)
        prev = float(sub["mean_prevalence"].iloc[0])
        ax.axvline(prev, color=INK2, lw=0.8, ls=":")
        ax.set_title(REGIME_LABEL[reg], loc="left", color=INK)
        panel(ax, letter)
        ax.set_yticks(y); ax.set_yticklabels([SHORT[m] for m in SHOW])
        ax.grid(axis="y", visible=False)
        ax.set_xlim(0, 0.75)
    fig.supxlabel("AUPRC (mean and 95% bootstrap CI over 100 test instances)", fontsize=8, y=0.06)
    handles = [plt.Line2D([], [], marker="o", ls="-", color=FAMILY[k], label=l) for k, l in
               [("frontg", "FrontG and ablations"), ("heuristic", "Unlearned heuristics"),
                ("learned", "Learned models"), ("hybrid", "Learned + FrontG eligibility")]]
    handles.append(plt.Line2D([], [], color=INK2, ls=":", label="prevalence"))
    fig.legend(handles=handles, loc="lower center", ncol=5, frameon=False, bbox_to_anchor=(0.55, -0.03))
    fig.tight_layout(rect=(0, 0.07, 1, 1))
    save(fig, 5)


# --------------------------------------------------------------------------- #
def fig6_safety() -> None:
    inst = pd.read_csv(B / "instance_metrics.csv")
    g = inst.groupby("method")
    n_inst = g["seed"].count()
    met = pd.DataFrame({
        "low": g["n_low_floor_flags"].sum() / n_inst,
        "weak": g["n_weak_evidence_flags"].sum() / n_inst,
        "g1": g["n_bystander_g1_flags"].sum() / g["n_bystander_g1_paths"].sum(),
        "g2": g["n_bystander_g2_flags"].sum() / g["n_bystander_g2_paths"].sum(),
        "g3": g["n_bystander_g3_flags"].sum() / g["n_bystander_g3_paths"].sum(),
        "hid": g["tp_funding_hidden"].sum() / g["n_true_funding_hidden"].sum(),
    })
    met.to_csv(B / "safety_pooled_all_regimes.csv")
    show = [m for m in SHOW if m != "centrality"]
    panels = [("low", "Flags with a grade ≤1 hop\n(per instance)", None),
              ("weak", "Weak-evidence-only flags\n(per instance)", None),
              ("g1", "Bystander paths flagged\n(grade-1 attachment)", (0, 1)),
              ("g2", "Bystander paths flagged\n(grade-2 attachment)", (0, 1)),
              ("g3", "Bystander paths flagged\n(grade-3 attachment)", (0, 1)),
              ("hid", "Recall of pathways with\nundisclosed funding", (0, 1))]
    cnt = {m_: (int(g["n_bystander_g1_flags"].sum()[m_]), int(g["n_bystander_g1_paths"].sum()[m_]))
           for m_ in n_inst.index}
    fig, axes = plt.subplots(2, 3, figsize=(W, 5.0), sharey=True)
    axes = axes.flatten()
    y = np.arange(len(show))[::-1]
    for ax, (col, title, lim), letter in zip(axes, panels, "ABCDEF"):
        vals = met.loc[show, col].values
        ax.barh(y, vals, height=0.62, color=[FAMILY[METHOD_FAMILY[m]] for m in show], zorder=2)
        top = max(vals.max(), 1e-9) if lim is None else lim[1]
        for yi, v in zip(y, vals):
            m_ = show[len(show) - 1 - int(yi)]
            if col == "g1":
                f_, n_ = cnt[m_]
                txt = f"{int(f_)}/{int(n_)}"
            else:
                txt = f"{v:.2f}" if lim else (f"{v:.1f}" if v >= 0.05 else ("0" if v == 0 else f"{v:.2f}"))
            ax.text(v + top * 0.03, yi, txt, va="center", fontsize=6.3, color=INK)
        ax.set_xlim(0, (lim[1] if lim else top) * 1.38)
        ax.set_title(f"{letter}   {title}", fontsize=7.2, loc="left", color=INK)
        ax.grid(axis="y", visible=False)
        ax.tick_params(axis="x", labelsize=6.5)
    for k in (0, 3):
        axes[k].set_yticks(y); axes[k].set_yticklabels([SHORT[m] for m in show])
    fig.text(0.5, -0.01, "Pooled over all six regimes (600 test instances). Path centrality omitted "
             "(flags nearly every candidate).", ha="center", fontsize=6.5, color=INK2)
    fig.tight_layout(w_pad=0.8, h_pad=1.6)
    save(fig, 6)


# --------------------------------------------------------------------------- #
def fig7_separability() -> None:
    s = pd.read_csv(B / "separability_summary.csv")
    meths = ["frontg", "mean_grade", "logreg_path", "gbm", "gbm_elig"]
    style = {"frontg": ("#2a78d6", "-", "o"), "mean_grade": ("#8a8984", "-", "s"),
             "logreg_path": ("#eda100", "-", "D"), "gbm": ("#eb6834", "-", "^"),
             "gbm_elig": ("#1baf7a", "-", "v")}
    fig, axes = plt.subplots(1, 3, figsize=(W, 2.9))
    specs = [("auprc_mean", "AUPRC (mean, 95% CI)", "auprc_lo", "auprc_hi"),
             (None, "Bystander paths flagged\n(grade-2 or grade-3 attachment)", None, None),
             ("n_low_floor_flags", "Flags with a grade ≤1 hop\n(total over 100 instances)", None, None)]
    for ax, (col, lab, lo, hi), letter in zip(axes, specs, "ABC"):
        for m in meths:
            sub = s[s["method"] == m].sort_values("lambda")
            c, ls, mk = style[m]
            if col is None:
                v = ((sub["n_bystander_g2_flags"] + sub["n_bystander_g3_flags"])
                     / (sub["n_bystander_g2_paths"] + sub["n_bystander_g3_paths"])).values
            else:
                v = sub[col].values
            ax.plot(sub["lambda"], v, ls=ls, color=c, marker=mk, ms=4, lw=1.6, label=SHORT[m],
                    mec="white", mew=0.6)
            if lo:
                ax.fill_between(sub["lambda"], sub[lo], sub[hi], color=c, alpha=0.15, lw=0)
        if col == "auprc_mean":
            prev = s.groupby("lambda")["mean_prevalence"].first()
            ax.plot(prev.index, prev.values, color=INK2, ls=":", lw=1, label="prevalence")
        ax.set_title(f"{letter}   {lab}", fontsize=7.2, loc="left", color=INK)
        ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
    axes[0].set_ylim(0, 0.8)
    h, l = axes[0].get_legend_handles_labels()
    fig.supxlabel("Separability λ (0 = decoys observed exactly like true pathways; 1 = well separated)",
                  fontsize=7.5, y=0.13)
    fig.legend(h, l, loc="lower center", ncol=3, frameon=False, bbox_to_anchor=(0.5, -0.02))
    fig.tight_layout(rect=(0, 0.15, 1, 1))
    save(fig, 7)


# --------------------------------------------------------------------------- #
def fig8_er() -> None:
    import frontg_er_challenge as ER
    bc = pd.read_csv(B / "er_challenge_by_category.csv")
    ov = pd.read_csv(B / "er_challenge_overall.csv").set_index("rule")
    rules = [("token_jaccard_v1", "Published v1 rule (token Jaccard)"),
             ("normalised_token_acronym", "Normalised tokens + acronym referral")]
    cats = ER.ALIAS_CATS + ER.DISTINCT_CATS
    nice = {c: c.replace("_", " ") for c in cats}
    fig, axes = plt.subplots(1, 2, figsize=(W, 3.0), sharey=True)
    y = np.arange(len(cats))[::-1]
    cols = {"auto_merge": "#2a78d6", "refer": "#eda100", "keep_separate": "#d6d5d0"}
    for ax, (rule, title), letter in zip(axes, rules, "AB"):
        sub = bc[bc["rule"] == rule].set_index("category").loc[cats]
        left = np.zeros(len(cats))
        for k, lab in [("auto_merge", "auto-merge"), ("refer", "refer to human"), ("keep_separate", "keep separate")]:
            ax.barh(y, sub[k].values, left=left, height=0.66, color=cols[k], label=lab,
                    edgecolor="white", linewidth=1.0, zorder=2)
            left += sub[k].values
        for yi, c in zip(y, cats):
            if c in ER.DISTINCT_CATS and sub.loc[c, "auto_merge"] > 0:
                ax.text(1.02, yi, "false merges", va="center", fontsize=6.3, color="#c0392b", fontweight="bold")
        o = ov.loc[rule]
        ax.set_title(f"{letter}   {title}\nfalse merges {int(o['false_merges'])}/{int(o['n_distinct_pairs'])} · "
                     f"auto-merge recall {o['auto_merge_recall']:.2f} · referral {o['referral_rate']:.2f}",
                     fontsize=6.6, loc="left", color=INK)
        ax.axhline(y[len(ER.ALIAS_CATS) - 1] - 0.5, color=INK2, lw=0.8)
        ax.set_xlim(0, 1.3); ax.set_xticks([0, 0.5, 1.0])
        ax.set_xlabel("Share of test pairs")
        ax.grid(axis="y", visible=False)
    axes[0].set_yticks(y)
    axes[0].set_yticklabels([("alias: " if c in ER.ALIAS_CATS else "distinct: ") + nice[c] for c in cats])
    h, l = axes[0].get_legend_handles_labels()
    fig.legend(h, l, loc="lower center", ncol=3, frameon=False, bbox_to_anchor=(0.55, -0.04))
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    save(fig, 8)


def main() -> None:
    fig1_design()
    # Benchmark A figures: clean publication versions archived in figures_benchmark_A/
    A = ROOT / "figures_benchmark_A"
    copy_as(A / "score_distribution.png", 2)
    copy_as(A / "robustness.png", 3)
    fig4_learnability()
    fig5_auprc()
    fig6_safety()
    fig7_separability()
    fig8_er()
    for i, name in enumerate(["planted_paths", "entity_resolution", "bystanders", "active_noise"], 1):
        shutil.copy(A / f"{name}.png", OUT / f"Figure_S{i}.png")
    print(f"Figures written to {OUT}")


if __name__ == "__main__":
    main()
