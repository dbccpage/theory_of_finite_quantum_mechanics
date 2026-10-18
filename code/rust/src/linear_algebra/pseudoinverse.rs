
use super::elimination::{inverse_with_limits, rref_with_limits};
use super::involution::adjoint;
use super::matrix::{from_fn_with_limits, multiply_with_limits, zeros_with_limits};
use super::ordered::HermitianOrdered;
use super::{charge, element_count, plus, times, ExactFieldError};
use crate::linear_algebra::basic_matrix::{BasicMatrix, OperationLimits};

pub fn pseudoinverse<F: HermitianOrdered>(
    c: &BasicMatrix<F>,
) -> Result<BasicMatrix<F>, ExactFieldError> {
    pseudoinverse_with_limits(c, OperationLimits::UNLIMITED)
}

pub fn pseudoinverse_with_limits<F: HermitianOrdered>(
    c: &BasicMatrix<F>,
    limits: OperationLimits,
) -> Result<BasicMatrix<F>, ExactFieldError> {
    let span = plus(c.rows(), c.cols())?;
    charge(
        limits,
        element_count(span, span)?,
        times(100, times(times(span, span)?, span)?)?,
    )?;
    let reduction = rref_with_limits(c, limits)?;
    let pivots = reduction.pivot_columns();
    let rank = pivots.len();
    if rank == 0 {
        return zeros_with_limits(c.cols(), c.rows(), limits);
    }
    let a = from_fn_with_limits(c.rows(), rank, limits, |r, k| {
        c.as_slice()[r * c.cols() + pivots[k]].clone()
    })?;
    let b = from_fn_with_limits(rank, c.cols(), limits, |r, k| {
        reduction.matrix().as_slice()[r * c.cols() + k].clone()
    })?;
    if multiply_with_limits(&a, &b, limits)? != *c {
        return Err(ExactFieldError::ReplayFailed {
            operation: "full-rank factorization",
        });
    }
    let a_star = adjoint(&a)?;
    let b_star = adjoint(&b)?;
    let a_gram = multiply_with_limits(&a_star, &a, limits)?;
    let b_gram = multiply_with_limits(&b, &b_star, limits)?;
    let a_inverse = inverse_with_limits(&a_gram, limits)?;
    let b_inverse = inverse_with_limits(&b_gram, limits)?;
    let left = multiply_with_limits(&b_star, &b_inverse, limits)?;
    let right = multiply_with_limits(&a_inverse, &a_star, limits)?;
    let inverse = multiply_with_limits(&left, &right, limits)?;
    verify_penrose(c, &inverse, limits)?;
    Ok(inverse)
}

pub fn verify_penrose<F: HermitianOrdered>(
    c: &BasicMatrix<F>,
    inverse: &BasicMatrix<F>,
    limits: OperationLimits,
) -> Result<(), ExactFieldError> {
    if inverse.shape() != (c.cols(), c.rows()) {
        return Err(ExactFieldError::CertificateRejected {
            reason: "pseudoinverse has wrong shape",
        });
    }
    let cp = multiply_with_limits(c, inverse, limits)?;
    let pc = multiply_with_limits(inverse, c, limits)?;
    if multiply_with_limits(&cp, c, limits)? != *c
        || multiply_with_limits(&pc, inverse, limits)? != *inverse
        || adjoint(&cp)? != cp
        || adjoint(&pc)? != pc
    {
        return Err(ExactFieldError::CertificateRejected {
            reason: "a Penrose identity failed",
        });
    }
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::super::matrix::{from_rows, identity};
    use super::*;
    use num_rational::BigRational;
    fn q(n: i64) -> BigRational {
        BigRational::from_integer(n.into())
    }
    #[test]
    fn rectangular_rank_deficient_inverse_replays_all_penrose_laws() {
        let c = from_rows(vec![vec![q(1), q(2), q(3)], vec![q(2), q(4), q(6)]]).unwrap();
        let p = pseudoinverse(&c).unwrap();
        assert_eq!(p.shape(), (3, 2));
        assert_eq!(p.as_slice()[0], BigRational::new(1.into(), 70.into()));
        verify_penrose(&c, &p, OperationLimits::UNLIMITED).unwrap();
        let bad = from_rows(vec![vec![q(0), q(0)], vec![q(0), q(0)], vec![q(0), q(0)]]).unwrap();
        assert!(verify_penrose(&c, &bad, OperationLimits::UNLIMITED).is_err());
    }
    #[test]
    fn inverse_and_zero_cases_have_the_canonical_shapes() {
        let c = identity::<BigRational>(3).unwrap();
        assert_eq!(pseudoinverse(&c).unwrap(), c);
        let zero = zeros_with_limits::<BigRational>(2, 3, OperationLimits::UNLIMITED).unwrap();
        assert_eq!(pseudoinverse(&zero).unwrap().shape(), (3, 2));
        assert!(pseudoinverse_with_limits(
            &c,
            OperationLimits {
                max_elements: 1,
                max_scalar_ops: 1
            }
        )
        .is_err());
    }
}
