
use crate::cochain::Cochain;
use crate::errors::HomologicalError;
use crate::hashing::{hash_matrix, Hash256};
use crate::ids::Degree;
use crate::linear_algebra::scalars::Q;
use crate::linear_algebra::basic_matrix::BasicMatrix;

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct CoboundaryMap {
    pub from_degree: Degree,
    pub to_degree: Degree,
    pub matrix: BasicMatrix<Q>,
    pub map_hash: Hash256,
}

impl CoboundaryMap {
    pub fn new(from_degree: Degree, to_degree: Degree, matrix: BasicMatrix<Q>) -> Self {
        let map_hash = hash_matrix(&matrix);
        Self {
            from_degree,
            to_degree,
            matrix,
            map_hash,
        }
    }

    pub fn apply(&self, cochain: &Cochain) -> Result<Cochain, HomologicalError> {
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
        Ok(Cochain::new(
            self.to_degree,
            cochain.basis_id.clone(),
            result,
        ))
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

#[cfg(test)]
mod tests {
    use super::*;
    use crate::ids::BasisId;
    use crate::linear_algebra::scalars::q;

    #[test]
    fn apply_rejects_coefficient_length_mismatch() {
        let matrix = BasicMatrix::<Q>::zero(2, 3).expect("2x3 zero matrix");
        let map = CoboundaryMap::new(Degree::new(0), Degree::new(1), matrix);
        let cochain = Cochain::new(Degree::new(0), BasisId::new("test"), vec![q(1)]);
        assert!(matches!(
            map.apply(&cochain),
            Err(HomologicalError::DimensionMismatch {
                expected: 3,
                got: 1
            })
        ));
    }
}
