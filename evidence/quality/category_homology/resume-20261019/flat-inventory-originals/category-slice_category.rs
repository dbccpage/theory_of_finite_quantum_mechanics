//! slice_category shell for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.
//!
//! C/c (objects over c): objects are morphisms x → c; morphisms are commuting triangles.

use serde::{Deserialize, Serialize};

/// Best-effort slice category shell C / apex.
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct SliceCategoryShell {
    pub label: String,
    pub base_label: String,
    /// Apex object tag in the base category.
    pub apex: String,
    /// Object tags of the slice (typically names of morphisms into apex).
    pub objects: Vec<String>,
    pub notes: Vec<String>,
}

impl SliceCategoryShell {
    pub fn new(label: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            base_label: String::new(),
            apex: String::new(),
            objects: Vec::new(),
            notes: Vec::new(),
        }
    }

    pub fn over(
        label: impl Into<String>,
        base_label: impl Into<String>,
        apex: impl Into<String>,
    ) -> Self {
        Self {
            label: label.into(),
            base_label: base_label.into(),
            apex: apex.into(),
            objects: Vec::new(),
            notes: Vec::new(),
        }
    }

    pub fn validate_shell(&self) -> Result<(), String> {
        if self.label.is_empty() {
            return Err("empty label".into());
        }
        if self.base_label.is_empty() {
            return Err("empty base_label".into());
        }
        if self.apex.is_empty() {
            return Err("empty apex".into());
        }
        for (i, o) in self.objects.iter().enumerate() {
            if o.is_empty() {
                return Err(format!("empty object tag at index {i}"));
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
        assert!(SliceCategoryShell::over("C/c", "C", "c")
            .validate_shell()
            .is_ok());
    }

    #[test]
    fn validate_rejects_empty() {
        assert!(SliceCategoryShell::new("").validate_shell().is_err());
        assert!(SliceCategoryShell::new("S").validate_shell().is_err());
    }
}
