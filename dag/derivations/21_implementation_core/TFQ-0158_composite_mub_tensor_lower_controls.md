# [TFQ-0158] Composite MUB tensor lower controls

> **Stage**: `IMPLEMENTATION_CORE` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `bf15a4fe-c841-5b15-8ba0-8bc2d149ed91`  
> **Parent Derivation**: [TFQ-0154](TFQ-0154_canonical_mub_inversion.md)

---

## 1. Abstract & Formal Statement

Covers mub/composite.rs, mub/composite_controls.rs, mub/composite_completion_gate.rs, mub/composite_tensor_family_gate.rs, mub/d10_controls.rs, and mub/non_cyclic_falser.rs. composite.rs pairs Kronecker products of factor MUB projectors and, for dimension 6, records three bases from factors 2 and 3. The other files keep that lower control apart from a complete family, mark the d=10 boundary as partial, and search MUB-6 candidates outside the cyclic Weyl class. A Python replay and a Lean 4 declaration would still have to match the paired-product count.

### Governing Obligation
Match the paired Kronecker lower control, including three bases in dimension 6, and the partial d=10 boundary.

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
- [`omega_engine/crates_rs/omega_quantum_physics/src/mub/composite.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/mub/composite_completion_gate.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/mub/composite_controls.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/mub/composite_tensor_family_gate.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/mub/d10_controls.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/mub/non_cyclic_falser.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`The python twin is not located for mub/composite.rs. composition_tensor_mub.py is a tensor-statistics replay, not this lower-control gate.`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`
