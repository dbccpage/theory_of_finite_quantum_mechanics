# [TFQ-0137] Unitary steps and Hamiltonians

> **Stage**: `IMPLEMENTATION_CORE` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `e34e7797-41b1-5b3b-b3f8-41b1e16786de`  
> **Parent Derivation**: [TFQ-0133](TFQ-0133_observables_and_local_star_algebras.md)

---

## 1. Abstract & Formal Statement

Covers unitary_operator.rs, quantum_hamiltonian.rs, dynamics.rs, finite_schrodinger_step.rs, and perturbation_theory.rs. unitary_operator.rs is the finite face of U adjoint U = I on states and densities. quantum_hamiltonian.rs takes a Hamiltonian to be Hermitian and generates the unitary step it declares. The other files are finite toggle dynamics, exact finite-step Schrodinger transport, and a Rayleigh-Schrodinger series checked against the characteristic polynomial. A Python replay and a Lean 4 declaration would still have to match the adjoint identity and the finite-step transport.

### Governing Obligation
Match U adjoint U = I on the finite face and exact finite-step Schrodinger transport.

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
- [`omega_engine/crates_rs/omega_quantum_physics/src/dynamics.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/finite_schrodinger_step.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/perturbation_theory.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/quantum_hamiltonian.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/unitary_operator.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm/use_cases/discrete_dynamics.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0138](TFQ-0138_heisenberg_picture_and_cayley_jet.md)
- [TFQ-0140](TFQ-0140_product_formulas_and_locality_cones.md)
- [TFQ-0142](TFQ-0142_finite_kernels_and_scattering_matrices.md)
- [TFQ-0143](TFQ-0143_dirac_gamma_admission.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`
