# Overclaim review: PGW-WDP-HANDOFF-TO-L1

AuthorityEffect: None.

## Scope

The narrowed statement of PGW-WDP-HANDOFF-TO-L1 (record TFQ-0558). Status stays OPEN. No other node is in this review.

## Method

The module `lean4/CampaignPgwWdpHandoffToL1.lean` was read in full and built with `lake build CampaignPgwWdpHandoffToL1` under Lean 4.35.0. It has no import. Mathlib v4.35.0 commit 56a005855ea17e0b0958f73ec801ae140b0a1679 was present through a junction and unused by this module. Each `#print axioms` line was read from that build. The independent check `checks/independent/pgw-wdp-handoff-to-l1.py` recomputed the concrete values and a finite integer box with exact integers. Every numeral in the narrowed statement was recomputed that way. The Python box does not discharge a Lean quantifier over every integer.

## Result

0 FULL, 1 NARROWED, 0 OVERCLAIM.

## Corrections to the PR's own text

None. The statement is the one-triangle case. The weighted rational certificate, the bounded-circulation dual, the LGGR adapter, sector weights, and the L1 stage stay in the bottleneck. Status stays OPEN.

## Per-node table

| Node | Theorems that discharge it | Verdict | Reason |
|---|---|---|---|
| PGW-WDP-HANDOFF-TO-L1 | `distance_at_least`, `repair_residual_neg`, `repair_residual_nonneg`, `meet_neg`, `meet_nonneg`, `face_zero_is_coboundary`, `leakage_is_not_quotient`, `face_of_obstruction`, `obstructed_verdict`, `closed_verdict`, `equal_report_passes`, `unequal_report_fails` | NARROWED | The theorems are the unit-weight integer triangle. They do not certify a weighted rational window or identify the quotient with a coboundary length. Status stays OPEN. |

### Statement versus theorem

| Claim | Declaration | Verdict |
|---|---|---|
| coboundary on the triangle is (f1 - f0, f2 - f1, f2 - f0) | `d0` and `d0_components` | NARROWED |
| face is x01 + x12 - x02 | `face` | NARROWED |
| every integer residual has unit l1 length at least the absolute face value | `distance_at_least` | NARROWED |
| the negative-face repair leaves residual (0, 0, -face) | `repair_picks_neg`, `repair_residual_neg` | NARROWED |
| the other repair leaves residual (face, 0, 0) | `repair_picks_nonneg`, `repair_residual_nonneg` | NARROWED |
| both residuals have unit l1 length equal to the absolute face value | `meet_neg`, `meet_nonneg` | NARROWED |
| a face of 0 is the coboundary of the non-negative repair | `face_zero_is_coboundary` | NARROWED |
| vertex values (0, 1, 0) have coboundary length 2 | `leakage_of_repair_vertex` | NARROWED |
| the edge triple (1, -1, 0) is that coboundary and its self-residual has length 0 | `coboundary_of_repair_vertex`, `quotient_of_that_coboundary` | NARROWED |
| 2 is not that quotient value | `leakage_is_not_quotient` | NARROWED |
| the edge triple (1, 0, 0) has face 1 | `face_of_obstruction` | NARROWED |
| the verdict of (1, 1) is 0 | `obstructed_verdict` | NARROWED |
| the verdict of (0, 0) is 1 | `closed_verdict` | NARROWED |
| fibre decisions (1, 1) pass and (0, 1) do not | `equal_report_passes`, `unequal_report_fails` | NARROWED |
| weighted l1 over the rationals | not proved | NOT PROVED |
| bounded circulation on a general carrier | not proved | NOT PROVED |
| the LGGR adapter and the identification with a coboundary length | not proved | NOT PROVED |
| sector weights, a quantum state, and the L1 stage | not proved | NOT PROVED |
| the same zero-face fact on a general complex | not proved | NOT PROVED |

## Numbers recomputed

| Number | Recomputation | Match |
|---|---|---|
| 2 | unit l1 length of (1, -1, 0), the coboundary of (0, 1, 0) | match |
| 0 | unit l1 length of (1, -1, 0) minus itself | match |
| 1 | face of (1, 0, 0), and also the closed verdict of (0, 0) | match |
| 0 | obstructed verdict of (1, 1) | match |
| 16778 | conditions counted by the independent check | match |
| 0 | failures counted by that check | match |

## Axioms

`face_of_coboundary`, `l1_ge_face`, `distance_at_least`, `meet_neg`, and `meet_nonneg` depend on propext and Quot.sound. `repair_residual_neg`, `repair_residual_nonneg`, and `face_zero_is_coboundary` depend on propext, Classical.choice, and Quot.sound. The remaining printed theorems depend on no axioms. The module contains no `sorry`, no `axiom` declaration, no `native_decide`, and no `unsafe`.

## What the scanner could not decide

`scripts/overclaim_scan.py --changed-since origin/main --strict` reported HIGH 0, MEDIUM 0, LOW 3. The three LOW findings are R10 on TENSOR-ASSUMPTION-COUNTERMODELS and two R5 notes in files the evidence refresh already carried. They were left unchanged.

A Python loop over integers from -2 to 2 does not prove a statement quantified over every integer. Those universal claims are the Lean theorems named above. The scanner cannot tell this triangle from the original weighted window; the table above is the decision.
