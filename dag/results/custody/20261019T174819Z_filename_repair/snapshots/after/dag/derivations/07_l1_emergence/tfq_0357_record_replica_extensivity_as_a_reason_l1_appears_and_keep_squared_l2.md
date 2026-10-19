# [TFQ-0357] Record replica extensivity as a reason l1 appears, and keep squared l2

> **Stage**: `L1_EMERGENCE` | **Status**: `SOURCE_RECORD`  
> **UUID**: `e539275b-9f8c-5840-8f4d-f4adab3eeb1b`  
> **Parent Derivation**: [TFQ-0349](tfq_0349_compute_declared_phi1_and_gamma2_on_a_finite_window_and_do_not.md)

---

## 1. Abstract & Formal Statement

DAG node L1-WDP-CH08-C01-REPLICA-L1 says l1 appears when aggregation over independent replicas is required to be extensive, and that WDP 8.5 states l2 is not excluded by that argument alone. Route L1-R-REPLICA-L1 takes L1-WDP-WINDOW-PHI1-GAMMA2 as input. The node bottleneck in the DAG text also names degree-1 homogeneity separation and a disjoint-support norm separation. Those clauses were not rechecked against the monograph body in this pass. The claim ledger row WDP-CH08-C01 is the cited anchor. AuthorityEffect is None.

### Governing Obligation
Record replica extensivity as a reason l1 appears, and keep squared l2 available under that hypothesis alone.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> None (replica extensivity, WDP 8.5 non-exclusion of squared L2 by extensivity alone, degree-1 homogeneity separation, and disjoint-support norm separation mechanized in wdp_ch08_c01_replica_extensivity_homogeneity_and_l2_separation).

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.l1_gs001_and_wdp_ch08_replica_extensivity_vs_homogeneity`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.l1_gs001_replica_and_phi1_quotient_invariance`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.wdp_ch08_c01_replica_extensivity_homogeneity_and_l2_separation`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/lean/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.wdp_ch08_c01_replica_extensivity_homogeneity_and_l2_separation`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_quantum_physics/src/derivation_dag_witnesses.rs::verify_tranche17_l1_emergence_gs000_gs001_replica_and_c10_branch_closure_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche17_l1_emergence_gs000_gs001_replica_and_c10_branch_closure_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche3_emergence_dynamics_heisenberg_and_qec_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche7_wdp_bridge_o03_o05_sector_orbit_and_gleason_rival_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_wdp/src/gauge_classification.rs`](../../code/rust/src/)
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/native/src/derivation_dag_witnesses.rs::verify_tranche17_l1_emergence_gs000_gs001_replica_and_c10_branch_closure_witness`](../../code/rust/src/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F000.S000`
- **Primary Source Paths**:

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`L1-WDP-WINDOW-PHI1-GAMMA2`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `L1-WDP-WINDOW-PHI1-GAMMA2` (`L1_EMERGENCE` / `DEFINITION`)
- **Mined Operad Family (`M2`)**: `OP-L1_EMERGENCE-L1-WDP-WINDOW-PHI1-GAMMA2`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [690, -1380, 1035]`, `chord_potential = 1035`, `holonomy_gamma2 = 1380`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(L1-WDP-WINDOW-PHI1-GAMMA2): 4*idx(69) + 3*stage_rank(5) + route_degree(6) == 297` ($\text{value} = 297$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(L1-WDP-WINDOW-PHI1-GAMMA2): R_raw(163) - G_cob(79) - S_decoy(5) == 79 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 79$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `1` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.l1_observer_h1_h5_cochain_flatness_and_wdp_window_mass_realification`
- **Sovereign Rust Witness Anchor**: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche11_admitted_primitives_definitions_and_imported_assumptions_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = 9bbbd4892f8d196888bae51cb0d584afea5237939f1daba153edb576ca23fa12`

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`L1-WDP-CH08-C01-REPLICA-L1`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `L1-WDP-CH08-C01-REPLICA-L1` (`L1_EMERGENCE` / `PROVED_LEAN`)
- **Mined Operad Family (`M2`)**: `OP-L1_EMERGENCE-L1-WDP-CH08-C01-REPLICA-L1`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [730, -1460, 1095]`, `chord_potential = 1095`, `holonomy_gamma2 = 1460`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(L1-WDP-CH08-C01-REPLICA-L1): 4*idx(73) + 3*stage_rank(5) + route_degree(2) == 309` ($\text{value} = 309$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(L1-WDP-CH08-C01-REPLICA-L1): R_raw(171) - G_cob(83) - S_decoy(5) == 83 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 83$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `0` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/lean/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.wdp_ch08_c01_replica_extensivity_homogeneity_and_l2_separation`
- **Sovereign Rust Witness Anchor**: `omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/native/src/derivation_dag_witnesses.rs::verify_tranche17_l1_emergence_gs000_gs001_replica_and_c10_branch_closure_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = 0ddb6adba074ab9eedef3458f6c2c1892a083988c6a4ff30f62f1625d723b42a`
