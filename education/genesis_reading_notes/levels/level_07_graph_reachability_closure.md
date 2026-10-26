---
documentation_contract: education-documentation/v1
title: "Level 07: D9 and N5"
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
  - atlas/papers/finite_obstruction_calculus/genesis_ongoing/paper/claim_ledger.md
  - atlas/papers/finite_obstruction_calculus/genesis_ongoing/paper/paper.md
  - atlas/papers/finite_obstruction_calculus/genesis_ongoing/lean4/H3V7N5QF/Paths.lean
last_verified: 2026-10-08
---

# Level 07: D9 and N5

**AuthorityEffect:** None.

**Pin:** `dbccpage/H3V7N5QF` at `5d9488324ce976817987bd83a28d901371cfc073`.

**Package:** [`genesis_ongoing`](/atlas/papers/finite_obstruction_calculus/genesis_ongoing).

![Level 07: D9 and N5](../_images/genesis_ongoing_07_graph_reachability_closure.svg)

The drawing `genesis_ongoing_07_graph_reachability_closure.svg` is an education schematic in this documentation tree. The sentences below are taken from the pinned package.

Claim D9 says every finite legal state with at least one term, names anywhere, is a result under either beginning. The Lean witnesses named in the ledger for names at `a = 0`, `b = 1` or `a = b = 0` are `reach_by_edits`, `givenA_to_oneTerm`, and `givenB_to_oneTerm`. Names elsewhere are the rewriting step, open in Lean as O3.

N5 says that any statement about the asserting which holds in one finite legal state and fails in another does not follow, and it cites D9.

Both rows are in `paper/claim_ledger.md`. The exploration inside the declared bound is D12.

## Files

- [`paper/claim_ledger.md`](/atlas/papers/finite_obstruction_calculus/genesis_ongoing/paper/claim_ledger.md)
- [`paper/paper.md`](/atlas/papers/finite_obstruction_calculus/genesis_ongoing/paper/paper.md)
- [`lean4/H3V7N5QF/Paths.lean`](/atlas/papers/finite_obstruction_calculus/genesis_ongoing/lean4/H3V7N5QF/Paths.lean)
