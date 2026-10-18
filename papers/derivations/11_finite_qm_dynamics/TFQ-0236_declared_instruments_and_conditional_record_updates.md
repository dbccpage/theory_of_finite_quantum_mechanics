# [TFQ-0236] Declared instruments and conditional record updates

> **Stage**: `FINITE_QM_DYNAMICS` | **Status**: `SOURCE_RECORD`  
> **UUID**: `6672005d-e1b6-5ff2-bb3c-da0b1c3e8937`  
> **Parent Derivation**: [TFQ-0235](TFQ-0235_selective_measurement_update_as_idempotent_conditioning.md)

---

## 1. Abstract & Formal Statement

Finite Quantum Mechanics section 13.3, after the Hilbert carrier is supplied, obliges an instrument to be a family of completely positive maps indexed by record labels, with Kraus operators summing to the identity in the adjoint form stated there. Outcome weights use the supplied trace pairing, and the conditional state is the branch divided by a positive probability. A zero-probability branch has no normalized state. Projective instruments recover a Luders update and an idempotent non-selective dephasing channel; general instruments need not be projective, repeatable, or idempotent.

### Governing Obligation
Record conditional updating from a declared instrument and pairing, without treating that update as the occurrence of one event.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `declared outcome partition (observer-relative) (assumption)`
- **Admitted**: `probability pairing and normalization (assumption)`
- **Admitted**: `projection postulate / spectral structure (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Lean mechanization targeted, not delivered (PL-QM037-1); incompatible measurements out of scope (C9).

> [!WARNING]
> Overlaps L1_TO_L2 Born nodes (QM_020, other fragment).

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_gap_measurement_projection_cptp_and_continuous_time_generator_countermodels`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm021_040_041_043_commutator_heisenberg_global_weight_and_conditioning`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.qm021_idempotent_conditioning_and_order_sensitivity`](../../code/lean4/)
- [`lean4/quantum_mechanics/GleasonTheorem.lean::d2_binary_non_bornian_obstruction`](../../code/lean4/)
- [`lean4/quantum_mechanics/H013BornPairingBoundary.lean::born_pairing_boundary`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/lean/DerivationDagQMClosure.lean`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_quantum_physics/src/exact_instrument.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/instruments.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/measurement.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_ds_qm_dynamics_structure_and_majorana_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche13_ds_qm_final_16_second_witness_closure_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche15_gap_nonderivation_countermodels_and_conditional_route_bridges_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche5_full_dag_177_node_coverage_witness`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0237](TFQ-0237_measurement-problem_slot_left_undeclared.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`
