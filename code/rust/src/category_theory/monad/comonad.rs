//! comonad shell for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.
//!
//! Dual of a monad: endofunctor W with counit ε : W ⇒ Id and
//! comultiply δ : W ⇒ W². Label refs only; law discharge is external.

use serde::{Deserialize, Serialize};
use omega_category_theory::errors::ArithmosError;

/// Best-effort shell for a labeled comonad (W, ε, δ).
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct Comonad {
    pub label: String,
    /// Ref to the underlying endofunctor W : C → C.
    pub endofunctor_ref: String,
    /// Ref to the counit natural transformation ε : W ⇒ Id.
    pub counit_ref: String,
    /// Ref to the comultiplication natural transformation δ : W ⇒ W².
    pub comultiply_ref: String,
    /// Optional base category label (diagnostic).
    pub category_ref: String,
    pub notes: Vec<String>,
}

impl Comonad {
    pub fn new(label: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            endofunctor_ref: String::new(),
            counit_ref: String::new(),
            comultiply_ref: String::new(),
            category_ref: String::new(),
            notes: Vec::new(),
        }
    }

    pub fn with_structure(
        label: impl Into<String>,
        endofunctor_ref: impl Into<String>,
        counit_ref: impl Into<String>,
        comultiply_ref: impl Into<String>,
    ) -> Self {
        Self {
            label: label.into(),
            endofunctor_ref: endofunctor_ref.into(),
            counit_ref: counit_ref.into(),
            comultiply_ref: comultiply_ref.into(),
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
        if self.counit_ref.is_empty() {
            return Err(ArithmosError::InvalidShape("empty counit_ref".into()));
        }
        if self.comultiply_ref.is_empty() {
            return Err(ArithmosError::InvalidShape("empty comultiply_ref".into()));
        }
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn validate_ok() {
        let w = Comonad::with_structure("Env", "W_Env", "ε_Env", "δ_Env");
        assert!(w.validate_shell().is_ok());
    }

    #[test]
    fn validate_rejects_empty_label() {
        assert!(Comonad::new("").validate_shell().is_err());
    }

    #[test]
    fn validate_rejects_missing_refs() {
        let w = Comonad::new("W");
        assert!(w.validate_shell().is_err());
    }
}
