//! enriched_presheaf shell for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.

use serde::{Deserialize, Serialize};
use omega_category_theory::errors::ArithmosError;

/// Best-effort enriched presheaf shell F : C^op → V (V-enriched).
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct EnrichedPresheaf {
    pub label: String,
    /// Domain enriched category shell label (C).
    pub domain_enriched: String,
    /// Base monoidal / closed V label (codomain of the presheaf).
    pub base_monoidal_v: String,
    /// Object-assignment ref (A ↦ FA ∈ Ob(V)).
    pub object_map_ref: String,
    /// Action / restriction family ref.
    pub action_ref: String,
    pub notes: Vec<String>,
}

impl EnrichedPresheaf {
    pub fn new(label: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            domain_enriched: String::new(),
            base_monoidal_v: String::new(),
            object_map_ref: String::new(),
            action_ref: String::new(),
            notes: Vec::new(),
        }
    }

    pub fn on(
        label: impl Into<String>,
        domain_enriched: impl Into<String>,
        base_monoidal_v: impl Into<String>,
    ) -> Self {
        Self {
            label: label.into(),
            domain_enriched: domain_enriched.into(),
            base_monoidal_v: base_monoidal_v.into(),
            object_map_ref: String::new(),
            action_ref: String::new(),
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
        assert!(EnrichedPresheaf::on("P", "C", "V").validate_shell().is_ok());
    }

    #[test]
    fn validate_rejects_empty() {
        assert!(EnrichedPresheaf::new("").validate_shell().is_err());
    }
}
