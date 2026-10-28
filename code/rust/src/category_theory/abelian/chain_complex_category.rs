//! chain_complex_category shell for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.
//!
//! Category of chain complexes (bounded or degree-windowed). Degree bounds are
//! shape metadata only. Concrete boundary-law complexes and homology computation
//! live in `omega_homology` (conceptual link in docs comments only).

use serde::{Deserialize, Serialize};
use tfqm_category_theory::errors::ArithmosError;

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
            Some(self.degree_max.abs_diff(self.degree_min))
        } else {
            None
        }
    }

    /// Validate structural emptiness and ordered degree bounds (shell gate).
    pub fn validate_shell(&self) -> Result<(), ArithmosError> {
        if self.label.is_empty() {
            return Err(ArithmosError::InvalidShape("empty label".into()));
        }
        if self.degree_min > self.degree_max {
            return Err(ArithmosError::InvalidShape(format!(
                "degree_min {} > degree_max {}",
                self.degree_min, self.degree_max
            )));
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
        assert_eq!(ChainComplexCategory::new("").validate_shell(),
            Err(ArithmosError::InvalidShape("empty label".into())));
    }

    #[test]
    fn rejects_inverted_bounds() {
        let c = ChainComplexCategory::with_degree_bounds("bad", 3, 1);
        assert_eq!(c.validate_shell(), Err(ArithmosError::InvalidShape("degree_min 3 > degree_max 1".into())));
        assert_eq!(c.degree_span(), None);
    }

    #[test]
    fn degree_span_covers_the_entire_signed_domain() {
        let bounds = [i32::MIN, i32::MIN + 1, -1, 0, 1, i32::MAX - 1, i32::MAX];
        for lower in bounds {
            for upper in bounds {
                let declaration = ChainComplexCategory::with_degree_bounds("window", lower, upper);
                // A widened signed difference is independent of the unsigned
                // abs_diff implementation and fits u32 for ordered i32 bounds.
                let difference = i64::from(upper) - i64::from(lower);
                let expected = u32::try_from(difference).ok();
                assert_eq!(declaration.degree_span(), expected);
                assert_eq!(declaration.validate_shell().is_ok(), lower <= upper);
            }
        }
        assert_eq!(
            ChainComplexCategory::with_degree_bounds("all", i32::MIN, i32::MAX).degree_span(),
            Some(u32::MAX)
        );
    }

    #[test]
    fn notes_append_without_changing_the_degree_window() {
        let original = ChainComplexCategory::with_degree_bounds("window", -3, 4);
        let mut expected = original.clone();
        expected.notes.push("raw declaration only".into());
        assert_eq!(original.with_note("raw declaration only"), expected);
    }
}
