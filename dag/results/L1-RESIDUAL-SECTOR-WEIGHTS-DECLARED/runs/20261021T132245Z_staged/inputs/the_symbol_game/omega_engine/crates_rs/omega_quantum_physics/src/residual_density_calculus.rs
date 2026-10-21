// AuthorityEffect: None.

//! Exact pointer states, nonselective sector measurements, stochastic mass
//! transport and unitary conjugation. Programme ledgers and coherence
//! admission records live in the finite-QM native campaign.

use crate::exact_hermitian::{self};
use linear_algebra::backend::basic_matrix::{BasicMatrix, OperationLimits};
use linear_algebra::exact_field::{involution, matrix};

use omega_number_theory::cyclotomic::GaussianRat;
use omega_number_theory::rational::Rational;

/// Refusals for ledgers, densities and channels.
#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum ResidualDensityError {
    #[error(transparent)]
    ExactAlgebra(#[from] linear_algebra::exact_field::ExactFieldError),
    #[error(transparent)]
    Storage(#[from] linear_algebra::backend::basic_matrix::MatrixError),
    #[error("no sectors were declared")]
    Empty,
    #[error("sector {index} has negative mass")]
    NegativeMass { index: usize },
    #[error("total mass is zero")]
    ZeroTotalMass,
    #[error("matrix is not square with one row per sector")]
    Shape,
    #[error("density has a nonzero off-diagonal entry at ({row}, {col})")]
    OffDiagonal { row: usize, col: usize },
    #[error("density is not PSD with unit trace")]
    NotADensity,
    #[error("channel row {row} is negative or does not sum to one")]
    NotRowStochastic { row: usize },
    #[error("the conjugating matrix is not unitary")]
    NotUnitary,
    #[error("pointer carrier exceeds the finite dimension bound {limit}")]
    ResourceBudget { limit: usize },
    #[error(transparent)]
    Stochastic(#[from] omega_finite_probability::error::ClassicalShadowError),
}
pub const MAX_POINTER_DIMENSION: usize = 128;
const LIMITS: OperationLimits = OperationLimits {
    max_elements: 1 << 20,
    max_scalar_ops: 1 << 24,
};

/// `Tr(|s><s| rho)` for every sector `s`: the sector-basis measurement.
pub fn sector_measurement(
    rho: &BasicMatrix<GaussianRat>,
) -> Result<Vec<Rational>, ResidualDensityError> {
    if rho.rows() > MAX_POINTER_DIMENSION {
        return Err(ResidualDensityError::ResourceBudget {
            limit: MAX_POINTER_DIMENSION,
        });
    }
    if rho.rows() != rho.cols() || rho.rows() == 0 {
        return Err(ResidualDensityError::Shape);
    }
    if !exact_hermitian::is_positive_semidefinite(rho) || matrix::trace(&rho)? != GaussianRat::one()
    {
        return Err(ResidualDensityError::NotADensity);
    }
    Ok((0..rho.rows())
        .map(|s| {
            rho.get_ref(s, s)
                .expect("validated density dimension")
                .re
                .clone()
        })
        .collect())
}

/// `out_j = sum_i mu_i K_ij` for a row-stochastic `K`.
pub fn row_stochastic_pushforward(
    channel: &BasicMatrix<Rational>,
    masses: &[Rational],
) -> Result<Vec<Rational>, ResidualDensityError> {
    use omega_finite_probability::{error::ClassicalShadowError, stochastic_map::StochasticMap};
    if channel.rows() != masses.len() || masses.is_empty() {
        return Err(ResidualDensityError::Shape);
    }
    let width = channel.cols();
    if masses.len() > MAX_POINTER_DIMENSION || width > MAX_POINTER_DIMENSION {
        return Err(ResidualDensityError::ResourceBudget {
            limit: MAX_POINTER_DIMENSION,
        });
    }
    if masses.len().checked_mul(width).is_none_or(|n| n > 1 << 20) {
        return Err(ResidualDensityError::Shape);
    }
    StochasticMap::try_from_basic_matrix(channel, "residual mass transport").map_err(|error| {
        match error {
            ClassicalShadowError::RowNotNormalized { row, .. } => {
                ResidualDensityError::NotRowStochastic { row }
            }
            ClassicalShadowError::NegativeEntry { index } => {
                ResidualDensityError::NotRowStochastic { row: index / width }
            }
            other => ResidualDensityError::Stochastic(other),
        }
    })?;
    // The linear extension also accepts signed difference vectors, so this
    // same map witnesses classical l1 contraction of quantum differences.
    Ok(matrix::multiply_vector_with_limits(
        &matrix::transpose(channel)?,
        masses,
        LIMITS,
    )?)
}

/// Conjugate a density by a unitary: `U rho U*`. Used to exhibit phase-sensitive mixing.
/// Refused unless both matrices are square of one size and `U U* = I`.
pub fn conjugate(
    unitary: &BasicMatrix<GaussianRat>,
    rho: &BasicMatrix<GaussianRat>,
) -> Result<BasicMatrix<GaussianRat>, ResidualDensityError> {
    if unitary.rows() > MAX_POINTER_DIMENSION {
        return Err(ResidualDensityError::ResourceBudget {
            limit: MAX_POINTER_DIMENSION,
        });
    }
    if unitary.rows() != unitary.cols() || rho.rows() != rho.cols() || unitary.rows() != rho.rows()
    {
        return Err(ResidualDensityError::Shape);
    }
    if matrix::multiply(&unitary, &involution::adjoint(&unitary)?)?
        != matrix::identity(unitary.rows())?
    {
        return Err(ResidualDensityError::NotUnitary);
    }
    Ok(matrix::multiply(
        &matrix::multiply(&unitary, rho)?,
        &involution::adjoint(&unitary)?,
    )?)
}

/// Pointer-state embedding of exact positive masses using the shared normalized
/// probability constructor, with no ledger or governance admission object.
pub fn diagonal_density_from_masses(
    masses: &[Rational],
) -> Result<BasicMatrix<GaussianRat>, ResidualDensityError> {
    if masses.len() > MAX_POINTER_DIMENSION {
        return Err(ResidualDensityError::ResourceBudget {
            limit: MAX_POINTER_DIMENSION,
        });
    }
    let p = omega_functional::born_probabilities::BornProbabilities::from_weights(masses).map_err(
        |e| match e {
            omega_functional::born_probabilities::BornProbabilityError::EmptyInput => {
                ResidualDensityError::Empty
            }
            omega_functional::born_probabilities::BornProbabilityError::NegativeWeight {
                index,
            } => ResidualDensityError::NegativeMass { index },
            _ => ResidualDensityError::ZeroTotalMass,
        },
    )?;
    Ok(matrix::diagonal(
        &p.probabilities()
            .iter()
            .cloned()
            .map(GaussianRat::from_rational)
            .collect::<Vec<_>>(),
    )?)
}
/// Nonselective measurement in the pointer basis. This is an idempotent CPTP
/// pinching map; positivity and unit trace are checked on the input.
pub fn pointer_pinching(
    rho: &BasicMatrix<GaussianRat>,
) -> Result<BasicMatrix<GaussianRat>, ResidualDensityError> {
    let probabilities = sector_measurement(rho)?;
    Ok(matrix::diagonal(
        &probabilities
            .into_iter()
            .map(GaussianRat::from_rational)
            .collect::<Vec<_>>(),
    )?)
}
#[cfg(test)]
mod pointer_tests {
    use super::*;
    use crate::exact_hermitian::gq;
    use omega_number_theory::rational::rq;
    #[test]
    fn pointer_pinching_preserves_populations_and_is_idempotent() {
        let rho = matrix::from_rows(vec![
            vec![gq(1, 2, 0, 1), gq(0, 1, 1, 2)],
            vec![gq(0, 1, -1, 2), gq(1, 2, 0, 1)],
        ])
        .unwrap();
        let diagonal = pointer_pinching(&rho).unwrap();
        assert_eq!(
            sector_measurement(&rho).unwrap(),
            sector_measurement(&diagonal).unwrap()
        );
        assert_eq!(pointer_pinching(&diagonal).unwrap(), diagonal);
        assert_eq!(
            diagonal,
            diagonal_density_from_masses(&[rq(3, 1), rq(3, 1)]).unwrap()
        );
        assert_ne!(rho, diagonal);
        assert!(matches!(
            diagonal_density_from_masses(&vec![rq(1, 1); MAX_POINTER_DIMENSION + 1]),
            Err(ResidualDensityError::ResourceBudget { .. })
        ));
        assert!(matches!(
            row_stochastic_pushforward(
                &BasicMatrix::from_row_major(MAX_POINTER_DIMENSION + 1, 0, vec![]).unwrap(),
                &vec![rq(1, 1); MAX_POINTER_DIMENSION + 1]
            ),
            Err(ResidualDensityError::ResourceBudget { .. })
        ));
    }
}
