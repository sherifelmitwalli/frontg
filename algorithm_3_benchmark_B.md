# Algorithm 3 - Benchmark B: latent-truth generation, comparators, and evaluation

**Inputs:** a regime (observation-model and topology parameters, `frontg_v2_generator.RegimeV2`);
seed ranges for training, validation, test, and in-regime reference training.
**Outputs:** per-instance metrics for every comparator; regime summaries with 95%
bootstrap confidence intervals; separability sweep; learnability diagnostic;
adversarial entity-resolution results. Synthetic data only.

```
function GENERATE_INSTANCE(regime, seed):
    funders <- n_funders new Funder nodes (neutral random identifiers)
    kinds   <- shuffle([true]*n_true + [decoy]*n_decoy + [weak_decoy]*n_weak)
    pool    <- {}                                    # shared intermediary pool
    for kind in kinds:
        f <- random(funders); L <- sample({2,3,4}, length_probs)
        nodes <- f, intermediary (reuse from pool w.p. p_reuse, else new),
                 middle nodes (Proxy/Event/Intermediary/MediaOutlet), terminal
        if kind == true:   hop types ~ observation model for TRUE pathways
                           (funding observed w.p. p_fund_obs_true, else a
                            grade-3 or weaker signal; hop grades ~ grade_probs_true;
                            grade-2 hops are supporting signals w.p. p_supporting_true;
                            phases coherent w.p. p_phase_coherent_true)
        if kind == decoy:  same, with the DECOY parameters (legitimate relation)
        if kind == weak:   every hop grade <= 2, no funding edge
        record label 1 only for kind == true (exact node sequence)
    for stratum in {1, 2, 3}:                        # bystanders
        attach new independent actor B to a random interior node of a true OR
        decoy pathway by a grade-`stratum` edge; B -> new terminal by grade <= stratum
    background: isolated filler | Barabasi-Albert hubs | SBM communities,
                bridged into the active graph (hub/community) by n_bridges edges

function EVALUATE(regimes):
    train, valid <- candidate tables from base-regime seeds   # labels used only here
    fit logistic regression (FrontG features; all features), gradient boosting
    tune F1-optimal thresholds on valid for every non-FrontG decision rule
    for regime in regimes:
        fit in-regime gradient boosting on that regime's own seeds (reference only)
        for seed in test seeds:
            C <- ENUMERATE_AND_SCORE(GENERATE_INSTANCE(regime, seed))   # Algorithm 2
            for method in comparators:
                record precision, recall, F1, AUPRC, flags,
                       flags containing a grade <= 1 hop,
                       weak-evidence-only flags (no funding edge, max grade <= 2),
                       bystander flags by attachment stratum,
                       recall split by whether the true pathway's funding was observed
    summarise: instance means with 95% percentile bootstrap CI (2,000 resamples)

function SEPARABILITY_SWEEP(lambdas):
    for lambda in lambdas:   # decoy parameters = (1-lambda)*true + lambda*far-decoy
        train/tune/test within the same lambda; record as above

function DIAGNOSTIC():
    Benchmark A: gradient boosting trained on one fixed-template scenario,
                 tested on another (template learnability)
    Benchmark B: gradient boosting on evidence features; topology-only probe
    report AUPRC against prevalence and the feature-ambiguity rate
```

The FrontG decision rule, weights, gate, threshold (60), and eligibility rule are
taken unchanged from Algorithm 2; nothing in Benchmark B tunes them except the
explicitly labelled `frontg_tuned` comparator.
