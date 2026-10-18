//! Discrete Dirac spinor field on simplicial complexes.
//!
//! Origin: papers/derivations/general_relativity/rust/src/spinor_field.rs
//! Claim: DERIV-GR-SPINOR-001
//! AuthorityEffect: None.

use num_rational::Ratio;
use num_traits::Zero;
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum SpinorError {
    DimensionMismatch,
    NonConservedFermionCurrent,
}

/// A discrete 4-component Dirac spinor psi on a vertex.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct DiscreteSpinor {
    pub vertex: usize,
    /// Rational real and imaginary parts of 4 spinor components
    pub components: Vec<(Ratio<i64>, Ratio<i64>)>,
}

impl DiscreteSpinor {
    pub fn new(vertex: usize, components: Vec<(Ratio<i64>, Ratio<i64>)>) -> Self {
        Self { vertex, components }
    }

    /// Probability density / fermion current rho = sum (|re|^2 + |im|^2).
    pub fn probability_density(&self) -> Ratio<i64> {
        let mut sum = Ratio::zero();
        for (re, im) in &self.components {
            sum += (*re) * (*re) + (*im) * (*im);
        }
        sum
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn spinor_norm() {
        let spinor = DiscreteSpinor::new(
            0,
            vec![
                (Ratio::new(1, 2), Ratio::zero()),
                (Ratio::new(1, 2), Ratio::zero()),
                (Ratio::new(1, 2), Ratio::zero()),
                (Ratio::new(1, 2), Ratio::zero()),
            ],
        );
        // 4 * (1/4) = 1
        assert_eq!(spinor.probability_density(), Ratio::from_integer(1));
    }
}
