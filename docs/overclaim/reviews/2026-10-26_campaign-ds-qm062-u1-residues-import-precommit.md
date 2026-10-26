# Overclaim review: DS-QM062-U1-RESIDUES-IMPORT

Scope: worktree `C:/gw/derive-ds-qm062`, branch `derive/DS-QM062-U1-RESIDUES-IMPORT`, diff against `origin/main` at `4fea09ae176aae31115e38bb2b21819237055811`. Pre-commit review. This pass did not rebuild the module; the replay receipt records the earlier `lake build`.

## Method

`python -I -X utf8 scripts/overclaim_scan.py --changed-since origin/main --strict` returned HIGH=0, MEDIUM=0, LOW=3. The node statement, bottleneck, and `lean4/CampaignDsQm062U1Residues.lean` were read against the declarations. Numbers were recomputed by integer arithmetic and by `python -I -X utf8 checks/independent/ds-qm062-u1-residues-import.py` (checks=257, failures=0).

## Result

0 FULL, 1 NARROWED, 0 OVERCLAIM. No node was raised.

Continuity, local tomography, field uniqueness, and a U(1) phase fiber are not the statement of any new declaration. Status stays `IMPORTED_ASSUMPTION`. `AuthorityEffect` stays None. The standing statement is the order-4 integer matrix and the remainder identity for every natural number.

## Per-node table

Node: `DS-QM062-U1-RESIDUES-IMPORT`. Verdict: NARROWED.

| Claim | Declaration | Verdict |
| --- | --- | --- |
| for every natural k, (k + 4) % 4 = k % 4 | `alias4` (lean4/CampaignDsQm062U1Residues.lean:34) | matched |
| for every natural k, (k + 1) % 4 = (k % 4 + 1) % 4 | `mod_succ` (same file:53) | matched |
| for every natural k, the k-th right product equals the representative of k % 4 | `pow_rep` (same file:66) | matched |
| that product equals the identity iff k % 4 = 0 | `pow_eye` (same file:89) | matched |
| the product at k + 4 equals the product at k | `pow_period` (same file:93) | matched |
| identity is (1, 0, 0, 1) and J is (0, -1, 1, 0) | `eye_entries` (same file:29), `jay_entries` (same file:30) | matched |
| square is (-1, 0, 0, -1) and cube is (0, 1, -1, 0) | `jay2_entries` (same file:31), `jay3_entries` (same file:32) | matched |
| J times J is the square, that times J is the cube, that times J is the identity | `sq` (same file:46), `cu` (same file:47), `fourth` (same file:48) | matched |
| J, the square, and the cube differ from the identity | `jayNe`, `jay2Ne`, `jay3Ne` (same file:49-51) | matched |
| products at 1, 2, 3, 4 are J, the square, the cube, and the identity | `pow1` through `pow4` (same file:96-99) | matched |
| remainders of 0, 1, 2, 3, 4 are 0, 1, 2, 3, 0 | `rem0` through `rem4` (same file:37-41) | matched |
| 0 * 0 - 1 * 1 = -1 and (-1) * (-1) = 1 | `stepNeg` (same file:43), `stepBack` (same file:44) | matched |
| continuity, local tomography, a U(1) fiber, separation from Q/Z torsion | not proved | left in the bottleneck |

Axioms from the receipt, not rebuilt here: `alias4` and `mod_succ` use `propext`. `rep_step`, `pow_rep`, `rep_eye`, `pow_eye`, and `pow_period` use `propext` and `Quot.sound`. The `decide` and `rfl` declarations use none. No `sorryAx` and no `Classical.choice`.

`rep_step` takes a hypothesis that the residue is below 4. `pow_rep` applies it only to `k % 4`, which `Nat.mod_lt` places below 4. The quantifier on k is every natural number.

## Numbers recomputed

| Where | Claimed | Recomputed | Match |
| --- | --- | --- | --- |
| `sq`, `cu`, `fourth` | products give (-1, 0, 0, -1), (0, 1, -1, 0), (1, 0, 0, 1) | same tuples by the row-column product | yes |
| `stepNeg`, `stepBack` | 0 * 0 - 1 * 1 = -1 and (-1) * (-1) = 1 | -1 and 1 | yes |
| `rem0` through `rem4` | 0, 1, 2, 3, 4 leave remainders 0, 1, 2, 3, 0 | same | yes |
| `pow1` through `pow4` | powers 1 through 4 are J, the square, the cube, the identity | same | yes |
| independent check | checks=257 failures=0 | 17 closed identities plus 40 values of k times 6 checks = 257 | yes |

The range k from 0 through 39 is a check bound. `alias4`, `mod_succ`, `pow_rep`, `pow_eye`, and `pow_period` quantify over every natural number.

## Scanner rows left out of this node

LOW R10 on TENSOR-ASSUMPTION-COUNTERMODELS, LOW R5 on `tfq_1019_fq_gap_tensor_uniqueness.md` (20261019), and LOW R5 on `tfq_0413_tensor_assumption_countermodels.md` (1/2, 1/4). Those notes moved because tensor receipt hashes were rebound. They are not claims of this node.

## What is still open

Continuity of reversible dynamics, global field uniqueness, local tomography, a U(1) phase fiber, a complex involution, and a separation of that fiber from Q/Z torsion.
