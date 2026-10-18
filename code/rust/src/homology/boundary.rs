//! Boundary maps in a chain complex: d_n : C_n -> C_{n-1}.

use crate::chain::Chain;
use crate::errors::HomologicalError;
use crate::hashing::{hash_matrix, Hash256};
use crate::ids::Degree;
use crate::linear_algebra::scalars::Q;
use crate::linear_algebra::basic_matrix::BasicMatrix;

/// A boundary map d_n : C_n -> C_{n-1}.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct BoundaryMap {
    /// Source degree n.
    pub from_degree: Degree,
    /// Target degree n-1.
    pub to_degree: Degree,
    /// The matrix representation (rows = dim C_{n-1}, cols = dim C_n).
    pub matrix: BasicMatrix<Q>,
    /// Hash of the matrix for manifest binding.
    pub map_hash: Hash256,
}

impl BoundaryMap {
    /// Create a new boundary map, computing its hash.
    pub fn new(from_degree: Degree, to_degree: Degree, matrix: BasicMatrix<Q>) -> Self {
        let map_hash = hash_matrix(&matrix);
        Self {
            from_degree,
            to_degree,
            matrix,
            map_hash,
        }
    }

    /// Apply the boundary map to a chain: d_n(c).
    pub fn apply(&self, chain: &Chain) -> Result<Chain, HomologicalError> {
        if chain.coefficients.len() != self.matrix.cols() {
            return Err(HomologicalError::DimensionMismatch {
                expected: self.matrix.cols(),
                got: chain.coefficients.len(),
            });
        }
        let result = self
            .matrix
            .mul_vec(&chain.coefficients)
            .map_err(HomologicalError::MatrixError)?;
        Ok(Chain::new(self.to_degree, chain.basis_id.clone(), result))
    }

    /// Source dimension (number of columns).
    pub fn source_dim(&self) -> usize {
        self.matrix.cols()
    }

    /// Target dimension (number of rows).
    pub fn target_dim(&self) -> usize {
        self.matrix.rows()
    }

    /// Recompute and return the hash.
    pub fn hash(&self) -> Hash256 {
        hash_matrix(&self.matrix)
    }
}
