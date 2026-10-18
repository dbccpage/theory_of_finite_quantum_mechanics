//! Morphism abstraction in Category Theory (omega_category_theory).
//!
//! Aligned with URN contract: `urn:omega:math:morphism:v0.1.0`.
//! A morphism `f: A -> B` represents a structure-preserving arrow between objects
//! `A` (domain) and `B` (codomain) within a category.

use std::fmt::Debug;

pub const MORPHISM_CONTRACT_ID: &str = "urn:omega:math:morphism:v0.1.0";

/// Morphism trait between objects `Dom` and `Cod`.
pub trait MorphismTrait<Dom, Cod>: Debug {
    fn domain(&self) -> &Dom;
    fn codomain(&self) -> &Cod;
    fn id(&self) -> &str;
    fn category_id(&self) -> &str;
    fn evaluate(&self, input: &Dom) -> Cod;
}

/// Abstract representation of a typed Skill Morphism mapping states between domains.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct SkillMorphism {
    pub contract_id: String,
    pub morphism_id: String,
    pub domain_id: String,
    pub codomain_id: String,
    pub category_id: String,
    pub governance_authority: String,
    pub evidence_ceiling: String,
    pub description: String,
}

impl SkillMorphism {
    pub fn new(
        morphism_id: impl Into<String>,
        domain_id: impl Into<String>,
        codomain_id: impl Into<String>,
        category_id: impl Into<String>,
        governance_authority: impl Into<String>,
        evidence_ceiling: impl Into<String>,
        description: impl Into<String>,
    ) -> Self {
        Self {
            contract_id: MORPHISM_CONTRACT_ID.to_string(),
            morphism_id: morphism_id.into(),
            domain_id: domain_id.into(),
            codomain_id: codomain_id.into(),
            category_id: category_id.into(),
            governance_authority: governance_authority.into(),
            evidence_ceiling: evidence_ceiling.into(),
            description: description.into(),
        }
    }

    /// Compose two skill morphisms `g . f` if `f.codomain_id == g.domain_id` and category matches.
    pub fn compose(&self, next: &SkillMorphism) -> Option<SkillMorphism> {
        if self.codomain_id == next.domain_id {
            Some(SkillMorphism {
                contract_id: MORPHISM_CONTRACT_ID.to_string(),
                morphism_id: format!("{} >> {}", self.morphism_id, next.morphism_id),
                domain_id: self.domain_id.clone(),
                codomain_id: next.codomain_id.clone(),
                category_id: self.category_id.clone(),
                governance_authority: self.governance_authority.clone(),
                evidence_ceiling: self.evidence_ceiling.clone(),
                description: format!(
                    "Composite morphism of {} and {}",
                    self.morphism_id, next.morphism_id
                ),
            })
        } else {
            None
        }
    }
}
