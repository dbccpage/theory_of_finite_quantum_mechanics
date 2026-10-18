//! counit (ε) shell for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.
//!
//! Natural-transformation-style record for the counit of an adjunction:
//! ε : L ∘ R ⇒ Id_D.

use serde::{Deserialize, Serialize};
use std::collections::BTreeMap;

/// Best-effort shell for an adjunction counit ε : L∘R ⇒ Id.
///
/// Natural-transformation shape: source/target functor labels plus
/// object → component morphism tags. Not a naturality certificate.
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct CounitShell {
    pub label: String,
    /// Source functor label (typically L∘R).
    pub source_functor: String,
    /// Target functor label (typically Id_D).
    pub target_functor: String,
    /// Component map: object tag → morphism tag ε_B : L(R(B)) → B.
    pub components: BTreeMap<String, String>,
    /// Optional owning adjunction label.
    pub adjunction_ref: String,
    pub notes: Vec<String>,
}

impl CounitShell {
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
        for (obj, mor) in &self.components {
            if obj.is_empty() || mor.is_empty() {
                return Err("empty counit component key or value".into());
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
        let c = CounitShell::between("ε", "L∘R", "Id_D");
        assert!(c.validate_shell().is_ok());
    }

    #[test]
    fn validate_rejects_empty() {
        assert!(CounitShell::new("").validate_shell().is_err());
    }

    #[test]
    fn with_component_ok() {
        let c = CounitShell::between("ε", "LR", "Id")
            .with_component("b", "ε_b")
            .with_adjunction_ref("free-forget");
        assert_eq!(c.components.len(), 1);
        assert!(c.validate_shell().is_ok());
    }

    #[test]
    fn rejects_empty_component_tags() {
        let mut c = CounitShell::between("ε", "LR", "Id");
        c.set_component("b", "");
        assert!(c.validate_shell().is_err());
    }
}
