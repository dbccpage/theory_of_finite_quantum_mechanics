//! Exact diagnostics and negative controls for Target Q2 Degree-4 Moment SDP Relaxation.
//! AuthorityEffect: None.

use linear_algebra::exact_ldlt::{
    ldlt_decomposition_rational, ldlt_pivots_strictly_positive_rational,
};
use num_rational::BigRational;
use num_traits::{One, Zero};

use omega_mub::omega_native::exact::mub6_degree2_sdp::build_block_diagonal_gramian;
use omega_mub::omega_native::exact::mub6_degree4_sdp::{
    build_degree4_extended_moment_matrix, build_degree4_invariant_moment_matrix,
    build_extended_dual_witness_s6, build_invariant_dual_witness_x0, get_basis_pairs,
    solve_target_q2_degree4_certificate, DEG4_EXTENDED_DIM, DEG4_INVARIANT_DIM, SCHEMA_VERSION,
    SCOPE_STRING,
};
use omega_mub::omega_native::exact::mub6_firewall::{AUTHORITY_EFFECT, FIREWALL};
use omega_mub::omega_native::exact::mub6_quad_sdp::canonical_quad_gramian;

#[test]
fn test_basis_pairs_structure() {
    let pairs = get_basis_pairs();
    assert_eq!(pairs.len(), 6);
    assert_eq!(pairs, vec![(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]);
}

#[test]
fn test_degree4_invariant_moment_matrix_shape() {
    let g_diag = build_block_diagonal_gramian();
    let m4_inv = build_degree4_invariant_moment_matrix(&g_diag).expect("M_4^{inv} build failed");

    assert_eq!(m4_inv.len(), DEG4_INVARIANT_DIM);
    assert_eq!(m4_inv[0].len(), DEG4_INVARIANT_DIM);

    // Exact rational symmetry
    for i in 0..DEG4_INVARIANT_DIM {
        for j in 0..DEG4_INVARIANT_DIM {
            assert_eq!(m4_inv[i][j], m4_inv[j][i], "Asymmetry at ({i}, {j})");
        }
    }

    assert_eq!(m4_inv[0][0], BigRational::one());
    for a in 0..4 {
        assert_eq!(m4_inv[0][1 + a], BigRational::one());
        assert_eq!(m4_inv[1 + a][1 + a], BigRational::one());
    }
}

#[test]
fn test_degree4_extended_moment_matrix_shape() {
    let g_diag = build_block_diagonal_gramian();
    let m4_ext = build_degree4_extended_moment_matrix(&g_diag).expect("M_4^{ext} build failed");

    assert_eq!(m4_ext.len(), DEG4_EXTENDED_DIM);
    assert_eq!(m4_ext[0].len(), DEG4_EXTENDED_DIM);

    for i in 0..DEG4_EXTENDED_DIM {
        for j in 0..DEG4_EXTENDED_DIM {
            assert_eq!(m4_ext[i][j], m4_ext[j][i], "Asymmetry at ({i}, {j})");
        }
    }

    assert_eq!(m4_ext[0][0], BigRational::one());
}

#[test]
fn test_invariant_dual_witness_x0_strictly_negative_trace() {
    let g_diag = build_block_diagonal_gramian();
    let m4_inv = build_degree4_invariant_moment_matrix(&g_diag).expect("M_4^{inv} build failed");

    let w4_inv = build_invariant_dual_witness_x0(true);
    let tr = w4_inv.trace_inner(&m4_inv).expect("trace_inner failed");

    assert!(tr < BigRational::zero(), "Expected Tr < 0, got {tr}");

    let w_mat = w4_inv.to_full_matrix().expect("to_full_matrix failed");
    let pivots = ldlt_pivots_strictly_positive_rational(&w_mat).expect("pivots failed");
    assert_eq!(pivots.len(), DEG4_INVARIANT_DIM);
    for (idx, p) in pivots.iter().enumerate() {
        assert!(p > &BigRational::zero(), "Pivot at {idx} <= 0: {p}");
    }
}

#[test]
fn test_extended_dual_witness_s6_strictly_negative_trace() {
    let g_synth = canonical_quad_gramian();
    let m4_ext = build_degree4_extended_moment_matrix(&g_synth).expect("M_4^{ext} build failed");

    let w4_ext = build_extended_dual_witness_s6(true);
    let tr = w4_ext.trace_inner(&m4_ext).expect("trace_inner failed");

    assert!(tr < BigRational::zero(), "Expected Tr < 0, got {tr}");

    let w_mat = w4_ext.to_full_matrix().expect("to_full_matrix failed");
    let pivots = ldlt_pivots_strictly_positive_rational(&w_mat).expect("pivots failed");
    assert_eq!(pivots.len(), DEG4_EXTENDED_DIM);
    for (idx, p) in pivots.iter().enumerate() {
        assert!(p > &BigRational::zero(), "Pivot at {idx} <= 0: {p}");
    }
}

#[test]
fn test_solve_target_q2_degree4_certificate_complete() {
    let cert = solve_target_q2_degree4_certificate().expect("solve failed");

    assert_eq!(cert.schema_version, SCHEMA_VERSION);
    assert_eq!(cert.firewall, FIREWALL);
    assert_eq!(cert.authority_effect, AUTHORITY_EFFECT);
    assert_eq!(cert.scope, SCOPE_STRING);
    assert_eq!(cert.invariant_dim, DEG4_INVARIANT_DIM);
    assert_eq!(cert.extended_dim, DEG4_EXTENDED_DIM);

    assert!(cert.receipt_x0.strictly_negative);
    assert!(cert.receipt_x0.pivots_strictly_positive);
    assert_eq!(cert.receipt_x0.pivots.len(), DEG4_INVARIANT_DIM);

    assert!(cert.receipt_s6.strictly_negative);
    assert!(cert.receipt_s6.pivots_strictly_positive);
    assert_eq!(cert.receipt_s6.pivots.len(), DEG4_EXTENDED_DIM);

    assert!(cert.complete);
}

#[test]
fn test_negative_control_non_symmetric_rejected() {
    let m_bad = vec![
        vec![BigRational::one(), BigRational::from_integer(2.into())],
        vec![BigRational::zero(), BigRational::one()],
    ];
    let res = ldlt_decomposition_rational(&m_bad);
    assert!(res.is_err());
    assert!(res.unwrap_err().contains("not symmetric"));
}

#[test]
fn test_negative_control_indefinite_pivots_rejected() {
    let m_indef = vec![
        vec![BigRational::one(), BigRational::from_integer(2.into())],
        vec![BigRational::from_integer(2.into()), BigRational::one()],
    ];
    let res = ldlt_pivots_strictly_positive_rational(&m_indef);
    assert!(res.is_err());
    assert!(res.unwrap_err().contains("not strictly positive"));
}
