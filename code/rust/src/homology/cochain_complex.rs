//! Finite cochain complex C^0 --d0--> C^1 --d1--> C^2 with d1 * d0 = 0.
//! AuthorityEffect: None. Public construction admits canonical Q coefficients.

use crate::homology::coboundary::CoboundaryMap;
use crate::homology::errors::HomologicalError;
use crate::homology::hashing::{hash_cochain_complex_manifest, hash_provenance, Hash256};
use crate::homology::ids::Degree;
use crate::homology::witness::CochainComplexWitness;
use crate::linear_algebra::basic_matrix::BasicMatrix;
use crate::linear_algebra::scalars::Q;
use serde::{Deserialize, Serialize};

/// Caller-supplied provenance label associated with a checked complex.
///
/// Admission checks only that the label is nonblank. This record does not
/// resolve the source or verify a theorem, authorship or authority.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(try_from = "String", into = "String")]
pub struct TheoremProvenance {
    verification_source: String,
}

impl TheoremProvenance {
    /// Store a nonblank provenance label without interpreting it.
    ///
    /// # Errors
    /// Returns `HomologicalError::EmptyVerificationSource` if the source string is empty
    /// or contains only whitespace.
    pub fn new(verification_source: String) -> Result<Self, HomologicalError> {
        if verification_source.trim().is_empty() {
            return Err(HomologicalError::EmptyVerificationSource);
        }
        Ok(Self {
            verification_source,
        })
    }

    /// Returns the verification source string.
    pub fn verification_source(&self) -> &str {
        &self.verification_source
    }

    /// Computes the hash of this provenance.
    pub fn provenance_hash(&self) -> Hash256 {
        hash_provenance(&self.verification_source)
    }
}

impl TryFrom<String> for TheoremProvenance {
    type Error = HomologicalError;
    fn try_from(value: String) -> Result<Self, Self::Error> {
        Self::new(value)
    }
}
impl From<TheoremProvenance> for String {
    fn from(value: TheoremProvenance) -> String {
        value.verification_source
    }
}

/// A finite cochain complex with verified coboundary law.
///
/// C^0 --d0--> C^1 --d1--> C^2
/// Invariant: d1 * d0 = 0
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct CochainComplex {
    /// Dimension of C^0.
    pub(super) c0_dim: usize,
    /// Dimension of C^1.
    pub(super) c1_dim: usize,
    /// Dimension of C^2.
    pub(super) c2_dim: usize,
    /// Coboundary map d0 : C^0 -> C^1 (matrix is c1_dim x c0_dim).
    pub(super) d0: CoboundaryMap,
    /// Coboundary map d1 : C^1 -> C^2 (matrix is c2_dim x c1_dim).
    pub(super) d1: CoboundaryMap,
    /// Receipt recorded after the coboundary-law check.
    pub(super) witness: CochainComplexWitness,
}

impl CochainComplex {
    /// Construct a cochain complex, verifying d1 * d0 = 0.
    ///
    /// # Arguments
    /// * `c0_dim` - Dimension of the degree-0 cochain group C^0.
    /// * `c1_dim` - Dimension of the degree-1 cochain group C^1.
    /// * `c2_dim` - Dimension of the degree-2 cochain group C^2.
    /// * `d0_matrix` - Coboundary map d^0: C^0 -> C^1 as a c1_dim x c0_dim matrix.
    /// * `d1_matrix` - Coboundary map d^1: C^1 -> C^2 as a c2_dim x c1_dim matrix.
    /// * `provenance` - Provenance recording the verification source.
    ///
    /// # Errors
    /// Returns `HomologicalError::ShapeMismatch` if matrix dimensions do not match
    /// the specified cochain group dimensions.
    /// Returns `HomologicalError::InvalidRational` for undefined or noncanonical coefficients.
    /// Returns `HomologicalError::CoboundaryLawViolation` if d1 * d0 != 0.
    /// Returns `HomologicalError::MatrixError` if matrix multiplication fails.
    pub fn new(
        c0_dim: usize,
        c1_dim: usize,
        c2_dim: usize,
        d0_matrix: BasicMatrix<Q>,
        d1_matrix: BasicMatrix<Q>,
        provenance: TheoremProvenance,
    ) -> Result<Self, HomologicalError> {
        super::exact_scalar::admit_shaped_matrix(&d0_matrix, (c1_dim, c0_dim))?;
        super::exact_scalar::admit_shaped_matrix(&d1_matrix, (c2_dim, c1_dim))?;
        super::exact_scalar::admit_zero_product(
            &d1_matrix,
            &d0_matrix,
            HomologicalError::CoboundaryLawViolation { degree: 0 },
        )?;

        let d0 = CoboundaryMap::new(Degree::new(0), Degree::new(1), d0_matrix)?;
        let d1 = CoboundaryMap::new(Degree::new(1), Degree::new(2), d1_matrix)?;

        let provenance_hash = provenance.provenance_hash();
        let complex_hash =
            hash_cochain_complex_manifest(c0_dim, c1_dim, c2_dim, &d0.map_hash, &d1.map_hash);

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

    /// Hash identifying this cochain complex.
    pub fn complex_hash(&self) -> &Hash256 {
        &self.witness.complex_hash
    }

    pub fn d0(&self) -> &CoboundaryMap {
        &self.d0
    }
    pub fn d1(&self) -> &CoboundaryMap {
        &self.d1
    }
    pub fn witness(&self) -> &CochainComplexWitness {
        &self.witness
    }

    /// Returns the dimension of the cochain group at the given degree.
    ///
    /// # Errors
    /// Returns `HomologicalError::InvalidDegree` for indices outside [0, 2]
    /// that fit i32, or `HomologicalError::InvalidDegreeIndex` otherwise.
    pub fn dim(&self, degree: usize) -> Result<usize, HomologicalError> {
        match degree {
            0 => Ok(self.c0_dim),
            1 => Ok(self.c1_dim),
            2 => Ok(self.c2_dim),
            _ => Err(HomologicalError::invalid_degree_index(degree)),
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
        // C^0 = R, C^1 = 0, C^2 = 0
        // All coboundary maps are zero.
        let d0 = zero_matrix(0, 1);
        let d1 = zero_matrix(0, 0);

        let complex = CochainComplex::new(1, 0, 0, d0, d1, test_provenance());
        assert!(complex.is_ok());
    }

    #[test]
    fn test_coboundary_law_verified() {
        // Simple cochain complex where d1 * d0 = 0 is satisfied.
        // C^0 = R, C^1 = R^2, C^2 = R
        // d0: [1; -1], d1: [1, 1]
        // d1 * d0 = [1, 1] * [1; -1] = 1 + (-1) = 0

        let d0 = BasicMatrix::from_row_major(2, 1, vec![r(1), r(-1)]).expect("d0 creation");
        let d1 = BasicMatrix::from_row_major(1, 2, vec![r(1), r(1)]).expect("d1 creation");

        let complex = CochainComplex::new(1, 2, 1, d0, d1, test_provenance());
        assert!(complex.is_ok());
    }

    #[test]
    fn test_coboundary_law_violation_rejected() {
        // d1 * d0 != 0 should fail.
        // d0: [1; 1], d1: [1, 1]
        // d1 * d0 = [1, 1] * [1; 1] = 2 != 0

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
        // d0 has wrong dimensions.
        let d0 = BasicMatrix::from_row_major(3, 1, vec![r(0); 3]).expect("d0 creation");
        let d1 = zero_matrix(1, 2);

        let complex = CochainComplex::new(1, 2, 1, d0, d1, test_provenance());
        assert!(matches!(
            complex,
            Err(HomologicalError::ShapeMismatch { .. })
        ));
    }

    #[test]
    fn test_dimension_mismatch_d1() {
        // d1 has wrong dimensions.
        let d0 = zero_matrix(2, 1);
        let d1 = BasicMatrix::from_row_major(2, 2, vec![r(0); 4]).expect("d1 creation");

        let complex = CochainComplex::new(1, 2, 1, d0, d1, test_provenance());
        assert!(matches!(
            complex,
            Err(HomologicalError::ShapeMismatch { .. })
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

// Contract registry membership is metadata, not evidence for d1*d0=0.
// The constructor rejection tests above exercise the executable law directly.
