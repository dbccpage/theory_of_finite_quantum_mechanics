# [TFQ-0311] Ordinary matrix algebra over C is not recovered

> **Stage**: `FINITE_HILBERT` | **Status**: `GAP`  
> **UUID**: `5c9c66f8-9249-568a-90cf-f55d0e515d0a`  
> **Parent Derivation**: [TFQ-0310](TFQ-0310_finite_hilbert_boundary_from_a_presented_carrier.md)

---

## 1. Abstract & Formal Statement

Ordinary M_n(C) is not recovered. qm_122_finite_hilbert_boundary_from_primitive_difference.md says a scoped endomorphism algebra on a finite enumerated report set with Gaussian-integer coefficients is not the matrix algebra over the complex numbers. Gauss integers are not a field, a self-adjoint matrix over them need not have an eigenvalue in that ring, and completeness of the complex numbers is not obtained from invertibility inside the stand-in. The claim ledger lists the remaining matrix-algebra object as still open in that sense. derivation_dag.json records L1-QM122-LEFTOVER-MNC-NOT-RECOVERED.

### Governing Obligation
Do not identify finite Gauss-integer matrices with ordinary M_n(C).

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `CPTP: assumption`
- **Admitted**: `Gleason: assumption`
- **Admitted**: `Hilbert tensor product: assumption`
- **Admitted**: `circle phases: assumption`
- **Admitted**: `complex field: assumption`
- **Admitted**: `continuous time: assumption`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> The six import boundaries separating the finite walk from full M_n(C) have mechanized drop-one independence and finite countermodels; full M_n(C) recovery remains conditional on the declared imports.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.conditional_route_bridges_pg_l1_fq_ds_sixteen_route_closure`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm072_073_090_and_fq_import_boundary_certificates`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.fq_entropy_renyi_purity_dichotomy_and_qm122_six_import_drop_one_census`](../../code/lean4/)
- [`lean4/quantum_mechanics/FiniteQM.lean`](../../code/lean4/)
- [`lean4/quantum_mechanics/H017Fin.lean`](../../code/lean4/)
- [`lean4/quantum_mechanics/H017Finish.lean`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche15_gap_nonderivation_countermodels_and_conditional_route_bridges_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche2_row_sparsity_bell_torsion_and_structure_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche8_tensor_stone_continuum_embedding_and_leftover_mnc_witness`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/_code/qm_122/qm122_lib/qm122_dual.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0312](TFQ-0312_four_necessity_verdicts_stay_open_beside_the_matrix_gap.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001`, `F001.S000`, `F001.S000:001_from_primitive_difference_to_quantum_mechanics`, `F002`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/floor.yaml`
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/shelf.yaml`
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/001_from_primitive_difference_to_quantum_mechanics/book/README.md`
  - `omega_engine_atlas/coda_atlas/F002_continuum/floor.yaml`

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`L1-QM122-LEFTOVER-MNC-NOT-RECOVERED`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `L1-QM122-LEFTOVER-MNC-NOT-RECOVERED` (`L1_TO_L2` / `PROVED_LEAN`)
- **Mined Operad Family (`M2`)**: `OP-L1_TO_L2-L1-QM122-LEFTOVER-MNC-NOT-RECOVERED`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [930, -1860, 1395]`, `chord_potential = 1395`, `holonomy_gamma2 = 1860`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(L1-QM122-LEFTOVER-MNC-NOT-RECOVERED): 4*idx(93) + 3*stage_rank(6) + route_degree(2) == 392` ($\text{value} = 392$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(L1-QM122-LEFTOVER-MNC-NOT-RECOVERED): R_raw(216) - G_cob(105) - S_decoy(6) == 105 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 105$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `0` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/lean/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.l1_qm122_leftover_mnc_eight_extra_finish_table_and_dilation_classifications`
- **Sovereign Rust Witness Anchor**: `omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/native/src/derivation_dag_witnesses.rs::verify_tranche21_pg_wdp_bridge_sector_weights_qm122_finish_embedding_and_baker_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = ec9b9688fabaa0c9bd197faf6ff73a3e645f3992778dc385593e9f7647d1d1eb`

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`GP-FIN-GAUSS-MATRIX-ALGEBRA`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `GP-FIN-GAUSS-MATRIX-ALGEBRA` (`FINITE_QM_CORE` / `PROVED_LEAN`)
- **Mined Operad Family (`M2`)**: `OP-FINITE_QM_CORE-GP-FIN-GAUSS-MATRIX-ALGEBRA`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [1320, -2640, 1980]`, `chord_potential = 1980`, `holonomy_gamma2 = 2640`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(GP-FIN-GAUSS-MATRIX-ALGEBRA): 4*idx(132) + 3*stage_rank(7) + route_degree(2) == 551` ($\text{value} = 551$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(GP-FIN-GAUSS-MATRIX-ALGEBRA): R_raw(299) - G_cob(146) - S_decoy(7) == 146 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 146$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `2` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.fq_impl_wdp_amplitude_realification_pairing_and_gauss_matrix_algebra`
- **Sovereign Rust Witness Anchor**: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche12_pg_l1_fq_gp_second_witness_certificates_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4-flash` | `status = PASS` | `receipt_sha256 = da368211df4b3d06de555fb8c63b4b144ff317a5ef63d0dad6aaf03864ab2ce5`
