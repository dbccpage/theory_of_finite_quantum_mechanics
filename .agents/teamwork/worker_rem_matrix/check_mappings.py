import os
import re
import json

def verify_all():
    # Load claims
    with open(".agents/teamwork/worker_m4_matrix/all_claims.json", "r", encoding="utf-8") as f:
        all_claims = json.load(f)

    # 1. Map for MUB
    mub_py_map = {
        'MUB6-C01': ('code/python/src/mub/mub_verify/target_g1_orbit_incompatibilities.py', 'code/python/tests/mub/test_route_c_fourier_landing.py'),
        'MUB6-C02': ('code/python/src/mub/mub_verify/target_g1_orbit_incompatibilities.py', 'code/python/tests/mub/test_route_c_fourier_landing.py'),
        'MUB6-C03': ('code/python/src/mub/mub_verify/target_g1_orbit_incompatibilities.py', 'code/python/tests/mub/test_route_c_fourier_landing.py'),
        'MUB6-C04': ('code/python/src/mub/mub_verify/target_g1_orbit_incompatibilities.py', 'code/python/tests/mub/test_route_c_fourier_landing.py'),
        'MUB6-C05': ('code/python/src/mub/mub_verify/target_g1_orbit_incompatibilities.py', 'code/python/tests/mub/test_route_c_fourier_landing.py'),
        'MUB6-C06': ('code/python/src/mub/conj2_symbolic_verification/conj2_tensor_product_proof.py', 'code/python/tests/mub/test_conj2_all_slice_configurations.py'),
        'MUB6-C07': ('code/python/src/mub/conj2_symbolic_verification/conj2_szollosi_2circulant_proof.py', 'code/python/tests/mub/test_conj2_all_slice_configurations.py'),
        'MUB6-C08': ('code/python/src/mub/mub_verify/cyclotomic.py', 'code/python/tests/mub/test_option_b_premises.py'),
        'MUB6-C09': ('code/python/src/mub/mub_verify/cyclotomic.py', 'code/python/tests/mub/test_option_b_premises.py'),
        'MUB6-C10': ('code/python/src/mub/mub_verify/target_a4_gram_certifier.py', 'code/python/tests/mub/test_remediation_b1_b11.py'),
        'MUB6-C11': ('code/python/src/mub/mub_verify/target_a4_gram_certifier.py', 'code/python/tests/mub/test_remediation_b1_b11.py'),
        'MUB6-C12': ('code/python/src/mub/mub_verify/target_a4_gram_certifier.py', 'code/python/tests/mub/test_remediation_b1_b11.py'),
        'MUB6-C13': ('code/python/src/mub/mub_verify/interval.py', 'code/python/tests/mub/test_remediation_b1_b11.py'),
        'MUB6-C14': ('code/python/src/mub/mub_verify/cyclotomic.py', 'code/python/tests/mub/test_remediation_b1_b11.py'),
        'MUB6-C15': ('code/python/src/mub/mub_verify/cyclotomic.py', 'code/python/tests/mub/test_remediation_b1_b11.py'),
        'MUB6-C16': ('code/python/src/mub/mub_verify/cyclotomic.py', 'code/python/tests/mub/test_remediation_b1_b11.py'),
        'MUB6-C17': ('code/python/src/mub/mub_verify/interval.py', 'code/python/tests/mub/test_remediation_b1_b11.py'),
        'MUB6-C18': ('code/python/src/mub/mub_verify/interval.py', 'code/python/tests/mub/test_remediation_b1_b11.py'),
        'MUB6-C19': ('code/python/src/mub/mub_verify/deltoid_cusp_input.py', 'code/python/tests/mub/test_remediation_b1_b11.py'),
        'MUB6-C20': ('code/python/src/mub/mub_verify/target_a4_gram_certifier.py', 'code/python/tests/mub/test_gauged_reflection_wire.py'),
        'MUB6-C21': ('code/python/src/mub/mub_verify/cover.py', 'code/python/tests/mub/test_gauged_reflection_wire.py'),
        'MUB6-C22': ('code/python/src/mub/conj2_symbolic_verification/conj2_szollosi_2circulant_proof.py', 'code/python/tests/mub/test_remediation_b1_b11.py'),
        'MUB6-C23': ('code/python/src/mub/conj2_symbolic_verification/conj2_szollosi_2circulant_proof.py', 'code/python/tests/mub/test_remediation_b1_b11.py'),
        'MUB6-C24': ('code/python/src/mub/conj2_symbolic_verification/conj2_szollosi_2circulant_proof.py', 'code/python/tests/mub/test_remediation_b1_b11.py'),
        'MUB6-C25': ('code/python/src/mub/mub_verify/interval.py', 'code/python/tests/mub/test_rectangular_reflection_wire.py'),
        'MUB6-C26': ('code/python/src/mub/mub_verify/target_a4_gram_certifier.py', 'code/python/tests/mub/test_gauged_reflection_wire.py'),
        'MUB6-C27': ('code/python/src/mub/mub_verify/target_a4_gram_certifier.py', 'code/python/tests/mub/test_rectangular_reflection_wire.py'),
        'MUB6-C28': ('code/python/src/mub/mub_verify/cover.py', 'code/python/tests/mub/test_gauged_reflection_wire.py'),
        'MUB6-C29': ('code/python/src/mub/mub_verify/target_q_degree8_and_gns.py', 'code/python/tests/mub/test_remediation_m1_m4.py'),
        'MUB6-C30': ('code/python/src/mub/mub_verify/target_q_degree8_and_gns.py', 'code/python/tests/mub/test_remediation_m1_m4.py'),
        'MUB6-C31': ('code/python/src/mub/mub_verify/target_q_degree8_and_gns.py', 'code/python/tests/mub/test_remediation_m1_m4.py'),
        'MUB6-C32': ('code/python/src/mub/mub_verify/target_q_degree8_and_gns.py', 'code/python/tests/mub/test_remediation_m1_m4.py'),
        'MUB6-C33': ('code/python/src/mub/mub_verify/target_q_degree8_and_gns.py', 'code/python/tests/mub/test_remediation_m1_m4.py'),
        'MUB6-C34': ('code/python/src/mub/mub_verify/packet_firewall.py', 'code/python/tests/mub/test_remediation_m1_m4.py'),
        'MUB6-C35': ('code/python/src/mub/mub_verify/target_q_degree8_and_gns.py', 'code/python/tests/mub/test_remediation_m1_m4.py'),
        'MUB6-C36': ('code/python/src/mub/mub_verify/target_q_degree8_and_gns.py', 'code/python/tests/mub/test_remediation_m1_m4.py'),
        'MUB6-C37': ('code/python/src/mub/mub_verify/target_q_degree8_and_gns.py', 'code/python/tests/mub/test_remediation_m1_m4.py'),
        'MUB6-C38': ('code/python/src/mub/mub_verify/mub_triples.py', 'code/python/tests/mub/test_36_check_publication_audit.py'),
        'MUB6-C39': ('code/python/src/mub/mub_verify/target_a4_gram_certifier.py', 'code/python/tests/mub/test_36_check_publication_audit.py'),
        'MUB6-C40': ('code/python/src/mub/mub_verify/mub_triples.py', 'code/python/tests/mub/test_publication_release.py'),
        'MUB6-C41': ('code/python/src/mub/mub_verify/deltoid_cusp_input.py', 'code/python/tests/mub/test_publication_release.py')
    }

    mub_rust_map = {
        'MUB6-C01': ('code/rust/src/mub/omega_native/mub6_fourier_landing_verifier.rs', 'test_fourier_landing_verification'),
        'MUB6-C02': ('code/rust/tests/omega_mub/test_target_a11_orbit_exhaustiveness.rs', 'test_exact_spectrum_fourier_f6'),
        'MUB6-C03': ('code/rust/tests/omega_mub/test_target_a11_orbit_exhaustiveness.rs', 'test_fourier_dita_family_all_points_classified_fourier'),
        'MUB6-C04': ('code/rust/tests/omega_mub/test_target_a11_orbit_exhaustiveness.rs', 'test_boundary_confluence_classification_consistency'),
        'MUB6-C05': ('code/rust/tests/omega_mub/test_target_3_normalized_triples.rs', 'test_transition_scaling_cross_multiplication'),
        'MUB6-C06': ('code/rust/src/mub/omega_native/mub6_matolcsi_weiner_conj2.rs', 'gamma1_has_20_permutations'),
        'MUB6-C07': ('code/rust/src/mub/omega_native/mub6_matolcsi_weiner_conj2.rs', 'g_h_on_fourier_f6_gamma1_vanishes'),
        'MUB6-C08': ('code/rust/src/mub/omega_native/mub6_chm_registry.rs', 'registry_mechanical_checks_pass'),
        'MUB6-C09': ('code/rust/src/mub/omega_native/mub6_chm_registry.rs', 'registry_separates_charted_from_open'),
        'MUB6-C10': ('code/rust/tests/omega_mub/test_matrix_residuals.rs', 'supplied_matrix_residual_and_perturbation'),
        'MUB6-C11': ('code/rust/tests/omega_mub/test_target_4_gap_propagation.rs', 'test_grid_partition_and_margin_positivity'),
        'MUB6-C12': ('code/rust/tests/omega_mub/test_target_a7_zerorel_variety.rs', 'test_exact_108_equation_count'),
        'MUB6-C13': ('code/rust/src/mub/omega_native/mub6_szollosi_executable.rs', 'gauged_export_retains_every_original_coefficient_and_probe'),
        'MUB6-C14': ('code/rust/src/mub/omega_native/mub6_balanced_table_replay.rs', 'regeneration_has_forty_two_constant_rows'),
        'MUB6-C15': ('code/rust/src/mub/omega_native/mub6_balanced_table_replay.rs', 'rational_literals_are_canonical_only'),
        'MUB6-C16': ('code/rust/src/mub/omega_native/mub6_quadratic_lift.rs', 'full_table_contracts_only_transition_coordinates_and_remains_unresolved'),
        'MUB6-C17': ('code/rust/src/mub/omega_native/mub6_szollosi_executable.rs', 'gauged_shape_requires_its_exact_schema_and_equation_count'),
        'MUB6-C18': ('code/rust/src/mub/omega_native/mub6_szollosi_executable.rs', 'gauged_reference_rejects_missing_or_changed_balance_rows'),
        'MUB6-C19': ('code/rust/tests/omega_mub/test_szollosi_deltoid_cover.rs', 'test_szollosi_deltoid_smoke_cover'),
        'MUB6-C20': ('code/rust/src/mub/omega_native/mub6_szollosi_executable.rs', 'gauged_export_retains_every_original_coefficient_and_probe'),
        'MUB6-C21': ('code/rust/src/mub/omega_native/mub6_szollosi_t5_cover.rs', 'test_system_eval_on_p0'),
        'MUB6-C22': ('code/rust/src/mub/omega_native/szollosi_triad_solver.rs', 'discrete_szollosi_chm_points_exist_and_are_exact'),
        'MUB6-C23': ('code/rust/src/mub/omega_native/szollosi_triad_solver.rs', 'tao_s6_is_exact_complex_hadamard'),
        'MUB6-C24': ('code/rust/src/mub/omega_native/mub6_szollosi_executable.rs', 'gauged_shape_requires_its_exact_schema_and_equation_count'),
        'MUB6-C25': ('code/rust/src/mub/omega_native/mub6_rectangular_exclusion_solver.rs', 'test_interval_arithmetic'),
        'MUB6-C26': ('code/rust/src/mub/omega_native/mub6_column_gauge_verifier.rs', 'test_column_gauge_verification'),
        'MUB6-C27': ('code/rust/src/mub/omega_native/mub6_chunked_reflection_engine.rs', 'test_chunked_reflection_verification'),
        'MUB6-C28': ('code/rust/src/mub/omega_native/mub6_szollosi_t5_cover.rs', 'test_pair_gap_bound'),
        'MUB6-C29': ('code/rust/src/mub/omega_native/mub6_flat_moment_extractor.rs', 'test_flat_moment_extraction'),
        'MUB6-C30': ('code/rust/src/mub/omega_native/mub6_moment_flatness_verifier.rs', 'test_moment_flatness_verification'),
        'MUB6-C31': ('code/rust/tests/omega_mub/test_matrix_residuals.rs', 'zero_matrix_residual'),
        'MUB6-C32': ('code/rust/tests/omega_mub/test_degree2_sdp.rs', 'test_degree2_moment_matrix_dimensions_and_structure'),
        'MUB6-C33': ('code/rust/tests/omega_mub/test_moment_ledger.rs', 'test_trace_formulas_degree_2'),
        'MUB6-C34': ('code/rust/src/mub/omega_native/mub6_claim_gate.rs', 'a_huge_float_cannot_invent_an_exact_certificate'),
        'MUB6-C35': ('code/rust/src/mub/omega_native/mub6_moment_flatness_verifier.rs', 'test_moment_flatness_verification'),
        'MUB6-C36': ('code/rust/src/mub/omega_native/mub6_flat_extension_certifier.rs', 'test_exact_rational_rank_identity'),
        'MUB6-C37': ('code/rust/src/mub/omega_native/mub6_flat_extension_certifier.rs', 'test_flat_extension_evaluation'),
        'MUB6-C38': ('code/rust/tests/omega_mub/test_mub6_prompt05_campaign_checks.rs', 'table_is_the_regeneration_of_its_definitions'),
        'MUB6-C39': ('code/rust/tests/omega_mub/test_mub6_prompt05_campaign_checks.rs', 'jacobian_at_the_centre_is_nonzero_and_rank_deficient'),
        'MUB6-C40': ('code/rust/src/mub/omega_native/mub6_basis_extension_packet.rs', 'standard_basis_does_not_extend_the_canonical_triple'),
        'MUB6-C41': ('code/rust/src/mub/omega_native/mub6_deltoid_cusp_collar_solver.rs', 'test_deltoid_cusp_verification')
    }

    # 2. Map for FSP
    fsp_py_map = {
        'PO-023-C1': ('code/python/src/fsp/bqnf_sign_evaluator.py', 'code/python/tests/fsp/e2e/test_monograph_derivation_walk_e2e.py'),
        'PO-023-C2': ('code/python/src/fsp/bqnf_sign_evaluator.py', 'code/python/tests/fsp/e2e/test_monograph_derivation_walk_e2e.py'),
        'GIN-C1': ('code/python/src/fsp/fermion_gin_index.py', 'code/python/tests/fsp/test_fermion_gin_index.py'),
        'GIN-C2': ('code/python/src/fsp/fermionic_hamiltonian.py', 'code/python/tests/fsp/test_fermion_sign_engine.py'),
        'GIN-C3': ('code/python/src/fsp/hamiltonian_gin_bridge.py', 'code/python/tests/fsp/integration/test_hamiltonian_gin_bridge.py'),
        'GIN-C4': ('code/python/src/fsp/hamiltonian_gin_bridge.py', 'code/python/tests/fsp/integration/test_hamiltonian_gin_bridge.py'),
        'GIN-C5': ('code/python/src/fsp/fermion_gin_index.py', 'code/python/tests/fsp/integration/test_majorana_zero_modes.py'),
        'GIN-C6': ('code/python/src/fsp/bqnf_sign_evaluator.py', 'code/python/tests/fsp/test_fermion_sign_engine.py'),
        'GIN-C7': ('code/python/src/fsp/fermion_gin_index.py', 'code/python/tests/fsp/integration/test_majorana_zero_modes.py'),
        'GIN-C8': ('code/python/src/fsp/sign_sql/run_sign_sql.py', 'code/python/tests/fsp/integration/test_sign_sql.py'),
        'GIN-C9': ('code/python/src/fsp/su2_lattice_gauge.py', 'code/python/tests/fsp/integration/test_su2_lattice_gauge.py'),
        'GIN-C10': ('code/python/src/fsp/su3_baryon_triality.py', 'code/python/tests/fsp/integration/test_su3_baryon_triality.py'),
        'GIN-C11': ('code/python/src/fsp/su3_polyakov_loop.py', 'code/python/tests/fsp/integration/test_su3_polyakov_loop.py'),
        'GIN-C12': ('code/python/src/fsp/su_nc_adjoint_flux.py', 'code/python/tests/fsp/integration/test_su_nc_adjoint_flux.py'),
        'GIN-C13': ('code/python/src/fsp/regge_pachner_wdw.py', 'code/python/tests/fsp/integration/test_regge_pachner_wdw.py'),
        'GIN-C14': ('code/python/src/fsp/pfp_fsp_bridge.py', 'code/python/tests/fsp/e2e/test_monograph_derivation_walk_e2e.py'),
        'GIN-C15': ('code/python/src/fsp/chiral_anomaly_inflow.py', 'code/python/tests/fsp/integration/test_chiral_anomaly_inflow.py'),
        'GIN-C16': ('code/python/src/fsp/fqh_laughlin_braiding.py', 'code/python/tests/fsp/integration/test_fqh_laughlin_braiding.py'),
        'GIN-C17': ('code/python/src/fsp/fibonacci_anyon_braiding.py', 'code/python/tests/fsp/integration/test_fibonacci_anyon_braiding.py'),
        'GIN-C18': ('code/python/src/fsp/ising_majorana_braiding.py', 'code/python/tests/fsp/integration/test_ising_majorana_braiding.py'),
        'GIN-C19': ('code/python/src/fsp/bf_linked_flux_braiding.py', 'code/python/tests/fsp/integration/test_bf_linked_flux_braiding.py'),
        'GIN-C20': ('code/python/src/fsp/bf_nonabelian_3loop_braiding.py', 'code/python/tests/fsp/integration/test_bf_nonabelian_3loop_braiding.py'),
        'GIN-C21': ('code/python/src/fsp/higher_2group_gauge_bf.py', 'code/python/tests/fsp/integration/test_higher_2group_gauge_bf.py'),
        'GIN-C22': ('code/python/src/fsp/cobordism_5d_higher_anomaly.py', 'code/python/tests/fsp/integration/test_cobordism_5d_higher_anomaly.py'),
        'GIN-C23': ('code/python/src/fsp/instanton_dyon_gas_braiding.py', 'code/python/tests/fsp/integration/test_instanton_dyon_gas_braiding.py'),
        'GIN-C24': ('code/python/src/fsp/foliated_fracton_2gauge_defects.py', 'code/python/tests/fsp/integration/test_foliated_fracton_2gauge_defects.py'),
        'NF-001': ('code/python/src/fsp/fermion_sign_nf_evaluator.py', 'code/python/tests/fsp/test_normal_form_laws.py'),
        'NF-002': ('code/python/src/fsp/fermion_sign_nf_evaluator.py', 'code/python/tests/fsp/test_normal_form_laws.py'),
        'NF-003': ('code/python/src/fsp/fermion_sign_nf_evaluator.py', 'code/python/tests/fsp/test_normal_form_laws.py'),
        'MERON-001': ('code/python/src/fsp/sign_sql/exact_models.py', 'code/python/tests/fsp/sign_sql/test_exact_models.py'),
        'MERON-002': ('code/python/src/fsp/sign_sql/exact_models.py', 'code/python/tests/fsp/sign_sql/test_exact_models.py'),
        'HUBBARD-001': ('code/python/src/fsp/sign_sql/exact_models.py', 'code/python/tests/fsp/sign_sql/test_exact_models.py'),
        'HUBBARD-002': ('code/python/src/fsp/sign_sql/exact_models.py', 'code/python/tests/fsp/sign_sql/test_exact_models.py'),
        'ORIGIN-001': ('code/python/src/fsp/sign_sql/exact_models.py', 'code/python/tests/fsp/sign_sql/test_exact_models.py'),
        'HUBBARD-003': ('code/python/src/fsp/sign_sql/exact_models.py', 'code/python/tests/fsp/sign_sql/test_exact_models.py')
    }

    fsp_rust_map = {
        'PO-023-C1': ('code/rust/tests/test_fsp.rs', 'test_dual_face_witness_contract_and_refusals'),
        'PO-023-C2': ('code/rust/tests/test_fsp.rs', 'test_dual_face_witness_contract_and_refusals'),
        'GIN-C1': ('code/rust/tests/test_fsp.rs', 'test_gin_inverted_index_and_cancellation_audit'),
        'GIN-C2': ('code/rust/tests/test_fsp.rs', 'test_car_algebra_creation_annihilation_anticommutation'),
        'GIN-C3': ('code/rust/tests/test_fsp.rs', 'test_gin_inverted_index_and_cancellation_audit'),
        'GIN-C4': ('code/rust/tests/test_fsp.rs', 'test_discrete_fermionic_hamiltonian_and_euler_path_sum'),
        'GIN-C5': ('code/rust/tests/test_fsp.rs', 'test_kitaev_chain_majorana_zero_modes'),
        'GIN-C6': ('code/rust/tests/test_fsp.rs', 'test_bqnf_terminal_routing_5_fold_classification'),
        'GIN-C7': ('code/rust/tests/test_fsp.rs', 'test_kitaev_chain_majorana_zero_modes'),
        'GIN-C8': ('code/rust/tests/test_fsp.rs', 'test_root_barrel_integration_and_inventory'),
        'GIN-C9': ('code/rust/tests/test_fsp.rs', 'test_dual_face_witness_contract_and_refusals'),
        'GIN-C10': ('code/rust/src/fsp/bqnf.rs', 'cochain_nilpotence_check'),
        'GIN-C11': ('code/rust/tests/test_fsp.rs', 'test_dual_face_witness_contract_and_refusals'),
        'GIN-C12': ('code/rust/tests/test_fsp.rs', 'test_dual_face_witness_contract_and_refusals'),
        'GIN-C13': ('code/rust/tests/test_fsp.rs', 'test_dual_face_witness_contract_and_refusals'),
        'GIN-C14': ('code/rust/tests/test_fsp.rs', 'test_root_barrel_integration_and_inventory'),
        'GIN-C15': ('code/rust/src/fsp/fock.rs', 'car_anticommutation_relation_on_fock_states'),
        'GIN-C16': ('code/rust/tests/test_fsp.rs', 'test_dual_face_witness_contract_and_refusals'),
        'GIN-C17': ('code/rust/tests/test_fsp.rs', 'test_dual_face_witness_contract_and_refusals'),
        'GIN-C18': ('code/rust/src/fsp/gin.rs', 'kitaev_chain_majorana_zero_mode_isolation_test'),
        'GIN-C19': ('code/rust/tests/test_fsp.rs', 'test_dual_face_witness_contract_and_refusals'),
        'GIN-C20': ('code/rust/tests/test_fsp.rs', 'test_dual_face_witness_contract_and_refusals'),
        'GIN-C21': ('code/rust/tests/test_fsp.rs', 'test_dual_face_witness_contract_and_refusals'),
        'GIN-C22': ('code/rust/tests/test_fsp.rs', 'test_dual_face_witness_contract_and_refusals'),
        'GIN-C23': ('code/rust/tests/test_fsp.rs', 'test_dual_face_witness_contract_and_refusals'),
        'GIN-C24': ('code/rust/tests/test_fsp.rs', 'test_dual_face_witness_contract_and_refusals'),
        'NF-001': ('code/rust/src/fsp/normal_forms.rs', 'quotient_normal_form_projection'),
        'NF-002': ('code/rust/src/fsp/normal_forms.rs', 'sign_switching_triangle_obstruction'),
        'NF-003': ('code/rust/src/fsp/normal_forms.rs', 'rref_2x2_identity_and_singular'),
        'MERON-001': ('code/rust/src/fsp/witness.rs', 'exact_star_and_orbit_witness_parity'),
        'MERON-002': ('code/rust/src/fsp/hubbard.rs', 'exact_determinant_2x2_and_3x3'),
        'HUBBARD-001': ('code/rust/src/fsp/hubbard.rs', 'exact_determinant_2x2_and_3x3'),
        'HUBBARD-002': ('code/rust/src/fsp/hubbard.rs', 'attractive_hubbard_square_root_symmetry_on_square_plaquette'),
        'ORIGIN-001': ('code/rust/src/fsp/fock.rs', 'free_fermion_triangle_paths_and_cancellation'),
        'HUBBARD-003': ('code/rust/tests/test_fsp.rs', 'test_exact_rational_hubbard_determinants_and_attractive_symmetry')
    }

    # 3. Map for Majorana
    maj_py_map = {
        'MAJ-C1': ('code/python/src/majorana/dual_observer.py', 'code/python/src/majorana/tests/unit/test_gf2_trichotomy.py'),
        'MAJ-C2': ('code/python/src/majorana/classify.py', 'code/python/src/majorana/tests/unit/test_trichotomy.py'),
        'MAJ-C3': ('code/python/src/majorana/gf2_terminalizer.py', 'code/python/src/majorana/tests/unit/test_gf2_matrix.py'),
        'MAJ-C4': ('code/python/src/majorana/complexes.py', 'code/python/src/majorana/tests/unit/test_gf2_trichotomy.py'),
        'MAJ-C5': ('code/python/src/majorana/tetron.py', 'code/python/src/majorana/tests/unit/test_tetron_benchmark.py'),
        'MAJ-C6': ('code/python/src/majorana/sparse_kitaev.py', 'code/python/src/majorana/tests/unit/test_kitaev_chain_exact.py'),
        'MAJ-C7': ('code/python/src/majorana/braid_action.py', 'code/python/src/majorana/tests/unit/test_majorana_braid_exact.py'),
        'MAJ-C8': ('code/python/src/majorana/majorana_fock_algebra.py', 'code/python/src/majorana/tests/unit/test_gf2_trichotomy.py'),
        'MAJ-C9': ('code/python/src/majorana/hard_invariants.py', 'code/python/src/majorana/tests/unit/test_gf2_trichotomy.py'),
        'MAJ-C10': ('code/python/src/majorana/dual_observer.py', 'code/python/src/majorana/tests/unit/test_gf2_trichotomy.py'),
        'MAJ-C11': ('code/python/src/majorana/lggr.py', 'code/python/src/majorana/tests/unit/test_gf2_trichotomy.py'),
        'MAJ-C12': ('code/python/src/majorana/tetron.py', 'code/python/src/majorana/tests/unit/test_tetron_carrier.py'),
        'MAJ-C13': ('code/python/src/majorana/tetron.py', 'code/python/src/majorana/tests/unit/test_tetron_carrier.py'),
        'MAJ-C14': ('code/python/src/majorana/harmonic.py', 'code/python/src/majorana/tests/unit/test_harmonic.py'),
        'MAJ-C15': ('code/python/src/majorana/repair_limit.py', 'code/python/src/majorana/tests/unit/test_fault_tolerance_repair_capacity.py'),
        'MAJ-C16': ('code/python/src/majorana/classify.py', 'code/python/src/majorana/tests/unit/test_trichotomy_well_formedness.py'),
        'MAJ-C17': ('code/python/src/majorana/repair_capacity.py', 'code/python/src/majorana/tests/unit/test_fault_tolerance_repair_capacity.py'),
        'MAJ-C18': ('code/python/src/majorana/packet_wall.py', 'code/python/src/majorana/tests/unit/test_open_system_transfer_bounds.py'),
        'MAJ-C19': ('code/python/src/majorana/noise_mc.py', 'code/python/src/majorana/tests/unit/test_majorana_noise_sweep.py'),
        'MAJ-C20': ('code/python/src/majorana/pauli_noise.py', 'code/python/src/majorana/tests/unit/test_majorana_multiqubit_noise.py')
    }

    maj_rust_map = {
        'MAJ-C1': ('code/rust/src/majorana/dual_observer.rs', 'edge_off_face_zero_disagrees_with_the_full_syndrome'),
        'MAJ-C2': ('code/rust/src/majorana/classify.rs', 'torus_reaches_every_terminal'),
        'MAJ-C3': ('code/rust/src/majorana/gf2_terminalizer.rs', 'test_gf2_matrix_boundary_and_terminalization'),
        'MAJ-C4': ('code/rust/src/majorana/complexes.rs', 'all_complexes_have_valid_boundary'),
        'MAJ-C5': ('code/rust/src/majorana/tetron.rs', 'cell_counts_match_the_lattice'),
        'MAJ-C6': ('code/rust/src/majorana/sparse_kitaev.rs', 'sparse_coefficients_and_generator_match_independent_fock_operator'),
        'MAJ-C7': ('code/rust/src/majorana/braid_action.rs', 'yang_baxter_far_commutativity_inverse_and_parity'),
        'MAJ-C8': ('code/rust/src/majorana/majorana_fock_algebra.rs', 'test_canonical_anticommutation_relations'),
        'MAJ-C9': ('code/rust/src/majorana/hard_invariants.rs', 'inv1_all_stock_complexes_satisfy_d1_d0_zero'),
        'MAJ-C10': ('code/rust/src/majorana/dual_observer.rs', 'plaquette_face_vs_even_parity_disagreement'),
        'MAJ-C11': ('code/rust/src/majorana/lggr.rs', 'torus_logical_is_lggr'),
        'MAJ-C12': ('code/rust/src/majorana/tetron.rs', 'dim_h1_is_the_topologys_betti_number'),
        'MAJ-C13': ('code/rust/src/majorana/tetron.rs', 'degenerate_periodic_extents_are_refused'),
        'MAJ-C14': ('code/rust/src/majorana/harmonic.rs', 'code_distance_is_the_topological_one'),
        'MAJ-C15': ('code/rust/src/majorana/repair_limit.rs', 'repair_capacity_bound_formula'),
        'MAJ-C16': ('code/rust/src/majorana/classify.rs', 'six_by_six_torus_weight_one_is_open_within_a_tenth_of_a_second'),
        'MAJ-C17': ('code/rust/src/majorana/repair_capacity.rs', 'min_weight_ignores_evens_empty_and_the_first_odd_vector'),
        'MAJ-C18': ('code/rust/src/majorana/packet_wall.rs', 'complete_torus_logical_closed_residual_auth_none'),
        'MAJ-C19': ('code/rust/src/majorana/noise_mc.rs', 'open_fraction_rises_with_p'),
        'MAJ-C20': ('code/rust/src/majorana/pauli_noise.rs', 'repeated_oriented_couplings_accumulate_and_cancel')
    }

    # Verify python files
    print("Checking Python files...")
    all_py_maps = [mub_py_map, fsp_py_map, maj_py_map]
    py_errors = 0
    for m in all_py_maps:
        for cid, (p_src, p_test) in m.items():
            if not os.path.isfile(p_src):
                print(f"[FAIL PY SRC] {cid}: {p_src} does not exist!")
                py_errors += 1
            if not os.path.isfile(p_test):
                print(f"[FAIL PY TEST] {cid}: {p_test} does not exist!")
                py_errors += 1
    if py_errors == 0:
        print("  All Python source and test files EXIST (100% PASS).")

    # Verify rust test symbols
    print("Checking Rust test symbols in code/rust/...")
    rust_errors = 0
    all_rust_maps = [mub_rust_map, fsp_rust_map, maj_rust_map]
    for m in all_rust_maps:
        for cid, (r_file, r_test) in m.items():
            if not os.path.isfile(r_file):
                print(f"[FAIL RUST FILE] {cid}: {r_file} does not exist!")
                rust_errors += 1
                continue
            with open(r_file, "r", encoding="utf-8", errors="ignore") as fp:
                content = fp.read()
            if r_test not in content:
                print(f"[FAIL RUST TEST] {cid}: {r_test} not found in {r_file}!")
                rust_errors += 1
    if rust_errors == 0:
        print("  All Rust implementation files and test functions EXIST (100% PASS).")

    # Verify lean modules
    print("Checking Lean 4 modules in lean4/...")
    lean_errors = 0
    for cat in ['mub', 'fsp', 'majorana']:
        for c in all_claims[cat]['claims']:
            cid = c['id']
            ldata = c.get('lean4') or c.get('lean4_formalization') or c.get('conditional_lean_reference')
            if ldata and isinstance(ldata, dict):
                mod = ldata.get('module')
                if mod and mod != 'N/A':
                    lpath = os.path.join('lean4', mod + '.lean')
                    if not os.path.isfile(lpath):
                        print(f"[FAIL LEAN MOD] {cid}: {lpath} does not exist!")
                        lean_errors += 1
    if lean_errors == 0:
        print("  All Lean 4 modules in claim tables EXIST (100% PASS).")

if __name__ == "__main__":
    verify_all()
