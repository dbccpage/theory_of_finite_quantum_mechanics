//! Cochain: a linear functional / coordinate vector on chains in degree n.

use crate::errors::HomologicalError;
use crate::hashing::{hash_vector, Hash256};
use crate::ids::{BasisId, Degree};
use crate::crate::crate::linear_algebra::scalars::Q;
use num_traits::Zero;
use serde::{Deserialize, Serialize};

/// A cochain element: a vector of coefficients in a given degree.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct Cochain {
    pub degree: Degree,
    pub basis_id: BasisId,
    pub coefficients: Vec<Q>,
}

impl Cochain {
    /// Create a new cochain with the given coefficients.
    pub fn new(degree: Degree, basis_id: BasisId, coefficients: Vec<Q>) -> Self {
        Self {
            degree,
            basis_id,
            coefficients,
        }
    }

    /// Create a zero cochain of given dimension.
    pub fn zero(degree: Degree, basis_id: BasisId, dim: usize) -> Self {
        Self {
            degree,
            basis_id,
            coefficients: vec![Q::zero(); dim],
        }
    }

    /// Dimension of the cochain (number of coefficients).
    pub fn dimension(&self) -> usize {
        self.coefficients.len()
    }

    /// Check if all coefficients are zero.
    pub fn is_zero(&self) -> bool {
        self.coefficients.iter().all(|c| c.is_zero())
    }

    /// Compute a deterministic hash of this cochain.
    pub fn hash(&self) -> Hash256 {
        hash_vector(&self.coefficients)
    }

    /// Add two cochains of the same degree and basis.
    pub fn add(&self, other: &Cochain) -> Result<Cochain, HomologicalError> {
        if self.degree != other.degree {
            return Err(HomologicalError::DimensionMismatch {
                expected: self.degree.0 as usize,
                got: other.degree.0 as usize,
            });
        }
        if self.coefficients.len() != other.coefficients.len() {
            return Err(HomologicalError::DimensionMismatch {
                expected: self.coefficients.len(),
                got: other.coefficients.len(),
            });
        }
        let coefficients = self
            .coefficients
            .iter()
            .zip(other.coefficients.iter())
            .map(|(a, b)| a + b)
            .collect();
        Ok(Cochain {
            degree: self.degree,
            basis_id: self.basis_id.clone(),
            coefficients,
        })
    }

    /// Subtract another cochain.
    pub fn sub(&self, other: &Cochain) -> Result<Cochain, HomologicalError> {
        if self.degree != other.degree {
            return Err(HomologicalError::DimensionMismatch {
                expected: self.degree.0 as usize,
                got: other.degree.0 as usize,
            });
        }
        if self.coefficients.len() != other.coefficients.len() {
            return Err(HomologicalError::DimensionMismatch {
                expected: self.coefficients.len(),
                got: other.coefficients.len(),
            });
        }
        let coefficients = self
            .coefficients
            .iter()
            .zip(other.coefficients.iter())
            .map(|(a, b)| a - b)
            .collect();
        Ok(Cochain {
            degree: self.degree,
            basis_id: self.basis_id.clone(),
            coefficients,
        })
    }

    /// Scalar multiplication.
    pub fn scalar_mul(&self, scalar: &Q) -> Cochain {
        let coefficients = self.coefficients.iter().map(|c| c * scalar).collect();
        Cochain {
            degree: self.degree,
            basis_id: self.basis_id.clone(),
            coefficients,
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use num_rational::Rational64;

    fn r(n: i64, d: i64) -> Q {
        crate::crate::crate::linear_algebra::scalars::qr(n, d)
    }

    fn test_basis_id() -> BasisId {
        BasisId("test_basis".to_string())
    }

    #[test]
    fn test_cochain_new() {
        let coeffs = vec![r(1, 1), r(2, 1), r(3, 1)];
        let cochain = Cochain::new(Degree(0), test_basis_id(), coeffs.clone());
        assert_eq!(cochain.degree, Degree(0));
        assert_eq!(cochain.coefficients, coeffs);
        assert_eq!(cochain.dimension(), 3);
    }

    #[test]
    fn test_cochain_zero() {
        let cochain = Cochain::zero(Degree(1), test_basis_id(), 5);
        assert_eq!(cochain.dimension(), 5);
        assert!(cochain.is_zero());
    }

    #[test]
    fn test_cochain_is_zero() {
        let zero_cochain = Cochain::zero(Degree(0), test_basis_id(), 3);
        assert!(zero_cochain.is_zero());

        let non_zero = Cochain::new(Degree(0), test_basis_id(), vec![r(0, 1), r(1, 1), r(0, 1)]);
        assert!(!non_zero.is_zero());
    }

    #[test]
    fn test_cochain_add() {
        let a = Cochain::new(Degree(0), test_basis_id(), vec![r(1, 1), r(2, 1)]);
        let b = Cochain::new(Degree(0), test_basis_id(), vec![r(3, 1), r(4, 1)]);
        let sum = a.add(&b).unwrap();
        assert_eq!(sum.coefficients, vec![r(4, 1), r(6, 1)]);
    }

    #[test]
    fn test_cochain_add_degree_mismatch() {
        let a = Cochain::new(Degree(0), test_basis_id(), vec![r(1, 1)]);
        let b = Cochain::new(Degree(1), test_basis_id(), vec![r(1, 1)]);
        let result = a.add(&b);
        assert!(matches!(
            result,
            Err(HomologicalError::DimensionMismatch { .. })
        ));
    }

    #[test]
    fn test_cochain_add_dimension_mismatch() {
        let a = Cochain::new(Degree(0), test_basis_id(), vec![r(1, 1), r(2, 1)]);
        let b = Cochain::new(Degree(0), test_basis_id(), vec![r(1, 1)]);
        let result = a.add(&b);
        assert!(matches!(
            result,
            Err(HomologicalError::DimensionMismatch { .. })
        ));
    }

    #[test]
    fn test_cochain_sub() {
        let a = Cochain::new(Degree(0), test_basis_id(), vec![r(5, 1), r(7, 1)]);
        let b = Cochain::new(Degree(0), test_basis_id(), vec![r(2, 1), r(3, 1)]);
        let diff = a.sub(&b).unwrap();
        assert_eq!(diff.coefficients, vec![r(3, 1), r(4, 1)]);
    }

    #[test]
    fn test_cochain_sub_self_is_zero() {
        let a = Cochain::new(Degree(0), test_basis_id(), vec![r(1, 1), r(2, 1), r(3, 1)]);
        let diff = a.sub(&a).unwrap();
        assert!(diff.is_zero());
    }

    #[test]
    fn test_cochain_scalar_mul() {
        let a = Cochain::new(Degree(0), test_basis_id(), vec![r(1, 1), r(2, 1), r(3, 1)]);
        let scaled = a.scalar_mul(&r(2, 1));
        assert_eq!(scaled.coefficients, vec![r(2, 1), r(4, 1), r(6, 1)]);
    }

    #[test]
    fn test_cochain_scalar_mul_by_zero() {
        let a = Cochain::new(Degree(0), test_basis_id(), vec![r(1, 1), r(2, 1), r(3, 1)]);
        let scaled = a.scalar_mul(&r(0, 1));
        assert!(scaled.is_zero());
    }

    #[test]
    fn test_cochain_scalar_mul_by_fraction() {
        let a = Cochain::new(Degree(0), test_basis_id(), vec![r(2, 1), r(4, 1)]);
        let scaled = a.scalar_mul(&r(1, 2));
        assert_eq!(scaled.coefficients, vec![r(1, 1), r(2, 1)]);
    }

    #[test]
    fn test_cochain_hash_deterministic() {
        let a = Cochain::new(Degree(0), test_basis_id(), vec![r(1, 1), r(2, 1), r(3, 1)]);
        let hash1 = a.hash();
        let hash2 = a.hash();
        assert_eq!(hash1, hash2);
    }

    #[test]
    fn test_cochain_hash_different_for_different_cochains() {
        let a = Cochain::new(Degree(0), test_basis_id(), vec![r(1, 1), r(2, 1)]);
        let b = Cochain::new(Degree(0), test_basis_id(), vec![r(1, 1), r(3, 1)]);
        assert_ne!(a.hash(), b.hash());
    }
}
