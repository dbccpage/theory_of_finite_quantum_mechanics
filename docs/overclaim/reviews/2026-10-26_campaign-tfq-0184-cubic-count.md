# Overclaim review: TFQ-0184 cubic count

Scope: worktree changes for `derive/TFQ-0184` against `origin/main` at `92a639ddc0676a202bee5c837c35a7460e55f2fe`. Node status stays OPEN. AuthorityEffect: None.

## Method

Read `CampaignTfq0184CubicCount.lean` against the TFQ-0184 statement. Recomputed the split in `checks/independent/tfq-0184.py` (`python -I -X utf8`, 604 checks, 0 failures). Lake build exited 0. Printed axioms are empty, or `propext` and `Quot.sound`. `scripts/overclaim_scan.py --changed-since origin/main --strict` reported HIGH=0, MEDIUM=0, LOW=2, and exited 0. The two LOW findings are R10 and R5 on `TENSOR-ASSUMPTION-COUNTERMODELS`, from the repin of `dag/research/tensor_countermodel_validation.json`. They are not a TFQ-0184 claim, and this change does not edit that note.

## Result

0 FULL, 1 NARROWED, 0 OVERCLAIM. Status stays OPEN.

## Statement versus theorem

| Claim | Declaration | Verdict |
| --- | --- | --- |
| For every natural number n, n * n * n is at most n * n * n | `cubicReflexivity` | FULL |
| For every n at least 1, twice the cube equals (n - 1) * n * (2 * n - 1) plus n * (3 * n - 1) | `eliminationSplit` | FULL |
| For every n at least 1, (n - 1) * n * (2 * n - 1) is strictly below twice the cube | `eliminationBelowTwiceCube` | FULL |
| For every n at least 1, n * (3 * n - 1) is at least 2 | `gapAtLeastTwo` | FULL |
| At n = 4 the cube is 64 | `fourCube` | FULL |
| At n = 4, 1 * 1 + 2 * 2 + 3 * 3 is 14 | `fourSumOfSquares` | FULL |
| At n = 4, (3 * 4 * (2 * 4 - 1)) / 6 is 14 | `fourClosedForm` | FULL |
| 14 is strictly below 64 | `fourCountBelowCube` | FULL |
| Paper 009 README title custody | not proved | NOT PROVED |
| Enum rfl declarations are measured tetron homology, or are not | not proved | NOT PROVED |
| F004 realization-packet gap, noise sweeps, evaluator role | not proved | NOT PROVED |

The opening custody sentences stay in the statement as the open reading. The bottleneck says they are outside the checked slice. The node is not PROVED_LEAN.

## Numbers recomputed

64 = 4 * 4 * 4. 14 = 1 + 4 + 9. 14 = (3 * 4 * 7) / 6. 14 < 64. For n from 1 through 29, 2 * n * n * n = (n - 1) * n * (2 * n - 1) + n * (3 * n - 1) and the gap is at least 2. Match.

## What the scanner could not decide

Whether the retained README sentences could be read as a discharged custody claim. They are not discharged. Status stays OPEN. The reflexivity comparison is the same product on both sides, which is what `Nat.le_refl` states. The split identity is the non-trivial count. The scanner's two LOW findings name another node whose receipt hash moved in the repin; they are left as they stand.
