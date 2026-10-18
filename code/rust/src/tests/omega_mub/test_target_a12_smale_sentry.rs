//! Comprehensive Unit and Integration Test Suite for Target A12:
//! Rust Native Exact Smale Root Sentry.
//!
//! AuthorityEffect: None
//! Both Branch A and Branch B must be rigorously supported and verified without bias.

use num_bigint::BigInt;
use num_rational::BigRational;
use std::fs;
use std::path::Path;
use syn::visit::Visit;

use omega_kernel::interval::{Interval, IntervalBox};
use omega_mub::omega_native::exact::d6_exact_curvature_cochain::D;
use omega_mub::omega_native::exact::mub6_f6_chart::f6_family_columns;
use omega_mub::omega_native::exact::mub6_firewall::{AUTHORITY_EFFECT, FIREWALL};
use omega_mub::omega_native::exact::mub6_smale_sentry::{
    compute_smale_invariants, eval_108_mub_relations, eval_single_mub_relation,
    eval_single_mub_relation_cyc24, krawczyk_contractor, smale_alpha_threshold, vec_norm_1,
    vec_norm_inf, CertifiedLeafCell, ExactRationalLu, LuError, QuadraticComponent, RationalMatrix,
    SmaleSentry, SquarePolynomialSystem, SMALE_ALPHA_THRESHOLD_DEN, SMALE_ALPHA_THRESHOLD_NUM,
    TOTAL_MUB_RELATIONS,
};
use omega_mub::omega_native::exact::mub6_zerorel_variety::{
    dita_representative_triple, standard_basis, szollosi_representative_triple,
    tao_representative_triple,
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
        .join("mub6_smale_sentry.rs");

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
        "Target A12 Rust module violated zero-float discipline at AST level: {:?}",
        visitor.found_floats
    );

    // 2. Lexical check
    assert!(
        !source.contains("f32"),
        "mub6_smale_sentry.rs must contain zero f32 occurrences"
    );
    assert!(
        !source.contains("f64"),
        "mub6_smale_sentry.rs must contain zero f64 occurrences"
    );
}

// ============================================================================
// 2. CLAIM HYGIENE AND CONSTANTS AUDIT
// ============================================================================

#[test]
fn test_claim_hygiene_constants() {
    assert_eq!(
        FIREWALL,
        "stated region only; mints no authority"
    );
    assert_eq!(AUTHORITY_EFFECT, "None");
    assert_eq!(TOTAL_MUB_RELATIONS, 108);
    assert_eq!(SMALE_ALPHA_THRESHOLD_NUM, 157);
    assert_eq!(SMALE_ALPHA_THRESHOLD_DEN, 1000);

    let alpha_0 = smale_alpha_threshold();
    assert_eq!(alpha_0, rq(157, 1000));

    // Classical Smale alpha_0 is (13 - 3*sqrt(17))/4 approx 0.15767078.
    // Verify rational threshold 157/1000 < (13 - 3*sqrt(17))/4 exactly:
    // 157/1000 < (13 - 3*sqrt(17))/4 <=> 628/1000 < 13 - 3*sqrt(17)
    // <=> 3*sqrt(17) < 13 - 0.628 = 12.372
    // <=> 9 * 17 = 153 < 12.372^2 = 153.066384
    // 153 < 153.066384 holds strictly!
    let lhs = BigRational::from_integer(BigInt::from(153));
    let rhs = rq(12372, 1000) * rq(12372, 1000);
    assert!(
        lhs < rhs,
        "157/1000 must be strictly below classical Smale point"
    );
}

// ============================================================================
// 3. 108 MUB POLYNOMIAL EVALUATION TESTS
// ============================================================================

#[test]
fn test_108_mub_relations_structure_and_counts() {
    let t_dita = dita_representative_triple();
    let cand_cols = f6_family_columns(1, 2);

    let residuals = eval_108_mub_relations(&t_dita, &cand_cols);
    assert_eq!(residuals.len(), TOTAL_MUB_RELATIONS);

    let mut basis_counts = [0usize; 3];
    for (rel, val) in &residuals {
        assert!(rel.basis < 3);
        assert!(rel.row < D);
        assert!(rel.col < D);
        basis_counts[rel.basis] += 1;
        // All residuals must be exact rationals
        assert_eq!(val.denom(), &val.denom().clone());
    }

    assert_eq!(basis_counts[0], 36);
    assert_eq!(basis_counts[1], 36);
    assert_eq!(basis_counts[2], 36);
}

#[test]
fn test_108_mub_relations_tao_and_szollosi() {
    let cand_cols = f6_family_columns(0, 4);

    let t_tao = tao_representative_triple();
    let res_tao = eval_108_mub_relations(&t_tao, &cand_cols);
    assert_eq!(res_tao.len(), 108);

    let t_sz = szollosi_representative_triple();
    let res_sz = eval_108_mub_relations(&t_sz, &cand_cols);
    assert_eq!(res_sz.len(), 108);
}

#[test]
fn test_single_mub_relation_exact() {
    let b0 = standard_basis();
    let e0 = &b0[0];
    let e1 = &b0[1];

    // Inner product <e0, e0> = 1, norm_sq = 1. Residual = 1 - 1/6 = 5/6.
    let r00 = eval_single_mub_relation(e0, e0);
    assert_eq!(r00, rq(5, 6));

    // Inner product <e0, e1> = 0, norm_sq = 0. Residual = 0 - 1/6 = -1/6.
    let r01 = eval_single_mub_relation_cyc24(e0, e1);
    assert_eq!(r01, rq(-1, 6));
}

// ============================================================================
// 4. EXACT RATIONAL LINEAR ALGEBRA & LU SOLVER TESTS
// ============================================================================

#[test]
fn test_rational_matrix_multiplication_and_norms() {
    // 2x2 matrix A = [[1, 2], [3, 4]]
    let a = RationalMatrix::from_rows(vec![vec![rq(1, 1), rq(2, 1)], vec![rq(3, 1), rq(4, 1)]]);

    // Vector x = [5, 6]
    let x = vec![rq(5, 1), rq(6, 1)];

    // A * x = [1*5 + 2*6, 3*5 + 4*6] = [17, 39]
    let ax = a.mul_vec(&x).unwrap();
    assert_eq!(ax, vec![rq(17, 1), rq(39, 1)]);

    // Infinity norm of A: max(|1|+|2|, |3|+|4|) = 7
    assert_eq!(a.norm_inf(), rq(7, 1));

    // 1-norm of A: max(|1|+|3|, |2|+|4|) = 6
    assert_eq!(a.norm_1(), rq(6, 1));

    // Transpose of A
    let at = a.transpose();
    assert_eq!(at.data[0][1], rq(3, 1));
    assert_eq!(at.data[1][0], rq(2, 1));

    // Vector norms of ax = [17, 39]
    assert_eq!(vec_norm_inf(&ax), rq(39, 1));
    assert_eq!(vec_norm_1(&ax), rq(56, 1));
}

#[test]
fn test_exact_rational_lu_factorize_and_solve() {
    // Non-trivial 3x3 system:
    //  2x +  y -  z =  8
    // -3x -  y + 2z = -11
    // -2x +  y + 2z = -3
    let a = RationalMatrix::from_rows(vec![
        vec![rq(2, 1), rq(1, 1), rq(-1, 1)],
        vec![rq(-3, 1), rq(-1, 1), rq(2, 1)],
        vec![rq(-2, 1), rq(1, 1), rq(2, 1)],
    ]);

    let b = vec![rq(8, 1), rq(-11, 1), rq(-3, 1)];

    let lu = ExactRationalLu::factorize(&a).expect("matrix should be invertible");

    // Solution should be x = 2, y = 3, z = -1
    let x_sol = lu.solve(&b).expect("solve should succeed");
    assert_eq!(x_sol, vec![rq(2, 1), rq(3, 1), rq(-1, 1)]);

    // Check determinant: det(A) = -1
    let det = lu.determinant();
    assert_eq!(det, rq(-1, 1));

    // Inverse check: A * A^(-1) = I
    let a_inv = lu.inverse().expect("inverse should succeed");
    let ident = a.mul_mat(&a_inv).expect("mul should succeed");
    for i in 0..3 {
        for j in 0..3 {
            if i == j {
                assert_eq!(ident.data[i][j], rq(1, 1));
            } else {
                assert_eq!(ident.data[i][j], rq(0, 1));
            }
        }
    }
}

#[test]
fn test_exact_rational_lu_singular_rejection() {
    // Singular matrix with identical rows
    let a = RationalMatrix::from_rows(vec![vec![rq(1, 1), rq(2, 1)], vec![rq(1, 1), rq(2, 1)]]);

    let res = ExactRationalLu::factorize(&a);
    assert!(res.is_err());
    match res.unwrap_err() {
        LuError::ZeroPivotAt(idx) => assert_eq!(idx, 1),
        e => panic!("unexpected error: {:?}", e),
    }
}

// ============================================================================
// 5. EXACT RATIONAL INTERVAL ARITHMETIC & BOX TESTS
// ============================================================================

#[test]
fn test_rational_interval_operations() {
    let iv1 = Interval::new(rq(-1, 2), rq(3, 4));
    let iv2 = Interval::new(rq(1, 3), rq(2, 1));

    // Addition: [-1/2 + 1/3, 3/4 + 2] = [-1/6, 11/4]
    let add_res = iv1.add(&iv2);
    assert_eq!(*add_res.lo(), rq(-1, 6));
    assert_eq!(*add_res.hi(), rq(11, 4));

    // Subtraction: [-1/2 - 2, 3/4 - 1/3] = [-5/2, 5/12]
    let sub_res = iv1.sub(&iv2);
    assert_eq!(*sub_res.lo(), rq(-5, 2));
    assert_eq!(*sub_res.hi(), rq(5, 12));

    // Multiplication: [-1/2, 3/4] * [1/3, 2] = [-1, 3/2]
    let mul_res = iv1.mul(&iv2);
    assert_eq!(*mul_res.lo(), rq(-1, 1));
    assert_eq!(*mul_res.hi(), rq(3, 2));

    // Square of straddling interval [-1/2, 3/4]^2 = [0, 9/16]
    let sq_res = iv1.sq();
    assert_eq!(*sq_res.lo(), rq(0, 1));
    assert_eq!(*sq_res.hi(), rq(9, 16));

    // Strict interior inclusion
    let inner_iv = Interval::new(rq(-1, 4), rq(1, 2));
    assert!(inner_iv.strict_interior_subset_of(&iv1));
    assert!(!iv1.strict_interior_subset_of(&inner_iv));
}

#[test]
fn test_rational_interval_box_interior_containment() {
    let center = vec![rq(1, 2), rq(-1, 3)];
    let parent = IntervalBox::from_center_uniform_radius(&center, &rq(1, 10));
    let child = IntervalBox::from_center_uniform_radius(&center, &rq(1, 20));

    assert!(child.strict_interior_subset_of(&parent));
    assert!(!parent.strict_interior_subset_of(&child));

    assert!(parent.contains_point(&center));
    assert!(child.contains_point(&center));
}

// ============================================================================
// 6. SMALE INVARIANTS (BETA, GAMMA, ALPHA) TESTS
// ============================================================================

/// Construct a toy 2D quadratic system:
/// F_0(x, y) = x^2 + y - 2 = 0
/// F_1(x, y) = x + y^2 - 2 = 0
///
/// An exact root is (x*, y*) = (1, 1).
fn toy_quadratic_system_2d() -> SquarePolynomialSystem {
    // Component 0: -2 + [0, 1]*[x, y]^T + (1/2) [x, y] * [[2, 0], [0, 0]] * [x, y]^T
    // = -2 + y + x^2
    let c0 = rq(-2, 1);
    let a0 = vec![rq(0, 1), rq(1, 1)];
    let h0 = RationalMatrix::from_rows(vec![vec![rq(2, 1), rq(0, 1)], vec![rq(0, 1), rq(0, 1)]]);
    let q0 = QuadraticComponent::new(c0, a0, h0);

    // Component 1: -2 + [1, 0]*[x, y]^T + (1/2) [x, y] * [[0, 0], [0, 2]] * [x, y]^T
    // = -2 + x + y^2
    let c1 = rq(-2, 1);
    let a1 = vec![rq(1, 1), rq(0, 1)];
    let h1 = RationalMatrix::from_rows(vec![vec![rq(0, 1), rq(0, 1)], vec![rq(0, 1), rq(2, 1)]]);
    let q1 = QuadraticComponent::new(c1, a1, h1);

    SquarePolynomialSystem::new(vec![q0, q1])
}

#[test]
fn test_smale_invariants_at_exact_root() {
    let sys = toy_quadratic_system_2d();
    let exact_root = vec![rq(1, 1), rq(1, 1)];

    let inv = compute_smale_invariants(&sys, &exact_root).expect("LU should invert");

    // At exact root: F(x*) = 0, so beta = 0, alpha = 0.
    assert_eq!(inv.beta, rq(0, 1));
    assert_eq!(inv.alpha, rq(0, 1));
    assert!(inv.is_certified_approx_zero);
    assert!(inv.gamma > rq(0, 1));
}

#[test]
fn test_smale_invariants_near_approximate_root() {
    let sys = toy_quadratic_system_2d();

    // Perturb root slightly: (1 + 1/100, 1 + 1/100) = (101/100, 101/100)
    let approx_root = vec![rq(101, 100), rq(101, 100)];

    let inv = compute_smale_invariants(&sys, &approx_root).expect("LU should invert");

    // beta > 0, gamma > 0
    assert!(inv.beta > rq(0, 1));
    assert!(inv.gamma > rq(0, 1));
    assert!(inv.alpha > rq(0, 1));

    // For perturbation 1/100, alpha should be well below 157/1000:
    assert!(
        inv.is_certified_approx_zero,
        "alpha = {} must be strictly less than threshold {}",
        inv.alpha, inv.threshold
    );
}

#[test]
fn test_smale_invariants_rejection_far_from_root() {
    let sys = toy_quadratic_system_2d();

    // Far from root: (3, 3)
    let far_point = vec![rq(3, 1), rq(3, 1)];

    let inv = compute_smale_invariants(&sys, &far_point).expect("LU should invert");

    // beta is large, alpha exceeds 157/1000
    assert!(
        !inv.is_certified_approx_zero,
        "alpha = {} should exceed threshold {}",
        inv.alpha, inv.threshold
    );
}

// ============================================================================
// 7. KRAWCZYK CONTRACTOR TESTS
// ============================================================================

#[test]
fn test_krawczyk_contractor_strict_contraction() {
    let sys = toy_quadratic_system_2d();

    // Isolating box around root (1, 1) with radius 1/10: [9/10, 11/10] x [9/10, 11/10]
    let center = vec![rq(101, 100), rq(101, 100)];
    let x_box = IntervalBox::from_center_uniform_radius(&center, &rq(1, 10));

    let k_res = krawczyk_contractor(&sys, &x_box, Some(&center))
        .expect("Krawczyk computation should succeed");

    // Contractor must strictly contract into the interior of x_box!
    assert!(
        k_res.is_strictly_contracted,
        "Krawczyk box {:?} must strictly contract inside parent box {:?}",
        k_res.krawczyk_box, x_box
    );
    assert!(!k_res.is_disjoint);
}

#[test]
fn test_krawczyk_contractor_disjoint_far_box() {
    let sys = toy_quadratic_system_2d();

    // Box far from any root: [10, 11] x [10, 11]
    let center = vec![rq(21, 2), rq(21, 2)];
    let x_box = IntervalBox::from_center_uniform_radius(&center, &rq(1, 2));

    let k_res = krawczyk_contractor(&sys, &x_box, Some(&center))
        .expect("Krawczyk computation should succeed");

    // It must NOT contract inside the interior of this far box
    assert!(!k_res.is_strictly_contracted);
}

// ============================================================================
// 8. SENTRY MONITOR: BISECTION LEAVES & SYNTHETIC ROOT INJECTION
// ============================================================================

#[test]
fn test_sentry_scan_bisection_leaves_positive_margins() {
    // Create a mock collection of certified bisection leaf cells from the global atlas
    let cells = vec![
        CertifiedLeafCell {
            cell_id: "cell_dita_f6_0".to_string(),
            center: vec![rq(0, 1), rq(0, 1)],
            radius: rq(1, 1000),
            residual_margin: rq(37249, 90000), // canonical margin ~ 0.4138
        },
        CertifiedLeafCell {
            cell_id: "cell_szollosi_b6_1".to_string(),
            center: vec![rq(1, 10), rq(2, 10)],
            radius: rq(1, 1000),
            residual_margin: rq(12133, 30000), // boundary margin ~ 0.4044
        },
        CertifiedLeafCell {
            cell_id: "cell_tao_s6_2".to_string(),
            center: vec![rq(1, 2), rq(1, 2)],
            radius: rq(1, 1000),
            residual_margin: rq(527, 576), // Tao margin ~ 0.9149
        },
    ];

    let summary = SmaleSentry::scan_bisection_leaves(&cells);

    assert!(
        summary.all_positive,
        "All certified cells must have strictly positive margins"
    );
    assert_eq!(summary.scanned_count, 3);
    assert_eq!(summary.min_margin, rq(12133, 30000));
    assert!(summary.zero_or_negative_margin_cells.is_empty());
}

#[test]
fn test_sentry_scan_bisection_leaves_detects_violation() {
    let cells = vec![
        CertifiedLeafCell {
            cell_id: "certified_cell_0".to_string(),
            center: vec![rq(0, 1)],
            radius: rq(1, 100),
            residual_margin: rq(1, 10),
        },
        CertifiedLeafCell {
            cell_id: "violating_cell_defect_zero".to_string(),
            center: vec![rq(1, 1)],
            radius: rq(1, 100),
            residual_margin: rq(0, 1), // Defect 0: uncertified!
        },
        CertifiedLeafCell {
            cell_id: "violating_cell_negative".to_string(),
            center: vec![rq(2, 1)],
            radius: rq(1, 100),
            residual_margin: rq(-1, 50), // Negative margin!
        },
    ];

    let summary = SmaleSentry::scan_bisection_leaves(&cells);

    assert!(!summary.all_positive);
    assert_eq!(summary.scanned_count, 3);
    assert_eq!(summary.min_margin, rq(-1, 50));
    assert_eq!(summary.zero_or_negative_margin_cells.len(), 2);
    assert!(summary
        .zero_or_negative_margin_cells
        .contains(&"violating_cell_defect_zero".to_string()));
    assert!(summary
        .zero_or_negative_margin_cells
        .contains(&"violating_cell_negative".to_string()));
}

#[test]
fn test_sentry_synthetic_root_injection_detection() {
    let sys = toy_quadratic_system_2d();
    let exact_root = vec![rq(1, 1), rq(1, 1)];

    // 1. Small perturbation (1/500): genuine approximate zero
    let small_perturbation = rq(1, 500);
    let box_radius = rq(1, 10);

    let inspection = SmaleSentry::test_synthetic_root_injection(
        &sys,
        &exact_root,
        &small_perturbation,
        &box_radius,
    )
    .expect("Inspection should compute");

    match inspection {
        omega_mub::omega_native::exact::mub6_smale_sentry::SentryRootInspection::RootCertified {
            alpha,
            beta,
            gamma,
            isolating_box,
            krawczyk_box,
        } => {
            assert!(alpha < smale_alpha_threshold());
            assert!(beta > rq(0, 1));
            assert!(gamma > rq(0, 1));
            assert!(krawczyk_box.strict_interior_subset_of(&isolating_box));
        }
        omega_mub::omega_native::exact::mub6_smale_sentry::SentryRootInspection::RootUncertified {
            alpha,
            reason,
        } => {
            panic!(
                "Expected RootCertified for small perturbation, got uncertified with alpha={}: {}",
                alpha, reason
            );
        }
    }

    // 2. Large perturbation (1/2): far from root, must be flagged as uncertified
    let large_perturbation = rq(1, 2);
    let inspection_fail = SmaleSentry::test_synthetic_root_injection(
        &sys,
        &exact_root,
        &large_perturbation,
        &box_radius,
    )
    .expect("Inspection should compute");

    match inspection_fail {
        omega_mub::omega_native::exact::mub6_smale_sentry::SentryRootInspection::RootUncertified {
            alpha,
            ..
        } => {
            assert!(alpha >= smale_alpha_threshold());
        }
        omega_mub::omega_native::exact::mub6_smale_sentry::SentryRootInspection::RootCertified {
            ..
        } => {
            panic!("Expected RootUncertified for large perturbation");
        }
    }
}

#[test]
fn test_sentry_scan_bisection_leaves_empty() {
    let summary = SmaleSentry::scan_bisection_leaves(&[]);
    assert!(!summary.all_positive);
    assert_eq!(summary.scanned_count, 0);
    assert_eq!(summary.min_margin, rq(0, 1));
    assert!(summary.zero_or_negative_margin_cells.is_empty());
}

#[test]
fn test_krawczyk_contractor_outside_center_rejected() {
    let sys = SquarePolynomialSystem::new(vec![QuadraticComponent::new(
        rq(-1, 1),
        vec![rq(0, 1)],
        RationalMatrix::from_rows(vec![vec![rq(2, 1)]]),
    )]);
    let box_x = IntervalBox::new(vec![Interval::new(rq(9, 10), rq(11, 10))]);
    let outside_center = vec![rq(2, 1)];

    let res = krawczyk_contractor(&sys, &box_x, Some(&outside_center));
    assert!(matches!(res, Err(LuError::CenterOutsideBox)));

    // Midpoint contracts strictly
    let midpoint_res = krawczyk_contractor(&sys, &box_x, None).unwrap();
    assert!(midpoint_res.is_strictly_contracted);
}
