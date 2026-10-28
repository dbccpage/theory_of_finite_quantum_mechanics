//! monoidal_category shell for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.

use serde::{Deserialize, Serialize};
use tfqm_category_theory::errors::ArithmosError;

/// Best-effort monoidal category shell.
/// Tensor, unit object, and coherence iso refs are string labels only.
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct MonoidalCategory {
    pub label: String,
    /// Underlying ordinary category label.
    pub underlying_category: String,
    /// Tensor bifunctor label/ref (⊗ : C × C → C).
    pub tensor: String,
    /// Unit object label (I ∈ Ob(C)).
    pub unit_object: String,
    /// Associator natural-iso ref α.
    pub associator_ref: String,
    /// Left unitor natural-iso ref λ.
    pub left_unitor_ref: String,
    /// Right unitor natural-iso ref ρ.
    pub right_unitor_ref: String,
    pub notes: Vec<String>,
}

impl MonoidalCategory {
    pub fn new(label: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            underlying_category: String::new(),
            tensor: String::new(),
            unit_object: String::new(),
            associator_ref: String::new(),
            left_unitor_ref: String::new(),
            right_unitor_ref: String::new(),
            notes: Vec::new(),
        }
    }

    pub fn with_structure(
        label: impl Into<String>,
        underlying_category: impl Into<String>,
        tensor: impl Into<String>,
        unit_object: impl Into<String>,
        associator_ref: impl Into<String>,
        left_unitor_ref: impl Into<String>,
        right_unitor_ref: impl Into<String>,
    ) -> Self {
        Self {
            label: label.into(),
            underlying_category: underlying_category.into(),
            tensor: tensor.into(),
            unit_object: unit_object.into(),
            associator_ref: associator_ref.into(),
            left_unitor_ref: left_unitor_ref.into(),
            right_unitor_ref: right_unitor_ref.into(),
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
        if self.tensor.is_empty() {
            return Err(ArithmosError::InvalidShape("empty tensor".into()));
        }
        if self.unit_object.is_empty() {
            return Err(ArithmosError::InvalidShape("empty unit_object".into()));
        }
        if self.associator_ref.is_empty() {
            return Err(ArithmosError::InvalidShape("empty associator_ref".into()));
        }
        if self.left_unitor_ref.is_empty() {
            return Err(ArithmosError::InvalidShape("empty left_unitor_ref".into()));
        }
        if self.right_unitor_ref.is_empty() {
            return Err(ArithmosError::InvalidShape("empty right_unitor_ref".into()));
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
            MonoidalCategory::with_structure("Vec", "Set", "x", "1", "a", "l", "r")
                .validate_shell()
                .is_ok()
        );
    }

    #[test]
    fn validate_rejects_empty() {
        assert!(MonoidalCategory::new("").validate_shell().is_err());
    }
}
