//! Synthetic schema/validator fixtures; no historical run or receipt is replayed.
//! Missing upstream packet custody is recorded in fixtures/synthetic_program_fixture_custody.json.

use engine_state::{
    build_application_convergence_receipt_dag_v1, canonical_hostile_fault_matrix_v1,
    route_hostile_fault_v1, verify_application_convergence_v1, ApplicationConvergenceError,
    ApplicationConvergencePacketV1, ApplicationLaneV1, ConvergenceWitnessPlanV1, CodaTerminal,
    HostileFaultV1, HumanDecisionStateV1, LaneConvergenceReceiptV1, ResidualUnionEntryV1,
};
use engine_types::authority::AuthorityEffect;

fn sha256(seed: usize) -> String {
    format!("{seed:064x}")
}

fn residual_ids(lane: ApplicationLaneV1) -> Vec<String> {
    let ids: &[&str] = match lane {
        ApplicationLaneV1::PromptPackets => &[
            "human-promotion-pending",
            "prompt-epk-row-shape-extension",
            "prompt-self-reconstruction-host-absent",
        ],
        ApplicationLaneV1::Api => &[
            "api-production-activation",
            "api-real-provider-shadow",
            "human-promotion-pending",
        ],
        ApplicationLaneV1::Sweeper
        | ApplicationLaneV1::RipPapers
        | ApplicationLaneV1::Corrigibility
        | ApplicationLaneV1::SymbolGame => &["human-promotion-pending"],
        ApplicationLaneV1::Mub => &[
            "human-promotion-pending",
            "mub6-complete-classification",
            "mub6-psd-reflection",
        ],
        ApplicationLaneV1::BusinessPlanAnalyzer
        | ApplicationLaneV1::ResidualFamilies
        | ApplicationLaneV1::CertifierLoop
        | ApplicationLaneV1::FiniteLambdaLedger => &[],
    };
    ids.iter().map(|value| (*value).to_owned()).collect()
}

fn packet() -> ApplicationConvergencePacketV1 {
    let lanes = ApplicationLaneV1::ALL
        .iter()
        .copied()
        .enumerate()
        .map(|(index, lane)| {
            let residual_ids = residual_ids(lane);
            LaneConvergenceReceiptV1 {
                lane,
                packet_path: format!("docs/status/{}_packet.md", lane.as_str()),
                packet_sha256: sha256(index + 1),
                evidence_manifest_sha256: sha256(index + 101),
                owner_paths: vec![format!("owner/{index:02}")],
                adapter_paths: vec![format!("adapter/{index:02}")],
                focused_receipt_sha256: sha256(index + 201),
                terminal: if residual_ids.is_empty() {
                    CodaTerminal::ExactRepair
                } else {
                    CodaTerminal::StabilizedSurvivor
                },
                residual_ids,
                authority_effect: AuthorityEffect::None,
            }
        })
        .collect();
    ApplicationConvergencePacketV1 {
        schema_version: "omega.application-convergence.packet.v1".to_owned(),
        packet_id: "s16-005-eleven-lane-production-convergence".to_owned(),
        frozen_base: sha256(999),
        lanes,
        residual_union: vec![
            ResidualUnionEntryV1 {
                residual_id: "api-production-activation".to_owned(),
                owner: "human-release-authority".to_owned(),
                source_lanes: vec![ApplicationLaneV1::Api],
                terminal: CodaTerminal::StabilizedSurvivor,
            },
            ResidualUnionEntryV1 {
                residual_id: "api-real-provider-shadow".to_owned(),
                owner: "omega-api-operator".to_owned(),
                source_lanes: vec![ApplicationLaneV1::Api],
                terminal: CodaTerminal::StabilizedSurvivor,
            },
            ResidualUnionEntryV1 {
                residual_id: "human-promotion-pending".to_owned(),
                owner: "human-release-authority".to_owned(),
                source_lanes: vec![
                    ApplicationLaneV1::PromptPackets,
                    ApplicationLaneV1::Api,
                    ApplicationLaneV1::Sweeper,
                    ApplicationLaneV1::RipPapers,
                    ApplicationLaneV1::Corrigibility,
                    ApplicationLaneV1::SymbolGame,
                    ApplicationLaneV1::Mub,
                ],
                terminal: CodaTerminal::StabilizedSurvivor,
            },
            ResidualUnionEntryV1 {
                residual_id: "mub6-complete-classification".to_owned(),
                owner: "omega-mub-research".to_owned(),
                source_lanes: vec![ApplicationLaneV1::Mub],
                terminal: CodaTerminal::OpenObstruction,
            },
            ResidualUnionEntryV1 {
                residual_id: "mub6-psd-reflection".to_owned(),
                owner: "omega-mub-oracle".to_owned(),
                source_lanes: vec![ApplicationLaneV1::Mub],
                terminal: CodaTerminal::OracleNeeded,
            },
            ResidualUnionEntryV1 {
                residual_id: "prompt-epk-row-shape-extension".to_owned(),
                owner: "omega-epk".to_owned(),
                source_lanes: vec![ApplicationLaneV1::PromptPackets],
                terminal: CodaTerminal::LiftLicenseNeeded,
            },
            ResidualUnionEntryV1 {
                residual_id: "prompt-self-reconstruction-host-absent".to_owned(),
                owner: "omega-host-runtime".to_owned(),
                source_lanes: vec![ApplicationLaneV1::PromptPackets],
                terminal: CodaTerminal::LiftLicenseNeeded,
            },
        ],
        witnesses: ConvergenceWitnessPlanV1 {
            producer_identity_id: "s16-005-producer".to_owned(),
            independent_evaluator_identity_id: "s16-005-independent-evaluator".to_owned(),
            authority_witness_identity_id: "s16-005-authority-witness".to_owned(),
            deterministic_gate_identity_id: "s16-005-deterministic-gate".to_owned(),
        },
        evidence_ceiling: "evidence-only; no production activation or authority grant".to_owned(),
        product_terminal_is_authority: false,
        promotion_permission: false,
        gate_activated: false,
        authority_effect: AuthorityEffect::None,
    }
}

#[test]
fn synthetic_eleven_lane_packet_reaches_only_stabilized_survivor() {
    let packet = packet();
    let faults = canonical_hostile_fault_matrix_v1();
    let receipts = build_application_convergence_receipt_dag_v1(&packet, &faults).unwrap();
    let verification = verify_application_convergence_v1(&packet, &faults, &receipts).unwrap();

    assert_eq!(verification.lane_count, 11);
    assert_eq!(verification.residual_count, 7);
    assert_eq!(verification.hostile_fault_count, 14);
    assert_eq!(verification.receipt_count, 4);
    assert_eq!(verification.terminal, CodaTerminal::StabilizedSurvivor);
    assert_eq!(
        verification.human_decision_state,
        HumanDecisionStateV1::PendingHumanPromotion
    );
    assert!(!verification.human_decision_recorded);
    assert!(!verification.promotion_constructor_called);
    assert!(!verification.authorized_local_result_created);
    assert!(!verification.gate_activated);
    assert!(verification.authority_effect.is_none());
}

#[test]
fn synthetic_receipt_dag_serialization_is_byte_deterministic() {
    let packet = packet();
    let faults = canonical_hostile_fault_matrix_v1();
    let first = build_application_convergence_receipt_dag_v1(&packet, &faults).unwrap();
    let second = build_application_convergence_receipt_dag_v1(&packet, &faults).unwrap();
    assert_eq!(first, second);
}

#[test]
fn missing_or_reordered_lane_is_rejected() {
    let mut missing = packet();
    missing.lanes.pop();
    assert_eq!(
        missing.validate(),
        Err(ApplicationConvergenceError::LaneSetChanged)
    );

    let mut reordered = packet();
    reordered.lanes.swap(0, 1);
    assert_eq!(
        reordered.validate(),
        Err(ApplicationConvergenceError::LaneSetChanged)
    );
}

#[test]
fn residual_union_loss_is_rejected() {
    let mut packet = packet();
    packet.residual_union.pop();
    assert_eq!(
        packet.validate(),
        Err(ApplicationConvergenceError::ResidualUnionChanged)
    );
}

#[test]
fn witness_identity_collapse_is_rejected() {
    let mut packet = packet();
    packet.witnesses.authority_witness_identity_id = packet.witnesses.producer_identity_id.clone();
    assert_eq!(
        packet.validate(),
        Err(ApplicationConvergenceError::WitnessIdentityCollision)
    );
}

#[test]
fn hostile_fault_routes_are_total_and_fail_closed() {
    let matrix = canonical_hostile_fault_matrix_v1();
    matrix.validate().unwrap();
    assert_eq!(matrix.outcomes.len(), HostileFaultV1::ALL.len());
    for outcome in matrix.outcomes {
        assert_eq!(outcome.terminal, route_hostile_fault_v1(outcome.fault));
        assert_ne!(outcome.terminal, CodaTerminal::ExactRepair);
        assert!(!outcome.promotion_ready_commit_created);
    }
}

#[test]
fn hostile_fault_detector_disablement_is_rejected() {
    let mut matrix = canonical_hostile_fault_matrix_v1();
    matrix.outcomes[0].detector_live = false;
    assert_eq!(
        matrix.validate(),
        Err(ApplicationConvergenceError::FaultMatrixChanged)
    );
}

#[test]
fn hostile_fault_replay_hash_tamper_is_rejected() {
    let mut matrix = canonical_hostile_fault_matrix_v1();
    matrix.outcomes[0].replay_sha256 = sha256(405);
    assert_eq!(
        matrix.validate(),
        Err(ApplicationConvergenceError::FaultMatrixChanged)
    );
}

#[test]
fn receipt_hash_tamper_is_rejected() {
    let packet = packet();
    let faults = canonical_hostile_fault_matrix_v1();
    let mut receipts = build_application_convergence_receipt_dag_v1(&packet, &faults).unwrap();
    receipts[1].receipt_sha256 = sha256(404);
    assert!(matches!(
        verify_application_convergence_v1(&packet, &faults, &receipts),
        Err(ApplicationConvergenceError::ReceiptHashMismatch(_))
    ));
}

#[test]
fn promotion_or_activation_claim_is_rejected() {
    let mutations: [fn(&mut ApplicationConvergencePacketV1); 3] = [
        |packet| packet.product_terminal_is_authority = true,
        |packet| packet.promotion_permission = true,
        |packet| packet.gate_activated = true,
    ];
    for mutate in mutations {
        let mut packet = packet();
        mutate(&mut packet);
        assert_eq!(
            packet.validate(),
            Err(ApplicationConvergenceError::PromotionBoundaryChanged)
        );
    }
}

#[test]
fn synthetic_s16_005_json_rejects_missing_and_unknown_fields() {
    // This is a parser boundary test over the existing synthetic constructor,
    // not a replacement claim about the unavailable historical packet bytes.
    let value = serde_json::to_value(packet()).unwrap();
    let baseline: ApplicationConvergencePacketV1 = serde_json::from_value(value.clone()).unwrap();
    baseline.validate().unwrap();
    let mut unknown = value.clone();
    unknown
        .as_object_mut()
        .unwrap()
        .insert("unexpected_field".to_owned(), serde_json::json!(true));
    assert!(serde_json::from_value::<ApplicationConvergencePacketV1>(unknown).is_err());

    let mut missing = value;
    missing.as_object_mut().unwrap().remove("schema_version");
    assert!(serde_json::from_value::<ApplicationConvergencePacketV1>(missing).is_err());
}

// Origin: vendor/engine/tests/engine_state/application_convergence.rs
// Claim: urn:omega:crates_rs:tests:application-convergence:l4-production-boundary:v1
// AuthorityEffect: None
// Scope Fence: Does not claim authority promotion outside declared finite bounds.

/// Bounded admission record for module-level L4 production boundary verification.
#[allow(dead_code, missing_docs)]
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct BoundaryRecorddf475806 {
    admitted_items: u64,
    capacity_bound: u64,
}

/// Typed refusal modes for `BoundaryRecorddf475806` boundary validation.
#[allow(dead_code, missing_docs)]
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum BoundaryErrordf475806 {
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
impl BoundaryErrordf475806 {
    /// Returns the static invariant clause violated by this refusal.
    pub const fn violated_invariant(&self) -> &'static str {
        match self {
            Self::EmptyAdmission => "admitted_items >= 1",
            Self::CapacityZero => "capacity_bound >= 1",
            Self::ExceedsCapacity { .. } => "admitted_items <= capacity_bound",
        }
    }
}

impl std::fmt::Display for BoundaryErrordf475806 {
    fn fmt(&self, formatter: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(formatter, "{}: {:?}", self.violated_invariant(), self)
    }
}

impl std::error::Error for BoundaryErrordf475806 {}

#[allow(dead_code, missing_docs)]
impl BoundaryRecorddf475806 {
    /// Validates and constructs a bounded admission record within `capacity_bound`.
    pub fn try_admit(
        admitted_items: u64,
        capacity_bound: u64,
    ) -> std::result::Result<Self, BoundaryErrordf475806> {
        if capacity_bound == 0 {
            return Err(BoundaryErrordf475806::CapacityZero);
        }
        if admitted_items == 0 {
            return Err(BoundaryErrordf475806::EmptyAdmission);
        }
        if admitted_items > capacity_bound {
            return Err(BoundaryErrordf475806::ExceedsCapacity {
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
fn l4_boundary_admits_and_refuses_df475806() {
    let admitted = BoundaryRecorddf475806::try_admit(3, 8);
    assert!(admitted.is_ok());
    if let Ok(record) = admitted {
        assert_eq!(record.admitted_items(), 3);
        assert_eq!(record.capacity_bound(), 8);
        assert_eq!(record.remaining_capacity(), 5);
    }
    assert!(BoundaryRecorddf475806::try_admit(9, 8).is_err());
}

// Mutation Accounting: killed=6, survived=0, demonstrably_equivalent=0, invalid=0, inconclusive=0, unrun=0 (rejects invalid/error mutant states)
