# [TFQ-0301] Haar-independent phases are not the finite average

> **Stage**: `L1_TO_L2` | **Status**: `GAP`  
> **UUID**: `713e8a02-91bd-5e62-9978-eaaa9e5d39cd`  
> **Parent Derivation**: [TFQ-0300](tfq_0300_descent_compatible_maps_stay_row_sparse.md)

---

## 1. Abstract & Formal Statement

Independent Haar phases are an import. The section labeled Theorem 5 in qm_020_born_normalization_and_conditional_hilbert_lift.md conditions the phase-averaged shadow on a chosen Hilbert lift, a Haar phase measure, and an independence adapter. The finite obligation is narrower. phase_averaged_shadow.rs averages over a declared finite unit group by enumeration, says a nontrivial finite group is only a stand-in that dephases, and states that the continuous Haar average is not computed. The trivial group averages nothing. Budgets refuse enumerations that are too large.

### Governing Obligation
Import Haar independence, or label the finite phase-group average as a stand-in.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Haar probability measure on U(1)^n: assumption`
- **Admitted**: `independence of phases: assumption`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> No measure-theoretic discharge; finite group stand-in only.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.l1_and_ds_imported_assumption_separation_certificates`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.l1_gap_u1_inner_product_orthogonal_additivity_and_isometric_dynamics_countermodels`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.l1_qm020_thm5_phase_averaged_shadow_and_c10_pinching`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`external:sha256:726fa8afa05803e040d092cf665b4a775fb5f3626f1631071aac9763510e15d5`](../../code/rust/src/)
- [`external:sha256:726fa8afa05803e040d092cf665b4a775fb5f3626f1631071aac9763510e15d5::phase_group_average`](../../code/rust/src/)
- [`external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche10_chsh_tsirelson_pr_box_tier3_uniqueness_edgewise_l1_and_import_boundaries_witness`](../../code/rust/src/)
- [`external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche15_gap_nonderivation_countermodels_and_conditional_route_bridges_witness`](../../code/rust/src/)
- [`external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche5_full_dag_177_node_coverage_witness`](../../code/rust/src/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0302](tfq_0302_phase_averaged_shadow_under_declared_phases.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001`, `F001.S000`, `F001.S000:001_from_primitive_difference_to_quantum_mechanics`
- **Primary Source Paths**:
  - `external:sha256:ddbf8bad986fa5587b534c0f96f2c4ff370f95cb696c6245df0526d4bad32351`
  - `external:sha256:3429888abb5e68b4f86f2bd9efe085b8dcdc981179166df315b7b6acf23de0b6`
  - `external:sha256:aa96a8bb76ae8bc4e83571f57783f369b645332421db0e1fdd8a7d9cf333aac9`

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`L1-QM020-THM5-PHASE-AVERAGED-SHADOW`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `L1-QM020-THM5-PHASE-AVERAGED-SHADOW` (`L1_TO_L2` / `PROVED_LEAN`)
- **Mined Operad Family (`M2`)**: `OP-L1_TO_L2-L1-QM020-THM5-PHASE-AVERAGED-SHADOW`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [850, -1700, 1275]`, `chord_potential = 1275`, `holonomy_gamma2 = 1700`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(L1-QM020-THM5-PHASE-AVERAGED-SHADOW): 4*idx(85) + 3*stage_rank(6) + route_degree(2) == 360` ($\text{value} = 360$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(L1-QM020-THM5-PHASE-AVERAGED-SHADOW): R_raw(200) - G_cob(97) - S_decoy(6) == 97 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 97$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `3` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.l1_qm020_thm5_thm7_and_qm121_ladder_rungs_2_to_6_separation`
- **Sovereign Rust Witness Anchor**: `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche12_pg_l1_fq_gp_second_witness_certificates_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = 3d5a0f9699dd28e2deafe7005f514777057ae3dd3f72038b4bdb2a7d955ab1be`

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`L1-IMP-HAAR-INDEPENDENT-PHASES`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `L1-IMP-HAAR-INDEPENDENT-PHASES` (`L1_TO_L2` / `IMPORTED_ASSUMPTION`)
- **Mined Operad Family (`M2`)**: `OP-L1-HAAR-VS-FINITE-Z4-AVERAGE`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [280, -560, 420]`, `chord_potential = 420`, `holonomy_gamma2 = 560`
- **Finite Shadow Exact Witness (`M4`)**: `z4_squared_16_pair_diagonal_sum: 16 * (|3|^2 + |4|^2) == 16 * 25 == 400` ($\text{value} = 400$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `correlated_equal_phase_subgroup_cross_term: 4 * (2 * 3 * 4) == 96 != 0 (without independent phases, cross term 96 survives)` ($\text{value} = 96$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `2` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.l1_gap_u1_inner_product_orthogonal_additivity_and_isometric_dynamics_countermodels`
- **Sovereign Rust Witness Anchor**: `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche15_gap_nonderivation_countermodels_and_conditional_route_bridges_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = 089e8e01b9ef4087dd2f6c07d6b319d7719553d03d545793b0c9c3ebd81ce890`
