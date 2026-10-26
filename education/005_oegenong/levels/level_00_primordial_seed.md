---
documentation_contract: symbol-game-documentation/v1
title: "Level 00: the base seed, two terms and `arb`"
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
  - ../../../../omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/paper/paper.md
  - ../../../../omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/paper/claim_ledger.md
  - ../../../../omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/research/reading_the_seed.md
  - ../../../../omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/research/notes.md
  - ../../../../omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/research/identification_only.py
  - ../../../../omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/code/xry/state.py
  - ../../../../omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4/H3V7N5QF/Basic.lean
  - ../../../../omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/prompt/seed_prompt.md
last_verified: 2026-10-08
---

# Level 00: the base seed, two terms and `arb`

**AuthorityEffect:** None.

**Pin:** `dbccpage/H3V7N5QF` at `5d9488324ce976817987bd83a28d901371cfc073`.

**Package:** [`001_genesis_ongoing_h3v7n5qf`](../../../../omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf).

![Level 00: the base seed, two terms and `arb`](../_images/genesis_ongoing_00_primordial_seed.svg)

The drawing `genesis_ongoing_00_primordial_seed.svg` is an education schematic in this documentation tree. The sentences below are taken from the pinned package.

The base manuscript is derivation 1, [`paper/paper.md`](../../../../omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/paper/paper.md). The seed gives terms written with letters, an assertion `xry`, `arb` asserted, no `xrx`, and four changes: identify two terms, remove an assertion, add a term, add an assertion.

`code/xry/state.py` builds what is given with `given(bra, sameness)`. Terms are `a` written 0 and `b` written 1. `arb` is asserted. `bra` is asserted only when the caller passes `bra=True`. `GIVEN_TERMS` is 2 and `GIVEN_ASSERTIONS` is 1.

Lean `given_distinct` and `two_states_on_given_terms` are in `lean4/H3V7N5QF/Basic.lean`. Claim ledger rows D1 and D2 record that `a` and `b` are two terms, and that on those terms exactly two legal states contain `arb`.

N1 and N2 record that `bra` is neither derived nor refuted. N5 records that a statement about the asserting which holds in one finite legal state and fails in another does not follow.

## Research Working Notes (`research/`)

The working research notes record the textual decisions and mathematical properties of the base setting:

- **Lexical decisions (`research/reading_the_seed.md`):** The relation symbol `r` is deliberately omitted from candidate term letters so that expressions parse with an unambiguous single-character relation slot. Directed order is preserved (`arb` is asserted while `bra` is flagged as not given).
- **The closed reading (C2):** The seed flags only `bra` as not given among pairs on `a` and `b`. The closed start contains exactly `a` and `b`. An open reading with additional unmentioned terms yields states reachable by term additions, supporting the closed model without loss of results (D9).
- **Interpretations of "build structure" (C7):** Post-change repair fails because adding terms or identifying terms cannot clear `xrx` once present; only removal restores legality (D5). Preparatory removal reduces to the removal answer. The adopted reading treats "build structure" as an identification-inversion stand-in: adding a new term $t$ and assertion $xrt$ or $trx$ such that identifying $t$ back with $x$ would yield the obstructed outcome.
- **Identifications alone (`research/identification_only.py`):** Across all 238 legal states with $\le 4$ terms under FREE sameness, following unobstructed identifications alone terminates in end states where every pair is related. The end-state term bounds match the graph-coloring / independent-set partition bounds, verified across all 238 states.
- **100-Round horizon (`research/notes.md`):** Cycle-type partitioning of permutations on $n \le 102$ terms creates a combinatorial barrier beyond round 20, leaving unbounded exact orbit counts open (O2).

## Files

- [`paper/paper.md`](../../../../omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/paper/paper.md)
- [`paper/claim_ledger.md`](../../../../omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/paper/claim_ledger.md)
- [`research/reading_the_seed.md`](../../../../omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/research/reading_the_seed.md)
- [`research/notes.md`](../../../../omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/research/notes.md)
- [`research/identification_only.py`](../../../../omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/research/identification_only.py)
- [`code/xry/state.py`](../../../../omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/code/xry/state.py)
- [`lean4/H3V7N5QF/Basic.lean`](../../../../omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4/H3V7N5QF/Basic.lean)
- [`prompt/seed_prompt.md`](../../../../omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/prompt/seed_prompt.md)
