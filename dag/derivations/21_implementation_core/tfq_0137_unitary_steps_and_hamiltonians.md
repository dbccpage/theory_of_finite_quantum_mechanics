# [TFQ-0137] Unitary steps and Hamiltonians

> **Stage**: `IMPLEMENTATION_CORE` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `e34e7797-41b1-5b3b-b3f8-41b1e16786de`  
> **Parent Derivation**: [TFQ-0133](tfq_0133_observables_and_local_star_algebras.md)

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
- [`absent: no local lean twin located for lean4/quantum_mechanics`](../../lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`absent: no local rust twin located for external:sha256:c71889c523b16e93349d9c2db4bd3486d3d58a47fcd30a4fd95231e853d56095`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:1c89f0f444d9e0936b761e3fd1890c3e4011a8a0a5dc404fba96f5b66a515e9a`](../../code/rust/src/)
- [`code/rust/src/qm/campaigns/dynamics.rs`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:6ab07bdd1ae577a675dc767e612844d3f4d1a9efd78e8392959395026af2e92e`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:a60d347705d09f5b9f8544dc54af5241d756b5b8e476337baf9eb9d4f93d82b3`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`code/python/src/majorana/tests/support/finite_qm/use_cases/discrete_dynamics.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0138](tfq_0138_heisenberg_picture_and_cayley_jet.md)
- [TFQ-0140](tfq_0140_product_formulas_and_locality_cones.md)
- [TFQ-0142](tfq_0142_finite_kernels_and_scattering_matrices.md)
- [TFQ-0143](tfq_0143_dirac_gamma_admission.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `external:git-tree:662d50fe40fdbf9e98bc3ae140d0355d3b3a45f5`
