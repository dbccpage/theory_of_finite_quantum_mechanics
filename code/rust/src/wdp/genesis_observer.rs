
use crate::types::AuthorityEffect;
use tfqm_category_theory::finite_history_context::{
    run, FiniteWordTransducer, HistoryContext, HistoryDescent, HistoryError, StateContextLift,
};
use tfqm_category_theory::finite_moore::FiniteMoore;
use std::collections::{BTreeMap, BTreeSet, VecDeque};

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum OriginalObserverError {
    InvalidDomain,
    InvalidInitialState,
    UnknownContext,
    UnknownGrammar,
    MissingEncoder,
    InvalidEncoder,
    History(HistoryError),
}
impl From<HistoryError> for OriginalObserverError {
    fn from(error: HistoryError) -> Self {
        Self::History(error)
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum GenesisTerminal {
    Proved,
    Refuted,
    Unresolved,
    Outside,
    Refused,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct GenesisSixData {
    pub states: Vec<String>,
    pub alphabet: Vec<String>,
    pub initial: String,
    pub update: BTreeMap<(String, String), String>,
    pub profile: BTreeMap<String, String>,
    pub profile_alphabet: BTreeSet<String>,
    pub grammar: BTreeSet<String>,
    pub terminal: BTreeMap<String, GenesisTerminal>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ProfileGrammarEncoder {
    table: BTreeMap<String, String>,
}
impl ProfileGrammarEncoder {
    pub fn new(
        profiles: &BTreeSet<String>,
        grammar: &BTreeSet<String>,
        table: BTreeMap<String, String>,
    ) -> Result<Self, OriginalObserverError> {
        if table.keys().cloned().collect::<BTreeSet<_>>() != *profiles
            || table.values().any(|g| !grammar.contains(g))
        {
            return Err(OriginalObserverError::InvalidEncoder);
        }
        Ok(Self { table })
    }
}

fn ids(labels: &[String]) -> Result<BTreeMap<String, usize>, OriginalObserverError> {
    let map: BTreeMap<_, _> = labels
        .iter()
        .enumerate()
        .map(|(i, s)| (s.clone(), i))
        .collect();
    if map.len() != labels.len() || labels.iter().any(|s| s.is_empty()) {
        return Err(OriginalObserverError::InvalidDomain);
    }
    Ok(map)
}
fn build_memory(
    data: &GenesisSixData,
) -> Result<(FiniteMoore, usize, Vec<String>), OriginalObserverError> {
    let states = ids(&data.states)?;
    ids(&data.alphabet)?;
    let initial = states
        .get(&data.initial)
        .copied()
        .ok_or(OriginalObserverError::InvalidInitialState)?;
    if data.profile.keys().cloned().collect::<BTreeSet<_>>() != states.keys().cloned().collect()
        || data
            .profile
            .values()
            .any(|s| !data.profile_alphabet.contains(s))
        || data.profile_alphabet.iter().any(|s| s.is_empty())
        || data.update.len()
            != data
                .states
                .len()
                .checked_mul(data.alphabet.len())
                .ok_or(OriginalObserverError::InvalidDomain)?
    {
        return Err(OriginalObserverError::InvalidDomain);
    }
    let labels: Vec<_> = data.profile_alphabet.iter().cloned().collect();
    let reports = ids(&labels)?;
    let mut transitions = Vec::new();
    for state in &data.states {
        let mut row = Vec::new();
        for symbol in &data.alphabet {
            let target = data
                .update
                .get(&(state.clone(), symbol.clone()))
                .ok_or(OriginalObserverError::InvalidDomain)?;
            row.push(
                *states
                    .get(target)
                    .ok_or(OriginalObserverError::InvalidDomain)?,
            );
        }
        transitions.push(row);
    }
    let memory = FiniteMoore::new(
        data.states
            .iter()
            .map(|s| reports[&data.profile[s]])
            .collect(),
        transitions,
        data.alphabet.len(),
    )
    .map_err(|_| OriginalObserverError::InvalidDomain)?;
    Ok((memory, initial, labels))
}

pub struct OriginalGenesisObserver<C: HistoryContext> {
    data: GenesisSixData,
    memory: FiniteMoore,
    initial: usize,
    profile_labels: Vec<String>,
    contexts: BTreeMap<String, C>,
}
impl<C: HistoryContext> OriginalGenesisObserver<C> {
    pub fn new(
        data: GenesisSixData,
        contexts: BTreeMap<String, C>,
    ) -> Result<Self, OriginalObserverError> {
        let (memory, initial, profile_labels) = build_memory(&data)?;
        if data.grammar.iter().any(|g| g.is_empty())
            || data.terminal.keys().cloned().collect::<BTreeSet<_>>() != data.grammar
            || contexts.keys().any(|c| c.is_empty())
        {
            return Err(OriginalObserverError::InvalidDomain);
        }
        Ok(Self {
            data,
            memory,
            initial,
            profile_labels,
            contexts,
        })
    }
    pub fn data(&self) -> &GenesisSixData {
        &self.data
    }
    pub fn memory(&self) -> &FiniteMoore {
        &self.memory
    }
    pub fn profile_alphabet(&self) -> BTreeSet<String> {
        self.profile_labels.iter().cloned().collect()
    }
    pub fn authority_effect(&self) -> AuthorityEffect {
        AuthorityEffect::None
    }
    pub fn history_state(&self, word: &[usize]) -> Result<usize, OriginalObserverError> {
        Ok(run(&self.memory, self.initial, word)?)
    }
    pub fn history_profile(&self, word: &[usize]) -> Result<&str, OriginalObserverError> {
        let x = self.history_state(word)?;
        Ok(&self.profile_labels[self.memory.reports()[x]])
    }
    pub fn contextual_profile(
        &self,
        context: &str,
        word: &[usize],
    ) -> Result<&str, OriginalObserverError> {
        self.history_state(word)?;
        let rho = self
            .contexts
            .get(context)
            .ok_or(OriginalObserverError::UnknownContext)?;
        let transformed = rho.apply(word)?;
        self.history_profile(&transformed)
    }
    pub fn terminal_for_expression(
        &self,
        expression: &str,
    ) -> Result<GenesisTerminal, OriginalObserverError> {
        self.data
            .terminal
            .get(expression)
            .copied()
            .ok_or(OriginalObserverError::UnknownGrammar)
    }
    pub fn terminal_for_history(
        &self,
        word: &[usize],
        encoder: Option<&ProfileGrammarEncoder>,
    ) -> Result<GenesisTerminal, OriginalObserverError> {
        let encoder = encoder.ok_or(OriginalObserverError::MissingEncoder)?;
        if encoder.table.keys().cloned().collect::<BTreeSet<_>>() != self.profile_alphabet()
            || encoder
                .table
                .values()
                .any(|g| !self.data.grammar.contains(g))
        {
            return Err(OriginalObserverError::InvalidEncoder);
        }
        let profile = self.history_profile(word)?;
        self.terminal_for_expression(&encoder.table[profile])
    }
}
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum GenesisClass {
    OutsideO1,
    O1Only,
    O2,
}
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct GenesisClassification {
    pub class: GenesisClass,
    pub o1_witness: Option<Vec<usize>>,
    pub o2_witness: Option<(String, Vec<usize>, Vec<usize>)>,
}

impl OriginalGenesisObserver<FiniteWordTransducer> {
    pub fn classify_original(&self) -> Result<GenesisClassification, OriginalObserverError> {
        let first_report = self.memory.reports()[self.initial];
        let mut words = BTreeMap::from([(self.initial, vec![])]);
        let mut pending = VecDeque::from([self.initial]);
        let mut o1_witness = None;
        while let Some(state) = pending.pop_front() {
            let word = words[&state].clone();
            if self.memory.reports()[state] != first_report && o1_witness.is_none() {
                o1_witness = Some(word.clone());
            }
            for d in 0..self.memory.input_count() {
                let target = self.memory.transitions()[state][d];
                if !words.contains_key(&target) {
                    let mut extended = word.clone();
                    extended.push(d);
                    words.insert(target, extended);
                    pending.push_back(target);
                }
            }
        }
        let mut o2_witness = None;
        for (name, context) in &self.contexts {
            if let Some((first, second)) =
                context.profile_noncongruence(&self.memory, self.initial)?
            {
                o2_witness = Some((name.clone(), first, second));
                break;
            }
        }
        let class = if o2_witness.is_some() {
            GenesisClass::O2
        } else if o1_witness.is_some() {
            GenesisClass::O1Only
        } else {
            GenesisClass::OutsideO1
        };
        Ok(GenesisClassification {
            class,
            o1_witness,
            o2_witness,
        })
    }
    pub fn new_checked(
        data: GenesisSixData,
        contexts: BTreeMap<String, FiniteWordTransducer>,
    ) -> Result<Self, OriginalObserverError> {
        if contexts
            .values()
            .any(|rho| rho.alphabet_size() != data.alphabet.len())
        {
            return Err(OriginalObserverError::History(
                HistoryError::InvalidAlphabet,
            ));
        }
        Self::new(data, contexts)
    }
    pub fn context_state_descent(
        &self,
        context: &str,
    ) -> Result<HistoryDescent, OriginalObserverError> {
        let rho = self
            .contexts
            .get(context)
            .ok_or(OriginalObserverError::UnknownContext)?;
        Ok(rho.descend(&self.memory, self.initial)?)
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct OriginalOperationalData {
    pub states: Vec<String>,
    pub alphabet: Vec<String>,
    pub initial: String,
    pub update: BTreeMap<(String, String), String>,
    pub transition_report: BTreeMap<(String, String), String>,
    pub report_alphabet: BTreeSet<String>,
    pub profile_alphabet: BTreeSet<String>,
    pub profile: BTreeMap<String, String>,
    pub contexts: BTreeMap<String, BTreeMap<String, String>>,
}
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct OriginalOperationalObserver {
    data: OriginalOperationalData,
    memory: FiniteMoore,
    initial: usize,
    report_rows: Vec<Vec<String>>,
}
impl OriginalOperationalObserver {
    pub fn new(data: OriginalOperationalData) -> Result<Self, OriginalObserverError> {
        let proxy = GenesisSixData {
            states: data.states.clone(),
            alphabet: data.alphabet.clone(),
            initial: data.initial.clone(),
            update: data.update.clone(),
            profile: data.profile.clone(),
            profile_alphabet: data.profile_alphabet.clone(),
            grammar: BTreeSet::new(),
            terminal: BTreeMap::new(),
        };
        let (base, initial, _) = build_memory(&proxy)?;
        if data.transition_report.len()
            != data
                .states
                .len()
                .checked_mul(data.alphabet.len())
                .ok_or(OriginalObserverError::InvalidDomain)?
            || data.report_alphabet.iter().any(|r| r.is_empty())
            || data
                .transition_report
                .values()
                .any(|r| !data.report_alphabet.contains(r))
        {
            return Err(OriginalObserverError::InvalidDomain);
        }
        let mut report_rows = Vec::new();
        for state in &data.states {
            let row = data
                .alphabet
                .iter()
                .map(|d| {
                    data.transition_report
                        .get(&(state.clone(), d.clone()))
                        .cloned()
                        .ok_or(OriginalObserverError::InvalidDomain)
                })
                .collect::<Result<Vec<_>, _>>()?;
            if row.iter().any(|r| r.is_empty()) {
                return Err(OriginalObserverError::InvalidDomain);
            }
            report_rows.push(row);
        }
        let states = ids(&data.states)?;
        for (label, context) in &data.contexts {
            if label.is_empty()
                || context.keys().cloned().collect::<BTreeSet<_>>()
                    != states.keys().cloned().collect()
                || context.values().any(|x| !states.contains_key(x))
            {
                return Err(OriginalObserverError::InvalidDomain);
            }
        }
        let mut row_ids = BTreeMap::new();
        let reports = report_rows
            .iter()
            .map(|row| {
                let fresh = row_ids.len();
                *row_ids.entry(row.clone()).or_insert(fresh)
            })
            .collect();
        let memory = FiniteMoore::new(reports, base.transitions().to_vec(), data.alphabet.len())
            .map_err(|_| OriginalObserverError::InvalidDomain)?;
        Ok(Self {
            data,
            memory,
            initial,
            report_rows,
        })
    }
    pub fn data(&self) -> &OriginalOperationalData {
        &self.data
    }
    pub fn memory(&self) -> &FiniteMoore {
        &self.memory
    }
    pub fn authority_effect(&self) -> AuthorityEffect {
        AuthorityEffect::None
    }
    pub fn report_trace(
        &self,
        word: &[usize],
    ) -> Result<(Vec<String>, usize), OriginalObserverError> {
        let mut state = self.initial;
        let mut reports = Vec::new();
        for &d in word {
            if d >= self.data.alphabet.len() {
                return Err(OriginalObserverError::History(HistoryError::InvalidWord));
            }
            reports.push(self.report_rows[state][d].clone());
            state = run(&self.memory, state, &[d])?;
        }
        Ok((reports, state))
    }
    pub fn lift_state_context(
        &self,
        context: &str,
    ) -> Result<StateContextLift, OriginalObserverError> {
        let table = self
            .data
            .contexts
            .get(context)
            .ok_or(OriginalObserverError::UnknownContext)?;
        let states = ids(&self.data.states)?;
        Ok(StateContextLift::new(
            self.memory.clone(),
            self.initial,
            self.data.states.iter().map(|s| states[&table[s]]).collect(),
        )?)
    }
}
