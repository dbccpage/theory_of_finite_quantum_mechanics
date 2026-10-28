//! derived_category shell for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.
//!
//! Derived category of an abelian category (localization of chain complexes
//! at quasi-isomorphisms). Shape only: records the base abelian label.
//! Computational homology of complexes is owned by `omega_homology` (docs link).

use serde::{Deserialize, Serialize};
use tfqm_category_theory::errors::ArithmosError;

/// Best-effort shell for a derived-category claim.
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct DerivedCategory {
    pub label: String,
    /// Label of the base abelian category of which this is D(·) / D^b(·) / ….
    pub base_abelian_label: String,
    pub notes: Vec<String>,
}

impl DerivedCategory {
    pub fn new(label: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            base_abelian_label: String::new(),
            notes: Vec::new(),
        }
    }

    pub fn of_abelian(label: impl Into<String>, base_abelian_label: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            base_abelian_label: base_abelian_label.into(),
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
        if self.base_abelian_label.is_empty() {
            return Err(ArithmosError::InvalidShape("empty base_abelian_label".into()));
        }
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn validate_ok() {
        let d = DerivedCategory::of_abelian("D(Ab)", "Ab");
        assert!(d.validate_shell().is_ok());
    }

    #[test]
    fn validate_rejects_empty_label() {
        let d = DerivedCategory::of_abelian("", "Ab");
        assert!(d.validate_shell().is_err());
    }

    #[test]
    fn validate_rejects_empty_base() {
        let d = DerivedCategory::new("D");
        assert!(d.validate_shell().is_err());
    }
}
