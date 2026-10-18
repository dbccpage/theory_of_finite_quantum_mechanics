//! Univalence witness shape records (ShapeOnly).
//!
//! [`UnivalenceWitness`] holds references that *would* inhabit a univalence
//! statement in a universe. **This module does not claim that the univalence
//! axiom is proved**, does not mint authority, and does not assert that
//! `proof_ref` is a completed formal proof — only that the shape is filled.

use serde::{Deserialize, Serialize};
use thiserror::Error;

/// ShapeOnly witness record for univalence in a named universe.
///
/// - `universe_ref` — carrier universe (e.g. `U_i`) in which UA is stated
/// - `proof_ref` — external reference to a purported witness/certificate object
///
/// **AuthorityEffect: None.** Presence of this record is not a proof of UA
/// and must not be promoted as one.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct UnivalenceWitness {
    pub universe_ref: String,
    pub proof_ref: String,
}

impl UnivalenceWitness {
    /// Shape-only validation: universe and proof references must be non-empty.
    ///
    /// Does **not** verify that `proof_ref` is a valid univalence proof.
    pub fn validate(&self) -> Result<(), UnivalenceWitnessError> {
        if self.universe_ref.is_empty() || self.proof_ref.is_empty() {
            return Err(UnivalenceWitnessError::MissingReference);
        }
        Ok(())
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Error)]
pub enum UnivalenceWitnessError {
    #[error("univalence witness is missing universe or proof reference")]
    MissingReference,
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn univalence_witness_shape_only_validate() {
        let w = UnivalenceWitness {
            universe_ref: "U0".to_string(),
            proof_ref: "ua-shape-ref".to_string(),
        };
        assert!(w.validate().is_ok());
    }

    #[test]
    fn univalence_witness_rejects_empty() {
        let w = UnivalenceWitness {
            universe_ref: String::new(),
            proof_ref: "p".to_string(),
        };
        assert_eq!(w.validate(), Err(UnivalenceWitnessError::MissingReference));
    }
}
