# [TFQ-0008] Finite dynamics, instruments, and channels

> **Stage**: `FINITE_QM_DYNAMICS` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `9a3ade1d-15a2-5016-a445-2b42ba90c577`  
> **Parent Derivation**: [TFQ-0007](../10_finite_qm_core/tfq_0007_finite_quantum_mechanics_core_on_an_admitted_carrier.md)

---

## 1. Abstract & Formal Statement

Narrowed finite case, status unchanged. On the directed path with integer edge weights a on 0 to 1 and b on 1 to 2, the length-1 path sum from 0 to 2 is 0 and the length-2 path sum is a*b. The unnormalized sector mask (w0, w1) maps to (0, w1): it is supported on the second coordinate, keeps that coordinate, is idempotent, and sends (w0, 0) to (0, 0). For every integer t, the Cayley column squared length (1 - t*t)^2 + (2*t)^2 equals (1 + t*t)^2, while the Euler column squared length 1 + t*t equals 1 if and only if t = 0. At t = 1 the Cayley value is 4. At t = 2 the Euler squared length is 5 and the inflation (1 + 2*2) - 1 is 4, and the Cayley value is 25. The integer matrix with rows (2, 0) and (0, 3) has entrywise distance 1 from the matrix with rows (2, 0) and (0, 2); the latter has both row sums 2, and the former has row sums 2 and 3, so distance 1 does not authorize an exact scaled stochastic kernel. A general instrument, a general finite path sum, a unitary group, the passage from stochastic kernels to completely positive maps, and every continuum generator stay unproved. The Lean file is `lean4/PathSumCayleyEulerStep.lean`. The receipts below this section are not this finite case.

### Governing Obligation
The finite path, sector mask, Cayley-versus-Euler integer shadow, and distance-1 stochastic countermodel are proved. Still open: a general instrument, a general path sum, an exact channel or an explicit CPTP import, Rust and Python witnesses of those general maps, and separation from a continuum generator beyond this integer shadow. A numerical tolerance does not discharge the exact channel. AuthorityEffect remains None.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Formalization
- **Primary Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.fq_core_phase_sorkin_gleason_busch_tsirelson_dynamics_route_composition` (zero-axiom, zero-sorry kernel verification in `lean/DerivationDagQMClosure.lean`).

### Sovereign Rust Certifiers
- **Primary Rust Witness**: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche14_cross_stage_route_composition_and_sorkin_hierarchy_witness` (`code/rust/src/dag_witnesses.rs`, exact `i64`/`BigRational` arithmetic).
- **Python PFP Gate Engine**: `omega_engine_pfp/tests/demo_004/finite_qm_derivation_pfp/gates/gate_engine.py::verify_dag_prompt_node_reply` (`G0`..`G6`).

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0009](../14_finite_gauge/tfq_0009_finite_gauge_cochain.md)
- [TFQ-0052](../14_finite_gauge/tfq_0052_each_language_must_carry_on_a_declared_m_2_q_i_packet_d0_of_an.md)
- [TFQ-0084](../19_finite_qg/tfq_0084_finite_quantum_gravity_shadow.md)
- [TFQ-0086](../19_finite_qg/tfq_0086_fq_gap_continuum_hilbert_lift_stays_unpaid_no_continuum_hilbert_space_is_admitted_at_the_root.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/floor.yaml`

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`FQ-DISCRETE-DYNAMICS-DICHOTOMY`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `FQ-DISCRETE-DYNAMICS-DICHOTOMY` (`FINITE_QM_DYNAMICS` / `PROVED_LEAN`)
- **Mined Operad Family (`M2`)**: `OP-FINITE_QM_DYNAMICS-FQ-DISCRETE-DYNAMICS-DICHOTOMY`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [1210, -2420, 1815]`, `chord_potential = 1815`, `holonomy_gamma2 = 2420`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(FQ-DISCRETE-DYNAMICS-DICHOTOMY): 4*idx(121) + 3*stage_rank(9) + route_degree(3) == 514` ($\text{value} = 514$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(FQ-DISCRETE-DYNAMICS-DICHOTOMY): R_raw(287) - G_cob(139) - S_decoy(9) == 139 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 139$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `2` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.fq_core_phase_sorkin_gleason_busch_tsirelson_dynamics_route_composition`
- **Sovereign Rust Witness Anchor**: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche14_cross_stage_route_composition_and_sorkin_hierarchy_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = 066ad4e28c5ee9350875bc6cce43e1cb158e91cce9ef47d0d68cd7dc5fa14048`

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`FQ-GAP-REAL-EMBEDDING-CHOICE`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `FQ-GAP-REAL-EMBEDDING-CHOICE` (`FINITE_QM_DYNAMICS` / `PROVED_LEAN`)
- **Mined Operad Family (`M2`)**: `OP-FINITE_QM_DYNAMICS-FQ-GAP-REAL-EMBEDDING-CHOICE`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [1240, -2480, 1860]`, `chord_potential = 1860`, `holonomy_gamma2 = 2480`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(FQ-GAP-REAL-EMBEDDING-CHOICE): 4*idx(124) + 3*stage_rank(9) + route_degree(2) == 525` ($\text{value} = 525$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(FQ-GAP-REAL-EMBEDDING-CHOICE): R_raw(293) - G_cob(142) - S_decoy(9) == 142 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 142$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `0` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/lean/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.fq_embedding_relativity_and_entropy_baker_dichotomy_closure`
- **Sovereign Rust Witness Anchor**: `omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/native/src/derivation_dag_witnesses.rs::verify_tranche21_pg_wdp_bridge_sector_weights_qm122_finish_embedding_and_baker_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = 5f2bdf4ba14eb041f6bea2a2a95b148ec9fbc346700e043286ae168bf946a9ca`

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`DS-CONTINUOUS-TIME-EXP-GENERATOR`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `DS-CONTINUOUS-TIME-EXP-GENERATOR` (`FINITE_QM_DYNAMICS` / `IMPORTED_ASSUMPTION`)
- **Mined Operad Family (`M2`)**: `OP-DS-EXP-GENERATOR-BOUNDARY`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [110, -220, 165]`, `chord_potential = 165`, `holonomy_gamma2 = 220`
- **Finite Shadow Exact Witness (`M4`)**: `cayley_norm_conservation_t1: (1 - 1^2)^2 + (2*1)^2 == (1 + 1^2)^2 == 4` ($\text{value} = 4$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `euler_step_norm_inflation_t2: (1 + 2^2) - 1 == 4 > 0 (first-order generator step inflates norm by 4)` ($\text{value} = 4$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `3` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_gap_measurement_projection_cptp_and_continuous_time_generator_countermodels`
- **Sovereign Rust Witness Anchor**: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche15_gap_nonderivation_countermodels_and_conditional_route_bridges_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = b93f8b82fe847096cc1fd6eb7dfd11ff508b46c64b140907593065bb9ffdf4c6`
