
use serde::{Deserialize, Serialize};
use thiserror::Error;

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct UnivalenceWitness {
    pub universe_ref: String,
    pub proof_ref: String,
}

impl UnivalenceWitness {
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
