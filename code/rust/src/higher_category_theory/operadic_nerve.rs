
use std::collections::{BTreeMap, HashMap};

use omega_kernel::resource_limits::OperationLimits;
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};

use crate::error::{reserve_exact, HigherCategoryError};
use crate::simplicial_set::{Horn, QuasiCategoryValidator, SimplicialSet};

#[derive(Debug, Clone, PartialEq, Eq, PartialOrd, Ord, Serialize, Deserialize)]
pub struct MultiAryOp {
    pub id: String,
    pub inputs: Vec<String>,
    pub output: String,
}

impl MultiAryOp {
    pub fn arity(&self) -> usize {
        self.inputs.len()
    }

    pub fn is_unary(&self) -> bool {
        self.inputs.len() == 1
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct ColouredOperad {
    pub colours: Vec<String>,
    pub operations: Vec<MultiAryOp>,
    pub id_ops: BTreeMap<String, String>,
    pub comp1_table: BTreeMap<(String, String), String>,
}

impl ColouredOperad {
    pub fn new(limits: &OperationLimits) -> Result<Self, HigherCategoryError> {
        let mut colours = Vec::new();
        reserve_exact(&mut colours, 0, limits)?;
        let mut operations = Vec::new();
        reserve_exact(&mut operations, 0, limits)?;
        Ok(Self {
            colours,
            operations,
            id_ops: BTreeMap::new(),
            comp1_table: BTreeMap::new(),
        })
    }

    pub fn add_colour(
        &mut self,
        colour: impl Into<String>,
        limits: &OperationLimits,
    ) -> Result<(), HigherCategoryError> {
        let c = colour.into();
        if self.colours.contains(&c) {
            return Err(HigherCategoryError::DuplicateCell { id: c });
        }
        reserve_exact(&mut self.colours, 1, limits)?;
        self.colours.push(c);
        Ok(())
    }

    pub fn add_unary_operation(
        &mut self,
        id: impl Into<String>,
        src: impl Into<String>,
        tgt: impl Into<String>,
        limits: &OperationLimits,
    ) -> Result<(), HigherCategoryError> {
        let id_str = id.into();
        let src_str = src.into();
        let tgt_str = tgt.into();

        if !self.colours.contains(&src_str) {
            return Err(HigherCategoryError::ZeroCellNotFound { id: src_str });
        }
        if !self.colours.contains(&tgt_str) {
            return Err(HigherCategoryError::ZeroCellNotFound { id: tgt_str });
        }
        if self.operations.iter().any(|op| op.id == id_str) {
            return Err(HigherCategoryError::DuplicateCell { id: id_str });
        }

        reserve_exact(&mut self.operations, 1, limits)?;
        self.operations.push(MultiAryOp {
            id: id_str,
            inputs: vec![src_str],
            output: tgt_str,
        });
        Ok(())
    }

    pub fn add_multi_ary_operation(
        &mut self,
        id: impl Into<String>,
        inputs: Vec<String>,
        output: impl Into<String>,
        limits: &OperationLimits,
    ) -> Result<(), HigherCategoryError> {
        let id_str = id.into();
        let out_str = output.into();

        for input in &inputs {
            if !self.colours.contains(input) {
                return Err(HigherCategoryError::ZeroCellNotFound { id: input.clone() });
            }
        }
        if !self.colours.contains(&out_str) {
            return Err(HigherCategoryError::ZeroCellNotFound { id: out_str });
        }
        if self.operations.iter().any(|op| op.id == id_str) {
            return Err(HigherCategoryError::DuplicateCell { id: id_str });
        }

        reserve_exact(&mut self.operations, 1, limits)?;
        self.operations.push(MultiAryOp {
            id: id_str,
            inputs,
            output: out_str,
        });
        Ok(())
    }

    pub fn set_identity_operation(
        &mut self,
        colour: &str,
        op_id: &str,
    ) -> Result<(), HigherCategoryError> {
        if !self.colours.iter().any(|c| c == colour) {
            return Err(HigherCategoryError::ZeroCellNotFound {
                id: colour.to_string(),
            });
        }
        let op = self
            .operations
            .iter()
            .find(|op| op.id == op_id)
            .ok_or_else(|| HigherCategoryError::OneCellNotFound {
                id: op_id.to_string(),
            })?;

        if !op.is_unary() || op.inputs[0] != colour || op.output != colour {
            return Err(HigherCategoryError::BoundaryMismatch {
                expected: format!("unary identity [c] -> c for c='{}'", colour),
                found: format!("{:?} -> {}", op.inputs, op.output),
            });
        }

        self.id_ops.insert(colour.to_string(), op_id.to_string());
        Ok(())
    }

    pub fn register_comp1(
        &mut self,
        g_id: &str,
        f_id: &str,
        gf_id: &str,
    ) -> Result<(), HigherCategoryError> {
        let f = self
            .operations
            .iter()
            .find(|op| op.id == f_id)
            .ok_or_else(|| HigherCategoryError::OneCellNotFound {
                id: f_id.to_string(),
            })?;
        let g = self
            .operations
            .iter()
            .find(|op| op.id == g_id)
            .ok_or_else(|| HigherCategoryError::OneCellNotFound {
                id: g_id.to_string(),
            })?;
        let gf = self
            .operations
            .iter()
            .find(|op| op.id == gf_id)
            .ok_or_else(|| HigherCategoryError::OneCellNotFound {
                id: gf_id.to_string(),
            })?;

        if !f.is_unary() || !g.is_unary() || !gf.is_unary() {
            return Err(HigherCategoryError::BoundaryMismatch {
                expected: "unary operations for comp1".to_string(),
                found: format!(
                    "arities: f={}, g={}, gf={}",
                    f.arity(),
                    g.arity(),
                    gf.arity()
                ),
            });
        }

        if f.output != g.inputs[0] {
            return Err(HigherCategoryError::OneCellNotComposable {
                first: f_id.to_string(),
                second: g_id.to_string(),
                tgt: f.output.clone(),
                src: g.inputs[0].clone(),
            });
        }

        if gf.inputs[0] != f.inputs[0] || gf.output != g.output {
            return Err(HigherCategoryError::BoundaryMismatch {
                expected: format!("[{}] -> {}", f.inputs[0], g.output),
                found: format!("{:?} -> {}", gf.inputs, gf.output),
            });
        }

        self.comp1_table
            .insert((g_id.to_string(), f_id.to_string()), gf_id.to_string());
        Ok(())
    }

    pub fn validate_spine_associativity(&self) -> Result<(), HigherCategoryError> {
        for ((g1, f1), gf1) in &self.comp1_table {
            for ((h2, g2), hg2) in &self.comp1_table {
                if g1 == g2 {
                    let left = self.comp1_table.get(&(hg2.clone(), f1.clone()));
                    let right = self.comp1_table.get(&(h2.clone(), gf1.clone()));

                    match (left, right) {
                        (Some(l), Some(r)) => {
                            if l != r {
                                return Err(HigherCategoryError::AssociativityViolation {
                                    details: format!(
                                        "Unary spine associativity failed: ({} o_1 {}) o_1 {} = '{}' != '{}' = {} o_1 ({} o_1 {})",
                                        h2, g1, f1, l, r, h2, g1, f1
                                    ),
                                });
                            }
                        }
                        (None, Some(_)) => {
                            return Err(HigherCategoryError::AssociativityViolation {
                                details: format!(
                                    "Unary spine associativity failed: composite ({} o_1 {}) o_1 {} not registered in operad",
                                    h2, g1, f1
                                ),
                            });
                        }
                        (Some(_), None) => {
                            return Err(HigherCategoryError::AssociativityViolation {
                                details: format!(
                                    "Unary spine associativity failed: composite {} o_1 ({} o_1 {}) not registered in operad",
                                    h2, g1, f1
                                ),
                            });
                        }
                        (None, None) => {}
                    }
                }
            }
        }
        Ok(())
    }

    pub fn validate_spine_unitality(&self) -> Result<(), HigherCategoryError> {
        for op in &self.operations {
            if op.is_unary() {
                let a = &op.inputs[0];
                let b = &op.output;

                if let Some(id_b) = self.id_ops.get(b) {
                    if let Some(composite) = self.comp1_table.get(&(id_b.clone(), op.id.clone())) {
                        if composite != &op.id {
                            return Err(HigherCategoryError::UnitLawViolation {
                                details: format!(
                                    "Left unitality failed for '{}': id_{} o_1 {} = '{}' != '{}'",
                                    op.id, b, op.id, composite, op.id
                                ),
                            });
                        }
                    }
                }

                if let Some(id_a) = self.id_ops.get(a) {
                    if let Some(composite) = self.comp1_table.get(&(op.id.clone(), id_a.clone())) {
                        if composite != &op.id {
                            return Err(HigherCategoryError::UnitLawViolation {
                                details: format!(
                                    "Right unitality failed for '{}': {} o_1 id_{} = '{}' != '{}'",
                                    op.id, op.id, a, composite, op.id
                                ),
                            });
                        }
                    }
                }
            }
        }
        Ok(())
    }

    pub fn canonical_hash(&self) -> String {
        let mut hasher = Sha256::new();
        hasher.update(b"COLORED_OPERAD_V1:");
        for c in &self.colours {
            hasher.update(c.as_bytes());
            hasher.update(b";");
        }
        for op in &self.operations {
            hasher.update(op.id.as_bytes());
            hasher.update(b":");
            for inp in &op.inputs {
                hasher.update(inp.as_bytes());
                hasher.update(b",");
            }
            hasher.update(b"->");
            hasher.update(op.output.as_bytes());
            hasher.update(b";");
        }
        for ((g, f), gf) in &self.comp1_table {
            hasher.update(g.as_bytes());
            hasher.update(b"o");
            hasher.update(f.as_bytes());
            hasher.update(b"=");
            hasher.update(gf.as_bytes());
            hasher.update(b";");
        }
        format!("{:x}", hasher.finalize())
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct OperadNerve0 {
    pub colour: String,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct OperadNerve1 {
    pub c0: String,
    pub c1: String,
    pub f: String,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct OperadNerve2 {
    pub c0: String,
    pub c1: String,
    pub c2: String,
    pub f01: String,
    pub f12: String,
    pub f02: String,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct InnerHorn2_1 {
    pub x0: OperadNerve1,
    pub x2: OperadNerve1,
}

impl InnerHorn2_1 {
    pub fn new(x0: OperadNerve1, x2: OperadNerve1) -> Result<Self, HigherCategoryError> {
        if x2.c1 != x0.c0 {
            return Err(HigherCategoryError::OperadicNerveBoundaryMismatch {
                details: format!(
                    "Inner horn Lambda^1_2 compatibility violated: target of d2 ('{}') != source of d0 ('{}')",
                    x2.c1, x0.c0
                ),
            });
        }
        Ok(Self { x0, x2 })
    }
}

pub fn fill_inner_horn_2_1(
    operad: &ColouredOperad,
    horn: &InnerHorn2_1,
) -> Result<OperadNerve2, HigherCategoryError> {
    if horn.x2.c1 != horn.x0.c0 {
        return Err(HigherCategoryError::OperadicNerveBoundaryMismatch {
            details: format!(
                "Inner horn boundary mismatch: x2.c1='{}' != x0.c0='{}'",
                horn.x2.c1, horn.x0.c0
            ),
        });
    }

    let f02 = operad
        .comp1_table
        .get(&(horn.x0.f.clone(), horn.x2.f.clone()))
        .cloned()
        .ok_or_else(|| HigherCategoryError::InnerHornFillingViolation {
            dimension: 2,
            k: 1,
            details: format!(
                "Operadic composition {} o_1 {} not defined in operad",
                horn.x0.f, horn.x2.f
            ),
        })?;

    let filler = OperadNerve2 {
        c0: horn.x2.c0.clone(),
        c1: horn.x2.c1.clone(),
        c2: horn.x0.c1.clone(),
        f01: horn.x2.f.clone(),
        f12: horn.x0.f.clone(),
        f02: f02.clone(),
    };

    if filler.c1 != horn.x0.c0 || filler.c2 != horn.x0.c1 || filler.f12 != horn.x0.f {
        return Err(HigherCategoryError::OperadicNerveBoundaryMismatch {
            details: format!("Face d0 does not match x0: expected {:?}, actual d0", horn.x0),
        });
    }

    if filler.c0 != horn.x2.c0 || filler.c1 != horn.x2.c1 || filler.f01 != horn.x2.f {
        return Err(HigherCategoryError::OperadicNerveBoundaryMismatch {
            details: format!("Face d2 does not match x2: expected {:?}, actual d2", horn.x2),
        });
    }

    Ok(filler)
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct OperadicNerve {
    pub operad_hash: String,
    pub simplicial_set: SimplicialSet,
    pub inner_horns_verified: usize,
}

impl OperadicNerve {
    pub fn from_coloured_operad(
        operad: &ColouredOperad,
        limits: &OperationLimits,
    ) -> Result<Self, HigherCategoryError> {
        operad.validate_spine_associativity()?;
        operad.validate_spine_unitality()?;

        let mut sset = SimplicialSet::new(2, limits)?;

        for c in &operad.colours {
            sset.add_simplex(0, c, limits)?;
        }

        for op in &operad.operations {
            if op.is_unary() {
                sset.add_simplex(1, &op.id, limits)?;
                sset.set_face(1, 0, &op.id, &op.output)?;
                sset.set_face(1, 1, &op.id, &op.inputs[0])?;
            }
        }

        for (c, id_op) in &operad.id_ops {
            sset.set_degeneracy(0, 0, c, id_op)?;
        }

        let mut horn_count = 0;
        for ((g_id, f_id), gf_id) in &operad.comp1_table {
            let f = operad.operations.iter().find(|op| &op.id == f_id).unwrap();
            let g = operad.operations.iter().find(|op| &op.id == g_id).unwrap();

            let tri_id = format!("tri_{}_{}", f_id, g_id);
            sset.add_simplex(2, &tri_id, limits)?;

            sset.set_face(2, 0, &tri_id, g_id)?;
            sset.set_face(2, 1, &tri_id, gf_id)?;
            sset.set_face(2, 2, &tri_id, f_id)?;

            let horn_x0 = OperadNerve1 {
                c0: g.inputs[0].clone(),
                c1: g.output.clone(),
                f: g_id.clone(),
            };
            let horn_x2 = OperadNerve1 {
                c0: f.inputs[0].clone(),
                c1: f.output.clone(),
                f: f_id.clone(),
            };
            let horn = InnerHorn2_1::new(horn_x0, horn_x2)?;
            let filler = fill_inner_horn_2_1(operad, &horn)?;
            assert_eq!(&filler.f02, gf_id);
            horn_count += 1;
        }

        Ok(Self {
            operad_hash: operad.canonical_hash(),
            simplicial_set: sset,
            inner_horns_verified: horn_count,
        })
    }

    pub fn verify_quasi_category_property(&self) -> Result<bool, HigherCategoryError> {
        let mut horns = Vec::new();
        let one_simplices = &self.simplicial_set.simplices_by_dim[1];
        for f in one_simplices {
            let f_tgt = self.simplicial_set.face_maps.get(&(1, 0, f.id.clone()));
            for g in one_simplices {
                let g_src = self.simplicial_set.face_maps.get(&(1, 1, g.id.clone()));
                if let (Some(tgt), Some(src)) = (f_tgt, g_src) {
                    if tgt == src {
                        let mut faces = HashMap::new();
                        faces.insert(0, g.id.clone());
                        faces.insert(2, f.id.clone());
                        horns.push(Horn {
                            dimension: 2,
                            omitted_index: 1,
                            faces,
                        });
                    }
                }
            }
        }
        QuasiCategoryValidator::verify_inner_horns(&self.simplicial_set, &horns)?;
        Ok(true)
    }

    pub fn canonical_hash(&self) -> String {
        let mut hasher = Sha256::new();
        hasher.update(b"OPERADIC_NERVE_V1:");
        hasher.update(self.operad_hash.as_bytes());
        hasher.update(b":HORNS=");
        hasher.update(self.inner_horns_verified.to_string().as_bytes());
        format!("{:x}", hasher.finalize())
    }
}
