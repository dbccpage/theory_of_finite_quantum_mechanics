//! Partial finite dynamics and shortest distinguishing continuations.
//!
//! One fresh, observably distinct absorbing state totalizes unavailability.
//! Moore refinement therefore preserves BOTH answers and availability for every
//! finite word. The added state is internal, never a physical alternative.

use crate::finite_moore::{FiniteMoore, MooreError, MooreQuotient};
use std::collections::{BTreeMap, VecDeque};

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum ContinuationError {
    Machine(MooreError),
    OutsideCarrier,
    OutsideAlphabet,
    WorkLimit,
    CertificateMismatch,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct PartialDynamics {
    reports: Vec<usize>,
    transitions: Vec<Vec<Option<usize>>>,
    machine: FiniteMoore,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DistinguishingWord {
    pub left: usize,
    pub right: usize,
    pub word: Vec<usize>,
    pub left_answer: Option<usize>,
    pub right_answer: Option<usize>,
}

type StatePair = (usize, usize);

// Each discovered pair has exactly one earlier predecessor;the root has none.
struct PairFrontier {
    parents: BTreeMap<StatePair, Option<(StatePair, usize)>>,
    queue: VecDeque<StatePair>,
}

impl PairFrontier {
    fn new(root: StatePair) -> Self {
        Self { parents: BTreeMap::from([(root, None)]), queue: VecDeque::from([root]) }
    }

    fn discover(&mut self, parent: StatePair, next: StatePair, input: usize, maximum: usize) -> Result<(), ContinuationError> {
        if self.parents.contains_key(&next) {
            return Ok(());
        }
        if self.parents.len() >= maximum {
            return Err(ContinuationError::WorkLimit);
        }
        self.parents.insert(next, Some((parent, input)));
        self.queue.push_back(next);
        Ok(())
    }

    fn word(&self, mut pair: StatePair) -> Vec<usize> {
        let mut reversed = Vec::new();
        while let Some(Some((previous, input))) = self.parents.get(&pair) {
            reversed.push(*input);
            pair = *previous;
        }
        reversed.reverse();
        reversed
    }
}

impl PartialDynamics {
    pub fn new(
        reports: Vec<usize>,
        transitions: Vec<Vec<Option<usize>>>,
        inputs: usize,
    ) -> Result<Self, ContinuationError> {
        if reports.is_empty() {
            return Err(ContinuationError::Machine(MooreError::EmptyCarrier));
        }
        if transitions.len() != reports.len() || transitions.iter().any(|r| r.len() != inputs) {
            return Err(ContinuationError::Machine(MooreError::TransitionShape));
        }
        if transitions
            .iter()
            .flatten()
            .flatten()
            .any(|&t| t >= reports.len())
        {
            return Err(ContinuationError::Machine(
                MooreError::TransitionOutsideCarrier,
            ));
        }
        // Intern Option<label>, rather than label+1: usize::MAX is a valid label.
        let mut labels = BTreeMap::new();
        let mut outputs = Vec::new();
        for label in reports
            .iter()
            .copied()
            .map(Some)
            .chain(std::iter::once(None))
        {
            let next = labels.len();
            outputs.push(*labels.entry(label).or_insert(next));
        }
        let dead = reports.len();
        let mut total: Vec<Vec<usize>> = transitions
            .iter()
            .map(|row| row.iter().map(|t| t.unwrap_or(dead)).collect())
            .collect();
        total.push(vec![dead; inputs]);
        let machine =
            FiniteMoore::new(outputs, total, inputs).map_err(ContinuationError::Machine)?;
        Ok(Self {
            reports,
            transitions,
            machine,
        })
    }

    pub fn reports(&self) -> &[usize] {
        &self.reports
    }
    pub fn transitions(&self) -> &[Vec<Option<usize>>] {
        &self.transitions
    }
    pub fn quotient(&self) -> MooreQuotient {
        self.machine.behavioral_quotient()
    }
    pub fn verify_quotient(&self, q: &MooreQuotient) -> bool {
        self.machine.verify_quotient(q)
    }

    /// Full word validation occurs even if an earlier operation is unavailable.
    pub fn run(&self, start: usize, word: &[usize]) -> Result<Option<usize>, ContinuationError> {
        if start >= self.reports.len() {
            return Err(ContinuationError::OutsideCarrier);
        }
        if word.iter().any(|&a| a >= self.machine.input_count()) {
            return Err(ContinuationError::OutsideAlphabet);
        }
        let mut state = Some(start);
        for &a in word {
            state = state.and_then(|s| self.transitions[s][a]);
        }
        Ok(state)
    }

    /// Exactly one partial update per real quotient class. The sink's class
    /// occupies no entry; no failed operation is silently an identity.
    pub fn quotient_operations(&self) -> Vec<Vec<Option<usize>>> {
        let q = self.quotient();
        let dead = q.state_to_block[self.reports.len()];
        // First-state block numbering puts the uniquely labelled sink last.
        q.quotient.transitions()[..dead]
            .iter()
            .map(|row| {
                row.iter()
                    .map(|&t| if t == dead { None } else { Some(t) })
                    .collect()
            })
            .collect()
    }

    /// BFS on ordered state pairs. A completed empty result proves equivalence
    /// in THIS finite machine; exceeding `max_pairs` is a resource refusal.
    /// Predecessors retain first discovery;only a successful word is materialized.
    pub fn distinguish(
        &self,
        left: usize,
        right: usize,
        max_pairs: usize,
    ) -> Result<Option<DistinguishingWord>, ContinuationError> {
        if left >= self.reports.len() || right >= self.reports.len() {
            return Err(ContinuationError::OutsideCarrier);
        }
        if max_pairs == 0 {
            return Err(ContinuationError::WorkLimit);
        }
        let mut frontier = PairFrontier::new((left, right));
        while let Some(pair) = frontier.queue.pop_front() {
            if let Some(witness) = self.distinction_at(left, right, pair, &frontier) {
                return Ok(Some(witness));
            }
            self.enqueue_successors(pair, max_pairs, &mut frontier)?;
        }
        Ok(None)
    }

    fn distinction_at(&self, left: usize, right: usize, (l, r): StatePair, frontier: &PairFrontier) -> Option<DistinguishingWord> {
        if self.machine.reports()[l] == self.machine.reports()[r] {
            return None;
        }
        Some(DistinguishingWord {
            left, right, word: frontier.word((l, r)),
            left_answer: self.reports.get(l).copied(),
            right_answer: self.reports.get(r).copied(),
        })
    }

    fn enqueue_successors(&self, parent: StatePair, maximum: usize, frontier: &mut PairFrontier) -> Result<(), ContinuationError> {
        for input in 0..self.machine.input_count() {
            let next = (self.machine.transitions()[parent.0][input], self.machine.transitions()[parent.1][input]);
            frontier.discover(parent, next, input, maximum)?;
        }
        Ok(())
    }

    /// Replay the claimed distinction without trusting its saved answers.
    /// Validates self-described endpoints/answers,not shortestness or an external query.
    pub fn verify_distinction(&self, c: &DistinguishingWord) -> Result<(), ContinuationError> {
        let l = self.run(c.left, &c.word)?.map(|s| self.reports[s]);
        let r = self.run(c.right, &c.word)?.map(|s| self.reports[s]);
        if l == r || l != c.left_answer || r != c.right_answer {
            return Err(ContinuationError::CertificateMismatch);
        }
        Ok(())
    }
}
