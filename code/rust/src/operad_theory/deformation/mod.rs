//! Deformation theory, cooperads, and homotopy algebras.
//!
//! Origin: papers/derivations/operad_theory/rust/src/deformation/mod.rs
//! Claim: DERIV-OPERAD-DEF-001
//! AuthorityEffect: None.

pub mod bar_cobar;
pub mod cooperad;
pub mod quadratic_operad;

use num_rational::Ratio;
use num_traits::{One, Zero};
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum DeformationError {
    ObstructionNonZero(Ratio<i64>),
    GradingMismatch,
}

/// Evaluates deformation cohomology and Maurer-Cartan equation: d(x) + 1/2 [x, x] = 0.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct DeformationComplex {
    pub degree: usize,
    pub maurer_cartan_residual: Ratio<i64>,
}

impl DeformationComplex {
    pub fn new(degree: usize, residual: Ratio<i64>) -> Self {
        Self {
            degree,
            maurer_cartan_residual: residual,
        }
    }

    /// Verifies that the Maurer-Cartan residual vanishes exactly: MC(x) = 0.
    pub fn is_formal_deformation(&self) -> Result<bool, DeformationError> {
        if !self.maurer_cartan_residual.is_zero() {
            return Err(DeformationError::ObstructionNonZero(
                self.maurer_cartan_residual,
            ));
        }
        Ok(true)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_deformation_mc() {
        let comp = DeformationComplex::new(1, Ratio::zero());
        assert!(comp.is_formal_deformation().unwrap());

        let obstructed = DeformationComplex::new(1, Ratio::new(1, 4));
        assert!(obstructed.is_formal_deformation().is_err());
    }
}
