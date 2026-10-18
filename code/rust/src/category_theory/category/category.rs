//! category shell (finite presentation) for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.

use serde::{Deserialize, Serialize};
use std::collections::BTreeMap;

/// Named morphism boundary triple: (source, target, name).
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct MorphismTriple {
    pub source: String,
    pub target: String,
    pub name: String,
}

impl MorphismTriple {
    pub fn new(
        source: impl Into<String>,
        target: impl Into<String>,
        name: impl Into<String>,
    ) -> Self {
        Self {
            source: source.into(),
            target: target.into(),
            name: name.into(),
        }
    }
}

/// Best-effort finite category shell: objects, morphisms, identity keys.
///
/// Composition tables are optional diagnostic notes only — not a law certificate.
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct FiniteCategoryShell {
    pub label: String,
    pub objects: Vec<String>,
    /// Morphisms as (source, target, name) triples.
    pub morphisms: Vec<MorphismTriple>,
    /// object → identity morphism name.
    pub identity_map: BTreeMap<String, String>,
    pub notes: Vec<String>,
}

impl FiniteCategoryShell {
    pub fn new(label: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            objects: Vec::new(),
            morphisms: Vec::new(),
            identity_map: BTreeMap::new(),
            notes: Vec::new(),
        }
    }

    pub fn with_objects(label: impl Into<String>, objects: Vec<String>) -> Self {
        let mut identity_map = BTreeMap::new();
        let mut morphisms = Vec::new();
        for o in &objects {
            let id_name = format!("id_{o}");
            identity_map.insert(o.clone(), id_name.clone());
            morphisms.push(MorphismTriple::new(o.clone(), o.clone(), id_name));
        }
        Self {
            label: label.into(),
            objects,
            morphisms,
            identity_map,
            notes: Vec::new(),
        }
    }

    pub fn validate_shell(&self) -> Result<(), String> {
        if self.label.is_empty() {
            return Err("empty label".into());
        }
        for (i, o) in self.objects.iter().enumerate() {
            if o.is_empty() {
                return Err(format!("empty object tag at index {i}"));
            }
        }
        for (i, m) in self.morphisms.iter().enumerate() {
            if m.source.is_empty() || m.target.is_empty() || m.name.is_empty() {
                return Err(format!("empty morphism field at index {i}"));
            }
        }
        for (obj, id_name) in &self.identity_map {
            if obj.is_empty() || id_name.is_empty() {
                return Err("empty identity_map key or value".into());
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
        assert!(FiniteCategoryShell::new("C").validate_shell().is_ok());
    }

    #[test]
    fn validate_rejects_empty() {
        assert!(FiniteCategoryShell::new("").validate_shell().is_err());
    }

    #[test]
    fn with_objects_ok() {
        let c = FiniteCategoryShell::with_objects("C", vec!["a".into(), "b".into()]);
        assert_eq!(c.objects.len(), 2);
        assert_eq!(c.identity_map.len(), 2);
        assert!(c.validate_shell().is_ok());
    }
}
