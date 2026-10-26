# [TFQ-0437] collection-extensionality

> **Stage**: `GENESIS` | **Status**: `PROVED_LEAN`  
> **UUID**: `0256c85d-13a2-5dd5-8048-27711b278bdf`  
> **Parent Derivation**: [TFQ-0433](tfq_0433_contexts_plugging_profiles.md)

---

## 1. Abstract & Formal Statement

Python's admitted collections are sets while Lean's are deduplicated lists. Under RegimeExt (equal datum counts and form tables, and membership-equal instance, rule and requirement collections) every stated observable transports: derivability, context well-formedness, collapse, separability, item and delta application, and response validity (derivable_ext through validResponse_ext). Two list representations of the same admitted sets therefore agree on each of those observables.

### Governing Obligation
Show that membership-equal instance, rule and requirement lists with equal datum counts and form tables give the same derivability, collapse, separability, delta application and response validity.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Lean-to-Lean only: equal datum counts and equal indexed form tables stay premises, that every exported claim factors through these observables is not asserted, and executable comparisons with Python and Rust have their own input populations.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/Imported/Genesis19l57g1/Derivation/Ext.lean::collapsed_ext`](../../../lean4/Imported/Genesis19l57g1/Derivation/Ext.lean)
- [`lean4/Imported/Genesis19l57g1/Derivation/Ext.lean::derivable_ext`](../../../lean4/Imported/Genesis19l57g1/Derivation/Ext.lean)
- [`lean4/Imported/Genesis19l57g1/Derivation/Ext.lean::separable_ext`](../../../lean4/Imported/Genesis19l57g1/Derivation/Ext.lean)
- [`lean4/Imported/Genesis19l57g1/Derivation/Ext.lean::validResponse_ext`](../../../lean4/Imported/Genesis19l57g1/Derivation/Ext.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `missing obligation: no Rust statement of RegimeExt; the Rust regime stores instances, rules and requirements as BTreeSet collections, so list order does not arise there`

### Python Oracles & Numerical Evaluators
- `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/derivation/model.py::Regime` (private upstream source, not in this repository)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/genesis_source.txt:114-123`
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/genesis_source.txt:123-126`
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/paper.md:272-277`
