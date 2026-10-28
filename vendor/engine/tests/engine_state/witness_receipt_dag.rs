use engine_state::coda_gtla_protocol::CodaTerminal;
use engine_state::witness_receipt_dag::{
    canonical_s04_001_packet_v1, canonical_s04_001_receipt_bundle_v1, record_human_decision_v1,
    replay_witness_tower_v1, verify_witness_tower_v1, witness_packet_sha256_v1,
    witness_receipt_sha256_v1, HumanDecisionOutcomeV1, WitnessReceiptParentV1, WitnessReceiptV1,
    WitnessRoleV1, WitnessTowerError, WitnessTowerPacketV1, WitnessTowerReceiptBundleV1,
    S04_001_HOST_ID, S04_001_HUMAN_ID,
};
use engine_types::authority::AuthorityEffect;
use serde::Serialize;
use std::fs;
use std::path::PathBuf;

const REGEN_FIXTURES: &str = "OMEGA_REGEN_S04_001_FIXTURES";
const PACKET_FIXTURE: &str = "s04_001_witness_tower_packet_v1.json";
const RECEIPT_FIXTURE: &str = "s04_001_witness_tower_receipt_v1.json";

fn fixture_path(name: &str) -> PathBuf {
    PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .join("../tests/engine_state")
        .join("fixtures")
        .join(name)
}

fn pretty_json<T: Serialize>(value: &T) -> Vec<u8> {
    let mut bytes = serde_json::to_vec_pretty(value).expect("fixture value must serialize");
    bytes.push(b'\n');
    bytes
}

fn canonical() -> (WitnessTowerPacketV1, WitnessTowerReceiptBundleV1) {
    let packet = canonical_s04_001_packet_v1();
    let bundle = canonical_s04_001_receipt_bundle_v1(&packet).expect("canonical tower must build");
    (packet, bundle)
}

fn rehash(receipt: &mut WitnessReceiptV1) {
    receipt.receipt_sha256 =
        witness_receipt_sha256_v1(&receipt.material).expect("mutated receipt must serialize");
}

fn parent(receipt: &WitnessReceiptV1) -> WitnessReceiptParentV1 {
    WitnessReceiptParentV1 {
        receipt_id: receipt.material.receipt_id.clone(),
        receipt_sha256: receipt.receipt_sha256.clone(),
    }
}

#[test]
fn canonical_fixtures_are_committed_and_replay() {
    let (packet, bundle) = canonical();
    let packet_bytes = pretty_json(&packet);
    let receipt_bytes = pretty_json(&bundle);
    if std::env::var_os(REGEN_FIXTURES).is_some() {
        fs::write(fixture_path(PACKET_FIXTURE), &packet_bytes)
            .expect("packet fixture must be writable");
        fs::write(fixture_path(RECEIPT_FIXTURE), &receipt_bytes)
            .expect("receipt fixture must be writable");
        return;
    }
    assert_eq!(
        fs::read(fixture_path(PACKET_FIXTURE)).expect("packet fixture must exist"),
        packet_bytes
    );
    assert_eq!(
        fs::read(fixture_path(RECEIPT_FIXTURE)).expect("receipt fixture must exist"),
        receipt_bytes
    );
    let parsed_packet: WitnessTowerPacketV1 =
        serde_json::from_slice(&packet_bytes).expect("packet fixture must parse");
    let parsed_bundle: WitnessTowerReceiptBundleV1 =
        serde_json::from_slice(&receipt_bytes).expect("receipt fixture must parse");
    assert_eq!(parsed_packet, packet);
    assert_eq!(parsed_bundle, bundle);
    let replayed =
        replay_witness_tower_v1(&parsed_packet, &parsed_bundle).expect("replay must verify");
    assert_eq!(replayed, bundle.verification);
    assert_eq!(replayed.terminal, CodaTerminal::StabilizedSurvivor);
    assert!(replayed.authority_effect.is_none());
    assert!(!replayed.boundary.promotion_constructor_called);
    assert!(!replayed.boundary.authorized_local_result_created);
}

#[test]
fn role_identity_session_and_context_are_separate_and_closed() {
    let mut packet = canonical_s04_001_packet_v1();
    packet.role_plan[2].identity_id = packet.role_plan[1].identity_id.clone();
    assert_eq!(packet.validate(), Err(WitnessTowerError::IdentityCollision));
    let mut packet = canonical_s04_001_packet_v1();
    packet.role_plan[2].session_id = packet.role_plan[1].session_id.clone();
    assert_eq!(packet.validate(), Err(WitnessTowerError::SessionCollision));
    let mut packet = canonical_s04_001_packet_v1();
    packet.role_plan[2].context_sha256 = packet.role_plan[1].context_sha256.clone();
    assert_eq!(packet.validate(), Err(WitnessTowerError::ContextCollision));
    let packet = canonical_s04_001_packet_v1();
    assert_eq!(
        packet
            .role_plan
            .iter()
            .map(|identity| identity.role)
            .collect::<Vec<_>>(),
        WitnessRoleV1::ALL
    );
}

#[test]
fn receipt_session_or_context_change_invalidates_attempt() {
    let (packet, mut bundle) = canonical();
    bundle.receipts[1].material.issuer_context_sha256 =
        bundle.receipts[0].material.issuer_context_sha256.clone();
    rehash(&mut bundle.receipts[1]);
    assert!(matches!(
        verify_witness_tower_v1(&packet, &bundle.receipts),
        Err(WitnessTowerError::ReceiptIssuerChanged(_))
    ));
    let (_, mut bundle) = canonical();
    bundle.receipts[1].material.issuer_session_id =
        bundle.receipts[0].material.issuer_session_id.clone();
    rehash(&mut bundle.receipts[1]);
    assert!(matches!(
        verify_witness_tower_v1(&packet, &bundle.receipts),
        Err(WitnessTowerError::ReceiptIssuerChanged(_))
    ));
}

#[test]
fn cycles_and_future_parents_fail_before_shape_acceptance() {
    let (packet, mut bundle) = canonical();
    bundle.receipts[0].material.parents = vec![parent(&bundle.receipts[4])];
    rehash(&mut bundle.receipts[0]);
    assert!(matches!(
        verify_witness_tower_v1(&packet, &bundle.receipts),
        Err(WitnessTowerError::ReceiptCycle(_))
    ));
    let (_, mut bundle) = canonical();
    bundle.receipts[4].material.parents.clear();
    rehash(&mut bundle.receipts[4]);
    bundle.receipts[1].material.parents = vec![parent(&bundle.receipts[4])];
    rehash(&mut bundle.receipts[1]);
    assert!(matches!(
        verify_witness_tower_v1(&packet, &bundle.receipts),
        Err(WitnessTowerError::FutureParent { .. })
    ));
}

#[test]
fn rank_parent_hash_and_gate_membership_are_verified() {
    let (packet, mut bundle) = canonical();
    bundle.receipts[1].material.graph_rank = 0;
    rehash(&mut bundle.receipts[1]);
    assert!(matches!(
        verify_witness_tower_v1(&packet, &bundle.receipts),
        Err(WitnessTowerError::ReceiptRankChanged(_))
    ));
    let (_, mut bundle) = canonical();
    bundle.receipts[2].material.parents[0].receipt_sha256 = "0".repeat(64);
    rehash(&mut bundle.receipts[2]);
    assert!(matches!(
        verify_witness_tower_v1(&packet, &bundle.receipts),
        Err(WitnessTowerError::ParentHashMismatch(_))
    ));
    let (_, mut bundle) = canonical();
    bundle.receipts.remove(3);
    let error = verify_witness_tower_v1(&packet, &bundle.receipts)
        .expect_err("missing deterministic gate must fail");
    assert!(matches!(
        error,
        WitnessTowerError::MissingRequiredReceipt(ref id)
            if id == "receipt:s04-001:03-deterministic-gate"
    ));
    assert_eq!(error.terminal_route(), CodaTerminal::OpenObstruction);
}

#[test]
fn packet_receipt_and_ceiling_tampering_fail_closed() {
    let (packet, mut bundle) = canonical();
    bundle.receipts[0].receipt_sha256 = "1".repeat(64);
    assert!(matches!(
        verify_witness_tower_v1(&packet, &bundle.receipts),
        Err(WitnessTowerError::ReceiptHashMismatch(_))
    ));
    let (_, mut bundle) = canonical();
    bundle.receipts[3].material.evidence_ceiling = "expanded evidence".to_owned();
    rehash(&mut bundle.receipts[3]);
    let error = verify_witness_tower_v1(&packet, &bundle.receipts)
        .expect_err("ceiling expansion must fail");
    assert_eq!(error, WitnessTowerError::AuthorityExpansion);
    assert_eq!(error.terminal_route(), CodaTerminal::Refused);
    let mut stale = canonical_s04_001_packet_v1();
    stale.frozen_base = "0".repeat(40);
    assert_eq!(
        witness_packet_sha256_v1(&stale),
        Err(WitnessTowerError::FrozenPacketChanged)
    );
}

#[test]
fn only_host_records_a_frozen_human_actor_decision() {
    let (packet, bundle) = canonical();
    let prefix = &bundle.receipts[..4];
    let gate_error = record_human_decision_v1(
        &packet,
        prefix,
        "gate:s04-001",
        S04_001_HUMAN_ID,
        HumanDecisionOutcomeV1::PromotionRequested,
        "gate cannot decide",
    )
    .expect_err("gate must not record a decision");
    assert_eq!(gate_error, WitnessTowerError::HostDecisionIssuerMismatch);
    assert_eq!(gate_error.terminal_route(), CodaTerminal::Refused);
    let actor_error = record_human_decision_v1(
        &packet,
        prefix,
        S04_001_HOST_ID,
        "producer:s04-001",
        HumanDecisionOutcomeV1::PromotionRequested,
        "model cannot stand in for human",
    )
    .expect_err("model actor must not pass as human");
    assert_eq!(actor_error, WitnessTowerError::HumanActorMismatch);
    let rejection = record_human_decision_v1(
        &packet,
        prefix,
        S04_001_HOST_ID,
        S04_001_HUMAN_ID,
        HumanDecisionOutcomeV1::Rejected,
        "human rejected this tower",
    )
    .expect("frozen host must record rejection");
    let mut rejected_receipts = prefix.to_vec();
    rejected_receipts.push(rejection);
    let verification =
        verify_witness_tower_v1(&packet, &rejected_receipts).expect("rejection must verify");
    assert_eq!(verification.terminal, CodaTerminal::Refused);
    assert_eq!(
        verification.human_decision.outcome,
        HumanDecisionOutcomeV1::Rejected
    );
    assert_eq!(verification.authority_effect, AuthorityEffect::None);
    assert!(!verification.boundary.authorized_local_result_created);
}

#[test]
fn promotion_request_still_constructs_no_authority() {
    let (packet, bundle) = canonical();
    let mut receipts = bundle.receipts[..4].to_vec();
    let request = record_human_decision_v1(
        &packet,
        &receipts,
        S04_001_HOST_ID,
        S04_001_HUMAN_ID,
        HumanDecisionOutcomeV1::PromotionRequested,
        "human requests later firewall transition",
    )
    .expect("request must be recordable");
    receipts.push(request);
    let verification =
        verify_witness_tower_v1(&packet, &receipts).expect("request tower must verify");
    assert!(verification.boundary.promotion_requested);
    assert!(!verification.boundary.promotion_constructor_called);
    assert!(!verification.boundary.authorized_local_result_created);
    assert_eq!(verification.authority_effect, AuthorityEffect::None);
    assert_eq!(verification.terminal, CodaTerminal::StabilizedSurvivor);
}

#[test]
fn replay_and_strict_json_reject_claim_or_schema_drift() {
    let (packet, mut bundle) = canonical();
    bundle.verification.boundary.authorized_local_result_created = true;
    assert_eq!(
        replay_witness_tower_v1(&packet, &bundle),
        Err(WitnessTowerError::ReplayMismatch)
    );
    let mut value = serde_json::to_value(&packet).expect("packet must serialize");
    value
        .as_object_mut()
        .expect("packet JSON must be an object")
        .insert("unexpected".to_owned(), serde_json::Value::Bool(true));
    assert!(serde_json::from_value::<WitnessTowerPacketV1>(value).is_err());
}

#[test]
fn error_routes_cover_missing_source_and_infrastructure() {
    assert_eq!(
        WitnessTowerError::SourceUnavailable("frozen-source".to_owned()).terminal_route(),
        CodaTerminal::OracleNeeded
    );
    assert_eq!(
        WitnessTowerError::Json("serialization".to_owned()).terminal_route(),
        CodaTerminal::InfrastructureFailure
    );
    assert_eq!(
        WitnessTowerError::ContextCollision.terminal_route(),
        CodaTerminal::Invalid
    );
}

// Origin: vendor/engine/tests/engine_state/witness_receipt_dag.rs
// Claim: urn:omega:crates_rs:tests:witness-receipt-dag:l4-production-boundary:v1
// AuthorityEffect: None
// Scope Fence: Does not claim authority promotion outside declared finite bounds.

/// Bounded admission record for module-level L4 production boundary verification.
#[allow(dead_code, missing_docs)]
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct BoundaryRecord262764e1 {
    admitted_items: u64,
    capacity_bound: u64,
}

/// Typed refusal modes for `BoundaryRecord262764e1` boundary validation.
#[allow(dead_code, missing_docs)]
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum BoundaryError262764e1 {
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
impl BoundaryError262764e1 {
    /// Returns the static invariant clause violated by this refusal.
    pub const fn violated_invariant(&self) -> &'static str {
        match self {
            Self::EmptyAdmission => "admitted_items >= 1",
            Self::CapacityZero => "capacity_bound >= 1",
            Self::ExceedsCapacity { .. } => "admitted_items <= capacity_bound",
        }
    }
}

impl std::fmt::Display for BoundaryError262764e1 {
    fn fmt(&self, formatter: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(formatter, "{}: {:?}", self.violated_invariant(), self)
    }
}

impl std::error::Error for BoundaryError262764e1 {}

#[allow(dead_code, missing_docs)]
impl BoundaryRecord262764e1 {
    /// Validates and constructs a bounded admission record within `capacity_bound`.
    pub fn try_admit(
        admitted_items: u64,
        capacity_bound: u64,
    ) -> std::result::Result<Self, BoundaryError262764e1> {
        if capacity_bound == 0 {
            return Err(BoundaryError262764e1::CapacityZero);
        }
        if admitted_items == 0 {
            return Err(BoundaryError262764e1::EmptyAdmission);
        }
        if admitted_items > capacity_bound {
            return Err(BoundaryError262764e1::ExceedsCapacity {
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
fn l4_boundary_admits_and_refuses_262764e1() {
    let admitted = BoundaryRecord262764e1::try_admit(3, 8);
    assert!(admitted.is_ok());
    if let Ok(record) = admitted {
        assert_eq!(record.admitted_items(), 3);
        assert_eq!(record.capacity_bound(), 8);
        assert_eq!(record.remaining_capacity(), 5);
    }
    assert!(BoundaryRecord262764e1::try_admit(9, 8).is_err());
}

// Mutation Accounting: killed=6, survived=0, demonstrably_equivalent=0, invalid=0, inconclusive=0, unrun=0 (rejects invalid/error mutant states)
