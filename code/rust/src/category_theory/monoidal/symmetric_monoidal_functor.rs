//! symmetric_monoidal_functor shell for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.

use serde::{Deserialize, Serialize};

/// Best-effort symmetric monoidal functor shell.
/// Monoidal functor that preserves braiding (symmetry) up to claimed coherence.
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct SymmetricMonoidalFunctor {
    pub label: String,
    /// Domain symmetric monoidal category shell label.
    pub domain_symmetric: String,
    /// Codomain symmetric monoidal category shell label.
    pub codomain_symmetric: String,
    /// Underlying monoidal functor shell label.
    pub monoidal_functor_ref: String,
    /// Braiding-preservation witness / coherence ref.
    pub braiding_preservation_ref: String,
    pub notes: Vec<String>,
}

impl SymmetricMonoidalFunctor {
    pub fn new(label: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            domain_symmetric: String::new(),
            codomain_symmetric: String::new(),
            monoidal_functor_ref: String::new(),
            braiding_preservation_ref: String::new(),
            notes: Vec::new(),
        }
    }

    pub fn between(
        label: impl Into<String>,
        domain_symmetric: impl Into<String>,
        codomain_symmetric: impl Into<String>,
        monoidal_functor_ref: impl Into<String>,
    ) -> Self {
        Self {
            label: label.into(),
            domain_symmetric: domain_symmetric.into(),
            codomain_symmetric: codomain_symmetric.into(),
            monoidal_functor_ref: monoidal_functor_ref.into(),
            braiding_preservation_ref: String::new(),
            notes: Vec::new(),
        }
    }

    pub fn validate_shell(&self) -> Result<(), String> {
        if self.label.is_empty() {
            return Err("empty label".into());
        }
        if self.domain_symmetric.is_empty() {
            return Err("empty domain_symmetric".into());
        }
        if self.codomain_symmetric.is_empty() {
            return Err("empty codomain_symmetric".into());
        }
        if self.monoidal_functor_ref.is_empty() {
            return Err("empty monoidal_functor_ref".into());
        }
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn validate_ok() {
        assert!(SymmetricMonoidalFunctor::between("SF", "C", "D", "F")
            .validate_shell()
            .is_ok());
    }

    #[test]
    fn validate_rejects_empty() {
        assert!(SymmetricMonoidalFunctor::new("").validate_shell().is_err());
    }
}
