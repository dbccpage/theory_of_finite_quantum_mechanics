//! Exact diagnostics and negative controls for Target Q4 Degree-8 Moment SDP Relaxation.
//! AuthorityEffect: None.

use linear_algebra::exact_ldlt::{
    ldlt_decomposition_rational, ldlt_pivots_strictly_positive_rational,
};
use num_rational::BigRational;
use num_traits::{One, Zero};

use omega_mub::omega_native::exact::mub6_degree2_sdp::build_block_diagonal_gramian;
use omega_mub::omega_native::exact::mub6_degree8_sdp::{
    build_degree8_extended_diagnostic_matrix, build_degree8_extended_moment_matrix,
    build_degree8_invariant_diagnostic_matrix, build_degree8_invariant_moment_matrix,
    build_extended_dual_witness_s6, build_invariant_dual_witness_x0,
    evaluate_target_q4_diagnostics, get_basis_pairs, get_basis_quadruples, get_basis_triples,
    solve_target_q4_degree8_certificate, DEG8_EXTENDED_DIM, DEG8_INVARIANT_DIM, SCHEMA_VERSION,
    SCOPE_STRING,
};
use omega_mub::omega_native::exact::mub6_firewall::{AUTHORITY_EFFECT, FIREWALL};
use omega_mub::omega_native::exact::mub6_quad_sdp::canonical_quad_gramian;

#[test]
fn test_basis_monomial_indexers() {
    let pairs = get_basis_pairs();
    assert_eq!(pairs.len(), 6);
    assert_eq!(pairs, vec![(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]);

    let triples = get_basis_triples();
    assert_eq!(triples.len(), 4);
    assert_eq!(triples, vec![(0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)]);

    let quadruples = get_basis_quadruples();
    assert_eq!(quadruples.len(), 1);
    assert_eq!(quadruples, vec![(0, 1, 2, 3)]);
}

#[test]
fn test_degree8_invariant_moment_matrix_shape() {
    let g_diag = build_block_diagonal_gramian();
    let m8_inv =
        build_degree8_invariant_diagnostic_matrix(&g_diag).expect("M_8^{inv} build failed");

    assert_eq!(m8_inv.len(), DEG8_INVARIANT_DIM);
    assert_eq!(m8_inv[0].len(), DEG8_INVARIANT_DIM);

    // Exact rational symmetry
    for i in 0..DEG8_INVARIANT_DIM {
        for j in 0..DEG8_INVARIANT_DIM {
            assert_eq!(m8_inv[i][j], m8_inv[j][i], "Asymmetry at ({i}, {j})");
        }
    }

    assert_eq!(m8_inv[0][0], BigRational::one());
    for a in 0..4 {
        assert_eq!(m8_inv[0][1 + a], BigRational::one());
        assert_eq!(m8_inv[1 + a][1 + a], BigRational::one());
    }

    // Quadruple entry symmetry with identity
    assert_eq!(m8_inv[0][21], m8_inv[21][0]);
}

#[test]
fn test_degree8_extended_moment_matrix_shape() {
    let g_synth = canonical_quad_gramian();
    let m8_ext =
        build_degree8_extended_diagnostic_matrix(&g_synth).expect("M_8^{ext} build failed");

    assert_eq!(m8_ext.len(), DEG8_EXTENDED_DIM);
    assert_eq!(m8_ext[0].len(), DEG8_EXTENDED_DIM);

    for i in 0..DEG8_EXTENDED_DIM {
        for j in 0..DEG8_EXTENDED_DIM {
            assert_eq!(m8_ext[i][j], m8_ext[j][i], "Asymmetry at ({i}, {j})");
        }
    }

    assert_eq!(m8_ext[0][0], BigRational::one());
    assert_eq!(m8_ext[0][35], m8_ext[35][0]);
    assert!(m8_ext[35][35] > BigRational::zero());
}

#[test]
fn test_invariant_dual_witness_x0_strictly_negative_trace() {
    let g_diag = build_block_diagonal_gramian();
    let m8_inv =
        build_degree8_invariant_diagnostic_matrix(&g_diag).expect("M_8^{inv} build failed");

    let w8_inv = build_invariant_dual_witness_x0(true);
    let tr = w8_inv.trace_inner(&m8_inv).expect("trace failed");

    assert!(tr < BigRational::zero(), "Expected Tr < 0, got {tr}");

    let w_mat = w8_inv.to_full_matrix().expect("full matrix failed");
    let pivots = ldlt_pivots_strictly_positive_rational(&w_mat).expect("pivots failed");
    assert_eq!(pivots.len(), DEG8_INVARIANT_DIM);
    for (idx, p) in pivots.iter().enumerate() {
        assert!(p > &BigRational::zero(), "Pivot at {idx} <= 0: {p}");
    }
}

#[test]
fn test_extended_dual_witness_s6_strictly_negative_trace() {
    let g_synth = canonical_quad_gramian();
    let m8_ext =
        build_degree8_extended_diagnostic_matrix(&g_synth).expect("M_8^{ext} build failed");

    let w8_ext = build_extended_dual_witness_s6(true);
    let tr = w8_ext.trace_inner(&m8_ext).expect("trace failed");

    assert!(tr < BigRational::zero(), "Expected Tr < 0, got {tr}");

    let w_mat = w8_ext.to_full_matrix().expect("full matrix failed");
    let pivots = ldlt_pivots_strictly_positive_rational(&w_mat).expect("pivots failed");
    assert_eq!(pivots.len(), DEG8_EXTENDED_DIM);
    for (idx, p) in pivots.iter().enumerate() {
        assert!(p > &BigRational::zero(), "Pivot at {idx} <= 0: {p}");
    }
}

#[test]
fn test_evaluate_target_q4_diagnostics_structure() {
    let cert = evaluate_target_q4_diagnostics().expect("diagnostics failed");

    assert_eq!(cert.schema_version, SCHEMA_VERSION);
    assert_eq!(cert.firewall, FIREWALL);
    assert_eq!(cert.authority_effect, AUTHORITY_EFFECT);
    assert_eq!(cert.scope, SCOPE_STRING);
    assert_eq!(cert.invariant_dim, DEG8_INVARIANT_DIM);
    assert_eq!(cert.extended_dim, DEG8_EXTENDED_DIM);

    assert!(cert.receipt_x0.strictly_negative);
    assert!(cert.receipt_x0.pivots_strictly_positive);
    assert_eq!(cert.receipt_x0.pivots.len(), DEG8_INVARIANT_DIM);

    assert!(cert.receipt_s6.strictly_negative);
    assert!(cert.receipt_s6.pivots_strictly_positive);
    assert_eq!(cert.receipt_s6.pivots.len(), DEG8_EXTENDED_DIM);

    assert!(!cert.complete);
    assert!(cert.diagnostics_complete);
    assert!(!cert.moment_semantics_verified);
    assert!(!cert.moment_report.candidate_x0_refuted);
    assert!(!cert.moment_report.candidate_s6_refuted);
}

#[test]
fn test_certification_apis_refuse_missing_moment_semantics() {
    let g = canonical_quad_gramian();
    assert!(build_degree8_invariant_moment_matrix(&g).is_err());
    assert!(build_degree8_extended_moment_matrix(&g).is_err());
    assert!(solve_target_q4_degree8_certificate().is_err());
}

#[test]
fn test_negative_control_non_symmetric_rejected() {
    let m_bad = vec![
        vec![BigRational::one(), BigRational::new(2.into(), 1.into())],
        vec![BigRational::zero(), BigRational::one()],
    ];
    let res = ldlt_decomposition_rational(&m_bad);
    assert!(res.is_err());
    assert!(res.unwrap_err().contains("not symmetric"));
}

#[test]
fn test_negative_control_indefinite_pivots_rejected() {
    let m_indef = vec![
        vec![BigRational::one(), BigRational::new(2.into(), 1.into())],
        vec![BigRational::new(2.into(), 1.into()), BigRational::one()],
    ];
    let res = ldlt_pivots_strictly_positive_rational(&m_indef);
    assert!(res.is_err());
    assert!(res.unwrap_err().contains("not strictly positive"));
}

#[test]
fn test_negative_control_invalid_gramian_dim_rejected() {
    let bad_g = vec![vec![]; 20];
    let res_inv = build_degree8_invariant_diagnostic_matrix(&bad_g);
    assert!(res_inv.is_err());
    assert!(res_inv
        .unwrap_err()
        .contains("Gramian dimension must be 24x24"));

    let res_ext = build_degree8_extended_diagnostic_matrix(&bad_g);
    assert!(res_ext.is_err());
    assert!(res_ext
        .unwrap_err()
        .contains("Gramian dimension must be 24x24"));
}

#[test]
fn test_negative_control_empty_matrix_rejected() {
    let empty: Vec<Vec<BigRational>> = vec![];
    let res = ldlt_decomposition_rational(&empty);
    assert!(res.is_err());
    assert!(res.unwrap_err().contains("non-empty and square"));
}
