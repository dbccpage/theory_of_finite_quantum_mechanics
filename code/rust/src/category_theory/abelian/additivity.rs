//! additivity shell for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.
//!
//! Additive-category shape flags (zero object, biproducts). Not a proof of
//! enrichment over Ab or of biproduct existence.

use serde::{Deserialize, Serialize};
use tfqm_category_theory::errors::ArithmosError;

/// Best-effort shell for an additive-category claim.
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct Additivity {
    pub label: String,
    /// Claim that finite biproducts exist (shape flag only).
    pub has_biproducts: bool,
    /// Claim that a zero object exists (shape flag only).
    pub zero_object: bool,
    pub notes: Vec<String>,
}

impl Additivity {
    pub fn new(label: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            has_biproducts: false,
            zero_object: false,
            notes: Vec::new(),
        }
    }

    pub fn with_flags(label: impl Into<String>, has_biproducts: bool, zero_object: bool) -> Self {
        Self {
            label: label.into(),
            has_biproducts,
            zero_object,
            notes: Vec::new(),
        }
    }

    pub fn with_note(mut self, note: impl Into<String>) -> Self {
        self.notes.push(note.into());
        self
    }

    /// Validate structural emptiness only (shell gate).
    pub fn validate_shell(&self) -> Result<(), ArithmosError> {
        if self.label.is_empty() {
            return Err(ArithmosError::InvalidShape("empty label".into()));
        }
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn validate_ok() {
        assert!(Additivity::new("Ab").validate_shell().is_ok());
    }

    #[test]
    fn validate_rejects_empty() {
        assert!(Additivity::new("").validate_shell().is_err());
    }

    #[test]
    fn with_flags_sets_bools() {
        let a = Additivity::with_flags("Add", true, true);
        assert!(a.has_biproducts && a.zero_object);
        assert!(a.validate_shell().is_ok());
    }
}
