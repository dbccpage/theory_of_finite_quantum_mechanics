---
pattern_id: HP_PY_019
name: tests_exercise_the_code
category: healthy_pattern
language: python
dual_pattern: AP_PY_019_tautological_and_self_certifying_test_slop
authority_effect: None
---

# Healthy pattern: Tests that exercise the code (`HP_PY_019`)

## Description

Call the code under test and compare with an expectation that has an independent basis (SCORING.md 3.4).

## Remediation

- Replace the literal assert with a call to the function and a recomputed expectation.
- Inside `pytest.raises`, call the function with the bad input.

## Removes

[AP_PY_019_tautological_and_self_certifying_test_slop](../../anti/python/AP_PY_019_tautological_and_self_certifying_test_slop.md). Applying this pattern leaves the anti-pattern's signature empty for the change it covers; it does not certify the rest of the file.
