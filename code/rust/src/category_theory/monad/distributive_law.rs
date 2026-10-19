//! distributive_law shell for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.
//!
//! A distributive law λ : T G ⇒ G T between monads T and G (or dual variants).
//! Shell holds monad refs and a transformation label; law discharge is external.

use serde::{Deserialize, Serialize};
use omega_category_theory::errors::ArithmosError;

/// Best-effort shell for a labeled distributive law between two monads.
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct DistributiveLaw {
    pub label: String,
    /// Ref to the “left” / outer-bound monad T.
    pub monad_t_ref: String,
    /// Ref to the “right” / inner-bound monad G.
    pub monad_g_ref: String,
    /// Ref to the natural transformation λ : T G ⇒ G T.
    pub transformation_ref: String,
    pub notes: Vec<String>,
}

impl DistributiveLaw {
    pub fn new(label: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            monad_t_ref: String::new(),
            monad_g_ref: String::new(),
            transformation_ref: String::new(),
            notes: Vec::new(),
        }
    }

    pub fn with_structure(
        label: impl Into<String>,
        monad_t_ref: impl Into<String>,
        monad_g_ref: impl Into<String>,
        transformation_ref: impl Into<String>,
    ) -> Self {
        Self {
            label: label.into(),
            monad_t_ref: monad_t_ref.into(),
            monad_g_ref: monad_g_ref.into(),
            transformation_ref: transformation_ref.into(),
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
        if self.monad_t_ref.is_empty() {
            return Err(ArithmosError::InvalidShape("empty monad_t_ref".into()));
        }
        if self.monad_g_ref.is_empty() {
            return Err(ArithmosError::InvalidShape("empty monad_g_ref".into()));
        }
        if self.transformation_ref.is_empty() {
            return Err(ArithmosError::InvalidShape("empty transformation_ref".into()));
        }
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn validate_ok() {
        let d = DistributiveLaw::with_structure("λ_TG", "T", "G", "λ");
        assert!(d.validate_shell().is_ok());
    }

    #[test]
    fn validate_rejects_empty() {
        assert!(DistributiveLaw::new("").validate_shell().is_err());
        assert!(DistributiveLaw::new("λ").validate_shell().is_err());
    }
}
