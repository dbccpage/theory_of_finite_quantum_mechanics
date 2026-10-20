//! Private provider storage with owned, fallible exact arithmetic.
//! Raw construction transports coefficients; arithmetic admits every input,
//! including entries unused by empty products. Limits count output scalar slots
//! and arithmetic calls, not bytes, bit growth, validation cost or elapsed time.
//! AuthorityEffect: None.
#![forbid(unsafe_code)]
use super::scalars::{Ring, ScalarError, Semiring};
use ::linear_algebra::backend::basic_matrix as storage;
pub use storage::{CheckedMatrixError, MatrixError, OperationLimits};
type ArithmeticResult<T> = Result<T, CheckedMatrixError<ScalarError>>;
pub const DEFAULT_LIMITS: OperationLimits = OperationLimits {
    max_elements: 4096,
    max_scalar_ops: 1_000_000,
};

/// Shape-checked transport. No Deref or public provider escape is exposed.
/// ```compile_fail
/// use theory_of_finite_qm::linear_algebra::basic_matrix::BasicMatrix;
/// let matrix = BasicMatrix::from_row_major(1,1,vec![1i64]).unwrap();
/// let raw = &matrix.0;
/// ```
/// ```compile_fail
/// use theory_of_finite_qm::linear_algebra::basic_matrix::BasicMatrix;
/// let matrix = BasicMatrix::from_row_major(1,1,vec![1i64]).unwrap();
/// let _ = matrix.into_provider();
/// ```
/// ```compile_fail
/// use theory_of_finite_qm::linear_algebra::basic_matrix::BasicMatrix;
/// let matrix = BasicMatrix::from_row_major(1,1,vec![0.5f64]).unwrap();
/// let _ = matrix.mul(&matrix);
/// ```
#[derive(Debug, Clone, PartialEq, Eq, serde::Serialize, serde::Deserialize)]
#[serde(transparent)]
pub struct BasicMatrix<T>(storage::BasicMatrix<T>);
impl<T> BasicMatrix<T> {
    pub fn from_row_major(rows: usize, cols: usize, data: Vec<T>) -> Result<Self, MatrixError> {
        storage::BasicMatrix::from_row_major(rows, cols, data).map(Self)
    }
    pub fn from_row_major_with_limit(
        rows: usize,
        cols: usize,
        data: Vec<T>,
        limit: usize,
    ) -> Result<Self, MatrixError> {
        storage::BasicMatrix::from_row_major_with_limit(rows, cols, data, limit).map(Self)
    }
    pub fn try_from_fn<F: FnMut(usize, usize) -> T>(
        rows: usize,
        cols: usize,
        f: F,
    ) -> Result<Self, MatrixError> {
        storage::BasicMatrix::try_from_fn(rows, cols, f).map(Self)
    }
    pub fn try_from_fn_with_limit<F: FnMut(usize, usize) -> T>(
        rows: usize,
        cols: usize,
        limit: usize,
        f: F,
    ) -> Result<Self, MatrixError> {
        storage::BasicMatrix::try_from_fn_with_limit(rows, cols, limit, f).map(Self)
    }
    pub fn try_from_fn_result<F: FnMut(usize, usize) -> Result<T, E>, E: From<MatrixError>>(
        rows: usize,
        cols: usize,
        f: F,
    ) -> Result<Self, E> {
        storage::BasicMatrix::try_from_fn_result(rows, cols, f).map(Self)
    }
    pub fn try_from_fn_result_with_limit<
        F: FnMut(usize, usize) -> Result<T, E>,
        E: From<MatrixError>,
    >(
        rows: usize,
        cols: usize,
        limit: usize,
        f: F,
    ) -> Result<Self, E> {
        storage::BasicMatrix::try_from_fn_result_with_limit(rows, cols, limit, f).map(Self)
    }
    pub fn rows(&self) -> usize {
        self.0.rows()
    }
    pub fn cols(&self) -> usize {
        self.0.cols()
    }
    pub fn shape(&self) -> (usize, usize) {
        self.0.shape()
    }
    pub fn as_slice(&self) -> &[T] {
        self.0.as_slice()
    }
    pub fn get_ref(&self, row: usize, col: usize) -> Result<&T, MatrixError> {
        self.0.get_ref(row, col)
    }
    pub fn try_to_nalgebra(&self) -> Result<nalgebra::DMatrix<T>, MatrixError>
    where
        T: nalgebra::Scalar,
    {
        self.0.try_to_nalgebra()
    }
    pub fn try_from_nalgebra(m: &nalgebra::DMatrix<T>) -> Result<Self, MatrixError>
    where
        T: nalgebra::Scalar,
    {
        storage::BasicMatrix::try_from_nalgebra(m).map(Self)
    }
}
impl<T: Clone> BasicMatrix<T> {
    pub fn get(&self, row: usize, col: usize) -> Result<T, MatrixError> {
        self.0.get(row, col)
    }
    pub fn set(&mut self, row: usize, col: usize, value: T) -> Result<(), MatrixError> {
        self.0.set(row, col, value)
    }
    pub fn try_transpose(&self) -> Result<Self, MatrixError> {
        self.0.try_transpose().map(Self)
    }
    pub fn try_map<U, E: From<MatrixError>, F: FnMut(&T) -> Result<U, E>>(
        &self,
        f: F,
    ) -> Result<BasicMatrix<U>, E> {
        self.0.try_map(f).map(BasicMatrix)
    }
}
fn scalar(e: ScalarError) -> CheckedMatrixError<ScalarError> {
    CheckedMatrixError::Scalar(e)
}
fn admit<T: Semiring>(values: &[T]) -> ArithmeticResult<()> {
    for value in values {
        value.validate().map_err(scalar)?;
    }
    Ok(())
}
fn preflight(
    rows: usize,
    cols: usize,
    inner: usize,
    limits: OperationLimits,
) -> Result<usize, MatrixError> {
    let elements = super::element_count(rows, cols)?;
    let work = super::times(super::times(2, elements)?, inner)?;
    super::charge(limits, elements, work)?;
    Ok(elements)
}
impl<T: Semiring> BasicMatrix<T> {
    /// Explicit internal transport boundary for existing provider consumers.
    /// Coefficients are admitted before the single fallible owned storage copy.
    pub(crate) fn try_from_provider(
        matrix: &storage::BasicMatrix<T>,
    ) -> Result<Self, super::ExactFieldError> {
        super::charge(DEFAULT_LIMITS, matrix.as_slice().len(), 0)?;
        super::validate_values(matrix.as_slice())?;
        let mut data = super::reserve(matrix.as_slice().len())?;
        data.extend_from_slice(matrix.as_slice());
        Ok(Self::from_row_major(matrix.rows(), matrix.cols(), data)?)
    }
    /// Move admitted storage across an explicit provider API boundary. This
    /// does not approve arithmetic in the receiving provider. It is crate-only;
    /// public local matrix arithmetic continues through the checked protocol.
    pub(crate) fn into_provider(self) -> Result<storage::BasicMatrix<T>, super::ExactFieldError> {
        super::validate_values(self.as_slice())?;
        Ok(self.0)
    }
    pub fn zero(rows: usize, cols: usize) -> Result<Self, MatrixError> {
        Self::try_from_fn_with_limit(rows, cols, DEFAULT_LIMITS.max_elements, |_, _| T::zero())
    }
    pub fn mul(&self, rhs: &Self) -> ArithmeticResult<Self> {
        self.checked_mul(rhs)
    }
    pub fn mul_vec(&self, rhs: &[T]) -> ArithmeticResult<Vec<T>> {
        self.checked_mul_vec(rhs)
    }
    pub fn add(&self, rhs: &Self) -> ArithmeticResult<Self> {
        self.checked_add(rhs)
    }
    pub fn checked_add(&self, rhs: &Self) -> ArithmeticResult<Self> {
        self.checked_add_with_limit(rhs, DEFAULT_LIMITS.max_elements)
    }
    pub fn checked_add_with_limit(&self, rhs: &Self, limit: usize) -> ArithmeticResult<Self> {
        self.zip(rhs, limit, |a, b| a.try_add(b))
    }
    fn zip<F: FnMut(&T, &T) -> Result<T, ScalarError>>(
        &self,
        rhs: &Self,
        limit: usize,
        mut f: F,
    ) -> ArithmeticResult<Self> {
        if self.shape() != rhs.shape() {
            return Err(MatrixError::DimensionMismatch {
                left: self.shape(),
                right: rhs.shape(),
            }
            .into());
        }
        super::charge(
            OperationLimits {
                max_elements: limit,
                max_scalar_ops: usize::MAX,
            },
            self.as_slice().len(),
            0,
        )?;
        admit(self.as_slice())?;
        admit(rhs.as_slice())?;
        let mut out = super::reserve(self.as_slice().len())?;
        for (a, b) in self.as_slice().iter().zip(rhs.as_slice()) {
            out.push(f(a, b).map_err(scalar)?);
        }
        Ok(Self::from_row_major(self.rows(), self.cols(), out)?)
    }
    pub fn checked_mul(&self, rhs: &Self) -> ArithmeticResult<Self> {
        self.checked_mul_with_limits(rhs, DEFAULT_LIMITS)
    }
    pub fn checked_mul_with_limit(&self, rhs: &Self, limit: usize) -> ArithmeticResult<Self> {
        self.checked_mul_with_limits(
            rhs,
            OperationLimits {
                max_elements: limit,
                max_scalar_ops: DEFAULT_LIMITS.max_scalar_ops,
            },
        )
    }
    pub fn checked_mul_with_limits(
        &self,
        rhs: &Self,
        limits: OperationLimits,
    ) -> ArithmeticResult<Self> {
        if self.cols() != rhs.rows() {
            return Err(MatrixError::DimensionMismatch {
                left: self.shape(),
                right: rhs.shape(),
            }
            .into());
        }
        let count = preflight(self.rows(), rhs.cols(), self.cols(), limits)?;
        admit(self.as_slice())?;
        admit(rhs.as_slice())?;
        let mut out = super::reserve(count)?;
        for index in 0..count {
            let (r, c) = (index / rhs.cols(), index % rhs.cols());
            out.push(self.product_entry(rhs, r, c)?);
        }
        Ok(Self::from_row_major(self.rows(), rhs.cols(), out)?)
    }
    // Called only after shape, work and complete operand admission. Coordinates
    // come from the admitted flat output range, so every borrowed index exists.
    fn product_entry(&self, rhs: &Self, r: usize, c: usize) -> ArithmeticResult<T> {
        let mut sum = T::zero();
        for k in 0..self.cols() {
            let product = self.as_slice()[r * self.cols() + k]
                .try_mul(&rhs.as_slice()[k * rhs.cols() + c])
                .map_err(scalar)?;
            sum = sum.try_add(&product).map_err(scalar)?;
        }
        Ok(sum)
    }
    pub fn checked_mul_vec(&self, rhs: &[T]) -> ArithmeticResult<Vec<T>> {
        self.checked_mul_vec_with_limits(rhs, DEFAULT_LIMITS)
    }
    pub fn checked_mul_vec_with_limit(&self, rhs: &[T], limit: usize) -> ArithmeticResult<Vec<T>> {
        self.checked_mul_vec_with_limits(
            rhs,
            OperationLimits {
                max_elements: limit,
                max_scalar_ops: DEFAULT_LIMITS.max_scalar_ops,
            },
        )
    }
    pub fn checked_mul_vec_with_limits(
        &self,
        rhs: &[T],
        limits: OperationLimits,
    ) -> ArithmeticResult<Vec<T>> {
        if self.cols() != rhs.len() {
            return Err(MatrixError::DimensionMismatch {
                left: self.shape(),
                right: (rhs.len(), 1),
            }
            .into());
        }
        let count = preflight(self.rows(), 1, self.cols(), limits)?;
        admit(self.as_slice())?;
        admit(rhs)?;
        let mut out = super::reserve(count)?;
        for row in 0..count {
            let mut sum = T::zero();
            for (col, value) in rhs.iter().enumerate() {
                let product = self.as_slice()[row * self.cols() + col]
                    .try_mul(value)
                    .map_err(scalar)?;
                sum = sum.try_add(&product).map_err(scalar)?;
            }
            out.push(sum);
        }
        Ok(out)
    }
}
impl<T: Ring> BasicMatrix<T> {
    pub fn sub(&self, rhs: &Self) -> ArithmeticResult<Self> {
        self.checked_sub(rhs)
    }
    pub fn checked_sub(&self, rhs: &Self) -> ArithmeticResult<Self> {
        self.checked_sub_with_limit(rhs, DEFAULT_LIMITS.max_elements)
    }
    pub fn checked_sub_with_limit(&self, rhs: &Self, limit: usize) -> ArithmeticResult<Self> {
        self.zip(rhs, limit, |a, b| a.try_sub(b))
    }
}

#[cfg(test)]
mod tests {
    use super::super::scalars::{q, Operation, Q};
    use super::*;
    #[test]
    fn explicit_provider_transport_admits_both_directions_and_preserves_shape() {
        let raw = storage::BasicMatrix::from_row_major(2, 1, vec![q(2), q(-3)]).unwrap();
        let admitted = BasicMatrix::try_from_provider(&raw).unwrap();
        assert_eq!(admitted.shape(), (2, 1));
        assert_eq!(admitted.into_provider().unwrap(), raw);
        for value in [
            Q::new_raw(1.into(), 0.into()),
            Q::new_raw(1.into(), (-1).into()),
            Q::new_raw(2.into(), 2.into()),
        ] {
            let raw = storage::BasicMatrix::from_row_major(1, 1, vec![value.clone()]).unwrap();
            assert!(BasicMatrix::try_from_provider(&raw).is_err());
            let local = BasicMatrix::from_row_major(1, 1, vec![value]).unwrap();
            assert!(local.into_provider().is_err());
        }
    }
    fn ternary(mut code: usize) -> BasicMatrix<i64> {
        let mut values = Vec::new();
        for _ in 0..4 {
            values.push((code % 3) as i64 - 1);
            code /= 3;
        }
        BasicMatrix::from_row_major(2, 2, values).unwrap()
    }
    #[test]
    fn all_small_products_and_binary_operations_match_wide_integer_oracles() {
        for a in 0..81 {
            for b in 0..81 {
                let a = ternary(a);
                let b = ternary(b);
                let product = a.mul(&b).unwrap();
                let sum = a.add(&b).unwrap();
                let difference = a.sub(&b).unwrap();
                for r in 0..2 {
                    for c in 0..2 {
                        let expected = (0..2)
                            .map(|k| {
                                i128::from(a.as_slice()[2 * r + k])
                                    * i128::from(b.as_slice()[2 * k + c])
                            })
                            .sum::<i128>();
                        assert_eq!(i128::from(product.as_slice()[2 * r + c]), expected);
                        assert_eq!(
                            i128::from(sum.as_slice()[2 * r + c]),
                            i128::from(a.as_slice()[2 * r + c])
                                + i128::from(b.as_slice()[2 * r + c])
                        );
                        assert_eq!(
                            i128::from(difference.as_slice()[2 * r + c]),
                            i128::from(a.as_slice()[2 * r + c])
                                - i128::from(b.as_slice()[2 * r + c])
                        );
                    }
                }
                assert_eq!(
                    a.mul_vec(&[b.as_slice()[0], b.as_slice()[2]]).unwrap(),
                    vec![product.as_slice()[0], product.as_slice()[2]]
                );
            }
        }
    }
    #[test]
    fn native_overflow_is_a_typed_refusal_on_every_legacy_entry() {
        let matrix = |x| BasicMatrix::from_row_major(1, 1, vec![x]).unwrap();
        let max = matrix(i64::MAX);
        let min = matrix(i64::MIN);
        assert_eq!(
            max.mul(&matrix(2)),
            Err(scalar(ScalarError::OutOfRange {
                operation: Operation::Multiply
            }))
        );
        assert_eq!(
            max.mul_vec(&[2]),
            Err(scalar(ScalarError::OutOfRange {
                operation: Operation::Multiply
            }))
        );
        assert_eq!(
            max.add(&matrix(1)),
            Err(scalar(ScalarError::OutOfRange {
                operation: Operation::Add
            }))
        );
        assert_eq!(
            min.sub(&matrix(1)),
            Err(scalar(ScalarError::OutOfRange {
                operation: Operation::Subtract
            }))
        );
        assert_eq!(matrix(i64::MAX).mul(&matrix(1)).unwrap(), max);
    }
    #[test]
    fn all_inputs_are_admitted_before_empty_products_and_output_allocation() {
        let left = BasicMatrix::<Q>::from_row_major(0, 1, vec![]).unwrap();
        let right = BasicMatrix::<Q>::from_row_major(1, 0, vec![]).unwrap();
        for bad in [
            Q::new_raw(1.into(), 0.into()),
            Q::new_raw(1.into(), (-1).into()),
            Q::new_raw(2.into(), 2.into()),
        ] {
            let a = BasicMatrix::from_row_major(1, 1, vec![bad.clone()]).unwrap();
            assert!(matches!(left.mul(&a), Err(CheckedMatrixError::Scalar(_))));
            assert!(matches!(a.mul(&right), Err(CheckedMatrixError::Scalar(_))));
            assert!(matches!(
                left.mul_vec(&[bad]),
                Err(CheckedMatrixError::Scalar(_))
            ));
        }
        assert_eq!(
            BasicMatrix::<i64>::from_row_major(usize::MAX, 0, vec![])
                .unwrap()
                .mul(&BasicMatrix::from_row_major(0, 0, vec![]).unwrap())
                .unwrap()
                .shape(),
            (usize::MAX, 0)
        );
        let a = BasicMatrix::from_row_major(1, 1, vec![q(3)]).unwrap();
        assert!(a
            .checked_mul_with_limits(
                &a,
                OperationLimits {
                    max_elements: 1,
                    max_scalar_ops: 2
                }
            )
            .is_ok());
        assert!(matches!(
            a.checked_mul_with_limits(
                &a,
                OperationLimits {
                    max_elements: 1,
                    max_scalar_ops: 1
                }
            ),
            Err(CheckedMatrixError::Matrix(
                MatrixError::OperationLimitExceeded {
                    requested: 2,
                    limit: 1
                }
            ))
        ));
        assert!(matches!(
            a.checked_mul_with_limit(&a, 0),
            Err(CheckedMatrixError::Matrix(
                MatrixError::AllocationLimitExceeded {
                    requested: 1,
                    limit: 0
                }
            ))
        ));
        let encoded = serde_json::to_string(&a).unwrap();
        assert_eq!(serde_json::from_str::<BasicMatrix<Q>>(&encoded).unwrap(), a);
        assert!(
            serde_json::from_str::<BasicMatrix<i64>>(r#"{"rows":2,"cols":2,"data":[1]}"#).is_err()
        );
    }
}
