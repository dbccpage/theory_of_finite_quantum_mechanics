

fn reproduced(name: &str, operation: impl FnOnce() + std::panic::UnwindSafe) {
    assert!(std::panic::catch_unwind(operation).is_err(), "expected reachable panic was not reproduced");
    println!("DEFECT_CONFIRMED:{name}");
}

#[test]
fn gaussian_scalar_accepts_raw_invalid_rational_until_inverse_panics() {
    use tfqm_homology_linear_audit::linear_algebra::scalars::{GaussianRational, Field, Q, q};
    let candidate = GaussianRational::new(Q::new_raw(1.into(), 0.into()), q(0));
    reproduced("gaussian_scalar_accepts_raw_invalid_rational_until_inverse_panics", || { let _ = candidate.try_inv(); });
}
