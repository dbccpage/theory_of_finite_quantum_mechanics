//! Typed newtype IDs for homological algebra entities.
//!
//! Each ID type uniquely identifies a specific kind of mathematical object
//! within the omega_homology system. Numeric constructors reject the zero id.
//! Basis names are checked by [`BasisId::try_new`]. [`Degree::new`] stays total
//! because chain complexes use negative degrees; the degree-drop law is
//! [`boundary_lowers_degree_by_one`].

use serde::{Deserialize, Serialize};

/// Refusal of an identifier constructor.
#[derive(Debug, Clone, Copy, PartialEq, Eq, thiserror::Error)]
pub enum IdError {
    /// A numeric homological id was zero.
    #[error("zero identifier")]
    ZeroId,
    /// A basis name was empty or only whitespace.
    #[error("empty basis identifier")]
    EmptyBasis,
    /// A degree shift overflowed `i32`.
    #[error("degree overflow")]
    DegreeOverflow,
}

macro_rules! define_id {
    ($(#[$meta:meta])* $name:ident) => {
        $(#[$meta])*
        #[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize)]
        #[serde(try_from = "u64", into = "u64")]
        pub struct $name(u64);

        impl $name {
            /// Construct a nonzero id. Zero is not an identifier.
            pub fn new(id: u64) -> Result<Self, IdError> {
                if id == 0 {
                    Err(IdError::ZeroId)
                } else {
                    Ok(Self(id))
                }
            }

            pub fn get(self) -> u64 {
                self.0
            }
        }

        impl TryFrom<u64> for $name {
            type Error = IdError;
            fn try_from(value: u64) -> Result<Self, IdError> { Self::new(value) }
        }
        impl From<$name> for u64 {
            fn from(value: $name) -> u64 { value.0 }
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
#[serde(try_from = "String", into = "String")]
pub struct BasisId(String);

impl BasisId {
    /// Construct an identifier for a graded basis family; empty names are invalid.
    pub fn new(name: impl Into<String>) -> Result<Self, IdError> {
        Self::try_new(&name.into())
    }

    pub fn as_str(&self) -> &str {
        &self.0
    }

    /// Reject an empty or whitespace basis name.
    pub fn try_new(name: &str) -> Result<Self, IdError> {
        if name.trim().is_empty() {
            Err(IdError::EmptyBasis)
        } else {
            Ok(Self(name.to_string()))
        }
    }
}

impl TryFrom<String> for BasisId {
    type Error = IdError;
    fn try_from(value: String) -> Result<Self, IdError> {
        Self::new(value)
    }
}
impl From<BasisId> for String {
    fn from(value: BasisId) -> String {
        value.0
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

    pub fn checked_pred(self) -> Result<Self, IdError> {
        self.0
            .checked_sub(1)
            .map(Self)
            .ok_or(IdError::DegreeOverflow)
    }

    pub fn checked_succ(self) -> Result<Self, IdError> {
        self.0
            .checked_add(1)
            .map(Self)
            .ok_or(IdError::DegreeOverflow)
    }
}

impl std::fmt::Display for Degree {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "deg({})", self.0)
    }
}

/// Boundary maps lower degree by exactly one, and that shift is invertible
/// away from `i32` overflow.
pub fn boundary_lowers_degree_by_one(source: Degree) -> Result<(), IdError> {
    let target = source.checked_pred()?;
    let restored = target.checked_succ()?;
    if restored != source {
        return Err(IdError::DegreeOverflow);
    }
    if restored.value().checked_sub(target.value()) != Some(1) {
        return Err(IdError::DegreeOverflow);
    }
    Ok(())
}

/// Display prefixes of the numeric id kinds are pairwise distinct, and a
/// nonzero chain id round-trips through its display text.
pub fn identifier_kinds_round_trip(id: u64) -> Result<(), IdError> {
    let chain = ChainId::new(id)?;
    let rendered = chain.to_string();
    let payload = parse_parenthesized(&rendered, "ChainId")?;
    if payload != id {
        return Err(IdError::ZeroId);
    }
    let mut prefixes = element_kind_prefixes()?.to_vec();
    prefixes.extend(structure_kind_prefixes()?);
    for (index, prefix) in prefixes.iter().enumerate() {
        let head = prefix.split('(').next().unwrap_or("");
        if head.is_empty() {
            return Err(IdError::EmptyBasis);
        }
        for earlier in prefixes.iter().take(index) {
            let other = earlier.split('(').next().unwrap_or("");
            if head == other {
                return Err(IdError::ZeroId);
            }
        }
    }
    Ok(())
}

fn element_kind_prefixes() -> Result<[String; 6], IdError> {
    Ok([
        ChainId::new(1)?.to_string(),
        CochainId::new(1)?.to_string(),
        CycleId::new(1)?.to_string(),
        CocycleId::new(1)?.to_string(),
        BoundaryId::new(1)?.to_string(),
        CoboundaryId::new(1)?.to_string(),
    ])
}

fn structure_kind_prefixes() -> Result<[String; 8], IdError> {
    Ok([
        ChainComplexId::new(1)?.to_string(),
        CochainComplexId::new(1)?.to_string(),
        HomologyClassId::new(1)?.to_string(),
        CohomologyClassId::new(1)?.to_string(),
        CarrierId::new(1)?.to_string(),
        MatrixId::new(1)?.to_string(),
        ManifestId::new(1)?.to_string(),
        WitnessId::new(1)?.to_string(),
    ])
}

fn parse_parenthesized(text: &str, kind: &str) -> Result<u64, IdError> {
    let Some(rest) = text.strip_prefix(kind) else {
        return Err(IdError::EmptyBasis);
    };
    let Some(inner) = rest
        .strip_prefix('(')
        .and_then(|body| body.strip_suffix(')'))
    else {
        return Err(IdError::EmptyBasis);
    };
    let value: u64 = inner.parse().map_err(|_| IdError::ZeroId)?;
    if value == 0 {
        Err(IdError::ZeroId)
    } else {
        Ok(value)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_id_display() {
        assert!(matches!(ChainId::new(0), Err(IdError::ZeroId)));
        assert_eq!(
            ChainId::new(42).map(|id| id.to_string()).ok().as_deref(),
            Some("ChainId(42)")
        );
    }

    #[test]
    fn test_degree_ordering() {
        let d0 = Degree::new(0);
        let d1 = Degree::new(1);
        let d_neg = Degree::new(-1);
        assert!(d_neg < d0);
        assert!(d0 < d1);
        assert!(boundary_lowers_degree_by_one(d1).is_ok());
        assert!(boundary_lowers_degree_by_one(Degree::new(i32::MIN)).is_err());
    }

    #[test]
    fn test_id_equality() {
        let a = CarrierId::new(100).ok();
        let b = CarrierId::new(100).ok();
        let c = CarrierId::new(101).ok();
        assert_eq!(a, b);
        assert_ne!(a, c);
        assert!(BasisId::try_new("  ").is_err());
        assert!(BasisId::try_new("edge").is_ok());
        assert!(identifier_kinds_round_trip(7).is_ok());
    }
}
