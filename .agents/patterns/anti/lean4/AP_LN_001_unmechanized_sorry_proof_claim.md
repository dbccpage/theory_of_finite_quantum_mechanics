---
pattern_id: AP_LN_001
name: unmechanized_sorry_proof_claim
category: anti_pattern
language: lean4
dual_pattern: HP_LN_001_zero_sorry_axiom_allowlist
authority_effect: None
---

# Anti-pattern: Unmechanized sorry proof claim (`AP_LN_001`)

## Description

A Lean module leaves an obligation open with an admission token while a node, a receipt or prose says the result is mechanized. The campaign honesty gate forbids `sorry`, `admit`, `axiom`, `native_decide` and `unsafe` in added Lean.

## Detection signature

- One of the tokens outside comments and strings (constructor and match-arm names after `|` are not the tactic).
- `#print axioms` output that lists `sorryAx`, or a replay receipt whose axioms exceed the allowed three.

Mechanical check: `scripts/auto/anti_pattern_lint.py` rule AP_LN_001 (added lines with `--changed-since`; every line otherwise); `scripts/overclaim_scan.py` rule R3 for modules cited by a PROVED_LEAN or CONDITIONAL node.

## Hazard

- Every node citing the module is OVERCLAIM until the token is removed and the module is replayed (overclaim rubric, R3).

## Dual healthy pattern

[HP_LN_001_zero_sorry_axiom_allowlist](../../helpful/lean4/HP_LN_001_zero_sorry_axiom_allowlist.md)
