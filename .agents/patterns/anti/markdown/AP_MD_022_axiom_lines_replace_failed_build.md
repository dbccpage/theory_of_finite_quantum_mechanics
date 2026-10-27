---
pattern_id: AP_MD_022
name: axiom_lines_replace_failed_build
category: anti_pattern
language: markdown
dual_pattern: HP_MD_022_build_exit_before_axiom_lines
authority_effect: None
---

# Anti-pattern: Axiom lines stand in for a failed build (`AP_MD_022`)

## Description

A `lake build` exits non-zero, yet its `does not depend on any axioms` info lines are quoted as evidence that the module is checked.

## Detection signature

- A receipt or note quoting axiom lines from a build whose exit status was not 0, or whose `.olean` was not written.

Mechanical check: none; read by hand.

## Hazard

- A module that did not build is cited as replayed.

## Dual healthy pattern

[HP_MD_022_build_exit_before_axiom_lines](../../helpful/markdown/HP_MD_022_build_exit_before_axiom_lines.md)
