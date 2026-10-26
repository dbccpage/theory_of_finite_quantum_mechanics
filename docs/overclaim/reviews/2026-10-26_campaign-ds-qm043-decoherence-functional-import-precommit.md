# Overclaim review: DS-QM043-DECOHERENCE-FUNCTIONAL-IMPORT

Scope: worktree `C:/gw/derive-ds-qm043`, branch `derive/DS-QM043-DECOHERENCE-FUNCTIONAL-IMPORT`, diff against `origin/main` at `4fea09ae176aae31115e38bb2b21819237055811`. Pre-commit review. This pass did not rebuild the module; the replay receipt records the earlier `lake build`.

## Method

`python -I -X utf8 scripts/overclaim_scan.py --changed-since origin/main --strict` returned HIGH=0, MEDIUM=0, LOW=3. The node statement, bottleneck, and `lean4/CampaignDsQm043DecoherenceFunctional.lean` were read against the declarations. Numbers were recomputed by integer arithmetic and by `python -I -X utf8 checks/independent/ds-qm043-decoherence-functional-import.py` (checks=3459, failures=0).

## Result

0 FULL, 1 NARROWED, 0 OVERCLAIM. No node was raised.

The imported formula `D_jk = Tr(C_j rho C_k^dagger)`, a density operator, class operators, and a transport bridge are not the statement of any new declaration. Status stays `IMPORTED_ASSUMPTION`. `AuthorityEffect` stays None. The standing statement is the integer Gram square, the determinant identity, and the two cleared witnesses.

## Per-node table

Node: `DS-QM043-DECOHERENCE-FUNCTIONAL-IMPORT`. Verdict: NARROWED.

| Claim | Declaration | Verdict |
| --- | --- | --- |
| for each integer n, n * n is at least 0 | `squareNonneg` (lean4/CampaignDsQm043DecoherenceFunctional.lean:13) | matched |
| for each integer n, (-n) * (-n) = n * n | `negMulNeg` (same file:7) | matched |
| for each integer a, b, x, y, (a*x + b*y) * (a*x + b*y) is at least 0 | `gramValueNonneg` (same file:25) | matched |
| for each integer a, a * a is at least 0 | `diagNonneg` (same file:29) | matched |
| for each integer a, b, (a*b)*(a*b) = a*a*(b*b) | `gramProd` (same file:32) | matched |
| that difference is 0 | `gramDet` (same file:40) | matched |
| a*a + b*b is at least 0 | `traceSquaresNonneg` (same file:44) | matched |
| 1 + 1 = 2 * 1 and 1*1 + 1*1 = 2 | `halfClass` (same file:49), `halfSquares` (same file:51) | matched |
| 2 * 2 = 4 and 2 differs from 4 | `halfDenom` (same file:53), `halfSeparates` (same file:55) | matched |
| (1 + 1) * (1 + 1) = 4 and 4 = 4 * 1 | `halfGlobal` (same file:57), `halfGlobalOne` (same file:59) | matched |
| at 1, 1, 1, 1 the square and the expanded product count both equal 4 | `gramAtOnes` (same file:73) | matched |
| 3*3 + 4*4 = 25 and 5*5 = 25, so the square-sum equals 5*5 | `krausSquares` (same file:61), `fiveSquare` (same file:63), `krausHolds` (same file:65) | matched |
| 3 + 4 = 7, 7*7 = 49, and 49 differs from 25 | `classSum` (same file:67), `sevenSquare` (same file:69), `classSeparates` (same file:71) | matched |
| the trace formula, density, class operators, and a transport bridge | not proved | left in the bottleneck |

Axioms from the receipt, not rebuilt here: `negMulNeg`, `squareNonneg`, `gramValueNonneg`, `diagNonneg`, and `gramProd` use `propext`. `gramDet` and `traceSquaresNonneg` use `propext` and `Quot.sound`. The `decide` declarations use none. No `sorryAx` and no `Classical.choice`.

The derivation note calls `gramDet` the determinant of the symmetric table with entries a*a, a*b, a*b, b*b. That is this integer identity. The module has no matrix type and no general positive-semidefinite predicate.

## Numbers recomputed

| Where | Claimed | Recomputed | Match |
| --- | --- | --- | --- |
| statement and `halfClass` | 1 + 1 = 2 * 1 | 2 = 2 | yes |
| `halfSquares` | 1*1 + 1*1 = 2 | 2 = 2 | yes |
| `halfDenom`, `halfSeparates` | 2*2 = 4 and 2 differs from 4 | 4 = 4, 2 != 4 | yes |
| `halfGlobal`, `halfGlobalOne` | (1+1)*(1+1) = 4 = 4*1 | 4 = 4 = 4 | yes |
| `gramAtOnes` | both sides equal 4 | (1+1)*(1+1) = 4; 1+2+1 = 4 | yes |
| note line 19 | 3*3 + 4*4 = 9 + 16 = 25 | 9 + 16 = 25 | yes |
| `fiveSquare`, `krausHolds` | 5*5 = 25 and the square-sum equals it | 25 = 25 | yes |
| `classSum`, `sevenSquare`, `classSeparates` | 3+4 = 7, 7*7 = 49, 49 differs from 25 | 7, 49, 49 != 25 | yes |
| note, cleared halves | (1/2)^2 + (1/2)^2 = 1/2, numerator 2 against denominator square 4 | 1/4 + 1/4 = 2/4 = 1/2 | yes |
| note, cleared 3 and 4 | ((3+4)/5)^2 = 49/25, which differs from 1 | 49/25 != 25/25 | yes |
| independent check | checks=3459 failures=0 | 61 squares, 169 pairs times 20, plus 18 closed identities = 3459 | yes |

The ranges n from -30 through 30, a and b from -6 through 6, and the four x and y samples are check bounds. `squareNonneg`, `gramValueNonneg`, `gramProd`, `gramDet`, and `traceSquaresNonneg` quantify over every integer.

## Scanner rows left out of this node

LOW R10 on TENSOR-ASSUMPTION-COUNTERMODELS, LOW R5 on `tfq_1019_fq_gap_tensor_uniqueness.md` (20261019), and LOW R5 on `tfq_0413_tensor_assumption_countermodels.md` (1/2, 1/4). Those notes moved because tensor receipt hashes were rebound. They are not claims of this node.

## What is still open

The formula D_jk = Tr(C_j rho C_k^dagger), a representation bridge from finite transport, a choice of class operators, and a physical history normalization. The two witnesses do not select that model.
