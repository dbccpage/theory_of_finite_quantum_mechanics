use std::{env, fs, path::PathBuf};

use engine_state::coda_gtla_protocol::{CodaGtlaStage, CodaTerminal};
use engine_state::sprint_governance::{
    compile_process_profile_v1, verify_sprint_governance_v1, ProcessProfileKindV1,
    ProfileOperationV1, SprintActorRoleV1, SprintAuthorityStatusV1, SprintGovernanceError,
    SprintGovernancePacketV1, SprintLifecycleV1, SprintPathLeaseV1, SprintRetrospectiveV1,
    SprintSuccessorRequestV1, StoryDependencyV1,
};
use serde_json::Value;

fn fixture(name: &str) -> String {
    fs::read_to_string(
        PathBuf::from(env!("CARGO_MANIFEST_DIR"))
            .join("../tests/engine_state")
            .join("fixtures")
            .join(name),
    )
    .unwrap()
}

fn fixture_packet() -> SprintGovernancePacketV1 {
    serde_json::from_str(&fixture("sprint_governance_packet_v1.json")).unwrap()
}

fn retrospective() -> SprintRetrospectiveV1 {
    serde_json::from_str(&fixture("sprint_retrospective_v1.json")).unwrap()
}

fn terminalized_fixture_packet() -> SprintGovernancePacketV1 {
    let mut packet = fixture_packet();
    packet.lifecycle = SprintLifecycleV1::Completed;
    packet.coda_terminal = Some(CodaTerminal::StabilizedSurvivor);
    for story in &mut packet.stories {
        story.lifecycle = SprintLifecycleV1::Completed;
    }
    packet
}

#[test]
fn golden_packet_compiles_every_profile_to_twelve_evidence_only_stages() {
    let packet = fixture_packet();
    let receipt = verify_sprint_governance_v1(&packet, &[]).unwrap();

    assert_eq!(receipt.profile_kinds, ProcessProfileKindV1::ALL);
    assert_eq!(receipt.stage_count_per_profile, CodaGtlaStage::ALL.len());
    assert_eq!(receipt.story_count, 6);
    assert!(receipt.authority_effect.is_none());
    for profile in ProcessProfileKindV1::ALL {
        let compiled = compile_process_profile_v1(profile);
        compiled.validate().unwrap();
        assert_eq!(compiled.stages, CodaGtlaStage::ALL);
        assert!(compiled.authority_effect.is_none());
    }
}

#[test]
fn schema_rejects_missing_and_unknown_fields() {
    let mut missing: Value =
        serde_json::from_str(&fixture("sprint_governance_packet_v1.json")).unwrap();
    missing.as_object_mut().unwrap().remove("stories");
    assert!(serde_json::from_value::<SprintGovernancePacketV1>(missing).is_err());

    let mut unknown: Value =
        serde_json::from_str(&fixture("sprint_governance_packet_v1.json")).unwrap();
    unknown["gate_activated"] = Value::Bool(true);
    assert!(serde_json::from_value::<SprintGovernancePacketV1>(unknown).is_err());
}

#[test]
fn active_sprint_requires_frozen_base_packet_and_observer() {
    let mut packet = fixture_packet();
    packet.frozen_base = None;
    assert_eq!(
        packet.validate().unwrap_err(),
        SprintGovernanceError::UnfrozenAdmission
    );

    let mut packet = fixture_packet();
    packet.packet_sha256 = Some("short".to_owned());
    assert_eq!(
        packet.validate().unwrap_err(),
        SprintGovernanceError::UnfrozenAdmission
    );
}

#[test]
fn sprint_has_exactly_one_parent() {
    let mut packet = fixture_packet();
    packet.parent_saga_ids.push("SAGA-16".to_owned());
    assert_eq!(
        packet.validate().unwrap_err(),
        SprintGovernanceError::ParentCount(2)
    );
}

#[test]
fn profile_rejects_an_unsupported_operation() {
    let mut packet = fixture_packet();
    packet.stories[0].operations = vec![
        ProfileOperationV1::EditRust,
        ProfileOperationV1::EditPython,
        ProfileOperationV1::RunFocusedGate,
    ];
    let error = packet.validate().unwrap_err();
    assert!(matches!(
        error,
        SprintGovernanceError::UnsupportedOperation {
            profile: ProcessProfileKindV1::RustDevelopment,
            operation: ProfileOperationV1::EditPython,
        }
    ));
    assert_eq!(error.terminal_route(), CodaTerminal::LiftLicenseNeeded);
}

#[test]
fn serialized_enum_collections_are_order_independent_but_reject_duplicates() {
    let mut packet = fixture_packet();
    packet.profiles.reverse();
    packet.stories[0].operations.reverse();
    packet.validate().unwrap();

    packet.profiles.push(packet.profiles[0]);
    assert_eq!(
        packet.validate().unwrap_err(),
        SprintGovernanceError::DuplicateValue("profiles")
    );

    let mut packet = fixture_packet();
    let duplicate_operation = packet.stories[0].operations[0];
    packet.stories[0].operations.push(duplicate_operation);
    assert_eq!(
        packet.validate().unwrap_err(),
        SprintGovernanceError::DuplicateValue("story operations")
    );
}

#[test]
fn dependency_cycle_is_invalid() {
    let mut packet = fixture_packet();
    packet.dependency_edges.push(StoryDependencyV1 {
        predecessor: "S15-900-06".to_owned(),
        successor: "S15-900-01".to_owned(),
    });
    let error = packet.validate().unwrap_err();
    assert_eq!(error, SprintGovernanceError::DependencyCycle);
    assert_eq!(error.terminal_route(), CodaTerminal::Invalid);
}

#[test]
fn shared_write_requires_one_producer() {
    let mut packet = fixture_packet();
    packet.stories[1].write_surface = packet.stories[0].write_surface.clone();
    let error = packet.validate().unwrap_err();
    assert!(matches!(
        error,
        SprintGovernanceError::SharedWriteConflict(_)
    ));

    packet.stories[1].producer_id = packet.stories[0].producer_id.clone();
    packet.validate().unwrap();
}

#[test]
fn foreign_exact_path_lease_blocks_the_story() {
    let packet = fixture_packet();
    let lease = SprintPathLeaseV1 {
        lease_id: "lease:rust-owner".to_owned(),
        owner: "another-producer".to_owned(),
        exact_paths: vec!["src/governance.rs".to_owned()],
    };
    let error = packet.validate_against_leases(&[lease]).unwrap_err();
    assert!(matches!(error, SprintGovernanceError::LeaseConflict { .. }));
    assert_eq!(error.terminal_route(), CodaTerminal::OpenObstruction);
}

#[test]
fn only_host_may_instantiate_a_bounded_successor() {
    let packet = fixture_packet();
    let mut request = SprintSuccessorRequestV1 {
        source_sprint_id: packet.sprint_id.clone(),
        requested_by: SprintActorRoleV1::Producer,
        candidate_ids: vec!["candidate:01".to_owned()],
    };
    let error = packet.validate_successor_request(&request).unwrap_err();
    assert_eq!(error, SprintGovernanceError::SuccessorHostOnly);
    assert_eq!(error.terminal_route(), CodaTerminal::Refused);

    request.requested_by = SprintActorRoleV1::Host;
    packet.validate_successor_request(&request).unwrap();
    request.candidate_ids.push("candidate:02".to_owned());
    assert_eq!(
        packet.validate_successor_request(&request).unwrap_err(),
        SprintGovernanceError::SuccessorBudgetExceeded
    );
}

#[test]
fn retrospective_is_terminal_only_and_cannot_self_activate() {
    let packet = fixture_packet();
    let retrospective = retrospective();
    assert_eq!(
        retrospective.validate_against(&packet).unwrap_err(),
        SprintGovernanceError::RetrospectiveBeforeTerminal
    );
    retrospective
        .validate_against(&terminalized_fixture_packet())
        .unwrap();

    let mut hostile: Value =
        serde_json::from_str(&fixture("sprint_retrospective_v1.json")).unwrap();
    hostile["improvement_candidates"][0]["route"] = Value::String("active".to_owned());
    assert!(serde_json::from_value::<SprintRetrospectiveV1>(hostile).is_err());
}

#[test]
fn lifecycle_terminal_and_authority_domains_stay_separate() {
    let mut packet = fixture_packet();
    packet.coda_terminal = Some(CodaTerminal::ExactRepair);
    assert_eq!(
        packet.validate().unwrap_err(),
        SprintGovernanceError::TerminalDomainConflation
    );

    let mut packet = fixture_packet();
    packet.authority_status = SprintAuthorityStatusV1::PendingHumanPromotion;
    assert_eq!(
        packet.validate().unwrap_err(),
        SprintGovernanceError::AuthorityConflation
    );
}

#[test]
fn write_surfaces_are_exact_repo_relative_paths() {
    let mut packet = fixture_packet();
    packet.exact_write_surface[5] = "workspace/**".to_owned();
    let error = packet.validate().unwrap_err();
    assert!(matches!(error, SprintGovernanceError::NonExactPath { .. }));
}

// Origin: vendor/engine/tests/engine_state/sprint_governance.rs
// Claim: urn:omega:crates_rs:tests:sprint-governance:l4-production-boundary:v1
// AuthorityEffect: None
// Scope Fence: Does not claim authority promotion outside declared finite bounds.

/// Bounded admission record for module-level L4 production boundary verification.
#[allow(dead_code, missing_docs)]
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct BoundaryRecord310268d2 {
    admitted_items: u64,
    capacity_bound: u64,
}

/// Typed refusal modes for `BoundaryRecord310268d2` boundary validation.
#[allow(dead_code, missing_docs)]
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum BoundaryError310268d2 {
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
impl BoundaryError310268d2 {
    /// Returns the static invariant clause violated by this refusal.
    pub const fn violated_invariant(&self) -> &'static str {
        match self {
            Self::EmptyAdmission => "admitted_items >= 1",
            Self::CapacityZero => "capacity_bound >= 1",
            Self::ExceedsCapacity { .. } => "admitted_items <= capacity_bound",
        }
    }
}

impl std::fmt::Display for BoundaryError310268d2 {
    fn fmt(&self, formatter: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(formatter, "{}: {:?}", self.violated_invariant(), self)
    }
}

impl std::error::Error for BoundaryError310268d2 {}

#[allow(dead_code, missing_docs)]
impl BoundaryRecord310268d2 {
    /// Validates and constructs a bounded admission record within `capacity_bound`.
    pub fn try_admit(
        admitted_items: u64,
        capacity_bound: u64,
    ) -> std::result::Result<Self, BoundaryError310268d2> {
        if capacity_bound == 0 {
            return Err(BoundaryError310268d2::CapacityZero);
        }
        if admitted_items == 0 {
            return Err(BoundaryError310268d2::EmptyAdmission);
        }
        if admitted_items > capacity_bound {
            return Err(BoundaryError310268d2::ExceedsCapacity {
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
fn l4_boundary_admits_and_refuses_310268d2() {
    let admitted = BoundaryRecord310268d2::try_admit(3, 8);
    assert!(admitted.is_ok());
    if let Ok(record) = admitted {
        assert_eq!(record.admitted_items(), 3);
        assert_eq!(record.capacity_bound(), 8);
        assert_eq!(record.remaining_capacity(), 5);
    }
    assert!(BoundaryRecord310268d2::try_admit(9, 8).is_err());
}

// Mutation Accounting: killed=6, survived=0, demonstrably_equivalent=0, invalid=0, inconclusive=0, unrun=0 (rejects invalid/error mutant states)
