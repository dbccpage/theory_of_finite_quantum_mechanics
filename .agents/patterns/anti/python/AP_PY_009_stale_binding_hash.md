---
pattern_id: AP_PY_009
name: stale_binding_hash
category: anti_pattern
language: python
dual_pattern: HP_PY_009_recomputed_binding
authority_effect: None
---

# Anti-pattern: Stale binding hash (`AP_PY_009`)

## Description

A receipt or a contract companion records a sha256 for a source that has since changed, or names a commit other than the one whose bytes were hashed. The digest is well formed and names the wrong bytes.

## Detection signature

- A replay receipt's `sha256` differs from the current file (CRLF-folded hash also checked by R4).
- A `*.contract.score.yaml` whose `source_sha256` or `artifact.sha256` differs from the source's current bytes.

Mechanical check: partly `scripts/overclaim_scan.py` rule R4 (replay receipts) and `scripts/contract_scores.py check` (companion history bytes); otherwise by hand.

## Hazard

- A reader treats the receipt as evidence for code it does not bind.

## Dual healthy pattern

[HP_PY_009_recomputed_binding](../../helpful/python/HP_PY_009_recomputed_binding.md)
