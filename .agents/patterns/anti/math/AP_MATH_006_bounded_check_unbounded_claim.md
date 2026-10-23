---
pattern_id: AP_MATH_006
name: bounded_check_unbounded_claim
category: anti_pattern
language: math
dual_pattern: HP_MATH_006_statement_matches_check_bound
authority_effect: None
---

# Anti-pattern: Bounded check, unbounded claim (`AP_MATH_006`)

## Description

A check exhaustive to a small bound, or a single instance closed by `decide`, is written up as a statement about all cases. Overclaim failure class 2.

## Detection signature

- The statement says all, every, unique or iff while the Lean quantifies over a fixed finite range.
- A table of a few rows offered as a non-existence result for the general case.

Mechanical check: partly `scripts/overclaim_scan.py` rule R2 (universal wording over closed instances); otherwise the statement-vs-theorem review.

## Hazard

- The node claims a general law that nothing in the repository proves.

## Dual healthy pattern

[HP_MATH_006_statement_matches_check_bound](../../helpful/math/HP_MATH_006_statement_matches_check_bound.md)

Adapted from the_symbol_game card AP_MATH_006_finite_matrix_promotion_fallacy.md. The source's witnesses are the_symbol_game history and are not repeated here.
