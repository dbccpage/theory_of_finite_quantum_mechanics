
use std::collections::{HashMap, HashSet};

use omega_kernel::resource_limits::OperationLimits;
use serde::{Deserialize, Serialize};

use crate::error::{reserve_exact, HigherCategoryError};

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct ModelMorphism {
    pub id: String,
    pub source: String,
    pub target: String,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct CommutativeSquare {
    pub i_map: String,
    pub p_map: String,
    pub u_map: String,
    pub v_map: String,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct MorphismFactorizations {
    pub morphism: String,
    pub i_map: String,
    pub p_map: String,
    pub j_map: String,
    pub q_map: String,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct ModelCategory {
    pub objects: Vec<String>,
    pub morphisms: Vec<ModelMorphism>,
    pub compositions: HashMap<(String, String), String>,
    pub identities: HashMap<String, String>,
    pub weak_equivalences: HashSet<String>,
    pub fibrations: HashSet<String>,
    pub cofibrations: HashSet<String>,
    pub factorizations: HashMap<String, MorphismFactorizations>,
}

impl ModelCategory {
    pub fn new(limits: &OperationLimits) -> Result<Self, HigherCategoryError> {
        let mut objects = Vec::new();
        reserve_exact(&mut objects, 8, limits)?;
        let mut morphisms = Vec::new();
        reserve_exact(&mut morphisms, 16, limits)?;

        Ok(Self {
            objects,
            morphisms,
            compositions: HashMap::new(),
            identities: HashMap::new(),
            weak_equivalences: HashSet::new(),
            fibrations: HashSet::new(),
            cofibrations: HashSet::new(),
            factorizations: HashMap::new(),
        })
    }

    pub fn add_object(&mut self, object_id: impl Into<String>, limits: &OperationLimits) -> Result<(), HigherCategoryError> {
        let obj = object_id.into();
        if self.objects.contains(&obj) {
            return Err(HigherCategoryError::DuplicateCell { id: obj });
        }
        reserve_exact(&mut self.objects, 1, limits)?;
        self.objects.push(obj);
        Ok(())
    }

    pub fn add_morphism(
        &mut self,
        id: impl Into<String>,
        source: impl Into<String>,
        target: impl Into<String>,
        limits: &OperationLimits,
    ) -> Result<(), HigherCategoryError> {
        let id_str = id.into();
        let src_str = source.into();
        let tgt_str = target.into();

        if !self.objects.contains(&src_str) {
            return Err(HigherCategoryError::ZeroCellNotFound { id: src_str });
        }
        if !self.objects.contains(&tgt_str) {
            return Err(HigherCategoryError::ZeroCellNotFound { id: tgt_str });
        }
        if self.morphisms.iter().any(|m| m.id == id_str) {
            return Err(HigherCategoryError::DuplicateCell { id: id_str });
        }

        reserve_exact(&mut self.morphisms, 1, limits)?;
        self.morphisms.push(ModelMorphism {
            id: id_str,
            source: src_str,
            target: tgt_str,
        });
        Ok(())
    }

    pub fn set_identity(&mut self, object: &str, id_morphism: &str) -> Result<(), HigherCategoryError> {
        if !self.objects.contains(&object.to_string()) {
            return Err(HigherCategoryError::ZeroCellNotFound { id: object.to_string() });
        }
        if !self.morphisms.iter().any(|m| m.id == id_morphism) {
            return Err(HigherCategoryError::OneCellNotFound { id: id_morphism.to_string() });
        }
        self.identities.insert(object.to_string(), id_morphism.to_string());
        self.weak_equivalences.insert(id_morphism.to_string());
        self.fibrations.insert(id_morphism.to_string());
        self.cofibrations.insert(id_morphism.to_string());
        Ok(())
    }

    pub fn add_composition(
        &mut self,
        f: &str,
        g: &str,
        h: &str,
    ) -> Result<(), HigherCategoryError> {
        let f_m = self.get_morphism(f)?;
        let g_m = self.get_morphism(g)?;
        let h_m = self.get_morphism(h)?;

        if f_m.target != g_m.source {
            return Err(HigherCategoryError::OneCellNotComposable {
                first: f.to_string(),
                second: g.to_string(),
                tgt: f_m.target.clone(),
                src: g_m.source.clone(),
            });
        }
        if h_m.source != f_m.source || h_m.target != g_m.target {
            return Err(HigherCategoryError::BoundaryMismatch {
                expected: format!("{} -> {}", f_m.source, g_m.target),
                found: format!("{} -> {}", h_m.source, h_m.target),
            });
        }

        self.compositions.insert((f.to_string(), g.to_string()), h.to_string());
        Ok(())
    }

    pub fn get_morphism(&self, id: &str) -> Result<&ModelMorphism, HigherCategoryError> {
        self.morphisms
            .iter()
            .find(|m| m.id == id)
            .ok_or_else(|| HigherCategoryError::OneCellNotFound { id: id.to_string() })
    }

    pub fn compose(&self, f: &str, g: &str) -> Result<&str, HigherCategoryError> {
        self.compositions
            .get(&(f.to_string(), g.to_string()))
            .map(|s| s.as_str())
            .ok_or_else(|| HigherCategoryError::OneCellNotComposable {
                first: f.to_string(),
                second: g.to_string(),
                tgt: "unknown".to_string(),
                src: "unknown".to_string(),
            })
    }

    pub fn is_acyclic_cofibration(&self, id: &str) -> bool {
        self.weak_equivalences.contains(id) && self.cofibrations.contains(id)
    }

    pub fn is_acyclic_fibration(&self, id: &str) -> bool {
        self.weak_equivalences.contains(id) && self.fibrations.contains(id)
    }

    pub fn verify_two_out_of_three(&self) -> Result<(), HigherCategoryError> {
        for ((f, g), h) in &self.compositions {
            let f_in = self.weak_equivalences.contains(f);
            let g_in = self.weak_equivalences.contains(g);
            let h_in = self.weak_equivalences.contains(h);

            if f_in && g_in && !h_in {
                return Err(HigherCategoryError::TwoOutOfThreeViolation {
                    f: f.clone(),
                    g: g.clone(),
                    details: format!("f and g in W, but composite g ∘ f ('{}') not in W", h),
                });
            }
            if f_in && h_in && !g_in {
                return Err(HigherCategoryError::TwoOutOfThreeViolation {
                    f: f.clone(),
                    g: g.clone(),
                    details: format!("f and g ∘ f in W, but g ('{}') not in W", g),
                });
            }
            if g_in && h_in && !f_in {
                return Err(HigherCategoryError::TwoOutOfThreeViolation {
                    f: f.clone(),
                    g: g.clone(),
                    details: format!("g and g ∘ f in W, but f ('{}') not in W", f),
                });
            }
        }
        Ok(())
    }

    pub fn verify_lift(
        &self,
        square: &CommutativeSquare,
        h_lift: &str,
    ) -> Result<(), HigherCategoryError> {
        let u_comp_p = self.compose(&square.u_map, &square.p_map)?;
        let i_comp_v = self.compose(&square.i_map, &square.v_map)?;
        if u_comp_p != i_comp_v {
            return Err(HigherCategoryError::LiftingPropertyViolation {
                cofibration: square.i_map.clone(),
                fibration: square.p_map.clone(),
                details: format!(
                    "Square does not commute: p ∘ u ('{}') != v ∘ i ('{}')",
                    u_comp_p, i_comp_v
                ),
            });
        }

        let i_comp_h = self.compose(&square.i_map, h_lift)?;
        if i_comp_h != square.u_map {
            return Err(HigherCategoryError::LiftingPropertyViolation {
                cofibration: square.i_map.clone(),
                fibration: square.p_map.clone(),
                details: format!(
                    "Top triangle fails: h ∘ i ('{}') != u ('{}')",
                    i_comp_h, square.u_map
                ),
            });
        }

        let h_comp_p = self.compose(h_lift, &square.p_map)?;
        if h_comp_p != square.v_map {
            return Err(HigherCategoryError::LiftingPropertyViolation {
                cofibration: square.i_map.clone(),
                fibration: square.p_map.clone(),
                details: format!(
                    "Bottom triangle fails: p ∘ h ('{}') != v ('{}')",
                    h_comp_p, square.v_map
                ),
            });
        }

        Ok(())
    }

    pub fn verify_factorizations(&self) -> Result<(), HigherCategoryError> {
        if self.morphisms.is_empty() {
            return Ok(());
        }
        for mor in &self.morphisms {
            let m_id = &mor.id;
            let facts = self.factorizations.get(m_id).ok_or_else(|| {
                HigherCategoryError::FactorizationViolation {
                    morphism: m_id.clone(),
                    details: format!("Morphism '{}' missing required factorization witness", m_id),
                }
            })?;

            let i_comp_p = self.compose(&facts.i_map, &facts.p_map)?;
            if i_comp_p != *m_id {
                return Err(HigherCategoryError::FactorizationViolation {
                    morphism: m_id.clone(),
                    details: format!("Factorization 1 p ∘ i ('{}') != f ('{}')", i_comp_p, m_id),
                });
            }
            if !self.is_acyclic_cofibration(&facts.i_map) {
                return Err(HigherCategoryError::FactorizationViolation {
                    morphism: m_id.clone(),
                    details: format!("i ('{}') is not an acyclic cofibration (W ∩ C)", facts.i_map),
                });
            }
            if !self.fibrations.contains(&facts.p_map) {
                return Err(HigherCategoryError::FactorizationViolation {
                    morphism: m_id.clone(),
                    details: format!("p ('{}') is not a fibration (F)", facts.p_map),
                });
            }

            let j_comp_q = self.compose(&facts.j_map, &facts.q_map)?;
            if j_comp_q != *m_id {
                return Err(HigherCategoryError::FactorizationViolation {
                    morphism: m_id.clone(),
                    details: format!("Factorization 2 q ∘ j ('{}') != f ('{}')", j_comp_q, m_id),
                });
            }
            if !self.cofibrations.contains(&facts.j_map) {
                return Err(HigherCategoryError::FactorizationViolation {
                    morphism: m_id.clone(),
                    details: format!("j ('{}') is not a cofibration (C)", facts.j_map),
                });
            }
            if !self.is_acyclic_fibration(&facts.q_map) {
                return Err(HigherCategoryError::FactorizationViolation {
                    morphism: m_id.clone(),
                    details: format!("q ('{}') is not an acyclic fibration (W ∩ F)", facts.q_map),
                });
            }
        }
        Ok(())
    }

    pub fn validate(&self) -> Result<(), HigherCategoryError> {
        for obj in &self.objects {
            let id_m = self.identities.get(obj).ok_or_else(|| {
                HigherCategoryError::FactorizationViolation {
                    morphism: obj.clone(),
                    details: format!("Object '{}' missing identity morphism", obj),
                }
            })?;
            if !self.weak_equivalences.contains(id_m) {
                return Err(HigherCategoryError::FactorizationViolation {
                    morphism: id_m.clone(),
                    details: format!("Identity '{}' must be a weak equivalence", id_m),
                });
            }
            if !self.fibrations.contains(id_m) {
                return Err(HigherCategoryError::FactorizationViolation {
                    morphism: id_m.clone(),
                    details: format!("Identity '{}' must be a fibration", id_m),
                });
            }
            if !self.cofibrations.contains(id_m) {
                return Err(HigherCategoryError::FactorizationViolation {
                    morphism: id_m.clone(),
                    details: format!("Identity '{}' must be a cofibration", id_m),
                });
            }
        }
        self.verify_two_out_of_three()?;
        self.verify_factorizations()?;
        Ok(())
    }
}
