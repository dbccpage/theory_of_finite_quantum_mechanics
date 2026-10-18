//! enriched_category shell for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.

use serde::{Deserialize, Serialize};

/// Hom-object entry: pair of object labels maps to a V-object label.
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct HomObjectEntry {
    pub domain: String,
    pub codomain: String,
    /// Hom-object label in the base monoidal category V.
    pub hom_object: String,
}

/// Best-effort V-enriched category shell.
/// Base monoidal V + hom-objects map; composition/ids are optional refs.
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct EnrichedCategory {
    pub label: String,
    /// Base monoidal category V shell label.
    pub base_monoidal_v: String,
    /// Object labels of C.
    pub objects: Vec<String>,
    /// Hom-objects C(A,B) ∈ Ob(V).
    pub hom_objects: Vec<HomObjectEntry>,
    /// Optional composition morphism family ref in V.
    pub composition_ref: String,
    /// Optional identity morphism family ref j_A : I → C(A,A) in V.
    pub identity_ref: String,
    pub notes: Vec<String>,
}

impl EnrichedCategory {
    pub fn new(label: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            base_monoidal_v: String::new(),
            objects: Vec::new(),
            hom_objects: Vec::new(),
            composition_ref: String::new(),
            identity_ref: String::new(),
            notes: Vec::new(),
        }
    }

    pub fn over_v(label: impl Into<String>, base_monoidal_v: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            base_monoidal_v: base_monoidal_v.into(),
            objects: Vec::new(),
            hom_objects: Vec::new(),
            composition_ref: String::new(),
            identity_ref: String::new(),
            notes: Vec::new(),
        }
    }

    pub fn with_hom(
        &mut self,
        domain: impl Into<String>,
        codomain: impl Into<String>,
        hom_object: impl Into<String>,
    ) {
        self.hom_objects.push(HomObjectEntry {
            domain: domain.into(),
            codomain: codomain.into(),
            hom_object: hom_object.into(),
        });
    }

    pub fn validate_shell(&self) -> Result<(), String> {
        if self.label.is_empty() {
            return Err("empty label".into());
        }
        if self.base_monoidal_v.is_empty() {
            return Err("empty base_monoidal_v".into());
        }
        for (i, o) in self.objects.iter().enumerate() {
            if o.is_empty() {
                return Err(format!("empty object tag at index {i}"));
            }
        }
        for (i, h) in self.hom_objects.iter().enumerate() {
            if h.domain.is_empty() || h.codomain.is_empty() || h.hom_object.is_empty() {
                return Err(format!("empty hom_objects entry at index {i}"));
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
        assert!(EnrichedCategory::over_v("C", "V").validate_shell().is_ok());
    }

    #[test]
    fn validate_rejects_empty() {
        assert!(EnrichedCategory::new("").validate_shell().is_err());
    }
}
