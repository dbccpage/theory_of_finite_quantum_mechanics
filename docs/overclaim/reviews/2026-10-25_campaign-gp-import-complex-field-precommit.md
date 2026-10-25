# Review of campaign GP-IMPORT-COMPLEX-FIELD

Scope: worktree branch derive/GP-IMPORT-COMPLEX-FIELD against origin/main c50dc1b472596d1b5934408b00b9fbb72db91345. Rule applied: PROVED_LEAN only if Lean declarations in the repository state the node's full statement and compile with only propext, Classical.choice and Quot.sound.

Method: read the standing statement, bottleneck, and pfp_review; read the five cited declarations and the printed axiom lines in the replay receipt. Scanner: `python -I -X utf8 scripts/overclaim_scan.py --changed-since origin/main --strict` (HIGH 0, MEDIUM 0, LOW 3 on pre-existing tensor notes). Lean was built before this review; this review step did not rebuild.

Result: 1 node NARROWED, 0 FULL, 0 OVERCLAIM. No node was raised. Status stays IMPORTED_ASSUMPTION.

Corrections to the PR's own text:
- The prior sentence about a complete field is no longer the standing statement. It remains the prior_statement and is named in the bottleneck.

## Per-node table
| Node | Declarations that discharge it | Verdict | Reason |
|---|---|---|---|
| GP-IMPORT-COMPLEX-FIELD | `onePlusI_mul_coords` (lean4/CampaignGpImportComplexField.lean:67), `onePlusI_not_unit` (line 90), `fib_conjugate_transpose` (line 208), `fib_mulVec` (line 215), `fib_no_gauss_eigenpair` (line 221) | NARROWED | Standing text matches those declarations. The prior complete-field sentence is not a declaration. |

## Statement versus theorem
| Claim in the standing statement | Declaration | Verdict |
|---|---|---|
| (1+i)*(a+bi) equals (a-b)+(a+b)i | onePlusI_mul_coords | FULL |
| that product differs from the real unit | onePlusI_not_unit, first conjunct | FULL |
| (a+bi)*(1+i) differs from the real unit | onePlusI_not_unit, second conjunct | FULL |
| diagonal entries equal their conjugates and off-diagonal entries are conjugates of each other | fib_conjugate_transpose | FULL |
| the matrix sends (x, y) to (y, x+y) | fib_mulVec | FULL |
| a nonzero column image differs from lam*(x, y) | fib_no_gauss_eigenpair | FULL |
| complete complex field | not proved | NOT PROVED |
| spectral theorem for a general self-adjoint matrix | not proved | NOT PROVED |

Axiom lines from the receipt: onePlusI_mul_coords, onePlusI_not_unit, and fib_no_gauss_eigenpair use propext, Classical.choice, and Quot.sound; fib_mulVec uses propext; fib_conjugate_transpose uses no axioms.

## Numbers recomputed
| Where | Claimed | Recomputed (method) | Match |
|---|---|---|---|
| independent check | small squares 4,1,0,1,4 and char gap 5 | `python -I -X utf8 checks/independent/gp-import-complex-field.py` | match |
| README lean refs | 2473 to 2475 | removed 3 refs and added 5 | match |
| README derivation papers | 1098 to 1099 | one new note under dag/derivations | match |
| README lake libraries / roots | 120/972 to 121/973 | one new lean_lib | match |
| README scope counts | consistent 66 to 65, statement_narrowed 68 to 69 | one decision moved from consistent to statement_narrowed | match |

## Scanner output
No new HIGH finding. Three LOW findings name pre-existing tensor notes and were left unchanged. No baseline entry added.
