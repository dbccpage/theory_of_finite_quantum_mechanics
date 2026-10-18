
use crate::hashing::Hash256;
use serde::{Deserialize, Serialize};

#[allow(clippy::manual_non_exhaustive)]
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct ChainComplexWitness {
    pub complex_hash: Hash256,
    pub boundary_1_hash: Hash256,
    pub boundary_2_hash: Hash256,
    pub c0_dim: usize,
    pub c1_dim: usize,
    pub c2_dim: usize,
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

#[allow(clippy::manual_non_exhaustive)]
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct CochainComplexWitness {
    pub complex_hash: Hash256,
    pub d0_hash: Hash256,
    pub d1_hash: Hash256,
    pub d0_shape: (usize, usize),
    pub d1_shape: (usize, usize),
    pub provenance_hash: Hash256,
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

#[allow(clippy::manual_non_exhaustive)]
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct BoundaryZeroWitness {
    pub complex_hash: Hash256,
    pub degree: usize,
    pub element_hash: Hash256,
    pub boundary_map_hash: Option<Hash256>,
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

#[allow(clippy::manual_non_exhaustive)]
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct CoboundaryZeroWitness {
    pub complex_hash: Hash256,
    pub degree: usize,
    pub element_hash: Hash256,
    pub coboundary_map_hash: Option<Hash256>,
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

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct CycleWitness {
    pub boundary_zero: BoundaryZeroWitness,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct CocycleWitness {
    pub coboundary_zero: CoboundaryZeroWitness,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct HomologyWitness {
    pub complex_hash: Hash256,
    pub degree: usize,
    pub ker_dim: usize,
    pub im_dim: usize,
    pub homology_dim: usize,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct CohomologyWitness {
    pub complex_hash: Hash256,
    pub degree: usize,
    pub ker_dim: usize,
    pub im_dim: usize,
    pub cohomology_dim: usize,
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
