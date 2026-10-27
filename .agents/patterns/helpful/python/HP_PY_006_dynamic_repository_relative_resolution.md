---
pattern_id: HP_PY_006
name: dynamic_repository_relative_resolution
category: healthy_pattern
language: python
dual_pattern: AP_PY_006_host_absolute_path_injection
authority_effect: None
---

# Healthy pattern: Repository-relative path resolution (`HP_PY_006`)

## Description

Resolve paths from the script: `ROOT = Path(__file__).resolve().parents[n]`, or take them as arguments.

## Remediation

- Replace the literal with a path built from `ROOT`, or a command-line option with a repository-relative default.

## Removes

[AP_PY_006_host_absolute_path_injection](../../anti/python/AP_PY_006_host_absolute_path_injection.md). Applying this pattern leaves the anti-pattern's signature empty for the change it covers; it does not certify the rest of the file.
