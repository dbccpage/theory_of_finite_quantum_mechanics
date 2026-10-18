
use crate::error::HigherCategoryError;
use crate::two_category::{Strict2Category, TwoCategory};
use std::collections::BTreeMap;

#[derive(Debug, Clone, PartialEq, Eq, serde::Serialize, serde::Deserialize)]
pub struct Invertible2Cell<TwoCell> {
    pub forward: TwoCell,
    pub inverse: TwoCell,
}

impl<TwoCell> Invertible2Cell<TwoCell> {
    pub fn new(forward: TwoCell, inverse: TwoCell) -> Self {
        Self { forward, inverse }
    }
}

pub trait Bicategory: TwoCategory {
    fn associator(
        &self,
        f: &Self::OneCell,
        g: &Self::OneCell,
        h: &Self::OneCell,
    ) -> Result<Invertible2Cell<Self::TwoCell>, HigherCategoryError>;

    fn left_unitor(
        &self,
        f: &Self::OneCell,
    ) -> Result<Invertible2Cell<Self::TwoCell>, HigherCategoryError>;

    fn right_unitor(
        &self,
        f: &Self::OneCell,
    ) -> Result<Invertible2Cell<Self::TwoCell>, HigherCategoryError>;
}

#[derive(Debug, Clone, PartialEq, Eq, serde::Serialize, serde::Deserialize)]
pub struct FiniteBicategory {
    pub base_strict: Strict2Category,
    pub associator_table: BTreeMap<(String, String, String), Invertible2Cell<String>>,
    pub left_unitor_table: BTreeMap<String, Invertible2Cell<String>>,
    pub right_unitor_table: BTreeMap<String, Invertible2Cell<String>>,
}

impl FiniteBicategory {
    pub fn new(base_strict: Strict2Category) -> Self {
        Self {
            base_strict,
            associator_table: BTreeMap::new(),
            left_unitor_table: BTreeMap::new(),
            right_unitor_table: BTreeMap::new(),
        }
    }

    pub fn set_associator(
        &mut self,
        f: impl Into<String>,
        g: impl Into<String>,
        h: impl Into<String>,
        forward: impl Into<String>,
        inverse: impl Into<String>,
    ) -> Result<(), HigherCategoryError> {
        let f_s = f.into();
        let g_s = g.into();
        let h_s = h.into();
        let fwd = forward.into();
        let inv = inverse.into();

        let hg = self.base_strict.compose_1(&g_s, &h_s)?;
        let gf = self.base_strict.compose_1(&f_s, &g_s)?;
        let source = self.base_strict.compose_1(&f_s, &hg)?;
        let target = self.base_strict.compose_1(&gf, &h_s)?;

        let fwd_cell = self
            .base_strict
            .two_cells
            .get(&fwd)
            .ok_or_else(|| HigherCategoryError::TwoCellNotFound { id: fwd.clone() })?;
        let inv_cell = self
            .base_strict
            .two_cells
            .get(&inv)
            .ok_or_else(|| HigherCategoryError::TwoCellNotFound { id: inv.clone() })?;

        if fwd_cell.src_1 != source || fwd_cell.tgt_1 != target {
            return Err(HigherCategoryError::AssociativityViolation {
                details: format!(
                    "associator ({f_s}, {g_s}, {h_s}) must be {source} => {target}, found {} => {}",
                    fwd_cell.src_1, fwd_cell.tgt_1
                ),
            });
        }

        if fwd_cell.tgt_1 != inv_cell.src_1 || inv_cell.tgt_1 != fwd_cell.src_1 {
            return Err(HigherCategoryError::InvertibilityViolation {
                cell: fwd.clone(),
                details: format!(
                    "Forward ({fwd}: {} => {}) and inverse ({inv}: {} => {}) boundaries do not match",
                    fwd_cell.src_1, fwd_cell.tgt_1, inv_cell.src_1, inv_cell.tgt_1
                ),
            });
        }

        let id_src = self.base_strict.id_2(&fwd_cell.src_1)?;
        let id_tgt = self.base_strict.id_2(&fwd_cell.tgt_1)?;

        let comp1 = self.base_strict.compose_2_vertical(&fwd, &inv)?;
        if comp1 != id_src {
            return Err(HigherCategoryError::InvertibilityViolation {
                cell: fwd.clone(),
                details: format!(
                    "inv ∘_v fwd = '{comp1}' != id_{{{}}} = '{id_src}'",
                    fwd_cell.src_1
                ),
            });
        }

        let comp2 = self.base_strict.compose_2_vertical(&inv, &fwd)?;
        if comp2 != id_tgt {
            return Err(HigherCategoryError::InvertibilityViolation {
                cell: fwd.clone(),
                details: format!(
                    "fwd ∘_v inv = '{comp2}' != id_{{{}}} = '{id_tgt}'",
                    fwd_cell.tgt_1
                ),
            });
        }

        self.associator_table
            .insert((f_s, g_s, h_s), Invertible2Cell::new(fwd, inv));
        Ok(())
    }

    pub fn set_left_unitor(
        &mut self,
        f: impl Into<String>,
        forward: impl Into<String>,
        inverse: impl Into<String>,
    ) -> Result<(), HigherCategoryError> {
        let f_s = f.into();
        let fwd = forward.into();
        let inv = inverse.into();

        let target_ob = self.base_strict.target_0_of_1(&f_s)?;
        let id_target = self.base_strict.id_1(&target_ob)?;
        let source = self.base_strict.compose_1(&f_s, &id_target)?;

        let fwd_cell = self
            .base_strict
            .two_cells
            .get(&fwd)
            .ok_or_else(|| HigherCategoryError::TwoCellNotFound { id: fwd.clone() })?;
        let inv_cell = self
            .base_strict
            .two_cells
            .get(&inv)
            .ok_or_else(|| HigherCategoryError::TwoCellNotFound { id: inv.clone() })?;

        if fwd_cell.src_1 != source || fwd_cell.tgt_1 != f_s {
            return Err(HigherCategoryError::UnitLawViolation {
                details: format!(
                    "left unitor of {f_s} must be {source} => {f_s}, found {} => {}",
                    fwd_cell.src_1, fwd_cell.tgt_1
                ),
            });
        }

        if fwd_cell.tgt_1 != inv_cell.src_1 || inv_cell.tgt_1 != fwd_cell.src_1 {
            return Err(HigherCategoryError::InvertibilityViolation {
                cell: fwd.clone(),
                details: format!(
                    "Left unitor forward ({fwd}) and inverse ({inv}) boundaries do not match"
                ),
            });
        }

        let id_src = self.base_strict.id_2(&fwd_cell.src_1)?;
        let id_tgt = self.base_strict.id_2(&fwd_cell.tgt_1)?;

        let comp1 = self.base_strict.compose_2_vertical(&fwd, &inv)?;
        if comp1 != id_src {
            return Err(HigherCategoryError::InvertibilityViolation {
                cell: fwd.clone(),
                details: format!("Left unitor inv ∘_v fwd != id: '{comp1}' != '{id_src}'"),
            });
        }

        let comp2 = self.base_strict.compose_2_vertical(&inv, &fwd)?;
        if comp2 != id_tgt {
            return Err(HigherCategoryError::InvertibilityViolation {
                cell: fwd.clone(),
                details: format!("Left unitor fwd ∘_v inv != id: '{comp2}' != '{id_tgt}'"),
            });
        }

        self.left_unitor_table
            .insert(f_s, Invertible2Cell::new(fwd, inv));
        Ok(())
    }

    pub fn set_right_unitor(
        &mut self,
        f: impl Into<String>,
        forward: impl Into<String>,
        inverse: impl Into<String>,
    ) -> Result<(), HigherCategoryError> {
        let f_s = f.into();
        let fwd = forward.into();
        let inv = inverse.into();

        let source_ob = self.base_strict.source_0_of_1(&f_s)?;
        let id_source = self.base_strict.id_1(&source_ob)?;
        let source = self.base_strict.compose_1(&id_source, &f_s)?;

        let fwd_cell = self
            .base_strict
            .two_cells
            .get(&fwd)
            .ok_or_else(|| HigherCategoryError::TwoCellNotFound { id: fwd.clone() })?;
        let inv_cell = self
            .base_strict
            .two_cells
            .get(&inv)
            .ok_or_else(|| HigherCategoryError::TwoCellNotFound { id: inv.clone() })?;

        if fwd_cell.src_1 != source || fwd_cell.tgt_1 != f_s {
            return Err(HigherCategoryError::UnitLawViolation {
                details: format!(
                    "right unitor of {f_s} must be {source} => {f_s}, found {} => {}",
                    fwd_cell.src_1, fwd_cell.tgt_1
                ),
            });
        }

        if fwd_cell.tgt_1 != inv_cell.src_1 || inv_cell.tgt_1 != fwd_cell.src_1 {
            return Err(HigherCategoryError::InvertibilityViolation {
                cell: fwd.clone(),
                details: format!(
                    "Right unitor forward ({fwd}) and inverse ({inv}) boundaries do not match"
                ),
            });
        }

        let id_src = self.base_strict.id_2(&fwd_cell.src_1)?;
        let id_tgt = self.base_strict.id_2(&fwd_cell.tgt_1)?;

        let comp1 = self.base_strict.compose_2_vertical(&fwd, &inv)?;
        if comp1 != id_src {
            return Err(HigherCategoryError::InvertibilityViolation {
                cell: fwd.clone(),
                details: format!("Right unitor inv ∘_v fwd != id: '{comp1}' != '{id_src}'"),
            });
        }

        let comp2 = self.base_strict.compose_2_vertical(&inv, &fwd)?;
        if comp2 != id_tgt {
            return Err(HigherCategoryError::InvertibilityViolation {
                cell: fwd.clone(),
                details: format!("Right unitor fwd ∘_v inv != id: '{comp2}' != '{id_tgt}'"),
            });
        }

        self.right_unitor_table
            .insert(f_s, Invertible2Cell::new(fwd, inv));
        Ok(())
    }

    pub fn validate_coherence(
        &self,
    ) -> Result<crate::coherence::CoherenceReport, HigherCategoryError> {
        let one_cells: Vec<String> = self.base_strict.one_cells.keys().cloned().collect();
        crate::coherence::verify_bicategory_coherence(self, &one_cells)
    }
}

impl Bicategory for FiniteBicategory {
    fn associator(
        &self,
        f: &Self::OneCell,
        g: &Self::OneCell,
        h: &Self::OneCell,
    ) -> Result<Invertible2Cell<Self::TwoCell>, HigherCategoryError> {
        self.associator_table
            .get(&(f.clone(), g.clone(), h.clone()))
            .cloned()
            .ok_or_else(|| HigherCategoryError::AssociativityViolation {
                details: format!("Associator missing for triple ({f}, {g}, {h})"),
            })
    }

    fn left_unitor(
        &self,
        f: &Self::OneCell,
    ) -> Result<Invertible2Cell<Self::TwoCell>, HigherCategoryError> {
        self.left_unitor_table.get(f).cloned().ok_or_else(|| {
            HigherCategoryError::UnitLawViolation {
                details: format!("Left unitor missing for 1-cell {f}"),
            }
        })
    }

    fn right_unitor(
        &self,
        f: &Self::OneCell,
    ) -> Result<Invertible2Cell<Self::TwoCell>, HigherCategoryError> {
        self.right_unitor_table.get(f).cloned().ok_or_else(|| {
            HigherCategoryError::UnitLawViolation {
                details: format!("Right unitor missing for 1-cell {f}"),
            }
        })
    }
}

impl TwoCategory for FiniteBicategory {
    type ZeroCell = String;
    type OneCell = String;
    type TwoCell = String;

    fn source_0_of_1(&self, f: &Self::OneCell) -> Result<Self::ZeroCell, HigherCategoryError> {
        self.base_strict.source_0_of_1(f)
    }

    fn target_0_of_1(&self, f: &Self::OneCell) -> Result<Self::ZeroCell, HigherCategoryError> {
        self.base_strict.target_0_of_1(f)
    }

    fn source_1_of_2(&self, alpha: &Self::TwoCell) -> Result<Self::OneCell, HigherCategoryError> {
        self.base_strict.source_1_of_2(alpha)
    }

    fn target_1_of_2(&self, alpha: &Self::TwoCell) -> Result<Self::OneCell, HigherCategoryError> {
        self.base_strict.target_1_of_2(alpha)
    }

    fn id_1(&self, a: &Self::ZeroCell) -> Result<Self::OneCell, HigherCategoryError> {
        self.base_strict.id_1(a)
    }

    fn id_2(&self, f: &Self::OneCell) -> Result<Self::TwoCell, HigherCategoryError> {
        self.base_strict.id_2(f)
    }

    fn compose_1(
        &self,
        f: &Self::OneCell,
        g: &Self::OneCell,
    ) -> Result<Self::OneCell, HigherCategoryError> {
        self.base_strict.compose_1(f, g)
    }

    fn compose_2_vertical(
        &self,
        alpha: &Self::TwoCell,
        beta: &Self::TwoCell,
    ) -> Result<Self::TwoCell, HigherCategoryError> {
        self.base_strict.compose_2_vertical(alpha, beta)
    }

    fn compose_2_horizontal(
        &self,
        alpha: &Self::TwoCell,
        beta: &Self::TwoCell,
    ) -> Result<Self::TwoCell, HigherCategoryError> {
        self.base_strict.compose_2_horizontal(alpha, beta)
    }
}
