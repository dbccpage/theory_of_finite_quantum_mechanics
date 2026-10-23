---
pattern_id: HP_LN_001
name: zero_sorry_axiom_allowlist
category: healthy_pattern
language: lean4
dual_pattern: AP_LN_001_unmechanized_sorry_proof_claim
authority_effect: None
---

# Healthy pattern: Zero-sorry axiom allowlist (`HP_LN_001`)

## Description

Close every obligation in the kernel. A declaration counts only if it compiles with only `propext`, `Classical.choice` and `Quot.sound`, as shown by its `#print axioms` line and a replay receipt in `dag/research/`.

## Remediation

- Replace the placeholder with a proof, or narrow the node statement to what is proved and write the rest into its bottleneck.
- Record the `#print axioms` line for every cited declaration and re-pin the replay receipt.

## Removes

[AP_LN_001_unmechanized_sorry_proof_claim](../../anti/lean4/AP_LN_001_unmechanized_sorry_proof_claim.md). Applying this pattern leaves the anti-pattern's signature empty for the change it covers; it does not certify the rest of the file.

Adapted from the_symbol_game card HP_LN_001_zero_sorry_axiom_allowlist.md.
