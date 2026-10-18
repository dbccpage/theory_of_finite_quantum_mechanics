
use crate::boundary::BoundaryMap;
use crate::errors::HomologicalError;
use crate::hashing::{hash_chain_complex_manifest, Hash256};
use crate::ids::Degree;
use crate::linear_algebra::scalars::Q;
use crate::witness::ChainComplexWitness;
use crate::linear_algebra::basic_matrix::BasicMatrix;
use num_traits::Zero;

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ChainComplex {
    pub c0_dim: usize,
    pub c1_dim: usize,
    pub c2_dim: usize,
    pub boundary_1: BoundaryMap,
    pub boundary_2: BoundaryMap,
    pub witness: ChainComplexWitness,
    pub boundaries: Vec<BasicMatrix<Q>>,
}

impl ChainComplex {
    pub fn new(
        c0_dim: usize,
        c1_dim: usize,
        c2_dim: usize,
        d1_matrix: BasicMatrix<Q>,
        d2_matrix: BasicMatrix<Q>,
    ) -> Result<Self, HomologicalError> {
        if d1_matrix.rows() != c0_dim || d1_matrix.cols() != c1_dim {
            return Err(HomologicalError::DimensionMismatch {
                expected: c0_dim * c1_dim,
                got: d1_matrix.rows() * d1_matrix.cols(),
            });
        }

        if d2_matrix.rows() != c1_dim || d2_matrix.cols() != c2_dim {
            return Err(HomologicalError::DimensionMismatch {
                expected: c1_dim * c2_dim,
                got: d2_matrix.rows() * d2_matrix.cols(),
            });
        }

        if c0_dim > 0 && c2_dim > 0 {
            let product = d1_matrix
                .mul(&d2_matrix)
                .map_err(HomologicalError::MatrixError)?;
            if !product.as_slice().iter().all(|x| x.is_zero()) {
                return Err(HomologicalError::BoundaryLawViolation { degree: 1 });
            }
        }

        let boundaries = vec![d1_matrix.clone(), d2_matrix.clone()];
        let boundary_1 = BoundaryMap::new(Degree::new(1), Degree::new(0), d1_matrix);
        let boundary_2 = BoundaryMap::new(Degree::new(2), Degree::new(1), d2_matrix);

        let complex_hash = hash_chain_complex_manifest(
            c0_dim,
            c1_dim,
            c2_dim,
            &boundary_1.map_hash,
            &boundary_2.map_hash,
        );

        let witness = ChainComplexWitness::new(
            complex_hash.clone(),
            boundary_1.map_hash.clone(),
            boundary_2.map_hash.clone(),
            c0_dim,
            c1_dim,
            c2_dim,
        );

        Ok(Self {
            c0_dim,
            c1_dim,
            c2_dim,
            boundary_1,
            boundary_2,
            witness,
            boundaries,
        })
    }

    pub fn complex_hash(&self) -> &Hash256 {
        &self.witness.complex_hash
    }

    pub fn dim(&self, degree: usize) -> Result<usize, HomologicalError> {
        match degree {
            0 => Ok(self.c0_dim),
            1 => Ok(self.c1_dim),
            2 => Ok(self.c2_dim),
            _ => Err(HomologicalError::InvalidDegree(degree as i32)),
        }
    }
}

impl crate::chain_map::FiniteChainComplexView<Q> for ChainComplex {
    fn boundaries(&self) -> &[BasicMatrix<Q>] {
        &self.boundaries
    }
    fn complex_hash_bytes(&self) -> [u8; 32] {
        self.complex_hash().0
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn r(n: i64) -> Q {
        crate::linear_algebra::scalars::q(n)
    }

    fn zero_matrix(rows: usize, cols: usize) -> BasicMatrix<Q> {
        BasicMatrix::from_row_major(rows, cols, vec![r(0); rows * cols])
            .expect("zero matrix creation should succeed")
    }

    #[test]
    fn test_trivial_chain_complex() {
        let d1 = zero_matrix(1, 0);
        let d2 = zero_matrix(0, 0);

        let complex = ChainComplex::new(1, 0, 0, d1, d2);
        assert!(complex.is_ok());
    }

    #[test]
    fn test_boundary_law_verified() {

        let d1 = BasicMatrix::from_row_major(1, 2, vec![r(1), r(1)]).expect("d1 creation");
        let d2 = BasicMatrix::from_row_major(2, 1, vec![r(1), r(-1)]).expect("d2 creation");

        let complex = ChainComplex::new(1, 2, 1, d1, d2);
        assert!(complex.is_ok());
    }

    #[test]
    fn test_boundary_law_violation_rejected() {

        let d1 = BasicMatrix::from_row_major(1, 2, vec![r(1), r(1)]).expect("d1 creation");
        let d2 = BasicMatrix::from_row_major(2, 1, vec![r(1), r(1)]).expect("d2 creation");

        let complex = ChainComplex::new(1, 2, 1, d1, d2);
        assert!(matches!(
            complex,
            Err(HomologicalError::BoundaryLawViolation { degree: 1 })
        ));
    }

    #[test]
    fn test_dimension_mismatch_d1() {
        let d1 = BasicMatrix::from_row_major(2, 2, vec![r(0); 4]).expect("d1 creation");
        let d2 = zero_matrix(2, 1);

        let complex = ChainComplex::new(1, 2, 1, d1, d2);
        assert!(matches!(
            complex,
            Err(HomologicalError::DimensionMismatch { .. })
        ));
    }

    #[test]
    fn test_dimension_mismatch_d2() {
        let d1 = zero_matrix(1, 2);
        let d2 = BasicMatrix::from_row_major(3, 1, vec![r(0); 3]).expect("d2 creation");

        let complex = ChainComplex::new(1, 2, 1, d1, d2);
        assert!(matches!(
            complex,
            Err(HomologicalError::DimensionMismatch { .. })
        ));
    }

    #[test]
    fn dim_rejects_degree_outside_finite_support() {
        let d1 = zero_matrix(1, 0);
        let d2 = zero_matrix(0, 0);
        let complex = ChainComplex::new(1, 0, 0, d1, d2).expect("trivial complex");
        assert_eq!(complex.dim(0).expect("degree 0 in support"), 1);
        assert_eq!(complex.dim(1).expect("degree 1 in support"), 0);
        assert_eq!(complex.dim(2).expect("degree 2 in support"), 0);
        assert!(matches!(
            complex.dim(3),
            Err(HomologicalError::InvalidDegree(3))
        ));
    }
}
