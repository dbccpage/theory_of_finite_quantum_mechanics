//! Comprehensive Unit and Integration Test Suite for Target A9:
//! Rust Native Haagerup Orbit Certifier & Cycle Circulation Engine.
//!
//! AuthorityEffect: None.

use num_rational::BigRational;
use num_traits::Zero;
use std::fs;
use std::path::Path;
use syn::visit::Visit;

use omega_mub::omega_native::exact::d6_exact_curvature_cochain::D;
use omega_mub::omega_native::exact::mub6_constants::{base_gap, delta_certified, lipschitz_bound};
use omega_mub::omega_native::exact::mub6_f6_chart::f6_family_columns;
use omega_mub::omega_native::exact::mub6_firewall::{AUTHORITY_EFFECT, FIREWALL};
use omega_mub::omega_native::exact::mub6_haagerup::{
    certify_haagerup_cycle_circulation, certify_haagerup_full_orbit, curvature_margin,
    enumerate_225_submatrices, extract_cross_ratio_exponents, haagerup_h6_matrix,
    haagerup_phi1_circulation, root24_exponent, verify_deltoid_identity, verify_haagerup_chm,
    verify_orbit_isolation_b6, verify_orbit_isolation_f6, verify_orbit_isolation_s6,
    CrossRatioSpectrum, HaagerupError, HaagerupOrbitReceipt, NUM_SUBMATRICES_225,
};
use omega_mub::omega_native::exact::mub6_matrix6::matrix_adjoint;
use omega_mub::omega_native::exact::mub6_matrix6::{matrix_mul, matrix_zero};
use omega_mub::omega_native::exact::mub6_tao_chart::tao_s6_matrix;
use omega_mub::omega_native::exact::szollosi_triad_solver::szollosi_dephased_b6;
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
        .join("omega_native")
        .join("mub6_haagerup.rs");

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
        "Target A9 Rust module violated zero-float discipline at AST level: {:?}",
        visitor.found_floats
    );

    // 2. Lexical check
    assert!(
        !source.contains("f32"),
        "mub6_haagerup.rs must contain zero f32 occurrences"
    );
    assert!(
        !source.contains("f64"),
        "mub6_haagerup.rs must contain zero f64 occurrences"
    );
}

// ============================================================================
// 2. EXACT HAAGERUP CHM & DELTOID IDENTITY VERIFICATION
// ============================================================================

#[test]
fn test_exact_haagerup_chm_construction_and_orthogonality() {
    let h6 = haagerup_h6_matrix();

    // 1. Verify CHM properties
    let chm_res = verify_haagerup_chm(&h6);
    assert!(
        chm_res.is_ok(),
        "Haagerup H_6 must be an exact Complex Hadamard Matrix: {:?}",
        chm_res
    );

    // 2. Exact unitarity: H_6 * H_6† == 6 I_6
    let h6_adj = matrix_adjoint(&h6);
    let prod = matrix_mul(&h6, &h6_adj);
    let six = Cyc24::rat(ri(6));
    let zero = Cyc24::zero();

    for i in 0..D {
        for j in 0..D {
            let expected = if i == j { &six } else { &zero };
            assert_eq!(
                &prod[i][j], expected,
                "Orthogonality failure at ({i}, {j}): got {:?}, expected {:?}",
                prod[i][j], expected
            );
        }
    }

    // 3. Every entry has unit modulus |H_{jk}|^2 == 1 in Cyc24
    let one = Cyc24::rat(ri(1));
    for i in 0..D {
        for j in 0..D {
            let mod_sq = h6[i][j].mul(&h6[i][j].conj());
            assert_eq!(mod_sq, one, "Entry ({i}, {j}) does not have unit modulus");
        }
    }

    // 4. Deltoid condition z1 + z2 == 0
    let b = Cyc24::zeta24(0);
    let c = Cyc24::zeta24(6);
    let e = Cyc24::zeta24(0);
    let f = Cyc24::zeta24(12);
    let deltoid_res = verify_deltoid_identity(&b, &c, &e, &f);
    assert!(
        deltoid_res.is_ok(),
        "Deltoid identity z1 + z2 == 0 must hold"
    );
}

// ============================================================================
// 3. 225 SUBMATRIX CROSS-RATIO INVARIANT SPECTRUM CALCULATION
// ============================================================================

#[test]
fn test_225_submatrix_cross_ratio_invariant_spectrum() {
    let submatrices = enumerate_225_submatrices();
    assert_eq!(submatrices.len(), NUM_SUBMATRICES_225);

    // Verify uniqueness and strict index ordering
    for idx in &submatrices {
        assert!(idx.r0 < idx.r1 && idx.r1 < D);
        assert!(idx.c0 < idx.c1 && idx.c1 < D);
    }

    let h6 = haagerup_h6_matrix();
    let exps =
        extract_cross_ratio_exponents(&h6).expect("All cross-ratios must be exact roots of unity");

    assert_eq!(exps.len(), NUM_SUBMATRICES_225);

    let spec = CrossRatioSpectrum::from_exponents(&exps);
    assert_eq!(spec.total_count, NUM_SUBMATRICES_225);

    // Exact count verification:
    // - 30 entries with exponent 0 (value 1)
    // - 60 entries with exponent 6 (value i)
    // - 75 entries with exponent 12 (value -1)
    // - 60 entries with exponent 18 (value -i)
    assert_eq!(spec.count_of(0), 30, "Exponent 0 count must be 30");
    assert_eq!(spec.count_of(6), 60, "Exponent 6 count must be 60");
    assert_eq!(spec.count_of(12), 75, "Exponent 12 count must be 75");
    assert_eq!(spec.count_of(18), 60, "Exponent 18 count must be 60");

    assert_eq!(
        spec.count_of(0) + spec.count_of(6) + spec.count_of(12) + spec.count_of(18),
        225,
        "Sum of quartic root counts must equal 225"
    );

    // All exponents are quartic: strictly in {0, 6, 12, 18}
    assert!(
        spec.is_strictly_quartic(),
        "Haagerup spectrum must be strictly quartic mod 24"
    );
    assert!(
        !spec.is_strictly_cubic(),
        "Haagerup spectrum cannot be cubic"
    );

    // Total imaginary count is 60 + 60 = 120
    assert_eq!(spec.imaginary_unit_count(), 120);

    // Cross-validate against artifacts/mub_target_a9_haagerup_receipt.json if present
    let manifest_dir = env!("CARGO_MANIFEST_DIR");
    let repo_artifact = Path::new(manifest_dir)
        .join("..")
        .join("..")
        .join("..")
        .join("artifacts")
        .join("mub_target_a9_haagerup_receipt.json");
    if repo_artifact.exists() {
        let content = fs::read_to_string(&repo_artifact).expect("Read receipt artifact");
        let val: serde_json::Value =
            serde_json::from_str(&content).expect("Parse receipt artifact");
        if let Some(arr) = val
            .pointer("/cross_ratios_225/exponents_mod24")
            .and_then(|v| v.as_array())
        {
            let receipt_exps: Vec<i64> = arr.iter().filter_map(|v| v.as_i64()).collect();
            assert_eq!(
                exps, receipt_exps,
                "Computed exponents must match canonical receipt exactly"
            );
        }
    }
}

// ============================================================================
// 4. ORBIT ISOLATION VERIFICATION AGAINST S_6, F_6, AND B_6
// ============================================================================

#[test]
fn test_orbit_isolation_against_s6_f6_b6() {
    let h6 = haagerup_h6_matrix();
    let h6_exps = extract_cross_ratio_exponents(&h6).unwrap();

    // 1. Tao S_6 Isolation
    let s6 = tao_s6_matrix();
    let s6_exps = extract_cross_ratio_exponents(&s6).unwrap();
    let spec_s6 = CrossRatioSpectrum::from_exponents(&s6_exps);

    // Verify S_6 is strictly cubic {0, 8, 16}
    assert!(
        spec_s6.is_strictly_cubic(),
        "S_6 must be strictly cubic mod 24"
    );
    assert_eq!(
        spec_s6.imaginary_unit_count(),
        0,
        "S_6 must contain 0 imaginary units"
    );
    assert_eq!(spec_s6.count_of(0), 45);
    assert_eq!(spec_s6.count_of(8), 93);
    assert_eq!(spec_s6.count_of(16), 87);

    let iso_s6 = verify_orbit_isolation_s6(&h6_exps, &s6_exps)
        .expect("Orbit isolation check against S_6 must succeed");
    assert!(iso_s6.separated);
    assert_eq!(iso_s6.h6_imaginary_count, 120);
    assert_eq!(iso_s6.other_imaginary_count, 0);

    // 2. Fourier F_6(0,0) Isolation
    let f6_cols = f6_family_columns(0, 0);
    // Convert column vectors to Matrix6 unnormalized
    let sqrt6 = Cyc24::zeta24(3)
        .add(&Cyc24::zeta24(-3))
        .mul(&Cyc24::zeta24(2).add(&Cyc24::zeta24(-2)));
    let mut f6_mat = matrix_zero();
    for j in 0..D {
        for i in 0..D {
            // Unscale by sqrt(6) to get CHM entries with unit modulus
            f6_mat[i][j] = f6_cols[j][i].mul(&sqrt6);
        }
    }
    let f6_exps = extract_cross_ratio_exponents(&f6_mat).unwrap();
    let spec_f6 = CrossRatioSpectrum::from_exponents(&f6_exps);
    assert_eq!(
        spec_f6.imaginary_unit_count(),
        0,
        "F_6(0,0) must contain 0 imaginary units"
    );

    let iso_f6 = verify_orbit_isolation_f6(&h6_exps, &f6_exps)
        .expect("Orbit isolation check against F_6 must succeed");
    assert!(iso_f6.separated);
    assert_eq!(iso_f6.h6_imaginary_count, 120);
    assert_eq!(iso_f6.other_imaginary_count, 0);

    // 3. B_6 Point 3 (omega, omega^2) Isolation
    let b6_pt3 = szollosi_dephased_b6(
        &Cyc24::zeta24(0),
        &Cyc24::zeta24(8),
        &Cyc24::zeta24(0),
        &Cyc24::zeta24(16),
    )
    .expect("B_6 Point 3 must be valid");
    let b6_exps = extract_cross_ratio_exponents(&b6_pt3).unwrap();
    let spec_b6 = CrossRatioSpectrum::from_exponents(&b6_exps);
    assert_eq!(
        spec_b6.imaginary_unit_count(),
        0,
        "B_6 Point 3 must contain 0 imaginary units"
    );

    let iso_b6 = verify_orbit_isolation_b6(&h6_exps, &b6_exps)
        .expect("Orbit isolation check against B_6 must succeed");
    assert!(iso_b6.separated);
    assert_eq!(iso_b6.h6_imaginary_count, 120);
    assert_eq!(iso_b6.other_imaginary_count, 0);
}

// ============================================================================
// 5. CURVATURE MARGIN & CANONICAL CONSTANTS
// ============================================================================

#[test]
fn test_curvature_margin_and_canonical_constants() {
    let bg = base_gap();
    let lb = lipschitz_bound();
    let ms = delta_certified();
    let cm = curvature_margin();
    let phi1_min = haagerup_phi1_circulation();

    assert_eq!(bg, rq(37249, 90000));
    assert_eq!(lb, rq(85, 9));
    assert_eq!(ms, rq(1, 1000));

    // Erosion L * delta = 85/9 * 1/1000 = 85/9000 = 17/1800
    let erosion = &lb * &ms;
    assert_eq!(erosion, rq(17, 1800));

    // Curvature margin: 37249/90000 - 850/90000 = 36399/90000 = 12133/30000
    assert_eq!(cm, rq(12133, 30000));
    assert!(cm > BigRational::zero());

    // Circulation Phi_1 = 3 * cm = 12133/10000
    assert_eq!(phi1_min, rq(12133, 10000));
    assert!(phi1_min > BigRational::zero());
}

// ============================================================================
// 6. NETWORK SIMPLEX PHI_1 > 0 CYCLE CIRCULATION CERTIFICATION
// ============================================================================

#[test]
fn test_network_simplex_phi1_positive_cycle_circulation() {
    // 1. Scale 30000
    let cert30k = certify_haagerup_cycle_circulation(30000)
        .expect("Circulation certification at scale 30000 must succeed");

    assert_eq!(cert30k.scale, 30000);
    assert_eq!(cert30k.edge_cochain, vec![12133, 12133, 12133]);
    assert_eq!(cert30k.net_circulation, 36399);
    assert_eq!(cert30k.phi1_objective, 36399);
    assert!(cert30k.phi1_objective > 0);
    assert!(cert30k.dual_gap_zero);
    assert_eq!(cert30k.coboundary_sum, 0);
    assert!(cert30k.circulation_conserved);
    assert!(cert30k.certified);
    assert_eq!(cert30k.rational_phi1, "12133/10000");

    // 2. Scale 90000
    let cert90k = certify_haagerup_cycle_circulation(90000)
        .expect("Circulation certification at scale 90000 must succeed");

    assert_eq!(cert90k.scale, 90000);
    assert_eq!(cert90k.edge_cochain, vec![36399, 36399, 36399]);
    assert_eq!(cert90k.net_circulation, 109197);
    assert_eq!(cert90k.phi1_objective, 109197);
    assert!(cert90k.dual_gap_zero);
    assert_eq!(cert90k.coboundary_sum, 0);
    assert!(cert90k.circulation_conserved);
    assert!(cert90k.certified);
    assert_eq!(cert90k.rational_phi1, "12133/10000");
}

// ============================================================================
// 7. CANONICAL SEALED RECEIPT GENERATION & SERDE
// ============================================================================

#[test]
fn test_haagerup_orbit_receipt_generation_and_serde() {
    let s6 = tao_s6_matrix();
    let s6_exps = extract_cross_ratio_exponents(&s6).unwrap();

    let sqrt6 = Cyc24::zeta24(3)
        .add(&Cyc24::zeta24(-3))
        .mul(&Cyc24::zeta24(2).add(&Cyc24::zeta24(-2)));
    let f6_cols = f6_family_columns(0, 0);
    let mut f6_mat = matrix_zero();
    for j in 0..D {
        for i in 0..D {
            f6_mat[i][j] = f6_cols[j][i].mul(&sqrt6);
        }
    }
    let f6_exps = extract_cross_ratio_exponents(&f6_mat).unwrap();

    let b6_pt3 = szollosi_dephased_b6(
        &Cyc24::zeta24(0),
        &Cyc24::zeta24(8),
        &Cyc24::zeta24(0),
        &Cyc24::zeta24(16),
    )
    .unwrap();
    let b6_exps = extract_cross_ratio_exponents(&b6_pt3).unwrap();

    let receipt = certify_haagerup_full_orbit(30000, &s6_exps, &f6_exps, &b6_exps)
        .expect("Full orbit certification must succeed");

    assert_eq!(receipt.schema_version, "omega.mub.target-a9-haagerup.v1");
    assert_eq!(receipt.firewall, FIREWALL);
    assert_eq!(receipt.authority_effect, AUTHORITY_EFFECT);
    assert_eq!(receipt.matrix_name, "Haagerup_H6_2circulant");
    assert!(receipt.is_exact_chm);
    assert!(receipt.z1_plus_z2_zero);
    assert_eq!(receipt.num_submatrices, 225);
    assert!(receipt.isolated_from_s6);
    assert!(receipt.isolated_from_f6);
    assert!(receipt.isolated_from_b6_generic);
    assert_eq!(receipt.base_gap, "37249/90000");
    assert_eq!(receipt.lipschitz_bound, "85/9");
    assert_eq!(receipt.mesh_step, "1/1000");
    assert_eq!(receipt.curvature_margin, "12133/30000");
    assert_eq!(receipt.phi1_circulation, "12133/10000");
    assert_eq!(receipt.scale, 30000);
    assert_eq!(receipt.integer_phi1_objective, 36399);
    assert_eq!(receipt.net_circulation, 36399);
    assert!(receipt.circulation_conserved);
    assert!(receipt.verified);

    // JSON serialization round-trip
    let json_str = receipt
        .to_json_string()
        .expect("JSON serialization must succeed");
    assert!(json_str.contains("omega.mub.target-a9-haagerup.v1"));
    assert!(json_str.contains("12133/30000"));
    assert!(json_str.contains("12133/10000"));

    let deserialized =
        HaagerupOrbitReceipt::from_json_str(&json_str).expect("JSON deserialization must succeed");
    assert_eq!(receipt, deserialized);
}

// ============================================================================
// 8. COMPREHENSIVE NEGATIVE CONTROL FALSIFICATION SUITE
// ============================================================================

#[test]
fn test_negative_control_perturbed_non_unitary_matrix_rejected() {
    let mut bad_m = haagerup_h6_matrix();
    // Mutate entry (0, 0) from 1 to 2
    bad_m[0][0] = Cyc24::rat(ri(2));

    let res = verify_haagerup_chm(&bad_m);
    assert!(
        matches!(
            res,
            Err(HaagerupError::NotUnitModulus { row: 0, col: 0, .. })
        ),
        "Mutated non-unimodular entry must fail verify_haagerup_chm"
    );
}

#[test]
fn test_negative_control_perturbed_non_orthogonal_matrix_rejected() {
    let mut bad_m = haagerup_h6_matrix();
    // Mutate entry (1, 1) to -1 (remains unimodular, but ruins orthogonality)
    bad_m[1][1] = Cyc24::zeta24(12);

    let res = verify_haagerup_chm(&bad_m);
    assert!(
        matches!(res, Err(HaagerupError::NotOrthogonal { .. })),
        "Mutated non-orthogonal matrix must fail verify_haagerup_chm"
    );
}

#[test]
fn test_negative_control_deltoid_condition_violation_rejected() {
    // Parameters where z1 + z2 != 0:
    // b=1, c=1, e=1, f=1 => z1 = 3, z2 = 3 => z1 + z2 = 6 != 0
    let one = Cyc24::rat(ri(1));
    let res = verify_deltoid_identity(&one, &one, &one, &one);
    assert!(
        matches!(res, Err(HaagerupError::DeltoidConditionViolated { .. })),
        "Violated deltoid condition must be rejected"
    );
}

#[test]
fn test_negative_control_invalid_cross_ratio_element_detected() {
    // An element in Cyc24 that is NOT a 24th root of unity, e.g. 1/2
    let non_root = Cyc24::rat(ri(1) / ri(2));
    assert!(
        root24_exponent(&non_root).is_none(),
        "Non-root element must return None for root24_exponent"
    );
}

#[test]
fn test_negative_control_non_positive_circulation_rejected() {
    // Zero scale
    let res_zero = certify_haagerup_cycle_circulation(0);
    assert!(
        matches!(res_zero, Err(HaagerupError::InvalidParameter(_))),
        "Zero scale must be rejected"
    );

    // Negative scale
    let res_neg = certify_haagerup_cycle_circulation(-30000);
    assert!(
        matches!(res_neg, Err(HaagerupError::InvalidParameter(_))),
        "Negative scale must be rejected"
    );
}

#[test]
fn test_negative_control_orbit_isolation_identical_spectra_rejected() {
    let h6 = haagerup_h6_matrix();
    let h6_exps = extract_cross_ratio_exponents(&h6).unwrap();

    // Comparing H_6 with itself in F_6 check must fail separation
    let res_f6 = verify_orbit_isolation_f6(&h6_exps, &h6_exps);
    assert!(
        matches!(res_f6, Err(HaagerupError::OrbitIsolationFailed(_))),
        "Identical spectra must fail F_6 orbit isolation"
    );

    let res_b6 = verify_orbit_isolation_b6(&h6_exps, &h6_exps);
    assert!(
        matches!(res_b6, Err(HaagerupError::OrbitIsolationFailed(_))),
        "Identical spectra must fail B_6 orbit isolation"
    );
}
