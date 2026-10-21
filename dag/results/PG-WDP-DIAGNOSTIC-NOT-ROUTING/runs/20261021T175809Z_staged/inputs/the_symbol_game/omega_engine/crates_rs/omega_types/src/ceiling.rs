//! Canonical evidence ceiling type.
//!
//! This is the single authoritative definition of the evidence-routing ceiling.
//! It is a routing/authorization convention, not an absolute truth-strength claim.
//! See `evidence_ceiling_reconciliation_proof.md` for the formal justification.

use serde::{Deserialize, Serialize};

/// The canonical evidence ceiling chain.
///
/// `ShapeOnly < LocalReplay < BoundaryChecked < ExternalOracleRequired < EmpiricalOracleRequired`
///
/// This is a **capability chain** describing what the host can verify.
/// It is NOT a rigor/provenance axis (see `RigorGrade`) and NOT a
/// witness-certainty axis (see `WitnessCertainty`).
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash, Serialize, Deserialize)]
#[repr(u8)]
pub enum EvidenceCeiling {
    ShapeOnly = 0,
    LocalReplay = 1,
    BoundaryChecked = 2,
    ExternalOracleRequired = 3,
    EmpiricalOracleRequired = 4,
}

impl EvidenceCeiling {
    pub fn meet(self, other: Self) -> Self {
        std::cmp::min(self, other)
    }

    pub fn join(self, other: Self) -> Self {
        std::cmp::max(self, other)
    }

    pub fn raise_with(self, cert_level: Self) -> Self {
        std::cmp::max(self, cert_level)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn order_chain_correct() {
        assert!(EvidenceCeiling::ShapeOnly < EvidenceCeiling::LocalReplay);
        assert!(EvidenceCeiling::LocalReplay < EvidenceCeiling::BoundaryChecked);
        assert!(EvidenceCeiling::BoundaryChecked < EvidenceCeiling::ExternalOracleRequired);
        assert!(EvidenceCeiling::ExternalOracleRequired < EvidenceCeiling::EmpiricalOracleRequired);
    }

    #[test]
    fn meet_returns_minimum() {
        assert_eq!(
            EvidenceCeiling::BoundaryChecked.meet(EvidenceCeiling::ShapeOnly),
            EvidenceCeiling::ShapeOnly,
        );
        assert_eq!(
            EvidenceCeiling::ShapeOnly.meet(EvidenceCeiling::EmpiricalOracleRequired),
            EvidenceCeiling::ShapeOnly,
        );
    }

    #[test]
    fn join_returns_maximum() {
        assert_eq!(
            EvidenceCeiling::ShapeOnly.join(EvidenceCeiling::BoundaryChecked),
            EvidenceCeiling::BoundaryChecked,
        );
        assert_eq!(
            EvidenceCeiling::EmpiricalOracleRequired.join(EvidenceCeiling::LocalReplay),
            EvidenceCeiling::EmpiricalOracleRequired,
        );
    }

    #[test]
    fn meet_idempotent() {
        for v in [
            EvidenceCeiling::ShapeOnly,
            EvidenceCeiling::LocalReplay,
            EvidenceCeiling::BoundaryChecked,
        ] {
            assert_eq!(v.meet(v), v);
        }
    }

    #[test]
    fn join_idempotent() {
        for v in [
            EvidenceCeiling::ShapeOnly,
            EvidenceCeiling::ExternalOracleRequired,
            EvidenceCeiling::EmpiricalOracleRequired,
        ] {
            assert_eq!(v.join(v), v);
        }
    }

    #[test]
    fn meet_commutative() {
        let a = EvidenceCeiling::LocalReplay;
        let b = EvidenceCeiling::ExternalOracleRequired;
        assert_eq!(a.meet(b), b.meet(a));
    }

    #[test]
    fn join_commutative() {
        let a = EvidenceCeiling::ShapeOnly;
        let b = EvidenceCeiling::BoundaryChecked;
        assert_eq!(a.join(b), b.join(a));
    }

    #[test]
    fn absorption() {
        let a = EvidenceCeiling::LocalReplay;
        let b = EvidenceCeiling::BoundaryChecked;
        assert_eq!(a.meet(a.join(b)), a);
        assert_eq!(a.join(a.meet(b)), a);
    }

    #[test]
    fn raise_with_is_max() {
        assert_eq!(
            EvidenceCeiling::ShapeOnly.raise_with(EvidenceCeiling::BoundaryChecked),
            EvidenceCeiling::BoundaryChecked,
        );
        assert_eq!(
            EvidenceCeiling::EmpiricalOracleRequired.raise_with(EvidenceCeiling::LocalReplay),
            EvidenceCeiling::EmpiricalOracleRequired,
        );
    }
}
