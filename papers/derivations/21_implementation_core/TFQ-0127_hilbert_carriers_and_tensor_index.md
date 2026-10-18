# [TFQ-0127] Hilbert carriers and tensor index

> **Stage**: `IMPLEMENTATION_CORE` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `b6cb76a2-e7d9-5fcf-b719-1d87badeeb34`  
> **Parent Derivation**: [TFQ-0126](TFQ-0126_finite_configurations_and_complex_structure.md)

---

## 1. Abstract & Formal Statement

Covers hilbert_space.rs, higher_dim.rs, dagger_category.rs, and operational_axiom_selection.rs. hilbert_space.rs takes HilbertSpace as a labeled carrier C^d, d at least 1, in the declared standard basis, and TensorCarrier as a lexicographic flat index. Overflow past operation limits is a typed refusal. The other files check a PPT Tiles complement, the dagger compact category of finite Gaussian-rational spaces, and local tomography versus dimension. A Python replay and a Lean 4 declaration would still have to match the flat-index bijection and those refusals.

### Governing Obligation
Match the declared lexicographic flat-index bijection, dimension product, and typed refusal past operation limits.

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
- [`omega_engine/crates_rs/omega_quantum_physics/src/dagger_category.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/higher_dim.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/hilbert_space.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/operational_axiom_selection.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`not located`](../../code/python/)
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm/use_cases/operational_axiom_selection.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0128](TFQ-0128_declared_u_1_connections.md)
- [TFQ-0129](TFQ-0129_exact_rays_and_pure_states.md)
- [TFQ-0164](TFQ-0164_ribbon_anyons_and_yang-baxter.md)
- [TFQ-0165](TFQ-0165_spin-network_area_labels.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`
