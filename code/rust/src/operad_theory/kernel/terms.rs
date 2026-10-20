
use serde_json::{json, Value};
use std::collections::BTreeMap;

use super::canonical::{canonical_id, CanonicalError};
use super::model::{BoundarySignature, OperationSpec, OperationSpecInput, PortSpec};
use super::result::Refusal;

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum OperationTerm {
    Identity(PortSpec),
    Primitive(OperationSpec),
    Substitute {
        outer: Box<OperationTerm>,
        slot: usize,
        inner: Box<OperationTerm>,
    },
    Admitted(NormalizedTerm),
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum ChildNode {
    Input(PortSpec),
    Operation {
        operation: OperationSpec,
        children: Vec<ChildNode>,
    },
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum TreeNode {
    Identity(PortSpec),
    Operation {
        operation: OperationSpec,
        children: Vec<ChildNode>,
    },
}

impl ChildNode {
    fn inputs(&self) -> Vec<PortSpec> {
        match self {
            ChildNode::Input(port) => vec![port.clone()],
            ChildNode::Operation { children, .. } => {
                children.iter().flat_map(|c| c.inputs()).collect()
            }
        }
    }

    #[allow(dead_code)]
    pub fn output(&self) -> PortSpec {
        match self {
            ChildNode::Input(port) => port.clone(),
            ChildNode::Operation { operation, .. } => operation.output_port.clone(),
        }
    }

    fn to_data(&self) -> Value {
        match self {
            ChildNode::Input(port) => json!({ "input": port.to_canonical() }),
            ChildNode::Operation {
                operation,
                children,
            } => json!({
                "operation": operation.to_canonical(),
                "children": children.iter().map(|c| c.to_data()).collect::<Vec<_>>(),
            }),
        }
    }

    fn collect_operations(&self, map: &mut BTreeMap<String, OperationSpec>) {
        if let ChildNode::Operation {
            operation,
            children,
        } = self
        {
            if let Ok(id) = operation.canonical_id() {
                map.insert(id, operation.clone());
            }
            for child in children {
                child.collect_operations(map);
            }
        }
    }
}

impl TreeNode {
    pub fn inputs(&self) -> Vec<PortSpec> {
        match self {
            TreeNode::Identity(port) => vec![port.clone()],
            TreeNode::Operation { children, .. } => {
                children.iter().flat_map(|c| c.inputs()).collect()
            }
        }
    }

    pub fn output(&self) -> PortSpec {
        match self {
            TreeNode::Identity(port) => port.clone(),
            TreeNode::Operation { operation, .. } => operation.output_port.clone(),
        }
    }

    pub fn to_data(&self) -> Value {
        match self {
            TreeNode::Identity(port) => json!({ "identity": port.to_canonical() }),
            TreeNode::Operation {
                operation,
                children,
            } => json!({
                "operation": operation.to_canonical(),
                "children": children.iter().map(|c| c.to_data()).collect::<Vec<_>>(),
            }),
        }
    }

    pub fn operations(&self) -> Vec<OperationSpec> {
        let mut map = BTreeMap::new();
        if let TreeNode::Operation {
            operation,
            children,
        } = self
        {
            if let Ok(id) = operation.canonical_id() {
                map.insert(id, operation.clone());
            }
            for child in children {
                child.collect_operations(&mut map);
            }
        }
        map.into_values().collect()
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct NormalizedTerm {
    pub tree: TreeNode,
}

impl NormalizedTerm {
    pub fn new(tree: TreeNode) -> Self {
        Self { tree }
    }

    pub fn boundary(&self) -> BoundarySignature {
        BoundarySignature::new(self.tree.inputs(), self.tree.output())
    }

    pub fn operations(&self) -> Vec<OperationSpec> {
        self.tree.operations()
    }

    pub fn to_canonical(&self) -> Value {
        json!({
            "tree": self.tree.to_data(),
            "boundary": self.boundary().to_canonical(),
        })
    }

    pub fn canonical_id(&self) -> Result<String, CanonicalError> {
        canonical_id("omega.oewas.operation-term.normal.v1", &self.to_canonical())
    }
}

fn replace_leaf_in_children(
    children: Vec<ChildNode>,
    slot: usize,
    replacement: &(OperationSpec, Vec<ChildNode>),
) -> (Vec<ChildNode>, isize) {
    let mut remaining = slot as isize;
    let mut new_children = Vec::with_capacity(children.len());
    let mut replaced = false;
    for child in children {
        if replaced {
            new_children.push(child);
            continue;
        }
        let (new_child, rem_after) = replace_leaf(
            child,
            remaining as usize,
            (replacement.0.clone(), replacement.1.clone()),
        );
        if rem_after == -1 {
            replaced = true;
        } else {
            remaining = rem_after;
        }
        new_children.push(new_child);
    }
    (new_children, if replaced { -1 } else { remaining })
}

fn replace_leaf(
    node: ChildNode,
    slot: usize,
    replacement: (OperationSpec, Vec<ChildNode>),
) -> (ChildNode, isize) {
    match node {
        ChildNode::Input(port) => {
            if slot == 0 {
                (
                    ChildNode::Operation {
                        operation: replacement.0,
                        children: replacement.1,
                    },
                    -1,
                )
            } else {
                (ChildNode::Input(port), (slot as isize) - 1)
            }
        }
        ChildNode::Operation {
            operation,
            children,
        } => {
            let (new_children, rem) = replace_leaf_in_children(children, slot, &replacement);
            (
                ChildNode::Operation {
                    operation,
                    children: new_children,
                },
                rem,
            )
        }
    }
}

fn invalid_spec(message: String) -> Refusal {
    Refusal {
        code: "INVALID_OPERATION_SPEC".into(),
        message,
        locus: String::new(),
        details: Vec::new(),
    }
}

fn validate_port(port: &PortSpec) -> Result<(), Refusal> {
    let checked = PortSpec::new(&port.port_id, &port.colour_id, &port.schema_ref)
        .map_err(|error| invalid_spec(error.to_string()))?;
    if checked != *port {
        return Err(invalid_spec(
            "port differs from its canonical constructor value".into(),
        ));
    }
    Ok(())
}

fn validate_operation(operation: &OperationSpec) -> Result<(), Refusal> {
    for port in operation
        .input_ports
        .iter()
        .chain(std::iter::once(&operation.output_port))
    {
        validate_port(port)?;
    }
    let checked = OperationSpec::new(OperationSpecInput {
        operation_id: &operation.operation_id,
        version: &operation.version,
        input_ports: operation.input_ports.clone(),
        output_port: operation.output_port.clone(),
        executor_ref: &operation.executor_ref,
        executor_digest: &operation.executor_digest,
        tool_refs: operation.tool_refs.clone(),
        effects: operation.effects.clone(),
        invocation_grade: operation.invocation_grade,
        authority_effect: operation.authority_effect,
        authority_ceiling: operation.authority_ceiling,
    })
    .map_err(|error| invalid_spec(error.to_string()))?;
    if checked != *operation {
        return Err(invalid_spec(
            "operation differs from its canonical constructor value".into(),
        ));
    }
    Ok(())
}

fn validate_children(operation: &OperationSpec, children: &[ChildNode]) -> Result<(), Refusal> {
    validate_operation(operation)?;
    if operation.input_ports.len() != children.len() {
        return Err(Refusal {
            code: "ARITY_MISMATCH".into(),
            message: "admitted operation children differ from its declared arity".into(),
            locus: operation.key(),
            details: vec![
                ("expected".into(), operation.input_ports.len().to_string()),
                ("actual".into(), children.len().to_string()),
            ],
        });
    }
    for (slot, (expected, child)) in operation.input_ports.iter().zip(children).enumerate() {
        match child {
            ChildNode::Input(port) => validate_port(port)?,
            ChildNode::Operation {
                operation,
                children,
            } => validate_children(operation, children)?,
        }
        let actual = child.output();
        if !expected.same_type(&actual) {
            return Err(Refusal {
                code: "BOUNDARY_MISMATCH".into(),
                message: "admitted child output does not match its declared input".into(),
                locus: operation.key(),
                details: vec![
                    ("slot".into(), slot.to_string()),
                    ("expected_colour".into(), expected.colour_id.clone()),
                    ("expected_schema".into(), expected.schema_ref.clone()),
                    ("actual_colour".into(), actual.colour_id),
                    ("actual_schema".into(), actual.schema_ref),
                ],
            });
        }
    }
    Ok(())
}

fn validate_substitution_slot(
    outer_inputs: &[PortSpec],
    slot: usize,
    inner_out: &PortSpec,
) -> Result<(), Refusal> {
    if slot >= outer_inputs.len() {
        return Err(Refusal {
            code: "SLOT_OUT_OF_RANGE".into(),
            message: format!("slot {} is outside outer arity {}", slot, outer_inputs.len()),
            locus: String::new(),
            details: vec![
                ("slot".into(), slot.to_string()),
                ("arity".into(), outer_inputs.len().to_string()),
            ],
        });
    }
    if !outer_inputs[slot].same_type(inner_out) {
        return Err(Refusal {
            code: "BOUNDARY_MISMATCH".into(),
            message: "inner output does not match the selected outer input".into(),
            locus: String::new(),
            details: vec![
                ("expected_colour".into(), outer_inputs[slot].colour_id.clone()),
                ("expected_schema".into(), outer_inputs[slot].schema_ref.clone()),
                ("actual_colour".into(), inner_out.colour_id.clone()),
                ("actual_schema".into(), inner_out.schema_ref.clone()),
            ],
        });
    }
    Ok(())
}

fn normalize_substitution(
    outer: &OperationTerm,
    slot: usize,
    inner: &OperationTerm,
) -> Result<TreeNode, Refusal> {
    let outer_tree = normalize_tree(outer)?;
    let inner_tree = normalize_tree(inner)?;
    let outer_inputs = outer_tree.inputs();
    let inner_out = inner_tree.output();
    validate_substitution_slot(&outer_inputs, slot, &inner_out)?;

    match (&outer_tree, &inner_tree) {
        (TreeNode::Identity(_), _) => Ok(inner_tree),
        (_, TreeNode::Identity(_)) => Ok(outer_tree),
        (
            TreeNode::Operation {
                operation,
                children,
            },
            TreeNode::Operation {
                operation: in_op,
                children: in_children,
            },
        ) => {
            let (new_children, rem) = replace_leaf_in_children(
                children.clone(),
                slot,
                &(in_op.clone(), in_children.clone()),
            );
            if rem != -1 {
                return Err(Refusal {
                    code: "NORMALIZATION_FAILED".into(),
                    message: "selected input leaf was not replaced".into(),
                    locus: String::new(),
                    details: Vec::new(),
                });
            }
            Ok(TreeNode::Operation {
                operation: operation.clone(),
                children: new_children,
            })
        }
    }
}

fn validate_admitted_tree(tree: &TreeNode) -> Result<TreeNode, Refusal> {
    match tree {
        TreeNode::Identity(port) => validate_port(port)?,
        TreeNode::Operation {
            operation,
            children,
        } => validate_children(operation, children)?,
    }
    Ok(tree.clone())
}

fn normalize_tree(term: &OperationTerm) -> Result<TreeNode, Refusal> {
    match term {
        OperationTerm::Admitted(norm) => validate_admitted_tree(&norm.tree),
        OperationTerm::Identity(port) => {
            validate_port(port)?;
            Ok(TreeNode::Identity(port.clone()))
        }
        OperationTerm::Primitive(op) => {
            validate_operation(op)?;
            let children = op
                .input_ports
                .iter()
                .cloned()
                .map(ChildNode::Input)
                .collect();
            Ok(TreeNode::Operation {
                operation: op.clone(),
                children,
            })
        }
        OperationTerm::Substitute { outer, slot, inner } => {
            normalize_substitution(outer, *slot, inner)
        }
    }
}

pub fn normalize_term(term: &OperationTerm) -> Result<NormalizedTerm, Refusal> {
    let tree = normalize_tree(term)?;
    Ok(NormalizedTerm::new(tree))
}

pub fn identity(port: PortSpec) -> OperationTerm {
    OperationTerm::Identity(port)
}

pub fn normalize(term: &OperationTerm) -> Result<NormalizedTerm, Refusal> {
    normalize_term(term)
}

pub fn substitute(
    outer: &OperationTerm,
    slot: usize,
    inner: &OperationTerm,
) -> Result<NormalizedTerm, Refusal> {
    normalize_term(&OperationTerm::Substitute {
        outer: Box::new(outer.clone()),
        slot,
        inner: Box::new(inner.clone()),
    })
}

pub fn term_from_normalized(term: &NormalizedTerm) -> OperationTerm {
    OperationTerm::Admitted(term.clone())
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::kernel::model::{AuthorityEffect, InvocationGrade};

    const DIGEST: &str =
        "sha256:0000000000000000000000000000000000000000000000000000000000000000";

    fn port(id: &str, colour: &str) -> PortSpec {
        PortSpec::new(id, colour, "any").unwrap()
    }

    fn op(in_colour: &str, out_colour: &str) -> OperationSpec {
        OperationSpec::new(OperationSpecInput {
            operation_id: "step",
            version: "v1",
            input_ports: vec![port("in_0", in_colour)],
            output_port: port("out", out_colour),
            executor_ref: "skill.step",
            executor_digest: DIGEST,
            tool_refs: vec![],
            effects: vec![],
            invocation_grade: InvocationGrade::Discipline,
            authority_effect: AuthorityEffect::None,
            authority_ceiling: AuthorityEffect::None,
        })
        .unwrap()
    }

    #[test]
    fn normalize_and_substitute_preserve_boundaries_and_refuse_invalid_slots_or_types() {
        let p_state = port("x", "State");
        let id_term = identity(p_state.clone());
        let step_op = op("State", "State");
        let prim = OperationTerm::Primitive(step_op);
        let left_unit = substitute(&id_term, 0, &prim).unwrap();
        let right_unit = substitute(&prim, 0, &id_term).unwrap();
        assert_eq!(left_unit, right_unit);
        assert!(left_unit.canonical_id().unwrap().starts_with("sha256:"));

        let slot_err = substitute(&prim, 1, &id_term).unwrap_err();
        assert_eq!(slot_err.code, "SLOT_OUT_OF_RANGE");

        let bad_id = identity(port("y", "Code"));
        let type_err = substitute(&prim, 0, &bad_id).unwrap_err();
        assert_eq!(type_err.code, "BOUNDARY_MISMATCH");
    }
}
