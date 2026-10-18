//! set shell for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.

use serde::{Deserialize, Serialize};

/// Best-effort shell for a labeled set (elements as string tags).
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct Set {
    pub label: String,
    /// Element tags (not a formal carrier; diagnostic inventory only).
    pub elements: Vec<String>,
    pub notes: Vec<String>,
}

impl Set {
    pub fn new(label: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            elements: Vec::new(),
            notes: Vec::new(),
        }
    }

    pub fn with_elements(label: impl Into<String>, elements: Vec<String>) -> Self {
        Self {
            label: label.into(),
            elements,
            notes: Vec::new(),
        }
    }

    pub fn cardinality(&self) -> usize {
        self.elements.len()
    }

    pub fn validate_shell(&self) -> Result<(), String> {
        if self.label.is_empty() {
            return Err("empty label".into());
        }
        for (i, e) in self.elements.iter().enumerate() {
            if e.is_empty() {
                return Err(format!("empty element tag at index {i}"));
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
        assert!(Set::new("x").validate_shell().is_ok());
    }

    #[test]
    fn validate_rejects_empty() {
        assert!(Set::new("").validate_shell().is_err());
    }

    #[test]
    fn with_elements_cardinality() {
        let s = Set::with_elements("S", vec!["a".into(), "b".into()]);
        assert_eq!(s.cardinality(), 2);
        assert!(s.validate_shell().is_ok());
    }

    #[test]
    fn rejects_empty_element_tag() {
        let s = Set::with_elements("S", vec!["a".into(), "".into()]);
        assert!(s.validate_shell().is_err());
    }
}
