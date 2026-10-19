# [TFQ-0294] Circle phases as an imported unit group

> **Stage**: `L1_TO_L2` | **Status**: `GAP`  
> **UUID**: `f30a6b2f-b24d-5cea-8112-9734ed29552e`  
> **Parent Derivation**: [TFQ-0293](tfq_0293_complex_field_as_a_declared_carrier.md)

---

## 1. Abstract & Formal Statement

U(1) phases on sector amplitudes are an import. qm_122_finite_hilbert_boundary_from_primitive_difference.md says the mixing leftover already runs on plus and minus one, and that excluding the sign group needs an extra non-exponent-two condition. That exclusion does not construct the circle. The circle stays imported, and continuity of a one-parameter phase group stays a hypothesis. phase_blind_quotient.rs enumerates a declared finite unit group inside the Gaussian rationals. phase_averaged_shadow.rs says the continuous Haar average is not computed.

### Governing Obligation
Import circle phases, or name the finite unit group actually enumerated.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `circle group U(1) (assumption)`
- **Admitted**: `circle group U(1): assumption`
- **Admitted**: `continuity of one-parameter phase group (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> See L1-U1-SELECTOR-OTHER-SEGMENT.

> [!WARNING]
> Algebraic non-square obstruction in Q(i) and rational Cayley punctured-circle parameterization are mechanized; compact continuous R/Z completion remains a declared external import.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.conditional_route_bridges_pg_l1_fq_ds_sixteen_route_closure`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.fq_gap_u1_circle_pythagorean_half_exponent_obstruction`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.fq_u1_selector_split_real_zero_divisors_and_cayley_unit_circle`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.l1_gap_u1_inner_product_orthogonal_additivity_and_isometric_dynamics_countermodels`](../../code/lean4/)
- [`lean4/quantum_mechanics/H011Circle.lean::sign_excluded_circle_still_imported`](../../code/lean4/)
- [`lean4/quantum_mechanics/H011U1SelectorBoundary.lean::selector_not_free`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_quantum_physics/src/complex_structure_selector.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/phase_averaged_shadow.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/phase_blind_quotient.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/phase_blind_quotient.rs::UnitPhaseGroup`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche15_gap_nonderivation_countermodels_and_conditional_route_bridges_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche2_row_sparsity_bell_torsion_and_structure_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche9_bloch_gap_cayley_u1_hadamard_coherence_and_destructive_interference_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_wdp/src/amplitude_bridge.rs::half_exponent_obstruction`](../../code/rust/src/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0295](tfq_0295_born_readout_of_a_supplied_lift_is_redundant.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001`, `F001.S000`, `F001.S000:001_from_primitive_difference_to_quantum_mechanics`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/floor.yaml`
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/shelf.yaml`
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/001_from_primitive_difference_to_quantum_mechanics/book/README.md`

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`L1-QM122-CIRCLE-SELECTOR-BOUNDARY`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `L1-QM122-CIRCLE-SELECTOR-BOUNDARY` (`L1_TO_L2` / `PROVED_LEAN`)
- **Mined Operad Family (`M2`)**: `OP-L1_TO_L2-L1-QM122-CIRCLE-SELECTOR-BOUNDARY`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [910, -1820, 1365]`, `chord_potential = 1365`, `holonomy_gamma2 = 1820`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(L1-QM122-CIRCLE-SELECTOR-BOUNDARY): 4*idx(91) + 3*stage_rank(6) + route_degree(4) == 386` ($\text{value} = 386$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(L1-QM122-CIRCLE-SELECTOR-BOUNDARY): R_raw(212) - G_cob(103) - S_decoy(6) == 103 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 103$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `1` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.l1_to_l2_and_cross_fragment_route_composition`
- **Sovereign Rust Witness Anchor**: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche14_cross_stage_route_composition_and_sorkin_hierarchy_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = 5479f83cbfbaea4a586a6fac7ba15720f40dc2d87c8faf1c06cf512ac1a19906`

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`L1-U1-SELECTOR-OTHER-SEGMENT`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `L1-U1-SELECTOR-OTHER-SEGMENT` (`L1_TO_L2` / `PROVED_LEAN`)
- **Mined Operad Family (`M2`)**: `OP-L1_TO_L2-L1-U1-SELECTOR-OTHER-SEGMENT`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [940, -1880, 1410]`, `chord_potential = 1410`, `holonomy_gamma2 = 1880`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(L1-U1-SELECTOR-OTHER-SEGMENT): 4*idx(94) + 3*stage_rank(6) + route_degree(3) == 397` ($\text{value} = 397$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(L1-U1-SELECTOR-OTHER-SEGMENT): R_raw(218) - G_cob(106) - S_decoy(6) == 106 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 106$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `0` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/lean/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm062_and_l1_u1_selector_frob_exclusions_and_gaussian_ring_injectivity`
- **Sovereign Rust Witness Anchor**: `omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/native/src/derivation_dag_witnesses.rs::verify_tranche19_ds_qm062_094_101_206_u1_selector_everett_threshold_and_boundary_synthesis_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = 25bbbb501bd826d64e5304b7235044a63b218647d94ad13773d4426e9fd619dd`

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`FQ-GAP-U1-CIRCLE`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `FQ-GAP-U1-CIRCLE` (`FINITE_QM_CORE` / `CONDITIONAL`)
- **Mined Operad Family (`M2`)**: `OP-FQ-CAYLEY-U1-PUNCTURED-CIRCLE`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [80, -160, 120]`, `chord_potential = 120`, `holonomy_gamma2 = 160`
- **Finite Shadow Exact Witness (`M4`)**: `cayley_t2_pythagorean_identity: (1 - 2^2)^2 + (2*2)^2 == (1 + 2^2)^2 == 25` ($\text{value} = 25$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `half_angle_obstruction: (a^2 - b^2 = 15 and 2ab = 20) has no integer solution (min_residual |(4^2-2^2)-15| + |2*4*2-20| = 3 + 4 = 7)` ($\text{value} = 7$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `2` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.conditional_route_bridges_pg_l1_fq_ds_sixteen_route_closure`
- **Sovereign Rust Witness Anchor**: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche15_gap_nonderivation_countermodels_and_conditional_route_bridges_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = 013e82297478109c69e3bdf8df3e4e441184ffbbc37583e7ea336f23c1c67d8d`

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`GP-IMPORT-CIRCLE-U1`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `GP-IMPORT-CIRCLE-U1` (`L1_TO_L2` / `IMPORTED_ASSUMPTION`)
- **Mined Operad Family (`M2`)**: `OP-GP-CIRCLE-U1-IMPORT`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [200, -400, 300]`, `chord_potential = 300`, `holonomy_gamma2 = 400`
- **Finite Shadow Exact Witness (`M4`)**: `sign_fiber_destructive_cancellation: (1 + (-1))^2 == 0 vs (1 + 1)^2 == 4 (gap 4)` ($\text{value} = 4$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `non_exponent_two_satisfied_by_Z3: |Z/3Z| == 3 (finite group of order 3 is not exponent-2 yet is not the circle U(1))` ($\text{value} = 3$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `2` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.gp_and_l1_imported_field_circle_dilation_and_time_interpolation_boundaries`
- **Sovereign Rust Witness Anchor**: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche11_admitted_primitives_definitions_and_imported_assumptions_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = 7c35753fa4028aabc0abad1200143bd785e3fa2d2f5fa1d396f4d05eba145d01`

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`L1-IMP-U1-PHASES`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `L1-IMP-U1-PHASES` (`L1_TO_L2` / `IMPORTED_ASSUMPTION`)
- **Mined Operad Family (`M2`)**: `OP-L1-U1-PHASE-GROUP-H011`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [330, -660, 495]`, `chord_potential = 495`, `holonomy_gamma2 = 660`
- **Finite Shadow Exact Witness (`M4`)**: `gaussian_phase_order_4: i^4 = 1 and |{1, i, -1, -i}| == 4` ($\text{value} = 4$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `sign_group_exponent_two_bound: (-1)^2 == 1 and |{+1,-1}| == 2 (sign group suffices for binary destructive interference)` ($\text{value} = 2$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `1` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.l1_gap_u1_inner_product_orthogonal_additivity_and_isometric_dynamics_countermodels`
- **Sovereign Rust Witness Anchor**: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche15_gap_nonderivation_countermodels_and_conditional_route_bridges_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = a699e6e2bbc0abecc474c7893b0069c53394debba69c1279cc0012cf98d545eb`
