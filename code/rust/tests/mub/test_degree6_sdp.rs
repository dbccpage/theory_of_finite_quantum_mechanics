//! Exact diagnostics and negative controls for Target Q3 Degree-6 Moment SDP Relaxation.
//! AuthorityEffect: None.

use linear_algebra::exact_ldlt::{
    ldlt_decomposition_rational, ldlt_pivots_strictly_positive_rational,
};
use num_rational::BigRational;
use num_traits::{One, Zero};

use tfqm_mub::native::exact::mub6_degree2_sdp::build_block_diagonal_gramian;
use tfqm_mub::native::exact::mub6_degree6_sdp::{
    build_degree6_extended_diagnostic_matrix, build_degree6_invariant_diagnostic_matrix,
    build_extended_dual_witness_s6, build_invariant_dual_witness_x0,
    evaluate_target_q3_diagnostics, get_basis_pairs, get_basis_triples, DEG6_EXTENDED_DIM,
    DEG6_INVARIANT_DIM, SCHEMA_VERSION, SCOPE_STRING,
};
use tfqm_mub::native::exact::mub6_firewall::{AUTHORITY_EFFECT, FIREWALL};
use tfqm_mub::native::exact::mub6_quad_sdp::canonical_quad_gramian;

#[test]
fn test_basis_monomial_indexers() {
    let pairs = get_basis_pairs();
    assert_eq!(pairs.len(), 6);
    assert_eq!(pairs, vec![(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]);

    let triples = get_basis_triples();
    assert_eq!(triples.len(), 4);
    assert_eq!(triples, vec![(0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)]);
}

#[test]
fn test_degree6_invariant_moment_matrix_shape() {
    let g_diag = build_block_diagonal_gramian();
    let m6_inv =
        build_degree6_invariant_diagnostic_matrix(&g_diag).expect("M_6^{inv} build failed");

    assert_eq!(m6_inv.len(), DEG6_INVARIANT_DIM);
    assert_eq!(m6_inv[0].len(), DEG6_INVARIANT_DIM);

    // Exact rational symmetry
    for i in 0..DEG6_INVARIANT_DIM {
        for j in 0..DEG6_INVARIANT_DIM {
            assert_eq!(m6_inv[i][j], m6_inv[j][i], "Asymmetry at ({i}, {j})");
        }
    }

    assert_eq!(m6_inv[0][0], BigRational::one());
    for a in 0..4 {
        assert_eq!(m6_inv[0][1 + a], BigRational::one());
        assert_eq!(m6_inv[1 + a][1 + a], BigRational::one());
    }
}

#[test]
fn test_degree6_extended_moment_matrix_shape() {
    let g_synth = canonical_quad_gramian();
    let m6_ext =
        build_degree6_extended_diagnostic_matrix(&g_synth).expect("M_6^{ext} build failed");

    assert_eq!(m6_ext.len(), DEG6_EXTENDED_DIM);
    assert_eq!(m6_ext[0].len(), DEG6_EXTENDED_DIM);

    for i in 0..DEG6_EXTENDED_DIM {
        for j in 0..DEG6_EXTENDED_DIM {
            assert_eq!(m6_ext[i][j], m6_ext[j][i], "Asymmetry at ({i}, {j})");
        }
    }

    assert_eq!(m6_ext[0][0], BigRational::one());
}

#[test]
fn test_invariant_dual_witness_x0_strictly_negative_trace() {
    let g_diag = build_block_diagonal_gramian();
    let m6_inv =
        build_degree6_invariant_diagnostic_matrix(&g_diag).expect("M_6^{inv} build failed");

    let w6_inv = build_invariant_dual_witness_x0(true);
    let tr = w6_inv.trace_inner(&m6_inv).unwrap();

    assert!(tr < BigRational::zero(), "Expected Tr < 0, got {tr}");

    let w_mat = w6_inv.to_full_matrix().unwrap();
    let pivots = ldlt_pivots_strictly_positive_rational(&w_mat).expect("pivots failed");
    assert_eq!(pivots.len(), DEG6_INVARIANT_DIM);
    for (idx, p) in pivots.iter().enumerate() {
        assert!(p > &BigRational::zero(), "Pivot at {idx} <= 0: {p}");
    }
}

#[test]
fn test_extended_dual_witness_s6_strictly_negative_trace() {
    let g_synth = canonical_quad_gramian();
    let m6_ext =
        build_degree6_extended_diagnostic_matrix(&g_synth).expect("M_6^{ext} build failed");

    let w6_ext = build_extended_dual_witness_s6(true);
    let tr = w6_ext.trace_inner(&m6_ext).unwrap();

    assert!(tr < BigRational::zero(), "Expected Tr < 0, got {tr}");

    let w_mat = w6_ext.to_full_matrix().unwrap();
    let pivots = ldlt_pivots_strictly_positive_rational(&w_mat).expect("pivots failed");
    assert_eq!(pivots.len(), DEG6_EXTENDED_DIM);
    for (idx, p) in pivots.iter().enumerate() {
        assert!(p > &BigRational::zero(), "Pivot at {idx} <= 0: {p}");
    }
}

#[test]
fn test_evaluate_target_q3_diagnostics_complete() {
    let cert = evaluate_target_q3_diagnostics().expect("solve failed");

    assert_eq!(cert.schema_version, SCHEMA_VERSION);
    assert_eq!(cert.firewall, FIREWALL);
    assert_eq!(cert.authority_effect, AUTHORITY_EFFECT);
    assert_eq!(cert.scope, SCOPE_STRING);
    assert_eq!(cert.invariant_dim, DEG6_INVARIANT_DIM);
    assert_eq!(cert.extended_dim, DEG6_EXTENDED_DIM);

    assert!(cert.receipt_x0.strictly_negative);
    assert!(cert.receipt_x0.pivots_strictly_positive);
    assert_eq!(cert.receipt_x0.pivots.len(), DEG6_INVARIANT_DIM);

    assert!(cert.receipt_s6.strictly_negative);
    assert!(cert.receipt_s6.pivots_strictly_positive);
    assert_eq!(cert.receipt_s6.pivots.len(), DEG6_EXTENDED_DIM);

    assert!(!cert.complete);
    assert!(cert.diagnostics_complete);
    assert!(!cert.moment_semantics_verified);
    assert!(!cert.moment_report.candidate_x0_refuted);
    assert!(!cert.moment_report.candidate_s6_refuted);
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

fn repeated_basis_gramian() -> Vec<Vec<omega_number_theory::cyclotomic::Cyc24>> {
    use omega_number_theory::cyclotomic::Cyc24;
    (0..24)
        .map(|i| {
            (0..24)
                .map(|j| {
                    if i % 6 == j % 6 {
                        Cyc24::rat(BigRational::one())
                    } else {
                        Cyc24::zero()
                    }
                })
                .collect()
        })
        .collect()
}

#[test]
fn nonrational_real_part_is_rejected() {
    use tfqm_mub::native::exact::mub6_degree6_sdp as q;
    use omega_number_theory::cyclotomic::Cyc24;
    let sqrt3 = Cyc24::zeta24(2).add(&Cyc24::zeta24(-2));
    assert!(q::cyc_real_rational(&sqrt3).is_err());
    assert!(q::cyc_real_constant_coefficient(&sqrt3).is_zero());
    assert_eq!(
        q::cyc_real_rational(&Cyc24::rat(BigRational::one())).unwrap(),
        BigRational::one()
    );
}

#[test]
fn certification_requires_missing_moment_semantics() {
    use tfqm_mub::native::exact::mub6_degree6_sdp as q;
    let g = repeated_basis_gramian();
    assert!(q::solve_target_q3_degree6_certificate()
        .unwrap_err()
        .contains("MissingProofObligation"));
    assert!(q::build_degree6_invariant_moment_matrix(&g).is_err());
    assert!(q::build_degree6_extended_moment_matrix(&g).is_err());
    for (m, idx) in [
        (
            q::build_degree6_invariant_diagnostic_matrix(&g).unwrap(),
            [0, 5, 19],
        ),
        (
            q::build_degree6_extended_diagnostic_matrix(&g).unwrap(),
            [0, 25, 26],
        ),
    ] {
        let z = [-1, 1, 1];
        let mut value = BigRational::zero();
        for i in 0..3 {
            for j in 0..3 {
                value += &m[idx[i]][idx[j]] * BigRational::from_integer((z[i] * z[j]).into());
            }
        }
        assert_eq!(value, -BigRational::one());
    }
}

#[test]
fn malformed_witnesses_are_rejected_on_every_operation() {
    let mut w = build_invariant_dual_witness_x0(true);
    let m = w.to_full_matrix().unwrap();
    w.weights[0] = -BigRational::one();
    assert!(w.to_full_matrix().is_err());
    assert!(w.trace_inner(&m).is_err());
    w.weights[0] = BigRational::one();
    w.vectors[0].pop();
    assert!(w.to_full_matrix().is_err());
    assert!(w.trace_inner(&m).is_err());
    assert!(build_invariant_dual_witness_x0(true)
        .trace_inner(&[])
        .is_err());
}

#[test]
fn singular_ldlt_reconstructs_and_zero_pivot_defect_rejects() {
    let one = BigRational::one();
    let zero = BigRational::zero();
    for m in [
        vec![
            vec![one.clone(), one.clone()],
            vec![one.clone(), one.clone()],
        ],
        vec![
            vec![zero.clone(), zero.clone()],
            vec![zero.clone(), one.clone()],
        ],
    ] {
        let (l, d, ok) = ldlt_decomposition_rational(&m).unwrap();
        assert!(ok);
        for i in 0..2 {
            for j in 0..2 {
                let reconstructed: BigRational = (0..2).map(|k| &l[i][k] * &d[k] * &l[j][k]).sum();
                assert_eq!(reconstructed, m[i][j]);
            }
        }
    }
    assert!(
        !ldlt_decomposition_rational(&[vec![zero.clone(), one.clone()], vec![one, zero]])
            .unwrap()
            .2
    );
}

#[test]
fn every_diagnostic_entry_matches_python_fixtures() {
    use sha2::{Digest, Sha256};
    let fixtures: serde_json::Value =
        serde_json::from_str(include_str!("fixtures/pr60_degree6_diagnostics.json")).unwrap();
    for (name, g) in [
        ("x0", build_block_diagonal_gramian()),
        ("s6", canonical_quad_gramian()),
        ("repeated", repeated_basis_gramian()),
    ] {
        for (label, m) in [
            (
                "invariant",
                build_degree6_invariant_diagnostic_matrix(&g).unwrap(),
            ),
            (
                "extended",
                build_degree6_extended_diagnostic_matrix(&g).unwrap(),
            ),
        ] {
            let payload: String = m
                .iter()
                .flatten()
                .map(|v| format!("{}/{}\n", v.numer(), v.denom()))
                .collect();
            let digest = format!("{:x}", Sha256::digest(payload.as_bytes()));
            assert_eq!(
                fixtures[format!("{}_{}", name, label)].as_str().unwrap(),
                digest,
                "{} {}",
                name,
                label
            );
        }
    }
}
