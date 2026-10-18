//! coreflective subcategory shell for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.
//!
//! A full subcategory i : A ↪ C is coreflective when the inclusion admits
//! a right adjoint (coreflector) c : C → A, i ⊣ c.

use serde::{Deserialize, Serialize};

/// Best-effort shell for a coreflective subcategory declaration.
///
/// Records subcategory and coreflector labels only — not a coreflectivity proof.
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct CoreflectiveSubcategoryShell {
    pub label: String,
    /// Ambient category C.
    pub ambient_category: String,
    /// Subcategory A ⊆ C (full subcategory label).
    pub subcategory: String,
    /// Inclusion i : A → C label.
    pub inclusion: String,
    /// Coreflector (right adjoint) c : C → A label.
    pub coreflector: String,
    /// Optional unit ref for i ⊣ c.
    pub unit_ref: String,
    /// Optional counit ref for i ⊣ c.
    pub counit_ref: String,
    pub notes: Vec<String>,
}

impl CoreflectiveSubcategoryShell {
    pub fn new(label: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            ambient_category: String::new(),
            subcategory: String::new(),
            inclusion: String::new(),
            coreflector: String::new(),
            unit_ref: String::new(),
            counit_ref: String::new(),
            notes: Vec::new(),
        }
    }

    pub fn with_labels(
        label: impl Into<String>,
        ambient_category: impl Into<String>,
        subcategory: impl Into<String>,
        coreflector: impl Into<String>,
    ) -> Self {
        Self {
            label: label.into(),
            ambient_category: ambient_category.into(),
            subcategory: subcategory.into(),
            inclusion: String::new(),
            coreflector: coreflector.into(),
            unit_ref: String::new(),
            counit_ref: String::new(),
            notes: Vec::new(),
        }
    }

    pub fn with_inclusion(mut self, inclusion: impl Into<String>) -> Self {
        self.inclusion = inclusion.into();
        self
    }

    pub fn with_unit_counit(
        mut self,
        unit_ref: impl Into<String>,
        counit_ref: impl Into<String>,
    ) -> Self {
        self.unit_ref = unit_ref.into();
        self.counit_ref = counit_ref.into();
        self
    }

    pub fn validate_shell(&self) -> Result<(), String> {
        if self.label.is_empty() {
            return Err("empty label".into());
        }
        if self.ambient_category.is_empty() {
            return Err("empty ambient_category".into());
        }
        if self.subcategory.is_empty() {
            return Err("empty subcategory".into());
        }
        if self.coreflector.is_empty() {
            return Err("empty coreflector".into());
        }
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn validate_ok() {
        let c = CoreflectiveSubcategoryShell::with_labels("corefl", "C", "A", "c");
        assert!(c.validate_shell().is_ok());
    }

    #[test]
    fn validate_rejects_empty() {
        assert!(CoreflectiveSubcategoryShell::new("")
            .validate_shell()
            .is_err());
    }

    #[test]
    fn with_inclusion_and_unit_ok() {
        let c = CoreflectiveSubcategoryShell::with_labels("compactly-gen", "Top", "CG", "k")
            .with_inclusion("i")
            .with_unit_counit("η", "ε");
        assert_eq!(c.coreflector, "k");
        assert!(c.validate_shell().is_ok());
    }

    #[test]
    fn rejects_missing_coreflector() {
        let mut c = CoreflectiveSubcategoryShell::new("x");
        c.ambient_category = "C".into();
        c.subcategory = "A".into();
        assert!(c.validate_shell().is_err());
    }
}
