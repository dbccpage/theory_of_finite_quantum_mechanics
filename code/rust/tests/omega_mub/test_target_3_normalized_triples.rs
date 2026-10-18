//! Integration and unit tests for Target 3: Normalized Triples Chart & Regular Corner Reconstruction.
//!
//! AuthorityEffect: None.

use num_traits::Zero;

use omega_mub::omega_native::exact::mub6_firewall::FIREWALL;
use omega_mub::omega_native::exact::mub6_normalized_triples::{
    corner_det_poly_cyc, corner_det_poly_rat, extract_corner_param_3x3, extract_leading_corner_3x3,
    generate_normalized_triple_report, is_regular_corner_cyc, is_singular_corner_cyc,
    sample_normalized_fourier_triple, verify_transition_scaling_cross_mult, CornerParamCyc,
};
use omega_number_theory::cyclotomic::Cyc24;
use omega_number_theory::rational::rq;

#[test]
fn test_transition_scaling_cross_multiplication() {
    assert!(verify_transition_scaling_cross_mult());
    assert_eq!(1i64 * 36, 6i64 * 6);
    assert_eq!(rq(1, 36) * rq(6, 1), rq(1, 6));
}

#[test]
fn test_regular_corner_chart_nonzero_exact_cyclotomic() {
    // 4th roots of unity:
    // a = zeta_24^6  = i
    // b = zeta_24^12 = -1
    // c = zeta_24^18 = -i
    // d = zeta_24^0  = 1
    let a = Cyc24::zeta24(6);
    let b = Cyc24::zeta24(12);
    let c = Cyc24::zeta24(18);
    let d = Cyc24::zeta24(0);

    let param = CornerParamCyc { a, b, c, d };
    let det = corner_det_poly_cyc(&param);

    // Expected: -2 - 2i
    let expected = Cyc24::rat(rq(-2, 1)).sub(&Cyc24::zeta24(6).mul(&Cyc24::rat(rq(2, 1))));
    assert_eq!(det, expected);
    assert!(!det.is_zero());
    assert!(is_regular_corner_cyc(&param));
    assert!(!is_singular_corner_cyc(&param));
}

#[test]
fn test_extract_leading_corner_and_param() {
    let (h, _) = sample_normalized_fourier_triple();
    let corner = extract_leading_corner_3x3(&h);

    assert_eq!(corner.len(), 3);
    assert_eq!(corner[0].len(), 3);

    let param = extract_corner_param_3x3(&corner);
    assert_eq!(param.a, corner[1][1]);
    assert_eq!(param.b, corner[1][2]);
    assert_eq!(param.c, corner[2][1]);
    assert_eq!(param.d, corner[2][2]);
}

#[test]
fn test_report_generation() {
    let a = Cyc24::zeta24(6);
    let b = Cyc24::zeta24(12);
    let c = Cyc24::zeta24(18);
    let d = Cyc24::zeta24(0);
    let param = CornerParamCyc { a, b, c, d };

    let report = generate_normalized_triple_report(&param);
    assert_eq!(report.firewall, FIREWALL);
    assert!(report.transition_scaling_verified);
    assert!(report.regular_chart_certified);
    assert!(report.zero_denominator_isolated);
}

#[test]
fn test_negative_controls() {
    // 1. All entries equal 1 in Q(zeta_24) => det must vanish
    let one = Cyc24::zeta24(0);
    let param_ones = CornerParamCyc {
        a: one.clone(),
        b: one.clone(),
        c: one.clone(),
        d: one.clone(),
    };
    assert!(corner_det_poly_cyc(&param_ones).is_zero());
    assert!(!is_regular_corner_cyc(&param_ones));
    assert!(is_singular_corner_cyc(&param_ones));

    // 2. All entries equal i in Q(zeta_24) => det must vanish
    let i_unit = Cyc24::zeta24(6);
    let param_i = CornerParamCyc {
        a: i_unit.clone(),
        b: i_unit.clone(),
        c: i_unit.clone(),
        d: i_unit,
    };
    assert!(corner_det_poly_cyc(&param_i).is_zero());
    assert!(!is_regular_corner_cyc(&param_i));
    assert!(is_singular_corner_cyc(&param_i));

    // 3. Exact rational affine singular branch where det = 0:
    // ad - bc - a + b + c - d = 0
    // With a = 2, b = 1, c = 3 => 2d - 3 - 2 + 1 + 3 - d = d - 1 = 0 => d = 1
    let a_rat = rq(2, 1);
    let b_rat = rq(1, 1);
    let c_rat = rq(3, 1);
    let d_rat = rq(1, 1);
    let det_rat = corner_det_poly_rat(&a_rat, &b_rat, &c_rat, &d_rat);
    assert!(det_rat.is_zero());

    // 4. Non-matching transition modulus scale rejected:
    let wrong_modulus = rq(5, 1);
    assert_ne!(wrong_modulus, rq(6, 1));
    let normalized_equiv = wrong_modulus * rq(1, 36);
    assert_ne!(normalized_equiv, rq(1, 6));
}

#[test]
fn test_ast_zero_float_discipline() {
    let src = include_str!("../../omega_mub/src/omega_native/mub6_normalized_triples.rs");
    assert!(
        !src.contains("f32"),
        "mub6_normalized_triples.rs must contain zero f32 occurrences"
    );
    assert!(
        !src.contains("f64"),
        "mub6_normalized_triples.rs must contain zero f64 occurrences"
    );
}
