//! Campaign correlation receipts, with independent exact comparison controls.
use finite_qm_native::campaigns::quantum_correlation::*;
use linear_algebra::exact_field::ordered::HermitianOrdered;
use num_bigint::BigInt;
use omega_number_theory::cyclotomic_field::Cyclotomic;
use omega_number_theory::rational::{ri, rq, Rational};
use omega_quantum_physics::quantum_correlation::{self as physics, PlanarObservable};
fn scalar(q: Rational) -> Cyclotomic<24> {
    Cyclotomic::rational(q)
}

#[test]
fn test_t940_chsh_evaluation_and_witnesses() {
    let q2 = q2_optimal_witness();
    assert_eq!(q2.conductor, 8);
    assert!(q2.attained);
    assert_eq!(q2.exact_chsh_value, "2*sqrt(2)");
    assert_eq!(q2.minimal_polynomial, "x^2 - 8 = 0");
    let q1 = q1_bounded_witness(5).unwrap();
    assert_eq!(q1.conductor, 4);
    assert!(!q1.attained);
    assert_eq!(q1.exact_chsh_value, "14/5");
    assert_eq!(q1.minimal_polynomial, "5*x - 14 = 0");
    assert_eq!(q1.distance_minimal_polynomial, "25*x^2 + 140*x - 4 = 0");
}
#[test]
fn test_t941_cross_language_parity_staircase() {
    let staircase = compute_staircase(&DECLARED_CONDUCTORS, HEIGHT_BOUND).unwrap();
    assert_eq!(staircase.len(), 5);
    for row in staircase {
        assert_eq!(
            row.max_chsh_exact,
            if row.conductor == 8 {
                "2*sqrt(2)"
            } else {
                "14/5"
            }
        );
        assert_eq!(row.tsirelson_attained, row.conductor == 8);
        if row.conductor == 8 {
            assert_eq!(row.distance_from_tsirelson_exact, "0");
        }
    }
}
#[test]
fn test_t942_mutation_1_floating_point_comparison() {
    let target = physics::tsirelson_value();
    let q = scalar(rq(14, 5));
    assert_ne!(q, target);
    let gap = &target - &q;
    assert_eq!(gap.fixed_field_sign(), Some(1));
    assert_eq!(
        minimal_polynomial_string(&gap).unwrap(),
        "25*x^2 + 140*x - 4 = 0"
    );
}
#[test]
fn test_t942_mutation_2_max_at_bound_reported_as_supremum() {
    let d = [
        (ri(1), ri(0)),
        (ri(0), ri(1)),
        (rq(21, 29), rq(20, 29)),
        (rq(20, 29), rq(-21, 29)),
    ]
    .into_iter()
    .map(|(x, y)| PlanarObservable::new(scalar(x), scalar(y), "Pell direction").unwrap())
    .collect::<Vec<_>>();
    let value = physics::evaluate_planar_chsh(&d[0], &d[1], &d[2], &d[3]).unwrap();
    assert_eq!(value, scalar(rq(82, 29)));
    assert_eq!((&value - &scalar(rq(14, 5))).fixed_field_sign(), Some(1));
    let larger = physics::finite_planar_chsh_max(
        &physics::generate_unit_vectors(4, 29).unwrap(),
        true,
        1_000_000,
    )
    .unwrap();
    assert_eq!(
        (&larger.value - &scalar(rq(14, 5))).fixed_field_sign(),
        Some(1)
    );
}
#[test]
fn test_t942_mutation_3_measurement_outside_height_bound_admitted() {
    for v in physics::generate_unit_vectors(4, 5).unwrap() {
        for x in [&v.x, &v.y] {
            assert!(x.as_number().as_rational().unwrap().denom() <= &BigInt::from(5));
        }
    }
    assert!(physics::generate_unit_vectors(0, 5).is_err());
    assert!(physics::generate_unit_vectors(4, 129).is_err());
}
#[test]
fn test_t942_mutation_4_local_bound_confused_with_quantum_bound() {
    let q = scalar(rq(14, 5));
    assert_eq!((&q - &scalar(ri(2))).fixed_field_sign(), Some(1));
    assert_eq!(
        (&physics::tsirelson_value() - &q).fixed_field_sign(),
        Some(1)
    );
}
#[test]
fn test_t942_mutation_5_planted_attainment_at_conductor_4() {
    let real = optimize_chsh_at_bound(4, 5).unwrap();
    assert!(!real.tsirelson_attained);
    assert_ne!(real.max_chsh_exact, "2*sqrt(2)");
    assert!(!physics::sqrt2_in_cyclotomic(4));
}
#[test]
fn exact_signs_order_values_that_floats_cannot_separate() {
    let gap = &physics::tsirelson_value() - &scalar(rq(14, 5));
    assert_eq!(gap.fixed_field_sign(), Some(1));
    assert_eq!((-gap).fixed_field_sign(), Some(-1));
    let tiny = Rational::new(BigInt::from(1), BigInt::from(10).pow(100));
    let near = scalar(ri(1) + tiny);
    assert_eq!((&near - &scalar(ri(1))).fixed_field_sign(), Some(1));
    let row = optimize_chsh_at_bound(8, HEIGHT_BOUND).unwrap();
    assert_eq!(row.max_chsh_exact, "2*sqrt(2)");
    assert!(row.tsirelson_attained);
}
