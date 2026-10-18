//! Exact graded coordinate vectors with sealed chain/cochain kinds.
//! AuthorityEffect: None. BasisId names a graded coordinate family.
//! Arithmetic is defined only within one kind, degree and basis family.

use crate::homology::errors::HomologicalError;
use crate::homology::hashing::{hash_graded_vector, Hash256};
use crate::homology::ids::{BasisId, Degree};
use crate::linear_algebra::scalars::Q;
use num_traits::Zero;
use serde::{Deserialize, Serialize};

mod sealed {
    pub trait Sealed {}
}

pub trait VectorKind: sealed::Sealed + Clone + std::fmt::Debug + PartialEq + Eq {
    const TAG: &'static [u8];
}
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ChainKind;
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct CochainKind;
impl sealed::Sealed for ChainKind {}
impl sealed::Sealed for CochainKind {}
impl VectorKind for ChainKind {
    const TAG: &'static [u8] = b"chain";
}
impl VectorKind for CochainKind {
    const TAG: &'static [u8] = b"cochain";
}

/// A chain element: a vector of coefficients in a given degree.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(try_from = "VectorWire", bound = "")]
pub struct GradedVector<K: VectorKind> {
    #[serde(skip)]
    kind: std::marker::PhantomData<K>,
    pub(super) degree: Degree,
    pub(super) basis_id: BasisId,
    pub(super) coefficients: Vec<Q>,
}

#[derive(Deserialize)]
#[serde(deny_unknown_fields)]
struct VectorWire {
    degree: Degree,
    basis_id: BasisId,
    coefficients: Vec<Q>,
}
impl<K: VectorKind> TryFrom<VectorWire> for GradedVector<K> {
    type Error = HomologicalError;
    fn try_from(value: VectorWire) -> Result<Self, Self::Error> {
        Self::new(value.degree, value.basis_id, value.coefficients)
    }
}

impl<K: VectorKind> GradedVector<K> {
    /// Create a new chain with the given coefficients.
    pub fn new(
        degree: Degree,
        basis_id: BasisId,
        coefficients: Vec<Q>,
    ) -> Result<Self, HomologicalError> {
        super::exact_scalar::admit_coefficients(&coefficients)?;
        Ok(Self {
            degree,
            basis_id,
            coefficients,
            kind: std::marker::PhantomData,
        })
    }

    pub fn degree(&self) -> Degree {
        self.degree
    }
    pub fn basis_id(&self) -> &BasisId {
        &self.basis_id
    }
    pub fn coefficients(&self) -> &[Q] {
        &self.coefficients
    }

    /// Create a zero chain of given dimension.
    pub fn zero(degree: Degree, basis_id: BasisId, dim: usize) -> Result<Self, HomologicalError> {
        let mut coefficients = Vec::new();
        coefficients
            .try_reserve_exact(dim)
            .map_err(|_| HomologicalError::ResourceLimit("zero vector allocation"))?;
        coefficients.resize(dim, Q::zero());
        Self::new(degree, basis_id, coefficients)
    }

    /// Dimension of the chain (number of coefficients).
    pub fn dimension(&self) -> usize {
        self.coefficients.len()
    }

    /// Check if all coefficients are zero.
    pub fn is_zero(&self) -> bool {
        self.coefficients.iter().all(|c| c.is_zero())
    }

    /// Compute a deterministic hash of this chain.
    pub fn hash(&self) -> Hash256 {
        hash_graded_vector(
            K::TAG,
            self.degree.value(),
            self.basis_id.as_str(),
            &self.coefficients,
        )
    }

    /// Add two chains of the same degree and basis.
    pub fn add(&self, other: &Self) -> Result<Self, HomologicalError> {
        self.check_compatible(other)?;
        let coefficients = self
            .coefficients
            .iter()
            .zip(other.coefficients.iter())
            .map(|(a, b)| a + b)
            .collect();
        Ok(Self {
            degree: self.degree,
            basis_id: self.basis_id.clone(),
            coefficients,
            kind: std::marker::PhantomData,
        })
    }

    /// Subtract another chain.
    pub fn sub(&self, other: &Self) -> Result<Self, HomologicalError> {
        self.check_compatible(other)?;
        let coefficients = self
            .coefficients
            .iter()
            .zip(other.coefficients.iter())
            .map(|(a, b)| a - b)
            .collect();
        Ok(Self {
            degree: self.degree,
            basis_id: self.basis_id.clone(),
            coefficients,
            kind: std::marker::PhantomData,
        })
    }

    fn check_compatible(&self, other: &Self) -> Result<(), HomologicalError> {
        if self.degree != other.degree {
            return Err(HomologicalError::DegreeMismatch {
                expected: self.degree.value(),
                got: other.degree.value(),
            });
        }
        if self.basis_id != other.basis_id {
            return Err(HomologicalError::BasisMismatch {
                description: "different graded basis families".into(),
            });
        }
        if self.coefficients.len() != other.coefficients.len() {
            return Err(HomologicalError::DimensionMismatch {
                expected: self.coefficients.len(),
                got: other.coefficients.len(),
            });
        }
        Ok(())
    }

    /// Scalar multiplication.
    pub fn scalar_mul(&self, scalar: &Q) -> Result<Self, HomologicalError> {
        super::exact_scalar::admit_coefficients(std::slice::from_ref(scalar))?;
        Self::new(
            self.degree,
            self.basis_id.clone(),
            self.coefficients.iter().map(|c| c * scalar).collect(),
        )
    }
}
