---
pattern_id: HP_LN_002
name: scoped_target_cache_build
category: healthy_pattern
language: lean4
dual_pattern: AP_LN_002_unconstrained_lake_mathlib_rebuild
authority_effect: None
---

# Healthy pattern: Scoped target build on the Mathlib cache (`HP_LN_002`)

## Description

Fetch the cache, then build only the module that is cited.

## Remediation

- In `lean4/`: `lake exe cache get`, then `lake build <Module>` for the cited module only.
- Check free disk space first (more than 10 GB). Say "not rebuilt" when relying on an existing receipt.

## Removes

[AP_LN_002_unconstrained_lake_mathlib_rebuild](../../anti/lean4/AP_LN_002_unconstrained_lake_mathlib_rebuild.md). Applying this pattern leaves the anti-pattern's signature empty for the change it covers; it does not certify the rest of the file.
