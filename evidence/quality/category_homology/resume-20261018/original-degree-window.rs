//! chain_complex_category shell for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.
//!
//! Category of chain complexes (bounded or degree-windowed). Degree bounds are
//! shape metadata only. Concrete boundary-law complexes and homology computation
//! live in `omega_homology` (conceptual link in docs comments only).

use serde::{Deserialize, Serialize};

/// Best-effort shell for Ch(A) / Kom(A) with optional degree window.
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct ChainComplexCategory {
    pub label: String,
    /// Inclusive lower degree bound for complexes in this shell.
    pub degree_min: i32,
    /// Inclusive upper degree bound for complexes in this shell.
    pub degree_max: i32,
    pub notes: Vec<String>,
}

impl ChainComplexCategory {
    pub fn new(label: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            degree_min: 0,
            degree_max: 0,
            notes: Vec::new(),
        }
    }

    pub fn with_degree_bounds(label: impl Into<String>, degree_min: i32, degree_max: i32) -> Self {
        Self {
            label: label.into(),
            degree_min,
            degree_max,
            notes: Vec::new(),
        }
    }

    pub fn with_note(mut self, note: impl Into<String>) -> Self {
        self.notes.push(note.into());
        self
    }

    /// Span of the declared degree window (non-negative when bounds are ordered).
    pub fn degree_span(&self) -> Option<u32> {
        if self.degree_min <= self.degree_max {
            Some((self.degree_max - self.degree_min) as u32)
        } else {
            None
        }
    }

    /// Validate structural emptiness and ordered degree bounds (shell gate).
    pub fn validate_shell(&self) -> Result<(), String> {
        if self.label.is_empty() {
            return Err("empty label".into());
        }
        if self.degree_min > self.degree_max {
            return Err(format!(
                "degree_min {} > degree_max {}",
                self.degree_min, self.degree_max
            ));
        }
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn validate_ok() {
        let c = ChainComplexCategory::with_degree_bounds("Ch(Ab)", 0, 2);
        assert!(c.validate_shell().is_ok());
        assert_eq!(c.degree_span(), Some(2));
    }

    #[test]
    fn validate_rejects_empty() {
        assert!(ChainComplexCategory::new("").validate_shell().is_err());
    }

    #[test]
    fn rejects_inverted_bounds() {
        let c = ChainComplexCategory::with_degree_bounds("bad", 3, 1);
        assert!(c.validate_shell().is_err());
        assert_eq!(c.degree_span(), None);
    }
}
