//! arrow_category shell for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.
//!
//! Arr(C): objects are morphisms of C; morphisms are commutative squares.

use serde::{Deserialize, Serialize};

use super::category::MorphismTriple;

/// Best-effort arrow category shell Arr(C).
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct ArrowCategoryShell {
    pub label: String,
    pub base_label: String,
    /// Objects of Arr(C) = morphisms of C (as triples).
    pub arrow_objects: Vec<MorphismTriple>,
    pub notes: Vec<String>,
}

impl ArrowCategoryShell {
    pub fn new(label: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            base_label: String::new(),
            arrow_objects: Vec::new(),
            notes: Vec::new(),
        }
    }

    pub fn of_base(label: impl Into<String>, base_label: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            base_label: base_label.into(),
            arrow_objects: Vec::new(),
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
        for (i, m) in self.arrow_objects.iter().enumerate() {
            if m.source.is_empty() || m.target.is_empty() || m.name.is_empty() {
                return Err(format!("empty arrow_object field at index {i}"));
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
        assert!(ArrowCategoryShell::of_base("Arr(C)", "C")
            .validate_shell()
            .is_ok());
    }

    #[test]
    fn validate_rejects_empty() {
        assert!(ArrowCategoryShell::new("").validate_shell().is_err());
        assert!(ArrowCategoryShell::new("A").validate_shell().is_err());
    }

    #[test]
    fn with_arrow_object_ok() {
        let mut a = ArrowCategoryShell::of_base("Arr(C)", "C");
        a.arrow_objects.push(MorphismTriple::new("x", "y", "f"));
        assert!(a.validate_shell().is_ok());
    }
}
