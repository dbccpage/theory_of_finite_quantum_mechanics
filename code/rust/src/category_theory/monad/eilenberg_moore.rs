//! eilenberg_moore shell for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.
//!
//! Eilenberg–Moore category C^T of algebras for a monad T.
//! Shell holds a base monad ref only; algebra objects are separate shells.

use serde::{Deserialize, Serialize};
use omega_category_theory::errors::ArithmosError;

/// Best-effort shell for a labeled Eilenberg–Moore category of a monad.
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct EilenbergMoore {
    pub label: String,
    /// Ref to the base monad T whose EM category this records.
    pub base_monad_ref: String,
    /// Optional base category label (diagnostic).
    pub base_category_ref: String,
    pub notes: Vec<String>,
}

impl EilenbergMoore {
    pub fn new(label: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            base_monad_ref: String::new(),
            base_category_ref: String::new(),
            notes: Vec::new(),
        }
    }

    pub fn for_monad(label: impl Into<String>, base_monad_ref: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            base_monad_ref: base_monad_ref.into(),
            base_category_ref: String::new(),
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
        if self.base_monad_ref.is_empty() {
            return Err(ArithmosError::InvalidShape("empty base_monad_ref".into()));
        }
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn validate_ok() {
        let em = EilenbergMoore::for_monad("EM(Maybe)", "Maybe");
        assert!(em.validate_shell().is_ok());
    }

    #[test]
    fn validate_rejects_empty() {
        assert!(EilenbergMoore::new("").validate_shell().is_err());
        assert!(EilenbergMoore::new("EM").validate_shell().is_err());
    }
}
