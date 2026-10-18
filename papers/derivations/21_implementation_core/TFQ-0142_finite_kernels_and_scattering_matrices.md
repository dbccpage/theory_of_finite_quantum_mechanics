# [TFQ-0142] Finite kernels and scattering matrices

> **Stage**: `IMPLEMENTATION_CORE` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `093c1aee-0e11-5daf-a942-9f2cafcbfd11`  
> **Parent Derivation**: [TFQ-0137](TFQ-0137_unitary_steps_and_hamiltonians.md)

---

## 1. Abstract & Formal Statement

Covers path_integral.rs, time_sliced_action_shadow.rs, s_matrix.rs, scattering_amplitude.rs, and feynman_diagram.rs. path_integral.rs computes finite time-sliced kernels and says formal coefficients do not assert a continuum measure. s_matrix.rs builds S from a Hermitian reaction matrix over Q(i). scattering_amplitude.rs uses T = (S - I)/(2i) at a declared energy with no on-shell limit. The other files add a phase policy and finite Wick symmetry factors. A Python replay and a Lean 4 declaration would still have to match the reaction-matrix formula and that continuum refusal.

### Governing Obligation
Match S built from a Hermitian reaction matrix over Q(i) and the refusal to assert a continuum measure.

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
- [`omega_engine/crates_rs/omega_quantum_physics/src/feynman_diagram.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/path_integral.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/s_matrix.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/scattering_amplitude.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/time_sliced_action_shadow.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`The python twin is not located for path_integral.rs under 006_finite_qm/python/finite_qm.`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`
