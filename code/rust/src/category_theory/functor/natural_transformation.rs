//! natural_transformation shell for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.
//!
//! Natural transformation η : F ⇒ G as a labeled finite record (shape only).

use tfqm_category_theory::errors::ArithmosError;
use serde::{Deserialize, Serialize};

/// Best-effort shell for a natural transformation between labeled functors.
///
/// `components` are diagnostic (object, morphism) pairs, not naturality certificates.
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct NaturalTransformation {
    pub label: String,
    pub source_functor: String,
    pub target_functor: String,
    /// Component map as (object, morphism) pairs: η_A : F(A) → G(A).
    pub components: Vec<(String, String)>,
    pub notes: Vec<String>,
}

impl NaturalTransformation {
    pub fn new(label: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            source_functor: String::new(),
            target_functor: String::new(),
            components: Vec::new(),
            notes: Vec::new(),
        }
    }

    pub fn between(
        label: impl Into<String>,
        source_functor: impl Into<String>,
        target_functor: impl Into<String>,
    ) -> Self {
        Self {
            label: label.into(),
            source_functor: source_functor.into(),
            target_functor: target_functor.into(),
            components: Vec::new(),
            notes: Vec::new(),
        }
    }

    pub fn with_components(mut self, components: Vec<(String, String)>) -> Self {
        self.components = components;
        self
    }

    pub fn validate_shell(&self) -> Result<(), ArithmosError> {
        if self.label.is_empty() {
            return Err(ArithmosError::InvalidShape("empty label".into()));
        }
        if self.source_functor.is_empty() {
            return Err(ArithmosError::InvalidShape("empty source_functor".into()));
        }
        if self.target_functor.is_empty() {
            return Err(ArithmosError::InvalidShape("empty target_functor".into()));
        }
        for (i, (obj, mor)) in self.components.iter().enumerate() {
            if obj.is_empty() || mor.is_empty() {
                return Err(ArithmosError::InvalidShape(format!("empty component tag at index {i}")));
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
        assert!(NaturalTransformation::between("eta", "F", "G")
            .validate_shell()
            .is_ok());
    }

    #[test]
    fn validate_rejects_empty() {
        assert!(NaturalTransformation::new("").validate_shell().is_err());
    }

    #[test]
    fn validate_rejects_missing_functors() {
        assert!(NaturalTransformation::new("eta").validate_shell().is_err());
    }

    #[test]
    fn with_components_ok() {
        let n = NaturalTransformation::between("eta", "F", "G")
            .with_components(vec![("A".into(), "eta_A".into())]);
        assert_eq!(n.components.len(), 1);
        assert!(n.validate_shell().is_ok());
    }

    #[test]
    fn rejects_empty_component_tag() {
        let n = NaturalTransformation::between("eta", "F", "G")
            .with_components(vec![("A".into(), "".into())]);
        assert!(n.validate_shell().is_err());
    }
}
