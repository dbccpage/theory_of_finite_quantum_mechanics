# Overclaim review: PGW-PYTHON-LEAN-CARRIER-BRIDGE

AuthorityEffect: None.

## Scope

The narrowed statement of PGW-PYTHON-LEAN-CARRIER-BRIDGE (record TFQ-0499). Status stays OPEN. No other node is in this review.

## Method

The module `lean4/CampaignPgwPythonLeanCarrierBridge.lean` was read in full and built with `lake build CampaignPgwPythonLeanCarrierBridge` under Lean 4.35.0. It imports the sealed kernel and no Mathlib module. Mathlib v4.35.0 commit 56a005855ea17e0b0958f73ec801ae140b0a1679 was present through a junction and unused by this module. Each `#print axioms` line was read from that build. The independent check `checks/independent/pgw-python-lean-carrier-bridge.py` recomputed both replays with integer steps. Every numeral in the statement was recomputed that way.

## Result

0 FULL, 1 NARROWED, 0 OVERCLAIM.

## Corrections to the PR's own text

None. The statement lists the two histories, the two regimes, and their inequality. A Python-to-Lean refinement stays in the bottleneck.

## Per-node table

| Node | Theorems that discharge it | Verdict | Reason |
|---|---|---|---|
| PGW-PYTHON-LEAN-CARRIER-BRIDGE | `pgwHistoryL_replays`, `pgwHistoryF_replays`, `pgwR2L_ne_R2F`, `pgwReplay_ne`, `pgwData_counts`, `pgwReqs`, `pgwEmpty_carriers`, `pgwHistory_lengths` | NARROWED | Each theorem is a `decide` fact on the two sealed histories. None joins a Python computation to a Lean statement. Status stays OPEN. |

### Statement versus theorem

| Claim | Declaration | Verdict |
|---|---|---|
| the reading-L history has length 7 | `pgwHistory_lengths` | NARROWED |
| that history replays from genesis to R2L | `pgwHistoryL_replays` | NARROWED |
| the reading-F history has length 8 | `pgwHistory_lengths` | NARROWED |
| that history replays from genesis to R2F | `pgwHistoryF_replays` | NARROWED |
| R2L has data count 2 and R2F has data count 3 | `pgwData_counts` | NARROWED |
| R2L requirements are (0, 1) and R2F requirements are (1, 2) | `pgwReqs` | NARROWED |
| both regimes have empty form, instance, and rule lists | `pgwEmpty_carriers` | NARROWED |
| R2L is not R2F | `pgwR2L_ne_R2F` | NARROWED |
| the two replay results are not equal | `pgwReplay_ne` | NARROWED |
| a refinement from Python to Lean | not proved | NOT PROVED |
| token erasure, the license binding, and rung-two track one | not proved | NOT PROVED |

## Numbers recomputed

| Number | Recomputation | Match |
|---|---|---|
| 7 | length of the reading-L event list | match |
| 8 | length of the reading-F event list | match |
| 2 | data count after two admit-datum steps from genesis, supplies ignored | match |
| 3 | data count after three admit-datum steps from genesis, supplies ignored | match |
| (0, 1) | the single impose on reading L, with 0 < 1 < 2 | match |
| (1, 2) | the single impose on reading F, with 1 < 2 < 3 | match |
| 0 | length of each form, instance, and rule list | match |

## Axioms

`pgwHistoryL_replays`, `pgwHistoryF_replays`, and `pgwReplay_ne` depend on propext. `pgwR2L_ne_R2F`, `pgwData_counts`, `pgwReqs`, `pgwEmpty_carriers`, and `pgwHistory_lengths` depend on no axioms. The module contains no `sorry`, no `axiom` declaration, no `native_decide`, and no `unsafe`.

## What the scanner could not decide

The Python histories that stop before a requirement are outside this module. The scanner cannot tell a sealed Lean replay from a refinement; the table above is the decision.
