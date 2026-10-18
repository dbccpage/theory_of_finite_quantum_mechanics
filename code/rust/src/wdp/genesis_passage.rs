//! Native port of Genesis `PrimitivePassage.step` (the original paper kernel).
//!
//! Positions index `occ`; token values are not positions. Store order, directed
//! pairs, and column order are significant. A guarded-out event is a no-op in
//! the source's TOTAL replay. `enabled` additionally declares the guard-success
//! partial-operation reading used by the continuation adapter. Resource refusal
//! is neither a source no-op nor an obstruction certificate.

use serde::{Deserialize, Serialize};

pub type Pair = (usize, usize);
pub type Column = Vec<usize>;

#[derive(Debug, Clone, PartialEq, Eq, PartialOrd, Ord, Serialize, Deserialize)]
pub struct PassageState {
    pub occ: Vec<usize>,
    pub asserted: Vec<Pair>,
    pub wit: Vec<Pair>,
    pub prot: Vec<Pair>,
    pub obs: Option<Vec<Column>>,
    pub budget: usize,
    pub licensed: bool,
    pub refusals: Vec<Pair>,
    pub halted: bool,
}

impl Default for PassageState {
    fn default() -> Self {
        Self {
            occ: vec![],
            asserted: vec![],
            wit: vec![],
            prot: vec![],
            obs: None,
            budget: 0,
            licensed: true,
            refusals: vec![],
            halted: false,
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq, PartialOrd, Ord, Serialize, Deserialize)]
pub enum PassageEvent {
    AdmitOcc(usize),
    AssertWit(usize, usize),
    AdmitWit(usize, usize),
    Protect(usize, usize),
    DeclareObs,
    RefineCol(Column, usize),
    AddCol(Column),
    Refuse(usize, usize),
    SetBudget(usize),
    SetLicense(bool),
    Halt,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum PassageError {
    ResourceLimit,
}

pub fn separates(column: &[usize], i: usize, j: usize) -> bool {
    column.contains(&i) != column.contains(&j)
}

pub fn separated(columns: &[Column], i: usize, j: usize) -> bool {
    columns.iter().any(|c| separates(c, i, j))
}

impl PassageState {
    /// Original `zeroDeclP`: true before declaration, a convention, not an
    /// assertion that an undeclared observer exists. Educational `zero_p_gate`
    /// is the strict alternative (`declared && zero_declared`).
    pub fn zero_declared(&self, i: usize, j: usize) -> bool {
        self.obs.as_ref().is_none_or(|cols| !separated(cols, i, j))
    }

    pub fn gates(&self, i: usize, j: usize) -> [bool; 4] {
        [
            self.wit.contains(&(i, j)),
            self.prot.contains(&(i, j)),
            self.obs.is_some(),
            self.zero_declared(i, j),
        ]
    }

    pub fn obstructed(&self, i: usize, j: usize) -> bool {
        self.gates(i, j).into_iter().all(|b| b)
    }

    pub fn well_formed_pair(&self, i: usize, j: usize) -> bool {
        i != j && i < self.occ.len() && j < self.occ.len()
    }

    fn refined(columns: &[Column], v: &Column, p: usize) -> Vec<Column> {
        columns
            .iter()
            .map(|c| {
                if c == v {
                    std::iter::once(p).chain(c.iter().copied()).collect()
                } else {
                    c.clone()
                }
            })
            .collect()
    }

    pub fn refine_ok(&self, v: &Column, p: usize) -> bool {
        let Some(cols) = &self.obs else { return false };
        if !cols.contains(v) || p >= self.occ.len() || v.contains(&p) {
            return false;
        }
        let replacement: Column = std::iter::once(p).chain(v.iter().copied()).collect();
        if !self
            .prot
            .iter()
            .any(|&(i, j)| self.obstructed(i, j) && separates(&replacement, i, j))
        {
            return false;
        }
        let after = Self::refined(cols, v, p);
        self.prot
            .iter()
            .all(|&(i, j)| !separated(cols, i, j) || separated(&after, i, j))
    }

    pub fn column_ok(&self, c: &Column) -> bool {
        self.obs.as_ref().is_some_and(|cols| {
            c.iter().all(|&p| p < self.occ.len())
                && !cols.contains(c)
                && self
                    .prot
                    .iter()
                    .any(|&(i, j)| self.obstructed(i, j) && separates(c, i, j))
        })
    }

    /// Guard-success reading. Idempotent admissions/settings remain available;
    /// halt is available even at a terminal. This is declared alongside, and
    /// does not change, the source's total no-op semantics.
    pub fn enabled(&self, event: &PassageEvent) -> bool {
        use PassageEvent::*;
        if matches!(event, Halt) {
            return true;
        }
        if self.halted {
            return false;
        }
        match event {
            AdmitOcc(_) | DeclareObs | SetBudget(_) | SetLicense(_) => true,
            AssertWit(i, j) => self.well_formed_pair(*i, *j),
            AdmitWit(i, j) => self.well_formed_pair(*i, *j) && self.asserted.contains(&(*i, *j)),
            Protect(i, j) => self.wit.contains(&(*i, *j)),
            RefineCol(v, p) => self.refine_ok(v, *p) && self.budget > 0,
            AddCol(c) => self.column_ok(c) && self.licensed && self.budget > 0,
            Refuse(i, j) => self.obstructed(*i, *j),
            Halt => true,
        }
    }

    /// Exact total transition on the Rust natural-number fragment of the
    /// original Lean state. In particular refinement does NOT require license;
    /// passage refusal records active obstruction, NOT response exhaustion.
    pub fn step(&self, event: &PassageEvent) -> Self {
        use PassageEvent::*;
        if !self.enabled(event) {
            return self.clone();
        }
        let mut out = self.clone();
        match event {
            AdmitOcc(t) => {
                if !out.occ.contains(t) {
                    out.occ.push(*t);
                }
            }
            AssertWit(i, j) => {
                if !out.asserted.contains(&(*i, *j)) {
                    out.asserted.push((*i, *j));
                }
            }
            AdmitWit(i, j) => {
                if !out.wit.contains(&(*i, *j)) {
                    out.wit.push((*i, *j));
                }
            }
            Protect(i, j) => {
                if !out.prot.contains(&(*i, *j)) {
                    out.prot.push((*i, *j));
                }
            }
            DeclareObs => {
                if out.obs.is_none() {
                    out.obs = Some(vec![]);
                }
            }
            RefineCol(v, p) => {
                if let Some(cols) = &self.obs {
                    out.obs = Some(Self::refined(cols, v, *p));
                    out.budget -= 1;
                }
            }
            AddCol(c) => {
                if let Some(cols) = &mut out.obs {
                    cols.push(c.clone());
                    out.budget -= 1;
                }
            }
            Refuse(i, j) => {
                if !out.refusals.contains(&(*i, *j)) {
                    out.refusals.push((*i, *j));
                }
            }
            SetBudget(n) => out.budget = *n,
            SetLicense(b) => out.licensed = *b,
            Halt => out.halted = true,
        }
        out
    }

    /// A structural-cell bound, not a bound on numeric values or CPU time.
    pub fn within_cells(&self, limit: usize) -> bool {
        let mut total = Some(self.occ.len());
        for count in [
            self.asserted.len(),
            self.wit.len(),
            self.prot.len(),
            self.refusals.len(),
        ] {
            total = total.and_then(|n| count.checked_mul(2).and_then(|m| n.checked_add(m)));
        }
        if let Some(cols) = &self.obs {
            total = total.and_then(|n| n.checked_add(cols.len()));
            for c in cols {
                total = total.and_then(|n| n.checked_add(c.len()));
            }
        }
        total.is_some_and(|n| n <= limit)
    }

    /// Original `nextFamilyP`: all same-level repair blocks, then singleton
    /// funded extension proposals, per obstructed protected pair. Keeps ties
    /// and repeats. This is a proposal family: halted/license/budget gates are
    /// still checked on execution and do not disappear because of membership.
    pub fn next_family(
        &self,
        max_candidates: usize,
    ) -> Result<Vec<Vec<PassageEvent>>, PassageError> {
        let cols = self.obs.as_deref().unwrap_or(&[]);
        let work = cols
            .len()
            .checked_add(1)
            .and_then(|n| n.checked_mul(self.occ.len()))
            .and_then(|n| n.checked_mul(self.prot.len()));
        if work.is_none_or(|n| n > max_candidates) {
            return Err(PassageError::ResourceLimit);
        }
        let mut out = Vec::new();
        for &(i, j) in &self.prot {
            if !self.obstructed(i, j) {
                continue;
            }
            for v in cols {
                for p in 0..self.occ.len() {
                    if self.refine_ok(v, p) && separated(&Self::refined(cols, v, p), i, j) {
                        out.push(vec![PassageEvent::RefineCol(v.clone(), p)]);
                    }
                }
            }
            for p in 0..self.occ.len() {
                let column = vec![p];
                if self.column_ok(&column) && separates(&column, i, j) {
                    out.push(vec![
                        PassageEvent::SetBudget(1),
                        PassageEvent::AddCol(column),
                    ]);
                }
            }
        }
        Ok(out)
    }
}

pub fn replay(
    events: &[PassageEvent],
    max_events: usize,
    max_cells: usize,
) -> Result<PassageState, PassageError> {
    if events.len() > max_events {
        return Err(PassageError::ResourceLimit);
    }
    let mut state = PassageState::default();
    for e in events {
        if matches!(e, PassageEvent::AddCol(c) | PassageEvent::RefineCol(c,_) if c.len() > max_cells)
        {
            return Err(PassageError::ResourceLimit);
        }
        state = state.step(e);
        if !state.within_cells(max_cells) {
            return Err(PassageError::ResourceLimit);
        }
    }
    Ok(state)
}
