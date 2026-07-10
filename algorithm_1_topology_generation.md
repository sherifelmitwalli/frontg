# Algorithm 1 - Synthetic topology generation and answer-key construction

**Inputs:** a deterministic `ScenarioSpec` (fixed seed; target sizes; counts of
proxy paths, false-friend pairs, alias groups, isolated and embedded negative
controls, weak-signal chains, false leads and noise edges).
**Outputs:** a synthetic directed multigraph `G`; answer keys for seeded proxy
paths, entity-resolution pairs, negative controls and weak-signal chains. All
entities are abstract and synthetic; no real-world data is used.

```
function BUILD_TOPOLOGY(spec):
    rng <- deterministic RNG seeded with spec.seed
    G   <- empty directed multigraph

    # RQ1: seed known multi-hop proxy paths (the recoverable ground truth)
    for i in 1..spec.n_proxy_paths:
        choose a 3-hop or 4-hop chain Funder -> Intermediary -> ... -> (Campaign|Report)
        assign documentary edge types (funds, partners_with, hosts, speaks_at,
            publishes); cluster adjacent hops into the same campaign phase
        add nodes and edges to G, marked is_ground_truth = true

    # weaker funder-originated false leads (distractors, label 0)
    for j in 1..spec.n_false_leads:
        build Funder -> Intermediary -> ... ending in a LOW-grade hop

    # RQ2: entity-resolution answer key
    for k in 1..spec.n_false_friend_pairs:           # distinct identities
        create two surface forms sharing 2 tokens, differing in 1; distinct
            canonical IDs; expected decision: never auto-merge
    for g in 1..spec.n_alias_groups:                 # same identity
        create 2-3 surface forms sharing a canonical ID; some groups include a
            re-ordered member that lands in the human-referral band

    # RQ3a: isolated negative controls (disconnected)
    for c in 1..spec.n_negative_controls:
        create an IndependentControl cluster (grade 0-1 edges) with NO link to
            the seeded structure; expected priority ~ 0

    # RQ3b: embedded negative controls (weakly attached, funder-reachable)
    for e in 1..spec.n_embedded_controls:
        attach an IndependentControl to a seeded intermediary/proxy using ONLY
            weak (grade <= 2) edges, terminating at its own Campaign/Report;
            the control now appears inside enumerated candidate paths and the
            test is whether it stays below the triage threshold

    # RQ5: adversarial weak-signal-only chains
    for w in 1..spec.n_weak_chains:
        build Funder -> ... -> (Campaign|Report) using ONLY grade <= 2 signals
            (shared links, amplification, similar language, co-occurrence);
            expected flag status: never flagged, gated or ungated

    # background noise within an isolated filler pool (does not touch funders)
    add filler Media/Social/Report/Event nodes with weak co-occurrence,
        similar-language and amplification edges
    pad nodes and edges deterministically to the scenario size targets

    # connected active-network noise challenge (medium and stress scenarios)
    for a in 1..spec.n_active_*:
        add labelled (is_active_noise = true) edges from funder-reachable
            intermediaries to alternative terminals and cross-path proxies,
            including weak signals and misleading documentary-grade edges;
            these deliberately create alternative funder-to-terminal candidate
            paths, and all resulting false positives are retained and reported

    return G and all answer keys
```

**Key invariants.** Funders connect only along their seeded chains, the
controlled false leads, the embedded-control attachments, the weak-signal
chains and the separately labelled connected active-noise edges, so candidate
enumeration stays tractable at every scale, and every funder-originated
structure has a known label. Unlabelled filler noise remains isolated and never
forges spurious funder-originated proxy paths; separately labelled connected
active noise (medium and stress scenarios) deliberately creates alternative
funder-originated candidate paths for adverse challenge testing, and the
resulting false positives are retained and reported rather than tuned away.
Every output is a synthetic indicator for expert human review only.
