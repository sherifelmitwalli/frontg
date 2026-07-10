#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_synthetic_graph.py
===========================

Synthetic validation harness for a human-in-the-loop network-analysis framework.

PURPOSE
-------
Validate the *logic* of a network-based triage framework against fully synthetic,
abstract topologies with KNOWN ground truth, BEFORE any possible real-world use.
The harness does NOT collect, infer, or assert anything about real people,
organisations, campaigns, funders, or social-media accounts. There are NO live
searches, NO API keys, NO crawling, and NO real-world data of any kind. All
entities are abstract (e.g. ``Funder_01``) and all evidence snippets are synthetic.

Outputs are *indicators for expert review* and *review-priority (triage) scores*.
They are explicitly NOT proof of misconduct, undisclosed conflicts of interest,
hidden funding, or any wrongdoing.

VALIDATION TASKS
----------------
RQ1  recover seeded multi-hop proxy paths;
RQ2  three-zone entity resolution (auto-merge / refer-to-human / keep-separate);
RQ3  negative controls: isolated (disconnected) AND embedded (weakly attached,
     funder-reachable) controls must stay below the triage threshold;
RQ4  transparent, auditable review-priority scoring and score-band truth summaries;
RQ5  robustness: weak-signal-only chains can never be flagged (analytic bound +
     seeded adversarial chains), gate ablation, threshold sweep, weight
     sensitivity, and a cross-seed consistency check.

ARCHITECTURAL REFERENCE
-----------------------
This file re-uses ONLY the architecture of an earlier search-and-crawl pipeline
and replaces every live component with a synthetic equivalent
(SearchAgent -> SyntheticEvidenceAgent, CrawlerAgent -> SyntheticCorpusGenerator,
EntityVerificationAgent -> SyntheticGroundTruthVerifier, ReportAgent ->
ValidationReportGenerator). The original code is not imported, executed, or modified.

USAGE
-----
    python generate_synthetic_graph.py --scenario small
    python generate_synthetic_graph.py --scenario medium
    python generate_synthetic_graph.py --scenario stress
    python generate_synthetic_graph.py --all              # + cross-seed consistency check
    python generate_synthetic_graph.py --all --output-dir .
    python generate_synthetic_graph.py --replications

Dependencies: networkx, pandas, numpy, matplotlib (figures) + standard library.
"""
from __future__ import annotations

import argparse
import dataclasses
import itertools
import json
from dataclasses import dataclass, field
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
import networkx as nx

import frontg_config as CFG
from frontg_config import (EDGE_TYPE_GRADE, EVIDENCE_GRADING_MATRIX, NODE_CLASSES,
                           PHASES, ScenarioSpec, ScoreWeights, SCENARIOS,
                           TRIAGE_THRESHOLD, ER_AUTO_MERGE_THRESHOLD,
                           ER_REFER_THRESHOLD, THRESHOLD_SWEEP_STEP,
                           SENSITIVITY_N_DRAWS, SENSITIVITY_REL_RANGE,
                           SENSITIVITY_SEED)
import frontg_metrics as MET

OUTPUT_DIR = Path(__file__).resolve().parent
TERMINAL_CLASSES = {"Campaign", "Report"}


# --------------------------------------------------------------------------- #
# Data classes
# --------------------------------------------------------------------------- #
@dataclass
class SyntheticNode:
    node_id: str
    node_class: str
    canonical_id: str
    surface_form: str
    is_independent_control: bool = False


@dataclass
class SyntheticEdge:
    source: str
    target: str
    edge_type: str
    evidence_snippet: str
    evidence_grade: int
    phase: str
    is_ground_truth: bool = False
    is_distractor: bool = False
    is_negative_control: bool = False
    is_active_noise: bool = False
    key: int = 0


# --------------------------------------------------------------------------- #
# Synthetic evidence agent (replaces SearchAgent)
# --------------------------------------------------------------------------- #
class SyntheticEvidenceAgent:
    """Formats deterministic synthetic evidence snippets. No network access."""

    TEMPLATES = {
        "funds": "Synthetic record: {s} is listed as providing funding to {t} during {ph}.",
        "partners_with": "Synthetic record: {s} is described as a partner of {t} during {ph}.",
        "hosts": "Synthetic record: {s} is listed as a host of {t} during {ph}.",
        "speaks_at": "Synthetic record: a representative of {s} is listed as speaking at {t} during {ph}.",
        "publishes": "Synthetic record: {s} is listed as the publisher of {t} during {ph}.",
        "cites": "Synthetic record: {s} cites {t} in an abstract document during {ph}.",
        "shares_link": "Synthetic record: {s} and {t} shared the same abstract link during {ph}.",
        "amplifies": "Synthetic record: {s} repeatedly amplified output attributed to {t} during {ph}.",
        "uses_similar_language": "Synthetic record: {s} used wording closely similar to {t} during {ph}.",
        "co_occurs_with": "Synthetic record: {s} and {t} co-occurred in one abstract index during {ph}.",
        "no_known_link": "Synthetic record: no documented association observed between {s} and {t}.",
    }

    def snippet(self, source: str, target: str, edge_type: str, phase: str) -> str:
        tmpl = self.TEMPLATES.get(edge_type, "Synthetic record: {s} relates to {t} during {ph}.")
        return tmpl.format(s=source, t=target, ph=phase)


# --------------------------------------------------------------------------- #
# Synthetic corpus / topology generator (replaces CrawlerAgent)
# --------------------------------------------------------------------------- #
class SyntheticCorpusGenerator:
    """Builds an abstract synthetic directed multigraph and all ground-truth keys.

    Supports a hand-seeded ``small`` scenario (identical to the original proof of
    concept) and programmatically scaled ``medium`` / ``stress`` scenarios with
    the same structural ingredients at larger sizes.
    """

    def __init__(self, spec: ScenarioSpec):
        self.spec = spec
        self.seed = spec.seed
        self.rng = np.random.default_rng(spec.seed)
        self.evidence = SyntheticEvidenceAgent()
        self.nodes: Dict[str, SyntheticNode] = {}
        self.edges: List[SyntheticEdge] = []
        self.ground_truth_paths: List[Dict[str, Any]] = []
        self.entity_resolution_rows: List[Dict[str, Any]] = []
        self.negative_controls: List[Dict[str, Any]] = []
        self.weak_signal_chains: List[Dict[str, Any]] = []
        self.weak_chain_funders: set = set()
        self.embedded_control_nodes: set = set()
        self._edge_keys: Dict[Tuple[str, str], int] = {}
        self._filler: List[str] = []

    # -- helpers ------------------------------------------------------------ #
    def add_node(self, node_id: str, node_class: str, canonical_id: Optional[str] = None,
                 surface_form: Optional[str] = None, is_independent_control: bool = False) -> None:
        if node_id in self.nodes:
            return
        self.nodes[node_id] = SyntheticNode(
            node_id=node_id, node_class=node_class, canonical_id=canonical_id or node_id,
            surface_form=surface_form or node_id, is_independent_control=is_independent_control)

    def add_edge(self, source: str, target: str, edge_type: str, phase: Optional[str] = None,
                 is_ground_truth: bool = False, is_distractor: bool = False,
                 is_negative_control: bool = False, is_active_noise: bool = False) -> None:
        if phase is None:
            phase = PHASES[int(self.rng.integers(0, len(PHASES)))]
        grade = EDGE_TYPE_GRADE[edge_type]
        snippet = self.evidence.snippet(source, target, edge_type, phase)
        key = self._edge_keys.get((source, target), 0)
        self._edge_keys[(source, target)] = key + 1
        self.edges.append(SyntheticEdge(
            source=source, target=target, edge_type=edge_type, evidence_snippet=snippet,
            evidence_grade=grade, phase=phase, is_ground_truth=is_ground_truth,
            is_distractor=is_distractor, is_negative_control=is_negative_control,
            is_active_noise=is_active_noise, key=key))

    def _record_path(self, path_id: str, node_seq, edge_types) -> None:
        grades = [EDGE_TYPE_GRADE[e] for e in edge_types]
        self.ground_truth_paths.append({
            "path_id": path_id,
            "node_sequence": " -> ".join(n for n, _ in node_seq),
            "edge_types": " -> ".join(edge_types),
            "path_length": len(edge_types),
            "evidence_grades": " -> ".join(str(g) for g in grades),
            "max_evidence_grade": max(grades), "mean_evidence_grade": round(float(np.mean(grades)), 3),
            "expected_review_priority": "high", "is_true_seeded_proxy_path": True})

    def _seed_one_path(self, path_id: str, node_seq, edge_types) -> None:
        for nid, ncls in node_seq:
            self.add_node(nid, ncls)
        for i, etype in enumerate(edge_types):
            phase = PHASES[min(i // 2, len(PHASES) - 1)]   # temporal clustering
            self.add_edge(node_seq[i][0], node_seq[i + 1][0], etype, phase=phase, is_ground_truth=True)
        self._record_path(path_id, node_seq, edge_types)

    # -- embedded negative controls (RQ3b) ----------------------------------- #
    def _add_embedded_control(self, idx: int, attach_node: str) -> None:
        """An IndependentControl actor attached to the ACTIVE graph by weak
        (grade <= 2) edges only, so that it is reachable from a funder and DOES
        appear inside enumerated candidate paths. This makes the negative-control
        test non-trivial: the control can be flagged in principle, and the test
        is whether the score keeps it below the triage threshold."""
        ec = f"EmbeddedControl_{idx:02d}"
        term_cls = "Campaign" if idx % 2 == 0 else "Report"
        term = f"{term_cls}_EC{idx:02d}"
        self.add_node(ec, "IndependentControl", is_independent_control=True)
        self.add_node(term, term_cls)
        e1 = "co_occurs_with"
        e2 = "shares_link" if idx % 2 == 0 else "co_occurs_with"
        self.add_edge(attach_node, ec, e1, phase="Phase_02",
                      is_distractor=True, is_negative_control=True)
        self.add_edge(ec, term, e2, phase="Phase_03",
                      is_distractor=True, is_negative_control=True)
        self.embedded_control_nodes.add(ec)
        self.negative_controls.append({
            "control_id": f"EC_{idx:02d}", "control_type": "embedded",
            "nodes": f"{ec}; {term}", "attached_to": attach_node,
            "edges": f"{attach_node}-[{e1}]->{ec}; {ec}-[{e2}]->{term}",
            "expected_priority": "below threshold", "expected_flag_status": "do_not_flag"})

    # -- weak-signal-only chains (RQ5) --------------------------------------- #
    def _add_weak_chain(self, idx: int) -> None:
        """A funder-reachable chain built ONLY from weak signals (shared links,
        amplification, similar language, co-occurrence; every hop grade <= 2,
        no funding edge). The answer key requires that such chains are never
        flagged: weak signals alone must not create review priority."""
        fu = f"Funder_W{idx:02d}"
        self.add_node(fu, "Funder")
        self.weak_chain_funders.add(fu)
        if idx % 2 == 0:   # 3-hop variant, all grade 2, same phase (max temporal)
            nseq = [(fu, "Funder"), (f"SocialAccount_WC{idx:02d}", "SocialAccount"),
                    (f"MediaOutlet_WC{idx:02d}", "MediaOutlet"),
                    (f"Campaign_WC{idx:02d}", "Campaign")]
            et = ["shares_link", "amplifies", "uses_similar_language"]
            phases = ["Phase_01", "Phase_01", "Phase_01"]
        else:              # 4-hop variant including a grade-1 hop
            nseq = [(fu, "Funder"), (f"SocialAccount_WC{idx:02d}", "SocialAccount"),
                    (f"MediaOutlet_WC{idx:02d}", "MediaOutlet"),
                    (f"Proxy_WC{idx:02d}", "Proxy"), (f"Report_WC{idx:02d}", "Report")]
            et = ["co_occurs_with", "shares_link", "amplifies", "uses_similar_language"]
            phases = ["Phase_01", "Phase_01", "Phase_02", "Phase_02"]
        for nid, ncls in nseq:
            self.add_node(nid, ncls)
        for i, etype in enumerate(et):
            self.add_edge(nseq[i][0], nseq[i + 1][0], etype, phase=phases[i],
                          is_distractor=True)
        grades = [EDGE_TYPE_GRADE[e] for e in et]
        self.weak_signal_chains.append({
            "chain_id": f"WC_{idx:02d}",
            "node_sequence": " -> ".join(n for n, _ in nseq),
            "edge_types": " -> ".join(et),
            "evidence_grades": " -> ".join(str(g) for g in grades),
            "max_evidence_grade": max(grades),
            "expected_flag_status": "do_not_flag",
            "rationale": "weak signals only (every hop grade <= 2, no funding edge); "
                         "must remain below the triage threshold"})

    # ===================================================================== #
    #  SMALL scenario  (hand-seeded proof of concept, unchanged structure)
    # ===================================================================== #
    def _build_small(self) -> None:
        seeded = [
            ("GT_PATH_01", [("Funder_01", "Funder"), ("Intermediary_Alpha", "Intermediary"),
                            ("Proxy_X", "Proxy"), ("Campaign_Y", "Campaign")],
             ["funds", "partners_with", "hosts"]),
            ("GT_PATH_02", [("Funder_02", "Funder"), ("Intermediary_Beta", "Intermediary"),
                            ("Event_C", "Event"), ("Proxy_Z", "Proxy"), ("Report_Q", "Report")],
             ["funds", "hosts", "speaks_at", "publishes"]),
            ("GT_PATH_03", [("Funder_03", "Funder"), ("Intermediary_Gamma", "Intermediary"),
                            ("Proxy_W", "Proxy"), ("Campaign_V", "Campaign")],
             ["funds", "partners_with", "amplifies"]),
            ("GT_PATH_04", [("Funder_01", "Funder"), ("Intermediary_Delta", "Intermediary"),
                            ("Event_D", "Event"), ("Report_R", "Report")],
             ["funds", "hosts", "publishes"]),
        ]
        for pid, nseq, et in seeded:
            self._seed_one_path(pid, nseq, et)

        false_friends = [("Health_Alliance_A", "CANON_HA_A"), ("Health_Alliance_B", "CANON_HA_B"),
                         ("Public_Choice_Network", "CANON_PCN_1"), ("Public_Choices_Network", "CANON_PCN_2"),
                         ("Research_Forum_Alpha", "CANON_RF_1"), ("Research_Forums_Alpha", "CANON_RF_2")]
        for i, (surface, canon) in enumerate(false_friends, 1):
            self.add_node(surface, "Proxy", canonical_id=canon, surface_form=surface)
            self.entity_resolution_rows.append({
                "entity_id": f"ER_FF_{i:02d}", "surface_form": surface, "canonical_id": canon,
                "is_true_alias": False, "is_false_friend": True, "expected_merge_decision": "do_not_merge"})

        alias_groups = [("CANON_GAMMA", [("Intermediary_Gamma", "Intermediary"),
                                         ("Intermediary_Gamma_Group", "Intermediary"),
                                         ("Gamma_Intermediary_Network", "Intermediary")]),
                        ("CANON_OMEGA", [("Campaign_Omega", "Campaign"),
                                         ("Campaign_Omega_Initiative", "Campaign")])]
        ai = 1
        for canon, members in alias_groups:
            for surface, ncls in members:
                self.add_node(surface, ncls, canonical_id=canon, surface_form=surface)
                self.entity_resolution_rows.append({
                    "entity_id": f"ER_AL_{ai:02d}", "surface_form": surface, "canonical_id": canon,
                    "is_true_alias": True, "is_false_friend": False, "expected_merge_decision": "merge"})
                ai += 1

        controls = [
            ("NC_01", [("IndependentControl_01", "IndependentControl"), ("Event_Ind_01", "Event")],
             [("IndependentControl_01", "Event_Ind_01", "co_occurs_with")]),
            ("NC_02", [("IndependentControl_02", "IndependentControl"), ("Report_Ind_02", "Report")],
             [("IndependentControl_02", "Report_Ind_02", "no_known_link")]),
            ("NC_03", [("IndependentControl_03", "IndependentControl"),
                       ("SocialAccount_Ind_03", "SocialAccount"), ("MediaOutlet_Ind_03", "MediaOutlet")],
             [("IndependentControl_03", "SocialAccount_Ind_03", "no_known_link"),
              ("SocialAccount_Ind_03", "MediaOutlet_Ind_03", "co_occurs_with")]),
            ("NC_04", [("IndependentControl_04", "IndependentControl"), ("Campaign_Ind_04", "Campaign")],
             [("IndependentControl_04", "Campaign_Ind_04", "no_known_link")]),
        ]
        self._add_controls(controls)

        # embedded negative controls: weakly attached to the active structure,
        # so they appear in funder-originated candidate paths (RQ3b)
        for i, attach in enumerate(["Intermediary_Alpha", "Proxy_X"][:self.spec.n_embedded_controls]):
            self._add_embedded_control(i + 1, attach)

        # weak-signal-only chains (RQ5)
        for i in range(self.spec.n_weak_chains):
            self._add_weak_chain(i + 1)

        for nid, ncls in [("MediaOutlet_Theta", "MediaOutlet"), ("SocialAccount_Eta", "SocialAccount"),
                          ("SocialAccount_Iota", "SocialAccount"), ("Report_Sigma", "Report"),
                          ("Event_Kappa", "Event")]:
            self.add_node(nid, ncls)
        for s, t, et in [("MediaOutlet_Theta", "Report_Sigma", "cites"),
                         ("SocialAccount_Eta", "MediaOutlet_Theta", "amplifies"),
                         ("SocialAccount_Iota", "SocialAccount_Eta", "co_occurs_with"),
                         ("Event_Kappa", "Report_Sigma", "co_occurs_with"),
                         ("SocialAccount_Iota", "MediaOutlet_Theta", "uses_similar_language"),
                         ("Event_Kappa", "SocialAccount_Eta", "co_occurs_with")]:
            self.add_edge(s, t, et, is_distractor=True)
        for s, t, et in [("Intermediary_Beta", "Report_R", "co_occurs_with"),
                         ("Proxy_W", "Campaign_Y", "shares_link")]:
            if s in self.nodes and t in self.nodes:
                self.add_edge(s, t, et, is_distractor=True)

    def _add_controls(self, controls) -> None:
        for ctrl_id, node_seq, edge_seq in controls:
            for nid, ncls in node_seq:
                self.add_node(nid, ncls, is_independent_control=True)
            for s, t, et in edge_seq:
                self.add_edge(s, t, et, phase="Phase_01", is_distractor=True, is_negative_control=True)
            self.negative_controls.append({
                "control_id": ctrl_id, "control_type": "isolated",
                "nodes": "; ".join(n for n, _ in node_seq), "attached_to": "",
                "edges": "; ".join(f"{s}-[{et}]->{t}" for s, t, et in edge_seq),
                "expected_priority": 0.0, "expected_flag_status": "do_not_flag"})

    # ===================================================================== #
    #  SCALED scenarios (medium / stress) - programmatic, deterministic
    # ===================================================================== #
    ADJ = ["Health", "Public", "Civic", "Policy", "Wellness", "Reform", "Liberty", "Standards",
           "Data", "Citizen", "Research", "Market", "Consumer", "Global", "Regional", "National",
           "Open", "Future", "Common", "Progress", "Heritage", "Unity", "Frontier", "Summit",
           "Pioneer", "Anchor", "Beacon", "Cardinal", "Meridian", "Vanguard"]
    NOUN = ["Alliance", "Choice", "Forum", "Council", "League", "Circle", "Board", "Coalition",
            "Institute", "Trust", "Society", "Union", "Partnership", "Assembly", "Foundation"]
    SUFFIX = ["Gamma", "Delta", "Sigma", "Omega", "Theta", "Lambda", "Kappa", "Zeta", "Eta",
              "Iota", "Mu", "Nu", "Xi", "Pi", "Rho", "Tau", "Phi", "Chi", "Psi", "Beta"]

    def _bases(self, n: int):
        """Deterministic unique two-word bases (adjective + noun).

        Adjective and noun indices are staggered so that consecutive bases share
        no token; token reuse across distant bases still occurs (realistically),
        but cross-pair overlap stays bounded instead of every base sharing one
        adjective."""
        out = []
        for i in range(n):
            a = self.ADJ[i % len(self.ADJ)]
            b = self.NOUN[(i + i // len(self.NOUN)) % len(self.NOUN)]
            out.append((a, b))
        return out

    def _build_scaled(self) -> None:
        sp = self.spec
        # ---- RQ1: seeded proxy paths ---- #
        for i in range(sp.n_proxy_paths):
            fu, inter = f"Funder_{i:03d}", f"Intermediary_{i:03d}"
            kind = i % 4
            if kind == 0:
                nseq = [(fu, "Funder"), (inter, "Intermediary"),
                        (f"Proxy_{i:03d}", "Proxy"), (f"Campaign_{i:03d}", "Campaign")]
                et = ["funds", "partners_with", "hosts"]
            elif kind == 1:
                nseq = [(fu, "Funder"), (inter, "Intermediary"), (f"Event_{i:03d}", "Event"),
                        (f"Proxy_{i:03d}", "Proxy"), (f"Report_{i:03d}", "Report")]
                et = ["funds", "hosts", "speaks_at", "publishes"]
            elif kind == 2:
                nseq = [(fu, "Funder"), (inter, "Intermediary"),
                        (f"Proxy_{i:03d}", "Proxy"), (f"Campaign_{i:03d}", "Campaign")]
                et = ["funds", "partners_with", "amplifies"]   # min grade 2 (still recoverable)
            else:
                nseq = [(fu, "Funder"), (inter, "Intermediary"),
                        (f"Event_{i:03d}", "Event"), (f"Report_{i:03d}", "Report")]
                et = ["funds", "hosts", "publishes"]
            self._seed_one_path(f"GT_PATH_{i:03d}", nseq, et)

        # ---- weaker funder-originated false leads (distractors, label 0) ---- #
        for j in range(sp.n_false_leads):
            fu, inter = f"Funder_L{j:03d}", f"Intermediary_L{j:03d}"
            self.add_node(fu, "Funder"); self.add_node(inter, "Intermediary")
            self.add_edge(fu, inter, "funds", phase="Phase_01", is_distractor=True)
            if j % 2 == 0:                                  # ends in weak co-occurrence -> true negative
                rep = f"Report_L{j:03d}"; self.add_node(rep, "Report")
                self.add_edge(inter, rep, "co_occurs_with", phase="Phase_02", is_distractor=True)
            else:                                           # ends in shared-link -> possible false positive
                pr = f"Proxy_L{j:03d}"; camp = f"Campaign_L{j:03d}"
                self.add_node(pr, "Proxy"); self.add_node(camp, "Campaign")
                self.add_edge(inter, pr, "partners_with", phase="Phase_01", is_distractor=True)
                self.add_edge(pr, camp, "shares_link", phase="Phase_02", is_distractor=True)

        # ---- RQ2: false friends (distinct identities) ---- #
        bases = self._bases(sp.n_false_friend_pairs + sp.n_alias_groups + 5)
        bi = 0
        for k in range(sp.n_false_friend_pairs):
            a, b = bases[bi]; bi += 1
            if k % 2 == 0:
                sa, sb = f"{a}_{b}_Alpha", f"{a}_{b}_Beta"            # share 2 tokens, jaccard 0.5
            else:
                sa, sb = f"{a}_{b}_Branch", f"{a}_{b}_Branches"       # singular/plural, jaccard 0.5
            for s, canon in [(sa, f"CANON_FF_{k:03d}_A"), (sb, f"CANON_FF_{k:03d}_B")]:
                self.add_node(s, "Proxy", canonical_id=canon, surface_form=s)
                self.entity_resolution_rows.append({
                    "entity_id": f"ER_FF_{k:03d}_{'A' if canon.endswith('A') else 'B'}",
                    "surface_form": s, "canonical_id": canon, "is_true_alias": False,
                    "is_false_friend": True, "expected_merge_decision": "do_not_merge"})

        # ---- RQ2: true aliases (same identity) ---- #
        for g in range(sp.n_alias_groups):
            a, b = bases[bi]; bi += 1
            suf = self.SUFFIX[g % len(self.SUFFIX)]
            canon = f"CANON_ALIAS_{g:03d}"
            size3 = (g % 6 == 0)
            members = [f"{a}_{b}_{suf}", f"{a}_{b}_{suf}_Group"]
            if size3:
                members.append(f"{suf}_{a}_Network")                 # re-ordered, one pair will miss
            ncls = "Intermediary" if g % 2 == 0 else "Campaign"
            for m_i, surface in enumerate(members):
                self.add_node(surface, ncls, canonical_id=canon, surface_form=surface)
                self.entity_resolution_rows.append({
                    "entity_id": f"ER_AL_{g:03d}_{m_i}", "surface_form": surface, "canonical_id": canon,
                    "is_true_alias": True, "is_false_friend": False, "expected_merge_decision": "merge"})

        # ---- RQ3: negative-control subgraphs ---- #
        controls = []
        for c in range(sp.n_negative_controls):
            ic = f"IndependentControl_{c:03d}"
            if c % 3 == 0:
                nodes = [(ic, "IndependentControl"), (f"Event_Ind_{c:03d}", "Event")]
                edges = [(ic, f"Event_Ind_{c:03d}", "co_occurs_with")]
            elif c % 3 == 1:
                nodes = [(ic, "IndependentControl"), (f"Report_Ind_{c:03d}", "Report")]
                edges = [(ic, f"Report_Ind_{c:03d}", "no_known_link")]
            else:
                nodes = [(ic, "IndependentControl"), (f"SocialAccount_Ind_{c:03d}", "SocialAccount"),
                         (f"MediaOutlet_Ind_{c:03d}", "MediaOutlet")]
                edges = [(ic, f"SocialAccount_Ind_{c:03d}", "no_known_link"),
                         (f"SocialAccount_Ind_{c:03d}", f"MediaOutlet_Ind_{c:03d}", "co_occurs_with")]
            controls.append((f"NC_{c:03d}", nodes, edges))
        self._add_controls(controls)

        # ---- RQ3b: embedded controls attached to seeded intermediaries/proxies ---- #
        attach_pool = ([f"Intermediary_{i:03d}" for i in range(sp.n_proxy_paths)]
                       + [f"Proxy_{i:03d}" for i in range(sp.n_proxy_paths)
                          if f"Proxy_{i:03d}" in self.nodes])
        attach_pool = [a for a in attach_pool if a in self.nodes]
        for e in range(sp.n_embedded_controls):
            self._add_embedded_control(e + 1, attach_pool[e % max(1, len(attach_pool))])

        # ---- RQ5: weak-signal-only chains ---- #
        for wc in range(sp.n_weak_chains):
            self._add_weak_chain(wc + 1)

        # ---- background noise within an isolated filler pool ---- #
        self._build_active_network_noise()
        self._build_filler_noise()

        # ---- pad to size targets deterministically ---- #
        self._pad_to_targets()

    def _build_active_network_noise(self) -> None:
        """Add seeded distractor edges inside the funder-reachable graph.

        These edges are deliberately connected to existing intermediaries,
        proxies, campaigns, and reports. They therefore create alternative
        funder-to-terminal paths rather than disconnected filler variation.
        Every edge is tagged so its candidate-level effect can be reported.
        """
        sp = self.spec
        total = (sp.n_active_weak_cooccur + sp.n_active_shared_link + sp.n_active_semantic
                 + sp.n_active_amplify + sp.n_active_misleading_documentary
                 + sp.n_active_cross_path)
        if not total:
            return
        intermediaries = sorted(n for n, d in self.nodes.items()
                                if d.node_class == "Intermediary" and n.startswith("Intermediary_"))
        terminals = sorted(n for n, d in self.nodes.items()
                           if d.node_class in TERMINAL_CLASSES and (n.startswith("Campaign_") or n.startswith("Report_")))
        proxies = sorted(n for n, d in self.nodes.items()
                         if d.node_class == "Proxy" and n.startswith("Proxy_"))
        if not intermediaries or not terminals:
            return

        def add_terminal_edges(count: int, edge_type: str, offset: int) -> None:
            for i in range(count):
                source = intermediaries[i % len(intermediaries)]
                target = terminals[(i + offset) % len(terminals)]
                self.add_edge(source, target, edge_type, phase=PHASES[(i + offset) % len(PHASES)],
                              is_distractor=True, is_active_noise=True)

        add_terminal_edges(sp.n_active_weak_cooccur, "co_occurs_with", 1)
        add_terminal_edges(sp.n_active_shared_link, "shares_link", 3)
        add_terminal_edges(sp.n_active_semantic, "uses_similar_language", 5)
        add_terminal_edges(sp.n_active_amplify, "amplifies", 7)
        add_terminal_edges(sp.n_active_misleading_documentary, "partners_with", 11)
        if proxies:
            for i in range(sp.n_active_cross_path):
                source = intermediaries[i % len(intermediaries)]
                target = proxies[(i + 1) % len(proxies)]
                self.add_edge(source, target, "shares_link", phase=PHASES[(i + 2) % len(PHASES)],
                              is_distractor=True, is_active_noise=True)
    def _build_filler_noise(self) -> None:
        sp = self.spec
        n_filler = sp.n_filler_nodes or max(40, sp.n_weak_cooccur // 6 + sp.n_semantic_distractors // 5)
        classes = ["MediaOutlet", "SocialAccount", "Report", "Event"]
        for i in range(n_filler):
            nid = f"Noise_{classes[i % 4][:3]}_{i:03d}"
            self.add_node(nid, classes[i % 4]); self._filler.append(nid)
        pool = self._filler
        if not pool:
            return
        def rnode():
            return pool[int(self.rng.integers(0, len(pool)))]
        for _ in range(sp.n_weak_cooccur):
            s, t = rnode(), rnode()
            if s != t:
                self.add_edge(s, t, "co_occurs_with", is_distractor=True)
        for _ in range(sp.n_semantic_distractors):
            s, t = rnode(), rnode()
            if s != t:
                self.add_edge(s, t, "uses_similar_language", is_distractor=True)
        for _ in range(sp.n_amplify_distractors):
            s, t = rnode(), rnode()
            if s != t:
                self.add_edge(s, t, "amplifies", is_distractor=True)

    def _pad_to_targets(self) -> None:
        sp = self.spec
        idx = 0
        # pad nodes with small disconnected weak clusters
        while len(self.nodes) < sp.target_nodes:
            a, b = f"Pad_Soc_{idx:03d}", f"Pad_Med_{idx:03d}"
            self.add_node(a, "SocialAccount"); self.add_node(b, "MediaOutlet")
            self._filler += [a, b]
            if len([e for e in self.edges]) < sp.target_edges_max:
                self.add_edge(a, b, "co_occurs_with", is_distractor=True)
            idx += 1
        # pad edges up to the minimum using the filler pool
        pool = self._filler or list(self.nodes)
        guard = 0
        while len(self.edges) < sp.target_edges_min and guard < sp.target_edges_max * 3:
            s = pool[int(self.rng.integers(0, len(pool)))]
            t = pool[int(self.rng.integers(0, len(pool)))]
            if s != t:
                self.add_edge(s, t, "co_occurs_with", is_distractor=True)
            guard += 1

    # -- build dispatch ----------------------------------------------------- #
    def build(self) -> "SyntheticCorpusGenerator":
        if self.spec.programmatic:
            self._build_scaled()
        else:
            self._build_small()
        return self

    # -- NetworkX export ---------------------------------------------------- #
    def to_multidigraph(self) -> nx.MultiDiGraph:
        G = nx.MultiDiGraph(name=f"synthetic_network_{self.spec.key}", seed=self.seed)
        for n in self.nodes.values():
            G.add_node(n.node_id, node_class=n.node_class, canonical_id=n.canonical_id,
                       surface_form=n.surface_form, is_independent_control=bool(n.is_independent_control))
        for e in self.edges:
            G.add_edge(e.source, e.target, key=e.key, edge_type=e.edge_type,
                       evidence_snippet=e.evidence_snippet, evidence_grade=int(e.evidence_grade),
                       phase=e.phase, is_ground_truth=bool(e.is_ground_truth),
                       is_distractor=bool(e.is_distractor), is_negative_control=bool(e.is_negative_control),
                       is_active_noise=bool(e.is_active_noise))
        return G


# --------------------------------------------------------------------------- #
# Synthetic ground-truth verifier (replaces EntityVerificationAgent)
# --------------------------------------------------------------------------- #
class SyntheticGroundTruthVerifier:
    """Transparent token-set entity resolution, evaluated against the answer key.

    Decisions follow a three-zone rule in the spirit of Fellegi and Sunter's
    classic linkage decision model: clear matches are auto-merged, clear
    non-matches are kept separate, and the ambiguous middle band is REFERRED to
    a human reviewer rather than decided automatically. In a sensitive domain
    the automated rule must never merge on ambiguity."""

    def __init__(self, er_rows: List[Dict[str, Any]],
                 auto_merge_threshold: float = ER_AUTO_MERGE_THRESHOLD,
                 refer_threshold: float = ER_REFER_THRESHOLD):
        self.er_rows = er_rows
        self.merge_threshold = auto_merge_threshold     # backward-compatible name
        self.auto_merge_threshold = auto_merge_threshold
        self.refer_threshold = refer_threshold

    @staticmethod
    def _tokens(s: str) -> set:
        return set(t for t in s.lower().replace("_", " ").split() if t)

    @staticmethod
    def _norm(s: str) -> str:
        return s.lower().replace("_", " ").strip()

    def token_jaccard(self, a: str, b: str) -> float:
        ta, tb = self._tokens(a), self._tokens(b)
        return len(ta & tb) / len(ta | tb) if (ta and tb) else 0.0

    def sequence_ratio(self, a: str, b: str) -> float:
        return SequenceMatcher(None, self._norm(a), self._norm(b)).ratio()

    def similarity(self, a: str, b: str) -> float:
        return self.token_jaccard(a, b)

    def decision_zone(self, sim: float) -> str:
        if sim >= self.auto_merge_threshold:
            return "auto_merge"
        if sim >= self.refer_threshold:
            return "refer_to_human"
        return "keep_separate"

    @staticmethod
    def _outcome(zone: str, truth: str) -> str:
        if zone == "auto_merge":
            return "correct_auto_merge" if truth == "merge" else "FALSE_MERGE"
        if zone == "refer_to_human":
            return "referred_true_alias" if truth == "merge" else "referred_distinct_pair"
        return "conservative_miss" if truth == "merge" else "correct_keep_separate"

    def propose_merges(self, only_related: bool = False) -> List[Dict[str, Any]]:
        results = []
        for a, b in itertools.combinations(self.er_rows, 2):
            sim = self.similarity(a["surface_form"], b["surface_form"])
            truth = "merge" if a["canonical_id"] == b["canonical_id"] else "do_not_merge"
            if only_related and sim < 0.30 and truth == "do_not_merge":
                continue
            zone = self.decision_zone(sim)
            proposed = "merge" if zone == "auto_merge" else "do_not_merge"
            results.append({
                "surface_a": a["surface_form"], "surface_b": b["surface_form"],
                "token_similarity": round(sim, 3),
                "char_similarity": round(self.sequence_ratio(a["surface_form"], b["surface_form"]), 3),
                "decision_zone": zone,
                "proposed_decision": proposed, "ground_truth_decision": truth,
                "outcome": self._outcome(zone, truth),
                "correct": proposed == truth,
                "pair_type": "true_alias" if truth == "merge" else "false_friend"})
        return results


# --------------------------------------------------------------------------- #
# Review-priority (triage) scorer  -- RQ4
# --------------------------------------------------------------------------- #
class ReviewPriorityScorer:
    """Computes the transparent review-priority score for a candidate path."""

    def __init__(self, G: nx.MultiDiGraph, weights: Optional[ScoreWeights] = None):
        self.G = G
        self.w = weights or ScoreWeights()

    def _edges_on_path(self, nodes: List[str]) -> List[Dict[str, Any]]:
        out = []
        for s, t in zip(nodes[:-1], nodes[1:]):
            best = None
            for _k, data in self.G.get_edge_data(s, t, default={}).items():
                if best is None or data["evidence_grade"] > best["evidence_grade"]:
                    best = data
            if best is not None:
                out.append(best)
        return out

    def features(self, nodes: List[str]) -> Dict[str, Any]:
        edges = self._edges_on_path(nodes)
        if not edges:
            return {}
        etypes = [e["edge_type"] for e in edges]
        grades = [e["evidence_grade"] for e in edges]
        phases = [e["phase"] for e in edges]
        phase_counts = pd.Series(phases).value_counts()
        return {
            "edge_types": " -> ".join(etypes),
            "evidence_grades": " -> ".join(str(g) for g in grades),
            "evidence_snippets": " || ".join(e["evidence_snippet"] for e in edges),
            "n_evidence_types": len(set(etypes)),
            "mean_grade": round(float(np.mean(grades)), 3),
            "max_grade": float(np.max(grades)), "min_grade": float(np.min(grades)),
            "temporal_clustering": round(float(phase_counts.iloc[0] / len(phases)), 3),
            "semantic_similarity": 1.0 if "uses_similar_language" in etypes else 0.0,
            "amplification": 1.0 if "amplifies" in etypes else 0.0,
            "cooccurrence": 1.0 if (etypes.count("co_occurs_with") + etypes.count("shares_link")) >= 2 else 0.0,
            "has_funding_edge": 1.0 if "funds" in etypes else 0.0,
            "has_active_noise": 1.0 if any(e.get("is_active_noise", False) for e in edges) else 0.0,
            "path_length": len(edges)}

    def score(self, nodes: List[str]) -> Tuple[float, Dict[str, Any], Dict[str, float]]:
        f = self.features(nodes)
        if not f:
            return 0.0, {}, {}
        comps = MET.score_components(f, self.w)
        return comps["score"], f, comps


# --------------------------------------------------------------------------- #
# Candidate-path enumeration
# --------------------------------------------------------------------------- #
def enumerate_candidate_paths(G: nx.MultiDiGraph, scorer: ReviewPriorityScorer,
                              gt_paths: List[Dict[str, Any]],
                              weak_funders: Optional[set] = None,
                              embedded_nodes: Optional[set] = None,
                              max_len: int = 4,
                              max_candidates: int = 20000
                              ) -> Tuple[pd.DataFrame, List[Dict[str, Any]]]:
    """Enumerate simple directed Funder->terminal paths and score each for triage.

    Returns the candidate table and the per-candidate feature dictionaries (used
    by the weight-sensitivity analysis). Each candidate also carries an UNGATED
    ablation score (support gate removed) for the RQ5 gate-ablation analysis.
    """
    weak_funders = weak_funders or set()
    embedded_nodes = embedded_nodes or set()
    simpleG = nx.DiGraph()
    simpleG.add_nodes_from(G.nodes(data=True))
    for s, t in set((u, v) for u, v, _ in G.edges(keys=True)):
        simpleG.add_edge(s, t)
    funders = [n for n, d in G.nodes(data=True) if d["node_class"] == "Funder"]
    terminals = set(n for n, d in G.nodes(data=True) if d["node_class"] in TERMINAL_CLASSES)
    gt_sequences = {p["node_sequence"] for p in gt_paths}

    rows, feats_list, cid, seen = [], [], 0, set()
    for f in funders:
        if f not in simpleG:
            continue
        for nodes in nx.all_simple_paths(simpleG, f, terminals, cutoff=max_len):
            if len(nodes) < 3:
                continue
            key = tuple(nodes)
            if key in seen:
                continue
            seen.add(key)
            score, feats, comps = scorer.score(nodes)
            if not feats:
                continue
            score_ungated = MET.score_components(feats, scorer.w, gated=False)["score"]
            eligibility = MET.high_priority_eligibility(feats)
            score_threshold_crossed = int(score >= TRIAGE_THRESHOLD)
            high_priority_review = int(score_threshold_crossed and eligibility["eligible_for_high_priority"])
            cid += 1
            seq = " -> ".join(nodes)
            rows.append({
                "candidate_id": f"CAND_{cid:04d}", "node_sequence": seq,
                "edge_types": feats["edge_types"], "evidence_grades": feats["evidence_grades"],
                "n_evidence_types": feats["n_evidence_types"],
                "temporal_clustering_score": feats["temporal_clustering"],
                "semantic_similarity_score": feats["semantic_similarity"],
                "amplification_score": feats["amplification"],
                "review_priority_score": score,
                "score_ungated_ablation": score_ungated,
                "score_threshold_crossed": score_threshold_crossed,
                "eligible_for_high_priority": int(eligibility["eligible_for_high_priority"]),
                "eligibility_rule_version": eligibility["eligibility_rule_version"],
                "ineligible_reason": eligibility["ineligible_reason"],
                "high_priority_review": high_priority_review,
                "path_length": feats["path_length"],
                "has_funding_edge": int(feats["has_funding_edge"]),
                "has_active_noise": int(feats["has_active_noise"]),
                "is_weak_chain": int(nodes[0] in weak_funders),
                "touches_embedded_control": int(any(n in embedded_nodes for n in nodes)),
                "ground_truth_label": int(seq in gt_sequences)})
            feats_list.append(feats)
            if cid >= max_candidates:
                break
        if cid >= max_candidates:
            break
    df = pd.DataFrame(rows)
    if not df.empty:
        order = df["review_priority_score"].sort_values(ascending=False).index
        df = df.loc[order].reset_index(drop=True)
        feats_list = [feats_list[i] for i in order]
    df.attrs["candidate_cap"] = max_candidates
    df.attrs["candidate_cap_reached"] = bool(cid >= max_candidates)
    return df, feats_list


# --------------------------------------------------------------------------- #
# Scenario computation + output writing
# --------------------------------------------------------------------------- #
@dataclass
class ScenarioResult:
    spec: ScenarioSpec
    gen: SyntheticCorpusGenerator
    G: nx.MultiDiGraph
    scorer: ReviewPriorityScorer
    cand_df: pd.DataFrame
    er_decisions: pd.DataFrame
    nc_audit: pd.DataFrame
    metrics: Dict[str, Any]
    weights: ScoreWeights
    features_list: List[Dict[str, Any]] = field(default_factory=list)
    sweep_df: Optional[pd.DataFrame] = None
    sensitivity_draws: Optional[pd.DataFrame] = None
    bounds_df: Optional[pd.DataFrame] = None


def compute_scenario(spec: ScenarioSpec, robustness: bool = True) -> ScenarioResult:
    gen = SyntheticCorpusGenerator(spec).build()
    G = gen.to_multidigraph()
    weights = ScoreWeights()
    scorer = ReviewPriorityScorer(G, weights)
    cand_df, features_list = enumerate_candidate_paths(
        G, scorer, gen.ground_truth_paths,
        weak_funders=gen.weak_chain_funders, embedded_nodes=gen.embedded_control_nodes)
    # Compare candidate enumeration before and after connected active noise.
    active_noise_edges = [(u, v, k) for u, v, k, d in G.edges(keys=True, data=True)
                          if d.get("is_active_noise", False)]
    baseline_G = G.copy()
    for u, v, key in active_noise_edges:
        baseline_G.remove_edge(u, v, key)
    baseline_scorer = ReviewPriorityScorer(baseline_G, weights)
    baseline_cand_df, _ = enumerate_candidate_paths(
        baseline_G, baseline_scorer, gen.ground_truth_paths,
        weak_funders=gen.weak_chain_funders, embedded_nodes=gen.embedded_control_nodes)
    # Keep raw threshold crossing transparent; final triage uses the separate safety gate.
    cand_df["flagged"] = cand_df["high_priority_review"].astype(int)

    # ---- RQ2: three-zone entity resolution ---- #
    verifier = SyntheticGroundTruthVerifier(gen.entity_resolution_rows)
    er_decisions = pd.DataFrame(verifier.propose_merges())
    truth01 = [1 if r == "merge" else 0 for r in er_decisions["ground_truth_decision"]]
    auto01 = [1 if z == "auto_merge" else 0 for z in er_decisions["decision_zone"]]
    er_eval = MET.binary_metrics(truth01, auto01)
    n_true_alias_pairs = int(sum(truth01))
    referred = er_decisions[er_decisions["decision_zone"] == "refer_to_human"]
    n_ref_alias = int((referred["ground_truth_decision"] == "merge").sum())
    n_ref_distinct = int((referred["ground_truth_decision"] == "do_not_merge").sum())
    n_false_merges = int(((er_decisions["decision_zone"] == "auto_merge")
                          & (er_decisions["ground_truth_decision"] == "do_not_merge")).sum())
    # This is an upper bound only: no human adjudication is observed in this study.
    potential_recall = round((er_eval["tp"] + n_ref_alias) / max(1, n_true_alias_pairs), 4)

    # ---- RQ3: negative controls (isolated force-scored + embedded via enumeration) ---- #
    nc_rows = []
    for nc in gen.negative_controls:
        nodes = [n.strip() for n in nc["nodes"].split(";")]
        s, _, _ = scorer.score(nodes)
        control_features = scorer.features(nodes)
        eligibility = MET.high_priority_eligibility(control_features)
        score_threshold_crossed = int(s >= TRIAGE_THRESHOLD)
        nc_rows.append({**nc, "review_priority_score": round(s, 2),
                        "score_threshold_crossed": score_threshold_crossed,
                        "eligible_for_high_priority": int(eligibility["eligible_for_high_priority"]),
                        "eligibility_rule_version": eligibility["eligibility_rule_version"],
                        "ineligible_reason": eligibility["ineligible_reason"],
                        "high_priority_review": int(score_threshold_crossed and eligibility["eligible_for_high_priority"]),
                        "flagged": int(score_threshold_crossed and eligibility["eligible_for_high_priority"])})
    nc_audit = pd.DataFrame(nc_rows)
    iso = nc_audit[nc_audit["control_type"] == "isolated"]
    nc_specificity = round((len(iso) - int(iso["flagged"].sum())) / max(1, len(iso)), 4)
    emb_mask = cand_df["touches_embedded_control"] == 1
    emb_cands = cand_df[emb_mask]
    emb_specificity = round((len(emb_cands) - int(emb_cands["flagged"].sum()))
                            / max(1, len(emb_cands)), 4) if len(emb_cands) else 1.0
    max_emb_score = round(float(emb_cands["review_priority_score"].max()), 2) if len(emb_cands) else 0.0

    # ---- RQ1/RQ4: path triage metrics ---- #
    raw_threshold_eval = MET.binary_metrics(cand_df["ground_truth_label"].tolist(),
                                               cand_df["score_threshold_crossed"].tolist())
    path_eval = MET.binary_metrics(cand_df["ground_truth_label"].tolist(),
                                  cand_df["high_priority_review"].tolist())
    seeded_seqs = {p["node_sequence"] for p in gen.ground_truth_paths}
    recovered = cand_df[(cand_df["ground_truth_label"] == 1) & (cand_df["flagged"] == 1)]
    pr_recall = round(len(set(recovered["node_sequence"])) / max(1, len(seeded_seqs)), 4)
    n_flag = int(cand_df["flagged"].sum())
    pr_precision = round(int(((cand_df["flagged"] == 1) & (cand_df["ground_truth_label"] == 1)).sum())
                         / max(1, n_flag), 4)

    def mean_score(mask):
        sub = cand_df[mask]
        return round(float(sub["review_priority_score"].mean()), 2) if len(sub) else 0.0
    mean_true = mean_score(cand_df["ground_truth_label"] == 1)
    mean_false = mean_score((cand_df["ground_truth_label"] == 0) & (cand_df["is_weak_chain"] == 0)
                            & (~emb_mask))
    mean_nc = round(float(nc_audit["review_priority_score"].mean()), 2) if len(nc_audit) else 0.0

    # ---- RQ5: robustness analyses ---- #
    wc_mask = cand_df["is_weak_chain"] == 1
    wc = cand_df[wc_mask]
    rq5: Dict[str, Any] = {
        "n_weak_chains_seeded": len(gen.weak_signal_chains),
        "n_weak_chain_candidates": int(len(wc)),
        "max_weak_chain_score_gated": round(float(wc["review_priority_score"].max()), 2) if len(wc) else 0.0,
        "max_weak_chain_score_ungated": round(float(wc["score_ungated_ablation"].max()), 2) if len(wc) else 0.0,
        "n_weak_chain_raw_threshold_crossed": int(wc["score_threshold_crossed"].sum()) if len(wc) else 0,
        "n_weak_chain_high_priority_review": int(wc["high_priority_review"].sum()) if len(wc) else 0,
        "n_weak_chain_flagged_ungated": int((wc["score_ungated_ablation"] >= TRIAGE_THRESHOLD).sum()) if len(wc) else 0,
        "n_raw_threshold_crossed_all": int(cand_df["score_threshold_crossed"].sum()),
        "n_high_priority_review_all": n_flag,
        "n_flagged_ungated_all": int((cand_df["score_ungated_ablation"] >= TRIAGE_THRESHOLD).sum()),
    }
    sweep_df = sens_draws = bounds_df = None
    if robustness:
        bounds_df = MET.attainable_score_bounds(weights, TRIAGE_THRESHOLD)
        weak_bound = bounds_df[bounds_df["family"] == "weak_only_no_funding"].iloc[0]
        sweep_df = MET.threshold_sweep(cand_df, step=THRESHOLD_SWEEP_STEP)
        sens = MET.weight_sensitivity(features_list, cand_df["ground_truth_label"].tolist(),
                                      weights, TRIAGE_THRESHOLD, n_draws=SENSITIVITY_N_DRAWS,
                                      rel_range=SENSITIVITY_REL_RANGE, seed=SENSITIVITY_SEED)
        sens_draws = sens["draws"]
        rq5.update({
            "weak_signal_only_max_attainable_gated": float(weak_bound["max_score_gated"]),
            "weak_signal_only_max_attainable_ungated": float(weak_bound["max_score_ungated"]),
            "weak_signal_only_raw_can_reach_threshold": bool(weak_bound["score_threshold_crossed_ungated"]),
            "weight_sensitivity": sens["summary"],
        })

    active_noise_mask = cand_df["has_active_noise"] == 1
    active_noise_false_positives = cand_df[(active_noise_mask)
                                           & (cand_df["ground_truth_label"] == 0)
                                           & (cand_df["high_priority_review"] == 1)]
    active_noise_metrics = {
        "n_active_noise_edges": len(active_noise_edges),
        "candidate_paths_before_active_noise": int(len(baseline_cand_df)),
        "candidate_paths_after_active_noise": int(len(cand_df)),
        "n_candidate_paths_using_active_noise": int(active_noise_mask.sum()),
        "n_high_priority_active_noise_false_positives": int(len(active_noise_false_positives)),
        "candidate_cap": int(cand_df.attrs.get("candidate_cap", 0)),
        "candidate_cap_reached": bool(cand_df.attrs.get("candidate_cap_reached", False)),
    }
    metrics = {
        "reproducibility": {"seed": spec.seed, "scenario": spec.key},
        "network_summary": {
            "n_nodes": G.number_of_nodes(), "n_edges": G.number_of_edges(),
            "n_node_classes": len({d["node_class"] for _, d in G.nodes(data=True)}),
            "n_edge_types": len({d["edge_type"] for *_e, d in G.edges(data=True)}),
            "n_seeded_proxy_paths": len(gen.ground_truth_paths),
            "n_false_friend_entities": int(pd.DataFrame(gen.entity_resolution_rows)["is_false_friend"].sum()),
            "n_true_alias_records": int(pd.DataFrame(gen.entity_resolution_rows)["is_true_alias"].sum()),
            "n_true_alias_groups": int(pd.DataFrame(gen.entity_resolution_rows)
                                       .query("is_true_alias")["canonical_id"].nunique()),
            "n_negative_control_subgraphs": len(gen.negative_controls),
            "n_isolated_controls": int(len(iso)),
            "n_embedded_controls": int((nc_audit["control_type"] == "embedded").sum()),
            "n_weak_chains": len(gen.weak_signal_chains),
            "n_candidate_paths": int(cand_df.shape[0])},
        "rq1_path_recovery": {**path_eval, "path_recovery_recall": pr_recall,
                              "path_recovery_precision": pr_precision, "triage_threshold": TRIAGE_THRESHOLD,
                              "decision_basis": "high_priority_review"},
        "rq2_entity_resolution": {**er_eval, "entity_resolution_precision": er_eval["precision"],
                                  "entity_resolution_recall": er_eval["recall"],
                                  "auto_merge_threshold": verifier.auto_merge_threshold,
                                  "refer_threshold": verifier.refer_threshold,
                                  "n_true_alias_pairs": n_true_alias_pairs,
                                  "n_referred_pairs": int(len(referred)),
                                  "n_referred_true_alias": n_ref_alias,
                                  "n_referred_distinct": n_ref_distinct,
                                  "n_false_merges": n_false_merges,
                                  "no_false_friend_auto_merged": bool(n_false_merges == 0),
                                  "potential_recall_if_all_referred_true_aliases_are_correctly_confirmed": potential_recall,
                                  "observed_human_adjudication_recall": None},
        "rq3_negative_controls": {"negative_control_specificity": nc_specificity,
                                  "n_controls": len(nc_audit),
                                  "max_control_score": round(float(nc_audit["review_priority_score"].max()), 2) if len(nc_audit) else 0.0,
                                  "all_controls_below_threshold": bool(int(nc_audit["flagged"].sum()) == 0),
                                  "embedded_control_specificity": emb_specificity,
                                  "n_embedded_control_candidates": int(len(emb_cands)),
                                  "max_embedded_candidate_score": max_emb_score,
                                  "all_embedded_below_threshold": bool(int(emb_cands["flagged"].sum()) == 0) if len(emb_cands) else True},
        "rq4_review_priority": {"triage_threshold": TRIAGE_THRESHOLD,
                                "n_raw_score_threshold_crossed": int(cand_df["score_threshold_crossed"].sum()),
                                "n_high_priority_review": n_flag,
                                "raw_score_threshold_metrics": raw_threshold_eval,
                                "score_band_truth_summary": MET.score_band_truth_summary(cand_df),
                                "score_min": round(float(cand_df["review_priority_score"].min()), 2),
                                "score_max": round(float(cand_df["review_priority_score"].max()), 2),
                                "score_mean": round(float(cand_df["review_priority_score"].mean()), 2),
                                "mean_score_true_paths": mean_true,
                                "mean_score_false_leads": mean_false,
                                "mean_score_weak_chains": mean_score(wc_mask),
                                "mean_score_embedded_controls": mean_score(emb_mask),
                                "mean_score_negative_controls": mean_nc},
        "rq5_robustness": rq5,
        "active_noise_validation": active_noise_metrics,
        "disclaimer": CFG.DISCLAIMER,
    }
    return ScenarioResult(spec, gen, G, scorer, cand_df, er_decisions, nc_audit, metrics, weights,
                          features_list=features_list, sweep_df=sweep_df,
                          sensitivity_draws=sens_draws, bounds_df=bounds_df)


def write_core_outputs(res: ScenarioResult, out: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)
    nx.write_graphml(res.G, out / "synthetic_network.graphml")
    try:
        data = nx.node_link_data(res.G, edges="links")
    except TypeError:
        data = nx.node_link_data(res.G)
    (out / "synthetic_network.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
    pd.DataFrame(res.gen.ground_truth_paths).to_csv(out / "ground_truth_paths.csv", index=False)
    pd.DataFrame(res.gen.entity_resolution_rows).to_csv(out / "ground_truth_entity_resolution.csv", index=False)
    res.nc_audit.to_csv(out / "negative_control_subgraphs.csv", index=False)
    res.cand_df.to_csv(out / "candidate_paths.csv", index=False)
    res.er_decisions.to_csv(out / "entity_resolution_decisions.csv", index=False)
    pd.DataFrame(EVIDENCE_GRADING_MATRIX).to_csv(out / "evidence_grading_matrix.csv", index=False)
    pd.DataFrame(res.gen.weak_signal_chains).to_csv(out / "weak_signal_chains.csv", index=False)
    MET.formula_table(res.weights, TRIAGE_THRESHOLD).to_csv(
        out / "review_priority_formula.csv", index=False)
    if res.bounds_df is not None:
        res.bounds_df.to_csv(out / "score_bounds.csv", index=False)
    if res.sweep_df is not None:
        res.sweep_df.to_csv(out / "threshold_sweep.csv", index=False)
    if res.sensitivity_draws is not None:
        res.sensitivity_draws.to_csv(out / "sensitivity_analysis.csv", index=False)
    # flat + json metrics
    flat = []
    for grp in ["network_summary", "rq1_path_recovery", "rq2_entity_resolution",
                "rq3_negative_controls", "rq4_review_priority", "rq5_robustness",
                "active_noise_validation"]:
        for k, v in res.metrics[grp].items():
            if k == "score_band_truth_summary":
                continue
            if isinstance(v, dict):
                for k2, v2 in v.items():
                    flat.append({"group": grp, "metric": f"{k}.{k2}", "value": v2})
            else:
                flat.append({"group": grp, "metric": k, "value": v})
    pd.DataFrame(flat).to_csv(out / "validation_metrics.csv", index=False)
    (out / "validation_metrics.json").write_text(json.dumps(res.metrics, indent=2), encoding="utf-8")


def run_scenario(spec: ScenarioSpec, base_dir: Path, make_figures: bool = True) -> Dict[str, Any]:
    """Compute one scenario and write every output (core, audit, report, figures)."""
    out = base_dir / spec.folder
    res = compute_scenario(spec)
    write_core_outputs(res, out)
    # audit + report + figures (imported lazily to keep core importable on its own)
    import frontg_audit as AUD
    import frontg_report_writer as REP
    path_audit, triage_audit, er_audit, nc_audit = AUD.build_audit_tables(res)
    path_audit.to_csv(out / "path_recovery_audit.csv", index=False)
    triage_audit.to_csv(out / "triage_score_audit.csv", index=False)
    er_audit.to_csv(out / "entity_resolution_audit.csv", index=False)
    REP.write_tracking_report(res, path_audit, triage_audit, er_audit, nc_audit, out)
    if make_figures:
        import frontg_visualisation as VIS
        VIS.generate_all_figures(res, path_audit, out)
    print(f"[{spec.key}] nodes={res.metrics['network_summary']['n_nodes']} "
          f"edges={res.metrics['network_summary']['n_edges']} "
          f"recall={res.metrics['rq1_path_recovery']['path_recovery_recall']} "
          f"precision={res.metrics['rq1_path_recovery']['path_recovery_precision']} "
          f"ER_prec={res.metrics['rq2_entity_resolution']['entity_resolution_precision']} "
          f"NC_spec={res.metrics['rq3_negative_controls']['negative_control_specificity']} "
          f"EC_spec={res.metrics['rq3_negative_controls']['embedded_control_specificity']} "
          f"weak_high_priority={res.metrics['rq5_robustness']['n_weak_chain_high_priority_review']}")
    return res.metrics


def write_cross_scenario_summary(all_metrics: Dict[str, Dict[str, Any]], base_dir: Path) -> None:
    rows = []
    for key in CFG.ALL_SCENARIO_KEYS:
        if key not in all_metrics:
            continue
        m = all_metrics[key]; ns, r1, r2, r3, r4 = (m["network_summary"], m["rq1_path_recovery"],
                                                     m["rq2_entity_resolution"], m["rq3_negative_controls"],
                                                     m["rq4_review_priority"])
        active = m["active_noise_validation"]
        rows.append({
            "scenario": SCENARIOS[key].name, "scenario_key": key,
            "n_nodes": ns["n_nodes"], "n_edges": ns["n_edges"],
            "n_seeded_proxy_paths": ns["n_seeded_proxy_paths"], "n_candidate_paths": ns["n_candidate_paths"],
            "n_false_friend_entities": ns["n_false_friend_entities"],
            "n_true_alias_records": ns["n_true_alias_records"], "n_true_alias_groups": ns["n_true_alias_groups"],
            "n_negative_controls": ns["n_negative_control_subgraphs"],
            "n_active_noise_edges": active["n_active_noise_edges"],
            "candidate_paths_before_active_noise": active["candidate_paths_before_active_noise"],
            "active_noise_candidate_paths": active["n_candidate_paths_using_active_noise"],
            "active_noise_high_priority_false_positives": active["n_high_priority_active_noise_false_positives"],
            "candidate_cap_reached": active["candidate_cap_reached"],
            "path_recovery_precision": r1["path_recovery_precision"],
            "path_recovery_recall": r1["path_recovery_recall"], "f1_score": r1["f1"],
            "false_positive_rate": r1["false_positive_rate"], "false_negative_rate": r1["false_negative_rate"],
            "entity_resolution_precision": r2["entity_resolution_precision"],
            "entity_resolution_recall": r2["entity_resolution_recall"],
            "er_potential_recall_under_perfect_adjudication": r2["potential_recall_if_all_referred_true_aliases_are_correctly_confirmed"],
            "er_n_referred_pairs": r2["n_referred_pairs"],
            "er_n_false_merges": r2["n_false_merges"],
            "negative_control_specificity": r3["negative_control_specificity"],
            "embedded_control_specificity": r3["embedded_control_specificity"],
            "max_embedded_candidate_score": r3["max_embedded_candidate_score"],
            "n_weak_chain_high_priority_review": m["rq5_robustness"]["n_weak_chain_high_priority_review"],
            "n_weak_chain_flagged_ungated": m["rq5_robustness"]["n_weak_chain_flagged_ungated"],
            "max_weak_chain_score_gated": m["rq5_robustness"]["max_weak_chain_score_gated"],
            "max_weak_chain_score_ungated": m["rq5_robustness"]["max_weak_chain_score_ungated"],
            "sensitivity_recall_min": m["rq5_robustness"].get("weight_sensitivity", {}).get("recall_min", ""),
            "sensitivity_jaccard_median": m["rq5_robustness"].get("weight_sensitivity", {}).get("flagged_set_jaccard_median", ""),
            "mean_score_true_paths": r4["mean_score_true_paths"],
            "mean_score_false_leads": r4["mean_score_false_leads"],
            "mean_score_weak_chains": r4["mean_score_weak_chains"],
            "mean_score_negative_controls": r4["mean_score_negative_controls"]})
    pd.DataFrame(rows).to_csv(base_dir / "cross_scenario_validation_summary.csv", index=False)


def run_replications(base_dir: Path, keys: Optional[List[str]] = None) -> pd.DataFrame:
    """Cross-seed consistency check: rerun the programmatic scenarios under
    several seeds (no figures, no per-scenario outputs) and tabulate the
    headline metrics. The planted answer-key structure is fixed by design and
    only background filler/noise placement varies with the seed, so identical
    metrics across seeds are a determinism/consistency check, not an
    independent statistical replication."""
    rows = []
    for key in (keys or ["medium", "stress"]):
        spec = SCENARIOS[key]
        for sd in spec.replication_seeds or (spec.seed,):
            sp2 = dataclasses.replace(spec, seed=sd)
            res = compute_scenario(sp2, robustness=False)
            m = res.metrics
            rows.append({
                "scenario_key": key, "seed": sd,
                "n_nodes": m["network_summary"]["n_nodes"],
                "n_edges": m["network_summary"]["n_edges"],
                "n_candidate_paths": m["network_summary"]["n_candidate_paths"],
                "path_recovery_recall": m["rq1_path_recovery"]["path_recovery_recall"],
                "path_recovery_precision": m["rq1_path_recovery"]["path_recovery_precision"],
                "entity_resolution_precision": m["rq2_entity_resolution"]["entity_resolution_precision"],
                "er_potential_recall_under_perfect_adjudication": m["rq2_entity_resolution"]["potential_recall_if_all_referred_true_aliases_are_correctly_confirmed"],
                "er_n_false_merges": m["rq2_entity_resolution"]["n_false_merges"],
                "negative_control_specificity": m["rq3_negative_controls"]["negative_control_specificity"],
                "embedded_control_specificity": m["rq3_negative_controls"]["embedded_control_specificity"],
                "n_weak_chain_high_priority_review": m["rq5_robustness"]["n_weak_chain_high_priority_review"],
                "mean_score_true_paths": m["rq4_review_priority"]["mean_score_true_paths"],
                "mean_score_false_leads": m["rq4_review_priority"]["mean_score_false_leads"]})
            print(f"[cross-seed consistency {key} seed={sd}] recall="
                  f"{rows[-1]['path_recovery_recall']} precision={rows[-1]['path_recovery_precision']} "
                  f"NC_spec={rows[-1]['negative_control_specificity']} "
                  f"EC_spec={rows[-1]['embedded_control_specificity']}")
    df = pd.DataFrame(rows)
    df.to_csv(base_dir / "multiseed_replication.csv", index=False)
    return df


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def main(argv: Optional[List[str]] = None) -> None:
    ap = argparse.ArgumentParser(description="Synthetic validation harness (synthetic data only).")
    ap.add_argument("--scenario", choices=["small", "medium", "stress"], help="run a single scenario")
    ap.add_argument("--all", action="store_true", help="run all scenarios")
    ap.add_argument("--output-dir", default=str(OUTPUT_DIR), help="base output directory")
    ap.add_argument("--no-figures", action="store_true", help="skip figure generation")
    ap.add_argument("--replications", action="store_true",
                    help="also run the cross-seed consistency check (medium + stress)")
    args = ap.parse_args(argv)

    base = Path(args.output_dir).resolve()
    keys = CFG.ALL_SCENARIO_KEYS if (args.all or not args.scenario) else [args.scenario]
    all_metrics = {}
    for key in keys:
        all_metrics[key] = run_scenario(SCENARIOS[key], base, make_figures=not args.no_figures)
    if len(keys) > 1:
        write_cross_scenario_summary(all_metrics, base)
        print(f"Cross-scenario summary written to {base / 'cross_scenario_validation_summary.csv'}")
    if args.replications or args.all:
        run_replications(base)
        print(f"Cross-seed consistency check written to {base / 'multiseed_replication.csv'}")
    print("Done. Synthetic data only - indicators for expert human review, not proof of wrongdoing.")


if __name__ == "__main__":
    main()
