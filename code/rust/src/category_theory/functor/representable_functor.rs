//! representable_functor shell for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.
//!
//! Representable functor claim (≅ Hom(A, −) or Hom(−, A)) — shape only.

use serde::{Deserialize, Serialize};
use tfqm_category_theory::errors::ArithmosError;

/// Best-effort shell for a representable functor on a category reference.
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct RepresentableFunctor {
    pub label: String,
    pub category_ref: String,
    /// Optional representing object tag.
    pub representing_object: String,
    pub notes: Vec<String>,
}

impl RepresentableFunctor {
    pub fn new(label: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            category_ref: String::new(),
            representing_object: String::new(),
            notes: Vec::new(),
        }
    }

    pub fn on_category(label: impl Into<String>, category_ref: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            category_ref: category_ref.into(),
            representing_object: String::new(),
            notes: Vec::new(),
        }
    }

    pub fn represented_by(
        label: impl Into<String>,
        category_ref: impl Into<String>,
        representing_object: impl Into<String>,
    ) -> Self {
        Self {
            label: label.into(),
            category_ref: category_ref.into(),
            representing_object: representing_object.into(),
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
        assert!(RepresentableFunctor::on_category("y_A", "C")
            .validate_shell()
            .is_ok());
    }

    #[test]
    fn validate_rejects_empty() {
        assert!(RepresentableFunctor::new("").validate_shell().is_err());
    }

    #[test]
    fn validate_rejects_missing_ref() {
        assert!(RepresentableFunctor::new("x").validate_shell().is_err());
    }

    #[test]
    fn represented_by_sets_object() {
        let r = RepresentableFunctor::represented_by("y_A", "C", "A");
        assert_eq!(r.representing_object, "A");
        assert!(r.validate_shell().is_ok());
    }
}
