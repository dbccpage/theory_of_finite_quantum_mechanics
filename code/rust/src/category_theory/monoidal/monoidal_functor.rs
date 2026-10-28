//! monoidal_functor shell for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.

use serde::{Deserialize, Serialize};
use tfqm_category_theory::errors::ArithmosError;

/// Best-effort monoidal functor shell F : C → D with strength data refs.
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct MonoidalFunctor {
    pub label: String,
    /// Domain monoidal category shell label.
    pub domain_monoidal: String,
    /// Codomain monoidal category shell label.
    pub codomain_monoidal: String,
    /// Underlying ordinary functor ref.
    pub functor_ref: String,
    /// Tensorator / strength μ : F(A) ⊗ F(B) → F(A ⊗ B) ref.
    pub tensorator_ref: String,
    /// Unit comparison ε : I_D → F(I_C) ref.
    pub unit_comparison_ref: String,
    /// True if strong monoidal is claimed (diagnostic only).
    pub strong_claimed: bool,
    pub notes: Vec<String>,
}

impl MonoidalFunctor {
    pub fn new(label: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            domain_monoidal: String::new(),
            codomain_monoidal: String::new(),
            functor_ref: String::new(),
            tensorator_ref: String::new(),
            unit_comparison_ref: String::new(),
            strong_claimed: false,
            notes: Vec::new(),
        }
    }

    pub fn between(
        label: impl Into<String>,
        domain_monoidal: impl Into<String>,
        codomain_monoidal: impl Into<String>,
        functor_ref: impl Into<String>,
    ) -> Self {
        Self {
            label: label.into(),
            domain_monoidal: domain_monoidal.into(),
            codomain_monoidal: codomain_monoidal.into(),
            functor_ref: functor_ref.into(),
            tensorator_ref: String::new(),
            unit_comparison_ref: String::new(),
            strong_claimed: false,
            notes: Vec::new(),
        }
    }

    pub fn validate_shell(&self) -> Result<(), ArithmosError> {
        if self.label.is_empty() {
            return Err(ArithmosError::InvalidShape("empty label".into()));
        }
        if self.domain_monoidal.is_empty() {
            return Err(ArithmosError::InvalidShape("empty domain_monoidal".into()));
        }
        if self.codomain_monoidal.is_empty() {
            return Err(ArithmosError::InvalidShape("empty codomain_monoidal".into()));
        }
        if self.functor_ref.is_empty() {
            return Err(ArithmosError::InvalidShape("empty functor_ref".into()));
        }
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn validate_ok() {
        assert!(MonoidalFunctor::between("F", "C", "D", "F0")
            .validate_shell()
            .is_ok());
    }

    #[test]
    fn validate_rejects_empty() {
        assert!(MonoidalFunctor::new("").validate_shell().is_err());
    }
}
