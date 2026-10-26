# Overclaim review: GP-IMPORT-CONTINUUM-HILBERT

Scope: worktree `C:/gw/derive-gp-chilbert`, branch `derive/GP-IMPORT-CONTINUUM-HILBERT`, diff against `origin/main` at `4fea09ae176aae31115e38bb2b21819237055811`. Pre-commit review. This pass did not rebuild the module; the replay receipt records the earlier `lake build`.

## Method

`python -I -X utf8 scripts/overclaim_scan.py --changed-since origin/main --strict` returned HIGH=0, MEDIUM=0, LOW=3. The node statement, bottleneck, `pfp_review`, and `lean4/CampaignGpImportContinuumHilbert.lean` were read against the declarations. Numbers were recomputed by `python -I -X utf8 checks/independent/gp-import-continuum-hilbert.py` (checks=261, failures=0).

## Result

0 FULL, 1 NARROWED, 0 OVERCLAIM.

The original transition to a continuous infinite-dimensional Hilbert space is not the statement of any declaration in the new module. Status stays `IMPORTED_ASSUMPTION`. `AuthorityEffect` stays None.

## Per-node table

Node: `GP-IMPORT-CONTINUUM-HILBERT`. Verdict: NARROWED.

| Claim | Declaration | Verdict |
| --- | --- | --- |
| pow4 0 = 1 and pow4 (k + 1) = pow4 k * 4 | `pow4` at lean4/CampaignGpImportContinuumHilbert.lean:7 | stated by the definition |
| sumPow4 0 = 0 and sumPow4 (k + 1) = sumPow4 k + pow4 k | `sumPow4` at lean4/CampaignGpImportContinuumHilbert.lean:11 | stated by the definition |
| 8 = 4 + 4, 4 = 2 + 2, 2 = 1 + 1 | `halves` at lean4/CampaignGpImportContinuumHilbert.lean:30 | matched |
| 8 * 8, 4 * 4, 2 * 2, 1 * 1 equal 64, 16, 4, 1 | `windowSquares` at lean4/CampaignGpImportContinuumHilbert.lean:33 | matched |
| those products sum to 85 | `windowSum` at lean4/CampaignGpImportContinuumHilbert.lean:36 | matched |
| that sum equals sumPow4 4 | `windowIsSum` at lean4/CampaignGpImportContinuumHilbert.lean:45 | matched |
| 3 * 85 + 1 = 256 | `windowScaled` at lean4/CampaignGpImportContinuumHilbert.lean:39 | matched |
| pow4 4 = 256 | `pow4Four` at lean4/CampaignGpImportContinuumHilbert.lean:42 | matched |
| 64 - 16, 16 - 4, 4 - 1 equal 48, 12, 3 and equal 3 * 16, 3 * 4, 3 * 1 | `squareDiffs` at lean4/CampaignGpImportContinuumHilbert.lean:48 | matched |
| for each natural n, 3 * sumPow4 n + 1 = pow4 n | `closedTail` at lean4/CampaignGpImportContinuumHilbert.lean:15 | matched |
| for each natural n, pow4 n - 3 * sumPow4 n = 1 | `scaledTailIsOne` at lean4/CampaignGpImportContinuumHilbert.lean:22 | matched |
| for each natural n, sumPow4 (n + 1) - sumPow4 n = pow4 n | `sumDiff` at lean4/CampaignGpImportContinuumHilbert.lean:26 | matched |
| no positive natural z has z + z = 1 | `noPositiveDoubleOfOne` at lean4/CampaignGpImportContinuumHilbert.lean:53 | matched |
| continuous infinite-dimensional Hilbert carrier, topology, Cauchy completion, scalar-field selection, l2 uniformity | not proved | left in the bottleneck |

Axioms from the receipt: `closedTail`, `scaledTailIsOne`, `sumDiff`, and `noPositiveDoubleOfOne` use `propext` and `Quot.sound`. The other listed declarations use none. `Classical.choice` does not appear.

## Numbers recomputed

Independent check, integer arithmetic only: window (8, 4, 2, 1), squares (64, 16, 4, 1), sum 85, 3 * 85 + 1 = 256, pow4(4) = 256, differences (48, 12, 3) = (3 * 16, 3 * 4, 3 * 1), and 3 * S(n) + 1 = 4^n for n from 0 through 40. Match. The bound 40 is only the check range; the Lean statements quantify over every natural number by induction.

## Scanner rows left out of this node

LOW R10 on TENSOR-ASSUMPTION-COUNTERMODELS, LOW R5 on tfq_1019_fq_gap_tensor_uniqueness.md (number 20261019), and LOW R5 on tfq_0413_tensor_assumption_countermodels.md (1/2, 1/4). Those notes moved because tensor receipt hashes were rebound. They are not claims of GP-IMPORT-CONTINUUM-HILBERT.

## What is still open

Scalar-field selection, l2 uniformity, a verified topology, a Cauchy completion, and the lift of bounded exact operators. QM_122 section 6 and the QM_020 demotion box still fence that transition.
