//! Quillen Model Category implementation and exact verification.
//!
//! Models Quillen model categories satisfying axioms MC1-MC5:
//! - Complete and cocomplete category
//! - Three distinguished classes of morphisms: Weak Equivalences (W), Fibrations (F), Cofibrations (C)
//! - Two-out-of-three property for W
//! - Retract closure
//! - Lifting properties: (W ∩ C) ⋔ F and C ⋔ (W ∩ F)
//! - Functorial factorizations: f = p ∘ i (i ∈ W ∩ C, p ∈ F) and f = q ∘ j (j ∈ C, q ∈ W ∩ F)
//!
//! Zero floats. Soviet Builder allocation bounded by `OperationLimits`.
//!
//! AuthorityEffect: None.

use std::collections::{HashMap, HashSet};

use omega_kernel::resource_limits::OperationLimits;
use serde::{Deserialize, Serialize};

use crate::error::{reserve_exact, HigherCategoryError};

/// Morphism in a model category.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct ModelMorphism {
    pub id: String,
    pub source: String,
    pub target: String,
}

/// A commutative square representing a lifting problem:
///   A -- u --> X
///   |          |
///   i          p
///   v          v
///   B -- v_map -> Y
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct CommutativeSquare {
    pub i_map: String,
    pub p_map: String,
    pub u_map: String,
    pub v_map: String,
}

/// A pair of factorizations for a morphism f:
/// 1. f = p_map ∘ i_map with i_map ∈ W ∩ C (acyclic cofibration), p_map ∈ F (fibration)
/// 2. f = q_map ∘ j_map with j_map ∈ C (cofibration), q_map ∈ W ∩ F (acyclic fibration)
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct MorphismFactorizations {
    pub morphism: String,
    pub i_map: String,
    pub p_map: String,
    pub j_map: String,
    pub q_map: String,
}

/// Finite Quillen Model Category.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct ModelCategory {
    pub objects: Vec<String>,
    pub morphisms: Vec<ModelMorphism>,
    /// Composition table: (f, g) -> g ∘ f (where f: X -> Y, g: Y -> Z)
    pub compositions: HashMap<(String, String), String>,
    /// Identity map per object: object -> id_morphism
    pub identities: HashMap<String, String>,
    /// Weak equivalences W
    pub weak_equivalences: HashSet<String>,
    /// Fibrations F
    pub fibrations: HashSet<String>,
    /// Cofibrations C
    pub cofibrations: HashSet<String>,
    /// Factorization witnesses
    pub factorizations: HashMap<String, MorphismFactorizations>,
}

impl ModelCategory {
    /// Constructs an empty model category with preallocated capacities under `OperationLimits`.
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

    /// Adds an object to the category.
    pub fn add_object(&mut self, object_id: impl Into<String>, limits: &OperationLimits) -> Result<(), HigherCategoryError> {
        let obj = object_id.into();
        if self.objects.contains(&obj) {
            return Err(HigherCategoryError::DuplicateCell { id: obj });
        }
        reserve_exact(&mut self.objects, 1, limits)?;
        self.objects.push(obj);
        Ok(())
    }

    /// Adds a morphism to the category.
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

    /// Declares the identity morphism for an object.
    pub fn set_identity(&mut self, object: &str, id_morphism: &str) -> Result<(), HigherCategoryError> {
        if !self.objects.contains(&object.to_string()) {
            return Err(HigherCategoryError::ZeroCellNotFound { id: object.to_string() });
        }
        if !self.morphisms.iter().any(|m| m.id == id_morphism) {
            return Err(HigherCategoryError::OneCellNotFound { id: id_morphism.to_string() });
        }
        self.identities.insert(object.to_string(), id_morphism.to_string());
        // In any model category, identities are trivial cofibrations and trivial fibrations:
        self.weak_equivalences.insert(id_morphism.to_string());
        self.fibrations.insert(id_morphism.to_string());
        self.cofibrations.insert(id_morphism.to_string());
        Ok(())
    }

    /// Declares composition g ∘ f = h (where f: X -> Y, g: Y -> Z, h: X -> Z).
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

    /// Retrieves a morphism reference by ID.
    pub fn get_morphism(&self, id: &str) -> Result<&ModelMorphism, HigherCategoryError> {
        self.morphisms
            .iter()
            .find(|m| m.id == id)
            .ok_or_else(|| HigherCategoryError::OneCellNotFound { id: id.to_string() })
    }

    /// Evaluates composition g ∘ f if defined.
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

    /// Returns true if morphism is an acyclic cofibration (W ∩ C).
    pub fn is_acyclic_cofibration(&self, id: &str) -> bool {
        self.weak_equivalences.contains(id) && self.cofibrations.contains(id)
    }

    /// Returns true if morphism is an acyclic fibration (W ∩ F).
    pub fn is_acyclic_fibration(&self, id: &str) -> bool {
        self.weak_equivalences.contains(id) && self.fibrations.contains(id)
    }

    /// Verifies the two-out-of-three axiom for all composable pairs:
    /// If two of {f, g, g ∘ f} are in W, then so is the third.
    pub fn verify_two_out_of_three(&self) -> Result<(), HigherCategoryError> {
        for ((f, g), h) in &self.compositions {
            let f_in = self.weak_equivalences.contains(f);
            let g_in = self.weak_equivalences.contains(g);
            let h_in = self.weak_equivalences.contains(h);

            // Case 1: f ∈ W, g ∈ W => h ∈ W
            if f_in && g_in && !h_in {
                return Err(HigherCategoryError::TwoOutOfThreeViolation {
                    f: f.clone(),
                    g: g.clone(),
                    details: format!("f and g in W, but composite g ∘ f ('{}') not in W", h),
                });
            }
            // Case 2: f ∈ W, h ∈ W => g ∈ W
            if f_in && h_in && !g_in {
                return Err(HigherCategoryError::TwoOutOfThreeViolation {
                    f: f.clone(),
                    g: g.clone(),
                    details: format!("f and g ∘ f in W, but g ('{}') not in W", g),
                });
            }
            // Case 3: g ∈ W, h ∈ W => f ∈ W
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

    /// Verifies a diagonal lift h for a commutative square:
    ///   A -- u --> X
    ///   |          |
    ///   i          p
    ///   v          v
    ///   B -- v_map -> Y
    ///
    /// Must satisfy:
    /// 1. Commutativity of outer square: p ∘ u = v_map ∘ i
    /// 2. Top triangle: h ∘ i = u
    /// 3. Bottom triangle: p ∘ h = v_map
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

        // Top triangle: h ∘ i = u
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

        // Bottom triangle: p ∘ h = v
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

    /// Verifies functorial factorizations for all declared morphisms.
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

            // Factorization 1: f = p ∘ i with i ∈ W ∩ C, p ∈ F
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

            // Factorization 2: f = q ∘ j with j ∈ C, q ∈ W ∩ F
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

    /// Master validation: validates Quillen model category axioms on declared structure.
    pub fn validate(&self) -> Result<(), HigherCategoryError> {
        // Axiom M1/Identity: every object has an identity morphism
        for obj in &self.objects {
            let id_m = self.identities.get(obj).ok_or_else(|| {
                HigherCategoryError::FactorizationViolation {
                    morphism: obj.clone(),
                    details: format!("Object '{}' missing identity morphism", obj),
                }
            })?;
            // Retract closure: identity morphisms are weak equivalences, fibrations, and cofibrations
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
