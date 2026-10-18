//! exact_category shell for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.
//!
//! Exact category shape: admissible short exact sequences. Optional bound on
//! tracked exact-sequence length is a diagnostic note only.

use serde::{Deserialize, Serialize};

/// Best-effort shell for an exact-category claim.
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct ExactCategory {
    pub label: String,
    /// Optional diagnostic bound: maximum exact-sequence length tracked.
    /// Shape note only — does not enforce Quillen exactness axioms.
    pub max_exact_sequences: Option<usize>,
    pub notes: Vec<String>,
}

impl ExactCategory {
    pub fn new(label: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            max_exact_sequences: None,
            notes: Vec::new(),
        }
    }

    pub fn with_max_exact_sequences(label: impl Into<String>, max_exact_sequences: usize) -> Self {
        Self {
            label: label.into(),
            max_exact_sequences: Some(max_exact_sequences),
            notes: Vec::new(),
        }
    }

    pub fn with_note(mut self, note: impl Into<String>) -> Self {
        self.notes.push(note.into());
        self
    }

    /// Validate structural emptiness only (shell gate).
    pub fn validate_shell(&self) -> Result<(), String> {
        if self.label.is_empty() {
            return Err("empty label".into());
        }
        if let Some(0) = self.max_exact_sequences {
            return Err("max_exact_sequences must be > 0 when set".into());
        }
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn validate_ok() {
        assert!(ExactCategory::new("exact").validate_shell().is_ok());
    }

    #[test]
    fn validate_rejects_empty() {
        assert!(ExactCategory::new("").validate_shell().is_err());
    }

    #[test]
    fn with_max_ok() {
        let e = ExactCategory::with_max_exact_sequences("Ex", 3);
        assert_eq!(e.max_exact_sequences, Some(3));
        assert!(e.validate_shell().is_ok());
    }

    #[test]
    fn rejects_zero_max() {
        let e = ExactCategory::with_max_exact_sequences("Ex", 0);
        assert!(e.validate_shell().is_err());
    }
}
