

fn reproduced(name: &str, operation: impl FnOnce() + std::panic::UnwindSafe) {
    if std::panic::catch_unwind(operation).is_err() {
        println!("DEFECT_CONFIRMED:{name}");
    } else {
        println!("NO_PANIC_OBSERVED:{name}");
    }
}

#[test]
fn gaussian_scalar_accepts_raw_invalid_rational_until_inverse_panics() {
    use theory_of_finite_qm::linear_algebra::scalars::{GaussianRational, Field, Q, q};
    reproduced("gaussian_scalar_accepts_raw_invalid_rational_until_inverse_panics", || {
        let candidate = GaussianRational::new(Q::new_raw(1.into(), 0.into()), q(0));
        let _ = candidate.map(|value| value.try_inv());
    });
}

#[test]
fn provider_marks_overflowing_i64_as_exact() {
    use theory_of_finite_qm::linear_algebra::scalars::{ExactRing, Semiring};
    fn require_exact<T: ExactRing>() {}
    require_exact::<i64>();
    reproduced("provider_marks_overflowing_i64_as_exact", || {
        let _ = Semiring::add(&i64::MAX, &1);
    });
}
