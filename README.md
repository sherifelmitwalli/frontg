# FrontG Synthetic Validation Harness

FrontG is a synthetic-only validation harness for a transparent, human-review-gated network triage score.

The repository contains two complementary benchmarks:

- **Benchmark A** (the original harness, unchanged in method and results): fixed planted templates at three scales, used as **specification tests** with exact score bounds.
- **Benchmark B** (added in version 2.0.0): a stochastic **latent-truth** benchmark with learned and heuristic comparators, distribution-shift regimes, a separability sweep, a template-learnability diagnostic, and an adversarial entity-resolution challenge set.

The repository contains no real people, organisations, websites, accounts, APIs, searches, scraping, crawling, or personal data. See `CHANGELOG.md` for changes since version 1.0.0.

The harness evaluates deterministic abstract graph topologies with planted answer keys. Scores prioritise synthetic candidate paths for expert review only; they are not probabilities, findings about real parties, or proof of wrongdoing.

## Install

```bash
python -m pip install -r requirements.txt
```

Python 3.10 or later is required.

## Run

```bash
# Benchmark A (fixed templates; specification tests)
python generate_synthetic_graph.py --all
python test_synthetic_harness.py

# Benchmark B (latent truth; comparators, regimes, sweep, ER challenge) ~4 min
python run_v2_benchmark.py
python test_benchmark_B.py

# Manuscript figures (180 mm, 300 dpi, PNG + TIFF)
python make_v2_figures.py
```

`--all` regenerates the small, medium, and stress scenario outputs, the cross-scenario summary, and the cross-seed consistency check (`multiseed_replication.csv`). The planted answer-key structure is fixed by design and only background filler/noise placement varies with the seed, so identical metrics across seeds are a determinism/consistency check, not an independent statistical replication.

Exact tested dependency versions are pinned in `requirements-lock.txt`; continuous integration runs the self-test suite on every push (`.github/workflows/tests.yml`).

## Folder contents

| Path | Contents |
|---|---|
| `*.py` | All code (Benchmark A harness, Benchmark B, comparators, ER challenge, figures, tests) |
| `scenario_A_small/`, `scenario_B_medium/`, `scenario_C_stress/` | Benchmark A synthetic networks, answer keys, audits, metrics, figures |
| `benchmark_B/` | Benchmark B per-instance metrics, summaries, separability sweep, diagnostics, ER challenge |
| `cross_scenario_validation_summary.csv`, `multiseed_replication.csv` | Benchmark A cross-scenario and cross-seed tables |
| `figures_for_submission/` | Manuscript Figures 1-8 (PNG + TIFF, 300 dpi) and Supplementary Figures S1-S4 |
| `figures_benchmark_A/` | Archived source images for Figures 2-3 and S1-S4 |
| `algorithm_*.md` | Pseudocode |

Every file produced by the code can be deleted and regenerated with the commands above; a clean rebuild reproduces those files byte for byte. Three `calibration_plot.png` files and the root-level `review_priority_formula.csv` are retained from version 1.0.0 for continuity; the current code no longer writes them, and the formula table is reproduced in each scenario folder.

## Decision model

The raw review-priority score is a bounded, auditable weighted sum. A raw threshold crossing is recorded separately from final triage. A path enters `high_priority_review` only when both conditions hold:

```text
raw score >= 60
has_funding_edge == 1 AND min_grade >= 2
```

The eligibility rule is versioned as `funding_and_min_grade_2_v1`. It does not alter raw scores. It prevents paths with a grade-0 or grade-1 hop, or without a funding edge, from entering the high-priority queue. At the published weights it is non-binding (exact enumeration shows that no ineligible path can score above 57.7, below the threshold of 60); it is retained as an invariant that holds under any change to the weights, gate or threshold, or when wrapped around another ranker (Benchmark B).

Entity resolution uses `auto_merge`, `refer_to_human`, and `keep_separate` zones. The repository reports automated performance and a separately labelled potential recall under perfect referral adjudication. No human adjudication is observed.

## Outputs

Each scenario folder contains the synthetic graph, planted answer keys, candidate and audit tables, score-bound enumeration, an integer threshold sweep from 0 through 100, sensitivity analysis, active-network-noise challenge metrics, validation metrics, reports, and figures.

`score_bounds.csv` enumerates all two-to-four-hop sequences from the controlled edge vocabulary. Its bounds are exact for that implemented vocabulary and score rule, not for arbitrary real-world networks.

`score_band_truth_summary.png` and the corresponding metric table describe planted-positive proportions by synthetic score band. They are descriptive summaries, not probability estimates.

## Scope limits

Sensitivity analysis reports complete-ranking Spearman rho and Kendall tau-b correlations, top-k membership stability, and threshold behaviour under the specified perturbations. These are robustness checks for the implemented score and synthetic candidate sets, not evidence of real-world performance. Medium and stress scenarios also add deterministic connected active-network noise that creates alternative candidate paths; the resulting false positives are retained and reported. Benchmark-A entity-resolution metrics describe its generated evaluation pairs; the adversarial challenge set in `frontg_er_challenge.py` is reported separately and shows that the published token-Jaccard rule false-merges sibling-qualifier names.

## Benchmark B

Benchmark A plants answer-key pathways from fixed templates. That makes it a good specification test suite, but a supervised learner reproduces its answer key perfectly (AUPRC 1.0 across scenarios; `benchmark_B/diagnostic_learnability.csv`), so Benchmark A results are not evidence of discriminative accuracy.

Benchmark B samples true influence pathways and legitimate decoy pathways from the same structural distribution (shared funders, a shared intermediary pool, neutral identifiers). They differ only through overlapping class-conditional observation probabilities. Each regime is evaluated on 100 independent test instances:

| Regime | What changes |
|---|---|
| `base` | overlapping evidence distributions; isolated background |
| `hidden_funding` | true pathways' funding is observed only 40% of the time |
| `weak_coordination` | true pathways mostly evidenced by weak signals |
| `documentary_decoys` | legitimate decoys heavily documented and temporally coherent |
| `hub_background` | Barabasi-Albert background bridged to the active graph |
| `community_background` | stochastic-block-model background bridged to the active graph |

Comparators: FrontG (published rule), two ablations, FrontG with a tuned threshold, mean evidence grade, path PageRank centrality, logistic regression (FrontG features; all features), gradient boosting, gradient boosting wrapped by the FrontG eligibility rule, and an in-regime gradient-boosting reference. Learned models and tuned thresholds use base-regime training and validation instances only, so the other regimes are distribution shifts.

Outputs in `benchmark_B/`: `instance_metrics.csv`, `summary_by_regime_method.csv`, `safety_pooled_all_regimes.csv`, `separability_summary.csv`, `diagnostic_learnability.csv`, `er_challenge_overall.csv`, `er_challenge_by_category.csv`, `regimes.csv`, `thresholds.json`.

## Main files

- `frontg_config.py`: controlled vocabulary, thresholds, score weights, and scenario definitions.
- `frontg_metrics.py`: score components, eligibility rule, exact controlled-vocabulary bounds, threshold sweep, and sensitivity metrics.
- `generate_synthetic_graph.py`: graph generation, scoring, scenario execution, and machine-readable outputs.
- `frontg_audit.py`: path and entity-resolution audit tables.
- `frontg_report_writer.py`: Markdown and HTML validation reports.
- `frontg_visualisation.py`: deterministic figures.
- `test_synthetic_harness.py`: self-checks for Benchmark A.
- `frontg_v2_generator.py`: Benchmark-B latent-truth generator and regimes.
- `frontg_v2_methods.py`: candidate extraction, comparators, and per-instance evaluation.
- `run_v2_benchmark.py`: Benchmark-B runner, separability sweep, and learnability diagnostic.
- `frontg_er_challenge.py`: adversarial entity-resolution challenge set.
- `make_v2_figures.py`: manuscript figures.
- `test_benchmark_B.py`: self-checks for Benchmark B.
- `algorithm_1_topology_generation.md`, `algorithm_2_path_scoring.md`, `algorithm_3_benchmark_B.md`: pseudocode.
