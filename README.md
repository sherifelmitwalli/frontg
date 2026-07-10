# FrontG Synthetic Validation Harness

FrontG is a synthetic-only validation harness for a transparent network triage score. It contains no real people, organisations, websites, accounts, APIs, searches, scraping, crawling, or personal data.

The harness evaluates deterministic abstract graph topologies with planted answer keys. Scores prioritise synthetic candidate paths for expert review only; they are not probabilities, findings about real parties, or proof of wrongdoing.

## Install

```bash
python -m pip install -r requirements.txt
```

Python 3.10 or later is required.

## Run

```bash
python generate_synthetic_graph.py --scenario small
python generate_synthetic_graph.py --all
python generate_synthetic_graph.py --replications
python make_audit_visuals.py --all
python test_synthetic_harness.py
```

`--all` regenerates the small, medium, and stress scenario outputs, the cross-scenario summary, and the cross-seed consistency check (`multiseed_replication.csv`). The planted answer-key structure is fixed by design and only background filler/noise placement varies with the seed, so identical metrics across seeds are a determinism/consistency check, not an independent statistical replication.

Exact tested dependency versions are pinned in `requirements-lock.txt`; continuous integration runs the self-test suite on every push (`.github/workflows/tests.yml`).

## Decision model

The raw review-priority score is a bounded, auditable weighted sum. A raw threshold crossing is recorded separately from final triage. A path enters `high_priority_review` only when both conditions hold:

```text
raw score >= 60
has_funding_edge == 1 AND min_grade >= 2
```

The eligibility rule is versioned as `funding_and_min_grade_2_v1`. It does not alter raw scores. It prevents paths with a grade-0 or grade-1 hop, or without a funding edge, from entering the high-priority queue.

Entity resolution uses `auto_merge`, `refer_to_human`, and `keep_separate` zones. The repository reports automated performance and a separately labelled potential recall under perfect referral adjudication. No human adjudication is observed.

## Outputs

Each scenario folder contains the synthetic graph, planted answer keys, candidate and audit tables, score-bound enumeration, an integer threshold sweep from 0 through 100, sensitivity analysis, active-network-noise challenge metrics, validation metrics, reports, and figures.

`score_bounds.csv` enumerates all two-to-four-hop sequences from the controlled edge vocabulary. Its bounds are exact for that implemented vocabulary and score rule, not for arbitrary real-world networks.

`score_band_truth_summary.png` and the corresponding metric table describe planted-positive proportions by synthetic score band. They are descriptive summaries, not probability estimates.

## Scope limits

Sensitivity analysis reports complete-ranking Spearman rho and Kendall tau-b correlations, top-k membership stability, and threshold behaviour under the specified perturbations. These are robustness checks for the implemented score and synthetic candidate sets, not evidence of real-world performance. Medium and stress scenarios also add deterministic connected active-network noise that creates alternative candidate paths; the resulting false positives are retained and reported. Entity-resolution metrics describe the generated evaluation pairs; a dedicated adversarial challenge-pair evaluation remains future work.

## Main files

- `frontg_config.py`: controlled vocabulary, thresholds, score weights, and scenario definitions.
- `frontg_metrics.py`: score components, eligibility rule, exact controlled-vocabulary bounds, threshold sweep, and sensitivity metrics.
- `generate_synthetic_graph.py`: graph generation, scoring, scenario execution, and machine-readable outputs.
- `frontg_audit.py`: path and entity-resolution audit tables.
- `frontg_report_writer.py`: Markdown and HTML validation reports.
- `frontg_visualisation.py`: deterministic figures.
- `test_synthetic_harness.py`: self-checks for deterministic synthetic validation.
