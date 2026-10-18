# [TFQ-0354] Do not derive declared l1 sector weights from the Phi1 and Gamma2

> **Stage**: `L1_EMERGENCE` | **Status**: `GAP`  
> **UUID**: `679d56c6-3c7c-5ed1-bb5a-d1b190feddba`  
> **Parent Derivation**: [TFQ-0353](TFQ-0353_under_admitted_h1-h5_record_an_edgewise_weighted_l1_aggregate_orbit-constant_weights_and.md)

---

## 1. Abstract & Formal Statement

The l1-to-l2 segment note still says the step from the Phi1 and Gamma2 residual to l1 sector weights has no derivation in the sources read for that fragment. Weights enter as declared mass in WDP 8.2, as a definition in the QM_012 carrier, or as an input to QM_003 and QM_020. Node L1-RESIDUAL-SECTOR-WEIGHTS-DECLARED repeats that no derivation of the weight vector from the residual is given, and it is tagged gap. A later conditional label on L1-R-RESIDUAL-TO-WEIGHTS is not adopted; any selector remains extra data.

### Governing Obligation
Do not derive declared l1 sector weights from the Phi1 and Gamma2 residual; a fixed minimizer or a symmetry selector remains an extra hypothesis, and the Hilbert lift stays outside this slice.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `declared sector decomposition and masses: assumption`
- **Admitted**: `weighted l1 norm on C1 (declared, see L1-OBSERVER-AXIOMS-H1-H5): assumption`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> On a fixed minimizer r* or under the dihedral symmetry-orbit selector (l1_even_cycle_symmetry_orbit_canonical_sector_weights), sector weights are uniquely determined and sum to Phi_1; without a selector, even cycles have multiple L1 minimizers.

> [!WARNING]
> The weighted l1 form of the norm is declared in the window definition, not derived from MSS-0 or Difference. Upstream window construction is in the WDP fragment.

> [!WARNING]
> None (derived from parent L1-OBSERVER-AXIOMS-H1-H5 via gs003_coordinate_l1_weighted_sum_and_orbit_collapse, l1_gs000_edgewise_l1_and_symmetry_collapse, and l1_gs000_edgewise_l1_weighted_anisotropy_and_l_inf_countermodels).

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/BornRedundancy.lean::normalize`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.even_cycle_sector_weights_require_selector`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.gs003_coordinate_l1_weighted_sum_and_orbit_collapse`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.l1_even_cycle_symmetry_orbit_canonical_sector_weights`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.l1_gs000_edgewise_l1_and_symmetry_collapse`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.l1_gs000_edgewise_l1_weighted_anisotropy_and_l_inf_countermodels`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.l1_gs001_replica_and_phi1_quotient_invariance`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.l1_observer_h1_h5_cochain_flatness_and_wdp_window_mass_realification`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.l1_qm020_c10_branch_pinching_and_residual_sector_orbit_closure`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.master_dag_177_node_10_stage_and_172_route_partition_conservation`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.master_operad_25_family_composition_and_end_to_end_chain_closure`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.sector_weights_sum_to_phi1`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/lean/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.gs003_coordinate_l1_weighted_sum_and_orbit_collapse`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/lean/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.l1_qm020_c10_branch_pinching_and_residual_sector_orbit_closure`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_finite_probability/src/simplex.rs::try_from_weights`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_functional/src/phi1.rs::Phi1Functional`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/derivation_dag_witnesses.rs::verify_tranche17_l1_emergence_gs000_gs001_replica_and_c10_branch_closure_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/residual_density_calculus.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_l1_sector_weights_and_density_lift_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche10_chsh_tsirelson_pr_box_tier3_uniqueness_edgewise_l1_and_import_boundaries_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche11_admitted_primitives_definitions_and_imported_assumptions_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche16_master_177_node_172_route_dag_completeness_and_operad_audit_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche17_l1_emergence_gs000_gs001_replica_and_c10_branch_closure_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche3_emergence_dynamics_heisenberg_and_qec_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche4_edgewise_l1_u1_holonomy_chsh_and_cayley_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche7_wdp_bridge_o03_o05_sector_orbit_and_gleason_rival_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_wdp/src/gauge_classification.rs::standard_l1`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_wdp/src/obstruction.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_wdp/src/obstruction.rs::Cochain1`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_wdp/src/obstruction.rs::solve_exact_potential_weighted`](../../code/rust/src/)
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/native/src/derivation_dag_witnesses.rs::verify_tranche17_l1_emergence_gs000_gs001_replica_and_c10_branch_closure_witness`](../../code/rust/src/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0355](TFQ-0355_stop_at_the_open_residual-to-weight_gap_and_do_not_import_a_hilbert.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F000.S000`
- **Primary Source Paths**:
