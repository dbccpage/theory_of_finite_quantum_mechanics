---
pattern_id: HP_RS_001
name: shared_cargo_target_cache
category: healthy_pattern
language: rust
dual_pattern: AP_RS_001_worktree_target_duplication
authority_effect: None
---

# Healthy pattern: Shared Cargo target directory (`HP_RS_001`)

## Description

Point every worktree at one `CARGO_TARGET_DIR` outside the worktrees, and prune it between runs.

## Remediation

- Set `CARGO_TARGET_DIR` to a short shared path before `cargo test`; run `cargo clean` there when space is low.

## Removes

[AP_RS_001_worktree_target_duplication](../../anti/rust/AP_RS_001_worktree_target_duplication.md). Applying this pattern leaves the anti-pattern's signature empty for the change it covers; it does not certify the rest of the file.

Adapted from the_symbol_game card HP_RS_001_shared_cargo_target_cache.md.
