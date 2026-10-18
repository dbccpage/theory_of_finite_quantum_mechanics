# [TFQ-0006] Conditional finite Hilbert lift

> **Stage**: `L1_TO_L2` | **Status**: `GAP`  
> **UUID**: `c5fc9265-5e57-5684-b28d-3870cf71e931`  
> **Parent Derivation**: [TFQ-0005](../07_l1_emergence/TFQ-0005_declared_l1_sector_weights.md)

---

## 1. Abstract & Formal Statement

The pass from L1 weights to a finite Hilbert carrier imports structure the finite papers do not derive: a square-root field, a complex field, U(1) phases, an inner product, orthogonal additivity, Haar-independent phases, and linear isometric dynamics. QM_020 states that it does not derive quantum mechanics. QM_122 recovers matrices over the Gaussian integers and leaves ordinary matrix algebras over the complex numbers unrecovered. Python, Rust, and Lean 4 must name each import and keep it imported. A finite matrix calculation is not a discharge of the import list.

### Governing Obligation
List each imported structure the finite Hilbert lift still requires, and do not discharge them by naming quantum mechanics.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Formalization
- **Primary Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.l1_to_l2_and_cross_fragment_route_composition` (zero-axiom, zero-sorry kernel verification in `lean/DerivationDagQMClosure.lean`).

### Sovereign Rust Certifiers
- **Primary Rust Witness**: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche14_cross_stage_route_composition_and_sorkin_hierarchy_witness` (`code/rust/src/dag_witnesses.rs`, exact `i64`/`BigRational` arithmetic).
- **Python PFP Gate Engine**: `omega_engine_pfp/tests/demo_004/finite_qm_derivation_pfp/gates/gate_engine.py::verify_dag_prompt_node_reply` (`G0`..`G6`).

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0007](../10_finite_qm_core/TFQ-0007_finite_quantum_mechanics_core_on_an_admitted_carrier.md)
- [TFQ-0234](../10_finite_qm_core/TFQ-0234_supplied_hilbert_carrier_after_the_conditional_lift.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001`, `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/floor.yaml`
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/shelf.yaml`

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`L1-QM122-PHASE-BLIND-FIBER-INTERFERENCE`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `L1-QM122-PHASE-BLIND-FIBER-INTERFERENCE` (`L1_TO_L2` / `PROVED_LEAN`)
- **Mined Operad Family (`M2`)**: `OP-L1_TO_L2-L1-QM122-PHASE-BLIND-FIBER-INTERFERENCE`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [900, -1800, 1350]`, `chord_potential = 1350`, `holonomy_gamma2 = 1800`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(L1-QM122-PHASE-BLIND-FIBER-INTERFERENCE): 4*idx(90) + 3*stage_rank(6) + route_degree(4) == 382` ($\text{value} = 382$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(L1-QM122-PHASE-BLIND-FIBER-INTERFERENCE): R_raw(210) - G_cob(102) - S_decoy(6) == 102 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 102$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `1` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.l1_to_l2_and_cross_fragment_route_composition`
- **Sovereign Rust Witness Anchor**: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche14_cross_stage_route_composition_and_sorkin_hierarchy_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = 252d95ebc14fe52e670005365fdb71eb7628efdbe61010d9831097c51e670f38`

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`L1-QM020-C10-BRANCH-LOCALIZATION`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `L1-QM020-C10-BRANCH-LOCALIZATION` (`L1_TO_L2` / `PROVED_LEAN`)
- **Mined Operad Family (`M2`)**: `OP-L1_TO_L2-L1-QM020-C10-BRANCH-LOCALIZATION`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [950, -1900, 1425]`, `chord_potential = 1425`, `holonomy_gamma2 = 1900`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(L1-QM020-C10-BRANCH-LOCALIZATION): 4*idx(95) + 3*stage_rank(6) + route_degree(2) == 400` ($\text{value} = 400$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(L1-QM020-C10-BRANCH-LOCALIZATION): R_raw(220) - G_cob(107) - S_decoy(6) == 107 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 107$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `0` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/lean/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.l1_qm020_c10_branch_pinching_and_residual_sector_orbit_closure`
- **Sovereign Rust Witness Anchor**: `omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/native/src/derivation_dag_witnesses.rs::verify_tranche17_l1_emergence_gs000_gs001_replica_and_c10_branch_closure_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = db66edbe975c0a6c0d8239227d59c0bab645e917425a57d7dad974b7cab1301f`

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`L1-WDP-REALIFICATION-J`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `L1-WDP-REALIFICATION-J` (`L1_TO_L2` / `DEFINITION`)
- **Mined Operad Family (`M2`)**: `OP-L1_TO_L2-L1-WDP-REALIFICATION-J`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [880, -1760, 1320]`, `chord_potential = 1320`, `holonomy_gamma2 = 1760`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(L1-WDP-REALIFICATION-J): 4*idx(88) + 3*stage_rank(6) + route_degree(3) == 373` ($\text{value} = 373$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(L1-WDP-REALIFICATION-J): R_raw(206) - G_cob(100) - S_decoy(6) == 100 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 100$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `1` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.l1_observer_h1_h5_cochain_flatness_and_wdp_window_mass_realification`
- **Sovereign Rust Witness Anchor**: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche11_admitted_primitives_definitions_and_imported_assumptions_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = ca19effa7cccd8f8c47263468fd7e5eba53bec31053e23e3d04ff1423826b2cc`
