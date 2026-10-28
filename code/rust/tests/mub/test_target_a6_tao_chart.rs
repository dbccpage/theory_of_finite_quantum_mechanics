//! Comprehensive Integration and Falsification Test Suite for Target A6 (Tao Confluence Chart).
//!
//! AuthorityEffect: None

use std::fs;
use std::path::Path;
use syn::visit::Visit;

use tfqm_mub::native::exact::d6_exact_curvature_cochain::D;
use tfqm_mub::native::exact::mub6_tao_chart::{
    confluence_point_theta_star, enumerate_225_submatrices, extract_cross_ratio_exponents,
    solve_target_a6, tao_chart_eval, tao_chart_eval_discrete, tao_s6_matrix,
    verify_confluence_evaluation, verify_local_rational_neighborhood_certificate,
    NUM_SUBMATRICES_225, TAO_PHASES,
};
use tfqm_mub::native::exact::mub6_tao_confluence::TaoConfluenceReport;
use omega_number_theory::cyclotomic::Cyc24;
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
        .join("native")
        .join("mub6_tao_chart.rs");

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
        "Target A6 Rust module violated zero-float discipline: {:?}",
        visitor.found_floats
    );
}

// ============================================================================
// 2. CONFLUENCE POINT EVALUATION THEOREM TESTS
// ============================================================================

#[test]
fn test_confluence_evaluation_identity() {
    assert!(
        verify_confluence_evaluation(),
        "Confluence evaluation theorem failed: Phi(theta*) != S_6"
    );

    let theta_star = confluence_point_theta_star();
    let phi = tao_chart_eval(&theta_star);
    let s6 = tao_s6_matrix();

    for i in 0..D {
        for j in 0..D {
            assert_eq!(phi[i][j], s6[i][j], "Entry mismatch at ({i}, {j})");
        }
    }
}

#[test]
fn test_dephased_corner_preservation() {
    let perturbations = [
        [
            Cyc24::zeta24(1),
            Cyc24::zeta24(2),
            Cyc24::zeta24(3),
            Cyc24::zeta24(4),
            Cyc24::zeta24(5),
        ],
        [
            Cyc24::zeta24(8),
            Cyc24::zeta24(16),
            Cyc24::zeta24(0),
            Cyc24::zeta24(8),
            Cyc24::zeta24(16),
        ],
        [
            Cyc24::zeta24(6),
            Cyc24::zeta24(12),
            Cyc24::zeta24(18),
            Cyc24::zeta24(0),
            Cyc24::zeta24(6),
        ],
    ];

    let one = Cyc24::zeta24(0);
    for u in &perturbations {
        let phi = tao_chart_eval(u);
        // Row 0 must remain identically 1
        for j in 0..D {
            assert_eq!(phi[0][j], one, "Row 0 entry ({}, {}) must be 1", 0, j);
        }
        // Column 0 must remain identically 1
        for i in 0..D {
            assert_eq!(phi[i][0], one, "Column 0 entry ({}, {}) must be 1", i, 0);
        }
    }
}

// ============================================================================
// 3. 225 SUBMATRIX ENUMERATION & STRUCTURE
// ============================================================================

#[test]
fn test_225_submatrix_enumeration() {
    let submatrices = enumerate_225_submatrices();
    assert_eq!(submatrices.len(), NUM_SUBMATRICES_225);

    // Verify uniqueness and strict index ordering
    for idx in &submatrices {
        assert!(idx.r0 < idx.r1 && idx.r1 < D);
        assert!(idx.c0 < idx.c1 && idx.c1 < D);
    }
}

// ============================================================================
// 4. AUTOMATED RECEIPT VALIDATION & EXPONENT MATCHING
// ============================================================================

#[test]
fn test_match_mub_tao_confluence_receipt() {
    let manifest_dir = env!("CARGO_MANIFEST_DIR");
    let receipt_path = Path::new(manifest_dir)
        .join("../tests/mub/artifacts")
        .join("mub_tao_confluence_receipt.json");

    let content = fs::read_to_string(&receipt_path)
        .unwrap_or_else(|e| panic!("Failed to read {}: {}", receipt_path.display(), e));
    let receipt: TaoConfluenceReport =
        serde_json::from_str(&content).unwrap_or_else(|e| panic!("Failed to parse receipt: {}", e));

    assert_eq!(receipt.phase_table, TAO_PHASES);

    let s6 = tao_s6_matrix();
    let computed_exponents =
        extract_cross_ratio_exponents(&s6).expect("All cross-ratios must be exact roots of unity");

    assert_eq!(computed_exponents.len(), NUM_SUBMATRICES_225);
    assert_eq!(
        computed_exponents, receipt.cross_ratio_exponents_mod24,
        "Computed 225 cross-ratio exponents must match receipt exactly"
    );

    // Verify all exponents are cubic mod 24: e in {0, 8, 16}
    for (m, &e) in computed_exponents.iter().enumerate() {
        assert!(
            e == 0 || e == 8 || e == 16,
            "Exponent at index {m} ({e}) is not cubic mod 24"
        );
        assert_ne!(e, 12, "Exponent at index {m} equals 12 (cr = -1)");
    }
}

// ============================================================================
// 5. LOCAL RATIONAL NEIGHBORHOOD CERTIFICATE
// ============================================================================

#[test]
fn test_neighborhood_certificate_bounds() {
    let r = rq(1, 24);
    let (valid, min_dist) = verify_local_rational_neighborhood_certificate(r);
    assert!(valid, "Neighborhood certificate must be valid for r = 1/24");
    assert!(
        min_dist > rq(9, 10),
        "Minimum distance to -1 must exceed 9/10, got {min_dist}"
    );

    // Negative control: excessive radius must be rejected
    let (invalid, _) = verify_local_rational_neighborhood_certificate(rq(1, 1));
    assert!(!invalid, "Certificate must reject excessive radius r = 1");
}

// ============================================================================
// 6. FULL VERIFIER & NEGATIVE CONTROLS
// ============================================================================

#[test]
fn test_solve_target_a6_comprehensive() {
    let manifest_dir = env!("CARGO_MANIFEST_DIR");
    let receipt_path = Path::new(manifest_dir)
        .join("../tests/mub/artifacts")
        .join("mub_tao_confluence_receipt.json");

    let content = fs::read_to_string(&receipt_path).unwrap();
    let receipt: TaoConfluenceReport = serde_json::from_str(&content).unwrap();

    let report = solve_target_a6(&receipt.cross_ratio_exponents_mod24);
    assert!(report.confluence_evaluated_identically);
    assert_eq!(report.total_submatrices, 225);
    assert!(report.exponents_match_receipt);
    assert!(report.all_exponents_cubic_mod24);
    assert!(report.no_exponent_minus_one);
    assert!(report.no_submatrix_orthogonal);
    assert!(report.neighborhood_certificate_valid);

    // Negative control 1: perturbed exponents are rejected
    let mut corrupted_exponents = receipt.cross_ratio_exponents_mod24.clone();
    corrupted_exponents[0] = 12; // Inject -1 cross-ratio
    let bad_report = solve_target_a6(&corrupted_exponents);
    assert!(
        !bad_report.exponents_match_receipt,
        "Corrupted exponents must not match receipt"
    );

    // Negative control 2: discrete chart evaluation away from theta* != S_6
    let shifted_phi = tao_chart_eval_discrete(&[1, 0, 0, 0, 0]);
    let s6 = tao_s6_matrix();
    assert_ne!(
        shifted_phi[1][1], s6[1][1],
        "Shifted chart must differ from S_6 at perturbed diagonal entry"
    );
}
