# [TFQ-0234] Supplied Hilbert carrier after the conditional lift

> **Stage**: `FINITE_QM_CORE` | **Status**: `SOURCE_RECORD`  
> **UUID**: `5c74553c-d178-5130-9430-ebc2a3c0e96f`  
> **Parent Derivation**: [TFQ-0006](../08_l1_to_l2/tfq_0006_conditional_finite_hilbert_lift.md)

---

## 1. Abstract & Formal Statement

Once a Hilbert carrier is already in hand, finite quantum mechanics does not start again from primitive difference. Finite Quantum Mechanics section 1.1 calls the eight rungs an assumption audit: pairing, phase, tensor composition, reversible steps, instruments, and representation hypotheses stay extra structure. Section 5 leaves the continuum Hilbert lift open. Ledger row FQM-F3 separates the general trace identity from the narrower Lean model. The header opened in lean/FiniteQM.lean declares a narrow opening scope, a rational degree-4 readout identity and five 2x2 import-independence countermodels.

### Governing Obligation
Treat the Hilbert carrier, inner product, and Born pairing as supplied inputs for every later finite step.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `complex field C (assumption)`
- **Admitted**: `complex scalars with modulus: lift`
- **Admitted**: `continuum Hilbert space (assumption)`
- **Admitted**: `square root field: lift`
- **Admitted**: `unit phases: lift`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> No Lean theorem for |c|^2 normalization over C found; BornNormalization.lean treats discrete 2x2 density / POVM. Rust exact_amplitudes returns None unless every p_j is a rational square.

> [!WARNING]
> Z[i] non-field obstruction and discriminant-5 spectral exit from Q(i) are mechanized; continuum Hilbert completion remains an explicit import.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/BornNormalization.lean::born_normalization_redundancy`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.conditional_route_bridges_pg_l1_fq_ds_sixteen_route_closure`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm072_073_090_and_fq_import_boundary_certificates`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.fq_gap_stone_rational_rotation_infinite_order_and_zi_non_field_obstruction`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.qm020_thm4_hilbert_lift_redundancy`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/lean/FiniteQM.lean`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_quantum_physics/src/mass_phase_embedding.rs::born_weights`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/mass_phase_embedding.rs::exact_amplitudes`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_l1_to_l2_bridges_and_ladder_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche15_gap_nonderivation_countermodels_and_conditional_route_bridges_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche2_row_sparsity_bell_torsion_and_structure_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche8_tensor_stone_continuum_embedding_and_leftover_mnc_witness`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0235](../11_finite_qm_dynamics/tfq_0235_selective_measurement_update_as_idempotent_conditioning.md)
- [TFQ-0239](../11_finite_qm_dynamics/tfq_0239_finite_path_sum_on_a_unique_intermediate_cut.md)
- [TFQ-0251](../12_finite_qm_structure/tfq_0251_superposition_as_a_quotient_fiber.md)
- [TFQ-0256](../12_finite_qm_structure/tfq_0256_product_defect_on_a_bipartite_weight_table.md)
- [TFQ-0262](../12_finite_qm_structure/tfq_0262_cptp_class_recorded_as_a_definition.md)
- [TFQ-0272](../13_finite_qm_information/tfq_0272_interpretations_as_authority_shadows.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`FQ-PRIMDIFF-QUOTIENT-KERNEL`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `FQ-PRIMDIFF-QUOTIENT-KERNEL` (`FINITE_QM_CORE` / `PROVED_LEAN`)
- **Mined Operad Family (`M2`)**: `OP-FINITE_QM_CORE-FQ-PRIMDIFF-QUOTIENT-KERNEL`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [980, -1960, 1470]`, `chord_potential = 1470`, `holonomy_gamma2 = 1960`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(FQ-PRIMDIFF-QUOTIENT-KERNEL): 4*idx(98) + 3*stage_rank(7) + route_degree(8) == 421` ($\text{value} = 421$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(FQ-PRIMDIFF-QUOTIENT-KERNEL): R_raw(231) - G_cob(112) - S_decoy(7) == 112 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 112$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `2` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.l1_to_l2_and_cross_fragment_route_composition`
- **Sovereign Rust Witness Anchor**: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche14_cross_stage_route_composition_and_sorkin_hierarchy_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = d38bc3b82a459c3a2a7aa1e77f081143f6203fdabded64bb482121ee0329ca9b`

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`FQ-INTERFERENCE-NONDESCENT`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `FQ-INTERFERENCE-NONDESCENT` (`FINITE_QM_CORE` / `PROVED_LEAN`)
- **Mined Operad Family (`M2`)**: `OP-FINITE_QM_CORE-FQ-INTERFERENCE-NONDESCENT`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [1020, -2040, 1530]`, `chord_potential = 1530`, `holonomy_gamma2 = 2040`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(FQ-INTERFERENCE-NONDESCENT): 4*idx(102) + 3*stage_rank(7) + route_degree(2) == 431` ($\text{value} = 431$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(FQ-INTERFERENCE-NONDESCENT): R_raw(239) - G_cob(116) - S_decoy(7) == 116 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 116$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `1` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/H010InterferenceNonDescent.lean::mix_separates`
- **Sovereign Rust Witness Anchor**: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche12_pg_l1_fq_gp_second_witness_certificates_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = db089d1b2acae5e8dd8734e7bac78f2a7e7c3ace7fa97a0c434da783cc8f5c13`

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`FQ-SORKIN-READOUT-CLASS-QM208`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `FQ-SORKIN-READOUT-CLASS-QM208` (`FINITE_QM_CORE` / `PROVED_LEAN`)
- **Mined Operad Family (`M2`)**: `OP-FINITE_QM_CORE-FQ-SORKIN-READOUT-CLASS-QM208`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [1030, -2060, 1545]`, `chord_potential = 1545`, `holonomy_gamma2 = 2060`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(FQ-SORKIN-READOUT-CLASS-QM208): 4*idx(103) + 3*stage_rank(7) + route_degree(3) == 436` ($\text{value} = 436$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(FQ-SORKIN-READOUT-CLASS-QM208): R_raw(241) - G_cob(117) - S_decoy(7) == 117 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 117$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `2` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.fq_core_phase_sorkin_gleason_busch_tsirelson_dynamics_route_composition`
- **Sovereign Rust Witness Anchor**: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche14_cross_stage_route_composition_and_sorkin_hierarchy_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = 2d0bd5a00111979bcd4b4f93a6c5f03d97d1591b4d2a56683ee1d9d3e3eeaf0f`

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`FQ-GAP-CONTINUUM-HILBERT-LIFT`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `FQ-GAP-CONTINUUM-HILBERT-LIFT` (`FINITE_QM_CORE` / `CONDITIONAL`)
- **Mined Operad Family (`M2`)**: `OP-FQ-CONTINUUM-WINTNER-WIELANDT`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [40, -80, 60]`, `chord_potential = 60`, `holonomy_gamma2 = 80`
- **Finite Shadow Exact Witness (`M4`)**: `wintner_wielandt_trace_commutator Tr([A,B]) == 0 and norm_1_plus_i == 2` ($\text{value} = 2$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `discriminant_2x2_self_adjoint [[1,1],[1,0]] == 5 (not a square in Z[i], exiting Q(i))` ($\text{value} = 5$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `2` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.conditional_route_bridges_pg_l1_fq_ds_sixteen_route_closure`
- **Sovereign Rust Witness Anchor**: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche15_gap_nonderivation_countermodels_and_conditional_route_bridges_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = ff39939e9b28a8b84cf626b2096e55594ad238a0d45d7fc3845ab2f0e98401f9`
