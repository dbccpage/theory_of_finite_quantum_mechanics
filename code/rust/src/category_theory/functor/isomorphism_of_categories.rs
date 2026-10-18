//! isomorphism_of_categories shell for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.
//!
//! Strict isomorphism of categories (inverse functors) — shape only.

use serde::{Deserialize, Serialize};

/// Best-effort shell for an isomorphism-of-categories claim.
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct IsomorphismOfCategories {
    pub label: String,
    pub functor_ref: String,
    pub inverse_functor_ref: String,
    pub notes: Vec<String>,
}

impl IsomorphismOfCategories {
    pub fn new(label: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            functor_ref: String::new(),
            inverse_functor_ref: String::new(),
            notes: Vec::new(),
        }
    }

    pub fn between(
        label: impl Into<String>,
        functor_ref: impl Into<String>,
        inverse_functor_ref: impl Into<String>,
    ) -> Self {
        Self {
            label: label.into(),
            functor_ref: functor_ref.into(),
            inverse_functor_ref: inverse_functor_ref.into(),
            notes: Vec::new(),
        }
    }

    pub fn validate_shell(&self) -> Result<(), String> {
        if self.label.is_empty() {
            return Err("empty label".into());
        }
        if self.functor_ref.is_empty() {
            return Err("empty functor_ref".into());
        }
        if self.inverse_functor_ref.is_empty() {
            return Err("empty inverse_functor_ref".into());
        }
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn validate_ok() {
        assert!(IsomorphismOfCategories::between("iso", "F", "F_inv")
            .validate_shell()
            .is_ok());
    }

    #[test]
    fn validate_rejects_empty() {
        assert!(IsomorphismOfCategories::new("").validate_shell().is_err());
    }

    #[test]
    fn validate_rejects_missing_refs() {
        assert!(IsomorphismOfCategories::new("iso")
            .validate_shell()
            .is_err());
    }
}
