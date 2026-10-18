# [TFQ-0093] Imported area scale and Casimir stay unpaid. The Einstein equation and smooth

> **Stage**: `FINITE_QG` | **Status**: `EXACT_LABEL`  
> **UUID**: `000df926-af2d-5504-b24f-b4d6b896812c`  
> **Parent Derivation**: [TFQ-0092](TFQ-0092_qm-110-c11_hamiltonian_constraint_stays_q-held_continuum_su_2_data_in_qm-110-c10_are_imported.md)

---

## 1. Abstract & Formal Statement

spin_area_spectrum.rs computes an exact rational square, n times n plus 2 over 4, for twice-spin n, then a surd label and a magnetic count n plus 1. Fusion dimensions follow the finite triangle rule inside a declared spin bound. The factor built from 8, pi, gamma, and a Planck length squared is a separately declared physical choice, not an output of the rational label. What is finite is that label arithmetic. What is not discharged is a continuum area operator, a fixed Immirzi parameter, and the Einstein equation. Reading the labels as smooth curvature stays GAP.

### Governing Obligation
Imported area scale and Casimir stay unpaid. The Einstein equation and smooth curvature remain GAP.

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
- [`omega_engine/crates_rs/omega_quantum_physics/src/spin_area_spectrum.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_ds_qm_dynamics_structure_and_majorana_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche13_ds_qm_final_16_second_witness_closure_witness`](../../code/rust/src/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0094](TFQ-0094_gap_physical_cosmological_constant_and_continuum_hilbert_space_are_outside_this_tetrahedron.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`
