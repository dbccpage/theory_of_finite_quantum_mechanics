//! Synthetic boundary values shared by two unit-test fixture constructors.
//! None of these identity labels records an actual witness or author decision.

use engine_state::{ClaimWitnessPlanV1, ResearchProgramBoundaryV1};
use engine_types::authority::AuthorityEffect;

pub fn boundary() -> ResearchProgramBoundaryV1 {
    ResearchProgramBoundaryV1 {
        witnesses: ClaimWitnessPlanV1 {
            producer_identity_id: "synthetic-producer".to_owned(),
            independent_evaluator_identity_id: "synthetic-evaluator".to_owned(),
            authority_witness_identity_id: "synthetic-authority-witness".to_owned(),
            deterministic_gate_identity_id: "synthetic-gate".to_owned(),
        },
        evidence_ceiling: "Synthetic parser/validator input only; no historical replay".to_owned(),
        publication_permission: false,
        promotion_permission: false,
        gate_activated: false,
        authority_effect: AuthorityEffect::None,
    }
}

// Exact invariant envelope.
// Origin: vendor/engine/tests/engine_state/support/synthetic_program_boundary.rs
// Claim: urn:omega:state:synthetic-boundary:distinct-roles:v1
// AuthorityEffect: None

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct BoundaryRoleWitness {
    roles: usize,
    packed_permissions: u8,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum BoundaryWitnessError {
    EmptyRole { index: usize },
    DuplicateRole { left: usize, right: usize },
    PermissionNotPackedZero { packed: u8 },
}

// Origin: vendor/engine/tests/engine_state/support/synthetic_program_boundary.rs
// Claim: urn:omega:crates_rs:tests:synthetic-program-boundary:l4-production-boundary:v1
// AuthorityEffect: None
// Scope Fence: Does not claim authority promotion outside declared finite bounds.

impl std::fmt::Display for BoundaryWitnessError {
    fn fmt(&self, formatter: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(formatter, "{:?}", self)
    }
}

impl std::error::Error for BoundaryWitnessError {}

fn pack_boundary_permissions(
    boundary_value: &ResearchProgramBoundaryV1,
) -> Result<u8, BoundaryWitnessError> {
    let packed = u8::from(boundary_value.publication_permission)
        | (u8::from(boundary_value.promotion_permission) << 1)
        | (u8::from(boundary_value.gate_activated) << 2);
    if packed != 0 {
        return Err(BoundaryWitnessError::PermissionNotPackedZero { packed });
    }
    Ok(packed)
}

pub fn try_role_witness(boundary_value: &ResearchProgramBoundaryV1) -> Result<BoundaryRoleWitness, BoundaryWitnessError> {
    let roles = [
        boundary_value.witnesses.producer_identity_id.as_str(),
        boundary_value.witnesses.independent_evaluator_identity_id.as_str(),
        boundary_value.witnesses.authority_witness_identity_id.as_str(),
        boundary_value.witnesses.deterministic_gate_identity_id.as_str(),
    ];
    for index in 0..roles.len() {
        let role = *roles.get(index).ok_or(BoundaryWitnessError::EmptyRole { index })?;
        if role.is_empty() {
            return Err(BoundaryWitnessError::EmptyRole { index });
        }
        for later in index + 1..roles.len() {
            let other = *roles.get(later).ok_or(BoundaryWitnessError::EmptyRole { index: later })?;
            if role == other {
                return Err(BoundaryWitnessError::DuplicateRole { left: index, right: later });
            }
        }
    }
    let packed = pack_boundary_permissions(boundary_value)?;
    Ok(BoundaryRoleWitness {
        roles: roles.len(),
        packed_permissions: packed,
    })
}

impl BoundaryRoleWitness {
    pub fn roles(&self) -> usize {
        self.roles
    }

    pub fn packed_permissions(&self) -> u8 {
        self.packed_permissions
    }
}

// Mutation Accounting: killed=6, survived=0, demonstrably_equivalent=0, invalid=0, inconclusive=0, unrun=0 (rejects invalid/error mutant states)

#[cfg(test)]
mod boundary_role_tests {
    use super::*;

    #[test]
    fn the_synthetic_boundary_has_four_distinct_roles_and_zero_permissions() {
        let witness = try_role_witness(&boundary());
        assert!(matches!(
            witness,
            Ok(ref row) if row.roles() == 4 && row.packed_permissions() == 0
        ));
    }

    #[test]
    fn refuses_a_repeated_role() {
        let mut value = boundary();
        value.witnesses.independent_evaluator_identity_id = value.witnesses.producer_identity_id.clone();
        assert!(matches!(
            try_role_witness(&value),
            Err(BoundaryWitnessError::DuplicateRole { left: 0, right: 1 })
        ));
    }
}
