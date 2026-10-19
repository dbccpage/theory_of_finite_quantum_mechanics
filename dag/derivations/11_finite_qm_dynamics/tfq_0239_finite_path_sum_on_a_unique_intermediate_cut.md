# [TFQ-0239] Finite path sum on a unique intermediate cut

> **Stage**: `FINITE_QM_DYNAMICS` | **Status**: `SOURCE_RECORD`  
> **UUID**: `6de60bd3-578e-5460-96d0-29528fd61987`  
> **Parent Derivation**: [TFQ-0234](../10_finite_qm_core/tfq_0234_supplied_hilbert_carrier_after_the_conditional_lift.md)

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

- [TFQ-0240](tfq_0240_ungraded_overcount_and_multiplicative_gauge_residual.md)
- [TFQ-0241](tfq_0241_projection_postulate_and_born_pairing_remain_imported.md)
- [TFQ-0242](tfq_0242_graded_path_sum_as_finite_transport.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`DS-QM030-UNGRADED-OVERCOUNT`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `DS-QM030-UNGRADED-OVERCOUNT` (`FINITE_QM_DYNAMICS` / `PROVED_LEAN`)
- **Mined Operad Family (`M2`)**: `OP-FINITE_QM_DYNAMICS-DS-QM030-UNGRADED-OVERCOUNT`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [1350, -2700, 2025]`, `chord_potential = 2025`, `holonomy_gamma2 = 2700`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(DS-QM030-UNGRADED-OVERCOUNT): 4*idx(135) + 3*stage_rank(9) + route_degree(4) == 571` ($\text{value} = 571$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(DS-QM030-UNGRADED-OVERCOUNT): R_raw(315) - G_cob(153) - S_decoy(9) == 153 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 153$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `0` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm030_032_graded_pathsum_overcount_transfer_and_feynman_shadow`
- **Sovereign Rust Witness Anchor**: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche13_ds_qm_final_16_second_witness_closure_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = e213aec69283111f1fe54261af612cfa4d5943015837cf39f38888e40527fa24`

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

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`DS-QM030-TRANSFER-OPERATOR-SHADOW`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `DS-QM030-TRANSFER-OPERATOR-SHADOW` (`FINITE_QM_DYNAMICS` / `PROVED_LEAN`)
- **Mined Operad Family (`M2`)**: `OP-FINITE_QM_DYNAMICS-DS-QM030-TRANSFER-OPERATOR-SHADOW`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [1360, -2720, 2040]`, `chord_potential = 2040`, `holonomy_gamma2 = 2720`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(DS-QM030-TRANSFER-OPERATOR-SHADOW): 4*idx(136) + 3*stage_rank(9) + route_degree(5) == 576` ($\text{value} = 576$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(DS-QM030-TRANSFER-OPERATOR-SHADOW): R_raw(317) - G_cob(154) - S_decoy(9) == 154 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 154$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `1` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm030_032_graded_pathsum_overcount_transfer_and_feynman_shadow`
- **Sovereign Rust Witness Anchor**: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche13_ds_qm_final_16_second_witness_closure_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = d1516dc59af64f84726a6728311e8a810dfe9b0fe917c10885cc53ca12f2b15d`
