//! reflective subcategory shell for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.
//!
//! A full subcategory i : A ↪ C is reflective when the inclusion admits
//! a left adjoint (reflector) r : C → A, r ⊣ i.

use serde::{Deserialize, Serialize};
use omega_category_theory::errors::ArithmosError;

/// Best-effort shell for a reflective subcategory declaration.
///
/// Records subcategory and reflector labels only — not a reflectivity proof.
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct ReflectiveSubcategoryShell {
    pub label: String,
    /// Ambient category C.
    pub ambient_category: String,
    /// Subcategory A ⊆ C (full subcategory label).
    pub subcategory: String,
    /// Inclusion i : A → C label.
    pub inclusion: String,
    /// Reflector (left adjoint) r : C → A label.
    pub reflector: String,
    /// Optional unit ref for r ⊣ i.
    pub unit_ref: String,
    /// Optional counit ref for r ⊣ i.
    pub counit_ref: String,
    pub notes: Vec<String>,
}

impl ReflectiveSubcategoryShell {
    pub fn new(label: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            ambient_category: String::new(),
            subcategory: String::new(),
            inclusion: String::new(),
            reflector: String::new(),
            unit_ref: String::new(),
            counit_ref: String::new(),
            notes: Vec::new(),
        }
    }

    pub fn with_labels(
        label: impl Into<String>,
        ambient_category: impl Into<String>,
        subcategory: impl Into<String>,
        reflector: impl Into<String>,
    ) -> Self {
        Self {
            label: label.into(),
            ambient_category: ambient_category.into(),
            subcategory: subcategory.into(),
            inclusion: String::new(),
            reflector: reflector.into(),
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

    pub fn validate_shell(&self) -> Result<(), ArithmosError> {
        if self.label.is_empty() {
            return Err(ArithmosError::InvalidShape("empty label".into()));
        }
        if self.ambient_category.is_empty() {
            return Err(ArithmosError::InvalidShape("empty ambient_category".into()));
        }
        if self.subcategory.is_empty() {
            return Err(ArithmosError::InvalidShape("empty subcategory".into()));
        }
        if self.reflector.is_empty() {
            return Err(ArithmosError::InvalidShape("empty reflector".into()));
        }
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn validate_ok() {
        let r = ReflectiveSubcategoryShell::with_labels("refl", "C", "A", "r");
        assert!(r.validate_shell().is_ok());
    }

    #[test]
    fn validate_rejects_empty() {
        assert!(ReflectiveSubcategoryShell::new("")
            .validate_shell()
            .is_err());
    }

    #[test]
    fn with_inclusion_and_unit_ok() {
        let r = ReflectiveSubcategoryShell::with_labels("sheafification", "PSh", "Sh", "a")
            .with_inclusion("i")
            .with_unit_counit("η", "ε");
        assert_eq!(r.inclusion, "i");
        assert!(r.validate_shell().is_ok());
    }

    #[test]
    fn rejects_missing_reflector() {
        let r = ReflectiveSubcategoryShell::new("x").with_inclusion("i");
        // ambient/subcategory/reflector still empty
        let mut r = r;
        r.ambient_category = "C".into();
        r.subcategory = "A".into();
        assert!(r.validate_shell().is_err());
    }
}
