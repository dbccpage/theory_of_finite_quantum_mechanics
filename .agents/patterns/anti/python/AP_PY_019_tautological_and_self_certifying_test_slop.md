---
pattern_id: AP_PY_019
name: tautological_and_self_certifying_test_slop
category: anti_pattern
language: python
dual_pattern: HP_PY_019_tests_exercise_the_code
authority_effect: None
---

# Anti-pattern: Tautological test (`AP_PY_019`)

## Description

A test asserts a fact about literals, or raises the exception itself inside `pytest.raises`, so it cannot fail whatever the code does.

## Detection signature

- `assert 2 % 2 == 0`, `assert True`, `assert Fraction(0) == Fraction(0)` written with literals only.
- `with pytest.raises(E): raise E(...)`.

Mechanical check: `scripts/auto/anti_pattern_lint.py` rule AP_PY_019 (an assert over constants only; `pytest.raises` around a bare `raise`).

## Hazard

- The test count rises while nothing is checked; SCORING.md grades a tautological test E for Gate 4.

## Dual healthy pattern

[HP_PY_019_tests_exercise_the_code](../../helpful/python/HP_PY_019_tests_exercise_the_code.md)

Adapted from the_symbol_game card AP_PY_019_tautological_and_self_certifying_test_slop.md. The source's witnesses are the_symbol_game history and are not repeated here.
