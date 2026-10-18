# [TFQ-0265] Stochastic population shadow of a channel

> **Stage**: `FINITE_QM_STRUCTURE` | **Status**: `SOURCE_RECORD`  
> **UUID**: `85374b52-c3e3-5895-8040-22672ea15902`  
> **Parent Derivation**: [TFQ-0262](TFQ-0262_cptp_class_recorded_as_a_definition.md)

---

## 1. Abstract & Formal Statement

QM_082 obliges a one-direction relation between channels and stochastic kernels. The opened title line says the note is about population shadows of channels, not a derivation of quantum dynamics. DS-QM082-STOCHASTIC-KERNEL-CPTP-DIAGONAL states the finite content: a stochastic kernel preserves states and composes, and a CPTP map with Kraus operators induces a column-stochastic population shadow after a basis choice and a diagonal read. The induced kernel is basis-relative, and the diagonal shadow does not fix the full channel. Identity and dephasing can share a shadow while differing on a coherent state.

### Governing Obligation
Derive only the population shadow of a supplied CPTP map, and do not invert that shadow into the channel.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Kraus operators (assumption)`
- **Admitted**: `basis choice and diagonal read (lift)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Direction CPTP -> kernel only; see GAP route.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm081_082_090_093_stochastic_contraction_channel_shadow_firewall_and_cochain`](../../code/lean4/)
- [`lean4/quantum_mechanics/H018Channel.lean::diagonal_shadow_does_not_fix_channel`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/lean/DerivationDagQMClosure.lean`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_quantum_physics/src/exact_channel.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/quantum_channel.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_ds_qm_dynamics_structure_and_majorana_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche13_ds_qm_final_16_second_witness_closure_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche5_full_dag_177_node_coverage_witness`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0266](TFQ-0266_no_derivation_from_stochastic_kernels_to_complete_positivity.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`DS-QM082-STOCHASTIC-KERNEL-CPTP-DIAGONAL`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `DS-QM082-STOCHASTIC-KERNEL-CPTP-DIAGONAL` (`FINITE_QM_STRUCTURE` / `PROVED_LEAN`)
- **Mined Operad Family (`M2`)**: `OP-FINITE_QM_STRUCTURE-DS-QM082-STOCHASTIC-KERNEL-CPTP-DIAGONAL`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [1600, -3200, 2400]`, `chord_potential = 2400`, `holonomy_gamma2 = 3200`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(DS-QM082-STOCHASTIC-KERNEL-CPTP-DIAGONAL): 4*idx(160) + 3*stage_rank(8) + route_degree(5) == 669` ($\text{value} = 669$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(DS-QM082-STOCHASTIC-KERNEL-CPTP-DIAGONAL): R_raw(360) - G_cob(176) - S_decoy(8) == 176 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 176$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `2` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm081_082_090_093_stochastic_contraction_channel_shadow_firewall_and_cochain`
- **Sovereign Rust Witness Anchor**: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche5_full_dag_177_node_coverage_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = 48778e3e4e96cf41cf8086cb117df6c9bea3484ca59f2d8177e40ff129ea557a`

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
