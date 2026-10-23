---
pattern_id: HP_PY_001
name: scoped_mypy_overrides
category: healthy_pattern
language: python
dual_pattern: AP_PY_001_blanket_mypy_ignore
authority_effect: None
---

# Healthy pattern: Scoped type ignore (`HP_PY_001`)

## Description

Name the error code: `# type: ignore[attr-defined]`, or fix the type.

## Remediation

- Run mypy on the file, read the code it reports for the line, and scope the ignore to it.

## Removes

[AP_PY_001_blanket_mypy_ignore](../../anti/python/AP_PY_001_blanket_mypy_ignore.md). Applying this pattern leaves the anti-pattern's signature empty for the change it covers; it does not certify the rest of the file.

Adapted from the_symbol_game card HP_PY_001_scoped_mypy_overrides.md.
