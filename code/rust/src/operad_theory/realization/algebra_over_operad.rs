
use std::collections::HashMap;
use std::sync::Arc;
use serde::{Deserialize, Serialize};
use crate::foundation::{OperadColour, PlanarColoredOperad, PlanarTree, TreeChild};

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct PolicyDecisionRef {
    pub decision_id: String,
    pub is_admissible: bool,
    pub policy_name: String,
    pub notes: String,
}

impl PolicyDecisionRef {
    pub fn new(decision_id: impl Into<String>, is_admissible: bool) -> Self {
        Self {
            decision_id: decision_id.into(),
            is_admissible,
            policy_name: "StandardAdmissibilityPolicy".to_string(),
            notes: String::new(),
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct EvaluationReceipt {
    pub receipt_id: String,
    pub term_hash: String,
    pub agent_id: String,
    pub policy_decision_ref: Option<PolicyDecisionRef>,
    pub status: String,
    pub output_colour: String,
    pub output_value: serde_json::Value,
    pub emitted_at: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct EvaluationOutcome {
    pub is_completed: bool,
    pub value: Option<serde_json::Value>,
    pub receipt: Option<EvaluationReceipt>,
    pub error_message: Option<String>,
}

type ActionFn = Arc<dyn Fn(&[serde_json::Value]) -> Result<serde_json::Value, String> + Send + Sync>;

#[derive(Clone)]
pub struct OperadAlgebra {
    pub operad: PlanarColoredOperad,
    pub name: String,
    pub agent_id: String,
    carriers: HashMap<String, String>,
    actions: HashMap<String, ActionFn>,
}

impl OperadAlgebra {
    pub fn new(operad: PlanarColoredOperad, name: impl Into<String>, agent_id: impl Into<String>) -> Self {
        Self {
            operad,
            name: name.into(),
            agent_id: agent_id.into(),
            carriers: HashMap::new(),
            actions: HashMap::new(),
        }
    }

    pub fn set_carrier(&mut self, colour: &OperadColour, carrier_space: impl Into<String>) -> Result<(), String> {
        if self.operad.is_closed_universe && !self.operad.colours().contains(colour) {
            return Err(format!("Cannot set carrier for unadmitted colour '{}'", colour.as_str()));
        }
        self.carriers.insert(colour.as_str().to_string(), carrier_space.into());
        Ok(())
    }

    pub fn get_carrier(&self, colour: &OperadColour) -> Option<&str> {
        self.carriers.get(colour.as_str()).map(|s| s.as_str())
    }

    pub fn register_action(
        &mut self,
        op_id: &str,
        action: impl Fn(&[serde_json::Value]) -> Result<serde_json::Value, String> + Send + Sync + 'static,
    ) -> Result<(), String> {
        if !self.operad.operations().contains_key(op_id) {
            return Err(format!("Operation '{}' not in operad '{}'", op_id, self.operad.name));
        }
        self.actions.insert(op_id.to_string(), Arc::new(action));
        Ok(())
    }

    pub fn evaluate_tree(
        &self,
        tree: &PlanarTree,
        leaf_inputs: &[serde_json::Value],
        policy_ref: Option<PolicyDecisionRef>,
    ) -> EvaluationOutcome {
        if leaf_inputs.len() != tree.arity() {
            return EvaluationOutcome {
                is_completed: false,
                value: None,
                receipt: None,
                error_message: Some(format!(
                    "Leaf input count {} != tree arity {}",
                    leaf_inputs.len(),
                    tree.arity()
                )),
            };
        }

        let mut offset = 0;
        match self.evaluate_tree_recursive(tree, leaf_inputs, &mut offset) {
            Ok(val) => {
                let receipt = EvaluationReceipt {
                    receipt_id: format!("rec_{}", tree.term_hash()),
                    term_hash: tree.term_hash(),
                    agent_id: self.agent_id.clone(),
                    policy_decision_ref: policy_ref,
                    status: "Completed".to_string(),
                    output_colour: tree.output_colour().as_str().to_string(),
                    output_value: val.clone(),
                    emitted_at: "2026-08-20T00:00:00Z".to_string(),
                };
                EvaluationOutcome {
                    is_completed: true,
                    value: Some(val),
                    receipt: Some(receipt),
                    error_message: None,
                }
            }
            Err(e) => EvaluationOutcome {
                is_completed: false,
                value: None,
                receipt: None,
                error_message: Some(e),
            },
        }
    }

    fn evaluate_tree_recursive(
        &self,
        tree: &PlanarTree,
        leaf_inputs: &[serde_json::Value],
        offset: &mut usize,
    ) -> Result<serde_json::Value, String> {
        let mut child_results = Vec::new();
        for ch in &tree.children {
            match ch {
                TreeChild::Leaf(_) => {
                    if *offset >= leaf_inputs.len() {
                        return Err("Leaf inputs exhausted".to_string());
                    }
                    child_results.push(leaf_inputs[*offset].clone());
                    *offset += 1;
                }
                TreeChild::Subtree(sub) => {
                    let sub_val = self.evaluate_tree_recursive(sub, leaf_inputs, offset)?;
                    child_results.push(sub_val);
                }
            }
        }

        if tree.root.is_identity() && child_results.len() == 1 {
            return Ok(child_results.remove(0));
        }

        if let Some(action) = self.actions.get(tree.root.op_id.as_str()) {
            action(&child_results)
        } else {
            Ok(serde_json::json!({
                "operation": tree.root.op_id.as_str(),
                "inputs": child_results,
            }))
        }
    }
}
