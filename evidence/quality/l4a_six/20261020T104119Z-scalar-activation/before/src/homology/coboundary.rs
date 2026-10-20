//! Coboundary maps in a cochain complex: d^n : C^n -> C^{n+1}.

use crate::homology::cochain::Cochain;
use crate::homology::errors::HomologicalError;
use crate::homology::hashing::{hash_matrix, Hash256};
use crate::homology::ids::Degree;
use crate::linear_algebra::basic_matrix::BasicMatrix;
use crate::linear_algebra::scalars::Q;

/// A coboundary map d^n : C^n -> C^{n+1}.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct CoboundaryMap {
    /// Source degree n.
    pub(super) from_degree: Degree,
    /// Target degree n+1.
    pub(super) to_degree: Degree,
    /// The matrix representation (rows = dim C^{n+1}, cols = dim C^n).
    pub(super) matrix: BasicMatrix<Q>,
    /// Hash of the matrix for manifest binding.
    pub(super) map_hash: Hash256,
}

impl CoboundaryMap {
    /// Create a new coboundary map, computing its hash.
    pub fn new(
        from_degree: Degree,
        to_degree: Degree,
        matrix: BasicMatrix<Q>,
    ) -> Result<Self, HomologicalError> {
        super::exact_scalar::admit_matrix(&matrix)?;
        let expected = from_degree
            .checked_succ()
            .map_err(|_| HomologicalError::DegreeOverflow)?;
        if to_degree != expected {
            return Err(HomologicalError::DegreeMismatch {
                expected: expected.value(),
                got: to_degree.value(),
            });
        }
        let map_hash = hash_matrix(&matrix)?;
        Ok(Self {
            from_degree,
            to_degree,
            matrix,
            map_hash,
        })
    }

    /// Apply the coboundary map to a cochain: d^n(alpha).
    pub fn apply(&self, cochain: &Cochain) -> Result<Cochain, HomologicalError> {
        if cochain.degree != self.from_degree {
            return Err(HomologicalError::DegreeMismatch {
                expected: self.from_degree.value(),
                got: cochain.degree.value(),
            });
        }
        if cochain.coefficients.len() != self.matrix.cols() {
            return Err(HomologicalError::DimensionMismatch {
                expected: self.matrix.cols(),
                got: cochain.coefficients.len(),
            });
        }
        let result = self
            .matrix
            .mul_vec(&cochain.coefficients)
            .map_err(HomologicalError::MatrixError)?;
        Cochain::new(self.to_degree, cochain.basis_id.clone(), result)
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

    /// Return the hash bound at admission. Immutable storage preserves it.
    pub fn hash(&self) -> Hash256 {
        self.map_hash.clone()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::homology::ids::BasisId;
    use crate::linear_algebra::scalars::q;

    #[test]
    fn apply_rejects_coefficient_length_mismatch() {
        let matrix = BasicMatrix::<Q>::zero(2, 3).expect("2x3 zero matrix");
        let map = CoboundaryMap::new(Degree::new(0), Degree::new(1), matrix).expect("valid map");
        let cochain = Cochain::new(
            Degree::new(0),
            BasisId::new("test").expect("valid basis"),
            vec![q(1)],
        )
        .expect("valid fixture");
        assert!(matches!(
            map.apply(&cochain),
            Err(HomologicalError::DimensionMismatch {
                expected: 3,
                got: 1
            })
        ));
    }
}
