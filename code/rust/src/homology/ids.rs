//! Typed newtype IDs for homological algebra entities.
//!
//! Each ID type uniquely identifies a specific kind of mathematical object
//! within the omega_homology system.

use serde::{Deserialize, Serialize};

macro_rules! define_id {
    ($(#[$meta:meta])* $name:ident) => {
        $(#[$meta])*
        #[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize)]
        pub struct $name(pub u64);

        impl $name {
            pub fn new(id: u64) -> Self {
                Self(id)
            }
        }

        impl std::fmt::Display for $name {
            fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
                write!(f, "{}({})", stringify!($name), self.0)
            }
        }
    };
}

define_id!(
    /// Identifies a chain element.
    ChainId
);
define_id!(
    /// Identifies a cochain element.
    CochainId
);
define_id!(
    /// Identifies a verified cycle.
    CycleId
);
define_id!(
    /// Identifies a verified cocycle.
    CocycleId
);
define_id!(
    /// Identifies a boundary element.
    BoundaryId
);
define_id!(
    /// Identifies a coboundary element.
    CoboundaryId
);
define_id!(
    /// Identifies a chain complex.
    ChainComplexId
);
define_id!(
    /// Identifies a cochain complex.
    CochainComplexId
);
define_id!(
    /// Identifies a homology class.
    HomologyClassId
);
define_id!(
    /// Identifies a cohomology class.
    CohomologyClassId
);
define_id!(
    /// Identifies a carrier.
    CarrierId
);
/// Identifies a basis by name.
#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub struct BasisId(pub String);

impl BasisId {
    pub fn new(name: impl Into<String>) -> Self {
        Self(name.into())
    }
}

impl std::fmt::Display for BasisId {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "BasisId({})", self.0)
    }
}
define_id!(
    /// Identifies a matrix.
    MatrixId
);
define_id!(
    /// Identifies a manifest.
    ManifestId
);
define_id!(
    /// Identifies a witness.
    WitnessId
);

/// Grading degree in a chain/cochain complex.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, PartialOrd, Ord, Serialize, Deserialize)]
pub struct Degree(pub i32);

impl Degree {
    pub fn new(n: i32) -> Self {
        Self(n)
    }

    pub fn value(self) -> i32 {
        self.0
    }
}

impl std::fmt::Display for Degree {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "deg({})", self.0)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_id_display() {
        let chain_id = ChainId::new(42);
        assert_eq!(format!("{}", chain_id), "ChainId(42)");
    }

    #[test]
    fn test_degree_ordering() {
        let d0 = Degree::new(0);
        let d1 = Degree::new(1);
        let d_neg = Degree::new(-1);
        assert!(d_neg < d0);
        assert!(d0 < d1);
    }

    #[test]
    fn test_id_equality() {
        let a = CarrierId::new(100);
        let b = CarrierId::new(100);
        let c = CarrierId::new(101);
        assert_eq!(a, b);
        assert_ne!(a, c);
    }
}
