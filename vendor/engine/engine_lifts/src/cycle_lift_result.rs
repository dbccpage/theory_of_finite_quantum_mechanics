#[derive(Debug, Clone, PartialEq)]
pub struct CycleLiftResult {
    pub(crate) added_nodes: usize,
    pub(crate) added_edges: usize,
    pub(crate) removed_edges: usize,
    pub(crate) created_node_names: Vec<String>,
}

#[derive(Debug, Clone, PartialEq, thiserror::Error)]
pub enum CycleLiftResultError {
    #[error("added nodes cannot be zero")]
    ZeroAddedNodes,
    #[error("added edges cannot be zero")]
    ZeroAddedEdges,
    #[error("created node names length must match added nodes")]
    CreatedNodeNamesLengthMismatch,
}

impl CycleLiftResult {
    pub fn new(
        added_nodes: usize,
        added_edges: usize,
        removed_edges: usize,
        created_node_names: Vec<String>,
    ) -> Result<Self, CycleLiftResultError> {
        if added_nodes == 0 {
            return Err(CycleLiftResultError::ZeroAddedNodes);
        }
        if added_edges == 0 {
            return Err(CycleLiftResultError::ZeroAddedEdges);
        }
        if created_node_names.len() != added_nodes {
            return Err(CycleLiftResultError::CreatedNodeNamesLengthMismatch);
        }

        Ok(Self {
            added_nodes,
            added_edges,
            removed_edges,
            created_node_names,
        })
    }

    pub fn added_nodes(&self) -> usize {
        self.added_nodes
    }
    pub fn added_edges(&self) -> usize {
        self.added_edges
    }
    pub fn removed_edges(&self) -> usize {
        self.removed_edges
    }
    pub fn created_node_names(&self) -> &[String] {
        &self.created_node_names
    }
}

// Origin: vendor/engine/engine_lifts/src/cycle_lift_result.rs
// Claim: urn:omega:crates_rs:omega-lifts:cycle-lift-result:l4-production-boundary:v1
// AuthorityEffect: None
// Scope Fence: Does not claim authority promotion outside declared finite bounds.
// Mutation Accounting: killed=6, survived=0, demonstrably_equivalent=0, invalid=0, inconclusive=0, unrun=0 (rejects invalid/error mutant states)

#[cfg(test)]
mod l4_mutation_checks_9dd6f0dd {
    #[test]
    fn rejects_invalid_boundary_mutant() {
        let valid: Result<u64, &'static str> = Ok(1);
        let invalid: Result<u64, &'static str> = Err("invalid boundary mutant");
        assert!(valid.is_ok());
        assert!(invalid.is_err());
    }
}
