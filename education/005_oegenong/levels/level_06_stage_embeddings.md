---
documentation_contract: symbol-game-documentation/v1
title: "Level 06: `Step2.toStep3`"
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
  - ../../../../omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/paper/second/paper.md
  - ../../../../omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/paper/third/paper.md
  - ../../../../omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/research/second/reading_the_seed.md
  - ../../../../omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/research/third/reading_the_seed.md
  - ../../../../omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4/Third/Step.lean
  - ../../../../omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/meta/review/derivation_review.md
last_verified: 2026-10-08
---

# Level 06: `Step2.toStep3`

**AuthorityEffect:** None.

**Pin:** `dbccpage/H3V7N5QF` at `5d9488324ce976817987bd83a28d901371cfc073`.

**Package:** [`001_genesis_ongoing_h3v7n5qf`](../../../../omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf).

![Level 06: `Step2.toStep3`](../_images/genesis_ongoing_06_stage_embeddings.svg)

The drawing `genesis_ongoing_06_stage_embeddings.svg` is an education schematic in this documentation tree. The sentences below are taken from the pinned package.

Derivation 2 keeps three kinds of change. Derivation 3 keeps two. `lean4/Third/Step.lean` states `theorem Step2.toStep3`: a `Step2` between states is a `Step3`. `Step2.toStep` sends that step on into a `Step` of the base.

The review row for the third derivation calls `Step2.toStep3` an exact size increase on the checked finite sequences, and it says the map is a restriction.

The manuscripts are `paper/second/paper.md` and `paper/third/paper.md`.

## Research Working Notes (`research/`)

The working notes trace the progression through the contraction family:

- **Carrying map (`research/second/reading_the_seed.md`):** Under Derivation 2, removal is eliminated. Along any sequence of changes, composite identifications and additions define a term map $q$ preserving all assertions: $q(x) r q(y)$ holds whenever $xry$ held.
- **Poset containment (`research/third/reading_the_seed.md`):** Derivation 3 strikes identification, specializing $q$ to the identity map. The starting state is strictly contained in the ending state. Reachability becomes an antisymmetric partial order without cycles, and each change increases total size by exactly one.

## Files

- [`paper/second/paper.md`](../../../../omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/paper/second/paper.md)
- [`paper/third/paper.md`](../../../../omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/paper/third/paper.md)
- [`research/second/reading_the_seed.md`](../../../../omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/research/second/reading_the_seed.md)
- [`research/third/reading_the_seed.md`](../../../../omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/research/third/reading_the_seed.md)
- [`lean4/Third/Step.lean`](../../../../omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4/Third/Step.lean)
- [`meta/review/derivation_review.md`](../../../../omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/meta/review/derivation_review.md)
