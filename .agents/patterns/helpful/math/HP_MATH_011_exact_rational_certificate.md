---
pattern_id: HP_MATH_011
name: exact_rational_certificate
category: healthy_pattern
language: math
dual_pattern: AP_MATH_011_float_in_exact_certificate
authority_effect: None
---

# Healthy pattern: Exact rational certificate (`HP_MATH_011`)

## Description

Use integers, `fractions.Fraction`, Gaussian rationals or exact SymPy objects throughout, and compare exactly.

## Remediation

- Replace float arithmetic with `Fraction` or `sympy.Rational`; print floats only for display, after the exact comparison.

## Removes

[AP_MATH_011_float_in_exact_certificate](../../anti/math/AP_MATH_011_float_in_exact_certificate.md). Applying this pattern leaves the anti-pattern's signature empty for the change it covers; it does not certify the rest of the file.

Adapted from the_symbol_game card HP_MATH_010_rational_interval_smale_sentry.md.
