
use std::collections::{BTreeMap, BTreeSet};

use engine_kernel::resource_limits::OperationLimits;
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};

use crate::error::{reserve_exact, HigherCategoryError};

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct TranslationFunctor {
    pub object_shifts: BTreeMap<String, String>,
    pub morphism_shifts: BTreeMap<String, String>,
}

impl Default for TranslationFunctor {
    fn default() -> Self {
        Self::new()
    }
}

impl TranslationFunctor {
    pub fn new() -> Self {
        Self {
            object_shifts: BTreeMap::new(),
            morphism_shifts: BTreeMap::new(),
        }
    }

    pub fn register_object_shift(&mut self, orig: &str, shifted: &str) {
        self.object_shifts
            .insert(orig.to_string(), shifted.to_string());
    }

    pub fn register_morphism_shift(&mut self, orig: &str, shifted: &str) {
        self.morphism_shifts
            .insert(orig.to_string(), shifted.to_string());
    }

    pub fn shift_object(&self, orig: &str) -> String {
        self.object_shifts
            .get(orig)
            .cloned()
            .unwrap_or_else(|| format!("{orig}[1]"))
    }

    pub fn shift_morphism(&self, orig: &str) -> String {
        self.morphism_shifts
            .get(orig)
            .cloned()
            .unwrap_or_else(|| format!("{orig}[1]"))
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct DistinguishedTriangle {
    pub id: String,
    pub x: String,
    pub y: String,
    pub z: String,
    pub u: String,
    pub v: String,
    pub w: String,
    pub shifted_x: String,
    pub w_sign: i8,
}

impl DistinguishedTriangle {
    pub fn new(
        id: &str,
        x: &str,
        y: &str,
        z: &str,
        u: &str,
        v: &str,
        w: &str,
        shifted_x: &str,
    ) -> Self {
        Self {
            id: id.to_string(),
            x: x.to_string(),
            y: y.to_string(),
            z: z.to_string(),
            u: u.to_string(),
            v: v.to_string(),
            w: w.to_string(),
            shifted_x: shifted_x.to_string(),
            w_sign: 1,
        }
    }

    pub fn with_sign(
        id: &str,
        x: &str,
        y: &str,
        z: &str,
        u: &str,
        v: &str,
        w: &str,
        shifted_x: &str,
        w_sign: i8,
    ) -> Self {
        Self {
            id: id.to_string(),
            x: x.to_string(),
            y: y.to_string(),
            z: z.to_string(),
            u: u.to_string(),
            v: v.to_string(),
            w: w.to_string(),
            shifted_x: shifted_x.to_string(),
            w_sign,
        }
    }
}

pub struct RotationValidator;

impl RotationValidator {
    pub fn validate_rotation(
        orig: &DistinguishedTriangle,
        rotated: &DistinguishedTriangle,
        shift: &TranslationFunctor,
    ) -> Result<(), HigherCategoryError> {
        let expected_shifted_x = shift.shift_object(&orig.x);
        let expected_shifted_y = shift.shift_object(&orig.y);
        let expected_shifted_u = shift.shift_morphism(&orig.u);

        if rotated.x != orig.y {
            return Err(HigherCategoryError::RotationAxiomViolation {
                details: format!(
                    "Rotated 0-cell X mismatch: expected orig.Y='{}', found '{}'",
                    orig.y, rotated.x
                ),
            });
        }
        if rotated.y != orig.z {
            return Err(HigherCategoryError::RotationAxiomViolation {
                details: format!(
                    "Rotated 0-cell Y mismatch: expected orig.Z='{}', found '{}'",
                    orig.z, rotated.y
                ),
            });
        }
        if rotated.z != orig.shifted_x && rotated.z != expected_shifted_x {
            return Err(HigherCategoryError::RotationAxiomViolation {
                details: format!(
                    "Rotated 0-cell Z mismatch: expected orig.X[1]='{expected_shifted_x}', found '{}'",
                    rotated.z
                ),
            });
        }
        if rotated.shifted_x != expected_shifted_y {
            return Err(HigherCategoryError::RotationAxiomViolation {
                details: format!(
                    "Rotated 0-cell shifted_X mismatch: expected Y[1]='{expected_shifted_y}', found '{}'",
                    rotated.shifted_x
                ),
            });
        }

        if rotated.u != orig.v {
            return Err(HigherCategoryError::RotationAxiomViolation {
                details: format!(
                    "Rotated 1-cell u mismatch: expected orig.v='{}', found '{}'",
                    orig.v, rotated.u
                ),
            });
        }
        if rotated.v != orig.w {
            return Err(HigherCategoryError::RotationAxiomViolation {
                details: format!(
                    "Rotated 1-cell v mismatch: expected orig.w='{}', found '{}'",
                    orig.w, rotated.v
                ),
            });
        }
        if rotated.w != expected_shifted_u && rotated.w != format!("{}[1]", orig.u) {
            return Err(HigherCategoryError::RotationAxiomViolation {
                details: format!(
                    "Rotated 1-cell w morphism mismatch: expected u[1]='{expected_shifted_u}', found '{}'",
                    rotated.w
                ),
            });
        }

        if rotated.w_sign != -1 {
            return Err(HigherCategoryError::RotationAxiomViolation {
                details: format!(
                    "TR2 sign violation: rotated third morphism '{w}' has sign {sign}, must be -1 for -u[1]",
                    w = rotated.w,
                    sign = rotated.w_sign
                ),
            });
        }

        Ok(())
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct OctahedralDiagram {
    pub id: String,
    pub x: String,
    pub y: String,
    pub z: String,
    pub u: String,
    pub v: String,
    pub vu: String,
    pub tri_u: DistinguishedTriangle,
    pub tri_v: DistinguishedTriangle,
    pub tri_vu: DistinguishedTriangle,
    pub tri_cone: DistinguishedTriangle,
    pub f: String,
    pub g: String,
    pub h: String,
}

pub struct OctahedralBraidValidator;

impl OctahedralBraidValidator {
    pub fn validate(
        cat: &TriangulatedCategory,
        oct: &OctahedralDiagram,
    ) -> Result<(), HigherCategoryError> {
        if !cat.distinguished_triangles.contains_key(&oct.tri_u.id) {
            return Err(HigherCategoryError::OctahedralAxiomViolation {
                details: format!("tri_u '{}' is not distinguished", oct.tri_u.id),
            });
        }
        if !cat.distinguished_triangles.contains_key(&oct.tri_v.id) {
            return Err(HigherCategoryError::OctahedralAxiomViolation {
                details: format!("tri_v '{}' is not distinguished", oct.tri_v.id),
            });
        }
        if !cat.distinguished_triangles.contains_key(&oct.tri_vu.id) {
            return Err(HigherCategoryError::OctahedralAxiomViolation {
                details: format!("tri_vu '{}' is not distinguished", oct.tri_vu.id),
            });
        }
        if !cat.distinguished_triangles.contains_key(&oct.tri_cone.id) {
            return Err(HigherCategoryError::OctahedralAxiomViolation {
                details: format!("tri_cone '{}' is not distinguished", oct.tri_cone.id),
            });
        }

        if oct.tri_u.x != oct.x || oct.tri_u.y != oct.y {
            return Err(HigherCategoryError::OctahedralAxiomViolation {
                details: "tri_u objects do not match (X, Y)".to_string(),
            });
        }
        if oct.tri_v.x != oct.y || oct.tri_v.y != oct.z {
            return Err(HigherCategoryError::OctahedralAxiomViolation {
                details: "tri_v objects do not match (Y, Z)".to_string(),
            });
        }
        if oct.tri_vu.x != oct.x || oct.tri_vu.y != oct.z {
            return Err(HigherCategoryError::OctahedralAxiomViolation {
                details: "tri_vu objects do not match (X, Z)".to_string(),
            });
        }

        let cu = &oct.tri_u.z;
        let cv = &oct.tri_v.z;
        let cvu = &oct.tri_vu.z;
        if &oct.tri_cone.x != cu || &oct.tri_cone.y != cvu || &oct.tri_cone.z != cv {
            return Err(HigherCategoryError::OctahedralAxiomViolation {
                details: format!(
                    "tri_cone boundary mismatch: expected ({cu}, {cvu}, {cv}), found ({}, {}, {})",
                    oct.tri_cone.x, oct.tri_cone.y, oct.tri_cone.z
                ),
            });
        }

        let i = &oct.tri_u.v;
        let v = &oct.v;
        let m = &oct.tri_vu.v;
        let comp_fi = cat.compose(i, &oct.f);
        let comp_mv = cat.compose(v, m);
        if let (Ok(fi), Ok(mv)) = (comp_fi, comp_mv) {
            if fi != mv && !cat.are_morphisms_isomorphic(&fi, &mv) {
                return Err(HigherCategoryError::OctahedralAxiomViolation {
                    details: format!("Face commutativity failed: f ∘ i '{fi}' != m ∘ v '{mv}'"),
                });
            }
        }

        let comp_gm = cat.compose(m, &oct.g);
        let k = &oct.tri_v.v;
        if let Ok(gm) = comp_gm {
            if &gm != k && !cat.are_morphisms_isomorphic(&gm, k) {
                return Err(HigherCategoryError::OctahedralAxiomViolation {
                    details: format!("Face commutativity failed: g ∘ m '{gm}' != k '{k}'"),
                });
            }
        }

        Ok(())
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct TriangulatedCategory {
    pub name: String,
    pub objects: BTreeSet<String>,
    pub morphisms: BTreeMap<String, (String, String)>,
    pub composition_table: BTreeMap<(String, String), String>,
    pub shift: TranslationFunctor,
    pub distinguished_triangles: BTreeMap<String, DistinguishedTriangle>,
    pub limits: OperationLimits,
}

impl TriangulatedCategory {
    pub fn new(name: &str) -> Self {
        Self::with_limits(name, OperationLimits::default())
    }

    pub fn with_limits(name: &str, limits: OperationLimits) -> Self {
        Self {
            name: name.to_string(),
            objects: BTreeSet::new(),
            morphisms: BTreeMap::new(),
            composition_table: BTreeMap::new(),
            shift: TranslationFunctor::new(),
            distinguished_triangles: BTreeMap::new(),
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
        self.morphisms.insert(id.to_string(), (src.to_string(), tgt.to_string()));
        Ok(())
    }

    pub fn set_composition(
        &mut self,
        first: &str,
        second: &str,
        comp: &str,
    ) -> Result<(), HigherCategoryError> {
        let (f_src, f_tgt) = self.morphisms.get(first).ok_or_else(|| {
            HigherCategoryError::OneCellNotFound { id: first.to_string() }
        })?;
        let (s_src, s_tgt) = self.morphisms.get(second).ok_or_else(|| {
            HigherCategoryError::OneCellNotFound { id: second.to_string() }
        })?;

        if f_tgt != s_src {
            return Err(HigherCategoryError::OneCellNotComposable {
                first: first.to_string(),
                second: second.to_string(),
                tgt: f_tgt.clone(),
                src: s_src.clone(),
            });
        }

        let (c_src, c_tgt) = self.morphisms.get(comp).ok_or_else(|| {
            HigherCategoryError::OneCellNotFound { id: comp.to_string() }
        })?;

        if c_src != f_src || c_tgt != s_tgt {
            return Err(HigherCategoryError::BoundaryMismatch {
                expected: format!("src={f_src}, tgt={s_tgt}"),
                found: format!("src={c_src}, tgt={c_tgt}"),
            });
        }

        self.composition_table
            .insert((first.to_string(), second.to_string()), comp.to_string());
        Ok(())
    }

    pub fn compose(&self, first: &str, second: &str) -> Result<String, HigherCategoryError> {
        self.composition_table
            .get(&(first.to_string(), second.to_string()))
            .cloned()
            .ok_or_else(|| HigherCategoryError::OneCellNotComposable {
                first: first.to_string(),
                second: second.to_string(),
                tgt: "unknown".to_string(),
                src: "unknown".to_string(),
            })
    }

    pub fn are_morphisms_isomorphic(&self, m1: &str, m2: &str) -> bool {
        m1 == m2
    }

    pub fn add_distinguished_triangle(
        &mut self,
        tri: DistinguishedTriangle,
    ) -> Result<(), HigherCategoryError> {
        if self.distinguished_triangles.contains_key(&tri.id) {
            return Err(HigherCategoryError::DuplicateCell { id: tri.id });
        }
        if self.distinguished_triangles.len() >= self.limits.max_cells {
            return Err(HigherCategoryError::AllocationLimitExceeded {
                requested: self.distinguished_triangles.len() + 1,
                limit: self.limits.max_cells,
            });
        }
        self.distinguished_triangles.insert(tri.id.clone(), tri);
        Ok(())
    }

    pub fn rotate_triangle(
        &self,
        tri_id: &str,
    ) -> Result<DistinguishedTriangle, HigherCategoryError> {
        let orig = self
            .distinguished_triangles
            .get(tri_id)
            .ok_or_else(|| HigherCategoryError::OneCellNotFound { id: tri_id.to_string() })?;

        let rotated_id = format!("Rot({})", orig.id);
        let shifted_x = self.shift.shift_object(&orig.x);
        let shifted_y = self.shift.shift_object(&orig.y);
        let shifted_u = self.shift.shift_morphism(&orig.u);

        Ok(DistinguishedTriangle {
            id: rotated_id,
            x: orig.y.clone(),
            y: orig.z.clone(),
            z: shifted_x,
            u: orig.v.clone(),
            v: orig.w.clone(),
            w: shifted_u,
            shifted_x: shifted_y,
            w_sign: -1,
        })
    }

    pub fn check_rotation_axiom(
        &self,
        orig_id: &str,
        rot_id: &str,
    ) -> Result<(), HigherCategoryError> {
        let orig = self
            .distinguished_triangles
            .get(orig_id)
            .ok_or_else(|| HigherCategoryError::OneCellNotFound { id: orig_id.to_string() })?;
        let rot = self
            .distinguished_triangles
            .get(rot_id)
            .ok_or_else(|| HigherCategoryError::OneCellNotFound { id: rot_id.to_string() })?;

        RotationValidator::validate_rotation(orig, rot, &self.shift)
    }

    pub fn check_octahedral_axiom(
        &self,
        oct: &OctahedralDiagram,
    ) -> Result<(), HigherCategoryError> {
        OctahedralBraidValidator::validate(self, oct)
    }

    pub fn all_triangles(&self) -> Result<Vec<DistinguishedTriangle>, HigherCategoryError> {
        let mut list = Vec::new();
        for tri in self.distinguished_triangles.values() {
            reserve_exact(&mut list, 1, &self.limits)?;
            list.push(tri.clone());
        }
        Ok(list)
    }

    pub fn content_hash(&self) -> String {
        let mut hasher = Sha256::new();
        hasher.update(self.name.as_bytes());
        for obj in &self.objects {
            hasher.update(obj.as_bytes());
        }
        for (id, (src, tgt)) in &self.morphisms {
            hasher.update(id.as_bytes());
            hasher.update(src.as_bytes());
            hasher.update(tgt.as_bytes());
        }
        for (id, tri) in &self.distinguished_triangles {
            hasher.update(id.as_bytes());
            hasher.update(tri.x.as_bytes());
            hasher.update(tri.y.as_bytes());
            hasher.update(tri.z.as_bytes());
            hasher.update(&tri.w_sign.to_be_bytes());
        }
        format!("{:x}", hasher.finalize())
    }
}
