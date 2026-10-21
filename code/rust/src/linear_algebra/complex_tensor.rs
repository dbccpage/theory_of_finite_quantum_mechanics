use super::{charge, element_count, inverse_of, matrix as mx, plus, times, ExactFieldError};
use crate::linear_algebra::basic_matrix::{BasicMatrix, MatrixError, OperationLimits};
use crate::linear_algebra::scalars::{ExactRing, Field};

#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum ComplexTensorError {
    #[error("scalar arithmetic: {0}")]
    Scalar(#[from] crate::linear_algebra::scalars::ScalarError),
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
    if two.try_is_zero()? {
        return Err(ExactFieldError::CharacteristicTwo {
            operation: "complex tensor normalization",
        }
        .into());
    }
    let h = inverse_of("complex tensor normalization", &two)?;
    if two.try_mul(&h)? != one {
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

fn realify_entry<F: Field + ExactRing>(
    real: &BasicMatrix<F>,
    imaginary: &BasicMatrix<F>,
    m: usize,
    n: usize,
    row: usize,
    col: usize,
) -> Result<F, ExactFieldError> {
    let index = (row % m) * n + col % n;
    match (row / m, col / n) {
        (0, 1) => Ok(imaginary.as_slice()[index].try_neg()?),
        (1, 0) => Ok(imaginary.as_slice()[index].clone()),
        _ => Ok(real.as_slice()[index].clone()),
    }
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
    Ok(mx::try_from_fn_with_limits(
        rows,
        cols,
        limits,
        |row, col| realify_entry(real, imaginary, m, n, row, col),
    )?)
}

fn balance_map_entry<F: Field + ExactRing>(
    row: usize,
    col: usize,
    left: usize,
    right: usize,
    n: usize,
    one: &F,
    minus_one: &F,
) -> F {
    let (a, b, i, j) = coordinate(col, left, right);
    if row % n != i * right + j {
        return F::zero();
    }
    match (row / n, a, b) {
        (0, 0, 0) | (1, 0, 1) | (1, 1, 0) => one.clone(),
        (0, 1, 1) => minus_one.clone(),
        _ => F::zero(),
    }
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
        balance_map_entry(row, col, left, right, n, &one, &minus_one)
    })?)
}

fn balance_projector_entry<F: Field + ExactRing>(
    row: usize,
    col: usize,
    left: usize,
    right: usize,
    h: &F,
    minus_h: &F,
) -> F {
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
        balance_projector_entry(row, col, left, right, &h, &minus_h)
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
    super::validate_values(matrix.as_slice())?;
    for row in 0..m {
        for col in 0..n {
            let at = |r, c| &matrix.as_slice()[r * matrix.cols() + c];
            if at(row, col) != at(m + row, n + col)
                || *at(row, n + col) != at(m + row, col).try_neg()?
            {
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

fn tensor_work_elements(r: usize, s: usize, rs: usize) -> Result<usize, ComplexTensorError> {
    let r_sq = times(r, r)?;
    let s_sq = times(s, s)?;
    let rs_elem = times(16, rs)?;
    let r_elem = times(8, r_sq)?;
    let s_elem = times(8, s_sq)?;
    Ok(rs_elem.max(r_elem).max(s_elem))
}

fn tensor_multiply_ops(r: usize, s: usize, rs: usize) -> Result<usize, ComplexTensorError> {
    let r_rs = times(r, rs)?;
    let s_rs = times(s, rs)?;
    let ops_r = times(64, r_rs)?;
    let ops_s = times(32, s_rs)?;
    Ok(plus(ops_r, ops_s)?)
}

fn tensor_overhead_ops(
    a: usize,
    b: usize,
    c: usize,
    d: usize,
    overhead: usize,
) -> Result<usize, ComplexTensorError> {
    let in_ab = element_count(a, c)?;
    let in_cd = element_count(b, d)?;
    let input_elements = plus(in_ab, in_cd)?;
    Ok(plus(input_elements, overhead)?)
}

fn tensor_work_scalar_ops(
    r: usize,
    s: usize,
    rs: usize,
    a: usize,
    b: usize,
    c: usize,
    d: usize,
    normalized: bool,
) -> Result<usize, ComplexTensorError> {
    let multiply_ops = tensor_multiply_ops(r, s, rs)?;
    let coeff = if normalized { 20 } else { 16 };
    let overhead = if normalized { 5 } else { 2 };
    let tail_ops = tensor_overhead_ops(a, b, c, d, overhead)?;
    let main_ops = plus(multiply_ops, times(coeff, rs)?)?;
    Ok(plus(main_ops, tail_ops)?)
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
    let elements = tensor_work_elements(r, s, rs)?;
    let scalar_ops = tensor_work_scalar_ops(r, s, rs, a, b, c, d, normalized)?;
    Ok((elements, scalar_ops))
}

fn compute_tensor_product<F: Field + ExactRing>(
    left: &BasicMatrix<F>,
    right: &BasicMatrix<F>,
    output_map: &BasicMatrix<F>,
    input_map: &BasicMatrix<F>,
    limits: OperationLimits,
) -> Result<BasicMatrix<F>, ComplexTensorError> {
    let product = mx::kronecker_with_limits(left, right, limits)?;
    let intermediate = mx::multiply_with_limits(output_map, &product, limits)?;
    let input_trans = mx::transpose(input_map)?;
    Ok(mx::multiply_with_limits(&intermediate, &input_trans, limits)?)
}

fn balance_maps_for_tensor<F: Field + ExactRing>(
    left: &BasicMatrix<F>,
    right: &BasicMatrix<F>,
    limits: OperationLimits,
) -> Result<(BasicMatrix<F>, BasicMatrix<F>), ComplexTensorError> {
    let (a, c) = doubled_shape("left", left.shape())?;
    let (b, d) = doubled_shape("right", right.shape())?;
    require_image("left", left)?;
    require_image("right", right)?;
    let output = balance_map_with_limits(a, b, limits)?;
    let input = balance_map_with_limits(c, d, limits)?;
    Ok((output, input))
}

fn scale_tensor_result<F: Field + ExactRing>(
    result: BasicMatrix<F>,
    normalized: bool,
) -> Result<BasicMatrix<F>, ComplexTensorError> {
    if normalized {
        let scale = half::<F>()?;
        Ok(mx::scale(&result, &scale)?)
    } else {
        Ok(result)
    }
}

fn tensor<F: Field + ExactRing>(
    left: &BasicMatrix<F>,
    right: &BasicMatrix<F>,
    normalized: bool,
    limits: OperationLimits,
) -> Result<BasicMatrix<F>, ComplexTensorError> {
    let (elements, scalar_ops) = tensor_work_bound(left.shape(), right.shape(), normalized)?;
    charge(limits, elements, scalar_ops)?;
    let (output, input) = balance_maps_for_tensor(left, right, limits)?;
    let result = compute_tensor_product(left, right, &output, &input, limits)?;
    scale_tensor_result(result, normalized)
}

fn charge_balanced_lift_budget(
    n: usize,
    limits: OperationLimits,
) -> Result<(), ComplexTensorError> {
    let square = times(n, n)?;
    let sq_n = times(square, n)?;
    let ops_a = times(96, sq_n)?;
    let ops_b = times(17, square)?;
    let total_ops = plus(plus(ops_a, ops_b)?, 4)?;
    charge(limits, times(16, square)?, total_ops)?;
    Ok(())
}

fn compute_balanced_lift<F: Field + ExactRing>(
    view: &BasicMatrix<F>,
    left: usize,
    right: usize,
    limits: OperationLimits,
) -> Result<BasicMatrix<F>, ComplexTensorError> {
    let h = half::<F>()?;
    let map = balance_map_with_limits(left, right, limits)?;
    let map_t = mx::transpose(&map)?;
    let first = mx::multiply_with_limits(&map_t, view, limits)?;
    let second = mx::multiply_with_limits(&first, &map, limits)?;
    Ok(mx::scale(&second, &h)?)
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
    charge_balanced_lift_budget(n, limits)?;
    require_image("view", view)?;
    compute_balanced_lift(view, left, right, limits)
}

#[cfg(test)]
mod tests;
