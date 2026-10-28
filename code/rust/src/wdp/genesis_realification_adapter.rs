
use crate::types::AuthorityEffect;
use linear_algebra::backend::basic_matrix::{BasicMatrix, OperationLimits};
use tfqm_number_theory::rational::Rational;
use omega_quantum_physics::complex_realification::{self, ComplexTensorError};
use omega_quantum_physics::exact_instrument::ExactDensityState;

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DeclaredRealComposite {
    left_dimension: usize,
    right_dimension: usize,
    view: BasicMatrix<Rational>,
    balanced_state: BasicMatrix<Rational>,
}

impl DeclaredRealComposite {
    pub fn from_complex(
        state: &ExactDensityState,
        left_dimension: usize,
        right_dimension: usize,
        limits: OperationLimits,
    ) -> Result<Self, ComplexTensorError> {
        let (view, balanced_state) = complex_realification::composite_density_views_with_limits(
            state,
            left_dimension,
            right_dimension,
            limits,
        )?;
        Ok(Self {
            left_dimension,
            right_dimension,
            view,
            balanced_state,
        })
    }

    pub fn local_dimensions(&self) -> (usize, usize) {
        (self.left_dimension, self.right_dimension)
    }

    pub fn real_view(&self) -> &BasicMatrix<Rational> {
        &self.view
    }

    pub fn balanced_state(&self) -> &BasicMatrix<Rational> {
        &self.balanced_state
    }

    pub fn authority_effect(&self) -> AuthorityEffect {
        AuthorityEffect::None
    }
}
