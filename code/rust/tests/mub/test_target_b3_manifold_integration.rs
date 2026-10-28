//! Comprehensive Integration and Unit Test Suite for Target B3:
//! Global Manifold Obstruction Integration & Complete Moduli Non-Extendibility Closure.
//!
//! AuthorityEffect: None
//!
//! Enforces 100% exact rational and cyclotomic arithmetic, strict zero-floating-point
//! discipline via AST-level inspection with `syn`, exact Cech 2-cocycle condition across
//! all 53 covering nerve triples, continuous Szöllősi parameter chaining, discrete 28-cell
//! partition cover obstruction, Network Simplex cycle circulation lower bound Phi_1 >= Gamma,
//! master unified obstruction disjunction, and negative controls.

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
    is_holonomy_non_trivial, loop_holonomy, ModuliChart5, ModuliLoop, TransitionCocycleFamily,
    Unitary6,
};
use tfqm_mub::native::exact::mub6_manifold_integration::{
    canonical_28_cell_samples, canonical_5_chart_representatives, circulation_gamma,
    continuous_szollosi_chain_samples, evaluate_discrete_circulation_gamma,
    evaluate_master_unified_obstruction, evaluate_target_b3_manifold_integration,
    total_domain_volume, verify_cech_cocycles_all_53_triples, verify_continuous_szollosi_chaining,
    verify_full_unified_coverage, ManifoldIntegrationError, MasterUnifiedObstructionResult,
    UnifiedModuliSample, UnifiedObstructionArm, NUM_CANONICAL_CHARTS,
    NUM_CECH_TRIPLES, TOTAL_CELL_COUNT,
};
use omega_number_theory::cyclotomic::Cyc24;
use omega_number_theory::rational::rq;

// ============================================================================
// 1. STRICT ZERO-FLOAT DISCIPLINE AST AUDIT & NEGATIVE CONTROL
// ============================================================================

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

    // 1. AST-level parse and visit
    let syntax_tree = syn::parse_file(&source)
        .unwrap_or_else(|e| panic!("Failed to parse {}: {}", target_file.display(), e));

    let mut visitor = FloatAuditVisitor {
        found_floats: Vec::new(),
    };
    visitor.visit_file(&syntax_tree);

    assert!(
        visitor.found_floats.is_empty(),
        "Target B3 mub6_manifold_integration.rs violated zero-float discipline: {:?}",
        visitor.found_floats
    );

    // 2. Exact string search: zero occurrences of forbidden float types
    assert!(
        !source.contains("f32"),
        "mub6_manifold_integration.rs must contain zero f32 occurrences"
    );
    assert!(
        !source.contains("f64"),
        "mub6_manifold_integration.rs must contain zero f64 occurrences"
    );
}

#[test]
fn test_negative_control_ast_visitor_catches_floats() {
    // Negative control: Verify that our AST visitor genuinely flags forbidden float types and literals
    let synthetic_source_with_float = r#"
        fn forbidden_calculation() {
            let a: f64 = 1.25;
            let b: f32 = 0.5;
        }
    "#;
    let syntax_tree = syn::parse_file(synthetic_source_with_float)
        .expect("Failed to parse synthetic float source");

    let mut visitor = FloatAuditVisitor {
        found_floats: Vec::new(),
    };
    visitor.visit_file(&syntax_tree);

    assert!(
        visitor.found_floats.len() >= 4,
        "AST visitor must detect both float types and both float literals"
    );
    assert!(visitor.found_floats.iter().any(|f| f.contains("f64")));
    assert!(visitor.found_floats.iter().any(|f| f.contains("f32")));
}

// ============================================================================
// 2. CERTIFIED CONSTANTS & EXACT ALGEBRAIC IDENTITIES
// ============================================================================

#[test]
fn test_certified_constants_and_exact_identities() {
    let gamma = circulation_gamma();
    let eps_min = certified_margin();
    let eps_0 = base_gap();
    let l = lipschitz_bound();
    let delta = delta_certified();
    let d_crit = delta_crit();
    let total_vol = total_domain_volume();

    // 1. Exact rational values matching Lean 4 formalization
    assert_eq!(
        gamma,
        rq(12133, 5000),
        "Gamma must equal 12133 / 5000"
    );
    assert_eq!(
        eps_min,
        rq(12133, 30000),
        "eps_min must equal 12133 / 30000"
    );
    assert_eq!(
        eps_0,
        rq(37249, 90000),
        "eps_0 must equal 37249 / 90000"
    );
    assert_eq!(
        l,
        rq(85, 9),
        "L must equal 85 / 9"
    );
    assert_eq!(
        delta,
        rq(1, 1000),
        "delta must equal 1 / 1000"
    );
    assert_eq!(
        d_crit,
        rq(37249, 850000),
        "delta_crit must equal 37249 / 850000"
    );
    assert_eq!(
        total_vol,
        rq(5001, 1000),
        "Total domain volume must equal 5001 / 1000"
    );

    // 2. Exact identity: 6 * eps_min = Gamma
    let six = BigRational::from_integer(BigInt::from(6));
    let six_eps = &six * &eps_min;
    assert_eq!(
        six_eps, gamma,
        "6 * eps_min must identically equal Gamma = 12133 / 5000"
    );

    // 3. Exact identity: eps_0 - L * delta = eps_min
    let erosion = &l * &delta;
    assert_eq!(erosion, rq(17, 1800), "L * delta must equal 17 / 1800");
    let margin = &eps_0 - &erosion;
    assert_eq!(
        margin, eps_min,
        "eps_0 - L * delta must identically equal eps_min = 12133 / 30000"
    );

    // 4. Mesh step strictly below critical threshold
    assert!(
        delta < d_crit,
        "Certified step 1/1000 must be strictly less than delta_crit = 37249 / 850000"
    );

    // 5. Positive thresholds
    assert!(gamma > BigRational::zero());
    assert!(eps_min > BigRational::zero());
    assert!(total_vol > BigRational::zero());
}

// ============================================================================
// 3. DISCRETE 28-CELL PARTITION COVER EVALUATION
// ============================================================================

#[test]
fn test_discrete_28_cell_coverage_evaluation() {
    let samples = canonical_28_cell_samples();
    assert_eq!(
        samples.len(),
        TOTAL_CELL_COUNT,
        "Must have exactly 28 canonical leaf cell samples"
    );

    let c_family = TransitionCocycleFamily::canonical();
    let min_margin = certified_margin();

    for (idx, sample) in samples.iter().enumerate() {
        // Every cell has certified curvature margin at least eps_min
        assert!(
            sample.curvature_margin >= min_margin,
            "Sample {} ({}) margin {} is below eps_min {}",
            idx,
            sample.sample_id,
            sample.curvature_margin,
            min_margin
        );

        // Disjunction evaluation confirms obstruction
        let res = evaluate_master_unified_obstruction(sample, &c_family, None);
        assert!(
            res.is_obstructed,
            "Sample {} must be obstructed",
            sample.sample_id
        );
        assert!(
            res.curvature_obstructed,
            "Sample {} must satisfy Arm 1 curvature margin",
            sample.sample_id
        );
        assert!(
            res.active_arm == UnifiedObstructionArm::BothArms
                || res.active_arm == UnifiedObstructionArm::CurvatureMarginOnly
        );
    }
}

// ============================================================================
// 4. CONTINUOUS SZÖLLŐSI CHAINING EVALUATION
// ============================================================================

#[test]
fn test_continuous_szollosi_chaining_evaluation() {
    let rep = verify_continuous_szollosi_chaining(40)
        .expect("Continuous Szöllősi chaining verification failed");

    assert!(rep.all_samples_obstructed);
    assert!(rep.gap_stability_certified);
    assert_eq!(rep.mesh_step, delta_certified());
    assert_eq!(rep.uniform_chaining_margin, certified_margin());
    assert_eq!(rep.num_samples_verified, 40);

    // Verify discrete chain samples
    let chain_samples = continuous_szollosi_chain_samples(20);
    assert_eq!(chain_samples.len(), 20);

    let c_family = TransitionCocycleFamily::canonical();
    for sample in &chain_samples {
        assert_eq!(sample.chart, ModuliChart5::SzollosiCurve);
        assert_eq!(sample.curvature_margin, certified_margin());

        let res = evaluate_master_unified_obstruction(sample, &c_family, None);
        assert!(res.is_obstructed);
    }
}

// ============================================================================
// 5. EXACT ČECH COCYCLE VERIFICATION ON ALL 53 TRIPLES
// ============================================================================

#[test]
fn test_cech_cocycle_verification_all_53_triples() {
    let rep = verify_cech_cocycles_all_53_triples()
        .expect("Čech cocycle verification on all 53 triples failed");

    assert_eq!(
        rep.total_triples_verified, NUM_CECH_TRIPLES,
        "Must verify exactly 53 Nerve2 triples"
    );
    assert!(rep.all_triples_valid);
    assert!(rep.deltoid_corner_valid);
    assert!(rep.tao_corner_valid);

    // Verify canonical 5 charts count
    assert_eq!(NUM_CANONICAL_CHARTS, 5);
}

// ============================================================================
// 6. LOOP HOLONOMY NON-TRIVIALITY & NETWORK SIMPLEX CIRCULATION
// ============================================================================

#[test]
fn test_loop_holonomy_and_network_simplex_circulation() {
    let c_family = TransitionCocycleFamily::canonical();

    // 1. Loop holonomy non-triviality on torus collar generator
    let collar_gen = ModuliLoop::torus_collar_generator(4);
    let collar_hol = loop_holonomy(&c_family, &collar_gen);
    assert!(
        is_holonomy_non_trivial(&collar_hol),
        "Generating loop of pi_1(M_6) must have non-trivial holonomy"
    );

    // 2. Network Simplex discrete circulation evaluator Phi_1 >= Gamma
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

// ============================================================================
// 7. MASTER UNIFIED OBSTRUCTION DISJUNCTION
// ============================================================================

#[test]
fn test_master_unified_obstruction_disjunction_cases() {
    let c_family = TransitionCocycleFamily::canonical();
    let min_margin = certified_margin();
    let gamma = circulation_gamma();

    // Case A: Both arms hold (standard certified cell sample)
    let sample_both = UnifiedModuliSample::new(
        "sample_both".to_string(),
        ModuliChart5::SzollosiCurve,
        None,
        vec![BigRational::zero()],
        min_margin.clone(),
        Some(gamma.clone()),
    );
    let res_both = evaluate_master_unified_obstruction(
        &sample_both,
        &c_family,
        Some(&ModuliLoop::composite_6cycle()),
    );
    assert!(res_both.is_obstructed);
    assert!(res_both.curvature_obstructed);
    assert!(res_both.circulation_obstructed);
    assert_eq!(res_both.active_arm, UnifiedObstructionArm::BothArms);

    // Case B: Arm 1 (Curvature Margin) only
    let sample_curv_only = UnifiedModuliSample::new(
        "sample_curv_only".to_string(),
        ModuliChart5::KarlssonManifold,
        None,
        vec![BigRational::zero()],
        min_margin.clone(),
        Some(BigRational::zero()), // circulation 0 < Gamma
    );
    let res_curv = evaluate_master_unified_obstruction(&sample_curv_only, &c_family, None);
    assert!(res_curv.is_obstructed);
    assert!(res_curv.curvature_obstructed);
    assert!(!res_curv.circulation_obstructed);
    assert_eq!(
        res_curv.active_arm,
        UnifiedObstructionArm::CurvatureMarginOnly
    );

    // Case C: Arm 2 (Circulation) only
    let sample_circ_only = UnifiedModuliSample::new(
        "sample_circ_only".to_string(),
        ModuliChart5::DeltoidCusps,
        None,
        vec![BigRational::zero()],
        BigRational::zero(), // margin 0 < eps_min
        Some(gamma.clone()),
    );
    let res_circ = evaluate_master_unified_obstruction(
        &sample_circ_only,
        &c_family,
        Some(&ModuliLoop::composite_6cycle()),
    );
    assert!(res_circ.is_obstructed);
    assert!(!res_circ.curvature_obstructed);
    assert!(res_circ.circulation_obstructed);
    assert_eq!(
        res_circ.active_arm,
        UnifiedObstructionArm::LoopCirculationOnly
    );

    // A scalar claim alone cannot substitute for the missing loop and replay.
    let unwitnessed = evaluate_master_unified_obstruction(&sample_circ_only, &c_family, None);
    assert!(unwitnessed.circulation_phi1.is_none());
    assert!(!unwitnessed.circulation_obstructed);
    assert!(!unwitnessed.is_obstructed);

    // Case D: Neither arm holds (unobstructed counterfactual)
    let sample_neither = UnifiedModuliSample::new(
        "sample_neither".to_string(),
        ModuliChart5::HaagerupOrbit,
        None,
        vec![BigRational::zero()],
        BigRational::zero(),
        Some(BigRational::zero()),
    );
    let res_neither: MasterUnifiedObstructionResult =
        evaluate_master_unified_obstruction(&sample_neither, &c_family, None);
    assert!(!res_neither.is_obstructed);
    assert!(!res_neither.curvature_obstructed);
    assert!(!res_neither.circulation_obstructed);
    assert_eq!(res_neither.active_arm, UnifiedObstructionArm::Neither);
}

#[test]
fn test_canonical_5_chart_representatives() {
    let reps = canonical_5_chart_representatives();
    assert_eq!(reps.len(), NUM_CANONICAL_CHARTS);
    let min_margin = certified_margin();
    for rep in &reps {
        assert!(rep.curvature_margin >= min_margin);
        assert_eq!(rep.generating_circulation, Some(circulation_gamma()));
    }
}

// ============================================================================
// 8. FULL UNIFIED COVERAGE VERIFIER
// ============================================================================

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

// ============================================================================
// 9. MASTER TARGET B3 MANIFOLD INTEGRATION SYNTHESIS
// ============================================================================

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

// ============================================================================
// 10. NEGATIVE CONTROLS
// ============================================================================

#[test]
fn test_negative_control_corrupted_cocycles_rejected() {
    // Construct corrupted cocycle family
    let mut corrupted = TransitionCocycleFamily::canonical();

    // Perturb transition matrix c_{01} by non-trivial phase shift
    let zero = Cyc24::zero();
    let phase = Cyc24::zeta24(4);
    let mat: [[Cyc24; D]; D] = std::array::from_fn(|i| {
        std::array::from_fn(|j| if i == j { phase.clone() } else { zero.clone() })
    });
    corrupted.transitions[0][1] = Unitary6::from_matrix_unchecked(mat);

    // Čech verification must detect violation on any triple containing (0, 1)
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

    assert!(
        violation_detected,
        "Negative control: perturbed cocycle must violate Čech 2-cocycle condition"
    );
}

#[test]
fn test_negative_control_corrupted_circulation_threshold_rejected() {
    let composite_6 = ModuliLoop::composite_6cycle();
    let scale: i128 = 30000;

    // Provide artificially zero defects to simulate collapsed curvature margins
    let zero_defects = vec![BigRational::zero(); 6];
    let res = tfqm_mub::native::exact::mub6_global_gluing::solve_loop_circulation(
        &composite_6,
        scale,
        Some(zero_defects),
    );

    assert!(
        res.is_err(),
        "Negative control: zero defects must be rejected by circulation solver"
    );
}

#[test]
fn test_negative_control_step_exceeds_delta_crit_rejected() {
    let engine = AdaptiveStepEngine::canonical();
    let excessive_step = rq(1, 10); // 1/10 = 85000/850000 > delta_crit = 37249/850000

    assert!(
        !engine.is_admissible_step(&excessive_step),
        "Negative control: excessive step size must be non-admissible"
    );

    let res = engine.validate_step(&excessive_step);
    assert!(
        res.is_err(),
        "Negative control: validate_step must reject step exceeding delta_crit"
    );
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

    let err53 = ManifoldIntegrationError::Expected53Triples { found: 50 };
    assert_eq!(err53.to_string(), "Expected 53 triples in Nerve2, found 50");
}
