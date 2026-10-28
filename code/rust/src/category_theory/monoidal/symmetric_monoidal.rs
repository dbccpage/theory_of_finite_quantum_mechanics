//! symmetric_monoidal shell for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.

use serde::{Deserialize, Serialize};
use tfqm_category_theory::errors::ArithmosError;

/// Best-effort symmetric monoidal category shell.
/// Braiding ref with optional symmetry claim (c_{Y,X} ∘ c_{X,Y} = id).
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct SymmetricMonoidal {
    pub label: String,
    /// Underlying monoidal (or braided) category shell label.
    pub monoidal_ref: String,
    /// Braiding natural-iso ref (symmetric when squared = id).
    pub braiding_ref: String,
    /// Diagnostic flag: claimed symmetric (not certified).
    pub symmetric_claimed: bool,
    pub notes: Vec<String>,
}

impl SymmetricMonoidal {
    pub fn new(label: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            monoidal_ref: String::new(),
            braiding_ref: String::new(),
            symmetric_claimed: true,
            notes: Vec::new(),
        }
    }

    pub fn with_braiding(
        label: impl Into<String>,
        monoidal_ref: impl Into<String>,
        braiding_ref: impl Into<String>,
    ) -> Self {
        Self {
            label: label.into(),
            monoidal_ref: monoidal_ref.into(),
            braiding_ref: braiding_ref.into(),
            symmetric_claimed: true,
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
        if self.braiding_ref.is_empty() {
            return Err(ArithmosError::InvalidShape("empty braiding_ref".into()));
        }
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn validate_ok() {
        assert!(SymmetricMonoidal::with_braiding("Sym", "Mon", "sigma")
            .validate_shell()
            .is_ok());
    }

    #[test]
    fn validate_rejects_empty() {
        assert!(SymmetricMonoidal::new("").validate_shell().is_err());
    }
}
