//! monad_transformer shell for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.
//!
//! A monad transformer lifts an inner monad through an outer constructor.
//! Shell holds label refs only; lift/law discharge is external.

use serde::{Deserialize, Serialize};
use tfqm_category_theory::errors::ArithmosError;

/// Best-effort shell for a labeled monad transformer.
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct MonadTransformer {
    pub label: String,
    /// Ref to the outer monad constructor / transformer family (e.g. StateT).
    pub outer_ref: String,
    /// Ref to the inner (base) monad being lifted.
    pub inner_monad_ref: String,
    /// Optional ref to the resulting composite monad.
    pub result_monad_ref: String,
    pub notes: Vec<String>,
}

impl MonadTransformer {
    pub fn new(label: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            outer_ref: String::new(),
            inner_monad_ref: String::new(),
            result_monad_ref: String::new(),
            notes: Vec::new(),
        }
    }

    pub fn with_structure(
        label: impl Into<String>,
        outer_ref: impl Into<String>,
        inner_monad_ref: impl Into<String>,
    ) -> Self {
        Self {
            label: label.into(),
            outer_ref: outer_ref.into(),
            inner_monad_ref: inner_monad_ref.into(),
            result_monad_ref: String::new(),
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
        if self.outer_ref.is_empty() {
            return Err(ArithmosError::InvalidShape("empty outer_ref".into()));
        }
        if self.inner_monad_ref.is_empty() {
            return Err(ArithmosError::InvalidShape("empty inner_monad_ref".into()));
        }
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn validate_ok() {
        let t = MonadTransformer::with_structure("StateT_Maybe", "StateT", "Maybe");
        assert!(t.validate_shell().is_ok());
    }

    #[test]
    fn validate_rejects_empty() {
        assert!(MonadTransformer::new("").validate_shell().is_err());
        assert!(MonadTransformer::new("T").validate_shell().is_err());
    }
}
