# [TFQ-0253] Conditional complex-carrier selector

> **Stage**: `FINITE_QM_STRUCTURE` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `61ce663b-47da-5586-8d9f-3b67421a6b1e`  
> **Parent Derivation**: [TFQ-0251](TFQ-0251_superposition_as_a_quotient_fiber.md)

---

## 1. Abstract & Formal Statement

QM_062 sharpens the open complex and U(1) selector. Its own status line says the note is not a derivation of the complex numbers from nothing. The header distinguishes a complex-structure layer, with a square root of minus one as an operator, from a claim that the ladder forces that layer. DS-QM062-U1-SELECTOR-LAYERS and DS-QM062-U1-RESIDUES-IMPORT record the layers and the imported residues, and FQ-GAP-U1-CIRCLE marks the circle as still open. A real plane can carry a complex structure and still admit operations that are not complex-linear, so naming an operator does not select an operational theory.

### Governing Obligation
Keep the complex carrier and the continuous circle as conditional imports; the selector paper does not derive them from an empty carrier.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `U(1) phase fiber and complex involution (assumption)`
- **Admitted**: `circle group U(1) (assumption)`
- **Admitted**: `connectedness / continuity (assumption)`
- **Admitted**: `continuity of one-parameter phase group (assumption)`
- **Admitted**: `local tomography (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> None (derived from parent DS-QM062-U1-RESIDUES-IMPORT via ds_qm062_and_l1_u1_selector_frob_exclusions_and_gaussian_ring_injectivity and ds_qm062_u1_selector_layers_and_ring_iso).

> [!WARNING]
> Overlaps FQ-GAP-U1-CIRCLE (other fragment); here it is the 062/207 ledger statement.

> [!WARNING]
> Algebraic non-square obstruction in Q(i) and rational Cayley punctured-circle parameterization are mechanized; compact continuous R/Z completion remains a declared external import.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.conditional_route_bridges_pg_l1_fq_ds_sixteen_route_closure`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_gap_measurement_projection_cptp_and_continuous_time_generator_countermodels`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm062_and_l1_u1_selector_frob_exclusions_and_gaussian_ring_injectivity`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm062_u1_selector_layers_and_ring_iso`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.fq_gap_u1_circle_pythagorean_half_exponent_obstruction`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.fq_u1_selector_split_real_zero_divisors_and_cayley_unit_circle`](../../code/lean4/)
- [`lean4/quantum_mechanics/H011U1SelectorBoundary.lean::u1_selector_boundary`](../../code/lean4/)
- [`lean4/quantum_mechanics/U1AngleAddition.lean::J_squared_eq_neg_id`](../../code/lean4/)
- [`lean4/quantum_mechanics/U1AngleAddition.lean::one_parameter_group_law`](../../code/lean4/)
- [`lean4/quantum_mechanics/U1TorsionExclusion.lean::period_lattice_infinite`](../../code/lean4/)
- [`lean4/quantum_mechanics/U1TorsionExclusion.lean::torsion_order_excluded`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/lean/DerivationDagQMClosure.lean`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/lean/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm062_and_l1_u1_selector_frob_exclusions_and_gaussian_ring_injectivity`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_quantum_physics/src/complex_structure_selector.rs::PairingInvolution`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/derivation_dag_witnesses.rs::verify_tranche19_ds_qm062_094_101_206_u1_selector_everett_threshold_and_boundary_synthesis_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche13_ds_qm_final_16_second_witness_closure_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche15_gap_nonderivation_countermodels_and_conditional_route_bridges_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche19_ds_qm062_094_101_206_u1_selector_everett_threshold_and_boundary_synthesis_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche2_row_sparsity_bell_torsion_and_structure_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche4_edgewise_l1_u1_holonomy_chsh_and_cayley_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche5_full_dag_177_node_coverage_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche9_bloch_gap_cayley_u1_hadamard_coherence_and_destructive_interference_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_wdp/src/amplitude_bridge.rs::half_exponent_obstruction`](../../code/rust/src/)
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/native/src/derivation_dag_witnesses.rs::verify_tranche19_ds_qm062_094_101_206_u1_selector_everett_threshold_and_boundary_synthesis_witness`](../../code/rust/src/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0254](TFQ-0254_holonomy-structured_coherent_intensity.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`DS-QM062-U1-SELECTOR-LAYERS`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `DS-QM062-U1-SELECTOR-LAYERS` (`FINITE_QM_STRUCTURE` / `PROVED_LEAN`)
- **Mined Operad Family (`M2`)**: `OP-FINITE_QM_STRUCTURE-DS-QM062-U1-SELECTOR-LAYERS`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [1470, -2940, 2205]`, `chord_potential = 2205`, `holonomy_gamma2 = 2940`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(DS-QM062-U1-SELECTOR-LAYERS): 4*idx(147) + 3*stage_rank(8) + route_degree(4) == 616` ($\text{value} = 616$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(DS-QM062-U1-SELECTOR-LAYERS): R_raw(334) - G_cob(163) - S_decoy(8) == 163 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 163$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `0` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/lean/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm062_and_l1_u1_selector_frob_exclusions_and_gaussian_ring_injectivity`
- **Sovereign Rust Witness Anchor**: `omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/native/src/derivation_dag_witnesses.rs::verify_tranche19_ds_qm062_094_101_206_u1_selector_everett_threshold_and_boundary_synthesis_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = b708a3068d4620daa6a5374c808e0e9f8d7883d17eda4f32a423bb3b666d7773`
