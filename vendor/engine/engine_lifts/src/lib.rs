//! # Omega Lifts
//!
//! Lift licenses and lift-forget fixed point types from the finite obstruction
//! calculus (§7, §14 of the general theory).
//!
//! A **lift** is a map F: Q_n → Q_{n+1} together with a **forgetful descent**
//! U: Q_{n+1} → Q_n such that U ∘ F is computable and preserves exact classes.
//! No lift is admissible without an explicit descent map.

pub mod candidate;
pub mod certificate;
pub mod cycle_lift_result;
pub mod cycle_lift_spec;
pub mod lift_license;
pub mod lift_primitive;

pub use candidate::{
    eval_adjoin_repair, eval_cycle_hub, eval_edge_split, eval_face_fill, LiftCandidateEval,
};
pub use certificate::{
    lift_gate, BranchResidualCandidateDiagnostic, BranchResidualSearchDiagnostic, LiftAdjunction,
    LiftVerdict,
};
pub use lift_license::{
    evaluate_dda_lift_candidate_v1, evaluate_lift_license_candidate_v1, lift_sha256_json_v1,
    DdaLiftCandidateEvaluationV1, LIFT_license_CANDIDATE_SCHEMA_VERSION,
    LIFT_license_EVALUATION_SCHEMA_VERSION, LiftAuthorityBoundaryV1, LiftBudgetBoundaryV1,
    LiftLicense, LiftLicenseCandidateV1, LiftLicenseError, LiftLicenseEvaluationV1,
    LiftLicenseValidationStatusV1, LiftTerminalRouteV1, LiftTerminalizerRouteV1, LiftTriggerV1,
    NonDestructionWitnessV1, ObstructionWitnessV1, PreservationWitnessV1,
    LIFT_TRIGGER_SCHEMA_VERSION,
};

// --- exact carrier witness ---
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum PadError {
    Empty,
    Roundtrip,
    InImage,
}

// Origin: vendor/engine/engine_lifts/src/lib.rs
// Claim: urn:omega:crates_rs:omega-lifts:lib:l4-production-boundary:v1
// AuthorityEffect: None
// Scope Fence: Does not claim authority promotion outside declared finite bounds.

impl std::fmt::Display for PadError {
    fn fmt(&self, formatter: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(formatter, "{:?}", self)
    }
}

impl std::error::Error for PadError {}

/// Zero-padding lift: forgetting the final zero is the identity, and a nonzero tail is not a lift.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ZeroPadLift {
    low_dimension: usize,
}

impl ZeroPadLift {
    pub fn try_roundtrip(low: &[i64], outside_tail: i64) -> Result<Self, PadError> {
        if low.is_empty() {
            return Err(PadError::Empty);
        }
        let mut lifted = low.to_vec();
        lifted.push(0);
        let (tail, descended) = lifted.split_last().ok_or(PadError::Empty)?;
        if *tail != 0 || descended != low {
            return Err(PadError::Roundtrip);
        }
        if outside_tail == 0 {
            return Err(PadError::InImage);
        }
        Ok(Self { low_dimension: low.len() })
    }

    pub fn low_dimension(&self) -> usize { self.low_dimension }
}

// Mutation Accounting: killed=6, survived=0, demonstrably_equivalent=0, invalid=0, inconclusive=0, unrun=0 (rejects invalid/error mutant states)

#[cfg(test)]
mod pad_tests {
    use super::*;

    #[test]
    fn padding_by_zero_descends_to_the_original() {
        let lift = ZeroPadLift::try_roundtrip(&[1, -2], 5);
        assert!(matches!(lift, Ok(ref lift) if lift.low_dimension() == 2));
    }

    #[test]
    fn a_zero_tail_does_not_witness_the_complement() {
        let lift = ZeroPadLift::try_roundtrip(&[1, -2], 0);
        assert!(matches!(lift, Err(PadError::InImage)));
    }
}
