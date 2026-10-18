
use crate::coboundary::CoboundaryMap;
use crate::errors::HomologicalError;
use crate::hashing::{
    hash_cochain_complex_manifest, hash_cochain_witness, hash_provenance, Hash256,
};
use crate::ids::Degree;
use crate::linear_algebra::scalars::Q;
use crate::witness::CochainComplexWitness;
use crate::linear_algebra::basic_matrix::BasicMatrix;
use num_traits::Zero;
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct TheoremProvenance {
    verification_source: String,
}

impl TheoremProvenance {
    pub fn new(verification_source: String) -> Result<Self, HomologicalError> {
        if verification_source.trim().is_empty() {
            return Err(HomologicalError::EmptyVerificationSource);
        }
        Ok(Self {
            verification_source,
        })
    }

    pub fn verification_source(&self) -> &str {
        &self.verification_source
    }

    pub fn provenance_hash(&self) -> Hash256 {
        hash_provenance(&self.verification_source)
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct CochainComplex {
    pub c0_dim: usize,
    pub c1_dim: usize,
    pub c2_dim: usize,
    pub d0: CoboundaryMap,
    pub d1: CoboundaryMap,
    pub witness: CochainComplexWitness,
}

impl CochainComplex {
    pub fn new(
        c0_dim: usize,
        c1_dim: usize,
        c2_dim: usize,
        d0_matrix: BasicMatrix<Q>,
        d1_matrix: BasicMatrix<Q>,
        provenance: TheoremProvenance,
    ) -> Result<Self, HomologicalError> {
        if d0_matrix.rows() != c1_dim || d0_matrix.cols() != c0_dim {
            return Err(HomologicalError::DimensionMismatch {
                expected: c1_dim * c0_dim,
                got: d0_matrix.rows() * d0_matrix.cols(),
            });
        }

        if d1_matrix.rows() != c2_dim || d1_matrix.cols() != c1_dim {
            return Err(HomologicalError::DimensionMismatch {
                expected: c2_dim * c1_dim,
                got: d1_matrix.rows() * d1_matrix.cols(),
            });
        }

        if c2_dim > 0 && c0_dim > 0 {
            let product = d1_matrix
                .mul(&d0_matrix)
                .map_err(HomologicalError::MatrixError)?;
            if !product.as_slice().iter().all(|x| x.is_zero()) {
                return Err(HomologicalError::CoboundaryLawViolation { degree: 0 });
            }
        }

        let d0 = CoboundaryMap::new(Degree::new(0), Degree::new(1), d0_matrix);
        let d1 = CoboundaryMap::new(Degree::new(1), Degree::new(2), d1_matrix);

        let provenance_hash = provenance.provenance_hash();
        let complex_hash =
            hash_cochain_complex_manifest(c0_dim, c1_dim, c2_dim, &d0.map_hash, &d1.map_hash);

        let _witness_hash =
            hash_cochain_witness(d0.matrix.shape(), d1.matrix.shape(), &provenance_hash);

        let witness = CochainComplexWitness::new(
            complex_hash,
            d0.map_hash.clone(),
            d1.map_hash.clone(),
            d0.matrix.shape(),
            d1.matrix.shape(),
            provenance_hash,
        );

        Ok(Self {
            c0_dim,
            c1_dim,
            c2_dim,
            d0,
            d1,
            witness,
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

    fn test_provenance() -> TheoremProvenance {
        TheoremProvenance::new("unit_test".to_string()).expect("provenance")
    }

    #[test]
    fn test_trivial_cochain_complex() {
        let d0 = zero_matrix(0, 1);
        let d1 = zero_matrix(0, 0);

        let complex = CochainComplex::new(1, 0, 0, d0, d1, test_provenance());
        assert!(complex.is_ok());
    }

    #[test]
    fn test_coboundary_law_verified() {

        let d0 = BasicMatrix::from_row_major(2, 1, vec![r(1), r(-1)]).expect("d0 creation");
        let d1 = BasicMatrix::from_row_major(1, 2, vec![r(1), r(1)]).expect("d1 creation");

        let complex = CochainComplex::new(1, 2, 1, d0, d1, test_provenance());
        assert!(complex.is_ok());
    }

    #[test]
    fn test_coboundary_law_violation_rejected() {

        let d0 = BasicMatrix::from_row_major(2, 1, vec![r(1), r(1)]).expect("d0 creation");
        let d1 = BasicMatrix::from_row_major(1, 2, vec![r(1), r(1)]).expect("d1 creation");

        let complex = CochainComplex::new(1, 2, 1, d0, d1, test_provenance());
        assert!(matches!(
            complex,
            Err(HomologicalError::CoboundaryLawViolation { degree: 0 })
        ));
    }

    #[test]
    fn test_dimension_mismatch_d0() {
        let d0 = BasicMatrix::from_row_major(3, 1, vec![r(0); 3]).expect("d0 creation");
        let d1 = zero_matrix(1, 2);

        let complex = CochainComplex::new(1, 2, 1, d0, d1, test_provenance());
        assert!(matches!(
            complex,
            Err(HomologicalError::DimensionMismatch { .. })
        ));
    }

    #[test]
    fn test_dimension_mismatch_d1() {
        let d0 = zero_matrix(2, 1);
        let d1 = BasicMatrix::from_row_major(2, 2, vec![r(0); 4]).expect("d1 creation");

        let complex = CochainComplex::new(1, 2, 1, d0, d1, test_provenance());
        assert!(matches!(
            complex,
            Err(HomologicalError::DimensionMismatch { .. })
        ));
    }

    #[test]
    fn test_empty_provenance_rejected() {
        let result = TheoremProvenance::new("   ".to_string());
        assert!(matches!(
            result,
            Err(HomologicalError::EmptyVerificationSource)
        ));
    }

    #[test]
    fn dim_rejects_degree_outside_finite_support() {
        let d0 = zero_matrix(0, 1);
        let d1 = zero_matrix(0, 0);
        let complex = CochainComplex::new(1, 0, 0, d0, d1, test_provenance())
            .expect("trivial cochain complex");
        assert_eq!(complex.dim(0).expect("degree 0 in support"), 1);
        assert_eq!(complex.dim(1).expect("degree 1 in support"), 0);
        assert_eq!(complex.dim(2).expect("degree 2 in support"), 0);
        assert!(matches!(
            complex.dim(3),
            Err(HomologicalError::InvalidDegree(3))
        ));
    }
}

#[cfg(test)]
mod contract_conformance {
    use super::CochainComplex;
    use omega_contracts::binding::ImplementsContract;
    use omega_contracts::contract_images::CochainComplexContract;

    impl ImplementsContract<CochainComplexContract> for CochainComplex {}

    #[test]
    fn cochain_complex_binds_and_audits_its_contract() {
        omega_contracts::assert_contract_binding!(CochainComplex, CochainComplexContract);
    }
}
