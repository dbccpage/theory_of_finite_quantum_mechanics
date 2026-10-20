//! Canonical rational admission and bounded zero-product verification.
//! AuthorityEffect: None. Internal homology boundary; no provider multiplication.

use super::errors::HomologicalError;
use super::hashing::Hash256;
use crate::linear_algebra::scalars::hash_bigint;
use crate::linear_algebra::{BasicMatrix, MatrixError, Q};
use num_integer::Integer;
use num_traits::{One, Zero};

/// Per-input and logical-output cells and conservative field arithmetic.
/// These limits exclude scalar bit growth, hashing, allocator internals and
/// caller-owned input construction. A zero-product check stores no output matrix.
#[derive(Debug, Clone, Copy)]
pub(super) struct ZeroProductLimits {
    pub max_input_cells: usize,
    pub max_output_cells: usize,
    pub max_scalar_operations: usize,
}
impl Default for ZeroProductLimits {
    fn default() -> Self {
        Self {
            max_input_cells: 4096,
            max_output_cells: 4096,
            max_scalar_operations: 1_000_000,
        }
    }
}

/// The immutable borrow keeps the admission invariant valid for its lifetime.
/// There is no public or sibling-module unchecked constructor.
#[derive(Clone, Copy)]
pub(super) struct AdmittedMatrix<'a> {
    matrix: &'a BasicMatrix<Q>,
}
impl<'a> AdmittedMatrix<'a> {
    pub(super) fn try_new(matrix: &'a BasicMatrix<Q>) -> Result<Self, HomologicalError> {
        admit_coefficients(matrix.as_slice())?;
        Ok(Self { matrix })
    }
    pub(super) fn matrix(self) -> &'a BasicMatrix<Q> {
        self.matrix
    }

    /// Same canonical byte frame as hashing::hash_matrix, without cloning and
    /// reducing a value whose canonicality this token already established.
    pub(super) fn digest(self) -> Hash256 {
        let mut hasher = blake3::Hasher::new();
        hasher.update(super::hashing::MATRIX_Q_DOMAIN);
        hasher.update(&(self.matrix.rows() as u64).to_le_bytes());
        hasher.update(&(self.matrix.cols() as u64).to_le_bytes());
        for value in self.matrix.as_slice() {
            hash_bigint(&mut hasher, value.numer());
            hash_bigint(&mut hasher, value.denom());
        }
        Hash256(*hasher.finalize().as_bytes())
    }

    fn zero_product(
        self,
        right: Self,
        violation: HomologicalError,
    ) -> Result<(), HomologicalError> {
        let (left, right) = (self.matrix, right.matrix);
        // Zero-area dimensions may contain usize::MAX metadata. No row loop
        // or multiplication is needed for their vacuous product.
        if left.rows() == 0 || right.cols() == 0 || left.cols() == 0 {
            return Ok(());
        }
        for row in 0..left.rows() {
            for col in 0..right.cols() {
                if !dot_product(left, right, row, col)?.is_zero() {
                    return Err(violation);
                }
            }
        }
        Ok(())
    }
}

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
    AdmittedMatrix::try_new(matrix).map(|_| ())
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
fn cells(rows: usize, cols: usize, limit: usize) -> Result<usize, MatrixError> {
    let count = rows
        .checked_mul(cols)
        .ok_or(MatrixError::DimensionOverflow { rows, cols })?;
    if count > limit {
        return Err(MatrixError::AllocationLimitExceeded {
            requested: count,
            limit,
        });
    }
    Ok(count)
}
fn product_admission(
    left: &BasicMatrix<Q>,
    right: &BasicMatrix<Q>,
    limits: ZeroProductLimits,
) -> Result<(), MatrixError> {
    cells(left.rows(), left.cols(), limits.max_input_cells)?;
    cells(right.rows(), right.cols(), limits.max_input_cells)?;
    if left.cols() != right.rows() {
        return Err(MatrixError::DimensionMismatch {
            left: left.shape(),
            right: right.shape(),
        });
    }
    let count = cells(left.rows(), right.cols(), limits.max_output_cells)?;
    // Left-to-right order preserves the zero-output shortcut before multiplying
    // by potentially huge inner metadata; no spurious overflow for 0*k.
    let operations = product_work(count, left.cols())?;
    if operations > limits.max_scalar_operations {
        return Err(MatrixError::OperationLimitExceeded {
            requested: operations,
            limit: limits.max_scalar_operations,
        });
    }
    Ok(())
}
fn product_work(outputs: usize, inner: usize) -> Result<usize, MatrixError> {
    outputs
        .checked_mul(inner)
        .and_then(|n| n.checked_mul(2))
        .ok_or(MatrixError::OperationCountOverflow)
}
fn dot_product(
    left: &BasicMatrix<Q>,
    right: &BasicMatrix<Q>,
    row: usize,
    col: usize,
) -> Result<Q, MatrixError> {
    let mut sum = Q::zero();
    for inner in 0..left.cols() {
        sum += left.get_ref(row, inner)? * right.get_ref(inner, col)?;
    }
    Ok(sum)
}
pub(super) fn admit_zero_product(
    first: &BasicMatrix<Q>,
    second: &BasicMatrix<Q>,
    violation: HomologicalError,
) -> Result<(), HomologicalError> {
    admit_zero_product_with_limits(first, second, violation, ZeroProductLimits::default())
}
pub(super) fn admit_zero_product_with_limits(
    first: &BasicMatrix<Q>,
    second: &BasicMatrix<Q>,
    violation: HomologicalError,
    limits: ZeroProductLimits,
) -> Result<(), HomologicalError> {
    product_admission(first, second, limits)?;
    AdmittedMatrix::try_new(first)?.zero_product(AdmittedMatrix::try_new(second)?, violation)
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::linear_algebra::scalars::q;
    fn violation() -> HomologicalError {
        HomologicalError::BoundaryLawViolation { degree: 1 }
    }
    fn matrix(rows: usize, cols: usize, values: &[i64]) -> BasicMatrix<Q> {
        BasicMatrix::from_row_major(rows, cols, values.iter().copied().map(q).collect()).unwrap()
    }
    #[test]
    fn all_small_rectangular_products_match_integer_oracle() {
        for (rows, inner, cols) in [(1, 2, 1), (2, 1, 2), (2, 2, 1)] {
            let left_len = rows * inner;
            let right_len = inner * cols;
            for code in 0..3usize.pow((left_len + right_len) as u32) {
                let mut code = code;
                let mut values = Vec::new();
                for _ in 0..left_len + right_len {
                    values.push((code % 3) as i64 - 1);
                    code /= 3;
                }
                let (a, b) = values.split_at(left_len);
                let zero = (0..rows).all(|i| {
                    (0..cols).all(|j| {
                        (0..inner)
                            .map(|k| a[i * inner + k] * b[k * cols + j])
                            .sum::<i64>()
                            == 0
                    })
                });
                let result = admit_zero_product(
                    &matrix(rows, inner, a),
                    &matrix(inner, cols, b),
                    violation(),
                );
                assert_eq!(result, if zero { Ok(()) } else { Err(violation()) });
            }
        }
    }
    #[test]
    fn canonical_admission_rejects_every_raw_failure_class() {
        for raw in [
            Q::new_raw(1.into(), 0.into()),
            Q::new_raw(1.into(), (-1).into()),
            Q::new_raw(2.into(), 4.into()),
            Q::new_raw(0.into(), 2.into()),
        ] {
            let input = BasicMatrix::from_row_major(1, 2, vec![q(1), raw]).unwrap();
            assert!(matches!(
                AdmittedMatrix::try_new(&input),
                Err(HomologicalError::InvalidRational { index: 1 })
            ));
        }
        for value in [
            q(0),
            Q::new((-1).into(), 2.into()),
            Q::new(3.into(), 2.into()),
        ] {
            admit_coefficients(&[value]).unwrap();
        }
    }
    #[test]
    fn zero_product_validates_both_inputs_even_when_one_side_is_zero() {
        let zero = matrix(1, 1, &[0]);
        let bad = BasicMatrix::from_row_major(1, 1, vec![Q::new_raw(1.into(), 0.into())]).unwrap();
        for (left, right) in [(&bad, &zero), (&zero, &bad)] {
            assert_eq!(
                admit_zero_product(left, right, violation()),
                Err(HomologicalError::InvalidRational { index: 0 })
            );
        }
        assert_eq!(
            admit_shaped_matrix(&zero, (2, 1)),
            Err(HomologicalError::ShapeMismatch {
                expected: (2, 1),
                got: (1, 1)
            })
        );
        admit_shaped_matrix(&zero, (1, 1)).unwrap();
        let a = BasicMatrix::from_row_major(
            1,
            2,
            vec![Q::new(1.into(), 2.into()), Q::new(1.into(), 3.into())],
        )
        .unwrap();
        let b = matrix(2, 1, &[2, -3]);
        admit_zero_product(&a, &b, violation()).unwrap();
    }
    #[test]
    fn canonical_digest_preserves_literal_signed_frames_and_public_hash() {
        let input =
            BasicMatrix::from_row_major(1, 2, vec![Q::new((-3).into(), 2.into()), q(0)]).unwrap();
        let admitted = AdmittedMatrix::try_new(&input).unwrap();
        assert!(std::ptr::eq(admitted.matrix(), &input));
        assert_eq!(
            admitted.digest(),
            super::super::hashing::hash_matrix(&input).unwrap()
        );
        let mut h = blake3::Hasher::new();
        h.update(b"MSSN.BasicMatrix<BigRational>.v2");
        h.update(&1u64.to_le_bytes());
        h.update(&2u64.to_le_bytes());
        for byte in [253u8, 2, 0, 1] {
            h.update(&1u64.to_le_bytes());
            h.update(&[byte]);
        }
        assert_eq!(admitted.digest(), Hash256(*h.finalize().as_bytes()));
    }
    #[test]
    fn cell_work_shape_and_machine_boundaries_are_typed_and_inclusive() {
        let a = matrix(1, 2, &[1, 1]);
        let b = matrix(2, 1, &[1, -1]);
        let limits = ZeroProductLimits {
            max_input_cells: 2,
            max_output_cells: 1,
            max_scalar_operations: 4,
        };
        admit_zero_product_with_limits(&a, &b, violation(), limits).unwrap();
        for limits in [
            ZeroProductLimits {
                max_input_cells: 1,
                ..limits
            },
            ZeroProductLimits {
                max_output_cells: 0,
                ..limits
            },
        ] {
            assert!(matches!(
                admit_zero_product_with_limits(&a, &b, violation(), limits),
                Err(HomologicalError::MatrixError(
                    MatrixError::AllocationLimitExceeded { .. }
                ))
            ));
        }
        assert_eq!(
            admit_zero_product_with_limits(
                &a,
                &b,
                violation(),
                ZeroProductLimits {
                    max_scalar_operations: 3,
                    ..limits
                }
            ),
            Err(HomologicalError::MatrixError(
                MatrixError::OperationLimitExceeded {
                    requested: 4,
                    limit: 3
                }
            ))
        );
        assert!(matches!(
            admit_zero_product(&a, &a, violation()),
            Err(HomologicalError::MatrixError(
                MatrixError::DimensionMismatch { .. }
            ))
        ));
        assert!(matches!(
            cells(usize::MAX, 2, usize::MAX),
            Err(MatrixError::DimensionOverflow { .. })
        ));
        assert_eq!(
            product_work(usize::MAX, 1),
            Err(MatrixError::OperationCountOverflow)
        );
        assert_eq!(product_work(usize::MAX, 0), Ok(0));
        for (r, k, c) in [(0, usize::MAX, 0), (usize::MAX, 0, 0), (0, 0, usize::MAX)] {
            let a = BasicMatrix::from_row_major(r, k, vec![]).unwrap();
            let b = BasicMatrix::from_row_major(k, c, vec![]).unwrap();
            admit_zero_product_with_limits(
                &a,
                &b,
                violation(),
                ZeroProductLimits {
                    max_input_cells: 0,
                    max_output_cells: 0,
                    max_scalar_operations: 0,
                },
            )
            .unwrap();
        }
        let a = BasicMatrix::from_row_major(usize::MAX, 0, vec![]).unwrap();
        let b = matrix(0, 1, &[]);
        admit_zero_product_with_limits(
            &a,
            &b,
            violation(),
            ZeroProductLimits {
                max_input_cells: 0,
                max_output_cells: usize::MAX,
                max_scalar_operations: 0,
            },
        )
        .unwrap();
    }
}
