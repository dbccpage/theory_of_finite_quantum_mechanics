//! Shared finite category declarations.
//!
//! This module is the canonical finite category data model for the functor
//! core.  It keeps declarations explicit and auditable, while
//! `ValidatedFiniteCategory` marks data that has passed the finite category
//! law checks.

use super::cat_functor::Category;
use std::collections::{BTreeMap, BTreeSet};

/// Composition table convention:
/// compositions[(f, g)] = g composed after f.
pub type CompositionTable = BTreeMap<(String, String), String>;

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DeclaredMorphism {
    pub name: String,
    pub source: String,
    pub target: String,
}

impl DeclaredMorphism {
    pub fn new(name: &str, source: &str, target: &str) -> Self {
        Self {
            name: name.into(),
            source: source.into(),
            target: target.into(),
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DeclaredFiniteCategory {
    pub name: String,
    pub objects: BTreeSet<String>,
    pub morphisms: BTreeMap<String, DeclaredMorphism>,
    pub identities: BTreeMap<String, String>,
    pub compositions: CompositionTable,
}

impl DeclaredFiniteCategory {
    pub fn new(name: &str) -> Self {
        Self {
            name: name.into(),
            objects: BTreeSet::new(),
            morphisms: BTreeMap::new(),
            identities: BTreeMap::new(),
            compositions: BTreeMap::new(),
        }
    }

    pub fn add_object(&mut self, object: &str) {
        self.objects.insert(object.into());
    }

    pub fn add_morphism(&mut self, name: &str, source: &str, target: &str) {
        self.objects.insert(source.into());
        self.objects.insert(target.into());
        self.morphisms
            .insert(name.into(), DeclaredMorphism::new(name, source, target));
    }

    pub fn set_identity(&mut self, object: &str, morphism: &str) {
        self.objects.insert(object.into());
        self.identities.insert(object.into(), morphism.into());
    }

    pub fn add_identity(&mut self, object: &str, morphism: &str) {
        self.add_morphism(morphism, object, object);
        self.set_identity(object, morphism);
    }

    pub fn set_composition(&mut self, first: &str, second: &str, composite: &str) {
        self.compositions
            .insert((first.into(), second.into()), composite.into());
    }

    pub fn identity_of(&self, object: &str) -> Option<&str> {
        self.identities.get(object).map(|id| id.as_str())
    }

    pub fn boundary_of(&self, morphism: &str) -> Option<(&str, &str)> {
        self.morphisms
            .get(morphism)
            .map(|mor| (mor.source.as_str(), mor.target.as_str()))
    }

    /// Returns g ∘ f (first `f`, then `g`).
    pub fn compose(&self, f: &str, g: &str) -> Option<&str> {
        self.compositions
            .get(&(f.into(), g.into()))
            .map(|composite| composite.as_str())
    }

    pub fn has_object(&self, object: &str) -> bool {
        self.objects.contains(object)
    }

    pub fn has_morphism(&self, morphism: &str) -> bool {
        self.morphisms.contains_key(morphism)
    }

    pub fn object_names(&self) -> Vec<&str> {
        self.objects.iter().map(|object| object.as_str()).collect()
    }

    pub fn morphism_names(&self) -> Vec<&str> {
        self.morphisms
            .keys()
            .map(|morphism| morphism.as_str())
            .collect()
    }

    pub fn boundary_triples(&self) -> Vec<(String, String, String)> {
        self.morphisms
            .values()
            .map(|morphism| {
                (
                    morphism.name.clone(),
                    morphism.source.clone(),
                    morphism.target.clone(),
                )
            })
            .collect()
    }

    pub fn composition_triples(&self) -> Vec<(String, String, String)> {
        self.compositions
            .iter()
            .map(|((first, second), composite)| (first.clone(), second.clone(), composite.clone()))
            .collect()
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ValidatedFiniteCategory {
    declared: DeclaredFiniteCategory,
}

impl ValidatedFiniteCategory {
    pub fn try_new(
        declared: DeclaredFiniteCategory,
    ) -> Result<Self, super::validation::ValidationReport> {
        let report = super::finite_category_validation::validate_finite_category(&declared);
        if report.all_passed() {
            Ok(Self { declared })
        } else {
            Err(report)
        }
    }

    pub fn declared(&self) -> &DeclaredFiniteCategory {
        &self.declared
    }

    pub fn into_declared(self) -> DeclaredFiniteCategory {
        self.declared
    }
}

impl Category for ValidatedFiniteCategory {
    type Ob = String;
    type Mor = String;

    fn id(&self, x: &Self::Ob) -> Option<Self::Mor> {
        self.declared.identity_of(x).map(str::to_string)
    }

    fn src(&self, f: &Self::Mor) -> Option<Self::Ob> {
        self.declared
            .boundary_of(f)
            .map(|(source, _)| source.to_string())
    }

    fn tgt(&self, f: &Self::Mor) -> Option<Self::Ob> {
        self.declared
            .boundary_of(f)
            .map(|(_, target)| target.to_string())
    }

    fn compose(&self, f: &Self::Mor, g: &Self::Mor) -> Option<Self::Mor> {
        self.declared
            .compose(f, g)
            .map(|composite| composite.into())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn walking_arrow() -> DeclaredFiniteCategory {
        let mut cat = DeclaredFiniteCategory::new("WalkingArrow");
        cat.add_morphism("id_A", "A", "A");
        cat.add_morphism("id_B", "B", "B");
        cat.add_morphism("f", "A", "B");
        cat.set_identity("A", "id_A");
        cat.set_identity("B", "id_B");
        cat.set_composition("id_A", "id_A", "id_A");
        cat.set_composition("id_B", "id_B", "id_B");
        cat.set_composition("id_A", "f", "f");
        cat.set_composition("f", "id_B", "f");
        cat
    }

    #[test]
    fn validated_category_implements_category_trait() {
        let cat = ValidatedFiniteCategory::try_new(walking_arrow())
            .expect("walking arrow should validate");

        assert_eq!(cat.id(&"A".into()), Some("id_A".into()));
        assert_eq!(cat.src(&"f".into()), Some("A".into()));
        assert_eq!(cat.tgt(&"f".into()), Some("B".into()));
        assert_eq!(cat.compose(&"id_A".into(), &"f".into()), Some("f".into()));
    }

    #[test]
    fn try_new_refuses_object_without_identity() {
        let mut cat = DeclaredFiniteCategory::new("Broken");
        cat.add_object("A");
        let err = ValidatedFiniteCategory::try_new(cat)
            .expect_err("an object with no identity is not a category");
        assert!(err.typed_violations.iter().any(|violation| {
            violation.unit
                == crate::validation::ValidationUnit::FiniteCategory(
                    crate::validation::FiniteCategoryValidation::IdentityTotality,
                )
        }));
    }
}
