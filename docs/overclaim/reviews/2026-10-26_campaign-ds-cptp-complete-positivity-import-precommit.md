# Overclaim review: DS-CPTP-COMPLETE-POSITIVITY-IMPORT

Scope: worktree `C:/gw/derive-ds-cptppos`, branch `derive/DS-CPTP-COMPLETE-POSITIVITY-IMPORT`, diff against `origin/main` at `4fea09ae176aae31115e38bb2b21819237055811`. Pre-commit review. This pass did not rebuild the module; the replay receipt records the earlier `lake build`.

## Method

`python -I -X utf8 scripts/overclaim_scan.py --changed-since origin/main --strict` returned HIGH=0, MEDIUM=0, LOW=3. The node statement, bottleneck, and `lean4/CampaignDsCptpCompletePositivity.lean` were read against the declarations. Numbers were recomputed by integer arithmetic and by `python -I -X utf8 checks/independent/ds-cptp-complete-positivity-import.py` (checks=648, failures=0).

## Result

0 FULL, 1 NARROWED, 0 OVERCLAIM. No node was raised.

Complete positivity of a tensor extension, Kraus, Choi and Stinespring forms, and coherence transport are not the statement of any new declaration. Status stays `IMPORTED_ASSUMPTION`. `AuthorityEffect` stays None. The standing statement is the nonnegative integer product and the strict sign of `t * (-2)`.

## Per-node table

Node: `DS-CPTP-COMPLETE-POSITIVITY-IMPORT`. Verdict: NARROWED.

| Claim | Declaration | Verdict |
| --- | --- | --- |
| for every integer n, n * n is at least 0 | `squareNonneg` (lean4/CampaignDsCptpCompletePositivity.lean:13) | matched |
| (-n) * (-n) = n * n | `negMulNeg` (same file:7) | matched |
| for natural k, m, the integer product equals the integer of k * m | `mulOfNat` (same file:25) | matched |
| a nonnegative integer times a nonnegative integer is at least 0 | `mulNonneg` (same file:28) | matched |
| if t is at least 0, then t * ((x + w) * (x + w)) is at least 0 | `bellNonneg` (same file:42) | matched |
| 1 * (-1) + (-1) * 1 = -2 | `pairing` (same file:46) | matched |
| t times that sum equals (-2) * t | `scaled` (same file:48) | matched |
| t * (-2) = 2 * (-t) | `scaleTwice` (same file:52) | matched |
| if t is greater than 0, then t * (-2) is less than 0 and -t is less than 0 | `negOut` (same file:54), `negT` (same file:56) | matched |
| 0 * (-2) = 0 | `zeroScale` (same file:58) | matched |
| 0*0 + 1*1 + (-1)*(-1) + 0*0 = 2 | `normSq` (same file:60) | matched |
| tensor complete positivity, Kraus, Choi, Stinespring, coherence transport | not proved | left in the bottleneck |

Axioms from the receipt, not rebuilt here: `negMulNeg`, `squareNonneg`, `mulOfNat`, and `scaled` use `propext`. `mulNonneg`, `bellNonneg`, `scaleTwice`, `negOut`, and `negT` use `propext` and `Quot.sound`. `pairing`, `zeroScale`, and `normSq` use none. No `sorryAx` and no `Classical.choice`.

The strict sign needs t greater than 0. At t = 0 the same product is 0. The check ranges are bounds. `squareNonneg`, `bellNonneg`, `scaled`, `scaleTwice`, `negOut`, and `negT` quantify over every integer in their hypotheses.

## Numbers recomputed

| Where | Claimed | Recomputed | Match |
| --- | --- | --- | --- |
| `pairing` | 1 * (-1) + (-1) * 1 = -2 | -1 + -1 = -2 | yes |
| `normSq` | 0 + 1 + 1 + 0 = 2 | 2 | yes |
| `zeroScale` | 0 * (-2) = 0 | 0 | yes |
| `scaleTwice` | t * (-2) = 2 * (-t) | both equal -2t | yes |
| independent check | checks=648 failures=0 | 82 squares, 162 products, 49 nonnegative pairs, 294 Bell samples, 1 pairing, 34 scales, 24 strict signs, 2 closed identities = 648 | yes |

## Scanner rows left out of this node

LOW R10 on TENSOR-ASSUMPTION-COUNTERMODELS, LOW R5 on `tfq_1019_fq_gap_tensor_uniqueness.md` (20261019), and LOW R5 on `tfq_0413_tensor_assumption_countermodels.md` (1/2, 1/4). Those notes moved because tensor receipt hashes were rebound. They are not claims of this node.

## What is still open

Complete positivity of a tensor extension, Kraus, Choi and Stinespring forms, and coherence transport above a classical kernel.
