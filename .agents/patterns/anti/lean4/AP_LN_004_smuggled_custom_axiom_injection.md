---
pattern_id: AP_LN_004
name: smuggled_custom_axiom_injection
category: anti_pattern
language: lean4
dual_pattern: HP_LN_004_constructive_kernel_discharge
authority_effect: None
---

# Anti-pattern: Smuggled custom axiom (`AP_LN_004`)

## Description

A custom `axiom` declaration stands in for a hard obligation, and the node or prose then calls the result proved.

## Detection signature

- An `axiom` declaration outside comments.
- `#print axioms` naming anything beyond the allowed three.

Mechanical check: `scripts/auto/anti_pattern_lint.py` rule AP_LN_004; `scripts/overclaim_scan.py` rules R3 and R4.

## Hazard

- A false axiom proves `False`, so every downstream theorem is void. The node is at most CONDITIONAL on a named, imported assumption.

## Dual healthy pattern

[HP_LN_004_constructive_kernel_discharge](../../helpful/lean4/HP_LN_004_constructive_kernel_discharge.md)
