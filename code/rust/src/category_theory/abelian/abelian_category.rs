//! abelian_category shell for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.
//!
//! Abelian category = additive + kernels + cokernels (flags only). Does not
//! verify that every mono is a kernel or that coimage ≅ image.

use serde::{Deserialize, Serialize};
use omega_category_theory::errors::ArithmosError;

/// Best-effort shell for an abelian-category claim.
///
/// Stores the classical checklist as bools: additive structure, kernels, and
/// cokernels. Shape validation only — no law discharge.
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct AbelianCategory {
    pub label: String,
    /// Additive structure present (Hom-sets are abelian groups, biproducts, …).
    pub additive: bool,
    /// Every morphism has a kernel (shape flag).
    pub has_kernels: bool,
    /// Every morphism has a cokernel (shape flag).
    pub has_cokernels: bool,
    pub notes: Vec<String>,
}

impl AbelianCategory {
    pub fn new(label: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            additive: false,
            has_kernels: false,
            has_cokernels: false,
            notes: Vec::new(),
        }
    }

    pub fn with_flags(
        label: impl Into<String>,
        additive: bool,
        has_kernels: bool,
        has_cokernels: bool,
    ) -> Self {
        Self {
            label: label.into(),
            additive,
            has_kernels,
            has_cokernels,
            notes: Vec::new(),
        }
    }

    /// Convenience: all three abelian checklist flags set true.
    pub fn claimed_abelian(label: impl Into<String>) -> Self {
        Self::with_flags(label, true, true, true)
    }

    pub fn with_note(mut self, note: impl Into<String>) -> Self {
        self.notes.push(note.into());
        self
    }

    /// Whether the stored flags match the classical abelian checklist.
    pub fn checklist_complete(&self) -> bool {
        self.additive && self.has_kernels && self.has_cokernels
    }

    /// Validate structural emptiness only (shell gate).
    pub fn validate_shell(&self) -> Result<(), ArithmosError> {
        if self.label.is_empty() {
            return Err(ArithmosError::InvalidShape("empty label".into()));
        }
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn validate_ok() {
        assert!(AbelianCategory::new("Mod_R").validate_shell().is_ok());
    }

    #[test]
    fn validate_rejects_empty() {
        assert!(AbelianCategory::new("").validate_shell().is_err());
    }

    #[test]
    fn claimed_abelian_sets_flags() {
        let a = AbelianCategory::claimed_abelian("Ab");
        assert!(a.additive && a.has_kernels && a.has_cokernels);
        assert!(a.checklist_complete());
        assert!(a.validate_shell().is_ok());
    }

    #[test]
    fn incomplete_checklist() {
        let a = AbelianCategory::with_flags("pre", true, true, false);
        assert!(!a.checklist_complete());
        assert!(a.validate_shell().is_ok());
    }
}
