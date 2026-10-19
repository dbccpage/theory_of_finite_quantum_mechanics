//! faithful_functor shell for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.
//!
//! Faithfulness claim (injective on Hom-sets) — shape only, not a proof.

use serde::{Deserialize, Serialize};
use omega_category_theory::errors::ArithmosError;

/// Best-effort shell for a faithfulness claim on a functor reference.
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct FaithfulFunctor {
    pub label: String,
    pub functor_ref: String,
    pub notes: Vec<String>,
}

impl FaithfulFunctor {
    pub fn new(label: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            functor_ref: String::new(),
            notes: Vec::new(),
        }
    }

    pub fn on_functor(label: impl Into<String>, functor_ref: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            functor_ref: functor_ref.into(),
            notes: Vec::new(),
        }
    }

    pub fn validate_shell(&self) -> Result<(), ArithmosError> {
        if self.label.is_empty() {
            return Err(ArithmosError::InvalidShape("empty label".into()));
        }
        if self.functor_ref.is_empty() {
            return Err(ArithmosError::InvalidShape("empty functor_ref".into()));
        }
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn validate_ok() {
        assert!(FaithfulFunctor::on_functor("faithful", "F")
            .validate_shell()
            .is_ok());
    }

    #[test]
    fn validate_rejects_empty() {
        assert!(FaithfulFunctor::new("").validate_shell().is_err());
    }

    #[test]
    fn validate_rejects_missing_ref() {
        assert!(FaithfulFunctor::new("x").validate_shell().is_err());
    }
}
