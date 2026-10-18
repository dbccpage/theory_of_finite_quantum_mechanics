//! copresheaf shell for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.
//!
//! Copresheaf on C (functor C → Set) — shape only.

use serde::{Deserialize, Serialize};

/// Best-effort shell for a copresheaf on a category reference.
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct Copresheaf {
    pub label: String,
    pub category_ref: String,
    pub notes: Vec<String>,
}

impl Copresheaf {
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
        assert!(Copresheaf::on_category("Q", "C").validate_shell().is_ok());
    }

    #[test]
    fn validate_rejects_empty() {
        assert!(Copresheaf::new("").validate_shell().is_err());
    }

    #[test]
    fn validate_rejects_missing_ref() {
        assert!(Copresheaf::new("Q").validate_shell().is_err());
    }
}
