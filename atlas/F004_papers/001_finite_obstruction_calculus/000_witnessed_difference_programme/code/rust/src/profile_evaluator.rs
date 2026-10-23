// Executable finite evidence; AuthorityEffect: None.
use serde::{Deserialize, Serialize};
use std::collections::{BTreeMap, BTreeSet};
use crate::error::WdpError;

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct FiniteProfile {
    pub table: BTreeMap<String, bool>,
    pub admitted: BTreeSet<String>,
    pub refused: BTreeSet<String>,
    pub budget: usize,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct Evidence {
    pub query: String,
    pub value: bool,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum EvaluationStatus {
    Admitted(bool),
    Refused,
    OutsideDomain,
    BudgetExhausted,
}

impl FiniteProfile {
    pub fn new(
        table: BTreeMap<String, bool>,
        admitted: BTreeSet<String>,
        refused: BTreeSet<String>,
        budget: usize,
    ) -> Result<Self, WdpError> {
        for q in &admitted {
            if !table.contains_key(q) {
                return Err(WdpError::InvalidInput { detail: format!("admitted query {} not in table", q) });
            }
        }
        for q in &refused {
            if !admitted.contains(q) {
                return Err(WdpError::InvalidInput { detail: format!("refused query {} not admitted", q) });
            }
        }
        Ok(Self { table, admitted, refused, budget })
    }

    pub fn evaluate(&self, query: &str, candidates: &[Evidence]) -> EvaluationStatus {
        if !self.table.contains_key(query) {
            return EvaluationStatus::OutsideDomain;
        }
        if self.refused.contains(query) {
            return EvaluationStatus::Refused;
        }
        if !self.admitted.contains(query) {
            return EvaluationStatus::OutsideDomain;
        }
        let matching = candidates.iter().take(self.budget).find(|e| e.query == query);
        match matching {
            Some(ev) => {
                let declared_val = self.table[query];
                EvaluationStatus::Admitted(ev.value == declared_val)
            }
            None => EvaluationStatus::BudgetExhausted,
        }
    }
}
