---
pattern_id: HP_PY_009
name: recomputed_binding
category: healthy_pattern
language: python
dual_pattern: AP_PY_009_stale_binding_hash
authority_effect: None
---

# Healthy pattern: Recomputed binding (`HP_PY_009`)

## Description

Recompute the digest from the bytes at the moment of recording, and re-pin whenever the source changes.

## Remediation

- Rebuild and re-pin the replay receipt in the same PR as the Lean change.
- Append a new score record to the companion when the source changes; never edit the old one.

## Removes

[AP_PY_009_stale_binding_hash](../../anti/python/AP_PY_009_stale_binding_hash.md). Applying this pattern leaves the anti-pattern's signature empty for the change it covers; it does not certify the rest of the file.

Adapted from the_symbol_game card HP_PY_009_recomputed_binding.md.
