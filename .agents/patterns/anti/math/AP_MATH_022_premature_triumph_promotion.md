---
pattern_id: AP_MATH_022
name: premature_triumph_promotion
category: anti_pattern
language: math
dual_pattern: HP_MATH_022_bounded_claim_with_named_assumptions
authority_effect: None
---

# Anti-pattern: Premature triumph promotion (`AP_MATH_022`)

## Description

Prose announces an unconditional or complete result while the DAG records it as conditional on named imports, or as open.

## Detection signature

- Absolute wording (`derives quantum mechanics`, `without any assumptions`) or a node called proved in prose while its status is lower.

Mechanical check: partly `scripts/overclaim_scan.py` rules R6 and R7; otherwise by hand.

## Hazard

- The public text says more than the derivation graph; the project's labels stop meaning anything.

## Dual healthy pattern

[HP_MATH_022_bounded_claim_with_named_assumptions](../../helpful/math/HP_MATH_022_bounded_claim_with_named_assumptions.md)

Adapted from the_symbol_game card AP_MATH_022_premature_triumph_promotion.md. The source's witnesses are the_symbol_game history and are not repeated here.
