# [TFQ-0446] pruning-lemmas-cost-two

> **Stage**: `GENESIS` | **Status**: `PROVED_LEAN`  
> **UUID**: `33886a64-5276-54ea-a2db-ffc704a6ba51`  
> **Parent Derivation**: [TFQ-0445](tfq_0445_response_existence_mark_progress.md)

---

## 1. Abstract & Formal Statement

A separation witness never inhabits a uniformly ruled form, so shrinking the final rule set preserves every separation (separable_of_subrules). With the item-level bridge applyDelta_dropRules, a delta containing a uniform-rule item is never minimal: dropping its rule items leaves a valid, strictly shorter delta with the same new-form arity sum (rule_item_never_minimal). The mention lemma shows that appending instances that mention neither datum of a pair leaves that pair's collapse unchanged (collapsed_append_unmentioning), and under the well-formedness conjuncts a fresh unreferenced datum or form leaves the collapse of every existing pair unchanged (collapsed_fresh_datum, collapsed_fresh_form).

### Governing Obligation
Show that rule items never occur in a minimum valid response and that unreferenced fresh data, unreferenced fresh forms and instances not mentioning a target datum cannot change the target pair's collapse.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> The three irrelevance inputs and the rule bridge are theorems, but the enclosing claim that the pruned cost-2 enumeration contains every minimum (CL-PRUNE-STRUCTURAL) stays a bounded theorem on computational evidence over the declared grammar slice.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/Imported/Genesis19l57g1/Derivation/Mention.lean::collapsed_append_unmentioning`](../../../lean4/Imported/Genesis19l57g1/Derivation/Mention.lean)
- [`lean4/Imported/Genesis19l57g1/Derivation/Mention.lean::collapsed_fresh_datum`](../../../lean4/Imported/Genesis19l57g1/Derivation/Mention.lean)
- [`lean4/Imported/Genesis19l57g1/Derivation/Mention.lean::collapsed_fresh_form`](../../../lean4/Imported/Genesis19l57g1/Derivation/Mention.lean)
- [`lean4/Imported/Genesis19l57g1/Derivation/Progress.lean::separable_of_subrules`](../../../lean4/Imported/Genesis19l57g1/Derivation/Progress.lean)
- [`lean4/Imported/Genesis19l57g1/Derivation/RuleBridge.lean::rule_item_never_minimal`](../../../lean4/Imported/Genesis19l57g1/Derivation/RuleBridge.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/enumeration.rs::iter_cost2_deltas`](https://github.com/dbccpage/the_symbol_game/blob/7351ed452e518cb8cf2bf973d4c4881289084bce/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/enumeration.rs)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/enumeration.rs::pruned_and_unpruned_agree_on_valid_deltas`](https://github.com/dbccpage/the_symbol_game/blob/7351ed452e518cb8cf2bf973d4c4881289084bce/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/enumeration.rs)

### Python Oracles & Numerical Evaluators
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/derivation/candidates.py::iter_cost2_deltas`](https://github.com/dbccpage/the_symbol_game/blob/7351ed452e518cb8cf2bf973d4c4881289084bce/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/derivation/candidates.py)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/derivation/candidates.py::iter_full_deltas`](https://github.com/dbccpage/the_symbol_game/blob/7351ed452e518cb8cf2bf973d4c4881289084bce/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/derivation/candidates.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0448](tfq_0448_branch_trees_and_roles.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/genesis_source.txt:414-422`
  - `lean4/Imported/Genesis19l57g1/Derivation/Mention.lean:94-96`
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/genesis_source.txt:742-747`
