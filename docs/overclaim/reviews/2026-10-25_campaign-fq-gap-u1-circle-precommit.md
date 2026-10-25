# Review of campaign FQ-GAP-U1-CIRCLE

Scope: worktree branch derive/FQ-GAP-U1-CIRCLE against origin/main 7fa69d621c27. Reviewed against the statements as they stand after the narrowing. Rule applied: PROVED_LEAN only if Lean declarations in the repository state the node's full statement and compile with only propext, Classical.choice and Quot.sound.

Method: `python -I -X utf8 scripts/overclaim_scan.py --changed-since origin/main --strict` (HIGH 0, MEDIUM 0, LOW 6, exit 0). Read `FQ-GAP-U1-CIRCLE` statement, bottleneck and `pfp_review` in `dag/derivation_dag.json`, and `lean4/CampaignFqGapU1Circle.lean` through `noNonzeroClearedSquareRoot` together with the `#print axioms` lines. Recomputed the concrete identity and the finite scans with `python -I -X utf8 checks/independent/fq-gap-u1-circle.py`. Lean was built in this worktree before the scan; this review did not rebuild.

Result: 1 node FULL against the narrowed statement, 0 NARROWED as a further cut, 0 OVERCLAIM. The campaign outcome is Narrowed because the prior statement was wider. No node was raised. Status stays CONDITIONAL.

Corrections to the PR's own text:
- None. The standing statement matches the theorem types.

## Per-node table

| Node | Declarations that discharge it | Verdict | Reason |
|---|---|---|---|
| FQ-GAP-U1-CIRCLE | `pythagorean345`, `fiveFourSquareForcesZero`, `clearedDenominatorForcesFourFifths`, `noNonzeroClearedSquareRoot` | FULL on the narrowed statement | Each atomic sentence of the standing statement is the type of one of those declarations. Axioms are `propext` and `Quot.sound` or empty. The circle group, continuity, `n` mapped to `u^n`, and the homomorphism stay in the bottleneck and are not claimed. |

Atomic claims:
- `3*3 + 4*4 = 5*5` matches `pythagorean345` (`lean4/CampaignFqGapU1Circle.lean`).
- For every natural `a` and `b`, `5*(a*a) = 4*(b*b)` only when `b = 0` matches `fiveFourSquareForcesZero`.
- For every integer `a`, `b` and `d`, both `5*(a*a - b*b) = 3*(d*d)` and `a*a + b*b = d*d` only at `0, 0, 0` matches `noNonzeroClearedSquareRoot`. The bridge `5*(a*a) = 4*(d*d)` matches `clearedDenominatorForcesFourFifths`.

## Numbers recomputed

| Where | Claimed | Recomputed (method) | Match |
|---|---|---|---|
| statement and `pythagorean345` | 3*3 + 4*4 = 5*5 | independent check and Lean `decide` | match |
| independent check | no natural `b` in 1..2000 with `5*a*a = 4*b*b` | `checks/independent/fq-gap-u1-circle.py` | match; the scan is finite and is not the descent |
| independent check | integers in -12..12 solve both equations only at 0,0,0 | same script | match; the box is finite and is not the integer theorem |
| derivation note | the Python scan is not the all-integer descent | note text | match |

## Scanner output
HIGH 0. MEDIUM 0. No baseline change.

LOW findings in scope, left as they stood on main:
- R10 `TENSOR-ASSUMPTION-COUNTERMODELS`: cited modules have no replay receipt.
- R5 `tfq_1019_fq_gap_tensor_uniqueness.md`: number 20261019.
- R5 `tfq_0413_tensor_assumption_countermodels.md`: fractions 1/2 and 1/4.
- R5 notes `tfq_0294`, `tfq_0253` and `tfq_0053` name `FQ-GAP-U1-CIRCLE` and carry older counts. This narrowing does not edit those notes.

What the scanner could not decide: whether the older U(1) modules still cited on the node prove more than this statement. They are not used as the discharge of the standing statement. The Python bounds 2000 and 12 are scans, recorded as such in the derivation note.
