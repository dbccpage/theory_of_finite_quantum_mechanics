# [TFQ-0141] Meron source majorants

> **Stage**: `IMPLEMENTATION_CORE` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `a6a6f844-6e93-5e65-b89f-3f1dcf463099`  
> **Parent Derivation**: [TFQ-0140](TFQ-0140_product_formulas_and_locality_cones.md)

---

## 1. Abstract & Formal Statement

Covers meron_source_field.rs, meron_spatial_source.rs, meron_time_refinement.rs, and adaptive_integrator.rs. meron_source_field.rs takes a supplied source target and an exact rational error majorant, leaving infinite-volume arguments aside. The spatial and time files bound a written Gaussian source and rational Euler slices without inferring a thermodynamic limit. adaptive_integrator.rs updates an open two-local qubit chain from full cluster factors in order A then B. A Python replay and a Lean 4 declaration would still have to match the rational majorant and the refused limits.

### Governing Obligation
Match the exact rational source majorant and the refusal to infer an infinite-volume or thermodynamic limit.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_quantum_physics/src/adaptive_integrator.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/meron_source_field.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/meron_spatial_source.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/meron_time_refinement.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`The python twin is not located for meron_source_field.rs under 006_finite_qm/python/finite_qm.`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`
