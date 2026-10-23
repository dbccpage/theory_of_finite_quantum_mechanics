# [TFQ-0433] contexts-plugging-profiles

> **Stage**: `GENESIS` | **Status**: `DEFINITION`  
> **UUID**: `272a76f7-26b3-5f69-889c-5b2fc5a27377`  
> **Parent Derivation**: [TFQ-0431](tfq_0431_regime_isomorphism_unordered_pairs.md)

---

## 1. Abstract & Formal Statement

A context is an admitted form with a slot tuple of its arity in which every filled slot names an admitted datum and at least one slot is a hole; plugging a datum fills every hole with that same datum. Derivability is membership in the admitted instances or coverage by a uniform all-tuples rule, and no other inference exists. The profile of a datum is the set of well-formed contexts whose plugging is derivable. Two data are collapsed when their profiles are equal and separable when some well-formed context is derivable for one and not the other; that is the declared sense used for every separation requirement.

### Governing Obligation
Enumerate well-formed contexts with at least one hole, plug by filling every hole with one datum, decide derivability by instance membership or a uniform rule only, and compare profiles.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Declared derivability: admitted-instance membership or a uniform all-tuples rule, with no other inference (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> These are declared definitions: separability means a difference in positive derivability only, and an imposed requirement records a demand for separation without making it hold.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/Imported/Genesis19l57g1/Derivation/Basic.lean::collapsed`](../../../lean4/Imported/Genesis19l57g1/Derivation/Basic.lean)
- [`lean4/Imported/Genesis19l57g1/Derivation/Basic.lean::derivable`](../../../lean4/Imported/Genesis19l57g1/Derivation/Basic.lean)
- [`lean4/Imported/Genesis19l57g1/Derivation/Basic.lean::plug`](../../../lean4/Imported/Genesis19l57g1/Derivation/Basic.lean)
- [`lean4/Imported/Genesis19l57g1/Derivation/Basic.lean::separable`](../../../lean4/Imported/Genesis19l57g1/Derivation/Basic.lean)
- [`lean4/Imported/Genesis19l57g1/Derivation/Basic.lean::wfCtx`](../../../lean4/Imported/Genesis19l57g1/Derivation/Basic.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/context.rs::contexts`](https://github.com/dbccpage/the_symbol_game/blob/7351ed452e518cb8cf2bf973d4c4881289084bce/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/context.rs)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/profile.rs::profile`](https://github.com/dbccpage/the_symbol_game/blob/7351ed452e518cb8cf2bf973d4c4881289084bce/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/profile.rs)

### Python Oracles & Numerical Evaluators
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/derivation/observe.py::contexts`](https://github.com/dbccpage/the_symbol_game/blob/7351ed452e518cb8cf2bf973d4c4881289084bce/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/derivation/observe.py)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/derivation/observe.py::profile`](https://github.com/dbccpage/the_symbol_game/blob/7351ed452e518cb8cf2bf973d4c4881289084bce/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/derivation/observe.py)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/derivation/observe.py::separable`](https://github.com/dbccpage/the_symbol_game/blob/7351ed452e518cb8cf2bf973d4c4881289084bce/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/derivation/observe.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0434](tfq_0434_collapse_without_instances.md)
- [TFQ-0436](tfq_0436_context_count_formula.md)
- [TFQ-0437](tfq_0437_collection_extensionality.md)
- [TFQ-0438](tfq_0438_responses_costs_mu1_mu2.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/genesis_source.txt:140-146`
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/genesis_source.txt:147-153`
  - `omega_engine_education/documentation/001_oegen/genesis.md:15`
