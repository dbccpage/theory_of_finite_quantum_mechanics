# [TFQ-0262] CPTP class recorded as a definition

> **Stage**: `FINITE_QM_STRUCTURE` | **Status**: `SOURCE_RECORD`  
> **UUID**: `8a655514-e502-5d5d-ae90-f5be8fecc814`  
> **Parent Derivation**: [TFQ-0234](../10_finite_qm_core/TFQ-0234_supplied_hilbert_carrier_after_the_conditional_lift.md)

---

## 1. Abstract & Formal Statement

FQ-CPTP-CLASS-DEFINITION, seen in the derivation graph, says the channel class is defined by a positive-semidefinite Choi matrix and by Stinespring realizations with a declared environment metric. That is a definition, not a derivation of the class from primitive difference. Finite Quantum Mechanics section 11.3 then uses the full stated CPTP family as a hypothesis for a trace-norm conclusion, and it says the argument does not select that family from primitive difference. Section 2 separates a numerical demonstration, which carries an algorithm and a tolerance, from an exact certificate.

### Governing Obligation
Use CPTP as a declared class. Do not treat a numerical tolerance as an exact certificate, and do not derive the class from a stochastic kernel.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `positivity (Choi PSD) (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Class is declared; channel availability is an operational premise.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/H063CptpChannelsStinespring.lean::choi_dimension_is_four`](../../code/lean4/)
- [`lean4/quantum_mechanics/H063CptpChannelsStinespring.lean::depol_choi_1_3_psd`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/lean/DerivationDagQMClosure.lean`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_quantum_physics/src/cptp_channels_stinespring.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/cptp_channels_stinespring.rs::WeightedStinespring`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/exact_channel.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/exact_channel.rs::ExactChoiMatrix`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/quantum_channel.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0263](TFQ-0263_trace_norm_under_a_supplied_cptp_family.md)
- [TFQ-0265](TFQ-0265_stochastic_population_shadow_of_a_channel.md)
- [TFQ-0268](../13_finite_qm_information/TFQ-0268_von_neumann_entropy_interface_for_mixed_states.md)
- [TFQ-0269](../13_finite_qm_information/TFQ-0269_threshold_theorems_read_as_repair-capacity_certificates.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`FQ-CPTP-CLASS-DEFINITION`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `FQ-CPTP-CLASS-DEFINITION` (`FINITE_QM_STRUCTURE` / `DEFINITION`)
- **Mined Operad Family (`M2`)**: `OP-FINITE_QM_STRUCTURE-FQ-CPTP-CLASS-DEFINITION`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [1110, -2220, 1665]`, `chord_potential = 1665`, `holonomy_gamma2 = 2220`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(FQ-CPTP-CLASS-DEFINITION): 4*idx(111) + 3*stage_rank(8) + route_degree(3) == 471` ($\text{value} = 471$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(FQ-CPTP-CLASS-DEFINITION): R_raw(262) - G_cob(127) - S_decoy(8) == 127 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 127$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `1` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/H063CptpChannelsStinespring.lean::depol_choi_1_3_psd`
- **Sovereign Rust Witness Anchor**: `omega_engine/crates_rs/omega_quantum_physics/src/exact_channel.rs::ExactChoiMatrix`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = 3b0b2ee15c1d00783fd40bc1e04a947d6bc37067520c77576589d89a14b77a5e`

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`DS-QM081-STOCHASTIC-L1-CONTRACTION`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `DS-QM081-STOCHASTIC-L1-CONTRACTION` (`FINITE_QM_STRUCTURE` / `PROVED_LEAN`)
- **Mined Operad Family (`M2`)**: `OP-FINITE_QM_STRUCTURE-DS-QM081-STOCHASTIC-L1-CONTRACTION`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [1590, -3180, 2385]`, `chord_potential = 2385`, `holonomy_gamma2 = 3180`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(DS-QM081-STOCHASTIC-L1-CONTRACTION): 4*idx(159) + 3*stage_rank(8) + route_degree(3) == 663` ($\text{value} = 663$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(DS-QM081-STOCHASTIC-L1-CONTRACTION): R_raw(358) - G_cob(175) - S_decoy(8) == 175 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 175$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `0` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm081_082_090_093_stochastic_contraction_channel_shadow_firewall_and_cochain`
- **Sovereign Rust Witness Anchor**: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche13_ds_qm_final_16_second_witness_closure_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4-flash` | `status = PASS` | `receipt_sha256 = 4a4c2d855ed177edafdae84c7d3e4fa68e01c075d96be875d74e810677bbf926`

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`GP-IMPORT-CPTP-CLASS`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `GP-IMPORT-CPTP-CLASS` (`L1_TO_L2` / `IMPORTED_ASSUMPTION`)
- **Mined Operad Family (`M2`)**: `OP-GP-CPTP-STINESPRING-IMPORT`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [240, -480, 360]`, `chord_potential = 360`, `holonomy_gamma2 = 480`
- **Finite Shadow Exact Witness (`M4`)**: `stochastic_column_conservation: col0_sum(10) + col1_sum(10) == 20` ($\text{value} = 20$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `reversible_bool_x_bool_Reset_dilations_count == 4 (4 distinct bijections realize reset, none selects complex Kraus CPTP)` ($\text{value} = 4$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `2` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.gp_and_l1_imported_field_circle_dilation_and_time_interpolation_boundaries`
- **Sovereign Rust Witness Anchor**: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche11_admitted_primitives_definitions_and_imported_assumptions_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = 5abe05fc56b66b83533844675b9e2c3cdd23bf2314dec075f74173374ee8a207`
