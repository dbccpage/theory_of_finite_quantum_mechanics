# [TFQ-0318] Float lift helper is not the exact embedding

> **Stage**: `FINITE_HILBERT` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `5817230b-6be0-51b1-9a12-b070c82b6545`  
> **Parent Derivation**: [TFQ-0317](tfq_0317_three_lean_files_stay_on_a_narrow_carrier.md)

---

## 1. Abstract & Formal Statement

The finite obligation is the mismatch between two lift helpers. The Python function l1_to_l2_amplitude_lift in the qm_020 core takes a floating square root and, when phases are omitted, returns a real nonnegative vector. mass_phase_embedding.rs refuses a missing phase, so it does not invent a phase convention, and it returns exact amplitudes only when every normalized weight is a rational square. Those are different contracts. A numeric check that squared moduli sum to one does not discharge the square-root gap, the complex-field gap, or Born uniqueness.

### Governing Obligation
Do not treat the floating amplitude helper as the exact finite Hilbert embedding.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `complex scalars with modulus: lift`
- **Admitted**: `real closed field or algebraic closure of weights: assumption`
- **Admitted**: `square root field: lift`
- **Admitted**: `unit phases: lift`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Choice of coefficient field is not derived from carriers.

> [!WARNING]
> No Lean theorem for |c|^2 normalization over C found; BornNormalization.lean treats discrete 2x2 density / POVM. Rust exact_amplitudes returns None unless every p_j is a rational square.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/BornNormalization.lean::born_normalization_redundancy`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.l1_and_ds_imported_assumption_separation_certificates`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.l1_gap_u1_inner_product_orthogonal_additivity_and_isometric_dynamics_countermodels`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.l1_minkowski_sqrt_decoherence_and_scoped_custody_witness`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.qm020_thm4_hilbert_lift_redundancy`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_quantum_physics/src/mass_phase_embedding.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/mass_phase_embedding.rs::born_weights`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/mass_phase_embedding.rs::exact_amplitudes`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/quantum_state.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_l1_to_l2_bridges_and_ladder_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche10_chsh_tsirelson_pr_box_tier3_uniqueness_edgewise_l1_and_import_boundaries_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche15_gap_nonderivation_countermodels_and_conditional_route_bridges_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche5_full_dag_177_node_coverage_witness`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/001_from_primitive_difference_to_quantum_mechanics/python/src/finite_quantum/density_matrix.py`](../../code/python/)
- [`omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/_code/qm_020/code/qm_020_born_normalization_and_conditional_hilbert_lift_core.py`](../../code/python/)
- [`omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/_code/qm_020/tests/test_qm020_born_lift.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001`, `F001.S000`, `F001.S000:001_from_primitive_difference_to_quantum_mechanics`, `F003`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/floor.yaml`
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/shelf.yaml`
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/001_from_primitive_difference_to_quantum_mechanics/book/README.md`
  - `omega_engine_atlas/coda_atlas/F003_omega_engine/floor.yaml`

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`FQ-TSIRELSON-SOS-Q-SQRT2`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `FQ-TSIRELSON-SOS-Q-SQRT2` (`FINITE_QM_CORE` / `PROVED_LEAN`)
- **Mined Operad Family (`M2`)**: `OP-FINITE_QM_CORE-FQ-TSIRELSON-SOS-Q-SQRT2`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [1160, -2320, 1740]`, `chord_potential = 1740`, `holonomy_gamma2 = 2320`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(FQ-TSIRELSON-SOS-Q-SQRT2): 4*idx(116) + 3*stage_rank(7) + route_degree(2) == 487` ($\text{value} = 487$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(FQ-TSIRELSON-SOS-Q-SQRT2): R_raw(267) - G_cob(130) - S_decoy(7) == 130 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 130$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `3` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.fq_core_phase_sorkin_gleason_busch_tsirelson_dynamics_route_composition`
- **Sovereign Rust Witness Anchor**: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche14_cross_stage_route_composition_and_sorkin_hierarchy_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = bb48d89472357ea4f8ca7a46fcebe5ed16dbb04d9a73b6e5fd0814be7b00d40b`

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`L1-IMP-SQRT-FIELD`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `L1-IMP-SQRT-FIELD` (`L1_TO_L2` / `IMPORTED_ASSUMPTION`)
- **Mined Operad Family (`M2`)**: `OP-L1-SQRT-FIELD-EXTENSION`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [320, -640, 480]`, `chord_potential = 480`, `holonomy_gamma2 = 640`
- **Finite Shadow Exact Witness (`M4`)**: `pythagorean_square_weights_lift: sqrt(9) + sqrt(16) = 3 + 4 == 7` ($\text{value} = 7$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `non_square_weight_2_gap: min_{z in Z} |z^2 - 2| == 1 (2 has no square root in Z or Q; exact_amplitudes returns None)` ($\text{value} = 1$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `1` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.l1_gap_u1_inner_product_orthogonal_additivity_and_isometric_dynamics_countermodels`
- **Sovereign Rust Witness Anchor**: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche15_gap_nonderivation_countermodels_and_conditional_route_bridges_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = e0dcb5a9572e390e346f0e9877fefc1c37654d7bd5b77969b44aeffda7da3298`
