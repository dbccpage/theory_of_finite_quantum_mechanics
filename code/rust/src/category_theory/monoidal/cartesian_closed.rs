//! cartesian_closed shell for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.

use serde::{Deserialize, Serialize};
use tfqm_category_theory::errors::ArithmosError;

/// Best-effort cartesian closed category shell (CCC).
/// Product as tensor; exponential as internal-hom.
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct CartesianClosed {
    pub label: String,
    /// Underlying category label.
    pub underlying_category: String,
    /// Binary product / cartesian tensor ref.
    pub product_ref: String,
    /// Terminal object (unit) label.
    pub terminal_object: String,
    /// Exponential / internal-hom ref.
    pub exponential_ref: String,
    pub notes: Vec<String>,
}

impl CartesianClosed {
    pub fn new(label: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            underlying_category: String::new(),
            product_ref: String::new(),
            terminal_object: String::new(),
            exponential_ref: String::new(),
            notes: Vec::new(),
        }
    }

    pub fn with_structure(
        label: impl Into<String>,
        underlying_category: impl Into<String>,
        product_ref: impl Into<String>,
        terminal_object: impl Into<String>,
        exponential_ref: impl Into<String>,
    ) -> Self {
        Self {
            label: label.into(),
            underlying_category: underlying_category.into(),
            product_ref: product_ref.into(),
            terminal_object: terminal_object.into(),
            exponential_ref: exponential_ref.into(),
            notes: Vec::new(),
        }
    }

    pub fn validate_shell(&self) -> Result<(), ArithmosError> {
        if self.label.is_empty() {
            return Err(ArithmosError::InvalidShape("empty label".into()));
        }
        if self.underlying_category.is_empty() {
            return Err(ArithmosError::InvalidShape("empty underlying_category".into()));
        }
        if self.product_ref.is_empty() {
            return Err(ArithmosError::InvalidShape("empty product_ref".into()));
        }
        if self.terminal_object.is_empty() {
            return Err(ArithmosError::InvalidShape("empty terminal_object".into()));
        }
        if self.exponential_ref.is_empty() {
            return Err(ArithmosError::InvalidShape("empty exponential_ref".into()));
        }
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn validate_ok() {
        assert!(
            CartesianClosed::with_structure("Set", "Set", "x", "1", "exp")
                .validate_shell()
                .is_ok()
        );
    }

    #[test]
    fn validate_rejects_empty() {
        assert!(CartesianClosed::new("").validate_shell().is_err());
    }
}
