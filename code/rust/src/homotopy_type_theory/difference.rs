use serde::{Deserialize, Serialize};
use std::fmt::Debug;
use thiserror::Error;

/// In CODA_GTLA HoTT foundation:
/// "Difference is primitive; sameness is certified zero-difference."
///
/// This trait represents the primitive difference object between two entities.
pub trait Difference<T> {
    type DiffObj: Debug;

    /// Computes the primitive difference between `self` and `other`.
    fn primitive_difference(&self, other: &T) -> Self::DiffObj;

    /// A certificate that the difference is strictly zero, constituting sameness.
    fn verify_zero_difference(diff: &Self::DiffObj) -> bool;
}

/// A finite primitive-difference packet.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct DifferenceTerm {
    pub source_ref: String,
    pub target_ref: String,
    pub difference_ref: String,
    pub computed_by_ref: String,
}

impl DifferenceTerm {
    pub fn validate(&self) -> Result<(), DifferenceError> {
        if self.source_ref.is_empty() || self.target_ref.is_empty() {
            return Err(DifferenceError::MissingEndpoint);
        }
        if self.difference_ref.is_empty() {
            return Err(DifferenceError::MissingDifferenceObject);
        }
        if self.computed_by_ref.is_empty() {
            return Err(DifferenceError::MissingComputationReference);
        }
        Ok(())
    }
}

/// Certificate that a declared difference has been checked to be zero.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct ZeroDifferenceCertificate {
    pub difference_ref: String,
    pub checker_ref: String,
    pub replay_ref: String,
}

impl ZeroDifferenceCertificate {
    pub fn validate(&self) -> Result<(), DifferenceError> {
        if self.difference_ref.is_empty() {
            return Err(DifferenceError::MissingDifferenceObject);
        }
        if self.checker_ref.is_empty() || self.replay_ref.is_empty() {
            return Err(DifferenceError::MissingZeroCertificate);
        }
        Ok(())
    }
}

/// A proof-relevant contextual congruence witness.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct ContextualDifferenceWitness {
    pub left_ref: String,
    pub right_ref: String,
    pub context_ref: String,
    pub before_difference_ref: String,
    pub after_difference_ref: String,
}

impl ContextualDifferenceWitness {
    pub fn is_failed_transport_witness(&self) -> bool {
        !self.before_difference_ref.is_empty()
            && !self.after_difference_ref.is_empty()
            && self.before_difference_ref != self.after_difference_ref
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Error)]
pub enum DifferenceError {
    #[error("difference endpoint missing")]
    MissingEndpoint,
    #[error("primitive difference object missing")]
    MissingDifferenceObject,
    #[error("difference computation reference missing")]
    MissingComputationReference,
    #[error("zero-difference certificate requires checker and replay refs")]
    MissingZeroCertificate,
}
