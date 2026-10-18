# [TFQ-0242] Graded path sum as finite transport

> **Stage**: `FINITE_QM_DYNAMICS` | **Status**: `SOURCE_RECORD`  
> **UUID**: `4a9bf379-16d7-569d-9969-6ce83fe73b63`  
> **Parent Derivation**: [TFQ-0239](TFQ-0239_finite_path_sum_on_a_unique_intermediate_cut.md)

---

## 1. Abstract & Formal Statement

QM_031 presents the finite path sum as graded transport and, in the opened header, places itself as a synthesis rung of the ingredient ladder rather than as a primitive of quantum mechanics. Its companions name Born normalization, the CPTP boundary, stochastic population shadows, the phase fiber, and the interference cross term as neighboring obligations. DS-QM030-GRADED-PATHSUM joins this paper with QM_030: on a time-sliced category with a commutative semiring and finite fibers, the propagator equals the sum of length-n weight products. The Lagrangian or edge weights are declared.

### Governing Obligation
Keep the graded path sum as a finite semiring identity with declared weights, not as a derived continuum propagator.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `commutative semiring of weights (assumption)`
- **Admitted**: `finite fibers (assumption)`
- **Admitted**: `grading / time-slicing of the category (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Lean file FinitePathSum.lean cited by QM-031 not located by me under lean4/quantum_mechanics; the WDP SemiringTransport lemma is the only receipted algebra I could check.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm030_032_033_041_043_dynamics_and_heisenberg_duality`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm030_032_graded_pathsum_overcount_transfer_and_feynman_shadow`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.master_dag_177_node_10_stage_and_172_route_partition_conservation`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.master_operad_25_family_composition_and_end_to_end_chain_closure`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/lean/DerivationDagQMClosure.lean`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_quantum_physics/src/graded_path_sum.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/graded_path_sum.rs::TimeSlicedTransport`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/path_integral.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche13_ds_qm_final_16_second_witness_closure_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche16_master_177_node_172_route_dag_completeness_and_operad_audit_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche3_emergence_dynamics_heisenberg_and_qec_witness`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0243](TFQ-0243_finite_feynman_history_shadow.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`
