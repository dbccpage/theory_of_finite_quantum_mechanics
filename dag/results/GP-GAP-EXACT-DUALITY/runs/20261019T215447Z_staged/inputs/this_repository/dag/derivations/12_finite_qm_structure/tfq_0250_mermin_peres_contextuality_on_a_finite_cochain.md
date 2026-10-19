# [TFQ-0250] Mermin-Peres contextuality on a finite cochain

> **Stage**: `FINITE_QM_STRUCTURE` | **Status**: `SOURCE_RECORD`  
> **UUID**: `2101fa9a-11bb-5615-9878-a7ea1f3b9a95`  
> **Parent Derivation**: [TFQ-0249](tfq_0249_trace_zero_summaries_do_not_fix_commutation.md)

---

## 1. Abstract & Formal Statement

QM_120 obliges a Mermin-Peres parity obstruction as a cochain fact on a declared finite packet. DS-QM120-MERMIN-PERES-F2-OBSTRUCTION says the six signed contexts have no global plus-or-minus assignment, because the declared signs multiply to minus one while any global assignment multiplies to plus one, and that every single context and every five-context subset remains satisfiable. The incidence form is an F2 cochain obstruction. The node says this derives neither quantum mechanics nor a Hilbert space.

### Governing Obligation
Record the finite Mermin-Peres parity obstruction on its declared contexts, without deriving a Hilbert space from that packet.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `declared measurement scenarios and contexts (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Lean names in the ledger (QM.MerminPeres.*) differ from names on disk (see notes).

> [!WARNING]
> Scenario and second measurement context are admitted; the cochain construction does not derive them.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/ContextualityObstruction.lean::d0_of_global_section`](../../code/lean4/)
- [`lean4/quantum_mechanics/ContextualityObstruction.lean::differential_squares_to_zero`](../../code/lean4/)
- [`lean4/quantum_mechanics/ContextualityObstruction.lean::x1_has_no_global_section`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm120_mermin_peres_f2_no_global_section`](../../code/lean4/)
- [`lean4/quantum_mechanics/DualWitness.lean::mermin_peres_parity_obstruction`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/lean/DerivationDagQMClosure.lean`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_quantum_physics/src/contextuality_obstruction.rs::construct_cabello_scenario`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/kochen_specker.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/parity_context_packet.rs::ParityAdmission`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche2_row_sparsity_bell_torsion_and_structure_witness`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`FQ-CABELLO-NO-INTEGER-FRAME`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `FQ-CABELLO-NO-INTEGER-FRAME` (`FINITE_QM_CORE` / `PROVED_LEAN`)
- **Mined Operad Family (`M2`)**: `OP-FINITE_QM_CORE-FQ-CABELLO-NO-INTEGER-FRAME`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [1070, -2140, 1605]`, `chord_potential = 1605`, `holonomy_gamma2 = 2140`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(FQ-CABELLO-NO-INTEGER-FRAME): 4*idx(107) + 3*stage_rank(7) + route_degree(5) == 454` ($\text{value} = 454$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(FQ-CABELLO-NO-INTEGER-FRAME): R_raw(249) - G_cob(121) - S_decoy(7) == 121 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 121$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `1` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/H053EverettForkingTree.lean::cabello_parity_obstruction`
- **Sovereign Rust Witness Anchor**: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche12_pg_l1_fq_gp_second_witness_certificates_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = ee4503323cdc9ca06aa0d15cd5d4cc48c7a7b5cf08b95a7d7d32130d3df07b18`

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`FQ-CONTEXTUALITY-CECH-F2`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `FQ-CONTEXTUALITY-CECH-F2` (`FINITE_QM_CORE` / `PROVED_LEAN`)
- **Mined Operad Family (`M2`)**: `OP-FINITE_QM_CORE-FQ-CONTEXTUALITY-CECH-F2`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [1170, -2340, 1755]`, `chord_potential = 1755`, `holonomy_gamma2 = 2340`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(FQ-CONTEXTUALITY-CECH-F2): 4*idx(117) + 3*stage_rank(7) + route_degree(3) == 492` ($\text{value} = 492$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(FQ-CONTEXTUALITY-CECH-F2): R_raw(269) - G_cob(131) - S_decoy(7) == 131 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 131$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `1` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DualWitness.lean::mermin_peres_parity_obstruction`
- **Sovereign Rust Witness Anchor**: `omega_engine/crates_rs/omega_quantum_physics/src/parity_context_packet.rs::ParityAdmission`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4-flash` | `status = PASS` | `receipt_sha256 = 9e973ede4508f1fd972fd1c8487d914603442b24e597d5f73180734084d0f5d8`

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`GP-GAP-EXACT-DUALITY`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `GP-GAP-EXACT-DUALITY` (`FINITE_QM_STRUCTURE` / `PROVED_LEAN`)
- **Mined Operad Family (`M2`)**: `OP-FINITE_QM_STRUCTURE-GP-GAP-EXACT-DUALITY`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [1310, -2620, 1965]`, `chord_potential = 1965`, `holonomy_gamma2 = 2620`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(GP-GAP-EXACT-DUALITY): 4*idx(131) + 3*stage_rank(8) + route_degree(3) == 551` ($\text{value} = 551$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(GP-GAP-EXACT-DUALITY): R_raw(302) - G_cob(147) - S_decoy(8) == 147 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 147$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `0` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/LggrFiniteResults.lean::LggrFiniteResults.totalSatWeight3_le_two_mul_mass`
- **Sovereign Rust Witness Anchor**: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche13_ds_qm_final_16_second_witness_closure_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = c8a5318ce3d61fa11275d04af6f9ee53367c95da45b9a4f2d3a4fa696217cd93`

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`DS-QM120-MERMIN-PERES-F2-OBSTRUCTION`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `DS-QM120-MERMIN-PERES-F2-OBSTRUCTION` (`FINITE_QM_STRUCTURE` / `PROVED_LEAN`)
- **Mined Operad Family (`M2`)**: `OP-FINITE_QM_STRUCTURE-DS-QM120-MERMIN-PERES-F2-OBSTRUCTION`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [1710, -3420, 2565]`, `chord_potential = 2565`, `holonomy_gamma2 = 3420`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(DS-QM120-MERMIN-PERES-F2-OBSTRUCTION): 4*idx(171) + 3*stage_rank(8) + route_degree(5) == 713` ($\text{value} = 713$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(DS-QM120-MERMIN-PERES-F2-OBSTRUCTION): R_raw(382) - G_cob(187) - S_decoy(8) == 187 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 187$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `0` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm120_mermin_peres_f2_no_global_section`
- **Sovereign Rust Witness Anchor**: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche2_row_sparsity_bell_torsion_and_structure_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = 4b7b90ac4663017c9ec193829215699a99aaa73a9affd264f52acdd0cb4a4183`
