# Review of campaign TFQ-0313 precommit

Scope: worktree `derive/TFQ-0313` against merge base `7fa69d621c27`. Reviewed before the pull request. Rule applied: PROVED_LEAN only if Lean declarations in the repository state the node's full statement and compile with only propext, Classical.choice and Quot.sound.

Method: `python -I -X utf8 scripts/overclaim_scan.py --changed-since origin/main --strict` (HIGH 0, MEDIUM 0, LOW 3, exit 0). The module `lean4/CampaignTfq0313OperatorAlgebraShadow.lean` was rebuilt with `lake build CampaignTfq0313OperatorAlgebraShadow` under Lean 4.35.0; every `#print axioms` line is `propext`. The independent check was run with `python -I -X utf8 checks/independent/tfq-0313.py`. Status was not raised.

Result: 0 nodes FULL, 1 NARROWED, 0 OVERCLAIM. No node was raised.

Corrections to the PR's own text:
- TFQ-0313: the finite fragment is the 16-element module only. The QM_202 stub, continuum operator algebra, and an identification of the coefficient ring with the integers or the Gaussian integers are not theorems.

## Per-node table

| Node | Declarations that discharge it | Verdict | Reason |
|---|---|---|---|
| TFQ-0313 | `A_on`, `B_on`, `A_additive`, `B_additive`, `A_homogeneous`, `B_homogeneous`, `ab_matrix`, `ba_matrix`, `commutator_matrix`, `ab_ne_ba`, `ab_matches_composition`, `ba_matches_composition`, `actions_differ_on_e0`, `left_action_e0`, `right_action_e0`, `commutator_on_e0`, `diagonals_commute`, `diagonal_product`, `A_not_scalar`, `coeff_char_four`, `module_has_sixteen_vectors`, `module_lists_every_vector` in `lean4/CampaignTfq0313OperatorAlgebraShadow.lean` | NARROWED | Status stays OPEN. The documentary sentences about qm_202, qm_004, and qm_122 are not Lean theorems. The route `UDG-R-TFQ-0313` stays `GAP_NO_DERIVATION`. |

Atomic claims of the narrowed fragment, each matched to a declaration type:

| Claim | Declaration | Verdict |
|---|---|---|
| A sends (x, y) to (y, 0); B sends (x, y) to (0, x) | `A_on`, `B_on` | matched |
| A and B are additive and Z/4Z-homogeneous on every vector | `A_additive`, `B_additive`, `A_homogeneous`, `B_homogeneous` | matched |
| AB = [[1, 0], [0, 0]], BA = [[0, 0], [0, 1]], AB − BA = [[1, 0], [0, 3]], and AB ≠ BA | `ab_matrix`, `ba_matrix`, `commutator_matrix`, `ab_ne_ba` | matched |
| The matrix products act as the composites, and the two composites differ on (1, 0) by (1, 0) | `ab_matches_composition`, `ba_matches_composition`, `left_action_e0`, `right_action_e0`, `actions_differ_on_e0`, `commutator_on_e0` | matched |
| diag(1, 2) and diag(3, 1) commute with product diag(3, 2) | `diagonals_commute`, `diagonal_product` | matched |
| A is not a scalar matrix | `A_not_scalar` | matched |
| 1+1+1+1 = 0 and 1 ≠ 0 | `coeff_char_four` | matched |
| The carrier lists 16 distinct vectors and every vector of the module | `module_has_sixteen_vectors`, `module_lists_every_vector` | matched |
| qm_202 is a stub, neighboring records do not fill it, and qm_122 is only a Gaussian-integer stand-in | not proved | not proved |
| The coefficient ring is not identified with the integers or the Gaussian integers | not a theorem; the statement says the Lean file does not identify them | not proved |

## Numbers recomputed

| Where | Claimed | Recomputed (method) | Match |
|---|---|---|---|
| statement, note, Lean, Python | 16 vectors | `allV.length = 16` and `len(VECTORS) == len(set(VECTORS)) == 16` | match |
| statement, note, Lean, Python | AB [[1, 0], [0, 0]] | matrix product over Z/4Z in `checks/independent/tfq-0313.py` and `ab_matrix` | match |
| statement, note, Lean, Python | BA [[0, 0], [0, 1]] | same pair of checks, `ba_matrix` | match |
| statement, note, Lean, Python | AB − BA [[1, 0], [0, 3]] | lower-right entry 0 − 1 = 3 mod 4; `commutator_matrix` | match |
| statement, note, Lean, Python | diagonal product diag(3, 2) | `1*3 = 3`, `2*1 = 2`; `diagonal_product` | match |
| statement, note, Lean, Python | 1+1+1+1 = 0 and 1 ≠ 0 | `coeff_char_four` and the Python `char` check | match |
| independent script stdout | 722 conditions, 0 failures | 10 closed checks + 4 scalar checks + 4 checks on (1, 0) + 4×16 action checks + 2×16×16 additivity checks + 2×16×4 homogeneity checks = 722 | match |
| README inventory | 2428 tracked `.lean` files under `dag` | `git ls-tree -r --name-only HEAD -- dag` filtered to `.lean` | match |

The evidence page grades TFQ-0313 E3. That grade counts cited files. It is not a statement-match review, and the map records 0 nodes at E4.

## Scanner output

HIGH 0, MEDIUM 0. The three LOW findings are not about TFQ-0313: R10 on TENSOR-ASSUMPTION-COUNTERMODELS, and R5 numbers `20261019`, `1/2`, and `1/4` in two derivation notes whose evidence pages were regenerated because the tensor receipt hash moved. No baseline change. Section 6 of the pre-existing TFQ-0313 derivation paper was not edited and was not recomputed.
