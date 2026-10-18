//! Dependent function type former `Π(x:A). B(x)`.
//!
//! Structural record only: base and family are opaque string refs.

use serde::{Deserialize, Serialize};
use thiserror::Error;

/// Dependent product (function) type `Π(x : base). family(x)`.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct PiType {
    pub base_type_ref: String,
    pub family_ref: String,
}

impl PiType {
    /// Validate that base and family references are non-empty.
    pub fn validate(&self) -> Result<(), PiTypeError> {
        if self.base_type_ref.is_empty() {
            return Err(PiTypeError::EmptyBaseTypeRef);
        }
        if self.family_ref.is_empty() {
            return Err(PiTypeError::EmptyFamilyRef);
        }
        Ok(())
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Error)]
pub enum PiTypeError {
    #[error("pi type base_type_ref must be non-empty")]
    EmptyBaseTypeRef,
    #[error("pi type family_ref must be non-empty")]
    EmptyFamilyRef,
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn validate_ok() {
        let pi = PiType {
            base_type_ref: "A".to_string(),
            family_ref: "B".to_string(),
        };
        assert!(pi.validate().is_ok());
    }

    #[test]
    fn validate_rejects_empty_base() {
        let pi = PiType {
            base_type_ref: String::new(),
            family_ref: "B".to_string(),
        };
        assert_eq!(pi.validate(), Err(PiTypeError::EmptyBaseTypeRef));
    }

    #[test]
    fn validate_rejects_empty_family() {
        let pi = PiType {
            base_type_ref: "A".to_string(),
            family_ref: String::new(),
        };
        assert_eq!(pi.validate(), Err(PiTypeError::EmptyFamilyRef));
    }
}
