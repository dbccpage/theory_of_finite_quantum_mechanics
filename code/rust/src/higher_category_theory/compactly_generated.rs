//! Compactly Generated Categories and Compact Objects.
//!
//! Provides mathematically rigorous foundations for accessible and presentable ∞-categories:
//! - Compact objects K: Hom(K, -) commutes with filtered colimits (finite presentability).
//! - Filtered colimit diagrams and cocones.
//! - Factorization of morphisms K -> colim D through finite stages D(i_0).
//! - Compact generators G: set of compact objects generating the category under filtered colimits.
//! - Coverage verification: every object is a filtered colimit of compact generators.
//!
//! Zero floats. Soviet Builder allocation bounded by `OperationLimits`.
//!
//! AuthorityEffect: None.

use std::collections::{HashMap, HashSet};

use omega_kernel::resource_limits::OperationLimits;
use serde::{Deserialize, Serialize};

use crate::error::{reserve_exact, HigherCategoryError};

/// A compact object K in a compactly generated category.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct CompactObject {
    pub id: String,
    pub is_generator: bool,
}

/// A stage in a filtered diagram.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct DiagramStage {
    pub index: usize,
    pub object_id: String,
    /// Coprojection map ι_i: D(i) -> colim D
    pub coprojection_id: String,
}

/// A filtered diagram D: I -> C with colimit L = colim D.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct FilteredDiagram {
    pub id: String,
    pub colimit_object_id: String,
    pub stages: Vec<DiagramStage>,
}

/// Witness that a morphism f: K -> colim D factors through some finite stage D(i_0):
/// f = ι_{i_0} ∘ g where g: K -> D(i_0).
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct FactorizationWitness {
    pub morphism_id: String,
    pub compact_object_id: String,
    pub diagram_id: String,
    pub stage_index: usize,
    /// The factored morphism g: K -> D(i_0)
    pub factored_morphism_id: String,
}

/// Compactly generated category structure and verification.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct CompactlyGeneratedCategory {
    pub objects: Vec<String>,
    pub compact_generators: HashSet<String>,
    pub diagrams: HashMap<String, FilteredDiagram>,
    pub factorizations: Vec<FactorizationWitness>,
    /// Representation of each general object as a filtered colimit of compact generators
    pub object_presentations: HashMap<String, String>,
}

impl CompactlyGeneratedCategory {
    /// Constructs an empty compactly generated category under `OperationLimits`.
    pub fn new(limits: &OperationLimits) -> Result<Self, HigherCategoryError> {
        let mut objects = Vec::new();
        reserve_exact(&mut objects, 8, limits)?;
        Ok(Self {
            objects,
            compact_generators: HashSet::new(),
            diagrams: HashMap::new(),
            factorizations: Vec::new(),
            object_presentations: HashMap::new(),
        })
    }

    /// Adds an object to the category.
    pub fn add_object(&mut self, id: impl Into<String>, is_generator: bool, limits: &OperationLimits) -> Result<(), HigherCategoryError> {
        let id_str = id.into();
        if self.objects.contains(&id_str) {
            return Err(HigherCategoryError::DuplicateCell { id: id_str });
        }
        reserve_exact(&mut self.objects, 1, limits)?;
        if is_generator {
            self.compact_generators.insert(id_str.clone());
        }
        self.objects.push(id_str);
        Ok(())
    }

    /// Registers a filtered diagram with its colimit object.
    pub fn add_diagram(&mut self, diagram: FilteredDiagram) {
        self.diagrams.insert(diagram.id.clone(), diagram);
    }

    /// Registers a factorization witness for a morphism from a compact object to a colimit.
    pub fn add_factorization_witness(&mut self, witness: FactorizationWitness, limits: &OperationLimits) -> Result<(), HigherCategoryError> {
        reserve_exact(&mut self.factorizations, 1, limits)?;
        self.factorizations.push(witness);
        Ok(())
    }

    /// Declares how an object is presented as a filtered colimit of compact generators.
    pub fn set_object_presentation(&mut self, object_id: &str, diagram_id: &str) -> Result<(), HigherCategoryError> {
        if !self.objects.contains(&object_id.to_string()) {
            return Err(HigherCategoryError::ZeroCellNotFound { id: object_id.to_string() });
        }
        if !self.diagrams.contains_key(diagram_id) {
            return Err(HigherCategoryError::ZeroCellNotFound { id: diagram_id.to_string() });
        }
        self.object_presentations.insert(object_id.to_string(), diagram_id.to_string());
        Ok(())
    }

    /// Verifies that all factorization witnesses are structurally valid:
    /// 1. Morphism IDs are non-empty and well-formed.
    /// 2. The compact object is registered.
    /// 3. The diagram exists, contains the claimed stage index, and stage fields are non-empty.
    pub fn verify_compact_factorizations(&self) -> Result<(), HigherCategoryError> {
        for witness in &self.factorizations {
            if witness.morphism_id.trim().is_empty() || witness.factored_morphism_id.trim().is_empty() {
                return Err(HigherCategoryError::CompactnessViolation {
                    object: witness.compact_object_id.clone(),
                    details: "Factorization witness contains empty morphism_id or factored_morphism_id".to_string(),
                });
            }
            if !self.compact_generators.contains(&witness.compact_object_id) {
                return Err(HigherCategoryError::CompactnessViolation {
                    object: witness.compact_object_id.clone(),
                    details: format!(
                        "Object '{}' is not registered as a compact generator",
                        witness.compact_object_id
                    ),
                });
            }
            let diagram = self.diagrams.get(&witness.diagram_id).ok_or_else(|| {
                HigherCategoryError::CompactnessViolation {
                    object: witness.compact_object_id.clone(),
                    details: format!("Diagram '{}' not found", witness.diagram_id),
                }
            })?;

            let stage = diagram.stages.iter().find(|s| s.index == witness.stage_index).ok_or_else(|| {
                HigherCategoryError::CompactnessViolation {
                    object: witness.compact_object_id.clone(),
                    details: format!(
                        "Diagram '{}' does not contain claimed stage index {}",
                        witness.diagram_id, witness.stage_index
                    ),
                }
            })?;
            if stage.object_id.trim().is_empty() || stage.coprojection_id.trim().is_empty() {
                return Err(HigherCategoryError::CompactnessViolation {
                    object: witness.compact_object_id.clone(),
                    details: format!(
                        "Diagram '{}' stage {} has empty object_id or coprojection_id",
                        witness.diagram_id, stage.index
                    ),
                });
            }
        }
        Ok(())
    }

    /// Verifies that every object in the category is covered by compact generators:
    /// Either the object is itself a compact generator, or it has a valid presentation
    /// as a filtered colimit whose stages consist of compact generators.
    pub fn verify_generator_coverage(&self) -> Result<(), HigherCategoryError> {
        for obj in &self.objects {
            if self.compact_generators.contains(obj) {
                continue;
            }
            let diag_id = match self.object_presentations.get(obj) {
                Some(d) => d,
                None => {
                    return Err(HigherCategoryError::CompactGeneratorCoverageViolation {
                        object: obj.clone(),
                        details: format!("Object '{}' has no filtered colimit presentation and is not a compact generator", obj),
                    });
                }
            };
            let diagram = self.diagrams.get(diag_id).ok_or_else(|| {
                HigherCategoryError::CompactGeneratorCoverageViolation {
                    object: obj.clone(),
                    details: format!("Presenting diagram '{}' not found for object '{}'", diag_id, obj),
                }
            })?;

            // Check that all stages in presenting diagram are compact generators
            for stage in &diagram.stages {
                if !self.compact_generators.contains(&stage.object_id) {
                    return Err(HigherCategoryError::CompactGeneratorCoverageViolation {
                        object: obj.clone(),
                        details: format!(
                            "Presenting diagram '{}' stage {} object '{}' is not a compact generator",
                            diag_id, stage.index, stage.object_id
                        ),
                    });
                }
            }
        }
        Ok(())
    }

    /// Master verification for compactly generated category.
    pub fn validate(&self) -> Result<(), HigherCategoryError> {
        self.verify_compact_factorizations()?;
        self.verify_generator_coverage()?;
        Ok(())
    }
}
