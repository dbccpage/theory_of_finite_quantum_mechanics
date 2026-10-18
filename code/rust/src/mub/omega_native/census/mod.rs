//! Exact census auditor and partition validation for MUB(6) solution candidates.
//!
//! Origin: papers/derivations/mub/rust/src/omega_native/census/mod.rs
//! Claim: MUB6-CENSUS-001
//! AuthorityEffect: None.

pub mod catalog;
pub mod partition;

use num_rational::Ratio;
use num_traits::{One, Zero};
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum CensusError {
    InvalidCount(String),
    PopulationNegative,
    WeightSumMismatch,
}

/// Exact solution census auditor for finite search spaces.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct CensusAuditor {
    pub category: String,
    pub isolated_count: usize,
    pub continuous_families: usize,
    pub exact_weights: Vec<Ratio<i64>>,
}

impl CensusAuditor {
    pub fn new(category: impl Into<String>, isolated: usize, families: usize) -> Self {
        Self {
            category: category.into(),
            isolated_count: isolated,
            continuous_families: families,
            exact_weights: Vec::new(),
        }
    }

    pub fn add_weight(&mut self, w: Ratio<i64>) -> Result<(), CensusError> {
        if w < Ratio::zero() {
            return Err(CensusError::PopulationNegative);
        }
        self.exact_weights.push(w);
        Ok(())
    }

    /// Verifies that the normalized weights sum to exactly 1 over Q.
    pub fn verify_weight_normalization(&self) -> Result<bool, CensusError> {
        if self.exact_weights.is_empty() {
            return Ok(true);
        }
        let sum: Ratio<i64> = self.exact_weights.iter().copied().sum();
        Ok(sum == Ratio::one())
    }

    pub fn total_candidates(&self) -> usize {
        self.isolated_count + self.continuous_families
    }
}

#[cfg(test)]
mod census_tests {
    use super::*;

    #[test]
    fn test_census_auditor() {
        let mut auditor = CensusAuditor::new("Fourier-B3", 5, 1);
        assert_eq!(auditor.total_candidates(), 6);
        auditor.add_weight(Ratio::new(1, 2)).unwrap();
        auditor.add_weight(Ratio::new(1, 2)).unwrap();
        assert!(auditor.verify_weight_normalization().unwrap());
    }
}
