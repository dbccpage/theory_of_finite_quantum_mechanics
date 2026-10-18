# [TFQ-0244] Discrete Schrodinger cochain on a finite graph

> **Stage**: `FINITE_QM_DYNAMICS` | **Status**: `SOURCE_RECORD`  
> **UUID**: `31829269-e130-58f5-905d-c18d04881f45`  
> **Parent Derivation**: [TFQ-0243](TFQ-0243_finite_feynman_history_shadow.md)

---

## 1. Abstract & Formal Statement

QM_033 obliges a discrete Schrodinger cochain on a finite interaction graph. For a Hermitian matrix the opened status box says the squared Euclidean norm of the amplitude is conserved, and it says that quantity is not an l1 mass of absolute values. The paper's non-claim box refuses the continuous Schrodinger equation on a continuum space, refuses treating an L2 container as intrinsic, and refuses Born uniqueness from additivity alone. Gauge invariance of a cycle sum is separated from the open claim that the holonomy is nonzero whenever the U(1) cohomology is nonzero.

### Governing Obligation
Conserve the squared Euclidean amplitude norm under a declared finite Hermitian step, without deriving the continuum equation.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `L2 norm as conserved mass (assumption)`
- **Admitted**: `complex field and Hermitian generator H (assumption)`
- **Admitted**: `continuous time t and hbar (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Skew-symmetric L2 norm conservation under -J H and separation from stochastic L1 dissipation are mechanized; Hermitian H and continuous time t remain explicit imports.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.conditional_route_bridges_pg_l1_fq_ds_sixteen_route_closure`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm030_032_033_041_043_dynamics_and_heisenberg_duality`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm033_skew_hermitian_l2_norm_conservation_and_stochastic_separation`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/lean/DerivationDagQMClosure.lean`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_quantum_physics/src/dynamics.rs::cayley_transform_toggle`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/finite_schrodinger_step.rs::cycle_product`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/finite_schrodinger_step.rs::euler_propagator`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/finite_schrodinger_step.rs::norm_rate`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche15_gap_nonderivation_countermodels_and_conditional_route_bridges_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche3_emergence_dynamics_heisenberg_and_qec_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche6_conditional_and_open_boundary_certificates_witness`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0245](TFQ-0245_unitary_finite-shadow_slot_still_reserved.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`
