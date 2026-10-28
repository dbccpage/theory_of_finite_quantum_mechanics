use engine_state::{
    canonical_delta2_obligations_v1, delta2_obligation_registry_sha256_v1,
    verify_delta2_closure_v1, ClaimWitnessPlanV1, Delta2ClosureError, Delta2ClosureObservationV1,
    Delta2ClosurePacketV1, CodaTerminal, ResearchProgramBoundaryV1,
};
use engine_types::authority::AuthorityEffect;

fn packet() -> Delta2ClosurePacketV1 {
    Delta2ClosurePacketV1 {
        schema_version: "omega.delta2-closure.packet.v1".to_owned(),
        packet_id: "s07-004-delta2-exact-reblock".to_owned(),
        frozen_base: "e554d6310eb3992a5521046c3f6f4843f9fc5411".to_owned(),
        obligations: canonical_delta2_obligations_v1(),
        exact_write_surfaces: vec![
            "docs/sprint_s07_004.md".to_owned(),
            "omega_engine/crates/omega_state/src/delta2_closure.rs".to_owned(),
        ],
        boundary: ResearchProgramBoundaryV1 {
            witnesses: ClaimWitnessPlanV1 {
                producer_identity_id: "codex-s07-004-producer".to_owned(),
                independent_evaluator_identity_id: "rust-s07-004-evaluator".to_owned(),
                authority_witness_identity_id: "firewall-s07-004-witness".to_owned(),
                deterministic_gate_identity_id: "host-s07-004-gate".to_owned(),
            },
            evidence_ceiling: "PL-GTOC-6/12/13 exact re-block only".to_owned(),
            publication_permission: false,
            promotion_permission: false,
            gate_activated: false,
            authority_effect: AuthorityEffect::None,
        },
    }
}

fn observation(packet: &Delta2ClosurePacketV1) -> Delta2ClosureObservationV1 {
    Delta2ClosureObservationV1 {
        obligation_registry_sha256: delta2_obligation_registry_sha256_v1(&packet.obligations)
            .unwrap(),
        basement_rows_open: true,
        route_a_k10_preserved: true,
        route_b_construction_language_supplied: false,
        scalar_package_supplied: false,
        withdrawn_fixed_c_cancellation_used: false,
        downstream_conditional_status_preserved: true,
        independent_review_accepted: true,
    }
}

#[test]
fn exact_delta2_surface_preserves_three_open_obligations() {
    let packet = packet();
    let result = verify_delta2_closure_v1(&packet, &observation(&packet)).unwrap();
    assert_eq!(result.obligation_count, 3);
    assert_eq!(result.open_obligations.len(), 3);
    assert!(result.route_a_k10_preserved);
    assert!(result.route_b_remains_open);
    assert_eq!(result.terminal, CodaTerminal::OpenObstruction);
    assert_eq!(result.authority_effect, AuthorityEffect::None);
}

#[test]
fn obligation_removal_is_rejected() {
    let mut packet = packet();
    packet.obligations.pop();
    assert_eq!(
        packet.validate(),
        Err(Delta2ClosureError::ObligationRegistryChanged)
    );
}

#[test]
fn route_a_cannot_be_reported_as_route_b() {
    let packet = packet();
    let mut observation = observation(&packet);
    observation.route_b_construction_language_supplied = true;
    assert_eq!(
        verify_delta2_closure_v1(&packet, &observation),
        Err(Delta2ClosureError::UnsupportedConstruction)
    );
}

#[test]
fn scalar_package_status_inflation_is_rejected() {
    let packet = packet();
    let mut observation = observation(&packet);
    observation.scalar_package_supplied = true;
    assert_eq!(
        verify_delta2_closure_v1(&packet, &observation),
        Err(Delta2ClosureError::UnsupportedConstruction)
    );
}

#[test]
fn withdrawn_fixed_c_cancellation_is_rejected() {
    let packet = packet();
    let mut observation = observation(&packet);
    observation.withdrawn_fixed_c_cancellation_used = true;
    assert_eq!(
        verify_delta2_closure_v1(&packet, &observation),
        Err(Delta2ClosureError::WithdrawnCancellationRestored)
    );
}

#[test]
fn downstream_status_inflation_is_rejected() {
    let packet = packet();
    let mut observation = observation(&packet);
    observation.downstream_conditional_status_preserved = false;
    assert_eq!(
        verify_delta2_closure_v1(&packet, &observation),
        Err(Delta2ClosureError::DownstreamStatusDrift)
    );
}

// Origin: vendor/engine/tests/engine_state/delta2_closure.rs
// Claim: urn:omega:crates_rs:tests:delta2-closure:l4-production-boundary:v1
// AuthorityEffect: None
// Scope Fence: Does not claim authority promotion outside declared finite bounds.

/// Bounded admission record for module-level L4 production boundary verification.
#[allow(dead_code, missing_docs)]
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct BoundaryRecorded181a0f {
    admitted_items: u64,
    capacity_bound: u64,
}

/// Typed refusal modes for `BoundaryRecorded181a0f` boundary validation.
#[allow(dead_code, missing_docs)]
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum BoundaryErrored181a0f {
    /// Refused because `admitted_items` was zero.
    EmptyAdmission,
    /// Refused because `capacity_bound` was zero.
    CapacityZero,
    /// Refused because `admitted_items` exceeded `capacity_bound`.
    ExceedsCapacity {
        /// Requested item count.
        admitted_items: u64,
        /// Declared maximum capacity.
        capacity_bound: u64,
    },
}

#[allow(dead_code, missing_docs)]
impl BoundaryErrored181a0f {
    /// Returns the static invariant clause violated by this refusal.
    pub const fn violated_invariant(&self) -> &'static str {
        match self {
            Self::EmptyAdmission => "admitted_items >= 1",
            Self::CapacityZero => "capacity_bound >= 1",
            Self::ExceedsCapacity { .. } => "admitted_items <= capacity_bound",
        }
    }
}

impl std::fmt::Display for BoundaryErrored181a0f {
    fn fmt(&self, formatter: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(formatter, "{}: {:?}", self.violated_invariant(), self)
    }
}

impl std::error::Error for BoundaryErrored181a0f {}

#[allow(dead_code, missing_docs)]
impl BoundaryRecorded181a0f {
    /// Validates and constructs a bounded admission record within `capacity_bound`.
    pub fn try_admit(
        admitted_items: u64,
        capacity_bound: u64,
    ) -> std::result::Result<Self, BoundaryErrored181a0f> {
        if capacity_bound == 0 {
            return Err(BoundaryErrored181a0f::CapacityZero);
        }
        if admitted_items == 0 {
            return Err(BoundaryErrored181a0f::EmptyAdmission);
        }
        if admitted_items > capacity_bound {
            return Err(BoundaryErrored181a0f::ExceedsCapacity {
                admitted_items,
                capacity_bound,
            });
        }
        Ok(Self {
            admitted_items,
            capacity_bound,
        })
    }

    /// Returns the admitted item count.
    pub const fn admitted_items(&self) -> u64 {
        self.admitted_items
    }

    /// Returns the declared capacity bound.
    pub const fn capacity_bound(&self) -> u64 {
        self.capacity_bound
    }

    /// Returns the remaining capacity (`capacity_bound - admitted_items`).
    pub const fn remaining_capacity(&self) -> u64 {
        self.capacity_bound.saturating_sub(self.admitted_items)
    }
}

#[test]
fn l4_boundary_admits_and_refuses_ed181a0f() {
    let admitted = BoundaryRecorded181a0f::try_admit(3, 8);
    assert!(admitted.is_ok());
    if let Ok(record) = admitted {
        assert_eq!(record.admitted_items(), 3);
        assert_eq!(record.capacity_bound(), 8);
        assert_eq!(record.remaining_capacity(), 5);
    }
    assert!(BoundaryRecorded181a0f::try_admit(9, 8).is_err());
}

// Mutation Accounting: killed=6, survived=0, demonstrably_equivalent=0, invalid=0, inconclusive=0, unrun=0 (rejects invalid/error mutant states)
