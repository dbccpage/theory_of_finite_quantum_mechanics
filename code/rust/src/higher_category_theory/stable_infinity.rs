
use std::collections::HashMap;

use engine_kernel::resource_limits::OperationLimits;
use serde::{Deserialize, Serialize};

use crate::error::{reserve_exact, HigherCategoryError};

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct PointedObject {
    pub id: String,
    pub is_zero: bool,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct PointedMorphism {
    pub id: String,
    pub source: String,
    pub target: String,
    pub is_zero_morphism: bool,
    pub is_equivalence: bool,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct FiberSequence {
    pub fiber: String,
    pub total: String,
    pub base: String,
    pub inclusion_map: String,
    pub projection_map: String,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct SpectrumLevel {
    pub level: usize,
    pub space_id: String,
    pub structure_map_id: String,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct StableInfinityCategory {
    pub objects: Vec<PointedObject>,
    pub morphisms: Vec<PointedMorphism>,
    pub zero_object_id: String,
    pub suspension_objects: HashMap<String, String>,
    pub loop_objects: HashMap<String, String>,
    pub unit_morphisms: HashMap<String, String>,
    pub counit_morphisms: HashMap<String, String>,
    pub fiber_sequences: Vec<FiberSequence>,
    pub spectra: HashMap<String, Vec<SpectrumLevel>>,
}

impl StableInfinityCategory {
    pub fn new(zero_object: impl Into<String>, limits: &OperationLimits) -> Result<Self, HigherCategoryError> {
        let zero_id = zero_object.into();
        let mut objects = Vec::new();
        reserve_exact(&mut objects, 8, limits)?;
        objects.push(PointedObject {
            id: zero_id.clone(),
            is_zero: true,
        });

        let mut morphisms = Vec::new();
        reserve_exact(&mut morphisms, 16, limits)?;

        Ok(Self {
            objects,
            morphisms,
            zero_object_id: zero_id,
            suspension_objects: HashMap::new(),
            loop_objects: HashMap::new(),
            unit_morphisms: HashMap::new(),
            counit_morphisms: HashMap::new(),
            fiber_sequences: Vec::new(),
            spectra: HashMap::new(),
        })
    }

    pub fn add_object(&mut self, id: impl Into<String>, limits: &OperationLimits) -> Result<(), HigherCategoryError> {
        let id_str = id.into();
        if self.objects.iter().any(|o| o.id == id_str) {
            return Err(HigherCategoryError::DuplicateCell { id: id_str });
        }
        reserve_exact(&mut self.objects, 1, limits)?;
        self.objects.push(PointedObject {
            id: id_str,
            is_zero: false,
        });
        Ok(())
    }

    pub fn add_morphism(
        &mut self,
        id: impl Into<String>,
        source: impl Into<String>,
        target: impl Into<String>,
        is_zero_morphism: bool,
        is_equivalence: bool,
        limits: &OperationLimits,
    ) -> Result<(), HigherCategoryError> {
        let id_str = id.into();
        let src_str = source.into();
        let tgt_str = target.into();

        if !self.objects.iter().any(|o| o.id == src_str) {
            return Err(HigherCategoryError::ZeroCellNotFound { id: src_str });
        }
        if !self.objects.iter().any(|o| o.id == tgt_str) {
            return Err(HigherCategoryError::ZeroCellNotFound { id: tgt_str });
        }
        if self.morphisms.iter().any(|m| m.id == id_str) {
            return Err(HigherCategoryError::DuplicateCell { id: id_str });
        }

        reserve_exact(&mut self.morphisms, 1, limits)?;
        self.morphisms.push(PointedMorphism {
            id: id_str,
            source: src_str,
            target: tgt_str,
            is_zero_morphism,
            is_equivalence,
        });
        Ok(())
    }

    pub fn set_suspension_loop_pair(&mut self, x: &str, sigma_x: &str, omega_sigma_x: &str) -> Result<(), HigherCategoryError> {
        self.suspension_objects.insert(x.to_string(), sigma_x.to_string());
        self.loop_objects.insert(sigma_x.to_string(), omega_sigma_x.to_string());
        Ok(())
    }

    pub fn set_unit_equivalence(&mut self, x: &str, eta_map: &str) -> Result<(), HigherCategoryError> {
        let m = self.get_morphism(eta_map)?;
        if m.source != x {
            return Err(HigherCategoryError::BoundaryMismatch {
                expected: format!("source '{}'", x),
                found: format!("source '{}'", m.source),
            });
        }
        if !m.is_equivalence {
            return Err(HigherCategoryError::SuspensionLoopInvertibilityViolation {
                object: x.to_string(),
                details: format!("Unit map '{}' is not declared as an equivalence", eta_map),
            });
        }
        self.unit_morphisms.insert(x.to_string(), eta_map.to_string());
        Ok(())
    }

    pub fn set_counit_equivalence(&mut self, y: &str, epsilon_map: &str) -> Result<(), HigherCategoryError> {
        let m = self.get_morphism(epsilon_map)?;
        if m.target != y {
            return Err(HigherCategoryError::BoundaryMismatch {
                expected: format!("target '{}'", y),
                found: format!("target '{}'", m.target),
            });
        }
        if !m.is_equivalence {
            return Err(HigherCategoryError::SuspensionLoopInvertibilityViolation {
                object: y.to_string(),
                details: format!("Counit map '{}' is not declared as an equivalence", epsilon_map),
            });
        }
        self.counit_morphisms.insert(y.to_string(), epsilon_map.to_string());
        Ok(())
    }

    pub fn get_morphism(&self, id: &str) -> Result<&PointedMorphism, HigherCategoryError> {
        self.morphisms
            .iter()
            .find(|m| m.id == id)
            .ok_or_else(|| HigherCategoryError::OneCellNotFound { id: id.to_string() })
    }

    pub fn has_object(&self, id: &str) -> bool {
        self.objects.iter().any(|o| o.id == id)
    }

    pub fn verify_loop_suspension_equivalence(&self) -> Result<(), HigherCategoryError> {
        if self.objects.len() > 1 && (self.unit_morphisms.is_empty() || self.counit_morphisms.is_empty()) {
            return Err(HigherCategoryError::SuspensionLoopInvertibilityViolation {
                object: self.zero_object_id.clone(),
                details: "Category has non-zero objects but unit or counit witness map is empty".to_string(),
            });
        }

        for (x, eta_id) in &self.unit_morphisms {
            if !self.has_object(x) {
                return Err(HigherCategoryError::ZeroCellNotFound { id: x.clone() });
            }
            let m = self.get_morphism(eta_id)?;
            if m.source != *x || !self.has_object(&m.target) {
                return Err(HigherCategoryError::SuspensionLoopInvertibilityViolation {
                    object: x.clone(),
                    details: format!(
                        "Unit morphism '{}' source '{}' != '{}' or target '{}' not in objects",
                        eta_id, m.source, x, m.target
                    ),
                });
            }
            if !m.is_equivalence {
                return Err(HigherCategoryError::SuspensionLoopInvertibilityViolation {
                    object: x.clone(),
                    details: format!("Unit morphism '{}' is not an equivalence", eta_id),
                });
            }
        }

        for (y, eps_id) in &self.counit_morphisms {
            if !self.has_object(y) {
                return Err(HigherCategoryError::ZeroCellNotFound { id: y.clone() });
            }
            let m = self.get_morphism(eps_id)?;
            if m.target != *y || !self.has_object(&m.source) {
                return Err(HigherCategoryError::SuspensionLoopInvertibilityViolation {
                    object: y.clone(),
                    details: format!(
                        "Counit morphism '{}' target '{}' != '{}' or source '{}' not in objects",
                        eps_id, m.target, y, m.source
                    ),
                });
            }
            if !m.is_equivalence {
                return Err(HigherCategoryError::SuspensionLoopInvertibilityViolation {
                    object: y.clone(),
                    details: format!("Counit morphism '{}' is not an equivalence", eps_id),
                });
            }
        }

        Ok(())
    }

    pub fn add_spectrum(&mut self, spectrum_id: impl Into<String>, levels: Vec<SpectrumLevel>) {
        self.spectra.insert(spectrum_id.into(), levels);
    }

    pub fn verify_spectrum(&self, spectrum_id: &str) -> Result<(), HigherCategoryError> {
        let levels = self.spectra.get(spectrum_id).ok_or_else(|| {
            HigherCategoryError::ZeroCellNotFound { id: spectrum_id.to_string() }
        })?;

        for level in levels {
            if !self.has_object(&level.space_id) {
                return Err(HigherCategoryError::ZeroCellNotFound { id: level.space_id.clone() });
            }
            let m = self.get_morphism(&level.structure_map_id)?;
            if m.source != level.space_id {
                return Err(HigherCategoryError::SpectrumEquivalenceViolation {
                    level: level.level,
                    details: format!(
                        "Structure map '{}' source '{}' != spectrum space '{}' at level {}",
                        level.structure_map_id, m.source, level.space_id, level.level
                    ),
                });
            }
            if !self.has_object(&m.target) {
                return Err(HigherCategoryError::ZeroCellNotFound { id: m.target.clone() });
            }
            if !m.is_equivalence {
                return Err(HigherCategoryError::SpectrumEquivalenceViolation {
                    level: level.level,
                    details: format!(
                        "Structure map '{}' at spectrum level {} is not an equivalence",
                        level.structure_map_id, level.level
                    ),
                });
            }
        }
        Ok(())
    }
}
