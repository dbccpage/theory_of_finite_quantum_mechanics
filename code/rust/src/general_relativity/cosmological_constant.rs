
use num_rational::Ratio;
use num_traits::{One, Zero};
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum CosmologicalError {
    NegativeVolume,
    ZeroCoupling,
    InvalidDeficitAngle,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct CosmologicalCoupling {
    pub dimension: usize,
    pub lambda: Ratio<i64>,
    pub kappa: Ratio<i64>,
}

impl CosmologicalCoupling {
    pub fn new(dimension: usize, lambda: Ratio<i64>, kappa: Ratio<i64>) -> Result<Self, CosmologicalError> {
        if kappa.is_zero() {
            return Err(CosmologicalError::ZeroCoupling);
        }
        Ok(Self { dimension, lambda, kappa })
    }

    pub fn evaluate_action(
        &self,
        total_hinge_curvature: Ratio<i64>,
        total_volume: Ratio<i64>,
    ) -> Result<Ratio<i64>, CosmologicalError> {
        if total_volume < Ratio::zero() {
            return Err(CosmologicalError::NegativeVolume);
        }
        let curvature_term = total_hinge_curvature / (Ratio::from_integer(2) * self.kappa);
        let volume_term = self.lambda * total_volume;
        Ok(curvature_term - volume_term)
    }

    pub fn effective_scalar_curvature(&self) -> Ratio<i64> {
        Ratio::from_integer(2) * self.lambda * self.kappa
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_cosmological_action() {
        let cc = CosmologicalCoupling::new(4, Ratio::new(1, 10), Ratio::new(1, 2)).unwrap();
        assert_eq!(cc.effective_scalar_curvature(), Ratio::new(1, 10));

        let s = cc.evaluate_action(Ratio::from_integer(10), Ratio::from_integer(20)).unwrap();
        assert_eq!(s, Ratio::from_integer(8));
    }
}
