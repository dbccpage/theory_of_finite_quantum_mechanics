# Overclaim review: L1-U1-SELECTOR-OTHER-SEGMENT

- **Date**: 2026-10-26
- **Node**: `L1-U1-SELECTOR-OTHER-SEGMENT`
- **Branch**: `derive/L1-U1-SELECTOR-OTHER-SEGMENT`
- **AuthorityEffect**: None

## Scope

The narrowed statement of `L1-U1-SELECTOR-OTHER-SEGMENT` and `lean4/CampaignL1U1SelectorOtherSegment.lean`. Status stays OPEN.

## Method

`python -I -X utf8 scripts/overclaim_scan.py --changed-since origin/main --strict` reported HIGH=0, MEDIUM=0, LOW=3. The three LOW rows are `R10` on `TENSOR-ASSUMPTION-COUNTERMODELS` and `R5` on the tensor-uniqueness and tensor-countermodel notes. They are outside this statement. The Lake build already exited 0 before the scan. No new HIGH finding.

## Result

1 NARROWED, 0 FULL, 0 OVERCLAIM.

## Statement versus theorems

| Claim | Declaration | Verdict |
| --- | --- | --- |
| The eight powers of (2, 2) modulo 7 are (1, 0), (2, 2), (0, 1), (5, 2), (6, 0), (5, 5), (0, 6), (2, 5), and the next product is (1, 0) | `step1` through `step8` | FULL |
| Each of those eight pairs satisfies x*x + y*y = 1 modulo 7 | `norms` | FULL |
| Every residue pair modulo 7 with that equation is one of the eight | `solutions_iff` | FULL |
| The eight pairs are distinct | `eight_distinct` | FULL |
| 8 = 7 + 1 and 8 is not 4 | `eight` | FULL |
| The seven powers before the return differ from (1, 0) | `earlier_ne_one` | FULL |
| (2, 2) is not an axis pair | `not_axis` | FULL |
| Selection of C or U(1), Gaussian rationals, other moduli, cyclotomic extensions, completion, continuity | not proved | NOT PROVED |

The narrowed statement matches the modulo-7 table. The node stays OPEN because that wider selection is not the statement.

## Axioms

Each `#print axioms` line is empty. Allowed set: `propext`, `Classical.choice`, `Quot.sound`. None of those three appears.

## Numbers recomputed

The independent script `checks/independent/l1-u1-selector-other-segment.py` exited 0: 96 checks, 0 failures. It recomputes the eight powers, the return at step 8, the all 49 candidate pairs and the eight solutions, and 8 = 7 + 1.

Review correction: this is a historical pre-repair review. The current node retains its original selection target and old Gaussian-rational result, with the modulo-7 case separately recorded. Current checker output and acceptance are in `dag/research/pr435_review_lean_replay.json` and `docs/overclaim/reviews/2026-10-26_review-pr-435.md`.
