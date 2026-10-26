# Overclaim review: OPS-RUST-RECEIPTS-AND-LIMITS

Scope: precommit campaign narrowing of `OPS-RUST-RECEIPTS-AND-LIMITS`. AuthorityEffect: None.

Method: the node statement was split into atomic claims and matched to `lean4/CampaignOpsRustReceiptsAndLimits.lean`. `lake build CampaignOpsRustReceiptsAndLimits` exited 0. `#print axioms` reports no axioms on the twelve theorems. `python -I -X utf8 checks/independent/ops-rust-receipts-and-limits.py` printed `checks=12 failures=0`. `scripts/overclaim_scan.py --changed-since origin/main --strict` reported HIGH 0, MEDIUM 0, LOW 9. The LOW rows are on other nodes (`TENSOR-ASSUMPTION-COUNTERMODELS`, `OPS-PARITY-CYCLE-DESCENT-NCF`, `OPS-TEST-482-REPAIR`, and older notes). They are not claims added by this statement.

Result: 0 FULL, 1 NARROWED, 0 OVERCLAIM. Status stays CONDITIONAL. The narrowed arithmetic is matched. The original Rust receipt rows are not proved, and there is no DERIVED_LEAN route, so the status is not raised.

## Statement versus theorem

| Claim | Lean declaration | Verdict |
| --- | --- | --- |
| maxGlobal = 2^20 | `CampaignOpsRustReceiptsAndLimits.maxGlobal_eq_pow` | FULL |
| maxGlobal = 1048576 | `CampaignOpsRustReceiptsAndLimits.maxGlobal_eq_decimal` | FULL |
| maxLp = 2^22 | `CampaignOpsRustReceiptsAndLimits.maxLp_eq_pow` | FULL |
| maxLp = 4194304 | `CampaignOpsRustReceiptsAndLimits.maxLp_eq_decimal` | FULL |
| 2^64 > maxGlobal | `CampaignOpsRustReceiptsAndLimits.sixty_four_assignments_above` | FULL |
| 2^21 = 2097152 | `CampaignOpsRustReceiptsAndLimits.twenty_one_sections_eq` | FULL |
| 2^21 > maxGlobal | `CampaignOpsRustReceiptsAndLimits.twenty_one_sections_above` | FULL |
| 10 * 2 = 20 | `CampaignOpsRustReceiptsAndLimits.ten_rows` | FULL |
| 2^10 = 1024 | `CampaignOpsRustReceiptsAndLimits.ten_assignments` | FULL |
| 20 * 1024 = 20480 | `CampaignOpsRustReceiptsAndLimits.ten_entries` | FULL |
| 2^10 < maxGlobal | `CampaignOpsRustReceiptsAndLimits.ten_assignments_inside` | FULL |
| 20 * 1024 < maxLp | `CampaignOpsRustReceiptsAndLimits.ten_entries_inside` | FULL |
| zero duality gap, dual inequality, tamper or shape rejection, rebuilt linear programme, singleton census, Rust refusal | not proved | NOT PROVED |

## Numbers recomputed

| Number | Recomputation | Match |
| --- | --- | --- |
| 1048576 | 2**20 | match |
| 4194304 | 2**22 | match |
| 2097152 | 2**21 | match |
| 1024 | 2**10 | match |
| 20 | 10 * 2 | match |
| 20480 | 20 * 1024 | match |

The independent script exits 0. No float is used.

## What the scanner could not decide

Whether a later reader will treat `2^64` as a completed Rust census of 64 singletons. The statement now says that census is not in the statement, and the Lean file has no singleton object.
