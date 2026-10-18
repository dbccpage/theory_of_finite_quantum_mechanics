# [TFQ-0349] Compute declared Phi1 and Gamma2 on a finite window, and do not

> **Stage**: `L1_EMERGENCE` | **Status**: `SOURCE_RECORD`  
> **UUID**: `7d92ecf2-0981-50ae-b43b-15af02bc16d9`  
> **Parent Derivation**: [TFQ-0345](../06_wdp/TFQ-0345_on_a_declared_window_with_d1_d0_0_compute_q1_kappa1.md)

---

## 1. Abstract & Formal Statement

DAG node L1-WDP-WINDOW-PHI1-GAMMA2 restates the declared window: Phi1 of a class is the quotient seminorm, the minimum of a weighted l1 norm of x minus d0 h, and Gamma2 is the l1 norm of d1 on a minimizer. The node says the weighted l1 form is declared, not derived from MSS-0 or from Difference, and it warns that WDP Gamma2 is a norm while a later QM note uses Gamma for a set of residual sectors. primitive_axiomatics.rs says Root P owns no arithmetic: d0 and d1 come from omega_homology, and Phi1, Gamma2, and the trichotomy come from omega_functional.

### Governing Obligation
Compute declared Phi1 and Gamma2 on a finite window, and do not treat the weighted l1 norm as derived from MSS-0.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Complex/chain structure d1 d0 = 0 (assumption: window hypothesis)`
- **Admitted**: `Finite-dimensional real/complex vector space and norm J (assumption: declared)`
- **Admitted**: `weighted l1 norm on C1 (declared, see L1-OBSERVER-AXIOMS-H1-H5): assumption`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> The weighted l1 form of the norm is declared in the window definition, not derived from MSS-0 or Difference. Upstream window construction is in the WDP fragment.

> [!WARNING]
> The window is declared, not derived from <> or Real_0 (PG-GAP-GENESIS-TO-WINDOW). Geometry derivation belongs to the L1 emergence fragment.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.conditional_route_bridges_pg_l1_fq_ds_sixteen_route_closure`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.l1_gs001_replica_and_phi1_quotient_invariance`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.l1_observer_h1_h5_cochain_flatness_and_wdp_window_mass_realification`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/lean4/WitnessedDifference/Obstruction.lean::Repair`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/lean4/WitnessedDifference/Obstruction.lean::kappa`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_functional/src/phi1.rs::Phi1Functional`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche11_admitted_primitives_definitions_and_imported_assumptions_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche15_gap_nonderivation_countermodels_and_conditional_route_bridges_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche3_emergence_dynamics_heisenberg_and_qec_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_wdp/src/obstruction.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_wdp/src/obstruction.rs::Cochain1`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_wdp/src/obstruction.rs::solve_exact_potential_weighted`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_wdp/src/phi1_coda_adapter.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_wdp/src/primitive_axiomatics.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_wdp/src/primitive_axiomatics.rs::TriadSignature`](../../code/rust/src/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0350](TFQ-0350_assume_d1_d0_0_only_by_a_declared_certificate_or_the.md)
- [TFQ-0352](TFQ-0352_admit_h1_through_h5_as_observer_hypotheses_on_a_finite_edge_projection.md)
- [TFQ-0357](TFQ-0357_record_replica_extensivity_as_a_reason_l1_appears_and_keep_squared_l2.md)
- [TFQ-0358](TFQ-0358_normalize_a_declared_positive_witness_mass_to_cell_values_that_are_nonnegative.md)
- [TFQ-0359](TFQ-0359_keep_the_phi1_banach-quotient_reading_on_a_finite-dimensional_repair_packet_and_leave.md)

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

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`L1-OBSERVER-AXIOMS-H1-H5`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `L1-OBSERVER-AXIOMS-H1-H5` (`L1_EMERGENCE` / `ADMITTED_PRIMITIVE`)
- **Mined Operad Family (`M2`)**: `OP-L1_EMERGENCE-L1-OBSERVER-AXIOMS-H1-H5`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [700, -1400, 1050]`, `chord_potential = 1050`, `holonomy_gamma2 = 1400`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(L1-OBSERVER-AXIOMS-H1-H5): 4*idx(70) + 3*stage_rank(5) + route_degree(5) == 300` ($\text{value} = 300$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(L1-OBSERVER-AXIOMS-H1-H5): R_raw(165) - G_cob(80) - S_decoy(5) == 80 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 80$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `2` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/lean/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.gs003_coordinate_l1_weighted_sum_and_orbit_collapse`
- **Sovereign Rust Witness Anchor**: `omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/native/src/derivation_dag_witnesses.rs::verify_tranche17_l1_emergence_gs000_gs001_replica_and_c10_branch_closure_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = 0bf2e578f1165af226304c4fcb0352e7047249cecbcf97fd368d7a8b75905f6e`
