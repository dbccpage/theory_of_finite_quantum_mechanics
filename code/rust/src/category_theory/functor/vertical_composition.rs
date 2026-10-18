//! vertical_composition shell for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.
//!
//! Vertical composition of natural transformations (β ∘ α) — shape only.

use serde::{Deserialize, Serialize};

/// Best-effort shell for a vertical composition claim on nat-trans refs.
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct VerticalComposition {
    pub label: String,
    /// Outer (later) natural transformation.
    pub outer_nat_trans_ref: String,
    /// Inner (earlier) natural transformation.
    pub inner_nat_trans_ref: String,
    /// Optional result nat-trans label.
    pub result_ref: String,
    pub notes: Vec<String>,
}

impl VerticalComposition {
    pub fn new(label: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            outer_nat_trans_ref: String::new(),
            inner_nat_trans_ref: String::new(),
            result_ref: String::new(),
            notes: Vec::new(),
        }
    }

    pub fn of(
        label: impl Into<String>,
        outer_nat_trans_ref: impl Into<String>,
        inner_nat_trans_ref: impl Into<String>,
    ) -> Self {
        Self {
            label: label.into(),
            outer_nat_trans_ref: outer_nat_trans_ref.into(),
            inner_nat_trans_ref: inner_nat_trans_ref.into(),
            result_ref: String::new(),
            notes: Vec::new(),
        }
    }

    pub fn validate_shell(&self) -> Result<(), String> {
        if self.label.is_empty() {
            return Err("empty label".into());
        }
        if self.outer_nat_trans_ref.is_empty() {
            return Err("empty outer_nat_trans_ref".into());
        }
        if self.inner_nat_trans_ref.is_empty() {
            return Err("empty inner_nat_trans_ref".into());
        }
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn validate_ok() {
        assert!(VerticalComposition::of("vcomp", "beta", "alpha")
            .validate_shell()
            .is_ok());
    }

    #[test]
    fn validate_rejects_empty() {
        assert!(VerticalComposition::new("").validate_shell().is_err());
    }

    #[test]
    fn validate_rejects_missing_refs() {
        assert!(VerticalComposition::new("v").validate_shell().is_err());
    }
}
