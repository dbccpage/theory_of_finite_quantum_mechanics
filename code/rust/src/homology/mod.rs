
use crate::linear_algebra::{ExactMatrix, MatrixError, Q};
use crate::linear_algebra::scalars::{hash_rational, q};
use serde::{Deserialize, Serialize};
use thiserror::Error;

#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub struct Hash256(pub [u8; 32]);

impl Hash256 {
    pub fn to_hex(&self) -> String {
        hex::encode(self.0)
    }
}

pub fn hash_exact_matrix(m: &ExactMatrix<Q>) -> Hash256 {
    let mut hasher = blake3::Hasher::new();
    hasher.update(b"TheoryOfFiniteQM.ExactMatrix<Q>.v1");
    hasher.update(&(m.rows() as u64).to_le_bytes());
    hasher.update(&(m.cols() as u64).to_le_bytes());
    for val in m.as_slice() {
        hash_rational(&mut hasher, val);
    }
    Hash256(*hasher.finalize().as_bytes())
}

#[derive(Debug, Clone, PartialEq, Eq, Error)]
pub enum HomologicalError {
    #[error("Dimension mismatch: expected {expected}, got {got}")]
    DimensionMismatch { expected: usize, got: usize },
    #[error("Coboundary law violated: d1 * d0 != 0")]
    CoboundaryLawViolation,
    #[error("Weight dimension mismatch: expected {expected}, got {got}")]
    WeightDimensionMismatch { expected: usize, got: usize },
    #[error("Non-positive weight at index {index}")]
    NonPositiveWeight { index: usize },
    #[error("Homology dimension underflow: ker_dim={ker_dim}, im_dim={im_dim}")]
    HomologyDimensionUnderflow { ker_dim: usize, im_dim: usize },
    #[error("Matrix error: {0}")]
    Matrix(#[from] MatrixError),
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct Carrier {
    pub c0_dim: usize,
    pub c1_dim: usize,
    pub c2_dim: usize,
    pub d0: ExactMatrix<Q>,
    pub d1: ExactMatrix<Q>,
    pub weights: Vec<Q>,
    pub d0_hash: Hash256,
    pub d1_hash: Hash256,
}

impl Carrier {
    pub fn new(
        c0_dim: usize,
        c1_dim: usize,
        c2_dim: usize,
        d0: ExactMatrix<Q>,
        d1: ExactMatrix<Q>,
        weights: Vec<Q>,
    ) -> Result<Self, HomologicalError> {
        if d0.rows() != c1_dim || d0.cols() != c0_dim {
            return Err(HomologicalError::DimensionMismatch {
                expected: c1_dim * c0_dim,
                got: d0.rows() * d0.cols(),
            });
        }
        if d1.rows() != c2_dim || d1.cols() != c1_dim {
            return Err(HomologicalError::DimensionMismatch {
                expected: c2_dim * c1_dim,
                got: d1.rows() * d1.cols(),
            });
        }
        if weights.len() != c1_dim {
            return Err(HomologicalError::WeightDimensionMismatch {
                expected: c1_dim,
                got: weights.len(),
            });
        }
        for (i, w) in weights.iter().enumerate() {
            if *w <= q(0) {
                return Err(HomologicalError::NonPositiveWeight { index: i });
            }
        }

        let comp = d1.mul(&d0)?;
        let zero = ExactMatrix::zeros(c2_dim, c0_dim);
        if comp != zero {
            return Err(HomologicalError::CoboundaryLawViolation);
        }

        let d0_hash = hash_exact_matrix(&d0);
        let d1_hash = hash_exact_matrix(&d1);

        Ok(Self {
            c0_dim,
            c1_dim,
            c2_dim,
            d0,
            d1,
            weights,
            d0_hash,
            d1_hash,
        })
    }

    pub fn rank_d0(&self) -> usize {
        self.d0.rank()
    }

    pub fn rank_d1(&self) -> usize {
        self.d1.rank()
    }

    pub fn dim_q1(&self) -> usize {
        self.c1_dim - self.rank_d0()
    }

    pub fn dim_h1(&self) -> Result<usize, HomologicalError> {
        let ker_d1 = self.c1_dim - self.rank_d1();
        let im_d0 = self.rank_d0();
        ker_d1
            .checked_sub(im_d0)
            .ok_or(HomologicalError::HomologyDimensionUnderflow {
                ker_dim: ker_d1,
                im_dim: im_d0,
            })
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_triangle_carrier_homology() {
        let d0_rows = vec![
            vec![q(-1), q(1), q(0)],
            vec![q(0), q(-1), q(1)],
            vec![q(1), q(0), q(-1)],
        ];
        let d0 = ExactMatrix::from_rows(d0_rows).unwrap();
        let d1_rows = vec![vec![q(1), q(1), q(1)]];
        let d1 = ExactMatrix::from_rows(d1_rows).unwrap();
        let weights = vec![q(1), q(1), q(1)];

        let carrier = Carrier::new(3, 3, 1, d0, d1, weights).unwrap();
        assert_eq!(carrier.rank_d0(), 2);
        assert_eq!(carrier.rank_d1(), 1);
        assert_eq!(carrier.dim_q1(), 1);
        assert_eq!(carrier.dim_h1().unwrap(), 0);
    }
}