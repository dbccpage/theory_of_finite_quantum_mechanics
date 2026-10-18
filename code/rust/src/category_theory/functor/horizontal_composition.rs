//! horizontal_composition shell for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.
//!
//! Horizontal (Godement) composition of natural transformations — shape only.

use serde::{Deserialize, Serialize};

/// Best-effort shell for a horizontal composition claim on nat-trans refs.
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct HorizontalComposition {
    pub label: String,
    pub left_nat_trans_ref: String,
    pub right_nat_trans_ref: String,
    /// Optional result nat-trans label.
    pub result_ref: String,
    pub notes: Vec<String>,
}

impl HorizontalComposition {
    pub fn new(label: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            left_nat_trans_ref: String::new(),
            right_nat_trans_ref: String::new(),
            result_ref: String::new(),
            notes: Vec::new(),
        }
    }

    pub fn of(
        label: impl Into<String>,
        left_nat_trans_ref: impl Into<String>,
        right_nat_trans_ref: impl Into<String>,
    ) -> Self {
        Self {
            label: label.into(),
            left_nat_trans_ref: left_nat_trans_ref.into(),
            right_nat_trans_ref: right_nat_trans_ref.into(),
            result_ref: String::new(),
            notes: Vec::new(),
        }
    }

    pub fn validate_shell(&self) -> Result<(), String> {
        if self.label.is_empty() {
            return Err("empty label".into());
        }
        if self.left_nat_trans_ref.is_empty() {
            return Err("empty left_nat_trans_ref".into());
        }
        if self.right_nat_trans_ref.is_empty() {
            return Err("empty right_nat_trans_ref".into());
        }
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn validate_ok() {
        assert!(HorizontalComposition::of("hcomp", "alpha", "beta")
            .validate_shell()
            .is_ok());
    }

    #[test]
    fn validate_rejects_empty() {
        assert!(HorizontalComposition::new("").validate_shell().is_err());
    }

    #[test]
    fn validate_rejects_missing_refs() {
        assert!(HorizontalComposition::new("h").validate_shell().is_err());
    }
}
