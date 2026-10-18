
use serde::{Deserialize, Serialize};
use thiserror::Error;

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct SigmaType {
    pub base_type_ref: String,
    pub family_ref: String,
}

impl SigmaType {
    pub fn validate(&self) -> Result<(), SigmaTypeError> {
        if self.base_type_ref.is_empty() {
            return Err(SigmaTypeError::EmptyBaseTypeRef);
        }
        if self.family_ref.is_empty() {
            return Err(SigmaTypeError::EmptyFamilyRef);
        }
        Ok(())
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Error)]
pub enum SigmaTypeError {
    #[error("sigma type base_type_ref must be non-empty")]
    EmptyBaseTypeRef,
    #[error("sigma type family_ref must be non-empty")]
    EmptyFamilyRef,
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn validate_ok() {
        let sigma = SigmaType {
            base_type_ref: "A".to_string(),
            family_ref: "B".to_string(),
        };
        assert!(sigma.validate().is_ok());
    }

    #[test]
    fn validate_rejects_empty_base() {
        let sigma = SigmaType {
            base_type_ref: String::new(),
            family_ref: "B".to_string(),
        };
        assert_eq!(sigma.validate(), Err(SigmaTypeError::EmptyBaseTypeRef));
    }

    #[test]
    fn validate_rejects_empty_family() {
        let sigma = SigmaType {
            base_type_ref: "A".to_string(),
            family_ref: String::new(),
        };
        assert_eq!(sigma.validate(), Err(SigmaTypeError::EmptyFamilyRef));
    }
}
