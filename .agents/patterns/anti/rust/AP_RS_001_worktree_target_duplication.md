---
pattern_id: AP_RS_001
name: worktree_target_duplication
category: anti_pattern
language: rust
dual_pattern: HP_RS_001_shared_cargo_target_cache
authority_effect: None
---

# Anti-pattern: Cargo target duplicated per worktree (`AP_RS_001`)

## Description

Each git worktree builds `code/rust` into its own `target/`, so several worktrees fill the disk with identical artefacts.

## Detection signature

- Several `code/rust/target` directories of many gigabytes under `.claude/worktrees/`.

Mechanical check: none; read by hand.

## Hazard

- Builds fail when the disk fills; long paths under nested worktrees hit Windows MAX_PATH.

## Dual healthy pattern

[HP_RS_001_shared_cargo_target_cache](../../helpful/rust/HP_RS_001_shared_cargo_target_cache.md)
