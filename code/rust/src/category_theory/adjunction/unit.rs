//! unit (η) shell for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.
//!
//! Natural-transformation-style record for the unit of an adjunction:
//! η : Id_C ⇒ R ∘ L.

use omega_category_theory::errors::ArithmosError;
use serde::{Deserialize, Serialize};
use std::collections::BTreeMap;

/// Best-effort shell for an adjunction unit η : Id ⇒ R∘L.
///
/// Natural-transformation shape: source/target functor labels plus
/// object → component morphism tags. Not a naturality certificate.
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct UnitShell {
    pub label: String,
    /// Source functor label (typically Id_C).
    pub source_functor: String,
    /// Target functor label (typically R∘L).
    pub target_functor: String,
    /// Component map: object tag → morphism tag η_A : A → R(L(A)).
    pub components: BTreeMap<String, String>,
    /// Optional owning adjunction label.
    pub adjunction_ref: String,
    pub notes: Vec<String>,
}

impl UnitShell {
    pub fn new(label: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            source_functor: String::new(),
            target_functor: String::new(),
            components: BTreeMap::new(),
            adjunction_ref: String::new(),
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
            components: BTreeMap::new(),
            adjunction_ref: String::new(),
            notes: Vec::new(),
        }
    }

    pub fn with_component(
        mut self,
        object: impl Into<String>,
        morphism: impl Into<String>,
    ) -> Self {
        self.components.insert(object.into(), morphism.into());
        self
    }

    pub fn set_component(&mut self, object: impl Into<String>, morphism: impl Into<String>) {
        self.components.insert(object.into(), morphism.into());
    }

    pub fn with_adjunction_ref(mut self, adjunction_ref: impl Into<String>) -> Self {
        self.adjunction_ref = adjunction_ref.into();
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
        for (obj, mor) in &self.components {
            if obj.is_empty() || mor.is_empty() {
                return Err(ArithmosError::InvalidShape("empty unit component key or value".into()));
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
        let u = UnitShell::between("η", "Id_C", "R∘L");
        assert!(u.validate_shell().is_ok());
    }

    #[test]
    fn validate_rejects_empty() {
        assert!(UnitShell::new("").validate_shell().is_err());
    }

    #[test]
    fn with_component_ok() {
        let u = UnitShell::between("η", "Id", "RL")
            .with_component("a", "η_a")
            .with_adjunction_ref("free-forget");
        assert_eq!(u.components.len(), 1);
        assert!(u.validate_shell().is_ok());
    }

    #[test]
    fn rejects_empty_component_tags() {
        let mut u = UnitShell::between("η", "Id", "RL");
        u.set_component("", "m");
        assert!(u.validate_shell().is_err());
    }
}
