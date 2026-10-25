# Review of campaign PGW-STREAM-AT-FOUR-ITEMS

Scope: branch derive/PGW-STREAM-AT-FOUR-ITEMS against origin/main at 7fa69d621c27bed7045d0b7fe34bbb1d34b27248. Reviewed against the statements as they stand in this worktree. Rule applied: PROVED_LEAN only if Lean declarations in the repository state the node's full statement and compile with only propext, Classical.choice and Quot.sound.

Method: read the fragment summary, obligation, and fence for TFQ-0502; read lean4/CampaignPgwStreamAtFourItems.lean through the axiom lines; read checks/independent/pgw-stream-at-four-items.py and dag/derivations/independent/pgw-stream-at-four-items.md. Scanner: `python -I -X utf8 scripts/overclaim_scan.py --changed-since origin/main --strict` (HIGH 0, MEDIUM 0, LOW 3). The lake build of CampaignPgwStreamAtFourItems exited 0 before this review. Cargo was not rebuilt. The independent check was run with `python -I -X utf8`.

Result: 0 nodes FULL, 1 NARROWED, 0 OVERCLAIM. No node was raised. PGW-STREAM-AT-FOUR-ITEMS stays OPEN.

Corrections to the PR's own text:
- None. The standing statement is one refusal pair and one search flag. The four-item stream computation is not proved.

## Per-node table

| Node | Declarations that discharge it | Verdict | Reason |
|---|---|---|---|
| PGW-STREAM-AT-FOUR-ITEMS | `pgwStreamRefusesAt` (lean4/CampaignPgwStreamAtFourItems.lean:8); `pgwStreamSearched` (:11); `pgwStreamAtThree` (:14); `pgwStreamThreeNotFour` (:17); `pgwStreamFourRefuses` (:20); `pgwStreamFourAccepts` (:23); `pgwStreamShortCircuitSkipsFour` (:26); `pgwStreamOpenSearchReachesFour` (:29); `pgwStreamShortCircuitKeepsThree` (:32) | NARROWED | Those Bool facts state the one reply at item count 3, the two replies at item count 4, and the three search facts. Printed axioms are empty. The retained minima, the refusal census, the guard-stopped frontier, and the four-item stream computation are not proved. Status stays OPEN. |

## Numbers recomputed

| Where | Claimed | Recomputed (method) | Match |
|---|---|---|---|
| Refusal at 3 | item count 3 with the bit set refuses at 3 | `pgwStreamAtThree` and the check's first assertion | Match |
| Same reply at 4 | does not refuse at 4 | `pgwStreamThreeNotFour` and the check | Match |
| Reply at 4, bit set | refuses at 4 | `pgwStreamFourRefuses` and the check | Match |
| Reply at 4, bit clear | does not refuse at 4 | `pgwStreamFourAccepts` and the check | Match |
| Short-circuit | target 4 after refusal at 3 is not searched; target 3 is searched | `pgwStreamShortCircuitSkipsFour`, `pgwStreamShortCircuitKeepsThree`, and the check | Match |
| Flag clear | target 4 is searched | `pgwStreamOpenSearchReachesFour` and the check | Match |
| Independent check | checked 7 conditions, 0 failures | one assertion for each of the seven theorems | Match |
| README lean references | 2294 resolve | prior README row 2287 plus these 7 declarations | Match |
| README lake libraries / roots | 91 / 943 | prior 90 / 942 plus this one `lean_lib` and its one root | Match |
| README derivation papers | 1069 | prior 1068 plus this independent note | Match |
| README lean4 `.lean` files | 1000 | prior 999 plus this module | Match |
| Fragment source quotes | 1039 and the other census figures | not recomputed; they stay in the pre-existing source quotes and are not in the standing statement | Unrecomputed |
| README rows other than the four deltas above | inventory figures written by `scripts/build_readme_facts.py --write` | `scripts/build_readme_facts.py --check` exited 0 on this worktree | Match to that script |

## Scanner output
HIGH 0. MEDIUM 0. LOW 3, none on this node: R10 TENSOR-ASSUMPTION-COUNTERMODELS (lean4/TensorCountermodelCones.lean in no replay receipt); R5 dag/derivations/10_finite_qm_core/tfq_1019_fq_gap_tensor_uniqueness.md (20261019); R5 dag/derivations/27_tensor_composition/tfq_0413_tensor_assumption_countermodels.md (1/2, 1/4). No baseline entry is proposed.

The evidence page grades this node E3. That grade counts files and a matching receipt. It is not a statement-match review, and it is not E4.
