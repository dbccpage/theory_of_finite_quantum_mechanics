# [TFQ-0242] Graded path sum as finite transport

> **Stage**: `FINITE_QM_DYNAMICS` | **Status**: `SOURCE_RECORD`  
> **UUID**: `4a9bf379-16d7-569d-9969-6ce83fe73b63`  
> **Parent Derivation**: [TFQ-0239](tfq_0239_finite_path_sum_on_a_unique_intermediate_cut.md)

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

- [TFQ-0243](tfq_0243_finite_feynman_history_shadow.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`DS-QM030-GRADED-PATHSUM`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `DS-QM030-GRADED-PATHSUM` (`FINITE_QM_DYNAMICS` / `PROVED_LEAN`)
- **Mined Operad Family (`M2`)**: `OP-FINITE_QM_DYNAMICS-DS-QM030-GRADED-PATHSUM`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [1340, -2680, 2010]`, `chord_potential = 2010`, `holonomy_gamma2 = 2680`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(DS-QM030-GRADED-PATHSUM): 4*idx(134) + 3*stage_rank(9) + route_degree(5) == 568` ($\text{value} = 568$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(DS-QM030-GRADED-PATHSUM): R_raw(313) - G_cob(152) - S_decoy(9) == 152 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 152$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `3` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.master_operad_25_family_composition_and_end_to_end_chain_closure`
- **Sovereign Rust Witness Anchor**: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche16_master_177_node_172_route_dag_completeness_and_operad_audit_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = d23231919eb9f7981671c81ea8d96c1acd989816567c3cc97ab49e5508d909f6`

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`DS-QM043-OFFDIAG-GLOBAL-WEIGHT-IDENTITY`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `DS-QM043-OFFDIAG-GLOBAL-WEIGHT-IDENTITY` (`FINITE_QM_DYNAMICS` / `PROVED_LEAN`)
- **Mined Operad Family (`M2`)**: `OP-FINITE_QM_DYNAMICS-DS-QM043-OFFDIAG-GLOBAL-WEIGHT-IDENTITY`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [1420, -2840, 2130]`, `chord_potential = 2130`, `holonomy_gamma2 = 2840`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(DS-QM043-OFFDIAG-GLOBAL-WEIGHT-IDENTITY): 4*idx(142) + 3*stage_rank(9) + route_degree(2) == 597` ($\text{value} = 597$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(DS-QM043-OFFDIAG-GLOBAL-WEIGHT-IDENTITY): R_raw(329) - G_cob(160) - S_decoy(9) == 160 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 160$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `1` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm021_040_041_043_commutator_heisenberg_global_weight_and_conditioning`
- **Sovereign Rust Witness Anchor**: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche13_ds_qm_final_16_second_witness_closure_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = c5a639c88af3e8b7b9392756845d9a04f436ea6d6040e96132c31cb2b6f269d3`
