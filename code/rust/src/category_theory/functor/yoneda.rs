//! yoneda shell for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.
//!
//! Yoneda embedding / lemma carrier — shape only (label + category_ref).

use serde::{Deserialize, Serialize};
use omega_category_theory::errors::ArithmosError;

/// Best-effort shell for a Yoneda construction on a category reference.
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct Yoneda {
    pub label: String,
    pub category_ref: String,
    pub notes: Vec<String>,
}

impl Yoneda {
    pub fn new(label: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            category_ref: String::new(),
            notes: Vec::new(),
        }
    }

    pub fn on_category(label: impl Into<String>, category_ref: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            category_ref: category_ref.into(),
            notes: Vec::new(),
        }
    }

    pub fn validate_shell(&self) -> Result<(), ArithmosError> {
        if self.label.is_empty() {
            return Err(ArithmosError::InvalidShape("empty label".into()));
        }
        if self.category_ref.is_empty() {
            return Err(ArithmosError::InvalidShape("empty category_ref".into()));
        }
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn validate_ok() {
        assert!(Yoneda::on_category("y", "C").validate_shell().is_ok());
    }

    #[test]
    fn validate_rejects_empty() {
        assert!(Yoneda::new("").validate_shell().is_err());
    }

    #[test]
    fn validate_rejects_missing_ref() {
        assert!(Yoneda::new("y").validate_shell().is_err());
    }
}
