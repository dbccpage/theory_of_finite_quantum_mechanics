//! Exact diagnostics and negative controls for Target Q1 Degree-2 SDP Moment Relaxation.
//! AuthorityEffect: None.

use linear_algebra::exact_ldlt::{
    ldlt_decomposition_rational, ldlt_pivots_strictly_positive_rational,
};
use num_rational::BigRational;
use num_traits::{One, Zero};

use omega_mub::omega_native::exact::mub6_degree2_sdp::{
    build_block_diag_dual_witness, build_block_diagonal_gramian,
    build_degree2_projector_moment_matrix, solve_target_q1_degree2_certificate,
    verify_pairwise_cross_ratios, DIM_HILBERT, GRAMIAN_DIM, MOMENT_DIM, SCHEMA_VERSION,
    SCOPE_STRING,
};
use omega_mub::omega_native::exact::mub6_firewall::{AUTHORITY_EFFECT, FIREWALL};
use omega_mub::omega_native::exact::mub6_quad_sdp::{
    canonical_quad_gramian, dual_certificate_matrix, exact_rational, ldlt_pivots_rational,
    trace_inner_product,
};
use omega_number_theory::cyclotomic::Cyc24;

#[test]
fn test_degree2_moment_matrix_dimensions_and_structure() {
    let g_diag = build_block_diagonal_gramian();
    let m2 = build_degree2_projector_moment_matrix(&g_diag).expect("M_2(G_diag) build failed");

    assert_eq!(m2.len(), MOMENT_DIM);
    assert_eq!(m2[0].len(), MOMENT_DIM);

    // Row 0: identity expectation 1
    assert_eq!(m2[0][0], BigRational::one());

    // Diagonal elements: row 0 is 1, rows 1..24 are 1/6
    let sixth = BigRational::new(1.into(), 6.into());
    for idx in 1..MOMENT_DIM {
        assert_eq!(m2[0][idx], sixth);
        assert_eq!(m2[idx][0], sixth);
        assert_eq!(m2[idx][idx], sixth);
    }

    // Exact rational symmetry
    for i in 0..MOMENT_DIM {
        for j in 0..MOMENT_DIM {
            assert_eq!(m2[i][j], m2[j][i], "Asymmetry at ({i}, {j})");
        }
    }
}

#[test]
fn test_pairwise_cross_ratios_canonical_triple() {
    let g_diag = build_block_diagonal_gramian();
    let report = verify_pairwise_cross_ratios(&g_diag);

    // Canonical triple pairs (0, 1), (0, 2), (1, 2) must be sound
    let triple_pairs = [(0, 1), (0, 2), (1, 2)];
    let mut found = 0;
    for summary in &report.pair_summaries {
        if triple_pairs.contains(&(summary.basis_a, summary.basis_b)) {
            assert_eq!(summary.total_submatrices, 225);
            assert!(summary.all_modulus_thirty_sixth);
            assert!(summary.all_normalized_modulus_one);
            assert_eq!(summary.violations_count, 0);
            found += 1;
        }
    }
    assert_eq!(found, 3);
}

#[test]
fn test_pairwise_cross_ratios_synthetic_s6() {
    let g_synth = canonical_quad_gramian();
    let report = verify_pairwise_cross_ratios(&g_synth);

    assert_eq!(report.total_pairs, 6);
    assert_eq!(report.total_cross_ratios_evaluated, 6 * 225);
    assert!(report.all_pairs_sound);
    for summary in &report.pair_summaries {
        assert!(summary.all_modulus_thirty_sixth);
        assert_eq!(summary.violations_count, 0);
    }
}

#[test]
fn test_block_diagonal_completion_violates_modulus() {
    let g_diag = build_block_diagonal_gramian();
    let m2 = build_degree2_projector_moment_matrix(&g_diag).expect("M_2 build failed");

    // For X = 0, cross-terms between basis 0 and basis 3 are zero
    for i in 0..DIM_HILBERT {
        for j in 0..DIM_HILBERT {
            let row_idx = 0 * DIM_HILBERT + i + 1;
            let col_idx = 3 * DIM_HILBERT + j + 1;
            assert_eq!(m2[row_idx][col_idx], BigRational::zero());
        }
    }
}

#[test]
fn test_block_diagonal_dual_witness_strictly_negative_trace() {
    let g_diag = build_block_diagonal_gramian();
    let m2_diag = build_degree2_projector_moment_matrix(&g_diag).expect("M_2 build failed");

    let w2_rank1 = build_block_diag_dual_witness(false);
    assert!(w2_rank1.is_valid());

    let tr = w2_rank1.trace_inner(&m2_diag).expect("trace failed");
    assert_eq!(tr, BigRational::new((-1).into(), 2.into()));
    assert!(tr < BigRational::zero());
}

#[test]
fn test_block_diagonal_strict_dual_witness_all_pivots_positive() {
    let g_diag = build_block_diagonal_gramian();
    let m2_diag = build_degree2_projector_moment_matrix(&g_diag).expect("M_2 build failed");

    let w2_strict = build_block_diag_dual_witness(true);
    assert!(w2_strict.is_valid());

    let tr = w2_strict.trace_inner(&m2_diag).expect("trace failed");
    assert_eq!(tr, BigRational::new((-9).into(), 20.into()));
    assert!(tr < BigRational::zero());

    let w_mat = w2_strict.to_full_matrix().unwrap();
    let pivots = ldlt_pivots_strictly_positive_rational(&w_mat)
        .expect("Strict dual witness must have positive pivots");
    assert_eq!(pivots.len(), MOMENT_DIM);
    assert!(pivots.iter().all(|p| p > &BigRational::zero()));
}

#[test]
fn test_synthetic_s6_dual_witness_strictly_negative_trace() {
    let g_synth = canonical_quad_gramian();

    // Rank-1 witness: Tr(W * G) = -7
    let w_rank1 = dual_certificate_matrix(false);
    let inner_rank1 = trace_inner_product(&w_rank1, &g_synth);
    let rat_rank1 = exact_rational(&inner_rank1).expect("trace must be rational");
    assert_eq!(rat_rank1, BigRational::from_integer((-7).into()));

    // Strict witness: Tr(W_strict * G) = -6
    let w_strict = dual_certificate_matrix(true);
    let inner_strict = trace_inner_product(&w_strict, &g_synth);
    let rat_strict = exact_rational(&inner_strict).expect("trace must be rational");
    assert_eq!(rat_strict, BigRational::from_integer((-6).into()));
}

#[test]
fn test_synthetic_s6_strict_witness_all_pivots_positive() {
    let w_strict = dual_certificate_matrix(true);
    let pivots = ldlt_pivots_rational(&w_strict).expect("LDL^T failed for W_strict");
    assert_eq!(pivots.len(), GRAMIAN_DIM);
    assert!(pivots.iter().all(|p| p > &BigRational::zero()));
}

#[test]
fn test_solve_target_q1_degree2_certificate_complete() {
    let cert = solve_target_q1_degree2_certificate();

    assert_eq!(cert.schema_version, SCHEMA_VERSION);
    assert_eq!(cert.firewall, FIREWALL);
    assert_eq!(cert.authority_effect, AUTHORITY_EFFECT);
    assert_eq!(cert.scope, SCOPE_STRING);
    assert_eq!(cert.dimension, 6);
    assert_eq!(cert.bases_count, 4);
    assert_eq!(cert.gramian_dim, 24);
    assert_eq!(cert.moment_dim, 25);
    assert!(cert.complete);

    assert!(cert.receipt_violating_modulus_x0.strictly_negative);
    assert!(cert.receipt_violating_modulus_x0.pivots_strictly_positive);
    assert_eq!(cert.receipt_violating_modulus_x0.inner_product, "-9/20");

    assert!(cert.receipt_violating_psd_s6.strictly_negative);
    assert!(cert.receipt_violating_psd_s6.pivots_strictly_positive);
    assert_eq!(cert.receipt_violating_psd_s6.inner_product, "-6");
}

#[test]
fn test_negative_control_perturbed_modulus_cross_ratio_rejection() {
    let g = canonical_quad_gramian();
    let delta = Cyc24::rat(BigRational::new(1.into(), 10.into()));
    let mut g_mut = g.clone();
    g_mut[0][18] = g_mut[0][18].add(&delta);
    g_mut[18][0] = g_mut[0][18].conj();

    let report = verify_pairwise_cross_ratios(&g_mut);
    assert!(!report.all_pairs_sound);
    assert!(report.pair_summaries.iter().any(|s| s.violations_count > 0));
}

#[test]
fn test_negative_control_perturbed_witness_negative_pivot_rejected() {
    let indef_mat = vec![
        vec![BigRational::one(), BigRational::from_integer(2.into())],
        vec![BigRational::from_integer(2.into()), BigRational::one()],
    ];

    let (_, d, is_psd) = ldlt_decomposition_rational(&indef_mat).expect("decomposition succeeds");
    assert!(!is_psd);
    assert!(d[1] < BigRational::zero());

    let result = ldlt_pivots_strictly_positive_rational(&indef_mat);
    assert!(result.is_err());
}

#[test]
fn test_negative_control_non_symmetric_matrix_rejected() {
    let non_sym = vec![
        vec![BigRational::one(), BigRational::from_integer(2.into())],
        vec![BigRational::zero(), BigRational::one()],
    ];
    let result = ldlt_decomposition_rational(&non_sym);
    assert!(result.is_err());
}

#[test]
fn malformed_dual_witnesses_fail_closed() {
    let mut w = build_block_diag_dual_witness(true);
    w.vectors[0].clear();
    assert!(!w.is_valid());
    assert!(w.to_full_matrix().is_err());
    let m = vec![vec![BigRational::from_integer(0.into()); MOMENT_DIM]; MOMENT_DIM];
    assert!(w.trace_inner(&m).is_err());
    let mut negative = build_block_diag_dual_witness(true);
    negative.weights[0] = BigRational::from_integer((-1).into());
    assert!(!negative.is_valid());
    assert!(negative.trace_inner(&m).is_err());
}
