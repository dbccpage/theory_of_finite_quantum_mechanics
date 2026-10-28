
use std::collections::{BTreeMap, BTreeSet};

use engine_kernel::resource_limits::OperationLimits;
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};

use crate::dg_category::{add_terms, canonicalize_terms, scale_terms};
use crate::error::{reserve_exact, HigherCategoryError};

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct ChainComplex {
    pub id: String,
    pub components: BTreeMap<i32, Vec<String>>,
    pub differentials: BTreeMap<i32, BTreeMap<String, Vec<(i64, String)>>>,
}

impl ChainComplex {
    pub fn new(id: &str) -> Self {
        Self {
            id: id.to_string(),
            components: BTreeMap::new(),
            differentials: BTreeMap::new(),
        }
    }

    pub fn add_generator(&mut self, degree: i32, gen: &str) {
        let entry = self.components.entry(degree).or_default();
        if !entry.contains(&gen.to_string()) {
            entry.push(gen.to_string());
        }
    }

    pub fn set_differential(
        &mut self,
        degree: i32,
        gen: &str,
        target_terms: Vec<(i64, String)>,
    ) {
        self.differentials
            .entry(degree)
            .or_default()
            .insert(gen.to_string(), canonicalize_terms(&target_terms));
    }

    pub fn differential_of(&self, degree: i32, gen: &str) -> Vec<(i64, String)> {
        self.differentials
            .get(&degree)
            .and_then(|m| m.get(gen))
            .cloned()
            .unwrap_or_default()
    }

    pub fn apply_differential_to_terms(
        &self,
        degree: i32,
        terms: &[(i64, String)],
    ) -> Vec<(i64, String)> {
        let mut result = Vec::new();
        for (coeff, gen) in terms {
            let d_gen = self.differential_of(degree, gen);
            let scaled = scale_terms(&d_gen, *coeff);
            result = add_terms(&result, &scaled);
        }
        result
    }

    pub fn check_nilpotence(&self) -> Result<(), HigherCategoryError> {
        for (&deg, generators) in &self.components {
            for gen in generators {
                let d1 = self.differential_of(deg, gen);
                let d2 = self.apply_differential_to_terms(deg - 1, &d1);
                if !d2.is_empty() {
                    return Err(HigherCategoryError::DifferentialNotNilpotent {
                        degree: deg,
                        details: format!(
                            "d²({gen}) = {d2:?} != 0 in complex '{id}' at degree {deg}",
                            id = self.id
                        ),
                    });
                }
            }
        }
        Ok(())
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct ChainMap {
    pub id: String,
    pub src_complex: String,
    pub tgt_complex: String,
    pub components: BTreeMap<i32, BTreeMap<String, Vec<(i64, String)>>>,
}

impl ChainMap {
    pub fn new(id: &str, src: &str, tgt: &str) -> Self {
        Self {
            id: id.to_string(),
            src_complex: src.to_string(),
            tgt_complex: tgt.to_string(),
            components: BTreeMap::new(),
        }
    }

    pub fn set_component(
        &mut self,
        degree: i32,
        src_gen: &str,
        target_terms: Vec<(i64, String)>,
    ) {
        self.components
            .entry(degree)
            .or_default()
            .insert(src_gen.to_string(), canonicalize_terms(&target_terms));
    }

    pub fn apply_to_gen(&self, degree: i32, src_gen: &str) -> Vec<(i64, String)> {
        self.components
            .get(&degree)
            .and_then(|m| m.get(src_gen))
            .cloned()
            .unwrap_or_default()
    }

    pub fn apply_to_terms(
        &self,
        degree: i32,
        terms: &[(i64, String)],
    ) -> Vec<(i64, String)> {
        let mut result = Vec::new();
        for (coeff, gen) in terms {
            let f_gen = self.apply_to_gen(degree, gen);
            let scaled = scale_terms(&f_gen, *coeff);
            result = add_terms(&result, &scaled);
        }
        result
    }

    pub fn check_commutes_with_differential(
        &self,
        x: &ChainComplex,
        y: &ChainComplex,
    ) -> Result<(), HigherCategoryError> {
        for (&deg, generators) in &x.components {
            for gen in generators {
                let f_x = self.apply_to_gen(deg, gen);
                let d_y_f_x = y.apply_differential_to_terms(deg, &f_x);

                let d_x = x.differential_of(deg, gen);
                let f_d_x = self.apply_to_terms(deg - 1, &d_x);

                if d_y_f_x != f_d_x {
                    return Err(HigherCategoryError::DifferentialNotNilpotent {
                        degree: deg,
                        details: format!(
                            "Chain map '{id}' fails d_Y ∘ f == f ∘ d_X on gen '{gen}' at degree {deg}: LHS={d_y_f_x:?} != RHS={f_d_x:?}",
                            id = self.id
                        ),
                    });
                }
            }
        }
        Ok(())
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct ConeDifferentialMatrix {
    pub degree: i32,
    pub d_y_sign: i8,
    pub f_sign: i8,
    pub d_x_sign: i8,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct MappingCone {
    pub id: String,
    pub chain_map_id: String,
    pub source_complex_id: String,
    pub target_complex_id: String,
    pub cone_complex: ChainComplex,
    pub block_matrices: BTreeMap<i32, ConeDifferentialMatrix>,
}

impl MappingCone {
    pub fn construct(
        map: &ChainMap,
        x: &ChainComplex,
        y: &ChainComplex,
        limits: &OperationLimits,
    ) -> Result<Self, HigherCategoryError> {
        map.check_commutes_with_differential(x, y)?;
        x.check_nilpotence()?;
        y.check_nilpotence()?;

        let cone_id = format!("Cone({})", map.id);
        let mut cone = ChainComplex::new(&cone_id);
        let mut block_matrices = BTreeMap::new();

        let mut degrees = BTreeSet::new();
        for &deg in y.components.keys() {
            degrees.insert(deg);
        }
        for &deg in x.components.keys() {
            degrees.insert(deg + 1);
        }

        if degrees.len() >= limits.max_cells {
            return Err(HigherCategoryError::AllocationLimitExceeded {
                requested: degrees.len(),
                limit: limits.max_cells,
            });
        }

        for &deg in &degrees {
            if let Some(y_gens) = y.components.get(&deg) {
                let entry = cone.components.entry(deg).or_default();
                reserve_exact(entry, y_gens.len(), limits)?;
                for gen in y_gens {
                    entry.push(format!("Y::{gen}"));
                }
            }
            if let Some(x_gens) = x.components.get(&(deg - 1)) {
                let entry = cone.components.entry(deg).or_default();
                reserve_exact(entry, x_gens.len(), limits)?;
                for gen in x_gens {
                    entry.push(format!("X1::{gen}"));
                }
            }
        }

        for &deg in &degrees {
            block_matrices.insert(
                deg,
                ConeDifferentialMatrix {
                    degree: deg,
                    d_y_sign: 1,
                    f_sign: 1,
                    d_x_sign: -1,
                },
            );

            if let Some(y_gens) = y.components.get(&deg) {
                for gen in y_gens {
                    let d_y = y.differential_of(deg, gen);
                    let mapped_terms: Vec<(i64, String)> = d_y
                        .into_iter()
                        .map(|(c, g)| (c, format!("Y::{g}")))
                        .collect();
                    cone.set_differential(deg, &format!("Y::{gen}"), mapped_terms);
                }
            }

            let x_deg = deg - 1;
            if let Some(x_gens) = x.components.get(&x_deg) {
                for gen in x_gens {
                    let f_x = map.apply_to_gen(x_deg, gen);
                    let mut terms: Vec<(i64, String)> = f_x
                        .into_iter()
                        .map(|(c, g)| (c, format!("Y::{g}")))
                        .collect();

                    let d_x = x.differential_of(x_deg, gen);
                    let neg_d_x: Vec<(i64, String)> = d_x
                        .into_iter()
                        .map(|(c, g)| (-c, format!("X1::{g}")))
                        .collect();

                    terms.extend(neg_d_x);
                    cone.set_differential(deg, &format!("X1::{gen}"), canonicalize_terms(&terms));
                }
            }
        }

        cone.check_nilpotence()?;

        Ok(Self {
            id: cone_id,
            chain_map_id: map.id.clone(),
            source_complex_id: x.id.clone(),
            target_complex_id: y.id.clone(),
            cone_complex: cone,
            block_matrices,
        })
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct QuasiIsomorphism {
    pub chain_map_id: String,
    pub is_quasi_iso: bool,
    pub degrees_checked: Vec<i32>,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct DerivedCategory {
    pub name: String,
    pub complexes: BTreeMap<String, ChainComplex>,
    pub chain_maps: BTreeMap<String, ChainMap>,
    pub mapping_cones: BTreeMap<String, MappingCone>,
    pub limits: OperationLimits,
}

impl DerivedCategory {
    pub fn new(name: &str) -> Self {
        Self::with_limits(name, OperationLimits::default())
    }

    pub fn with_limits(name: &str, limits: OperationLimits) -> Self {
        Self {
            name: name.to_string(),
            complexes: BTreeMap::new(),
            chain_maps: BTreeMap::new(),
            mapping_cones: BTreeMap::new(),
            limits,
        }
    }

    pub fn add_complex(&mut self, complex: ChainComplex) -> Result<(), HigherCategoryError> {
        if self.complexes.contains_key(&complex.id) {
            return Err(HigherCategoryError::DuplicateCell { id: complex.id });
        }
        if self.complexes.len() >= self.limits.max_cells {
            return Err(HigherCategoryError::AllocationLimitExceeded {
                requested: self.complexes.len() + 1,
                limit: self.limits.max_cells,
            });
        }
        complex.check_nilpotence()?;
        self.complexes.insert(complex.id.clone(), complex);
        Ok(())
    }

    pub fn add_chain_map(&mut self, map: ChainMap) -> Result<(), HigherCategoryError> {
        if self.chain_maps.contains_key(&map.id) {
            return Err(HigherCategoryError::DuplicateCell { id: map.id });
        }
        let src = self
            .complexes
            .get(&map.src_complex)
            .ok_or_else(|| HigherCategoryError::OneCellNotFound {
                id: map.src_complex.clone(),
            })?;
        let tgt = self
            .complexes
            .get(&map.tgt_complex)
            .ok_or_else(|| HigherCategoryError::OneCellNotFound {
                id: map.tgt_complex.clone(),
            })?;

        map.check_commutes_with_differential(src, tgt)?;
        self.chain_maps.insert(map.id.clone(), map);
        Ok(())
    }

    pub fn construct_mapping_cone(
        &mut self,
        map_id: &str,
    ) -> Result<MappingCone, HigherCategoryError> {
        let map = self
            .chain_maps
            .get(map_id)
            .ok_or_else(|| HigherCategoryError::OneCellNotFound {
                id: map_id.to_string(),
            })?;
        let src = self.complexes.get(&map.src_complex).unwrap();
        let tgt = self.complexes.get(&map.tgt_complex).unwrap();

        let cone = MappingCone::construct(map, src, tgt, &self.limits)?;
        self.mapping_cones.insert(cone.id.clone(), cone.clone());
        Ok(cone)
    }

    pub fn check_cone_nilpotence(&self, cone_id: &str) -> Result<(), HigherCategoryError> {
        let cone = self
            .mapping_cones
            .get(cone_id)
            .ok_or_else(|| HigherCategoryError::OneCellNotFound {
                id: cone_id.to_string(),
            })?;
        cone.cone_complex.check_nilpotence()
    }

    pub fn validate_all(&self) -> Result<(), HigherCategoryError> {
        for complex in self.complexes.values() {
            complex.check_nilpotence()?;
        }
        for map in self.chain_maps.values() {
            let src = &self.complexes[&map.src_complex];
            let tgt = &self.complexes[&map.tgt_complex];
            map.check_commutes_with_differential(src, tgt)?;
        }
        for cone in self.mapping_cones.values() {
            cone.cone_complex.check_nilpotence()?;
        }
        Ok(())
    }

    pub fn content_hash(&self) -> String {
        let mut hasher = Sha256::new();
        hasher.update(self.name.as_bytes());
        for (id, comp) in &self.complexes {
            hasher.update(id.as_bytes());
            for (deg, gens) in &comp.components {
                hasher.update(&deg.to_be_bytes());
                for g in gens {
                    hasher.update(g.as_bytes());
                }
            }
            for (deg, diff_map) in &comp.differentials {
                hasher.update(&deg.to_be_bytes());
                for (gen, terms) in diff_map {
                    hasher.update(gen.as_bytes());
                    for (coeff, target_gen) in terms {
                        hasher.update(&coeff.to_be_bytes());
                        hasher.update(target_gen.as_bytes());
                    }
                }
            }
        }
        for (id, map) in &self.chain_maps {
            hasher.update(id.as_bytes());
            hasher.update(map.src_complex.as_bytes());
            hasher.update(map.tgt_complex.as_bytes());
            for (deg, comp_map) in &map.components {
                hasher.update(&deg.to_be_bytes());
                for (src_gen, terms) in comp_map {
                    hasher.update(src_gen.as_bytes());
                    for (coeff, target_gen) in terms {
                        hasher.update(&coeff.to_be_bytes());
                        hasher.update(target_gen.as_bytes());
                    }
                }
            }
        }
        for (id, cone) in &self.mapping_cones {
            hasher.update(id.as_bytes());
            hasher.update(cone.chain_map_id.as_bytes());
            hasher.update(cone.source_complex_id.as_bytes());
            hasher.update(cone.target_complex_id.as_bytes());
            for (deg, matrix) in &cone.block_matrices {
                hasher.update(&deg.to_be_bytes());
                hasher.update(&[matrix.d_y_sign as u8, matrix.f_sign as u8, matrix.d_x_sign as u8]);
            }
        }
        format!("{:x}", hasher.finalize())
    }
}
