//! enriched_functor shell for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.

use serde::{Deserialize, Serialize};
use omega_category_theory::errors::ArithmosError;

/// Best-effort V-enriched functor shell F : C → D.
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct EnrichedFunctor {
    pub label: String,
    /// Domain enriched category shell label.
    pub domain_enriched: String,
    /// Codomain enriched category shell label.
    pub codomain_enriched: String,
    /// Shared base monoidal V label.
    pub base_monoidal_v: String,
    /// Object-map ref.
    pub object_map_ref: String,
    /// Hom-map family ref F_{A,B} : C(A,B) → D(FA,FB) in V.
    pub hom_map_ref: String,
    pub notes: Vec<String>,
}

impl EnrichedFunctor {
    pub fn new(label: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            domain_enriched: String::new(),
            codomain_enriched: String::new(),
            base_monoidal_v: String::new(),
            object_map_ref: String::new(),
            hom_map_ref: String::new(),
            notes: Vec::new(),
        }
    }

    pub fn between(
        label: impl Into<String>,
        domain_enriched: impl Into<String>,
        codomain_enriched: impl Into<String>,
        base_monoidal_v: impl Into<String>,
    ) -> Self {
        Self {
            label: label.into(),
            domain_enriched: domain_enriched.into(),
            codomain_enriched: codomain_enriched.into(),
            base_monoidal_v: base_monoidal_v.into(),
            object_map_ref: String::new(),
            hom_map_ref: String::new(),
            notes: Vec::new(),
        }
    }

    pub fn validate_shell(&self) -> Result<(), ArithmosError> {
        if self.label.is_empty() {
            return Err(ArithmosError::InvalidShape("empty label".into()));
        }
        if self.domain_enriched.is_empty() {
            return Err(ArithmosError::InvalidShape("empty domain_enriched".into()));
        }
        if self.codomain_enriched.is_empty() {
            return Err(ArithmosError::InvalidShape("empty codomain_enriched".into()));
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
        assert!(EnrichedFunctor::between("F", "C", "D", "V")
            .validate_shell()
            .is_ok());
    }

    #[test]
    fn validate_rejects_empty() {
        assert!(EnrichedFunctor::new("").validate_shell().is_err());
    }
}
