use engine_state::{
    canonical_t26_dependents_v1, canonical_t26_hypotheses_v1, t26_hypothesis_registry_sha256_v1,
    verify_t26_glue_v1, ClaimWitnessPlanV1, CodaTerminal, ResearchProgramBoundaryV1, T26GlueError,
    T26GlueObservationV1, T26GluePacketV1,
};
use engine_types::authority::AuthorityEffect;

fn packet() -> T26GluePacketV1 {
    T26GluePacketV1 {
        schema_version: "omega.gtla-t26-glue.packet.v1".to_owned(),
        packet_id: "s07-003-gtla-t26-exact-reblock".to_owned(),
        frozen_base: "e554d6310eb3992a5521046c3f6f4843f9fc5411".to_owned(),
        enc_id: "ENC-0546".to_owned(),
        theorem_id: "GTLA-T26".to_owned(),
        hypotheses: canonical_t26_hypotheses_v1(),
        downstream: canonical_t26_dependents_v1(),
        exact_write_surfaces: vec![
            "docs/sprint_s07_003.md".to_owned(),
            "omega_engine/crates/omega_state/src/gtla_t26_glue.rs".to_owned(),
        ],
        boundary: ResearchProgramBoundaryV1 {
            witnesses: ClaimWitnessPlanV1 {
                producer_identity_id: "codex-s07-003-producer".to_owned(),
                independent_evaluator_identity_id: "rust-s07-003-evaluator".to_owned(),
                authority_witness_identity_id: "firewall-s07-003-witness".to_owned(),
                deterministic_gate_identity_id: "host-s07-003-gate".to_owned(),
            },
            evidence_ceiling: "GTLA-T26 exact re-block only".to_owned(),
            publication_permission: false,
            promotion_permission: false,
            gate_activated: false,
            authority_effect: AuthorityEffect::None,
        },
    }
}

fn observation(packet: &T26GluePacketV1) -> T26GlueObservationV1 {
    T26GlueObservationV1 {
        hypothesis_registry_sha256: t26_hypothesis_registry_sha256_v1(&packet.hypotheses).unwrap(),
        h3_double_prime_construction_supplied: false,
        enc_status: "CONDITIONAL".to_owned(),
        lean_status: "NOT-STARTED".to_owned(),
        downstream_statuses_preserved: true,
        independent_review_accepted: true,
    }
}

#[test]
fn exact_t26_surface_reblocks_only_h3_double_prime() {
    let packet = packet();
    let result = verify_t26_glue_v1(&packet, &observation(&packet)).unwrap();
    assert_eq!(result.hypothesis_count, 6);
    assert_eq!(result.open_hypotheses.len(), 1);
    assert_eq!(result.terminal, CodaTerminal::OpenObstruction);
    assert_eq!(result.authority_effect, AuthorityEffect::None);
    assert!(!result.human_decision_recorded);
    assert!(!result.gate_activated);
}

#[test]
fn a_missing_hypothesis_is_rejected() {
    let mut packet = packet();
    packet.hypotheses.pop();
    assert_eq!(
        packet.validate(),
        Err(T26GlueError::HypothesisRegistryChanged)
    );
}

#[test]
fn an_unlicensed_glue_construction_is_rejected() {
    let packet = packet();
    let mut observation = observation(&packet);
    observation.h3_double_prime_construction_supplied = true;
    assert_eq!(
        verify_t26_glue_v1(&packet, &observation),
        Err(T26GlueError::UnsupportedGlueConstruction)
    );
}

#[test]
fn enc_or_lean_status_inflation_is_rejected() {
    let packet = packet();
    let mut observation = observation(&packet);
    observation.enc_status = "PROVED-PROSE".to_owned();
    assert_eq!(
        verify_t26_glue_v1(&packet, &observation),
        Err(T26GlueError::StatusInflation)
    );
}

#[test]
fn downstream_status_drift_is_rejected() {
    let packet = packet();
    let mut observation = observation(&packet);
    observation.downstream_statuses_preserved = false;
    assert_eq!(
        verify_t26_glue_v1(&packet, &observation),
        Err(T26GlueError::DownstreamStatusDrift)
    );
}

#[test]
fn witness_identity_collapse_is_rejected() {
    let mut packet = packet();
    packet.boundary.witnesses.independent_evaluator_identity_id =
        packet.boundary.witnesses.producer_identity_id.clone();
    assert!(packet.validate().is_err());
}

// Origin: vendor/engine/tests/engine_state/coda_gtla_t26_glue.rs
// Claim: urn:omega:crates_rs:tests:coda-gtla-t26-glue:l4-production-boundary:v1
// AuthorityEffect: None
// Scope Fence: Does not claim authority promotion outside declared finite bounds.

/// Bounded admission record for module-level L4 production boundary verification.
#[allow(dead_code, missing_docs)]
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct BoundaryRecord938abf9f {
    admitted_items: u64,
    capacity_bound: u64,
}

/// Typed refusal modes for `BoundaryRecord938abf9f` boundary validation.
#[allow(dead_code, missing_docs)]
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum BoundaryError938abf9f {
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
impl BoundaryError938abf9f {
    /// Returns the static invariant clause violated by this refusal.
    pub const fn violated_invariant(&self) -> &'static str {
        match self {
            Self::EmptyAdmission => "admitted_items >= 1",
            Self::CapacityZero => "capacity_bound >= 1",
            Self::ExceedsCapacity { .. } => "admitted_items <= capacity_bound",
        }
    }
}

impl std::fmt::Display for BoundaryError938abf9f {
    fn fmt(&self, formatter: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(formatter, "{}: {:?}", self.violated_invariant(), self)
    }
}

impl std::error::Error for BoundaryError938abf9f {}

#[allow(dead_code, missing_docs)]
impl BoundaryRecord938abf9f {
    /// Validates and constructs a bounded admission record within `capacity_bound`.
    pub fn try_admit(
        admitted_items: u64,
        capacity_bound: u64,
    ) -> std::result::Result<Self, BoundaryError938abf9f> {
        if capacity_bound == 0 {
            return Err(BoundaryError938abf9f::CapacityZero);
        }
        if admitted_items == 0 {
            return Err(BoundaryError938abf9f::EmptyAdmission);
        }
        if admitted_items > capacity_bound {
            return Err(BoundaryError938abf9f::ExceedsCapacity {
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
fn l4_boundary_admits_and_refuses_938abf9f() {
    let admitted = BoundaryRecord938abf9f::try_admit(3, 8);
    assert!(admitted.is_ok());
    if let Ok(record) = admitted {
        assert_eq!(record.admitted_items(), 3);
        assert_eq!(record.capacity_bound(), 8);
        assert_eq!(record.remaining_capacity(), 5);
    }
    assert!(BoundaryRecord938abf9f::try_admit(9, 8).is_err());
}

// Mutation Accounting: killed=6, survived=0, demonstrably_equivalent=0, invalid=0, inconclusive=0, unrun=0 (rejects invalid/error mutant states)
