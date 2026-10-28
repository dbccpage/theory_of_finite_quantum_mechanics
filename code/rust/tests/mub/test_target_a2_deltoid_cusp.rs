//! Integration and unit tests for Target A2 Phase 2: Deltoid Cusp Desingularization.
//!
//! AuthorityEffect: None.

use std::fs;
use std::path::Path;
use syn::visit::Visit;

use num_rational::BigRational;
use num_traits::{One, Signed, Zero};

use engine_kernel::interval::Interval;
use tfqm_mub::native::exact::mub6_constants::delta_crit;
use tfqm_mub::native::exact::mub6_deltoid_cusp::{
    accelerate_blownup_cell_with_network_simplex, attempt_unblown_singular_certification,
    blowup_to_cartesian_cyc24, blowup_to_cartesian_rat, corner_determinant_cyc24,
    corner_determinant_rat, cusp0_segre_point_rat, cusp_segre_point_cyc24, delta_canonical,
    epsilon_cusp, erosion_cusp, evaluate_blownup_gradient_bounds_rat,
    evaluate_condition_number_exceptional_divisor, evaluate_unblown_lipschitz_gradient_rat,
    is_on_segre_variety_cyc24, is_on_segre_variety_rat, lipschitz_proj, margin_cusp,
    solve_desingularized_cusp_bisection, verify_exact_factorization_cyc24,
    verify_exact_factorization_rat, BisectionSolverConfig, DeltoidCusp, DeltoidCuspError,
    ProjectiveBlowupCoords, QPolynomial,
};
use tfqm_mub::native::exact::mub6_firewall::{AUTHORITY_EFFECT, FIREWALL};
use engine_number_theory::cyclotomic::Cyc24;
use engine_number_theory::rational::rq;

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
fn test_ast_zero_float_discipline() {
    let manifest_dir = env!("CARGO_MANIFEST_DIR");
    let target_file = Path::new(manifest_dir)
        .join("src")
        .join("native")
        .join("mub6_deltoid_cusp.rs");

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
        "Target A2 mub6_deltoid_cusp.rs violated zero-float discipline: {:?}",
        visitor.found_floats
    );

    // Also assert verbatim text excludes f32 / f64 tokens
    assert!(
        !source.contains("f32"),
        "mub6_deltoid_cusp.rs must contain zero occurrences of f32"
    );
    assert!(
        !source.contains("f64"),
        "mub6_deltoid_cusp.rs must contain zero occurrences of f64"
    );
}

// ============================================================================
// 2. SEGRE VARIETY LOCUS & CUSP CONFLUENCE
// ============================================================================

#[test]
fn test_segre_variety_definition_and_cusps() {
    // 1. Check Cusp 0 rational basepoint (1, 1, 1, 1)
    let p0 = cusp0_segre_point_rat();
    assert!(is_on_segre_variety_rat(&p0.a, &p0.b, &p0.c, &p0.d));
    assert_eq!(
        corner_determinant_rat(&p0.a, &p0.b, &p0.c, &p0.d),
        BigRational::zero()
    );

    // 2. Check all 3 deltoid cusps in Cyc24:
    // For each cusp theta in {0, 2pi/3, 4pi/3}, point (z, z, z, z) lies on Segre quadric
    for cusp in DeltoidCusp::all() {
        let p_cyc = cusp_segre_point_cyc24(cusp);
        assert!(
            is_on_segre_variety_cyc24(&p_cyc.a, &p_cyc.b, &p_cyc.c, &p_cyc.d),
            "Cusp {:?} must lie on the Segre variety locus in Cyc24",
            cusp
        );
        let det = corner_determinant_cyc24(&p_cyc.a, &p_cyc.b, &p_cyc.c, &p_cyc.d);
        assert_eq!(det, Cyc24::zero());
    }

    // 3. Non-trivial rational points on Segre variety
    let test_triples = [
        (rq(2, 1), rq(3, 1), rq(4, 1)),
        (rq(3, 2), rq(5, 3), rq(7, 5)),
        (rq(-1, 1), rq(2, 1), rq(-3, 1)),
        (rq(1, 3), rq(2, 5), rq(3, 7)),
        (rq(4, 5), rq(6, 7), rq(8, 9)),
    ];

    for (a, b, c) in test_triples {
        let d =
            tfqm_mub::native::exact::mub6_deltoid_cusp::compute_nontrivial_segre_d_rat(&a, &b, &c)
                .expect("d computation must succeed for a != 1");
        assert!(is_on_segre_variety_rat(&a, &b, &c, &d));
        assert_eq!(corner_determinant_rat(&a, &b, &c, &d), BigRational::zero());
    }
}

// ============================================================================
// 3. PROJECTIVE BLOW-UP COORDINATE TRANSFORM & EXACT FACTORIZATION
// ============================================================================

#[test]
fn test_projective_blowup_exact_factorization_rational() {
    let q_poly = QPolynomial::for_cusp(DeltoidCusp::Theta0);

    let test_coords = [
        ProjectiveBlowupCoords::new(rq(1, 1000), rq(0, 1), rq(0, 1)),
        ProjectiveBlowupCoords::new(rq(1, 500), rq(1, 2), rq(-1, 3)),
        ProjectiveBlowupCoords::new(rq(1, 100), rq(-1, 1), rq(1, 1)),
        ProjectiveBlowupCoords::new(rq(3, 250), rq(2, 5), rq(3, 7)),
        ProjectiveBlowupCoords::new(rq(1, 10), rq(-4, 5), rq(-2, 3)),
    ];

    for coords in &test_coords {
        let (a, b, c, d) = blowup_to_cartesian_rat(coords, &q_poly);
        let det = corner_determinant_rat(&a, &b, &c, &d);
        let q_val = q_poly.eval(&coords.u, &coords.v);
        let factored = &coords.r * q_val;

        assert_eq!(
            det, factored,
            "P_corner must equal r * Q(u, v) identically for coords {:?}",
            coords
        );
        assert!(verify_exact_factorization_rat(coords, &q_poly).is_ok());
    }
}

#[test]
fn test_projective_blowup_exact_factorization_cyc24() {
    for cusp in DeltoidCusp::all() {
        let q_poly = QPolynomial::for_cusp(cusp);

        let coords = ProjectiveBlowupCoords::new(rq(1, 200), rq(1, 4), rq(-1, 3));
        let (a, b, c, d) = blowup_to_cartesian_cyc24(&coords, &q_poly);
        let det = corner_determinant_cyc24(&a, &b, &c, &d);
        let q_val = q_poly.eval(&coords.u, &coords.v);
        let factored = Cyc24::rat(&coords.r * q_val);

        assert_eq!(
            det, factored,
            "P_corner in Cyc24 must equal r * Q(u, v) for cusp {:?}",
            cusp
        );
        assert!(verify_exact_factorization_cyc24(&coords, &q_poly).is_ok());
    }
}

// ============================================================================
// 4. CONDITION NUMBER ON EXCEPTIONAL DIVISOR
// ============================================================================

#[test]
fn test_condition_number_exceptional_divisor() {
    for cusp in DeltoidCusp::all() {
        let q_poly = QPolynomial::for_cusp(cusp);

        // Exceptional divisor sector [0, 1/2] x [0, 1/2]
        let u_ival = Interval::new(rq(0, 1), rq(1, 2));
        let v_ival = Interval::new(rq(0, 1), rq(1, 2));

        let report = evaluate_condition_number_exceptional_divisor(&u_ival, &v_ival, &q_poly)
            .expect("Condition number evaluation on sector must succeed");

        assert!(report.is_bounded);
        assert!(report.is_strictly_positive);

        let q_lo: BigRational = report.q_lo.parse().unwrap();
        let q_hi: BigRational = report.q_hi.parse().unwrap();
        let kappa: BigRational = report.condition_number.parse().unwrap();

        assert!(q_lo > BigRational::zero());
        assert!(q_hi >= q_lo);
        assert_eq!(kappa, &q_hi / &q_lo);
        // On [0, 1/2]^2, kappa is small and strictly bounded
        assert!(kappa < rq(3, 1));
    }
}

// ============================================================================
// 5. BOUNDED RECURSION DEPTH OF BISECTION SOLVER AROUND ALL 3 CUSPS
// ============================================================================

#[test]
fn test_desingularized_bisection_all_three_cusps() {
    let config = BisectionSolverConfig::canonical();

    for cusp in DeltoidCusp::all() {
        let report = solve_desingularized_cusp_bisection(cusp, &config)
            .unwrap_or_else(|e| panic!("Bisection failed for cusp {:?}: {:?}", cusp, e));

        assert_eq!(report.cusp, cusp);
        assert!(report.all_cells_certified);
        assert!(report.bounded_depth_guaranteed);
        assert!(
            report.max_depth_reached <= config.max_allowed_depth,
            "Cusp {:?} exceeded max allowed depth {}: reached {}",
            cusp,
            config.max_allowed_depth,
            report.max_depth_reached
        );
        assert!(report.total_leaf_cells > 0);
        assert!(report.all_phi1_positive);

        // Check that every cell satisfies the target condition number <= 3
        for cell in &report.cells {
            let kappa: BigRational = cell.condition_number.parse().unwrap();
            assert!(
                kappa <= config.target_condition_number,
                "Cell {} condition number {} exceeds target {}",
                cell.cell_id,
                kappa,
                config.target_condition_number
            );
            let q_lo: BigRational = cell.q_lo.parse().unwrap();
            assert!(q_lo > BigRational::zero());
            assert!(cell.phi1_objective.is_some());
            assert!(cell.phi1_objective.unwrap() > 0);
        }
    }
}

// ============================================================================
// 6. NETWORK SIMPLEX STRICT POSITIVE CYCLE CIRCULATION PHI_1 > 0
// ============================================================================

#[test]
fn test_network_simplex_phi1_positive_circulation() {
    let r_lo = rq(1, 1000);
    let q_lo = rq(37249, 90000);
    let scale = 90000i128;

    let phi1_sol = accelerate_blownup_cell_with_network_simplex(&r_lo, &q_lo, scale)
        .expect("Network Simplex solve must succeed");

    assert!(
        phi1_sol.objective > 0,
        "Network Simplex circulation Phi_1 objective must be strictly positive, got {}",
        phi1_sol.objective
    );

    // Verify dual potential differences
    assert_eq!(phi1_sol.vertex_potential.len(), 3);
    assert_eq!(phi1_sol.z.len(), 3);
}

// ============================================================================
// 7. NEGATIVE CONTROLS
// ============================================================================

#[test]
fn test_negative_control_unblown_singular_box_rejected() {
    // Unblown singular coordinates cannot be certified within bounded depth
    let res = attempt_unblown_singular_certification(DeltoidCusp::Theta0, 10);
    assert!(
        matches!(res, Err(DeltoidCuspError::RecursionDepthExceeded { .. })),
        "Unblown singular box must fail certification with RecursionDepthExceeded"
    );
}

#[test]
fn test_negative_control_zero_or_negative_radial_rejected() {
    let mut config = BisectionSolverConfig::canonical();
    config.r_min = BigRational::zero();
    let res = solve_desingularized_cusp_bisection(DeltoidCusp::Theta0, &config);
    assert!(
        matches!(res, Err(DeltoidCuspError::InvalidRadialParameter { .. })),
        "Zero r_min must be rejected"
    );

    config.r_min = rq(-1, 100);
    let res2 = solve_desingularized_cusp_bisection(DeltoidCusp::Theta0, &config);
    assert!(
        matches!(res2, Err(DeltoidCuspError::InvalidRadialParameter { .. })),
        "Negative r_min must be rejected"
    );
}

#[test]
fn test_negative_control_mutated_negative_q_rejected() {
    // Mutated Q polynomial with negative base gap
    let mutated_q = QPolynomial {
        c_base: rq(-1, 2),
        c_u: BigRational::zero(),
        c_v: BigRational::zero(),
        c_u2: BigRational::one(),
        c_v2: BigRational::one(),
    };

    let u_ival = Interval::new(rq(0, 1), rq(1, 10));
    let v_ival = Interval::new(rq(0, 1), rq(1, 10));

    let res = evaluate_condition_number_exceptional_divisor(&u_ival, &v_ival, &mutated_q);
    assert!(
        res.is_err(),
        "Mutated negative Q polynomial must fail exceptional divisor condition evaluation"
    );
}

#[test]
fn test_negative_control_off_variety_perturbation_phi1() {
    // On Segre variety: det = 0.
    // Perturbing d by delta produces det = delta and Phi_1 = |det| > 0 via Network Simplex
    let delta = rq(1, 10);
    let scale = 90000i128;
    let r_lo = BigRational::one();
    let q_lo = delta.clone();

    let sol = accelerate_blownup_cell_with_network_simplex(&r_lo, &q_lo, scale)
        .expect("Solve must succeed");

    assert!(
        sol.objective > 0,
        "Off-variety perturbation must produce positive circulation Phi_1 > 0"
    );
}

#[test]
fn test_claim_hygiene_constants() {
    assert_eq!(AUTHORITY_EFFECT, "None");
    assert_eq!(
        FIREWALL,
        "stated region only; mints no authority"
    );
    // Explicitly verify the firewall assertion
    assert!(!FIREWALL.contains("MUB(6) = 3"));
    assert!(!FIREWALL.contains("MUB(6) <= 3"));
}

#[test]
fn test_canonical_parameters_exact_values() {
    let eps = epsilon_cusp();
    let l = lipschitz_proj();
    let d_cert = delta_canonical();
    let d_crit = delta_crit();
    let erosion = erosion_cusp();
    let margin = margin_cusp();

    // 1. Exact parameter equality matching Lean 4 and Python
    assert_eq!(eps, rq(37249, 90000));
    assert_eq!(l, rq(85, 9));
    assert_eq!(d_cert, rq(1, 1000));
    assert_eq!(d_crit, rq(37249, 850000));
    assert_eq!(erosion, rq(17, 1800));
    assert_eq!(margin, rq(12133, 30000));

    // 2. Erosion formula: L_proj * delta = 17 / 1800
    assert_eq!(&l * &d_cert, erosion);

    // 3. Margin formula: eps - erosion = 12133 / 30000
    assert_eq!(&eps - &erosion, margin);
    assert!(margin > BigRational::zero());

    // 4. Critical delta threshold: delta < delta_crit
    assert!(d_cert < d_crit);
    assert_eq!(&eps / &l, d_crit);
}

#[test]
fn test_unblown_gradient_divergence_and_blownup_bound() {
    // In unblown coordinates d(a, b, c) = 1 + (b-1)(c-1)/(a-1):
    // Gradient diverges as a -> 1
    let b = rq(3, 2);
    let c = rq(5, 4);

    let grad_at_1 = evaluate_unblown_lipschitz_gradient_rat(&BigRational::one(), &b, &c);
    assert!(
        grad_at_1.is_err(),
        "Evaluating unblown gradient at a = 1 must fail due to zero denominator"
    );

    // As a approaches 1, |dd/da| grows without bound
    let a_close_1 = rq(1001, 1000); // a - 1 = 1/1000
    let (dd_da_1, _, _) = evaluate_unblown_lipschitz_gradient_rat(&a_close_1, &b, &c).unwrap();
    // dd_da = -(1/2 * 1/4) / (1/1000)^2 = -(1/8) * 1_000_000 = -125_000
    assert_eq!(dd_da_1, rq(-125000, 1));

    let a_close_2 = rq(10001, 10000); // a - 1 = 1/10000
    let (dd_da_2, _, _) = evaluate_unblown_lipschitz_gradient_rat(&a_close_2, &b, &c).unwrap();
    // dd_da = -(1/8) * 100_000_000 = -12_500_000
    assert_eq!(dd_da_2, rq(-12500000, 1));

    // In contrast, blown-up gradient bounds are uniformly bounded:
    let coords = ProjectiveBlowupCoords::new(rq(1, 1000), rq(1, 2), rq(1, 4));
    let q = rq(37249, 90000);
    let (dd_du, dd_dv, dd_dr) = evaluate_blownup_gradient_bounds_rat(&coords, &q);

    // All derivatives bounded by small constants
    assert_eq!(dd_du, rq(1, 4000));
    assert_eq!(dd_dv, rq(1, 2000));
    assert_eq!(dd_dr, rq(1, 8) + rq(37249, 90000));
    assert!(dd_du.abs() < BigRational::one());
    assert!(dd_dv.abs() < BigRational::one());
    assert!(dd_dr.abs() < BigRational::from_integer(2.into()));
}
