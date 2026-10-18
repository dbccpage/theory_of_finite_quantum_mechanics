
use std::collections::BTreeSet;
use serde_json::{json, Value};

use super::canonical::{
    canonical_id, require_digest, require_identifier, CanonicalError,
};
use super::model::{AuthorityEffect, OperandRef};
use super::result::KernelError;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct BudgetTransition {
    pub before: usize,
    pub after: usize,
}

impl BudgetTransition {
    pub fn new(before: usize, after: usize) -> Result<Self, KernelError> {
        if after > before {
            return Err(KernelError::Message(
                "an execution event cannot increase its budget".into(),
            ));
        }
        Ok(Self { before, after })
    }

    pub fn to_canonical(&self) -> Value {
        json!({
            "before": self.before,
            "after": self.after,
        })
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ExecutionEvent {
    pub run_id: String,
    pub sequence: usize,
    pub plan_digest: String,
    pub operation_spec_digest: String,
    pub executor_digest: String,
    pub policy_digest: String,
    pub environment_digest: String,
    pub validator_ref: String,
    pub validator_digest: String,
    pub verifier_ref: String,
    pub verifier_digest: String,
    pub admission_receipt_refs: Vec<String>,
    pub inputs: Vec<OperandRef>,
    pub outputs: Vec<OperandRef>,
    pub parent_event_refs: Vec<String>,
    pub budget: BudgetTransition,
    pub outcome_code: String,
    pub outcome_digest: String,
    pub authority_effect: AuthorityEffect,
}

#[derive(Debug, Clone)]
pub struct ExecutionEventInput {
    pub run_id: String,
    pub sequence: usize,
    pub plan_digest: String,
    pub operation_spec_digest: String,
    pub executor_digest: String,
    pub policy_digest: String,
    pub environment_digest: String,
    pub validator_ref: String,
    pub validator_digest: String,
    pub verifier_ref: String,
    pub verifier_digest: String,
    pub admission_receipt_refs: Vec<String>,
    pub inputs: Vec<OperandRef>,
    pub outputs: Vec<OperandRef>,
    pub parent_event_refs: Vec<String>,
    pub budget: BudgetTransition,
    pub outcome_code: String,
    pub outcome_digest: String,
    pub authority_effect: AuthorityEffect,
}

impl ExecutionEvent {
    pub fn new(input: ExecutionEventInput) -> Result<Self, KernelError> {
        let run_id = require_identifier(&input.run_id, "run_id")?;
        let plan_digest = require_digest(&input.plan_digest, "plan_digest")?;
        let operation_spec_digest = require_digest(&input.operation_spec_digest, "operation_spec_digest")?;
        let executor_digest = require_digest(&input.executor_digest, "executor_digest")?;
        let policy_digest = require_digest(&input.policy_digest, "policy_digest")?;
        let environment_digest = require_digest(&input.environment_digest, "environment_digest")?;
        let validator_ref = require_identifier(&input.validator_ref, "validator_ref")?;
        let validator_digest = require_digest(&input.validator_digest, "validator_digest")?;
        let verifier_ref = require_identifier(&input.verifier_ref, "verifier_ref")?;
        let verifier_digest = require_digest(&input.verifier_digest, "verifier_digest")?;
        let outcome_code = require_identifier(&input.outcome_code, "outcome_code")?;
        let outcome_digest = require_digest(&input.outcome_digest, "outcome_digest")?;

        if input.authority_effect != AuthorityEffect::None {
            return Err(KernelError::Message(
                "execution events are evidence records with AuthorityEffect None".into(),
            ));
        }

        let mut receipts = Vec::new();
        let mut seen_receipts = BTreeSet::new();
        for r in input.admission_receipt_refs {
            let digest = require_digest(&r, "admission_receipt_ref")?;
            if !seen_receipts.insert(digest.clone()) {
                return Err(KernelError::Message(
                    "admission receipt references must be unique".into(),
                ));
            }
            receipts.push(digest);
        }

        for operand in input.inputs.iter().chain(input.outputs.iter()) {
            if !seen_receipts.contains(&operand.admission_receipt_ref) {
                return Err(KernelError::Message(
                    "event admission receipts do not cover every input/output operand".into(),
                ));
            }
        }

        let mut parents = Vec::new();
        let mut seen_parents = BTreeSet::new();
        for p in input.parent_event_refs {
            let digest = require_digest(&p, "parent_event_ref")?;
            if !seen_parents.insert(digest.clone()) {
                return Err(KernelError::Message(
                    "parent event references must be unique".into(),
                ));
            }
            parents.push(digest);
        }

        Ok(Self {
            run_id,
            sequence: input.sequence,
            plan_digest,
            operation_spec_digest,
            executor_digest,
            policy_digest,
            environment_digest,
            validator_ref,
            validator_digest,
            verifier_ref,
            verifier_digest,
            admission_receipt_refs: receipts,
            inputs: input.inputs,
            outputs: input.outputs,
            parent_event_refs: parents,
            budget: input.budget,
            outcome_code,
            outcome_digest,
            authority_effect: input.authority_effect,
        })
    }

    pub fn to_canonical(&self) -> Value {
        json!({
            "run_id": self.run_id,
            "sequence": self.sequence,
            "plan_digest": self.plan_digest,
            "operation_spec_digest": self.operation_spec_digest,
            "executor_digest": self.executor_digest,
            "policy_digest": self.policy_digest,
            "environment_digest": self.environment_digest,
            "validator_ref": self.validator_ref,
            "validator_digest": self.validator_digest,
            "verifier_ref": self.verifier_ref,
            "verifier_digest": self.verifier_digest,
            "admission_receipt_refs": self.admission_receipt_refs,
            "inputs": self.inputs.iter().map(OperandRef::to_canonical).collect::<Vec<_>>(),
            "outputs": self.outputs.iter().map(OperandRef::to_canonical).collect::<Vec<_>>(),
            "parent_event_refs": self.parent_event_refs,
            "budget": self.budget.to_canonical(),
            "outcome_code": self.outcome_code,
            "outcome_digest": self.outcome_digest,
            "authority_effect": self.authority_effect.as_str(),
        })
    }

    pub fn canonical_id(&self) -> Result<String, CanonicalError> {
        canonical_id("omega.oewas.execution-event.v1", &self.to_canonical())
    }
}
