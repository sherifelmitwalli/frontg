#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
frontg_config.py
================

Central configuration for the synthetic validation harness. All values here are
abstract and synthetic. There are no real entities, no live APIs, and no
real-world data anywhere in this project.

This module holds:
  * controlled vocabularies (node classes, edge types, evidence-grade mapping);
  * the five-tier evidence-grading matrix;
  * the transparent review-priority score weights;
  * entity-resolution three-zone decision thresholds;
  * robustness-analysis constants (threshold sweep, weight sensitivity);
  * deterministic scenario specifications (small / medium / stress);
  * visual styling (per-class colours and marker shapes, per-grade edge styles).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List

# --------------------------------------------------------------------------- #
# Reproducibility / triage threshold
# --------------------------------------------------------------------------- #
DEFAULT_SEED: int = 42
TRIAGE_THRESHOLD: float = 60.0   # transparent review-priority cut-off (0..100)

# Entity resolution uses a three-zone (Fellegi-Sunter-style) decision rule:
#   similarity >= ER_AUTO_MERGE_THRESHOLD          -> auto_merge
#   ER_REFER_THRESHOLD <= similarity < AUTO_MERGE  -> refer_to_human (review queue)
#   similarity < ER_REFER_THRESHOLD                -> keep_separate
# The automated rule never merges in the ambiguous zone; a human decides.
ER_AUTO_MERGE_THRESHOLD: float = 0.60
ER_REFER_THRESHOLD: float = 0.40
MERGE_THRESHOLD: float = ER_AUTO_MERGE_THRESHOLD   # backward-compatible alias

# Robustness-analysis constants (RQ5)
THRESHOLD_SWEEP_STEP: int = 1          # evaluate every integer threshold 0..100
SENSITIVITY_N_DRAWS: int = 200         # weight-perturbation draws
SENSITIVITY_REL_RANGE: float = 0.20    # each weight multiplied by U(1-r, 1+r)
SENSITIVITY_SEED: int = 4242           # deterministic RNG for the perturbations

# --------------------------------------------------------------------------- #
# Controlled vocabularies (all abstract / synthetic)
# --------------------------------------------------------------------------- #
NODE_CLASSES: List[str] = [
    "Funder", "Intermediary", "Proxy", "Campaign", "Event",
    "Report", "MediaOutlet", "SocialAccount", "IndependentControl",
]

# Edge type -> default synthetic evidence grade (0..4).
EDGE_TYPE_GRADE: Dict[str, int] = {
    "no_known_link": 0,          # negative control / explicit non-link
    "co_occurs_with": 1,         # weak co-occurrence only
    "shares_link": 2,            # repeated public co-occurrence / shared links
    "uses_similar_language": 2,  # textual similarity signal
    "amplifies": 2,              # amplification signal
    "cites": 3,                  # documentary relationship
    "publishes": 3,              # documentary relationship
    "speaks_at": 3,              # documentary relationship (participation)
    "hosts": 3,                  # documentary relationship (participation)
    "partners_with": 3,          # documentary relationship (partnership)
    "funds": 4,                  # direct synthetic funding / formal link
}

# Five-tier synthetic evidence grading matrix.
EVIDENCE_GRADING_MATRIX: List[Dict[str, object]] = [
    {"grade": 0, "label": "No link / negative control",
     "description": "No known relationship, or an explicit negative-control non-link.",
     "example_edge_types": "no_known_link",
     "example_snippet": "No documented association observed between the two synthetic entities.",
     "review_weight": 0.0},
    {"grade": 1, "label": "Weak co-occurrence only",
     "description": "Entities mentioned together once in a synthetic context with no further signal.",
     "example_edge_types": "co_occurs_with",
     "example_snippet": "During Phase_01 the two synthetic entities were listed in the same abstract index.",
     "review_weight": 0.20},
    {"grade": 2, "label": "Repeated public co-occurrence or shared links",
     "description": "Repeated synthetic co-occurrence, shared links, amplification, or similar language.",
     "example_edge_types": "shares_link, uses_similar_language, amplifies",
     "example_snippet": "Across Phase_01 and Phase_02 the synthetic accounts repeatedly amplified the same abstract item.",
     "review_weight": 0.45},
    {"grade": 3, "label": "Documentary relationship",
     "description": "Synthetic event participation, report authorship, partnership, or co-publication.",
     "example_edge_types": "speaks_at, hosts, publishes, cites, partners_with",
     "example_snippet": "Intermediary_Alpha is recorded as a co-host of Event_Gamma alongside Proxy_Delta in Phase_02.",
     "review_weight": 0.75},
    {"grade": 4, "label": "Direct synthetic funding or formal organisational link",
     "description": "A direct synthetic funding relationship or a formal organisational link.",
     "example_edge_types": "funds",
     "example_snippet": "Funder_01 is recorded as providing synthetic funding to Intermediary_Alpha in Phase_01.",
     "review_weight": 1.00},
]

PHASES: List[str] = ["Phase_01", "Phase_02", "Phase_03", "Phase_04"]


# --------------------------------------------------------------------------- #
# Review-priority (triage) score weights
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class ScoreWeights:
    """Transparent, formula-based weights for the review-priority (triage) score.

    The score is an explicit, auditable weighted sum bounded to [0, 100]. It is a
    TRIAGE score for prioritising expert review only - never a probability of
    wrongdoing and never proof of anything.
    """
    w_funding_edge: float = 22.0       # direct synthetic funding edge present
    w_mean_grade: float = 30.0         # mean evidence grade along the path (0..4)
    w_min_grade: float = 16.0          # documentary continuity (weakest hop grade)
    w_evidence_types: float = 8.0      # number of independent evidence types
    w_temporal: float = 6.0            # temporal clustering of edges
    w_semantic: float = 4.0            # similar-language signal (supporting only)
    w_amplification: float = 5.0       # amplification signal (supporting only)
    w_cooccurrence: float = 4.0        # repeated actor co-occurrence (supporting)
    length_penalty: float = 2.0        # gentle penalty per hop beyond 3

    # normalisation constants
    grade_max: float = 4.0             # evidence grades run 0..4
    types_norm: float = 5.0            # normalising constant for evidence types


# --------------------------------------------------------------------------- #
# Scenario specifications (deterministic, fixed seeds)
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class ScenarioSpec:
    """Deterministic specification for one synthetic validation scenario."""
    key: str                     # small | medium | stress
    name: str                    # human-readable name
    folder: str                  # output sub-folder
    seed: int
    programmatic: bool           # False -> hand-seeded small graph
    n_proxy_paths: int = 0
    n_false_friend_pairs: int = 0
    n_alias_groups: int = 0
    n_negative_controls: int = 0
    n_embedded_controls: int = 0     # controls attached to the active graph by weak edges
    n_weak_chains: int = 0           # funder-reachable weak-signal-only chains (RQ5)
    n_false_leads: int = 0       # weaker funder-originated distractor paths
    n_weak_cooccur: int = 0      # weak co-occurrence noise edges
    n_semantic_distractors: int = 0  # similar-language-only noise edges
    n_amplify_distractors: int = 0   # amplification-only noise edges
    # Seeded, connected distractor edges inside the funder-reachable graph.
    n_active_weak_cooccur: int = 0
    n_active_shared_link: int = 0
    n_active_semantic: int = 0
    n_active_amplify: int = 0
    n_active_misleading_documentary: int = 0
    n_active_cross_path: int = 0
    n_filler_nodes: int = 0          # isolated/lightly-connected filler nodes
    target_nodes: int = 0
    target_edges_min: int = 0
    target_edges_max: int = 0
    replication_seeds: tuple = ()    # extra seeds for cross-seed replication


SCENARIOS: Dict[str, ScenarioSpec] = {
    "small": ScenarioSpec(
        key="small", name="Scenario A - Small proof-of-concept",
        folder="scenario_A_small", seed=42, programmatic=False,
        n_embedded_controls=2, n_weak_chains=2,
        target_nodes=40, target_edges_min=25, target_edges_max=45),
    "medium": ScenarioSpec(
        key="medium", name="Scenario B - Medium validation scenario",
        folder="scenario_B_medium", seed=142, programmatic=True,
        n_proxy_paths=12, n_false_friend_pairs=10, n_alias_groups=6,
        n_negative_controls=12, n_embedded_controls=6, n_weak_chains=6,
        n_false_leads=8, n_weak_cooccur=120,
        n_semantic_distractors=60, n_amplify_distractors=40,
        n_active_weak_cooccur=4, n_active_shared_link=4, n_active_semantic=3,
        n_active_amplify=3, n_active_misleading_documentary=4, n_active_cross_path=4,
        n_filler_nodes=24,
        target_nodes=150, target_edges_min=250, target_edges_max=400,
        replication_seeds=(142, 143, 144, 145, 146)),
    "stress": ScenarioSpec(
        key="stress", name="Scenario C - Larger stress-test scenario",
        folder="scenario_C_stress", seed=242, programmatic=True,
        n_proxy_paths=26, n_false_friend_pairs=18, n_alias_groups=12,
        n_negative_controls=24, n_embedded_controls=12, n_weak_chains=10,
        n_false_leads=16, n_weak_cooccur=560,
        n_semantic_distractors=260, n_amplify_distractors=200,
        n_active_weak_cooccur=10, n_active_shared_link=10, n_active_semantic=8,
        n_active_amplify=8, n_active_misleading_documentary=10, n_active_cross_path=10,
        n_filler_nodes=150,
        target_nodes=500, target_edges_min=1000, target_edges_max=2000,
        replication_seeds=(242, 243, 244)),
}

ALL_SCENARIO_KEYS = ["small", "medium", "stress"]


# --------------------------------------------------------------------------- #
# Visual styling
# --------------------------------------------------------------------------- #
# Consistent per-class colours and marker shapes used across every figure.
NODE_COLORS: Dict[str, str] = {
    "Funder": "#1b9e77", "Intermediary": "#d95f02", "Proxy": "#7570b3",
    "Campaign": "#e7298a", "Event": "#66a61e", "Report": "#e6ab02",
    "MediaOutlet": "#a6761d", "SocialAccount": "#444444", "IndependentControl": "#1f78b4",
}
NODE_SHAPES: Dict[str, str] = {
    "Funder": "s", "Intermediary": "o", "Proxy": "^", "Campaign": "D",
    "Event": "p", "Report": "h", "MediaOutlet": "v", "SocialAccount": "*",
    "IndependentControl": "X",
}
# Edge line styles keyed by evidence grade (0..4).
EDGE_GRADE_STYLES: Dict[int, Dict[str, object]] = {
    0: {"color": "#cfcfcf", "style": (0, (1, 3)), "width": 0.7, "label": "grade 0 - no/none"},
    1: {"color": "#bdbdbd", "style": (0, (2, 3)), "width": 0.9, "label": "grade 1 - weak co-occurrence"},
    2: {"color": "#fdae61", "style": (0, (4, 2)), "width": 1.3, "label": "grade 2 - shared link / amplify"},
    3: {"color": "#3182bd", "style": "solid", "width": 1.7, "label": "grade 3 - documentary"},
    4: {"color": "#b2182b", "style": "solid", "width": 2.6, "label": "grade 4 - direct funding"},
}

DISCLAIMER = ("All entities and relationships are synthetic and abstract. Outputs are "
              "indicators for expert human review only - not proof of misconduct, "
              "undisclosed conflicts of interest, hidden funding, or any wrongdoing.")
