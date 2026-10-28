
use std::collections::{BTreeMap, BTreeSet};

use engine_kernel::resource_limits::OperationLimits;
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};

use crate::error::{reserve_exact, HigherCategoryError};

pub fn canonicalize_terms(terms: &[(i64, String)]) -> Vec<(i64, String)> {
    let mut map: BTreeMap<String, i64> = BTreeMap::new();
    for (coeff, gen) in terms {
        *map.entry(gen.clone()).or_insert(0) += coeff;
    }
    map.into_iter()
        .filter(|(_, coeff)| *coeff != 0)
        .map(|(gen, coeff)| (coeff, gen))
        .collect()
}

pub fn add_terms(a: &[(i64, String)], b: &[(i64, String)]) -> Vec<(i64, String)> {
    let mut combined = Vec::with_capacity(a.len() + b.len());
    combined.extend_from_slice(a);
    combined.extend_from_slice(b);
    canonicalize_terms(&combined)
}

pub fn scale_terms(terms: &[(i64, String)], scalar: i64) -> Vec<(i64, String)> {
    if scalar == 0 {
        return Vec::new();
    }
    let scaled: Vec<(i64, String)> = terms
        .iter()
        .map(|(c, gen)| (c * scalar, gen.clone()))
        .collect();
    canonicalize_terms(&scaled)
}

#[derive(Debug, Clone, PartialEq, Eq, PartialOrd, Ord, Serialize, Deserialize)]
pub struct GradedMorphism {
    pub id: String,
    pub src: String,
    pub tgt: String,
    pub degree: i32,
}

pub type DifferentialMap = BTreeMap<String, Vec<(i64, String)>>;

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct ChainDifferential {
    pub degree_shift: i32,
    pub map: DifferentialMap,
}

impl ChainDifferential {
    pub fn new(degree_shift: i32) -> Self {
        Self {
            degree_shift,
            map: BTreeMap::new(),
        }
    }

    pub fn set_differential(&mut self, mor_id: &str, target_terms: Vec<(i64, String)>) {
        self.map
            .insert(mor_id.to_string(), canonicalize_terms(&target_terms));
    }

    pub fn get_differential(&self, mor_id: &str) -> Vec<(i64, String)> {
        self.map.get(mor_id).cloned().unwrap_or_default()
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct GradedHomComplex {
    pub src: String,
    pub tgt: String,
    pub morphisms: BTreeMap<String, GradedMorphism>,
    pub differential: ChainDifferential,
}

impl GradedHomComplex {
    pub fn new(src: &str, tgt: &str) -> Self {
        Self {
            src: src.to_string(),
            tgt: tgt.to_string(),
            morphisms: BTreeMap::new(),
            differential: ChainDifferential::new(1),
        }
    }
}

pub struct LeibnizSignValidator;

impl LeibnizSignValidator {
    #[inline]
    pub fn sign_for_degree(degree: i32) -> i8 {
        if degree.rem_euclid(2) == 0 {
            1
        } else {
            -1
        }
    }

    pub fn validate(cat: &DgCategory, g_id: &str, f_id: &str) -> Result<(), HigherCategoryError> {
        let f = cat
            .morphisms
            .get(f_id)
            .ok_or_else(|| HigherCategoryError::OneCellNotFound {
                id: f_id.to_string(),
            })?;
        let g = cat
            .morphisms
            .get(g_id)
            .ok_or_else(|| HigherCategoryError::OneCellNotFound {
                id: g_id.to_string(),
            })?;

        if f.tgt != g.src {
            return Err(HigherCategoryError::OneCellNotComposable {
                first: f_id.to_string(),
                second: g_id.to_string(),
                tgt: f.tgt.clone(),
                src: g.src.clone(),
            });
        }

        let gf_terms = cat.compose_morphisms(g_id, f_id)?;
        let lhs = cat.apply_differential_to_terms(&gf_terms)?;

        let d_g = cat.differential_of(g_id);
        let mut rhs_term1 = Vec::new();
        for (coeff_g, gen_g) in &d_g {
            let comp = cat.compose_morphisms(gen_g, f_id)?;
            let scaled = scale_terms(&comp, *coeff_g);
            rhs_term1 = add_terms(&rhs_term1, &scaled);
        }

        let sign_g = Self::sign_for_degree(g.degree) as i64;
        let d_f = cat.differential_of(f_id);
        let mut rhs_term2 = Vec::new();
        for (coeff_f, gen_f) in &d_f {
            let comp = cat.compose_morphisms(g_id, gen_f)?;
            let scaled = scale_terms(&comp, *coeff_f * sign_g);
            rhs_term2 = add_terms(&rhs_term2, &scaled);
        }

        let rhs = add_terms(&rhs_term1, &rhs_term2);

        if lhs != rhs {
            return Err(HigherCategoryError::LeibnizRuleViolation {
                details: format!(
                    "Leibniz rule failed for g='{g_id}' (deg {deg_g}) and f='{f_id}' (deg {deg_f}): LHS={lhs:?} != RHS={rhs:?} (term1={rhs_term1:?}, term2={rhs_term2:?}, sign={sign_g})",
                    deg_g = g.degree,
                    deg_f = f.degree
                ),
            });
        }

        Ok(())
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct CohomologyCategoryH0 {
    pub objects: BTreeSet<String>,
    pub zero_cycles: BTreeMap<(String, String), Vec<String>>,
    pub zero_boundaries: BTreeMap<(String, String), Vec<String>>,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct DgCategory {
    pub name: String,
    pub objects: BTreeSet<String>,
    pub morphisms: BTreeMap<String, GradedMorphism>,
    pub hom_complexes: BTreeMap<(String, String), GradedHomComplex>,
    pub composition_table: BTreeMap<(String, String), Vec<(i64, String)>>,
    pub identities: BTreeMap<String, String>,
    pub limits: OperationLimits,
}

impl DgCategory {
    pub fn new(name: &str) -> Self {
        Self::with_limits(name, OperationLimits::default())
    }

    pub fn with_limits(name: &str, limits: OperationLimits) -> Self {
        Self {
            name: name.to_string(),
            objects: BTreeSet::new(),
            morphisms: BTreeMap::new(),
            hom_complexes: BTreeMap::new(),
            composition_table: BTreeMap::new(),
            identities: BTreeMap::new(),
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

    pub fn add_morphism(
        &mut self,
        id: &str,
        src: &str,
        tgt: &str,
        degree: i32,
    ) -> Result<(), HigherCategoryError> {
        if self.morphisms.contains_key(id) {
            return Err(HigherCategoryError::DuplicateCell { id: id.to_string() });
        }
        if !self.objects.contains(src) {
            return Err(HigherCategoryError::ZeroCellNotFound { id: src.to_string() });
        }
        if !self.objects.contains(tgt) {
            return Err(HigherCategoryError::ZeroCellNotFound { id: tgt.to_string() });
        }
        if self.morphisms.len() >= self.limits.max_cells {
            return Err(HigherCategoryError::AllocationLimitExceeded {
                requested: self.morphisms.len() + 1,
                limit: self.limits.max_cells,
            });
        }

        let morphism = GradedMorphism {
            id: id.to_string(),
            src: src.to_string(),
            tgt: tgt.to_string(),
            degree,
        };

        self.morphisms.insert(id.to_string(), morphism.clone());

        let key = (src.to_string(), tgt.to_string());
        let hom = self
            .hom_complexes
            .entry(key)
            .or_insert_with(|| GradedHomComplex::new(src, tgt));
        hom.morphisms.insert(id.to_string(), morphism);

        Ok(())
    }

    pub fn set_differential(
        &mut self,
        mor_id: &str,
        target_terms: Vec<(i64, String)>,
    ) -> Result<(), HigherCategoryError> {
        let mor = self
            .morphisms
            .get(mor_id)
            .ok_or_else(|| HigherCategoryError::OneCellNotFound {
                id: mor_id.to_string(),
            })?;
        let src = mor.src.clone();
        let tgt = mor.tgt.clone();
        let expected_deg = mor.degree + 1;

        for (_coeff, target_id) in &target_terms {
            let target_mor = self
                .morphisms
                .get(target_id)
                .ok_or_else(|| HigherCategoryError::OneCellNotFound {
                    id: target_id.to_string(),
                })?;
            if target_mor.src != src || target_mor.tgt != tgt {
                return Err(HigherCategoryError::BoundaryMismatch {
                    expected: format!("morphism with src={src}, tgt={tgt}"),
                    found: format!("morphism with src={}, tgt={}", target_mor.src, target_mor.tgt),
                });
            }
            if target_mor.degree != expected_deg {
                return Err(HigherCategoryError::BoundaryMismatch {
                    expected: format!("degree {expected_deg}"),
                    found: format!("degree {}", target_mor.degree),
                });
            }
        }

        let key = (src, tgt);
        let hom = self.hom_complexes.get_mut(&key).expect("hom complex must exist");
        hom.differential.set_differential(mor_id, target_terms);

        Ok(())
    }

    pub fn set_composition(
        &mut self,
        g_id: &str,
        f_id: &str,
        result_terms: Vec<(i64, String)>,
    ) -> Result<(), HigherCategoryError> {
        let f = self
            .morphisms
            .get(f_id)
            .ok_or_else(|| HigherCategoryError::OneCellNotFound {
                id: f_id.to_string(),
            })?;
        let g = self
            .morphisms
            .get(g_id)
            .ok_or_else(|| HigherCategoryError::OneCellNotFound {
                id: g_id.to_string(),
            })?;

        if f.tgt != g.src {
            return Err(HigherCategoryError::OneCellNotComposable {
                first: f_id.to_string(),
                second: g_id.to_string(),
                tgt: f.tgt.clone(),
                src: g.src.clone(),
            });
        }

        let expected_deg = f.degree + g.degree;
        for (_coeff, h_id) in &result_terms {
            let h = self
                .morphisms
                .get(h_id)
                .ok_or_else(|| HigherCategoryError::OneCellNotFound {
                    id: h_id.to_string(),
                })?;
            if h.src != f.src || h.tgt != g.tgt {
                return Err(HigherCategoryError::BoundaryMismatch {
                    expected: format!("src={}, tgt={}", f.src, g.tgt),
                    found: format!("src={}, tgt={}", h.src, h.tgt),
                });
            }
            if h.degree != expected_deg {
                return Err(HigherCategoryError::BoundaryMismatch {
                    expected: format!("degree {expected_deg}"),
                    found: format!("degree {}", h.degree),
                });
            }
        }

        self.composition_table.insert(
            (g_id.to_string(), f_id.to_string()),
            canonicalize_terms(&result_terms),
        );
        Ok(())
    }

    pub fn set_identity(&mut self, obj_id: &str, mor_id: &str) -> Result<(), HigherCategoryError> {
        if !self.objects.contains(obj_id) {
            return Err(HigherCategoryError::ZeroCellNotFound {
                id: obj_id.to_string(),
            });
        }
        let mor = self
            .morphisms
            .get(mor_id)
            .ok_or_else(|| HigherCategoryError::OneCellNotFound {
                id: mor_id.to_string(),
            })?;
        if mor.src != obj_id || mor.tgt != obj_id {
            return Err(HigherCategoryError::BoundaryMismatch {
                expected: format!("endomorphism on {obj_id}"),
                found: format!("src={}, tgt={}", mor.src, mor.tgt),
            });
        }
        if mor.degree != 0 {
            return Err(HigherCategoryError::BoundaryMismatch {
                expected: "degree 0 for identity".to_string(),
                found: format!("degree {}", mor.degree),
            });
        }

        self.identities.insert(obj_id.to_string(), mor_id.to_string());
        Ok(())
    }

    pub fn differential_of(&self, mor_id: &str) -> Vec<(i64, String)> {
        if let Some(mor) = self.morphisms.get(mor_id) {
            let key = (mor.src.clone(), mor.tgt.clone());
            if let Some(hom) = self.hom_complexes.get(&key) {
                return hom.differential.get_differential(mor_id);
            }
        }
        Vec::new()
    }

    pub fn apply_differential_to_terms(
        &self,
        terms: &[(i64, String)],
    ) -> Result<Vec<(i64, String)>, HigherCategoryError> {
        let mut result = Vec::new();
        for (coeff, gen) in terms {
            let d_gen = self.differential_of(gen);
            let scaled = scale_terms(&d_gen, *coeff);
            result = add_terms(&result, &scaled);
        }
        Ok(result)
    }

    pub fn compose_morphisms(
        &self,
        g_id: &str,
        f_id: &str,
    ) -> Result<Vec<(i64, String)>, HigherCategoryError> {
        let key = (g_id.to_string(), f_id.to_string());
        if let Some(terms) = self.composition_table.get(&key) {
            Ok(terms.clone())
        } else {
            let f = self
                .morphisms
                .get(f_id)
                .ok_or_else(|| HigherCategoryError::OneCellNotFound {
                    id: f_id.to_string(),
                })?;
            let g = self
                .morphisms
                .get(g_id)
                .ok_or_else(|| HigherCategoryError::OneCellNotFound {
                    id: g_id.to_string(),
                })?;

            if let Some(id_src) = self.identities.get(&f.src) {
                if g_id == id_src && f.src == f.tgt {
                    return Ok(vec![(1, f_id.to_string())]);
                }
            }
            if let Some(id_tgt) = self.identities.get(&f.tgt) {
                if g_id == id_tgt {
                    return Ok(vec![(1, f_id.to_string())]);
                }
            }
            if let Some(id_gsrc) = self.identities.get(&g.src) {
                if f_id == id_gsrc {
                    return Ok(vec![(1, g_id.to_string())]);
                }
            }

            Ok(Vec::new())
        }
    }

    pub fn check_nilpotence(&self) -> Result<(), HigherCategoryError> {
        for (mor_id, mor) in &self.morphisms {
            let d_1 = self.differential_of(mor_id);
            let d_2 = self.apply_differential_to_terms(&d_1)?;
            if !d_2.is_empty() {
                return Err(HigherCategoryError::DifferentialNotNilpotent {
                    degree: mor.degree,
                    details: format!(
                        "d²({mor_id}) = {d_2:?} != 0 for morphism '{mor_id}' of degree {deg}",
                        deg = mor.degree
                    ),
                });
            }
        }
        Ok(())
    }

    pub fn check_leibniz_rule(&self, g_id: &str, f_id: &str) -> Result<(), HigherCategoryError> {
        LeibnizSignValidator::validate(self, g_id, f_id)
    }

    pub fn check_identities_closed(&self) -> Result<(), HigherCategoryError> {
        for (obj_id, id_mor) in &self.identities {
            let d_id = self.differential_of(id_mor);
            if !d_id.is_empty() {
                return Err(HigherCategoryError::DifferentialNotNilpotent {
                    degree: 0,
                    details: format!(
                        "Identity morphism '{id_mor}' for object '{obj_id}' is not closed: d(id) = {d_id:?}"
                    ),
                });
            }
        }
        Ok(())
    }

    pub fn validate_all(&self) -> Result<(), HigherCategoryError> {
        self.check_nilpotence()?;
        self.check_identities_closed()?;
        for (g_id, f_id) in self.composition_table.keys() {
            self.check_leibniz_rule(g_id, f_id)?;
        }
        Ok(())
    }

    pub fn compute_h0(&self) -> Result<CohomologyCategoryH0, HigherCategoryError> {
        let mut zero_cycles: BTreeMap<(String, String), Vec<String>> = BTreeMap::new();
        let mut zero_boundaries: BTreeMap<(String, String), Vec<String>> = BTreeMap::new();

        for (mor_id, mor) in &self.morphisms {
            if mor.degree == 0 {
                let key = (mor.src.clone(), mor.tgt.clone());
                let d_val = self.differential_of(mor_id);
                if d_val.is_empty() {
                    let entry = zero_cycles.entry(key.clone()).or_default();
                    reserve_exact(entry, 1, &self.limits)?;
                    entry.push(mor_id.clone());
                }
            } else if mor.degree == -1 {
                let key = (mor.src.clone(), mor.tgt.clone());
                let d_val = self.differential_of(mor_id);
                for (_coeff, target_gen) in d_val {
                    let entry = zero_boundaries.entry(key.clone()).or_default();
                    if !entry.contains(&target_gen) {
                        reserve_exact(entry, 1, &self.limits)?;
                        entry.push(target_gen);
                    }
                }
            }
        }

        Ok(CohomologyCategoryH0 {
            objects: self.objects.clone(),
            zero_cycles,
            zero_boundaries,
        })
    }

    pub fn content_hash(&self) -> String {
        let mut hasher = Sha256::new();
        hasher.update(self.name.as_bytes());
        for obj in &self.objects {
            hasher.update(obj.as_bytes());
        }
        for (id, mor) in &self.morphisms {
            hasher.update(id.as_bytes());
            hasher.update(mor.src.as_bytes());
            hasher.update(mor.tgt.as_bytes());
            hasher.update(&mor.degree.to_be_bytes());
        }
        for (obj_id, id_mor) in &self.identities {
            hasher.update(obj_id.as_bytes());
            hasher.update(id_mor.as_bytes());
        }
        for ((src, tgt), hom) in &self.hom_complexes {
            hasher.update(src.as_bytes());
            hasher.update(tgt.as_bytes());
            hasher.update(&hom.differential.degree_shift.to_be_bytes());
            for (mor_id, terms) in &hom.differential.map {
                hasher.update(mor_id.as_bytes());
                for (coeff, target_gen) in terms {
                    hasher.update(&coeff.to_be_bytes());
                    hasher.update(target_gen.as_bytes());
                }
            }
        }
        for ((g, f), terms) in &self.composition_table {
            hasher.update(g.as_bytes());
            hasher.update(f.as_bytes());
            for (c, gen) in terms {
                hasher.update(&c.to_be_bytes());
                hasher.update(gen.as_bytes());
            }
        }
        format!("{:x}", hasher.finalize())
    }
}
