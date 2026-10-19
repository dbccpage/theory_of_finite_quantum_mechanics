//! Boundary maps in a chain complex: d_n : C_n -> C_{n-1}.
//! AuthorityEffect: None. These are canonical coordinate matrices with a
//! checked degree drop, not independent certificates of a whole complex law.
//! Basis-family labels are supplied by the caller and preserved on application;
//! the map itself does not bind a family identifier.

use crate::homology::chain::Chain;
use crate::homology::errors::HomologicalError;
use crate::homology::hashing::{hash_matrix, Hash256};
use crate::homology::ids::Degree;
use crate::linear_algebra::basic_matrix::BasicMatrix;
use crate::linear_algebra::scalars::Q;

/// A boundary map d_n : C_n -> C_{n-1}.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct BoundaryMap {
    /// Source degree n.
    pub(super) from_degree: Degree,
    /// Target degree n-1.
    pub(super) to_degree: Degree,
    /// The matrix representation (rows = dim C_{n-1}, cols = dim C_n).
    pub(super) matrix: BasicMatrix<Q>,
    /// Hash of the matrix for manifest binding.
    pub(super) map_hash: Hash256,
}

impl BoundaryMap {
    /// Create a new boundary map, computing its hash.
    pub fn new(
        from_degree: Degree,
        to_degree: Degree,
        matrix: BasicMatrix<Q>,
    ) -> Result<Self, HomologicalError> {
        super::exact_scalar::admit_matrix(&matrix)?;
        let expected = from_degree
            .checked_pred()
            .map_err(|_| HomologicalError::DegreeOverflow)?;
        if to_degree != expected {
            return Err(HomologicalError::DegreeMismatch {
                expected: expected.value(),
                got: to_degree.value(),
            });
        }
        let map_hash = hash_matrix(&matrix);
        Ok(Self {
            from_degree,
            to_degree,
            matrix,
            map_hash,
        })
    }

    /// Apply the boundary map to a chain: d_n(c).
    pub fn apply(&self, chain: &Chain) -> Result<Chain, HomologicalError> {
        if chain.degree != self.from_degree {
            return Err(HomologicalError::DegreeMismatch {
                expected: self.from_degree.value(),
                got: chain.degree.value(),
            });
        }
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
        Ok(Chain::from_canonical(
            self.to_degree,
            chain.basis_id.clone(),
            result,
        ))
    }

    pub fn from_degree(&self) -> Degree {
        self.from_degree
    }
    pub fn to_degree(&self) -> Degree {
        self.to_degree
    }
    pub fn matrix(&self) -> &BasicMatrix<Q> {
        &self.matrix
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
