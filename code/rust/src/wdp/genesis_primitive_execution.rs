use num_bigint::{BigInt, BigUint};
use omega_combinatorics::cartesian_words::CartesianWords;
use omega_combinatorics::enumeration::CombinatoricsError;
use serde::{Deserialize, Serialize};
use std::collections::BTreeSet;

#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum PrimitiveExecutionError {
    #[error("ill-formed admitted regime or event")]
    InvalidArgument,
    #[error("native index or dimension overflow")]
    IndexOverflow,
    #[error("source candidate enumeration is declared only through two items")]
    OutsideCandidateBounds,
    #[error("complete intermediate regime or reading differs")]
    IntermediateMismatch,
    #[error("exact finite enumeration refused: {0}")]
    Enumeration(#[from] CombinatoricsError),
}

#[derive(Debug, Clone, PartialEq, Eq, PartialOrd, Ord, Serialize, Deserialize)]
pub struct PrimitiveInstance {
    pub form: usize,
    pub args: Vec<usize>,
}
#[derive(Debug, Clone, PartialEq, Eq, PartialOrd, Ord, Serialize, Deserialize)]
pub struct PrimitiveContext {
    pub form: usize,
    pub slots: Vec<Option<usize>>,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum PrimitiveReading {
    Dedup,
    Occurrence,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(tag = "kind", rename_all = "snake_case", deny_unknown_fields)]
pub enum PrimitiveEvent {
    Supply { token: String },
    AdmitDatum { token: String },
    AdmitForm { arity: usize },
    AdmitInst { form: usize, args: Vec<usize> },
    AdmitRuleAll { form: usize },
    Impose { i: usize, j: usize },
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct PrimitiveRegime {
    data: Vec<String>,
    forms: Vec<usize>,
    insts: BTreeSet<PrimitiveInstance>,
    rules: BTreeSet<usize>,
    requirements: BTreeSet<(usize, usize)>,
}
impl PrimitiveRegime {
    pub fn try_new(
        data: Vec<String>,
        forms: Vec<usize>,
        insts: BTreeSet<PrimitiveInstance>,
        rules: BTreeSet<usize>,
        requirements: BTreeSet<(usize, usize)>,
    ) -> Result<Self, PrimitiveExecutionError> {
        let regime = Self {
            data,
            forms,
            insts,
            rules,
            requirements,
        };
        if regime.forms.contains(&0)
            || regime.insts.iter().any(|inst| !regime.well_formed(inst))
            || regime.rules.iter().any(|&f| f >= regime.forms.len())
            || regime
                .requirements
                .iter()
                .any(|&(i, j)| i >= j || j >= regime.data.len())
        {
            return Err(PrimitiveExecutionError::InvalidArgument);
        }
        Ok(regime)
    }
    pub fn empty() -> Self {
        Self {
            data: vec![],
            forms: vec![],
            insts: BTreeSet::new(),
            rules: BTreeSet::new(),
            requirements: BTreeSet::new(),
        }
    }
    pub fn data(&self) -> &[String] {
        &self.data
    }
    pub fn forms(&self) -> &[usize] {
        &self.forms
    }
    pub fn instances(&self) -> &BTreeSet<PrimitiveInstance> {
        &self.insts
    }
    pub fn rules(&self) -> &BTreeSet<usize> {
        &self.rules
    }
    pub fn requirements(&self) -> &BTreeSet<(usize, usize)> {
        &self.requirements
    }
    fn well_formed(&self, inst: &PrimitiveInstance) -> bool {
        self.forms.get(inst.form) == Some(&inst.args.len())
            && inst.args.iter().all(|&a| a < self.data.len())
    }
    pub fn step(
        &self,
        event: &PrimitiveEvent,
        reading: PrimitiveReading,
    ) -> Result<Self, PrimitiveExecutionError> {
        let mut after = self.clone();
        match event {
            PrimitiveEvent::Supply { .. } => {}
            PrimitiveEvent::AdmitDatum { token } => {
                if reading == PrimitiveReading::Occurrence || !after.data.contains(token) {
                    after
                        .data
                        .len()
                        .checked_add(1)
                        .ok_or(PrimitiveExecutionError::IndexOverflow)?;
                    after.data.push(token.clone());
                }
            }
            PrimitiveEvent::AdmitForm { arity } => {
                if *arity == 0 {
                    return Err(PrimitiveExecutionError::InvalidArgument);
                }
                after
                    .forms
                    .len()
                    .checked_add(1)
                    .ok_or(PrimitiveExecutionError::IndexOverflow)?;
                after.forms.push(*arity);
            }
            PrimitiveEvent::AdmitInst { form, args } => {
                let inst = PrimitiveInstance {
                    form: *form,
                    args: args.clone(),
                };
                if !self.well_formed(&inst) {
                    return Err(PrimitiveExecutionError::InvalidArgument);
                }
                after.insts.insert(inst);
            }
            PrimitiveEvent::AdmitRuleAll { form } => {
                if *form >= self.forms.len() {
                    return Err(PrimitiveExecutionError::InvalidArgument);
                }
                after.rules.insert(*form);
            }
            PrimitiveEvent::Impose { i, j } => {
                if i >= j || *j >= self.data.len() {
                    return Err(PrimitiveExecutionError::InvalidArgument);
                }
                after.requirements.insert((*i, *j));
            }
        }
        Ok(after)
    }
    fn raw_derivable(&self, inst: &PrimitiveInstance) -> bool {
        self.rules.contains(&inst.form) || self.insts.contains(inst)
    }
    pub fn derivable(&self, inst: &PrimitiveInstance) -> Result<bool, PrimitiveExecutionError> {
        if !self.well_formed(inst) {
            return Err(PrimitiveExecutionError::InvalidArgument);
        }
        Ok(self.raw_derivable(inst))
    }
    pub fn contexts(
        &self,
        limits: PrimitiveLimits,
    ) -> Result<Vec<PrimitiveContext>, PrimitiveExecutionError> {
        let base = self
            .data
            .len()
            .checked_add(1)
            .ok_or(PrimitiveExecutionError::IndexOverflow)?;
        let mut remaining = limits.max_tuples;
        let mut out = Vec::new();
        for (form, &arity) in self.forms.iter().enumerate() {
            let words = CartesianWords::new(base, arity, remaining, limits.max_width)?;
            remaining -= words.cardinality();
            for word in words {
                if word.contains(&0) {
                    out.push(PrimitiveContext {
                        form,
                        slots: word
                            .into_iter()
                            .map(|s| if s == 0 { None } else { Some(s - 1) })
                            .collect(),
                    });
                }
            }
        }
        Ok(out)
    }
    fn plug(context: &PrimitiveContext, d: usize) -> PrimitiveInstance {
        PrimitiveInstance {
            form: context.form,
            args: context.slots.iter().map(|s| s.unwrap_or(d)).collect(),
        }
    }
    pub fn profiles(
        &self,
        limits: PrimitiveLimits,
    ) -> Result<Vec<BTreeSet<PrimitiveContext>>, PrimitiveExecutionError> {
        let contexts = self.contexts(limits)?;
        Ok((0..self.data.len())
            .map(|d| {
                contexts
                    .iter()
                    .filter(|c| self.raw_derivable(&Self::plug(c, d)))
                    .cloned()
                    .collect()
            })
            .collect())
    }
    pub fn witness(
        &self,
        i: usize,
        j: usize,
        limits: PrimitiveLimits,
    ) -> Result<Option<PrimitiveContext>, PrimitiveExecutionError> {
        if i >= self.data.len() || j >= self.data.len() {
            return Err(PrimitiveExecutionError::InvalidArgument);
        }
        Ok(self.contexts(limits)?.into_iter().find(|c| {
            self.raw_derivable(&Self::plug(c, i)) != self.raw_derivable(&Self::plug(c, j))
        }))
    }
    pub fn collapsed_pairs(
        &self,
        limits: PrimitiveLimits,
    ) -> Result<Vec<(usize, usize)>, PrimitiveExecutionError> {
        let profiles = self.profiles(limits)?;
        Ok((0..profiles.len())
            .flat_map(|i| {
                (i + 1..profiles.len())
                    .filter_map(|j| {
                        if profiles[i] == profiles[j] {
                            Some((i, j))
                        } else {
                            None
                        }
                    })
                    .collect::<Vec<_>>()
            })
            .collect())
    }
    pub fn satisfies(&self, limits: PrimitiveLimits) -> Result<bool, PrimitiveExecutionError> {
        let profiles = self.profiles(limits)?;
        Ok(self
            .requirements
            .iter()
            .all(|&(i, j)| profiles[i] != profiles[j]))
    }
    pub fn delta_events(
        &self,
        delta: &PrimitiveDelta,
    ) -> Result<Vec<PrimitiveEvent>, PrimitiveExecutionError> {
        let mut n = self.data.len();
        let mut out = Vec::new();
        for item in &delta.items {
            out.push(match item {
                PrimitiveItem::NewDatum => {
                    let event = PrimitiveEvent::AdmitDatum {
                        token: format!("w{n}"),
                    };
                    n = n
                        .checked_add(1)
                        .ok_or(PrimitiveExecutionError::IndexOverflow)?;
                    event
                }
                PrimitiveItem::NewForm { arity } => PrimitiveEvent::AdmitForm { arity: *arity },
                PrimitiveItem::NewRuleAll { form } => PrimitiveEvent::AdmitRuleAll { form: *form },
                PrimitiveItem::NewInst { form, args } => PrimitiveEvent::AdmitInst {
                    form: *form,
                    args: args.clone(),
                },
            });
        }
        Ok(out)
    }
    pub fn apply_delta(&self, delta: &PrimitiveDelta) -> Result<Self, PrimitiveExecutionError> {
        Ok(PrimitiveRun::replay(
            self.clone(),
            &self.delta_events(delta)?,
            PrimitiveReading::Dedup,
        )?
        .final_state()
        .clone())
    }
    pub fn response_valid(
        &self,
        target: (usize, usize),
        delta: &PrimitiveDelta,
        limits: PrimitiveLimits,
    ) -> Result<bool, PrimitiveExecutionError> {
        self.apply_delta(delta)?
            .step(
                &PrimitiveEvent::Impose {
                    i: target.0,
                    j: target.1,
                },
                PrimitiveReading::Dedup,
            )?
            .satisfies(limits)
    }
    pub fn full_deltas(
        &self,
        cost: usize,
        max_arity: usize,
        limits: PrimitiveLimits,
    ) -> Result<Vec<PrimitiveDelta>, PrimitiveExecutionError> {
        if cost > 2 {
            return Err(PrimitiveExecutionError::OutsideCandidateBounds);
        }
        if limits.max_candidates == 0 {
            return Err(CombinatoricsError::BudgetExceeded {
                what: "candidate items",
                requested: 1u8.into(),
                limit: 0,
            }
            .into());
        }
        if cost == 0 {
            return Ok(vec![PrimitiveDelta::new(vec![])]);
        }
        let mut universe = vec![PrimitiveItem::NewDatum];
        let mut remaining = limits.max_candidates - 1;
        let mut append = |item| -> Result<(), PrimitiveExecutionError> {
            if remaining == 0 {
                return Err(CombinatoricsError::BudgetExceeded {
                    what: "candidate items",
                    requested: BigUint::from(limits.max_candidates) + 1u8,
                    limit: limits.max_candidates,
                }
                .into());
            }
            remaining -= 1;
            universe.push(item);
            Ok(())
        };
        for arity in 1..=max_arity {
            append(PrimitiveItem::NewForm { arity })?;
        }
        let max_form = if cost == 1 {
            self.forms.len()
        } else {
            self.forms
                .len()
                .checked_add(1)
                .ok_or(PrimitiveExecutionError::IndexOverflow)?
        };
        let max_width = if cost == 1 {
            0
        } else {
            self.forms.iter().copied().max().unwrap_or(0).max(max_arity)
        };
        if cost == 2 {
            CartesianWords::new(0, max_width, 1, limits.max_width)?;
        }
        let base = self
            .data
            .len()
            .checked_add(usize::from(cost == 2))
            .ok_or(PrimitiveExecutionError::IndexOverflow)?;
        let mut tuple_budget = limits.max_tuples;
        if cost == 1 {
            for form in 0..max_form {
                if !self.rules.contains(&form) {
                    append(PrimitiveItem::NewRuleAll { form })?;
                }
            }
        }
        for form in 0..max_form {
            if cost == 2 {
                append(PrimitiveItem::NewRuleAll { form })?;
            }
            let arities: Vec<_> = if cost == 1 {
                vec![self.forms[form]]
            } else {
                (1..=max_width).collect()
            };
            for arity in arities {
                let words = CartesianWords::new(base, arity, tuple_budget, limits.max_width)?;
                tuple_budget -= words.cardinality();
                for args in words {
                    append(PrimitiveItem::NewInst { form, args })?;
                }
            }
        }
        if cost == 1 {
            return Ok(universe
                .into_iter()
                .map(|item| PrimitiveDelta::new(vec![item]))
                .collect());
        }
        let words =
            CartesianWords::new(universe.len(), 2, limits.max_candidates, limits.max_width)?;
        let mut seen = BTreeSet::new();
        let mut out = Vec::new();
        for pair in words {
            let delta =
                PrimitiveDelta::new(vec![universe[pair[0]].clone(), universe[pair[1]].clone()]);
            if seen.insert(delta.clone()) {
                match self.apply_delta(&delta) {
                    Ok(_) => out.push(delta),
                    Err(PrimitiveExecutionError::InvalidArgument) => {}
                    Err(error) => return Err(error),
                }
            }
        }
        Ok(out)
    }
    pub fn minimum_responses_checked(
        &self,
        target: (usize, usize),
        measure: PrimitiveMeasure,
        max_items: usize,
        max_arity: usize,
        limits: PrimitiveLimits,
    ) -> Result<Option<PrimitiveMinimum>, PrimitiveExecutionError> {
        if max_items > 2 {
            return Err(PrimitiveExecutionError::OutsideCandidateBounds);
        }
        if target.0 >= target.1 || target.1 >= self.data.len() {
            return Err(PrimitiveExecutionError::InvalidArgument);
        }
        for cost in 0..=max_items {
            let mut valid = BTreeSet::new();
            for delta in self.full_deltas(cost, max_arity, limits)? {
                match self.response_valid(target, &delta, limits) {
                    Ok(true) => {
                        valid.insert(delta);
                    }
                    Ok(false) | Err(PrimitiveExecutionError::InvalidArgument) => {}
                    Err(error) => return Err(error),
                }
            }
            if !valid.is_empty() {
                let arity = if measure == PrimitiveMeasure::ItemsThenArity {
                    valid.iter().map(|d| d.price().1).min().unwrap()
                } else {
                    BigInt::from(-1)
                };
                let deltas = valid
                    .into_iter()
                    .filter(|d| measure == PrimitiveMeasure::Items || d.price().1 == arity)
                    .collect();
                return Ok(Some(PrimitiveMinimum {
                    price: (BigInt::from(cost), arity),
                    deltas,
                }));
            }
        }
        Ok(None)
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct PrimitiveLimits {
    pub max_tuples: usize,
    pub max_width: usize,
    pub max_candidates: usize,
}

#[derive(Debug, Clone, PartialEq, Eq, PartialOrd, Ord, Serialize, Deserialize)]
#[serde(tag = "kind", rename_all = "snake_case", deny_unknown_fields)]
pub enum PrimitiveItem {
    NewDatum,
    NewForm { arity: usize },
    NewRuleAll { form: usize },
    NewInst { form: usize, args: Vec<usize> },
}
#[derive(Debug, Clone, PartialEq, Eq, PartialOrd, Ord)]
pub struct PrimitiveDelta {
    items: Vec<PrimitiveItem>,
}
impl PrimitiveDelta {
    pub fn new(mut items: Vec<PrimitiveItem>) -> Self {
        items.sort();
        Self { items }
    }
    pub fn items(&self) -> &[PrimitiveItem] {
        &self.items
    }
    pub fn price(&self) -> (BigInt, BigInt) {
        (
            BigInt::from(self.items.len()),
            self.items
                .iter()
                .map(|item| match item {
                    PrimitiveItem::NewForm { arity } => BigInt::from(*arity),
                    _ => BigInt::from(0),
                })
                .sum(),
        )
    }
}
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum PrimitiveMeasure {
    Items,
    ItemsThenArity,
}
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct PrimitiveMinimum {
    pub price: (BigInt, BigInt),
    pub deltas: Vec<PrimitiveDelta>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct PrimitiveRun {
    reading: PrimitiveReading,
    states: Vec<PrimitiveRegime>,
    events: Vec<PrimitiveEvent>,
}
impl PrimitiveRun {
    pub fn replay(
        initial: PrimitiveRegime,
        events: &[PrimitiveEvent],
        reading: PrimitiveReading,
    ) -> Result<Self, PrimitiveExecutionError> {
        let mut states = vec![initial];
        for event in events {
            states.push(states.last().unwrap().step(event, reading)?);
        }
        Ok(Self {
            reading,
            states,
            events: events.to_vec(),
        })
    }
    pub fn states(&self) -> &[PrimitiveRegime] {
        &self.states
    }
    pub fn events(&self) -> &[PrimitiveEvent] {
        &self.events
    }
    pub fn final_state(&self) -> &PrimitiveRegime {
        self.states.last().unwrap()
    }
    pub fn then(&self, after: &Self) -> Result<Self, PrimitiveExecutionError> {
        if self.reading != after.reading || self.final_state() != &after.states[0] {
            return Err(PrimitiveExecutionError::IntermediateMismatch);
        }
        let mut states = self.states.clone();
        states.extend_from_slice(&after.states[1..]);
        let mut events = self.events.clone();
        events.extend_from_slice(&after.events);
        Ok(Self {
            reading: self.reading,
            states,
            events,
        })
    }
}
