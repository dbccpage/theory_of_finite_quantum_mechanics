//! Legacy CLI and campaign suite dispatcher for Targets 1..22, C250, and C500.
//!
//! AuthorityEffect: None.

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
use engine_lie_theory::pauli_symplectic::*;
use engine_number_theory::cyclotomic_field::CyclotomicNumber;
use engine_number_theory::cyclotomic_ordered::standard_real_sign;
use engine_quantum_physics::branch_finegraining::search_smallest_irrational_conductor;
use engine_quantum_physics::commutator::*;
use engine_quantum_physics::grover::*;
use engine_quantum_physics::mub::*;
use engine_quantum_physics::phase_estimation::*;
use engine_quantum_physics::richardson::*;
use engine_quantum_physics::shor::*;
use engine_quantum_physics::tomography::*;
use engine_quantum_physics::wigner::*;
use serde::Serialize;
use serde_json::json;

fn to_json_val<T: Serialize>(val: &T) -> Result<serde_json::Value, String> {
    serde_json::to_value(val).map_err(|e| e.to_string())
}

fn status_token(ok: bool, pass_label: &'static str, fail_label: &'static str) -> &'static str {
    if ok {
        pass_label
    } else {
        fail_label
    }
}

pub fn run_legacy_target(target: &str) -> Result<serde_json::Value, String> {
    run_legacy_target_with_args(target, &[])
}

pub fn run_legacy_target_with_args(
    target: &str,
    args: &[String],
) -> Result<serde_json::Value, String> {
    if let Some(res) = dispatch_foundational_targets_1_to_6(target) {
        return res;
    }
    if let Some(res) = dispatch_foundational_targets_7_to_12(target) {
        return res;
    }
    if let Some(res) = dispatch_targets_13_to_17(target) {
        return res;
    }
    if let Some(res) = dispatch_targets_18_to_22(target) {
        return res;
    }
    if let Some(res) = dispatch_c250_part_a(target, args) {
        return res;
    }
    if let Some(res) = dispatch_c250_part_b(target) {
        return res;
    }
    if let Some(res) = dispatch_c500_part_a(target) {
        return res;
    }
    if let Some(res) = dispatch_c500_part_b(target) {
        return res;
    }
    Err(format!("UNKNOWN_SUITE:{target}"))
}

fn dispatch_foundational_targets_1_to_6(
    target: &str,
) -> Option<Result<serde_json::Value, String>> {
    match target {
        "--target-1" => Some(to_json_val(&verify_target1_primitive_difference())),
        "--target-2" => Some(to_json_val(&verify_target2_diamond_complex())),
        "--target-3" => Some(to_json_val(&verify_target3_sorkin_interference())),
        "--target-4" => Some(to_json_val(&verify_target4_rational_cayley())),
        "--target-5" => Some(to_json_val(&verify_target5_pentagon_identity())),
        "--target-6" => Some(to_json_val(&verify_target6_cabello_polytope())),
        _ => None,
    }
}

fn dispatch_foundational_targets_7_to_12(
    target: &str,
) -> Option<Result<serde_json::Value, String>> {
    match target {
        "--target-7" => Some(to_json_val(&verify_target7_monotone_unitarity())),
        "--target-8" => Some(to_json_val(&verify_target8_bell_chsh())),
        "--target-9" => Some(to_json_val(&verify_target9_bitflip_code())),
        "--target-10" => Some(to_json_val(&verify_target10_teleportation())),
        "--target-11" => Some(to_json_val(&verify_target11_superdense_coding())),
        "--target-12" => Some(to_json_val(&verify_target12_css_code())),
        _ => None,
    }
}

fn dispatch_targets_13_to_17(target: &str) -> Option<Result<serde_json::Value, String>> {
    match target {
        "--target-13" => Some(run_target_13_wigner_d5()),
        "--target-14" => {
            let shor = ShorNineQubitCode::new();
            Some(to_json_val(&shor))
        }
        "--target-15" => Some(run_target_15_phase_estimation()),
        "--target-16" => {
            let toric = ToricCode2x2::new();
            Some(to_json_val(&toric))
        }
        "--target-17" => {
            let grover = GroverRecurrenceN4::compute(6);
            Some(to_json_val(&grover))
        }
        _ => None,
    }
}

fn dispatch_targets_18_to_22(target: &str) -> Option<Result<serde_json::Value, String>> {
    match target {
        "--target-18" => Some(run_target_18_symplectic_f2()),
        "--target-19" => Some(
            audit_commutator_obstruction_d3()
                .map_err(|e| e.to_string())
                .and_then(|obs| to_json_val(&obs)),
        ),
        "--target-20" => {
            let rich = RichardsonExtrapolation::new(&[1, 2, 3]);
            Some(to_json_val(&rich))
        }
        "--target-21" => Some(run_target_21_ballistic_walk()),
        "--target-22" => Some(run_target_22_mub_tomography()),
        _ => None,
    }
}

fn wigner_d5_magic_has_negativity(wigner: &DiscreteWignerSystemD5) -> Result<bool, String> {
    let w_magic = wigner
        .evaluate_exact(&state_magic_d5())
        .map_err(|error| error.to_string())?;
    let signs = w_magic
        .iter()
        .flatten()
        .map(|value| standard_real_sign(&CyclotomicNumber::from(value)))
        .collect::<Result<Vec<_>, _>>()
        .map_err(|error| error.to_string())?;
    Ok(signs.iter().any(|&sign| sign < 0))
}

fn run_target_13_wigner_d5() -> Result<serde_json::Value, String> {
    let wigner = DiscreteWignerSystemD5::new();
    let w_ground = wigner
        .evaluate_wigner(&state_ground_d5())
        .map_err(|error| error.to_string())?;
    let zero_q = engine_number_theory::rational::r_zero();
    let stabilizer_non_neg = w_ground.iter().flatten().all(|v| v >= &zero_q);
    let magic_has_negativity = wigner_d5_magic_has_negativity(&wigner)?;
    let both_ok = [stabilizer_non_neg, magic_has_negativity].into_iter().all(|b| b);
    let receipt = json!({
        "target": 13,
        "dimension": 5,
        "phase_points": 25,
        "stabilizer_non_negative": stabilizer_non_neg,
        "magic_point_negativity_certified": magic_has_negativity,
        "authority_effect": "None",
        "status": status_token(both_ok, "VERIFIED_FINITE_CHECKS", "FAIL")
    });
    to_json_val(&receipt)
}

fn run_target_15_phase_estimation() -> Result<serde_json::Value, String> {
    let pe = DiscretePhaseEstimation::run(3, 1);
    let all_verified = DiscretePhaseEstimation::verify_all_dyadic_phases(3);
    let both_ok = [all_verified, pe.is_exact_projection].into_iter().all(|b| b);
    let receipt = json!({
        "target": 15,
        "m_qubits": pe.m_qubits,
        "register_dim": pe.register_dim,
        "dyadic_fraction": format!("{}/{}", pe.dyadic_numerator, pe.dyadic_denominator),
        "is_exact_projection": pe.is_exact_projection,
        "target_probability": format!("{}/{}", pe.target_probability.0, pe.target_probability.1),
        "all_dyadic_phases_verified": all_verified,
        "authority_effect": "None",
        "status": status_token(both_ok, "VERIFIED_FINITE_CHECKS", "FAIL")
    });
    to_json_val(&receipt)
}

fn run_target_18_symplectic_f2() -> Result<serde_json::Value, String> {
    let sp2_elements = generate_sp2_f2().map_err(|e| e.to_string())?;
    let sp4_elements = generate_sp4_f2().map_err(|e| e.to_string())?;
    let sp2_ok = sp2_elements.len() == 6;
    let sp4_ok = sp4_elements.len() == 720;
    let both_ok = [sp2_ok, sp4_ok].into_iter().all(|b| b);
    let receipt = json!({
        "target": 18,
        "sp2_f2_order": sp2_elements.len(),
        "sp4_f2_order": sp4_elements.len(),
        "sp2_generators_verified": sp2_ok,
        "sp4_generators_verified": sp4_ok,
        "isomorphic_to": "S_3",
        "authority_effect": "None",
        "status": status_token(both_ok, "VERIFIED_FINITE_CHECKS", "FAIL")
    });
    to_json_val(&receipt)
}

fn run_target_21_ballistic_walk() -> Result<serde_json::Value, String> {
    let s3_walk = BallisticWalkReceipt::evaluate("S3", 3).map_err(|e| e.to_string())?;
    let s4_walk = BallisticWalkReceipt::evaluate("S4", 4).map_err(|e| e.to_string())?;
    let ballistic = [s3_walk.is_ballistic_scaling, s4_walk.is_ballistic_scaling]
        .into_iter()
        .all(|b| b);
    let light_cone = [
        s3_walk.finite_light_cone_window_observed,
        s4_walk.finite_light_cone_window_observed,
    ]
    .into_iter()
    .all(|b| b);
    let receipt = json!({
        "target": 21,
        "s3_walk": s3_walk,
        "s4_walk": s4_walk,
        "ballistic_propagation_certified": ballistic,
        "finite_light_cone_window_observed": light_cone,
        "asymptotic_ballistic_scope": "OPEN_ASYMPTOTIC_SCALING",
        "authority_effect": "None",
        "status": status_token(light_cone, "VERIFIED_FINITE_CHECKS", "FAIL")
    });
    to_json_val(&receipt)
}

fn run_target_22_mub_tomography() -> Result<serde_json::Value, String> {
    let mub_d3 = MubSystem::mub_d3();
    let tomographer_d3 =
        ExactStateTomographerSystem::new(engine_quantum_physics::mub::MubSystem::mub_d3());
    let d3_tomography_ground = tomographer_d3.verify_exact_reconstruction(&state_ground_d3());
    let d3_tomography_magic = tomographer_d3.verify_exact_reconstruction(&state_magic_d3());

    let mub_d4 = MubSystem::mub_d4();
    let tomographer_d4 =
        ExactStateTomographerSystem::new(engine_quantum_physics::mub::MubSystem::mub_d4());
    let d4_tomography_bell = tomographer_d4.verify_exact_reconstruction(&state_bell_d4());
    let d4_tomography_mixed = tomographer_d4.verify_exact_reconstruction(&state_mixed_d4());
    let ck_receipt =
        crate::qm::campaigns::mub_reports::evaluate_all_1024_clifton_kent_valuations(&mub_d4)?;

    let d3_orth = mub_d3.verify_same_basis_orthogonality();
    let d3_unb = mub_d3.verify_cross_basis_unbiasedness();
    let d4_orth = mub_d4.verify_same_basis_orthogonality();
    let d4_unb = mub_d4.verify_cross_basis_unbiasedness();
    let all_ok = [
        d3_orth,
        d3_unb,
        d3_tomography_ground,
        d3_tomography_magic,
        d4_orth,
        d4_unb,
        d4_tomography_bell,
        d4_tomography_mixed,
        ck_receipt.contextuality_persists_unconditionally,
    ]
    .into_iter()
    .all(|b| b);

    let receipt = json!({
        "target": 22,
        "d3_bases": mub_d3.bases.len(),
        "d3_orthonormal": d3_orth,
        "d3_unbiased": d3_unb,
        "d3_tomography_ground_verified": d3_tomography_ground,
        "d3_tomography_magic_verified": d3_tomography_magic,
        "d4_bases": mub_d4.bases.len(),
        "d4_orthonormal": d4_orth,
        "d4_unbiased": d4_unb,
        "d4_tomography_bell_verified": d4_tomography_bell,
        "d4_tomography_mixed_verified": d4_tomography_mixed,
        "clifton_kent_deficit": ck_receipt,
        "authority_effect": "None",
        "status": status_token(all_ok, "VERIFIED_FINITE_CHECKS", "FAIL")
    });
    to_json_val(&receipt)
}

fn dispatch_c250_part_a(
    target: &str,
    args: &[String],
) -> Option<Result<serde_json::Value, String>> {
    match target {
        "--all" => Some(run_all_targets_and_c250()),
        "--c250-all" | "--all-c250" => Some(run_c250_all_summary()),
        "--busch-effects" | "--c250-effects" => Some(to_json_val(&run_all_recovery_combinations())),
        "--busch-recovery" | "--c250-recovery" => Some(run_busch_recovery_with_args(args)),
        "--finegraining" | "--c250-b02" => Some(run_c250_b02_finegraining()),
        _ => None,
    }
}

fn dispatch_c250_part_b1(target: &str) -> Option<Result<serde_json::Value, String>> {
    match target {
        "--embeddings" | "--c250-b03" => Some(
            run_block_03_verification()
                .map_err(|e| e.to_string())
                .and_then(|r| to_json_val(&r)),
        ),
        "--dynamics" | "--c250-b04" => Some(to_json_val(&execute_dynamics_dichotomy_report())),
        "--composition" | "--c250-b05" => Some(run_c250_b05_composition()),
        "--channels" | "--c250-b06" => Some(
            run_block_06_execution()
                .map_err(|e| e.to_string())
                .and_then(|r| to_json_val(&r)),
        ),
        _ => None,
    }
}

fn dispatch_c250_part_b(target: &str) -> Option<Result<serde_json::Value, String>> {
    if let Some(res) = dispatch_c250_part_b1(target) {
        return Some(res);
    }
    match target {
        "--contextuality" | "--c250-b07" => Some(to_json_val(&run_block_07_execution())),
        "--cancellations" | "--c250-b08" => Some(to_json_val(&run_block_08_execution())),
        "--growth-refinement" | "--c250-b09" => Some(to_json_val(&run_block_09_execution())),
        "--price-list" | "--c250-b10" => Some(to_json_val(&run_block_10_verification())),
        _ => None,
    }
}

fn dispatch_c500_part_a1(target: &str) -> Option<Result<serde_json::Value, String>> {
    match target {
        "--c500-b01" | "--weyl-b01" | "--weyl-ccr-residual" => Some(
            crate::qm::campaigns::weyl_ccr_residual::generate_canonical_block01_receipt()
                .map_err(|e| e.to_string())
                .and_then(|r| to_json_val(&r)),
        ),
        "--c500-b02" | "--norm-b02" | "--norm-frontier" => Some(to_json_val(
            &crate::qm::campaigns::norm_frontier::generate_canonical_block02_receipt(),
        )),
        "--c500-b03" | "--heisenberg-uniqueness" => Some(to_json_val(
            &crate::qm::campaigns::heisenberg_unique::generate_canonical_block03_rust_receipt(),
        )),
        _ => None,
    }
}

fn dispatch_c500_part_a(target: &str) -> Option<Result<serde_json::Value, String>> {
    if let Some(res) = dispatch_c500_part_a1(target) {
        return Some(res);
    }
    match target {
        "--c500-b04" | "--refinement-tower" => Some(to_json_val(
            &crate::qm::campaigns::refinement_tower::generate_canonical_block04_rust_receipt(),
        )),
        "--c500-b05" | "--topological-completion" => Some(to_json_val(
            &crate::qm::campaigns::tower_completion::generate_canonical_block05_rust_receipt(),
        )),
        "--c500-b06" | "--continuous-time" | "--locality-limit" => Some(to_json_val(
            &crate::qm::campaigns::locality_limit::generate_canonical_block06_rust_receipt(),
        )),
        _ => None,
    }
}

fn dispatch_c500_part_b1(target: &str) -> Option<Result<serde_json::Value, String>> {
    match target {
        "--c500-b07" | "--operational-axioms" | "--reconstruction" => Some(to_json_val(
            &crate::qm::campaigns::axiom_selection::generate_canonical_block07_rust_receipt(),
        )),
        "--c500-b08" | "--correlations" | "--npa-frontier" => Some(to_json_val(
            &crate::qm::campaigns::tensor_correlation::generate_canonical_block08_rust_receipt(),
        )),
        _ => None,
    }
}

fn dispatch_c500_part_b(target: &str) -> Option<Result<serde_json::Value, String>> {
    if let Some(res) = dispatch_c500_part_b1(target) {
        return Some(res);
    }
    match target {
        "--c500-b09" | "--many-body" | "--lattice-gauge" => Some(to_json_val(
            &crate::qm::campaigns::lattice_gauge::generate_canonical_block09_rust_receipt(),
        )),
        "--c500-b10" | "--fqmc1" | "--closure-ledger" => Some(to_json_val(
            &crate::qm::campaigns::operational_closure::generate_canonical_block10_rust_receipt(),
        )),
        "--c500-all" => Some(run_c500_all_summary()),
        _ => None,
    }
}

fn run_busch_recovery_with_args(args: &[String]) -> Result<serde_json::Value, String> {
    let dim: usize = args.get(2).and_then(|s| s.parse().ok()).unwrap_or(2);
    let conductor: usize = args.get(3).and_then(|s| s.parse().ok()).unwrap_or(4);
    let state_kind = args.get(4).map(|s| s.as_str()).unwrap_or("maximally_mixed");
    to_json_val(&verify_state_recovery(dim, conductor, state_kind))
}

fn run_c250_b02_finegraining() -> Result<serde_json::Value, String> {
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
        "status": status_token(neg_ctrl.all_controls_passed, "SCOPED_RESULTS_WITH_OPEN_OBLIGATIONS", "FAIL")
    });
    to_json_val(&receipt)
}

fn run_c250_b05_composition() -> Result<serde_json::Value, String> {
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
    to_json_val(&receipt)
}

fn run_c250_all_summary() -> Result<serde_json::Value, String> {
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
    let b1_ok = b1.iter().all(|r| [r.exact_match, r.is_psd].into_iter().all(|b| b));

    let c250_receipt = json!({
        "app": "finite_qm_rs",
        "authority_effect": "None",
        "citation": "sealed-derivation-v1 (3100c4e)",
        "campaign": "C250",
        "total_blocks": 10,
        "total_steps": 250,
        "block_01_busch_effects_verified": b1_ok,
        "block_02_finegraining_controls_passed": b2.all_controls_passed,
        "block_03_embeddings_galois_covariance": b3.galois_covariance_of_born_probabilities,
        "block_04_dynamics_pythagorean_infinite_order": b4.pythagorean_infinite_order_lean,
        "block_05_composition_tensor_unique": b5.tensor_unique_under_axioms,
        "block_06_channels_censused": b6.channels_censused,
        "block_07_contextuality_threshold_conductor": b7.contextuality_threshold_conductor_d3,
        "block_08_cancellations_unpairable": b8.targets_with_unpairable_cancellation_count,
        "block_09_growth_refinement_limit": b9.limit_object,
        "block_10_price_list_declarations": b10.declaration_count,
        "status": status_token(b5.status() != "FAIL", "SCOPED_RESULTS_WITH_OPEN_OBLIGATIONS", "FAIL")
    });
    to_json_val(&c250_receipt)
}

fn collect_c500_blocks_1_to_5() -> Result<Vec<serde_json::Value>, String> {
    let b01 = crate::qm::campaigns::weyl_ccr_residual::generate_canonical_block01_receipt()
        .map_err(|e| e.to_string())?;
    Ok(vec![
        to_json_val(&b01)?,
        to_json_val(&crate::qm::campaigns::norm_frontier::generate_canonical_block02_receipt())?,
        to_json_val(&crate::qm::campaigns::heisenberg_unique::generate_canonical_block03_rust_receipt())?,
        to_json_val(&crate::qm::campaigns::refinement_tower::generate_canonical_block04_rust_receipt())?,
        to_json_val(&crate::qm::campaigns::tower_completion::generate_canonical_block05_rust_receipt())?,
    ])
}

fn collect_c500_blocks_6_to_10() -> Result<Vec<serde_json::Value>, String> {
    Ok(vec![
        to_json_val(&crate::qm::campaigns::locality_limit::generate_canonical_block06_rust_receipt())?,
        to_json_val(&crate::qm::campaigns::axiom_selection::generate_canonical_block07_rust_receipt())?,
        to_json_val(&crate::qm::campaigns::tensor_correlation::generate_canonical_block08_rust_receipt())?,
        to_json_val(&crate::qm::campaigns::lattice_gauge::generate_canonical_block09_rust_receipt())?,
        to_json_val(&crate::qm::campaigns::operational_closure::generate_canonical_block10_rust_receipt())?,
    ])
}

fn run_c500_all_summary() -> Result<serde_json::Value, String> {
    let mut blocks = collect_c500_blocks_1_to_5()?;
    blocks.extend(collect_c500_blocks_6_to_10()?);
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
    to_json_val(&receipt)
}

fn all_bools(flags: &[bool]) -> bool {
    flags.iter().copied().all(|b| b)
}

fn evaluate_foundational_1_to_12_flags() -> ([bool; 12], bool, bool) {
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
    let r_one = engine_number_theory::rational::r_one();

    let flags = [
        all_bools(&[
            t1.identity_zero_verified,
            t1.antisymmetry_verified,
            t1.cocycle_identity_verified,
        ]),
        all_bools(&[
            t2.order_4_boundary_cycle_verified,
            t2.cyclotomic_minimal_polynomial_annihilated,
        ]),
        all_bools(&[
            t3.sorkin_i3_identically_zero,
            t3.non_zero_second_order_interference,
        ]),
        t4.is_exact_orthogonal_isometry,
        t5.pentagon_associator_deficit_is_zero,
        t6.interface_transfer_eliminates_non_bornian,
        all_bools(&[
            t7.exchangeable_is_signed_permutation,
            t7.irreversible_residue_detected,
        ]),
        t8.pythagorean_inequality_satisfied,
        all_bools(&[t9.stabilizers_commute, t9.deterministic_recovery_verified]),
        all_bools(&[
            t10.branch_count == 4,
            t10.branch_probabilities_equal,
            t10.all_branches_fidelity_one,
        ]),
        all_bools(&[
            t11.bell_gram_matrix_is_scaled_identity,
            t11.decoding_circuit_verified,
            t11.all_four_messages_deterministic,
        ]),
        all_bools(&[
            t12.stabilizers_commute,
            t12.logical_operators_commute_with_stabilizers,
        ]),
    ];
    let t10_fid_one = t10.exact_reconstruction_fidelity == r_one;
    let t11_succ_one = t11.decoding_success_probability == r_one;
    (flags, t10_fid_one, t11_succ_one)
}

fn build_c250_campaign_reports() -> Result<(serde_json::Value, String, bool), String> {
    let b5 = run_block_05_report();
    let b5_status = b5.status().to_string();
    let b10 = run_block_10_verification();
    let c250_all_ok = all_bools(&[b10.terminal_claim_verified, b5_status == "VERIFIED"]);
    let reports = json!({
        "block_01_recovery": run_all_recovery_combinations(),
        "block_02_controls": run_negative_controls(),
        "block_03": run_block_03_verification().map_err(|error| error.to_string())?,
        "block_04": execute_dynamics_dichotomy_report(),
        "block_05": b5,
        "block_06": run_block_06_execution().map_err(|e| e.to_string())?,
        "block_07": run_block_07_execution(),
        "block_08": run_block_08_execution(),
        "block_09": run_block_09_execution(),
        "block_10": b10
    });
    Ok((reports, b5_status, c250_all_ok))
}

fn select_all_status(b5_status: &str, all_ok: bool, verified_label: &'static str) -> &'static str {
    if b5_status == "FAIL" {
        "FAIL"
    } else if all_ok {
        verified_label
    } else {
        "SCOPED_RESULTS_WITH_OPEN_OBLIGATIONS"
    }
}

fn run_all_targets_and_c250() -> Result<serde_json::Value, String> {
    let (f1_12, t10_fid_one, t11_succ_one) = evaluate_foundational_1_to_12_flags();
    let wigner = DiscreteWignerSystemD5::new();
    let magic_has_negativity = wigner_d5_magic_has_negativity(&wigner)?;
    let shor_ok = ShorNineQubitCode::new().recovery_success_rate == engine_number_theory::rational::r_one();
    let pe_verified = DiscretePhaseEstimation::verify_all_dyadic_phases(3);
    let toric_ok = ToricCode2x2::new().logical_homology_braiding_phase == -1;
    let grover_ok = GroverRecurrenceN4::compute(6).exact_one_step_success;
    let sp2_order = generate_sp2_f2().map_err(|e| e.to_string())?.len();
    let sp4_order = generate_sp4_f2().map_err(|e| e.to_string())?.len();
    let sp_ok = all_bools(&[sp2_order == 6, sp4_order == 720]);
    let trace_zero = audit_commutator_obstruction_d3()
        .map_err(|e| e.to_string())?
        .commutator_trace_is_zero;
    let rich = RichardsonExtrapolation::new(&[1, 2, 3]);
    let rich_ok = all_bools(&[rich.weights_sum_to_one, rich.moments_cancelled]);
    let s3_walk = BallisticWalkReceipt::evaluate("S3", 3).map_err(|e| e.to_string())?;
    let s4_walk = BallisticWalkReceipt::evaluate("S4", 4).map_err(|e| e.to_string())?;
    let walk_ok = all_bools(&[s3_walk.is_ballistic_scaling, s4_walk.is_ballistic_scaling]);

    let mub_d3 = MubSystem::mub_d3();
    let mub_d4 = MubSystem::mub_d4();
    let d3_mub_ok = all_bools(&[
        mub_d3.verify_same_basis_orthogonality(),
        mub_d3.verify_cross_basis_unbiasedness(),
    ]);
    let d4_mub_ok = all_bools(&[
        mub_d4.verify_same_basis_orthogonality(),
        mub_d4.verify_cross_basis_unbiasedness(),
    ]);
    let d4_tomography_ok =
        ExactStateTomographerSystem::new(engine_quantum_physics::mub::MubSystem::mub_d4())
            .verify_exact_reconstruction(&state_bell_d4());
    let ck_receipt =
        crate::qm::campaigns::mub_reports::evaluate_all_1024_clifton_kent_valuations(&mub_d4)?;
    let t22_ok = all_bools(&[d3_mub_ok, d4_mub_ok, d4_tomography_ok]);

    let (campaign_reports, b5_status, c250_all_ok) = build_c250_campaign_reports()?;
    let tail_flags = [
        magic_has_negativity,
        shor_ok,
        pe_verified,
        toric_ok,
        grover_ok,
        sp_ok,
        trace_zero,
        rich_ok,
        walk_ok,
        t22_ok,
    ];
    let verified_target_count = f1_12.iter().chain(tail_flags.iter()).filter(|&&ok| ok).count();
    let finite_targets_ok = verified_target_count == 22;
    let c250_status = select_all_status(&b5_status, c250_all_ok, "VERIFIED");
    let overall_status = select_all_status(
        &b5_status,
        all_bools(&[c250_all_ok, finite_targets_ok]),
        "VERIFIED_FINITE_CHECKS",
    );

    let full_receipt = json!({
        "app": "finite_qm_rs",
        "authority_effect": "None",
        "citation": "sealed-derivation-v1 (3100c4e)",
        "targets_certified_count": verified_target_count,
        "target_checks_scope": "Declared finite checks; count does not promote source theorems or authority",
        "target_01_primitive_difference_certified": f1_12[0],
        "target_02_diamond_complex_cyclotomic_ring": f1_12[1],
        "target_03_sorkin_i3_identically_zero": f1_12[2],
        "target_04_rational_cayley_so8_isometry": f1_12[3],
        "target_05_pentagon_associator_closed": f1_12[4],
        "target_06_cabello_polytope_transfer_clean": f1_12[5],
        "target_07_monotone_layer_unitary_residue": f1_12[6],
        "target_08_bell_chsh_pythagorean_satisfied": f1_12[7],
        "target_09_bitflip_stabilizers_commute": f1_12[8],
        "target_10_teleportation_fidelity_one": t10_fid_one,
        "target_11_superdense_coding_success_one": t11_succ_one,
        "target_12_css_code_stabilizers_commute": f1_12[11],
        "target_13_wigner_d5_magic_point_negativity": magic_has_negativity,
        "target_14_shor_all_errors_recovered": shor_ok,
        "target_15_phase_estimation_dyadic_exact": pe_verified,
        "target_16_toric_braiding_phase_minus_one": toric_ok,
        "target_17_grover_n4_exact_chebyshev_success": grover_ok,
        "target_18_sp2_f2_order": sp2_order,
        "target_18_sp4_f2_order": sp4_order,
        "target_19_commutator_trace_vanishes": trace_zero,
        "target_20_richardson_moments_vanish": rich_ok,
        "target_21_quantum_walk_ballistic_scaling": walk_ok,
        "target_22_mub_d3_verified": d3_mub_ok,
        "target_22_ext_mub_d4_verified": d4_mub_ok,
        "target_22_d4_mub_tomography_verified": d4_tomography_ok,
        "target_22_clifton_kent_all_1024_non_psd_certified": ck_receipt.contextuality_persists_unconditionally,
        "target_22_clifton_kent_non_psd_count": ck_receipt.non_psd_valuations,
        "campaign_c250_blocks_certified_count": serde_json::Value::Null,
        "campaign_c250_reports": campaign_reports,
        "campaign_c250_all_blocks_verified": c250_all_ok,
        "campaign_c250_status": c250_status,
        "status": overall_status
    });
    to_json_val(&full_receipt)
}
