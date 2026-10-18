use omega_category_theory::finite_history_context::run;
use omega_category_theory::finite_moore::FiniteMoore;
use omega_category_theory::finite_partial_structure::{
    descend, verify, DescentError, FinitePartialStructure, PartialOperation, SortQuotient,
};
use std::collections::BTreeMap;

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
pub enum EvaluationOutcome {
    Passed,
    Failed,
    Unknown,
}
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
pub enum AdmissionDecision {
    Admit,
    Reject,
}
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Proposal {
    pub proposed_state: usize,
}
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DeclaredRow {
    pub proposal: Proposal,
    pub evaluation: EvaluationOutcome,
    pub decision: AdmissionDecision,
}
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum BridgeError {
    EmptyDomain,
    InvalidState,
    InvalidRow,
    InvalidHistory,
    FiberCollision {
        left: usize,
        right: usize,
        left_value: usize,
        right_value: usize,
    },
    InvalidRecordMap,
    FalseReplay,
    InvalidDecoder,
}
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Decoder {
    values: Vec<usize>,
}
impl Decoder {
    pub fn values(&self) -> &[usize] {
        &self.values
    }
    pub fn decode(&self, record: usize) -> Result<usize, BridgeError> {
        self.values
            .get(record)
            .copied()
            .ok_or(BridgeError::InvalidRecordMap)
    }
}
fn source(values: &[usize], value_count: usize) -> FinitePartialStructure {
    FinitePartialStructure {
        sizes: vec![values.len(), value_count],
        operations: vec![PartialOperation {
            inputs: vec![0],
            output: 1,
            values: values.iter().copied().map(Some).collect(),
        }],
        predicates: vec![],
    }
}
fn quotient(record_map: &[usize], record_count: usize, value_count: usize) -> SortQuotient {
    SortQuotient {
        target_sizes: vec![record_count, value_count],
        maps: vec![record_map.to_vec(), (0..value_count).collect()],
    }
}
fn factor(
    values: &[usize],
    value_count: usize,
    record_map: &[usize],
    record_count: usize,
) -> Result<Decoder, BridgeError> {
    if values.is_empty() {
        return Err(BridgeError::EmptyDomain);
    }
    let target = descend(
        &source(values, value_count),
        &quotient(record_map, record_count, value_count),
    )
    .map_err(|e| match e {
        DescentError::OperationConflict {
            left,
            right,
            left_image: Some(a),
            right_image: Some(b),
            ..
        } => BridgeError::FiberCollision {
            left,
            right,
            left_value: a,
            right_value: b,
        },
        _ => BridgeError::InvalidRecordMap,
    })?;
    Ok(Decoder {
        values: target.operations[0]
            .values
            .iter()
            .map(|v| v.expect("total source descends to total target"))
            .collect(),
    })
}
fn normalize<T: Ord>(values: impl IntoIterator<Item = T>) -> Vec<usize> {
    let mut ids = BTreeMap::new();
    values
        .into_iter()
        .map(|v| {
            let next = ids.len();
            *ids.entry(v).or_insert(next)
        })
        .collect()
}
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ProposalAdmissionModel {
    state_count: usize,
    rows: Vec<DeclaredRow>,
}
impl ProposalAdmissionModel {
    pub fn new(state_count: usize, rows: Vec<DeclaredRow>) -> Result<Self, BridgeError> {
        if state_count == 0 || rows.is_empty() {
            return Err(BridgeError::EmptyDomain);
        }
        if rows
            .iter()
            .any(|r| r.proposal.proposed_state >= state_count)
        {
            return Err(BridgeError::InvalidState);
        }
        Ok(Self { state_count, rows })
    }
    pub fn rows(&self) -> &[DeclaredRow] {
        &self.rows
    }
    pub fn evaluation_records(&self) -> Vec<usize> {
        normalize(self.rows.iter().map(|r| r.evaluation))
    }
    pub fn joint_records(&self) -> Vec<usize> {
        normalize(self.rows.iter().map(|r| (r.evaluation, r.decision)))
    }
    pub fn decision_from_records(
        &self,
        records: &[usize],
        record_count: usize,
    ) -> Result<Decoder, BridgeError> {
        factor(
            &self
                .rows
                .iter()
                .map(|r| r.decision as usize)
                .collect::<Vec<_>>(),
            2,
            records,
            record_count,
        )
    }
    pub fn evaluation_only_decision(&self) -> Result<Decoder, BridgeError> {
        let records = self.evaluation_records();
        let count = records.iter().max().map_or(0, |v| v + 1);
        self.decision_from_records(&records, count)
    }
    pub fn inspect_roles(
        &self,
        row: usize,
    ) -> Result<(EvaluationOutcome, AdmissionDecision), BridgeError> {
        self.rows
            .get(row)
            .map(|r| (r.evaluation, r.decision))
            .ok_or(BridgeError::InvalidRow)
    }
    pub fn apply_declared_admission(
        &self,
        row: usize,
        current: usize,
    ) -> Result<usize, BridgeError> {
        if current >= self.state_count {
            return Err(BridgeError::InvalidState);
        }
        let r = self.rows.get(row).ok_or(BridgeError::InvalidRow)?;
        Ok(match (r.evaluation, r.decision) {
            (EvaluationOutcome::Passed, AdmissionDecision::Admit) => r.proposal.proposed_state,
            _ => current,
        })
    }
}
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct HistoryModel {
    machine: FiniteMoore,
    start: usize,
    histories: Vec<Vec<usize>>,
    final_states: Vec<usize>,
}
impl HistoryModel {
    pub fn new(
        machine: FiniteMoore,
        start: usize,
        histories: Vec<Vec<usize>>,
    ) -> Result<Self, BridgeError> {
        if histories.is_empty() {
            return Err(BridgeError::EmptyDomain);
        }
        if start >= machine.state_count() {
            return Err(BridgeError::InvalidState);
        }
        let final_states = histories
            .iter()
            .map(|h| run(&machine, start, h).map_err(|_| BridgeError::InvalidHistory))
            .collect::<Result<_, _>>()?;
        Ok(Self {
            machine,
            start,
            histories,
            final_states,
        })
    }
    pub fn histories(&self) -> &[Vec<usize>] {
        &self.histories
    }
    pub fn final_states(&self) -> &[usize] {
        &self.final_states
    }
    pub fn replay_decoder(
        &self,
        records: &[usize],
        record_count: usize,
    ) -> Result<Decoder, BridgeError> {
        factor(
            &self.final_states,
            self.machine.state_count(),
            records,
            record_count,
        )
    }
    pub fn verify_claimed_states(&self, claimed: &[usize]) -> Result<(), BridgeError> {
        if claimed != self.final_states {
            return Err(BridgeError::FalseReplay);
        }
        Ok(())
    }
    pub fn verify_decoder(&self, records: &[usize], claimed: &[usize]) -> Result<(), BridgeError> {
        let q = quotient(records, claimed.len(), self.machine.state_count());
        let proposed = FinitePartialStructure {
            sizes: q.target_sizes.clone(),
            operations: vec![PartialOperation {
                inputs: vec![0],
                output: 1,
                values: claimed.iter().copied().map(Some).collect(),
            }],
            predicates: vec![],
        };
        verify(
            &source(&self.final_states, self.machine.state_count()),
            &q,
            &proposed,
        )
        .map_err(|_| BridgeError::InvalidDecoder)
    }
}
