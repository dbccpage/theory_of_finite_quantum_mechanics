//! Genesis refusal comparison and the separate 64-description constitution.
//! These are distinct source models, not extra toggles of PassageState.
//! Original `Refusal.stepR` is the projection forgetting forms/instances of the
//! richer Python comparison. Meta markers live in the history only.

use crate::genesis_passage::{separated, separates, Column, Pair};
use serde::{Deserialize, Serialize};
use std::collections::BTreeSet;

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum Discipline {
    Silent,
    Meta,
    Fact,
    ReifyUntagged,
    ReifyTagged,
    Occurrence,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum RefusalEvent {
    Supply(String),
    Admit(String),
    Marker(String),
    Form,
    Instance(usize),
}

#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct RefusalState {
    pub data: Vec<String>,
    pub tags: BTreeSet<usize>,
    pub refusals: usize,
    pub has_form: bool,
    pub insts: BTreeSet<usize>,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum RefusalError {
    CounterOverflow,
    InvalidDescription,
}

impl RefusalState {
    pub fn step(&self, mode: Discipline, event: &RefusalEvent) -> Result<Self, RefusalError> {
        let mut out = self.clone();
        match event {
            RefusalEvent::Supply(_) | RefusalEvent::Marker(_) => (),
            RefusalEvent::Form => out.has_form = true,
            RefusalEvent::Instance(i) => {
                if self.has_form && *i < self.data.len() {
                    out.insts.insert(*i);
                }
            }
            RefusalEvent::Admit(tok) => {
                if mode == Discipline::Occurrence || !self.data.contains(tok) {
                    out.data.push(tok.clone());
                } else {
                    match mode {
                        Discipline::Silent | Discipline::Meta => (),
                        Discipline::Fact => {
                            out.refusals = self
                                .refusals
                                .checked_add(1)
                                .ok_or(RefusalError::CounterOverflow)?
                        }
                        Discipline::ReifyUntagged => out.data.push(tok.clone()),
                        Discipline::ReifyTagged => {
                            out.tags.insert(out.data.len());
                            out.data.push(tok.clone());
                        }
                        Discipline::Occurrence => (),
                    }
                }
            }
        }
        Ok(out)
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub struct Constitution {
    pub dedup_admit: bool,
    pub guard_require: bool,
    pub guard_accept: bool,
    pub gate_budget: bool,
    pub gate_license: bool,
    pub cert_refusal: bool,
}

impl Constitution {
    pub const KERNEL: Self = Self {
        dedup_admit: true,
        guard_require: true,
        guard_accept: true,
        gate_budget: true,
        gate_license: true,
        cert_refusal: true,
    };

    /// Original Lean `allDescs` order: first field slowest, last fastest.
    /// This is NOT the educational `Desc.to_index` (first field least bit).
    pub fn from_lean_index(index: usize) -> Result<Self, RefusalError> {
        if index >= 64 {
            return Err(RefusalError::InvalidDescription);
        }
        Ok(Self {
            dedup_admit: index & 32 != 0,
            guard_require: index & 16 != 0,
            guard_accept: index & 8 != 0,
            gate_budget: index & 4 != 0,
            gate_license: index & 2 != 0,
            cert_refusal: index & 1 != 0,
        })
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct RepresentedWorld {
    pub data: Vec<usize>,
    pub views: Vec<Column>,
    pub reqs: Vec<Pair>,
    pub refusals: Vec<Pair>,
    pub budget: usize,
    pub aug_licensed: bool,
    pub notes: Vec<usize>,
}

impl Default for RepresentedWorld {
    fn default() -> Self {
        Self {
            data: vec![],
            views: vec![],
            reqs: vec![],
            refusals: vec![],
            budget: 0,
            aug_licensed: true,
            notes: vec![],
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum WorldEvent {
    Admit(usize),
    Require(usize, usize),
    Mark(Column, usize),
    AddView(Column),
    Refuse(usize, usize),
    Note(usize),
    SetBudget(usize),
    SetAugLicense(bool),
}

impl RepresentedWorld {
    pub fn satisfied(&self, r: Pair) -> bool {
        separated(&self.views, r.0, r.1)
    }
    pub fn violated(&self, r: Pair) -> bool {
        self.reqs.contains(&r) && !self.satisfied(r)
    }

    fn mark_apply(&self, v: &Column, p: usize) -> Self {
        let mut out = self.clone();
        out.views = self
            .views
            .iter()
            .map(|c| {
                if c == v {
                    std::iter::once(p).chain(c.iter().copied()).collect()
                } else {
                    c.clone()
                }
            })
            .collect();
        out
    }

    pub fn mark_ok(&self, v: &Column, p: usize) -> bool {
        if !self.views.contains(v) || p >= self.data.len() || v.contains(&p) {
            return false;
        }
        let after = self.mark_apply(v, p);
        self.reqs
            .iter()
            .any(|&r| self.violated(r) && after.satisfied(r))
            && self
                .reqs
                .iter()
                .all(|&r| !self.satisfied(r) || after.satisfied(r))
    }

    pub fn augmentation_ok(&self, c: &Column) -> bool {
        c.iter().all(|&p| p < self.data.len())
            && !self.views.contains(c)
            && (0..self.data.len()).any(|i| {
                (0..self.data.len())
                    .any(|j| i != j && separates(c, i, j) && !self.satisfied((i, j)))
            })
    }

    /// Exhausts the declared SAME-LEVEL response menu. Budget/license do not
    /// enter this predicate; absence of fuel is not a proof of no repair.
    pub fn obstructed(&self, r: Pair) -> bool {
        self.violated(r)
            && self.views.iter().all(|v| {
                (0..self.data.len())
                    .all(|p| !self.mark_ok(v, p) || !self.mark_apply(v, p).satisfied(r))
            })
    }

    pub fn step(&self, d: Constitution, e: &WorldEvent) -> Self {
        let mut out = self.clone();
        match e {
            WorldEvent::Admit(t) => {
                if !d.dedup_admit || !self.data.contains(t) {
                    out.data.push(*t);
                }
            }
            WorldEvent::Require(i, j) => {
                if !d.guard_require
                    || (i != j
                        && *i < self.data.len()
                        && *j < self.data.len()
                        && !self.reqs.contains(&(*i, *j)))
                {
                    out.reqs.push((*i, *j));
                }
            }
            WorldEvent::Mark(v, p) => {
                if (!d.guard_accept || self.mark_ok(v, *p)) && (!d.gate_budget || self.budget > 0) {
                    out = self.mark_apply(v, *p);
                    out.budget = self.budget.saturating_sub(1);
                }
            }
            WorldEvent::AddView(c) => {
                if (!d.guard_accept || self.augmentation_ok(c))
                    && (!d.gate_license || self.aug_licensed)
                    && (!d.gate_budget || self.budget > 0)
                {
                    out.views.push(c.clone());
                    out.budget = self.budget.saturating_sub(1);
                }
            }
            WorldEvent::Refuse(i, j) => {
                if (!d.cert_refusal || self.obstructed((*i, *j)))
                    && !self.refusals.contains(&(*i, *j))
                {
                    out.refusals.push((*i, *j));
                }
            }
            WorldEvent::Note(n) => out.notes.push(*n),
            WorldEvent::SetBudget(n) => out.budget = *n,
            WorldEvent::SetAugLicense(b) => out.aug_licensed = *b,
        }
        out
    }
}
