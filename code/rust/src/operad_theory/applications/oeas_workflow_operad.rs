//! Applications: OEAS Applied Workflow Operad.
//!
//! AuthorityEffect: None.

use std::collections::HashSet;
use serde::{Deserialize, Serialize};
use crate::foundation::{OperadColour, Operation, OperationId, OperadSignature, PlanarColoredOperad, PlanarTree};
use crate::realization::OperadAlgebra;

pub const OEAS_ADMITTED_PORT_COLOURS: &[&str] = &[
    "State",
    "Code",
    "AuditCandidate",
    "AuditFinding",
    "ProofCandidate",
    "AdmittedProof",
    "Post",
    "LedgerProposal",
    "LedgerSnapshot",
    "ReceiptPayload",
    "EvaluationReceipt",
];

/// Agent capability slice restricting an interpreter to permitted skill generators.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct AgentCapabilitySlice {
    pub agent_id: String,
    pub licensed_skills: HashSet<String>,
    pub allowed_input_ports: HashSet<OperadColour>,
    pub allowed_output_ports: HashSet<OperadColour>,
}

impl AgentCapabilitySlice {
    pub fn new(
        agent_id: impl Into<String>,
        licensed_skills: HashSet<String>,
        allowed_input_ports: HashSet<OperadColour>,
        allowed_output_ports: HashSet<OperadColour>,
    ) -> Self {
        Self {
            agent_id: agent_id.into(),
            licensed_skills,
            allowed_input_ports,
            allowed_output_ports,
        }
    }

    pub fn permits_skill(&self, skill_id: &str) -> bool {
        self.licensed_skills.contains(skill_id)
    }
}

/// Applied workflow operad typing all skill generators and planar workflow trees.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct OEASWorkflowOperad {
    pub operad: PlanarColoredOperad,
}

impl OEASWorkflowOperad {
    pub fn new() -> Result<Self, String> {
        let mut operad = PlanarColoredOperad::new("OEAS_WorkflowOperad", true);
        for &c_name in OEAS_ADMITTED_PORT_COLOURS {
            let c = OperadColour::new(c_name)?;
            operad.add_colour(c);
        }
        operad.ensure_identities();
        Ok(Self { operad })
    }

    pub fn register_skill(
        &mut self,
        skill_id: impl Into<String>,
        input_ports: &[&str],
        output_port: &str,
        description: impl Into<String>,
    ) -> Result<Operation, String> {
        let s_id = skill_id.into();
        for &inp in input_ports {
            if !OEAS_ADMITTED_PORT_COLOURS.contains(&inp) {
                return Err(format!("Cannot register skill '{}': unadmitted input port colour '{}'", s_id, inp));
            }
        }
        if !OEAS_ADMITTED_PORT_COLOURS.contains(&output_port) {
            return Err(format!("Cannot register skill '{}': unadmitted output port colour '{}'", s_id, output_port));
        }

        let in_cols: Result<Vec<OperadColour>, String> = input_ports.iter().map(|&s| OperadColour::new(s)).collect();
        let out_col = OperadColour::new(output_port)?;
        let sig = OperadSignature::new(in_cols?, out_col);

        let op = Operation::new_generator(OperationId::new(&s_id)?, sig, description);
        self.operad.add_operation(op.clone())?;
        Ok(op)
    }

    pub fn create_corolla(&self, skill_id: &str) -> Result<PlanarTree, String> {
        if let Some(op) = self.operad.operations().get(skill_id) {
            Ok(PlanarTree::corolla(op.clone()))
        } else {
            Err(format!("Skill '{}' is not registered in workflow operad", skill_id))
        }
    }

    pub fn compose_workflow_tree(
        &self,
        root_tree: &PlanarTree,
        slot_index: usize,
        child_tree: PlanarTree,
    ) -> Result<PlanarTree, String> {
        root_tree.graft(slot_index, child_tree)
    }

    pub fn compose_workflow(
        &self,
        root_skill_id: &str,
        slot_index: usize,
        child_skill_id: &str,
    ) -> Result<Operation, String> {
        let root_op = self
            .operad
            .operations()
            .get(root_skill_id)
            .ok_or_else(|| format!("Root skill '{}' not found in operad", root_skill_id))?;
        let child_op = self
            .operad
            .operations()
            .get(child_skill_id)
            .ok_or_else(|| format!("Child skill '{}' not found in operad", child_skill_id))?;

        self.operad.partial_compose(root_op, child_op, slot_index)
    }

    pub fn create_agent_interpreter(
        &self,
        agent_id: impl Into<String>,
        _capability_slice: Option<AgentCapabilitySlice>,
    ) -> OperadAlgebra {
        let a_id = agent_id.into();
        OperadAlgebra::new(self.operad.clone(), format!("AgentInterpreter_{}", a_id), a_id)
    }
}
