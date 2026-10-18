//! Exact diagnostics and negative controls for Target A4 quadruple Gramian matrix.
//! AuthorityEffect: None.

use num_rational::BigRational;
use num_traits::{One, Zero};
use omega_mub::omega_native::exact::mub6_quad_sdp::{
    canonical_dual_witness_rank1, canonical_dual_witness_strict, canonical_quad_gramian,
    checked_trace_inner_product, compute_gram_matrix_cyc, dual_certificate_matrix,
    dual_witness_vector, exact_rational, is_psd_cyc, ldlt_pivots_rational,
    solve_quad_sdp_certificate, trace_inner_product, verify_gramian_structure, DualWitnessCyc,
    DIM_HILBERT, GRAMIAN_DIM, NUM_BASES,
};
use omega_number_theory::cyclotomic::Cyc24;
use omega_number_theory::rational::ri;

#[test]
fn test_gramian_dimensions_and_structure() {
    let g = canonical_quad_gramian();
    assert_eq!(g.len(), GRAMIAN_DIM);
    assert_eq!(g[0].len(), GRAMIAN_DIM);

    let report = verify_gramian_structure(&g);
    assert!(report.verified_sound);
    assert!(report.diagonal_blocks_identity);
    assert!(report.off_diagonal_blocks_modulus_sixth);
    assert!(report.hermitian_exact);
}

#[test]
fn test_exact_block_entries_characterization() {
    let g = canonical_quad_gramian();
    let one = Cyc24::rat(BigRational::one());
    let zero = Cyc24::zero();
    let sixth = Cyc24::rat(BigRational::new(1.into(), 6.into()));

    // 1. All 4 diagonal blocks are exactly I_6
    for a in 0..NUM_BASES {
        for i in 0..DIM_HILBERT {
            for j in 0..DIM_HILBERT {
                let idx_i = a * DIM_HILBERT + i;
                let idx_j = a * DIM_HILBERT + j;
                if i == j {
                    assert_eq!(
                        g[idx_i][idx_j], one,
                        "Diagonal entry must be 1 at ({idx_i}, {idx_j})"
                    );
                } else {
                    assert_eq!(
                        g[idx_i][idx_j], zero,
                        "Off-diagonal entry in diagonal block must be 0 at ({idx_i}, {idx_j})"
                    );
                }
            }
        }
    }

    // 2. All 12 off-diagonal blocks satisfy |G_{ij}|^2 = 1/6
    for a in 0..NUM_BASES {
        for b in 0..NUM_BASES {
            if a == b {
                continue;
            }
            for i in 0..DIM_HILBERT {
                for j in 0..DIM_HILBERT {
                    let idx_i = a * DIM_HILBERT + i;
                    let idx_j = b * DIM_HILBERT + j;
                    let entry = &g[idx_i][idx_j];
                    let mod_sq = entry.mul(&entry.conj());
                    assert_eq!(
                        mod_sq, sixth,
                        "Off-diagonal modulus squared must be 1/6 at ({idx_i}, {idx_j})"
                    );
                }
            }
        }
    }

    // 3. Exactly Hermitian
    for i in 0..GRAMIAN_DIM {
        for j in 0..GRAMIAN_DIM {
            assert_eq!(
                g[j][i],
                g[i][j].conj(),
                "Hermitian symmetry violated at ({i}, {j})"
            );
        }
    }
}

#[test]
fn test_dual_witness_vector_norm() {
    let v = dual_witness_vector();
    assert_eq!(v.len(), GRAMIAN_DIM);

    // Compute exact squared norm ||v||^2 = sum_i |v_i|^2
    let mut norm_sq = Cyc24::zero();
    for entry in &v {
        norm_sq = norm_sq.add(&entry.mul(&entry.conj()));
    }

    // ||v_0||^2 = 0
    // ||v_1||^2 = 9 + 1 + 4 + 4 + 4 + 1 = 23
    // ||v_2||^2 = 9 + 1 + 1 + 1 + 9 + 9 = 30
    // ||v_3||^2 = 6 * (1 + 1 + 1 + 1 + 1 + 1) = 36
    // Total = 0 + 23 + 30 + 36 = 89
    let expected = Cyc24::rat(BigRational::from_integer(89.into()));
    assert_eq!(norm_sq, expected);
}

#[test]
fn test_rank1_dual_certificate_trace_inner_and_psd() {
    let g = canonical_quad_gramian();
    let w_rank1 = dual_certificate_matrix(false);

    assert_eq!(w_rank1.len(), GRAMIAN_DIM);
    assert_eq!(w_rank1[0].len(), GRAMIAN_DIM);

    let inner = trace_inner_product(&w_rank1, &g);
    assert_eq!(inner.a[0], BigRational::from_integer((-7).into()));
    assert!(inner.a[0] < BigRational::zero());

    // Verify LDL^T pivots are all non-negative
    let pivots = ldlt_pivots_rational(&w_rank1).expect("LDL^T decomposition should succeed");
    assert_eq!(pivots.len(), GRAMIAN_DIM);
    assert!(pivots.iter().all(|p| p >= &BigRational::zero()));

    // Pivot at index 6 is (-3)^2 = 9
    assert_eq!(pivots[6], BigRational::from_integer(9.into()));

    // Factored dual witness representation
    let w1_factored = canonical_dual_witness_rank1();
    assert!(w1_factored.is_valid());
    assert!(w1_factored.validate_psd().is_ok());
    assert_eq!(w1_factored.to_full_matrix(), w_rank1);

    let tr_factored = w1_factored
        .trace_inner(&g)
        .expect("trace_inner should succeed");
    assert_eq!(tr_factored.a[0], BigRational::from_integer((-7).into()));

    let obstructed = w1_factored
        .verify_dual_obstruction(&g)
        .expect("obstruction check succeeds");
    assert!(obstructed);
}

#[test]
fn test_strict_dual_certificate_trace_inner_and_psd() {
    let g = canonical_quad_gramian();
    let w_strict = dual_certificate_matrix(true);

    let inner = trace_inner_product(&w_strict, &g);
    // Tr(W_strict * G) = -7 + (1/24) * 24 = -6
    assert_eq!(inner.a[0], BigRational::from_integer((-6).into()));
    assert!(inner.a[0] < BigRational::zero());

    // Verify all 24 LDL^T pivots are strictly positive (> 0)
    let pivots = ldlt_pivots_rational(&w_strict).expect("LDL^T decomposition should succeed");
    assert_eq!(pivots.len(), GRAMIAN_DIM);
    assert!(pivots.iter().all(|p| p > &BigRational::zero()));

    // Factored strict dual witness representation
    let w_strict_factored = canonical_dual_witness_strict();
    assert!(w_strict_factored.is_valid());
    assert!(w_strict_factored.validate_psd().is_ok());
    assert_eq!(w_strict_factored.to_full_matrix(), w_strict);

    let tr_strict_factored = w_strict_factored
        .trace_inner(&g)
        .expect("trace_inner should succeed");
    assert_eq!(
        tr_strict_factored.a[0],
        BigRational::from_integer((-6).into())
    );

    let obstructed = w_strict_factored
        .verify_dual_obstruction(&g)
        .expect("obstruction check succeeds");
    assert!(obstructed);
}

#[test]
fn test_solve_quad_sdp_certificate_complete() {
    let cert = solve_quad_sdp_certificate();

    assert_eq!(cert.schema_version, "omega.mub.quad-sdp.v2");
    assert_eq!(cert.dimension, 6);
    assert_eq!(cert.bases_count, 4);
    assert_eq!(cert.gramian_dim, 24);
    assert_eq!(cert.rank1_inner_product, "-7");
    assert_eq!(cert.strict_inner_product, "-6");
    assert_eq!(cert.strict_regularizer, "1/24");
    assert_eq!(cert.firewall, "stated region only; mints no authority");
    assert_eq!(cert.authority_effect, "None");

    assert!(cert.gramian_structure.verified_sound);
    assert!(cert.rank1_strictly_negative);
    assert!(cert.strict_strictly_negative);
    assert!(cert.rank1_pivots_nonnegative);
    assert!(cert.strict_pivots_strictly_positive);
    assert!(cert.dual_certificate_psd_certified);
    assert!(cert.fixed_matrix_witness_checked);
    assert!(cert.constructed_matrix_not_psd);
    assert!(cert.complete);
}

#[test]
fn ldlt_refuses_nonrational_and_malformed_inputs() {
    use omega_number_theory::cyclotomic::Cyc24;
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
fn fixed_matrix_report_does_not_claim_dimension_wide_exclusion() {
    let r = solve_quad_sdp_certificate();
    assert!(!r.mub_nonexistence_established);
    assert_eq!(r.scope, "single_synthetic_block_matrix");
    assert!(!verify_gramian_structure(&[]).verified_sound);
}

// ==============================================================================
// MANDATORY NEGATIVE CONTROL TESTS (Target A4 / Target 5)
// ==============================================================================

#[test]
fn test_negative_control_perturbed_witness_negative_pivot_rejected() {
    // 1. DualWitnessCyc with negative diagonal weight D_k < 0
    let l = vec![
        vec![Cyc24::rat(BigRational::one()), Cyc24::zero()],
        vec![Cyc24::zero(), Cyc24::rat(BigRational::one())],
    ];
    let d_bad = vec![BigRational::one(), BigRational::new((-1).into(), 5.into())];
    let w_bad = DualWitnessCyc::new(l, d_bad).expect("shape valid");

    assert!(!w_bad.is_valid(), "Witness with D_k < 0 must not be valid");
    let err = w_bad.validate_psd().unwrap_err();
    assert!(
        err.contains("Negative pivot"),
        "Expected Negative pivot error, got: {err}"
    );

    let dummy_g = vec![
        vec![Cyc24::rat(BigRational::one()), Cyc24::zero()],
        vec![Cyc24::zero(), Cyc24::rat(BigRational::one())],
    ];
    assert!(
        w_bad.verify_dual_obstruction(&dummy_g).is_err(),
        "Must refuse obstruction when D_k < 0"
    );

    // 2. Direct matrix with negative pivot rejected by ldlt_pivots_rational
    let bad_mat = vec![
        vec![Cyc24::rat(ri(-1)), Cyc24::zero()],
        vec![Cyc24::zero(), Cyc24::rat(ri(1))],
    ];
    let err_mat = ldlt_pivots_rational(&bad_mat).unwrap_err();
    assert!(
        err_mat.contains("Negative pivot"),
        "Expected Negative pivot error, got: {err_mat}"
    );

    // 3. Perturbed 24x24 dual certificate matrix with a negative pivot
    let mut w_bad24 = dual_certificate_matrix(true);
    w_bad24[0][0] = Cyc24::rat(ri(-5));
    let err24 = ldlt_pivots_rational(&w_bad24).unwrap_err();
    assert!(
        err24.contains("Negative pivot at step 0"),
        "Expected step 0 negative pivot, got: {err24}"
    );
}

#[test]
fn test_negative_control_perturbed_gramian_off_diagonal_modulus_rejected() {
    let g = canonical_quad_gramian();
    let mut g_bad = g.clone();

    // Perturb off-diagonal entry G[0][6] (between Block 0 and Block 1)
    // Set to 1/2 so |1/2|^2 = 1/4 != 1/6
    let half = Cyc24::rat(BigRational::new(1.into(), 2.into()));
    g_bad[0][6] = half.clone();
    g_bad[6][0] = half; // preserve Hermitian symmetry

    let report = verify_gramian_structure(&g_bad);
    assert!(!report.verified_sound);
    assert!(report.diagonal_blocks_identity);
    assert!(!report.off_diagonal_blocks_modulus_sixth);
    assert!(report.hermitian_exact);
}

#[test]
fn test_negative_control_perturbed_gramian_diagonal_rejected() {
    let g = canonical_quad_gramian();

    // Case A: Perturb diagonal entry G[0][0] from 1 to 2
    let mut g_bad1 = g.clone();
    g_bad1[0][0] = Cyc24::rat(ri(2));

    let report1 = verify_gramian_structure(&g_bad1);
    assert!(!report1.verified_sound);
    assert!(!report1.diagonal_blocks_identity);
    assert!(report1.off_diagonal_blocks_modulus_sixth);
    assert!(report1.hermitian_exact);

    // Case B: Perturb off-diagonal entry within diagonal block G[0][1] from 0 to 1/10
    let mut g_bad2 = g.clone();
    let tenth = Cyc24::rat(BigRational::new(1.into(), 10.into()));
    g_bad2[0][1] = tenth.clone();
    g_bad2[1][0] = tenth;

    let report2 = verify_gramian_structure(&g_bad2);
    assert!(!report2.verified_sound);
    assert!(!report2.diagonal_blocks_identity);
    assert!(report2.hermitian_exact);
}

#[test]
fn test_negative_control_non_hermitian_gramian_rejected() {
    let g = canonical_quad_gramian();
    let mut g_bad = g.clone();

    // Perturb G[0][1] without updating G[1][0]
    g_bad[0][1] = Cyc24::rat(BigRational::new(1.into(), 4.into()));

    let report = verify_gramian_structure(&g_bad);
    assert!(!report.verified_sound);
    assert!(!report.hermitian_exact);

    let err = ldlt_pivots_rational(&g_bad).unwrap_err();
    assert!(
        err.contains("not Hermitian"),
        "Expected not Hermitian error, got: {err}"
    );
}

#[test]
fn test_negative_control_non_psd_gramian_fails_ldlt() {
    // 1. Canonical synthetic quad Gramian G is non-PSD, failing with indefinite minor
    let g = canonical_quad_gramian();
    let err = ldlt_pivots_rational(&g).unwrap_err();
    assert!(
        err.contains("Indefinite 2x2 minor"),
        "Expected Indefinite 2x2 minor error, got: {err}"
    );
    assert!(!is_psd_cyc(&g));

    // 2. Indefinite candidate block with off-diagonal coupling > diagonal
    let non_psd_block = vec![
        vec![Cyc24::rat(ri(1)), Cyc24::rat(ri(2))],
        vec![Cyc24::rat(ri(2)), Cyc24::rat(ri(1))],
    ];
    let err_block = ldlt_pivots_rational(&non_psd_block).unwrap_err();
    assert!(
        err_block.contains("Negative pivot"),
        "Expected Negative pivot error, got: {err_block}"
    );
    assert!(!is_psd_cyc(&non_psd_block));

    // 3. Perturbed Gramian with negative diagonal entry
    let mut g_neg_diag = canonical_quad_gramian();
    g_neg_diag[0][0] = Cyc24::rat(ri(-1));
    let err_diag = ldlt_pivots_rational(&g_neg_diag).unwrap_err();
    assert!(
        err_diag.contains("Negative pivot at step 0"),
        "Expected step 0 negative pivot, got: {err_diag}"
    );
    assert!(!is_psd_cyc(&g_neg_diag));
}

#[test]
fn test_valid_genuine_gramian_cannot_be_falsely_obstructed() {
    // Construct genuine Gram matrix from 6 standard basis vectors
    let mut basis = Vec::with_capacity(6);
    for i in 0..6 {
        let mut v = vec![Cyc24::zero(); 6];
        v[i] = Cyc24::rat(BigRational::one());
        basis.push(v);
    }
    let g_genuine = compute_gram_matrix_cyc(&basis).expect("gram matrix computation succeeds");
    assert!(is_psd_cyc(&g_genuine), "Genuine Gram matrix must be PSD");

    // Any valid dual witness W = L D L^\dagger with D >= 0 MUST yield Tr(W * G) >= 0
    let w_valid = DualWitnessCyc::from_cols(
        vec![
            vec![
                Cyc24::rat(ri(1)),
                Cyc24::zero(),
                Cyc24::zero(),
                Cyc24::zero(),
                Cyc24::zero(),
                Cyc24::zero(),
            ],
            vec![
                Cyc24::zero(),
                Cyc24::rat(ri(2)),
                Cyc24::zero(),
                Cyc24::zero(),
                Cyc24::zero(),
                Cyc24::zero(),
            ],
        ],
        vec![BigRational::one(), BigRational::new(3.into(), 2.into())],
    )
    .expect("valid witness");

    assert!(w_valid.is_valid());
    let tr = w_valid
        .trace_inner(&g_genuine)
        .expect("trace inner succeeds");
    let tr_rat = exact_rational(&tr).expect("trace must be rational");
    assert!(
        tr_rat >= BigRational::zero(),
        "Tr(W * G_genuine) must be non-negative"
    );

    let obstructed = w_valid
        .verify_dual_obstruction(&g_genuine)
        .expect("obstruction check succeeds");
    assert!(
        !obstructed,
        "Genuine PSD Gramian must NEVER be certified as obstructed"
    );
}

#[test]
fn test_checked_trace_inner_product_dimension_checks() {
    let one = Cyc24::rat(BigRational::one());
    let m1 = vec![vec![one.clone()]];
    let m2 = vec![vec![one.clone(), one.clone()], vec![one.clone(), one]];

    // Mismatched dimensions
    assert!(checked_trace_inner_product(&m1, &m2).is_err());

    // Empty matrix
    assert!(checked_trace_inner_product(&[], &[]).is_err());
}
