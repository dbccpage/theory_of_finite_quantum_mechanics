//! A declared finite complex realization mapped to its balanced real tensor.
//! State admission stays with the quantum owner, and balancing with the math owner.
//! These maps preserve a supplied operational model; they select no scalar/Born
//! axioms from the primitive mark and grant no execution permission.

use crate::types::AuthorityEffect;
use linear_algebra::backend::basic_matrix::{BasicMatrix, OperationLimits};
use omega_number_theory::rational::Rational;
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
    /// The caller supplies the actual complex composite and its local dimensions.
    /// Entangled inputs are allowed. Arithmetic refusal never grants admission.
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
