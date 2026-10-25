# Overclaim review: TFQ-0003 precommit

AuthorityEffect: None.

## Scope

Worktree `C:\gw\derive-tfq0003`, branch `derive/TFQ-0003`, against `origin/main` at `7fa69d621`. Node `TFQ-0003` only. Status was not raised: it stays `OPEN`.

## Method

`scripts/overclaim_scan.py --changed-since origin/main --strict` reported HIGH=0, MEDIUM=0, LOW=3. The statement was split into atomic claims and matched to `lean4/CampaignTfq0003FiniteObstruction.lean`. The module was built with `lake build CampaignTfq0003FiniteObstruction` (Lean 4.35.0). Numbers were recomputed by `python -I -X utf8 checks/independent/tfq-0003.py` (913 conditions, 0 failures).

## Result

0 FULL as a promotion, 1 NARROWED, 0 OVERCLAIM. The node stays OPEN. The finite fragment below is proved. The shelf admission, the three-language correspondence, Rust, and a derivation from Genesis are not proved.

## Per-node table

| Claim | Lean declaration | Verdict |
|---|---|---|
| Vertices {0,1,2} and 0 ≠ 2 do not make edge cochain (0,0,1) a coboundary | `comparison_is_not_the_quotient` | FULL |
| d1 ∘ d0 = 0 on the triangle | `d1_d0` | FULL |
| Quotient of edge cochains is equality of d1 | `equiv_iff_d1` | FULL |
| Phi1(w) = \|d1(w)\| and is attained by clearing the first two edges | `phi1_attained`, `phi1_lower` | FULL |
| Gamma2(w) = Phi1(w) on the triangle | `gamma2_eq_phi1` | FULL |
| w = (1,1,0) has Phi1 = 2, Gamma2 = 2, classical residual 2/2 | `sample_phi1`, `sample_gamma2`, `sample_rcl`, `sample_ratio_one` | FULL |
| Repair (0,1,0) leaves residual (0,2,0) of L1 mass 2 | `recorded_residual_l1` | FULL |
| Zero cochain has Phi1 = 0, Gamma2 = 0, both-vanish value 0 | `zero_signature` | FULL |
| Refusal cell rcl(0,1) = none, and neither complex meets it | `rcl_refuses_zero_over_one`, `triangle_rcl_defined`, `cycle_rcl_defined` | FULL |
| Unfilled 4-cycle has no 2-cell so Gamma2 = 0, and Phi1 is the absolute edge sum | `gamma2Cycle`, `phi1Cycle_attained`, `phi1Cycle_lower` | FULL |
| w = (1,0,0,0) has Phi1 = 1, Gamma2 = 0, classical residual 0, and is not a coboundary | `cycle_signature` | FULL |
| F000 shelf admission, three-language statement, Rust witness, derivation from Genesis | not proved | NOT PROVED |

## Axioms

Printed axioms are subsets of `propext` and `Quot.sound`. `Classical.choice` does not appear. No `sorry`, `admit`, `axiom`, `native_decide`, or `unsafe`.

## Numbers recomputed

| Number | Recomputation | Match |
|---|---|---|
| 2 | `d1(1,1,0) = 2`, Phi1 and Gamma2, residual L1 of (0,2,0) | match |
| 1 | ratio because Phi1 = Gamma2 = 2; cycle Phi1 = 1 | match |
| 0 | zero cochain charges; cycle Gamma2; cycle classical residual | match |

## What the scanner could not decide

LOW findings were not promoted. The scan cannot read whether a declaration states the node. The table above is that reading. A Lake build is not a three-language correspondence, and this review does not treat it as one.
