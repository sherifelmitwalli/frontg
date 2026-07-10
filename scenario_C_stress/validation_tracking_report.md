# Validation Tracking Report - Scenario C - Larger stress-test scenario

_Synthetic validation harness (seed = 242)._

**All entities and relationships are synthetic and abstract. Outputs are indicators for expert human review only - not proof of misconduct, undisclosed conflicts of interest, hidden funding, or any wrongdoing.**

## 1. Network summary

| Quantity | Value |
| --- | --- |
| Total nodes | 504 |
| Total edges | 1280 |
| Node classes | 9 |
| Relationship types | 10 |
| Seeded proxy paths | 26 |
| Candidate paths | 120 |
| False-friend entities | 36 |
| True-alias groups | 12 |
| Negative-control subgraphs (isolated + embedded) | 36 |
| Weak-signal chains (RQ5) | 10 |

**Triage threshold (review-priority cut-off): 60.0 / 100.** Scores are triage indicators for expert review only.

## 2. Seeded ground-truth proxy paths (answer key)

| Path ID | Node sequence | Relationship types | Grades |
| --- | --- | --- | --- |
| GT_PATH_000 | Funder_000 -> Intermediary_000 -> Proxy_000 -> Campaign_000 | funds -> partners_with -> hosts | 4 -> 3 -> 3 |
| GT_PATH_001 | Funder_001 -> Intermediary_001 -> Event_001 -> Proxy_001 -> Report_001 | funds -> hosts -> speaks_at -> publishes | 4 -> 3 -> 3 -> 3 |
| GT_PATH_002 | Funder_002 -> Intermediary_002 -> Proxy_002 -> Campaign_002 | funds -> partners_with -> amplifies | 4 -> 3 -> 2 |
| GT_PATH_003 | Funder_003 -> Intermediary_003 -> Event_003 -> Report_003 | funds -> hosts -> publishes | 4 -> 3 -> 3 |
| GT_PATH_004 | Funder_004 -> Intermediary_004 -> Proxy_004 -> Campaign_004 | funds -> partners_with -> hosts | 4 -> 3 -> 3 |
| GT_PATH_005 | Funder_005 -> Intermediary_005 -> Event_005 -> Proxy_005 -> Report_005 | funds -> hosts -> speaks_at -> publishes | 4 -> 3 -> 3 -> 3 |
| GT_PATH_006 | Funder_006 -> Intermediary_006 -> Proxy_006 -> Campaign_006 | funds -> partners_with -> amplifies | 4 -> 3 -> 2 |
| GT_PATH_007 | Funder_007 -> Intermediary_007 -> Event_007 -> Report_007 | funds -> hosts -> publishes | 4 -> 3 -> 3 |
| GT_PATH_008 | Funder_008 -> Intermediary_008 -> Proxy_008 -> Campaign_008 | funds -> partners_with -> hosts | 4 -> 3 -> 3 |
| GT_PATH_009 | Funder_009 -> Intermediary_009 -> Event_009 -> Proxy_009 -> Report_009 | funds -> hosts -> speaks_at -> publishes | 4 -> 3 -> 3 -> 3 |
| GT_PATH_010 | Funder_010 -> Intermediary_010 -> Proxy_010 -> Campaign_010 | funds -> partners_with -> amplifies | 4 -> 3 -> 2 |
| GT_PATH_011 | Funder_011 -> Intermediary_011 -> Event_011 -> Report_011 | funds -> hosts -> publishes | 4 -> 3 -> 3 |
| GT_PATH_012 | Funder_012 -> Intermediary_012 -> Proxy_012 -> Campaign_012 | funds -> partners_with -> hosts | 4 -> 3 -> 3 |
| GT_PATH_013 | Funder_013 -> Intermediary_013 -> Event_013 -> Proxy_013 -> Report_013 | funds -> hosts -> speaks_at -> publishes | 4 -> 3 -> 3 -> 3 |
| GT_PATH_014 | Funder_014 -> Intermediary_014 -> Proxy_014 -> Campaign_014 | funds -> partners_with -> amplifies | 4 -> 3 -> 2 |
| GT_PATH_015 | Funder_015 -> Intermediary_015 -> Event_015 -> Report_015 | funds -> hosts -> publishes | 4 -> 3 -> 3 |
| GT_PATH_016 | Funder_016 -> Intermediary_016 -> Proxy_016 -> Campaign_016 | funds -> partners_with -> hosts | 4 -> 3 -> 3 |
| GT_PATH_017 | Funder_017 -> Intermediary_017 -> Event_017 -> Proxy_017 -> Report_017 | funds -> hosts -> speaks_at -> publishes | 4 -> 3 -> 3 -> 3 |
| GT_PATH_018 | Funder_018 -> Intermediary_018 -> Proxy_018 -> Campaign_018 | funds -> partners_with -> amplifies | 4 -> 3 -> 2 |
| GT_PATH_019 | Funder_019 -> Intermediary_019 -> Event_019 -> Report_019 | funds -> hosts -> publishes | 4 -> 3 -> 3 |
| GT_PATH_020 | Funder_020 -> Intermediary_020 -> Proxy_020 -> Campaign_020 | funds -> partners_with -> hosts | 4 -> 3 -> 3 |
| GT_PATH_021 | Funder_021 -> Intermediary_021 -> Event_021 -> Proxy_021 -> Report_021 | funds -> hosts -> speaks_at -> publishes | 4 -> 3 -> 3 -> 3 |
| GT_PATH_022 | Funder_022 -> Intermediary_022 -> Proxy_022 -> Campaign_022 | funds -> partners_with -> amplifies | 4 -> 3 -> 2 |
| GT_PATH_023 | Funder_023 -> Intermediary_023 -> Event_023 -> Report_023 | funds -> hosts -> publishes | 4 -> 3 -> 3 |
| GT_PATH_024 | Funder_024 -> Intermediary_024 -> Proxy_024 -> Campaign_024 | funds -> partners_with -> hosts | 4 -> 3 -> 3 |
| GT_PATH_025 | Funder_025 -> Intermediary_025 -> Event_025 -> Proxy_025 -> Report_025 | funds -> hosts -> speaks_at -> publishes | 4 -> 3 -> 3 -> 3 |

## 3. Recovered candidate paths (flagged true positives)

| ID | Node sequence | Score |
| --- | --- | --- |
| GT_PATH_003 | Funder_003 -> Intermediary_003 -> Event_003 -> Report_003 | 67.80 |
| GT_PATH_004 | Funder_004 -> Intermediary_004 -> Proxy_004 -> Campaign_004 | 67.80 |
| GT_PATH_019 | Funder_019 -> Intermediary_019 -> Event_019 -> Report_019 | 67.80 |
| GT_PATH_007 | Funder_007 -> Intermediary_007 -> Event_007 -> Report_007 | 67.80 |
| GT_PATH_000 | Funder_000 -> Intermediary_000 -> Proxy_000 -> Campaign_000 | 67.80 |
| GT_PATH_016 | Funder_016 -> Intermediary_016 -> Proxy_016 -> Campaign_016 | 67.80 |
| GT_PATH_011 | Funder_011 -> Intermediary_011 -> Event_011 -> Report_011 | 67.80 |
| GT_PATH_015 | Funder_015 -> Intermediary_015 -> Event_015 -> Report_015 | 67.80 |
| GT_PATH_012 | Funder_012 -> Intermediary_012 -> Proxy_012 -> Campaign_012 | 67.80 |
| GT_PATH_008 | Funder_008 -> Intermediary_008 -> Proxy_008 -> Campaign_008 | 67.80 |
| GT_PATH_020 | Funder_020 -> Intermediary_020 -> Proxy_020 -> Campaign_020 | 67.80 |
| GT_PATH_024 | Funder_024 -> Intermediary_024 -> Proxy_024 -> Campaign_024 | 67.80 |
| GT_PATH_023 | Funder_023 -> Intermediary_023 -> Event_023 -> Report_023 | 67.80 |
| GT_PATH_001 | Funder_001 -> Intermediary_001 -> Event_001 -> Proxy_001 -> Report_001 | 65.78 |
| GT_PATH_013 | Funder_013 -> Intermediary_013 -> Event_013 -> Proxy_013 -> Report_013 | 65.78 |
| GT_PATH_017 | Funder_017 -> Intermediary_017 -> Event_017 -> Proxy_017 -> Report_017 | 65.78 |
| GT_PATH_009 | Funder_009 -> Intermediary_009 -> Event_009 -> Proxy_009 -> Report_009 | 65.78 |
| GT_PATH_005 | Funder_005 -> Intermediary_005 -> Event_005 -> Proxy_005 -> Report_005 | 65.78 |
| GT_PATH_025 | Funder_025 -> Intermediary_025 -> Event_025 -> Proxy_025 -> Report_025 | 65.78 |
| GT_PATH_021 | Funder_021 -> Intermediary_021 -> Event_021 -> Proxy_021 -> Report_021 | 65.78 |
| GT_PATH_018 | Funder_018 -> Intermediary_018 -> Proxy_018 -> Campaign_018 | 63.80 |
| GT_PATH_022 | Funder_022 -> Intermediary_022 -> Proxy_022 -> Campaign_022 | 63.80 |
| GT_PATH_014 | Funder_014 -> Intermediary_014 -> Proxy_014 -> Campaign_014 | 63.80 |
| GT_PATH_010 | Funder_010 -> Intermediary_010 -> Proxy_010 -> Campaign_010 | 63.80 |
| GT_PATH_002 | Funder_002 -> Intermediary_002 -> Proxy_002 -> Campaign_002 | 63.80 |
| GT_PATH_006 | Funder_006 -> Intermediary_006 -> Proxy_006 -> Campaign_006 | 63.80 |

Path-recovery recall **1.0**; precision **0.3881**.

## 4. Missed paths (seeded but not flagged)

None - all seeded proxy paths were recovered.

## 5. False-positive paths (flagged but not seeded)

| Candidate ID | Node sequence | Score |
| --- | --- | --- |
| CAND_0010 | Funder_001 -> Intermediary_001 -> Campaign_024 | 69.45 |
| CAND_0048 | Funder_005 -> Intermediary_005 -> Campaign_EC08 | 69.45 |
| CAND_0076 | Funder_009 -> Intermediary_009 -> Campaign_L003 | 69.45 |
| CAND_0029 | Funder_003 -> Intermediary_003 -> Campaign_EC04 | 66.45 |
| CAND_0055 | Funder_006 -> Intermediary_006 -> Campaign_EC10 | 66.45 |
| CAND_0023 | Funder_002 -> Intermediary_002 -> Campaign_EC02 | 66.45 |
| CAND_0059 | Funder_007 -> Intermediary_007 -> Campaign_EC12 | 66.45 |
| CAND_0070 | Funder_008 -> Intermediary_008 -> Campaign_L001 | 66.45 |
| CAND_0033 | Funder_004 -> Intermediary_004 -> Campaign_EC06 | 66.45 |
| CAND_0002 | Funder_000 -> Intermediary_000 -> Campaign_022 | 66.45 |
| CAND_0046 | Funder_005 -> Intermediary_005 -> Campaign_024 | 64.20 |
| CAND_0012 | Funder_001 -> Intermediary_001 -> Campaign_016 | 64.20 |
| CAND_0027 | Funder_003 -> Intermediary_003 -> Campaign_016 | 63.70 |
| CAND_0061 | Funder_007 -> Intermediary_007 -> Campaign_024 | 63.70 |
| CAND_0075 | Funder_009 -> Intermediary_009 -> Campaign_024 | 61.70 |
| CAND_0044 | Funder_005 -> Intermediary_005 -> Campaign_016 | 61.70 |
| CAND_0015 | Funder_001 -> Intermediary_001 -> Campaign_008 | 61.70 |
| CAND_0106 | Funder_L011 -> Intermediary_L011 -> Proxy_L011 -> Campaign_L011 | 61.30 |
| CAND_0108 | Funder_L013 -> Intermediary_L013 -> Proxy_L013 -> Campaign_L013 | 61.30 |
| CAND_0057 | Funder_007 -> Intermediary_007 -> Proxy_010 -> Campaign_010 | 61.30 |
| CAND_0096 | Funder_L001 -> Intermediary_L001 -> Proxy_L001 -> Campaign_L001 | 61.30 |
| CAND_0098 | Funder_L003 -> Intermediary_L003 -> Proxy_L003 -> Campaign_L003 | 61.30 |
| CAND_0104 | Funder_L009 -> Intermediary_L009 -> Proxy_L009 -> Campaign_L009 | 61.30 |
| CAND_0100 | Funder_L005 -> Intermediary_L005 -> Proxy_L005 -> Campaign_L005 | 61.30 |
| CAND_0102 | Funder_L007 -> Intermediary_L007 -> Proxy_L007 -> Campaign_L007 | 61.30 |
| CAND_0019 | Funder_002 -> Intermediary_002 -> Proxy_004 -> Campaign_004 | 61.30 |
| CAND_0050 | Funder_006 -> Intermediary_006 -> Proxy_009 -> Report_009 | 61.30 |
| CAND_0032 | Funder_003 -> Intermediary_003 -> Proxy_005 -> Report_005 | 61.30 |
| CAND_0110 | Funder_L015 -> Intermediary_L015 -> Proxy_L015 -> Campaign_L015 | 61.30 |
| CAND_0018 | Funder_002 -> Intermediary_002 -> Campaign_018 | 61.20 |
| CAND_0008 | Funder_000 -> Intermediary_000 -> Campaign_014 | 61.20 |
| CAND_0060 | Funder_007 -> Intermediary_007 -> Campaign_EC04 | 61.20 |
| CAND_0049 | Funder_006 -> Intermediary_006 -> Campaign_EC02 | 61.20 |
| CAND_0025 | Funder_003 -> Intermediary_003 -> Campaign_020 | 61.20 |
| CAND_0039 | Funder_004 -> Intermediary_004 -> Campaign_022 | 61.20 |
| CAND_0054 | Funder_006 -> Intermediary_006 -> Campaign_022 | 60.70 |
| CAND_0043 | Funder_005 -> Intermediary_005 -> Campaign_020 | 60.70 |
| CAND_0022 | Funder_002 -> Intermediary_002 -> Campaign_014 | 60.70 |
| CAND_0003 | Funder_000 -> Intermediary_000 -> Campaign_010 | 60.70 |
| CAND_0034 | Funder_004 -> Intermediary_004 -> Campaign_018 | 60.70 |
| CAND_0009 | Funder_001 -> Intermediary_001 -> Campaign_012 | 60.70 |

These are passed to a human reviewer as possible leads only. 31 contain a weak (grade <= 2) hop that inspection may set aside; 10 consist entirely of documentary-grade (>= 3) hops and are not separable from true pathways on grades alone, so they require full manual verification.

## 6. Negative-control results (isolated and embedded)

| Control ID | Type | Nodes | Score | Outcome | Explanation |
| --- | --- | --- | --- | --- | --- |
| NC_000 | isolated | IndependentControl_000; Event_Ind_000 | 19.10 | NOT flagged | score 19.10 is below the threshold of 60.0; this isolated control (disconnected from the seeded structure) is correctly not flagged |
| NC_001 | isolated | IndependentControl_001; Report_Ind_001 | 7.60 | NOT flagged | score 7.60 is below the threshold of 60.0; this isolated control (disconnected from the seeded structure) is correctly not flagged |
| NC_002 | isolated | IndependentControl_002; SocialAccount_Ind_002; MediaOutlet_Ind_002 | 12.95 | NOT flagged | score 12.95 is below the threshold of 60.0; this isolated control (disconnected from the seeded structure) is correctly not flagged |
| NC_003 | isolated | IndependentControl_003; Event_Ind_003 | 19.10 | NOT flagged | score 19.10 is below the threshold of 60.0; this isolated control (disconnected from the seeded structure) is correctly not flagged |
| NC_004 | isolated | IndependentControl_004; Report_Ind_004 | 7.60 | NOT flagged | score 7.60 is below the threshold of 60.0; this isolated control (disconnected from the seeded structure) is correctly not flagged |
| NC_005 | isolated | IndependentControl_005; SocialAccount_Ind_005; MediaOutlet_Ind_005 | 12.95 | NOT flagged | score 12.95 is below the threshold of 60.0; this isolated control (disconnected from the seeded structure) is correctly not flagged |
| NC_006 | isolated | IndependentControl_006; Event_Ind_006 | 19.10 | NOT flagged | score 19.10 is below the threshold of 60.0; this isolated control (disconnected from the seeded structure) is correctly not flagged |
| NC_007 | isolated | IndependentControl_007; Report_Ind_007 | 7.60 | NOT flagged | score 7.60 is below the threshold of 60.0; this isolated control (disconnected from the seeded structure) is correctly not flagged |
| NC_008 | isolated | IndependentControl_008; SocialAccount_Ind_008; MediaOutlet_Ind_008 | 12.95 | NOT flagged | score 12.95 is below the threshold of 60.0; this isolated control (disconnected from the seeded structure) is correctly not flagged |
| NC_009 | isolated | IndependentControl_009; Event_Ind_009 | 19.10 | NOT flagged | score 19.10 is below the threshold of 60.0; this isolated control (disconnected from the seeded structure) is correctly not flagged |
| NC_010 | isolated | IndependentControl_010; Report_Ind_010 | 7.60 | NOT flagged | score 7.60 is below the threshold of 60.0; this isolated control (disconnected from the seeded structure) is correctly not flagged |
| NC_011 | isolated | IndependentControl_011; SocialAccount_Ind_011; MediaOutlet_Ind_011 | 12.95 | NOT flagged | score 12.95 is below the threshold of 60.0; this isolated control (disconnected from the seeded structure) is correctly not flagged |
| NC_012 | isolated | IndependentControl_012; Event_Ind_012 | 19.10 | NOT flagged | score 19.10 is below the threshold of 60.0; this isolated control (disconnected from the seeded structure) is correctly not flagged |
| NC_013 | isolated | IndependentControl_013; Report_Ind_013 | 7.60 | NOT flagged | score 7.60 is below the threshold of 60.0; this isolated control (disconnected from the seeded structure) is correctly not flagged |
| NC_014 | isolated | IndependentControl_014; SocialAccount_Ind_014; MediaOutlet_Ind_014 | 12.95 | NOT flagged | score 12.95 is below the threshold of 60.0; this isolated control (disconnected from the seeded structure) is correctly not flagged |
| NC_015 | isolated | IndependentControl_015; Event_Ind_015 | 19.10 | NOT flagged | score 19.10 is below the threshold of 60.0; this isolated control (disconnected from the seeded structure) is correctly not flagged |
| NC_016 | isolated | IndependentControl_016; Report_Ind_016 | 7.60 | NOT flagged | score 7.60 is below the threshold of 60.0; this isolated control (disconnected from the seeded structure) is correctly not flagged |
| NC_017 | isolated | IndependentControl_017; SocialAccount_Ind_017; MediaOutlet_Ind_017 | 12.95 | NOT flagged | score 12.95 is below the threshold of 60.0; this isolated control (disconnected from the seeded structure) is correctly not flagged |
| NC_018 | isolated | IndependentControl_018; Event_Ind_018 | 19.10 | NOT flagged | score 19.10 is below the threshold of 60.0; this isolated control (disconnected from the seeded structure) is correctly not flagged |
| NC_019 | isolated | IndependentControl_019; Report_Ind_019 | 7.60 | NOT flagged | score 7.60 is below the threshold of 60.0; this isolated control (disconnected from the seeded structure) is correctly not flagged |
| NC_020 | isolated | IndependentControl_020; SocialAccount_Ind_020; MediaOutlet_Ind_020 | 12.95 | NOT flagged | score 12.95 is below the threshold of 60.0; this isolated control (disconnected from the seeded structure) is correctly not flagged |
| NC_021 | isolated | IndependentControl_021; Event_Ind_021 | 19.10 | NOT flagged | score 19.10 is below the threshold of 60.0; this isolated control (disconnected from the seeded structure) is correctly not flagged |
| NC_022 | isolated | IndependentControl_022; Report_Ind_022 | 7.60 | NOT flagged | score 7.60 is below the threshold of 60.0; this isolated control (disconnected from the seeded structure) is correctly not flagged |
| NC_023 | isolated | IndependentControl_023; SocialAccount_Ind_023; MediaOutlet_Ind_023 | 12.95 | NOT flagged | score 12.95 is below the threshold of 60.0; this isolated control (disconnected from the seeded structure) is correctly not flagged |
| EC_01 | embedded | EmbeddedControl_01; Report_EC01 | 19.10 | NOT flagged | score 19.10 is below the threshold of 60.0; this embedded control (weakly attached to the active graph, reachable from a funder) is correctly not flagged |
| EC_02 | embedded | EmbeddedControl_02; Campaign_EC02 | 30.60 | NOT flagged | score 30.60 is below the threshold of 60.0; this embedded control (weakly attached to the active graph, reachable from a funder) is correctly not flagged |
| EC_03 | embedded | EmbeddedControl_03; Report_EC03 | 19.10 | NOT flagged | score 19.10 is below the threshold of 60.0; this embedded control (weakly attached to the active graph, reachable from a funder) is correctly not flagged |
| EC_04 | embedded | EmbeddedControl_04; Campaign_EC04 | 30.60 | NOT flagged | score 30.60 is below the threshold of 60.0; this embedded control (weakly attached to the active graph, reachable from a funder) is correctly not flagged |
| EC_05 | embedded | EmbeddedControl_05; Report_EC05 | 19.10 | NOT flagged | score 19.10 is below the threshold of 60.0; this embedded control (weakly attached to the active graph, reachable from a funder) is correctly not flagged |
| EC_06 | embedded | EmbeddedControl_06; Campaign_EC06 | 30.60 | NOT flagged | score 30.60 is below the threshold of 60.0; this embedded control (weakly attached to the active graph, reachable from a funder) is correctly not flagged |
| EC_07 | embedded | EmbeddedControl_07; Report_EC07 | 19.10 | NOT flagged | score 19.10 is below the threshold of 60.0; this embedded control (weakly attached to the active graph, reachable from a funder) is correctly not flagged |
| EC_08 | embedded | EmbeddedControl_08; Campaign_EC08 | 30.60 | NOT flagged | score 30.60 is below the threshold of 60.0; this embedded control (weakly attached to the active graph, reachable from a funder) is correctly not flagged |
| EC_09 | embedded | EmbeddedControl_09; Report_EC09 | 19.10 | NOT flagged | score 19.10 is below the threshold of 60.0; this embedded control (weakly attached to the active graph, reachable from a funder) is correctly not flagged |
| EC_10 | embedded | EmbeddedControl_10; Campaign_EC10 | 30.60 | NOT flagged | score 30.60 is below the threshold of 60.0; this embedded control (weakly attached to the active graph, reachable from a funder) is correctly not flagged |
| EC_11 | embedded | EmbeddedControl_11; Report_EC11 | 19.10 | NOT flagged | score 19.10 is below the threshold of 60.0; this embedded control (weakly attached to the active graph, reachable from a funder) is correctly not flagged |
| EC_12 | embedded | EmbeddedControl_12; Campaign_EC12 | 30.60 | NOT flagged | score 30.60 is below the threshold of 60.0; this embedded control (weakly attached to the active graph, reachable from a funder) is correctly not flagged |

Isolated-control specificity **1.0**; highest control score **30.6**. Embedded-control specificity **1.0** over 12 funder-reachable candidate paths through embedded controls (max candidate score **51.3**).

## 7. Entity-resolution decisions (three-zone rule)

Decisions: auto_merge (similarity >= 0.6), refer_to_human (0.4-0.6), keep_separate (< 0.4). The automated rule never merges in the ambiguous band; referred pairs go to the human review queue.

| Surface A | Surface B | Pair type | Sim. | Zone | Outcome |
| --- | --- | --- | --- | --- | --- |
| Health_Alliance_Alpha | Health_Alliance_Beta | false_friend | 0.50 | refer_to_human | referred_distinct_pair |
| Public_Choice_Branch | Public_Choice_Branches | false_friend | 0.50 | refer_to_human | referred_distinct_pair |
| Public_Choice_Branch | National_Choice_Branch | false_friend | 0.50 | refer_to_human | referred_distinct_pair |
| Public_Choice_Branches | National_Choice_Branches | false_friend | 0.50 | refer_to_human | referred_distinct_pair |
| Civic_Forum_Alpha | Civic_Forum_Beta | false_friend | 0.50 | refer_to_human | referred_distinct_pair |
| Civic_Forum_Alpha | Open_Forum_Alpha | false_friend | 0.50 | refer_to_human | referred_distinct_pair |
| Civic_Forum_Beta | Open_Forum_Beta | false_friend | 0.50 | refer_to_human | referred_distinct_pair |
| Policy_Council_Branch | Policy_Council_Branches | false_friend | 0.50 | refer_to_human | referred_distinct_pair |
| Policy_Council_Branch | Future_Council_Branch | false_friend | 0.50 | refer_to_human | referred_distinct_pair |
| Policy_Council_Branches | Future_Council_Branches | false_friend | 0.50 | refer_to_human | referred_distinct_pair |
| Wellness_League_Alpha | Wellness_League_Beta | false_friend | 0.50 | refer_to_human | referred_distinct_pair |
| Reform_Circle_Branch | Reform_Circle_Branches | false_friend | 0.50 | refer_to_human | referred_distinct_pair |
| Liberty_Board_Alpha | Liberty_Board_Beta | false_friend | 0.50 | refer_to_human | referred_distinct_pair |
| Standards_Coalition_Branch | Standards_Coalition_Branches | false_friend | 0.50 | refer_to_human | referred_distinct_pair |
| Data_Institute_Alpha | Data_Institute_Beta | false_friend | 0.50 | refer_to_human | referred_distinct_pair |
| Citizen_Trust_Branch | Citizen_Trust_Branches | false_friend | 0.50 | refer_to_human | referred_distinct_pair |
| Research_Society_Alpha | Research_Society_Beta | false_friend | 0.50 | refer_to_human | referred_distinct_pair |
| Market_Union_Branch | Market_Union_Branches | false_friend | 0.50 | refer_to_human | referred_distinct_pair |
| Consumer_Partnership_Alpha | Consumer_Partnership_Beta | false_friend | 0.50 | refer_to_human | referred_distinct_pair |
| Global_Assembly_Branch | Global_Assembly_Branches | false_friend | 0.50 | refer_to_human | referred_distinct_pair |
| Regional_Foundation_Alpha | Regional_Foundation_Beta | false_friend | 0.50 | refer_to_human | referred_distinct_pair |
| National_Choice_Branch | National_Choice_Branches | false_friend | 0.50 | refer_to_human | referred_distinct_pair |
| Open_Forum_Alpha | Open_Forum_Beta | false_friend | 0.50 | refer_to_human | referred_distinct_pair |
| Future_Council_Branch | Future_Council_Branches | false_friend | 0.50 | refer_to_human | referred_distinct_pair |
| Common_League_Gamma | Common_League_Gamma_Group | true_alias | 0.75 | auto_merge | correct_auto_merge |
| Progress_Circle_Delta | Progress_Circle_Delta_Group | true_alias | 0.75 | auto_merge | correct_auto_merge |
| Heritage_Board_Sigma | Heritage_Board_Sigma_Group | true_alias | 0.75 | auto_merge | correct_auto_merge |
| Unity_Coalition_Omega | Unity_Coalition_Omega_Group | true_alias | 0.75 | auto_merge | correct_auto_merge |
| Frontier_Institute_Theta | Frontier_Institute_Theta_Group | true_alias | 0.75 | auto_merge | correct_auto_merge |
| Summit_Trust_Lambda | Summit_Trust_Lambda_Group | true_alias | 0.75 | auto_merge | correct_auto_merge |
| Pioneer_Society_Kappa | Pioneer_Society_Kappa_Group | true_alias | 0.75 | auto_merge | correct_auto_merge |
| Anchor_Union_Zeta | Anchor_Union_Zeta_Group | true_alias | 0.75 | auto_merge | correct_auto_merge |
| Beacon_Partnership_Eta | Beacon_Partnership_Eta_Group | true_alias | 0.75 | auto_merge | correct_auto_merge |
| Cardinal_Assembly_Iota | Cardinal_Assembly_Iota_Group | true_alias | 0.75 | auto_merge | correct_auto_merge |
| Meridian_Foundation_Mu | Meridian_Foundation_Mu_Group | true_alias | 0.75 | auto_merge | correct_auto_merge |
| Vanguard_Alliance_Nu | Vanguard_Alliance_Nu_Group | true_alias | 0.75 | auto_merge | correct_auto_merge |
| Common_League_Gamma | Gamma_Common_Network | true_alias | 0.50 | refer_to_human | referred_true_alias |
| Pioneer_Society_Kappa | Kappa_Pioneer_Network | true_alias | 0.50 | refer_to_human | referred_true_alias |
| Common_League_Gamma_Group | Gamma_Common_Network | true_alias | 0.40 | refer_to_human | referred_true_alias |
| Pioneer_Society_Kappa_Group | Kappa_Pioneer_Network | true_alias | 0.40 | refer_to_human | referred_true_alias |

Auto-merge precision **1.0**; auto-merge recall **0.75**; potential recall if all referred true-alias pairs are correctly confirmed **1.0** (assumption, not observed human performance). False merges: **0**. Referral queue: 28 pairs (4 true aliases, 24 distinct pairs).

## 7b. Robustness checks (weak-signal chains, gate ablation, sensitivity)

| Robustness check | Value |
| --- | --- |
| Seeded weak-signal chains | 10 |
| Weak-chain candidate paths | 10 |
| Weak-chain candidates entering high-priority review | 0 |
| Weak-chain candidates flagged (gate REMOVED) | 0 |
| Max weak-chain score (gated) | 38.3 |
| Max weak-chain score (gate removed) | 42.8 |
| Max attainable weak-signal-only score (exact controlled-vocabulary enumeration, gate removed) | 44.8 |

Weight-perturbation stability (200 draws, +/-20%): Spearman rho min/median **0.9818 / 0.9956**; Kendall tau-b min/median **0.927 / 0.978**; top-k Jaccard min **1.0**; threshold-based recall median **1.0**. Ties use average ranks for Spearman and tau-b correction for Kendall. See sensitivity_analysis.csv and threshold_sweep.csv.

## 7c. Connected active-network noise challenge

56 connected active-noise edges increased candidate-path enumeration from **64** to **120**. The scenario contained **56** candidate paths using active noise and **33** high-priority active-noise false positives. These false positives are retained as an adverse result; candidate enumeration did not reach the cap of 20000.

## 8. Path-by-path audit trail

Each candidate path is shown with its edge provenance, evidence snippets, triage decision and a recommended human-review action. Scores are triage indicators only.

### GT_PATH_003 (true_positive)

- **Node sequence:** Funder_003 -> Intermediary_003 -> Event_003 -> Report_003

- **Edge sequence:** funds -> hosts -> publishes

- **Evidence grades:** 4 -> 3 -> 3

- **Edge provenance:** ground-truth -> ground-truth -> ground-truth

- **Evidence snippets:** Synthetic record: Funder_003 is listed as providing funding to Intermediary_003 during Phase_01. || Synthetic record: Intermediary_003 is listed as a host of Event_003 during Phase_01. || Synthetic record: Event_003 is listed as the publisher of Report_003 during Phase_02.

- **Review-priority score:** 67.8 (threshold 60.0) -> FLAGGED

- **Ground-truth label:** seeded proxy path

- **Why:** HIGH-PRIORITY REVIEW (raw score 67.80 >= threshold 60.0 and eligible): includes a direct synthetic funding edge (grade 4); weakest hop grade 3, mean grade 3.33; documentary continuity maintained across all hops.

- **Recommended action:** Prioritise for expert review: inspect the underlying synthetic records and confirm each link independently before drawing any inference.

### GT_PATH_004 (true_positive)

- **Node sequence:** Funder_004 -> Intermediary_004 -> Proxy_004 -> Campaign_004

- **Edge sequence:** funds -> partners_with -> hosts

- **Evidence grades:** 4 -> 3 -> 3

- **Edge provenance:** ground-truth -> ground-truth -> ground-truth

- **Evidence snippets:** Synthetic record: Funder_004 is listed as providing funding to Intermediary_004 during Phase_01. || Synthetic record: Intermediary_004 is described as a partner of Proxy_004 during Phase_01. || Synthetic record: Proxy_004 is listed as a host of Campaign_004 during Phase_02.

- **Review-priority score:** 67.8 (threshold 60.0) -> FLAGGED

- **Ground-truth label:** seeded proxy path

- **Why:** HIGH-PRIORITY REVIEW (raw score 67.80 >= threshold 60.0 and eligible): includes a direct synthetic funding edge (grade 4); weakest hop grade 3, mean grade 3.33; documentary continuity maintained across all hops.

- **Recommended action:** Prioritise for expert review: inspect the underlying synthetic records and confirm each link independently before drawing any inference.

### GT_PATH_019 (true_positive)

- **Node sequence:** Funder_019 -> Intermediary_019 -> Event_019 -> Report_019

- **Edge sequence:** funds -> hosts -> publishes

- **Evidence grades:** 4 -> 3 -> 3

- **Edge provenance:** ground-truth -> ground-truth -> ground-truth

- **Evidence snippets:** Synthetic record: Funder_019 is listed as providing funding to Intermediary_019 during Phase_01. || Synthetic record: Intermediary_019 is listed as a host of Event_019 during Phase_01. || Synthetic record: Event_019 is listed as the publisher of Report_019 during Phase_02.

- **Review-priority score:** 67.8 (threshold 60.0) -> FLAGGED

- **Ground-truth label:** seeded proxy path

- **Why:** HIGH-PRIORITY REVIEW (raw score 67.80 >= threshold 60.0 and eligible): includes a direct synthetic funding edge (grade 4); weakest hop grade 3, mean grade 3.33; documentary continuity maintained across all hops.

- **Recommended action:** Prioritise for expert review: inspect the underlying synthetic records and confirm each link independently before drawing any inference.

### GT_PATH_007 (true_positive)

- **Node sequence:** Funder_007 -> Intermediary_007 -> Event_007 -> Report_007

- **Edge sequence:** funds -> hosts -> publishes

- **Evidence grades:** 4 -> 3 -> 3

- **Edge provenance:** ground-truth -> ground-truth -> ground-truth

- **Evidence snippets:** Synthetic record: Funder_007 is listed as providing funding to Intermediary_007 during Phase_01. || Synthetic record: Intermediary_007 is listed as a host of Event_007 during Phase_01. || Synthetic record: Event_007 is listed as the publisher of Report_007 during Phase_02.

- **Review-priority score:** 67.8 (threshold 60.0) -> FLAGGED

- **Ground-truth label:** seeded proxy path

- **Why:** HIGH-PRIORITY REVIEW (raw score 67.80 >= threshold 60.0 and eligible): includes a direct synthetic funding edge (grade 4); weakest hop grade 3, mean grade 3.33; documentary continuity maintained across all hops.

- **Recommended action:** Prioritise for expert review: inspect the underlying synthetic records and confirm each link independently before drawing any inference.

### GT_PATH_000 (true_positive)

- **Node sequence:** Funder_000 -> Intermediary_000 -> Proxy_000 -> Campaign_000

- **Edge sequence:** funds -> partners_with -> hosts

- **Evidence grades:** 4 -> 3 -> 3

- **Edge provenance:** ground-truth -> ground-truth -> ground-truth

- **Evidence snippets:** Synthetic record: Funder_000 is listed as providing funding to Intermediary_000 during Phase_01. || Synthetic record: Intermediary_000 is described as a partner of Proxy_000 during Phase_01. || Synthetic record: Proxy_000 is listed as a host of Campaign_000 during Phase_02.

- **Review-priority score:** 67.8 (threshold 60.0) -> FLAGGED

- **Ground-truth label:** seeded proxy path

- **Why:** HIGH-PRIORITY REVIEW (raw score 67.80 >= threshold 60.0 and eligible): includes a direct synthetic funding edge (grade 4); weakest hop grade 3, mean grade 3.33; documentary continuity maintained across all hops.

- **Recommended action:** Prioritise for expert review: inspect the underlying synthetic records and confirm each link independently before drawing any inference.

### GT_PATH_016 (true_positive)

- **Node sequence:** Funder_016 -> Intermediary_016 -> Proxy_016 -> Campaign_016

- **Edge sequence:** funds -> partners_with -> hosts

- **Evidence grades:** 4 -> 3 -> 3

- **Edge provenance:** ground-truth -> ground-truth -> ground-truth

- **Evidence snippets:** Synthetic record: Funder_016 is listed as providing funding to Intermediary_016 during Phase_01. || Synthetic record: Intermediary_016 is described as a partner of Proxy_016 during Phase_01. || Synthetic record: Proxy_016 is listed as a host of Campaign_016 during Phase_02.

- **Review-priority score:** 67.8 (threshold 60.0) -> FLAGGED

- **Ground-truth label:** seeded proxy path

- **Why:** HIGH-PRIORITY REVIEW (raw score 67.80 >= threshold 60.0 and eligible): includes a direct synthetic funding edge (grade 4); weakest hop grade 3, mean grade 3.33; documentary continuity maintained across all hops.

- **Recommended action:** Prioritise for expert review: inspect the underlying synthetic records and confirm each link independently before drawing any inference.

### GT_PATH_011 (true_positive)

- **Node sequence:** Funder_011 -> Intermediary_011 -> Event_011 -> Report_011

- **Edge sequence:** funds -> hosts -> publishes

- **Evidence grades:** 4 -> 3 -> 3

- **Edge provenance:** ground-truth -> ground-truth -> ground-truth

- **Evidence snippets:** Synthetic record: Funder_011 is listed as providing funding to Intermediary_011 during Phase_01. || Synthetic record: Intermediary_011 is listed as a host of Event_011 during Phase_01. || Synthetic record: Event_011 is listed as the publisher of Report_011 during Phase_02.

- **Review-priority score:** 67.8 (threshold 60.0) -> FLAGGED

- **Ground-truth label:** seeded proxy path

- **Why:** HIGH-PRIORITY REVIEW (raw score 67.80 >= threshold 60.0 and eligible): includes a direct synthetic funding edge (grade 4); weakest hop grade 3, mean grade 3.33; documentary continuity maintained across all hops.

- **Recommended action:** Prioritise for expert review: inspect the underlying synthetic records and confirm each link independently before drawing any inference.

### GT_PATH_015 (true_positive)

- **Node sequence:** Funder_015 -> Intermediary_015 -> Event_015 -> Report_015

- **Edge sequence:** funds -> hosts -> publishes

- **Evidence grades:** 4 -> 3 -> 3

- **Edge provenance:** ground-truth -> ground-truth -> ground-truth

- **Evidence snippets:** Synthetic record: Funder_015 is listed as providing funding to Intermediary_015 during Phase_01. || Synthetic record: Intermediary_015 is listed as a host of Event_015 during Phase_01. || Synthetic record: Event_015 is listed as the publisher of Report_015 during Phase_02.

- **Review-priority score:** 67.8 (threshold 60.0) -> FLAGGED

- **Ground-truth label:** seeded proxy path

- **Why:** HIGH-PRIORITY REVIEW (raw score 67.80 >= threshold 60.0 and eligible): includes a direct synthetic funding edge (grade 4); weakest hop grade 3, mean grade 3.33; documentary continuity maintained across all hops.

- **Recommended action:** Prioritise for expert review: inspect the underlying synthetic records and confirm each link independently before drawing any inference.

### GT_PATH_012 (true_positive)

- **Node sequence:** Funder_012 -> Intermediary_012 -> Proxy_012 -> Campaign_012

- **Edge sequence:** funds -> partners_with -> hosts

- **Evidence grades:** 4 -> 3 -> 3

- **Edge provenance:** ground-truth -> ground-truth -> ground-truth

- **Evidence snippets:** Synthetic record: Funder_012 is listed as providing funding to Intermediary_012 during Phase_01. || Synthetic record: Intermediary_012 is described as a partner of Proxy_012 during Phase_01. || Synthetic record: Proxy_012 is listed as a host of Campaign_012 during Phase_02.

- **Review-priority score:** 67.8 (threshold 60.0) -> FLAGGED

- **Ground-truth label:** seeded proxy path

- **Why:** HIGH-PRIORITY REVIEW (raw score 67.80 >= threshold 60.0 and eligible): includes a direct synthetic funding edge (grade 4); weakest hop grade 3, mean grade 3.33; documentary continuity maintained across all hops.

- **Recommended action:** Prioritise for expert review: inspect the underlying synthetic records and confirm each link independently before drawing any inference.

### GT_PATH_008 (true_positive)

- **Node sequence:** Funder_008 -> Intermediary_008 -> Proxy_008 -> Campaign_008

- **Edge sequence:** funds -> partners_with -> hosts

- **Evidence grades:** 4 -> 3 -> 3

- **Edge provenance:** ground-truth -> ground-truth -> ground-truth

- **Evidence snippets:** Synthetic record: Funder_008 is listed as providing funding to Intermediary_008 during Phase_01. || Synthetic record: Intermediary_008 is described as a partner of Proxy_008 during Phase_01. || Synthetic record: Proxy_008 is listed as a host of Campaign_008 during Phase_02.

- **Review-priority score:** 67.8 (threshold 60.0) -> FLAGGED

- **Ground-truth label:** seeded proxy path

- **Why:** HIGH-PRIORITY REVIEW (raw score 67.80 >= threshold 60.0 and eligible): includes a direct synthetic funding edge (grade 4); weakest hop grade 3, mean grade 3.33; documentary continuity maintained across all hops.

- **Recommended action:** Prioritise for expert review: inspect the underlying synthetic records and confirm each link independently before drawing any inference.

### GT_PATH_020 (true_positive)

- **Node sequence:** Funder_020 -> Intermediary_020 -> Proxy_020 -> Campaign_020

- **Edge sequence:** funds -> partners_with -> hosts

- **Evidence grades:** 4 -> 3 -> 3

- **Edge provenance:** ground-truth -> ground-truth -> ground-truth

- **Evidence snippets:** Synthetic record: Funder_020 is listed as providing funding to Intermediary_020 during Phase_01. || Synthetic record: Intermediary_020 is described as a partner of Proxy_020 during Phase_01. || Synthetic record: Proxy_020 is listed as a host of Campaign_020 during Phase_02.

- **Review-priority score:** 67.8 (threshold 60.0) -> FLAGGED

- **Ground-truth label:** seeded proxy path

- **Why:** HIGH-PRIORITY REVIEW (raw score 67.80 >= threshold 60.0 and eligible): includes a direct synthetic funding edge (grade 4); weakest hop grade 3, mean grade 3.33; documentary continuity maintained across all hops.

- **Recommended action:** Prioritise for expert review: inspect the underlying synthetic records and confirm each link independently before drawing any inference.

### GT_PATH_024 (true_positive)

- **Node sequence:** Funder_024 -> Intermediary_024 -> Proxy_024 -> Campaign_024

- **Edge sequence:** funds -> partners_with -> hosts

- **Evidence grades:** 4 -> 3 -> 3

- **Edge provenance:** ground-truth -> ground-truth -> ground-truth

- **Evidence snippets:** Synthetic record: Funder_024 is listed as providing funding to Intermediary_024 during Phase_01. || Synthetic record: Intermediary_024 is described as a partner of Proxy_024 during Phase_01. || Synthetic record: Proxy_024 is listed as a host of Campaign_024 during Phase_02.

- **Review-priority score:** 67.8 (threshold 60.0) -> FLAGGED

- **Ground-truth label:** seeded proxy path

- **Why:** HIGH-PRIORITY REVIEW (raw score 67.80 >= threshold 60.0 and eligible): includes a direct synthetic funding edge (grade 4); weakest hop grade 3, mean grade 3.33; documentary continuity maintained across all hops.

- **Recommended action:** Prioritise for expert review: inspect the underlying synthetic records and confirm each link independently before drawing any inference.

### GT_PATH_023 (true_positive)

- **Node sequence:** Funder_023 -> Intermediary_023 -> Event_023 -> Report_023

- **Edge sequence:** funds -> hosts -> publishes

- **Evidence grades:** 4 -> 3 -> 3

- **Edge provenance:** ground-truth -> ground-truth -> ground-truth

- **Evidence snippets:** Synthetic record: Funder_023 is listed as providing funding to Intermediary_023 during Phase_01. || Synthetic record: Intermediary_023 is listed as a host of Event_023 during Phase_01. || Synthetic record: Event_023 is listed as the publisher of Report_023 during Phase_02.

- **Review-priority score:** 67.8 (threshold 60.0) -> FLAGGED

- **Ground-truth label:** seeded proxy path

- **Why:** HIGH-PRIORITY REVIEW (raw score 67.80 >= threshold 60.0 and eligible): includes a direct synthetic funding edge (grade 4); weakest hop grade 3, mean grade 3.33; documentary continuity maintained across all hops.

- **Recommended action:** Prioritise for expert review: inspect the underlying synthetic records and confirm each link independently before drawing any inference.

### GT_PATH_001 (true_positive)

- **Node sequence:** Funder_001 -> Intermediary_001 -> Event_001 -> Proxy_001 -> Report_001

- **Edge sequence:** funds -> hosts -> speaks_at -> publishes

- **Evidence grades:** 4 -> 3 -> 3 -> 3

- **Edge provenance:** ground-truth -> ground-truth -> ground-truth -> ground-truth

- **Evidence snippets:** Synthetic record: Funder_001 is listed as providing funding to Intermediary_001 during Phase_01. || Synthetic record: Intermediary_001 is listed as a host of Event_001 during Phase_01. || Synthetic record: a representative of Event_001 is listed as speaking at Proxy_001 during Phase_02. || Synthetic record: Proxy_001 is listed as the publisher of Report_001 during Phase_02.

- **Review-priority score:** 65.78 (threshold 60.0) -> FLAGGED

- **Ground-truth label:** seeded proxy path

- **Why:** HIGH-PRIORITY REVIEW (raw score 65.78 >= threshold 60.0 and eligible): includes a direct synthetic funding edge (grade 4); weakest hop grade 3, mean grade 3.25; documentary continuity maintained across all hops.

- **Recommended action:** Prioritise for expert review: inspect the underlying synthetic records and confirm each link independently before drawing any inference.

### GT_PATH_013 (true_positive)

- **Node sequence:** Funder_013 -> Intermediary_013 -> Event_013 -> Proxy_013 -> Report_013

- **Edge sequence:** funds -> hosts -> speaks_at -> publishes

- **Evidence grades:** 4 -> 3 -> 3 -> 3

- **Edge provenance:** ground-truth -> ground-truth -> ground-truth -> ground-truth

- **Evidence snippets:** Synthetic record: Funder_013 is listed as providing funding to Intermediary_013 during Phase_01. || Synthetic record: Intermediary_013 is listed as a host of Event_013 during Phase_01. || Synthetic record: a representative of Event_013 is listed as speaking at Proxy_013 during Phase_02. || Synthetic record: Proxy_013 is listed as the publisher of Report_013 during Phase_02.

- **Review-priority score:** 65.78 (threshold 60.0) -> FLAGGED

- **Ground-truth label:** seeded proxy path

- **Why:** HIGH-PRIORITY REVIEW (raw score 65.78 >= threshold 60.0 and eligible): includes a direct synthetic funding edge (grade 4); weakest hop grade 3, mean grade 3.25; documentary continuity maintained across all hops.

- **Recommended action:** Prioritise for expert review: inspect the underlying synthetic records and confirm each link independently before drawing any inference.

### GT_PATH_017 (true_positive)

- **Node sequence:** Funder_017 -> Intermediary_017 -> Event_017 -> Proxy_017 -> Report_017

- **Edge sequence:** funds -> hosts -> speaks_at -> publishes

- **Evidence grades:** 4 -> 3 -> 3 -> 3

- **Edge provenance:** ground-truth -> ground-truth -> ground-truth -> ground-truth

- **Evidence snippets:** Synthetic record: Funder_017 is listed as providing funding to Intermediary_017 during Phase_01. || Synthetic record: Intermediary_017 is listed as a host of Event_017 during Phase_01. || Synthetic record: a representative of Event_017 is listed as speaking at Proxy_017 during Phase_02. || Synthetic record: Proxy_017 is listed as the publisher of Report_017 during Phase_02.

- **Review-priority score:** 65.78 (threshold 60.0) -> FLAGGED

- **Ground-truth label:** seeded proxy path

- **Why:** HIGH-PRIORITY REVIEW (raw score 65.78 >= threshold 60.0 and eligible): includes a direct synthetic funding edge (grade 4); weakest hop grade 3, mean grade 3.25; documentary continuity maintained across all hops.

- **Recommended action:** Prioritise for expert review: inspect the underlying synthetic records and confirm each link independently before drawing any inference.

### GT_PATH_009 (true_positive)

- **Node sequence:** Funder_009 -> Intermediary_009 -> Event_009 -> Proxy_009 -> Report_009

- **Edge sequence:** funds -> hosts -> speaks_at -> publishes

- **Evidence grades:** 4 -> 3 -> 3 -> 3

- **Edge provenance:** ground-truth -> ground-truth -> ground-truth -> ground-truth

- **Evidence snippets:** Synthetic record: Funder_009 is listed as providing funding to Intermediary_009 during Phase_01. || Synthetic record: Intermediary_009 is listed as a host of Event_009 during Phase_01. || Synthetic record: a representative of Event_009 is listed as speaking at Proxy_009 during Phase_02. || Synthetic record: Proxy_009 is listed as the publisher of Report_009 during Phase_02.

- **Review-priority score:** 65.78 (threshold 60.0) -> FLAGGED

- **Ground-truth label:** seeded proxy path

- **Why:** HIGH-PRIORITY REVIEW (raw score 65.78 >= threshold 60.0 and eligible): includes a direct synthetic funding edge (grade 4); weakest hop grade 3, mean grade 3.25; documentary continuity maintained across all hops.

- **Recommended action:** Prioritise for expert review: inspect the underlying synthetic records and confirm each link independently before drawing any inference.

### GT_PATH_005 (true_positive)

- **Node sequence:** Funder_005 -> Intermediary_005 -> Event_005 -> Proxy_005 -> Report_005

- **Edge sequence:** funds -> hosts -> speaks_at -> publishes

- **Evidence grades:** 4 -> 3 -> 3 -> 3

- **Edge provenance:** ground-truth -> ground-truth -> ground-truth -> ground-truth

- **Evidence snippets:** Synthetic record: Funder_005 is listed as providing funding to Intermediary_005 during Phase_01. || Synthetic record: Intermediary_005 is listed as a host of Event_005 during Phase_01. || Synthetic record: a representative of Event_005 is listed as speaking at Proxy_005 during Phase_02. || Synthetic record: Proxy_005 is listed as the publisher of Report_005 during Phase_02.

- **Review-priority score:** 65.78 (threshold 60.0) -> FLAGGED

- **Ground-truth label:** seeded proxy path

- **Why:** HIGH-PRIORITY REVIEW (raw score 65.78 >= threshold 60.0 and eligible): includes a direct synthetic funding edge (grade 4); weakest hop grade 3, mean grade 3.25; documentary continuity maintained across all hops.

- **Recommended action:** Prioritise for expert review: inspect the underlying synthetic records and confirm each link independently before drawing any inference.

### GT_PATH_025 (true_positive)

- **Node sequence:** Funder_025 -> Intermediary_025 -> Event_025 -> Proxy_025 -> Report_025

- **Edge sequence:** funds -> hosts -> speaks_at -> publishes

- **Evidence grades:** 4 -> 3 -> 3 -> 3

- **Edge provenance:** ground-truth -> ground-truth -> ground-truth -> ground-truth

- **Evidence snippets:** Synthetic record: Funder_025 is listed as providing funding to Intermediary_025 during Phase_01. || Synthetic record: Intermediary_025 is listed as a host of Event_025 during Phase_01. || Synthetic record: a representative of Event_025 is listed as speaking at Proxy_025 during Phase_02. || Synthetic record: Proxy_025 is listed as the publisher of Report_025 during Phase_02.

- **Review-priority score:** 65.78 (threshold 60.0) -> FLAGGED

- **Ground-truth label:** seeded proxy path

- **Why:** HIGH-PRIORITY REVIEW (raw score 65.78 >= threshold 60.0 and eligible): includes a direct synthetic funding edge (grade 4); weakest hop grade 3, mean grade 3.25; documentary continuity maintained across all hops.

- **Recommended action:** Prioritise for expert review: inspect the underlying synthetic records and confirm each link independently before drawing any inference.

### GT_PATH_021 (true_positive)

- **Node sequence:** Funder_021 -> Intermediary_021 -> Event_021 -> Proxy_021 -> Report_021

- **Edge sequence:** funds -> hosts -> speaks_at -> publishes

- **Evidence grades:** 4 -> 3 -> 3 -> 3

- **Edge provenance:** ground-truth -> ground-truth -> ground-truth -> ground-truth

- **Evidence snippets:** Synthetic record: Funder_021 is listed as providing funding to Intermediary_021 during Phase_01. || Synthetic record: Intermediary_021 is listed as a host of Event_021 during Phase_01. || Synthetic record: a representative of Event_021 is listed as speaking at Proxy_021 during Phase_02. || Synthetic record: Proxy_021 is listed as the publisher of Report_021 during Phase_02.

- **Review-priority score:** 65.78 (threshold 60.0) -> FLAGGED

- **Ground-truth label:** seeded proxy path

- **Why:** HIGH-PRIORITY REVIEW (raw score 65.78 >= threshold 60.0 and eligible): includes a direct synthetic funding edge (grade 4); weakest hop grade 3, mean grade 3.25; documentary continuity maintained across all hops.

- **Recommended action:** Prioritise for expert review: inspect the underlying synthetic records and confirm each link independently before drawing any inference.

### GT_PATH_018 (true_positive)

- **Node sequence:** Funder_018 -> Intermediary_018 -> Proxy_018 -> Campaign_018

- **Edge sequence:** funds -> partners_with -> amplifies

- **Evidence grades:** 4 -> 3 -> 2

- **Edge provenance:** ground-truth -> ground-truth -> ground-truth

- **Evidence snippets:** Synthetic record: Funder_018 is listed as providing funding to Intermediary_018 during Phase_01. || Synthetic record: Intermediary_018 is described as a partner of Proxy_018 during Phase_01. || Synthetic record: Proxy_018 repeatedly amplified output attributed to Campaign_018 during Phase_02.

- **Review-priority score:** 63.8 (threshold 60.0) -> FLAGGED

- **Ground-truth label:** seeded proxy path

- **Why:** HIGH-PRIORITY REVIEW (raw score 63.80 >= threshold 60.0 and eligible): includes a direct synthetic funding edge (grade 4); weakest hop grade 2, mean grade 3.00; drops to a grade-2 shared-link/amplification hop.

- **Recommended action:** Prioritise for expert review: inspect the underlying synthetic records and confirm each link independently before drawing any inference.

### GT_PATH_022 (true_positive)

- **Node sequence:** Funder_022 -> Intermediary_022 -> Proxy_022 -> Campaign_022

- **Edge sequence:** funds -> partners_with -> amplifies

- **Evidence grades:** 4 -> 3 -> 2

- **Edge provenance:** ground-truth -> ground-truth -> ground-truth

- **Evidence snippets:** Synthetic record: Funder_022 is listed as providing funding to Intermediary_022 during Phase_01. || Synthetic record: Intermediary_022 is described as a partner of Proxy_022 during Phase_01. || Synthetic record: Proxy_022 repeatedly amplified output attributed to Campaign_022 during Phase_02.

- **Review-priority score:** 63.8 (threshold 60.0) -> FLAGGED

- **Ground-truth label:** seeded proxy path

- **Why:** HIGH-PRIORITY REVIEW (raw score 63.80 >= threshold 60.0 and eligible): includes a direct synthetic funding edge (grade 4); weakest hop grade 2, mean grade 3.00; drops to a grade-2 shared-link/amplification hop.

- **Recommended action:** Prioritise for expert review: inspect the underlying synthetic records and confirm each link independently before drawing any inference.

### GT_PATH_014 (true_positive)

- **Node sequence:** Funder_014 -> Intermediary_014 -> Proxy_014 -> Campaign_014

- **Edge sequence:** funds -> partners_with -> amplifies

- **Evidence grades:** 4 -> 3 -> 2

- **Edge provenance:** ground-truth -> ground-truth -> ground-truth

- **Evidence snippets:** Synthetic record: Funder_014 is listed as providing funding to Intermediary_014 during Phase_01. || Synthetic record: Intermediary_014 is described as a partner of Proxy_014 during Phase_01. || Synthetic record: Proxy_014 repeatedly amplified output attributed to Campaign_014 during Phase_02.

- **Review-priority score:** 63.8 (threshold 60.0) -> FLAGGED

- **Ground-truth label:** seeded proxy path

- **Why:** HIGH-PRIORITY REVIEW (raw score 63.80 >= threshold 60.0 and eligible): includes a direct synthetic funding edge (grade 4); weakest hop grade 2, mean grade 3.00; drops to a grade-2 shared-link/amplification hop.

- **Recommended action:** Prioritise for expert review: inspect the underlying synthetic records and confirm each link independently before drawing any inference.

### GT_PATH_010 (true_positive)

- **Node sequence:** Funder_010 -> Intermediary_010 -> Proxy_010 -> Campaign_010

- **Edge sequence:** funds -> partners_with -> amplifies

- **Evidence grades:** 4 -> 3 -> 2

- **Edge provenance:** ground-truth -> ground-truth -> ground-truth

- **Evidence snippets:** Synthetic record: Funder_010 is listed as providing funding to Intermediary_010 during Phase_01. || Synthetic record: Intermediary_010 is described as a partner of Proxy_010 during Phase_01. || Synthetic record: Proxy_010 repeatedly amplified output attributed to Campaign_010 during Phase_02.

- **Review-priority score:** 63.8 (threshold 60.0) -> FLAGGED

- **Ground-truth label:** seeded proxy path

- **Why:** HIGH-PRIORITY REVIEW (raw score 63.80 >= threshold 60.0 and eligible): includes a direct synthetic funding edge (grade 4); weakest hop grade 2, mean grade 3.00; drops to a grade-2 shared-link/amplification hop.

- **Recommended action:** Prioritise for expert review: inspect the underlying synthetic records and confirm each link independently before drawing any inference.

### GT_PATH_002 (true_positive)

- **Node sequence:** Funder_002 -> Intermediary_002 -> Proxy_002 -> Campaign_002

- **Edge sequence:** funds -> partners_with -> amplifies

- **Evidence grades:** 4 -> 3 -> 2

- **Edge provenance:** ground-truth -> ground-truth -> ground-truth

- **Evidence snippets:** Synthetic record: Funder_002 is listed as providing funding to Intermediary_002 during Phase_01. || Synthetic record: Intermediary_002 is described as a partner of Proxy_002 during Phase_01. || Synthetic record: Proxy_002 repeatedly amplified output attributed to Campaign_002 during Phase_02.

- **Review-priority score:** 63.8 (threshold 60.0) -> FLAGGED

- **Ground-truth label:** seeded proxy path

- **Why:** HIGH-PRIORITY REVIEW (raw score 63.80 >= threshold 60.0 and eligible): includes a direct synthetic funding edge (grade 4); weakest hop grade 2, mean grade 3.00; drops to a grade-2 shared-link/amplification hop.

- **Recommended action:** Prioritise for expert review: inspect the underlying synthetic records and confirm each link independently before drawing any inference.

### GT_PATH_006 (true_positive)

- **Node sequence:** Funder_006 -> Intermediary_006 -> Proxy_006 -> Campaign_006

- **Edge sequence:** funds -> partners_with -> amplifies

- **Evidence grades:** 4 -> 3 -> 2

- **Edge provenance:** ground-truth -> ground-truth -> ground-truth

- **Evidence snippets:** Synthetic record: Funder_006 is listed as providing funding to Intermediary_006 during Phase_01. || Synthetic record: Intermediary_006 is described as a partner of Proxy_006 during Phase_01. || Synthetic record: Proxy_006 repeatedly amplified output attributed to Campaign_006 during Phase_02.

- **Review-priority score:** 63.8 (threshold 60.0) -> FLAGGED

- **Ground-truth label:** seeded proxy path

- **Why:** HIGH-PRIORITY REVIEW (raw score 63.80 >= threshold 60.0 and eligible): includes a direct synthetic funding edge (grade 4); weakest hop grade 2, mean grade 3.00; drops to a grade-2 shared-link/amplification hop.

- **Recommended action:** Prioritise for expert review: inspect the underlying synthetic records and confirm each link independently before drawing any inference.

### CAND_0010 (false_positive)

- **Node sequence:** Funder_001 -> Intermediary_001 -> Campaign_024

- **Edge sequence:** funds -> partners_with

- **Evidence grades:** 4 -> 3

- **Edge provenance:** ground-truth -> distractor

- **Evidence snippets:** Synthetic record: Funder_001 is listed as providing funding to Intermediary_001 during Phase_01. || Synthetic record: Intermediary_001 is described as a partner of Campaign_024 during Phase_01.

- **Review-priority score:** 69.45 (threshold 60.0) -> FLAGGED

- **Ground-truth label:** not seeded

- **Why:** HIGH-PRIORITY REVIEW (raw score 69.45 >= threshold 60.0 and eligible): includes a direct synthetic funding edge (grade 4); weakest hop grade 3, mean grade 3.50; documentary continuity maintained across all hops.

- **Recommended action:** Queue for expert review; every hop carries documentary-grade evidence, so this false lead is not separable from a true pathway on grades alone and requires full manual verification of each underlying record.

### CAND_0048 (false_positive)

- **Node sequence:** Funder_005 -> Intermediary_005 -> Campaign_EC08

- **Edge sequence:** funds -> partners_with

- **Evidence grades:** 4 -> 3

- **Edge provenance:** ground-truth -> distractor

- **Evidence snippets:** Synthetic record: Funder_005 is listed as providing funding to Intermediary_005 during Phase_01. || Synthetic record: Intermediary_005 is described as a partner of Campaign_EC08 during Phase_01.

- **Review-priority score:** 69.45 (threshold 60.0) -> FLAGGED

- **Ground-truth label:** not seeded

- **Why:** HIGH-PRIORITY REVIEW (raw score 69.45 >= threshold 60.0 and eligible): includes a direct synthetic funding edge (grade 4); weakest hop grade 3, mean grade 3.50; documentary continuity maintained across all hops.

- **Recommended action:** Queue for expert review; every hop carries documentary-grade evidence, so this false lead is not separable from a true pathway on grades alone and requires full manual verification of each underlying record.

### CAND_0076 (false_positive)

- **Node sequence:** Funder_009 -> Intermediary_009 -> Campaign_L003

- **Edge sequence:** funds -> partners_with

- **Evidence grades:** 4 -> 3

- **Edge provenance:** ground-truth -> distractor

- **Evidence snippets:** Synthetic record: Funder_009 is listed as providing funding to Intermediary_009 during Phase_01. || Synthetic record: Intermediary_009 is described as a partner of Campaign_L003 during Phase_01.

- **Review-priority score:** 69.45 (threshold 60.0) -> FLAGGED

- **Ground-truth label:** not seeded

- **Why:** HIGH-PRIORITY REVIEW (raw score 69.45 >= threshold 60.0 and eligible): includes a direct synthetic funding edge (grade 4); weakest hop grade 3, mean grade 3.50; documentary continuity maintained across all hops.

- **Recommended action:** Queue for expert review; every hop carries documentary-grade evidence, so this false lead is not separable from a true pathway on grades alone and requires full manual verification of each underlying record.

### CAND_0029 (false_positive)

- **Node sequence:** Funder_003 -> Intermediary_003 -> Campaign_EC04

- **Edge sequence:** funds -> partners_with

- **Evidence grades:** 4 -> 3

- **Edge provenance:** ground-truth -> distractor

- **Evidence snippets:** Synthetic record: Funder_003 is listed as providing funding to Intermediary_003 during Phase_01. || Synthetic record: Intermediary_003 is described as a partner of Campaign_EC04 during Phase_03.

- **Review-priority score:** 66.45 (threshold 60.0) -> FLAGGED

- **Ground-truth label:** not seeded

- **Why:** HIGH-PRIORITY REVIEW (raw score 66.45 >= threshold 60.0 and eligible): includes a direct synthetic funding edge (grade 4); weakest hop grade 3, mean grade 3.50; documentary continuity maintained across all hops.

- **Recommended action:** Queue for expert review; every hop carries documentary-grade evidence, so this false lead is not separable from a true pathway on grades alone and requires full manual verification of each underlying record.

### CAND_0055 (false_positive)

- **Node sequence:** Funder_006 -> Intermediary_006 -> Campaign_EC10

- **Edge sequence:** funds -> partners_with

- **Evidence grades:** 4 -> 3

- **Edge provenance:** ground-truth -> distractor

- **Evidence snippets:** Synthetic record: Funder_006 is listed as providing funding to Intermediary_006 during Phase_01. || Synthetic record: Intermediary_006 is described as a partner of Campaign_EC10 during Phase_02.

- **Review-priority score:** 66.45 (threshold 60.0) -> FLAGGED

- **Ground-truth label:** not seeded

- **Why:** HIGH-PRIORITY REVIEW (raw score 66.45 >= threshold 60.0 and eligible): includes a direct synthetic funding edge (grade 4); weakest hop grade 3, mean grade 3.50; documentary continuity maintained across all hops.

- **Recommended action:** Queue for expert review; every hop carries documentary-grade evidence, so this false lead is not separable from a true pathway on grades alone and requires full manual verification of each underlying record.

### CAND_0023 (false_positive)

- **Node sequence:** Funder_002 -> Intermediary_002 -> Campaign_EC02

- **Edge sequence:** funds -> partners_with

- **Evidence grades:** 4 -> 3

- **Edge provenance:** ground-truth -> distractor

- **Evidence snippets:** Synthetic record: Funder_002 is listed as providing funding to Intermediary_002 during Phase_01. || Synthetic record: Intermediary_002 is described as a partner of Campaign_EC02 during Phase_02.

- **Review-priority score:** 66.45 (threshold 60.0) -> FLAGGED

- **Ground-truth label:** not seeded

- **Why:** HIGH-PRIORITY REVIEW (raw score 66.45 >= threshold 60.0 and eligible): includes a direct synthetic funding edge (grade 4); weakest hop grade 3, mean grade 3.50; documentary continuity maintained across all hops.

- **Recommended action:** Queue for expert review; every hop carries documentary-grade evidence, so this false lead is not separable from a true pathway on grades alone and requires full manual verification of each underlying record.

### CAND_0059 (false_positive)

- **Node sequence:** Funder_007 -> Intermediary_007 -> Campaign_EC12

- **Edge sequence:** funds -> partners_with

- **Evidence grades:** 4 -> 3

- **Edge provenance:** ground-truth -> distractor

- **Evidence snippets:** Synthetic record: Funder_007 is listed as providing funding to Intermediary_007 during Phase_01. || Synthetic record: Intermediary_007 is described as a partner of Campaign_EC12 during Phase_03.

- **Review-priority score:** 66.45 (threshold 60.0) -> FLAGGED

- **Ground-truth label:** not seeded

- **Why:** HIGH-PRIORITY REVIEW (raw score 66.45 >= threshold 60.0 and eligible): includes a direct synthetic funding edge (grade 4); weakest hop grade 3, mean grade 3.50; documentary continuity maintained across all hops.

- **Recommended action:** Queue for expert review; every hop carries documentary-grade evidence, so this false lead is not separable from a true pathway on grades alone and requires full manual verification of each underlying record.

### CAND_0070 (false_positive)

- **Node sequence:** Funder_008 -> Intermediary_008 -> Campaign_L001

- **Edge sequence:** funds -> partners_with

- **Evidence grades:** 4 -> 3

- **Edge provenance:** ground-truth -> distractor

- **Evidence snippets:** Synthetic record: Funder_008 is listed as providing funding to Intermediary_008 during Phase_01. || Synthetic record: Intermediary_008 is described as a partner of Campaign_L001 during Phase_04.

- **Review-priority score:** 66.45 (threshold 60.0) -> FLAGGED

- **Ground-truth label:** not seeded

- **Why:** HIGH-PRIORITY REVIEW (raw score 66.45 >= threshold 60.0 and eligible): includes a direct synthetic funding edge (grade 4); weakest hop grade 3, mean grade 3.50; documentary continuity maintained across all hops.

- **Recommended action:** Queue for expert review; every hop carries documentary-grade evidence, so this false lead is not separable from a true pathway on grades alone and requires full manual verification of each underlying record.

### CAND_0033 (false_positive)

- **Node sequence:** Funder_004 -> Intermediary_004 -> Campaign_EC06

- **Edge sequence:** funds -> partners_with

- **Evidence grades:** 4 -> 3

- **Edge provenance:** ground-truth -> distractor

- **Evidence snippets:** Synthetic record: Funder_004 is listed as providing funding to Intermediary_004 during Phase_01. || Synthetic record: Intermediary_004 is described as a partner of Campaign_EC06 during Phase_04.

- **Review-priority score:** 66.45 (threshold 60.0) -> FLAGGED

- **Ground-truth label:** not seeded

- **Why:** HIGH-PRIORITY REVIEW (raw score 66.45 >= threshold 60.0 and eligible): includes a direct synthetic funding edge (grade 4); weakest hop grade 3, mean grade 3.50; documentary continuity maintained across all hops.

- **Recommended action:** Queue for expert review; every hop carries documentary-grade evidence, so this false lead is not separable from a true pathway on grades alone and requires full manual verification of each underlying record.

### CAND_0002 (false_positive)

- **Node sequence:** Funder_000 -> Intermediary_000 -> Campaign_022

- **Edge sequence:** funds -> partners_with

- **Evidence grades:** 4 -> 3

- **Edge provenance:** ground-truth -> distractor

- **Evidence snippets:** Synthetic record: Funder_000 is listed as providing funding to Intermediary_000 during Phase_01. || Synthetic record: Intermediary_000 is described as a partner of Campaign_022 during Phase_04.

- **Review-priority score:** 66.45 (threshold 60.0) -> FLAGGED

- **Ground-truth label:** not seeded

- **Why:** HIGH-PRIORITY REVIEW (raw score 66.45 >= threshold 60.0 and eligible): includes a direct synthetic funding edge (grade 4); weakest hop grade 3, mean grade 3.50; documentary continuity maintained across all hops.

- **Recommended action:** Queue for expert review; every hop carries documentary-grade evidence, so this false lead is not separable from a true pathway on grades alone and requires full manual verification of each underlying record.

### CAND_0046 (false_positive)

- **Node sequence:** Funder_005 -> Intermediary_005 -> Campaign_024

- **Edge sequence:** funds -> amplifies

- **Evidence grades:** 4 -> 2

- **Edge provenance:** ground-truth -> distractor

- **Evidence snippets:** Synthetic record: Funder_005 is listed as providing funding to Intermediary_005 during Phase_01. || Synthetic record: Intermediary_005 repeatedly amplified output attributed to Campaign_024 during Phase_01.

- **Review-priority score:** 64.2 (threshold 60.0) -> FLAGGED

- **Ground-truth label:** not seeded

- **Why:** HIGH-PRIORITY REVIEW (raw score 64.20 >= threshold 60.0 and eligible): includes a direct synthetic funding edge (grade 4); weakest hop grade 2, mean grade 3.00; drops to a grade-2 shared-link/amplification hop.

- **Recommended action:** Queue for expert review as a possible lead only; the weakest hop is low grade (grade 2), so it may be set aside on inspection of that hop.

### CAND_0012 (false_positive)

- **Node sequence:** Funder_001 -> Intermediary_001 -> Campaign_016

- **Edge sequence:** funds -> amplifies

- **Evidence grades:** 4 -> 2

- **Edge provenance:** ground-truth -> distractor

- **Evidence snippets:** Synthetic record: Funder_001 is listed as providing funding to Intermediary_001 during Phase_01. || Synthetic record: Intermediary_001 repeatedly amplified output attributed to Campaign_016 during Phase_01.

- **Review-priority score:** 64.2 (threshold 60.0) -> FLAGGED

- **Ground-truth label:** not seeded

- **Why:** HIGH-PRIORITY REVIEW (raw score 64.20 >= threshold 60.0 and eligible): includes a direct synthetic funding edge (grade 4); weakest hop grade 2, mean grade 3.00; drops to a grade-2 shared-link/amplification hop.

- **Recommended action:** Queue for expert review as a possible lead only; the weakest hop is low grade (grade 2), so it may be set aside on inspection of that hop.

### CAND_0027 (false_positive)

- **Node sequence:** Funder_003 -> Intermediary_003 -> Campaign_016

- **Edge sequence:** funds -> uses_similar_language

- **Evidence grades:** 4 -> 2

- **Edge provenance:** ground-truth -> distractor

- **Evidence snippets:** Synthetic record: Funder_003 is listed as providing funding to Intermediary_003 during Phase_01. || Synthetic record: Intermediary_003 used wording closely similar to Campaign_016 during Phase_01.

- **Review-priority score:** 63.7 (threshold 60.0) -> FLAGGED

- **Ground-truth label:** not seeded

- **Why:** HIGH-PRIORITY REVIEW (raw score 63.70 >= threshold 60.0 and eligible): includes a direct synthetic funding edge (grade 4); weakest hop grade 2, mean grade 3.00; drops to a grade-2 shared-link/amplification hop.

- **Recommended action:** Queue for expert review as a possible lead only; the weakest hop is low grade (grade 2), so it may be set aside on inspection of that hop.

### CAND_0061 (false_positive)

- **Node sequence:** Funder_007 -> Intermediary_007 -> Campaign_024

- **Edge sequence:** funds -> uses_similar_language

- **Evidence grades:** 4 -> 2

- **Edge provenance:** ground-truth -> distractor

- **Evidence snippets:** Synthetic record: Funder_007 is listed as providing funding to Intermediary_007 during Phase_01. || Synthetic record: Intermediary_007 used wording closely similar to Campaign_024 during Phase_01.

- **Review-priority score:** 63.7 (threshold 60.0) -> FLAGGED

- **Ground-truth label:** not seeded

- **Why:** HIGH-PRIORITY REVIEW (raw score 63.70 >= threshold 60.0 and eligible): includes a direct synthetic funding edge (grade 4); weakest hop grade 2, mean grade 3.00; drops to a grade-2 shared-link/amplification hop.

- **Recommended action:** Queue for expert review as a possible lead only; the weakest hop is low grade (grade 2), so it may be set aside on inspection of that hop.

### CAND_0075 (false_positive)

- **Node sequence:** Funder_009 -> Intermediary_009 -> Campaign_024

- **Edge sequence:** funds -> shares_link

- **Evidence grades:** 4 -> 2

- **Edge provenance:** ground-truth -> distractor

- **Evidence snippets:** Synthetic record: Funder_009 is listed as providing funding to Intermediary_009 during Phase_01. || Synthetic record: Intermediary_009 and Campaign_024 shared the same abstract link during Phase_01.

- **Review-priority score:** 61.7 (threshold 60.0) -> FLAGGED

- **Ground-truth label:** not seeded

- **Why:** HIGH-PRIORITY REVIEW (raw score 61.70 >= threshold 60.0 and eligible): includes a direct synthetic funding edge (grade 4); weakest hop grade 2, mean grade 3.00; drops to a grade-2 shared-link/amplification hop.

- **Recommended action:** Queue for expert review as a possible lead only; the weakest hop is low grade (grade 2), so it may be set aside on inspection of that hop.

### CAND_0044 (false_positive)

- **Node sequence:** Funder_005 -> Intermediary_005 -> Campaign_016

- **Edge sequence:** funds -> shares_link

- **Evidence grades:** 4 -> 2

- **Edge provenance:** ground-truth -> distractor

- **Evidence snippets:** Synthetic record: Funder_005 is listed as providing funding to Intermediary_005 during Phase_01. || Synthetic record: Intermediary_005 and Campaign_016 shared the same abstract link during Phase_01.

- **Review-priority score:** 61.7 (threshold 60.0) -> FLAGGED

- **Ground-truth label:** not seeded

- **Why:** HIGH-PRIORITY REVIEW (raw score 61.70 >= threshold 60.0 and eligible): includes a direct synthetic funding edge (grade 4); weakest hop grade 2, mean grade 3.00; drops to a grade-2 shared-link/amplification hop.

- **Recommended action:** Queue for expert review as a possible lead only; the weakest hop is low grade (grade 2), so it may be set aside on inspection of that hop.

### CAND_0015 (false_positive)

- **Node sequence:** Funder_001 -> Intermediary_001 -> Campaign_008

- **Edge sequence:** funds -> shares_link

- **Evidence grades:** 4 -> 2

- **Edge provenance:** ground-truth -> distractor

- **Evidence snippets:** Synthetic record: Funder_001 is listed as providing funding to Intermediary_001 during Phase_01. || Synthetic record: Intermediary_001 and Campaign_008 shared the same abstract link during Phase_01.

- **Review-priority score:** 61.7 (threshold 60.0) -> FLAGGED

- **Ground-truth label:** not seeded

- **Why:** HIGH-PRIORITY REVIEW (raw score 61.70 >= threshold 60.0 and eligible): includes a direct synthetic funding edge (grade 4); weakest hop grade 2, mean grade 3.00; drops to a grade-2 shared-link/amplification hop.

- **Recommended action:** Queue for expert review as a possible lead only; the weakest hop is low grade (grade 2), so it may be set aside on inspection of that hop.

### CAND_0106 (false_positive)

- **Node sequence:** Funder_L011 -> Intermediary_L011 -> Proxy_L011 -> Campaign_L011

- **Edge sequence:** funds -> partners_with -> shares_link

- **Evidence grades:** 4 -> 3 -> 2

- **Edge provenance:** distractor -> distractor -> distractor

- **Evidence snippets:** Synthetic record: Funder_L011 is listed as providing funding to Intermediary_L011 during Phase_01. || Synthetic record: Intermediary_L011 is described as a partner of Proxy_L011 during Phase_01. || Synthetic record: Proxy_L011 and Campaign_L011 shared the same abstract link during Phase_02.

- **Review-priority score:** 61.3 (threshold 60.0) -> FLAGGED

- **Ground-truth label:** not seeded

- **Why:** HIGH-PRIORITY REVIEW (raw score 61.30 >= threshold 60.0 and eligible): includes a direct synthetic funding edge (grade 4); weakest hop grade 2, mean grade 3.00; drops to a grade-2 shared-link/amplification hop.

- **Recommended action:** Queue for expert review as a possible lead only; the weakest hop is low grade (grade 2), so it may be set aside on inspection of that hop.

### CAND_0108 (false_positive)

- **Node sequence:** Funder_L013 -> Intermediary_L013 -> Proxy_L013 -> Campaign_L013

- **Edge sequence:** funds -> partners_with -> shares_link

- **Evidence grades:** 4 -> 3 -> 2

- **Edge provenance:** distractor -> distractor -> distractor

- **Evidence snippets:** Synthetic record: Funder_L013 is listed as providing funding to Intermediary_L013 during Phase_01. || Synthetic record: Intermediary_L013 is described as a partner of Proxy_L013 during Phase_01. || Synthetic record: Proxy_L013 and Campaign_L013 shared the same abstract link during Phase_02.

- **Review-priority score:** 61.3 (threshold 60.0) -> FLAGGED

- **Ground-truth label:** not seeded

- **Why:** HIGH-PRIORITY REVIEW (raw score 61.30 >= threshold 60.0 and eligible): includes a direct synthetic funding edge (grade 4); weakest hop grade 2, mean grade 3.00; drops to a grade-2 shared-link/amplification hop.

- **Recommended action:** Queue for expert review as a possible lead only; the weakest hop is low grade (grade 2), so it may be set aside on inspection of that hop.

### CAND_0057 (false_positive)

- **Node sequence:** Funder_007 -> Intermediary_007 -> Proxy_010 -> Campaign_010

- **Edge sequence:** funds -> shares_link -> amplifies

- **Evidence grades:** 4 -> 2 -> 2

- **Edge provenance:** ground-truth -> distractor -> ground-truth

- **Evidence snippets:** Synthetic record: Funder_007 is listed as providing funding to Intermediary_007 during Phase_01. || Synthetic record: Intermediary_007 and Proxy_010 shared the same abstract link during Phase_02. || Synthetic record: Proxy_010 repeatedly amplified output attributed to Campaign_010 during Phase_02.

- **Review-priority score:** 61.3 (threshold 60.0) -> FLAGGED

- **Ground-truth label:** not seeded

- **Why:** HIGH-PRIORITY REVIEW (raw score 61.30 >= threshold 60.0 and eligible): includes a direct synthetic funding edge (grade 4); weakest hop grade 2, mean grade 2.67; drops to a grade-2 shared-link/amplification hop.

- **Recommended action:** Queue for expert review as a possible lead only; the weakest hop is low grade (grade 2), so it may be set aside on inspection of that hop.

### CAND_0096 (false_positive)

- **Node sequence:** Funder_L001 -> Intermediary_L001 -> Proxy_L001 -> Campaign_L001

- **Edge sequence:** funds -> partners_with -> shares_link

- **Evidence grades:** 4 -> 3 -> 2

- **Edge provenance:** distractor -> distractor -> distractor

- **Evidence snippets:** Synthetic record: Funder_L001 is listed as providing funding to Intermediary_L001 during Phase_01. || Synthetic record: Intermediary_L001 is described as a partner of Proxy_L001 during Phase_01. || Synthetic record: Proxy_L001 and Campaign_L001 shared the same abstract link during Phase_02.

- **Review-priority score:** 61.3 (threshold 60.0) -> FLAGGED

- **Ground-truth label:** not seeded

- **Why:** HIGH-PRIORITY REVIEW (raw score 61.30 >= threshold 60.0 and eligible): includes a direct synthetic funding edge (grade 4); weakest hop grade 2, mean grade 3.00; drops to a grade-2 shared-link/amplification hop.

- **Recommended action:** Queue for expert review as a possible lead only; the weakest hop is low grade (grade 2), so it may be set aside on inspection of that hop.

### CAND_0098 (false_positive)

- **Node sequence:** Funder_L003 -> Intermediary_L003 -> Proxy_L003 -> Campaign_L003

- **Edge sequence:** funds -> partners_with -> shares_link

- **Evidence grades:** 4 -> 3 -> 2

- **Edge provenance:** distractor -> distractor -> distractor

- **Evidence snippets:** Synthetic record: Funder_L003 is listed as providing funding to Intermediary_L003 during Phase_01. || Synthetic record: Intermediary_L003 is described as a partner of Proxy_L003 during Phase_01. || Synthetic record: Proxy_L003 and Campaign_L003 shared the same abstract link during Phase_02.

- **Review-priority score:** 61.3 (threshold 60.0) -> FLAGGED

- **Ground-truth label:** not seeded

- **Why:** HIGH-PRIORITY REVIEW (raw score 61.30 >= threshold 60.0 and eligible): includes a direct synthetic funding edge (grade 4); weakest hop grade 2, mean grade 3.00; drops to a grade-2 shared-link/amplification hop.

- **Recommended action:** Queue for expert review as a possible lead only; the weakest hop is low grade (grade 2), so it may be set aside on inspection of that hop.

### CAND_0104 (false_positive)

- **Node sequence:** Funder_L009 -> Intermediary_L009 -> Proxy_L009 -> Campaign_L009

- **Edge sequence:** funds -> partners_with -> shares_link

- **Evidence grades:** 4 -> 3 -> 2

- **Edge provenance:** distractor -> distractor -> distractor

- **Evidence snippets:** Synthetic record: Funder_L009 is listed as providing funding to Intermediary_L009 during Phase_01. || Synthetic record: Intermediary_L009 is described as a partner of Proxy_L009 during Phase_01. || Synthetic record: Proxy_L009 and Campaign_L009 shared the same abstract link during Phase_02.

- **Review-priority score:** 61.3 (threshold 60.0) -> FLAGGED

- **Ground-truth label:** not seeded

- **Why:** HIGH-PRIORITY REVIEW (raw score 61.30 >= threshold 60.0 and eligible): includes a direct synthetic funding edge (grade 4); weakest hop grade 2, mean grade 3.00; drops to a grade-2 shared-link/amplification hop.

- **Recommended action:** Queue for expert review as a possible lead only; the weakest hop is low grade (grade 2), so it may be set aside on inspection of that hop.

### CAND_0100 (false_positive)

- **Node sequence:** Funder_L005 -> Intermediary_L005 -> Proxy_L005 -> Campaign_L005

- **Edge sequence:** funds -> partners_with -> shares_link

- **Evidence grades:** 4 -> 3 -> 2

- **Edge provenance:** distractor -> distractor -> distractor

- **Evidence snippets:** Synthetic record: Funder_L005 is listed as providing funding to Intermediary_L005 during Phase_01. || Synthetic record: Intermediary_L005 is described as a partner of Proxy_L005 during Phase_01. || Synthetic record: Proxy_L005 and Campaign_L005 shared the same abstract link during Phase_02.

- **Review-priority score:** 61.3 (threshold 60.0) -> FLAGGED

- **Ground-truth label:** not seeded

- **Why:** HIGH-PRIORITY REVIEW (raw score 61.30 >= threshold 60.0 and eligible): includes a direct synthetic funding edge (grade 4); weakest hop grade 2, mean grade 3.00; drops to a grade-2 shared-link/amplification hop.

- **Recommended action:** Queue for expert review as a possible lead only; the weakest hop is low grade (grade 2), so it may be set aside on inspection of that hop.

### CAND_0102 (false_positive)

- **Node sequence:** Funder_L007 -> Intermediary_L007 -> Proxy_L007 -> Campaign_L007

- **Edge sequence:** funds -> partners_with -> shares_link

- **Evidence grades:** 4 -> 3 -> 2

- **Edge provenance:** distractor -> distractor -> distractor

- **Evidence snippets:** Synthetic record: Funder_L007 is listed as providing funding to Intermediary_L007 during Phase_01. || Synthetic record: Intermediary_L007 is described as a partner of Proxy_L007 during Phase_01. || Synthetic record: Proxy_L007 and Campaign_L007 shared the same abstract link during Phase_02.

- **Review-priority score:** 61.3 (threshold 60.0) -> FLAGGED

- **Ground-truth label:** not seeded

- **Why:** HIGH-PRIORITY REVIEW (raw score 61.30 >= threshold 60.0 and eligible): includes a direct synthetic funding edge (grade 4); weakest hop grade 2, mean grade 3.00; drops to a grade-2 shared-link/amplification hop.

- **Recommended action:** Queue for expert review as a possible lead only; the weakest hop is low grade (grade 2), so it may be set aside on inspection of that hop.

### CAND_0019 (false_positive)

- **Node sequence:** Funder_002 -> Intermediary_002 -> Proxy_004 -> Campaign_004

- **Edge sequence:** funds -> shares_link -> hosts

- **Evidence grades:** 4 -> 2 -> 3

- **Edge provenance:** ground-truth -> distractor -> ground-truth

- **Evidence snippets:** Synthetic record: Funder_002 is listed as providing funding to Intermediary_002 during Phase_01. || Synthetic record: Intermediary_002 and Proxy_004 shared the same abstract link during Phase_01. || Synthetic record: Proxy_004 is listed as a host of Campaign_004 during Phase_02.

- **Review-priority score:** 61.3 (threshold 60.0) -> FLAGGED

- **Ground-truth label:** not seeded

- **Why:** HIGH-PRIORITY REVIEW (raw score 61.30 >= threshold 60.0 and eligible): includes a direct synthetic funding edge (grade 4); weakest hop grade 2, mean grade 3.00; drops to a grade-2 shared-link/amplification hop.

- **Recommended action:** Queue for expert review as a possible lead only; the weakest hop is low grade (grade 2), so it may be set aside on inspection of that hop.

### CAND_0050 (false_positive)

- **Node sequence:** Funder_006 -> Intermediary_006 -> Proxy_009 -> Report_009

- **Edge sequence:** funds -> shares_link -> publishes

- **Evidence grades:** 4 -> 2 -> 3

- **Edge provenance:** ground-truth -> distractor -> ground-truth

- **Evidence snippets:** Synthetic record: Funder_006 is listed as providing funding to Intermediary_006 during Phase_01. || Synthetic record: Intermediary_006 and Proxy_009 shared the same abstract link during Phase_01. || Synthetic record: Proxy_009 is listed as the publisher of Report_009 during Phase_02.

- **Review-priority score:** 61.3 (threshold 60.0) -> FLAGGED

- **Ground-truth label:** not seeded

- **Why:** HIGH-PRIORITY REVIEW (raw score 61.30 >= threshold 60.0 and eligible): includes a direct synthetic funding edge (grade 4); weakest hop grade 2, mean grade 3.00; drops to a grade-2 shared-link/amplification hop.

- **Recommended action:** Queue for expert review as a possible lead only; the weakest hop is low grade (grade 2), so it may be set aside on inspection of that hop.

### CAND_0032 (false_positive)

- **Node sequence:** Funder_003 -> Intermediary_003 -> Proxy_005 -> Report_005

- **Edge sequence:** funds -> shares_link -> publishes

- **Evidence grades:** 4 -> 2 -> 3

- **Edge provenance:** ground-truth -> distractor -> ground-truth

- **Evidence snippets:** Synthetic record: Funder_003 is listed as providing funding to Intermediary_003 during Phase_01. || Synthetic record: Intermediary_003 and Proxy_005 shared the same abstract link during Phase_02. || Synthetic record: Proxy_005 is listed as the publisher of Report_005 during Phase_02.

- **Review-priority score:** 61.3 (threshold 60.0) -> FLAGGED

- **Ground-truth label:** not seeded

- **Why:** HIGH-PRIORITY REVIEW (raw score 61.30 >= threshold 60.0 and eligible): includes a direct synthetic funding edge (grade 4); weakest hop grade 2, mean grade 3.00; drops to a grade-2 shared-link/amplification hop.

- **Recommended action:** Queue for expert review as a possible lead only; the weakest hop is low grade (grade 2), so it may be set aside on inspection of that hop.

### CAND_0110 (false_positive)

- **Node sequence:** Funder_L015 -> Intermediary_L015 -> Proxy_L015 -> Campaign_L015

- **Edge sequence:** funds -> partners_with -> shares_link

- **Evidence grades:** 4 -> 3 -> 2

- **Edge provenance:** distractor -> distractor -> distractor

- **Evidence snippets:** Synthetic record: Funder_L015 is listed as providing funding to Intermediary_L015 during Phase_01. || Synthetic record: Intermediary_L015 is described as a partner of Proxy_L015 during Phase_01. || Synthetic record: Proxy_L015 and Campaign_L015 shared the same abstract link during Phase_02.

- **Review-priority score:** 61.3 (threshold 60.0) -> FLAGGED

- **Ground-truth label:** not seeded

- **Why:** HIGH-PRIORITY REVIEW (raw score 61.30 >= threshold 60.0 and eligible): includes a direct synthetic funding edge (grade 4); weakest hop grade 2, mean grade 3.00; drops to a grade-2 shared-link/amplification hop.

- **Recommended action:** Queue for expert review as a possible lead only; the weakest hop is low grade (grade 2), so it may be set aside on inspection of that hop.

### CAND_0018 (false_positive)

- **Node sequence:** Funder_002 -> Intermediary_002 -> Campaign_018

- **Edge sequence:** funds -> amplifies

- **Evidence grades:** 4 -> 2

- **Edge provenance:** ground-truth -> distractor

- **Evidence snippets:** Synthetic record: Funder_002 is listed as providing funding to Intermediary_002 during Phase_01. || Synthetic record: Intermediary_002 repeatedly amplified output attributed to Campaign_018 during Phase_02.

- **Review-priority score:** 61.2 (threshold 60.0) -> FLAGGED

- **Ground-truth label:** not seeded

- **Why:** HIGH-PRIORITY REVIEW (raw score 61.20 >= threshold 60.0 and eligible): includes a direct synthetic funding edge (grade 4); weakest hop grade 2, mean grade 3.00; drops to a grade-2 shared-link/amplification hop.

- **Recommended action:** Queue for expert review as a possible lead only; the weakest hop is low grade (grade 2), so it may be set aside on inspection of that hop.

### CAND_0008 (false_positive)

- **Node sequence:** Funder_000 -> Intermediary_000 -> Campaign_014

- **Edge sequence:** funds -> amplifies

- **Evidence grades:** 4 -> 2

- **Edge provenance:** ground-truth -> distractor

- **Evidence snippets:** Synthetic record: Funder_000 is listed as providing funding to Intermediary_000 during Phase_01. || Synthetic record: Intermediary_000 repeatedly amplified output attributed to Campaign_014 during Phase_04.

- **Review-priority score:** 61.2 (threshold 60.0) -> FLAGGED

- **Ground-truth label:** not seeded

- **Why:** HIGH-PRIORITY REVIEW (raw score 61.20 >= threshold 60.0 and eligible): includes a direct synthetic funding edge (grade 4); weakest hop grade 2, mean grade 3.00; drops to a grade-2 shared-link/amplification hop.

- **Recommended action:** Queue for expert review as a possible lead only; the weakest hop is low grade (grade 2), so it may be set aside on inspection of that hop.

### CAND_0060 (false_positive)

- **Node sequence:** Funder_007 -> Intermediary_007 -> Campaign_EC04

- **Edge sequence:** funds -> amplifies

- **Evidence grades:** 4 -> 2

- **Edge provenance:** ground-truth -> distractor

- **Evidence snippets:** Synthetic record: Funder_007 is listed as providing funding to Intermediary_007 during Phase_01. || Synthetic record: Intermediary_007 repeatedly amplified output attributed to Campaign_EC04 during Phase_03.

- **Review-priority score:** 61.2 (threshold 60.0) -> FLAGGED

- **Ground-truth label:** not seeded

- **Why:** HIGH-PRIORITY REVIEW (raw score 61.20 >= threshold 60.0 and eligible): includes a direct synthetic funding edge (grade 4); weakest hop grade 2, mean grade 3.00; drops to a grade-2 shared-link/amplification hop.

- **Recommended action:** Queue for expert review as a possible lead only; the weakest hop is low grade (grade 2), so it may be set aside on inspection of that hop.

### CAND_0049 (false_positive)

- **Node sequence:** Funder_006 -> Intermediary_006 -> Campaign_EC02

- **Edge sequence:** funds -> amplifies

- **Evidence grades:** 4 -> 2

- **Edge provenance:** ground-truth -> distractor

- **Evidence snippets:** Synthetic record: Funder_006 is listed as providing funding to Intermediary_006 during Phase_01. || Synthetic record: Intermediary_006 repeatedly amplified output attributed to Campaign_EC02 during Phase_02.

- **Review-priority score:** 61.2 (threshold 60.0) -> FLAGGED

- **Ground-truth label:** not seeded

- **Why:** HIGH-PRIORITY REVIEW (raw score 61.20 >= threshold 60.0 and eligible): includes a direct synthetic funding edge (grade 4); weakest hop grade 2, mean grade 3.00; drops to a grade-2 shared-link/amplification hop.

- **Recommended action:** Queue for expert review as a possible lead only; the weakest hop is low grade (grade 2), so it may be set aside on inspection of that hop.

### CAND_0025 (false_positive)

- **Node sequence:** Funder_003 -> Intermediary_003 -> Campaign_020

- **Edge sequence:** funds -> amplifies

- **Evidence grades:** 4 -> 2

- **Edge provenance:** ground-truth -> distractor

- **Evidence snippets:** Synthetic record: Funder_003 is listed as providing funding to Intermediary_003 during Phase_01. || Synthetic record: Intermediary_003 repeatedly amplified output attributed to Campaign_020 during Phase_03.

- **Review-priority score:** 61.2 (threshold 60.0) -> FLAGGED

- **Ground-truth label:** not seeded

- **Why:** HIGH-PRIORITY REVIEW (raw score 61.20 >= threshold 60.0 and eligible): includes a direct synthetic funding edge (grade 4); weakest hop grade 2, mean grade 3.00; drops to a grade-2 shared-link/amplification hop.

- **Recommended action:** Queue for expert review as a possible lead only; the weakest hop is low grade (grade 2), so it may be set aside on inspection of that hop.

### CAND_0039 (false_positive)

- **Node sequence:** Funder_004 -> Intermediary_004 -> Campaign_022

- **Edge sequence:** funds -> amplifies

- **Evidence grades:** 4 -> 2

- **Edge provenance:** ground-truth -> distractor

- **Evidence snippets:** Synthetic record: Funder_004 is listed as providing funding to Intermediary_004 during Phase_01. || Synthetic record: Intermediary_004 repeatedly amplified output attributed to Campaign_022 during Phase_04.

- **Review-priority score:** 61.2 (threshold 60.0) -> FLAGGED

- **Ground-truth label:** not seeded

- **Why:** HIGH-PRIORITY REVIEW (raw score 61.20 >= threshold 60.0 and eligible): includes a direct synthetic funding edge (grade 4); weakest hop grade 2, mean grade 3.00; drops to a grade-2 shared-link/amplification hop.

- **Recommended action:** Queue for expert review as a possible lead only; the weakest hop is low grade (grade 2), so it may be set aside on inspection of that hop.

### CAND_0054 (false_positive)

- **Node sequence:** Funder_006 -> Intermediary_006 -> Campaign_022

- **Edge sequence:** funds -> uses_similar_language

- **Evidence grades:** 4 -> 2

- **Edge provenance:** ground-truth -> distractor

- **Evidence snippets:** Synthetic record: Funder_006 is listed as providing funding to Intermediary_006 during Phase_01. || Synthetic record: Intermediary_006 used wording closely similar to Campaign_022 during Phase_04.

- **Review-priority score:** 60.7 (threshold 60.0) -> FLAGGED

- **Ground-truth label:** not seeded

- **Why:** HIGH-PRIORITY REVIEW (raw score 60.70 >= threshold 60.0 and eligible): includes a direct synthetic funding edge (grade 4); weakest hop grade 2, mean grade 3.00; drops to a grade-2 shared-link/amplification hop.

- **Recommended action:** Queue for expert review as a possible lead only; the weakest hop is low grade (grade 2), so it may be set aside on inspection of that hop.

### CAND_0043 (false_positive)

- **Node sequence:** Funder_005 -> Intermediary_005 -> Campaign_020

- **Edge sequence:** funds -> uses_similar_language

- **Evidence grades:** 4 -> 2

- **Edge provenance:** ground-truth -> distractor

- **Evidence snippets:** Synthetic record: Funder_005 is listed as providing funding to Intermediary_005 during Phase_01. || Synthetic record: Intermediary_005 used wording closely similar to Campaign_020 during Phase_03.

- **Review-priority score:** 60.7 (threshold 60.0) -> FLAGGED

- **Ground-truth label:** not seeded

- **Why:** HIGH-PRIORITY REVIEW (raw score 60.70 >= threshold 60.0 and eligible): includes a direct synthetic funding edge (grade 4); weakest hop grade 2, mean grade 3.00; drops to a grade-2 shared-link/amplification hop.

- **Recommended action:** Queue for expert review as a possible lead only; the weakest hop is low grade (grade 2), so it may be set aside on inspection of that hop.

### CAND_0022 (false_positive)

- **Node sequence:** Funder_002 -> Intermediary_002 -> Campaign_014

- **Edge sequence:** funds -> uses_similar_language

- **Evidence grades:** 4 -> 2

- **Edge provenance:** ground-truth -> distractor

- **Evidence snippets:** Synthetic record: Funder_002 is listed as providing funding to Intermediary_002 during Phase_01. || Synthetic record: Intermediary_002 used wording closely similar to Campaign_014 during Phase_04.

- **Review-priority score:** 60.7 (threshold 60.0) -> FLAGGED

- **Ground-truth label:** not seeded

- **Why:** HIGH-PRIORITY REVIEW (raw score 60.70 >= threshold 60.0 and eligible): includes a direct synthetic funding edge (grade 4); weakest hop grade 2, mean grade 3.00; drops to a grade-2 shared-link/amplification hop.

- **Recommended action:** Queue for expert review as a possible lead only; the weakest hop is low grade (grade 2), so it may be set aside on inspection of that hop.

### CAND_0003 (false_positive)

- **Node sequence:** Funder_000 -> Intermediary_000 -> Campaign_010

- **Edge sequence:** funds -> uses_similar_language

- **Evidence grades:** 4 -> 2

- **Edge provenance:** ground-truth -> distractor

- **Evidence snippets:** Synthetic record: Funder_000 is listed as providing funding to Intermediary_000 during Phase_01. || Synthetic record: Intermediary_000 used wording closely similar to Campaign_010 during Phase_02.

- **Review-priority score:** 60.7 (threshold 60.0) -> FLAGGED

- **Ground-truth label:** not seeded

- **Why:** HIGH-PRIORITY REVIEW (raw score 60.70 >= threshold 60.0 and eligible): includes a direct synthetic funding edge (grade 4); weakest hop grade 2, mean grade 3.00; drops to a grade-2 shared-link/amplification hop.

- **Recommended action:** Queue for expert review as a possible lead only; the weakest hop is low grade (grade 2), so it may be set aside on inspection of that hop.

### CAND_0034 (false_positive)

- **Node sequence:** Funder_004 -> Intermediary_004 -> Campaign_018

- **Edge sequence:** funds -> uses_similar_language

- **Evidence grades:** 4 -> 2

- **Edge provenance:** ground-truth -> distractor

- **Evidence snippets:** Synthetic record: Funder_004 is listed as providing funding to Intermediary_004 during Phase_01. || Synthetic record: Intermediary_004 used wording closely similar to Campaign_018 during Phase_02.

- **Review-priority score:** 60.7 (threshold 60.0) -> FLAGGED

- **Ground-truth label:** not seeded

- **Why:** HIGH-PRIORITY REVIEW (raw score 60.70 >= threshold 60.0 and eligible): includes a direct synthetic funding edge (grade 4); weakest hop grade 2, mean grade 3.00; drops to a grade-2 shared-link/amplification hop.

- **Recommended action:** Queue for expert review as a possible lead only; the weakest hop is low grade (grade 2), so it may be set aside on inspection of that hop.

### CAND_0009 (false_positive)

- **Node sequence:** Funder_001 -> Intermediary_001 -> Campaign_012

- **Edge sequence:** funds -> uses_similar_language

- **Evidence grades:** 4 -> 2

- **Edge provenance:** ground-truth -> distractor

- **Evidence snippets:** Synthetic record: Funder_001 is listed as providing funding to Intermediary_001 during Phase_01. || Synthetic record: Intermediary_001 used wording closely similar to Campaign_012 during Phase_03.

- **Review-priority score:** 60.7 (threshold 60.0) -> FLAGGED

- **Ground-truth label:** not seeded

- **Why:** HIGH-PRIORITY REVIEW (raw score 60.70 >= threshold 60.0 and eligible): includes a direct synthetic funding edge (grade 4); weakest hop grade 2, mean grade 3.00; drops to a grade-2 shared-link/amplification hop.

- **Recommended action:** Queue for expert review as a possible lead only; the weakest hop is low grade (grade 2), so it may be set aside on inspection of that hop.

### CAND_0072 (true_negative)

- **Node sequence:** Funder_009 -> Intermediary_009 -> Proxy_013 -> Report_013

- **Edge sequence:** funds -> shares_link -> publishes

- **Evidence grades:** 4 -> 2 -> 3

- **Edge provenance:** ground-truth -> distractor -> ground-truth

- **Evidence snippets:** Synthetic record: Funder_009 is listed as providing funding to Intermediary_009 during Phase_01. || Synthetic record: Intermediary_009 and Proxy_013 shared the same abstract link during Phase_04. || Synthetic record: Proxy_013 is listed as the publisher of Report_013 during Phase_02.

- **Review-priority score:** 59.3 (threshold 60.0) -> not flagged

- **Ground-truth label:** not seeded

- **Why:** not high priority: raw score 59.30 is below threshold 60.0: includes a direct synthetic funding edge (grade 4); weakest hop grade 2, mean grade 3.00; drops to a grade-2 shared-link/amplification hop.

- **Recommended action:** No review action required; retain in the audit log for completeness.

### CAND_0045 (true_negative)

- **Node sequence:** Funder_005 -> Intermediary_005 -> Proxy_008 -> Campaign_008

- **Edge sequence:** funds -> shares_link -> hosts

- **Evidence grades:** 4 -> 2 -> 3

- **Edge provenance:** ground-truth -> distractor -> ground-truth

- **Evidence snippets:** Synthetic record: Funder_005 is listed as providing funding to Intermediary_005 during Phase_01. || Synthetic record: Intermediary_005 and Proxy_008 shared the same abstract link during Phase_04. || Synthetic record: Proxy_008 is listed as a host of Campaign_008 during Phase_02.

- **Review-priority score:** 59.3 (threshold 60.0) -> not flagged

- **Ground-truth label:** not seeded

- **Why:** not high priority: raw score 59.30 is below threshold 60.0: includes a direct synthetic funding edge (grade 4); weakest hop grade 2, mean grade 3.00; drops to a grade-2 shared-link/amplification hop.

- **Recommended action:** No review action required; retain in the audit log for completeness.

### CAND_0005 (true_negative)

- **Node sequence:** Funder_000 -> Intermediary_000 -> Proxy_001 -> Report_001

- **Edge sequence:** funds -> shares_link -> publishes

- **Evidence grades:** 4 -> 2 -> 3

- **Edge provenance:** ground-truth -> distractor -> ground-truth

- **Evidence snippets:** Synthetic record: Funder_000 is listed as providing funding to Intermediary_000 during Phase_01. || Synthetic record: Intermediary_000 and Proxy_001 shared the same abstract link during Phase_03. || Synthetic record: Proxy_001 is listed as the publisher of Report_001 during Phase_02.

- **Review-priority score:** 59.3 (threshold 60.0) -> not flagged

- **Ground-truth label:** not seeded

- **Why:** not high priority: raw score 59.30 is below threshold 60.0: includes a direct synthetic funding edge (grade 4); weakest hop grade 2, mean grade 3.00; drops to a grade-2 shared-link/amplification hop.

- **Recommended action:** No review action required; retain in the audit log for completeness.

### CAND_0014 (true_negative)

- **Node sequence:** Funder_001 -> Intermediary_001 -> Proxy_002 -> Campaign_002

- **Edge sequence:** funds -> shares_link -> amplifies

- **Evidence grades:** 4 -> 2 -> 2

- **Edge provenance:** ground-truth -> distractor -> ground-truth

- **Evidence snippets:** Synthetic record: Funder_001 is listed as providing funding to Intermediary_001 during Phase_01. || Synthetic record: Intermediary_001 and Proxy_002 shared the same abstract link during Phase_04. || Synthetic record: Proxy_002 repeatedly amplified output attributed to Campaign_002 during Phase_02.

- **Review-priority score:** 59.3 (threshold 60.0) -> not flagged

- **Ground-truth label:** not seeded

- **Why:** not high priority: raw score 59.30 is below threshold 60.0: includes a direct synthetic funding edge (grade 4); weakest hop grade 2, mean grade 2.67; drops to a grade-2 shared-link/amplification hop.

- **Recommended action:** No review action required; retain in the audit log for completeness.

### CAND_0066 (true_negative)

- **Node sequence:** Funder_008 -> Intermediary_008 -> Proxy_012 -> Campaign_012

- **Edge sequence:** funds -> shares_link -> hosts

- **Evidence grades:** 4 -> 2 -> 3

- **Edge provenance:** ground-truth -> distractor -> ground-truth

- **Evidence snippets:** Synthetic record: Funder_008 is listed as providing funding to Intermediary_008 during Phase_01. || Synthetic record: Intermediary_008 and Proxy_012 shared the same abstract link during Phase_03. || Synthetic record: Proxy_012 is listed as a host of Campaign_012 during Phase_02.

- **Review-priority score:** 59.3 (threshold 60.0) -> not flagged

- **Ground-truth label:** not seeded

- **Why:** not high priority: raw score 59.30 is below threshold 60.0: includes a direct synthetic funding edge (grade 4); weakest hop grade 2, mean grade 3.00; drops to a grade-2 shared-link/amplification hop.

- **Recommended action:** No review action required; retain in the audit log for completeness.

### CAND_0037 (true_negative)

- **Node sequence:** Funder_004 -> Intermediary_004 -> Proxy_006 -> Campaign_006

- **Edge sequence:** funds -> shares_link -> amplifies

- **Evidence grades:** 4 -> 2 -> 2

- **Edge provenance:** ground-truth -> distractor -> ground-truth

- **Evidence snippets:** Synthetic record: Funder_004 is listed as providing funding to Intermediary_004 during Phase_01. || Synthetic record: Intermediary_004 and Proxy_006 shared the same abstract link during Phase_03. || Synthetic record: Proxy_006 repeatedly amplified output attributed to Campaign_006 during Phase_02.

- **Review-priority score:** 59.3 (threshold 60.0) -> not flagged

- **Ground-truth label:** not seeded

- **Why:** not high priority: raw score 59.30 is below threshold 60.0: includes a direct synthetic funding edge (grade 4); weakest hop grade 2, mean grade 2.67; drops to a grade-2 shared-link/amplification hop.

- **Recommended action:** No review action required; retain in the audit log for completeness.

### CAND_0006 (true_negative)

- **Node sequence:** Funder_000 -> Intermediary_000 -> Campaign_006

- **Edge sequence:** funds -> shares_link

- **Evidence grades:** 4 -> 2

- **Edge provenance:** ground-truth -> distractor

- **Evidence snippets:** Synthetic record: Funder_000 is listed as providing funding to Intermediary_000 during Phase_01. || Synthetic record: Intermediary_000 and Campaign_006 shared the same abstract link during Phase_04.

- **Review-priority score:** 58.7 (threshold 60.0) -> not flagged

- **Ground-truth label:** not seeded

- **Why:** not high priority: raw score 58.70 is below threshold 60.0: includes a direct synthetic funding edge (grade 4); weakest hop grade 2, mean grade 3.00; drops to a grade-2 shared-link/amplification hop.

- **Recommended action:** No review action required; retain in the audit log for completeness.

### CAND_0031 (true_negative)

- **Node sequence:** Funder_003 -> Intermediary_003 -> Campaign_012

- **Edge sequence:** funds -> shares_link

- **Evidence grades:** 4 -> 2

- **Edge provenance:** ground-truth -> distractor

- **Evidence snippets:** Synthetic record: Funder_003 is listed as providing funding to Intermediary_003 during Phase_01. || Synthetic record: Intermediary_003 and Campaign_012 shared the same abstract link during Phase_03.

- **Review-priority score:** 58.7 (threshold 60.0) -> not flagged

- **Ground-truth label:** not seeded

- **Why:** not high priority: raw score 58.70 is below threshold 60.0: includes a direct synthetic funding edge (grade 4); weakest hop grade 2, mean grade 3.00; drops to a grade-2 shared-link/amplification hop.

- **Recommended action:** No review action required; retain in the audit log for completeness.

### CAND_0017 (true_negative)

- **Node sequence:** Funder_002 -> Intermediary_002 -> Campaign_010

- **Edge sequence:** funds -> shares_link

- **Evidence grades:** 4 -> 2

- **Edge provenance:** ground-truth -> distractor

- **Evidence snippets:** Synthetic record: Funder_002 is listed as providing funding to Intermediary_002 during Phase_01. || Synthetic record: Intermediary_002 and Campaign_010 shared the same abstract link during Phase_02.

- **Review-priority score:** 58.7 (threshold 60.0) -> not flagged

- **Ground-truth label:** not seeded

- **Why:** not high priority: raw score 58.70 is below threshold 60.0: includes a direct synthetic funding edge (grade 4); weakest hop grade 2, mean grade 3.00; drops to a grade-2 shared-link/amplification hop.

- **Recommended action:** No review action required; retain in the audit log for completeness.

### CAND_0062 (true_negative)

- **Node sequence:** Funder_007 -> Intermediary_007 -> Campaign_020

- **Edge sequence:** funds -> shares_link

- **Evidence grades:** 4 -> 2

- **Edge provenance:** ground-truth -> distractor

- **Evidence snippets:** Synthetic record: Funder_007 is listed as providing funding to Intermediary_007 during Phase_01. || Synthetic record: Intermediary_007 and Campaign_020 shared the same abstract link during Phase_03.

- **Review-priority score:** 58.7 (threshold 60.0) -> not flagged

- **Ground-truth label:** not seeded

- **Why:** not high priority: raw score 58.70 is below threshold 60.0: includes a direct synthetic funding edge (grade 4); weakest hop grade 2, mean grade 3.00; drops to a grade-2 shared-link/amplification hop.

- **Recommended action:** No review action required; retain in the audit log for completeness.

### CAND_0067 (true_negative)

- **Node sequence:** Funder_008 -> Intermediary_008 -> Campaign_022

- **Edge sequence:** funds -> shares_link

- **Evidence grades:** 4 -> 2

- **Edge provenance:** ground-truth -> distractor

- **Evidence snippets:** Synthetic record: Funder_008 is listed as providing funding to Intermediary_008 during Phase_01. || Synthetic record: Intermediary_008 and Campaign_022 shared the same abstract link during Phase_04.

- **Review-priority score:** 58.7 (threshold 60.0) -> not flagged

- **Ground-truth label:** not seeded

- **Why:** not high priority: raw score 58.70 is below threshold 60.0: includes a direct synthetic funding edge (grade 4); weakest hop grade 2, mean grade 3.00; drops to a grade-2 shared-link/amplification hop.

- **Recommended action:** No review action required; retain in the audit log for completeness.

### CAND_0051 (true_negative)

- **Node sequence:** Funder_006 -> Intermediary_006 -> Campaign_018

- **Edge sequence:** funds -> shares_link

- **Evidence grades:** 4 -> 2

- **Edge provenance:** ground-truth -> distractor

- **Evidence snippets:** Synthetic record: Funder_006 is listed as providing funding to Intermediary_006 during Phase_01. || Synthetic record: Intermediary_006 and Campaign_018 shared the same abstract link during Phase_02.

- **Review-priority score:** 58.7 (threshold 60.0) -> not flagged

- **Ground-truth label:** not seeded

- **Why:** not high priority: raw score 58.70 is below threshold 60.0: includes a direct synthetic funding edge (grade 4); weakest hop grade 2, mean grade 3.00; drops to a grade-2 shared-link/amplification hop.

- **Recommended action:** No review action required; retain in the audit log for completeness.

### CAND_0038 (true_negative)

- **Node sequence:** Funder_004 -> Intermediary_004 -> Campaign_014

- **Edge sequence:** funds -> shares_link

- **Evidence grades:** 4 -> 2

- **Edge provenance:** ground-truth -> distractor

- **Evidence snippets:** Synthetic record: Funder_004 is listed as providing funding to Intermediary_004 during Phase_01. || Synthetic record: Intermediary_004 and Campaign_014 shared the same abstract link during Phase_04.

- **Review-priority score:** 58.7 (threshold 60.0) -> not flagged

- **Ground-truth label:** not seeded

- **Why:** not high priority: raw score 58.70 is below threshold 60.0: includes a direct synthetic funding edge (grade 4); weakest hop grade 2, mean grade 3.00; drops to a grade-2 shared-link/amplification hop.

- **Recommended action:** No review action required; retain in the audit log for completeness.

### CAND_0064 (true_negative)

- **Node sequence:** Funder_007 -> Intermediary_007 -> Campaign_016

- **Edge sequence:** funds -> co_occurs_with

- **Evidence grades:** 4 -> 1

- **Edge provenance:** ground-truth -> distractor

- **Evidence snippets:** Synthetic record: Funder_007 is listed as providing funding to Intermediary_007 during Phase_01. || Synthetic record: Intermediary_007 and Campaign_016 co-occurred in one abstract index during Phase_01.

- **Review-priority score:** 53.95 (threshold 60.0) -> not flagged

- **Ground-truth label:** not seeded

- **Why:** not high priority: raw score 53.95 is below threshold 60.0: includes a direct synthetic funding edge (grade 4); weakest hop grade 1, mean grade 2.50; drops to a grade-0/1 hop and is ineligible for high-priority review.

- **Recommended action:** No review action required; retain in the audit log for completeness.

### CAND_0028 (true_negative)

- **Node sequence:** Funder_003 -> Intermediary_003 -> Campaign_008

- **Edge sequence:** funds -> co_occurs_with

- **Evidence grades:** 4 -> 1

- **Edge provenance:** ground-truth -> distractor

- **Evidence snippets:** Synthetic record: Funder_003 is listed as providing funding to Intermediary_003 during Phase_01. || Synthetic record: Intermediary_003 and Campaign_008 co-occurred in one abstract index during Phase_01.

- **Review-priority score:** 53.95 (threshold 60.0) -> not flagged

- **Ground-truth label:** not seeded

- **Why:** not high priority: raw score 53.95 is below threshold 60.0: includes a direct synthetic funding edge (grade 4); weakest hop grade 1, mean grade 2.50; drops to a grade-0/1 hop and is ineligible for high-priority review.

- **Recommended action:** No review action required; retain in the audit log for completeness.

### CAND_0079 (true_negative)

- **Node sequence:** Funder_011 -> Intermediary_011 -> EmbeddedControl_12 -> Campaign_EC12

- **Edge sequence:** funds -> co_occurs_with -> shares_link

- **Evidence grades:** 4 -> 1 -> 2

- **Edge provenance:** ground-truth -> negative-control -> negative-control

- **Evidence snippets:** Synthetic record: Funder_011 is listed as providing funding to Intermediary_011 during Phase_01. || Synthetic record: Intermediary_011 and EmbeddedControl_12 co-occurred in one abstract index during Phase_02. || Synthetic record: EmbeddedControl_12 and Campaign_EC12 shared the same abstract link during Phase_03.

- **Review-priority score:** 51.3 (threshold 60.0) -> not flagged

- **Ground-truth label:** not seeded

- **Why:** not high priority: raw score 51.30 is below threshold 60.0: includes a direct synthetic funding edge (grade 4); weakest hop grade 1, mean grade 2.33; drops to a grade-0/1 hop and is ineligible for high-priority review; passes through an embedded control actor connected only by weak co-occurrence.

- **Recommended action:** No review action required; retain in the audit log for completeness.

### CAND_0026 (true_negative)

- **Node sequence:** Funder_003 -> Intermediary_003 -> EmbeddedControl_04 -> Campaign_EC04

- **Edge sequence:** funds -> co_occurs_with -> shares_link

- **Evidence grades:** 4 -> 1 -> 2

- **Edge provenance:** ground-truth -> negative-control -> negative-control

- **Evidence snippets:** Synthetic record: Funder_003 is listed as providing funding to Intermediary_003 during Phase_01. || Synthetic record: Intermediary_003 and EmbeddedControl_04 co-occurred in one abstract index during Phase_02. || Synthetic record: EmbeddedControl_04 and Campaign_EC04 shared the same abstract link during Phase_03.

- **Review-priority score:** 51.3 (threshold 60.0) -> not flagged

- **Ground-truth label:** not seeded

- **Why:** not high priority: raw score 51.30 is below threshold 60.0: includes a direct synthetic funding edge (grade 4); weakest hop grade 1, mean grade 2.33; drops to a grade-0/1 hop and is ineligible for high-priority review; passes through an embedded control actor connected only by weak co-occurrence.

- **Recommended action:** No review action required; retain in the audit log for completeness.

### CAND_0041 (true_negative)

- **Node sequence:** Funder_005 -> Intermediary_005 -> EmbeddedControl_06 -> Campaign_EC06

- **Edge sequence:** funds -> co_occurs_with -> shares_link

- **Evidence grades:** 4 -> 1 -> 2

- **Edge provenance:** ground-truth -> negative-control -> negative-control

- **Evidence snippets:** Synthetic record: Funder_005 is listed as providing funding to Intermediary_005 during Phase_01. || Synthetic record: Intermediary_005 and EmbeddedControl_06 co-occurred in one abstract index during Phase_02. || Synthetic record: EmbeddedControl_06 and Campaign_EC06 shared the same abstract link during Phase_03.

- **Review-priority score:** 51.3 (threshold 60.0) -> not flagged

- **Ground-truth label:** not seeded

- **Why:** not high priority: raw score 51.30 is below threshold 60.0: includes a direct synthetic funding edge (grade 4); weakest hop grade 1, mean grade 2.33; drops to a grade-0/1 hop and is ineligible for high-priority review; passes through an embedded control actor connected only by weak co-occurrence.

- **Recommended action:** No review action required; retain in the audit log for completeness.

### CAND_0063 (true_negative)

- **Node sequence:** Funder_007 -> Intermediary_007 -> EmbeddedControl_08 -> Campaign_EC08

- **Edge sequence:** funds -> co_occurs_with -> shares_link

- **Evidence grades:** 4 -> 1 -> 2

- **Edge provenance:** ground-truth -> negative-control -> negative-control

- **Evidence snippets:** Synthetic record: Funder_007 is listed as providing funding to Intermediary_007 during Phase_01. || Synthetic record: Intermediary_007 and EmbeddedControl_08 co-occurred in one abstract index during Phase_02. || Synthetic record: EmbeddedControl_08 and Campaign_EC08 shared the same abstract link during Phase_03.

- **Review-priority score:** 51.3 (threshold 60.0) -> not flagged

- **Ground-truth label:** not seeded

- **Why:** not high priority: raw score 51.30 is below threshold 60.0: includes a direct synthetic funding edge (grade 4); weakest hop grade 1, mean grade 2.33; drops to a grade-0/1 hop and is ineligible for high-priority review; passes through an embedded control actor connected only by weak co-occurrence.

- **Recommended action:** No review action required; retain in the audit log for completeness.

### CAND_0013 (true_negative)

- **Node sequence:** Funder_001 -> Intermediary_001 -> EmbeddedControl_02 -> Campaign_EC02

- **Edge sequence:** funds -> co_occurs_with -> shares_link

- **Evidence grades:** 4 -> 1 -> 2

- **Edge provenance:** ground-truth -> negative-control -> negative-control

- **Evidence snippets:** Synthetic record: Funder_001 is listed as providing funding to Intermediary_001 during Phase_01. || Synthetic record: Intermediary_001 and EmbeddedControl_02 co-occurred in one abstract index during Phase_02. || Synthetic record: EmbeddedControl_02 and Campaign_EC02 shared the same abstract link during Phase_03.

- **Review-priority score:** 51.3 (threshold 60.0) -> not flagged

- **Ground-truth label:** not seeded

- **Why:** not high priority: raw score 51.30 is below threshold 60.0: includes a direct synthetic funding edge (grade 4); weakest hop grade 1, mean grade 2.33; drops to a grade-0/1 hop and is ineligible for high-priority review; passes through an embedded control actor connected only by weak co-occurrence.

- **Recommended action:** No review action required; retain in the audit log for completeness.

### CAND_0074 (true_negative)

- **Node sequence:** Funder_009 -> Intermediary_009 -> EmbeddedControl_10 -> Campaign_EC10

- **Edge sequence:** funds -> co_occurs_with -> shares_link

- **Evidence grades:** 4 -> 1 -> 2

- **Edge provenance:** ground-truth -> negative-control -> negative-control

- **Evidence snippets:** Synthetic record: Funder_009 is listed as providing funding to Intermediary_009 during Phase_01. || Synthetic record: Intermediary_009 and EmbeddedControl_10 co-occurred in one abstract index during Phase_02. || Synthetic record: EmbeddedControl_10 and Campaign_EC10 shared the same abstract link during Phase_03.

- **Review-priority score:** 51.3 (threshold 60.0) -> not flagged

- **Ground-truth label:** not seeded

- **Why:** not high priority: raw score 51.30 is below threshold 60.0: includes a direct synthetic funding edge (grade 4); weakest hop grade 1, mean grade 2.33; drops to a grade-0/1 hop and is ineligible for high-priority review; passes through an embedded control actor connected only by weak co-occurrence.

- **Recommended action:** No review action required; retain in the audit log for completeness.

### CAND_0107 (true_negative)

- **Node sequence:** Funder_L012 -> Intermediary_L012 -> Report_L012

- **Edge sequence:** funds -> co_occurs_with

- **Evidence grades:** 4 -> 1

- **Edge provenance:** distractor -> distractor

- **Evidence snippets:** Synthetic record: Funder_L012 is listed as providing funding to Intermediary_L012 during Phase_01. || Synthetic record: Intermediary_L012 and Report_L012 co-occurred in one abstract index during Phase_02.

- **Review-priority score:** 50.95 (threshold 60.0) -> not flagged

- **Ground-truth label:** not seeded

- **Why:** not high priority: raw score 50.95 is below threshold 60.0: includes a direct synthetic funding edge (grade 4); weakest hop grade 1, mean grade 2.50; drops to a grade-0/1 hop and is ineligible for high-priority review.

- **Recommended action:** No review action required; retain in the audit log for completeness.

### CAND_0109 (true_negative)

- **Node sequence:** Funder_L014 -> Intermediary_L014 -> Report_L014

- **Edge sequence:** funds -> co_occurs_with

- **Evidence grades:** 4 -> 1

- **Edge provenance:** distractor -> distractor

- **Evidence snippets:** Synthetic record: Funder_L014 is listed as providing funding to Intermediary_L014 during Phase_01. || Synthetic record: Intermediary_L014 and Report_L014 co-occurred in one abstract index during Phase_02.

- **Review-priority score:** 50.95 (threshold 60.0) -> not flagged

- **Ground-truth label:** not seeded

- **Why:** not high priority: raw score 50.95 is below threshold 60.0: includes a direct synthetic funding edge (grade 4); weakest hop grade 1, mean grade 2.50; drops to a grade-0/1 hop and is ineligible for high-priority review.

- **Recommended action:** No review action required; retain in the audit log for completeness.

### CAND_0097 (true_negative)

- **Node sequence:** Funder_L002 -> Intermediary_L002 -> Report_L002

- **Edge sequence:** funds -> co_occurs_with

- **Evidence grades:** 4 -> 1

- **Edge provenance:** distractor -> distractor

- **Evidence snippets:** Synthetic record: Funder_L002 is listed as providing funding to Intermediary_L002 during Phase_01. || Synthetic record: Intermediary_L002 and Report_L002 co-occurred in one abstract index during Phase_02.

- **Review-priority score:** 50.95 (threshold 60.0) -> not flagged

- **Ground-truth label:** not seeded

- **Why:** not high priority: raw score 50.95 is below threshold 60.0: includes a direct synthetic funding edge (grade 4); weakest hop grade 1, mean grade 2.50; drops to a grade-0/1 hop and is ineligible for high-priority review.

- **Recommended action:** No review action required; retain in the audit log for completeness.

### CAND_0105 (true_negative)

- **Node sequence:** Funder_L010 -> Intermediary_L010 -> Report_L010

- **Edge sequence:** funds -> co_occurs_with

- **Evidence grades:** 4 -> 1

- **Edge provenance:** distractor -> distractor

- **Evidence snippets:** Synthetic record: Funder_L010 is listed as providing funding to Intermediary_L010 during Phase_01. || Synthetic record: Intermediary_L010 and Report_L010 co-occurred in one abstract index during Phase_02.

- **Review-priority score:** 50.95 (threshold 60.0) -> not flagged

- **Ground-truth label:** not seeded

- **Why:** not high priority: raw score 50.95 is below threshold 60.0: includes a direct synthetic funding edge (grade 4); weakest hop grade 1, mean grade 2.50; drops to a grade-0/1 hop and is ineligible for high-priority review.

- **Recommended action:** No review action required; retain in the audit log for completeness.

### CAND_0040 (true_negative)

- **Node sequence:** Funder_004 -> Intermediary_004 -> Campaign_010

- **Edge sequence:** funds -> co_occurs_with

- **Evidence grades:** 4 -> 1

- **Edge provenance:** ground-truth -> distractor

- **Evidence snippets:** Synthetic record: Funder_004 is listed as providing funding to Intermediary_004 during Phase_01. || Synthetic record: Intermediary_004 and Campaign_010 co-occurred in one abstract index during Phase_02.

- **Review-priority score:** 50.95 (threshold 60.0) -> not flagged

- **Ground-truth label:** not seeded

- **Why:** not high priority: raw score 50.95 is below threshold 60.0: includes a direct synthetic funding edge (grade 4); weakest hop grade 1, mean grade 2.50; drops to a grade-0/1 hop and is ineligible for high-priority review.

- **Recommended action:** No review action required; retain in the audit log for completeness.

### CAND_0011 (true_negative)

- **Node sequence:** Funder_001 -> Intermediary_001 -> Campaign_004

- **Edge sequence:** funds -> co_occurs_with

- **Evidence grades:** 4 -> 1

- **Edge provenance:** ground-truth -> distractor

- **Evidence snippets:** Synthetic record: Funder_001 is listed as providing funding to Intermediary_001 during Phase_01. || Synthetic record: Intermediary_001 and Campaign_004 co-occurred in one abstract index during Phase_03.

- **Review-priority score:** 50.95 (threshold 60.0) -> not flagged

- **Ground-truth label:** not seeded

- **Why:** not high priority: raw score 50.95 is below threshold 60.0: includes a direct synthetic funding edge (grade 4); weakest hop grade 1, mean grade 2.50; drops to a grade-0/1 hop and is ineligible for high-priority review.

- **Recommended action:** No review action required; retain in the audit log for completeness.

### CAND_0042 (true_negative)

- **Node sequence:** Funder_005 -> Intermediary_005 -> Campaign_012

- **Edge sequence:** funds -> co_occurs_with

- **Evidence grades:** 4 -> 1

- **Edge provenance:** ground-truth -> distractor

- **Evidence snippets:** Synthetic record: Funder_005 is listed as providing funding to Intermediary_005 during Phase_01. || Synthetic record: Intermediary_005 and Campaign_012 co-occurred in one abstract index during Phase_03.

- **Review-priority score:** 50.95 (threshold 60.0) -> not flagged

- **Ground-truth label:** not seeded

- **Why:** not high priority: raw score 50.95 is below threshold 60.0: includes a direct synthetic funding edge (grade 4); weakest hop grade 1, mean grade 2.50; drops to a grade-0/1 hop and is ineligible for high-priority review.

- **Recommended action:** No review action required; retain in the audit log for completeness.

### CAND_0052 (true_negative)

- **Node sequence:** Funder_006 -> Intermediary_006 -> Campaign_014

- **Edge sequence:** funds -> co_occurs_with

- **Evidence grades:** 4 -> 1

- **Edge provenance:** ground-truth -> distractor

- **Evidence snippets:** Synthetic record: Funder_006 is listed as providing funding to Intermediary_006 during Phase_01. || Synthetic record: Intermediary_006 and Campaign_014 co-occurred in one abstract index during Phase_04.

- **Review-priority score:** 50.95 (threshold 60.0) -> not flagged

- **Ground-truth label:** not seeded

- **Why:** not high priority: raw score 50.95 is below threshold 60.0: includes a direct synthetic funding edge (grade 4); weakest hop grade 1, mean grade 2.50; drops to a grade-0/1 hop and is ineligible for high-priority review.

- **Recommended action:** No review action required; retain in the audit log for completeness.

### CAND_0021 (true_negative)

- **Node sequence:** Funder_002 -> Intermediary_002 -> Campaign_006

- **Edge sequence:** funds -> co_occurs_with

- **Evidence grades:** 4 -> 1

- **Edge provenance:** ground-truth -> distractor

- **Evidence snippets:** Synthetic record: Funder_002 is listed as providing funding to Intermediary_002 during Phase_01. || Synthetic record: Intermediary_002 and Campaign_006 co-occurred in one abstract index during Phase_04.

- **Review-priority score:** 50.95 (threshold 60.0) -> not flagged

- **Ground-truth label:** not seeded

- **Why:** not high priority: raw score 50.95 is below threshold 60.0: includes a direct synthetic funding edge (grade 4); weakest hop grade 1, mean grade 2.50; drops to a grade-0/1 hop and is ineligible for high-priority review.

- **Recommended action:** No review action required; retain in the audit log for completeness.

### CAND_0001 (true_negative)

- **Node sequence:** Funder_000 -> Intermediary_000 -> Campaign_002

- **Edge sequence:** funds -> co_occurs_with

- **Evidence grades:** 4 -> 1

- **Edge provenance:** ground-truth -> distractor

- **Evidence snippets:** Synthetic record: Funder_000 is listed as providing funding to Intermediary_000 during Phase_01. || Synthetic record: Intermediary_000 and Campaign_002 co-occurred in one abstract index during Phase_02.

- **Review-priority score:** 50.95 (threshold 60.0) -> not flagged

- **Ground-truth label:** not seeded

- **Why:** not high priority: raw score 50.95 is below threshold 60.0: includes a direct synthetic funding edge (grade 4); weakest hop grade 1, mean grade 2.50; drops to a grade-0/1 hop and is ineligible for high-priority review.

- **Recommended action:** No review action required; retain in the audit log for completeness.

### CAND_0069 (true_negative)

- **Node sequence:** Funder_008 -> Intermediary_008 -> Campaign_018

- **Edge sequence:** funds -> co_occurs_with

- **Evidence grades:** 4 -> 1

- **Edge provenance:** ground-truth -> distractor

- **Evidence snippets:** Synthetic record: Funder_008 is listed as providing funding to Intermediary_008 during Phase_01. || Synthetic record: Intermediary_008 and Campaign_018 co-occurred in one abstract index during Phase_02.

- **Review-priority score:** 50.95 (threshold 60.0) -> not flagged

- **Ground-truth label:** not seeded

- **Why:** not high priority: raw score 50.95 is below threshold 60.0: includes a direct synthetic funding edge (grade 4); weakest hop grade 1, mean grade 2.50; drops to a grade-0/1 hop and is ineligible for high-priority review.

- **Recommended action:** No review action required; retain in the audit log for completeness.

### CAND_0073 (true_negative)

- **Node sequence:** Funder_009 -> Intermediary_009 -> Campaign_020

- **Edge sequence:** funds -> co_occurs_with

- **Evidence grades:** 4 -> 1

- **Edge provenance:** ground-truth -> distractor

- **Evidence snippets:** Synthetic record: Funder_009 is listed as providing funding to Intermediary_009 during Phase_01. || Synthetic record: Intermediary_009 and Campaign_020 co-occurred in one abstract index during Phase_03.

- **Review-priority score:** 50.95 (threshold 60.0) -> not flagged

- **Ground-truth label:** not seeded

- **Why:** not high priority: raw score 50.95 is below threshold 60.0: includes a direct synthetic funding edge (grade 4); weakest hop grade 1, mean grade 2.50; drops to a grade-0/1 hop and is ineligible for high-priority review.

- **Recommended action:** No review action required; retain in the audit log for completeness.

### CAND_0103 (true_negative)

- **Node sequence:** Funder_L008 -> Intermediary_L008 -> Report_L008

- **Edge sequence:** funds -> co_occurs_with

- **Evidence grades:** 4 -> 1

- **Edge provenance:** distractor -> distractor

- **Evidence snippets:** Synthetic record: Funder_L008 is listed as providing funding to Intermediary_L008 during Phase_01. || Synthetic record: Intermediary_L008 and Report_L008 co-occurred in one abstract index during Phase_02.

- **Review-priority score:** 50.95 (threshold 60.0) -> not flagged

- **Ground-truth label:** not seeded

- **Why:** not high priority: raw score 50.95 is below threshold 60.0: includes a direct synthetic funding edge (grade 4); weakest hop grade 1, mean grade 2.50; drops to a grade-0/1 hop and is ineligible for high-priority review.

- **Recommended action:** No review action required; retain in the audit log for completeness.

### CAND_0101 (true_negative)

- **Node sequence:** Funder_L006 -> Intermediary_L006 -> Report_L006

- **Edge sequence:** funds -> co_occurs_with

- **Evidence grades:** 4 -> 1

- **Edge provenance:** distractor -> distractor

- **Evidence snippets:** Synthetic record: Funder_L006 is listed as providing funding to Intermediary_L006 during Phase_01. || Synthetic record: Intermediary_L006 and Report_L006 co-occurred in one abstract index during Phase_02.

- **Review-priority score:** 50.95 (threshold 60.0) -> not flagged

- **Ground-truth label:** not seeded

- **Why:** not high priority: raw score 50.95 is below threshold 60.0: includes a direct synthetic funding edge (grade 4); weakest hop grade 1, mean grade 2.50; drops to a grade-0/1 hop and is ineligible for high-priority review.

- **Recommended action:** No review action required; retain in the audit log for completeness.

### CAND_0099 (true_negative)

- **Node sequence:** Funder_L004 -> Intermediary_L004 -> Report_L004

- **Edge sequence:** funds -> co_occurs_with

- **Evidence grades:** 4 -> 1

- **Edge provenance:** distractor -> distractor

- **Evidence snippets:** Synthetic record: Funder_L004 is listed as providing funding to Intermediary_L004 during Phase_01. || Synthetic record: Intermediary_L004 and Report_L004 co-occurred in one abstract index during Phase_02.

- **Review-priority score:** 50.95 (threshold 60.0) -> not flagged

- **Ground-truth label:** not seeded

- **Why:** not high priority: raw score 50.95 is below threshold 60.0: includes a direct synthetic funding edge (grade 4); weakest hop grade 1, mean grade 2.50; drops to a grade-0/1 hop and is ineligible for high-priority review.

- **Recommended action:** No review action required; retain in the audit log for completeness.

### CAND_0095 (true_negative)

- **Node sequence:** Funder_L000 -> Intermediary_L000 -> Report_L000

- **Edge sequence:** funds -> co_occurs_with

- **Evidence grades:** 4 -> 1

- **Edge provenance:** distractor -> distractor

- **Evidence snippets:** Synthetic record: Funder_L000 is listed as providing funding to Intermediary_L000 during Phase_01. || Synthetic record: Intermediary_L000 and Report_L000 co-occurred in one abstract index during Phase_02.

- **Review-priority score:** 50.95 (threshold 60.0) -> not flagged

- **Ground-truth label:** not seeded

- **Why:** not high priority: raw score 50.95 is below threshold 60.0: includes a direct synthetic funding edge (grade 4); weakest hop grade 1, mean grade 2.50; drops to a grade-0/1 hop and is ineligible for high-priority review.

- **Recommended action:** No review action required; retain in the audit log for completeness.

### CAND_0053 (true_negative)

- **Node sequence:** Funder_006 -> Intermediary_006 -> EmbeddedControl_07 -> Report_EC07

- **Edge sequence:** funds -> co_occurs_with -> co_occurs_with

- **Evidence grades:** 4 -> 1 -> 1

- **Edge provenance:** ground-truth -> negative-control -> negative-control

- **Evidence snippets:** Synthetic record: Funder_006 is listed as providing funding to Intermediary_006 during Phase_01. || Synthetic record: Intermediary_006 and EmbeddedControl_07 co-occurred in one abstract index during Phase_02. || Synthetic record: EmbeddedControl_07 and Report_EC07 co-occurred in one abstract index during Phase_03.

- **Review-priority score:** 47.2 (threshold 60.0) -> not flagged

- **Ground-truth label:** not seeded

- **Why:** not high priority: raw score 47.20 is below threshold 60.0: includes a direct synthetic funding edge (grade 4); weakest hop grade 1, mean grade 2.00; drops to a grade-0/1 hop and is ineligible for high-priority review; passes through an embedded control actor connected only by weak co-occurrence.

- **Recommended action:** No review action required; retain in the audit log for completeness.

### CAND_0036 (true_negative)

- **Node sequence:** Funder_004 -> Intermediary_004 -> EmbeddedControl_05 -> Report_EC05

- **Edge sequence:** funds -> co_occurs_with -> co_occurs_with

- **Evidence grades:** 4 -> 1 -> 1

- **Edge provenance:** ground-truth -> negative-control -> negative-control

- **Evidence snippets:** Synthetic record: Funder_004 is listed as providing funding to Intermediary_004 during Phase_01. || Synthetic record: Intermediary_004 and EmbeddedControl_05 co-occurred in one abstract index during Phase_02. || Synthetic record: EmbeddedControl_05 and Report_EC05 co-occurred in one abstract index during Phase_03.

- **Review-priority score:** 47.2 (threshold 60.0) -> not flagged

- **Ground-truth label:** not seeded

- **Why:** not high priority: raw score 47.20 is below threshold 60.0: includes a direct synthetic funding edge (grade 4); weakest hop grade 1, mean grade 2.00; drops to a grade-0/1 hop and is ineligible for high-priority review; passes through an embedded control actor connected only by weak co-occurrence.

- **Recommended action:** No review action required; retain in the audit log for completeness.

### CAND_0007 (true_negative)

- **Node sequence:** Funder_000 -> Intermediary_000 -> EmbeddedControl_01 -> Report_EC01

- **Edge sequence:** funds -> co_occurs_with -> co_occurs_with

- **Evidence grades:** 4 -> 1 -> 1

- **Edge provenance:** ground-truth -> negative-control -> negative-control

- **Evidence snippets:** Synthetic record: Funder_000 is listed as providing funding to Intermediary_000 during Phase_01. || Synthetic record: Intermediary_000 and EmbeddedControl_01 co-occurred in one abstract index during Phase_02. || Synthetic record: EmbeddedControl_01 and Report_EC01 co-occurred in one abstract index during Phase_03.

- **Review-priority score:** 47.2 (threshold 60.0) -> not flagged

- **Ground-truth label:** not seeded

- **Why:** not high priority: raw score 47.20 is below threshold 60.0: includes a direct synthetic funding edge (grade 4); weakest hop grade 1, mean grade 2.00; drops to a grade-0/1 hop and is ineligible for high-priority review; passes through an embedded control actor connected only by weak co-occurrence.

- **Recommended action:** No review action required; retain in the audit log for completeness.

### CAND_0020 (true_negative)

- **Node sequence:** Funder_002 -> Intermediary_002 -> EmbeddedControl_03 -> Report_EC03

- **Edge sequence:** funds -> co_occurs_with -> co_occurs_with

- **Evidence grades:** 4 -> 1 -> 1

- **Edge provenance:** ground-truth -> negative-control -> negative-control

- **Evidence snippets:** Synthetic record: Funder_002 is listed as providing funding to Intermediary_002 during Phase_01. || Synthetic record: Intermediary_002 and EmbeddedControl_03 co-occurred in one abstract index during Phase_02. || Synthetic record: EmbeddedControl_03 and Report_EC03 co-occurred in one abstract index during Phase_03.

- **Review-priority score:** 47.2 (threshold 60.0) -> not flagged

- **Ground-truth label:** not seeded

- **Why:** not high priority: raw score 47.20 is below threshold 60.0: includes a direct synthetic funding edge (grade 4); weakest hop grade 1, mean grade 2.00; drops to a grade-0/1 hop and is ineligible for high-priority review; passes through an embedded control actor connected only by weak co-occurrence.

- **Recommended action:** No review action required; retain in the audit log for completeness.

### CAND_0078 (true_negative)

- **Node sequence:** Funder_010 -> Intermediary_010 -> EmbeddedControl_11 -> Report_EC11

- **Edge sequence:** funds -> co_occurs_with -> co_occurs_with

- **Evidence grades:** 4 -> 1 -> 1

- **Edge provenance:** ground-truth -> negative-control -> negative-control

- **Evidence snippets:** Synthetic record: Funder_010 is listed as providing funding to Intermediary_010 during Phase_01. || Synthetic record: Intermediary_010 and EmbeddedControl_11 co-occurred in one abstract index during Phase_02. || Synthetic record: EmbeddedControl_11 and Report_EC11 co-occurred in one abstract index during Phase_03.

- **Review-priority score:** 47.2 (threshold 60.0) -> not flagged

- **Ground-truth label:** not seeded

- **Why:** not high priority: raw score 47.20 is below threshold 60.0: includes a direct synthetic funding edge (grade 4); weakest hop grade 1, mean grade 2.00; drops to a grade-0/1 hop and is ineligible for high-priority review; passes through an embedded control actor connected only by weak co-occurrence.

- **Recommended action:** No review action required; retain in the audit log for completeness.

### CAND_0068 (true_negative)

- **Node sequence:** Funder_008 -> Intermediary_008 -> EmbeddedControl_09 -> Report_EC09

- **Edge sequence:** funds -> co_occurs_with -> co_occurs_with

- **Evidence grades:** 4 -> 1 -> 1

- **Edge provenance:** ground-truth -> negative-control -> negative-control

- **Evidence snippets:** Synthetic record: Funder_008 is listed as providing funding to Intermediary_008 during Phase_01. || Synthetic record: Intermediary_008 and EmbeddedControl_09 co-occurred in one abstract index during Phase_02. || Synthetic record: EmbeddedControl_09 and Report_EC09 co-occurred in one abstract index during Phase_03.

- **Review-priority score:** 47.2 (threshold 60.0) -> not flagged

- **Ground-truth label:** not seeded

- **Why:** not high priority: raw score 47.20 is below threshold 60.0: includes a direct synthetic funding edge (grade 4); weakest hop grade 1, mean grade 2.00; drops to a grade-0/1 hop and is ineligible for high-priority review; passes through an embedded control actor connected only by weak co-occurrence.

- **Recommended action:** No review action required; retain in the audit log for completeness.

### CAND_0112 (true_negative)

- **Node sequence:** Funder_W02 -> SocialAccount_WC02 -> MediaOutlet_WC02 -> Campaign_WC02

- **Edge sequence:** shares_link -> amplifies -> uses_similar_language

- **Evidence grades:** 2 -> 2 -> 2

- **Edge provenance:** distractor -> distractor -> distractor

- **Evidence snippets:** Synthetic record: Funder_W02 and SocialAccount_WC02 shared the same abstract link during Phase_01. || Synthetic record: SocialAccount_WC02 repeatedly amplified output attributed to MediaOutlet_WC02 during Phase_01. || Synthetic record: MediaOutlet_WC02 used wording closely similar to Campaign_WC02 during Phase_01.

- **Review-priority score:** 38.3 (threshold 60.0) -> not flagged

- **Ground-truth label:** not seeded

- **Why:** not high priority: raw score 38.30 is below threshold 60.0: no direct funding edge; weakest hop grade 2, mean grade 2.00; drops to a grade-2 shared-link/amplification hop; weak-signal-only chain (RQ5): no documentary hop anywhere.

- **Recommended action:** No review action required; retain in the audit log for completeness.

### CAND_0114 (true_negative)

- **Node sequence:** Funder_W04 -> SocialAccount_WC04 -> MediaOutlet_WC04 -> Campaign_WC04

- **Edge sequence:** shares_link -> amplifies -> uses_similar_language

- **Evidence grades:** 2 -> 2 -> 2

- **Edge provenance:** distractor -> distractor -> distractor

- **Evidence snippets:** Synthetic record: Funder_W04 and SocialAccount_WC04 shared the same abstract link during Phase_01. || Synthetic record: SocialAccount_WC04 repeatedly amplified output attributed to MediaOutlet_WC04 during Phase_01. || Synthetic record: MediaOutlet_WC04 used wording closely similar to Campaign_WC04 during Phase_01.

- **Review-priority score:** 38.3 (threshold 60.0) -> not flagged

- **Ground-truth label:** not seeded

- **Why:** not high priority: raw score 38.30 is below threshold 60.0: no direct funding edge; weakest hop grade 2, mean grade 2.00; drops to a grade-2 shared-link/amplification hop; weak-signal-only chain (RQ5): no documentary hop anywhere.

- **Recommended action:** No review action required; retain in the audit log for completeness.

### CAND_0120 (true_negative)

- **Node sequence:** Funder_W10 -> SocialAccount_WC10 -> MediaOutlet_WC10 -> Campaign_WC10

- **Edge sequence:** shares_link -> amplifies -> uses_similar_language

- **Evidence grades:** 2 -> 2 -> 2

- **Edge provenance:** distractor -> distractor -> distractor

- **Evidence snippets:** Synthetic record: Funder_W10 and SocialAccount_WC10 shared the same abstract link during Phase_01. || Synthetic record: SocialAccount_WC10 repeatedly amplified output attributed to MediaOutlet_WC10 during Phase_01. || Synthetic record: MediaOutlet_WC10 used wording closely similar to Campaign_WC10 during Phase_01.

- **Review-priority score:** 38.3 (threshold 60.0) -> not flagged

- **Ground-truth label:** not seeded

- **Why:** not high priority: raw score 38.30 is below threshold 60.0: no direct funding edge; weakest hop grade 2, mean grade 2.00; drops to a grade-2 shared-link/amplification hop; weak-signal-only chain (RQ5): no documentary hop anywhere.

- **Recommended action:** No review action required; retain in the audit log for completeness.

### CAND_0116 (true_negative)

- **Node sequence:** Funder_W06 -> SocialAccount_WC06 -> MediaOutlet_WC06 -> Campaign_WC06

- **Edge sequence:** shares_link -> amplifies -> uses_similar_language

- **Evidence grades:** 2 -> 2 -> 2

- **Edge provenance:** distractor -> distractor -> distractor

- **Evidence snippets:** Synthetic record: Funder_W06 and SocialAccount_WC06 shared the same abstract link during Phase_01. || Synthetic record: SocialAccount_WC06 repeatedly amplified output attributed to MediaOutlet_WC06 during Phase_01. || Synthetic record: MediaOutlet_WC06 used wording closely similar to Campaign_WC06 during Phase_01.

- **Review-priority score:** 38.3 (threshold 60.0) -> not flagged

- **Ground-truth label:** not seeded

- **Why:** not high priority: raw score 38.30 is below threshold 60.0: no direct funding edge; weakest hop grade 2, mean grade 2.00; drops to a grade-2 shared-link/amplification hop; weak-signal-only chain (RQ5): no documentary hop anywhere.

- **Recommended action:** No review action required; retain in the audit log for completeness.

### CAND_0118 (true_negative)

- **Node sequence:** Funder_W08 -> SocialAccount_WC08 -> MediaOutlet_WC08 -> Campaign_WC08

- **Edge sequence:** shares_link -> amplifies -> uses_similar_language

- **Evidence grades:** 2 -> 2 -> 2

- **Edge provenance:** distractor -> distractor -> distractor

- **Evidence snippets:** Synthetic record: Funder_W08 and SocialAccount_WC08 shared the same abstract link during Phase_01. || Synthetic record: SocialAccount_WC08 repeatedly amplified output attributed to MediaOutlet_WC08 during Phase_01. || Synthetic record: MediaOutlet_WC08 used wording closely similar to Campaign_WC08 during Phase_01.

- **Review-priority score:** 38.3 (threshold 60.0) -> not flagged

- **Ground-truth label:** not seeded

- **Why:** not high priority: raw score 38.30 is below threshold 60.0: no direct funding edge; weakest hop grade 2, mean grade 2.00; drops to a grade-2 shared-link/amplification hop; weak-signal-only chain (RQ5): no documentary hop anywhere.

- **Recommended action:** No review action required; retain in the audit log for completeness.

### CAND_0111 (true_negative)

- **Node sequence:** Funder_W01 -> SocialAccount_WC01 -> MediaOutlet_WC01 -> Proxy_WC01 -> Report_WC01

- **Edge sequence:** co_occurs_with -> shares_link -> amplifies -> uses_similar_language

- **Evidence grades:** 1 -> 2 -> 2 -> 2

- **Edge provenance:** distractor -> distractor -> distractor -> distractor

- **Evidence snippets:** Synthetic record: Funder_W01 and SocialAccount_WC01 co-occurred in one abstract index during Phase_01. || Synthetic record: SocialAccount_WC01 and MediaOutlet_WC01 shared the same abstract link during Phase_01. || Synthetic record: MediaOutlet_WC01 repeatedly amplified output attributed to Proxy_WC01 during Phase_02. || Synthetic record: Proxy_WC01 used wording closely similar to Report_WC01 during Phase_02.

- **Review-priority score:** 27.77 (threshold 60.0) -> not flagged

- **Ground-truth label:** not seeded

- **Why:** not high priority: raw score 27.77 is below threshold 60.0: no direct funding edge; weakest hop grade 1, mean grade 1.75; drops to a grade-0/1 hop and is ineligible for high-priority review; weak-signal-only chain (RQ5): no documentary hop anywhere.

- **Recommended action:** No review action required; retain in the audit log for completeness.

### CAND_0115 (true_negative)

- **Node sequence:** Funder_W05 -> SocialAccount_WC05 -> MediaOutlet_WC05 -> Proxy_WC05 -> Report_WC05

- **Edge sequence:** co_occurs_with -> shares_link -> amplifies -> uses_similar_language

- **Evidence grades:** 1 -> 2 -> 2 -> 2

- **Edge provenance:** distractor -> distractor -> distractor -> distractor

- **Evidence snippets:** Synthetic record: Funder_W05 and SocialAccount_WC05 co-occurred in one abstract index during Phase_01. || Synthetic record: SocialAccount_WC05 and MediaOutlet_WC05 shared the same abstract link during Phase_01. || Synthetic record: MediaOutlet_WC05 repeatedly amplified output attributed to Proxy_WC05 during Phase_02. || Synthetic record: Proxy_WC05 used wording closely similar to Report_WC05 during Phase_02.

- **Review-priority score:** 27.77 (threshold 60.0) -> not flagged

- **Ground-truth label:** not seeded

- **Why:** not high priority: raw score 27.77 is below threshold 60.0: no direct funding edge; weakest hop grade 1, mean grade 1.75; drops to a grade-0/1 hop and is ineligible for high-priority review; weak-signal-only chain (RQ5): no documentary hop anywhere.

- **Recommended action:** No review action required; retain in the audit log for completeness.

### CAND_0113 (true_negative)

- **Node sequence:** Funder_W03 -> SocialAccount_WC03 -> MediaOutlet_WC03 -> Proxy_WC03 -> Report_WC03

- **Edge sequence:** co_occurs_with -> shares_link -> amplifies -> uses_similar_language

- **Evidence grades:** 1 -> 2 -> 2 -> 2

- **Edge provenance:** distractor -> distractor -> distractor -> distractor

- **Evidence snippets:** Synthetic record: Funder_W03 and SocialAccount_WC03 co-occurred in one abstract index during Phase_01. || Synthetic record: SocialAccount_WC03 and MediaOutlet_WC03 shared the same abstract link during Phase_01. || Synthetic record: MediaOutlet_WC03 repeatedly amplified output attributed to Proxy_WC03 during Phase_02. || Synthetic record: Proxy_WC03 used wording closely similar to Report_WC03 during Phase_02.

- **Review-priority score:** 27.77 (threshold 60.0) -> not flagged

- **Ground-truth label:** not seeded

- **Why:** not high priority: raw score 27.77 is below threshold 60.0: no direct funding edge; weakest hop grade 1, mean grade 1.75; drops to a grade-0/1 hop and is ineligible for high-priority review; weak-signal-only chain (RQ5): no documentary hop anywhere.

- **Recommended action:** No review action required; retain in the audit log for completeness.

### CAND_0117 (true_negative)

- **Node sequence:** Funder_W07 -> SocialAccount_WC07 -> MediaOutlet_WC07 -> Proxy_WC07 -> Report_WC07

- **Edge sequence:** co_occurs_with -> shares_link -> amplifies -> uses_similar_language

- **Evidence grades:** 1 -> 2 -> 2 -> 2

- **Edge provenance:** distractor -> distractor -> distractor -> distractor

- **Evidence snippets:** Synthetic record: Funder_W07 and SocialAccount_WC07 co-occurred in one abstract index during Phase_01. || Synthetic record: SocialAccount_WC07 and MediaOutlet_WC07 shared the same abstract link during Phase_01. || Synthetic record: MediaOutlet_WC07 repeatedly amplified output attributed to Proxy_WC07 during Phase_02. || Synthetic record: Proxy_WC07 used wording closely similar to Report_WC07 during Phase_02.

- **Review-priority score:** 27.77 (threshold 60.0) -> not flagged

- **Ground-truth label:** not seeded

- **Why:** not high priority: raw score 27.77 is below threshold 60.0: no direct funding edge; weakest hop grade 1, mean grade 1.75; drops to a grade-0/1 hop and is ineligible for high-priority review; weak-signal-only chain (RQ5): no documentary hop anywhere.

- **Recommended action:** No review action required; retain in the audit log for completeness.

### CAND_0119 (true_negative)

- **Node sequence:** Funder_W09 -> SocialAccount_WC09 -> MediaOutlet_WC09 -> Proxy_WC09 -> Report_WC09

- **Edge sequence:** co_occurs_with -> shares_link -> amplifies -> uses_similar_language

- **Evidence grades:** 1 -> 2 -> 2 -> 2

- **Edge provenance:** distractor -> distractor -> distractor -> distractor

- **Evidence snippets:** Synthetic record: Funder_W09 and SocialAccount_WC09 co-occurred in one abstract index during Phase_01. || Synthetic record: SocialAccount_WC09 and MediaOutlet_WC09 shared the same abstract link during Phase_01. || Synthetic record: MediaOutlet_WC09 repeatedly amplified output attributed to Proxy_WC09 during Phase_02. || Synthetic record: Proxy_WC09 used wording closely similar to Report_WC09 during Phase_02.

- **Review-priority score:** 27.77 (threshold 60.0) -> not flagged

- **Ground-truth label:** not seeded

- **Why:** not high priority: raw score 27.77 is below threshold 60.0: no direct funding edge; weakest hop grade 1, mean grade 1.75; drops to a grade-0/1 hop and is ineligible for high-priority review; weak-signal-only chain (RQ5): no documentary hop anywhere.

- **Recommended action:** No review action required; retain in the audit log for completeness.

## 9. Visual validation

![Figure 1. Study design: public signals -> synthetic validation -> human review -> (future) governed pilot.](workflow_diagram.png)

![Figure 2. Full synthetic network (node classes by colour and shape).](synthetic_network_full.png)

![Figure 3. Seeded proxy-path recovery (non-path nodes faded).](synthetic_network_highlighted_paths.png)

![Figure 4. Negative-control subgraphs: isolated and embedded controls.](synthetic_network_negative_controls.png)

![Figure 5. Entity-resolution test (auto-merge / refer / keep-separate).](synthetic_network_entity_resolution.png)

![Figure 6. Review-priority score distribution by group.](triage_score_distribution.png)

![Figure 7. Descriptive score-band truth summary (planted-positive proportion by score bucket).](score_band_truth_summary.png)

![Figure 8. Robustness: threshold sweep and weight-perturbation stability.](robustness_threshold_sweep.png)

## 10. Interpretation statement

This report is a transparent, path-by-path audit trail. The framework is designed to prioritise manual expert review, not to automate accusation or attribution. **All entities and relationships are synthetic and abstract. Outputs are indicators for expert human review only - not proof of misconduct, undisclosed conflicts of interest, hidden funding, or any wrongdoing.**