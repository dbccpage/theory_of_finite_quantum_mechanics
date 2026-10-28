use num_rational::BigRational;
use tfqm_mub::native::exact::mub6_deltoid_cusp_asymptotics::{
    evaluate_taylor_lagrange_enclosure, solve_deltoid_cusp_asymptotics,
};
use engine_number_theory::rational::rq;

#[test]
fn invalid_widths_are_refused() {
    assert!(evaluate_taylor_lagrange_enclosure(&rq(-1, 1000)).is_err());
    assert!(evaluate_taylor_lagrange_enclosure(&rq(2, 1)).is_err());
}

#[test]
fn zero_width_is_an_exact_point() {
    let r = evaluate_taylor_lagrange_enclosure(&rq(0, 1)).unwrap();
    assert_eq!(r.total_re_interval, ["3", "3"]);
    assert_eq!(r.total_im_interval, ["0", "0"]);
}

#[test]
fn rational_polynomial_samples_are_enclosed() {
    for delta in [rq(1, 1000), rq(1, 2), rq(1, 1)] {
        let r = evaluate_taylor_lagrange_enclosure(&delta).unwrap();
        let re_lo: BigRational = r.total_re_interval[0].parse().unwrap();
        let re_hi: BigRational = r.total_re_interval[1].parse().unwrap();
        let im_lo: BigRational = r.total_im_interval[0].parse().unwrap();
        let im_hi: BigRational = r.total_im_interval[1].parse().unwrap();
        // Exact finite regression samples, not a proof of the analytic remainder.
        for i in -8..=8 {
            let s = &delta * rq(i, 8);
            let s2 = &s * &s;
            let re = rq(3, 1) - rq(3, 1) * &s2 + rq(3, 4) * &s2 * &s2;
            let im = &s * &s2 - rq(1, 4) * &s * &s2 * &s2;
            assert!(re_lo <= re && re <= re_hi);
            assert!(im_lo <= im && im <= im_hi);
        }
    }
    assert!(!solve_deltoid_cusp_asymptotics().mub_curvature_bound_established);
}
