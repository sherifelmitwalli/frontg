# Algorithm 2 - Scoring, eligibility, robustness, and audit generation

**Inputs:** synthetic graph `G`; transparent `ScoreWeights`; fixed
`triage_threshold`; and answer keys from Algorithm 1.
**Outputs:** scored candidate paths; raw-threshold and final-triage metrics;
robustness tables; and a path-by-path audit trail. Scores are synthetic triage
indicators for expert review only, never proof of wrongdoing.

```
function SCORE_AND_AUDIT(G, weights, threshold, answer_keys):
    for funder in funders(G):
        for path in all_simple_paths(G, funder, terminals, cutoff = 4):
            if length(path) >= 3: CANDIDATES.append(path)

    for path in CANDIDATES:
        feats <- features(path)        # highest-grade edge per hop
        support <- feats.min_grade / 4
        raw <- weighted bounded score using funding, evidence grades,
               evidence-type diversity, temporal clustering, and support-gated
               semantic/amplification/co-occurrence signals
        path.score <- clip(raw, 0, 100)
        path.score_ungated <- ablation with support fixed to 1
        path.score_threshold_crossed <- (path.score >= threshold)
        path.eligible_for_high_priority <-
            (path.has_funding_edge == 1 AND path.min_grade >= 2)
        path.high_priority_review <-
            (path.score_threshold_crossed AND path.eligible_for_high_priority)
        retain raw score and eligibility explanation in the audit table

    metrics.rq1 <- final high-priority precision/recall/F1 versus seeded paths
    metrics.rq2 <- automated three-zone entity resolution, referral burden,
                   and potential recall under perfect referral adjudication
                   (not observed human performance)
    metrics.rq3 <- isolated and embedded-control specificity
    metrics.rq4 <- raw-threshold behaviour and descriptive score-band truth summary
    metrics.rq5 <- weak-chain behaviour, exact controlled-vocabulary score bounds,
                   integer threshold sweep, weight perturbation, and replications

    write machine-readable outputs, audit CSVs, Markdown report, HTML report,
    and deterministic figures
```

The score-bound enumeration evaluates every two-to-four-hop sequence from the
implemented controlled edge vocabulary. It is exact for that vocabulary and
score rule. The separate eligibility rule does not modify the raw score; it
prevents paths without a funding edge or with a grade-0/1 hop from entering the
high-priority queue.
