
use crate::chain::Chain;
use crate::errors::HomologicalError;
use crate::hashing::{hash_matrix, Hash256};
use crate::ids::Degree;
use crate::linear_algebra::scalars::Q;
use crate::linear_algebra::basic_matrix::BasicMatrix;

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct BoundaryMap {
    pub from_degree: Degree,
    pub to_degree: Degree,
    pub matrix: BasicMatrix<Q>,
    pub map_hash: Hash256,
}

impl BoundaryMap {
    pub fn new(from_degree: Degree, to_degree: Degree, matrix: BasicMatrix<Q>) -> Self {
        let map_hash = hash_matrix(&matrix);
        Self {
            from_degree,
            to_degree,
            matrix,
            map_hash,
        }
    }

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

    pub fn source_dim(&self) -> usize {
        self.matrix.cols()
    }

    pub fn target_dim(&self) -> usize {
        self.matrix.rows()
    }

    pub fn hash(&self) -> Hash256 {
        hash_matrix(&self.matrix)
    }
}
