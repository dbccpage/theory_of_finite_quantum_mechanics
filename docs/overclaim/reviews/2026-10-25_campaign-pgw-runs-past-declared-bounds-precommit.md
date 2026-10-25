# Review of campaign PGW-RUNS-PAST-DECLARED-BOUNDS

Scope: branch derive/PGW-RUNS-PAST-DECLARED-BOUNDS against origin/main at 7fa69d621c27bed7045d0b7fe34bbb1d34b27248. Reviewed against the statements as they stand in this worktree. Rule applied: PROVED_LEAN only if Lean declarations in the repository state the node's full statement and compile with only propext, Classical.choice and Quot.sound.

Method: read the fragment summary, obligation, and fence for TFQ-0501; read lean4/CampaignPgwRunsPastDeclaredBounds.lean through the axiom lines; read the type of `mark_progress` in lean4/Imported/Genesis19l57g1/Derivation/Progress.lean; read checks/independent/pgw-runs-past-declared-bounds.py and dag/derivations/independent/pgw-runs-past-declared-bounds.md. Scanner: `python -I -X utf8 scripts/overclaim_scan.py --changed-since origin/main --strict` (HIGH 0, MEDIUM 0, LOW 3). The lake build of CampaignPgwRunsPastDeclaredBounds exited 0 before this review. Cargo was not rebuilt. The independent check was run with `python -I -X utf8`.

Result: 0 nodes FULL, 1 NARROWED, 0 OVERCLAIM. No node was raised. PGW-RUNS-PAST-DECLARED-BOUNDS stays OPEN.

Corrections to the PR's own text:
- None. The standing statement is five records. The census of stopped runs is not proved.

## Per-node table

| Node | Declarations that discharge it | Verdict | Reason |
|---|---|---|---|
| PGW-RUNS-PAST-DECLARED-BOUNDS | `pgwBoundInside` (lean4/CampaignPgwRunsPastDeclaredBounds.lean:8); `pgwBoundOnLine` (:11); `pgwBoundRoundPast` (:14); `pgwBoundNodePast` (:17); `pgwBoundDataFour` (:20); `pgwBoundItemPast` (:23) | NARROWED | Those five Bool facts state the five records. Printed axioms are empty. `mark_progress` (lean4/Imported/Genesis19l57g1/Derivation/Progress.lean:84) assumes a well-formed regime, two distinct indices below the data count, and separable requirements, and concludes one `validResponse`. It does not state the bound line. The census, leftovers H-2 to H-9, and unboundedness are not proved. Status stays OPEN. |

## Numbers recomputed

| Where | Claimed | Recomputed (method) | Match |
|---|---|---|---|
| Bound line | rounds ≤ 15, nodes ≤ 250, data < 4, items ≤ 2 | `pgwBoundInside` and the same four comparisons in the independent check | Match |
| Record (15, 250, 3, 2) | inside | `pgwBoundOnLine` and the check expect True | Match |
| Record (16, 250, 3, 2) | outside | `pgwBoundRoundPast` and the check expect False | Match |
| Record (15, 251, 3, 2) | outside | `pgwBoundNodePast` and the check expect False | Match |
| Record (15, 250, 4, 2) | outside | `pgwBoundDataFour` and the check expect False | Match |
| Record (15, 250, 3, 3) | outside | `pgwBoundItemPast` and the check expect False | Match |
| Independent check | checked 11 conditions, 0 failures | 1 list length + 5 record comparisons + 1 on-line conjunction + 1 round step + 1 node step + 1 data step + 1 item step = 11 | Match |
| README lean references | 2292 resolve | prior README row 2287 plus these 5 declarations (`mark_progress` was already cited) | Match |
| README lake libraries / roots | 91 / 943 | prior 90 / 942 plus this one `lean_lib` and its one root | Match |
| README derivation papers | 1069 | prior 1068 plus this independent note | Match |
| README lean4 `.lean` files | 1000 | prior 999 plus this module | Match |
| Fragment source quotes | 11266, 368, 116, 970, and the other census figures | not recomputed; they stay in the pre-existing source quotes and are not in the standing statement | Unrecomputed |
| README rows other than the four deltas above | inventory figures written by `scripts/build_readme_facts.py --write` | `scripts/build_readme_facts.py --check` exited 0 on this worktree | Match to that script |

## Scanner output
HIGH 0. MEDIUM 0. LOW 3, none on this node: R10 TENSOR-ASSUMPTION-COUNTERMODELS (lean4/TensorCountermodelCones.lean in no replay receipt); R5 dag/derivations/10_finite_qm_core/tfq_1019_fq_gap_tensor_uniqueness.md (20261019); R5 dag/derivations/27_tensor_composition/tfq_0413_tensor_assumption_countermodels.md (1/2, 1/4). No baseline entry is proposed.

The evidence page grades this node E3. That grade counts files and a matching receipt. It is not a statement-match review, and it is not E4.
