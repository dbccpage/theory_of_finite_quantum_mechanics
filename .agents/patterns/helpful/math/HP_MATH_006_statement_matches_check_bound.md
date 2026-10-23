---
pattern_id: HP_MATH_006
name: statement_matches_check_bound
category: healthy_pattern
language: math
dual_pattern: AP_MATH_006_bounded_check_unbounded_claim
authority_effect: None
---

# Healthy pattern: Statement matches the bound of the check (`HP_MATH_006`)

## Description

State the finite instance that is proved, and write the general case into the bottleneck as open.

## Remediation

- Compare every bound in the Lean with every quantifier in the statement; narrow the statement to the bound.

## Removes

[AP_MATH_006_bounded_check_unbounded_claim](../../anti/math/AP_MATH_006_bounded_check_unbounded_claim.md). Applying this pattern leaves the anti-pattern's signature empty for the change it covers; it does not certify the rest of the file.

Adapted from the_symbol_game card HP_MATH_021_bounded_claim_hygiene_and_receipt_attestation.md.
