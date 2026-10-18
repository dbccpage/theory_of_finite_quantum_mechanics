# [TFQ-0164] Ribbon anyons and Yang-Baxter

> **Stage**: `IMPLEMENTATION_CORE` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `54822c37-9195-5ec5-bf3a-6daf3751faaf`  
> **Parent Derivation**: [TFQ-0127](TFQ-0127_hilbert_carriers_and_tensor_index.md)

---

## 1. Abstract & Formal Statement

Covers anyon_model.rs, anyon.rs, r_matrix.rs, yang_baxter_equation.rs, modular_tensor_category.rs, and topological_quantum_computing.rs. anyon_model.rs runs fusion and braiding on a multiplicity-free ribbon category inside an explicit pentagon and hexagon bound. The other files read simple charges, retain a Yang-Baxter residual, and say a finite closure bound does not establish density of a braid image. A Python replay and a Lean 4 declaration would still have to match the bounded replay and the retained residual.

### Governing Obligation
Match bounded ribbon fusion replay and retention of the Yang-Baxter residual matrix.

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
- [`omega_engine/crates_rs/omega_quantum_physics/src/anyon.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/anyon_model.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/modular_tensor_category.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/r_matrix.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/topological_quantum_computing.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/yang_baxter_equation.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`The python twin is not located for anyon_model.rs under 006_finite_qm/python/finite_qm.`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`
