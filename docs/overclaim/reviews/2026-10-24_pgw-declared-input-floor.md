# Overclaim review: PGW-DECLARED-INPUT-FLOOR

AuthorityEffect: None.

## Scope

The narrowed statement of PGW-DECLARED-INPUT-FLOOR (record TFQ-0498). Status stays OPEN. No other node is in this review.

## Method

The module `lean4/CampaignPgwDeclaredInputFloor.lean` was read in full and built with `lake build CampaignPgwDeclaredInputFloor` under Lean 4.35.0. Mathlib v4.35.0 is commit 56a005855ea17e0b0958f73ec801ae140b0a1679, reached through a junction and not imported by this module. Each `#print axioms` line was read from that build. The independent check `checks/independent/pgw-declared-input-floor.py` was run with `python -I -X utf8`. Every numeral in the statement was recomputed from the constants parsed out of the Lean file.

## Result

0 FULL, 1 NARROWED, 0 OVERCLAIM.

## Corrections to the PR's own text

None. The statement lists the seven declared numerals and the comparisons the theorems state. The floor, the reduction below two past the bounds, the four-engine carry-forward, and the other completion-gate reading stay in the bottleneck.

## Per-node table

| Node | Theorems that discharge it | Verdict | Reason |
|---|---|---|---|
| PGW-DECLARED-INPUT-FLOOR | `pgwBounds_values`, `pgwInput_eq_items`, `pgwOne_below_input`, `pgwGuard_above_rounds`, `pgwEngines_ne_readings`, `pgwStrictlyBelow_list`, `pgwStrictlyBelow_length`, `pgwCeiling_not_below` | NARROWED | Each theorem is a `decide` fact on the declared numerals. None states a floor, a reduction past the bounds, an engine run, or a reading of the completion gate. Status stays OPEN. |

### Statement versus theorem

| Claim | Declaration | Verdict |
|---|---|---|
| rounds = 15, guard = 250, data ceiling = 4, item bound = 2, input count = 2, engines = 4, readings = 2 | `pgwBounds_values` | NARROWED |
| input count equals the item bound | `pgwInput_eq_items` | NARROWED |
| 1 is strictly below the input count | `pgwOne_below_input` | NARROWED |
| the guard is strictly above the round count | `pgwGuard_above_rounds` | NARROWED |
| the engine count is not the reading count | `pgwEngines_ne_readings` | NARROWED |
| candidates 0, 1, 2, 3, 4 filtered by a strict bound of 4 are 0, 1, 2, 3 | `pgwStrictlyBelow_list` | NARROWED |
| that filtered list has length 4 | `pgwStrictlyBelow_length` | NARROWED |
| the ceiling is not strictly below 4 | `pgwCeiling_not_below` | NARROWED |
| a floor for the declared-input count | not proved | NOT PROVED |
| a reduction below two past the bounds | not proved | NOT PROVED |
| four engines carry the grammar forward | not proved | NOT PROVED |
| the other reading of the completion gate | not proved | NOT PROVED |

## Numbers recomputed

| Number | Recomputation | Match |
|---|---|---|
| 15 | parsed `pgwRounds` | match |
| 250 | parsed `pgwGuard` | match |
| 4 | parsed `pgwDataCeiling` | match |
| 2 | parsed `pgwItemBound` and `pgwInputCount` | match |
| 4 | parsed `pgwEngines` | match |
| 2 | parsed `pgwReadings` | match |
| 1 < 2 | integer comparison on the parsed input count | match |
| 15 < 250 | integer comparison on the parsed round count and guard | match |
| 4 ≠ 2 | integer comparison on the parsed engine and reading counts | match |
| 0, 1, 2, 3 | filter of 0, 1, 2, 3, 4 by `n < 4` | match |
| 4 | length of that filter | match |
| false | `4 < 4` | match |

## Axioms

`pgwBounds_values`, `pgwInput_eq_items`, `pgwOne_below_input`, `pgwGuard_above_rounds`, `pgwEngines_ne_readings`, `pgwStrictlyBelow_list`, `pgwStrictlyBelow_length`, and `pgwCeiling_not_below` each do not depend on any axioms. The module contains no `sorry`, `admit`, `axiom` declaration, `native_decide`, or `unsafe`.

## What the scanner could not decide

The original prose that four engines carry a grammar forward is a computation at declared bounds in the source papers. This module does not rerun that computation. The scanner cannot tell a bound record from a floor; the table above is the decision.
