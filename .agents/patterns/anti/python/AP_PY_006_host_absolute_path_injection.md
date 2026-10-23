---
pattern_id: AP_PY_006
name: host_absolute_path_injection
category: anti_pattern
language: python
dual_pattern: HP_PY_006_dynamic_repository_relative_resolution
authority_effect: None
---

# Anti-pattern: Host-absolute path in code (`AP_PY_006`)

## Description

A script hard-codes a path such as `C:\Users\<name>\...` or `/home/<name>/...`, so it runs only on one workstation.

## Detection signature

- A string literal that starts with a drive letter and `Users`, or with `/home/<name>/` or `/Users/<name>/`.

Mechanical check: `scripts/auto/anti_pattern_lint.py` rule AP_PY_006 (string literals in non-test Python).

## Hazard

- The check fails or silently reads another file on CI and on every other machine.

## Dual healthy pattern

[HP_PY_006_dynamic_repository_relative_resolution](../../helpful/python/HP_PY_006_dynamic_repository_relative_resolution.md)

Adapted from the_symbol_game card AP_PY_006_host_absolute_path_injection.md. The source's witnesses are the_symbol_game history and are not repeated here.
