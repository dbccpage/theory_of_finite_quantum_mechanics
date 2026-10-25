# Overclaim review: L1-QM020-THM2B-MINKOWSKI

**AuthorityEffect:** None.

Scope: campaign branch `derive/L1-QM020-THM2B-MINKOWSKI` against `origin/main` `c50dc1b472596d1b5934408b00b9fbb72db91345`. One node. Status in this diff: `IMPORTED_ASSUMPTION` to `PROVED_LEAN` after the standing text was narrowed.

## Method

`python -I -X utf8 scripts/overclaim_scan.py --changed-since origin/main --strict` from the worktree. Then a statement-versus-theorem reading of `lean4/CampaignL1Qm020Thm2bMinkowski.lean` against the standing statement. The module was built with `lake build CampaignL1Qm020Thm2bMinkowski` (exit 0). Numbers were recomputed by `python -I -X utf8 checks/independent/l1-qm020-thm2b-minkowski.py`.

## Result

1 FULL, 0 NARROWED, 0 OVERCLAIM on the standing statement. Campaign outcome: Narrowed. The original real-p Minkowski citation is no longer the standing text.

Scanner: HIGH 0, MEDIUM 0, LOW 4. Three LOW findings are the pre-existing baseline items (R10 `TENSOR-ASSUMPTION-COUNTERMODELS`, R5 `20261019` on `FQ-GAP-TENSOR-UNIQUENESS`, R5 `1/2` and `1/4` on `TENSOR-ASSUMPTION-COUNTERMODELS`). The fourth LOW is R5 on the unchanged note `dag/derivations/08_l1_to_l2/tfq_0291_disjoint_aggregation_and_the_real_p_1_import.md` (numerals 820, 1230, 1640 and related cochain figures). That note was already on `origin/main`. It is reported in this diff because the node now shares record `TFQ-0291` with a claim status. Those numerals were not edited.

## Corrections to the PR text

None. The standing statement is the Nat slice the theorems state. Real exponent p>1, roots, strict convexity, and arbitrary-vector transport stay in the bottleneck.

## Per-node table

| Claim in the standing statement | Declaration | Axioms | Verdict |
|---|---|---|---|
| `(a + b) * (a + b) = a * a + b * b + 2 * (a * b)` for Nat `a`, `b` | `square_expansion` | propext, Quot.sound | FULL |
| Both positive implies `2 * (a * b) > 0` and `a * a + b * b < (a + b) * (a + b)` | `cross_positive`, `square_strict` | propext, Quot.sound | FULL |
| Left input 0: cross term 0 and `(0 + b) * (0 + b) = b * b` | `cross_zero_left`, `square_eq_left_zero` | propext, Quot.sound | FULL |
| Right input 0: cross term 0 and `(a + 0) * (a + 0) = a * a` | `cross_zero_right`, `square_eq_right_zero` | propext, Quot.sound | FULL |
| Cubic sum `(a + b) * (a + b) * (a + b) = a * a * a + b * b * b + 3 * a * b * (a + b)` | `cubic_sum` | propext, Quot.sound | FULL |
| Disjoint pair `(x + 0) * (x + 0) + (0 + y) * (0 + y) = x * x + y * y` | `disjoint_pair_squares` | none | FULL |
| Real-p Minkowski / strict convexity / arbitrary vectors | not a theorem in this module | — | not in the standing statement; bottleneck |

`prior_statement` still holds the original citation: strict l^p (p>1) subadditivity on disjoint supports, cited as standard analysis. That citation is not the standing text.

## Numbers recomputed

Independent check, exact integers, failures=0:

- Coordinates 0 through 12: 13 * 13 = 169 pairs. Each pair matches the square expansion, the cubic sum, and the disjoint-pair sum. Positive pairs have a positive cross term and a strict square gap. A zero on either side is an equality.
- Witness a = 3, b = 5: (3 + 5) * (3 + 5) = 64; 3 * 3 + 5 * 5 + 2 * (3 * 5) = 9 + 25 + 30 = 64; cross term 30; sum of squares 34; 34 < 64.
- Cube: 8 * 8 * 8 = 512; 27 + 125 + 3 * 3 * 5 * 8 = 27 + 125 + 360 = 512.

Printed line: `bound=12 pairs=169 failures=0 witness_square=64 witness_cross=30 witness_masses=34 witness_cubic=512`.

## What the scanner could not decide

Whether `prior_status` inside `pfp_review` should remain the historical `IMPORTED_ASSUMPTION`. `sync_pfp_results.py` records the current node status there when the decision does not carry a status override, and a status override cannot raise the rank. The review file on disk still describes the imported node. The standing statement does not say the real-p import has been discharged.
