
use std::collections::{BTreeMap, BTreeSet};

use omega_kernel::resource_limits::OperationLimits;
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};

use crate::error::{reserve_exact, HigherCategoryError};

#[derive(Debug, Clone, PartialEq, Eq, PartialOrd, Ord, Serialize, Deserialize)]
pub struct HomObject {
    pub src: String,
    pub tgt: String,
    pub v_object: String,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct EnrichedComposition {
    pub a: String,
    pub b: String,
    pub c: String,
    pub morphism_id: String,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct EnrichedUnit {
    pub object_id: String,
    pub morphism_id: String,
}

pub type EnrichedUnitMorphism = EnrichedUnit;

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct EnrichedCategory {
    pub name: String,
    pub base_monoidal_id: String,
    pub unit_object: String,
    pub objects: BTreeSet<String>,
    pub hom_objects: BTreeMap<(String, String), HomObject>,
    pub compositions: BTreeMap<(String, String, String), EnrichedComposition>,
    pub units: BTreeMap<String, EnrichedUnit>,
    pub v_morphisms: BTreeMap<String, (String, String)>,
    pub v_compose: BTreeMap<(String, String), String>,
    pub v_tensor_obj: BTreeMap<(String, String), String>,
    pub v_tensor_mor: BTreeMap<(String, String), String>,
    pub v_identities: BTreeMap<String, String>,
    pub left_unitors: BTreeMap<String, String>,
    pub right_unitors: BTreeMap<String, String>,
    pub associators: BTreeMap<(String, String, String), String>,
    pub limits: OperationLimits,
}

impl EnrichedCategory {
    pub fn new(name: &str, base_id: &str, unit_obj: &str) -> Self {
        Self::with_limits(name, base_id, unit_obj, OperationLimits::default())
    }

    pub fn with_limits(
        name: &str,
        base_id: &str,
        unit_obj: &str,
        limits: OperationLimits,
    ) -> Self {
        Self {
            name: name.to_string(),
            base_monoidal_id: base_id.to_string(),
            unit_object: unit_obj.to_string(),
            objects: BTreeSet::new(),
            hom_objects: BTreeMap::new(),
            compositions: BTreeMap::new(),
            units: BTreeMap::new(),
            v_morphisms: BTreeMap::new(),
            v_compose: BTreeMap::new(),
            v_tensor_obj: BTreeMap::new(),
            v_tensor_mor: BTreeMap::new(),
            v_identities: BTreeMap::new(),
            left_unitors: BTreeMap::new(),
            right_unitors: BTreeMap::new(),
            associators: BTreeMap::new(),
            limits,
        }
    }

    pub fn add_object(&mut self, id: &str) -> Result<(), HigherCategoryError> {
        if self.objects.contains(id) {
            return Err(HigherCategoryError::DuplicateCell { id: id.to_string() });
        }
        if self.objects.len() >= self.limits.max_cells {
            return Err(HigherCategoryError::AllocationLimitExceeded {
                requested: self.objects.len() + 1,
                limit: self.limits.max_cells,
            });
        }
        self.objects.insert(id.to_string());
        Ok(())
    }

    pub fn set_hom_object(
        &mut self,
        src: &str,
        tgt: &str,
        v_obj: &str,
    ) -> Result<(), HigherCategoryError> {
        if !self.objects.contains(src) {
            return Err(HigherCategoryError::ZeroCellNotFound { id: src.to_string() });
        }
        if !self.objects.contains(tgt) {
            return Err(HigherCategoryError::ZeroCellNotFound { id: tgt.to_string() });
        }
        self.hom_objects.insert(
            (src.to_string(), tgt.to_string()),
            HomObject {
                src: src.to_string(),
                tgt: tgt.to_string(),
                v_object: v_obj.to_string(),
            },
        );
        Ok(())
    }

    pub fn get_hom_object(&self, src: &str, tgt: &str) -> Result<String, HigherCategoryError> {
        self.hom_objects
            .get(&(src.to_string(), tgt.to_string()))
            .map(|h| h.v_object.clone())
            .ok_or_else(|| HigherCategoryError::OneCellNotFound {
                id: format!("Hom({src}, {tgt})"),
            })
    }

    pub fn set_v_morphism(
        &mut self,
        id: &str,
        src: &str,
        tgt: &str,
    ) -> Result<(), HigherCategoryError> {
        self.v_morphisms
            .insert(id.to_string(), (src.to_string(), tgt.to_string()));
        Ok(())
    }

    pub fn set_v_identity(&mut self, obj: &str, id_mor: &str) {
        self.v_identities.insert(obj.to_string(), id_mor.to_string());
        self.v_morphisms.insert(id_mor.to_string(), (obj.to_string(), obj.to_string()));
    }

    pub fn set_v_compose(&mut self, g: &str, f: &str, gf: &str) {
        self.v_compose
            .insert((g.to_string(), f.to_string()), gf.to_string());
    }

    pub fn set_v_tensor_obj(&mut self, x: &str, y: &str, xy: &str) {
        self.v_tensor_obj
            .insert((x.to_string(), y.to_string()), xy.to_string());
    }

    pub fn set_v_tensor_mor(&mut self, f: &str, g: &str, fg: &str) {
        self.v_tensor_mor
            .insert((f.to_string(), g.to_string()), fg.to_string());
    }

    pub fn set_left_unitor(&mut self, x: &str, lambda: &str) {
        self.left_unitors.insert(x.to_string(), lambda.to_string());
    }

    pub fn set_right_unitor(&mut self, x: &str, rho: &str) {
        self.right_unitors.insert(x.to_string(), rho.to_string());
    }

    pub fn set_associator(&mut self, x: &str, y: &str, z: &str, alpha: &str) {
        self.associators
            .insert((x.to_string(), y.to_string(), z.to_string()), alpha.to_string());
    }

    pub fn set_composition(
        &mut self,
        a: &str,
        b: &str,
        c: &str,
        mor_id: &str,
    ) -> Result<(), HigherCategoryError> {
        let hom_bc = self.get_hom_object(b, c)?;
        let hom_ab = self.get_hom_object(a, b)?;
        let hom_ac = self.get_hom_object(a, c)?;

        let expected_domain = self
            .v_tensor_obj
            .get(&(hom_bc.clone(), hom_ab.clone()))
            .cloned()
            .unwrap_or_else(|| format!("{hom_bc} tensor {hom_ab}"));

        let (mor_src, mor_tgt) = self.v_morphisms.get(mor_id).ok_or_else(|| {
            HigherCategoryError::OneCellNotFound { id: mor_id.to_string() }
        })?;

        if mor_src != &expected_domain || mor_tgt != &hom_ac {
            return Err(HigherCategoryError::BoundaryMismatch {
                expected: format!("morphism {expected_domain} -> {hom_ac}"),
                found: format!("morphism {mor_src} -> {mor_tgt}"),
            });
        }

        self.compositions.insert(
            (a.to_string(), b.to_string(), c.to_string()),
            EnrichedComposition {
                a: a.to_string(),
                b: b.to_string(),
                c: c.to_string(),
                morphism_id: mor_id.to_string(),
            },
        );
        Ok(())
    }

    pub fn set_unit(&mut self, a: &str, mor_id: &str) -> Result<(), HigherCategoryError> {
        let hom_aa = self.get_hom_object(a, a)?;
        let (mor_src, mor_tgt) = self.v_morphisms.get(mor_id).ok_or_else(|| {
            HigherCategoryError::OneCellNotFound { id: mor_id.to_string() }
        })?;

        if mor_src != &self.unit_object || mor_tgt != &hom_aa {
            return Err(HigherCategoryError::EnrichedUnitMismatch {
                object_id: a.to_string(),
                details: format!(
                    "Unit morphism '{mor_id}' has boundary {mor_src} -> {mor_tgt}, expected {} -> {hom_aa}",
                    self.unit_object
                ),
            });
        }

        self.units.insert(
            a.to_string(),
            EnrichedUnit {
                object_id: a.to_string(),
                morphism_id: mor_id.to_string(),
            },
        );
        Ok(())
    }

    fn check_left_unitality(
        &self,
        a: &str,
        b: &str,
        hom_ab: &str,
        id_hom_ab: &str,
    ) -> Result<(), HigherCategoryError> {
        let j_b = self
            .units
            .get(b)
            .ok_or_else(|| HigherCategoryError::EnrichedUnitMismatch {
                object_id: b.to_string(),
                details: format!("Missing unit morphism for object '{b}'"),
            })?;

        let j_b_tensor_id = self
            .v_tensor_mor
            .get(&(j_b.morphism_id.clone(), id_hom_ab.to_string()))
            .cloned()
            .unwrap_or_else(|| format!("{} tensor {}", j_b.morphism_id, id_hom_ab));

        let comp_abb = self
            .compositions
            .get(&(a.to_string(), b.to_string(), b.to_string()))
            .ok_or_else(|| HigherCategoryError::OneCellNotFound {
                id: format!("c({a}, {b}, {b})"),
            })?;

        let left_composite = self
            .v_compose
            .get(&(comp_abb.morphism_id.clone(), j_b_tensor_id.clone()))
            .cloned()
            .unwrap_or_else(|| format!("{} . {}", comp_abb.morphism_id, j_b_tensor_id));

        let lambda = self
            .left_unitors
            .get(hom_ab)
            .cloned()
            .unwrap_or_else(|| format!("lambda_{hom_ab}"));

        if left_composite != lambda {
            return Err(HigherCategoryError::EnrichedUnitMismatch {
                object_id: b.to_string(),
                details: format!(
                    "Left unit diagram failed: c ∘ (j_B ⊗ id) '{left_composite}' != lambda '{lambda}'"
                ),
            });
        }
        Ok(())
    }

    fn check_right_unitality(
        &self,
        a: &str,
        b: &str,
        hom_ab: &str,
        id_hom_ab: &str,
    ) -> Result<(), HigherCategoryError> {
        let j_a = self
            .units
            .get(a)
            .ok_or_else(|| HigherCategoryError::EnrichedUnitMismatch {
                object_id: a.to_string(),
                details: format!("Missing unit morphism for object '{a}'"),
            })?;

        let id_tensor_j_a = self
            .v_tensor_mor
            .get(&(id_hom_ab.to_string(), j_a.morphism_id.clone()))
            .cloned()
            .unwrap_or_else(|| format!("{} tensor {}", id_hom_ab, j_a.morphism_id));

        let comp_aab = self
            .compositions
            .get(&(a.to_string(), a.to_string(), b.to_string()))
            .ok_or_else(|| HigherCategoryError::OneCellNotFound {
                id: format!("c({a}, {a}, {b})"),
            })?;

        let right_composite = self
            .v_compose
            .get(&(comp_aab.morphism_id.clone(), id_tensor_j_a.clone()))
            .cloned()
            .unwrap_or_else(|| format!("{} . {}", comp_aab.morphism_id, id_tensor_j_a));

        let rho = self
            .right_unitors
            .get(hom_ab)
            .cloned()
            .unwrap_or_else(|| format!("rho_{hom_ab}"));

        if right_composite != rho {
            return Err(HigherCategoryError::EnrichedUnitMismatch {
                object_id: a.to_string(),
                details: format!(
                    "Right unit diagram failed: c ∘ (id ⊗ j_A) '{right_composite}' != rho '{rho}'"
                ),
            });
        }
        Ok(())
    }

    pub fn check_unitality(&self, a: &str, b: &str) -> Result<(), HigherCategoryError> {
        let hom_ab = self.get_hom_object(a, b)?;
        let id_hom_ab = self
            .v_identities
            .get(&hom_ab)
            .cloned()
            .unwrap_or_else(|| format!("id_{hom_ab}"));

        self.check_left_unitality(a, b, &hom_ab, &id_hom_ab)?;
        self.check_right_unitality(a, b, &hom_ab, &id_hom_ab)?;
        Ok(())
    }

    fn compute_associativity_lhs(
        &self,
        a: &str,
        b: &str,
        c: &str,
        d: &str,
        hom_ab: &str,
        hom_bc: &str,
        hom_cd: &str,
        id_ab: &str,
    ) -> Result<String, HigherCategoryError> {
        let c_bcd = &self
            .compositions
            .get(&(b.to_string(), c.to_string(), d.to_string()))
            .ok_or_else(|| HigherCategoryError::OneCellNotFound {
                id: format!("c({b}, {c}, {d})"),
            })?
            .morphism_id;

        let c_abd = &self
            .compositions
            .get(&(a.to_string(), b.to_string(), d.to_string()))
            .ok_or_else(|| HigherCategoryError::OneCellNotFound {
                id: format!("c({a}, {b}, {d})"),
            })?
            .morphism_id;

        let t1 = self
            .v_tensor_mor
            .get(&(c_bcd.clone(), id_ab.to_string()))
            .cloned()
            .unwrap_or_else(|| format!("{c_bcd} tensor id"));
        let p1_comp = self
            .v_compose
            .get(&(c_abd.clone(), t1.clone()))
            .cloned()
            .unwrap_or_else(|| format!("{c_abd} . {t1}"));
        let alpha = self
            .associators
            .get(&(hom_cd.to_string(), hom_bc.to_string(), hom_ab.to_string()))
            .cloned()
            .unwrap_or_else(|| "alpha".to_string());
        Ok(self
            .v_compose
            .get(&(p1_comp.clone(), alpha.clone()))
            .cloned()
            .unwrap_or_else(|| format!("{p1_comp} . {alpha}")))
    }

    fn compute_associativity_rhs(
        &self,
        a: &str,
        b: &str,
        c: &str,
        d: &str,
        id_cd: &str,
    ) -> Result<String, HigherCategoryError> {
        let c_abc = &self
            .compositions
            .get(&(a.to_string(), b.to_string(), c.to_string()))
            .ok_or_else(|| HigherCategoryError::OneCellNotFound {
                id: format!("c({a}, {b}, {c})"),
            })?
            .morphism_id;

        let c_acd = &self
            .compositions
            .get(&(a.to_string(), c.to_string(), d.to_string()))
            .ok_or_else(|| HigherCategoryError::OneCellNotFound {
                id: format!("c({a}, {c}, {d})"),
            })?
            .morphism_id;

        let t2 = self
            .v_tensor_mor
            .get(&(id_cd.to_string(), c_abc.clone()))
            .cloned()
            .unwrap_or_else(|| format!("id tensor {c_abc}"));
        Ok(self
            .v_compose
            .get(&(c_acd.clone(), t2.clone()))
            .cloned()
            .unwrap_or_else(|| format!("{c_acd} . {t2}")))
    }

    pub fn check_associativity(
        &self,
        a: &str,
        b: &str,
        c: &str,
        d: &str,
    ) -> Result<(), HigherCategoryError> {
        let hom_ab = self.get_hom_object(a, b)?;
        let hom_bc = self.get_hom_object(b, c)?;
        let hom_cd = self.get_hom_object(c, d)?;

        let id_ab = self
            .v_identities
            .get(&hom_ab)
            .cloned()
            .unwrap_or_else(|| format!("id_{hom_ab}"));
        let id_cd = self
            .v_identities
            .get(&hom_cd)
            .cloned()
            .unwrap_or_else(|| format!("id_{hom_cd}"));

        let lhs = self.compute_associativity_lhs(
            a, b, c, d, &hom_ab, &hom_bc, &hom_cd, &id_ab,
        )?;
        let rhs = self.compute_associativity_rhs(a, b, c, d, &id_cd)?;

        if lhs != rhs {
            return Err(HigherCategoryError::EnrichedAssociativityViolation {
                details: format!(
                    "Enriched associativity failed for ({a}, {b}, {c}, {d}): LHS '{lhs}' != RHS '{rhs}'"
                ),
            });
        }

        Ok(())
    }

    pub fn validate_all(&self) -> Result<(), HigherCategoryError> {
        let mut objs: Vec<String> = Vec::new();
        for o in &self.objects {
            reserve_exact(&mut objs, 1, &self.limits)?;
            objs.push(o.clone());
        }
        for i in 0..objs.len() {
            for j in 0..objs.len() {
                self.check_unitality(&objs[i], &objs[j])?;
            }
        }
        Ok(())
    }

    pub fn content_hash(&self) -> String {
        let mut hasher = Sha256::new();
        hasher.update(self.name.as_bytes());
        hasher.update(self.base_monoidal_id.as_bytes());
        hasher.update(self.unit_object.as_bytes());
        for obj in &self.objects {
            hasher.update(obj.as_bytes());
        }
        for ((s, t), hom) in &self.hom_objects {
            hasher.update(s.as_bytes());
            hasher.update(t.as_bytes());
            hasher.update(hom.v_object.as_bytes());
        }
        for (id, u) in &self.units {
            hasher.update(id.as_bytes());
            hasher.update(u.morphism_id.as_bytes());
        }
        format!("{:x}", hasher.finalize())
    }
}
