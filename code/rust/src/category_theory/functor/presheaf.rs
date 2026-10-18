//! presheaf shell for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.
//!
//! Presheaf on C (functor C^op → Set) — shape only (label + category_ref).

use serde::{Deserialize, Serialize};

/// Best-effort shell for a presheaf on a category reference.
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct Presheaf {
    pub label: String,
    pub category_ref: String,
    pub notes: Vec<String>,
}

impl Presheaf {
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

    pub fn validate_shell(&self) -> Result<(), String> {
        if self.label.is_empty() {
            return Err("empty label".into());
        }
        if self.category_ref.is_empty() {
            return Err("empty category_ref".into());
        }
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn validate_ok() {
        assert!(Presheaf::on_category("P", "C").validate_shell().is_ok());
    }

    #[test]
    fn validate_rejects_empty() {
        assert!(Presheaf::new("").validate_shell().is_err());
    }

    #[test]
    fn validate_rejects_missing_ref() {
        assert!(Presheaf::new("P").validate_shell().is_err());
    }
}
