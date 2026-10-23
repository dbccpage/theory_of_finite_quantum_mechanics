---
pattern_id: HP_MD_006
name: scoped_edge_not_proof
category: healthy_pattern
language: markdown
dual_pattern: AP_MD_006_unchecked_edge_as_proof
authority_effect: None
---

# Healthy pattern: A route is only as held as its inputs (`HP_MD_006`)

## Description

Give a route the status its weakest input allows: GAP_NO_DERIVATION or CONDITIONAL_ON_IMPORT when an input is open or imported, or drop the input if the proof does not use it.

## Remediation

- Read the output's Lean: if the open input is not used, remove it from the route; if it is used, lower the route and the output.

## Removes

[AP_MD_006_unchecked_edge_as_proof](../../anti/markdown/AP_MD_006_unchecked_edge_as_proof.md). Applying this pattern leaves the anti-pattern's signature empty for the change it covers; it does not certify the rest of the file.

Adapted from the_symbol_game card HP_MD_006_scoped_edge_not_proof.md.
