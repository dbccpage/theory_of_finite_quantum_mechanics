# [TFQ-0007] Finite quantum mechanics core on an admitted carrier

> **Stage**: `FINITE_QM_CORE` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `ca5793f0-74ef-5045-8426-ca1ec4993e6c`  
> **Parent Derivation**: [TFQ-0006](../08_l1_to_l2/tfq_0006_conditional_finite_hilbert_lift.md)

---

## 1. Abstract & Formal Statement

F001 coordinates finite Hilbert lifts, Born normalization, density-matrix geometry, and dual witness functionals. Its exit contract asks for exact duality-gap certificates, Lean 4 models, and Kraus transport audits. Those artifacts are the work, not a receipt that the work is finished. This gate fixes the order: a finite state, a finite effect, and a pairing on one admitted carrier come before channels, QED, QCD, and gravity. The three languages must name that carrier. Float tolerances do not authorize the pairing.

### Governing Obligation
Fix one finite carrier for states, effects, and pairings before dynamics, gauge theory, or gravity.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Formalization
- **Primary Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.master_operad_25_family_composition_and_end_to_end_chain_closure` (zero-axiom, zero-sorry kernel verification in `lean/DerivationDagQMClosure.lean`).

### Sovereign Rust Certifiers
- **Primary Rust Witness**: `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche16_master_177_node_172_route_dag_completeness_and_operad_audit_witness` (`code/rust/src/dag_witnesses.rs`, exact `i64`/`BigRational` arithmetic).
- **Python PFP Gate Engine**: `external:sha256:c526457bbf0fece01b6416f1a2524f9499bede37eb02e15a940eec358d6d45b4::verify_dag_prompt_node_reply` (`G0`..`G6`).

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0008](../11_finite_qm_dynamics/tfq_0008_finite_dynamics_instruments_and_channels.md)
- [TFQ-0125](../21_implementation_core/tfq_0125_crate_index_and_derivation_witnesses.md)
- [TFQ-0166](../22_implementation_sibling/tfq_0166_record_these_sibling_crates_as_controls_under_authorityeffect_none_not_as_completed.md)
- [TFQ-0200](../23_engine_custody/tfq_0200_three_language_custody_on_the_engine_runtime.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `external:sha256:3429888abb5e68b4f86f2bd9efe085b8dcdc981179166df315b7b6acf23de0b6`

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`FQ-CARRIER-CONTRACT-V2`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `FQ-CARRIER-CONTRACT-V2` (`FINITE_QM_CORE` / `DEFINITION`)
- **Mined Operad Family (`M2`)**: `OP-FINITE_QM_CORE-FQ-CARRIER-CONTRACT-V2`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [970, -1940, 1455]`, `chord_potential = 1455`, `holonomy_gamma2 = 1940`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(FQ-CARRIER-CONTRACT-V2): 4*idx(97) + 3*stage_rank(7) + route_degree(17) == 426` ($\text{value} = 426$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(FQ-CARRIER-CONTRACT-V2): R_raw(229) - G_cob(111) - S_decoy(7) == 111 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 111$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `3` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.master_operad_25_family_composition_and_end_to_end_chain_closure`
- **Sovereign Rust Witness Anchor**: `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche16_master_177_node_172_route_dag_completeness_and_operad_audit_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = f1df1f0f341241f290f96a145d8da58e8f8f327e0a843c796500c0d30bdfbf9b`

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`FQ-DECLARED-QUANTUM-INTERFACE`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `FQ-DECLARED-QUANTUM-INTERFACE` (`FINITE_QM_CORE` / `IMPORTED_ASSUMPTION`)
- **Mined Operad Family (`M2`)**: `OP-FQ-DECLARED-INTERFACE-GATE`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [10, -20, 15]`, `chord_potential = 15`, `holonomy_gamma2 = 20`
- **Finite Shadow Exact Witness (`M4`)**: `interface_bundle_component_count == 6 and gaussian_norm_3_4 == 25` ($\text{value} = 31$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `drop_one_import_surviving_axioms == 5 (none of the 6 components is derived from primitive difference <> alone)` ($\text{value} = 5$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `6` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.l1_and_ds_imported_assumption_separation_certificates`
- **Sovereign Rust Witness Anchor**: `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche10_chsh_tsirelson_pr_box_tier3_uniqueness_edgewise_l1_and_import_boundaries_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = 044fe92e7a52dad38b13fc9ad5aed5bbda1b87e3d6803bb5f67f52a2a091180e`

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`FQ-GAP-C500-ORIGINAL-TARGETS`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `FQ-GAP-C500-ORIGINAL-TARGETS` (`FINITE_QM_CORE` / `OPEN`)
- **Mined Operad Family (`M2`)**: `OP-FQ-C500-SCOPE-REDUCTION`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [30, -60, 45]`, `chord_potential = 45`, `holonomy_gamma2 = 60`
- **Finite Shadow Exact Witness (`M4`)**: `c500_total_blocks == 10 and scoped_evidence_blocks == 10` ($\text{value} = 100$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `block10_unpaid_bet_clauses_count(M2,M5,M7,J1,J2) == 5` ($\text{value} = 5$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `0` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.fq_gap_c500_ten_blocks_and_custody_axiom_audit_certificate`
- **Sovereign Rust Witness Anchor**: `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche6_conditional_and_open_boundary_certificates_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = d2f6692c4de4b94cc37d6e542849c39863fc352d33fb48b275a642f888db2e0c`

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`FQ-GAP-CORPUS-REWRITE`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `FQ-GAP-CORPUS-REWRITE` (`FINITE_QM_CORE` / `OPEN`)
- **Mined Operad Family (`M2`)**: `OP-FQ-CORPUS-CONSOLIDATION`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [50, -100, 75]`, `chord_potential = 75`, `holonomy_gamma2 = 100`
- **Finite Shadow Exact Witness (`M4`)**: `dag_total_nodes == 177 and dag_total_routes == 172` ($\text{value} = 349$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `unfinished_boundary_prompts_count == 35 (consolidation narrows scope without discharging the 35 boundary nodes)` ($\text{value} = 35$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `0` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.fq_gap_c500_ten_blocks_and_custody_axiom_audit_certificate`
- **Sovereign Rust Witness Anchor**: `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche6_conditional_and_open_boundary_certificates_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = 89825786c3ee13dfe19236bee5a20cf37647c4b68b434a462cd2822121966815`

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`FQ-PRIM-TO-QM-SELECTION-OPEN`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `FQ-PRIM-TO-QM-SELECTION-OPEN` (`FINITE_QM_CORE` / `CONDITIONAL`)
- **Mined Operad Family (`M2`)**: `OP-FQ-PRIM-TO-QM-PARAMETER-GAP`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [100, -200, 150]`, `chord_potential = 150`, `holonomy_gamma2 = 200`
- **Finite Shadow Exact Witness (`M4`)**: `d3_parameter_hierarchy: diag_params(3-1=2) + rebit_params(3*4/2-1=5) + qubit_params(3^2-1=8) == 15` ($\text{value} = 15$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `d3_qubit_minus_diagonal_parameter_gap: (3^2 - 1) - (3 - 1) == 6 unfixed coherence parameters` ($\text{value} = 6$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `1` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.conditional_route_bridges_pg_l1_fq_ds_sixteen_route_closure`
- **Sovereign Rust Witness Anchor**: `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche15_gap_nonderivation_countermodels_and_conditional_route_bridges_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = afcfb80d98f91d52fe05966a4b8f466848f83f0af6e760fe4672a846036d6192`
