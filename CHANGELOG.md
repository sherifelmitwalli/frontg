# Changelog

## 2.0.0 (October 2026)

Adds Benchmark B and supporting analyses for the revised manuscript. Benchmark A's method, parameters and reported metrics are unchanged.

### Added
- `frontg_v2_generator.py`: Benchmark B, a stochastic latent-truth generator. True and decoy pathways share funders, an intermediary pool, path-length distribution and neutral identifiers, and differ only through overlapping class-conditional observation probabilities. Includes undisclosed funding, bystanders stratified by attachment grade (1, 2, 3), weak-signal-only decoys, isolated / hub (Barabási–Albert) / community (stochastic block model) backgrounds, six regimes, and a separability sweep.
- `frontg_v2_methods.py`, `run_v2_benchmark.py`: ten comparators evaluated on 100 test instances per regime with 95% bootstrap confidence intervals: FrontG; FrontG without eligibility; FrontG without eligibility or gate; FrontG with tuned threshold; mean evidence grade; path PageRank centrality; logistic regression (FrontG features; all features); gradient boosting; gradient boosting wrapped by the FrontG eligibility rule; and an in-regime gradient-boosting reference. Also includes label-independent safety metrics, a template-learnability diagnostic and a topology-only structural-leakage probe.
- `frontg_er_challenge.py`: adversarial entity-resolution challenge set (seven alias and five distinct-pair categories) comparing seven similarity rules under the three-zone decision structure.
- `make_v2_figures.py`, `figures_for_submission/`, `figures_benchmark_A/`: manuscript figures (180 mm, 300 dpi, PNG and TIFF).
- `test_benchmark_B.py`: 25 self-checks for Benchmark B; CI now runs both suites (56 checks in total).
- `algorithm_3_benchmark_B.md`: pseudocode for Benchmark B.
- `benchmark_B/`: all Benchmark B outputs.

### Changed
- `frontg_metrics.py`: two additional exact-bound families (`no_funding_any_grade`, `ineligible_any`) in `score_bounds.csv`. The existing five rows are unchanged.
- Determinism fixes with no change to any metric: stable sort for tied scores; candidate graph built in sorted order rather than set order (set order varies with Python's per-process hash seed); deterministic node order in network drawings; tracking report written after the figures; GraphML written with networkx's pure-Python writer, so the files are identical whether or not lxml is installed. As a result, candidate identifiers for tied paths and the byte content of some figures and reports differ from 1.0.0; all scores, labels and metrics are identical.
- `requirements*.txt`: add scikit-learn and pillow.
- README and citation metadata updated for both benchmarks.
