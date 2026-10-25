# Overclaim review: MAJ-OPEN-LINDBLAD-TRANSFER-ENVELOPE

AuthorityEffect: None.

## Scope

The narrowed statement of MAJ-OPEN-LINDBLAD-TRANSFER-ENVELOPE (record TFQ-1177). Status stays OPEN. No other node is in this review.

## Method

The module `lean4/CampaignMajOpenLindbladTransferEnvelope.lean` was read in full. The campaign build `lake build CampaignMajOpenLindbladTransferEnvelope` under Lean 4.35.0 exited 0 before this review; this review did not rebuild it and uses that receipt. The module has no import. Mathlib v4.35.0 commit 56a005855ea17e0b0958f73ec801ae140b0a1679 was present through a junction and unused by this module. Each `#print axioms` line in the receipt names no axioms. The independent check `checks/independent/maj-open-lindblad-transfer-envelope.py` recomputed the same integers and printed `checked 19 conditions, 0 failures`. Every numeral in the narrowed statement was recomputed that way.

## Result

0 FULL, 1 NARROWED, 0 OVERCLAIM.

## Corrections to the PR's own text

None. The statement is the integer comparison at T = 1, 2 and 3. The Lindblad derivation, the four-mode model, the exponential poisoning term, the Landau-Zener square, and a positive lower bound on the physical transfer defect stay in the bottleneck. Status stays OPEN.

## Per-node table

| Node | Theorems that discharge it | Verdict | Reason |
|---|---|---|---|
| MAJ-OPEN-LINDBLAD-TRANSFER-ENVELOPE | `envelope_at_one`, `envelope_at_two`, `envelope_at_three`, `envelope_positive`, `defect_zero_below_envelope` | NARROWED | The theorems are five `decide` facts on `f(T) = 4 + T * T * T` and `comparison(T) = 3 * T * T` at three values, plus `0 < f 2`. They do not derive a Lindblad envelope. Status stays OPEN. |

### Statement versus theorem

| Claim | Declaration | Verdict |
|---|---|---|
| f(1) = 5 and that value is greater than comparison(1) = 3 | `envelope_at_one` | NARROWED |
| f(2) = 12 and comparison(2) = 12 | `envelope_at_two` | NARROWED |
| f(3) = 31 and that value is greater than comparison(3) = 27 | `envelope_at_three` | NARROWED |
| the value 12 is positive | `envelope_positive` | NARROWED |
| 0 is strictly below f(2) | `defect_zero_below_envelope` | NARROWED |
| a positive envelope value does not force a transfer defect to be positive | `defect_zero_below_envelope` together with `envelope_positive` | NARROWED |
| the Lindblad derivation for four modes | not proved | NOT PROVED |
| the exponential poisoning term and the Landau-Zener square | not proved | NOT PROVED |
| a positive lower bound on the physical transfer defect | not proved | NOT PROVED |

## Numbers recomputed

| Number | Recomputation | Match |
|---|---|---|
| 4 | constant term of f, and T^2 at T = 2 (`2 * 2`) | match |
| 1 | the time T = 1, and `4 + 1 = 5` | match |
| 5 | `f(1)` | match |
| 3 | `comparison(1)`, and the coefficient in `3 * 4 = 12` | match |
| 2 | the time T = 2 | match |
| 8 | `2 * 2 * 2` and `2 * 4` | match |
| 12 | `f(2)`, `comparison(2)`, `4 + 8`, and `3 * 4` | match |
| 31 | `f(3)` and `4 + 27` | match |
| 27 | `comparison(3)` and `3 * 3 * 3` | match |
| 0 | the reading strictly below `f(2)`, and the failure count of the independent check | match |
| 19 | conditions counted by the independent check | match |

## Axioms

`envelope_at_one`, `envelope_at_two`, `envelope_at_three`, `envelope_positive`, and `defect_zero_below_envelope` depend on no axioms. The module contains no `sorry`, no `axiom` declaration, no `native_decide`, and no `unsafe`.

## What the scanner could not decide

`scripts/overclaim_scan.py --changed-since origin/main --strict` reported HIGH 0, MEDIUM 0, LOW 3. Those LOW findings are R10 on TENSOR-ASSUMPTION-COUNTERMODELS and R5 on the refreshed notes for FQ-GAP-TENSOR-UNIQUENESS (`20261019`) and TENSOR-ASSUMPTION-COUNTERMODELS (`1/2`, `1/4`). They were left unchanged.

These three `decide` facts do not derive the source Lindblad envelope. The scanner cannot tell this integer stand-in from that physical bound; the table above is the decision.
