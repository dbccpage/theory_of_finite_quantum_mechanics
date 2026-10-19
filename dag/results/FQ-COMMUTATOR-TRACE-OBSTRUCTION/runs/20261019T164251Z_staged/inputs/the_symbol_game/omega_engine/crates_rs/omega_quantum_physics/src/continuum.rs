//! Exact finite canonical-commutator obstruction and Weyl certificates.
//! Finite trace cyclicity blocks [A,B]=lambda I for lambda!=0 in nonzero
//! dimension. Finite Weyl systems do not remove that obstruction.
//! AuthorityEffect: None.
use crate::exact_hermitian::{self, ExactHermitianError};
use linear_algebra::backend::basic_matrix::BasicMatrix;
use omega_number_theory::cyclotomic::GaussianRat;
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct CanonicalCommutatorObstruction {
    pub dimension: usize,
    pub trace_commutator: GaussianRat,
    pub trace_target: GaussianRat,
    pub equality_obstructed: bool,
}
pub fn canonical_commutator_obstruction(
    a: &BasicMatrix<GaussianRat>,
    b: &BasicMatrix<GaussianRat>,
    lambda: &GaussianRat,
) -> Result<CanonicalCommutatorObstruction, ExactHermitianError> {
    let n = exact_hermitian::square_dim(a)?;
    let m = exact_hermitian::square_dim(b)?;
    if n != m {
        return Err(ExactHermitianError::ShapeMismatch {
            expected: n,
            actual: m,
        });
    }
    let limits = linear_algebra::backend::basic_matrix::OperationLimits {
        max_elements: 1 << 20,
        max_scalar_ops: 1 << 24,
    };
    let ab = linear_algebra::exact_field::matrix::multiply_with_limits(a, b, limits)?;
    let ba = linear_algebra::exact_field::matrix::multiply_with_limits(b, a, limits)?;
    let trace_commutator = linear_algebra::exact_field::matrix::trace(
        &linear_algebra::exact_field::matrix::sub(&ab, &ba)?,
    )?;
    let trace_target =
        linear_algebra::exact_field::matrix::trace(&linear_algebra::exact_field::matrix::scale(
            &linear_algebra::exact_field::matrix::identity_with_limits::<GaussianRat>(n, limits)?,
            lambda,
        )?)?;
    let equality_obstructed = trace_commutator != trace_target;
    Ok(CanonicalCommutatorObstruction {
        dimension: n,
        trace_commutator,
        trace_target,
        equality_obstructed,
    })
}
