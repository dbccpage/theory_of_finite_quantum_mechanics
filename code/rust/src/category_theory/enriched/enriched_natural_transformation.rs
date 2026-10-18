//! enriched_natural_transformation shell for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.

use serde::{Deserialize, Serialize};

/// Best-effort enriched natural transformation shell α : F ⇒ G.
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct EnrichedNaturalTransformation {
    pub label: String,
    /// Source enriched functor shell label.
    pub source_functor: String,
    /// Target enriched functor shell label.
    pub target_functor: String,
    /// Shared base monoidal V label.
    pub base_monoidal_v: String,
    /// Component family ref α_A : I → D(FA, GA) in V (or equivalent).
    pub components_ref: String,
    pub notes: Vec<String>,
}

impl EnrichedNaturalTransformation {
    pub fn new(label: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            source_functor: String::new(),
            target_functor: String::new(),
            base_monoidal_v: String::new(),
            components_ref: String::new(),
            notes: Vec::new(),
        }
    }

    pub fn between(
        label: impl Into<String>,
        source_functor: impl Into<String>,
        target_functor: impl Into<String>,
        base_monoidal_v: impl Into<String>,
    ) -> Self {
        Self {
            label: label.into(),
            source_functor: source_functor.into(),
            target_functor: target_functor.into(),
            base_monoidal_v: base_monoidal_v.into(),
            components_ref: String::new(),
            notes: Vec::new(),
        }
    }

    pub fn validate_shell(&self) -> Result<(), String> {
        if self.label.is_empty() {
            return Err("empty label".into());
        }
        if self.source_functor.is_empty() {
            return Err("empty source_functor".into());
        }
        if self.target_functor.is_empty() {
            return Err("empty target_functor".into());
        }
        if self.base_monoidal_v.is_empty() {
            return Err("empty base_monoidal_v".into());
        }
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn validate_ok() {
        assert!(
            EnrichedNaturalTransformation::between("alpha", "F", "G", "V")
                .validate_shell()
                .is_ok()
        );
    }

    #[test]
    fn validate_rejects_empty() {
        assert!(EnrichedNaturalTransformation::new("")
            .validate_shell()
            .is_err());
    }
}
