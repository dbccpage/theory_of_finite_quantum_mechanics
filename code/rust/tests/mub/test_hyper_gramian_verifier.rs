use num_rational::BigRational;
use num_traits::Zero;
use tfqm_mub::native::exact::mub6_hyper_gramian::{
    canonical_5mub_gramian, canonical_6mub_gramian, dual_certificate_matrix_5,
    dual_certificate_matrix_6, dual_witness_vector_5, dual_witness_vector_6,
    solve_hyper_gramian_certificate, trace_inner_product, verify_hyper_gramian_structure,
    GRAMIAN_DIM_5, GRAMIAN_DIM_6, NUM_BASES_5, NUM_BASES_6,
};
use tfqm_mub::native::exact::mub6_quad_sdp::ldlt_pivots_rational;
use engine_number_theory::cyclotomic::Cyc24;

#[test]
fn test_5mub_gramian_dimensions_and_structure() {
    let g = canonical_5mub_gramian();
    assert_eq!(g.len(), GRAMIAN_DIM_5);
    assert_eq!(g[0].len(), GRAMIAN_DIM_5);

    let report = verify_hyper_gramian_structure(&g, NUM_BASES_5);
    assert!(report.verified_sound);
    assert!(report.diagonal_blocks_identity);
    assert!(report.off_diagonal_blocks_modulus_sixth);
    assert!(report.hermitian_exact);
}

#[test]
fn test_6mub_gramian_dimensions_and_structure() {
    let g = canonical_6mub_gramian();
    assert_eq!(g.len(), GRAMIAN_DIM_6);
    assert_eq!(g[0].len(), GRAMIAN_DIM_6);

    let report = verify_hyper_gramian_structure(&g, NUM_BASES_6);
    assert!(report.verified_sound);
    assert!(report.diagonal_blocks_identity);
    assert!(report.off_diagonal_blocks_modulus_sixth);
    assert!(report.hermitian_exact);
}

#[test]
fn test_dual_witness_vectors_norms() {
    let v5 = dual_witness_vector_5();
    assert_eq!(v5.len(), GRAMIAN_DIM_5);
    let mut norm5 = Cyc24::zero();
    for entry in &v5 {
        norm5 = norm5.add(&entry.mul(&entry.conj()));
    }
    assert_eq!(norm5, Cyc24::rat(BigRational::from_integer(89.into())));

    let v6 = dual_witness_vector_6();
    assert_eq!(v6.len(), GRAMIAN_DIM_6);
    let mut norm6 = Cyc24::zero();
    for entry in &v6 {
        norm6 = norm6.add(&entry.mul(&entry.conj()));
    }
    assert_eq!(norm6, Cyc24::rat(BigRational::from_integer(89.into())));
}

#[test]
fn test_5mub_dual_certificates_trace_and_pivots() {
    let g5 = canonical_5mub_gramian();
    let w_rank1 = dual_certificate_matrix_5(false);
    let w_strict = dual_certificate_matrix_5(true);

    let inner_r1 = trace_inner_product(&w_rank1, &g5);
    assert_eq!(inner_r1.a[0], BigRational::from_integer((-7).into()));
    assert!(inner_r1.a[0] < BigRational::zero());

    let inner_strict = trace_inner_product(&w_strict, &g5);
    assert_eq!(inner_strict.a[0], BigRational::from_integer((-6).into()));
    assert!(inner_strict.a[0] < BigRational::zero());

    let pivots_r1 = ldlt_pivots_rational(&w_rank1).expect("LDL^T of W_rank1^(5) failed");
    assert_eq!(pivots_r1.len(), GRAMIAN_DIM_5);
    assert!(pivots_r1.iter().all(|p| p >= &BigRational::zero()));

    let pivots_strict = ldlt_pivots_rational(&w_strict).expect("LDL^T of W_strict^(5) failed");
    assert_eq!(pivots_strict.len(), GRAMIAN_DIM_5);
    assert!(pivots_strict.iter().all(|p| p > &BigRational::zero()));
}

#[test]
fn test_6mub_dual_certificates_trace_and_pivots() {
    let g6 = canonical_6mub_gramian();
    let w_rank1 = dual_certificate_matrix_6(false);
    let w_strict = dual_certificate_matrix_6(true);

    let inner_r1 = trace_inner_product(&w_rank1, &g6);
    assert_eq!(inner_r1.a[0], BigRational::from_integer((-7).into()));
    assert!(inner_r1.a[0] < BigRational::zero());

    let inner_strict = trace_inner_product(&w_strict, &g6);
    assert_eq!(inner_strict.a[0], BigRational::from_integer((-6).into()));
    assert!(inner_strict.a[0] < BigRational::zero());

    let pivots_r1 = ldlt_pivots_rational(&w_rank1).expect("LDL^T of W_rank1^(6) failed");
    assert_eq!(pivots_r1.len(), GRAMIAN_DIM_6);
    assert!(pivots_r1.iter().all(|p| p >= &BigRational::zero()));

    let pivots_strict = ldlt_pivots_rational(&w_strict).expect("LDL^T of W_strict^(6) failed");
    assert_eq!(pivots_strict.len(), GRAMIAN_DIM_6);
    assert!(pivots_strict.iter().all(|p| p > &BigRational::zero()));
}

#[test]
fn test_solve_hyper_gramian_certificate_complete() {
    let cert = solve_hyper_gramian_certificate();

    assert_eq!(cert.schema_version, "omega.mub.hyper-gramian-sdp.v2");
    assert_eq!(cert.dimension, 6);
    assert_eq!(cert.bases_count_5, 5);
    assert_eq!(cert.gramian_dim_5, 30);
    assert_eq!(cert.bases_count_6, 6);
    assert_eq!(cert.gramian_dim_6, 36);

    assert_eq!(cert.mub5_rank1_inner_product, "-7");
    assert_eq!(cert.mub5_strict_inner_product, "-6");
    assert_eq!(cert.mub5_strict_regularizer, "1/30");

    assert_eq!(cert.mub6_rank1_inner_product, "-7");
    assert_eq!(cert.mub6_strict_inner_product, "-6");
    assert_eq!(cert.mub6_strict_regularizer, "1/36");

    assert_eq!(cert.firewall, "stated region only; mints no authority");
    assert_eq!(cert.authority_effect, "None");

    assert!(cert.gramian_5_structure.verified_sound);
    assert!(cert.gramian_6_structure.verified_sound);
    assert!(cert.mub5_rank1_strictly_negative);
    assert!(cert.mub5_strict_strictly_negative);
    assert!(cert.mub5_rank1_pivots_nonnegative);
    assert!(cert.mub5_strict_pivots_strictly_positive);
    assert!(cert.mub6_rank1_strictly_negative);
    assert!(cert.mub6_strict_strictly_negative);
    assert!(cert.mub6_rank1_pivots_nonnegative);
    assert!(cert.mub6_strict_pivots_strictly_positive);

    assert!(cert.dual_certificates_psd_certified);
    assert!(cert.fixed_matrix_5_witness_checked);
    assert!(cert.fixed_matrix_6_witness_checked);
    assert!(cert.constructed_matrix_5_not_psd);
    assert!(cert.constructed_matrix_6_not_psd);
    assert!(cert.complete);
}

#[test]
fn ldlt_refuses_nonrational_and_malformed_inputs() {
    use engine_number_theory::cyclotomic::Cyc24;
    let one = Cyc24::rat(BigRational::from_integer(1.into()));
    // 1-sqrt(2) has a positive rational coefficient but a negative real value.
    assert!(ldlt_pivots_rational(&[vec![one.sub(&Cyc24::sqrt2())]]).is_err());
    assert!(ldlt_pivots_rational(&[vec![Cyc24::zeta24(6)]]).is_err());
    assert!(ldlt_pivots_rational(&[]).is_err());
    assert!(ldlt_pivots_rational(&[vec![]]).is_err());
    let non_hermitian = vec![vec![one.clone(), one.clone()], vec![Cyc24::zero(), one]];
    assert!(ldlt_pivots_rational(&non_hermitian).is_err());
}

#[test]
fn fixed_matrices_do_not_claim_dimension_wide_exclusion() {
    let r = solve_hyper_gramian_certificate();
    assert!(!r.mub_nonexistence_established);
    assert_eq!(r.scope, "two_synthetic_block_matrices");
    assert!(!verify_hyper_gramian_structure(&[], 0).verified_sound);
    assert!(!verify_hyper_gramian_structure(&[], usize::MAX).verified_sound);
}

#[test]
fn large_phase_indices_reduce_before_machine_integer_arithmetic() {
    use tfqm_mub::native::exact::mub6_hyper_gramian::{chirp_fourier6_block, dita_d6_block};
    assert_eq!(
        chirp_fourier6_block(i64::MAX),
        chirp_fourier6_block(i64::MAX.rem_euclid(6))
    );
    assert_eq!(
        dita_d6_block(i64::MIN, i64::MAX),
        dita_d6_block(i64::MIN.rem_euclid(24), i64::MAX.rem_euclid(24))
    );
}
