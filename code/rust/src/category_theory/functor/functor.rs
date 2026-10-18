//! functor shell for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.
//!
//! Covariant functor F : C → D as a labeled finite record (shape only).

use serde::{Deserialize, Serialize};

/// Best-effort shell for a labeled functor between labeled categories.
///
/// `object_map` / `morphism_map` are diagnostic pair lists, not law certificates.
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct Functor {
    pub label: String,
    pub source_category: String,
    pub target_category: String,
    /// Object map as (source_object, target_object) pairs.
    pub object_map: Vec<(String, String)>,
    /// Morphism map as (source_morphism, target_morphism) pairs.
    pub morphism_map: Vec<(String, String)>,
    pub notes: Vec<String>,
}

impl Functor {
    pub fn new(label: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            source_category: String::new(),
            target_category: String::new(),
            object_map: Vec::new(),
            morphism_map: Vec::new(),
            notes: Vec::new(),
        }
    }

    pub fn between(
        label: impl Into<String>,
        source_category: impl Into<String>,
        target_category: impl Into<String>,
    ) -> Self {
        Self {
            label: label.into(),
            source_category: source_category.into(),
            target_category: target_category.into(),
            object_map: Vec::new(),
            morphism_map: Vec::new(),
            notes: Vec::new(),
        }
    }

    pub fn with_object_map(mut self, object_map: Vec<(String, String)>) -> Self {
        self.object_map = object_map;
        self
    }

    pub fn with_morphism_map(mut self, morphism_map: Vec<(String, String)>) -> Self {
        self.morphism_map = morphism_map;
        self
    }

    pub fn validate_shell(&self) -> Result<(), String> {
        if self.label.is_empty() {
            return Err("empty label".into());
        }
        if self.source_category.is_empty() {
            return Err("empty source_category".into());
        }
        if self.target_category.is_empty() {
            return Err("empty target_category".into());
        }
        for (i, (a, b)) in self.object_map.iter().enumerate() {
            if a.is_empty() || b.is_empty() {
                return Err(format!("empty object_map tag at index {i}"));
            }
        }
        for (i, (a, b)) in self.morphism_map.iter().enumerate() {
            if a.is_empty() || b.is_empty() {
                return Err(format!("empty morphism_map tag at index {i}"));
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
        assert!(Functor::between("F", "C", "D").validate_shell().is_ok());
    }

    #[test]
    fn validate_rejects_empty() {
        assert!(Functor::new("").validate_shell().is_err());
    }

    #[test]
    fn validate_rejects_missing_source() {
        let f = Functor::new("F");
        assert!(f.validate_shell().is_err());
    }

    #[test]
    fn with_maps_ok() {
        let f = Functor::between("F", "C", "D")
            .with_object_map(vec![("a".into(), "Fa".into())])
            .with_morphism_map(vec![("f".into(), "Ff".into())]);
        assert_eq!(f.object_map.len(), 1);
        assert_eq!(f.morphism_map.len(), 1);
        assert!(f.validate_shell().is_ok());
    }

    #[test]
    fn rejects_empty_map_tag() {
        let f = Functor::between("F", "C", "D").with_object_map(vec![("a".into(), "".into())]);
        assert!(f.validate_shell().is_err());
    }
}
