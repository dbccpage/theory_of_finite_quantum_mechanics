
use crate::ddc::ddc_alphabet::DdaTrace;
use crate::ddc::op_verification::VerifiedTrace;
use omega_types::authority::AuthorityEffect;

mod sealed {
    pub trait Sealed {}
}

pub trait RegisteredDdaTrace: sealed::Sealed {}

impl sealed::Sealed for DdaTrace {}
impl RegisteredDdaTrace for DdaTrace {}

impl sealed::Sealed for VerifiedTrace {}
impl RegisteredDdaTrace for VerifiedTrace {}

pub const REGISTERED_DDA_TRACE_TYPES: [&str; 2] =
    ["dda_alphabet::DdaTrace", "op_verification::VerifiedTrace"];

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
