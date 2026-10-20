extern crate self as omega_lie_theory;
pub mod cayley;
pub mod cayley_unitary;
pub mod clifford;
pub mod finite_group;
pub mod finite_groupoid_algebra;
pub mod finite_order;
pub mod finite_path_algebra;
pub mod heisenberg;
pub mod lie_algebra;
pub mod lorentz;
pub mod pauli_symplectic;
pub mod rotation;
pub mod scalar;
pub mod su2;
pub mod su2_matrix;
pub mod su_n;
pub mod twisted_abelian_algebra;

pub(crate) type QMatrix =
    linear_algebra::backend::basic_matrix::BasicMatrix<num_rational::BigRational>;

pub mod weyl_operators;

use num_rational::Ratio;

/// Test whether two rational diagonal entries have zero trace.
/// Raw ratios with a zero denominator are outside the domain and return false.
/// Each i64 cross-product has magnitude at most 2^126, so it and its negation
/// fit in i128. Comparing opposite products avoids overflowing their sum.
pub fn is_sl2_traceless(a11: Ratio<i64>, a22: Ratio<i64>) -> bool {
    if *a11.denom() == 0 || *a22.denom() == 0 {
        return false;
    }
    let left = i128::from(*a11.numer()) * i128::from(*a22.denom());
    let right = i128::from(*a22.numer()) * i128::from(*a11.denom());
    left == -right
}

#[cfg(test)]
mod lie_tests {
    use super::*;

    #[test]
    fn test_sl2() {
        assert!(is_sl2_traceless(Ratio::new(3, 5), Ratio::new(-3, 5)));
        assert!(!is_sl2_traceless(Ratio::new(1, 2), Ratio::new(1, 2)));
    }

    #[test]
    fn sl2_trace_does_not_overflow_on_i64_boundaries() {
        assert!(!is_sl2_traceless(
            Ratio::from_integer(i64::MAX),
            Ratio::from_integer(i64::MAX)
        ));
        assert!(!is_sl2_traceless(
            Ratio::from_integer(i64::MIN),
            Ratio::from_integer(i64::MIN)
        ));
        assert!(is_sl2_traceless(
            Ratio::new_raw(i64::MIN, 1),
            Ratio::new_raw(i64::MIN, -1)
        ));
        assert!(is_sl2_traceless(
            Ratio::new_raw(2, i64::MIN),
            Ratio::new_raw(-2, i64::MIN)
        ));
    }

    #[test]
    fn sl2_trace_rejects_raw_zero_denominators() {
        assert!(!is_sl2_traceless(
            Ratio::new_raw(0, 0),
            Ratio::from_integer(0)
        ));
        assert!(!is_sl2_traceless(
            Ratio::from_integer(0),
            Ratio::new_raw(1, 0)
        ));
    }

    #[test]
    fn sl2_trace_matches_unbounded_rational_oracle() {
        use num_bigint::BigInt;
        use num_rational::BigRational;
        use num_traits::Zero;
        let values = [
            i64::MIN,
            i64::MIN + 1,
            -7,
            -1,
            0,
            1,
            7,
            i64::MAX - 1,
            i64::MAX,
        ];
        for n1 in values {
            for d1 in values {
                for n2 in values {
                    for d2 in values {
                        let expected = d1 != 0
                            && d2 != 0
                            && (BigRational::new(BigInt::from(n1), BigInt::from(d1))
                                + BigRational::new(BigInt::from(n2), BigInt::from(d2)))
                            .is_zero();
                        assert_eq!(
                            is_sl2_traceless(Ratio::new_raw(n1, d1), Ratio::new_raw(n2, d2)),
                            expected,
                            "{n1}/{d1} + {n2}/{d2}"
                        );
                    }
                }
            }
        }
    }
}
