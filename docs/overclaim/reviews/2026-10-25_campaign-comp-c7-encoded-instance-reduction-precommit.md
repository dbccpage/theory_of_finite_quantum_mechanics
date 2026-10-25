# Review of campaign COMP-C7-ENCODED-INSTANCE-REDUCTION

Scope: branch derive/COMP-C7-ENCODED-INSTANCE-REDUCTION before the pull request, merge base c50dc1b47259. Reviewed against the statements as they stand in this worktree. Rule applied: PROVED_LEAN only if Lean declarations in the repository state the node's full statement and compile with only propext, Classical.choice and Quot.sound.

Method: read the domain record in dag/fragments/unified_dag.json, the synced node in dag/derivation_dag.json, lean4/CampaignCompC7EncodedInstanceReduction.lean, and lean4/GenesisCompUniv.lean lines 300-334. Scanner: python -I -X utf8 scripts/overclaim_scan.py --changed-since origin/main --strict (HIGH 0, MEDIUM 0, LOW 3). The lake build of CampaignCompC7EncodedInstanceReduction exited 0 before this review and is recorded in the campaign receipt. This review pass did not run lake again.

Result: 1 node FULL, 0 NARROWED, 0 OVERCLAIM. This review raises nothing.

Corrections to the PR's own text:
- None. The standing statement is the implication. The Primcodable instance and Computable startWord stay hypotheses.

## Per-node table
| Node | Declarations that discharge it | Verdict | Reason |
|---|---|---|---|
| COMP-C7-ENCODED-INSTANCE-REDUCTION | encoded_instance_reduction (lean4/CampaignCompC7EncodedInstanceReduction.lean:11); reach_problem_not_computable (lean4/GenesisCompUniv.lean:329) | FULL | every atomic claim matched: Primcodable mark type -> the instance binder; Computable startWord -> the hypothesis hc; the word predicate for Rules M0 is not ComputablePred -> the conclusion type. Printed axioms of both declarations are propext, Classical.choice, and Quot.sound. |

## Numbers recomputed
| Where | Claimed | Recomputed (method) | Match |
|---|---|---|---|
| checks/independent/comp-c7-encoded-instance-reduction.py | failures=0; code 0 misses (1, 0); code 1 meets (1, 0) | python -I -X utf8 checks/independent/comp-c7-encoded-instance-reduction.py | match |
| dag/research/campaign_comp-c7-encoded-instance-reduction_lean_replay.json | wall_clock_ms 12420 | lake timing of the successful target build; not an arithmetic identity | unrecomputed timing |

The node statement and the derivation note state no multi-digit count.

## Scanner output
HIGH findings: none. MEDIUM findings: none. LOW findings left in place: R10 on TENSOR-ASSUMPTION-COUNTERMODELS, and R5 on the pre-existing notes for FQ-GAP-TENSOR-UNIQUENESS (20261019) and TENSOR-ASSUMPTION-COUNTERMODELS (1/2, 1/4). No baseline change.

## What the scanner could not decide
Whether "mark type" and "fixed regime" in the English statement are the type Sym G1 (TM1to0.Λ' M1) and the relation Rules M0. The declarations name those objects, and the parent development uses the same names for the fixed regime. The antecedent is not constructed; the statement does not say that it is.
