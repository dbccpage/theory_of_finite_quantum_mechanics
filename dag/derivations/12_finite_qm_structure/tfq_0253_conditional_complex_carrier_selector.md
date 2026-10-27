# [TFQ-0253] Conditional complex-carrier selector

> **Stage**: `FINITE_QM_STRUCTURE` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `61ce663b-47da-5586-8d9f-3b67421a6b1e`  
> **Parent Derivation**: [TFQ-0251](tfq_0251_superposition_as_a_quotient_fiber.md)

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
- [`sources/atlas/papers/finite_quantum_mechanics/lean/DerivationDagQMClosure.lean`](../../code/lean4/)
- [`sources/atlas/papers/finite_quantum_mechanics/lean/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm062_and_l1_u1_selector_frob_exclusions_and_gaussian_ring_injectivity`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`external:sha256:ddaee3d0d77722244a6451750ca1e5acf7a57b4f02e75ecec70e810976d57d9e::PairingInvolution`](../../code/rust/src/)
- [`external:sha256:b4a0392795f1e742a256ae815cdc26550b49a4f6e92e1b8c6beb0d28f159c92d::verify_tranche19_ds_qm062_094_101_206_u1_selector_everett_threshold_and_boundary_synthesis_witness`](../../code/rust/src/)
- [`external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche13_ds_qm_final_16_second_witness_closure_witness`](../../code/rust/src/)
- [`external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche15_gap_nonderivation_countermodels_and_conditional_route_bridges_witness`](../../code/rust/src/)
- [`external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche19_ds_qm062_094_101_206_u1_selector_everett_threshold_and_boundary_synthesis_witness`](../../code/rust/src/)
- [`external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche2_row_sparsity_bell_torsion_and_structure_witness`](../../code/rust/src/)
- [`external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche4_edgewise_l1_u1_holonomy_chsh_and_cayley_witness`](../../code/rust/src/)
- [`external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche5_full_dag_177_node_coverage_witness`](../../code/rust/src/)
- [`external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche9_bloch_gap_cayley_u1_hadamard_coherence_and_destructive_interference_witness`](../../code/rust/src/)
- [`external:sha256:77726675ace7bc93c8e8203260618f203aa20359b38d15cd48dee38f04c7a89f::half_exponent_obstruction`](../../code/rust/src/)
- [`sources/atlas/papers/finite_quantum_mechanics/native/src/derivation_dag_witnesses.rs::verify_tranche19_ds_qm062_094_101_206_u1_selector_everett_threshold_and_boundary_synthesis_witness`](../../code/rust/src/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0254](tfq_0254_holonomy_structured_coherent_intensity.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `external:git-tree:662d50fe40fdbf9e98bc3ae140d0355d3b3a45f5`

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`DS-QM062-U1-SELECTOR-LAYERS`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `DS-QM062-U1-SELECTOR-LAYERS` (`FINITE_QM_STRUCTURE` / `PROVED_LEAN`)
- **Mined Operad Family (`M2`)**: `OP-FINITE_QM_STRUCTURE-DS-QM062-U1-SELECTOR-LAYERS`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [1470, -2940, 2205]`, `chord_potential = 2205`, `holonomy_gamma2 = 2940`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(DS-QM062-U1-SELECTOR-LAYERS): 4*idx(147) + 3*stage_rank(8) + route_degree(4) == 616` ($\text{value} = 616$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(DS-QM062-U1-SELECTOR-LAYERS): R_raw(334) - G_cob(163) - S_decoy(8) == 163 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 163$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `0` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `sources/atlas/papers/finite_quantum_mechanics/lean/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm062_and_l1_u1_selector_frob_exclusions_and_gaussian_ring_injectivity`
- **Sovereign Rust Witness Anchor**: `sources/atlas/papers/finite_quantum_mechanics/native/src/derivation_dag_witnesses.rs::verify_tranche19_ds_qm062_094_101_206_u1_selector_everett_threshold_and_boundary_synthesis_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = b708a3068d4620daa6a5374c808e0e9f8d7883d17eda4f32a423bb3b666d7773`

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`DS-QM062-U1-RESIDUES-IMPORT`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `DS-QM062-U1-RESIDUES-IMPORT` (`FINITE_QM_STRUCTURE` / `IMPORTED_ASSUMPTION`)
- **Mined Operad Family (`M2`)**: `OP-DS-U1-SELECTOR-RESIDUES`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [180, -360, 270]`, `chord_potential = 270`, `holonomy_gamma2 = 360`
- **Finite Shadow Exact Witness (`M4`)**: `elliptic_selector_det: det(3*I + 4*J) = 3^2 + 4^2 == 25` ($\text{value} = 25$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `split_complex_zero_divisor_det: det(1*I + 1*S) = 1^2 - 1^2 == 0 (hyperbolic ring has zero divisors)` ($\text{value} = 0$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `3` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_gap_measurement_projection_cptp_and_continuous_time_generator_countermodels`
- **Sovereign Rust Witness Anchor**: `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche15_gap_nonderivation_countermodels_and_conditional_route_bridges_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = 7f9d73950b35dbcb8f5978db02b992848c2592270bf4d1c1ff49de262004c453`

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`FQ-GAP-U1-CIRCLE`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `FQ-GAP-U1-CIRCLE` (`FINITE_QM_CORE` / `CONDITIONAL`)
- **Mined Operad Family (`M2`)**: `OP-FQ-CAYLEY-U1-PUNCTURED-CIRCLE`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [80, -160, 120]`, `chord_potential = 120`, `holonomy_gamma2 = 160`
- **Finite Shadow Exact Witness (`M4`)**: `cayley_t2_pythagorean_identity: (1 - 2^2)^2 + (2*2)^2 == (1 + 2^2)^2 == 25` ($\text{value} = 25$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `half_angle_obstruction: (a^2 - b^2 = 15 and 2ab = 20) has no integer solution (min_residual |(4^2-2^2)-15| + |2*4*2-20| = 3 + 4 = 7)` ($\text{value} = 7$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `2` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.conditional_route_bridges_pg_l1_fq_ds_sixteen_route_closure`
- **Sovereign Rust Witness Anchor**: `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche15_gap_nonderivation_countermodels_and_conditional_route_bridges_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = 013e82297478109c69e3bdf8df3e4e441184ffbbc37583e7ea336f23c1c67d8d`
