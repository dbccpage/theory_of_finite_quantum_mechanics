---
documentation_contract: symbol-game-documentation/v1
title: "Level 18: leftover feedback, `Reach16.unbounded`"
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
  - ../../../../omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/paper/tenth/paper.md
  - ../../../../omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/paper/sixteenth/paper.md
  - ../../../../omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/research/sixteenth/reading_the_seed.md
  - ../../../../omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4/Sixteenth/Reach.lean
last_verified: 2026-10-08
---

# Level 18: leftover feedback, `Reach16.unbounded`

**AuthorityEffect:** None.

**Pin:** `dbccpage/H3V7N5QF` at `5d9488324ce976817987bd83a28d901371cfc073`.

**Package:** [`001_genesis_ongoing_h3v7n5qf`](../../../../omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf).

![Level 18: leftover feedback, `Reach16.unbounded`](../_images/genesis_ongoing_18_leftovers_unboundedness.svg)

The drawing `genesis_ongoing_18_leftovers_unboundedness.svg` is an education schematic in this documentation tree. The sentences below are taken from the pinned package.

Derivation 10 records a leftover on each change and keeps the ninth state model. Derivation 16 admits the leftover back into the state. The manuscript is `paper/sixteenth/paper.md`.

`lean4/Sixteenth/Reach.lean` states `Reach16.unbounded`: if `Reach16 s t n` from a well-formed state with a term, then `Reach16 s t (2 * k + n)` for every `k`. The comment says the lengths are unbounded because the feedback does not terminate.

`admit_remove_unbounded` says `ara` reaches itself in `2 * k` changes by removing and admitting, for every `k`.

## Research Working Notes (`research/`)

The working notes for the sixteenth derivation (`research/sixteenth/reading_the_seed.md`) detail the dynamical feedback transition:

- **From passive record to active carrier:** Derivation 10 treated leftovers as terminal records in a side ledger. Derivation 16 admits leftovers back into the active state, closing a feedback loop.
- **Unbounded path generation:** Because admitted leftovers can be removed and subsequently re-admitted, reachability between states is no longer uniquely length-determined; recurrent cycles emerge and paths expand indefinitely (`Reach16.unbounded`).

## Files

- [`paper/tenth/paper.md`](../../../../omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/paper/tenth/paper.md)
- [`paper/sixteenth/paper.md`](../../../../omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/paper/sixteenth/paper.md)
- [`research/sixteenth/reading_the_seed.md`](../../../../omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/research/sixteenth/reading_the_seed.md)
- [`lean4/Sixteenth/Reach.lean`](../../../../omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4/Sixteenth/Reach.lean)
