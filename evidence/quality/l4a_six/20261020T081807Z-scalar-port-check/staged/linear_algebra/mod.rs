
use crate::linear_algebra::scalars::{ExactRing, Field, Involution};
use serde::{Deserialize, Serialize};
use thiserror::Error;

pub mod bareiss_det;
pub use bareiss_det as rational_bareiss;
pub mod basic_matrix;
pub mod char_poly;
pub mod commutant;
pub mod complex_tensor;
pub mod compositum_deg;
pub use compositum_deg as real_field_compositum_degrees;
pub mod congruence;
pub mod elimination;
pub mod entropy_dichotomy;
pub mod field_factors;
pub use field_factors as real_field_polynomial_factors;
pub mod field_squares;
pub use field_squares as real_field_squares;
pub mod image_kernel;
pub mod interpolation;
pub mod json_admission;
pub mod involution;
pub mod laws;
pub mod matrix;
pub mod ordered;
pub mod pseudoinverse;
pub mod quintic_split;
pub use quintic_split as quintic_splitting_algebras;
pub mod rational_factors;
pub use rational_factors as rational_polynomial_factors;
pub mod scalars;
pub mod second_jet;
pub mod smith_form;
pub mod splitting_deg;
pub use splitting_deg as real_field_splitting_degrees;
pub mod tensor_proj;
#[cfg(test)]
pub mod test_support;

pub use basic_matrix::{BasicMatrix, MatrixError, OperationLimits};
pub use scalars::{GaussianRational, Q, q, Semiring};

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct ExactMatrix<F>(pub BasicMatrix<F>);

impl<F: Field + ExactRing> ExactMatrix<F> {
    pub fn rows(&self) -> usize {
        self.0.rows()
    }

    pub fn cols(&self) -> usize {
        self.0.cols()
    }

    pub fn shape(&self) -> (usize, usize) {
        self.0.shape()
    }

    pub fn as_slice(&self) -> &[F] {
        self.0.as_slice()
    }

    pub fn get(&self, r: usize, c: usize) -> Result<&F, MatrixError> {
        self.0.get_ref(r, c)
    }

    pub fn zeros(rows: usize, cols: usize) -> Result<Self, ExactFieldError> {
        matrix::zeros(rows, cols).map(Self)
    }

    pub fn from_rows(rows: Vec<Vec<F>>) -> Result<Self, MatrixError> {
        let r = rows.len();
        let c = rows.first().map_or(0, Vec::len);
        for row in &rows {
            if row.len() != c {
                return Err(MatrixError::ShapeMismatch {
                    rows: r,
                    cols: c,
                    len: rows.iter().map(Vec::len).sum(),
                });
            }
        }
        let data: Vec<F> = rows.into_iter().flatten().collect();
        Ok(Self(BasicMatrix::from_row_major(r, c, data)?))
    }

    pub fn mul(&self, rhs: &Self) -> Result<Self, ExactFieldError> {
        matrix::multiply(&self.0, &rhs.0).map(Self)
    }

    pub fn rank(&self) -> Result<usize, ExactFieldError> {
        elimination::rank(&self.0)
    }
}

impl<F: Involution> ExactMatrix<F> {
    pub fn is_hermitian(&self) -> Result<bool, MatrixError> {
        involution::is_hermitian(&self.0).map_err(|e| MatrixError::InvalidOperation(e.to_string()))
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Error)]
pub enum ExactFieldError {
    #[error("checked scalar operation refused: {0}")]
    Scalar(#[from] scalars::ScalarError),
    /// Storage, shape or budget refusal from [`BasicMatrix`] (`DimensionOverflow`,
    /// `AllocationLimitExceeded`, `OperationLimitExceeded`, `OperationCountOverflow`, ...).
    #[error("matrix storage: {0}")]
    Matrix(#[from] MatrixError),

    /// Two operands whose shapes the operation cannot combine.
    #[error("{operation}: incompatible shapes {left:?} and {right:?}")]
    ShapeMismatch {
        operation: &'static str,
        left: (usize, usize),
        right: (usize, usize),
    },

    /// An operator-valued operation applied to a non-square matrix.
    #[error("{operation} needs a square matrix, got {rows}x{cols}")]
    NotSquare {
        operation: &'static str,
        rows: usize,
        cols: usize,
    },

    /// A row-list input whose rows do not all have the length of row 0.
    #[error("row {row} has {len} entries but row 0 has {expected}")]
    RaggedRows {
        row: usize,
        len: usize,
        expected: usize,
    },

    /// A vector operand of the wrong length.
    #[error("{operation}: vector has {got} entries, expected {expected}")]
    VectorLength {
        operation: &'static str,
        expected: usize,
        got: usize,
    },

    /// The matrix has no inverse. `rank < size`; a nonzero kernel vector is available
    /// from [`elimination::kernel_basis`] and replays `A x = 0`.
    #[error("matrix is singular: rank {rank} of dimension {size}")]
    Singular { rank: usize, size: usize },

    /// The first position `row < col` with `a[row][col] != a[col][row]`.
    #[error("matrix is not symmetric at ({row}, {col})")]
    NotSymmetric { row: usize, col: usize },

    /// The first position with `a[row][col] != conjugate(a[col][row])` (`row <= col`).
    #[error("matrix is not Hermitian at ({row}, {col})")]
    NotHermitian { row: usize, col: usize },

    /// A construction that needs `2 ≠ 0` was asked for over a field of characteristic 2.
    #[error("{operation} is undefined in characteristic 2")]
    CharacteristicTwo { operation: &'static str },

    /// An entry does not fit the requested fixed-width representation (see
    /// `matrix::narrow_to_rational64`); the first offending position.
    #[error("the entry at ({row}, {col}) does not fit the requested representation")]
    NotRepresentable { row: usize, col: usize },

    /// The scalar type broke an obligation its trait states (see [`laws`]).
    #[error("{operation}: the scalar type violates its contract: {violation}")]
    ScalarContract {
        operation: &'static str,
        violation: &'static str,
    },

    /// An exact replay of a computed answer disagreed with the answer. This is an
    /// internal inconsistency (a defective scalar implementation), never a statement
    /// about the input.
    #[error("{operation}: exact replay of the computed result failed")]
    ReplayFailed { operation: &'static str },

    /// A supplied certificate failed its exact replay.
    #[error("certificate rejected: {reason}")]
    CertificateRejected { reason: &'static str },

    /// A sample checked by [`laws`] violates a stated law.
    #[error("law violated on the sample: {law}")]
    LawViolated { law: &'static str },
}

pub(crate) fn reserve<T>(len: usize) -> Result<Vec<T>, MatrixError> {
    let mut data = Vec::new();
    data.try_reserve_exact(len)
        .map_err(|_| MatrixError::AllocationFailed { requested: len })?;
    Ok(data)
}

pub(crate) fn element_count(rows: usize, cols: usize) -> Result<usize, MatrixError> {
    rows.checked_mul(cols)
        .ok_or(MatrixError::DimensionOverflow { rows, cols })
}

pub(crate) fn times(a: usize, b: usize) -> Result<usize, MatrixError> {
    a.checked_mul(b).ok_or(MatrixError::OperationCountOverflow)
}

pub(crate) fn plus(a: usize, b: usize) -> Result<usize, MatrixError> {
    a.checked_add(b).ok_or(MatrixError::OperationCountOverflow)
}

pub(crate) fn charge(
    limits: OperationLimits,
    elements: usize,
    scalar_ops: usize,
) -> Result<(), MatrixError> {
    if elements > limits.max_elements {
        return Err(MatrixError::AllocationLimitExceeded {
            requested: elements,
            limit: limits.max_elements,
        });
    }
    if scalar_ops > limits.max_scalar_ops {
        return Err(MatrixError::OperationLimitExceeded {
            requested: scalar_ops,
            limit: limits.max_scalar_ops,
        });
    }
    Ok(())
}

pub(crate) fn require_square<T>(
    operation: &'static str,
    m: &BasicMatrix<T>,
) -> Result<usize, ExactFieldError> {
    if m.rows() == m.cols() {
        Ok(m.rows())
    } else {
        Err(ExactFieldError::NotSquare {
            operation,
            rows: m.rows(),
            cols: m.cols(),
        })
    }
}

pub(crate) fn require_same_shape<T>(
    operation: &'static str,
    a: &BasicMatrix<T>,
    b: &BasicMatrix<T>,
) -> Result<(), ExactFieldError> {
    if a.shape() == b.shape() {
        Ok(())
    } else {
        Err(ExactFieldError::ShapeMismatch {
            operation,
            left: a.shape(),
            right: b.shape(),
        })
    }
}

pub(crate) fn inverse_of<F: Field + ExactRing>(
    operation: &'static str,
    x: &F,
) -> Result<F, ExactFieldError> {
    x.try_inv().map_err(|error| match error {
        scalars::ScalarError::DivisionByZero => ExactFieldError::ScalarContract {
            operation, violation: "a nonzero element has no multiplicative inverse",
        },
        other => ExactFieldError::Scalar(other),
    })
}

#[derive(Debug, Clone)]
pub(crate) struct Grid<F> {
    rows: usize,
    cols: usize,
    data: Vec<F>,
}

impl<F: Clone> Grid<F> {
    pub(crate) fn from_matrix(m: &BasicMatrix<F>) -> Result<Self, MatrixError> {
        let mut data = reserve(m.as_slice().len())?;
        data.extend_from_slice(m.as_slice());
        Ok(Self {
            rows: m.rows(),
            cols: m.cols(),
            data,
        })
    }

    pub(crate) fn from_fn<E, G>(rows: usize, cols: usize, mut f: G) -> Result<Self, E>
    where
        E: From<MatrixError>,
        G: FnMut(usize, usize) -> Result<F, E>,
    {
        let len = element_count(rows, cols)?;
        let mut data = reserve(len)?;
        for r in 0..rows {
            for c in 0..cols {
                data.push(f(r, c)?);
            }
        }
        Ok(Self { rows, cols, data })
    }

    pub(crate) fn rows(&self) -> usize {
        self.rows
    }

    pub(crate) fn cols(&self) -> usize {
        self.cols
    }

    pub(crate) fn at(&self, r: usize, c: usize) -> &F {
        &self.data[r * self.cols + c]
    }

    pub(crate) fn put(&mut self, r: usize, c: usize, value: F) {
        self.data[r * self.cols + c] = value;
    }

    pub(crate) fn swap_rows(&mut self, a: usize, b: usize) {
        if a != b {
            for c in 0..self.cols {
                self.data.swap(a * self.cols + c, b * self.cols + c);
            }
        }
    }

    pub(crate) fn swap_columns(&mut self, a: usize, b: usize) {
        if a != b {
            for r in 0..self.rows {
                self.data.swap(r * self.cols + a, r * self.cols + b);
            }
        }
    }

    pub(crate) fn into_matrix(self) -> Result<BasicMatrix<F>, MatrixError> {
        BasicMatrix::from_row_major(self.rows, self.cols, self.data)
    }
}

impl<F: Field + ExactRing> Grid<F> {
    pub(crate) fn sub_scaled_row(&mut self, target: usize, source: usize, factor: &F, from: usize) {
        for c in from..self.cols {
            let delta = factor.try_mul(self.at(source, c))?;
            let updated = self.at(target, c).try_sub(&delta)?;
            self.put(target, c, updated);
        }
    }

    pub(crate) fn scale_row(&mut self, row: usize, factor: &F, from: usize) {
        for c in from..self.cols {
            let scaled = factor.try_mul(self.at(row, c))?;
            self.put(row, c, scaled);
        }
    }

    pub(crate) fn add_scaled_column(
        &mut self,
        target: usize,
        source: usize,
        factor: &F,
        from: usize,
    ) {
        for r in from..self.rows {
            let delta = factor.try_mul(self.at(r, source))?;
            let updated = self.at(r, target).try_add(&delta)?;
            self.put(r, target, updated);
        }
    }

    pub(crate) fn add_scaled_row(&mut self, target: usize, source: usize, factor: &F, from: usize) {
        for c in from..self.cols {
            let delta = factor.try_mul(self.at(source, c))?;
            let updated = self.at(target, c).try_add(&delta)?;
            self.put(target, c, updated);
        }
    }
}

pub mod exact_field {
    pub use super::*;
}

pub mod backend {
    pub mod basic_matrix {
        pub use crate::linear_algebra::basic_matrix::*;
    }
}

#[cfg(test)]
mod exact_matrix_contract {
    use super::*;
    use crate::linear_algebra::test_support::Z6;

    #[test]
    fn rank_of_a_non_field_keeps_the_scalar_refusal() {
        let matrix = ExactMatrix::from_rows(vec![
            vec![Z6::new(2), Z6::new(1)],
            vec![Z6::new(1), Z6::new(1)],
        ])
        .unwrap();
        assert_eq!(
            matrix.rank(),
            Err(ExactFieldError::ScalarContract {
                operation: "rref",
                violation: "a nonzero element has no multiplicative inverse",
            })
        );
    }

    #[test]
    fn multiplication_keeps_an_operation_count_overflow() {
        let left = ExactMatrix::<crate::linear_algebra::scalars::Q>::zeros(1, 0).unwrap();
        let right = ExactMatrix::<crate::linear_algebra::scalars::Q>::zeros(0, usize::MAX).unwrap();
        assert_eq!(
            left.mul(&right),
            Err(ExactFieldError::Matrix(MatrixError::OperationCountOverflow))
        );
    }

    #[test]
    fn zeros_returns_the_construction_error() {
        let refused = ExactMatrix::<crate::linear_algebra::scalars::Q>::zeros(usize::MAX, 2);
        assert!(matches!(
            refused,
            Err(ExactFieldError::Matrix(MatrixError::DimensionOverflow { .. }))
        ));
    }
}
