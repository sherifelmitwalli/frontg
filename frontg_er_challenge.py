#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
frontg_er_challenge.py
======================

Adversarial entity-resolution (ER) challenge set for the three-zone rule.
Synthetic, abstract organisation names only (no real organisations).

Benchmark A evaluates ER on its own generated pairs, most of which are easy
non-matches. This module builds a separately reported challenge set of
labelled name pairs in named categories:

  true aliases (should merge):  legal_suffix, case_punctuation, reorder,
                                acronym, typo, transliteration, qualifier_added
  distinct pairs (must not):    one_token_swap, plural, sibling_qualifier,
                                shared_acronym, easy_unrelated

and compares similarity rules under the same three-zone decision structure:

  * token_jaccard_v1         the published FrontG v1 rule (thresholds 0.6 / 0.4)
  * token_jaccard_calibrated same similarity, auto-merge threshold calibrated
  * normalised_token         casefold, accent strip, split on non-alphanumerics,
                             drop legal suffixes and stop words
  * normalised_token_acronym normalised_token + an acronym rule that refers
                             (never auto-merges) acronym-expansion matches
  * char_trigram             Jaccard over character 3-grams of the normalised name
  * sequence_ratio           difflib ratio on the normalised name
  * jaro_winkler             Jaro-Winkler on the normalised name

For every rule except token_jaccard_v1, the auto-merge threshold is calibrated
on a separate calibration set as the lowest value giving zero false merges
there (strictly above the highest distinct-pair similarity); the refer band is
the 0.2 below it, mirroring v1. Metrics are reported on a held-out test set.
"""
from __future__ import annotations

import itertools
import re
import unicodedata
from difflib import SequenceMatcher
from pathlib import Path
from typing import Callable, Dict, List, Tuple

import numpy as np
import pandas as pd

from frontg_config import ER_AUTO_MERGE_THRESHOLD, ER_REFER_THRESHOLD

OUT = Path(__file__).resolve().parent / "benchmark_B"

ADJ = ["Meridian", "Civic", "Beacon", "Anchor", "Summit", "Vanguard", "Cardinal", "Pioneer",
       "Heritage", "Unity", "Frontier", "Common", "Progress", "Liberty", "Standard", "Open",
       "Future", "Regional", "Citizen", "Consumer", "Market", "Reform", "Wellness", "Policy",
       "Kestrel", "Harbour", "Lantern", "Compass", "Granite", "Willow", "Juniper", "Cobalt"]
NOUN = ["Forum", "Council", "Alliance", "League", "Circle", "Coalition", "Institute",
        "Society", "Assembly", "Partnership", "Network", "Collective", "Panel", "Board"]
LEGAL = ["Ltd", "Limited", "Inc.", "CIC", "LLC", "e.V.", "PLC"]
QUALIFIERS = ["North", "South", "East", "West", "Central", "International", "Youth"]
STOP = {"for", "of", "the", "and"}
LEGAL_NORM = {"ltd", "limited", "inc", "cic", "llc", "ev", "plc"}

ALIAS_CATS = ["legal_suffix", "case_punctuation", "reorder", "acronym", "typo",
              "transliteration", "qualifier_added"]
DISTINCT_CATS = ["one_token_swap", "plural", "sibling_qualifier", "shared_acronym", "easy_unrelated"]


# --------------------------------------------------------------------------- #
# Name generation
# --------------------------------------------------------------------------- #
def _typo(rng, s: str) -> str:
    toks = s.split(" ")
    i = int(rng.integers(0, len(toks)))
    t = toks[i]
    j = int(rng.integers(1, max(2, len(t) - 1)))
    c = "abcdefghijklmnopqrstuvwxyz"[int(rng.integers(0, 26))]
    toks[i] = t[:j] + c + t[j + 1:]
    return " ".join(toks)


def _translit(s: str) -> str:
    out = s.replace("C", "K").replace("c", "k").replace("ph", "f").replace("y", "i")
    out = out.replace("e", "é", 1)
    return out


def _acronym(s: str) -> str:
    return "".join(w[0].upper() for w in s.split(" ") if w.lower() not in STOP)


def make_pairs(seed: int, n_entities: int = 150) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    # unique three-token base names: Adj1 Adj2 Noun
    combos = [(a, b, n) for a, b in itertools.permutations(ADJ, 2) for n in NOUN]
    idx = rng.choice(len(combos), size=n_entities, replace=False)
    bases = [" ".join(combos[i]) for i in idx]
    base_set = set(bases)
    rows = []

    def add(a, b, cat, truth):
        rows.append({"name_a": a, "name_b": b, "category": cat, "is_true_alias": int(truth)})

    for k, base in enumerate(bases):
        a1, a2, n = base.split(" ")
        # ---- true aliases ----
        add(base, f"{base} {LEGAL[int(rng.integers(0, len(LEGAL)))]}", "legal_suffix", True)
        add(base, base.upper().replace(" ", "-"), "case_punctuation", True)
        add(base, f"{n} for {a1} {a2}" if rng.random() < 0.5 else f"{a2} {n} {a1}", "reorder", True)
        add(base, _acronym(base), "acronym", True)
        add(base, _typo(rng, base), "typo", True)
        add(base, _translit(base), "transliteration", True)
        extra = [w for w in ("Group", "Initiative") if w != n]
        add(base, f"{base} {extra[int(rng.integers(0, len(extra)))]}", "qualifier_added", True)
        # ---- distinct pairs ----
        other_n = NOUN[(NOUN.index(n) + 1 + int(rng.integers(0, len(NOUN) - 1))) % len(NOUN)]
        swap = f"{a1} {a2} {other_n}"
        if swap not in base_set:
            add(base, swap, "one_token_swap", False)
        add(base, f"{a1} {a2} {n}s", "plural", False)
        q1, q2 = rng.choice(QUALIFIERS, size=2, replace=False)
        add(f"{base} {q1}", f"{base} {q2}", "sibling_qualifier", False)
        # a different organisation that shares the acronym of `base`
        cands = [b for b in bases if b != base and _acronym(b) == _acronym(base)]
        if not cands:
            alt = [w for w in ADJ if w[0] == a1[0] and w != a1] or [a1]
            alt2 = [w for w in ADJ if w[0] == a2[0] and w != a2] or [a2]
            altn = [w for w in NOUN if w[0] == n[0] and w != n] or [n]
            cands = [f"{alt[0]} {alt2[-1]} {altn[0]}"]
        if cands[0] != base:
            add(_acronym(base), cands[0], "shared_acronym", False)
        other = bases[(k + 1 + int(rng.integers(0, n_entities - 1))) % n_entities]
        add(base, other, "easy_unrelated", False)
    return pd.DataFrame(rows)


# --------------------------------------------------------------------------- #
# Similarity rules
# --------------------------------------------------------------------------- #
def _v1_tokens(s: str) -> set:
    return set(t for t in s.lower().replace("_", " ").split() if t)


def token_jaccard(a: str, b: str) -> float:
    ta, tb = _v1_tokens(a), _v1_tokens(b)
    return len(ta & tb) / len(ta | tb) if (ta and tb) else 0.0


def normalise(s: str) -> List[str]:
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c)).lower()
    toks = [t for t in re.split(r"[^a-z0-9]+", s.replace(".", "")) if t]
    return [t for t in toks if t not in STOP and t not in LEGAL_NORM]


def normalised_token(a: str, b: str) -> float:
    ta, tb = set(normalise(a)), set(normalise(b))
    return len(ta & tb) / len(ta | tb) if (ta and tb) else 0.0


def _norm_str(s: str) -> str:
    return " ".join(normalise(s))


def char_trigram(a: str, b: str) -> float:
    def grams(s):
        s = f"  {_norm_str(s)} "
        return {s[i:i + 3] for i in range(len(s) - 2)}
    ga, gb = grams(a), grams(b)
    return len(ga & gb) / len(ga | gb) if (ga and gb) else 0.0


def sequence_ratio(a: str, b: str) -> float:
    return SequenceMatcher(None, _norm_str(a), _norm_str(b)).ratio()


def jaro_winkler(a: str, b: str, p: float = 0.1) -> float:
    s1, s2 = _norm_str(a), _norm_str(b)
    if s1 == s2:
        return 1.0
    l1, l2 = len(s1), len(s2)
    if not l1 or not l2:
        return 0.0
    md = max(l1, l2) // 2 - 1
    m1, m2 = [False] * l1, [False] * l2
    m = 0
    for i in range(l1):
        for j in range(max(0, i - md), min(l2, i + md + 1)):
            if not m2[j] and s1[i] == s2[j]:
                m1[i] = m2[j] = True
                m += 1
                break
    if not m:
        return 0.0
    t, k = 0, 0
    for i in range(l1):
        if m1[i]:
            while not m2[k]:
                k += 1
            if s1[i] != s2[k]:
                t += 1
            k += 1
    jaro = (m / l1 + m / l2 + (m - t / 2) / m) / 3
    pre = 0
    for x, y in zip(s1[:4], s2[:4]):
        if x != y:
            break
        pre += 1
    return jaro + pre * p * (1 - jaro)


def acronym_match(a: str, b: str) -> bool:
    na, nb = normalise(a), normalise(b)
    for short, long_ in ((na, nb), (nb, na)):
        if len(short) == 1 and len(long_) >= 2 and short[0] == "".join(w[0] for w in long_):
            return True
    return False


RULES: Dict[str, Callable[[str, str], float]] = {
    "token_jaccard_v1": token_jaccard,
    "token_jaccard_calibrated": token_jaccard,
    "normalised_token": normalised_token,
    "normalised_token_acronym": normalised_token,
    "char_trigram": char_trigram,
    "sequence_ratio": sequence_ratio,
    "jaro_winkler": jaro_winkler,
}
RULE_LABELS = {
    "token_jaccard_v1": "Token Jaccard, published thresholds (FrontG v1)",
    "token_jaccard_calibrated": "Token Jaccard, calibrated",
    "normalised_token": "Normalised token Jaccard, calibrated",
    "normalised_token_acronym": "Normalised token Jaccard + acronym referral",
    "char_trigram": "Character 3-gram Jaccard, calibrated",
    "sequence_ratio": "Sequence ratio, calibrated",
    "jaro_winkler": "Jaro-Winkler, calibrated",
}


def zones(rule: str, sims: np.ndarray, pairs: pd.DataFrame, t_am: float, t_ref: float) -> np.ndarray:
    z = np.where(sims >= t_am, "auto_merge", np.where(sims >= t_ref, "refer_to_human", "keep_separate"))
    if rule == "normalised_token_acronym":
        acr = np.array([acronym_match(a, b) for a, b in zip(pairs["name_a"], pairs["name_b"])])
        z = np.where(acr & (z != "auto_merge"), "refer_to_human", z)
    return z


def calibrate(rule: str, cal: pd.DataFrame) -> Tuple[float, float]:
    if rule == "token_jaccard_v1":
        return ER_AUTO_MERGE_THRESHOLD, ER_REFER_THRESHOLD
    f = RULES[rule]
    sims = np.array([f(a, b) for a, b in zip(cal["name_a"], cal["name_b"])])
    max_distinct = float(sims[cal["is_true_alias"].values == 0].max())
    t_am = min(1.0, round(max_distinct + 1e-6, 6))
    if t_am <= max_distinct:          # distinct pairs reach 1.0: nothing can be auto-merged safely
        t_am = 1.0 + 1e-9
    return t_am, max(0.0, t_am - 0.2)


def evaluate(cal_seed: int = 501, test_seed: int = 502, out: Path = OUT) -> Dict[str, pd.DataFrame]:
    cal, test = make_pairs(cal_seed), make_pairs(test_seed)
    overall, by_cat = [], []
    for rule, f in RULES.items():
        t_am, t_ref = calibrate(rule, cal)
        sims = np.array([f(a, b) for a, b in zip(test["name_a"], test["name_b"])])
        z = zones(rule, sims, test, t_am, t_ref)
        y = test["is_true_alias"].values
        auto, ref = z == "auto_merge", z == "refer_to_human"
        n_alias, n_dist = int(y.sum()), int((1 - y).sum())
        overall.append({
            "rule": rule, "rule_label": RULE_LABELS[rule],
            "auto_merge_threshold": round(t_am, 6), "refer_threshold": round(t_ref, 6),
            "n_pairs": len(test), "n_true_alias_pairs": n_alias, "n_distinct_pairs": n_dist,
            "false_merges": int(np.sum(auto & (y == 0))),
            "false_merge_rate": round(float(np.sum(auto & (y == 0)) / n_dist), 4),
            "auto_merge_recall": round(float(np.sum(auto & (y == 1)) / n_alias), 4),
            "potential_recall_with_referral": round(float(np.sum((auto | ref) & (y == 1)) / n_alias), 4),
            "referral_rate": round(float(ref.mean()), 4),
            "referred_distinct_pairs": int(np.sum(ref & (y == 0))),
        })
        for cat in ALIAS_CATS + DISTINCT_CATS:
            mk = test["category"].values == cat
            by_cat.append({"rule": rule, "category": cat, "is_true_alias": int(cat in ALIAS_CATS),
                           "n": int(mk.sum()),
                           "auto_merge": round(float(auto[mk].mean()), 4),
                           "refer": round(float(ref[mk].mean()), 4),
                           "keep_separate": round(float((~auto & ~ref)[mk].mean()), 4)})
    res = {"overall": pd.DataFrame(overall), "by_category": pd.DataFrame(by_cat), "test_pairs": test}
    out.mkdir(parents=True, exist_ok=True)
    res["overall"].to_csv(out / "er_challenge_overall.csv", index=False)
    res["by_category"].to_csv(out / "er_challenge_by_category.csv", index=False)
    test.to_csv(out / "er_challenge_test_pairs.csv", index=False)
    return res


if __name__ == "__main__":
    r = evaluate()
    pd.set_option("display.width", 200)
    print(r["overall"].to_string(index=False))
