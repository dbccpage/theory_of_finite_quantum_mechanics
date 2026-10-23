---
pattern_id: AP_MATH_011
name: float_in_exact_certificate
category: anti_pattern
language: math
dual_pattern: HP_MATH_011_exact_rational_certificate
authority_effect: None
---

# Anti-pattern: Floating point in an exact certificate (`AP_MATH_011`)

## Description

An independent check or certificate computes with floating point, so the number it reports is an approximation. CONTRIBUTING.md honesty rule 4: a floating-point number is never a certificate.

## Detection signature

- A float literal, `float(...)`, `math.sqrt` or `sympy` `.evalf()` in an independent check.

Mechanical check: `scripts/auto/anti_pattern_lint.py` rule AP_MATH_011 (float literals, `float()`, `math.*` and `.evalf()` in `checks/independent/`).

## Hazard

- Rounding hides a wrong identity or a sign; the check agrees with the prose for the wrong reason.

## Dual healthy pattern

[HP_MATH_011_exact_rational_certificate](../../helpful/math/HP_MATH_011_exact_rational_certificate.md)

Adapted from the_symbol_game card AP_MATH_011_krawczyk_float_leak.md. The source's witnesses are the_symbol_game history and are not repeated here.
