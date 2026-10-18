
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Copy, PartialEq, PartialOrd, Serialize, Deserialize)]
pub struct L1Weight(pub f64);

#[derive(Debug, Clone, Copy, PartialEq, PartialOrd, Serialize, Deserialize)]
pub struct HilbertLift(pub f64);

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct WeightedL1Norm {
    weights: Vec<L1Weight>,
}

#[derive(Debug, thiserror::Error)]
pub enum WeightedL1NormError {
    #[error("empty weight vector")]
    Empty,
    #[error("non-finite weight at index {index}: {value}")]
    NonFinite { index: usize, value: f64 },
    #[error("non-positive weight at index {index}: {value}")]
    NonPositive { index: usize, value: f64 },
    #[error("dimension mismatch: norm has {expected} weights but vector has {actual} entries")]
    DimensionMismatch { expected: usize, actual: usize },
}

impl WeightedL1Norm {
    pub fn new(weights: Vec<f64>) -> Result<Self, WeightedL1NormError> {
        if weights.is_empty() {
            return Err(WeightedL1NormError::Empty);
        }
        let mut l1_weights = Vec::with_capacity(weights.len());
        for (index, &value) in weights.iter().enumerate() {
            if !value.is_finite() {
                return Err(WeightedL1NormError::NonFinite { index, value });
            }
            if value <= 0.0 {
                return Err(WeightedL1NormError::NonPositive { index, value });
            }
            l1_weights.push(L1Weight(value));
        }
        Ok(Self {
            weights: l1_weights,
        })
    }

    pub fn uniform(dim: usize) -> Result<Self, WeightedL1NormError> {
        if dim == 0 {
            return Err(WeightedL1NormError::Empty);
        }
        Ok(Self {
            weights: vec![L1Weight(1.0); dim],
        })
    }

    pub fn evaluate(&self, x: &[f64]) -> Result<f64, WeightedL1NormError> {
        if x.len() != self.weights.len() {
            return Err(WeightedL1NormError::DimensionMismatch {
                expected: self.weights.len(),
                actual: x.len(),
            });
        }
        Ok(self
            .weights
            .iter()
            .zip(x.iter())
            .map(|(w, xi)| w.0 * xi.abs())
            .sum())
    }

    pub fn dim(&self) -> usize {
        self.weights.len()
    }

    pub fn weights(&self) -> &[L1Weight] {
        &self.weights
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn uniform_norm_evaluates_correctly() {
        let norm = WeightedL1Norm::uniform(3).unwrap();
        let x = vec![1.0, -2.0, 3.0];
        assert!((norm.evaluate(&x).unwrap() - 6.0).abs() < 1e-12);
    }

    #[test]
    fn weighted_norm_evaluates_correctly() {
        let norm = WeightedL1Norm::new(vec![2.0, 0.5]).unwrap();
        let x = vec![1.0, -4.0];
        assert!((norm.evaluate(&x).unwrap() - 4.0).abs() < 1e-12);
    }

    #[test]
    fn rejects_non_positive_weight() {
        assert!(WeightedL1Norm::new(vec![1.0, 0.0, 2.0]).is_err());
        assert!(WeightedL1Norm::new(vec![1.0, -1.0]).is_err());
    }

    #[test]
    fn rejects_non_finite_weight() {
        assert!(WeightedL1Norm::new(vec![1.0, f64::NAN]).is_err());
        assert!(WeightedL1Norm::new(vec![f64::INFINITY]).is_err());
    }

    #[test]
    fn rejects_dimension_mismatch() {
        let norm = WeightedL1Norm::uniform(2).unwrap();
        assert!(norm.evaluate(&[1.0, 2.0, 3.0]).is_err());
    }
}
