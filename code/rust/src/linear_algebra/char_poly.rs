
use crate::linear_algebra::basic_matrix::{BasicMatrix, MatrixError, OperationLimits};
use crate::linear_algebra::elimination::{reduce_to_rref, reduction_cost};
use crate::linear_algebra::matrix::{
    identity, is_identity_matrix, is_zero_matrix, multiply, multiply_with_limits, power, zeros,
};
use crate::linear_algebra::{
    charge, element_count, plus, require_square, reserve, times, ExactFieldError, Grid,
};
use crate::linear_algebra::scalars::{ExactRing, Field};

pub fn characteristic_polynomial<F: Field + ExactRing>(
    a: &BasicMatrix<F>,
) -> Result<Vec<F>, ExactFieldError> {
    characteristic_polynomial_with_limits(a, OperationLimits::UNLIMITED)
}

pub fn characteristic_polynomial_with_limits<F: Field + ExactRing>(
    a: &BasicMatrix<F>,
    limits: OperationLimits,
) -> Result<Vec<F>, ExactFieldError> {
    let n = require_square("characteristic_polynomial", a)?;
    let square = element_count(n, n)?;
    let cube = times(square, n)?;
    let ops = plus(times(2, times(cube, n)?)?, times(4, cube)?)?;
    charge(limits, square, ops)?;

    let data = a.as_slice();
    let at = |r: usize, c: usize| &data[r * n + c];

    let mut poly: Vec<F> = reserve(1)?;
    poly.push(F::one());
    for k in (0..n).rev() {
        let s = n - k;
        let mut toeplitz: Vec<F> = reserve(s + 1)?;
        toeplitz.push(F::one());
        toeplitz.push(at(k, k).neg());
        let mut v: Vec<F> = reserve(s - 1)?;
        for i in 0..(s - 1) {
            v.push(at(k + 1 + i, k).clone());
        }
        for j in 0..(s - 1) {
            let mut acc = F::zero();
            for (idx, vi) in v.iter().enumerate() {
                acc = acc.add(&at(k, k + 1 + idx).mul(vi));
            }
            toeplitz.push(acc.neg());
            if j + 1 < s - 1 {
                let mut next: Vec<F> = reserve(s - 1)?;
                for i in 0..(s - 1) {
                    let mut sum = F::zero();
                    for (idx, vi) in v.iter().enumerate() {
                        sum = sum.add(&at(k + 1 + i, k + 1 + idx).mul(vi));
                    }
                    next.push(sum);
                }
                v = next;
            }
        }
        let mut next_poly: Vec<F> = reserve(s + 1)?;
        for i in 0..=s {
            let mut acc = F::zero();
            for j in 0..s.min(i + 1) {
                acc = acc.add(&toeplitz[i - j].mul(&poly[j]));
            }
            next_poly.push(acc);
        }
        poly = next_poly;
    }
    poly.reverse();
    Ok(poly)
}

pub fn evaluate_polynomial_at_matrix<F: Field + ExactRing>(
    coefficients: &[F],
    a: &BasicMatrix<F>,
) -> Result<BasicMatrix<F>, ExactFieldError> {
    evaluate_polynomial_at_matrix_with_limits(coefficients, a, OperationLimits::UNLIMITED)
}

pub fn evaluate_polynomial_at_matrix_with_limits<F: Field + ExactRing>(
    coefficients: &[F],
    a: &BasicMatrix<F>,
    limits: OperationLimits,
) -> Result<BasicMatrix<F>, ExactFieldError> {
    let n = require_square("evaluate_polynomial_at_matrix", a)?;
    let square = element_count(n, n)?;
    let terms = coefficients.len();
    let products = times(terms.saturating_sub(1), times(2, times(square, n)?)?)?;
    let ops = plus(products, times(terms, times(2, square)?)?)?;
    charge(limits, square, ops)?;

    let mut acc = zeros::<F>(n, n)?;
    for c in coefficients.iter().rev() {
        let product = multiply_with_limits(&acc, a, OperationLimits::UNLIMITED)?;
        acc = BasicMatrix::try_from_fn_result::<_, ExactFieldError>(n, n, |r, col| {
            let entry = product.get_ref(r, col)?;
            Ok(if r == col {
                entry.add(c)
            } else {
                entry.clone()
            })
        })?;
    }
    Ok(acc)
}

pub fn minimal_polynomial<F: Field + ExactRing>(
    a: &BasicMatrix<F>,
) -> Result<Vec<F>, ExactFieldError> {
    minimal_polynomial_with_limits(a, OperationLimits::UNLIMITED)
}

pub fn minimal_polynomial_with_limits<F: Field + ExactRing>(
    a: &BasicMatrix<F>,
    limits: OperationLimits,
) -> Result<Vec<F>, ExactFieldError> {
    let n = require_square("minimal_polynomial", a)?;
    if n == 0 {
        let mut one = reserve(1)?;
        one.push(F::one());
        return Ok(one);
    }
    let square = element_count(n, n)?;
    let mut ops = times(n, times(2, times(square, n)?)?)?;
    for k in 1..=n {
        ops = plus(ops, reduction_cost(square, plus(k, 1)?)?)?;
    }
    charge(limits, element_count(square, plus(n, 1)?)?, ops)?;

    let mut columns: Vec<Vec<F>> = reserve(n)?;
    let mut power = identity::<F>(n)?;
    let mut first: Vec<F> = reserve(square)?;
    first.extend_from_slice(power.as_slice());
    columns.push(first);
    for k in 1..=n {
        power = multiply_with_limits(&power, a, OperationLimits::UNLIMITED)?;
        let mut grid = Grid::from_fn(square, k + 1, |r, c| {
            Ok::<F, ExactFieldError>(if c < k {
                columns[c][r].clone()
            } else {
                power.as_slice()[r].clone()
            })
        })?;
        let pivots = reduce_to_rref(&mut grid)?;
        if pivots.last() != Some(&k) {
            let mut coefficients: Vec<F> = reserve(k + 1)?;
            for i in 0..k {
                coefficients.push(grid.at(i, k).neg());
            }
            coefficients.push(F::one());
            return Ok(coefficients);
        }
        let mut next: Vec<F> = reserve(square)?;
        next.extend_from_slice(power.as_slice());
        columns.push(next);
    }
    Err(ExactFieldError::ReplayFailed {
        operation: "minimal_polynomial",
    })
}

pub fn is_nilpotent<F: Field + ExactRing>(a: &BasicMatrix<F>) -> Result<bool, ExactFieldError> {
    let n = require_square("is_nilpotent", a)?;
    let exponent = u64::try_from(n).map_err(|_| MatrixError::OperationCountOverflow)?;
    Ok(is_zero_matrix(&power(a, exponent)?))
}

pub fn is_idempotent<F: Field + ExactRing>(a: &BasicMatrix<F>) -> Result<bool, ExactFieldError> {
    require_square("is_idempotent", a)?;
    Ok(&multiply(a, a)? == a)
}

pub fn is_involution<F: Field + ExactRing>(a: &BasicMatrix<F>) -> Result<bool, ExactFieldError> {
    require_square("is_involution", a)?;
    is_identity_matrix(&multiply(a, a)?)
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::linear_algebra::elimination::{determinant, inverse};
    use crate::linear_algebra::matrix::{from_rows, identity, scale, sub, trace, transpose};
    use crate::linear_algebra::test_support::{m, q, random_matrix, Fp, Rng};
    use num_rational::BigRational;

    type Q = BigRational;

    fn rat(v: &[&[i64]]) -> BasicMatrix<Q> {
        m(v)
    }

    fn ints(v: &[i64]) -> Vec<Q> {
        v.iter().map(|&x| q(x, 1)).collect()
    }


    #[test]
    fn known_characteristic_polynomials() {
        assert_eq!(
            characteristic_polynomial(&rat(&[&[7]])).unwrap(),
            ints(&[-7, 1])
        );
        assert_eq!(
            characteristic_polynomial(&rat(&[&[1, 2], &[3, 4]])).unwrap(),
            ints(&[-2, -5, 1])
        );
        assert_eq!(
            characteristic_polynomial(&identity::<Q>(4).unwrap()).unwrap(),
            ints(&[1, -4, 6, -4, 1])
        );
        assert_eq!(
            characteristic_polynomial(&zeros::<Q>(3, 3).unwrap()).unwrap(),
            ints(&[0, 0, 0, 1])
        );
        assert_eq!(
            characteristic_polynomial(&rat(&[&[1, 0, 0], &[0, 2, 0], &[0, 0, 3]])).unwrap(),
            ints(&[-6, 11, -6, 1])
        );
        assert_eq!(
            characteristic_polynomial(&zeros::<Q>(0, 0).unwrap()).unwrap(),
            ints(&[1])
        );
    }

    #[test]
    fn companion_matrix_reproduces_its_polynomial() {
        let companion = rat(&[&[0, 0, -5], &[1, 0, 2], &[0, 1, 0]]);
        assert_eq!(
            characteristic_polynomial(&companion).unwrap(),
            ints(&[5, -2, 0, 1])
        );
        let c4 = rat(&[&[0, 0, 0, 7], &[1, 0, 0, -4], &[0, 1, 0, 1], &[0, 0, 1, -3]]);
        assert_eq!(
            characteristic_polynomial(&c4).unwrap(),
            ints(&[-7, 4, -1, 3, 1])
        );
    }

    #[test]
    fn triangular_matrices_have_the_diagonal_polynomial_and_nilpotent_blocks_give_x_to_the_n() {
        let upper = rat(&[&[1, 5, 7, 9], &[0, 2, 4, 6], &[0, 0, 3, 8], &[0, 0, 0, 4]]);
        assert_eq!(
            characteristic_polynomial(&upper).unwrap(),
            ints(&[24, -50, 35, -10, 1])
        );
        let jordan = rat(&[&[0, 1, 0, 0], &[0, 0, 1, 0], &[0, 0, 0, 1], &[0, 0, 0, 0]]);
        assert_eq!(
            characteristic_polynomial(&jordan).unwrap(),
            ints(&[0, 0, 0, 0, 1])
        );
    }


    #[test]
    fn cayley_hamilton_holds_for_random_matrices_of_size_one_to_six() {
        let mut rng = Rng::new(201);
        for n in 1..=6usize {
            for _ in 0..3 {
                let a = random_matrix(&mut rng, n, n, 5);
                let p = characteristic_polynomial(&a).unwrap();
                assert_eq!(p.len(), n + 1);
                assert_eq!(p[n], q(1, 1), "monic");
                let evaluated = evaluate_polynomial_at_matrix(&p, &a).unwrap();
                assert!(is_zero_matrix(&evaluated), "p(A) != 0 at n={n}");
            }
        }
    }

    #[test]
    fn the_extreme_coefficients_are_the_trace_and_the_determinant() {
        let mut rng = Rng::new(211);
        for n in 1..=6usize {
            let a = random_matrix(&mut rng, n, n, 4);
            let p = characteristic_polynomial(&a).unwrap();
            assert_eq!(p[n - 1], -trace(&a).unwrap(), "n={n}");
            let det = determinant(&a).unwrap();
            let signed = if n % 2 == 0 { det } else { -det };
            assert_eq!(p[0], signed, "n={n}");
        }
    }

    #[test]
    fn the_polynomial_is_a_similarity_invariant() {
        let mut rng = Rng::new(221);
        for n in 2..=4usize {
            let a = random_matrix(&mut rng, n, n, 3);
            let mut s = random_matrix(&mut rng, n, n, 2);
            for r in 0..n {
                for c in 0..n {
                    let v = if r == c {
                        q(1, 1)
                    } else if c < r {
                        s.get(r, c).unwrap()
                    } else {
                        q(0, 1)
                    };
                    s.set(r, c, v).unwrap();
                }
            }
            let similar = multiply(&multiply(&s, &a).unwrap(), &inverse(&s).unwrap()).unwrap();
            assert_eq!(
                characteristic_polynomial(&similar).unwrap(),
                characteristic_polynomial(&a).unwrap(),
                "n={n}"
            );
        }
    }

    #[test]
    fn transpose_and_scaling_behave() {
        let mut rng = Rng::new(223);
        let a = random_matrix(&mut rng, 4, 4, 4);
        assert_eq!(
            characteristic_polynomial(&transpose(&a).unwrap()).unwrap(),
            characteristic_polynomial(&a).unwrap()
        );
        let c = q(3, 2);
        let scaled = characteristic_polynomial(&scale(&a, &c).unwrap()).unwrap();
        let base = characteristic_polynomial(&a).unwrap();
        let mut power_of_c = q(1, 1);
        for i in (0..=4usize).rev() {
            assert_eq!(
                scaled[i],
                base[i].clone() * power_of_c.clone(),
                "coefficient {i}"
            );
            power_of_c *= c.clone();
        }
    }


    #[test]
    fn the_algorithm_is_valid_in_small_characteristic() {
        fn check<const P: u64>(seed: u64) {
            let mut rng = Rng::new(seed);
            for n in 1..=6usize {
                for _ in 0..3 {
                    let rows: Vec<Vec<Fp<P>>> = (0..n)
                        .map(|_| {
                            (0..n)
                                .map(|_| Fp::<P>::new(rng.range(0, P as i64 - 1)))
                                .collect()
                        })
                        .collect();
                    let a = from_rows(rows).unwrap();
                    let p = characteristic_polynomial(&a).unwrap();
                    let evaluated = evaluate_polynomial_at_matrix(&p, &a).unwrap();
                    assert!(is_zero_matrix(&evaluated), "GF({P}) n={n}");
                }
            }
        }
        check::<2>(301);
        check::<3>(302);
        check::<5>(303);
    }

    #[test]
    fn the_characteristic_polynomial_needs_no_division_even_over_a_ring_with_zero_divisors() {
        use crate::linear_algebra::test_support::Z6;
        let mut rng = Rng::new(262);
        for n in 1..=5usize {
            for _ in 0..4 {
                let rows: Vec<Vec<Z6>> = (0..n)
                    .map(|_| (0..n).map(|_| Z6::new(rng.range(0, 5))).collect())
                    .collect();
                let a = from_rows(rows).unwrap();
                let p = characteristic_polynomial(&a).unwrap();
                assert_eq!(p.len(), n + 1);
                assert!(
                    is_zero_matrix(&evaluate_polynomial_at_matrix(&p, &a).unwrap()),
                    "Z/6 n={n}"
                );
            }
        }
    }

    #[test]
    fn a_hand_computed_polynomial_over_gf2() {
        type F2 = Fp<2>;
        let a = from_rows(vec![
            vec![F2::new(1), F2::new(1)],
            vec![F2::new(1), F2::new(0)],
        ])
        .unwrap();
        assert_eq!(
            characteristic_polynomial(&a).unwrap(),
            vec![F2::new(1), F2::new(1), F2::new(1)]
        );
    }


    #[test]
    fn evaluating_a_polynomial_at_a_matrix_matches_the_expanded_expression() {
        let a = rat(&[&[1, 2], &[3, 4]]);
        let p = ints(&[2, -3, 1]);
        let expected = crate::linear_algebra::matrix::add(
            &sub(&multiply(&a, &a).unwrap(), &scale(&a, &q(3, 1)).unwrap()).unwrap(),
            &scale(&identity::<Q>(2).unwrap(), &q(2, 1)).unwrap(),
        )
        .unwrap();
        assert_eq!(evaluate_polynomial_at_matrix(&p, &a).unwrap(), expected);
        assert!(is_zero_matrix(
            &evaluate_polynomial_at_matrix(&[], &a).unwrap()
        ));
        assert_eq!(
            evaluate_polynomial_at_matrix(&ints(&[5]), &a).unwrap(),
            scale(&identity::<Q>(2).unwrap(), &q(5, 1)).unwrap()
        );
    }


    #[test]
    fn known_minimal_polynomials() {
        assert_eq!(
            minimal_polynomial(&zeros::<Q>(3, 3).unwrap()).unwrap(),
            ints(&[0, 1])
        );
        assert_eq!(
            minimal_polynomial(&identity::<Q>(3).unwrap()).unwrap(),
            ints(&[-1, 1])
        );
        assert_eq!(
            minimal_polynomial(&rat(&[&[2, 0], &[0, 2]])).unwrap(),
            ints(&[-2, 1])
        );
        assert_eq!(
            minimal_polynomial(&rat(&[&[1, 1], &[0, 1]])).unwrap(),
            ints(&[1, -2, 1])
        );
        assert_eq!(
            minimal_polynomial(&rat(&[&[1, 0, 0], &[0, 1, 0], &[0, 0, 2]])).unwrap(),
            ints(&[2, -3, 1])
        );
        assert_eq!(
            minimal_polynomial(&rat(&[&[0, 1, 0], &[0, 0, 1], &[0, 0, 0]])).unwrap(),
            ints(&[0, 0, 0, 1])
        );
        assert_eq!(
            minimal_polynomial(&rat(&[&[0, 1, 0], &[0, 0, 0], &[0, 0, 0]])).unwrap(),
            ints(&[0, 0, 1])
        );
        assert_eq!(minimal_polynomial(&rat(&[&[7]])).unwrap(), ints(&[-7, 1]));
        assert_eq!(
            minimal_polynomial(&zeros::<Q>(0, 0).unwrap()).unwrap(),
            ints(&[1])
        );
        let companion = rat(&[&[0, 0, -5], &[1, 0, 2], &[0, 1, 0]]);
        assert_eq!(
            minimal_polynomial(&companion).unwrap(),
            ints(&[5, -2, 0, 1])
        );
    }

    fn remainder(mut f: Vec<Q>, g: &[Q]) -> Vec<Q> {
        while f.len() >= g.len() {
            let lead = f[f.len() - 1].clone();
            let shift = f.len() - g.len();
            for (i, gc) in g.iter().enumerate() {
                f[shift + i] = f[shift + i].clone() - lead.clone() * gc.clone();
            }
            f.pop();
        }
        f
    }

    #[test]
    fn the_minimal_polynomial_annihilates_divides_the_characteristic_polynomial_and_is_minimal() {
        use crate::linear_algebra::elimination::rank;
        let mut rng = Rng::new(251);
        for n in 1..=5usize {
            for trial in 0..6 {
                let a = if trial % 2 == 0 {
                    random_matrix(&mut rng, n, n, 3)
                } else {
                    let block = random_matrix(&mut rng, n.max(2) - 1, n.max(2) - 1, 2);
                    crate::linear_algebra::matrix::direct_sum(&block, &rat(&[&[3]])).unwrap()
                };
                let n_actual = a.rows();
                let min = minimal_polynomial(&a).unwrap();
                let chi = characteristic_polynomial(&a).unwrap();
                assert!(min.len() <= n_actual + 1);
                assert_eq!(min[min.len() - 1], q(1, 1));
                assert!(is_zero_matrix(
                    &evaluate_polynomial_at_matrix(&min, &a).unwrap()
                ));
                assert!(
                    remainder(chi, &min).iter().all(|c| *c == q(0, 1)),
                    "min must divide char"
                );
                let mut rows = Vec::new();
                for k in 0..=n_actual as u64 {
                    rows.push(power(&a, k).unwrap().as_slice().to_vec());
                }
                let krylov = from_rows(rows).unwrap();
                assert_eq!(
                    min.len() - 1,
                    rank(&krylov).unwrap(),
                    "n={n_actual} trial={trial}"
                );
            }
        }
    }

    #[test]
    fn the_minimal_polynomial_of_a_field_element_is_that_of_its_multiplication_matrix() {
        let one_plus_sqrt2 = rat(&[&[1, 2], &[1, 1]]);
        assert_eq!(
            minimal_polynomial(&one_plus_sqrt2).unwrap(),
            ints(&[-1, -2, 1])
        );
        assert_eq!(
            characteristic_polynomial(&one_plus_sqrt2).unwrap(),
            ints(&[-1, -2, 1])
        );
        let three = rat(&[&[3, 0], &[0, 3]]);
        assert_eq!(minimal_polynomial(&three).unwrap(), ints(&[-3, 1]));
        assert_eq!(
            characteristic_polynomial(&three).unwrap(),
            ints(&[9, -6, 1])
        );
    }

    #[test]
    fn minimal_polynomials_over_gf2() {
        type F2 = Fp<2>;
        let one = F2::new(1);
        let zero = F2::new(0);
        let t = from_rows(vec![vec![one, one], vec![zero, one]]).unwrap();
        assert_eq!(minimal_polynomial(&t).unwrap(), vec![one, zero, one]);
        assert_eq!(
            minimal_polynomial(&identity::<F2>(2).unwrap()).unwrap(),
            vec![one, one]
        );
    }

    #[test]
    fn minimal_polynomial_refuses_non_square_input_and_respects_its_budget() {
        assert!(matches!(
            minimal_polynomial(&zeros::<Q>(2, 3).unwrap()),
            Err(ExactFieldError::NotSquare {
                operation: "minimal_polynomial",
                ..
            })
        ));
        let a = rat(&[&[1, 2], &[3, 4]]);
        let exact = OperationLimits {
            max_elements: 12,
            max_scalar_ops: 154,
        };
        assert!(minimal_polynomial_with_limits(&a, exact).is_ok());
        assert_eq!(
            minimal_polynomial_with_limits(
                &a,
                OperationLimits {
                    max_scalar_ops: 153,
                    ..exact
                }
            ),
            Err(ExactFieldError::Matrix(
                MatrixError::OperationLimitExceeded {
                    requested: 154,
                    limit: 153
                }
            ))
        );
        assert!(minimal_polynomial_with_limits(
            &a,
            OperationLimits {
                max_elements: 11,
                ..exact
            }
        )
        .is_err());
    }


    #[test]
    fn nilpotent_idempotent_and_involution_predicates() {
        let strictly_upper = rat(&[&[0, 3, 1], &[0, 0, 2], &[0, 0, 0]]);
        assert!(is_nilpotent(&strictly_upper).unwrap());
        assert!(!is_nilpotent(&identity::<Q>(2).unwrap()).unwrap());
        assert!(!is_nilpotent(&rat(&[&[0, 1], &[1, 0]])).unwrap());
        assert!(is_nilpotent(&zeros::<Q>(0, 0).unwrap()).unwrap());

        let projector = rat(&[&[1, 0], &[0, 0]]);
        assert!(is_idempotent(&projector).unwrap());
        assert!(!is_idempotent(&rat(&[&[1, 1], &[0, 1]])).unwrap());

        let swap = rat(&[&[0, 1], &[1, 0]]);
        assert!(is_involution(&swap).unwrap());
        assert!(!is_involution(&rat(&[&[1, 1], &[0, 1]])).unwrap());
        assert!(!is_involution(&projector).unwrap());
        assert!(!is_idempotent(&swap).unwrap());
    }

    #[test]
    fn nilpotency_agrees_with_the_characteristic_polynomial_criterion() {
        let mut rng = Rng::new(241);
        for n in 1..=5usize {
            for trial in 0..4 {
                let raw = random_matrix(&mut rng, n, n, 3);
                let candidate = if trial % 2 == 0 {
                    let mut upper = raw.clone();
                    for r in 0..n {
                        for c in 0..=r {
                            upper.set(r, c, q(0, 1)).unwrap();
                        }
                    }
                    upper
                } else {
                    raw
                };
                let p = characteristic_polynomial(&candidate).unwrap();
                let is_x_to_the_n = p[..n].iter().all(|c| *c == q(0, 1));
                assert_eq!(
                    is_nilpotent(&candidate).unwrap(),
                    is_x_to_the_n,
                    "n={n} trial={trial}"
                );
            }
        }
    }

    #[test]
    fn predicates_and_polynomial_refuse_non_square_input() {
        let wide = zeros::<Q>(2, 3).unwrap();
        assert!(matches!(
            characteristic_polynomial(&wide),
            Err(ExactFieldError::NotSquare {
                operation: "characteristic_polynomial",
                ..
            })
        ));
        assert!(matches!(
            is_nilpotent(&wide),
            Err(ExactFieldError::NotSquare { .. })
        ));
        assert!(matches!(
            is_idempotent(&wide),
            Err(ExactFieldError::NotSquare { .. })
        ));
        assert!(matches!(
            is_involution(&wide),
            Err(ExactFieldError::NotSquare { .. })
        ));
        assert!(matches!(
            evaluate_polynomial_at_matrix(&ints(&[1]), &wide),
            Err(ExactFieldError::NotSquare { .. })
        ));
    }

    #[test]
    fn charpoly_budget_boundary_is_inclusive() {
        let a = rat(&[&[1, 2], &[3, 4]]);
        let exact = OperationLimits {
            max_elements: 4,
            max_scalar_ops: 64,
        };
        assert!(characteristic_polynomial_with_limits(&a, exact).is_ok());
        assert_eq!(
            characteristic_polynomial_with_limits(
                &a,
                OperationLimits {
                    max_scalar_ops: 63,
                    ..exact
                }
            ),
            Err(ExactFieldError::Matrix(
                MatrixError::OperationLimitExceeded {
                    requested: 64,
                    limit: 63
                }
            ))
        );
    }
}
