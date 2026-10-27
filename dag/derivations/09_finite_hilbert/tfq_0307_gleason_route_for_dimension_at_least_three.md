# [TFQ-0307] Gleason route for dimension at least three

> **Stage**: `FINITE_HILBERT` | **Status**: `GAP`  
> **UUID**: `1b78f444-5650-5192-b56b-a321c7702ee0`  
> **Parent Derivation**: [TFQ-0306](../08_l1_to_l2/tfq_0306_born_uniqueness_stays_an_imported_boundary.md)

---

## 1. Abstract & Formal Statement

Gleason for dimension n at least 3 is an import. In qm_020_born_normalization_and_conditional_hilbert_lift.md the section labeled Theorem 6, part 2, cites a Gleason route under frame-function hypotheses and says dimension 2 needs a further POVM or continuity strengthening. qm_122_finite_hilbert_boundary_from_primitive_difference.md records that a two-label host fails the dimension extra and that uniqueness at n at least 3 stays imported. The claim ledger calls that a dim-2 obstruction, not a bridge to the full package. derivation_dag.json records L1-QM020-THM6-P2-GLEASON and FQ-GAP-BORN-UNIQUENESS-GLEASON.

### Governing Obligation
Import Gleason hypotheses for n at least 3 and keep the two-label host below that bar.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Gleason theorem for d >= 3 (assumption)`
- **Admitted**: `Gleason theorem: assumption`
- **Admitted**: `Hilbert space (assumption)`
- **Admitted**: `complex Hilbert space of dim >= 3: assumption`
- **Admitted**: `orthogonal additivity / frame functions: assumption`
- **Admitted**: `projection lattice (assumption)`
- **Admitted**: `reversible linear isometric dynamics: assumption`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Gleason is cited, not proved here. GleasonTheorem.lean states it is NOT a proof of Gleason's theorem. native/src/campaigns/born_gleason.rs exists under 006_finite_qm (accept dim3 / refuse dim2 / refuse real scalars per ledger; test names not checked).

> [!WARNING]
> Finite rational frame obstructions (Cabello 18-9, d=2 plane, and d=3 rotated frame eliminating the quartic rival) are mechanized; continuum Gleason frame additivity on S^{n-1} remains an external import.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/BornNormalization.lean`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.conditional_route_bridges_pg_l1_fq_ds_sixteen_route_closure`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm072_073_090_and_fq_import_boundary_certificates`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.fq_gleason_d3_orthogonal_frame_additivity_eliminates_quartic_rival`](../../code/lean4/)
- [`lean4/quantum_mechanics/FiniteQM.lean`](../../code/lean4/)
- [`lean4/quantum_mechanics/GleasonTheorem.lean`](../../code/lean4/)
- [`lean4/quantum_mechanics/H013QuarticRivalSeparation.lean::frames_equinorm`](../../code/lean4/)
- [`lean4/quantum_mechanics/H017Gleason.lean::gleason_pack_uniqueness_still_imported`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`external:sha256:ae888a69f68011cf2bdbe26b173cbe6cf818f2a9c044b25aa7b39f5592b688c5`](../../code/rust/src/)
- [`external:sha256:c8f020f9abf33d6d86e8630fd8f9d3da0bb1db91835d6dfcbe56cfa4709cad7e`](../../code/rust/src/)
- [`external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche15_gap_nonderivation_countermodels_and_conditional_route_bridges_witness`](../../code/rust/src/)
- [`external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche2_row_sparsity_bell_torsion_and_structure_witness`](../../code/rust/src/)
- [`external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche7_wdp_bridge_o03_o05_sector_orbit_and_gleason_rival_witness`](../../code/rust/src/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0308](tfq_0308_born_uniqueness_band_slot_is_still_a_stub.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001`, `F001.S000`, `F001.S000:001_from_primitive_difference_to_quantum_mechanics`
- **Primary Source Paths**:
  - `external:sha256:ddbf8bad986fa5587b534c0f96f2c4ff370f95cb696c6245df0526d4bad32351`
  - `external:sha256:3429888abb5e68b4f86f2bd9efe085b8dcdc981179166df315b7b6acf23de0b6`
  - `external:sha256:aa96a8bb76ae8bc4e83571f57783f369b645332421db0e1fdd8a7d9cf333aac9`
  - `external:sha256:49250fc3940b574236fe8aeb8acabb9673af35fe28f17474e9deb52ecd18a713`

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`L1-QM122-BORN-PAIRING-NONUNIQUE`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `L1-QM122-BORN-PAIRING-NONUNIQUE` (`L1_TO_L2` / `PROVED_LEAN`)
- **Mined Operad Family (`M2`)**: `OP-L1_TO_L2-L1-QM122-BORN-PAIRING-NONUNIQUE`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [920, -1840, 1380]`, `chord_potential = 1380`, `holonomy_gamma2 = 1840`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(L1-QM122-BORN-PAIRING-NONUNIQUE): 4*idx(92) + 3*stage_rank(6) + route_degree(3) == 389` ($\text{value} = 389$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(L1-QM122-BORN-PAIRING-NONUNIQUE): R_raw(214) - G_cob(104) - S_decoy(6) == 104 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 104$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `1` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.l1_to_l2_and_cross_fragment_route_composition`
- **Sovereign Rust Witness Anchor**: `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche14_cross_stage_route_composition_and_sorkin_hierarchy_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = 0792ec8456cc7ac2b8647859c7410e1e5cb867f76c9e242099cb1aa7478f78c6`

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`FQ-GLEASON-D2-RATIONAL-PLANE-OBSTRUCTION`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `FQ-GLEASON-D2-RATIONAL-PLANE-OBSTRUCTION` (`FINITE_QM_CORE` / `PROVED_LEAN`)
- **Mined Operad Family (`M2`)**: `OP-FINITE_QM_CORE-FQ-GLEASON-D2-RATIONAL-PLANE-OBSTRUCTION`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [1060, -2120, 1590]`, `chord_potential = 1590`, `holonomy_gamma2 = 2120`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(FQ-GLEASON-D2-RATIONAL-PLANE-OBSTRUCTION): 4*idx(106) + 3*stage_rank(7) + route_degree(3) == 448` ($\text{value} = 448$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(FQ-GLEASON-D2-RATIONAL-PLANE-OBSTRUCTION): R_raw(247) - G_cob(120) - S_decoy(7) == 120 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 120$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `1` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/GleasonTheorem.lean::d2_binary_non_bornian_obstruction`
- **Sovereign Rust Witness Anchor**: `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche12_pg_l1_fq_gp_second_witness_certificates_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = 5c8524efabc0c7508c5938c6125653dac11b1547d5ad4fae6a2ce8153215e408`

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`FQ-BUSCH-EFFECT-FRAME`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `FQ-BUSCH-EFFECT-FRAME` (`FINITE_QM_STRUCTURE` / `PROVED_LEAN`)
- **Mined Operad Family (`M2`)**: `OP-FINITE_QM_STRUCTURE-FQ-BUSCH-EFFECT-FRAME`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [1090, -2180, 1635]`, `chord_potential = 1635`, `holonomy_gamma2 = 2180`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(FQ-BUSCH-EFFECT-FRAME): 4*idx(109) + 3*stage_rank(8) + route_degree(3) == 463` ($\text{value} = 463$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(FQ-BUSCH-EFFECT-FRAME): R_raw(258) - G_cob(125) - S_decoy(8) == 125 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 125$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `2` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.fq_core_phase_sorkin_gleason_busch_tsirelson_dynamics_route_composition`
- **Sovereign Rust Witness Anchor**: `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche14_cross_stage_route_composition_and_sorkin_hierarchy_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = ee337aecf2c6a1fcaf1dd832d1e9e6384c5d861854ab0f72d97382c34cb16302`

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`FQ-GAP-BORN-UNIQUENESS-GLEASON`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `FQ-GAP-BORN-UNIQUENESS-GLEASON` (`FINITE_QM_CORE` / `CONDITIONAL`)
- **Mined Operad Family (`M2`)**: `OP-FQ-SORKIN-GLEASON-BUSCH`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [20, -40, 30]`, `chord_potential = 30`, `holonomy_gamma2 = 40`
- **Finite Shadow Exact Witness (`M4`)**: `cabello_18_9_ray_sum == 18*2 and quartic_vs_born_frame_gap == 25^2 - (9 + 16)^2 + 288` ($\text{value} = 324$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `d2_unit_effect_two_pairings_disagree: l1_sum(3,4)=7 != l2_sq_sum(3,4)=25 (25 - 7 = 18)` ($\text{value} = 18$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `3` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.conditional_route_bridges_pg_l1_fq_ds_sixteen_route_closure`
- **Sovereign Rust Witness Anchor**: `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche15_gap_nonderivation_countermodels_and_conditional_route_bridges_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = 6d40469bbfc2d3d2b3b767b3d0ef508bddb0b142c6c691c175557fdc62c670d2`

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`GP-IMPORT-GLEASON`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `GP-IMPORT-GLEASON` (`L1_TO_L2` / `IMPORTED_ASSUMPTION`)
- **Mined Operad Family (`M2`)**: `OP-GP-GLEASON-FRAME-IMPORT`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [250, -500, 375]`, `chord_potential = 375`, `holonomy_gamma2 = 500`
- **Finite Shadow Exact Witness (`M4`)**: `sorkin_i3_quadratic_vanishing: I_3^(2)(1,1,1) = 3^2 - (2^2+2^2+2^2) + (1^2+1^2+1^2) == 0` ($\text{value} = 0$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `sorkin_i3_cubic_rival_nonzero: I_3^(3)(1,1,1) = 3^3 - 3*(2^3) + 3*(1^3) = 27 - 24 + 3 == 6` ($\text{value} = 6$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `2` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.l1_gap_u1_inner_product_orthogonal_additivity_and_isometric_dynamics_countermodels`
- **Sovereign Rust Witness Anchor**: `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche15_gap_nonderivation_countermodels_and_conditional_route_bridges_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = 340be3c3eed8b31920e6de8dde740d023fe82c7ea5d952f59c5c7bf02573d0d3`

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`L1-QM020-THM6-P2-GLEASON`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `L1-QM020-THM6-P2-GLEASON` (`L1_TO_L2` / `IMPORTED_ASSUMPTION`)
- **Mined Operad Family (`M2`)**: `OP-L1-GLEASON-BORN-UNIQUENESS`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [350, -700, 525]`, `chord_potential = 525`, `holonomy_gamma2 = 700`
- **Finite Shadow Exact Witness (`M4`)**: `gleason_firewall_premise_count == 7 and min_hilbert_dim == 3 (sum 10)` ($\text{value} = 10$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `d2_bloch_hemisphere_noncontextual_defect: d_min(3) - d_qubit(2) == 1 (dim 2 admits Kochen-Specker noncontextual dispersion-free countermodels without POVM)` ($\text{value} = 1$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `4` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/H017Gleason.lean::gleason_pack_uniqueness_still_imported`
- **Sovereign Rust Witness Anchor**: `external:sha256:c8f020f9abf33d6d86e8630fd8f9d3da0bb1db91835d6dfcbe56cfa4709cad7e`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = 7a5387ea551a1209b938051f7c7367aad747053e4ef2bb74cb7f7382d3ed6355`
