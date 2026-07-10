#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
make_audit_visuals.py
=====================

Convenience CLI to (re)generate the audit reports and figures for one or more
scenarios. It reruns the deterministic harness (seed-fixed) and writes the audit
CSVs, the tracking report (Markdown + HTML) and the six figures into each
scenario sub-folder. Synthetic data only - outputs are indicators for expert
human review, not proof of wrongdoing.

    python make_audit_visuals.py --scenario small
    python make_audit_visuals.py --all
"""
from __future__ import annotations

import argparse
from pathlib import Path

import frontg_config as CFG
from frontg_config import SCENARIOS
from generate_synthetic_graph import run_scenario


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(description="Regenerate audit reports and figures (synthetic only).")
    ap.add_argument("--scenario", choices=["small", "medium", "stress"])
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--output-dir", default=str(Path(__file__).resolve().parent))
    ap.add_argument("--no-figures", action="store_true")
    args = ap.parse_args(argv)
    base = Path(args.output_dir).resolve()
    keys = CFG.ALL_SCENARIO_KEYS if (args.all or not args.scenario) else [args.scenario]
    for key in keys:
        run_scenario(SCENARIOS[key], base, make_figures=not args.no_figures)
    print("Audit reports and figures regenerated. Synthetic data only.")


if __name__ == "__main__":
    main()
