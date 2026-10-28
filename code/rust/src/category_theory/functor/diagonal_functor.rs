//! diagonal_functor shell for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.
//!
//! Diagonal functor Δ : C → C × C (or C^n) — shape only.

use tfqm_category_theory::errors::ArithmosError;
use serde::{Deserialize, Serialize};

/// Best-effort shell for a diagonal functor on a category reference.
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct DiagonalFunctor {
    pub label: String,
    pub category_ref: String,
    /// Product arity (2 for C → C×C). Must be ≥ 2 when set.
    pub arity: u32,
    pub notes: Vec<String>,
}

impl DiagonalFunctor {
    pub fn new(label: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            category_ref: String::new(),
            arity: 2,
            notes: Vec::new(),
        }
    }

    pub fn on_category(label: impl Into<String>, category_ref: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            category_ref: category_ref.into(),
            arity: 2,
            notes: Vec::new(),
        }
    }

    pub fn with_arity(
        label: impl Into<String>,
        category_ref: impl Into<String>,
        arity: u32,
    ) -> Self {
        Self {
            label: label.into(),
            category_ref: category_ref.into(),
            arity,
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
        if self.arity < 2 {
            return Err(ArithmosError::InvalidShape(format!("arity {} < 2", self.arity)));
        }
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn validate_ok() {
        assert!(DiagonalFunctor::on_category("Delta", "C")
            .validate_shell()
            .is_ok());
    }

    #[test]
    fn validate_rejects_empty() {
        assert!(DiagonalFunctor::new("").validate_shell().is_err());
    }

    #[test]
    fn validate_rejects_missing_ref() {
        assert!(DiagonalFunctor::new("D").validate_shell().is_err());
    }

    #[test]
    fn rejects_arity_one() {
        let d = DiagonalFunctor::with_arity("D", "C", 1);
        assert!(d.validate_shell().is_err());
    }
}
