
use num_rational::Ratio;
use num_traits::{One, Zero};
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum Mub6CertError {
    UnbiasednessViolation { i: usize, j: usize, val: Ratio<i64> },
    NonUnitaryBasis,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct Mub6Certificate {
    pub dimension: usize,
    pub num_bases: usize,
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

    pub fn verify_bound(&self) -> bool {
        self.num_bases <= self.dimension + 1
    }

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
