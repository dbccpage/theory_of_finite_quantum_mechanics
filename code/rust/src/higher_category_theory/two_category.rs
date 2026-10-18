
use crate::error::HigherCategoryError;
use omega_kernel::resource_limits::OperationLimits;
use sha2::{Digest, Sha256};
use std::collections::{BTreeMap, BTreeSet};

pub trait TwoCategory {
    type ZeroCell: Clone + Eq + std::hash::Hash + std::fmt::Debug;
    type OneCell: Clone + Eq + std::hash::Hash + std::fmt::Debug;
    type TwoCell: Clone + Eq + std::hash::Hash + std::fmt::Debug;

    fn source_0_of_1(&self, f: &Self::OneCell) -> Result<Self::ZeroCell, HigherCategoryError>;
    fn target_0_of_1(&self, f: &Self::OneCell) -> Result<Self::ZeroCell, HigherCategoryError>;

    fn source_1_of_2(&self, alpha: &Self::TwoCell) -> Result<Self::OneCell, HigherCategoryError>;
    fn target_1_of_2(&self, alpha: &Self::TwoCell) -> Result<Self::OneCell, HigherCategoryError>;

    fn id_1(&self, a: &Self::ZeroCell) -> Result<Self::OneCell, HigherCategoryError>;
    fn id_2(&self, f: &Self::OneCell) -> Result<Self::TwoCell, HigherCategoryError>;

    fn compose_1(
        &self,
        f: &Self::OneCell,
        g: &Self::OneCell,
    ) -> Result<Self::OneCell, HigherCategoryError>;

    fn compose_2_vertical(
        &self,
        alpha: &Self::TwoCell,
        beta: &Self::TwoCell,
    ) -> Result<Self::TwoCell, HigherCategoryError>;

    fn compose_2_horizontal(
        &self,
        alpha: &Self::TwoCell,
        beta: &Self::TwoCell,
    ) -> Result<Self::TwoCell, HigherCategoryError>;
}

#[derive(Debug, Clone, PartialEq, Eq, serde::Serialize, serde::Deserialize)]
pub struct OneMorphismData {
    pub id: String,
    pub src: String,
    pub tgt: String,
}

impl OneMorphismData {
    pub fn new(id: impl Into<String>, src: impl Into<String>, tgt: impl Into<String>) -> Self {
        Self {
            id: id.into(),
            src: src.into(),
            tgt: tgt.into(),
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq, serde::Serialize, serde::Deserialize)]
pub struct TwoMorphismData {
    pub id: String,
    pub src_1: String,
    pub tgt_1: String,
    pub src_0: String,
    pub tgt_0: String,
}

impl TwoMorphismData {
    pub fn new(
        id: impl Into<String>,
        src_1: impl Into<String>,
        tgt_1: impl Into<String>,
        src_0: impl Into<String>,
        tgt_0: impl Into<String>,
    ) -> Self {
        Self {
            id: id.into(),
            src_1: src_1.into(),
            tgt_1: tgt_1.into(),
            src_0: src_0.into(),
            tgt_0: tgt_0.into(),
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq, serde::Serialize, serde::Deserialize)]
pub struct Strict2Category {
    pub name: String,
    pub zero_cells: BTreeSet<String>,
    pub one_cells: BTreeMap<String, OneMorphismData>,
    pub two_cells: BTreeMap<String, TwoMorphismData>,
    pub id_1_map: BTreeMap<String, String>,
    pub id_2_map: BTreeMap<String, String>,
    pub compose_1_table: BTreeMap<(String, String), String>,
    pub compose_2_v_table: BTreeMap<(String, String), String>,
    pub compose_2_h_table: BTreeMap<(String, String), String>,
    pub limits: OperationLimits,
}

impl Strict2Category {
    pub fn new(name: impl Into<String>) -> Self {
        Self::with_limits(
            name,
            OperationLimits {
                max_cells: 100_000,
                max_operations: 1_000_000,
                ..OperationLimits::default()
            },
        )
    }

    pub fn with_limits(name: impl Into<String>, limits: OperationLimits) -> Self {
        Self {
            name: name.into(),
            zero_cells: BTreeSet::new(),
            one_cells: BTreeMap::new(),
            two_cells: BTreeMap::new(),
            id_1_map: BTreeMap::new(),
            id_2_map: BTreeMap::new(),
            compose_1_table: BTreeMap::new(),
            compose_2_v_table: BTreeMap::new(),
            compose_2_h_table: BTreeMap::new(),
            limits,
        }
    }

    pub fn add_zero_cell(&mut self, id: impl Into<String>) -> Result<(), HigherCategoryError> {
        let id_str = id.into();
        if self.zero_cells.len().saturating_add(1) > self.limits.max_cells {
            return Err(HigherCategoryError::AllocationLimitExceeded {
                requested: self.zero_cells.len().saturating_add(1),
                limit: self.limits.max_cells,
            });
        }
        if self.zero_cells.contains(&id_str) {
            return Err(HigherCategoryError::DuplicateCell { id: id_str });
        }
        self.zero_cells.insert(id_str);
        Ok(())
    }

    pub fn add_one_cell(
        &mut self,
        id: impl Into<String>,
        src: impl Into<String>,
        tgt: impl Into<String>,
    ) -> Result<(), HigherCategoryError> {
        let id_str = id.into();
        let src_str = src.into();
        let tgt_str = tgt.into();

        if self.one_cells.len().saturating_add(1) > self.limits.max_cells {
            return Err(HigherCategoryError::AllocationLimitExceeded {
                requested: self.one_cells.len().saturating_add(1),
                limit: self.limits.max_cells,
            });
        }
        if !self.zero_cells.contains(&src_str) {
            return Err(HigherCategoryError::ZeroCellNotFound { id: src_str });
        }
        if !self.zero_cells.contains(&tgt_str) {
            return Err(HigherCategoryError::ZeroCellNotFound { id: tgt_str });
        }
        if self.one_cells.contains_key(&id_str) {
            return Err(HigherCategoryError::DuplicateCell { id: id_str });
        }

        self.one_cells.insert(
            id_str.clone(),
            OneMorphismData::new(id_str, src_str, tgt_str),
        );
        Ok(())
    }

    pub fn add_two_cell(
        &mut self,
        id: impl Into<String>,
        src_1: impl Into<String>,
        tgt_1: impl Into<String>,
    ) -> Result<(), HigherCategoryError> {
        let id_str = id.into();
        let s1_str = src_1.into();
        let t1_str = tgt_1.into();

        if self.two_cells.len().saturating_add(1) > self.limits.max_cells {
            return Err(HigherCategoryError::AllocationLimitExceeded {
                requested: self.two_cells.len().saturating_add(1),
                limit: self.limits.max_cells,
            });
        }

        let s1 = self
            .one_cells
            .get(&s1_str)
            .ok_or_else(|| HigherCategoryError::OneCellNotFound { id: s1_str.clone() })?;
        let t1 = self
            .one_cells
            .get(&t1_str)
            .ok_or_else(|| HigherCategoryError::OneCellNotFound { id: t1_str.clone() })?;

        if s1.src != t1.src || s1.tgt != t1.tgt {
            return Err(HigherCategoryError::NonParallel1Cells {
                src_1: s1_str,
                tgt_1: t1_str,
            });
        }

        if self.two_cells.contains_key(&id_str) {
            return Err(HigherCategoryError::DuplicateCell { id: id_str });
        }

        let cell = TwoMorphismData::new(
            id_str.clone(),
            s1_str,
            t1_str,
            s1.src.clone(),
            s1.tgt.clone(),
        );
        self.two_cells.insert(id_str, cell);
        Ok(())
    }

    pub fn set_id_1(
        &mut self,
        ob: impl Into<String>,
        id_mor: impl Into<String>,
    ) -> Result<(), HigherCategoryError> {
        let ob_str = ob.into();
        let id_str = id_mor.into();

        if !self.zero_cells.contains(&ob_str) {
            return Err(HigherCategoryError::ZeroCellNotFound { id: ob_str });
        }
        let mor = self
            .one_cells
            .get(&id_str)
            .ok_or_else(|| HigherCategoryError::OneCellNotFound { id: id_str.clone() })?;
        if mor.src != ob_str || mor.tgt != ob_str {
            let actual = if mor.src != ob_str {
                mor.src.clone()
            } else {
                mor.tgt.clone()
            };
            return Err(HigherCategoryError::OneCellBoundaryMismatch {
                cell: id_str,
                expected_src: ob_str,
                actual_src: actual,
            });
        }
        self.id_1_map.insert(ob_str, id_str);
        Ok(())
    }

    pub fn set_id_2(
        &mut self,
        mor: impl Into<String>,
        id_cell: impl Into<String>,
    ) -> Result<(), HigherCategoryError> {
        let mor_str = mor.into();
        let id_str = id_cell.into();

        if !self.one_cells.contains_key(&mor_str) {
            return Err(HigherCategoryError::OneCellNotFound { id: mor_str });
        }
        let cell = self
            .two_cells
            .get(&id_str)
            .ok_or_else(|| HigherCategoryError::TwoCellNotFound { id: id_str.clone() })?;
        if cell.src_1 != mor_str || cell.tgt_1 != mor_str {
            let actual = if cell.src_1 != mor_str {
                cell.src_1.clone()
            } else {
                cell.tgt_1.clone()
            };
            return Err(HigherCategoryError::TwoCellBoundaryMismatch {
                cell: id_str,
                expected_1_src: mor_str,
                actual_1_src: actual,
            });
        }
        self.id_2_map.insert(mor_str, id_str);
        Ok(())
    }

    pub fn set_compose_1(
        &mut self,
        f: impl Into<String>,
        g: impl Into<String>,
        comp: impl Into<String>,
    ) -> Result<(), HigherCategoryError> {
        let f_str = f.into();
        let g_str = g.into();
        let comp_str = comp.into();

        let f_cell = self
            .one_cells
            .get(&f_str)
            .ok_or_else(|| HigherCategoryError::OneCellNotFound { id: f_str.clone() })?;
        let g_cell = self
            .one_cells
            .get(&g_str)
            .ok_or_else(|| HigherCategoryError::OneCellNotFound { id: g_str.clone() })?;
        let comp_cell =
            self.one_cells
                .get(&comp_str)
                .ok_or_else(|| HigherCategoryError::OneCellNotFound {
                    id: comp_str.clone(),
                })?;

        if f_cell.tgt != g_cell.src {
            return Err(HigherCategoryError::OneCellNotComposable {
                first: f_str,
                second: g_str,
                tgt: f_cell.tgt.clone(),
                src: g_cell.src.clone(),
            });
        }
        if comp_cell.src != f_cell.src || comp_cell.tgt != g_cell.tgt {
            return Err(HigherCategoryError::OneCellBoundaryMismatch {
                cell: comp_str,
                expected_src: f_cell.src.clone(),
                actual_src: comp_cell.src.clone(),
            });
        }

        self.compose_1_table.insert((f_str, g_str), comp_str);
        Ok(())
    }

    pub fn set_compose_2_v(
        &mut self,
        alpha: impl Into<String>,
        beta: impl Into<String>,
        comp: impl Into<String>,
    ) -> Result<(), HigherCategoryError> {
        let a_str = alpha.into();
        let b_str = beta.into();
        let comp_str = comp.into();

        let a_cell = self
            .two_cells
            .get(&a_str)
            .ok_or_else(|| HigherCategoryError::TwoCellNotFound { id: a_str.clone() })?;
        let b_cell = self
            .two_cells
            .get(&b_str)
            .ok_or_else(|| HigherCategoryError::TwoCellNotFound { id: b_str.clone() })?;
        let comp_cell =
            self.two_cells
                .get(&comp_str)
                .ok_or_else(|| HigherCategoryError::TwoCellNotFound {
                    id: comp_str.clone(),
                })?;

        if a_cell.tgt_1 != b_cell.src_1 {
            return Err(HigherCategoryError::VerticalNotComposable {
                alpha: a_str,
                beta: b_str,
                tgt1: a_cell.tgt_1.clone(),
                src1: b_cell.src_1.clone(),
            });
        }
        if comp_cell.src_1 != a_cell.src_1 || comp_cell.tgt_1 != b_cell.tgt_1 {
            return Err(HigherCategoryError::TwoCellBoundaryMismatch {
                cell: comp_str,
                expected_1_src: a_cell.src_1.clone(),
                actual_1_src: comp_cell.src_1.clone(),
            });
        }

        self.compose_2_v_table.insert((a_str, b_str), comp_str);
        Ok(())
    }

    pub fn set_compose_2_h(
        &mut self,
        alpha: impl Into<String>,
        beta: impl Into<String>,
        comp: impl Into<String>,
    ) -> Result<(), HigherCategoryError> {
        let a_str = alpha.into();
        let b_str = beta.into();
        let comp_str = comp.into();

        let a_cell = self
            .two_cells
            .get(&a_str)
            .ok_or_else(|| HigherCategoryError::TwoCellNotFound { id: a_str.clone() })?;
        let b_cell = self
            .two_cells
            .get(&b_str)
            .ok_or_else(|| HigherCategoryError::TwoCellNotFound { id: b_str.clone() })?;
        let comp_cell =
            self.two_cells
                .get(&comp_str)
                .ok_or_else(|| HigherCategoryError::TwoCellNotFound {
                    id: comp_str.clone(),
                })?;

        if a_cell.tgt_0 != b_cell.src_0 {
            return Err(HigherCategoryError::HorizontalNotComposable {
                alpha: a_str,
                beta: b_str,
                tgt0: a_cell.tgt_0.clone(),
                src0: b_cell.src_0.clone(),
            });
        }

        let gf = self.compose_1(&a_cell.src_1, &b_cell.src_1)?;
        let gp_fp = self.compose_1(&a_cell.tgt_1, &b_cell.tgt_1)?;

        if comp_cell.src_1 != gf || comp_cell.tgt_1 != gp_fp {
            return Err(HigherCategoryError::TwoCellBoundaryMismatch {
                cell: comp_str,
                expected_1_src: gf,
                actual_1_src: comp_cell.src_1.clone(),
            });
        }

        self.compose_2_h_table.insert((a_str, b_str), comp_str);
        Ok(())
    }

    pub fn validate_all_laws(&self) -> Result<(), HigherCategoryError> {
        for ob in &self.zero_cells {
            let id_f = self.id_1(ob)?;
            let mor = self
                .one_cells
                .get(&id_f)
                .ok_or_else(|| HigherCategoryError::OneCellNotFound { id: id_f.clone() })?;
            if mor.src != *ob || mor.tgt != *ob {
                return Err(HigherCategoryError::OneCellBoundaryMismatch {
                    cell: id_f,
                    expected_src: ob.clone(),
                    actual_src: mor.src.clone(),
                });
            }
        }

        for (f_id, mor) in &self.one_cells {
            let id_src = self.id_1(&mor.src)?;
            let id_tgt = self.id_1(&mor.tgt)?;

            let right_comp = self.compose_1(&id_src, f_id)?;
            if right_comp != *f_id {
                return Err(HigherCategoryError::UnitLawViolation {
                    details: format!("Right identity failed for 1-cell {f_id}: compose_1({id_src}, {f_id}) = '{right_comp}' != '{f_id}'"),
                });
            }

            let left_comp = self.compose_1(f_id, &id_tgt)?;
            if left_comp != *f_id {
                return Err(HigherCategoryError::UnitLawViolation {
                    details: format!("Left identity failed for 1-cell {f_id}: compose_1({f_id}, {id_tgt}) = '{left_comp}' != '{f_id}'"),
                });
            }
        }

        for (f_id, f) in &self.one_cells {
            for (g_id, g) in &self.one_cells {
                if f.tgt != g.src {
                    continue;
                }
                let gf = self.compose_1(f_id, g_id)?;
                for (h_id, h) in &self.one_cells {
                    if g.tgt != h.src {
                        continue;
                    }
                    let hg = self.compose_1(g_id, h_id)?;

                    let lhs = self.compose_1(&gf, h_id)?;
                    let rhs = self.compose_1(f_id, &hg)?;
                    if lhs != rhs {
                        return Err(HigherCategoryError::AssociativityViolation {
                            details: format!("1-cell associativity failed for ({f_id}, {g_id}, {h_id}): ({h_id}∘{g_id})∘{f_id}='{lhs}' != {h_id}∘({g_id}∘{f_id})='{rhs}'"),
                        });
                    }
                }
            }
        }

        for mor_id in self.one_cells.keys() {
            let id_2 = self.id_2(mor_id)?;
            let cell2 = self
                .two_cells
                .get(&id_2)
                .ok_or_else(|| HigherCategoryError::TwoCellNotFound { id: id_2.clone() })?;
            if cell2.src_1 != *mor_id || cell2.tgt_1 != *mor_id {
                return Err(HigherCategoryError::TwoCellBoundaryMismatch {
                    cell: id_2,
                    expected_1_src: mor_id.clone(),
                    actual_1_src: cell2.src_1.clone(),
                });
            }
        }

        for (alpha_id, alpha) in &self.two_cells {
            let id_src1 = self.id_2(&alpha.src_1)?;
            let id_tgt1 = self.id_2(&alpha.tgt_1)?;

            let right_comp = self.compose_2_vertical(&id_src1, alpha_id)?;
            if right_comp != *alpha_id {
                return Err(HigherCategoryError::UnitLawViolation {
                    details: format!("Vertical right identity failed for 2-cell {alpha_id}: {right_comp} != {alpha_id}"),
                });
            }

            let left_comp = self.compose_2_vertical(alpha_id, &id_tgt1)?;
            if left_comp != *alpha_id {
                return Err(HigherCategoryError::UnitLawViolation {
                    details: format!("Vertical left identity failed for 2-cell {alpha_id}: {left_comp} != {alpha_id}"),
                });
            }
        }

        for (a_id, alpha) in &self.two_cells {
            for (b_id, beta) in &self.two_cells {
                if alpha.tgt_1 != beta.src_1 {
                    continue;
                }
                let ba = self.compose_2_vertical(a_id, b_id)?;
                for (c_id, gamma) in &self.two_cells {
                    if beta.tgt_1 != gamma.src_1 {
                        continue;
                    }
                    let cb = self.compose_2_vertical(b_id, c_id)?;

                    let lhs = self.compose_2_vertical(&ba, c_id)?;
                    let rhs = self.compose_2_vertical(a_id, &cb)?;
                    if lhs != rhs {
                        return Err(HigherCategoryError::AssociativityViolation {
                            details: format!("2-cell vertical associativity failed for ({a_id}, {b_id}, {c_id}): LHS '{lhs}' != RHS '{rhs}'"),
                        });
                    }
                }
            }
        }

        for (f_id, f) in &self.one_cells {
            for (g_id, g) in &self.one_cells {
                if f.tgt != g.src {
                    continue;
                }
                let gf = self.compose_1(f_id, g_id)?;
                let id_f = self.id_2(f_id)?;
                let id_g = self.id_2(g_id)?;
                let id_gf = self.id_2(&gf)?;

                let h_comp = self.compose_2_horizontal(&id_f, &id_g)?;
                if h_comp != id_gf {
                    return Err(HigherCategoryError::UnitLawViolation {
                        details: format!("Horizontal identity preservation failed: 1_{g_id} *_h 1_{f_id} = '{h_comp}' != 1_{{{gf}}} = '{id_gf}'"),
                    });
                }
            }
        }

        crate::exchange::verify_all_exchange_laws(self)?;

        Ok(())
    }

    pub fn content_hash(&self) -> String {
        let mut hasher = Sha256::new();
        hasher.update(b"Strict2Category:v1.0.0\n");
        hasher.update(self.name.as_bytes());
        hasher.update(b"\nobjects:");
        for ob in &self.zero_cells {
            hasher.update(ob.as_bytes());
            hasher.update(b",");
        }
        hasher.update(b"\none_cells:");
        for (id, mor) in &self.one_cells {
            hasher.update(id.as_bytes());
            hasher.update(b":");
            hasher.update(mor.src.as_bytes());
            hasher.update(b"->");
            hasher.update(mor.tgt.as_bytes());
            hasher.update(b";");
        }
        hasher.update(b"\ntwo_cells:");
        for (id, cell) in &self.two_cells {
            hasher.update(id.as_bytes());
            hasher.update(b":");
            hasher.update(cell.src_1.as_bytes());
            hasher.update(b"=>");
            hasher.update(cell.tgt_1.as_bytes());
            hasher.update(b";");
        }
        hasher.update(b"\nid_1:");
        for (ob, id_mor) in &self.id_1_map {
            hasher.update(ob.as_bytes());
            hasher.update(b"=");
            hasher.update(id_mor.as_bytes());
            hasher.update(b";");
        }
        hasher.update(b"\nid_2:");
        for (mor, id_cell) in &self.id_2_map {
            hasher.update(mor.as_bytes());
            hasher.update(b"=");
            hasher.update(id_cell.as_bytes());
            hasher.update(b";");
        }
        hasher.update(b"\ncompose_1:");
        for ((f, g), comp) in &self.compose_1_table {
            hasher.update(f.as_bytes());
            hasher.update(b",");
            hasher.update(g.as_bytes());
            hasher.update(b"=");
            hasher.update(comp.as_bytes());
            hasher.update(b";");
        }
        hasher.update(b"\ncompose_2_v:");
        for ((a, b), comp) in &self.compose_2_v_table {
            hasher.update(a.as_bytes());
            hasher.update(b",");
            hasher.update(b.as_bytes());
            hasher.update(b"=");
            hasher.update(comp.as_bytes());
            hasher.update(b";");
        }
        hasher.update(b"\ncompose_2_h:");
        for ((a, b), comp) in &self.compose_2_h_table {
            hasher.update(a.as_bytes());
            hasher.update(b",");
            hasher.update(b.as_bytes());
            hasher.update(b"=");
            hasher.update(comp.as_bytes());
            hasher.update(b";");
        }
        format!("{:x}", hasher.finalize())
    }
}

impl TwoCategory for Strict2Category {
    type ZeroCell = String;
    type OneCell = String;
    type TwoCell = String;

    fn source_0_of_1(&self, f: &Self::OneCell) -> Result<Self::ZeroCell, HigherCategoryError> {
        self.one_cells
            .get(f)
            .map(|d| d.src.clone())
            .ok_or_else(|| HigherCategoryError::OneCellNotFound { id: f.clone() })
    }

    fn target_0_of_1(&self, f: &Self::OneCell) -> Result<Self::ZeroCell, HigherCategoryError> {
        self.one_cells
            .get(f)
            .map(|d| d.tgt.clone())
            .ok_or_else(|| HigherCategoryError::OneCellNotFound { id: f.clone() })
    }

    fn source_1_of_2(&self, alpha: &Self::TwoCell) -> Result<Self::OneCell, HigherCategoryError> {
        self.two_cells
            .get(alpha)
            .map(|d| d.src_1.clone())
            .ok_or_else(|| HigherCategoryError::TwoCellNotFound { id: alpha.clone() })
    }

    fn target_1_of_2(&self, alpha: &Self::TwoCell) -> Result<Self::OneCell, HigherCategoryError> {
        self.two_cells
            .get(alpha)
            .map(|d| d.tgt_1.clone())
            .ok_or_else(|| HigherCategoryError::TwoCellNotFound { id: alpha.clone() })
    }

    fn id_1(&self, a: &Self::ZeroCell) -> Result<Self::OneCell, HigherCategoryError> {
        self.id_1_map
            .get(a)
            .cloned()
            .ok_or_else(|| HigherCategoryError::ZeroCellNotFound { id: a.clone() })
    }

    fn id_2(&self, f: &Self::OneCell) -> Result<Self::TwoCell, HigherCategoryError> {
        self.id_2_map
            .get(f)
            .cloned()
            .ok_or_else(|| HigherCategoryError::OneCellNotFound { id: f.clone() })
    }

    fn compose_1(
        &self,
        f: &Self::OneCell,
        g: &Self::OneCell,
    ) -> Result<Self::OneCell, HigherCategoryError> {
        let f_tgt = self.target_0_of_1(f)?;
        let g_src = self.source_0_of_1(g)?;
        if f_tgt != g_src {
            return Err(HigherCategoryError::OneCellNotComposable {
                first: f.clone(),
                second: g.clone(),
                tgt: f_tgt,
                src: g_src,
            });
        }
        self.compose_1_table
            .get(&(f.clone(), g.clone()))
            .cloned()
            .ok_or_else(|| HigherCategoryError::OneCellNotComposable {
                first: f.clone(),
                second: g.clone(),
                tgt: f_tgt,
                src: g_src,
            })
    }

    fn compose_2_vertical(
        &self,
        alpha: &Self::TwoCell,
        beta: &Self::TwoCell,
    ) -> Result<Self::TwoCell, HigherCategoryError> {
        let a_tgt = self.target_1_of_2(alpha)?;
        let b_src = self.source_1_of_2(beta)?;
        if a_tgt != b_src {
            return Err(HigherCategoryError::VerticalNotComposable {
                alpha: alpha.clone(),
                beta: beta.clone(),
                tgt1: a_tgt,
                src1: b_src,
            });
        }
        self.compose_2_v_table
            .get(&(alpha.clone(), beta.clone()))
            .cloned()
            .ok_or_else(|| HigherCategoryError::VerticalNotComposable {
                alpha: alpha.clone(),
                beta: beta.clone(),
                tgt1: a_tgt,
                src1: b_src,
            })
    }

    fn compose_2_horizontal(
        &self,
        alpha: &Self::TwoCell,
        beta: &Self::TwoCell,
    ) -> Result<Self::TwoCell, HigherCategoryError> {
        let f = self.source_1_of_2(alpha)?;
        let g = self.source_1_of_2(beta)?;
        let f_tgt0 = self.target_0_of_1(&f)?;
        let g_src0 = self.source_0_of_1(&g)?;
        if f_tgt0 != g_src0 {
            return Err(HigherCategoryError::HorizontalNotComposable {
                alpha: alpha.clone(),
                beta: beta.clone(),
                tgt0: f_tgt0.clone(),
                src0: g_src0.clone(),
            });
        }
        self.compose_2_h_table
            .get(&(alpha.clone(), beta.clone()))
            .cloned()
            .ok_or_else(|| HigherCategoryError::HorizontalNotComposable {
                alpha: alpha.clone(),
                beta: beta.clone(),
                tgt0: f_tgt0,
                src0: g_src0,
            })
    }
}
