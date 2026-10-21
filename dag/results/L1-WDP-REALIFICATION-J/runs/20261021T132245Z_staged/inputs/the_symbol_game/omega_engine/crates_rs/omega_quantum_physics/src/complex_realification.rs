//! Exact Q(i) realizations of a declared complex structure and balanced tensor.
//! Generic maps, quotient balancing and matrix arithmetic belong to linear_algebra.
//! Density inputs have already been admitted by ExactDensityState. No reconstruction
//! or authority follows from this representation. AuthorityEffect: None.

use crate::exact_instrument::ExactDensityState;
use linear_algebra::backend::basic_matrix::{BasicMatrix, MatrixError, OperationLimits};
pub use linear_algebra::exact_field::complex_tensor::ComplexTensorError;
use linear_algebra::exact_field::{complex_tensor as ct, matrix as mx};
use omega_number_theory::cyclotomic::GaussianRat;
use omega_number_theory::rational::{rq, Rational};

fn product(a: usize, b: usize) -> Result<usize, ComplexTensorError> {
    Ok(a.checked_mul(b)
        .ok_or(MatrixError::DimensionOverflow { rows: a, cols: b })?)
}

fn add(a: usize, b: usize) -> Result<usize, ComplexTensorError> {
    Ok(a.checked_add(b)
        .ok_or(MatrixError::OperationCountOverflow)?)
}

fn admit(limits: OperationLimits, elements: usize, calls: usize) -> Result<(), ComplexTensorError> {
    if elements > limits.max_elements {
        return Err(MatrixError::AllocationLimitExceeded {
            requested: elements,
            limit: limits.max_elements,
        }
        .into());
    }
    if calls > limits.max_scalar_ops {
        return Err(MatrixError::OperationLimitExceeded {
            requested: calls,
            limit: limits.max_scalar_ops,
        }
        .into());
    }
    Ok(())
}

/// Rectangular block realification; all real coordinates precede imaginary ones.
pub fn realify_operator_with_limits(
    operator: &BasicMatrix<GaussianRat>,
    limits: OperationLimits,
) -> Result<BasicMatrix<Rational>, ComplexTensorError> {
    let (m, n) = operator.shape();
    let count = product(m, n)?;
    product(2, m)?;
    product(2, n)?;
    admit(limits, product(4, count)?, count)?;
    let real = mx::from_fn_with_limits(m, n, limits, |r, c| {
        operator.as_slice()[r * n + c].re.clone()
    })?;
    let imaginary = mx::from_fn_with_limits(m, n, limits, |r, c| {
        operator.as_slice()[r * n + c].im.clone()
    })?;
    ct::realify_parts_with_limits(&real, &imaginary, limits)
}

/// Trace-one real state `R(rho)/2`; uses the admitted complex density as its premise.
pub fn realify_density_with_limits(
    state: &ExactDensityState,
    limits: OperationLimits,
) -> Result<BasicMatrix<Rational>, ComplexTensorError> {
    let count = product(state.dimension(), state.dimension())?;
    admit(limits, product(4, count)?, product(5, count)?)?;
    Ok(mx::scale(
        &realify_operator_with_limits(state.matrix(), limits)?,
        &rq(1, 2),
    )?)
}

fn tensor_preflight(
    left: (usize, usize),
    right: (usize, usize),
    density: bool,
    limits: OperationLimits,
) -> Result<(), ComplexTensorError> {
    let left_count = product(left.0, left.1)?;
    let right_count = product(right.0, right.1)?;
    let left_real = (product(2, left.0)?, product(2, left.1)?);
    let right_real = (product(2, right.0)?, product(2, right.1)?);
    let (elements, calls) = ct::tensor_work_bound(left_real, right_real, !density)?;
    let conversion = product(if density { 5 } else { 1 }, add(left_count, right_count)?)?;
    admit(
        limits,
        elements
            .max(product(4, left_count)?)
            .max(product(4, right_count)?),
        add(calls, conversion)?,
    )
}

/// The realification of the ordinary complex tensor of two declared operators.
/// Includes all conversion and balancing costs in one preflight.
pub fn product_operator_with_limits(
    left: &BasicMatrix<GaussianRat>,
    right: &BasicMatrix<GaussianRat>,
    limits: OperationLimits,
) -> Result<BasicMatrix<Rational>, ComplexTensorError> {
    tensor_preflight(left.shape(), right.shape(), false, limits)?;
    ct::normalized_tensor_with_limits(
        &realify_operator_with_limits(left, limits)?,
        &realify_operator_with_limits(right, limits)?,
        limits,
    )
}

/// `T (R(rho_left)/2 tensor R(rho_right)/2) T^t`, with trace one.
/// This product-state normalization differs from operator compression.
pub fn product_density_with_limits(
    left: &ExactDensityState,
    right: &ExactDensityState,
    limits: OperationLimits,
) -> Result<BasicMatrix<Rational>, ComplexTensorError> {
    tensor_preflight(left.matrix().shape(), right.matrix().shape(), true, limits)?;
    ct::unscaled_tensor_with_limits(
        &realify_density_with_limits(left, limits)?,
        &realify_density_with_limits(right, limits)?,
        limits,
    )
}

/// Lift any admitted complex composite, including entangled states, into the
/// ordinary doubled real tensor with support P: `T^t R(rho) T / 4`.
/// The declared dimensions must multiply to the actual density dimension.
pub fn lift_composite_density_with_limits(
    state: &ExactDensityState,
    left: usize,
    right: usize,
    limits: OperationLimits,
) -> Result<BasicMatrix<Rational>, ComplexTensorError> {
    Ok(composite_density_views_with_limits(state, left, right, limits)?.1)
}

/// Return the `2mn` real view and its normalized `4mn` balanced lift with one
/// shared conversion and one aggregate preflight.
pub fn composite_density_views_with_limits(
    state: &ExactDensityState,
    left: usize,
    right: usize,
    limits: OperationLimits,
) -> Result<(BasicMatrix<Rational>, BasicMatrix<Rational>), ComplexTensorError> {
    let n = product(left, right)?;
    if state.dimension() != n {
        return Err(
            linear_algebra::exact_field::ExactFieldError::ShapeMismatch {
                operation: "declared complex tensor density",
                left: state.matrix().shape(),
                right: (n, n),
            }
            .into(),
        );
    }
    let square = product(n, n)?;
    let cubic = product(square, n)?;
    let calls = add(add(product(96, cubic)?, product(22, square)?)?, 4)?;
    admit(limits, product(16, square)?, calls)?;
    let view = realify_density_with_limits(state, limits)?;
    let lifted = ct::balanced_lift_with_limits(&view, left, right, limits)?;
    Ok((view, lifted))
}
