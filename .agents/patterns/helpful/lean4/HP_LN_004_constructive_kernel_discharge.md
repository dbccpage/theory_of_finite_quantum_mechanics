---
pattern_id: HP_LN_004
name: constructive_kernel_discharge
category: healthy_pattern
language: lean4
dual_pattern: AP_LN_004_smuggled_custom_axiom_injection
authority_effect: None
---

# Healthy pattern: Constructive kernel discharge (`HP_LN_004`)

## Description

Discharge the obligation with a proof, or carry the assumption as an explicit hypothesis of the theorem and record it as `imported_structure` on the node.

## Remediation

- Turn `axiom h : P` into a theorem hypothesis `(h : P)` and propagate it to every caller.
- Give the node status CONDITIONAL (or IMPORTED_ASSUMPTION for the assumption itself), never PROVED_LEAN.

## Removes

[AP_LN_004_smuggled_custom_axiom_injection](../../anti/lean4/AP_LN_004_smuggled_custom_axiom_injection.md). Applying this pattern leaves the anti-pattern's signature empty for the change it covers; it does not certify the rest of the file.

Adapted from the_symbol_game card HP_LN_004_constructive_kernel_discharge.md.
