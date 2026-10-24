# [TFQ-0490] k-item-delta-grammar

> **Stage**: `GENESIS` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `c06b7aeb-a75f-538e-ad42-b19e32eb4eee`  
> **Parent Derivation**: [TFQ-0488](tfq_0488_declared_challenge_import_per_level.md)

---

## 1. Abstract & Formal Statement

Narrowed boundary, status left OPEN: the four declared Challenge 3 lists copied from deltaU0, deltaU1, deltaBL, and deltaBD each have length 2. Their new-form arities are 1, 1, 2, and 2, and the sum of those arities is 6. The argument lists are [0], [1], [0, 1], and [0, 0], and the four lists are pairwise distinct across 6 comparisons. One three-item list has length 3, and 3 > 2. This census is those four named lists. A k-item grammar for k at least 3, an exhaustive cost-two enumeration, and a response-size bound stay open. Status stays OPEN.

### Governing Obligation
Keep the four-list census separate from a k-item grammar. Defining that grammar for k at least 3, with the pruning lemmas it relies on, and certifying a pruned enumeration against the unpruned space stay open.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> The four lists are a copied census of deltaU0, deltaU1, deltaBL, and deltaBD. They are not an exhaustive enumeration of the sealed candidate space, and they do not define a k-item grammar for k at least 3. The cost-two minimum CL-3-MIN-TWO stays relative to the sealed grammar. A bound on response size stays open. Status stays OPEN.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/CampaignPgwKItemDeltaGrammar.lean::pgwKItem_arities`](../../../lean4/CampaignPgwKItemDeltaGrammar.lean)
- [`lean4/CampaignPgwKItemDeltaGrammar.lean::pgwKItem_arity_sum`](../../../lean4/CampaignPgwKItemDeltaGrammar.lean)
- [`lean4/CampaignPgwKItemDeltaGrammar.lean::pgwKItem_lengths`](../../../lean4/CampaignPgwKItemDeltaGrammar.lean)
- [`lean4/CampaignPgwKItemDeltaGrammar.lean::pgwKItem_pairwise`](../../../lean4/CampaignPgwKItemDeltaGrammar.lean)
- [`lean4/CampaignPgwKItemDeltaGrammar.lean::pgwKItem_three_above_two`](../../../lean4/CampaignPgwKItemDeltaGrammar.lean)
- [`lean4/CampaignPgwKItemDeltaGrammar.lean::pgwKItem_three_length`](../../../lean4/CampaignPgwKItemDeltaGrammar.lean)
- [`lean4/Imported/Genesis19l57g1/Derivation/Mention.lean::collapsed_fresh_datum`](../../../lean4/Imported/Genesis19l57g1/Derivation/Mention.lean)
- [`lean4/Imported/Genesis19l57g1/Derivation/RuleBridge.lean::rule_item_never_minimal`](../../../lean4/Imported/Genesis19l57g1/Derivation/RuleBridge.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/enumeration.rs::iter_cost2_deltas`](https://github.com/dbccpage/the_symbol_game/blob/7351ed452e518cb8cf2bf973d4c4881289084bce/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/enumeration.rs)

### Python Oracles & Numerical Evaluators
- [`checks/independent/pgw-k-item-delta-grammar.py`](../../../checks/independent/pgw-k-item-delta-grammar.py)
- [`github:dbccpage/19L57G1@85a83ae7c/research/second_stream/stream.py::iter_k_item_deltas`](https://github.com/dbccpage/19L57G1/blob/85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_stream/stream.py)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/derivation/candidates.py::iter_cost2_deltas`](https://github.com/dbccpage/the_symbol_game/blob/7351ed452e518cb8cf2bf973d4c4881289084bce/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/derivation/candidates.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/continuation.txt:1081-1084`
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/genesis_source.txt:414-433`
  - `omega_engine_education/documentation/001_oegen/archive/genesis_pre_2026-10-09.md:1101`
