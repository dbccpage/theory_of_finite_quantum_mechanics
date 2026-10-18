use num_rational::BigRational;
use omega_mub::omega_native::exact::mub6_collar_solver::{
    evaluate_collar_barrier, solve_karlsson_collar_cover,
};
use omega_number_theory::rational::rq;

#[test]
fn conditional_margin_does_not_certify_a_cover() {
    let report = solve_karlsson_collar_cover(2);
    assert_eq!(report.boxes.len(), 16);
    assert_eq!(report.barrier_arithmetic.conditional_margin, "12133/30000");
    assert!(!report.coverage_certified);
    assert!(!report.missing_obligations.is_empty());
    // All endpoints must parse as exact rationals, including zero and one.
    for b in &report.boxes {
        for interval in [&b.u_x, &b.v_x, &b.u_y, &b.v_y, &b.u_z, &b.v_z] {
            let lo: BigRational = interval[0].parse().unwrap();
            let hi: BigRational = interval[1].parse().unwrap();
            assert!(lo <= hi);
        }
    }
}

#[test]
fn barrier_refuses_invalid_inputs_and_reports_failed_margin() {
    assert!(evaluate_collar_barrier(&rq(1, 1), &rq(-1, 1), &rq(1, 1)).is_err());
    assert!(evaluate_collar_barrier(&rq(1, 1), &rq(1, 1), &rq(-1, 1)).is_err());
    assert!(
        !evaluate_collar_barrier(&rq(1, 1), &rq(2, 1), &rq(1, 1))
            .unwrap()
            .margin_positive
    );
}
