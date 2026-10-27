---
pattern_id: AP_MD_006
name: unchecked_edge_as_proof
category: anti_pattern
language: markdown
dual_pattern: HP_MD_006_scoped_edge_not_proof
authority_effect: None
---

# Anti-pattern: Unchecked edge as proof (`AP_MD_006`)

## Description

A DAG route, a diagram edge or a pointer is presented as a checked derivation while an input is open, a path is missing, or the pointer is background reading.

## Detection signature

- A DERIVED_LEAN, DERIVED_PROSE or COMPUTED route whose inputs include an OPEN or REFUTED node (a route requires all of its inputs).
- An evidence path that does not exist, still cited as a witness.

Mechanical check: partly `scripts/auto/obstruction_scan.py` rule O3 (a derived route with an OPEN or REFUTED input).

## Hazard

- The graph reads as a derivation that does not hold as recorded.

## Dual healthy pattern

[HP_MD_006_scoped_edge_not_proof](../../helpful/markdown/HP_MD_006_scoped_edge_not_proof.md)
