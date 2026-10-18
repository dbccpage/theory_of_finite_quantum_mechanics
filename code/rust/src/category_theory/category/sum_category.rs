//! sum_category (coproduct) shell for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.
//!
//! C + D: disjoint union of objects and morphisms; no cross morphisms.

use serde::{Deserialize, Serialize};

/// Best-effort sum (coproduct) category shell C + D.
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct SumCategoryShell {
    pub label: String,
    pub left_summand_label: String,
    pub right_summand_label: String,
    /// Optional left-tagged object inventory ("inl:c").
    pub left_objects: Vec<String>,
    /// Optional right-tagged object inventory ("inr:d").
    pub right_objects: Vec<String>,
    pub notes: Vec<String>,
}

impl SumCategoryShell {
    pub fn new(label: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            left_summand_label: String::new(),
            right_summand_label: String::new(),
            left_objects: Vec::new(),
            right_objects: Vec::new(),
            notes: Vec::new(),
        }
    }

    pub fn of(
        label: impl Into<String>,
        left_summand_label: impl Into<String>,
        right_summand_label: impl Into<String>,
    ) -> Self {
        Self {
            label: label.into(),
            left_summand_label: left_summand_label.into(),
            right_summand_label: right_summand_label.into(),
            left_objects: Vec::new(),
            right_objects: Vec::new(),
            notes: Vec::new(),
        }
    }

    pub fn validate_shell(&self) -> Result<(), String> {
        if self.label.is_empty() {
            return Err("empty label".into());
        }
        if self.left_summand_label.is_empty() {
            return Err("empty left_summand_label".into());
        }
        if self.right_summand_label.is_empty() {
            return Err("empty right_summand_label".into());
        }
        for (i, o) in self.left_objects.iter().enumerate() {
            if o.is_empty() {
                return Err(format!("empty left_objects tag at index {i}"));
            }
        }
        for (i, o) in self.right_objects.iter().enumerate() {
            if o.is_empty() {
                return Err(format!("empty right_objects tag at index {i}"));
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
        assert!(SumCategoryShell::of("C+D", "C", "D")
            .validate_shell()
            .is_ok());
    }

    #[test]
    fn validate_rejects_empty() {
        assert!(SumCategoryShell::new("").validate_shell().is_err());
        assert!(SumCategoryShell::new("S").validate_shell().is_err());
    }
}
