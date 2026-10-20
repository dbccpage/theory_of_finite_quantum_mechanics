
use super::{charge, element_count, inverse_of, matrix as mx, plus, times, ExactFieldError};
use crate::linear_algebra::basic_matrix::{BasicMatrix, MatrixError, OperationLimits};
use crate::linear_algebra::scalars::{ExactRing, Field};

#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum ComplexTensorError {
    #[error("exact tensor algebra: {0}")]
    Algebra(#[from] ExactFieldError),
    #[error("{operand} is {rows}x{cols}; both dimensions must be even")]
    NotDoubled {
        operand: &'static str,
        rows: usize,
        cols: usize,
    },
    #[error("{operand} does not intertwine the declared complex structures at ({row}, {col})")]
    ComplexStructure {
        operand: &'static str,
        row: usize,
        col: usize,
    },
}

impl From<MatrixError> for ComplexTensorError {
    fn from(error: MatrixError) -> Self {
        Self::Algebra(error.into())
    }
}

fn half<F: Field + ExactRing>() -> Result<F, ComplexTensorError> {
    let one = F::one();
    let two = one.try_add(&one)?;
    if two.is_zero() {
        return Err(ExactFieldError::CharacteristicTwo {
            operation: "complex tensor normalization",
        }
        .into());
    }
    let h = inverse_of("complex tensor normalization", &two)?;
    if two.mul(&h) != one {
        return Err(ExactFieldError::ScalarContract {
            operation: "complex tensor normalization",
            violation: "the supplied inverse of two does not multiply to one",
        }
        .into());
    }
    Ok(h)
}

fn carrier(left: usize, right: usize) -> Result<usize, ComplexTensorError> {
    element_count(2, left)?;
    element_count(2, right)?;
    Ok(element_count(left, right)?)
}

fn coordinate(index: usize, left: usize, right: usize) -> (usize, usize, usize, usize) {
    let local_row = index / (2 * right);
    let local_col = index % (2 * right);
    (
        local_row / left,
        local_col / right,
        local_row % left,
        local_col % right,
    )
}

pub fn realify_parts_with_limits<F: Field + ExactRing>(
    real: &BasicMatrix<F>,
    imaginary: &BasicMatrix<F>,
    limits: OperationLimits,
) -> Result<BasicMatrix<F>, ComplexTensorError> {
    super::require_same_shape("realification parts", real, imaginary)?;
    let (m, n) = real.shape();
    let rows = element_count(2, m)?;
    let cols = element_count(2, n)?;
    charge(limits, element_count(rows, cols)?, element_count(m, n)?)?;
    Ok(mx::from_fn_with_limits(rows, cols, limits, |row, col| {
        let index = (row % m) * n + col % n;
        match (row / m, col / n) {
            (0, 1) => imaginary.as_slice()[index].try_neg()?,
            (1, 0) => imaginary.as_slice()[index].clone(),
            _ => real.as_slice()[index].clone(),
        }
    })?)
}

pub fn balance_map_with_limits<F: Field + ExactRing>(
    left: usize,
    right: usize,
    limits: OperationLimits,
) -> Result<BasicMatrix<F>, ComplexTensorError> {
    let n = carrier(left, right)?;
    let rows = element_count(2, n)?;
    let cols = element_count(4, n)?;
    charge(limits, element_count(rows, cols)?, 1)?;
    let one = F::one();
    let minus_one = one.try_neg()?;
    Ok(mx::from_fn_with_limits(rows, cols, limits, |row, col| {
        let (a, b, i, j) = coordinate(col, left, right);
        if row % n != i * right + j {
            return F::zero();
        }
        match (row / n, a, b) {
            (0, 0, 0) | (1, 0, 1) | (1, 1, 0) => one.clone(),
            (0, 1, 1) => minus_one.clone(),
            _ => F::zero(),
        }
    })?)
}

pub fn balance_projector_with_limits<F: Field + ExactRing>(
    left: usize,
    right: usize,
    limits: OperationLimits,
) -> Result<BasicMatrix<F>, ComplexTensorError> {
    let n = carrier(left, right)?;
    let size = element_count(4, n)?;
    charge(limits, element_count(size, size)?, 4)?;
    let h = half::<F>()?;
    let minus_h = h.try_neg()?;
    Ok(mx::from_fn_with_limits(size, size, limits, |row, col| {
        let (a, b, i, j) = coordinate(row, left, right);
        let (c, d, k, l) = coordinate(col, left, right);
        if i != k || j != l {
            F::zero()
        } else if a == c && b == d {
            h.clone()
        } else if a != c && b != d {
            if a == b {
                minus_h.clone()
            } else {
                h.clone()
            }
        } else {
            F::zero()
        }
    })?)
}

fn doubled_shape(
    operand: &'static str,
    shape: (usize, usize),
) -> Result<(usize, usize), ComplexTensorError> {
    if shape.0 % 2 != 0 || shape.1 % 2 != 0 {
        return Err(ComplexTensorError::NotDoubled {
            operand,
            rows: shape.0,
            cols: shape.1,
        });
    }
    Ok((shape.0 / 2, shape.1 / 2))
}

fn require_image<F: Field + ExactRing>(
    operand: &'static str,
    matrix: &BasicMatrix<F>,
) -> Result<(), ComplexTensorError> {
    let (m, n) = doubled_shape(operand, matrix.shape())?;
    for row in 0..m {
        for col in 0..n {
            let at = |r, c| &matrix.as_slice()[r * matrix.cols() + c];
            if at(row, col) != at(m + row, n + col) || *at(row, n + col) != at(m + row, col).try_neg()? {
                return Err(ComplexTensorError::ComplexStructure { operand, row, col });
            }
        }
    }
    Ok(())
}

pub fn normalized_tensor_with_limits<F: Field + ExactRing>(
    left: &BasicMatrix<F>,
    right: &BasicMatrix<F>,
    limits: OperationLimits,
) -> Result<BasicMatrix<F>, ComplexTensorError> {
    tensor(left, right, true, limits)
}

pub fn unscaled_tensor_with_limits<F: Field + ExactRing>(
    left: &BasicMatrix<F>,
    right: &BasicMatrix<F>,
    limits: OperationLimits,
) -> Result<BasicMatrix<F>, ComplexTensorError> {
    tensor(left, right, false, limits)
}

pub fn tensor_work_bound(
    left: (usize, usize),
    right: (usize, usize),
    normalized: bool,
) -> Result<(usize, usize), ComplexTensorError> {
    let (a, c) = doubled_shape("left", left)?;
    let (b, d) = doubled_shape("right", right)?;
    let r = carrier(a, b)?;
    let s = carrier(c, d)?;
    let rs = times(r, s)?;
    let elements = times(16, rs)?
        .max(times(8, times(r, r)?)?)
        .max(times(8, times(s, s)?)?);
    let multiply_ops = plus(times(64, times(r, rs)?)?, times(32, times(s, rs)?)?)?;
    let scalar_ops = plus(
        plus(multiply_ops, times(if normalized { 20 } else { 16 }, rs)?)?,
        plus(
            plus(element_count(a, c)?, element_count(b, d)?)?,
            if normalized { 5 } else { 2 },
        )?,
    )?;
    Ok((elements, scalar_ops))
}

fn tensor<F: Field + ExactRing>(
    left: &BasicMatrix<F>,
    right: &BasicMatrix<F>,
    normalized: bool,
    limits: OperationLimits,
) -> Result<BasicMatrix<F>, ComplexTensorError> {
    let (elements, scalar_ops) = tensor_work_bound(left.shape(), right.shape(), normalized)?;
    charge(limits, elements, scalar_ops)?;
    let (a, c) = doubled_shape("left", left.shape())?;
    let (b, d) = doubled_shape("right", right.shape())?;
    require_image("left", left)?;
    require_image("right", right)?;
    let scale = if normalized { Some(half::<F>()?) } else { None };
    let output = balance_map_with_limits(a, b, limits)?;
    let input = balance_map_with_limits(c, d, limits)?;
    let product = mx::kronecker_with_limits(left, right, limits)?;
    let intermediate = mx::multiply_with_limits(&output, &product, limits)?;
    let result = mx::multiply_with_limits(&intermediate, &mx::transpose(&input)?, limits)?;
    Ok(if let Some(scale) = scale {
        mx::scale(&result, &scale)?
    } else {
        result
    })
}

pub fn balanced_lift_with_limits<F: Field + ExactRing>(
    view: &BasicMatrix<F>,
    left: usize,
    right: usize,
    limits: OperationLimits,
) -> Result<BasicMatrix<F>, ComplexTensorError> {
    let n = carrier(left, right)?;
    let size = element_count(2, n)?;
    if view.shape() != (size, size) {
        return Err(ExactFieldError::ShapeMismatch {
            operation: "balanced tensor lift",
            left: view.shape(),
            right: (size, size),
        }
        .into());
    }
    let square = times(n, n)?;
    charge(
        limits,
        times(16, square)?,
        plus(plus(times(96, times(square, n)?)?, times(17, square)?)?, 4)?,
    )?;
    require_image("view", view)?;
    let h = half::<F>()?;
    let map = balance_map_with_limits(left, right, limits)?;
    let first = mx::multiply_with_limits(&mx::transpose(&map)?, view, limits)?;
    Ok(mx::scale(
        &mx::multiply_with_limits(&first, &map, limits)?,
        &h,
    )?)
}

#[cfg(test)]
mod tests;
