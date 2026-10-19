//! enriched_adjunction shell for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.

use serde::{Deserialize, Serialize};
use omega_category_theory::errors::ArithmosError;

/// Best-effort enriched adjunction shell F ⊣ G (V-enriched).
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct EnrichedAdjunction {
    pub label: String,
    /// Left adjoint enriched functor shell label.
    pub left_adjoint: String,
    /// Right adjoint enriched functor shell label.
    pub right_adjoint: String,
    /// Shared base monoidal V label.
    pub base_monoidal_v: String,
    /// Hom-isomorphism / unit-counit family ref in V.
    pub hom_iso_ref: String,
    pub notes: Vec<String>,
}

impl EnrichedAdjunction {
    pub fn new(label: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            left_adjoint: String::new(),
            right_adjoint: String::new(),
            base_monoidal_v: String::new(),
            hom_iso_ref: String::new(),
            notes: Vec::new(),
        }
    }

    pub fn with_adjoints(
        label: impl Into<String>,
        left_adjoint: impl Into<String>,
        right_adjoint: impl Into<String>,
        base_monoidal_v: impl Into<String>,
    ) -> Self {
        Self {
            label: label.into(),
            left_adjoint: left_adjoint.into(),
            right_adjoint: right_adjoint.into(),
            base_monoidal_v: base_monoidal_v.into(),
            hom_iso_ref: String::new(),
            notes: Vec::new(),
        }
    }

    pub fn validate_shell(&self) -> Result<(), ArithmosError> {
        if self.label.is_empty() {
            return Err(ArithmosError::InvalidShape("empty label".into()));
        }
        if self.left_adjoint.is_empty() {
            return Err(ArithmosError::InvalidShape("empty left_adjoint".into()));
        }
        if self.right_adjoint.is_empty() {
            return Err(ArithmosError::InvalidShape("empty right_adjoint".into()));
        }
        if self.base_monoidal_v.is_empty() {
            return Err(ArithmosError::InvalidShape("empty base_monoidal_v".into()));
        }
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn validate_ok() {
        assert!(EnrichedAdjunction::with_adjoints("adj", "F", "G", "V")
            .validate_shell()
            .is_ok());
    }

    #[test]
    fn validate_rejects_empty() {
        assert!(EnrichedAdjunction::new("").validate_shell().is_err());
    }
}
