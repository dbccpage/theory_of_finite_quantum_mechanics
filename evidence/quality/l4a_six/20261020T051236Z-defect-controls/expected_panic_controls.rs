

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

#[test]
fn lggr_undefined_float_is_coerced_to_exact_zero() {
    let value = tfqm_local_green_global_red_lggr::adequacy::float_to_rational(f64::NAN);
    if value.as_ref().is_ok_and(num_traits::Zero::is_zero) {
        println!("DEFECT_CONFIRMED:lggr_undefined_float_is_coerced_to_exact_zero");
    } else {
        println!("COERCION_NOT_REPRODUCED:lggr_undefined_float_is_coerced_to_exact_zero");
    }
}

#[test]
fn smith_sparse_zero_domain_can_panic_on_dense_result_allocation() {
    use theory_of_finite_qm::linear_algebra::smith_form::SparseColMatrix;
    let matrix = SparseColMatrix::new_checked(usize::MAX, 0, vec![]).unwrap();
    reproduced("smith_sparse_zero_domain_can_panic_on_dense_result_allocation", || {
        let _ = matrix.mul_vec(&[]);
    });
}

#[test]
fn boundary_zero_domain_can_panic_on_dense_result_allocation() {
    use theory_of_finite_qm::homology::{boundary::BoundaryMap, chain::Chain, ids::{BasisId, Degree}};
    use theory_of_finite_qm::linear_algebra::{BasicMatrix, Q};
    let matrix = BasicMatrix::<Q>::from_row_major(usize::MAX, 0, vec![]).unwrap();
    let map = BoundaryMap::new(Degree::new(1), Degree::new(0), matrix).unwrap();
    let input = Chain::new(Degree::new(1), BasisId::new("probe").unwrap(), vec![]).unwrap();
    reproduced("boundary_zero_domain_can_panic_on_dense_result_allocation", || { let _ = map.apply(&input); });
}

#[test]
fn coboundary_zero_domain_can_panic_on_dense_result_allocation() {
    use theory_of_finite_qm::homology::{coboundary::CoboundaryMap, cochain::Cochain, ids::{BasisId, Degree}};
    use theory_of_finite_qm::linear_algebra::{BasicMatrix, Q};
    let matrix = BasicMatrix::<Q>::from_row_major(usize::MAX, 0, vec![]).unwrap();
    let map = CoboundaryMap::new(Degree::new(0), Degree::new(1), matrix).unwrap();
    let input = Cochain::new(Degree::new(0), BasisId::new("probe").unwrap(), vec![]).unwrap();
    reproduced("coboundary_zero_domain_can_panic_on_dense_result_allocation", || { let _ = map.apply(&input); });
}
