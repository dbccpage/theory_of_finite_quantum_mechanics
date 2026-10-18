//! functor_category shell for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.
//!
//! Functor category [C, D] (objects = functors, morphisms = nat-trans) — shape only.

use serde::{Deserialize, Serialize};

/// Best-effort shell for a labeled functor category [source, target].
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct FunctorCategory {
    pub label: String,
    pub source_category: String,
    pub target_category: String,
    pub notes: Vec<String>,
}

impl FunctorCategory {
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
        assert!(FunctorCategory::between("[C,D]", "C", "D")
            .validate_shell()
            .is_ok());
    }

    #[test]
    fn validate_rejects_empty() {
        assert!(FunctorCategory::new("").validate_shell().is_err());
    }

    #[test]
    fn validate_rejects_missing_categories() {
        assert!(FunctorCategory::new("x").validate_shell().is_err());
    }
}
