//! Exact periodic and aperiodic sectors of a declared finite unitary step.
//! Finite order is decided from cyclotomic characteristic factors and replay of
//! the resulting order; an unbounded-looking orbit is never certified by sampling.
//! AuthorityEffect: None.
use linear_algebra::backend::basic_matrix::BasicMatrix;
use linear_algebra::exact_field::{involution, ExactFieldError};
use omega_lie_theory::finite_order::{gaussian_finite_order, FiniteOrderError};
use omega_number_theory::cyclotomic::GaussianRat;
#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum DynamicsDichotomyError {
    #[error("the declared finite step is not unitary")]
    NotUnitary,
    #[error(transparent)]
    Matrix(#[from] ExactFieldError),
    #[error(transparent)]
    Order(#[from] FiniteOrderError),
}
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum UnitaryOrbit {
    Periodic { order: usize },
    Aperiodic,
}
/// Classifies a Q(i)-unitary of dimension at most eight, using the sovereign
/// exact finite-order decision on its faithful rational representation.
pub fn classify_unitary_orbit(
    step: &BasicMatrix<GaussianRat>,
) -> Result<UnitaryOrbit, DynamicsDichotomyError> {
    if !involution::is_unitary(step)? {
        return Err(DynamicsDichotomyError::NotUnitary);
    }
    Ok(match gaussian_finite_order(step)? {
        Some(order) => UnitaryOrbit::Periodic { order },
        None => UnitaryOrbit::Aperiodic,
    })
}
