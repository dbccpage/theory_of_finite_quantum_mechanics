# [TFQ-0094] GAP: physical cosmological constant and continuum Hilbert space are outside this tetrahedron

> **Stage**: `FINITE_QG` | **Status**: `FINITE_GEOMETRY`  
> **UUID**: `59644faa-1e57-5d92-b882-da76760bb6f2`  
> **Parent Derivation**: [TFQ-0093](tfq_0093_imported_area_scale_and_casimir_stay_unpaid_the_einstein_equation_and_smooth.md)

---

## 1. Abstract & Formal Statement

loop_quantum_gravity.rs evaluates exact rational flux closure and squared volume for one oriented tetrahedron given rational vertex coordinates, and it refuses a degenerate volume. The module fence says this finite geometric face does not construct a continuum Hilbert space. What is finite is one tetrahedron and its Gram determinant over the rationals. What is not discharged is a spin-network space, a physical cosmological constant, dynamics, and the continuum limit. Four points are not quantum gravity and do not discharge the Einstein equation.

### Governing Obligation
GAP: physical cosmological constant and continuum Hilbert space are outside this tetrahedron certificate.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Hamiltonian constraint / Einstein equation (assumption)`
- **Admitted**: `SU(2) gauge group (assumption)`
- **Admitted**: `continuum manifold, metric, connection (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Lean names not checked by me; dynamics Q-held.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm102_110_111_212_syndrome_hamming_lqg_wilson_and_majorana_braid`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.qm110_111_lqg_gr_kinematical_witness`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_general_relativity/src/lib.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_general_relativity/src/loop_quantum_gravity.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_ds_qm_dynamics_structure_and_majorana_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche13_ds_qm_final_16_second_witness_closure_witness`](../../code/rust/src/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0095](tfq_0095_qm_111_c3_does_not_discharge_nabla_g_equals_zero_qm_111_c7_imports_the_continuum.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`
