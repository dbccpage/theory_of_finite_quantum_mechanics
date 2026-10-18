//! Frozen agent licenses and mechanical capability-closure checks.
//!
//! Rust face of `omega_engine/kernel/higher_operad/capability.py`.

use std::collections::BTreeSet;
use serde_json::{json, Value};

use super::canonical::{
    canonical_id, require_digest, require_identifier, sorted_unique, CanonicalError,
};
use super::model::{AuthorityEffect, InvocationGrade};
use super::result::Refusal;
use super::terms::{normalize_term, term_from_normalized, ChildNode, NormalizedTerm, OperationTerm, TreeNode};

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct AgentLicense {
    pub agent_id: String,
    pub allowed_operation_keys: Vec<String>,
    pub allowed_colour_ids: Vec<String>,
    pub allowed_executor_refs: Vec<String>,
    pub allowed_tool_refs: Vec<String>,
    pub allowed_effects: Vec<String>,
    pub authority_ceiling: AuthorityEffect,
    pub lifecycle: String,
    pub policy_digest: String,
}

impl AgentLicense {
    #[allow(clippy::too_many_arguments)]
    pub fn new(
        agent_id: &str,
        allowed_operation_keys: Vec<String>,
        allowed_colour_ids: Vec<String>,
        allowed_executor_refs: Vec<String>,
        allowed_tool_refs: Vec<String>,
        allowed_effects: Vec<String>,
        authority_ceiling: AuthorityEffect,
        lifecycle: &str,
        policy_digest: &str,
    ) -> Result<Self, CanonicalError> {
        Ok(Self {
            agent_id: require_identifier(agent_id, "agent_id")?,
            allowed_operation_keys: sorted_unique(&allowed_operation_keys, "allowed_operation_keys")?,
            allowed_colour_ids: sorted_unique(&allowed_colour_ids, "allowed_colour_ids")?,
            allowed_executor_refs: sorted_unique(&allowed_executor_refs, "allowed_executor_refs")?,
            allowed_tool_refs: sorted_unique(&allowed_tool_refs, "allowed_tool_refs")?,
            allowed_effects: sorted_unique(&allowed_effects, "allowed_effects")?,
            authority_ceiling,
            lifecycle: require_identifier(lifecycle, "lifecycle")?,
            policy_digest: require_digest(policy_digest, "policy_digest")?,
        })
    }

    pub fn to_canonical(&self) -> Value {
        json!({
            "agent_id": self.agent_id,
            "allowed_operation_keys": self.allowed_operation_keys,
            "allowed_colour_ids": self.allowed_colour_ids,
            "allowed_executor_refs": self.allowed_executor_refs,
            "allowed_tool_refs": self.allowed_tool_refs,
            "allowed_effects": self.allowed_effects,
            "authority_ceiling": self.authority_ceiling.as_str(),
            "lifecycle": self.lifecycle,
            "policy_digest": self.policy_digest,
        })
    }

    pub fn canonical_id(&self) -> Result<String, CanonicalError> {
        canonical_id("omega.oewas.agent-license.v1", &self.to_canonical())
    }
}

/// One-shot execution license evidence.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ActionLicense {
    pub license_id: String,
    pub candidate_digest: String,
    pub evidence_sha256: String,
    pub authority_effect: String,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct LicensedTerm {
    pub license_id: String,
    pub term: NormalizedTerm,
}

impl LicensedTerm {
    pub fn new(license_id: &str, term: NormalizedTerm) -> Result<Self, CanonicalError> {
        Ok(Self {
            license_id: require_digest(license_id, "license_id")?,
            term,
        })
    }

    pub fn canonical_id(&self) -> Result<String, CanonicalError> {
        let term_id = self.term.canonical_id()?;
        canonical_id(
            "omega.oewas.licensed-term.v1",
            &json!({
                "license_id": self.license_id,
                "term_id": term_id,
            }),
        )
    }
}

fn check_entry_over_entry(tree: &TreeNode) -> bool {
    fn walk_child(child: &ChildNode, parent_is_entry: bool) -> bool {
        match child {
            ChildNode::Input(_) => false,
            ChildNode::Operation { operation, children } => {
                let current_is_entry = operation.invocation_grade == InvocationGrade::Entry;
                if parent_is_entry && current_is_entry {
                    return true;
                }
                children.iter().any(|c| walk_child(c, current_is_entry))
            }
        }
    }

    match tree {
        TreeNode::Identity(_) => false,
        TreeNode::Operation { operation, children } => {
            let current_is_entry = operation.invocation_grade == InvocationGrade::Entry;
            children.iter().any(|c| walk_child(c, current_is_entry))
        }
    }
}

pub fn authorize_term(
    license: &AgentLicense,
    term: &OperationTerm,
) -> Result<LicensedTerm, Refusal> {
    let normalized = normalize_term(term)?;
    let operations = normalized.operations();

    let term_op_keys: BTreeSet<String> = operations.iter().map(|op| op.key()).collect();
    let term_executors: BTreeSet<String> = operations.iter().map(|op| op.executor_ref.clone()).collect();
    let term_tools: BTreeSet<String> = operations.iter().flat_map(|op| op.tool_refs.clone()).collect();
    let term_effects: BTreeSet<String> = operations.iter().flat_map(|op| op.effects.clone()).collect();

    let mut colours: BTreeSet<String> = BTreeSet::new();
    let boundary = normalized.boundary();
    for p in &boundary.inputs {
        colours.insert(p.colour_id.clone());
    }
    colours.insert(boundary.output.colour_id.clone());
    for op in &operations {
        for p in &op.input_ports {
            colours.insert(p.colour_id.clone());
        }
        colours.insert(op.output_port.colour_id.clone());
    }

    let allowed_ops: BTreeSet<String> = license.allowed_operation_keys.iter().cloned().collect();
    let missing_ops: Vec<String> = term_op_keys.difference(&allowed_ops).cloned().collect();
    if !missing_ops.is_empty() {
        return Err(Refusal {
            code: "OPERATION_CAPABILITY_ESCAPE".into(),
            message: "term contains operations outside the frozen license".into(),
            locus: String::new(),
            details: vec![("operations".into(), missing_ops.join(","))],
        });
    }

    let allowed_colours: BTreeSet<String> = license.allowed_colour_ids.iter().cloned().collect();
    let missing_colours: Vec<String> = colours.difference(&allowed_colours).cloned().collect();
    if !missing_colours.is_empty() {
        return Err(Refusal {
            code: "COLOUR_CAPABILITY_ESCAPE".into(),
            message: "term contains colours outside the frozen license".into(),
            locus: String::new(),
            details: vec![("colours".into(), missing_colours.join(","))],
        });
    }

    let allowed_executors: BTreeSet<String> = license.allowed_executor_refs.iter().cloned().collect();
    let missing_executors: Vec<String> = term_executors.difference(&allowed_executors).cloned().collect();
    if !missing_executors.is_empty() {
        return Err(Refusal {
            code: "EXECUTOR_CAPABILITY_ESCAPE".into(),
            message: "term contains executors outside the frozen license".into(),
            locus: String::new(),
            details: vec![("executors".into(), missing_executors.join(","))],
        });
    }

    let allowed_tools: BTreeSet<String> = license.allowed_tool_refs.iter().cloned().collect();
    let missing_tools: Vec<String> = term_tools.difference(&allowed_tools).cloned().collect();
    if !missing_tools.is_empty() {
        return Err(Refusal {
            code: "TOOL_CAPABILITY_ESCAPE".into(),
            message: "term contains tools outside the frozen license".into(),
            locus: String::new(),
            details: vec![("tools".into(), missing_tools.join(","))],
        });
    }

    let allowed_effects: BTreeSet<String> = license.allowed_effects.iter().cloned().collect();
    let missing_effects: Vec<String> = term_effects.difference(&allowed_effects).cloned().collect();
    if !missing_effects.is_empty() {
        return Err(Refusal {
            code: "EFFECT_CAPABILITY_ESCAPE".into(),
            message: "term contains effects outside the frozen license".into(),
            locus: String::new(),
            details: vec![("effects".into(), missing_effects.join(","))],
        });
    }

    let mut excessive = Vec::new();
    for op in &operations {
        if op.authority_ceiling.rank() > license.authority_ceiling.rank() {
            excessive.push(op.key());
        }
    }
    if !excessive.is_empty() {
        excessive.sort();
        return Err(Refusal {
            code: "AUTHORITY_CAPABILITY_ESCAPE".into(),
            message: "term authority ceiling exceeds the frozen license ceiling".into(),
            locus: String::new(),
            details: vec![("operations".into(), excessive.join(","))],
        });
    }

    if check_entry_over_entry(&normalized.tree) {
        return Err(Refusal {
            code: "ENTRY_OVER_ENTRY".into(),
            message: "an entry operation may not contain another entry operation".into(),
            locus: String::new(),
            details: Vec::new(),
        });
    }

    let license_id = license.canonical_id().map_err(|e| Refusal {
        code: "CANONICAL_ERROR".into(),
        message: e.to_string(),
        locus: String::new(),
        details: Vec::new(),
    })?;

    Ok(LicensedTerm {
        license_id,
        term: normalized,
    })
}

pub fn authorize_normalized_term(
    license: &AgentLicense,
    term: &NormalizedTerm,
) -> Result<LicensedTerm, Refusal> {
    authorize_term(license, &term_from_normalized(term))
}
