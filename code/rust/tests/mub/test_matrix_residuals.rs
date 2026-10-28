//! P4 regression controls.
//! AuthorityEffect: None.
use tfqm_mub::native::exact::mub6_continuous_chaining::{t_max_multi_anchor, t_min_multi_anchor};
use tfqm_mub::native::exact::mub6_matrix_residuals::*;
use engine_number_theory::cyclotomic::Cyc24;
use engine_number_theory::rational::rq;

#[test]
fn supplied_matrix_residual_and_perturbation() {
    let mut h: Vec<Vec<Cyc24>> = (0..6)
        .map(|i| (0..6).map(|j| Cyc24::zeta24(4 * i * j)).collect())
        .collect();
    assert!(compute_matrix_residual(&h)
        .unwrap()
        .iter()
        .flatten()
        .all(|x| x == &Cyc24::zero()));
    h[0][0] = Cyc24::zero();
    let residual = compute_matrix_residual(&h).unwrap();
    assert_eq!(residual[0][0], Cyc24::rat(rq(-1, 1)));
    assert_eq!(residual[0][1], Cyc24::rat(rq(-1, 1)));
    assert_eq!(residual[1][1], Cyc24::zero());
}

#[test]
fn zero_matrix_residual() {
    let residual = compute_matrix_residual(&vec![vec![Cyc24::zero(); 6]; 6]).unwrap();
    for i in 0..6 {
        for j in 0..6 {
            assert_eq!(
                residual[i][j],
                Cyc24::rat(rq(if i == j { -6 } else { 0 }, 1))
            );
        }
    }
    assert!(compute_matrix_residual(&[]).is_err());
}

#[test]
fn parameter_only_certification_fails_closed() {
    for t in [t_min_multi_anchor(), rq(1, 10), t_max_multi_anchor()] {
        assert_eq!(
            compute_2circulant_residual_matrix(&t).unwrap_err(),
            MISSING_EVIDENCE
        );
        assert_eq!(
            compute_algebraic_derivative_bound(&t).unwrap_err(),
            MISSING_EVIDENCE
        );
    }
    assert_eq!(
        build_matrix_residual_verifier(250).unwrap_err(),
        MISSING_EVIDENCE
    );
    assert!(compute_2circulant_residual_matrix(&rq(-1, 1)).is_err());
}

#[test]
fn interval_cover_remains_arithmetic_only() {
    let mut cover = build_interval_cover(250).unwrap();
    assert_eq!(cover.balls.len(), 250);
    let receipt = cover.audit().unwrap();
    assert!(
        receipt.verified && receipt.endpoint_coverage_verified && receipt.adjacent_overlap_verified
    );
    assert!(!receipt.analytic_obstruction_verified);
    cover.balls.clear();
    assert!(cover.audit().is_err());
    assert!(build_interval_cover(80).is_err());
}

#[test]
fn overlap_rejects_nonpositive_radii_and_gaps() {
    assert!(verify_continuation_step(
        &rq(0, 1),
        &rq(1, 1),
        &rq(2, 1),
        &rq(1, 1)
    ));
    assert!(!verify_continuation_step(
        &rq(0, 1),
        &rq(-1, 1),
        &rq(0, 1),
        &rq(2, 1)
    ));
    assert!(!verify_continuation_step(
        &rq(0, 1),
        &rq(0, 1),
        &rq(0, 1),
        &rq(1, 1)
    ));
    assert!(!verify_continuation_step(
        &rq(0, 1),
        &rq(1, 1),
        &rq(3, 1),
        &rq(1, 1)
    ));
}
