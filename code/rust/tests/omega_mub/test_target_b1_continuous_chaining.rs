//! Comprehensive Integration and Unit Test Suite for Target B1:
//! Continuous Parameter Chaining & Global Manifold Embedding Engine.
//!
//! AuthorityEffect: None
//!
//! Enforces 100% exact rational arithmetic, strict zero-floating-point discipline
//! via AST inspection with `syn`, certified Lipschitz margin positivity, and
//! critical step-size threshold rejections.

use std::fs;
use std::path::Path;
use syn::visit::Visit;

use num_rational::BigRational;
use num_traits::{One, Zero};

use omega_mub::omega_native::exact::d6_exact_curvature_cochain::D;
use omega_mub::omega_native::exact::mub6_constants::{
    base_gap, certified_erosion, certified_margin, delta_certified, delta_crit, lipschitz_bound,
};
use omega_mub::omega_native::exact::mub6_continuous_chaining::{
    audit_continuation_chain, audit_multi_anchor_cover, build_multi_anchor_covering,
    build_multi_anchor_covering_domain, gap_probe_t, karlsson_boundary_z, num_anchors_min,
    t_max_multi_anchor, t_min_multi_anchor, theta_interval_lower, theta_interval_upper,
    verify_curvature_wall_propagation, verify_empty_zerorel_variety, verify_gap_probe_covered,
    AdaptiveStepEngine, ContinuousChainingError, ContinuousChainingPath, CurveRegime,
    KarlssonBoundaryConnection, MultiAnchorAuditReceipt, MultiAnchorBall, MultiAnchorCover,
    RepresentativePointSet, GAP_PROBE_T_DEN, GAP_PROBE_T_NUM, NUM_ANCHORS_MIN,
    T_MAX_MULTI_ANCHOR_DEN, T_MAX_MULTI_ANCHOR_NUM, T_MIN_MULTI_ANCHOR_DEN, T_MIN_MULTI_ANCHOR_NUM,
};
use omega_mub::omega_native::exact::mub6_f6_chart::f6_family_columns;
use omega_mub::omega_native::exact::mub6_firewall::{AUTHORITY_EFFECT, FIREWALL};
use omega_mub::omega_native::exact::mub6_zerorel_variety::{
    dita_representative_triple, tao_representative_triple, BasisCyc,
};
use omega_number_theory::rational::rq;

// ============================================================================
// 1. STRICT ZERO-FLOAT DISCIPLINE AST AUDIT
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
        .join("omega_native")
        .join("mub6_continuous_chaining.rs");

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
        "Target B1 mub6_continuous_chaining.rs violated zero-float discipline: {:?}",
        visitor.found_floats
    );

    // 2. Exact token assertions: 0 occurrences of f32 / f64
    assert!(
        !source.contains("f32"),
        "mub6_continuous_chaining.rs must contain zero f32 occurrences"
    );
    assert!(
        !source.contains("f64"),
        "mub6_continuous_chaining.rs must contain zero f64 occurrences"
    );
}

// ============================================================================
// 2. EXACT RATIONAL CERTIFIED CONSTANTS AND RELATIONS
// ============================================================================

#[test]
fn test_certified_constants_and_algebraic_relations() {
    let eps = base_gap();
    let l = lipschitz_bound();
    let d_crit = delta_crit();
    let d_cert = delta_certified();
    let erosion = certified_erosion();
    let margin = certified_margin();
    let z_bound = karlsson_boundary_z();

    // 1. Check exact rational values
    assert_eq!(eps, rq(37249, 90000), "Base gap ε must be 37249/90000");
    assert_eq!(l, rq(85, 9), "Lipschitz bound L must be 85/9");
    assert_eq!(
        d_crit,
        rq(37249, 850000),
        "Critical step δ_crit must be 37249/850000"
    );
    assert_eq!(d_cert, rq(1, 1000), "Certified step δ must be 1/1000");
    assert_eq!(
        erosion,
        rq(17, 1800),
        "Certified erosion L δ must be 17/1800"
    );
    assert_eq!(
        margin,
        rq(12133, 30000),
        "Certified margin ε - L δ must be 12133/30000"
    );
    assert_eq!(
        z_bound,
        rq(1, 1000),
        "Karlsson boundary depth z must be 1/1000"
    );

    // 2. Verify algebraic consistency: δ_crit = ε / L
    let computed_crit = &eps / &l;
    assert_eq!(
        computed_crit, d_crit,
        "Critical step must identically equal ε / L"
    );

    // 3. Verify algebraic consistency: erosion = L · δ
    let computed_erosion = &l * &d_cert;
    assert_eq!(
        computed_erosion, erosion,
        "Erosion must identically equal L · δ"
    );

    // 4. Verify algebraic consistency: margin = ε - L · δ
    let computed_margin = &eps - &computed_erosion;
    assert_eq!(
        computed_margin, margin,
        "Margin must identically equal ε - L · δ"
    );

    // 5. Margin must be strictly positive
    assert!(
        margin > BigRational::zero(),
        "Certified margin must be strictly positive"
    );

    // 6. Certified step must be strictly below critical threshold
    assert!(
        d_cert < d_crit,
        "Certified step 1/1000 must be strictly less than critical step 37249/850000"
    );
}

// ============================================================================
// 3. STEP-SIZE ADAPTIVITY & CRITICAL REJECTIONS
// ============================================================================

#[test]
fn test_step_size_adaptivity_and_critical_rejections() {
    let engine = AdaptiveStepEngine::canonical();

    // 1. Certified step size passes with exact expected margin
    let verified_margin = engine.validate_step(&delta_certified()).unwrap();
    assert_eq!(verified_margin, certified_margin());
    assert!(verified_margin >= rq(12133, 30000));

    // 2. Smaller step sizes yield strictly larger margins
    let half_step = rq(1, 2000);
    let half_margin = engine.validate_step(&half_step).unwrap();
    assert!(
        half_margin > verified_margin,
        "Refined step must increase margin"
    );
    assert_eq!(half_margin, rq(4603, 11250));

    // 3. Step size equal to critical threshold MUST be rejected
    let res_crit = engine.validate_step(&delta_crit());
    match res_crit {
        Err(ContinuousChainingError::StepExceedsCriticalThreshold { step, delta_crit }) => {
            assert_eq!(step, delta_crit);
        }
        other => panic!("Expected StepExceedsCriticalThreshold, got {:?}", other),
    }

    // 4. Super-critical step sizes MUST be rejected
    let oversized = rq(1, 10);
    assert!(matches!(
        engine.validate_step(&oversized),
        Err(ContinuousChainingError::StepExceedsCriticalThreshold { .. })
    ));

    // 5. Non-positive step sizes MUST be rejected
    assert!(matches!(
        engine.validate_step(&BigRational::zero()),
        Err(ContinuousChainingError::InvalidParameter(_))
    ));
    assert!(matches!(
        engine.validate_step(&rq(-1, 1000)),
        Err(ContinuousChainingError::InvalidParameter(_))
    ));

    // 6. Critical ratio check
    let ratio = engine.critical_ratio(&delta_certified());
    assert_eq!(ratio, rq(850, 37249));
    assert!(ratio < BigRational::one());

    // 7. Dynamic step adaptivity under curvature scaling
    let scale_factor = rq(2, 1);
    let adapted = engine.adapt_step(&scale_factor);
    assert_eq!(adapted, rq(1, 2000));
}

// ============================================================================
// 4. CONTINUOUS PARAMETER GRID EVALUATION OVER θ ∈ (0, π/3)
// ============================================================================

#[test]
fn test_continuous_parameter_grid_evaluation() {
    let path =
        ContinuousChainingPath::generate_canonical().expect("Canonical path generation failed");

    // 1. Verify path domain
    assert_eq!(path.domain_lo, theta_interval_lower());
    assert_eq!(path.domain_hi, theta_interval_upper());

    // 2. Node count and bounds
    assert!(
        path.total_nodes >= 167,
        "Path must have at least 167 nodes for step 1/1000"
    );
    assert_eq!(path.total_nodes, path.nodes.len());

    // 3. No-gap overlap verification
    assert!(
        path.no_gaps,
        "Path must be free of gaps between adjacent intervals"
    );
    for i in 0..(path.nodes.len() - 1) {
        let prev_hi = &path.nodes[i].interval.hi;
        let next_lo = &path.nodes[i + 1].interval.lo;
        assert!(
            next_lo <= prev_hi,
            "Interval {} ({:?}) and {} ({:?}) must overlap",
            i,
            path.nodes[i].interval,
            i + 1,
            path.nodes[i + 1].interval
        );
    }

    // 4. Positivity of all certified margins
    assert!(path.all_certified);
    assert!(
        path.min_margin >= certified_margin(),
        "Minimum margin {} must be at least certified margin {}",
        path.min_margin,
        certified_margin()
    );

    // 5. Query arbitrary intermediate points
    let query_mid = rq(1, 12); // θ = π/6
    let margin_mid = path.eval_margin_at_point(&query_mid).unwrap();
    assert!(margin_mid >= certified_margin());

    let query_cusp = rq(1, 2000); // near cusp
    let margin_cusp = path.eval_margin_at_point(&query_cusp).unwrap();
    assert!(margin_cusp >= certified_margin());

    let query_boundary = rq(497, 3000); // near boundary
    let margin_boundary = path.eval_margin_at_point(&query_boundary).unwrap();
    assert!(margin_boundary >= certified_margin());

    // 6. Out of bounds queries rejected
    assert!(matches!(
        path.eval_margin_at_point(&rq(-1, 100)),
        Err(ContinuousChainingError::PointOutOfBounds { .. })
    ));
    assert!(matches!(
        path.eval_margin_at_point(&rq(1, 2)),
        Err(ContinuousChainingError::PointOutOfBounds { .. })
    ));
}

// ============================================================================
// 5. REPRESENTATIVE POINTS & REGIME COVERAGE
// ============================================================================

#[test]
fn test_representative_points_and_regimes() {
    let rep_set = RepresentativePointSet::canonical();
    let engine = AdaptiveStepEngine::canonical();
    let path = ContinuousChainingPath::generate_canonical().unwrap();

    // 1. Check regimes of representative points
    for pt in &rep_set.near_cusp {
        assert_eq!(
            CurveRegime::classify(pt),
            CurveRegime::NearCusp,
            "Point {} must be in NearCusp regime",
            pt
        );
    }

    for pt in &rep_set.intermediate {
        assert_eq!(
            CurveRegime::classify(pt),
            CurveRegime::Intermediate,
            "Point {} must be in Intermediate regime",
            pt
        );
    }

    for pt in &rep_set.near_boundary {
        assert_eq!(
            CurveRegime::classify(pt),
            CurveRegime::NearBoundary,
            "Point {} must be in NearBoundary regime",
            pt
        );
    }

    // 2. Evaluate all representative points
    let evals = rep_set
        .evaluate_all(&engine, &delta_certified())
        .expect("Evaluation of representative points failed");

    for ev in &evals {
        assert!(
            ev.is_positive,
            "Point {} must have positive margin",
            ev.point
        );
        assert!(
            ev.satisfies_certified_floor,
            "Point {} must satisfy certified floor",
            ev.point
        );
        assert_eq!(ev.margin, certified_margin());
    }

    // 3. Verify all representative points are covered by the chaining path
    rep_set
        .verify_all_covered_by_path(&path)
        .expect("Representative points must all be covered by the path");
}

// ============================================================================
// 6. CONTINUOUS UNITARY GAUGE INTEGRATION TO KARLSSON BOUNDARY MANIFOLD
// ============================================================================

#[test]
fn test_continuous_unitary_gauge_integration_karlsson() {
    let connection = KarlssonBoundaryConnection::at_boundary_depth();

    // 1. Verify interface depth
    assert_eq!(connection.z_depth, rq(1, 1000));
    assert_eq!(connection.interface_margin, rq(12133, 30000));
    assert!(connection.is_unitary_certified);
    assert!(connection.preserves_curvature_wall);

    // 2. Verify unitary matrices along gauge path
    for phase_shift in [0, 1, 4, 8, 12, 16, 20] {
        let v = KarlssonBoundaryConnection::unitary_gauge_v(phase_shift);
        assert!(
            KarlssonBoundaryConnection::verify_matrix_unitary(&v),
            "Matrix V for phase shift {} must be strictly unitary",
            phase_shift
        );
    }

    // 3. Verify gauge invariance of curvature mass
    let t_dita = dita_representative_triple();
    let cand_u: BasisCyc = f6_family_columns(2, 4);

    for phase_shift in [1, 8, 16] {
        let invariant = connection
            .verify_gauge_invariance_along_path(&t_dita, &cand_u, phase_shift)
            .expect("Gauge invariance verification failed");
        assert!(
            invariant,
            "Curvature mass must be strictly invariant under unitary gauge shift {}",
            phase_shift
        );
    }

    let t_tao = tao_representative_triple();
    for phase_shift in [2, 4, 12] {
        let invariant = connection
            .verify_gauge_invariance_along_path(&t_tao, &cand_u, phase_shift)
            .expect("Gauge invariance verification failed");
        assert!(
            invariant,
            "Tao curvature mass must be strictly invariant under unitary gauge shift {}",
            phase_shift
        );
    }
}

// ============================================================================
// 7. CURVATURE WALL PROPAGATION & EMPTY ZEROREL VARIETY
// ============================================================================

#[test]
fn test_curvature_wall_propagation_and_empty_zerorel_variety() {
    let path = ContinuousChainingPath::generate_canonical().unwrap();

    // 1. Verify curvature wall propagation
    let cert = verify_curvature_wall_propagation(&path)
        .expect("Curvature wall propagation verification failed");

    assert!(cert.curvature_wall_intact);
    assert!(cert.zero_rel_variety_empty);
    assert_eq!(cert.min_margin, certified_margin());
    assert_eq!(cert.max_step, delta_certified());

    // 2. Verify empty ZeroRel variety with Dita representative triple
    let t_dita = dita_representative_triple();
    let cand_u: BasisCyc = f6_family_columns(2, 4);

    let empty_cert = verify_empty_zerorel_variety(&t_dita, &cand_u)
        .expect("ZeroRel variety emptiness check failed");

    assert!(empty_cert.variety_empty);
    assert!(empty_cert.candidate_curvature_mass >= certified_margin());
    assert_eq!(empty_cert.certified_margin_floor, certified_margin());
    assert_eq!(empty_cert.firewall_line, FIREWALL);

    // 3. Negative control: artificial broken path rejected
    let mut broken_path = path.clone();
    broken_path.nodes[5].certified_margin = rq(-1, 100);
    broken_path.min_margin = rq(-1, 100);

    assert!(matches!(
        verify_curvature_wall_propagation(&broken_path),
        Err(ContinuousChainingError::CurvatureWallViolation { .. })
    ));
}

// ============================================================================
// 8. EPISTEMIC FIREWALL & CLAIM HYGIENE AUDIT
// ============================================================================

#[test]
fn test_firewall_and_authority() {
    assert_eq!(
        FIREWALL,
        "stated region only; mints no authority"
    );
    assert_eq!(AUTHORITY_EFFECT, "None");
    assert_eq!(D, 6);
}

// ============================================================================
// 9. MULTI-ANCHOR COVERING, SENTRY & AUDITOR (TARGET P4 REQUIREMENT R2)
// ============================================================================

#[test]
fn test_multi_anchor_canonical_constants_and_helpers() {
    let t_min = t_min_multi_anchor();
    let t_max = t_max_multi_anchor();
    let probe = gap_probe_t();

    assert_eq!(t_min, rq(1, 180), "T_MIN must be 1/180");
    assert_eq!(t_max, rq(59, 180), "T_MAX must be 59/180");
    assert_eq!(probe, rq(1, 122), "GAP_PROBE_T must be 1/122");
    assert_eq!(NUM_ANCHORS_MIN, 80);
    assert_eq!(num_anchors_min(), 80);

    assert_eq!(T_MIN_MULTI_ANCHOR_NUM, 1);
    assert_eq!(T_MIN_MULTI_ANCHOR_DEN, 180);
    assert_eq!(T_MAX_MULTI_ANCHOR_NUM, 59);
    assert_eq!(T_MAX_MULTI_ANCHOR_DEN, 180);
    assert_eq!(GAP_PROBE_T_NUM, 1);
    assert_eq!(GAP_PROBE_T_DEN, 122);

    assert!(
        t_min < probe,
        "T_MIN 1/180 must be strictly less than probe 1/122"
    );
    assert!(
        probe < t_max,
        "Probe 1/122 must be strictly less than T_MAX 59/180"
    );
    assert!(t_min > BigRational::zero());
}

#[test]
fn test_multi_anchor_covering_acceptance_250() {
    let delta = delta_certified();
    let cover: MultiAnchorCover =
        build_multi_anchor_covering(250, &delta).expect("Multi-anchor covering build failed");

    // 1. Basic properties
    assert_eq!(cover.balls.len(), 250);
    assert_eq!(cover.t_min, t_min_multi_anchor());
    assert_eq!(cover.t_max, t_max_multi_anchor());
    assert!(cover.gap_probe_covered);

    // 2. Audit receipt verification
    let receipt: MultiAnchorAuditReceipt =
        audit_multi_anchor_cover(&cover).expect("Cover audit failed");
    assert!(receipt.verified);
    assert!(!receipt.analytic_obstruction_verified);
    assert!(receipt.adjacent_overlap_verified);
    assert!(receipt.endpoint_coverage_verified);
    assert!(receipt.gap_probe_covered);
    assert!(receipt.all_margins_positive);
    assert_eq!(receipt.num_balls, 250);
    assert_eq!(receipt.min_margin, certified_margin());

    // 3. Invariant (a): Adjacent overlap theta_{k+1} - theta_k <= delta_k + delta_{k+1}
    for i in 0..(cover.balls.len() - 1) {
        let b_curr = &cover.balls[i];
        let b_next = &cover.balls[i + 1];
        let step = &b_next.theta - &b_curr.theta;
        let radii_sum = &b_curr.delta + &b_next.delta;
        assert!(step <= radii_sum, "Adjacent overlap failed at index {i}");
        assert!(
            b_curr.overlaps_with(b_next),
            "Ball.overlaps_with failed at index {i}"
        );
    }

    // 4. Invariant (b): Endpoint coverage
    let left_0 = cover.balls[0].left();
    let right_last = cover.balls[cover.balls.len() - 1].right();
    assert!(
        left_0 <= t_min_multi_anchor(),
        "Left endpoint not covered: {left_0} > T_MIN"
    );
    assert!(
        right_last >= t_max_multi_anchor(),
        "Right endpoint not covered: {right_last} < T_MAX"
    );

    // 5. Invariant (c): Local positive margins
    for (i, b) in cover.balls.iter().enumerate() {
        assert!(b.is_anchor, "Ball {i} must be an anchor");
        assert!(
            b.margin > BigRational::zero(),
            "Ball {i} margin must be > 0"
        );
        assert!(
            b.margin >= certified_margin(),
            "Ball {i} margin {} must be >= certified_margin {}",
            b.margin,
            certified_margin()
        );
    }

    // 6. Invariant (d): Gap probe verification
    let probe = gap_probe_t();
    let (covered, probe_idx, dist_opt) = verify_gap_probe_covered(&cover.balls, &probe);
    assert!(covered, "Probe point 1/122 must be covered");
    assert!(probe_idx.is_some());
    let idx = probe_idx.unwrap();
    let covering_ball = &cover.balls[idx];
    assert!(covering_ball.contains(&probe));
    let dist = dist_opt.unwrap();
    assert!(dist <= delta);

    // 7. Margin evaluation at arbitrary points
    let margin_at_probe = cover.eval_margin_at_point(&probe).unwrap();
    assert!(margin_at_probe >= certified_margin());

    let margin_at_mid = cover.eval_margin_at_point(&rq(1, 10)).unwrap();
    assert!(margin_at_mid >= certified_margin());
}

#[test]
fn multi_anchor_audit_rechecks_mutated_ball_data() {
    let mut cover = build_multi_anchor_covering(600, &delta_certified()).unwrap();
    cover.balls[100].delta = BigRational::new((-1).into(), 100000.into());
    assert!(audit_multi_anchor_cover(&cover).is_err());
    let mut inflated = build_multi_anchor_covering(250, &delta_certified()).unwrap();
    inflated.balls[10].margin = inflated.balls[10].epsilon_base.clone();
    assert!(audit_multi_anchor_cover(&inflated).is_err());
}

#[test]
fn test_multi_anchor_covering_acceptance_200() {
    let delta = delta_certified();
    let cover = build_multi_anchor_covering(200, &delta).expect("N=200 build failed");
    assert_eq!(cover.balls.len(), 200);

    let receipt = cover.audit().expect("Audit failed for N=200");
    assert!(receipt.verified);
    assert!(receipt.gap_probe_covered);
    assert!(receipt.min_margin >= certified_margin());
}

#[test]
fn test_multi_anchor_negative_control_gapped_anchors() {
    // 1. Manually created gap by removing ball 10 from valid 250-cover
    let mut cover = build_multi_anchor_covering(250, &delta_certified()).unwrap();
    cover.balls.remove(10);

    let res = audit_multi_anchor_cover(&cover);
    match res {
        Err(ContinuousChainingError::AdjacentOverlapViolated {
            index,
            next_index,
            step,
            radii_sum,
        }) => {
            assert_eq!(index, 9);
            assert_eq!(next_index, 10);
            assert!(step > radii_sum);
        }
        other => panic!("Expected AdjacentOverlapViolated, got {:?}", other),
    }

    // 2. Insufficient points (N=80 with delta=1/1000 has step ~ 0.004 > 2*delta 0.002)
    let res_80 = build_multi_anchor_covering(80, &delta_certified());
    match res_80 {
        Err(ContinuousChainingError::AdjacentOverlapViolated { .. }) => {}
        other => panic!(
            "Expected AdjacentOverlapViolated for N=80 with delta=1/1000, got {:?}",
            other
        ),
    }

    // 3. Below minimum points (N=79 < NUM_ANCHORS_MIN=80)
    let res_79 = build_multi_anchor_covering(79, &delta_certified());
    match res_79 {
        Err(ContinuousChainingError::InvalidParameter(msg)) => {
            assert!(msg.contains("at least 80 points"));
        }
        other => panic!("Expected InvalidParameter for N=79, got {:?}", other),
    }
}

#[test]
fn test_multi_anchor_negative_control_undersized_endpoints() {
    let valid_cover = build_multi_anchor_covering(250, &delta_certified()).unwrap();

    // 1. Shift all balls right by 1/100 -> left endpoint theta_0 - delta > T_MIN
    let mut shifted_right = valid_cover.clone();
    let shift_right = rq(1, 100);
    for b in &mut shifted_right.balls {
        b.theta = &b.theta + &shift_right;
    }
    match audit_multi_anchor_cover(&shifted_right) {
        Err(ContinuousChainingError::EndpointCoverageViolated { left, t_min, .. }) => {
            assert!(left > t_min);
        }
        other => panic!("Expected EndpointCoverageViolated, got {:?}", other),
    }

    // 2. Shift all balls left by 1/100 -> right endpoint theta_{N-1} + delta < T_MAX
    let mut shifted_left = valid_cover.clone();
    let shift_left = rq(1, 100);
    for b in &mut shifted_left.balls {
        b.theta = &b.theta - &shift_left;
    }
    match audit_multi_anchor_cover(&shifted_left) {
        Err(ContinuousChainingError::EndpointCoverageViolated { right, t_max, .. }) => {
            assert!(right < t_max);
        }
        other => panic!("Expected EndpointCoverageViolated, got {:?}", other),
    }
}

#[test]
fn test_multi_anchor_negative_control_unanchored_cumulative_travel() {
    // 60 unanchored continuation steps of size 1/1000 from anchor at t = 6/1000
    // Under L = 85/9 and epsilon_base = 37249/90000:
    // When travel reaches 44/1000:
    // degradation = (85/9) * (44/1000) = 37400/90000 > 37249/90000,
    // so net margin = 37249/90000 - 37400/90000 = -151/90000 <= 0.
    let l = lipschitz_bound();
    let eps_base = base_gap();
    let delta = delta_certified();
    let erosion = certified_erosion();
    let anchor_t = rq(6, 1000);

    let mut balls = Vec::new();
    balls.push(MultiAnchorBall {
        index: 0,
        theta: anchor_t.clone(),
        delta: delta.clone(),
        epsilon_base: eps_base.clone(),
        lipschitz: l.clone(),
        margin: certified_margin(),
        is_anchor: true,
    });

    for i in 1..60 {
        let t_val = &anchor_t + rq(i as i64, 1000);
        let travel = rq(i as i64, 1000);
        let eff_base = &eps_base - (&l * &travel);
        let m = if &eff_base > &erosion {
            &eff_base - &erosion
        } else {
            rq(1, 10000000)
        };
        let ball_base = &m + &erosion;
        let b = MultiAnchorBall {
            index: i,
            theta: t_val,
            delta: delta.clone(),
            epsilon_base: ball_base,
            lipschitz: l.clone(),
            margin: m,
            is_anchor: false,
        };
        balls.push(b);
    }

    let res = audit_continuation_chain(
        &balls,
        &t_min_multi_anchor(),
        &t_max_multi_anchor(),
        false, // don't check full domain coverage
        true,  // check adjacent overlap
    );

    match res {
        Err(ContinuousChainingError::CumulativeTravelExhausted { travel, margin }) => {
            assert!(margin <= BigRational::zero());
            assert_eq!(travel, rq(44, 1000));
            assert_eq!(margin, rq(-151, 90000));
        }
        other => panic!("Expected CumulativeTravelExhausted, got {:?}", other),
    }
}

#[test]
fn test_multi_anchor_negative_control_excess_declared_margin() {
    let anchor = MultiAnchorBall {
        index: 0,
        theta: rq(6, 1000),
        delta: delta_certified(),
        epsilon_base: base_gap(),
        lipschitz: lipschitz_bound(),
        margin: certified_margin(),
        is_anchor: true,
    };
    // Unanchored point at travel 1/100 claiming un-degraded margin certified_margin()
    // when propagated margin is base_gap - (85/9)(1/100) - (85/9)(1/1000) < certified_margin()
    let bad_pt = MultiAnchorBall {
        index: 1,
        theta: rq(16, 1000),
        delta: delta_certified(),
        epsilon_base: base_gap(),
        lipschitz: lipschitz_bound(),
        margin: certified_margin(),
        is_anchor: false,
    };

    let res = audit_continuation_chain(
        &[anchor, bad_pt],
        &t_min_multi_anchor(),
        &t_max_multi_anchor(),
        false,
        false,
    );

    match res {
        Err(ContinuousChainingError::CurvatureWallViolation {
            point,
            margin,
            threshold,
        }) => {
            assert_eq!(point, rq(16, 1000));
            assert!(margin > threshold);
        }
        other => panic!("Expected CurvatureWallViolation, got {:?}", other),
    }
}

#[test]
fn test_multi_anchor_negative_control_non_positive_margins() {
    // 1. Constructor rejection of zero base gap
    let res_zero = MultiAnchorBall::new(
        0,
        t_min_multi_anchor(),
        delta_certified(),
        BigRational::zero(),
        lipschitz_bound(),
        true,
    );
    match res_zero {
        Err(ContinuousChainingError::NonPositiveMargin { margin, .. }) => {
            assert!(margin <= BigRational::zero());
        }
        other => panic!("Expected NonPositiveMargin, got {:?}", other),
    }

    // 2. Constructor rejection of negative base gap
    let res_neg = MultiAnchorBall::new(
        0,
        t_min_multi_anchor(),
        delta_certified(),
        rq(-1, 10),
        lipschitz_bound(),
        true,
    );
    assert!(matches!(
        res_neg,
        Err(ContinuousChainingError::NonPositiveMargin { .. })
    ));

    // 3. Auditor rejection of tampered non-positive margin
    let mut cover = build_multi_anchor_covering(250, &delta_certified()).unwrap();
    cover.balls[5].margin = rq(-1, 100);
    assert!(matches!(
        audit_multi_anchor_cover(&cover),
        Err(ContinuousChainingError::NonPositiveMargin { .. })
    ));

    // 4. Auditor rejection of tampered below-certified margin on anchor
    let mut cover_low = build_multi_anchor_covering(250, &delta_certified()).unwrap();
    cover_low.balls[5].margin = rq(1, 10000); // positive, but below certified floor 12133/30000
    assert!(matches!(
        audit_multi_anchor_cover(&cover_low),
        Err(ContinuousChainingError::CurvatureWallViolation { .. })
    ));
}

#[test]
fn test_multi_anchor_gap_probe_uncovered_rejection() {
    // Construct domain [1/50, 59/180], where probe 1/122 ~ 0.00819 < 1/50 = 0.02 is not covered
    let t_min_sub = rq(1, 50);
    let t_max_sub = t_max_multi_anchor();
    let res = build_multi_anchor_covering_domain(250, &delta_certified(), &t_min_sub, &t_max_sub);
    match res {
        Err(ContinuousChainingError::GapProbeNotCovered { probe_t }) => {
            assert_eq!(probe_t, gap_probe_t());
        }
        other => panic!("Expected GapProbeNotCovered, got {:?}", other),
    }
}

#[test]
fn test_multi_anchor_covering_path_bridge() {
    let cover = build_multi_anchor_covering(250, &delta_certified()).unwrap();
    let path = cover.to_chaining_path();

    assert_eq!(path.total_nodes, 250);
    assert!(path.no_gaps);
    assert!(path.all_certified);
    assert_eq!(path.min_margin, certified_margin());

    let cert = verify_curvature_wall_propagation(&path)
        .expect("Curvature wall propagation through MultiAnchorCover bridge failed");
    assert!(cert.curvature_wall_intact);
    assert!(cert.zero_rel_variety_empty);
}
