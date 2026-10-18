# [TFQ-0304] Lift capacity is not a dynamics derivation

> **Stage**: `L1_TO_L2` | **Status**: `SOURCE_RECORD`  
> **UUID**: `9765edbb-7887-51c5-a96f-e90bfa3f2eca`  
> **Parent Derivation**: [TFQ-0303](TFQ-0303_linear_isometric_dynamics_are_an_import.md)

---

## 1. Abstract & Formal Statement

The section labeled Theorem 7 in qm_020_born_normalization_and_conditional_hilbert_lift.md says the Hilbert lift is redundant for sector probabilities and still able to host phase-sensitive dynamics. The finite obligation is that capacity remark: redundancy of the probability reading does not by itself delete interference or reversible linear updates from the representation. The paper says the capacity comes from the imported complex linear representation and unitary dynamics, and that it does not alter direct normalization.

### Governing Obligation
Keep probability redundancy separate from any claim that lifted dynamics have been selected.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `complex Hilbert space: assumption`
- **Admitted**: `linear isometric dynamics: assumption`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> No Lean located. The interference non-descent boundary is in the QM_122 nodes.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/BornRedundancy.lean`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.l1_qm020_thm5_thm7_and_qm121_ladder_rungs_2_to_6_separation`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.qm020_thm7_representation_capacity`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_quantum_physics/src/coherent_interference.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/quantum_state.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_l1_to_l2_bridges_and_ladder_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche12_pg_l1_fq_gp_second_witness_certificates_witness`](../../code/rust/src/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0305](TFQ-0305_sector_weights_do_not_force_the_quadratic_form.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001`, `F001.S000`, `F001.S000:001_from_primitive_difference_to_quantum_mechanics`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/floor.yaml`
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/shelf.yaml`
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/001_from_primitive_difference_to_quantum_mechanics/book/README.md`
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/001_from_primitive_difference_to_quantum_mechanics/book/ch02_conditional_hilbert_lift_and_born_normalization.md`
