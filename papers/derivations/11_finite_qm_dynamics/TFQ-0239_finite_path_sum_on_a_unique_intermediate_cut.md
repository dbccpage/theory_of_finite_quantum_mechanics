# [TFQ-0239] Finite path sum on a unique intermediate cut

> **Stage**: `FINITE_QM_DYNAMICS` | **Status**: `SOURCE_RECORD`  
> **UUID**: `6de60bd3-578e-5460-96d0-29528fd61987`  
> **Parent Derivation**: [TFQ-0234](../10_finite_qm_core/TFQ-0234_supplied_hilbert_carrier_after_the_conditional_lift.md)

---

## 1. Abstract & Formal Statement

QM_030, now a redirect into the finite transport notes, obliges a path sum on finite layers over a commutative semiring. Adjacent transfer matrices multiply to the sum of history weights, provided every allowed history crosses one chosen intermediate cut exactly once. The retained proposition says this is finite distributivity and does not require an inner product, a metric, or a Hamiltonian generator. Ledger group SRC-030 and the derivation node DS-QM030-GRADED-PATHSUM record the same finite shadow: the n-step propagator matches the graded path sum, and concatenations multiply.

### Governing Obligation
Equate the finite history sum with the product of transfer matrices only when the intermediate cut is unique.

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

- [TFQ-0240](TFQ-0240_ungraded_overcount_and_multiplicative_gauge_residual.md)
- [TFQ-0241](TFQ-0241_projection_postulate_and_born_pairing_remain_imported.md)
- [TFQ-0242](TFQ-0242_graded_path_sum_as_finite_transport.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`
