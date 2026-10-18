//! Stacks, Character Stacks, Stacky Groupoids, Hypercovers, and Derived/Higher Stacks.
//!
//! Unverified metadata schemas associated with:
//! - urn:omega:math:stack:v0.1.0
//! - urn:omega:math:character_stack:v0.1.0
//! - urn:omega:math:stacky_groupoid:v0.1.0
//! - urn:omega:math:hypercover:v0.1.0
//! - urn:omega:math:derived_scheme:v0.1.0
//! - urn:omega:math:derived_stack:v0.1.0
//! - urn:omega:math:higher_stack:v0.1.0
//!
//! AuthorityEffect: None.

use crate::open_set::OpenSet;
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};
use std::collections::BTreeMap;

/// Groupoid object (objects and invertible morphisms).
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct FiniteGroupoid {
    pub objects: Vec<String>,
    /// Morphisms: (source, target, label)
    pub morphisms: Vec<(String, String, String)>,
}

impl FiniteGroupoid {
    pub fn new(objects: Vec<String>, morphisms: Vec<(String, String, String)>) -> Self {
        Self { objects, morphisms }
    }

    pub fn is_isomorphic(&self, obj1: &str, obj2: &str) -> bool {
        self.morphisms
            .iter()
            .any(|(s, t, _)| (s == obj1 && t == obj2) || (s == obj2 && t == obj1))
    }
}

/// A Stack (or 1-stack in groupoids) metadata for `urn:omega:math:stack:v0.1.0`.
///
/// Pseudofunctor F: C^op -> Gpd on a site (C, J) satisfying:
/// 1. Morphism sheaf condition (fully faithful descent).
/// 2. Object gluing condition (essentially surjective descent).
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct Stack {
    pub stack_id: String,
    pub site_id: String,
    /// Object assignment U -> FiniteGroupoid
    pub groupoid_sections: BTreeMap<OpenSet, FiniteGroupoid>,
}

impl Stack {
    pub fn new(stack_id: impl Into<String>, site_id: impl Into<String>) -> Self {
        Self {
            stack_id: stack_id.into(),
            site_id: site_id.into(),
            groupoid_sections: BTreeMap::new(),
        }
    }

    /// Descent cannot be decided without restriction functors and gluing data.
    pub fn is_essentially_surjective(&self, _u: &OpenSet, _cover: &[OpenSet]) -> Option<bool> {
        None
    }

    /// Compute deterministic artifact hash.
    pub fn artifact_hash(&self) -> String {
        let serialized = serde_json::to_vec(&(
            &self.stack_id,
            &self.site_id,
            self.groupoid_sections.iter().collect::<Vec<_>>(),
        ))
        .expect("strings and sequence-encoded finite sections serialize");
        let mut hasher = Sha256::new();
        hasher.update(&serialized);
        format!("{:x}", hasher.finalize())
    }
}

/// A Character Stack Char(Gamma, G) = [Hom(Gamma, G) / G] metadata for `urn:omega:math:character_stack:v0.1.0`.
///
/// Parametrizes representations of fundamental group Gamma into gauge group G up to conjugation action.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct CharacterStack {
    pub stack_id: String,
    pub source_group: String,
    pub gauge_group: String,
    /// Homomorphisms Gamma -> G represented as named mappings
    pub hom_representations: Vec<String>,
    /// Orbits under G-conjugation
    pub conjugation_orbits: Vec<Vec<String>>,
    pub carries_shifted_symplectic_structure: Option<bool>,
}

impl CharacterStack {
    pub fn new(
        stack_id: impl Into<String>,
        source_group: impl Into<String>,
        gauge_group: impl Into<String>,
        hom_representations: Vec<String>,
        conjugation_orbits: Vec<Vec<String>>,
    ) -> Self {
        Self {
            stack_id: stack_id.into(),
            source_group: source_group.into(),
            gauge_group: gauge_group.into(),
            hom_representations,
            conjugation_orbits,
            carries_shifted_symplectic_structure: None,
        }
    }

    pub fn num_conjugacy_classes(&self) -> usize {
        self.conjugation_orbits.len()
    }
}

/// A Stacky Groupoid G_1 => G_0 in Stacks metadata for `urn:omega:math:stacky_groupoid:v0.1.0`.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct StackyGroupoid {
    pub groupoid_id: String,
    pub object_stack: Stack,
    pub morphism_stack: Stack,
}

/// A Hypercover U_bullet -> X in a site metadata for `urn:omega:math:hypercover:v0.1.0`.
///
/// Simplicial object refining coverings at each simplicial level.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct Hypercover {
    pub hypercover_id: String,
    pub base_object: String,
    /// Simplicial levels: level 0 is cover {U_i}, level 1 is pairwise intersections, etc.
    pub levels: Vec<Vec<OpenSet>>,
}

impl Hypercover {
    pub fn new(base_object: impl Into<String>, levels: Vec<Vec<OpenSet>>) -> Self {
        let base_object = base_object.into();
        Self {
            hypercover_id: format!("hypercover_on_{base_object}"),
            base_object,
            levels,
        }
    }

    pub fn truncation_level(&self) -> usize {
        self.levels.len().saturating_sub(1)
    }
}

/// A Derived Scheme (X, O_X) metadata for `urn:omega:math:derived_scheme:v0.1.0`.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct DerivedScheme {
    pub scheme_id: String,
    pub underlying_space: String,
    pub affine_charts: Vec<String>,
    /// Caller declaration only; not a verified mathematical property.
    pub declared_cotangent_complex_perfect: bool,
}

/// A Derived Stack metadata for `urn:omega:math:derived_stack:v0.1.0`.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct DerivedStack {
    pub stack_id: String,
    pub base_category: String,
    pub deformation_theory_cotangent_complex: String,
    /// Caller declaration only; not a verified mathematical property.
    pub declared_satisfies_descent: bool,
}

/// A Higher Stack (n-stack) metadata for `urn:omega:math:higher_stack:v0.1.0`.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct HigherStack {
    pub stack_id: String,
    pub site_id: String,
    pub truncation_level: usize,
    /// Caller declaration only; not a verified mathematical property.
    pub declared_satisfies_higher_descent: bool,
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_character_stack_orbits() {
        let char_stack = CharacterStack::new(
            "char_pi1_su2",
            "Z_2",
            "SU(2)",
            vec!["id".to_string(), "-id".to_string()],
            vec![vec!["id".to_string()], vec!["-id".to_string()]],
        );
        assert_eq!(char_stack.num_conjugacy_classes(), 2);
        assert_eq!(char_stack.carries_shifted_symplectic_structure, None);
    }

    #[test]
    fn test_stack_artifact_hash_deterministic() {
        let s1 = Stack::new("s1", "site1");
        let s2 = Stack::new("s1", "site1");
        assert_eq!(s1.artifact_hash(), s2.artifact_hash());
    }
}
