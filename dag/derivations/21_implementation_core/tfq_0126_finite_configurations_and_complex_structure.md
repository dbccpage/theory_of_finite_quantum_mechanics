# [TFQ-0126] Finite configurations and complex structure

> **Stage**: `IMPLEMENTATION_CORE` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `f9f2c565-a29a-56de-a764-1112cabe206a`  
> **Parent Derivation**: [TFQ-0125](tfq_0125_crate_index_and_derivation_witnesses.md)

---

## 1. Abstract & Formal Statement

Covers finite_geometry.rs, complex_realification.rs, complex_structure_selector.rs, tower.rs, and embedding_relativity.rs. finite_geometry.rs states exact QM_122 configurations whose enumerations keep explicit finite bounds. The other files realize a declared Q(i) complex structure, the finite U(1)-selector checks, the cyclotomic tower with Q(zeta_6)=Q(zeta_3), and positivity relative to a declared real embedding. A Python replay and a Lean 4 declaration would still have to match those bounded configurations and the embedding-dependent sign.

### Governing Obligation
Match bounded QM_122 configurations, the Q(i) complex-structure realization, the cyclotomic tower criterion, and embedding-dependent positivity.

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
- [`omega_engine/crates_rs/omega_quantum_physics/src/complex_realification.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/complex_structure_selector.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/embedding_relativity.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/finite_geometry.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/tower.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`The python twin is not located for finite_geometry.rs under 006_finite_qm/python/finite_qm.`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0127](tfq_0127_hilbert_carriers_and_tensor_index.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`
