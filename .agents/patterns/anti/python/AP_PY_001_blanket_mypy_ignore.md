---
pattern_id: AP_PY_001
name: blanket_mypy_ignore
category: anti_pattern
language: python
dual_pattern: HP_PY_001_scoped_mypy_overrides
authority_effect: None
---

# Anti-pattern: Blanket type ignore (`AP_PY_001`)

## Description

`# type: ignore` with no error code silences every type error on the line, including ones introduced later.

## Detection signature

- A `# type: ignore` comment not followed by `[code]`.

Mechanical check: `scripts/auto/anti_pattern_lint.py` rule AP_PY_001 (LOW).

## Hazard

- Real type errors pass review unseen.

## Dual healthy pattern

[HP_PY_001_scoped_mypy_overrides](../../helpful/python/HP_PY_001_scoped_mypy_overrides.md)

Adapted from the_symbol_game card AP_PY_001_blanket_mypy_ignore.md. The source's witnesses are the_symbol_game history and are not repeated here.
