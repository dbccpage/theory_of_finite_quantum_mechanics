
use std::collections::{BTreeMap, BTreeSet};

use engine_kernel::resource_limits::OperationLimits;
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};

use crate::error::{reserve_exact, HigherCategoryError};

#[derive(Debug, Clone, PartialEq, Eq, PartialOrd, Ord, Serialize, Deserialize)]
pub struct HorizontalCell {
    pub id: String,
    pub src: String,
    pub tgt: String,
}

#[derive(Debug, Clone, PartialEq, Eq, PartialOrd, Ord, Serialize, Deserialize)]
pub struct VerticalCell {
    pub id: String,
    pub src: String,
    pub tgt: String,
}

#[derive(Debug, Clone, PartialEq, Eq, PartialOrd, Ord, Serialize, Deserialize)]
pub struct SquareCell {
    pub id: String,
    pub top_h: String,
    pub bot_h: String,
    pub left_v: String,
    pub right_v: String,
    pub src_0: String,
    pub tgt_0: String,
}

pub struct SquareInterchange;

impl SquareInterchange {
    pub fn verify_interchange(
        cat: &DoubleCategory,
        alpha: &str,
        beta: &str,
        gamma: &str,
        delta: &str,
    ) -> Result<(), HigherCategoryError> {
        let top_row = cat.compose_square_h(alpha, beta)?;
        let bot_row = cat.compose_square_h(gamma, delta)?;
        let lhs = cat.compose_square_v(&top_row, &bot_row)?;

        let left_col = cat.compose_square_v(alpha, gamma)?;
        let right_col = cat.compose_square_v(beta, delta)?;
        let rhs = cat.compose_square_h(&left_col, &right_col)?;

        if lhs != rhs {
            return Err(HigherCategoryError::SquareInterchangeViolation {
                left: lhs,
                right: rhs,
                details: format!(
                    "Middle-four interchange failed for grid [{alpha}, {beta} ; {gamma}, {delta}]"
                ),
            });
        }

        Ok(())
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct DoubleCategory {
    pub name: String,
    pub zero_cells: BTreeSet<String>,
    pub horiz_one_cells: BTreeMap<String, HorizontalCell>,
    pub vert_one_cells: BTreeMap<String, VerticalCell>,
    pub squares: BTreeMap<String, SquareCell>,
    pub compose_h_1_table: BTreeMap<(String, String), String>,
    pub compose_v_1_table: BTreeMap<(String, String), String>,
    pub compose_square_h_table: BTreeMap<(String, String), String>,
    pub compose_square_v_table: BTreeMap<(String, String), String>,
    pub limits: OperationLimits,
}

impl DoubleCategory {
    pub fn new(name: &str) -> Self {
        Self::with_limits(name, OperationLimits::default())
    }

    pub fn with_limits(name: &str, limits: OperationLimits) -> Self {
        Self {
            name: name.to_string(),
            zero_cells: BTreeSet::new(),
            horiz_one_cells: BTreeMap::new(),
            vert_one_cells: BTreeMap::new(),
            squares: BTreeMap::new(),
            compose_h_1_table: BTreeMap::new(),
            compose_v_1_table: BTreeMap::new(),
            compose_square_h_table: BTreeMap::new(),
            compose_square_v_table: BTreeMap::new(),
            limits,
        }
    }

    pub fn add_zero_cell(&mut self, id: &str) -> Result<(), HigherCategoryError> {
        if self.zero_cells.contains(id) {
            return Err(HigherCategoryError::DuplicateCell { id: id.to_string() });
        }
        if self.zero_cells.len() >= self.limits.max_cells {
            return Err(HigherCategoryError::AllocationLimitExceeded {
                requested: self.zero_cells.len() + 1,
                limit: self.limits.max_cells,
            });
        }
        self.zero_cells.insert(id.to_string());
        Ok(())
    }

    pub fn add_horiz_cell(
        &mut self,
        id: &str,
        src: &str,
        tgt: &str,
    ) -> Result<(), HigherCategoryError> {
        if self.horiz_one_cells.contains_key(id) {
            return Err(HigherCategoryError::DuplicateCell { id: id.to_string() });
        }
        if !self.zero_cells.contains(src) {
            return Err(HigherCategoryError::ZeroCellNotFound { id: src.to_string() });
        }
        if !self.zero_cells.contains(tgt) {
            return Err(HigherCategoryError::ZeroCellNotFound { id: tgt.to_string() });
        }
        if self.horiz_one_cells.len() >= self.limits.max_cells {
            return Err(HigherCategoryError::AllocationLimitExceeded {
                requested: self.horiz_one_cells.len() + 1,
                limit: self.limits.max_cells,
            });
        }
        self.horiz_one_cells.insert(
            id.to_string(),
            HorizontalCell {
                id: id.to_string(),
                src: src.to_string(),
                tgt: tgt.to_string(),
            },
        );
        Ok(())
    }

    pub fn add_vert_cell(
        &mut self,
        id: &str,
        src: &str,
        tgt: &str,
    ) -> Result<(), HigherCategoryError> {
        if self.vert_one_cells.contains_key(id) {
            return Err(HigherCategoryError::DuplicateCell { id: id.to_string() });
        }
        if !self.zero_cells.contains(src) {
            return Err(HigherCategoryError::ZeroCellNotFound { id: src.to_string() });
        }
        if !self.zero_cells.contains(tgt) {
            return Err(HigherCategoryError::ZeroCellNotFound { id: tgt.to_string() });
        }
        if self.vert_one_cells.len() >= self.limits.max_cells {
            return Err(HigherCategoryError::AllocationLimitExceeded {
                requested: self.vert_one_cells.len() + 1,
                limit: self.limits.max_cells,
            });
        }
        self.vert_one_cells.insert(
            id.to_string(),
            VerticalCell {
                id: id.to_string(),
                src: src.to_string(),
                tgt: tgt.to_string(),
            },
        );
        Ok(())
    }

    pub fn add_square(
        &mut self,
        id: &str,
        top_h: &str,
        bot_h: &str,
        left_v: &str,
        right_v: &str,
    ) -> Result<(), HigherCategoryError> {
        if self.squares.contains_key(id) {
            return Err(HigherCategoryError::DuplicateCell { id: id.to_string() });
        }
        let top = self.horiz_one_cells.get(top_h).ok_or_else(|| {
            HigherCategoryError::OneCellNotFound { id: top_h.to_string() }
        })?;
        let bot = self.horiz_one_cells.get(bot_h).ok_or_else(|| {
            HigherCategoryError::OneCellNotFound { id: bot_h.to_string() }
        })?;
        let left = self.vert_one_cells.get(left_v).ok_or_else(|| {
            HigherCategoryError::OneCellNotFound { id: left_v.to_string() }
        })?;
        let right = self.vert_one_cells.get(right_v).ok_or_else(|| {
            HigherCategoryError::OneCellNotFound { id: right_v.to_string() }
        })?;

        if left.src != top.src {
            return Err(HigherCategoryError::SquareBoundaryMismatch {
                square_id: id.to_string(),
                expected: format!("left.src == top.src ({})", top.src),
                actual: left.src.clone(),
            });
        }
        if right.src != top.tgt {
            return Err(HigherCategoryError::SquareBoundaryMismatch {
                square_id: id.to_string(),
                expected: format!("right.src == top.tgt ({})", top.tgt),
                actual: right.src.clone(),
            });
        }
        if left.tgt != bot.src {
            return Err(HigherCategoryError::SquareBoundaryMismatch {
                square_id: id.to_string(),
                expected: format!("left.tgt == bot.src ({})", bot.src),
                actual: left.tgt.clone(),
            });
        }
        if right.tgt != bot.tgt {
            return Err(HigherCategoryError::SquareBoundaryMismatch {
                square_id: id.to_string(),
                expected: format!("right.tgt == bot.tgt ({})", bot.tgt),
                actual: right.tgt.clone(),
            });
        }

        if self.squares.len() >= self.limits.max_cells {
            return Err(HigherCategoryError::AllocationLimitExceeded {
                requested: self.squares.len() + 1,
                limit: self.limits.max_cells,
            });
        }

        self.squares.insert(
            id.to_string(),
            SquareCell {
                id: id.to_string(),
                top_h: top_h.to_string(),
                bot_h: bot_h.to_string(),
                left_v: left_v.to_string(),
                right_v: right_v.to_string(),
                src_0: top.src.clone(),
                tgt_0: bot.tgt.clone(),
            },
        );
        Ok(())
    }

    pub fn set_compose_h_1(
        &mut self,
        first: &str,
        second: &str,
        comp: &str,
    ) -> Result<(), HigherCategoryError> {
        let f = self.horiz_one_cells.get(first).ok_or_else(|| {
            HigherCategoryError::OneCellNotFound { id: first.to_string() }
        })?;
        let s = self.horiz_one_cells.get(second).ok_or_else(|| {
            HigherCategoryError::OneCellNotFound { id: second.to_string() }
        })?;
        if f.tgt != s.src {
            return Err(HigherCategoryError::OneCellNotComposable {
                first: first.to_string(),
                second: second.to_string(),
                tgt: f.tgt.clone(),
                src: s.src.clone(),
            });
        }
        self.compose_h_1_table
            .insert((first.to_string(), second.to_string()), comp.to_string());
        Ok(())
    }

    pub fn set_compose_v_1(
        &mut self,
        first: &str,
        second: &str,
        comp: &str,
    ) -> Result<(), HigherCategoryError> {
        let f = self.vert_one_cells.get(first).ok_or_else(|| {
            HigherCategoryError::OneCellNotFound { id: first.to_string() }
        })?;
        let s = self.vert_one_cells.get(second).ok_or_else(|| {
            HigherCategoryError::OneCellNotFound { id: second.to_string() }
        })?;
        if f.tgt != s.src {
            return Err(HigherCategoryError::OneCellNotComposable {
                first: first.to_string(),
                second: second.to_string(),
                tgt: f.tgt.clone(),
                src: s.src.clone(),
            });
        }
        self.compose_v_1_table
            .insert((first.to_string(), second.to_string()), comp.to_string());
        Ok(())
    }

    pub fn set_compose_square_h(
        &mut self,
        left: &str,
        right: &str,
        comp: &str,
    ) -> Result<(), HigherCategoryError> {
        let l = self.squares.get(left).ok_or_else(|| {
            HigherCategoryError::TwoCellNotFound { id: left.to_string() }
        })?;
        let r = self.squares.get(right).ok_or_else(|| {
            HigherCategoryError::TwoCellNotFound { id: right.to_string() }
        })?;

        if l.right_v != r.left_v {
            return Err(HigherCategoryError::SquareNotComposable {
                first: left.to_string(),
                second: right.to_string(),
                direction: "horizontal".to_string(),
                details: format!("left.right_v '{}' != right.left_v '{}'", l.right_v, r.left_v),
            });
        }

        self.compose_square_h_table
            .insert((left.to_string(), right.to_string()), comp.to_string());
        Ok(())
    }

    pub fn set_compose_square_v(
        &mut self,
        top: &str,
        bot: &str,
        comp: &str,
    ) -> Result<(), HigherCategoryError> {
        let t = self.squares.get(top).ok_or_else(|| {
            HigherCategoryError::TwoCellNotFound { id: top.to_string() }
        })?;
        let b = self.squares.get(bot).ok_or_else(|| {
            HigherCategoryError::TwoCellNotFound { id: bot.to_string() }
        })?;

        if t.bot_h != b.top_h {
            return Err(HigherCategoryError::SquareNotComposable {
                first: top.to_string(),
                second: bot.to_string(),
                direction: "vertical".to_string(),
                details: format!("top.bot_h '{}' != bot.top_h '{}'", t.bot_h, b.top_h),
            });
        }

        self.compose_square_v_table
            .insert((top.to_string(), bot.to_string()), comp.to_string());
        Ok(())
    }

    pub fn compose_square_h(&self, left: &str, right: &str) -> Result<String, HigherCategoryError> {
        let l = self.squares.get(left).ok_or_else(|| {
            HigherCategoryError::TwoCellNotFound { id: left.to_string() }
        })?;
        let r = self.squares.get(right).ok_or_else(|| {
            HigherCategoryError::TwoCellNotFound { id: right.to_string() }
        })?;

        if l.right_v != r.left_v {
            return Err(HigherCategoryError::SquareNotComposable {
                first: left.to_string(),
                second: right.to_string(),
                direction: "horizontal".to_string(),
                details: format!("left.right_v '{}' != right.left_v '{}'", l.right_v, r.left_v),
            });
        }

        self.compose_square_h_table
            .get(&(left.to_string(), right.to_string()))
            .cloned()
            .ok_or_else(|| HigherCategoryError::SquareNotComposable {
                first: left.to_string(),
                second: right.to_string(),
                direction: "horizontal".to_string(),
                details: "composite not registered in table".to_string(),
            })
    }

    pub fn compose_square_v(&self, top: &str, bot: &str) -> Result<String, HigherCategoryError> {
        let t = self.squares.get(top).ok_or_else(|| {
            HigherCategoryError::TwoCellNotFound { id: top.to_string() }
        })?;
        let b = self.squares.get(bot).ok_or_else(|| {
            HigherCategoryError::TwoCellNotFound { id: bot.to_string() }
        })?;

        if t.bot_h != b.top_h {
            return Err(HigherCategoryError::SquareNotComposable {
                first: top.to_string(),
                second: bot.to_string(),
                direction: "vertical".to_string(),
                details: format!("top.bot_h '{}' != bot.top_h '{}'", t.bot_h, b.top_h),
            });
        }

        self.compose_square_v_table
            .get(&(top.to_string(), bot.to_string()))
            .cloned()
            .ok_or_else(|| HigherCategoryError::SquareNotComposable {
                first: top.to_string(),
                second: bot.to_string(),
                direction: "vertical".to_string(),
                details: "composite not registered in table".to_string(),
            })
    }

    pub fn verify_interchange(
        &self,
        alpha: &str,
        beta: &str,
        gamma: &str,
        delta: &str,
    ) -> Result<(), HigherCategoryError> {
        SquareInterchange::verify_interchange(self, alpha, beta, gamma, delta)
    }

    pub fn verify_all_interchanges(&self) -> Result<usize, HigherCategoryError> {
        let mut grids = Vec::new();
        let square_ids: Vec<&String> = self.squares.keys().collect();
        for &a in &square_ids {
            for &b in &square_ids {
                if self.squares[a].right_v != self.squares[b].left_v {
                    continue;
                }
                for &c in &square_ids {
                    if self.squares[a].bot_h != self.squares[c].top_h {
                        continue;
                    }
                    for &d in &square_ids {
                        if self.squares[c].right_v != self.squares[d].left_v {
                            continue;
                        }
                        if self.squares[b].bot_h != self.squares[d].top_h {
                            continue;
                        }
                        reserve_exact(&mut grids, 1, &self.limits)?;
                        grids.push((a.clone(), b.clone(), c.clone(), d.clone()));
                    }
                }
            }
        }

        let mut count = 0;
        for (a, b, c, d) in &grids {
            self.verify_interchange(a, b, c, d)?;
            count += 1;
        }
        Ok(count)
    }

    pub fn content_hash(&self) -> String {
        let mut hasher = Sha256::new();
        hasher.update(self.name.as_bytes());
        for z in &self.zero_cells {
            hasher.update(z.as_bytes());
        }
        for (id, h) in &self.horiz_one_cells {
            hasher.update(id.as_bytes());
            hasher.update(h.src.as_bytes());
            hasher.update(h.tgt.as_bytes());
        }
        for (id, v) in &self.vert_one_cells {
            hasher.update(id.as_bytes());
            hasher.update(v.src.as_bytes());
            hasher.update(v.tgt.as_bytes());
        }
        for (id, sq) in &self.squares {
            hasher.update(id.as_bytes());
            hasher.update(sq.top_h.as_bytes());
            hasher.update(sq.bot_h.as_bytes());
            hasher.update(sq.left_v.as_bytes());
            hasher.update(sq.right_v.as_bytes());
        }
        format!("{:x}", hasher.finalize())
    }
}
