//! forgetful_functor shell for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.
//!
//! Forgetful (underlying) functor U : C → D — shape only.

use serde::{Deserialize, Serialize};

/// Best-effort shell for a forgetful functor between labeled categories.
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct ForgetfulFunctor {
    pub label: String,
    pub source_category: String,
    pub target_category: String,
    pub notes: Vec<String>,
}

impl ForgetfulFunctor {
    pub fn new(label: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            source_category: String::new(),
            target_category: String::new(),
            notes: Vec::new(),
        }
    }

    pub fn between(
        label: impl Into<String>,
        source_category: impl Into<String>,
        target_category: impl Into<String>,
    ) -> Self {
        Self {
            label: label.into(),
            source_category: source_category.into(),
            target_category: target_category.into(),
            notes: Vec::new(),
        }
    }

    pub fn validate_shell(&self) -> Result<(), String> {
        if self.label.is_empty() {
            return Err("empty label".into());
        }
        if self.source_category.is_empty() {
            return Err("empty source_category".into());
        }
        if self.target_category.is_empty() {
            return Err("empty target_category".into());
        }
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn validate_ok() {
        assert!(ForgetfulFunctor::between("U", "Grp", "Set")
            .validate_shell()
            .is_ok());
    }

    #[test]
    fn validate_rejects_empty() {
        assert!(ForgetfulFunctor::new("").validate_shell().is_err());
    }

    #[test]
    fn validate_rejects_missing_categories() {
        assert!(ForgetfulFunctor::new("U").validate_shell().is_err());
    }
}
