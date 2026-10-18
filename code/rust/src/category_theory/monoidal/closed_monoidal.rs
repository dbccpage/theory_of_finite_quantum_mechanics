//! closed_monoidal shell for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.

use serde::{Deserialize, Serialize};

/// Best-effort closed monoidal category shell (internal-hom ref).
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct ClosedMonoidal {
    pub label: String,
    /// Underlying monoidal category shell label.
    pub monoidal_ref: String,
    /// Internal-hom bifunctor / object-family ref [-, -] or ⊸.
    pub internal_hom_ref: String,
    /// Optional evaluation morphism family ref.
    pub evaluation_ref: String,
    pub notes: Vec<String>,
}

impl ClosedMonoidal {
    pub fn new(label: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            monoidal_ref: String::new(),
            internal_hom_ref: String::new(),
            evaluation_ref: String::new(),
            notes: Vec::new(),
        }
    }

    pub fn with_internal_hom(
        label: impl Into<String>,
        monoidal_ref: impl Into<String>,
        internal_hom_ref: impl Into<String>,
    ) -> Self {
        Self {
            label: label.into(),
            monoidal_ref: monoidal_ref.into(),
            internal_hom_ref: internal_hom_ref.into(),
            evaluation_ref: String::new(),
            notes: Vec::new(),
        }
    }

    pub fn validate_shell(&self) -> Result<(), String> {
        if self.label.is_empty() {
            return Err("empty label".into());
        }
        if self.monoidal_ref.is_empty() {
            return Err("empty monoidal_ref".into());
        }
        if self.internal_hom_ref.is_empty() {
            return Err("empty internal_hom_ref".into());
        }
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn validate_ok() {
        assert!(ClosedMonoidal::with_internal_hom("Closed", "Mon", "[-,-]")
            .validate_shell()
            .is_ok());
    }

    #[test]
    fn validate_rejects_empty() {
        assert!(ClosedMonoidal::new("").validate_shell().is_err());
    }
}
