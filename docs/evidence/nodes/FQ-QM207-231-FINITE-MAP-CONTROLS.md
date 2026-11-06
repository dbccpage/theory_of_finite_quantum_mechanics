# FQ-QM207-231-FINITE-MAP-CONTROLS

Stage: [FINITE_QM_STRUCTURE](../stages/FINITE_QM_STRUCTURE.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Twenty-five finite-map controls QM-207..QM-231 (phase fiber, readout, context parity, frame function, clock tower, Symanzik/BPHZ, Dirac Ward-Takahashi, vacuum polarization, Kravchuk/hydrogen, Page-Wootters/Tsirelson/Wigner, electroweak, QCD beta0, Regge, Conf_2 spin-statistics, Dirac-Coulomb/helium, tree-level QED, PPN, GHZ/Mermin, Chern parity) each compute an exact finite invariant over Q or Q(zeta_N) and name the completion step and residual import in its own row. They are on main (PR #1132 merged, 5c6706eba; QM-226..231 added by bfa800fe2, 3c3042143, 0c3532f3b). Each row lists what is NOT derived (e.g. non-triviality of tau, second measurement context, Gleason positivity closure, Stone strong continuity, Feynman-parameter measure, UV subtraction).

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- distinct cited Lean declarations covered by a current replay receipt: 3
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

- `computational_no_runnable_test`: 0 in-repo Rust or Python symbol(s) cited, none a test. COMPUTATIONALLY_CHECKED with no in-repo runnable Rust or Python test cited.

## Imported structure

- each row s5.2 "Residual import" column (assumption)
- completion to R/C, Stone, period integrals (lift)

## Bottleneck

The 25 controls are exact native computations. Lean restates three of them (a helium variational identity, a Conf_2 character count, one Klein-Nishina ratio).

## Source status

Finite rational/integer control invariants for QM-207..231 mechanized across FiniteQM.lean, FiniteQFTAndGravity.lean, and DerivationDagQMClosure.lean

## Review

- PFP review: [evidence/results/FQ-QM207-231-FINITE-MAP-CONTROLS/reviews/20261019_boundaries_audit/review_result.json](../../../evidence/results/FQ-QM207-231-FINITE-MAP-CONTROLS/reviews/20261019_boundaries_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `status_lowered`; prior status `PROVED_LEAN`; qualifies for E4: no.
  - narrowest claim: The selected rational energy polynomial, exact minimizer and virial identity are kernel/native checked for all rational z where stated.
  - does not support: Derive the variational functional from the actual Hamiltonian/ansatz and audit the remaining finite-map rows and their residual imports. No batch closure of all25 controls, QED/QCD/gravity or physical spectrum is claimed.
  - next test: Derive the variational functional from the actual Hamiltonian/ansatz and audit the remaining finite-map rows and their residual imports. No batch closure of all25 controls, QED/QCD/gravity or physical spectrum is claimed.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/FiniteQFTAndGravity.lean`

- file: [lean4/FiniteQFTAndGravity.lean](../../../lean4/FiniteQFTAndGravity.lean)
- sha256 (`bytes`): `74e9ff5ac26167de3efcf46a7ce29be7c9fac106d6fe3b61a848f75ce28610d1`
- cited in: node.lean
- replay: `verified`
  - receipt [evidence/lean_receipts/lean_replay_campaign_finite_qcd.json](../../../evidence/lean_receipts/lean_replay_campaign_finite_qcd.json) (module `FiniteQFTAndGravity`): recorded sha256 `74e9ff5ac26167de3efcf46a7ce29be7c9fac106d6fe3b61a848f75ce28610d1` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
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
  - receipt [evidence/lean_receipts/lean_replay_campaign_finite_qcd.json](../../../evidence/lean_receipts/lean_replay_campaign_finite_qcd.json) (module `FiniteQM`): recorded sha256 `94cde0a3e760e5f17f309b950f2a02cfa40c895c8523a3986ab93123d7bd2759` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build FiniteQM`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `graph_conf2_exchange_betti_and_character_collapse` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms graph_conf2_exchange_betti_and_character_collapse` |
| `helium_kellner_variational_bound_and_virial_identity` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms helium_kellner_variational_bound_and_virial_identity` |

- counts toward the grade: yes

### Documents and data: `atlas/finite_quantum_mechanics/finite_quantum_mechanics.md`

- file: [atlas/finite_quantum_mechanics/finite_quantum_mechanics.md](../../../atlas/finite_quantum_mechanics/finite_quantum_mechanics.md)
- sha256 (`lf-normalised`): `85ca7b22b1c1e360a4c17ad8a9e0bddae03433592585b01d23a74cd09c82929e`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/15_finite_qed/tfq_0056_each_language_must_carry_clifford_admission_slash_square_exact_solution_rank_and_a.md`

- file: [dag/derivations/15_finite_qed/tfq_0056_each_language_must_carry_clifford_admission_slash_square_exact_solution_rank_and_a.md](../../../dag/derivations/15_finite_qed/tfq_0056_each_language_must_carry_clifford_admission_slash_square_exact_solution_rank_and_a.md)
- sha256 (`lf-normalised`): `4f62eccdbdd2a181e64f3dbbae8cafb93721d111a3a60ebe4a831992030730f3`
- generated view: listed, not counted
- cited in: record TFQ-0056 (shared)
- counts toward the grade: no

### Documents and data: `dag/derivations/15_finite_qed/tfq_0057_each_language_must_carry_rational_dirac_inversion_on_an_admitted_gamma_family.md`

- file: [dag/derivations/15_finite_qed/tfq_0057_each_language_must_carry_rational_dirac_inversion_on_an_admitted_gamma_family.md](../../../dag/derivations/15_finite_qed/tfq_0057_each_language_must_carry_rational_dirac_inversion_on_an_admitted_gamma_family.md)
- sha256 (`lf-normalised`): `aba4f6548c156df3043f7dea875d4b9a781bc947d47cb772f30e65f3a5ddf6e4`
- generated view: listed, not counted
- cited in: record TFQ-0057 (shared)
- counts toward the grade: no

### Documents and data: `dag/derivations/15_finite_qed/tfq_0058_each_language_must_carry_u_g_equals_the_scaled_principal_minor_of_the.md`

- file: [dag/derivations/15_finite_qed/tfq_0058_each_language_must_carry_u_g_equals_the_scaled_principal_minor_of_the.md](../../../dag/derivations/15_finite_qed/tfq_0058_each_language_must_carry_u_g_equals_the_scaled_principal_minor_of_the.md)
- sha256 (`lf-normalised`): `3037c0e231fe2b320e01212163004290750bce9aa9505048f9855a099cc53b82`
- generated view: listed, not counted
- cited in: record TFQ-0058
- counts toward the grade: no

### Documents and data: `dag/derivations/15_finite_qed/tfq_0060_each_language_must_carry_c1_1_2_exactly_and_higher_coefficients_only.md`

- file: [dag/derivations/15_finite_qed/tfq_0060_each_language_must_carry_c1_1_2_exactly_and_higher_coefficients_only.md](../../../dag/derivations/15_finite_qed/tfq_0060_each_language_must_carry_c1_1_2_exactly_and_higher_coefficients_only.md)
- sha256 (`lf-normalised`): `c54a60b34852c1c4c61dfd35753c07344c2217bfb4c04ae88fe9885c83c23b18`
- generated view: listed, not counted
- cited in: record TFQ-0060
- counts toward the grade: no

### Documents and data: `dag/derivations/15_finite_qed/tfq_0061_each_language_must_carry_2_forest_f0_equals_the_schur_complement_on_the.md`

- file: [dag/derivations/15_finite_qed/tfq_0061_each_language_must_carry_2_forest_f0_equals_the_schur_complement_on_the.md](../../../dag/derivations/15_finite_qed/tfq_0061_each_language_must_carry_2_forest_f0_equals_the_schur_complement_on_the.md)
- sha256 (`lf-normalised`): `9d95f8753643972408fc82d0f17178501b434abbee6a1dd16cd79416af72d54d`
- generated view: listed, not counted
- cited in: record TFQ-0061 (shared)
- counts toward the grade: no

### Documents and data: `dag/derivations/15_finite_qed/tfq_0063_each_language_must_carry_at_every_rational_loop_momentum_q_contracted_into.md`

- file: [dag/derivations/15_finite_qed/tfq_0063_each_language_must_carry_at_every_rational_loop_momentum_q_contracted_into.md](../../../dag/derivations/15_finite_qed/tfq_0063_each_language_must_carry_at_every_rational_loop_momentum_q_contracted_into.md)
- sha256 (`lf-normalised`): `0aca8accfc13358c7ef2c65f94e256ec8c0da872eb12fab48ada472061af00f1`
- generated view: listed, not counted
- cited in: record TFQ-0063
- counts toward the grade: no

### Documents and data: `dag/derivations/15_finite_qed/tfq_0064_each_language_must_carry_exact_cancellation_of_the_declared_infrared_cutoff_between.md`

- file: [dag/derivations/15_finite_qed/tfq_0064_each_language_must_carry_exact_cancellation_of_the_declared_infrared_cutoff_between.md](../../../dag/derivations/15_finite_qed/tfq_0064_each_language_must_carry_exact_cancellation_of_the_declared_infrared_cutoff_between.md)
- sha256 (`lf-normalised`): `90a771e55684b9e4ab2fcbfb144d1e1f5ab6e8f3d666d28e74a0e039a1e0ed32`
- generated view: listed, not counted
- cited in: record TFQ-0064
- counts toward the grade: no

### Documents and data: `dag/derivations/15_finite_qed/tfq_0065_each_language_must_carry_transverse_projector_identities_the_bubble_trace_match_u_1.md`

- file: [dag/derivations/15_finite_qed/tfq_0065_each_language_must_carry_transverse_projector_identities_the_bubble_trace_match_u_1.md](../../../dag/derivations/15_finite_qed/tfq_0065_each_language_must_carry_transverse_projector_identities_the_bubble_trace_match_u_1.md)
- sha256 (`lf-normalised`): `2ce29256afce134bde183cc5ae5c3b77049c79dadba3e7faa1a69ef51cac9f42`
- generated view: listed, not counted
- cited in: record TFQ-0065
- counts toward the grade: no

### Documents and data: `dag/derivations/15_finite_qed/tfq_0066_each_language_must_carry_the_twelve_digit_prefixes_for_pi_r_9_m_2_4_the_running.md`

- file: [dag/derivations/15_finite_qed/tfq_0066_each_language_must_carry_the_twelve_digit_prefixes_for_pi_r_9_m_2_4_the_running.md](../../../dag/derivations/15_finite_qed/tfq_0066_each_language_must_carry_the_twelve_digit_prefixes_for_pi_r_9_m_2_4_the_running.md)
- sha256 (`lf-normalised`): `79e2df7e291721a82f237a7fddcb044b556fa8c5129af77ce92008ec29ae0c4f`
- generated view: listed, not counted
- cited in: record TFQ-0066
- counts toward the grade: no

### Documents and data: `dag/derivations/15_finite_qed/tfq_0067_each_language_must_carry_kravchuk_brackets_and_spacing_balmer_values_1_n_2_on.md`

- file: [dag/derivations/15_finite_qed/tfq_0067_each_language_must_carry_kravchuk_brackets_and_spacing_balmer_values_1_n_2_on.md](../../../dag/derivations/15_finite_qed/tfq_0067_each_language_must_carry_kravchuk_brackets_and_spacing_balmer_values_1_n_2_on.md)
- sha256 (`lf-normalised`): `da368c35a7e7a1948519f6431fb57eb0139364282d06dbb1ec5a238d9455e366`
- generated view: listed, not counted
- cited in: record TFQ-0067 (shared)
- counts toward the grade: no

### Documents and data: `dag/derivations/15_finite_qed/tfq_0068_each_language_must_carry_n_2_coefficients_5_128_5_128_and_1_128_splitting_1_32.md`

- file: [dag/derivations/15_finite_qed/tfq_0068_each_language_must_carry_n_2_coefficients_5_128_5_128_and_1_128_splitting_1_32.md](../../../dag/derivations/15_finite_qed/tfq_0068_each_language_must_carry_n_2_coefficients_5_128_5_128_and_1_128_splitting_1_32.md)
- sha256 (`lf-normalised`): `013ad28ee683ed1ec756a228c705f1b80c10fa357a5b2628f37d339a71bea8ee`
- generated view: listed, not counted
- cited in: record TFQ-0068
- counts toward the grade: no

### Documents and data: `dag/derivations/15_finite_qed/tfq_0069_each_language_must_carry_the_uehling_prefix_and_the_lamb_bands_only.md`

- file: [dag/derivations/15_finite_qed/tfq_0069_each_language_must_carry_the_uehling_prefix_and_the_lamb_bands_only.md](../../../dag/derivations/15_finite_qed/tfq_0069_each_language_must_carry_the_uehling_prefix_and_the_lamb_bands_only.md)
- sha256 (`lf-normalised`): `9756b780e7a3f39464c118564ef40bb3169e544a81cf139dd6bcf9d85e30819c`
- generated view: listed, not counted
- cited in: record TFQ-0069
- counts toward the grade: no

### Documents and data: `dag/derivations/15_finite_qed/tfq_0070_each_language_must_carry_kellner_value_729_256_hylleraas_sign_change_on_2_9035_2_9030.md`

- file: [dag/derivations/15_finite_qed/tfq_0070_each_language_must_carry_kellner_value_729_256_hylleraas_sign_change_on_2_9035_2_9030.md](../../../dag/derivations/15_finite_qed/tfq_0070_each_language_must_carry_kellner_value_729_256_hylleraas_sign_change_on_2_9035_2_9030.md)
- sha256 (`lf-normalised`): `314acb552fa69e17ed3c9ed1ee184c983acf952148a07b3178eecb8876bb4a10`
- generated view: listed, not counted
- cited in: record TFQ-0070
- counts toward the grade: no

### Documents and data: `dag/derivations/15_finite_qed/tfq_0074_each_language_must_carry_klein_nishina_forward_value_1_thomson_shape_1_u_2_2_s_u.md`

- file: [dag/derivations/15_finite_qed/tfq_0074_each_language_must_carry_klein_nishina_forward_value_1_thomson_shape_1_u_2_2_s_u.md](../../../dag/derivations/15_finite_qed/tfq_0074_each_language_must_carry_klein_nishina_forward_value_1_thomson_shape_1_u_2_2_s_u.md)
- sha256 (`lf-normalised`): `07e03c078545cc00550c74655ee38c3610e103f945d9ecc99d09f4fe3bdb1e3c`
- generated view: listed, not counted
- cited in: record TFQ-0074
- counts toward the grade: no

### Documents and data: `dag/derivations/16_finite_electroweak/tfq_0075_each_language_must_carry_for_a_rational_doublet_of_radius_r_u_phi.md`

- file: [dag/derivations/16_finite_electroweak/tfq_0075_each_language_must_carry_for_a_rational_doublet_of_radius_r_u_phi.md](../../../dag/derivations/16_finite_electroweak/tfq_0075_each_language_must_carry_for_a_rational_doublet_of_radius_r_u_phi.md)
- sha256 (`lf-normalised`): `4568c59a5379f4e497695118c3b0697ddde40804f7b57875255f82f7672377da`
- generated view: listed, not counted
- cited in: record TFQ-0075
- counts toward the grade: no

### Documents and data: `dag/derivations/16_finite_electroweak/tfq_0076_each_language_must_carry_det_of_the_neutral_mass_matrix_is_0.md`

- file: [dag/derivations/16_finite_electroweak/tfq_0076_each_language_must_carry_det_of_the_neutral_mass_matrix_is_0.md](../../../dag/derivations/16_finite_electroweak/tfq_0076_each_language_must_carry_det_of_the_neutral_mass_matrix_is_0.md)
- sha256 (`lf-normalised`): `f04b9dffc316169eff815f7f82ecef089a45fb75d43616dc2dbb531d080b4a4b`
- generated view: listed, not counted
- cited in: record TFQ-0076
- counts toward the grade: no

### Documents and data: `dag/derivations/16_finite_electroweak/tfq_0077_each_language_must_carry_q_t3_y_on_the_standard.md`

- file: [dag/derivations/16_finite_electroweak/tfq_0077_each_language_must_carry_q_t3_y_on_the_standard.md](../../../dag/derivations/16_finite_electroweak/tfq_0077_each_language_must_carry_q_t3_y_on_the_standard.md)
- sha256 (`lf-normalised`): `1c6060820ef0d2f64958d082b7deb6074595519c6b2d2bd24c430fe34ee1aa7c`
- generated view: listed, not counted
- cited in: record TFQ-0077
- counts toward the grade: no

### Documents and data: `dag/derivations/16_finite_electroweak/tfq_0078_each_language_must_carry_the_four_anomaly_polynomials_vanish_at_n_c.md`

- file: [dag/derivations/16_finite_electroweak/tfq_0078_each_language_must_carry_the_four_anomaly_polynomials_vanish_at_n_c.md](../../../dag/derivations/16_finite_electroweak/tfq_0078_each_language_must_carry_the_four_anomaly_polynomials_vanish_at_n_c.md)
- sha256 (`lf-normalised`): `036a078c46014fff8b19cd941d67384ea6c59109d962af5668975df7b95f5d4f`
- generated view: listed, not counted
- cited in: record TFQ-0078
- counts toward the grade: no

### Documents and data: `dag/derivations/16_finite_electroweak/tfq_0079_each_language_must_carry_weyl_gamma5_square_and_trace_chiral_projector_algebra.md`

- file: [dag/derivations/16_finite_electroweak/tfq_0079_each_language_must_carry_weyl_gamma5_square_and_trace_chiral_projector_algebra.md](../../../dag/derivations/16_finite_electroweak/tfq_0079_each_language_must_carry_weyl_gamma5_square_and_trace_chiral_projector_algebra.md)
- sha256 (`lf-normalised`): `fa96d1dd66f077d052d5ae1d06e6cc033d6e2cec5190253a1d2a8e4ac5ad9ed5`
- generated view: listed, not counted
- cited in: record TFQ-0079
- counts toward the grade: no

### Documents and data: `dag/derivations/16_finite_electroweak/tfq_0080_rust_and_python_must_carry_exact_two_sided_unitarity_d_b_triangle_closure_and.md`

- file: [dag/derivations/16_finite_electroweak/tfq_0080_rust_and_python_must_carry_exact_two_sided_unitarity_d_b_triangle_closure_and.md](../../../dag/derivations/16_finite_electroweak/tfq_0080_rust_and_python_must_carry_exact_two_sided_unitarity_d_b_triangle_closure_and.md)
- sha256 (`lf-normalised`): `f6ed54a21c4854ee8d794bc739de7c62f980b00dfa372c1a0272467e1ccac903`
- generated view: listed, not counted
- cited in: record TFQ-0080
- counts toward the grade: no

### Documents and data: `dag/derivations/16_finite_electroweak/tfq_0081_each_language_must_carry_s_n_c_n_c_3_the_values_1_and_1_3.md`

- file: [dag/derivations/16_finite_electroweak/tfq_0081_each_language_must_carry_s_n_c_n_c_3_the_values_1_and_1_3.md](../../../dag/derivations/16_finite_electroweak/tfq_0081_each_language_must_carry_s_n_c_n_c_3_the_values_1_and_1_3.md)
- sha256 (`lf-normalised`): `e157ec729a980200aa8413c9a027f029591e596e5bd3fa3fba390f168f6b331e`
- generated view: listed, not counted
- cited in: record TFQ-0081
- counts toward the grade: no

### Documents and data: `dag/derivations/16_finite_electroweak/tfq_0082_each_language_must_carry_the_octet_and_decuplet_relations_as_polynomial_identities.md`

- file: [dag/derivations/16_finite_electroweak/tfq_0082_each_language_must_carry_the_octet_and_decuplet_relations_as_polynomial_identities.md](../../../dag/derivations/16_finite_electroweak/tfq_0082_each_language_must_carry_the_octet_and_decuplet_relations_as_polynomial_identities.md)
- sha256 (`lf-normalised`): `30e0aea10e001da68a2db72aa0e61688069429864427e9fa35b92f420eca296f`
- generated view: listed, not counted
- cited in: record TFQ-0082
- counts toward the grade: no

### Documents and data: `dag/derivations/16_finite_electroweak/tfq_0083_each_language_must_carry_an_explicit_gap_record_the_finite_gauge_dirac.md`

- file: [dag/derivations/16_finite_electroweak/tfq_0083_each_language_must_carry_an_explicit_gap_record_the_finite_gauge_dirac.md](../../../dag/derivations/16_finite_electroweak/tfq_0083_each_language_must_carry_an_explicit_gap_record_the_finite_gauge_dirac.md)
- sha256 (`lf-normalised`): `4e9ef44d9d701df1b6f6465e61f9a5abae4a36a7768d5202888f7a266cd356b5`
- generated view: listed, not counted
- cited in: record TFQ-0083 (shared)
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:376085dc410bbb86117c8efb40f2280ed15cb5734a22d050f6e1718aef3be579::evaluate_qm207_holonomy_bridge`
- `external:sha256:376085dc410bbb86117c8efb40f2280ed15cb5734a22d050f6e1718aef3be579::evaluate_qm211_clock_tower`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche2_row_sparsity_bell_torsion_and_structure_witness`
- `external:sha256:73ff1307c7f46b2f7648dd055f2db749abcaa4b8ab76c43fa35099fb1cd20ed4::evaluate_qm219_foundational_derivation_closure`
- `external:sha256:7b92d189c034dc6bb19e748fa9689912254a5b0b9a50a1f25d2566b9a4d4744f::analyze_conf2_graph`
- `external:sha256:b2756728a2444a8202ad7ab9078b63b94e2b41bb2addc311e7a2b1bebd8d9f44::ln_big_interval`
- `external:sha256:c5ad48d5c22ea89b1e481b44062e0de0f36728afa54ea6439e12e592c239f77a::ppn_deflection_factor`
- `external:sha256:dee13d74d257e960c55d1b3da0a35f7276c33ede91adba5203a17a7bb91cb34f::verify_qm224_dirac_coulomb_and_lamb_shift`

## Absences recorded by the TFQ records

- TFQ-0056 lean4: not located
- TFQ-0056 python: not located
- TFQ-0056 rust: no local rust twin located for external:sha256:6d09fe3d269514b28dde4a6f6dec6760ac77e87653e9f18c490226f9f26bb231
- TFQ-0057 lean4: not located
- TFQ-0057 python: no local python twin located for atlas/finite_quantum_mechanics/python/finite_qm/use_cases/dirac_ward_takahashi_control.py
- TFQ-0057 rust: no local rust twin located for external:sha256:376085dc410bbb86117c8efb40f2280ed15cb5734a22d050f6e1718aef3be579
- TFQ-0058 lean4: not located
- TFQ-0058 python: no local python twin located for atlas/finite_quantum_mechanics/python/finite_qm/use_cases/dressed_qed_g2_control.py
- TFQ-0058 rust: no local rust twin located for external:sha256:376085dc410bbb86117c8efb40f2280ed15cb5734a22d050f6e1718aef3be579
- TFQ-0060 lean4: not located
- TFQ-0060 python: no local python twin located for atlas/finite_quantum_mechanics/python/finite_qm/use_cases/dressed_qed_g2_control.py
- TFQ-0060 rust: no local rust twin located for external:sha256:376085dc410bbb86117c8efb40f2280ed15cb5734a22d050f6e1718aef3be579
- TFQ-0061 lean4: not located
- TFQ-0061 python: no local python twin located for atlas/finite_quantum_mechanics/python/finite_qm/use_cases/symanzik_two_forest_bphz_control.py
- TFQ-0061 rust: no local rust twin located for external:sha256:376085dc410bbb86117c8efb40f2280ed15cb5734a22d050f6e1718aef3be579
- TFQ-0063 lean4: not located
- TFQ-0063 python: no local python twin located for atlas/finite_quantum_mechanics/python/finite_qm/use_cases/dirac_ward_takahashi_control.py
- TFQ-0063 rust: no local rust twin located for external:sha256:376085dc410bbb86117c8efb40f2280ed15cb5734a22d050f6e1718aef3be579
- TFQ-0064 lean4: not located
- TFQ-0064 python: no local python twin located for atlas/finite_quantum_mechanics/python/finite_qm/use_cases/dirac_ward_takahashi_control.py
- TFQ-0064 rust: no local rust twin located for external:sha256:376085dc410bbb86117c8efb40f2280ed15cb5734a22d050f6e1718aef3be579
- TFQ-0065 lean4: not located
- TFQ-0065 python: no local python twin located for atlas/finite_quantum_mechanics/python/finite_qm/use_cases/vacuum_polarization_lamb_shift_control.py
- TFQ-0065 rust: no local rust twin located for external:sha256:ac46ba7dd3e8763a1c8f6bf42bc9e263b13e63bcc8783cdaf598f6ec34d4c9e3
- TFQ-0066 lean4: not located
- TFQ-0066 python: no local python twin located for atlas/finite_quantum_mechanics/python/finite_qm/use_cases/vacuum_polarization_lamb_shift_control.py
- TFQ-0066 rust: no local rust twin located for external:sha256:ac46ba7dd3e8763a1c8f6bf42bc9e263b13e63bcc8783cdaf598f6ec34d4c9e3
- TFQ-0067 lean4: not located
- TFQ-0067 python: no local python twin located for atlas/finite_quantum_mechanics/python/finite_qm/use_cases/algebraic_bound_state_spectra_control.py
- TFQ-0067 rust: no local rust twin located for external:sha256:a10da92df13ef926419410d2e5c98c7366f31aa5dd28fa48718916ad8f904b62
- TFQ-0068 lean4: not located
- TFQ-0068 python: no local python twin located for atlas/finite_quantum_mechanics/python/finite_qm/use_cases/atomic_dirac_lamb_hartree_fock_control.py
- TFQ-0068 rust: no local rust twin located for external:sha256:dee13d74d257e960c55d1b3da0a35f7276c33ede91adba5203a17a7bb91cb34f
- TFQ-0069 lean4: not located
- TFQ-0069 python: no local python twin located for atlas/finite_quantum_mechanics/python/finite_qm/use_cases/atomic_dirac_lamb_hartree_fock_control.py
- TFQ-0069 rust: no local rust twin located for external:sha256:dee13d74d257e960c55d1b3da0a35f7276c33ede91adba5203a17a7bb91cb34f
- TFQ-0070 lean4: not located
- TFQ-0070 python: no local python twin located for atlas/finite_quantum_mechanics/python/finite_qm/use_cases/atomic_dirac_lamb_hartree_fock_control.py
- TFQ-0070 rust: no local rust twin located for external:sha256:dee13d74d257e960c55d1b3da0a35f7276c33ede91adba5203a17a7bb91cb34f
- TFQ-0074 lean4: not located
- TFQ-0074 python: no local python twin located for atlas/finite_quantum_mechanics/python/finite_qm/use_cases/qed_weak_hadronic_control.py
- TFQ-0074 rust: no local rust twin located for external:sha256:b2756728a2444a8202ad7ab9078b63b94e2b41bb2addc311e7a2b1bebd8d9f44
- TFQ-0075 lean4: not located
- TFQ-0075 python: no local python twin located for atlas/finite_quantum_mechanics/python/finite_qm/use_cases/electroweak_dfm_weinberg_control.py
- TFQ-0075 rust: no local rust twin located for external:sha256:12edc74432418787b0ed633d04e6c77602431a6969b5172b53a4ffaf55e38d9f
- TFQ-0076 lean4: not located
- TFQ-0076 python: no local python twin located for atlas/finite_quantum_mechanics/python/finite_qm/use_cases/electroweak_dfm_weinberg_control.py
- TFQ-0076 rust: no local rust twin located for external:sha256:12edc74432418787b0ed633d04e6c77602431a6969b5172b53a4ffaf55e38d9f
- TFQ-0077 lean4: not located
- TFQ-0077 python: no local python twin located for atlas/finite_quantum_mechanics/python/finite_qm/use_cases/electroweak_dfm_weinberg_control.py
- TFQ-0077 rust: no local rust twin located for external:sha256:12edc74432418787b0ed633d04e6c77602431a6969b5172b53a4ffaf55e38d9f
- TFQ-0078 lean4: not located
- TFQ-0078 python: no local python twin located for atlas/finite_quantum_mechanics/python/finite_qm/use_cases/electroweak_dfm_weinberg_control.py
- TFQ-0078 rust: no local rust twin located for external:sha256:12edc74432418787b0ed633d04e6c77602431a6969b5172b53a4ffaf55e38d9f
- TFQ-0079 lean4: not located
- TFQ-0079 python: no local python twin located for atlas/finite_quantum_mechanics/python/finite_qm/use_cases/qed_weak_hadronic_control.py
- TFQ-0079 rust: no local rust twin located for external:sha256:b2756728a2444a8202ad7ab9078b63b94e2b41bb2addc311e7a2b1bebd8d9f44
- TFQ-0080 lean4: not located
- TFQ-0080 python: no local python twin located for atlas/finite_quantum_mechanics/python/finite_qm/use_cases/qed_weak_hadronic_control.py
- TFQ-0080 rust: no local rust twin located for external:sha256:b2756728a2444a8202ad7ab9078b63b94e2b41bb2addc311e7a2b1bebd8d9f44
- TFQ-0081 lean4: not located
- TFQ-0081 python: no local python twin located for atlas/finite_quantum_mechanics/python/finite_qm/use_cases/qed_weak_hadronic_control.py
- TFQ-0081 rust: no local rust twin located for external:sha256:b2756728a2444a8202ad7ab9078b63b94e2b41bb2addc311e7a2b1bebd8d9f44
- TFQ-0082 lean4: not located
- TFQ-0082 python: no local python twin located for atlas/finite_quantum_mechanics/python/finite_qm/use_cases/qed_weak_hadronic_control.py
- TFQ-0082 rust: no local rust twin located for external:sha256:b2756728a2444a8202ad7ab9078b63b94e2b41bb2addc311e7a2b1bebd8d9f44
- TFQ-0083 lean4: not located
- TFQ-0083 python: not located
- TFQ-0083 rust: no local rust twin located for external:sha256:2d9da71f2a615ba2de86c6896030b306594bc1169d72e912cd6e525b06887b66

## Routes

Incoming (1):

- `FQ-R-QM207-231` `COMPUTED`: [FQ-DECLARED-QUANTUM-INTERFACE](FQ-DECLARED-QUANTUM-INTERFACE.md) (IMPORTED_ASSUMPTION), [FQ-CARRIER-CONTRACT-V2](FQ-CARRIER-CONTRACT-V2.md) (DEFINITION)

Outgoing (0):

