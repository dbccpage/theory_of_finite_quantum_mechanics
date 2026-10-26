---
documentation_contract: education-documentation/v1
title: "Level 09: `swap9_swap`"
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
  - atlas/papers/finite_obstruction_calculus/genesis_ongoing/paper/ninth/paper.md
  - atlas/papers/finite_obstruction_calculus/genesis_ongoing/lean4/Ninth/State.lean
  - atlas/papers/finite_obstruction_calculus/genesis_ongoing/meta/review/derivation_review.md
  - atlas/papers/finite_obstruction_calculus/genesis_ongoing/research/ninth/reading_the_seed.md
last_verified: 2026-10-11
---

# Level 09: `swap9_swap`

**AuthorityEffect:** None.

**Pin:** `dbccpage/H3V7N5QF` at `5d9488324ce976817987bd83a28d901371cfc073`.

**Package:** [`genesis_ongoing`](/atlas/papers/finite_obstruction_calculus/genesis_ongoing).

![Level 09: `swap9_swap`](../_images/genesis_ongoing_09_involution_swap.svg)

The drawing `genesis_ongoing_09_involution_swap.svg` is an education schematic in this documentation tree. The sentences below are taken from the pinned package.

`lean4/Ninth/State.lean` states `theorem swap9_swap (s : NDSt) : s.swap.swap = s`. Applying the ninth swap twice returns the state.

The ninth manuscript is `paper/ninth/paper.md`. The review row says the swap evidence was checked together with the count evidence.

## Research Notes Context: Exchange Symmetry Restoration

`research/ninth/reading_the_seed.md` provides the structural rationale for the swap involution:

1. **Restoration of Broken Symmetry:** In the eighth derivation, the given datum (`arb` asserted in $r$, nothing asserted in $s$) broke the permutation symmetry between the two relations. The ninth seed, starting from an empty state with no given assertions, restores full bilateral exchange symmetry ($r \leftrightarrow s$).
2. **Involution Invariant:** The transformation `swap` transposes multiplicity functions $M_r(x, y) \leftrightarrow M_s(x, y)$ while leaving the underlying term alphabet untouched. `swap9_swap` shows in Lean that `swap` is a strict involution of order 2.
3. **Commutation with Rewriting and Steps:** `swap` commutes with term rewritings $\pi$ and maps each valid step $S \to T$ to an exchange-dual step $S.\text{swap} \to T.\text{swap}$. Consequently, `swap` preserves state size, shortest path costs, and reachability classes.
4. **Symmetric Results Census:** States fixed by `swap` are exactly those where $M_r = M_s$ identically. Their count with $n$ terms and total multiplicity $t$ reduces to the single-relation (seventh derivation) count with $n$ terms and total multiplicity $t/2$ for even $t$, and vanishes for odd $t$.

## Files

- [`paper/ninth/paper.md`](/atlas/papers/finite_obstruction_calculus/genesis_ongoing/paper/ninth/paper.md)
- [`lean4/Ninth/State.lean`](/atlas/papers/finite_obstruction_calculus/genesis_ongoing/lean4/Ninth/State.lean)
- [`meta/review/derivation_review.md`](/atlas/papers/finite_obstruction_calculus/genesis_ongoing/meta/review/derivation_review.md)
- [`research/ninth/reading_the_seed.md`](/atlas/papers/finite_obstruction_calculus/genesis_ongoing/research/ninth/reading_the_seed.md)

