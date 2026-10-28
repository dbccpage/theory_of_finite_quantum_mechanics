//! algebra_for_monad shell for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.
//!
//! An algebra for a monad T is a carrier A with structure map h : T(A) → A.
//! Shell holds carrier + structure-map labels and a monad ref.

use serde::{Deserialize, Serialize};
use tfqm_category_theory::errors::ArithmosError;

/// Best-effort shell for a labeled T-algebra (A, h).
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct AlgebraForMonad {
    pub label: String,
    /// Carrier object label A.
    pub carrier_label: String,
    /// Structure map label h : T(A) → A.
    pub structure_map_label: String,
    /// Ref to the ambient monad T.
    pub monad_ref: String,
    pub notes: Vec<String>,
}

impl AlgebraForMonad {
    pub fn new(label: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            carrier_label: String::new(),
            structure_map_label: String::new(),
            monad_ref: String::new(),
            notes: Vec::new(),
        }
    }

    pub fn with_structure(
        label: impl Into<String>,
        carrier_label: impl Into<String>,
        structure_map_label: impl Into<String>,
        monad_ref: impl Into<String>,
    ) -> Self {
        Self {
            label: label.into(),
            carrier_label: carrier_label.into(),
            structure_map_label: structure_map_label.into(),
            monad_ref: monad_ref.into(),
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
        if self.carrier_label.is_empty() {
            return Err(ArithmosError::InvalidShape("empty carrier_label".into()));
        }
        if self.structure_map_label.is_empty() {
            return Err(ArithmosError::InvalidShape("empty structure_map_label".into()));
        }
        if self.monad_ref.is_empty() {
            return Err(ArithmosError::InvalidShape("empty monad_ref".into()));
        }
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn validate_ok() {
        let a = AlgebraForMonad::with_structure("bool_alg", "Bool", "h_bool", "Maybe");
        assert!(a.validate_shell().is_ok());
    }

    #[test]
    fn validate_rejects_empty() {
        assert!(AlgebraForMonad::new("").validate_shell().is_err());
        assert!(AlgebraForMonad::new("a").validate_shell().is_err());
    }
}
