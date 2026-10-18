//! DDC No-Authority Firewall registry for the DDA crate's well-typed trace surfaces.
//!
//! Canonical provenance:
//! `coda_atlas/F004_papers/006_project_anomalon_codename_woland_omega_engine/001_discrete_deformation_calculus/discrete_deformation_calculus.md`
//! (Paper ID: `oe_010_dda_trace_calculus`, Series: `008_engine_runtime`, `OE010-04`).
//!
//! The registry is sealed: downstream code cannot declare an unrelated type to
//! be a registered DDA trace. Both admitted trace types remain evidence-only,
//! and the registry deliberately has no dependency on the host promotion
//! contract. Adding another trace representation requires editing this owner
//! module and replaying the constructor audit.

use crate::ddc::ddc_alphabet::DdaTrace;
use crate::ddc::op_verification::VerifiedTrace;
use omega_types::authority::AuthorityEffect;

mod sealed {
    pub trait Sealed {}
}

/// Marker for the complete frozen registry of well-typed DDA trace types.
///
/// This trait cannot be implemented outside this crate because its supertrait
/// is private. An untyped model proposal such as `agent_contract::DefectTrace`
/// is intentionally excluded until the existing operation verifier has
/// converted it into one of the registered representations.
pub trait RegisteredDdaTrace: sealed::Sealed {}

impl sealed::Sealed for DdaTrace {}
impl RegisteredDdaTrace for DdaTrace {}

impl sealed::Sealed for VerifiedTrace {}
impl RegisteredDdaTrace for VerifiedTrace {}

/// Stable names used by the repository audit to detect registry drift.
pub const REGISTERED_DDA_TRACE_TYPES: [&str; 2] =
    ["dda_alphabet::DdaTrace", "op_verification::VerifiedTrace"];

/// DDC No-Authority Firewall (`OE010-04`): authority ceiling for every sealed registered trace.
///
/// Verification can strengthen evidence but cannot change this return type or
/// value. In particular, this function cannot construct `CertifiedAuthority`
/// or `AuthorizedLocalResultV1`; those types are not dependencies of this
/// registry and their constructors remain outside the DDA crate.
pub fn registered_trace_authority_effect<T: RegisteredDdaTrace>(_trace: &T) -> AuthorityEffect {
    AuthorityEffect::None
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::ddc::degree_tower::{BinaryCochainSegment, BinaryLinearMap};
    use crate::ddc::op_verification::CochainState;

    fn initial_state() -> CochainState {
        let d0 = BinaryLinearMap::from_rows(1, vec![vec![true], vec![false]]).unwrap();
        let d1 = BinaryLinearMap::from_rows(2, vec![vec![false, true]]).unwrap();
        let segment = BinaryCochainSegment::new(1, d0, d1).unwrap();
        CochainState::new(segment, vec![false, false]).unwrap()
    }

    #[test]
    fn both_registered_trace_types_are_pinned_to_none() {
        let emitted = DdaTrace::new();
        let verified = VerifiedTrace::new(initial_state());

        assert_eq!(
            registered_trace_authority_effect(&emitted),
            AuthorityEffect::None
        );
        assert_eq!(
            registered_trace_authority_effect(&verified),
            AuthorityEffect::None
        );
        assert_eq!(emitted.authority_effect(), AuthorityEffect::None);
        assert_eq!(verified.authority_effect(), AuthorityEffect::None);
    }
}
