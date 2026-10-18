//! homological_algebra shell for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.
//!
//! Umbrella shell for homological-algebra vocabulary at the categorical layer
//! (Ext, Tor, long exact sequences, spectral sequences as categorical claims).
//! Computational homology / cochain machinery is owned by `omega_homology`
//! (conceptual link in docs comments only — no crate dependency).

use serde::{Deserialize, Serialize};

/// Best-effort shell for a homological-algebra topic claim.
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct HomologicalAlgebra {
    pub label: String,
    /// Optional base abelian / exact category label this topic sits over.
    pub base_category_label: String,
    pub notes: Vec<String>,
}

impl HomologicalAlgebra {
    pub fn new(label: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            base_category_label: String::new(),
            notes: Vec::new(),
        }
    }

    pub fn over_category(label: impl Into<String>, base_category_label: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            base_category_label: base_category_label.into(),
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
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn validate_ok() {
        let h = HomologicalAlgebra::over_category("Ext", "Mod_R");
        assert!(h.validate_shell().is_ok());
    }

    #[test]
    fn validate_rejects_empty() {
        assert!(HomologicalAlgebra::new("").validate_shell().is_err());
    }

    #[test]
    fn with_note_appends() {
        let h = HomologicalAlgebra::new("Tor").with_note("docs-only link to omega_homology");
        assert_eq!(h.notes.len(), 1);
        assert!(h.validate_shell().is_ok());
    }
}
