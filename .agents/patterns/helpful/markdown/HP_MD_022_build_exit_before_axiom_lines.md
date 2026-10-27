---
pattern_id: HP_MD_022
name: build_exit_before_axiom_lines
category: healthy_pattern
language: markdown
dual_pattern: AP_MD_022_axiom_lines_replace_failed_build
authority_effect: None
---

# Healthy pattern: Build exit status before axiom lines (`HP_MD_022`)

## Description

Record the build's exit status first; only a build that exited 0 may contribute axiom lines to a receipt.

## Remediation

- Keep the exit status and the toolchain pin in the replay receipt next to the axioms list.

## Removes

[AP_MD_022_axiom_lines_replace_failed_build](../../anti/markdown/AP_MD_022_axiom_lines_replace_failed_build.md). Applying this pattern leaves the anti-pattern's signature empty for the change it covers; it does not certify the rest of the file.
