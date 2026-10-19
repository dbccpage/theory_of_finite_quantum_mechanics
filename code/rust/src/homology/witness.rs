//! Stored computation receipts. AuthorityEffect: None.
//!
//! These records store fields; their constructors do not check a theorem.
//! The chain/cochain producers create their receipts after checking the law.
//! Other receipt kinds require a trusted producer; their type names, hashes
//! and serialization alone do not establish the recorded property.

use crate::homology::hashing::Hash256;
use serde::Serialize;

/// Witness that boundary_1 * boundary_2 = 0 in a chain complex.
// Sealed witness (PO-AUTH-NC): `_private: ()` blocks external literal construction.
#[allow(clippy::manual_non_exhaustive)]
#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct ChainComplexWitness {
    pub(super) complex_hash: Hash256,
    pub(super) boundary_1_hash: Hash256,
    pub(super) boundary_2_hash: Hash256,
    pub(super) c0_dim: usize,
    pub(super) c1_dim: usize,
    pub(super) c2_dim: usize,
    _private: (),
}

impl ChainComplexWitness {
    pub(crate) fn new(
        complex_hash: Hash256,
        boundary_1_hash: Hash256,
        boundary_2_hash: Hash256,
        c0_dim: usize,
        c1_dim: usize,
        c2_dim: usize,
    ) -> Self {
        Self {
            complex_hash,
            boundary_1_hash,
            boundary_2_hash,
            c0_dim,
            c1_dim,
            c2_dim,
            _private: (),
        }
    }
}

/// Witness that d1 * d0 = 0 in a cochain complex.
// Sealed witness (PO-AUTH-NC): `_private: ()` blocks external literal construction.
#[allow(clippy::manual_non_exhaustive)]
#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct CochainComplexWitness {
    pub(super) complex_hash: Hash256,
    pub(super) d0_hash: Hash256,
    pub(super) d1_hash: Hash256,
    pub(super) d0_shape: (usize, usize),
    pub(super) d1_shape: (usize, usize),
    pub(super) provenance_hash: Hash256,
    _private: (),
}

impl CochainComplexWitness {
    pub(crate) fn new(
        complex_hash: Hash256,
        d0_hash: Hash256,
        d1_hash: Hash256,
        d0_shape: (usize, usize),
        d1_shape: (usize, usize),
        provenance_hash: Hash256,
    ) -> Self {
        Self {
            complex_hash,
            d0_hash,
            d1_hash,
            d0_shape,
            d1_shape,
            provenance_hash,
            _private: (),
        }
    }

    pub fn d0_shape(&self) -> (usize, usize) {
        self.d0_shape
    }
    pub fn d1_shape(&self) -> (usize, usize) {
        self.d1_shape
    }
}

/// Stored boundary-zero receipt, conditional on its producer's check.
// Sealed witness (PO-AUTH-NC): `_private: ()` blocks external literal construction.
#[allow(clippy::manual_non_exhaustive)]
#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct BoundaryZeroWitness {
    pub(super) complex_hash: Hash256,
    pub(super) degree: usize,
    pub(super) element_hash: Hash256,
    pub(super) boundary_map_hash: Option<Hash256>,
    _private: (),
}

impl BoundaryZeroWitness {
    pub(crate) fn new(
        complex_hash: Hash256,
        degree: usize,
        element_hash: Hash256,
        boundary_map_hash: Option<Hash256>,
    ) -> Self {
        Self {
            complex_hash,
            degree,
            element_hash,
            boundary_map_hash,
            _private: (),
        }
    }
}

/// Stored coboundary-zero receipt, conditional on its producer's check.
// Sealed witness (PO-AUTH-NC): `_private: ()` blocks external literal construction.
#[allow(clippy::manual_non_exhaustive)]
#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct CoboundaryZeroWitness {
    pub(super) complex_hash: Hash256,
    pub(super) degree: usize,
    pub(super) element_hash: Hash256,
    pub(super) coboundary_map_hash: Option<Hash256>,
    _private: (),
}

impl CoboundaryZeroWitness {
    pub(crate) fn new(
        complex_hash: Hash256,
        degree: usize,
        element_hash: Hash256,
        coboundary_map_hash: Option<Hash256>,
    ) -> Self {
        Self {
            complex_hash,
            degree,
            element_hash,
            coboundary_map_hash,
            _private: (),
        }
    }
}

/// Stored cycle-membership receipt; no independent checker is provided here.
#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct CycleWitness {
    pub(super) boundary_zero: BoundaryZeroWitness,
}

/// Stored cocycle-membership receipt; no independent checker is provided here.
#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct CocycleWitness {
    pub(super) coboundary_zero: CoboundaryZeroWitness,
}

/// Stored homology-result fields; no dimension law is checked here.
#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct HomologyWitness {
    pub(super) complex_hash: Hash256,
    pub(super) degree: usize,
    pub(super) ker_dim: usize,
    pub(super) im_dim: usize,
    pub(super) homology_dim: usize,
}

/// Stored cohomology-result fields; no dimension law is checked here.
#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct CohomologyWitness {
    pub(super) complex_hash: Hash256,
    pub(super) degree: usize,
    pub(super) ker_dim: usize,
    pub(super) im_dim: usize,
    pub(super) cohomology_dim: usize,
}

#[cfg(test)]
mod tests {
    use super::*;

    fn dummy_hash() -> Hash256 {
        Hash256([0u8; 32])
    }

    #[test]
    fn test_cochain_complex_witness_accessors() {
        let w = CochainComplexWitness::new(
            dummy_hash(),
            dummy_hash(),
            dummy_hash(),
            (3, 5),
            (7, 3),
            dummy_hash(),
        );
        assert_eq!(w.d0_shape(), (3, 5));
        assert_eq!(w.d1_shape(), (7, 3));
    }

    #[test]
    fn test_homology_witness_fields() {
        let w = HomologyWitness {
            complex_hash: dummy_hash(),
            degree: 1,
            ker_dim: 5,
            im_dim: 3,
            homology_dim: 2,
        };
        assert_eq!(w.degree, 1);
        assert_eq!(w.homology_dim, 2);
    }

    #[test]
    fn test_cohomology_witness_fields() {
        let w = CohomologyWitness {
            complex_hash: dummy_hash(),
            degree: 2,
            ker_dim: 4,
            im_dim: 1,
            cohomology_dim: 3,
        };
        assert_eq!(w.degree, 2);
        assert_eq!(w.cohomology_dim, 3);
    }
}
