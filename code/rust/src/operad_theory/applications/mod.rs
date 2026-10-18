//! Operadic applications pipeline and domain modeling over finite complexes.
//!
//! Origin: papers/derivations/operad_theory/rust/src/applications/mod.rs
//! Claim: DERIV-OPERAD-APP-001
//! AuthorityEffect: None.

use num_rational::Ratio;
use num_traits::{One, Zero};
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum ApplicationError {
    StageExhaustion,
    InvalidArityMapping,
}

/// Pipeline processor for operadic algebraic representations.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct OperadPipeline {
    pub name: String,
    pub operations_discharged: usize,
    pub exact_contraction_factors: Vec<Ratio<i64>>,
}

impl OperadPipeline {
    pub fn new(name: impl Into<String>) -> Self {
        Self {
            name: name.into(),
            operations_discharged: 0,
            exact_contraction_factors: Vec::new(),
        }
    }

    pub fn record_contraction(&mut self, factor: Ratio<i64>) -> Result<(), ApplicationError> {
        if factor <= Ratio::zero() || factor > Ratio::one() {
            return Err(ApplicationError::InvalidArityMapping);
        }
        self.exact_contraction_factors.push(factor);
        self.operations_discharged += 1;
        Ok(())
    }

    pub fn net_contraction(&self) -> Ratio<i64> {
        self.exact_contraction_factors.iter().copied().product()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_operad_pipeline() {
        let mut pipe = OperadPipeline::new("StasheffPipeline");
        pipe.record_contraction(Ratio::new(1, 2)).unwrap();
        pipe.record_contraction(Ratio::new(1, 3)).unwrap();
        assert_eq!(pipe.operations_discharged, 2);
        assert_eq!(pipe.net_contraction(), Ratio::new(1, 6));
    }
}
