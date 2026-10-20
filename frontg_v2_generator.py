#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
frontg_v2_generator.py
======================

Benchmark B: a stochastic latent-truth generator for the FrontG synthetic
validation harness. Synthetic data only: every entity, relation, and evidence
snippet is abstract and programmatically generated.

Why a second generator?
-----------------------
Benchmark A (``generate_synthetic_graph.py``) plants answer-key pathways from a
small number of fixed templates. That design is ideal for specification
(acceptance) tests, but it has a known weakness: a supervised learner can
reproduce its answer key almost perfectly because labels are identifiable from
template artefacts (see ``run_v2_benchmark.py --diagnostic``). Benchmark B
removes that shortcut:

* **Latent truth, noisy observation.** True influence pathways and legitimate
  decoy pathways are sampled from the *same* structural distribution (same
  funders, overlapping intermediaries, same length distribution, same node
  classes, neutral node identifiers). They differ only through class-conditional
  *observation* probabilities (evidence grade per hop, whether funding is
  publicly observed, whether hop timing is coherent, whether grade-2 hops are
  amplification/similar-language signals). These distributions overlap, so
  labels are not a deterministic function of the observed features.
* **Hidden funding.** A true pathway's funding hop is observed as a funding
  edge only with probability ``p_fund_obs_true``; otherwise it appears as a
  weaker documentary or weak signal. This models undisclosed funding.
* **Bystanders stratified by attachment strength.** Independent actors are
  attached to true-pathway nodes by grade-1, grade-2, or grade-3 links, so the
  bystander property can be evaluated where it is guaranteed (grade 1) and
  where it is not (grade 2, grade 3).
* **Weak-signal decoys** from the same funders (no funding edge, every hop
  grade <= 2).
* **Background topology variants**: isolated filler, hub-dominated
  (Barabasi-Albert) background, and community-structured (stochastic block
  model) background, the latter two bridged into the active graph.
* **Regimes** shift the observation model (hidden funding, weak-signal
  coordination, documentary decoys) or the background topology, so methods can
  be compared under distribution shift.

The generator parameters below are set as scenario assumptions. They are not
estimated from real data and are deliberately varied across regimes.
"""
from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import Any, Dict, List, Optional, Tuple

import networkx as nx
import numpy as np

from frontg_config import EDGE_TYPE_GRADE, PHASES, ScenarioSpec
from generate_synthetic_graph import SyntheticCorpusGenerator

# Edge types by evidence grade (controlled vocabulary shared with Benchmark A).
TYPES_BY_GRADE: Dict[int, List[str]] = {
    1: ["co_occurs_with"],
    2: ["shares_link", "amplifies", "uses_similar_language"],
    3: ["partners_with", "hosts", "speaks_at", "publishes", "cites"],
    4: ["funds"],
}
SUPPORTING_TYPES = ["amplifies", "uses_similar_language"]
MIDDLE_CLASSES = ["Proxy", "Event", "Intermediary", "MediaOutlet"]
TERMINAL_CHOICES = ["Campaign", "Report"]
BACKGROUND_CLASSES = ["MediaOutlet", "SocialAccount", "Report", "Event"]


@dataclass(frozen=True)
class RegimeV2:
    """Parameters of one Benchmark-B regime (all synthetic assumptions)."""
    name: str
    description: str = ""
    # --- population ----------------------------------------------------- #
    n_funders: int = 8
    n_true_paths: int = 12
    n_decoy_paths: int = 24
    n_weak_decoys: int = 8
    n_bystanders_per_stratum: int = 3          # strata: attachment grade 1, 2, 3
    length_probs: Tuple[float, float, float] = (0.2, 0.5, 0.3)   # 2, 3, 4 hops
    p_decoy_reuses_true_node: float = 0.3      # any pathway reuses an existing intermediary (shared pool)
    # --- observation model: true pathways -------------------------------- #
    p_fund_obs_true: float = 0.85
    grade_probs_true: Tuple[float, float, float] = (0.10, 0.30, 0.60)   # grade 1, 2, 3
    p_supporting_true: float = 0.6             # P(grade-2 hop is amplification/similar language)
    p_phase_coherent_true: float = 0.7
    # --- observation model: legitimate decoy pathways -------------------- #
    p_fund_obs_decoy: float = 0.85
    grade_probs_decoy: Tuple[float, float, float] = (0.20, 0.35, 0.45)
    p_supporting_decoy: float = 0.3
    p_phase_coherent_decoy: float = 0.3
    # --- background topology --------------------------------------------- #
    background: str = "isolated"               # isolated | hub | community
    n_background: int = 150
    n_background_edges: int = 300              # isolated filler only
    n_bridges: int = 30                        # hub/community: active -> background edges
    background_grade_probs: Tuple[float, float, float] = (0.50, 0.35, 0.15)
    n_communities: int = 6


BASE = RegimeV2(name="base", description="Overlapping evidence distributions; isolated background.")

REGIMES: Dict[str, RegimeV2] = {
    "base": BASE,
    "hidden_funding": replace(
        BASE, name="hidden_funding",
        description="True pathways' funding is publicly observed only 40% of the time.",
        p_fund_obs_true=0.40),
    "weak_coordination": replace(
        BASE, name="weak_coordination",
        description="True pathways are mostly evidenced by weak (grade 1-2) coordination signals.",
        grade_probs_true=(0.20, 0.55, 0.25), p_supporting_true=0.8),
    "documentary_decoys": replace(
        BASE, name="documentary_decoys",
        description="Legitimate decoys are heavily documented and temporally coherent.",
        grade_probs_decoy=(0.05, 0.25, 0.70), p_phase_coherent_decoy=0.6, p_supporting_decoy=0.5),
    "hub_background": replace(
        BASE, name="hub_background",
        description="Base observation model; hub-dominated (Barabasi-Albert) background bridged to the active graph.",
        background="hub"),
    "community_background": replace(
        BASE, name="community_background",
        description="Base observation model; community-structured (SBM) background bridged to the active graph.",
        background="community"),
}
REGIME_ORDER = list(REGIMES)

# --------------------------------------------------------------------------- #
# Separability sweep: decoy observation parameters interpolated between
# "identical to true pathways" (lambda = 0, labels carry no observable signal)
# and a well-separated setting (lambda = 1). Base sits between the two.
# --------------------------------------------------------------------------- #
FAR_DECOY = dict(grade_probs_decoy=(0.40, 0.40, 0.20), p_supporting_decoy=0.10,
                 p_phase_coherent_decoy=0.10)
SEPARABILITY_LAMBDAS = (0.0, 0.25, 0.5, 0.75, 1.0)


def separability_regime(lam: float) -> RegimeV2:
    t_g, f_g = np.array(BASE.grade_probs_true), np.array(FAR_DECOY["grade_probs_decoy"])
    g = (1 - lam) * t_g + lam * f_g
    g = tuple(float(x) for x in g / g.sum())
    sup = (1 - lam) * BASE.p_supporting_true + lam * FAR_DECOY["p_supporting_decoy"]
    coh = (1 - lam) * BASE.p_phase_coherent_true + lam * FAR_DECOY["p_phase_coherent_decoy"]
    return replace(BASE, name=f"separability_{lam:.2f}",
                   description=f"Decoy observation model interpolated (lambda={lam:.2f}) between "
                               "true-pathway parameters and a well-separated decoy setting.",
                   grade_probs_decoy=g, p_supporting_decoy=float(sup),
                   p_phase_coherent_decoy=float(coh), p_fund_obs_decoy=BASE.p_fund_obs_true)


def _v2_spec(seed: int, regime: RegimeV2) -> ScenarioSpec:
    """Minimal ScenarioSpec so the Benchmark-A edge/evidence machinery can be reused."""
    return ScenarioSpec(key=f"v2_{regime.name}", name=f"Benchmark B - {regime.name}",
                        folder=f"benchmark_B/{regime.name}", seed=seed, programmatic=True)


class LatentTruthGenerator(SyntheticCorpusGenerator):
    """Benchmark-B generator (see module docstring)."""

    def __init__(self, regime: RegimeV2, seed: int):
        super().__init__(_v2_spec(seed, regime))
        self.regime = regime
        self._counters: Dict[str, int] = {}
        # provenance used only for evaluation (never visible to the methods)
        self.bystander_nodes: Dict[str, int] = {}          # node -> attachment grade stratum
        self.true_path_nodes: List[List[str]] = []
        self.decoy_sequences: List[str] = []
        self.weak_decoy_sequences: List[str] = []
        self.path_meta: Dict[str, Dict[str, Any]] = {}     # planted sequence -> meta

    # -- neutral identifiers (no role leakage in names) -------------------- #
    def _new(self, cls: str) -> str:
        self._counters[cls] = self._counters.get(cls, 0) + 1
        # random-looking but deterministic suffix so that index order does not leak role
        nid = f"{cls}_{int(self.rng.integers(100000, 999999))}"
        while nid in self.nodes:
            nid = f"{cls}_{int(self.rng.integers(100000, 999999))}"
        self.add_node(nid, cls)
        return nid

    def _choice(self, seq, p=None):
        return seq[int(self.rng.choice(len(seq), p=p))]

    def _length(self) -> int:
        return int(self.rng.choice([2, 3, 4], p=list(self.regime.length_probs)))

    def _hop_type(self, grade_probs, p_supporting) -> str:
        g = int(self.rng.choice([1, 2, 3], p=list(grade_probs)))
        if g == 2:
            if self.rng.random() < p_supporting:
                return self._choice(SUPPORTING_TYPES)
            return "shares_link"
        return self._choice(TYPES_BY_GRADE[g])

    def _phases(self, n_hops: int, p_coherent: float) -> List[str]:
        if self.rng.random() < p_coherent:
            ph = self._choice(PHASES)
            return [ph] * n_hops
        return [self._choice(PHASES) for _ in range(n_hops)]

    def _first_hop(self, p_fund_obs: float, grade_probs, p_supporting) -> str:
        if self.rng.random() < p_fund_obs:
            return "funds"
        # undisclosed funding: observed as a weaker documentary or weak signal
        if self.rng.random() < 0.5:
            return self._choice(TYPES_BY_GRADE[3])
        return self._hop_type(grade_probs, p_supporting)

    # -- pathway sampling -------------------------------------------------- #
    def _sample_nodes(self, funder: str, n_hops: int, reuse_pool: Optional[List[str]] = None,
                      p_reuse: float = 0.0) -> List[Tuple[str, str]]:
        seq = [(funder, "Funder")]
        for pos in range(1, n_hops + 1):
            if pos == n_hops:
                cls = self._choice(TERMINAL_CHOICES)
                seq.append((self._new(cls), cls))
            elif pos == 1:
                if reuse_pool and self.rng.random() < p_reuse:
                    seq.append((self._choice(reuse_pool), "Intermediary"))
                else:
                    seq.append((self._new("Intermediary"), "Intermediary"))
            else:
                cls = self._choice(MIDDLE_CLASSES)
                seq.append((self._new(cls), cls))
        return seq

    def _plant(self, nseq, etypes, phases, *, truth: bool, kind: str) -> str:
        for i, et in enumerate(etypes):
            self.add_edge(nseq[i][0], nseq[i + 1][0], et, phase=phases[i],
                          is_ground_truth=truth, is_distractor=not truth)
        seq = " -> ".join(n for n, _ in nseq)
        if truth:
            self._record_path(f"GT_{len(self.ground_truth_paths):03d}", nseq, etypes)
            self.true_path_nodes.append([n for n, _ in nseq])
        self.path_meta[seq] = {"kind": kind, "label": int(truth),
                               "funding_observed": int(etypes[0] == "funds"),
                               "n_hops": len(etypes)}
        return seq

    def _build_active(self) -> None:
        r = self.regime
        funders = [self._new("Funder") for _ in range(r.n_funders)]
        # Path kinds are generated in a random interleaved order and draw their
        # first intermediary from one shared pool with the same reuse
        # probability, so node degree / reuse carries no information about the
        # label (removing a structural shortcut found in development).
        kinds = (["true"] * r.n_true_paths + ["decoy"] * r.n_decoy_paths
                 + ["weak_decoy"] * r.n_weak_decoys)
        order = self.rng.permutation(len(kinds))
        pool: List[str] = []
        interior_all: List[str] = []
        for idx in order:
            kind = kinds[int(idx)]
            fu = self._choice(funders)
            n = self._length()
            nseq = self._sample_nodes(fu, n, pool, r.p_decoy_reuses_true_node)
            if nseq[1][0] not in pool and n > 1:
                pool.append(nseq[1][0])
            if kind == "true":
                et = [self._first_hop(r.p_fund_obs_true, r.grade_probs_true, r.p_supporting_true)]
                et += [self._hop_type(r.grade_probs_true, r.p_supporting_true) for _ in range(n - 1)]
                ph = self._phases(n, r.p_phase_coherent_true)
            elif kind == "decoy":
                et = [self._first_hop(r.p_fund_obs_decoy, r.grade_probs_decoy, r.p_supporting_decoy)]
                et += [self._hop_type(r.grade_probs_decoy, r.p_supporting_decoy) for _ in range(n - 1)]
                ph = self._phases(n, r.p_phase_coherent_decoy)
            else:   # weak-signal-only decoy: no funding edge, every hop grade <= 2
                et = [self._hop_type((0.3, 0.7, 0.0), 0.6) for _ in range(n)]
                ph = self._phases(n, 0.7)
            seq = self._plant(nseq, et, ph, truth=(kind == "true"), kind=kind)
            if kind == "decoy":
                self.decoy_sequences.append(seq)
            elif kind == "weak_decoy":
                self.weak_decoy_sequences.append(seq)
            if kind != "weak_decoy":
                interior_all += [x for x, _ in nseq[1:-1]]
        # bystanders attached to interior nodes of true AND decoy pathways,
        # stratified by attachment grade (same rule regardless of host label)
        attach_pool = sorted(set(interior_all))
        for stratum in (1, 2, 3):
            for _ in range(r.n_bystanders_per_stratum):
                if not attach_pool:
                    break
                host = self._choice(attach_pool)
                cls = self._choice(["Proxy", "Intermediary"])   # ordinary classes: no label leakage
                b = self._new(cls)
                term_cls = self._choice(TERMINAL_CHOICES)
                t = self._new(term_cls)
                e1 = self._choice(TYPES_BY_GRADE[stratum])
                e2 = self._choice(TYPES_BY_GRADE[int(self.rng.integers(1, stratum + 1))])
                phb = self._choice(PHASES)
                self.add_edge(host, b, e1, phase=phb, is_distractor=True, is_negative_control=True)
                self.add_edge(b, t, e2, phase=phb, is_distractor=True, is_negative_control=True)
                self.bystander_nodes[b] = stratum

    # -- background topologies -------------------------------------------- #
    def _bg_type(self) -> str:
        g = int(self.rng.choice([1, 2, 3], p=list(self.regime.background_grade_probs)))
        return self._choice(TYPES_BY_GRADE[g])

    def _build_background(self) -> None:
        r = self.regime
        bg = []
        for i in range(r.n_background):
            cls = BACKGROUND_CLASSES[i % len(BACKGROUND_CLASSES)]
            bg.append(self._new(cls))
        self.background_nodes = list(bg)
        rs = int(self.rng.integers(0, 2**31 - 1))
        if r.background == "isolated":
            for _ in range(r.n_background_edges):
                s, t = self._choice(bg), self._choice(bg)
                if s != t:
                    self.add_edge(s, t, self._bg_type(), is_distractor=True)
            return
        if r.background == "hub":
            H = nx.barabasi_albert_graph(len(bg), 2, seed=rs)
        elif r.background == "community":
            k = r.n_communities
            sizes = [len(bg) // k + (1 if i < len(bg) % k else 0) for i in range(k)]
            p = [[0.15 if i == j else 0.004 for j in range(k)] for i in range(k)]
            H = nx.stochastic_block_model(sizes, p, seed=rs)
        else:
            raise ValueError(f"unknown background {r.background}")
        for u, v in H.edges():
            s, t = (bg[u], bg[v]) if self.rng.random() < 0.5 else (bg[v], bg[u])
            self.add_edge(s, t, self._bg_type(), is_distractor=True)
        # bridges from active non-terminal nodes into the background
        active = sorted(n for n, d in self.nodes.items()
                        if d.node_class not in ("Funder", "Campaign", "Report")
                        and n not in set(bg) and n not in self.bystander_nodes)
        if r.background == "hub":
            deg = np.array([H.degree(i) for i in range(len(bg))], dtype=float)
            probs = deg / deg.sum()
        else:
            probs = None
        for _ in range(r.n_bridges):
            s = self._choice(active)
            t = bg[int(self.rng.choice(len(bg), p=probs))]
            self.add_edge(s, t, self._bg_type(), is_distractor=True, is_active_noise=True)

    def build(self) -> "LatentTruthGenerator":
        self._build_active()
        self._build_background()
        return self


def generate_instance(regime: RegimeV2, seed: int) -> LatentTruthGenerator:
    return LatentTruthGenerator(regime, seed).build()
