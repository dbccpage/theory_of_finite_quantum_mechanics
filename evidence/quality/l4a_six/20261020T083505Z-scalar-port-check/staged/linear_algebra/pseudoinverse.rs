
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

pub fn check_penrose_identities<F: HermitianOrdered>(
    c: &BasicMatrix<F>,
    inverse: &BasicMatrix<F>,
    limits: OperationLimits,
) -> Result<[bool; 4], ExactFieldError> {
    if inverse.shape() != (c.cols(), c.rows()) {
        return Err(ExactFieldError::CertificateRejected {
            reason: "pseudoinverse has wrong shape",
        });
    }
    let m = c.rows();
    let n = c.cols();
    let total_elements = element_count(m, n)?;
    let total_ops = times(2, times(times(m, n)?, plus(m, n)?)?)?;
    charge(limits, total_elements, total_ops)?;

    let cp = multiply_with_limits(c, inverse, limits)?;
    let pc = multiply_with_limits(inverse, c, limits)?;
    let eq1 = multiply_with_limits(&cp, c, limits)? == *c;
    let eq2 = multiply_with_limits(&pc, inverse, limits)? == *inverse;
    let eq3 = adjoint(&cp)? == cp;
    let eq4 = adjoint(&pc)? == pc;
    Ok([eq1, eq2, eq3, eq4])
}

pub fn verify_penrose<F: HermitianOrdered>(
    c: &BasicMatrix<F>,
    inverse: &BasicMatrix<F>,
    limits: OperationLimits,
) -> Result<(), ExactFieldError> {
    let [eq1, eq2, eq3, eq4] = check_penrose_identities(c, inverse, limits)?;
    if !eq1 || !eq2 || !eq3 || !eq4 {
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

    #[test]
    fn penrose_each_equation_fails_exclusively() {
        // Eq 1 fails exclusively: C = [1], X = [0]
        let c1 = from_rows(vec![vec![q(1)]]).unwrap();
        let x1 = from_rows(vec![vec![q(0)]]).unwrap();
        assert_eq!(
            check_penrose_identities(&c1, &x1, OperationLimits::UNLIMITED).unwrap(),
            [false, true, true, true]
        );
        assert!(verify_penrose(&c1, &x1, OperationLimits::UNLIMITED).is_err());

        // Eq 2 fails exclusively: C = [0], X = [1]
        let c2 = from_rows(vec![vec![q(0)]]).unwrap();
        let x2 = from_rows(vec![vec![q(1)]]).unwrap();
        assert_eq!(
            check_penrose_identities(&c2, &x2, OperationLimits::UNLIMITED).unwrap(),
            [true, false, true, true]
        );
        assert!(verify_penrose(&c2, &x2, OperationLimits::UNLIMITED).is_err());

        // Eq 3 fails exclusively: C = [1; 0] (2x1), X = [1, 1] (1x2)
        let c3 = from_rows(vec![vec![q(1)], vec![q(0)]]).unwrap();
        let x3 = from_rows(vec![vec![q(1), q(1)]]).unwrap();
        assert_eq!(
            check_penrose_identities(&c3, &x3, OperationLimits::UNLIMITED).unwrap(),
            [true, true, false, true]
        );
        assert!(verify_penrose(&c3, &x3, OperationLimits::UNLIMITED).is_err());

        // Eq 4 fails exclusively: C = [1, 0] (1x2), X = [1; 1] (2x1)
        let c4 = from_rows(vec![vec![q(1), q(0)]]).unwrap();
        let x4 = from_rows(vec![vec![q(1)], vec![q(1)]]).unwrap();
        assert_eq!(
            check_penrose_identities(&c4, &x4, OperationLimits::UNLIMITED).unwrap(),
            [true, true, true, false]
        );
        assert!(verify_penrose(&c4, &x4, OperationLimits::UNLIMITED).is_err());
    }

    #[test]
    fn pseudoinverse_empty_matrices() {
        let zero_00 = zeros_with_limits::<BigRational>(0, 0, OperationLimits::UNLIMITED).unwrap();
        assert_eq!(pseudoinverse(&zero_00).unwrap().shape(), (0, 0));
        let zero_03 = zeros_with_limits::<BigRational>(0, 3, OperationLimits::UNLIMITED).unwrap();
        assert_eq!(pseudoinverse(&zero_03).unwrap().shape(), (3, 0));
    }

}
