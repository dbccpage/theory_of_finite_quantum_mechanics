---
documentation_contract: education-documentation/v1
title: "Level 13: `Reach5.cycles`"
kind: grammar-reference
audience:
  - researchers
  - engineers
  - coding-agents
status: active
maturity: draft
claim_status: verified
authority_effect: "None"
source_pin: "dbccpage/H3V7N5QF@5d9488324ce976817987bd83a28d901371cfc073"
source_paths:
  - atlas/papers/finite_obstruction_calculus/genesis_ongoing/lean4/Fifth/Reach.lean
  - atlas/papers/finite_obstruction_calculus/genesis_ongoing/lean4/Ninth/Reach.lean
  - atlas/papers/finite_obstruction_calculus/genesis_ongoing/lean4/Sixteenth/Reach.lean
  - atlas/papers/finite_obstruction_calculus/genesis_ongoing/paper/fifth/paper.md
last_verified: 2026-10-08
---

# Level 13: `Reach5.cycles`

**AuthorityEffect:** None.

**Pin:** `dbccpage/H3V7N5QF` at `5d9488324ce976817987bd83a28d901371cfc073`.

**Package:** [`genesis_ongoing`](/atlas/papers/finite_obstruction_calculus/genesis_ongoing).

![Level 13: `Reach5.cycles`](../_images/genesis_ongoing_13_cycle_classification.svg)

The drawing `genesis_ongoing_13_cycle_classification.svg` is an education schematic in this documentation tree. The sentences below are taken from the pinned package.

`lean4/Fifth/Reach.lean` states `theorem Reach5.cycles`: a well-formed nonempty counted state reaches itself in `2 * k` steps for every natural `k`. `cycle2` is the length-2 case.

The same shape is stated again for later carriers: `Reach6.cycles`, `Reach7.cycles`, `Reach8.cycles`, `Reach9.cycles`, and `Reach16.cycles`.

`Reach7` and `Reach9` also have a zero-length fact at the empty beginning: `no_cycle_at_empty` and `no_cycle_at_empty9`.

## Files

- [`lean4/Fifth/Reach.lean`](/atlas/papers/finite_obstruction_calculus/genesis_ongoing/lean4/Fifth/Reach.lean)
- [`lean4/Ninth/Reach.lean`](/atlas/papers/finite_obstruction_calculus/genesis_ongoing/lean4/Ninth/Reach.lean)
- [`lean4/Sixteenth/Reach.lean`](/atlas/papers/finite_obstruction_calculus/genesis_ongoing/lean4/Sixteenth/Reach.lean)
- [`paper/fifth/paper.md`](/atlas/papers/finite_obstruction_calculus/genesis_ongoing/paper/fifth/paper.md)
