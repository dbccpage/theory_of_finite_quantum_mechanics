# FQ-QM207-231-FINITE-MAP-CONTROLS

Stage: [FINITE_QM_STRUCTURE](../stages/FINITE_QM_STRUCTURE.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Reviewed scope: The selected rational energy polynomial, exact minimizer and virial identity are kernel/native checked for all rational z where stated.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 4
- cited Lean declarations covered by a current replay receipt: 4
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- each row s5.2 "Residual import" column (assumption)
- completion to R/C, Stone, period integrals (lift)

## Bottleneck

Unmet after the PFP review: Derive the variational functional from the actual Hamiltonian/ansatz and audit the remaining finite-map rows and their residual imports. No batch closure of all25 controls, QED/QCD/gravity or physical spectrum is claimed. The broader source statement is kept in pfp_review.prior_statement.

## Source status

Finite rational/integer control invariants for QM-207..231 mechanized across FiniteQM.lean, FiniteQFTAndGravity.lean, and DerivationDagQMClosure.lean

## Review

- PFP review: [dag/results/FQ-QM207-231-FINITE-MAP-CONTROLS/reviews/20261019_boundaries_audit/review_result.json](../../../dag/results/FQ-QM207-231-FINITE-MAP-CONTROLS/reviews/20261019_boundaries_audit/review_result.json); file present and sha256 matches the node's record: no; verdict `scoped_result_or_obstruction_reviewed`; scope effect `statement_narrowed`; prior status `PROVED_LEAN`; qualifies for E4: no.
  - narrowest claim: The selected rational energy polynomial, exact minimizer and virial identity are kernel/native checked for all rational z where stated.
  - does not support: Derive the variational functional from the actual Hamiltonian/ansatz and audit the remaining finite-map rows and their residual imports. No batch closure of all25 controls, QED/QCD/gravity or physical spectrum is claimed.
  - next test: Derive the variational functional from the actual Hamiltonian/ansatz and audit the remaining finite-map rows and their residual imports. No batch closure of all25 controls, QED/QCD/gravity or physical spectrum is claimed.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.fq_qm207_231_finite_map_controls_master_certificate` | yes | yes | yes | none | `#print axioms QuantumMechanics.DerivationDagQMClosure.fq_qm207_231_finite_map_controls_master_certificate` |
- counts toward the grade: yes

### Lean: `lean4/FiniteQFTAndGravity.lean`

- file: [lean4/FiniteQFTAndGravity.lean](../../../lean4/FiniteQFTAndGravity.lean)
- sha256 (`bytes`): `74e9ff5ac26167de3efcf46a7ce29be7c9fac106d6fe3b61a848f75ce28610d1`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qcd.json](../../../dag/research/lean_replay_campaign_finite_qcd.json) (module `FiniteQFTAndGravity`): recorded sha256 `74e9ff5ac26167de3efcf46a7ce29be7c9fac106d6fe3b61a848f75ce28610d1` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build FiniteQFTAndGravity`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `kn_forward` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms kn_forward` |
- counts toward the grade: yes

### Lean: `lean4/FiniteQM.lean`

- file: [lean4/FiniteQM.lean](../../../lean4/FiniteQM.lean)
- sha256 (`bytes`): `94cde0a3e760e5f17f309b950f2a02cfa40c895c8523a3986ab93123d7bd2759`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qcd.json](../../../dag/research/lean_replay_campaign_finite_qcd.json) (module `FiniteQM`): recorded sha256 `94cde0a3e760e5f17f309b950f2a02cfa40c895c8523a3986ab93123d7bd2759` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build FiniteQM`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `graph_conf2_exchange_betti_and_character_collapse` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms graph_conf2_exchange_betti_and_character_collapse` |
| `helium_kellner_variational_bound_and_virial_identity` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms helium_kellner_variational_bound_and_virial_identity` |
- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_quantum_physics/src/atomic_dirac_lamb_hartree_fock.rs`

- file: `omega_engine/crates_rs/omega_quantum_physics/src/atomic_dirac_lamb_hartree_fock.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_quantum_physics/src/pauli_spin_statistics_graph.rs`

- file: `omega_engine/crates_rs/omega_quantum_physics/src/pauli_spin_statistics_graph.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_quantum_physics/src/qed_weak_hadronic_finite_maps.rs`

- file: `omega_engine/crates_rs/omega_quantum_physics/src/qed_weak_hadronic_finite_maps.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_quantum_physics/src/quantum_import_finite_maps.rs`

- file: `omega_engine/crates_rs/omega_quantum_physics/src/quantum_import_finite_maps.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_quantum_physics/src/quantum_import_finite_maps/foundational_derivation_closure.rs`

- file: `omega_engine/crates_rs/omega_quantum_physics/src/quantum_import_finite_maps/foundational_derivation_closure.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_quantum_physics/src/regge_gravity_ghz_chern_finite_maps.rs`

- file: `omega_engine/crates_rs/omega_quantum_physics/src/regge_gravity_ghz_chern_finite_maps.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/15_finite_qed/tfq_0056_each_language_must_carry_clifford_admission_slash_square_exact_solution_rank_and_a.md`

- file: [dag/derivations/15_finite_qed/tfq_0056_each_language_must_carry_clifford_admission_slash_square_exact_solution_rank_and_a.md](../../../dag/derivations/15_finite_qed/tfq_0056_each_language_must_carry_clifford_admission_slash_square_exact_solution_rank_and_a.md)
- sha256 (`lf-normalised`): `39f4c3c06256d4dca93b1c0e9d48f2ed8731bbe0a3610b1c8fa9cb2e707ed87d`
- generated view: listed, not counted
- cited in: record TFQ-0056 (shared)
- counts toward the grade: no

### Documents and data: `dag/derivations/15_finite_qed/tfq_0057_each_language_must_carry_rational_dirac_inversion_on_an_admitted_gamma_family.md`

- file: [dag/derivations/15_finite_qed/tfq_0057_each_language_must_carry_rational_dirac_inversion_on_an_admitted_gamma_family.md](../../../dag/derivations/15_finite_qed/tfq_0057_each_language_must_carry_rational_dirac_inversion_on_an_admitted_gamma_family.md)
- sha256 (`lf-normalised`): `cc30729fc06fba14ad3a2eb0b87d1af117d3864925ef95ab2f9043aa112cabca`
- generated view: listed, not counted
- cited in: record TFQ-0057 (shared)
- counts toward the grade: no

### Documents and data: `dag/derivations/15_finite_qed/tfq_0058_each_language_must_carry_u_g_equals_the_scaled_principal_minor_of_the.md`

- file: [dag/derivations/15_finite_qed/tfq_0058_each_language_must_carry_u_g_equals_the_scaled_principal_minor_of_the.md](../../../dag/derivations/15_finite_qed/tfq_0058_each_language_must_carry_u_g_equals_the_scaled_principal_minor_of_the.md)
- sha256 (`lf-normalised`): `99f3f8decdbeb3916d83469ffb998f092b21098a0df5d2bb73eb12ca9c10ca32`
- generated view: listed, not counted
- cited in: record TFQ-0058
- counts toward the grade: no

### Documents and data: `dag/derivations/15_finite_qed/tfq_0060_each_language_must_carry_c1_1_2_exactly_and_higher_coefficients_only.md`

- file: [dag/derivations/15_finite_qed/tfq_0060_each_language_must_carry_c1_1_2_exactly_and_higher_coefficients_only.md](../../../dag/derivations/15_finite_qed/tfq_0060_each_language_must_carry_c1_1_2_exactly_and_higher_coefficients_only.md)
- sha256 (`lf-normalised`): `7f99b216c954d89a6f0beedeef78d7f937efe14913aefbe973298bf35d73a4bc`
- generated view: listed, not counted
- cited in: record TFQ-0060
- counts toward the grade: no

### Documents and data: `dag/derivations/15_finite_qed/tfq_0061_each_language_must_carry_2_forest_f0_equals_the_schur_complement_on_the.md`

- file: [dag/derivations/15_finite_qed/tfq_0061_each_language_must_carry_2_forest_f0_equals_the_schur_complement_on_the.md](../../../dag/derivations/15_finite_qed/tfq_0061_each_language_must_carry_2_forest_f0_equals_the_schur_complement_on_the.md)
- sha256 (`lf-normalised`): `2eb09d978326d2668cbbf65652a12715ee78c76116299d79686905bf5ca7599d`
- generated view: listed, not counted
- cited in: record TFQ-0061 (shared)
- counts toward the grade: no

### Documents and data: `dag/derivations/15_finite_qed/tfq_0063_each_language_must_carry_at_every_rational_loop_momentum_q_contracted_into.md`

- file: [dag/derivations/15_finite_qed/tfq_0063_each_language_must_carry_at_every_rational_loop_momentum_q_contracted_into.md](../../../dag/derivations/15_finite_qed/tfq_0063_each_language_must_carry_at_every_rational_loop_momentum_q_contracted_into.md)
- sha256 (`lf-normalised`): `65985d9846acab455eefb676798349f88d0f7d3ac7d2eb6f481f57e04a7832e6`
- generated view: listed, not counted
- cited in: record TFQ-0063
- counts toward the grade: no

### Documents and data: `dag/derivations/15_finite_qed/tfq_0064_each_language_must_carry_exact_cancellation_of_the_declared_infrared_cutoff_between.md`

- file: [dag/derivations/15_finite_qed/tfq_0064_each_language_must_carry_exact_cancellation_of_the_declared_infrared_cutoff_between.md](../../../dag/derivations/15_finite_qed/tfq_0064_each_language_must_carry_exact_cancellation_of_the_declared_infrared_cutoff_between.md)
- sha256 (`lf-normalised`): `7cd065e64562a01faa4727ac0c1240d3ff90f67b29b8a3d89d2f3bf4f351fbf8`
- generated view: listed, not counted
- cited in: record TFQ-0064
- counts toward the grade: no

### Documents and data: `dag/derivations/15_finite_qed/tfq_0065_each_language_must_carry_transverse_projector_identities_the_bubble_trace_match_u_1.md`

- file: [dag/derivations/15_finite_qed/tfq_0065_each_language_must_carry_transverse_projector_identities_the_bubble_trace_match_u_1.md](../../../dag/derivations/15_finite_qed/tfq_0065_each_language_must_carry_transverse_projector_identities_the_bubble_trace_match_u_1.md)
- sha256 (`lf-normalised`): `aab480ddda557d1e5dca34c46796d0ae1c85531f4605e256ea2b1cd896c50644`
- generated view: listed, not counted
- cited in: record TFQ-0065
- counts toward the grade: no

### Documents and data: `dag/derivations/15_finite_qed/tfq_0066_each_language_must_carry_the_twelve_digit_prefixes_for_pi_r_9_m_2_4_the_running.md`

- file: [dag/derivations/15_finite_qed/tfq_0066_each_language_must_carry_the_twelve_digit_prefixes_for_pi_r_9_m_2_4_the_running.md](../../../dag/derivations/15_finite_qed/tfq_0066_each_language_must_carry_the_twelve_digit_prefixes_for_pi_r_9_m_2_4_the_running.md)
- sha256 (`lf-normalised`): `28302fae5e2b0b0415c4bb887223b1b6c6305d1ef04f12ae63cc4ddbebed90b3`
- generated view: listed, not counted
- cited in: record TFQ-0066
- counts toward the grade: no

### Documents and data: `dag/derivations/15_finite_qed/tfq_0067_each_language_must_carry_kravchuk_brackets_and_spacing_balmer_values_1_n_2_on.md`

- file: [dag/derivations/15_finite_qed/tfq_0067_each_language_must_carry_kravchuk_brackets_and_spacing_balmer_values_1_n_2_on.md](../../../dag/derivations/15_finite_qed/tfq_0067_each_language_must_carry_kravchuk_brackets_and_spacing_balmer_values_1_n_2_on.md)
- sha256 (`lf-normalised`): `e173adbbe0f1421f43e86a2cc92be90e64e94f727f4fff508248b945ba840e1a`
- generated view: listed, not counted
- cited in: record TFQ-0067 (shared)
- counts toward the grade: no

### Documents and data: `dag/derivations/15_finite_qed/tfq_0068_each_language_must_carry_n_2_coefficients_5_128_5_128_and_1_128_splitting_1_32.md`

- file: [dag/derivations/15_finite_qed/tfq_0068_each_language_must_carry_n_2_coefficients_5_128_5_128_and_1_128_splitting_1_32.md](../../../dag/derivations/15_finite_qed/tfq_0068_each_language_must_carry_n_2_coefficients_5_128_5_128_and_1_128_splitting_1_32.md)
- sha256 (`lf-normalised`): `6f592602518bc000db3331437fd65d256911dff05e6dc2331aca83ee95992453`
- generated view: listed, not counted
- cited in: record TFQ-0068
- counts toward the grade: no

### Documents and data: `dag/derivations/15_finite_qed/tfq_0069_each_language_must_carry_the_uehling_prefix_and_the_lamb_bands_only.md`

- file: [dag/derivations/15_finite_qed/tfq_0069_each_language_must_carry_the_uehling_prefix_and_the_lamb_bands_only.md](../../../dag/derivations/15_finite_qed/tfq_0069_each_language_must_carry_the_uehling_prefix_and_the_lamb_bands_only.md)
- sha256 (`lf-normalised`): `4ef3a6a025112bde43da217282aadc8313145baede28c0c8520a2790690976b8`
- generated view: listed, not counted
- cited in: record TFQ-0069
- counts toward the grade: no

### Documents and data: `dag/derivations/15_finite_qed/tfq_0070_each_language_must_carry_kellner_value_729_256_hylleraas_sign_change_on_2_9035_2_9030.md`

- file: [dag/derivations/15_finite_qed/tfq_0070_each_language_must_carry_kellner_value_729_256_hylleraas_sign_change_on_2_9035_2_9030.md](../../../dag/derivations/15_finite_qed/tfq_0070_each_language_must_carry_kellner_value_729_256_hylleraas_sign_change_on_2_9035_2_9030.md)
- sha256 (`lf-normalised`): `1e805c1e519e254b836a7017e4fbf075b5e7856155392f6e3bfc49e9f5095a09`
- generated view: listed, not counted
- cited in: record TFQ-0070
- counts toward the grade: no

### Documents and data: `dag/derivations/15_finite_qed/tfq_0074_each_language_must_carry_klein_nishina_forward_value_1_thomson_shape_1_u_2_2_s_u.md`

- file: [dag/derivations/15_finite_qed/tfq_0074_each_language_must_carry_klein_nishina_forward_value_1_thomson_shape_1_u_2_2_s_u.md](../../../dag/derivations/15_finite_qed/tfq_0074_each_language_must_carry_klein_nishina_forward_value_1_thomson_shape_1_u_2_2_s_u.md)
- sha256 (`lf-normalised`): `4d75e26292a8f6d77dae2930a34db4193654e26b3c6817c26acda8a196195adf`
- generated view: listed, not counted
- cited in: record TFQ-0074
- counts toward the grade: no

### Documents and data: `dag/derivations/16_finite_electroweak/tfq_0075_each_language_must_carry_for_a_rational_doublet_of_radius_r_u_phi.md`

- file: [dag/derivations/16_finite_electroweak/tfq_0075_each_language_must_carry_for_a_rational_doublet_of_radius_r_u_phi.md](../../../dag/derivations/16_finite_electroweak/tfq_0075_each_language_must_carry_for_a_rational_doublet_of_radius_r_u_phi.md)
- sha256 (`lf-normalised`): `eaf6204cb088a8e32915c0d00e474cba59d287b5e82a37d4c13e84fee59a1435`
- generated view: listed, not counted
- cited in: record TFQ-0075
- counts toward the grade: no

### Documents and data: `dag/derivations/16_finite_electroweak/tfq_0076_each_language_must_carry_det_of_the_neutral_mass_matrix_is_0.md`

- file: [dag/derivations/16_finite_electroweak/tfq_0076_each_language_must_carry_det_of_the_neutral_mass_matrix_is_0.md](../../../dag/derivations/16_finite_electroweak/tfq_0076_each_language_must_carry_det_of_the_neutral_mass_matrix_is_0.md)
- sha256 (`lf-normalised`): `078a8744a852108f0ac40e3c50ae197a3585ff38a69e86cc088169681c11f316`
- generated view: listed, not counted
- cited in: record TFQ-0076
- counts toward the grade: no

### Documents and data: `dag/derivations/16_finite_electroweak/tfq_0077_each_language_must_carry_q_t3_y_on_the_standard.md`

- file: [dag/derivations/16_finite_electroweak/tfq_0077_each_language_must_carry_q_t3_y_on_the_standard.md](../../../dag/derivations/16_finite_electroweak/tfq_0077_each_language_must_carry_q_t3_y_on_the_standard.md)
- sha256 (`lf-normalised`): `dc3f230512bbf5dca93bc41d27b2a5e6f3674eb0e436bc69843f37ed1f34c441`
- generated view: listed, not counted
- cited in: record TFQ-0077
- counts toward the grade: no

### Documents and data: `dag/derivations/16_finite_electroweak/tfq_0078_each_language_must_carry_the_four_anomaly_polynomials_vanish_at_n_c.md`

- file: [dag/derivations/16_finite_electroweak/tfq_0078_each_language_must_carry_the_four_anomaly_polynomials_vanish_at_n_c.md](../../../dag/derivations/16_finite_electroweak/tfq_0078_each_language_must_carry_the_four_anomaly_polynomials_vanish_at_n_c.md)
- sha256 (`lf-normalised`): `f5d008e24918fbec341e0004a2fcbf7e12feecabd8172a6e4025fed5eaf87e86`
- generated view: listed, not counted
- cited in: record TFQ-0078
- counts toward the grade: no

### Documents and data: `dag/derivations/16_finite_electroweak/tfq_0079_each_language_must_carry_weyl_gamma5_square_and_trace_chiral_projector_algebra.md`

- file: [dag/derivations/16_finite_electroweak/tfq_0079_each_language_must_carry_weyl_gamma5_square_and_trace_chiral_projector_algebra.md](../../../dag/derivations/16_finite_electroweak/tfq_0079_each_language_must_carry_weyl_gamma5_square_and_trace_chiral_projector_algebra.md)
- sha256 (`lf-normalised`): `0c2324896df1fa8f11ac2283654f17bcabc1a590c53b46b6f7064a5e1675daa1`
- generated view: listed, not counted
- cited in: record TFQ-0079
- counts toward the grade: no

### Documents and data: `dag/derivations/16_finite_electroweak/tfq_0080_rust_and_python_must_carry_exact_two_sided_unitarity_d_b_triangle_closure_and.md`

- file: [dag/derivations/16_finite_electroweak/tfq_0080_rust_and_python_must_carry_exact_two_sided_unitarity_d_b_triangle_closure_and.md](../../../dag/derivations/16_finite_electroweak/tfq_0080_rust_and_python_must_carry_exact_two_sided_unitarity_d_b_triangle_closure_and.md)
- sha256 (`lf-normalised`): `0c32e13453c19ff18fde07f9392b5b91d4129be8f8008637cc21304216dbffe6`
- generated view: listed, not counted
- cited in: record TFQ-0080
- counts toward the grade: no

### Documents and data: `dag/derivations/16_finite_electroweak/tfq_0081_each_language_must_carry_s_n_c_n_c_3_the_values_1_and_1_3.md`

- file: [dag/derivations/16_finite_electroweak/tfq_0081_each_language_must_carry_s_n_c_n_c_3_the_values_1_and_1_3.md](../../../dag/derivations/16_finite_electroweak/tfq_0081_each_language_must_carry_s_n_c_n_c_3_the_values_1_and_1_3.md)
- sha256 (`lf-normalised`): `0f14886c35a696c0a5eb481066dada49604ae239af4bf46a3b93148fd04e7348`
- generated view: listed, not counted
- cited in: record TFQ-0081
- counts toward the grade: no

### Documents and data: `dag/derivations/16_finite_electroweak/tfq_0082_each_language_must_carry_the_octet_and_decuplet_relations_as_polynomial_identities.md`

- file: [dag/derivations/16_finite_electroweak/tfq_0082_each_language_must_carry_the_octet_and_decuplet_relations_as_polynomial_identities.md](../../../dag/derivations/16_finite_electroweak/tfq_0082_each_language_must_carry_the_octet_and_decuplet_relations_as_polynomial_identities.md)
- sha256 (`lf-normalised`): `2a3b27fe8ec5ba9e64487cef08df841621d29ab874d4d144d6a1e9ed355b42e8`
- generated view: listed, not counted
- cited in: record TFQ-0082
- counts toward the grade: no

### Documents and data: `dag/derivations/16_finite_electroweak/tfq_0083_each_language_must_carry_an_explicit_gap_record_the_finite_gauge_dirac.md`

- file: [dag/derivations/16_finite_electroweak/tfq_0083_each_language_must_carry_an_explicit_gap_record_the_finite_gauge_dirac.md](../../../dag/derivations/16_finite_electroweak/tfq_0083_each_language_must_carry_an_explicit_gap_record_the_finite_gauge_dirac.md)
- sha256 (`lf-normalised`): `55926d07640196e84281a1e438d0cb9792d3df0d4781e8db3f75aa94df39ff8b`
- generated view: listed, not counted
- cited in: record TFQ-0083 (shared)
- counts toward the grade: no

### Documents and data: `sources/atlas/F004_papers/006_finite_qm/finite_quantum_mechanics.md`

- file: [sources/atlas/F004_papers/006_finite_qm/finite_quantum_mechanics.md](../../../sources/atlas/F004_papers/006_finite_qm/finite_quantum_mechanics.md)
- sha256 (`lf-normalised`): `5e43f206b08726fd4b27888d6fed3f211aac8398d5f8bf3dce712c415d7d81cc`
- cited in: node.source
- counts toward the grade: yes

## Absences recorded by the TFQ records

- TFQ-0056 lean4: not located
- TFQ-0056 python: not located
- TFQ-0056 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/dirac_gamma_admission.rs
- TFQ-0057 lean4: not located
- TFQ-0057 python: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm/use_cases/dirac_ward_takahashi_control.py
- TFQ-0057 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/quantum_import_finite_maps.rs
- TFQ-0058 lean4: not located
- TFQ-0058 python: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm/use_cases/dressed_qed_g2_control.py
- TFQ-0058 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/quantum_import_finite_maps.rs
- TFQ-0060 lean4: not located
- TFQ-0060 python: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm/use_cases/dressed_qed_g2_control.py
- TFQ-0060 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/quantum_import_finite_maps.rs
- TFQ-0061 lean4: not located
- TFQ-0061 python: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm/use_cases/symanzik_two_forest_bphz_control.py
- TFQ-0061 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/quantum_import_finite_maps.rs
- TFQ-0063 lean4: not located
- TFQ-0063 python: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm/use_cases/dirac_ward_takahashi_control.py
- TFQ-0063 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/quantum_import_finite_maps.rs
- TFQ-0064 lean4: not located
- TFQ-0064 python: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm/use_cases/dirac_ward_takahashi_control.py
- TFQ-0064 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/quantum_import_finite_maps.rs
- TFQ-0065 lean4: not located
- TFQ-0065 python: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm/use_cases/vacuum_polarization_lamb_shift_control.py
- TFQ-0065 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/quantum_import_finite_maps/vacuum_polarization_lamb_shift.rs
- TFQ-0066 lean4: not located
- TFQ-0066 python: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm/use_cases/vacuum_polarization_lamb_shift_control.py
- TFQ-0066 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/quantum_import_finite_maps/vacuum_polarization_lamb_shift.rs
- TFQ-0067 lean4: not located
- TFQ-0067 python: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm/use_cases/algebraic_bound_state_spectra_control.py
- TFQ-0067 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/quantum_import_finite_maps/algebraic_bound_state_spectra.rs
- TFQ-0068 lean4: not located
- TFQ-0068 python: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm/use_cases/atomic_dirac_lamb_hartree_fock_control.py
- TFQ-0068 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/atomic_dirac_lamb_hartree_fock.rs
- TFQ-0069 lean4: not located
- TFQ-0069 python: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm/use_cases/atomic_dirac_lamb_hartree_fock_control.py
- TFQ-0069 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/atomic_dirac_lamb_hartree_fock.rs
- TFQ-0070 lean4: not located
- TFQ-0070 python: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm/use_cases/atomic_dirac_lamb_hartree_fock_control.py
- TFQ-0070 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/atomic_dirac_lamb_hartree_fock.rs
- TFQ-0074 lean4: not located
- TFQ-0074 python: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm/use_cases/qed_weak_hadronic_control.py
- TFQ-0074 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/qed_weak_hadronic_finite_maps.rs
- TFQ-0075 lean4: not located
- TFQ-0075 python: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm/use_cases/electroweak_dfm_weinberg_control.py
- TFQ-0075 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/quantum_import_finite_maps/electroweak_dfm_weinberg_control.rs
- TFQ-0076 lean4: not located
- TFQ-0076 python: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm/use_cases/electroweak_dfm_weinberg_control.py
- TFQ-0076 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/quantum_import_finite_maps/electroweak_dfm_weinberg_control.rs
- TFQ-0077 lean4: not located
- TFQ-0077 python: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm/use_cases/electroweak_dfm_weinberg_control.py
- TFQ-0077 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/quantum_import_finite_maps/electroweak_dfm_weinberg_control.rs
- TFQ-0078 lean4: not located
- TFQ-0078 python: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm/use_cases/electroweak_dfm_weinberg_control.py
- TFQ-0078 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/quantum_import_finite_maps/electroweak_dfm_weinberg_control.rs
- TFQ-0079 lean4: not located
- TFQ-0079 python: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm/use_cases/qed_weak_hadronic_control.py
- TFQ-0079 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/qed_weak_hadronic_finite_maps.rs
- TFQ-0080 lean4: not located
- TFQ-0080 python: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm/use_cases/qed_weak_hadronic_control.py
- TFQ-0080 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/qed_weak_hadronic_finite_maps.rs
- TFQ-0081 lean4: not located
- TFQ-0081 python: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm/use_cases/qed_weak_hadronic_control.py
- TFQ-0081 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/qed_weak_hadronic_finite_maps.rs
- TFQ-0082 lean4: not located
- TFQ-0082 python: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm/use_cases/qed_weak_hadronic_control.py
- TFQ-0082 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/qed_weak_hadronic_finite_maps.rs
- TFQ-0083 lean4: not located
- TFQ-0083 python: not located
- TFQ-0083 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/s_matrix.rs

## Routes

Incoming (1):

- `FQ-R-QM207-231` `DERIVED_LEAN`: [FQ-DECLARED-QUANTUM-INTERFACE](FQ-DECLARED-QUANTUM-INTERFACE.md) (IMPORTED_ASSUMPTION), [FQ-CARRIER-CONTRACT-V2](FQ-CARRIER-CONTRACT-V2.md) (DEFINITION)

Outgoing (0):

