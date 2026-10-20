use super::*;
use crate::linear_algebra::test_support::{m, q, Fp, Shaky, Z6};
use crate::linear_algebra::{elimination, matrix as mx};
use num_rational::BigRational;

const LIMITS: OperationLimits = OperationLimits::UNLIMITED;

#[test]
fn projector_rank_kernel_and_two_complex_structures_agree() {
    for left in 0..=3 {
        for right in 0..=3 {
            let n = left * right;
            let t = balance_map_with_limits::<BigRational>(left, right, LIMITS).unwrap();
            let p = balance_projector_with_limits::<BigRational>(left, right, LIMITS).unwrap();
            assert_eq!(t.shape(), (2 * n, 4 * n));
            assert_eq!(
                mx::multiply(&t, &mx::transpose(&t).unwrap()).unwrap(),
                mx::scale(&mx::identity(2 * n).unwrap(), &q(2, 1)).unwrap()
            );
            assert_eq!(
                p,
                mx::scale(
                    &mx::multiply(&mx::transpose(&t).unwrap(), &t).unwrap(),
                    &q(1, 2)
                )
                .unwrap()
            );
            assert_eq!(mx::multiply(&p, &p).unwrap(), p);
            assert_eq!(elimination::rank(&p).unwrap(), 2 * n);
            assert_eq!(elimination::kernel_basis(&t).unwrap().len(), 2 * n);
            let jl = realify_parts_with_limits(
                &mx::zeros(left, left).unwrap(),
                &mx::identity(left).unwrap(),
                LIMITS,
            )
            .unwrap();
            let jr = realify_parts_with_limits(
                &mx::zeros(right, right).unwrap(),
                &mx::identity(right).unwrap(),
                LIMITS,
            )
            .unwrap();
            let global_j = realify_parts_with_limits(
                &mx::zeros(n, n).unwrap(),
                &mx::identity(n).unwrap(),
                LIMITS,
            )
            .unwrap();
            let first = mx::kronecker(&jl, &mx::identity(2 * right).unwrap()).unwrap();
            let second = mx::kronecker(&mx::identity(2 * left).unwrap(), &jr).unwrap();
            assert_eq!(
                mx::multiply(&t, &first).unwrap(),
                mx::multiply(&global_j, &t).unwrap()
            );
            assert_eq!(
                mx::multiply(&t, &second).unwrap(),
                mx::multiply(&global_j, &t).unwrap()
            );
            let relation = mx::sub(&first, &second).unwrap();
            assert!(mx::is_zero_matrix(&mx::multiply(&t, &relation).unwrap()).unwrap());
            assert_eq!(elimination::rank(&relation).unwrap(), 2 * n);
            let expected = mx::scale(
                &mx::sub(
                    &mx::identity(4 * n).unwrap(),
                    &mx::kronecker(&jl, &jr).unwrap(),
                )
                .unwrap(),
                &q(1, 2),
            )
            .unwrap();
            assert_eq!(p, expected);
        }
    }
}

#[test]
fn rectangular_operator_compression_matches_four_independent_component_products() {
    for (a, c, b, d) in [(2, 3, 3, 1), (1, 2, 2, 3), (0, 1, 2, 1), (2, 0, 1, 2)] {
        let real = mx::from_fn(a, c, |i, j| q((2 * i + j + 1) as i64, 3)).unwrap();
        let imag = mx::from_fn(a, c, |i, j| q(i as i64 - j as i64, 5)).unwrap();
        let second_real = mx::from_fn(b, d, |i, j| q((i + 3 * j) as i64, 2)).unwrap();
        let second_imag = mx::from_fn(b, d, |i, j| q((i + j + 1) as i64, 7)).unwrap();
        let left = realify_parts_with_limits(&real, &imag, LIMITS).unwrap();
        let right = realify_parts_with_limits(&second_real, &second_imag, LIMITS).unwrap();
        let expected_real = mx::sub(
            &mx::kronecker(&real, &second_real).unwrap(),
            &mx::kronecker(&imag, &second_imag).unwrap(),
        )
        .unwrap();
        let expected_imag = mx::add(
            &mx::kronecker(&real, &second_imag).unwrap(),
            &mx::kronecker(&imag, &second_real).unwrap(),
        )
        .unwrap();
        let expected = realify_parts_with_limits(&expected_real, &expected_imag, LIMITS).unwrap();
        assert_eq!(
            normalized_tensor_with_limits(&left, &right, LIMITS).unwrap(),
            expected
        );
        assert_eq!(
            unscaled_tensor_with_limits(&left, &right, LIMITS).unwrap(),
            mx::scale(&expected, &q(2, 1)).unwrap()
        );
    }
}

#[test]
fn balance_map_associativity_retains_the_actual_tensor_coordinate_order() {
    let (a, b, c) = (2, 1, 3);
    let first = mx::multiply(
        &balance_map_with_limits::<BigRational>(a * b, c, LIMITS).unwrap(),
        &mx::kronecker(
            &balance_map_with_limits(a, b, LIMITS).unwrap(),
            &mx::identity(2 * c).unwrap(),
        )
        .unwrap(),
    )
    .unwrap();
    let second = mx::multiply(
        &balance_map_with_limits::<BigRational>(a, b * c, LIMITS).unwrap(),
        &mx::kronecker(
            &mx::identity(2 * a).unwrap(),
            &balance_map_with_limits(b, c, LIMITS).unwrap(),
        )
        .unwrap(),
    )
    .unwrap();
    assert_eq!(first, second);
}

#[test]
fn product_state_normalization_differs_from_balanced_lift_and_operator_compression() {
    let state = mx::scale(&mx::identity::<BigRational>(2).unwrap(), &q(1, 2)).unwrap();
    let product = unscaled_tensor_with_limits(&state, &state, LIMITS).unwrap();
    assert_eq!(product, state);
    assert_eq!(mx::trace(&product).unwrap(), q(1, 1));
    let wrong_state = normalized_tensor_with_limits(&state, &state, LIMITS).unwrap();
    assert_eq!(mx::trace(&wrong_state).unwrap(), q(1, 2));
    let raw = mx::kronecker(&state, &state).unwrap();
    let p = balance_projector_with_limits(1, 1, LIMITS).unwrap();
    let projected = mx::multiply(&mx::multiply(&p, &raw).unwrap(), &p).unwrap();
    assert_eq!(mx::trace(&projected).unwrap(), q(1, 2));
    let lifted = balanced_lift_with_limits(&product, 1, 1, LIMITS).unwrap();
    assert_eq!(lifted, mx::scale(&projected, &q(2, 1)).unwrap());
    assert_eq!(mx::trace(&lifted).unwrap(), q(1, 1));
    assert_eq!(
        mx::multiply(&mx::multiply(&p, &lifted).unwrap(), &p).unwrap(),
        lifted
    );
    let t = balance_map_with_limits(1, 1, LIMITS).unwrap();
    let recovered = mx::scale(
        &mx::multiply(
            &mx::multiply(&t, &lifted).unwrap(),
            &mx::transpose(&t).unwrap(),
        )
        .unwrap(),
        &q(1, 2),
    )
    .unwrap();
    assert_eq!(recovered, product);
}

#[test]
fn shape_image_characteristic_and_inverse_contract_refusals_are_distinct() {
    let identity = mx::identity::<BigRational>(2).unwrap();
    assert!(matches!(
        normalized_tensor_with_limits(&mx::identity(1).unwrap(), &identity, LIMITS),
        Err(ComplexTensorError::NotDoubled { .. })
    ));
    let reflection = m(&[&[-1, 0], &[0, 1]]);
    assert!(matches!(
        normalized_tensor_with_limits(&reflection, &identity, LIMITS),
        Err(ComplexTensorError::ComplexStructure {
            operand: "left",
            ..
        })
    ));
    assert!(balanced_lift_with_limits(&identity, 1, 2, LIMITS).is_err());
    assert!(realify_parts_with_limits(&identity, &mx::identity(1).unwrap(), LIMITS).is_err());
    assert!(matches!(
        balance_projector_with_limits::<Fp<2>>(1, 1, LIMITS),
        Err(ComplexTensorError::Algebra(
            ExactFieldError::CharacteristicTwo { .. }
        ))
    ));
    assert!(matches!(
        balance_projector_with_limits::<Z6>(1, 1, LIMITS),
        Err(ComplexTensorError::Algebra(
            ExactFieldError::ScalarContract { .. }
        ))
    ));
    assert!(matches!(
        balance_projector_with_limits::<Shaky<8>>(1, 1, LIMITS),
        Err(ComplexTensorError::Algebra(
            ExactFieldError::ScalarContract { .. }
        ))
    ));
    let p = balance_projector_with_limits::<Fp<5>>(1, 2, LIMITS).unwrap();
    assert_eq!(mx::multiply(&p, &p).unwrap(), p);
}

#[test]
fn inclusive_aggregate_budgets_refuse_before_invalid_scalar_contracts() {
    let identity = mx::identity::<BigRational>(2).unwrap();
    let exact = OperationLimits {
        max_elements: 16,
        max_scalar_ops: 123,
    };
    assert!(normalized_tensor_with_limits(&identity, &identity, exact).is_ok());
    assert!(matches!(
        normalized_tensor_with_limits(
            &identity,
            &identity,
            OperationLimits {
                max_scalar_ops: 122,
                ..exact
            }
        ),
        Err(ComplexTensorError::Algebra(ExactFieldError::Matrix(
            MatrixError::OperationLimitExceeded {
                requested: 123,
                limit: 122
            }
        )))
    ));
    assert!(matches!(
        normalized_tensor_with_limits(
            &identity,
            &identity,
            OperationLimits {
                max_elements: 15,
                ..exact
            }
        ),
        Err(ComplexTensorError::Algebra(ExactFieldError::Matrix(
            MatrixError::AllocationLimitExceeded {
                requested: 16,
                limit: 15
            }
        )))
    ));
    assert!(unscaled_tensor_with_limits(
        &identity,
        &identity,
        OperationLimits {
            max_scalar_ops: 116,
            ..exact
        }
    )
    .is_ok());
    assert!(balanced_lift_with_limits(
        &identity,
        1,
        1,
        OperationLimits {
            max_scalar_ops: 117,
            ..exact
        }
    )
    .is_ok());
    assert!(balanced_lift_with_limits(
        &identity,
        1,
        1,
        OperationLimits {
            max_scalar_ops: 116,
            ..exact
        }
    )
    .is_err());
    let tiny = OperationLimits {
        max_elements: 16,
        max_scalar_ops: 3,
    };
    assert!(matches!(
        balance_projector_with_limits::<Shaky<8>>(1, 1, tiny),
        Err(ComplexTensorError::Algebra(ExactFieldError::Matrix(
            MatrixError::OperationLimitExceeded {
                requested: 4,
                limit: 3
            }
        )))
    ));
    assert!(balance_map_with_limits::<BigRational>(usize::MAX, 1, LIMITS).is_err());
    assert!(balance_projector_with_limits::<BigRational>(usize::MAX / 2, 2, LIMITS).is_err());
}

fn literal(rows: &[&[i64]]) -> BasicMatrix<BigRational> {
    mx::from_rows(
        rows.iter()
            .map(|row| row.iter().map(|&entry| q(entry, 1)).collect())
            .collect(),
    )
    .unwrap()
}

#[test]
fn balance_and_realification_pin_literal_coordinates() {
    assert_eq!(
        balance_map_with_limits::<BigRational>(1, 1, LIMITS).unwrap(),
        literal(&[&[1, 0, 0, -1], &[0, 1, 1, 0]])
    );
    assert_eq!(
        balance_map_with_limits::<BigRational>(1, 2, LIMITS).unwrap(),
        literal(&[
            &[1, 0, 0, 0, 0, 0, -1, 0],
            &[0, 1, 0, 0, 0, 0, 0, -1],
            &[0, 0, 1, 0, 1, 0, 0, 0],
            &[0, 0, 0, 1, 0, 1, 0, 0],
        ])
    );
    let real = literal(&[&[1]]);
    let imaginary = literal(&[&[2]]);
    assert_eq!(
        realify_parts_with_limits(&real, &imaginary, LIMITS).unwrap(),
        literal(&[&[1, -2], &[2, 1]])
    );
}
