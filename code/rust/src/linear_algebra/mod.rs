//! Exact linear algebra, scalar fields, polynomial algebra and exact solvers.

use crate::linear_algebra::basic_matrix::{BasicMatrix, MatrixError, OperationLimits};
use crate::crate::linear_algebra::scalars::{ExactRing, Field};
use thiserror::Error;

pub mod bareiss_det;
pub mod basic_matrix;
pub mod char_poly;
pub mod commutant;
pub mod complex_tensor;
pub mod compositum_deg;
pub mod congruence;
pub mod cyclo_density;
pub mod elimination;
pub mod entropy_dichotomy;
pub mod field_factors;
pub mod field_squares;
pub mod image_kernel;
pub mod interpolation;
pub mod involution;
pub mod laws;
pub mod matrix;
pub mod ordered;
pub mod poly_roots;
pub mod pseudoinverse;
pub mod quintic_split;
pub mod rational_factors;
pub mod scalars;
pub mod second_jet;
pub mod smith_form;
pub mod spectral_factors;
pub mod splitting_deg;
pub mod tensor_proj;
pub mod test_support;

pub use basic_matrix::{BasicMatrix, MatrixError, OperationLimits};
pub use matrix::ExactMatrix;
pub use scalars::{GaussianRational, Q, q, Semiring};

/// Refusals of the exact-field matrix algorithms.
#[derive(Debug, Clone, PartialEq, Eq, Error)]
pub enum ExactFieldError {
    #[error("matrix storage: {0}")]
    Matrix(#[from] MatrixError),

    #[error("{operation}: incompatible shapes {left:?} and {right:?}")]
    ShapeMismatch {
        operation: &'static str,
        left: (usize, usize),
        right: (usize, usize),
    },

    #[error("{operation} needs a square matrix, got {rows}x{cols}")]
    NotSquare {
        operation: &'static str,
        rows: usize,
        cols: usize,
    },

    #[error("row {row} has {len} entries but row 0 has {expected}")]
    RaggedRows {
        row: usize,
        len: usize,
        expected: usize,
    },

    #[error("{operation}: vector has {got} entries, expected {expected}")]
    VectorLength {
        operation: &'static str,
        expected: usize,
        got: usize,
    },

    #[error("matrix is singular: rank {rank} of dimension {size}")]
    Singular { rank: usize, size: usize },

    #[error("matrix is not symmetric at ({row}, {col})")]
    NotSymmetric { row: usize, col: usize },

    #[error("matrix is not Hermitian at ({row}, {col})")]
    NotHermitian { row: usize, col: usize },

    #[error("{operation} is undefined in characteristic 2")]
    CharacteristicTwo { operation: &'static str },

    #[error("the entry at ({row}, {col}) does not fit the requested representation")]
    NotRepresentable { row: usize, col: usize },

    #[error("{operation}: the scalar type violates its contract: {violation}")]
    ScalarContract {
        operation: &'static str,
        violation: &'static str,
    },

    #[error("{operation}: exact replay of the computed result failed")]
    ReplayFailed { operation: &'static str },

    #[error("certificate rejected: {reason}")]
    CertificateRejected { reason: &'static str },

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
    x.try_inv().ok_or(ExactFieldError::ScalarContract {
        operation,
        violation: "a nonzero element has no multiplicative inverse",
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
            let delta = factor.mul(self.at(source, c));
            let updated = self.at(target, c).sub(&delta);
            self.put(target, c, updated);
        }
    }

    pub(crate) fn scale_row(&mut self, row: usize, factor: &F, from: usize) {
        for c in from..self.cols {
            let scaled = factor.mul(self.at(row, c));
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
            let delta = factor.mul(self.at(r, source));
            let updated = self.at(r, target).add(&delta);
            self.put(r, target, updated);
        }
    }

    pub(crate) fn add_scaled_row(&mut self, target: usize, source: usize, factor: &F, from: usize) {
        for c in from..self.cols {
            let delta = factor.mul(self.at(source, c));
            let updated = self.at(target, c).add(&delta);
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
