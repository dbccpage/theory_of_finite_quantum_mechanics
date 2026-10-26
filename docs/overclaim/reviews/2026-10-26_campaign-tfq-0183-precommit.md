# Overclaim review: TFQ-0183

- **Date**: 2026-10-26
- **Node**: `TFQ-0183`
- **Branch**: `derive/TFQ-0183`
- **AuthorityEffect**: None

## Scope

The narrowed statement of `TFQ-0183` and `lean4/CampaignTfq0183FourModeDisk.lean`. Status stays OPEN.

## Method

`python -I -X utf8 scripts/overclaim_scan.py --changed-since origin/main --strict` reported HIGH=0, MEDIUM=0, LOW=3. The three LOW rows are `R10` on `TENSOR-ASSUMPTION-COUNTERMODELS` and `R5` on two tensor notes. They are outside this statement. Not rebuilt in this review pass: the Lake build already exited 0 before the scan. No new HIGH finding.

## Result

1 NARROWED, 0 FULL, 0 OVERCLAIM.

## Statement versus theorems

| Claim | Declaration | Verdict |
| --- | --- | --- |
| The counts are 4, 4 and 1 | `CampaignTfq0183FourModeDisk.counts` | FULL |
| 4 - 4 + 1 = 1 | `CampaignTfq0183FourModeDisk.eulerChar` | FULL |
| (4 - 1) - (4 - 1) = 0 | `CampaignTfq0183FourModeDisk.bettiArithmetic` | FULL |
| (1 + 1) mod 2 = 0, 4 * 2 = 8, and 8 mod 2 = 0 | `CampaignTfq0183FourModeDisk.cornerParity` | FULL |
| The mode count 4 is not 2 | `CampaignTfq0183FourModeDisk.fourNeTwo` | FULL |
| Superconducting device, physical Majorana mode, noise-sweep authority, larger-grid matrix rank, crate fence | not proved | NOT PROVED |

The narrowed statement matches the five theorems. The node stays OPEN because that wider fence is not the statement that was proved.

## Axioms

Each `#print axioms` line for the five theorems is empty. Allowed set: `propext`, `Classical.choice`, `Quot.sound`. None of those three appears.

## Numbers recomputed

| Number | Recomputation | Match |
| --- | --- | --- |
| 4, 4, 1 | independent checker modes, channels, islands | match |
| 4 - 4 + 1 = 1 | checker euler | match |
| (4 - 1) - (4 - 1) = 0 | checker prints `betti_arith=0` | match |
| (1 + 1) mod 2 = 0 | checker prints `corner_mod=0` | match |
| 4 * 2 = 8 and 8 mod 2 = 0 | checker prints `ends=8` | match |
| 4 is not 2 | checker assertion `4 != 2` | match |
| matrix ranks 3 and 1, dim_h1 0 | checker only; not a Lean theorem | match the checker, outside the statement |

Independent checker: `checks=482 failed=0`.

## What the scanner could not decide

Whether the integer skeleton should be read as the cell counts of `build_tetron_array(1, 1, Disk)`. The Lean file does not name that function. The checker does, and the bottleneck leaves the device reading outside the statement.
