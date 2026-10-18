//! coslice_category shell for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.
//!
//! c/C (objects under c): objects are morphisms c → x; morphisms are commuting triangles.

use serde::{Deserialize, Serialize};

/// Best-effort coslice category shell base / under nadir.
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct CosliceCategoryShell {
    pub label: String,
    pub base_label: String,
    /// Nadir (under-object) tag in the base category.
    pub nadir: String,
    /// Object tags of the coslice (typically names of morphisms out of nadir).
    pub objects: Vec<String>,
    pub notes: Vec<String>,
}

impl CosliceCategoryShell {
    pub fn new(label: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            base_label: String::new(),
            nadir: String::new(),
            objects: Vec::new(),
            notes: Vec::new(),
        }
    }

    pub fn under(
        label: impl Into<String>,
        base_label: impl Into<String>,
        nadir: impl Into<String>,
    ) -> Self {
        Self {
            label: label.into(),
            base_label: base_label.into(),
            nadir: nadir.into(),
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
        if self.nadir.is_empty() {
            return Err("empty nadir".into());
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
        assert!(CosliceCategoryShell::under("c/C", "C", "c")
            .validate_shell()
            .is_ok());
    }

    #[test]
    fn validate_rejects_empty() {
        assert!(CosliceCategoryShell::new("").validate_shell().is_err());
        assert!(CosliceCategoryShell::new("S").validate_shell().is_err());
    }
}
