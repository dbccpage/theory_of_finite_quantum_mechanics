//! Test suite for Target P6 / B3: Composite Manifold-Collar Boundary Chaining Verifier.
//!
//! AuthorityEffect: None
//!
//! Enforces 100% exact rational arithmetic, strict zero-floating-point discipline,
//! exact Cech 2-cocycle condition across all 53 covering nerve triples, continuous
//! Szöllősi parameter chaining, discrete 28-cell partition cover obstruction,
//! Network Simplex cycle circulation lower bound Phi_1 >= Gamma, master unified
//! obstruction disjunction, and negative controls.

use std::fs;
use std::path::Path;
use syn::visit::Visit;

use num_bigint::BigInt;
use num_rational::BigRational;
use num_traits::Zero;

use tfqm_mub::native::exact::d6_exact_curvature_cochain::D;
use tfqm_mub::native::exact::mub6_constants::{
    base_gap, certified_margin, delta_certified, delta_crit, lipschitz_bound,
};
use tfqm_mub::native::exact::mub6_continuous_chaining::AdaptiveStepEngine;
use tfqm_mub::native::exact::mub6_global_gluing::{
    is_holonomy_non_trivial, loop_holonomy, ModuliLoop, TransitionCocycleFamily, Unitary6,
};
use tfqm_mub::native::exact::mub6_manifold_integration::{
    canonical_28_cell_samples, circulation_gamma, evaluate_discrete_circulation_gamma,
    evaluate_master_unified_obstruction, evaluate_target_b3_manifold_integration,
    total_domain_volume, verify_cech_cocycles_all_53_triples, verify_continuous_szollosi_chaining,
    verify_full_unified_coverage, ManifoldIntegrationError, UnifiedObstructionArm,
    NUM_CANONICAL_CHARTS, NUM_CECH_TRIPLES, TOTAL_CELL_COUNT,
};
use engine_number_theory::cyclotomic::Cyc24;
use engine_number_theory::rational::rq;

struct FloatAuditVisitor {
    found_floats: Vec<String>,
}

impl<'ast> Visit<'ast> for FloatAuditVisitor {
    fn visit_type_path(&mut self, node: &'ast syn::TypePath) {
        for seg in &node.path.segments {
            let ident_str = seg.ident.to_string();
            if ident_str == "f32" || ident_str == "f64" {
                self.found_floats
                    .push(format!("Forbidden float type: {}", ident_str));
            }
        }
        syn::visit::visit_type_path(self, node);
    }

    fn visit_lit_float(&mut self, node: &'ast syn::LitFloat) {
        self.found_floats
            .push(format!("Forbidden float literal: {}", node));
        syn::visit::visit_lit_float(self, node);
    }
}

#[test]
fn test_strict_zero_float_discipline_ast() {
    let manifest_dir = env!("CARGO_MANIFEST_DIR");
    let target_file = Path::new(manifest_dir)
        .join("src")
        .join("native")
        .join("mub6_manifold_integration.rs");

    let source = fs::read_to_string(&target_file)
        .unwrap_or_else(|e| panic!("Failed to read {}: {}", target_file.display(), e));

    let syntax_tree = syn::parse_file(&source)
        .unwrap_or_else(|e| panic!("Failed to parse {}: {}", target_file.display(), e));

    let mut visitor = FloatAuditVisitor {
        found_floats: Vec::new(),
    };
    visitor.visit_file(&syntax_tree);

    assert!(
        visitor.found_floats.is_empty(),
        "mub6_manifold_integration.rs violated zero-float discipline: {:?}",
        visitor.found_floats
    );

    assert!(!source.contains("f32"));
    assert!(!source.contains("f64"));
}

#[test]
fn test_certified_constants_and_exact_identities() {
    let gamma = circulation_gamma();
    let eps_min = certified_margin();
    let eps_0 = base_gap();
    let l = lipschitz_bound();
    let delta = delta_certified();
    let d_crit = delta_crit();
    let total_vol = total_domain_volume();

    assert_eq!(gamma, rq(12133, 5000));
    assert_eq!(eps_min, rq(12133, 30000));
    assert_eq!(eps_0, rq(37249, 90000));
    assert_eq!(l, rq(85, 9));
    assert_eq!(delta, rq(1, 1000));
    assert_eq!(d_crit, rq(37249, 850000));
    assert_eq!(
        total_vol,
        rq(5001, 1000)
    );

    let six = BigRational::from_integer(BigInt::from(6));
    assert_eq!(&six * &eps_min, gamma);

    let erosion = &l * &delta;
    assert_eq!(erosion, rq(17, 1800));
    assert_eq!(&eps_0 - &erosion, eps_min);
    assert!(delta < d_crit);
    assert!(gamma > BigRational::zero());
    assert!(eps_min > BigRational::zero());
    assert!(total_vol > BigRational::zero());
}

#[test]
fn test_discrete_28_cell_coverage_evaluation() {
    let samples = canonical_28_cell_samples();
    assert_eq!(samples.len(), TOTAL_CELL_COUNT);

    let c_family = TransitionCocycleFamily::canonical();
    let min_margin = certified_margin();

    for (idx, sample) in samples.iter().enumerate() {
        assert!(
            sample.curvature_margin >= min_margin,
            "Sample {} ({}) margin below eps_min",
            idx,
            sample.sample_id
        );
        let res = evaluate_master_unified_obstruction(sample, &c_family, None);
        assert!(res.is_obstructed);
        assert!(res.curvature_obstructed);
        assert!(
            res.active_arm == UnifiedObstructionArm::BothArms
                || res.active_arm == UnifiedObstructionArm::CurvatureMarginOnly
        );
    }
}

#[test]
fn test_continuous_szollosi_chaining_evaluation() {
    let rep = verify_continuous_szollosi_chaining(40)
        .expect("Continuous Szöllősi chaining verification failed");

    assert!(rep.all_samples_obstructed);
    assert!(rep.gap_stability_certified);
    assert_eq!(rep.mesh_step, delta_certified());
    assert_eq!(rep.uniform_chaining_margin, certified_margin());
    assert_eq!(rep.num_samples_verified, 40);
}

#[test]
fn test_cech_cocycle_verification_all_53_triples() {
    let rep = verify_cech_cocycles_all_53_triples()
        .expect("Čech cocycle verification on all 53 triples failed");

    assert_eq!(rep.total_triples_verified, NUM_CECH_TRIPLES);
    assert!(rep.all_triples_valid);
    assert!(rep.deltoid_corner_valid);
    assert!(rep.tao_corner_valid);
    assert_eq!(NUM_CANONICAL_CHARTS, 5);
}

#[test]
fn test_loop_holonomy_and_network_simplex_circulation() {
    let c_family = TransitionCocycleFamily::canonical();

    let collar_gen = ModuliLoop::torus_collar_generator(4);
    let collar_hol = loop_holonomy(&c_family, &collar_gen);
    assert!(
        is_holonomy_non_trivial(&collar_hol),
        "Generating loop of pi_1(M_6) must have non-trivial holonomy"
    );

    let circ_rep = evaluate_discrete_circulation_gamma()
        .expect("Network Simplex circulation evaluation failed");

    assert_eq!(circ_rep.num_edges, 6);
    assert_eq!(circ_rep.gamma_scaled, 72798);
    assert!(circ_rep.phi1_objective >= circ_rep.gamma_scaled);
    assert_eq!(circ_rep.coboundary_sum, 0);
    assert!(circ_rep.circulation_conserved);
    assert!(circ_rep.dual_gap_zero);
    assert!(circ_rep.circulation_obstructed);
}

#[test]
fn test_full_unified_coverage_verifier() {
    let cov_rep =
        verify_full_unified_coverage().expect("Full unified coverage verification failed");

    assert!(cov_rep.all_samples_obstructed);
    // Finitely many obstructed samples cannot certify closure.
    assert!(!cov_rep.closure_certified);
    assert_eq!(cov_rep.cells_tested, TOTAL_CELL_COUNT);
    assert_eq!(cov_rep.charts_tested, NUM_CANONICAL_CHARTS);
    assert_eq!(
        cov_rep.coverage_fraction,
        BigRational::from_integer(BigInt::from(1))
    );
    assert_eq!(cov_rep.total_partition_volume, total_domain_volume());
}

#[test]
fn test_master_target_b3_manifold_integration_synthesis() {
    let rep = evaluate_target_b3_manifold_integration()
        .expect("Master Target B3 manifold integration evaluation failed");

    assert_eq!(
        rep.firewall,
        "stated region only; mints no authority"
    );
    assert_eq!(rep.authority_effect, "None");
    assert!(rep.discrete_28_cells_obstructed);
    assert!(rep.continuous_chaining_obstructed);
    assert!(rep.loop_circulation_obstructed);
    assert!(rep.master_unified_obstruction_verified);
    // Closure rests on sampled coverage, so neither the covering closure
    // nor the no-go it implies is established.
    assert!(!rep.moduli_covering_closure);
    assert!(!rep.no_complete_mub6);

    assert_eq!(rep.cech_report.total_triples_verified, 53);
    assert!(rep.cech_report.all_triples_valid);
    assert!(rep.cech_report.deltoid_corner_valid);
    assert!(rep.cech_report.tao_corner_valid);
    assert!(rep.circulation_report.circulation_obstructed);
    assert!(!rep.coverage_report.closure_certified);
}

#[test]
fn test_negative_control_corrupted_cocycles_rejected() {
    let mut corrupted = TransitionCocycleFamily::canonical();
    let zero = Cyc24::zero();
    let phase = Cyc24::zeta24(4);
    let mat: [[Cyc24; D]; D] = std::array::from_fn(|i| {
        std::array::from_fn(|j| if i == j { phase.clone() } else { zero.clone() })
    });
    corrupted.transitions[0][1] = Unitary6::from_matrix_unchecked(mat);

    let triples = tfqm_mub::native::exact::mub6_global_gluing::enumerate_nerve2_triples();
    let mut violation_detected = false;

    for &(i, j, k) in &triples {
        let cij = corrupted.get(i, j);
        let cjk = corrupted.get(j, k);
        let cki = corrupted.get(k, i);

        let prod = cij.mul(cjk).mul(cki);
        if !prod.is_identity() {
            violation_detected = true;
            break;
        }
    }

    assert!(violation_detected);
}

#[test]
fn test_negative_control_corrupted_circulation_threshold_rejected() {
    let composite_6 = ModuliLoop::composite_6cycle();
    let scale: i128 = 30000;
    let zero_defects = vec![BigRational::zero(); 6];
    let res = tfqm_mub::native::exact::mub6_global_gluing::solve_loop_circulation(
        &composite_6,
        scale,
        Some(zero_defects),
    );
    assert!(res.is_err());
}

#[test]
fn test_negative_control_step_exceeds_delta_crit_rejected() {
    let engine = AdaptiveStepEngine::canonical();
    let excessive_step = rq(1, 10);
    assert!(!engine.is_admissible_step(&excessive_step));
    assert!(engine.validate_step(&excessive_step).is_err());
}

#[test]
fn test_negative_control_incomplete_coverage_error() {
    let err = ManifoldIntegrationError::IncompleteCoverage {
        obstructed: 27,
        total: 28,
    };
    assert_eq!(
        err.to_string(),
        "Incomplete coverage: 27 of 28 samples obstructed"
    );
}
