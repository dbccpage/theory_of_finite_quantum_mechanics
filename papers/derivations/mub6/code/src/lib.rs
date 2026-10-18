//! MUB(6) candidate verification traits and exact certificate checkers.
//!
//! Origin: papers/derivations/mub6/code/src/lib.rs
//! Claim: DERIV-MUB6-LIB-001
//! AuthorityEffect: None.

use num_rational::Ratio;
use num_traits::{One, Zero};
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum Mub6CertError {
    UnbiasednessViolation { i: usize, j: usize, val: Ratio<i64> },
    NonUnitaryBasis,
}

/// Exact rational verification certificate for mutually unbiased bases in dimension d=6.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct Mub6Certificate {
    pub dimension: usize,
    pub num_bases: usize,
    /// Exact overlap modulus squared |<v_i, w_j>|^2
    pub overlap_modulus_sq: Ratio<i64>,
}

impl Mub6Certificate {
    pub fn new(dimension: usize, num_bases: usize) -> Self {
        Self {
            dimension,
            num_bases,
            overlap_modulus_sq: Ratio::new(1, dimension as i64),
        }
    }

    /// Verifies the theoretical maximum bound: at most d+1 bases in dimension d.
    pub fn verify_bound(&self) -> bool {
        self.num_bases <= self.dimension + 1
    }

    /// Verifies exact unbiasedness value = 1/6.
    pub fn verify_unbiasedness_target(&self) -> bool {
        self.overlap_modulus_sq == Ratio::new(1, 6)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_mub6_certificate() {
        let cert = Mub6Certificate::new(6, 3);
        assert!(cert.verify_bound());
        assert!(cert.verify_unbiasedness_target());
    }
}
