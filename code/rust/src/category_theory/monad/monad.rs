//! monad shell for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.
//!
//! A monad is an endofunctor T with unit η : Id ⇒ T and multiply μ : T² ⇒ T.
//! This shell holds label refs only; law discharge is external.

use serde::{Deserialize, Serialize};
use omega_category_theory::errors::ArithmosError;

/// Best-effort shell for a labeled monad (T, η, μ).
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct Monad {
    pub label: String,
    /// Ref to the underlying endofunctor T : C → C.
    pub endofunctor_ref: String,
    /// Ref to the unit natural transformation η : Id ⇒ T.
    pub unit_ref: String,
    /// Ref to the multiplication natural transformation μ : T² ⇒ T.
    pub multiply_ref: String,
    /// Optional base category label (diagnostic).
    pub category_ref: String,
    pub notes: Vec<String>,
}

impl Monad {
    pub fn new(label: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            endofunctor_ref: String::new(),
            unit_ref: String::new(),
            multiply_ref: String::new(),
            category_ref: String::new(),
            notes: Vec::new(),
        }
    }

    pub fn with_structure(
        label: impl Into<String>,
        endofunctor_ref: impl Into<String>,
        unit_ref: impl Into<String>,
        multiply_ref: impl Into<String>,
    ) -> Self {
        Self {
            label: label.into(),
            endofunctor_ref: endofunctor_ref.into(),
            unit_ref: unit_ref.into(),
            multiply_ref: multiply_ref.into(),
            category_ref: String::new(),
            notes: Vec::new(),
        }
    }

    pub fn with_note(mut self, note: impl Into<String>) -> Self {
        self.notes.push(note.into());
        self
    }

    /// Validate structural emptiness only (shell gate).
    pub fn validate_shell(&self) -> Result<(), ArithmosError> {
        if self.label.is_empty() {
            return Err(ArithmosError::InvalidShape("empty label".into()));
        }
        if self.endofunctor_ref.is_empty() {
            return Err(ArithmosError::InvalidShape("empty endofunctor_ref".into()));
        }
        if self.unit_ref.is_empty() {
            return Err(ArithmosError::InvalidShape("empty unit_ref".into()));
        }
        if self.multiply_ref.is_empty() {
            return Err(ArithmosError::InvalidShape("empty multiply_ref".into()));
        }
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn validate_ok() {
        let m = Monad::with_structure("Maybe", "T_Maybe", "η_Maybe", "μ_Maybe");
        assert!(m.validate_shell().is_ok());
    }

    #[test]
    fn validate_rejects_empty_label() {
        assert!(Monad::new("").validate_shell().is_err());
    }

    #[test]
    fn validate_rejects_missing_refs() {
        let m = Monad::new("M");
        assert!(m.validate_shell().is_err());
    }

    #[test]
    fn structure_fields_present() {
        let m = Monad::with_structure("Id", "T_Id", "η_Id", "μ_Id").with_note("shell");
        assert_eq!(m.endofunctor_ref, "T_Id");
        assert_eq!(m.unit_ref, "η_Id");
        assert_eq!(m.multiply_ref, "μ_Id");
        assert_eq!(m.notes.len(), 1);
        assert!(m.validate_shell().is_ok());
    }
}
