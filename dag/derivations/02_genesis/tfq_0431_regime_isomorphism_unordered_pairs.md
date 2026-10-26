# [TFQ-0431] regime-isomorphism-unordered-pairs

> **Stage**: `GENESIS` | **Status**: `DEFINITION`  
> **UUID**: `6b0d092c-55a9-5107-ba64-62e104298f75`  
> **Parent Derivation**: [TFQ-0430](tfq_0430_metatheory_object_language_split.md)

---

## 1. Abstract & Formal Statement

A regime isomorphism is a pair of bijections on datum and form indices that preserves form arities, ordered instance arguments, uniform-rule membership and the separation requirements read as unordered pairs; mapped requirement endpoints are sorted before comparison, and presentation tokens are erased first. Because requirements are unordered, exchanging the endpoints of a requirement can identify two responses; a relation preserving directed requirements would be a different convention. The Lean structure Iso states these fields over the admitted index ranges, and sortPair is shown to equal (min, max) and to be symmetric.

### Governing Obligation
Compare regimes by datum and form bijections that preserve arities, instances, rules and sorted requirement pairs, with tokens erased, and keep the unordered-requirement convention explicit.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Declared isomorphism convention with unordered requirement pairs, genesis_source.txt section 3.8 (assumption)`

### Further Prerequisites
- [TFQ-0378](tfq_0378_regime_tuple_and_events.md) regime-tuple-and-events

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> The convention is declared: Iso is a membership relation, so it also identifies list representations such as [p] and [p, p], and an isomorphism preserving directed requirements would give different tie classes.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/Imported/Genesis19l57g1/Derivation/IsoCanon.lean::sortPair_comm`](../../../lean4/Imported/Genesis19l57g1/Derivation/IsoCanon.lean)
- [`lean4/Imported/Genesis19l57g1/Derivation/IsoCanon.lean::sortPair_eq_minmax`](../../../lean4/Imported/Genesis19l57g1/Derivation/IsoCanon.lean)
- [`lean4/Imported/Genesis19l57g1/Derivation/Minimality.lean::Iso`](../../../lean4/Imported/Genesis19l57g1/Derivation/Minimality.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/canonical.rs::find_iso`](../../../atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/canonical.rs)

### Python Oracles & Numerical Evaluators
- [`atlas/papers/finite_obstruction_calculus/genesis/code/derivation/iso.py::find_iso`](../../../atlas/papers/finite_obstruction_calculus/genesis/code/derivation/iso.py)
- [`atlas/papers/finite_obstruction_calculus/genesis/code/tests/test_mathematics.py::test_unordered_requirement_identifies_unary_endpoint_responses`](../../../atlas/papers/finite_obstruction_calculus/genesis/code/tests/test_mathematics.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0433](tfq_0433_contexts_plugging_profiles.md)
- [TFQ-0459](tfq_0459_canonical_key_classification.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `atlas/papers/finite_obstruction_calculus/genesis/paper.md:206-212`
  - `atlas/papers/finite_obstruction_calculus/genesis/docs/sources/genesis_source.txt:168-173`
  - `lean4/Imported/Genesis19l57g1/Derivation/IsoCanon.lean:44-47`
