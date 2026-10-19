//! base_category shell for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.

use serde::{Deserialize, Serialize};
use omega_category_theory::errors::ArithmosError;

/// Best-effort shell for the base of enrichment (monoidal V, often closed).
/// Separates "V as enrichment base" from ordinary monoidal inventory.
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct BaseCategory {
    pub label: String,
    /// Underlying monoidal category shell label for V.
    pub monoidal_ref: String,
    /// Optional closed structure / internal-hom ref on V.
    pub closed_ref: String,
    /// Optional completeness / cocompleteness claim tags.
    pub completeness_notes: Vec<String>,
    pub notes: Vec<String>,
}

impl BaseCategory {
    pub fn new(label: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            monoidal_ref: String::new(),
            closed_ref: String::new(),
            completeness_notes: Vec::new(),
            notes: Vec::new(),
        }
    }

    pub fn from_monoidal(label: impl Into<String>, monoidal_ref: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            monoidal_ref: monoidal_ref.into(),
            closed_ref: String::new(),
            completeness_notes: Vec::new(),
            notes: Vec::new(),
        }
    }

    pub fn validate_shell(&self) -> Result<(), ArithmosError> {
        if self.label.is_empty() {
            return Err(ArithmosError::InvalidShape("empty label".into()));
        }
        if self.monoidal_ref.is_empty() {
            return Err(ArithmosError::InvalidShape("empty monoidal_ref".into()));
        }
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn validate_ok() {
        assert!(BaseCategory::from_monoidal("V", "MonV")
            .validate_shell()
            .is_ok());
    }

    #[test]
    fn validate_rejects_empty() {
        assert!(BaseCategory::new("").validate_shell().is_err());
    }
}
