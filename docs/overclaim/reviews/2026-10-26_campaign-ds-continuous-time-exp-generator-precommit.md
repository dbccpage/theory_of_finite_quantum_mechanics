# Overclaim review: DS-CONTINUOUS-TIME-EXP-GENERATOR

Scope: worktree `C:/gw/derive-ds-expgen`, branch `derive/DS-CONTINUOUS-TIME-EXP-GENERATOR`, diff against `origin/main` at `4fea09ae176aae31115e38bb2b21819237055811`. Pre-commit review. This pass did not rebuild the module; the replay receipt records the earlier `lake build`.

## Method

`python -I -X utf8 scripts/overclaim_scan.py --changed-since origin/main --strict` returned HIGH=0, MEDIUM=0, LOW=3. The node statement, bottleneck, and `lean4/CampaignDsContinuousTimeExpGenerator.lean` were read against the declarations. Numbers were recomputed by `python -I -X utf8 checks/independent/ds-continuous-time-exp-generator.py` (checks=679, failures=0).

## Result

0 FULL, 1 NARROWED, 0 OVERCLAIM.

The imported one-parameter family, analytic logarithm, and continuum path integral are not the statement of any new declaration. Status stays `IMPORTED_ASSUMPTION`. `AuthorityEffect` stays None. The two matrices square to a scale-4 swap. They are not stated to be normalized or unitary.

## Per-node table

Node: `DS-CONTINUOUS-TIME-EXP-GENERATOR`. Verdict: NARROWED.

| Claim | Declaration | Verdict |
| --- | --- | --- |
| toggle false = true and toggle true = false | `toggleImages` | matched |
| no map on the two labels squares to toggle | `noToggleSquare` | matched |
| pair sum (a, b) + (c, d) = (a + c, b + d) | `gAddCoords` | matched |
| pair product (a, b) * (c, d) = (a*c - b*d, a*d + b*c) | `gMulCoords` | matched |
| the stated matrix squares to diagonal (0, 0) and off-diagonal (4, 0) | `scaledSquare` | matched |
| its coordinatewise negation squares to that matrix and differs | `negSquare`, `scaledDiffer` | matched |
| for every integer t, the Cayley polynomial identity | `cayleyNorm` | matched |
| branch energy at 0 is 1 and at 1 is 3 | `energyZero`, `energyOne` | matched |
| distinct integers have distinct branch energies | `energyDistinct` | matched |
| (-1)*(-1) + 1*1 = 2 | `candidateCorner` | matched |
| no integers meet the swap-shift equations and the four zero-square equations | `noNilpotentIntegerLog` | matched |
| T(t) = exp(tH), H = log T, path integral, convergence, measure | not proved | left in the bottleneck |

Axioms from the receipt: `cayleyNorm`, `energyDistinct`, and `noNilpotentIntegerLog` use `propext` and `Quot.sound`. The other listed declarations use none.

## Numbers recomputed

Independent integer check: four Boolean maps, none squares to toggle; both Gaussian matrices square to ((0, 0), (4, 0), (4, 0), (0, 0)); Cayley identity for t from -20 through 20; energies 1 and 3; distinct energies on integers from -12 through 12; corner value 2. Match. The finite ranges are check bounds. `cayleyNorm` and `energyDistinct` quantify over every integer.

## Scanner rows left out of this node

LOW R10 on TENSOR-ASSUMPTION-COUNTERMODELS, LOW R5 on tfq_1019_fq_gap_tensor_uniqueness.md, and LOW R5 on tfq_0413_tensor_assumption_countermodels.md. Those notes moved because tensor receipt hashes were rebound. They are not claims of this node.

## What is still open

A continuous one-parameter family, an analytic logarithm, generator selection among the odd branch energies, a convergence oracle, and a continuum path-integral measure.
