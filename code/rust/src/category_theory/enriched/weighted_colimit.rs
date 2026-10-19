//! weighted_colimit shell for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.

use serde::{Deserialize, Serialize};
use omega_category_theory::errors::ArithmosError;

/// Best-effort weighted colimit shell W ★ D in a V-enriched setting.
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct WeightedColimit {
    pub label: String,
    /// Weight enriched functor W : J^op → V (or appropriate variance).
    pub weight_ref: String,
    /// Diagram enriched functor D : J → C ref.
    pub diagram_ref: String,
    /// Ambient enriched category shell label.
    pub ambient_enriched: String,
    /// Base monoidal V label.
    pub base_monoidal_v: String,
    /// Apex / colimit object label (if claimed).
    pub apex: String,
    pub notes: Vec<String>,
}

impl WeightedColimit {
    pub fn new(label: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            weight_ref: String::new(),
            diagram_ref: String::new(),
            ambient_enriched: String::new(),
            base_monoidal_v: String::new(),
            apex: String::new(),
            notes: Vec::new(),
        }
    }

    pub fn of(
        label: impl Into<String>,
        weight_ref: impl Into<String>,
        diagram_ref: impl Into<String>,
        ambient_enriched: impl Into<String>,
        base_monoidal_v: impl Into<String>,
    ) -> Self {
        Self {
            label: label.into(),
            weight_ref: weight_ref.into(),
            diagram_ref: diagram_ref.into(),
            ambient_enriched: ambient_enriched.into(),
            base_monoidal_v: base_monoidal_v.into(),
            apex: String::new(),
            notes: Vec::new(),
        }
    }

    pub fn validate_shell(&self) -> Result<(), ArithmosError> {
        if self.label.is_empty() {
            return Err(ArithmosError::InvalidShape("empty label".into()));
        }
        if self.weight_ref.is_empty() {
            return Err(ArithmosError::InvalidShape("empty weight_ref".into()));
        }
        if self.diagram_ref.is_empty() {
            return Err(ArithmosError::InvalidShape("empty diagram_ref".into()));
        }
        if self.ambient_enriched.is_empty() {
            return Err(ArithmosError::InvalidShape("empty ambient_enriched".into()));
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
        assert!(WeightedColimit::of("wcolim", "W", "D", "C", "V")
            .validate_shell()
            .is_ok());
    }

    #[test]
    fn validate_rejects_empty() {
        assert!(WeightedColimit::new("").validate_shell().is_err());
    }
}
