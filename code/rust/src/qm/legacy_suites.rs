

use crate::qm::campaigns::branch_finegraining::*;
use crate::qm::campaigns::busch_effects::*;
use crate::qm::campaigns::cancellations::*;
use crate::qm::campaigns::channel_census::*;
use crate::qm::campaigns::composite_mub::*;
use crate::qm::campaigns::context_thresholds::*;
use crate::qm::campaigns::dynamics_dichotomy::*;
use crate::qm::campaigns::embedding_relativity::*;
use crate::qm::campaigns::foundational_targets::*;
use crate::qm::campaigns::growth_refinement::*;
use crate::qm::campaigns::quantum_walk::*;
use crate::qm::campaigns::terminal_price_list::*;
use crate::qm::campaigns::toric::*;
use omega_lie_theory::pauli_symplectic::*;
use omega_number_theory::cyclotomic_field::CyclotomicNumber;
use omega_number_theory::cyclotomic_ordered::standard_real_sign;
use omega_quantum_physics::branch_finegraining::search_smallest_irrational_conductor;
use omega_quantum_physics::commutator::*;
use omega_quantum_physics::grover::*;
use omega_quantum_physics::mub::*;
use omega_quantum_physics::phase_estimation::*;
use omega_quantum_physics::richardson::*;
use omega_quantum_physics::shor::*;
use omega_quantum_physics::tomography::*;
use omega_quantum_physics::wigner::*;
use serde_json::json;

pub fn run_legacy_target(target: &str) -> Result<serde_json::Value, String> {
    run_legacy_target_with_args(target, &[])
}

pub fn run_legacy_target_with_args(
    target: &str,
    args: &[String],
) -> Result<serde_json::Value, String> {
    match target {
        "--target-1" => {
            let r = verify_target1_primitive_difference();
            serde_json::to_value(&r).map_err(|e| e.to_string())
        }
        "--target-2" => {
            let r = verify_target2_diamond_complex();
            serde_json::to_value(&r).map_err(|e| e.to_string())
        }
        "--target-3" => {
            let r = verify_target3_sorkin_interference();
            serde_json::to_value(&r).map_err(|e| e.to_string())
        }
        "--target-4" => {
            let r = verify_target4_rational_cayley();
            serde_json::to_value(&r).map_err(|e| e.to_string())
        }
        "--target-5" => {
            let r = verify_target5_pentagon_identity();
            serde_json::to_value(&r).map_err(|e| e.to_string())
        }
        "--target-6" => {
            let r = verify_target6_cabello_polytope();
            serde_json::to_value(&r).map_err(|e| e.to_string())
        }
        "--target-7" => {
            let r = verify_target7_monotone_unitarity();
            serde_json::to_value(&r).map_err(|e| e.to_string())
        }
        "--target-8" => {
            let r = verify_target8_bell_chsh();
            serde_json::to_value(&r).map_err(|e| e.to_string())
        }
        "--target-9" => {
            let r = verify_target9_bitflip_code();
            serde_json::to_value(&r).map_err(|e| e.to_string())
        }
        "--target-10" => {
            let r = verify_target10_teleportation();
            serde_json::to_value(&r).map_err(|e| e.to_string())
        }
        "--target-11" => {
            let r = verify_target11_superdense_coding();
            serde_json::to_value(&r).map_err(|e| e.to_string())
        }
        "--target-12" => {
            let r = verify_target12_css_code();
            serde_json::to_value(&r).map_err(|e| e.to_string())
        }
        "--target-13" => {
            let wigner = DiscreteWignerSystemD5::new();
            let w_ground = wigner
                .evaluate_wigner(&state_ground_d5())
                .expect("declared rational Wigner fixture");
            let w_magic = wigner
                .evaluate_exact(&state_magic_d5())
                .map_err(|error| error.to_string())?;
            let stabilizer_non_neg = w_ground.iter().all(|row| {
                row.iter()
                    .all(|v| v >= &omega_number_theory::rational::r_zero())
            });
            let magic_has_negativity = w_magic
                .iter()
                .flatten()
                .map(|value| standard_real_sign(&CyclotomicNumber::from(value)))
                .collect::<Result<Vec<_>, _>>()
                .map_err(|error| error.to_string())?
                .iter()
                .any(|&sign| sign < 0);
            let receipt = json!({
                "target": 13,
                "dimension": 5,
                "phase_points": 25,
                "stabilizer_non_negative": stabilizer_non_neg,
                "magic_point_negativity_certified": magic_has_negativity,
                "authority_effect": "None",
                "status": if stabilizer_non_neg && magic_has_negativity {"VERIFIED_FINITE_CHECKS"} else {"FAIL"}
            });
            serde_json::to_value(&receipt).map_err(|e| e.to_string())
        }
        "--target-14" => {
            let shor = ShorNineQubitCode::new();
            serde_json::to_value(&shor).map_err(|e| e.to_string())
        }
        "--target-15" => {
            let pe = DiscretePhaseEstimation::run(3, 1);
            let all_verified = DiscretePhaseEstimation::verify_all_dyadic_phases(3);
            let receipt = json!({
                "target": 15,
                "m_qubits": pe.m_qubits,
                "register_dim": pe.register_dim,
                "dyadic_fraction": format!("{}/{}", pe.dyadic_numerator, pe.dyadic_denominator),
                "is_exact_projection": pe.is_exact_projection,
                "target_probability": format!("{}/{}", pe.target_probability.0, pe.target_probability.1),
                "all_dyadic_phases_verified": all_verified,
                "authority_effect": "None",
                "status": if all_verified && pe.is_exact_projection {"VERIFIED_FINITE_CHECKS"} else {"FAIL"}
            });
            serde_json::to_value(&receipt).map_err(|e| e.to_string())
        }
        "--target-16" => {
            let toric = ToricCode2x2::new();
            serde_json::to_value(&toric).map_err(|e| e.to_string())
        }
        "--target-17" => {
            let grover = GroverRecurrenceN4::compute(6);
            serde_json::to_value(&grover).map_err(|e| e.to_string())
        }
        "--target-18" => {
            let sp2_elements = generate_sp2_f2().expect("declared Sp(2,F2) budget");
            let sp4_elements = generate_sp4_f2().expect("declared Sp(4,F2) budget");
            let receipt = json!({
                "target": 18,
                "sp2_f2_order": sp2_elements.len(),
                "sp4_f2_order": sp4_elements.len(),
                "sp2_generators_verified": sp2_elements.len() == 6,
                "sp4_generators_verified": sp4_elements.len() == 720,
                "isomorphic_to": "S_3",
                "authority_effect": "None",
                "status": if sp2_elements.len()==6 && sp4_elements.len()==720 {"VERIFIED_FINITE_CHECKS"} else {"FAIL"}
            });
            serde_json::to_value(&receipt).map_err(|e| e.to_string())
        }
        "--target-19" => {
            let trace_obs = audit_commutator_obstruction_d3().map_err(|e| e.to_string())?;
            serde_json::to_value(&trace_obs).map_err(|e| e.to_string())
        }
        "--target-20" => {
            let rich = RichardsonExtrapolation::new(&[1, 2, 3]);
            serde_json::to_value(&rich).map_err(|e| e.to_string())
        }
        "--target-21" => {
            let s3_walk =
                BallisticWalkReceipt::evaluate("S3", 3).expect("fixed campaign group and steps");
            let s4_walk =
                BallisticWalkReceipt::evaluate("S4", 4).expect("fixed campaign group and steps");
            let receipt = json!({
                "target": 21,
                "s3_walk": s3_walk,
                "s4_walk": s4_walk,
                "ballistic_propagation_certified": s3_walk.is_ballistic_scaling && s4_walk.is_ballistic_scaling,
                "finite_light_cone_window_observed": s3_walk.finite_light_cone_window_observed && s4_walk.finite_light_cone_window_observed,
                "asymptotic_ballistic_scope": "OPEN_ASYMPTOTIC_SCALING",
                "authority_effect": "None",
                "status": if s3_walk.finite_light_cone_window_observed && s4_walk.finite_light_cone_window_observed {"VERIFIED_FINITE_CHECKS"} else {"FAIL"}
            });
            serde_json::to_value(&receipt).map_err(|e| e.to_string())
        }
        "--target-22" => {
            let mub_d3 = MubSystem::mub_d3();
            let tomographer_d3 =
                ExactStateTomographerSystem::new(omega_quantum_physics::mub::MubSystem::mub_d3());
            let d3_tomography_ground =
                tomographer_d3.verify_exact_reconstruction(&state_ground_d3());
            let d3_tomography_magic = tomographer_d3.verify_exact_reconstruction(&state_magic_d3());

            let mub_d4 = MubSystem::mub_d4();
            let tomographer_d4 =
                ExactStateTomographerSystem::new(omega_quantum_physics::mub::MubSystem::mub_d4());
            let d4_tomography_bell = tomographer_d4.verify_exact_reconstruction(&state_bell_d4());
            let d4_tomography_mixed = tomographer_d4.verify_exact_reconstruction(&state_mixed_d4());
            let ck_receipt =
                crate::qm::campaigns::mub_reports::evaluate_all_1024_clifton_kent_valuations(&mub_d4)
                    .expect("declared d4 MUB receipt fixture");

            let receipt = json!({
                "target": 22,
                "d3_bases": mub_d3.bases.len(),
                "d3_orthonormal": mub_d3.verify_same_basis_orthogonality(),
                "d3_unbiased": mub_d3.verify_cross_basis_unbiasedness(),
                "d3_tomography_ground_verified": d3_tomography_ground,
                "d3_tomography_magic_verified": d3_tomography_magic,
                "d4_bases": mub_d4.bases.len(),
                "d4_orthonormal": mub_d4.verify_same_basis_orthogonality(),
                "d4_unbiased": mub_d4.verify_cross_basis_unbiasedness(),
                "d4_tomography_bell_verified": d4_tomography_bell,
                "d4_tomography_mixed_verified": d4_tomography_mixed,
                "clifton_kent_deficit": ck_receipt,
                "authority_effect": "None",
                "status": if mub_d3.verify_same_basis_orthogonality() && mub_d3.verify_cross_basis_unbiasedness() && d3_tomography_ground && d3_tomography_magic && mub_d4.verify_same_basis_orthogonality() && mub_d4.verify_cross_basis_unbiasedness() && d4_tomography_bell && d4_tomography_mixed && ck_receipt.contextuality_persists_unconditionally {"VERIFIED_FINITE_CHECKS"} else {"FAIL"}
            });
            serde_json::to_value(&receipt).map_err(|e| e.to_string())
        }
        "--all" => {
            let t1 = verify_target1_primitive_difference();
            let t2 = verify_target2_diamond_complex();
            let t3 = verify_target3_sorkin_interference();
            let t4 = verify_target4_rational_cayley();
            let t5 = verify_target5_pentagon_identity();
            let t6 = verify_target6_cabello_polytope();
            let t7 = verify_target7_monotone_unitarity();
            let t8 = verify_target8_bell_chsh();
            let t9 = verify_target9_bitflip_code();
            let t10 = verify_target10_teleportation();
            let t11 = verify_target11_superdense_coding();
            let t12 = verify_target12_css_code();

            let wigner = DiscreteWignerSystemD5::new();
            let shor = ShorNineQubitCode::new();
            let pe_verified = DiscretePhaseEstimation::verify_all_dyadic_phases(3);
            let toric = ToricCode2x2::new();
            let grover = GroverRecurrenceN4::compute(6);
            let trace_obs = audit_commutator_obstruction_d3().map_err(|e| e.to_string())?;
            let rich = RichardsonExtrapolation::new(&[1, 2, 3]);
            let s3_walk =
                BallisticWalkReceipt::evaluate("S3", 3).expect("fixed campaign group and steps");
            let s4_walk =
                BallisticWalkReceipt::evaluate("S4", 4).expect("fixed campaign group and steps");
            let mub_d3 = MubSystem::mub_d3();
            let mub_d4 = MubSystem::mub_d4();
            let tomographer_d4 =
                ExactStateTomographerSystem::new(omega_quantum_physics::mub::MubSystem::mub_d4());
            let d4_tomography_ok = tomographer_d4.verify_exact_reconstruction(&state_bell_d4());
            let ck_receipt =
                crate::qm::campaigns::mub_reports::evaluate_all_1024_clifton_kent_valuations(&mub_d4)
                    .expect("declared d4 MUB receipt fixture");
            let sp2_gens = generate_sp2_f2().expect("declared Sp(2,F2) budget");
            let sp4_gens = generate_sp4_f2().expect("declared Sp(4,F2) budget");

            let w_magic = wigner
                .evaluate_exact(&state_magic_d5())
                .map_err(|error| error.to_string())?;
            let magic_has_negativity = w_magic
                .iter()
                .flatten()
                .map(|value| standard_real_sign(&CyclotomicNumber::from(value)))
                .collect::<Result<Vec<_>, _>>()
                .map_err(|error| error.to_string())?
                .iter()
                .any(|&sign| sign < 0);

            let b5 = run_block_05_report();
            let b5_status = b5.status();
            let campaign_reports = json!({
                "block_01_recovery": run_all_recovery_combinations(),
                "block_02_controls": run_negative_controls(),
                "block_03": run_block_03_verification().map_err(|error|error.to_string())?,
                "block_04": execute_dynamics_dichotomy_report(),
                "block_05": b5,
                "block_06": run_block_06_execution().map_err(|e| e.to_string())?,
                "block_07": run_block_07_execution(),
                "block_08": run_block_08_execution(),
                "block_09": run_block_09_execution(),
                "block_10": run_block_10_verification()
            });
            let c250_all_ok =
                run_block_10_verification().terminal_claim_verified && b5_status == "VERIFIED";

            let verified_targets = [
                t1.identity_zero_verified
                    && t1.antisymmetry_verified
                    && t1.cocycle_identity_verified,
                t2.order_4_boundary_cycle_verified && t2.cyclotomic_minimal_polynomial_annihilated,
                t3.sorkin_i3_identically_zero && t3.non_zero_second_order_interference,
                t4.is_exact_orthogonal_isometry,
                t5.pentagon_associator_deficit_is_zero,
                t6.interface_transfer_eliminates_non_bornian,
                t7.exchangeable_is_signed_permutation && t7.irreversible_residue_detected,
                t8.pythagorean_inequality_satisfied,
                t9.stabilizers_commute && t9.deterministic_recovery_verified,
                t10.branch_count == 4
                    && t10.branch_probabilities_equal
                    && t10.all_branches_fidelity_one,
                t11.bell_gram_matrix_is_scaled_identity
                    && t11.decoding_circuit_verified
                    && t11.all_four_messages_deterministic,
                t12.stabilizers_commute && t12.logical_operators_commute_with_stabilizers,
                magic_has_negativity,
                shor.recovery_success_rate == omega_number_theory::rational::r_one(),
                pe_verified,
                toric.logical_homology_braiding_phase == -1,
                grover.exact_one_step_success,
                sp2_gens.len() == 6 && sp4_gens.len() == 720,
                trace_obs.commutator_trace_is_zero,
                rich.weights_sum_to_one && rich.moments_cancelled,
                s3_walk.is_ballistic_scaling && s4_walk.is_ballistic_scaling,
                mub_d3.verify_same_basis_orthogonality()
                    && mub_d3.verify_cross_basis_unbiasedness()
                    && mub_d4.verify_same_basis_orthogonality()
                    && mub_d4.verify_cross_basis_unbiasedness()
                    && d4_tomography_ok,
            ];
            let verified_target_count = verified_targets.iter().filter(|&&ok| ok).count();
            let finite_targets_ok = verified_targets.into_iter().all(|ok| ok);
            let full_receipt = json!({
                "app": "finite_qm_rs",
                "authority_effect": "None",
                "citation": "sealed-derivation-v1 (3100c4e)",
                "targets_certified_count": verified_target_count,
                "target_checks_scope": "Declared finite checks; count does not promote source theorems or authority",
                "target_01_primitive_difference_certified": t1.identity_zero_verified && t1.antisymmetry_verified && t1.cocycle_identity_verified,
                "target_02_diamond_complex_cyclotomic_ring": t2.order_4_boundary_cycle_verified && t2.cyclotomic_minimal_polynomial_annihilated,
                "target_03_sorkin_i3_identically_zero": t3.sorkin_i3_identically_zero && t3.non_zero_second_order_interference,
                "target_04_rational_cayley_so8_isometry": t4.is_exact_orthogonal_isometry,
                "target_05_pentagon_associator_closed": t5.pentagon_associator_deficit_is_zero,
                "target_06_cabello_polytope_transfer_clean": t6.interface_transfer_eliminates_non_bornian,
                "target_07_monotone_layer_unitary_residue": t7.exchangeable_is_signed_permutation && t7.irreversible_residue_detected,
                "target_08_bell_chsh_pythagorean_satisfied": t8.pythagorean_inequality_satisfied,
                "target_09_bitflip_stabilizers_commute": t9.stabilizers_commute && t9.deterministic_recovery_verified,
                "target_10_teleportation_fidelity_one": t10.exact_reconstruction_fidelity == omega_number_theory::rational::r_one(),
                "target_11_superdense_coding_success_one": t11.decoding_success_probability == omega_number_theory::rational::r_one(),
                "target_12_css_code_stabilizers_commute": t12.stabilizers_commute && t12.logical_operators_commute_with_stabilizers,
                "target_13_wigner_d5_magic_point_negativity": magic_has_negativity,
                "target_14_shor_all_errors_recovered": shor.recovery_success_rate == omega_number_theory::rational::r_one(),
                "target_15_phase_estimation_dyadic_exact": pe_verified,
                "target_16_toric_braiding_phase_minus_one": toric.logical_homology_braiding_phase == -1,
                "target_17_grover_n4_exact_chebyshev_success": grover.exact_one_step_success,
                "target_18_sp2_f2_order": sp2_gens.len(),
                "target_18_sp4_f2_order": sp4_gens.len(),
                "target_19_commutator_trace_vanishes": trace_obs.commutator_trace_is_zero,
                "target_20_richardson_moments_vanish": rich.weights_sum_to_one && rich.moments_cancelled,
                "target_21_quantum_walk_ballistic_scaling": s3_walk.is_ballistic_scaling && s4_walk.is_ballistic_scaling,
                "target_22_mub_d3_verified": mub_d3.verify_same_basis_orthogonality() && mub_d3.verify_cross_basis_unbiasedness(),
                "target_22_ext_mub_d4_verified": mub_d4.verify_same_basis_orthogonality() && mub_d4.verify_cross_basis_unbiasedness(),
                "target_22_d4_mub_tomography_verified": d4_tomography_ok,
                "target_22_clifton_kent_all_1024_non_psd_certified": ck_receipt.contextuality_persists_unconditionally,
                "target_22_clifton_kent_non_psd_count": ck_receipt.non_psd_valuations,
                "campaign_c250_blocks_certified_count": serde_json::Value::Null,
                "campaign_c250_reports": campaign_reports,
                "campaign_c250_all_blocks_verified": c250_all_ok,
                "campaign_c250_status": if b5_status == "FAIL" { "FAIL" } else if c250_all_ok { "VERIFIED" } else { "SCOPED_RESULTS_WITH_OPEN_OBLIGATIONS" },
                "status": if b5_status == "FAIL" { "FAIL" } else if c250_all_ok && finite_targets_ok { "VERIFIED_FINITE_CHECKS" } else { "SCOPED_RESULTS_WITH_OPEN_OBLIGATIONS" }
            });
            serde_json::to_value(&full_receipt).map_err(|e| e.to_string())
        }
        "--c250-all" | "--all-c250" => {
            let b1 = run_all_recovery_combinations();
            let b2 = run_negative_controls();
            let b3 = run_block_03_verification().map_err(|error| error.to_string())?;
            let b4 = execute_dynamics_dichotomy_report();
            let b5 = run_block_05_report();
            let b6 = run_block_06_execution().map_err(|e| e.to_string())?;
            let b7 = run_block_07_execution();
            let b8 = run_block_08_execution();
            let b9 = run_block_09_execution();
            let b10 = run_block_10_verification();

            let c250_receipt = json!({
                "app": "finite_qm_rs",
                "authority_effect": "None",
                "citation": "sealed-derivation-v1 (3100c4e)",
                "campaign": "C250",
                "total_blocks": 10,
                "total_steps": 250,
                "block_01_busch_effects_verified": b1.iter().all(|r| r.exact_match && r.is_psd),
                "block_02_finegraining_controls_passed": b2.all_controls_passed,
                "block_03_embeddings_galois_covariance": b3.galois_covariance_of_born_probabilities,
                "block_04_dynamics_pythagorean_infinite_order": b4.pythagorean_infinite_order_lean,
                "block_05_composition_tensor_unique": b5.tensor_unique_under_axioms,
                "block_06_channels_censused": b6.channels_censused,
                "block_07_contextuality_threshold_conductor": b7.contextuality_threshold_conductor_d3,
                "block_08_cancellations_unpairable": b8.targets_with_unpairable_cancellation_count,
                "block_09_growth_refinement_limit": b9.limit_object,
                "block_10_price_list_declarations": b10.declaration_count,
                "status": if b5.status() == "FAIL" { "FAIL" } else { "SCOPED_RESULTS_WITH_OPEN_OBLIGATIONS" }
            });
            serde_json::to_value(&c250_receipt).map_err(|e| e.to_string())
        }
        "--busch-effects" | "--c250-effects" => {
            let results = run_all_recovery_combinations();
            serde_json::to_value(&results).map_err(|e| e.to_string())
        }
        "--busch-recovery" | "--c250-recovery" => {
            let dim: usize = args.get(2).and_then(|s| s.parse().ok()).unwrap_or(2);
            let conductor: usize = args.get(3).and_then(|s| s.parse().ok()).unwrap_or(4);
            let state_kind = args.get(4).map(|s| s.as_str()).unwrap_or("maximally_mixed");
            let res = verify_state_recovery(dim, conductor, state_kind);
            serde_json::to_value(&res).map_err(|e| e.to_string())
        }
        "--finegraining" | "--c250-b02" => {
            let cond_res = search_smallest_irrational_conductor();
            let census = census_all_targets();
            let audit = envariance_deutsch_wallace_symmetry_audit();
            let neg_ctrl = run_negative_controls();
            let receipt = json!({
                "block": 2,
                "global_step": 100,
                "authority_effect": "None",
                "smallest_irrational_conductor": cond_res.smallest_conductor,
                "witness_state": cond_res.witness.state_description,
                "witness_minimal_polynomial": cond_res.witness.minimal_polynomial,
                "total_targets_censused": census.total_targets,
                "targets_rational_sector": census.targets_rational_sector,
                "targets_irrational_sector": census.targets_irrational_sector,
                "min_finegraining_chsh": census.min_finegraining_chsh,
                "symmetry_audit_rational_status": audit.rational_state_status,
                "symmetry_audit_irrational_status": audit.irrational_state_status,
                "everett_counting_status": audit.everett_counting_status,
                "negative_controls_passed": neg_ctrl.all_controls_passed,
                "status": if neg_ctrl.all_controls_passed {"SCOPED_RESULTS_WITH_OPEN_OBLIGATIONS"} else {"FAIL"}
            });
            serde_json::to_value(&receipt).map_err(|e| e.to_string())
        }
        "--embeddings" | "--c250-b03" => {
            let receipt = run_block_03_verification().map_err(|error| error.to_string())?;
            serde_json::to_value(&receipt).map_err(|e| e.to_string())
        }
        "--dynamics" | "--c250-b04" => {
            let receipt = execute_dynamics_dichotomy_report();
            serde_json::to_value(&receipt).map_err(|e| e.to_string())
        }
        "--composition" | "--c250-b05" => {
            let report = run_block_05_report();
            let receipt = json!({
                "block": 5,
                "global_step": 175,
                "authority_effect": "None",
                "tensor_unique_under_axioms": report.tensor_unique_under_axioms,
                "tensor_axiom_count": report.tensor_axiom_count,
                "rival_fails_covariance": report.rival_fails_covariance,
                "d6_mub_count_found": report.d6_mub_count_found,
                "d6_product_mubs_verified": report.d6_product_mubs_verified,
                "d6_fourth_mub_candidates_found": report.d6_fourth_mub_candidates_found,
                "d6_fourth_mub_search_outcome": report.d6_fourth_mub_search_outcome,
                "gkp_conductor_lower_bound_verified": report.gkp_conductor_lower_bound_verified,
                "gkp_conductor_scaling_factor": report.gkp_conductor_scaling_factor,
                "status": report.status()
            });
            serde_json::to_value(&receipt).map_err(|e| e.to_string())
        }
        "--channels" | "--c250-b06" => {
            let report = run_block_06_execution().map_err(|e| e.to_string())?;
            serde_json::to_value(&report).map_err(|e| e.to_string())
        }
        "--contextuality" | "--c250-b07" => {
            let report = run_block_07_execution();
            serde_json::to_value(&report).map_err(|e| e.to_string())
        }
        "--cancellations" | "--c250-b08" => {
            let report = run_block_08_execution();
            serde_json::to_value(&report).map_err(|e| e.to_string())
        }
        "--growth-refinement" | "--c250-b09" => {
            let report = run_block_09_execution();
            serde_json::to_value(&report).map_err(|e| e.to_string())
        }
        "--price-list" | "--c250-b10" => {
            let report = run_block_10_verification();
            serde_json::to_value(&report).map_err(|e| e.to_string())
        }
        "--c500-b01" | "--weyl-b01" | "--weyl-ccr-residual" => {
            let receipt = crate::qm::campaigns::weyl_ccr_residual::generate_canonical_block01_receipt()
                .map_err(|e| e.to_string())?;
            serde_json::to_value(&receipt).map_err(|e| e.to_string())
        }
        "--c500-b02" | "--norm-b02" | "--norm-frontier" => {
            let receipt =
                crate::qm::campaigns::norm_frontier::generate_canonical_block02_receipt();
            serde_json::to_value(&receipt).map_err(|e| e.to_string())
        }
        "--c500-b03" | "--heisenberg-uniqueness" => {
            let receipt = crate::qm::campaigns::heisenberg_unique::generate_canonical_block03_rust_receipt();
            serde_json::to_value(&receipt).map_err(|e| e.to_string())
        }
        "--c500-b04" | "--refinement-tower" => {
            let receipt =
                crate::qm::campaigns::refinement_tower::generate_canonical_block04_rust_receipt();
            serde_json::to_value(&receipt).map_err(|e| e.to_string())
        }
        "--c500-b05" | "--topological-completion" => {
            let receipt =
                crate::qm::campaigns::tower_completion::generate_canonical_block05_rust_receipt();
            serde_json::to_value(&receipt).map_err(|e| e.to_string())
        }
        "--c500-b06" | "--continuous-time" | "--locality-limit" => {
            let receipt =
                crate::qm::campaigns::locality_limit::generate_canonical_block06_rust_receipt();
            serde_json::to_value(&receipt).map_err(|e| e.to_string())
        }
        "--c500-b07" | "--operational-axioms" | "--reconstruction" => {
            let receipt =
                crate::qm::campaigns::axiom_selection::generate_canonical_block07_rust_receipt();
            serde_json::to_value(&receipt).map_err(|e| e.to_string())
        }
        "--c500-b08" | "--correlations" | "--npa-frontier" => {
            let receipt = crate::qm::campaigns::tensor_correlation::generate_canonical_block08_rust_receipt();
            serde_json::to_value(&receipt).map_err(|e| e.to_string())
        }
        "--c500-b09" | "--many-body" | "--lattice-gauge" => {
            let receipt =
                crate::qm::campaigns::lattice_gauge::generate_canonical_block09_rust_receipt();
            serde_json::to_value(&receipt).map_err(|e| e.to_string())
        }
        "--c500-b10" | "--fqmc1" | "--closure-ledger" => {
            let receipt =
                crate::qm::campaigns::operational_closure::generate_canonical_block10_rust_receipt(
                );
            serde_json::to_value(&receipt).map_err(|e| e.to_string())
        }
        "--c500-all" => {
            let blocks = vec![
                serde_json::to_value(crate::qm::campaigns::weyl_ccr_residual::generate_canonical_block01_receipt().map_err(|e| e.to_string())?).unwrap(),
                serde_json::to_value(crate::qm::campaigns::norm_frontier::generate_canonical_block02_receipt()).unwrap(),
                serde_json::to_value(crate::qm::campaigns::heisenberg_unique::generate_canonical_block03_rust_receipt()).unwrap(),
                serde_json::to_value(crate::qm::campaigns::refinement_tower::generate_canonical_block04_rust_receipt()).unwrap(),
                serde_json::to_value(crate::qm::campaigns::tower_completion::generate_canonical_block05_rust_receipt()).unwrap(),
                serde_json::to_value(crate::qm::campaigns::locality_limit::generate_canonical_block06_rust_receipt()).unwrap(),
                serde_json::to_value(crate::qm::campaigns::axiom_selection::generate_canonical_block07_rust_receipt()).unwrap(),
                serde_json::to_value(crate::qm::campaigns::tensor_correlation::generate_canonical_block08_rust_receipt()).unwrap(),
                serde_json::to_value(crate::qm::campaigns::lattice_gauge::generate_canonical_block09_rust_receipt()).unwrap(),
                serde_json::to_value(crate::qm::campaigns::operational_closure::generate_canonical_block10_rust_receipt()).unwrap(),
            ];
            let receipt = json!({
                "campaign": "C500",
                "blocks_generated": blocks.len(),
                "blocks": blocks,
                "global_steps": "301..550",
                "authority_effect": "None",
                "terminal_outcome": "FQMC1_OPEN_INTERNAL_GAPS",
                "launch_preconditions_verified": false,
                "gate_status": "NOT_VERIFIED_BY_CLI",
                "status": "SCOPED_COMPUTATIONS_WITH_OPEN_OBLIGATIONS"
            });
            serde_json::to_value(&receipt).map_err(|e| e.to_string())
        }
        _ => Err(format!("UNKNOWN_SUITE:{target}")),
    }
}
