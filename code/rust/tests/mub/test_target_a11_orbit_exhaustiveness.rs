//! Comprehensive Unit and Integration Test Suite for Target A11:
//! Rust Native Invariant Orbit Classifier & Catalog Certifier.
//!
//! AuthorityEffect: None.

use std::fs;
use std::path::Path;
use syn::visit::Visit;

use tfqm_mub::native::exact::d6_exact_curvature_cochain::D;
use tfqm_mub::native::exact::mub6_firewall::{AUTHORITY_EFFECT, FIREWALL};
use tfqm_mub::native::exact::mub6_haagerup::haagerup_h6_matrix;
use tfqm_mub::native::exact::mub6_matrix6::matrix_zero;
use tfqm_mub::native::exact::mub6_orbit_exhaustiveness::{
    canonical_catalog_candidates, certify_catalog_exhaustiveness, classify_orbit,
    corner_determinant, enumerate_225_submatrices, extract_szollosi_theta_approx,
    fourier_vanishing_test, has_affine_fourier_submatrix_condition, pi_approx, standard_fourier_f6,
    CrossRatioSpectrum, OrbitClass, NUM_SUBMATRICES_225,
};
use tfqm_mub::native::exact::mub6_tao_chart::tao_s6_matrix;
use tfqm_mub::native::exact::szollosi_triad_solver::szollosi_dephased_b6;
use omega_number_theory::cyclotomic::Cyc24;
use omega_number_theory::rational::ri;
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
        .join("mub6_orbit_exhaustiveness.rs");

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
        "Target A11 Rust module violated zero-float discipline at AST level: {:?}",
        visitor.found_floats
    );

    // 2. Lexical check
    assert!(
        !source.contains("f32"),
        "mub6_orbit_exhaustiveness.rs must contain zero f32 occurrences"
    );
    assert!(
        !source.contains("f64"),
        "mub6_orbit_exhaustiveness.rs must contain zero f64 occurrences"
    );
}

// ============================================================================
// 2. EXACT 225 SUBMATRIX INDEX & INVARIANT SPECTRUM EVALUATION
// ============================================================================

#[test]
fn test_225_submatrix_enumeration_and_ordering() {
    let submatrices = enumerate_225_submatrices();
    assert_eq!(submatrices.len(), NUM_SUBMATRICES_225);

    // Verify uniqueness and strict index ordering
    for (i, idx) in submatrices.iter().enumerate() {
        assert!(idx.r0 < idx.r1 && idx.r1 < D, "Row ordering failure at {i}");
        assert!(idx.c0 < idx.c1 && idx.c1 < D, "Col ordering failure at {i}");

        if i > 0 {
            let prev = &submatrices[i - 1];
            assert!(
                (prev.r0, prev.r1, prev.c0, prev.c1) < (idx.r0, idx.r1, idx.c0, idx.c1),
                "Lexicographical ordering failure at {i}"
            );
        }
    }
}

#[test]
fn test_exact_spectrum_fourier_f6() {
    let f6 = standard_fourier_f6();
    let spec = CrossRatioSpectrum::from_matrix(&f6);

    assert_eq!(spec.total_count, NUM_SUBMATRICES_225);
    assert_eq!(spec.non_root24_count, 0);

    // All cross-ratios of F6 are 6th roots of unity (multiples of 4 mod 24)
    for (&exp, &cnt) in &spec.exponent_counts {
        assert!(cnt > 0);
        assert_eq!(
            exp % 4,
            0,
            "F6 cross-ratio exponent {exp} must be a multiple of 4 mod 24"
        );
    }

    // Expected exact counts for standard F6:
    // exp 0: 36 (value 1)
    // exp 12: 45 (value -1)
    // exp 8 + exp 16: 60 + 48 = 108 (powers of omega_3)
    // exp 4 + exp 20: 26 + 10 = 36 (powers of zeta_6)
    assert_eq!(spec.count_of(0), 36);
    assert_eq!(spec.count_of(12), 45);
    assert_eq!(spec.count_of(8) + spec.count_of(16), 108);
    assert_eq!(spec.count_of(4) + spec.count_of(20), 36);
    assert_eq!(spec.imaginary_unit_count(), 0);

    // Classification tests
    assert!(!spec.haagerup_imaginary_spectrum_test());
    assert!(!spec.tao_cubic_spectrum_test());
    assert!(fourier_vanishing_test(&f6, &spec));
    assert_eq!(classify_orbit(&f6), OrbitClass::Fourier);
}

#[test]
fn test_exact_spectrum_tao_s6() {
    let s6 = tao_s6_matrix();
    let spec = CrossRatioSpectrum::from_matrix(&s6);

    assert_eq!(spec.total_count, NUM_SUBMATRICES_225);
    assert_eq!(spec.non_root24_count, 0);

    // Strictly cubic: all cross-ratios lie in {1, omega_3, omega_3^2} (exponents in {0, 8, 16})
    assert!(spec.is_strictly_cubic());
    assert_eq!(spec.count_of(0), 45);
    assert_eq!(spec.count_of(8), 93);
    assert_eq!(spec.count_of(16), 87);
    assert_eq!(spec.count_of(12), 0);
    assert_eq!(spec.imaginary_unit_count(), 0);

    // Verification tests
    assert!(spec.tao_cubic_spectrum_test());
    assert!(!spec.haagerup_imaginary_spectrum_test());
    assert!(!fourier_vanishing_test(&s6, &spec));
    assert_eq!(classify_orbit(&s6), OrbitClass::Tao);
}

#[test]
fn test_exact_spectrum_haagerup_h6() {
    let h6 = haagerup_h6_matrix();
    let spec = CrossRatioSpectrum::from_matrix(&h6);

    assert_eq!(spec.total_count, NUM_SUBMATRICES_225);
    assert_eq!(spec.non_root24_count, 0);

    // Strictly quartic: exponents in {0, 6, 12, 18}
    assert!(spec.is_strictly_quartic());
    assert_eq!(spec.count_of(0), 30);
    assert_eq!(spec.count_of(6), 60);
    assert_eq!(spec.count_of(12), 75);
    assert_eq!(spec.count_of(18), 60);

    // Exactly 120 imaginary unit cross-ratios
    assert_eq!(spec.imaginary_unit_count(), 120);

    // Verification tests
    assert!(spec.haagerup_imaginary_spectrum_test());
    assert!(!spec.tao_cubic_spectrum_test());
    assert!(!fourier_vanishing_test(&h6, &spec));
    assert_eq!(classify_orbit(&h6), OrbitClass::Haagerup);
}

#[test]
fn test_exact_spectrum_szollosi_b6_discrete_points() {
    // Test Szöllősi Point A: kb=0, kc=8, ke=8, kf=0 (theta = 2pi/3)
    let b = Cyc24::zeta24(0);
    let c = Cyc24::zeta24(8);
    let e = Cyc24::zeta24(8);
    let f = Cyc24::zeta24(0);
    let b6_a = szollosi_dephased_b6(&b, &c, &e, &f).expect("Szollosi Point A must construct B6");
    let spec_a = CrossRatioSpectrum::from_matrix(&b6_a);

    assert_eq!(spec_a.total_count, NUM_SUBMATRICES_225);
    assert_eq!(spec_a.imaginary_unit_count(), 0);
    assert!(!spec_a.is_strictly_cubic());
    assert!(!spec_a.haagerup_imaginary_spectrum_test());
    assert!(!has_affine_fourier_submatrix_condition(&b6_a));

    let pi = pi_approx();
    let expected_theta_a = (rq(8, 1) * &pi) / rq(12, 1);
    assert_eq!(
        classify_orbit(&b6_a),
        OrbitClass::Szollosi {
            theta_approx: expected_theta_a
        }
    );

    // Test Szöllősi Point B: kb=2, kc=19, ke=14, kf=1 (theta = 7pi/6)
    let b_b = Cyc24::zeta24(2);
    let c_b = Cyc24::zeta24(19);
    let e_b = Cyc24::zeta24(14);
    let f_b = Cyc24::zeta24(1);
    let b6_b =
        szollosi_dephased_b6(&b_b, &c_b, &e_b, &f_b).expect("Szollosi Point B must construct B6");
    let spec_b = CrossRatioSpectrum::from_matrix(&b6_b);

    assert_eq!(spec_b.total_count, NUM_SUBMATRICES_225);
    assert_eq!(spec_b.imaginary_unit_count(), 72); // 72 imaginary units != 120
    assert!(!spec_b.haagerup_imaginary_spectrum_test());
    assert!(!spec_b.tao_cubic_spectrum_test());
    assert!(!has_affine_fourier_submatrix_condition(&b6_b));

    let expected_theta_b = (rq(14, 1) * &pi) / rq(12, 1);
    assert_eq!(
        classify_orbit(&b6_b),
        OrbitClass::Szollosi {
            theta_approx: expected_theta_b
        }
    );
}

// ============================================================================
// 3. DETERMINISTIC DECISION-TREE ORBIT CLASSIFICATION
// ============================================================================

#[test]
fn test_deterministic_decision_tree_all_classes() {
    // 1. Fourier class
    let f6 = standard_fourier_f6();
    assert_eq!(classify_orbit(&f6), OrbitClass::Fourier);

    // 2. Tao class
    let s6 = tao_s6_matrix();
    assert_eq!(classify_orbit(&s6), OrbitClass::Tao);

    // 3. Haagerup class
    let h6 = haagerup_h6_matrix();
    assert_eq!(classify_orbit(&h6), OrbitClass::Haagerup);

    // 4. Szöllősi class
    let b = Cyc24::zeta24(0);
    let c = Cyc24::zeta24(8);
    let e = Cyc24::zeta24(8);
    let f = Cyc24::zeta24(0);
    let b6 = szollosi_dephased_b6(&b, &c, &e, &f).unwrap();
    let theta_approx = extract_szollosi_theta_approx(&b6);
    assert_eq!(classify_orbit(&b6), OrbitClass::Szollosi { theta_approx });
}

#[test]
fn test_fourier_dita_family_all_points_classified_fourier() {
    let w0 = Cyc24::rat(ri(1));
    let w1 = Cyc24::zeta24(8);
    let w2 = Cyc24::zeta24(16);
    let f3_arr = [
        [w0.clone(), w0.clone(), w0.clone()],
        [w0.clone(), w1.clone(), w2.clone()],
        [w0.clone(), w2.clone(), w1.clone()],
    ];

    let dita_pts = [
        (0i64, 0i64),
        (0, 8),
        (8, 0),
        (16, 16),
        (0, 16),
        (8, 8),
        (16, 0),
    ];

    for &(dx, dy) in &dita_pts {
        let d_diag = [
            Cyc24::rat(ri(1)),
            Cyc24::zeta24(dx as i32),
            Cyc24::zeta24(dy as i32),
        ];

        let mut mat = matrix_zero();
        for r in 0..3 {
            for c in 0..3 {
                mat[r][c] = f3_arr[r][c].clone();
                mat[r][c + 3] = d_diag[r].mul(&f3_arr[r][c]);
                mat[r + 3][c] = f3_arr[r][c].clone();
                mat[r + 3][c + 3] = d_diag[r].mul(&f3_arr[r][c]).neg();
            }
        }

        assert!(
            has_affine_fourier_submatrix_condition(&mat),
            "Dita point ({dx}, {dy}) must satisfy affine Fourier condition"
        );
        assert_eq!(
            classify_orbit(&mat),
            OrbitClass::Fourier,
            "Dita point ({dx}, {dy}) must be classified as Fourier"
        );
    }
}

// ============================================================================
// 4. BOUNDARY CONFLUENCE MATRICES CLASSIFICATION CONSISTENCY
// ============================================================================

#[test]
fn test_boundary_confluence_classification_consistency() {
    // Boundary Point 1: Szöllősi boundary point meeting Fourier at theta = 0
    // kb=0, kc=8, ke=0, kf=16
    let b = Cyc24::zeta24(0);
    let c = Cyc24::zeta24(8);
    let e = Cyc24::zeta24(0);
    let f = Cyc24::zeta24(16);
    let bnd_fourier = szollosi_dephased_b6(&b, &c, &e, &f).expect("Construct boundary Fourier");

    // Confluence matrix has affine Fourier structure
    assert!(has_affine_fourier_submatrix_condition(&bnd_fourier));
    assert_eq!(
        classify_orbit(&bnd_fourier),
        OrbitClass::Fourier,
        "Boundary matrix at theta = 0 must be consistently classified as Fourier"
    );

    // Boundary Point 2: Szöllősi boundary point meeting Haagerup at theta = pi/2
    // kb=0, kc=6, ke=0, kf=12
    let b_h = Cyc24::zeta24(0);
    let c_h = Cyc24::zeta24(6);
    let e_h = Cyc24::zeta24(0);
    let f_h = Cyc24::zeta24(12);
    let bnd_haagerup =
        szollosi_dephased_b6(&b_h, &c_h, &e_h, &f_h).expect("Construct boundary Haagerup");

    let spec_h = CrossRatioSpectrum::from_matrix(&bnd_haagerup);
    assert_eq!(spec_h.imaginary_unit_count(), 120);
    assert!(spec_h.haagerup_imaginary_spectrum_test());
    assert_eq!(
        classify_orbit(&bnd_haagerup),
        OrbitClass::Haagerup,
        "Boundary matrix at theta = pi/2 must be consistently classified as Haagerup"
    );
}

// ============================================================================
// 5. EXACT CATALOG EXHAUSTIVENESS CERTIFICATION
// ============================================================================

#[test]
fn test_canonical_catalog_exhaustiveness_certification() {
    let catalog = canonical_catalog_candidates();
    assert!(
        catalog.len() >= 10,
        "Catalog must contain at least 10 canonical candidates"
    );

    let report = certify_catalog_exhaustiveness(&catalog);

    // 1. Exhaustiveness assertion: zero unassigned residual
    assert!(
        report.is_exhaustive,
        "Catalog certification must be completely exhaustive"
    );
    assert_eq!(
        report.unassigned_residual_count, 0,
        "Zero unassigned residual candidate matrices permitted"
    );
    assert_eq!(report.total_candidates_tested, catalog.len());

    // 2. Class representation verification: all 4 classes populated
    assert!(
        report.fourier_count >= 8,
        "Fourier count must be at least 8 (F6 + 7 Dita)"
    );
    assert_eq!(report.tao_count, 1, "Tao count must be 1");
    assert!(
        report.haagerup_count >= 1,
        "Haagerup count must be at least 1"
    );
    assert!(
        report.szollosi_count >= 2,
        "Szollosi count must be at least 2"
    );

    // 3. Every individual result matches expected
    for res in &report.candidate_results {
        assert!(
            res.matches_expected,
            "Candidate {} misclassified: assigned {:?}, expected {:?}",
            res.candidate_name, res.assigned_class, res.expected_class
        );
    }

    // 4. Epistemic metadata
    assert_eq!(report.firewall, FIREWALL);
    assert_eq!(report.authority_effect, AUTHORITY_EFFECT);
    assert_eq!(
        report.schema_version,
        "omega.mub6.orbit-catalog-exhaustiveness.v1"
    );
}

// ============================================================================
// 6. CORNER DETERMINANT POLYNOMIAL IDENTITIES
// ============================================================================

#[test]
fn test_corner_determinant_polynomial_identities() {
    // Identity corner: a=1, b=1, c=1, d=1 -> det = 1*1 - 1*1 - 1 + 1 + 1 - 1 = 0
    let one = Cyc24::rat(ri(1));
    let p_zero = corner_determinant(&one, &one, &one, &one);
    assert!(
        p_zero.is_zero(),
        "P_corner(1,1,1,1) must vanish identically"
    );

    // General corner evaluation
    let a = Cyc24::zeta24(8); // omega
    let b = Cyc24::zeta24(16); // omega^2
    let c = Cyc24::zeta24(16); // omega^2
    let d = Cyc24::zeta24(8); // omega
                              // ad - bc - a + b + c - d = omega^2 - omega^4 - omega + omega^2 + omega^2 - omega
    let p = corner_determinant(&a, &b, &c, &d);
    // omega^2 = zeta(16), omega^4 = omega = zeta(8)
    // ad = omega^2, bc = omega^4 = omega
    // ad - bc = omega^2 - omega
    // - a + b + c - d = - omega + omega^2 + omega^2 - omega = 2 omega^2 - 2 omega
    // total = 3 omega^2 - 3 omega
    let expected = Cyc24::zeta24(16)
        .mul(&Cyc24::rat(ri(3)))
        .sub(&Cyc24::zeta24(8).mul(&Cyc24::rat(ri(3))));
    assert_eq!(p, expected);
}
