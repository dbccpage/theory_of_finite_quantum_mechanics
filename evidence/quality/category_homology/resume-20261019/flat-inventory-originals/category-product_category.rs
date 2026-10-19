//! product_category shell for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.
//!
//! C × D: objects are pairs (c, d); morphisms are pairs of morphisms.

use serde::{Deserialize, Serialize};

/// Best-effort product category shell C × D.
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct ProductCategoryShell {
    pub label: String,
    pub left_factor_label: String,
    pub right_factor_label: String,
    /// Optional object-pair tags as "c|d" (diagnostic inventory).
    pub object_pairs: Vec<String>,
    pub notes: Vec<String>,
}

impl ProductCategoryShell {
    pub fn new(label: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            left_factor_label: String::new(),
            right_factor_label: String::new(),
            object_pairs: Vec::new(),
            notes: Vec::new(),
        }
    }

    pub fn of(
        label: impl Into<String>,
        left_factor_label: impl Into<String>,
        right_factor_label: impl Into<String>,
    ) -> Self {
        Self {
            label: label.into(),
            left_factor_label: left_factor_label.into(),
            right_factor_label: right_factor_label.into(),
            object_pairs: Vec::new(),
            notes: Vec::new(),
        }
    }

    pub fn validate_shell(&self) -> Result<(), String> {
        if self.label.is_empty() {
            return Err("empty label".into());
        }
        if self.left_factor_label.is_empty() {
            return Err("empty left_factor_label".into());
        }
        if self.right_factor_label.is_empty() {
            return Err("empty right_factor_label".into());
        }
        for (i, p) in self.object_pairs.iter().enumerate() {
            if p.is_empty() {
                return Err(format!("empty object_pair tag at index {i}"));
            }
        }
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn validate_ok() {
        assert!(ProductCategoryShell::of("C×D", "C", "D")
            .validate_shell()
            .is_ok());
    }

    #[test]
    fn validate_rejects_empty() {
        assert!(ProductCategoryShell::new("").validate_shell().is_err());
        assert!(ProductCategoryShell::new("P").validate_shell().is_err());
    }
}
