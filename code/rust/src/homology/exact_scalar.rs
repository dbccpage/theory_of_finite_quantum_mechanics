//! Admission for canonical Q values, including Rust's unchecked `new_raw` path.
//! AuthorityEffect: None.

use super::errors::HomologicalError;
use crate::linear_algebra::{BasicMatrix, Q};
use num_integer::Integer;
use num_traits::{One, Zero};

pub(super) fn admit_coefficients(values: &[Q]) -> Result<(), HomologicalError> {
    for (index, value) in values.iter().enumerate() {
        if value.denom() <= &num_bigint::BigInt::zero()
            || !value.numer().gcd(value.denom()).is_one()
        {
            return Err(HomologicalError::InvalidRational { index });
        }
    }
    Ok(())
}

pub(super) fn admit_matrix(matrix: &BasicMatrix<Q>) -> Result<(), HomologicalError> {
    admit_coefficients(matrix.as_slice())
}

pub(super) fn admit_shaped_matrix(
    matrix: &BasicMatrix<Q>,
    expected: (usize, usize),
) -> Result<(), HomologicalError> {
    if matrix.shape() != expected {
        return Err(HomologicalError::ShapeMismatch {
            expected,
            got: matrix.shape(),
        });
    }
    admit_matrix(matrix)
}

/// Check a product of already admitted canonical-Q matrices.
/// Both production callers admit shape and coefficients before this helper.
/// This internal operation does not normalize or admit raw ratios itself.
pub(super) fn admit_zero_product(
    first: &BasicMatrix<Q>,
    second: &BasicMatrix<Q>,
    violation: HomologicalError,
) -> Result<(), HomologicalError> {
    let product = first.mul(second)?;
    if !product.as_slice().iter().all(Zero::is_zero) {
        return Err(violation);
    }
    Ok(())
}
