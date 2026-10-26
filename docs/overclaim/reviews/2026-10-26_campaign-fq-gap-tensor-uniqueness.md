# Review of campaign FQ-GAP-TENSOR-UNIQUENESS

Scope: pull request #442, branch `derive/FQ-GAP-TENSOR-UNIQUENESS` at `d296b6c6566c5a3976680a0cbaa6aaf9d68c608a`, after one rebase onto `e34adcea1d312a26cb65ef37fd08026d78bcd7c8`. The Lean file was built on `867c667201efccec701ce3d4e6a418aece5dde96` and was not edited again. Rule applied: PROVED_LEAN only if Lean declarations in the repository state the node's full statement and compile with only propext, Classical.choice and Quot.sound.

Method: read the node statement, bottleneck and `pfp_review` in `dag/derivation_dag.json`, and `lean4/CampaignFqGapTensorUniqueness.lean` through `identityNotOuter` (lines 9-41) with the `#print axioms` lines. Scanner: `python -I -X utf8 scripts/overclaim_scan.py --changed-since origin/main --strict` (HIGH 0, MEDIUM 0, LOW 3). Independent check rerun. The Lean job was not rebuilt after the rebase.

Result: 0 nodes FULL, 1 NARROWED, 0 OVERCLAIM. No node was raised. Status stays CONDITIONAL.

Corrections to the PR's own text:
- None in the Lean types. The operational sentences in the statement remain supplied, not discharged.

## Per-node table

| Node | Declarations that discharge it | Verdict | Reason |
|---|---|---|---|
| FQ-GAP-TENSOR-UNIQUENESS | `outerDet`, `identityDet`, `identityNotOuter` | NARROWED | The integer clauses match the declarations. The operational composition, PSD cones and saturation sentences are not proved. |

Statement-vs-theorem:

| Claim | Declaration | Verdict |
|---|---|---|
| General finite-dimensional composition follows from the supplied operational premises | not proved | NOT PROVED |
| State and generated effect cones are PSD, and full effect and POVM availability has saturation assumptions | not proved | NOT PROVED |
| Primitive difference has not supplied those premises | not proved | NOT PROVED |
| Every integer 2 by 2 outer product has determinant 0 | `CampaignFqGapTensorUniqueness.outerDet` (`lean4/CampaignFqGapTensorUniqueness.lean`) | FULL for this clause |
| The matrix with entries 1, 0, 0 and 1 has determinant 1 and is not an outer product of two integer vectors | `identityDet`, `identityNotOuter` | FULL for this clause |

Axioms printed for `productsEq`, `outerDet`, `identityDet` and `identityNotOuter`: `propext` only.

## Numbers recomputed

| Where | Claimed | Recomputed (method) | Match |
|---|---|---|---|
| `outerDet` | determinant 0 | `(a0*b0)*(a1*b1) - (a0*b1)*(a1*b0) = 0` by commuting integer products; sample `2*5, 2*7, 3*5, 3*7` gives `10*21 - 14*15 = 0` | match |
| `identityDet` | determinant 1 | `1*1 - 0*0 = 1` | match |
| independent check | failures 0 | `python -I -X utf8 checks/independent/fq-gap-tensor-uniqueness.py` printed `checks=2403 identity_det=1 sample_det=0 failures=0`. The box is the 7 integers from -3 through 3, and `7*7*7*7 + 2 = 2401 + 2 = 2403` | match |
| evidence README | 2417 declarations, 2345 receipt-backed, 2278 itemised, 38 non-test code citations | prior counts 2414, 2342, 2275 and 37, each plus the 3 new declarations or the 1 new Python file | match |

`20261019` in the generated TFQ-1019 note is a label copied from `source_status`. It is not a quantity in the new theorem. LOW R5 records that the token is absent from the cited Lean and Python files.

## Scanner output

HIGH 0. MEDIUM 0. LOW 3, not introduced as new arithmetic: R5 `20261019` on TFQ-1019; R5 `1/2` and `1/4` on `TENSOR-ASSUMPTION-COUNTERMODELS`; R10 that node cites Lean modules with no replay receipt. No baseline change.

## What the scanner could not decide

Whether the standing operational sentences, kept as supplied text, will be read as theorems. They have no matching declaration here, and the status remains CONDITIONAL.
