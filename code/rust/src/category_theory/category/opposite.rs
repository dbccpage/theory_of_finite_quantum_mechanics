//! opposite category shell for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.
//!
//! C^op has the same objects; morphisms reverse (source ↔ target).

use serde::{Deserialize, Serialize};

use super::category::MorphismTriple;

/// Best-effort opposite-category shell wrapping a base label.
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct OppositeCategoryShell {
    pub label: String,
    /// Label of the base category C (so this shell is C^op).
    pub base_label: String,
    /// Reversed morphism pairs: each triple is stored already reversed
    /// (source, target, name) relative to the base orientation.
    pub reversed_morphisms: Vec<MorphismTriple>,
    pub notes: Vec<String>,
}

impl OppositeCategoryShell {
    pub fn new(label: impl Into<String>, base_label: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            base_label: base_label.into(),
            reversed_morphisms: Vec::new(),
            notes: Vec::new(),
        }
    }

    /// Reverse a base morphism (src, dst, name) → (dst, src, name) for C^op.
    pub fn reverse_of(
        label: impl Into<String>,
        base_label: impl Into<String>,
        base_morphisms: Vec<MorphismTriple>,
    ) -> Self {
        let reversed_morphisms = base_morphisms
            .into_iter()
            .map(|m| MorphismTriple::new(m.target, m.source, m.name))
            .collect();
        Self {
            label: label.into(),
            base_label: base_label.into(),
            reversed_morphisms,
            notes: Vec::new(),
        }
    }

    pub fn validate_shell(&self) -> Result<(), String> {
        if self.label.is_empty() {
            return Err("empty label".into());
        }
        if self.base_label.is_empty() {
            return Err("empty base_label".into());
        }
        for (i, m) in self.reversed_morphisms.iter().enumerate() {
            if m.source.is_empty() || m.target.is_empty() || m.name.is_empty() {
                return Err(format!("empty reversed morphism field at index {i}"));
            }
        }
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn validate_ok() {
        assert!(OppositeCategoryShell::new("C^op", "C")
            .validate_shell()
            .is_ok());
    }

    #[test]
    fn validate_rejects_empty() {
        assert!(OppositeCategoryShell::new("", "C")
            .validate_shell()
            .is_err());
        assert!(OppositeCategoryShell::new("Cop", "")
            .validate_shell()
            .is_err());
    }

    #[test]
    fn reverse_of_swaps_endpoints() {
        let base = vec![MorphismTriple::new("a", "b", "f")];
        let op = OppositeCategoryShell::reverse_of("C^op", "C", base);
        assert_eq!(op.reversed_morphisms[0].source, "b");
        assert_eq!(op.reversed_morphisms[0].target, "a");
        assert!(op.validate_shell().is_ok());
    }
}
