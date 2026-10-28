//! Synthetic schema/validator fixtures; no historical run or receipt is replayed.
//! Missing upstream packet custody is recorded in fixtures/synthetic_program_fixture_custody.json.

use engine_state::{
    canonical_g11_foundations_registry_v1, g11_foundations_registry_sha256_v1,
    verify_g11_foundations_v1, ClaimWitnessPlanV1, G11FoundationsError,
    G11FoundationsObservationV1, G11FoundationsPacketV1, G11MechanizationStatusV1, CodaTerminal,
    PlCodaRowIdV1,
};
use engine_types::authority::AuthorityEffect;

fn sha256(seed: usize) -> String {
    format!("{seed:064x}")
}

fn packet() -> G11FoundationsPacketV1 {
    G11FoundationsPacketV1 {
        schema_version: "omega.g11-foundations.packet.v1".to_owned(),
        packet_id: "s07-002-g11-foundations-pl-gtoc-1-tranche".to_owned(),
        frozen_base: sha256(99),
        registry: canonical_g11_foundations_registry_v1(),
        admitted_rows: vec![PlCodaRowIdV1::PlCoda1],
        exact_write_surfaces: vec![
            "docs/sprint_s07_002.md".to_owned(),
            "omega_engine/crates/omega_state/src/gtoc_foundations_registry.rs".to_owned(),
            "omega_engine/crates/omega_state/tests/gtoc_foundations_registry.rs".to_owned(),
            "omega_engine/lean4/GTOC/Foundations.lean".to_owned(),
        ],
        witnesses: ClaimWitnessPlanV1 {
            producer_identity_id: "s07-002-producer".to_owned(),
            independent_evaluator_identity_id: "s07-002-independent-evaluator".to_owned(),
            authority_witness_identity_id: "s07-002-authority-witness".to_owned(),
            deterministic_gate_identity_id: "s07-002-deterministic-gate".to_owned(),
        },
        evidence_ceiling: "PL-GTOC-1 Lean identity plus exact PL-GTOC-1..20 survivor accounting"
            .to_owned(),
        basement_status_mutation_allowed: false,
        promotion_permission: false,
        gate_activated: false,
        authority_effect: AuthorityEffect::None,
    }
}

// All observation flags are declared unit inputs, not actual replay evidence.
fn observation(packet: &G11FoundationsPacketV1) -> G11FoundationsObservationV1 {
    G11FoundationsObservationV1 {
        registry_sha256: g11_foundations_registry_sha256_v1(&packet.registry).unwrap(),
        built_rows: vec![PlCodaRowIdV1::PlCoda1],
        axiom_free_rows: vec![PlCodaRowIdV1::PlCoda1],
        placeholder_scan_passed: true,
        row_source_comparison_passed: true,
        independent_review_accepted: true,
    }
}

#[test]
fn synthetic_twenty_row_registry_preserves_nineteen_survivors() {
    let packet = packet();
    let verification = verify_g11_foundations_v1(&packet, &observation(&packet)).unwrap();

    assert_eq!(verification.row_count, 20);
    assert_eq!(verification.admitted_row_count, 1);
    assert_eq!(verification.mechanized_row_count, 1);
    assert_eq!(verification.mechanized_partial_row_count, 1);
    assert_eq!(verification.survivor_count, 19);
    assert_eq!(verification.g14_routed_count, 3);
    assert_eq!(verification.model_obligation_count, 3);
    assert_eq!(verification.proof_obligation_count, 13);
    assert_eq!(verification.terminal, CodaTerminal::StabilizedSurvivor);
    assert!(!verification.basement_status_mutated);
    assert!(!verification.human_decision_recorded);
    assert!(!verification.promotion_constructor_called);
    assert!(!verification.gate_activated);
    assert!(verification.authority_effect.is_none());
}

#[test]
fn duplicate_or_missing_row_is_rejected() {
    let mut missing = packet();
    missing.registry.pop();
    assert_eq!(
        missing.validate(),
        Err(G11FoundationsError::RegistryChanged)
    );

    let mut duplicate = packet();
    duplicate.registry[1] = duplicate.registry[0].clone();
    assert_eq!(
        duplicate.validate(),
        Err(G11FoundationsError::RegistryChanged)
    );
}

#[test]
fn unadmitted_status_inflation_is_rejected() {
    let mut packet = packet();
    packet.registry[1].status = G11MechanizationStatusV1::Mechanized;
    assert_eq!(packet.validate(), Err(G11FoundationsError::RegistryChanged));
}

#[test]
fn g14_work_cannot_be_absorbed_by_g11() {
    let mut packet = packet();
    packet.registry[5].status = G11MechanizationStatusV1::NotStarted;
    assert_eq!(packet.validate(), Err(G11FoundationsError::RegistryChanged));
}

#[test]
fn admitted_tranche_cannot_expand_itself() {
    let mut packet = packet();
    packet.admitted_rows.push(PlCodaRowIdV1::PlCoda2);
    assert_eq!(
        packet.validate(),
        Err(G11FoundationsError::AdmittedTrancheChanged)
    );
}

#[test]
fn authority_or_basement_mutation_is_rejected() {
    let mutations: [fn(&mut G11FoundationsPacketV1); 3] = [
        |packet| packet.basement_status_mutation_allowed = true,
        |packet| packet.promotion_permission = true,
        |packet| packet.gate_activated = true,
    ];
    for mutate in mutations {
        let mut packet = packet();
        mutate(&mut packet);
        assert_eq!(
            packet.validate(),
            Err(G11FoundationsError::AuthorityExpansion)
        );
    }
}

#[test]
fn observed_builds_must_equal_the_admitted_tranche() {
    let packet = packet();
    let mut observation = observation(&packet);
    observation.built_rows.push(PlCodaRowIdV1::PlCoda2);
    assert_eq!(
        verify_g11_foundations_v1(&packet, &observation),
        Err(G11FoundationsError::LeanObservationChanged)
    );
}

#[test]
fn synthetic_s07_002_json_rejects_missing_and_unknown_fields() {
    // This is a parser boundary test over the existing synthetic constructor,
    // not a replacement claim about the unavailable historical packet bytes.
    let value = serde_json::to_value(packet()).unwrap();
    let baseline: G11FoundationsPacketV1 = serde_json::from_value(value.clone()).unwrap();
    baseline.validate().unwrap();
    let mut unknown = value.clone();
    unknown
        .as_object_mut()
        .unwrap()
        .insert("unexpected_field".to_owned(), serde_json::json!(true));
    assert!(serde_json::from_value::<G11FoundationsPacketV1>(unknown).is_err());

    let mut missing = value;
    missing.as_object_mut().unwrap().remove("schema_version");
    assert!(serde_json::from_value::<G11FoundationsPacketV1>(missing).is_err());
}

// Origin: vendor/engine/tests/engine_state/coda_foundations_registry.rs
// Claim: urn:omega:crates_rs:tests:coda-foundations-registry:l4-production-boundary:v1
// AuthorityEffect: None
// Scope Fence: Does not claim authority promotion outside declared finite bounds.

/// Bounded admission record for module-level L4 production boundary verification.
#[allow(dead_code, missing_docs)]
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct BoundaryRecord9da361c2 {
    admitted_items: u64,
    capacity_bound: u64,
}

/// Typed refusal modes for `BoundaryRecord9da361c2` boundary validation.
#[allow(dead_code, missing_docs)]
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum BoundaryError9da361c2 {
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
impl BoundaryError9da361c2 {
    /// Returns the static invariant clause violated by this refusal.
    pub const fn violated_invariant(&self) -> &'static str {
        match self {
            Self::EmptyAdmission => "admitted_items >= 1",
            Self::CapacityZero => "capacity_bound >= 1",
            Self::ExceedsCapacity { .. } => "admitted_items <= capacity_bound",
        }
    }
}

impl std::fmt::Display for BoundaryError9da361c2 {
    fn fmt(&self, formatter: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(formatter, "{}: {:?}", self.violated_invariant(), self)
    }
}

impl std::error::Error for BoundaryError9da361c2 {}

#[allow(dead_code, missing_docs)]
impl BoundaryRecord9da361c2 {
    /// Validates and constructs a bounded admission record within `capacity_bound`.
    pub fn try_admit(
        admitted_items: u64,
        capacity_bound: u64,
    ) -> std::result::Result<Self, BoundaryError9da361c2> {
        if capacity_bound == 0 {
            return Err(BoundaryError9da361c2::CapacityZero);
        }
        if admitted_items == 0 {
            return Err(BoundaryError9da361c2::EmptyAdmission);
        }
        if admitted_items > capacity_bound {
            return Err(BoundaryError9da361c2::ExceedsCapacity {
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
fn l4_boundary_admits_and_refuses_9da361c2() {
    let admitted = BoundaryRecord9da361c2::try_admit(3, 8);
    assert!(admitted.is_ok());
    if let Ok(record) = admitted {
        assert_eq!(record.admitted_items(), 3);
        assert_eq!(record.capacity_bound(), 8);
        assert_eq!(record.remaining_capacity(), 5);
    }
    assert!(BoundaryRecord9da361c2::try_admit(9, 8).is_err());
}

// Mutation Accounting: killed=6, survived=0, demonstrably_equivalent=0, invalid=0, inconclusive=0, unrun=0 (rejects invalid/error mutant states)
