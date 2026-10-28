//! Integration tests for Target A7: Exact ZeroRel Algebraic Variety & Curvature Certifier.
//!
//! AuthorityEffect: None

use num_rational::BigRational;
use num_traits::Zero;

use tfqm_mub::native::exact::d6_exact_curvature_cochain::D;
use tfqm_mub::native::exact::mub6_f6_chart::f6_family_columns;
use tfqm_mub::native::exact::mub6_matrix6::Matrix6;
use tfqm_mub::native::exact::mub6_zerorel_variety::{
    dita_representative_triple, eval_all_zerorel_residuals, eval_artin_schreier_curvature,
    margin_dita, margin_szollosi, margin_tao, standard_basis, szollosi_representative_triple,
    tao_representative_triple, verify_curvature_bound, verify_unitary_gauge_invariance, BasisCyc,
    TOTAL_ZEROREL_EQUATIONS,
};
use omega_number_theory::cyclotomic::Cyc24;
use omega_number_theory::rational::rq;

/// Helper: construct candidate fourth basis test matrices.
/// Candidate 1: phase-modulated Fourier basis columns.
fn candidate_basis_f6_shifted() -> BasisCyc {
    f6_family_columns(2, 4)
}

/// Helper: construct a non-trivial unitary transformation V in U(6) over Cyc24.
fn test_unitary_v() -> Matrix6 {
    // Diagonal unitary with root-of-unity phases
    std::array::from_fn(|r| {
        std::array::from_fn(|c| {
            if r == c {
                Cyc24::zeta24(((r * 4) % 24) as i32)
            } else {
                Cyc24::zero()
            }
        })
    })
}

#[test]
fn test_exact_108_equation_count() {
    assert_eq!(TOTAL_ZEROREL_EQUATIONS, 108);

    let t_dita = dita_representative_triple();
    let cand = candidate_basis_f6_shifted();

    let residuals = eval_all_zerorel_residuals(&t_dita, &cand);
    assert_eq!(residuals.len(), 108);

    // Verify all bases 0, 1, 2 are present
    let mut count_b0 = 0;
    let mut count_b1 = 0;
    let mut count_b2 = 0;
    for (rel, _) in &residuals {
        match rel.basis {
            0 => count_b0 += 1,
            1 => count_b1 += 1,
            2 => count_b2 += 1,
            _ => panic!("invalid basis index"),
        }
    }
    assert_eq!(count_b0, 36);
    assert_eq!(count_b1, 36);
    assert_eq!(count_b2, 36);
}

#[test]
fn test_standard_basis_orthonormality() {
    let b0 = standard_basis();
    assert_eq!(b0.len(), D);
    for col in 0..D {
        assert_eq!(b0[col][col], Cyc24::zeta24(0));
        for row in 0..D {
            if row != col {
                assert_eq!(b0[col][row], Cyc24::zero());
            }
        }
    }
}

#[test]
fn test_dita_fourier_curvature_lower_bound() {
    let t_dita = dita_representative_triple();
    let cand = candidate_basis_f6_shifted();

    let psi_sq = eval_artin_schreier_curvature(&t_dita, &cand);
    assert!(
        psi_sq > BigRational::zero(),
        "Psi^sq must be strictly positive"
    );

    let eps_dita = margin_dita();
    assert_eq!(eps_dita, rq(37249, 90000));
    assert!(
        verify_curvature_bound(&t_dita, &cand, &eps_dita),
        "Dita representative must satisfy certified lower bound margin"
    );
}

#[test]
fn test_szollosi_deltoid_curvature_lower_bound() {
    let t_sz = szollosi_representative_triple();
    let cand = candidate_basis_f6_shifted();

    let psi_sq = eval_artin_schreier_curvature(&t_sz, &cand);
    assert!(
        psi_sq > BigRational::zero(),
        "Psi^sq must be strictly positive"
    );

    let eps_sz = margin_szollosi();
    assert_eq!(eps_sz, rq(37249, 90000));
    assert!(
        verify_curvature_bound(&t_sz, &cand, &eps_sz),
        "Szollosi representative must satisfy certified lower bound margin"
    );
}

#[test]
fn test_tao_confluence_curvature_lower_bound() {
    let t_tao = tao_representative_triple();
    let cand = candidate_basis_f6_shifted();

    let psi_sq = eval_artin_schreier_curvature(&t_tao, &cand);
    assert!(
        psi_sq > BigRational::zero(),
        "Psi^sq must be strictly positive"
    );

    let eps_tao = margin_tao();
    assert_eq!(eps_tao, rq(527, 576));
    assert!(
        verify_curvature_bound(&t_tao, &cand, &eps_tao),
        "Tao representative must satisfy certified lower bound margin"
    );
}

#[test]
fn test_unitary_gauge_invariance() {
    let t_dita = dita_representative_triple();
    let cand = candidate_basis_f6_shifted();
    let v = test_unitary_v();

    assert!(
        verify_unitary_gauge_invariance(&t_dita, &cand, &v),
        "Artin-Schreier curvature mass must be invariant under unitary transformation V in U(6)"
    );

    let t_tao = tao_representative_triple();
    assert!(
        verify_unitary_gauge_invariance(&t_tao, &cand, &v),
        "Tao curvature mass must be invariant under unitary transformation V in U(6)"
    );
}

#[test]
fn test_negative_control_non_positive_margin_rejected() {
    let t_dita = dita_representative_triple();
    let cand = candidate_basis_f6_shifted();

    // Zero margin must be rejected
    assert!(
        !verify_curvature_bound(&t_dita, &cand, &BigRational::zero()),
        "Zero margin must be strictly rejected"
    );

    // Negative margin must be rejected
    let neg_margin = rq(-1, 100);
    assert!(
        !verify_curvature_bound(&t_dita, &cand, &neg_margin),
        "Negative margin must be strictly rejected"
    );

    // Excessively large margin must be rejected
    let huge_margin = rq(1000, 1);
    assert!(
        !verify_curvature_bound(&t_dita, &cand, &huge_margin),
        "Unwarranted excessive margin must be rejected"
    );
}

#[test]
fn test_ast_zero_float_discipline() {
    let src = include_str!("../../omega_mub/src/native/mub6_zerorel_variety.rs");

    // Assert strictly zero occurrences of f32 / f64 types or literals
    assert!(
        !src.contains("f32"),
        "mub6_zerorel_variety.rs must contain zero f32 occurrences"
    );
    assert!(
        !src.contains("f64"),
        "mub6_zerorel_variety.rs must contain zero f64 occurrences"
    );
}
