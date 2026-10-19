//! constant_functor shell for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.
//!
//! Constant functor Δ_d : C → D with value d — shape only.

use serde::{Deserialize, Serialize};
use omega_category_theory::errors::ArithmosError;

/// Best-effort shell for a constant functor between labeled categories.
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct ConstantFunctor {
    pub label: String,
    pub source_category: String,
    pub target_category: String,
    /// Constant object in the target category.
    pub constant_object: String,
    pub notes: Vec<String>,
}

impl ConstantFunctor {
    pub fn new(label: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            source_category: String::new(),
            target_category: String::new(),
            constant_object: String::new(),
            notes: Vec::new(),
        }
    }

    pub fn constant(
        label: impl Into<String>,
        source_category: impl Into<String>,
        target_category: impl Into<String>,
        constant_object: impl Into<String>,
    ) -> Self {
        Self {
            label: label.into(),
            source_category: source_category.into(),
            target_category: target_category.into(),
            constant_object: constant_object.into(),
            notes: Vec::new(),
        }
    }

    pub fn validate_shell(&self) -> Result<(), ArithmosError> {
        if self.label.is_empty() {
            return Err(ArithmosError::InvalidShape("empty label".into()));
        }
        if self.source_category.is_empty() {
            return Err(ArithmosError::InvalidShape("empty source_category".into()));
        }
        if self.target_category.is_empty() {
            return Err(ArithmosError::InvalidShape("empty target_category".into()));
        }
        if self.constant_object.is_empty() {
            return Err(ArithmosError::InvalidShape("empty constant_object".into()));
        }
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn validate_ok() {
        assert!(ConstantFunctor::constant("const_d", "C", "D", "d")
            .validate_shell()
            .is_ok());
    }

    #[test]
    fn validate_rejects_empty() {
        assert!(ConstantFunctor::new("").validate_shell().is_err());
    }

    #[test]
    fn validate_rejects_missing_fields() {
        assert!(ConstantFunctor::new("c").validate_shell().is_err());
    }
}
