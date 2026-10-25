# Overclaim review: PGW-WDP-HANDOFF-TO-L1

**AuthorityEffect:** None.

## Scope

One campaign change on `derive/PGW-WDP-HANDOFF-TO-L1` against `origin/main` `1fa451fe1eac640d84f0c34ba88a71dcdd32dfb6`. Node `PGW-WDP-HANDOFF-TO-L1` stays `OPEN`. Record `TFQ-0558` stays `OPEN_OBLIGATION`. The route `PGW-R-WDP-HANDOFF-TO-L1` stays `GAP_NO_DERIVATION`.

## Method

`python -I -X utf8 scripts/overclaim_scan.py --changed-since origin/main --strict` (exit 0). `python -I -X utf8 scripts/auto/anti_pattern_lint.py --changed-since origin/main` (exit 0). Statement-vs-theorem read of `lean4/CampaignPgwWdpHandoffToL1.lean` against the node statement. `lake build CampaignPgwWdpHandoffToL1` exit 0, module job 944 ms, wall clock 25281 ms. Each `#print axioms` line reports no axioms. Independent checker `python -I -X utf8 checks/independent/pgw-wdp-handoff-to-l1.py` printed `checked 12 claims, failures 0`.

## Result

0 FULL, 1 NARROWED, 0 OVERCLAIM.

The written statement is the three-vertex coboundary. The certified weighted window, the LGGR adapter, sector weights, a quantum state (TFQ-0004), and the L1 stage are outside that statement and stay open in the bottleneck.

## Corrections to the PR's own text

None in this review. The status is not raised.

## Per-node table

| Claim | Declaration | Match |
|---|---|---|
| Vertices 0, 1, 2 with values (0, 1, 0) have coboundary (1, -1, 0) in slot order (01, 12, 02) | `pgwHo_coboundary` | The type is `((1 : Int) - 0, (0 : Int) - 1, (0 : Int) - 0) = (1, -1, 0)` |
| L1 norm of that coboundary is 2 | `pgwHo_leakage` | `(1 : Int).natAbs + (-1 : Int).natAbs + (0 : Int).natAbs = 2` |
| Subtracting that coboundary leaves (0, 0, 0) | `pgwHo_repair` | Each slot difference is `0` |
| Residual L1 is 0 | `pgwHo_residual_l1` | `(0 : Nat) + 0 + 0 = 0` |
| 0 is at most every natural number, so this repair cost is a minimum | `pgwHo_zero_le` | `(n : Nat) : 0 ≤ n`, by `Nat.zero_le` |
| Leakage 2 is not that minimum | `pgwHo_leakage_not_min` | `(2 : Nat) ≠ 0` |
| Oriented sum `1 + (-1) - 0` equals 0 | `pgwHo_oriented` | `(1 : Int) + (-1) - 0 = 0` |
| Certified weighted quotient, LGGR adapter, sector weights, quantum state, L1 stage | none | Not in the statement. Bottleneck keeps them open |

Axioms of all seven declarations: none. The allowed set is `propext`, `Classical.choice`, and `Quot.sound`.

## Numbers recomputed

Integer arithmetic, no floats.

| Number | Recomputation | Result |
|---|---|---|
| coboundary slots | `1 - 0`, `0 - 1`, `0 - 0` | `(1, -1, 0)` match |
| leakage | `abs(1) + abs(-1) + abs(0)` | `2` match |
| residual | `1 - (1 - 0)`, `-1 - (0 - 1)`, `0 - (0 - 0)` | `(0, 0, 0)` match |
| residual L1 | `0 + 0 + 0` | `0` match |
| lower bound | `0 ≤ n` for a natural `n` | stated by `pgwHo_zero_le` |
| separation | `2 ≠ 0` | match |
| oriented sum | `1 + (-1) - 0` | `0` match |

## What the scanner could not decide

`--strict` reported HIGH 0, MEDIUM 0, LOW 3. The LOW rows are pre-existing and are not edited here:

- R10 `TENSOR-ASSUMPTION-COUNTERMODELS`: 5 cited Lean modules in no replay receipt, for example `lean4/TensorCountermodelCones.lean`
- R5 `dag/derivations/10_finite_qm_core/tfq_1019_fq_gap_tensor_uniqueness.md`: number `20261019`
- R5 `dag/derivations/27_tensor_composition/tfq_0413_tensor_assumption_countermodels.md`: numbers `1/2` and `1/4`

`anti_pattern_lint` reported 0 HIGH, 0 MEDIUM, 0 LOW on the changed Lean and Python files. Evidence grade E3 is separate from the OPEN status.
