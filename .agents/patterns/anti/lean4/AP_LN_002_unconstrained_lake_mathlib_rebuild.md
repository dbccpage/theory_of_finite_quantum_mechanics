---
pattern_id: AP_LN_002
name: unconstrained_lake_mathlib_rebuild
category: anti_pattern
language: lean4
dual_pattern: HP_LN_002_scoped_target_cache_build
authority_effect: None
---

# Anti-pattern: Unconstrained Lake Mathlib rebuild (`AP_LN_002`)

## Description

`lake build` runs in a fresh worktree without the Mathlib cache, so Mathlib compiles from source for hours and fills the disk.

## Detection signature

- `lake build` compiling `Mathlib.*` modules one by one.
- A new worktree's `lean4/.lake` growing past a few gigabytes during a build.

Mechanical check: none; read by hand.

## Hazard

- Timeouts and a full disk; a half-finished build that is later cited as a check.

## Dual healthy pattern

[HP_LN_002_scoped_target_cache_build](../../helpful/lean4/HP_LN_002_scoped_target_cache_build.md)
