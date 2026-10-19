//! Agent mapping declarations and literal skill-arrow relabeling. AuthorityEffect: None.
//! FunctorTrait specifies mapping operations without enforcing functor laws.
//! AgentFunctor stores raw configuration and is not an implementation of that trait.
//! map_skill_morphism formats labels and copies declared destination/affiliation tags;
//! it neither admits a source category nor proves identity/composition preservation or authority.

use crate::morphism::SkillMorphism;
use std::fmt::Debug;

pub const FUNCTOR_CONTRACT_ID: &str = "urn:omega:math:functor:v0.1.0";

/// Functor trait mapping object types and morphism types between categories `C` and `D`.
pub trait FunctorTrait<ObjC, ObjD, MorC, MorD>: Debug {
    fn source_category_id(&self) -> &str;
    fn target_category_id(&self) -> &str;
    fn map_object(&self, obj: &ObjC) -> ObjD;
    fn map_morphism(&self, mor: &MorC) -> MorD;
}

/// Raw agent configuration; fields can be changed without admission.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct AgentFunctor {
    pub contract_id: String,
    pub name: String,
    pub source_category_id: String,
    pub target_category_id: String,
    pub primary_role: String,
    pub council_affiliation: String,
    pub supported_skills: Vec<String>,
    pub description: String,
}

impl AgentFunctor {
    pub fn new(
        name: impl Into<String>,
        source_category_id: impl Into<String>,
        target_category_id: impl Into<String>,
        primary_role: impl Into<String>,
        council_affiliation: impl Into<String>,
        supported_skills: Vec<String>,
        description: impl Into<String>,
    ) -> Self {
        Self {
            contract_id: FUNCTOR_CONTRACT_ID.to_string(),
            name: name.into(),
            source_category_id: source_category_id.into(),
            target_category_id: target_category_id.into(),
            primary_role: primary_role.into(),
            council_affiliation: council_affiliation.into(),
            supported_skills,
            description: description.into(),
        }
    }

    /// Relabel a raw arrow and copy declared destination/affiliation metadata.
    pub fn map_skill_morphism(&self, morphism: &SkillMorphism) -> SkillMorphism {
        SkillMorphism {
            contract_id: morphism.contract_id.clone(),
            morphism_id: format!("{}[{}]", self.name, morphism.morphism_id),
            domain_id: format!("{}:{}", self.name, morphism.domain_id),
            codomain_id: format!("{}:{}", self.name, morphism.codomain_id),
            category_id: self.target_category_id.clone(),
            governance_authority: self.council_affiliation.clone(),
            evidence_ceiling: morphism.evidence_ceiling.clone(),
            description: format!(
                "Skill morphism {} lifted by Agent Functor {}",
                morphism.morphism_id, self.name
            ),
        }
    }
}
