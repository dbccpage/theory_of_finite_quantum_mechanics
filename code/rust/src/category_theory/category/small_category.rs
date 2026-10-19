//! small_category shell for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.
//!
//! A small category has a set (not a proper class) of morphisms.
//! This shell records a finite presentation claim only.

use omega_category_theory::errors::ArithmosError;
use serde::{Deserialize, Serialize};

use super::category::{FiniteCategoryShell, MorphismTriple};

/// Best-effort small-category shell (finite presentation + smallness claim).
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct SmallCategoryShell {
    pub label: String,
    /// Underlying raw presentation. Its object inventory may be empty;
    /// its label and stored tags must still pass the presentation shape checks.
    pub presentation: FiniteCategoryShell,
    /// Declared claim that Hom-sets are sets (diagnostic flag only).
    pub claims_small: bool,
    pub notes: Vec<String>,
}

impl SmallCategoryShell {
    pub fn new(label: impl Into<String>) -> Self {
        let label = label.into();
        Self {
            presentation: FiniteCategoryShell::new(label.clone()),
            label,
            claims_small: true,
            notes: Vec::new(),
        }
    }

    pub fn from_presentation(presentation: FiniteCategoryShell) -> Self {
        Self {
            label: presentation.label.clone(),
            presentation,
            claims_small: true,
            notes: Vec::new(),
        }
    }

    pub fn objects(&self) -> &[String] {
        &self.presentation.objects
    }

    pub fn morphisms(&self) -> &[MorphismTriple] {
        &self.presentation.morphisms
    }

    pub fn validate_shell(&self) -> Result<(), ArithmosError> {
        if self.label.is_empty() {
            return Err(ArithmosError::InvalidShape("empty label".into()));
        }
        if !self.claims_small {
            return Err(ArithmosError::InvalidShape(
                "claims_small must be true for SmallCategoryShell".into(),
            ));
        }
        self.presentation.validate_shell()?;
        // Child admission above already rejects an empty presentation label.
        if self.presentation.label != self.label && !self.presentation.objects.is_empty() {
            return Err(ArithmosError::InvalidShape(format!(
                "presentation.label {:?} != shell.label {:?}",
                self.presentation.label, self.label
            )));
        }
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn validate_ok() {
        assert!(SmallCategoryShell::new("C").validate_shell().is_ok());
    }

    #[test]
    fn validate_rejects_empty() {
        assert!(SmallCategoryShell::new("").validate_shell().is_err());
    }

    #[test]
    fn from_presentation_ok() {
        let p = FiniteCategoryShell::with_objects("C", vec!["x".into()]);
        let s = SmallCategoryShell::from_presentation(p);
        assert_eq!(s.objects().len(), 1);
        assert!(s.validate_shell().is_ok());
    }
}
