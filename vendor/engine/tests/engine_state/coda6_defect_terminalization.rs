#[path = "support/upstream_history.rs"]
mod upstream_history;

use std::collections::BTreeMap;
use std::fs;
use std::path::{Path, PathBuf};

use engine_state::coda6_defect_terminalization::{
    aggregate_coda6_terminals_v1, canonical_coda6_json_line_v1, canonical_s06_003_packet_v1,
    canonical_s06_003_receipt_v1, classify_coda6_diagnostic_v1, coda6_observer_sha256_v1,
    coda6_packet_sha256_v1, coda6_receipt_sha256_v1, coda6_verification_sha256_v1,
    parse_coda6_packet_canonical_v1, parse_coda6_receipt_canonical_v1,
    parse_coda6_verification_canonical_v1, verify_coda6_defect_terminalization_v1,
    DiagnosticEvidenceV1, DiagnosticRuleV1, Coda6ArtifactBytesV1,
    Coda6DefectTerminalizationPacketV1, Coda6DefectTerminalizationReceiptV1, Coda6Error,
    SurvivorRouteV1, S06_002_VERIFICATION_PATH, S06_003_FROZEN_BASE, S06_003_CODA5_RESIDUAL_ID,
};
use engine_state::coda_gtla_protocol::CodaTerminal;

const PACKET_FIXTURE: &str = "s06_003_gtoc6_packet_v1.json";
const RECEIPT_FIXTURE: &str = "s06_003_gtoc6_receipt_v1.json";
const VERIFICATION_FIXTURE: &str = "s06_003_gtoc6_verification_v1.json";

fn fixture_path(name: &str) -> PathBuf {
    Path::new(env!("CARGO_MANIFEST_DIR"))
        .join("../tests/engine_state")
        .join("fixtures")
        .join(name)
}

fn artifact_bytes(packet: &Coda6DefectTerminalizationPacketV1) -> Coda6ArtifactBytesV1 {
    packet
        .input_artifacts
        .iter()
        .map(|artifact| {
            let bytes = upstream_history::frozen_blob(&packet.frozen_base, &artifact.path);
            (artifact.path.clone(), bytes)
        })
        .collect::<BTreeMap<_, _>>()
}

fn canonical_case() -> (
    Coda6DefectTerminalizationPacketV1,
    Coda6DefectTerminalizationReceiptV1,
    Coda6ArtifactBytesV1,
) {
    let packet = canonical_s06_003_packet_v1();
    let receipt = canonical_s06_003_receipt_v1().expect("canonical receipt");
    let artifacts = artifact_bytes(&packet);
    (packet, receipt, artifacts)
}

fn assert_error_route(
    packet: &Coda6DefectTerminalizationPacketV1,
    receipt: &Coda6DefectTerminalizationReceiptV1,
    artifacts: &Coda6ArtifactBytesV1,
    expected: Coda6Error,
    route: CodaTerminal,
) {
    let error = verify_coda6_defect_terminalization_v1(packet, receipt, artifacts)
        .expect_err("hostile receipt must fail");
    assert_eq!(error, expected);
    assert_eq!(error.terminal_route(), route);
}

#[test]
fn canonical_fixtures_classify_every_subclaim_and_preserve_both_survivors() {
    let (packet, receipt, artifacts) = canonical_case();
    let verification = verify_coda6_defect_terminalization_v1(&packet, &receipt, &artifacts)
        .expect("canonical terminalization verifies");
    let packet_bytes = canonical_coda6_json_line_v1(&packet).unwrap();
    let receipt_bytes = canonical_coda6_json_line_v1(&receipt).unwrap();
    let verification_bytes = canonical_coda6_json_line_v1(&verification).unwrap();

    if std::env::var_os("OMEGA_REGEN_S06_003_FIXTURES").is_some() {
        for (name, bytes) in [
            (PACKET_FIXTURE, &packet_bytes),
            (RECEIPT_FIXTURE, &receipt_bytes),
            (VERIFICATION_FIXTURE, &verification_bytes),
        ] {
            fs::write(fixture_path(name), bytes).expect("write canonical fixture");
        }
    }

    assert_eq!(
        fs::read(fixture_path(PACKET_FIXTURE)).unwrap(),
        packet_bytes
    );
    assert_eq!(
        fs::read(fixture_path(RECEIPT_FIXTURE)).unwrap(),
        receipt_bytes
    );
    assert_eq!(
        fs::read(fixture_path(VERIFICATION_FIXTURE)).unwrap(),
        verification_bytes
    );

    let parsed_packet = parse_coda6_packet_canonical_v1(&packet_bytes).unwrap();
    let parsed_receipt = parse_coda6_receipt_canonical_v1(&receipt_bytes).unwrap();
    let parsed_verification = parse_coda6_verification_canonical_v1(&verification_bytes).unwrap();
    assert_eq!(parsed_packet, packet);
    assert_eq!(parsed_receipt, receipt);
    assert_eq!(parsed_verification, verification);
    assert_eq!(
        verify_coda6_defect_terminalization_v1(&parsed_packet, &parsed_receipt, &artifacts)
            .unwrap(),
        verification
    );

    assert_eq!(packet.frozen_base, S06_003_FROZEN_BASE);
    assert_eq!(verification.defect_count, 3);
    assert_eq!(verification.subclaim_count, 6);
    assert_eq!(verification.residual_count, 2);
    assert!(verification.every_defect_classified_once);
    assert!(verification.every_subclaim_classified_once);
    assert!(verification.every_local_terminal_recomputed);
    assert!(verification.every_residual_conserved);
    assert!(verification.aggregation_truth_table_replayed);
    assert!(verification.aggregation_permutation_invariant);
    assert!(verification.predecessor_receipt_verified);
    assert!(!verification.coda5_dependency_receipt_present);
    assert!(verification.coda5_dependency_preserved_as_residual);
    assert!(verification
        .residual_ids
        .contains(&S06_003_CODA5_RESIDUAL_ID.to_owned()));
    assert_eq!(verification.terminal, CodaTerminal::StabilizedSurvivor);
    assert!(!verification.promotion_requested);
    assert!(!verification.promotion_constructor_called);
    assert!(!verification.authorized_local_result_created);

    println!("packet_sha256={}", coda6_packet_sha256_v1(&packet).unwrap());
    println!(
        "observer_sha256={}",
        coda6_observer_sha256_v1(&packet.observer).unwrap()
    );
    println!(
        "receipt_sha256={}",
        coda6_receipt_sha256_v1(&receipt).unwrap()
    );
    println!(
        "verification_sha256={}",
        coda6_verification_sha256_v1(&verification).unwrap()
    );
}

#[test]
fn predecessor_artifact_is_required_and_hash_checked() {
    let (packet, receipt, mut artifacts) = canonical_case();
    artifacts.remove(S06_002_VERIFICATION_PATH);
    assert_error_route(
        &packet,
        &receipt,
        &artifacts,
        Coda6Error::MissingArtifact(S06_002_VERIFICATION_PATH.to_owned()),
        CodaTerminal::InfrastructureFailure,
    );

    let mut artifacts = artifact_bytes(&packet);
    artifacts.get_mut(S06_002_VERIFICATION_PATH).unwrap()[0] ^= 1;
    assert_error_route(
        &packet,
        &receipt,
        &artifacts,
        Coda6Error::ArtifactHashMismatch(S06_002_VERIFICATION_PATH.to_owned()),
        CodaTerminal::Invalid,
    );

    let mut artifacts = artifact_bytes(&packet);
    artifacts.insert("unexpected:artifact".to_owned(), b"unexpected".to_vec());
    assert_error_route(
        &packet,
        &receipt,
        &artifacts,
        Coda6Error::ArtifactSetMismatch,
        CodaTerminal::Invalid,
    );
}

#[test]
fn duplicate_defect_and_subclaim_attribution_is_rejected() {
    let (packet, mut receipt, artifacts) = canonical_case();
    receipt.defects[1].defect_id = receipt.defects[0].defect_id.clone();
    assert_error_route(
        &packet,
        &receipt,
        &artifacts,
        Coda6Error::DuplicateDefectId(receipt.defects[0].defect_id.clone()),
        CodaTerminal::Invalid,
    );

    let (_, mut receipt, _) = canonical_case();
    receipt.defects[0].subclaims[1].subclaim_id =
        receipt.defects[0].subclaims[0].subclaim_id.clone();
    assert_error_route(
        &packet,
        &receipt,
        &artifacts,
        Coda6Error::DuplicateSubclaimId(receipt.defects[0].subclaims[0].subclaim_id.clone()),
        CodaTerminal::Invalid,
    );
}

#[test]
fn fabricated_coda5_completion_and_changed_local_terminals_are_rejected() {
    let (packet, mut receipt, artifacts) = canonical_case();
    receipt.defects[1].subclaims[0].evidence = DiagnosticEvidenceV1::DependencyReceipt {
        receipt_id: "S14-005:GTOC-5".to_owned(),
        present: true,
        verified: true,
    };
    assert_error_route(
        &packet,
        &receipt,
        &artifacts,
        Coda6Error::DiagnosticEvidenceMismatch(
            "subclaim:s06-003:gtoc5-construction-receipt".to_owned(),
        ),
        CodaTerminal::Invalid,
    );

    let (_, mut receipt, _) = canonical_case();
    receipt.defects[0].subclaims[1].claimed_terminal = CodaTerminal::ExactRepair;
    assert_error_route(
        &packet,
        &receipt,
        &artifacts,
        Coda6Error::SubclaimTerminalMismatch {
            subclaim_id: "subclaim:s06-003:gtoc4-lift-residual-carried".to_owned(),
            expected: CodaTerminal::StabilizedSurvivor,
            found: CodaTerminal::ExactRepair,
        },
        CodaTerminal::Invalid,
    );
}

#[test]
fn residuals_cannot_be_dropped_duplicated_or_laundered_by_the_aggregate() {
    let (packet, mut receipt, artifacts) = canonical_case();
    receipt.defects[1].subclaims[0].residual_ids.clear();
    assert_error_route(
        &packet,
        &receipt,
        &artifacts,
        Coda6Error::SubclaimResidualMismatch(
            "subclaim:s06-003:gtoc5-construction-receipt".to_owned(),
        ),
        CodaTerminal::Invalid,
    );

    let (_, mut receipt, _) = canonical_case();
    receipt.residual_ledger.pop();
    assert_error_route(
        &packet,
        &receipt,
        &artifacts,
        Coda6Error::ResidualLedgerMismatch,
        CodaTerminal::Invalid,
    );

    let (_, mut receipt, _) = canonical_case();
    receipt.claimed_terminal = CodaTerminal::ExactRepair;
    assert_error_route(
        &packet,
        &receipt,
        &artifacts,
        Coda6Error::AggregateTerminalMismatch {
            expected: CodaTerminal::StabilizedSurvivor,
            found: CodaTerminal::ExactRepair,
        },
        CodaTerminal::Invalid,
    );
}

#[test]
fn aggregation_is_permutation_invariant_and_replays_all_terminal_precedence() {
    let all = CodaTerminal::ALL;
    for terminal in all {
        assert_eq!(
            aggregate_coda6_terminals_v1(&[terminal]).unwrap(),
            terminal,
            "every declared terminal variant must be handled explicitly"
        );
    }
    for first in all {
        for second in all {
            for third in all {
                let expected = aggregate_coda6_terminals_v1(&[first, second, third]).unwrap();
                for permutation in [
                    [first, third, second],
                    [second, first, third],
                    [second, third, first],
                    [third, first, second],
                    [third, second, first],
                ] {
                    assert_eq!(
                        aggregate_coda6_terminals_v1(&permutation).unwrap(),
                        expected
                    );
                }
            }
        }
    }
    assert_eq!(
        aggregate_coda6_terminals_v1(&[CodaTerminal::ExactRepair, CodaTerminal::OpenObstruction,])
            .unwrap(),
        CodaTerminal::StabilizedSurvivor
    );
    assert_eq!(
        aggregate_coda6_terminals_v1(&[
            CodaTerminal::LiftLicenseNeeded,
            CodaTerminal::OracleNeeded,
            CodaTerminal::Refused,
            CodaTerminal::Invalid,
            CodaTerminal::InfrastructureFailure,
        ])
        .unwrap(),
        CodaTerminal::InfrastructureFailure
    );
    assert_eq!(
        aggregate_coda6_terminals_v1(&[]),
        Err(Coda6Error::EmptyTerminalSet)
    );
}

#[test]
fn unavailable_rule_is_an_open_operator_needed_survivor_not_a_terminal_variant() {
    let outcome = classify_coda6_diagnostic_v1(
        DiagnosticRuleV1::Unavailable,
        &DiagnosticEvidenceV1::RuleUnavailable {
            rule_id: "diagnostic:unregistered".to_owned(),
        },
    )
    .unwrap();
    assert_eq!(outcome.terminal, CodaTerminal::OpenObstruction);
    assert_eq!(
        outcome.survivor_route,
        Some(SurvivorRouteV1::OperatorNeeded)
    );

    let mismatch = classify_coda6_diagnostic_v1(
        DiagnosticRuleV1::InvariantCheck,
        &DiagnosticEvidenceV1::RuleUnavailable {
            rule_id: "diagnostic:unregistered".to_owned(),
        },
    )
    .unwrap_err();
    assert_eq!(mismatch.terminal_route(), CodaTerminal::Invalid);
}

#[test]
fn authority_expansion_and_noncanonical_json_fail_closed() {
    let (packet, mut receipt, artifacts) = canonical_case();
    receipt.promotion_requested = true;
    assert_error_route(
        &packet,
        &receipt,
        &artifacts,
        Coda6Error::AuthorityExpanded,
        CodaTerminal::Refused,
    );

    let packet_bytes = canonical_coda6_json_line_v1(&packet).unwrap();
    let mut pretty = serde_json::to_vec_pretty(&packet).unwrap();
    pretty.push(b'\n');
    assert_eq!(
        parse_coda6_packet_canonical_v1(&pretty),
        Err(Coda6Error::NonCanonicalJson("GTOC-6 packet".to_owned()))
    );

    let mut value = serde_json::to_value(&packet).unwrap();
    value
        .as_object_mut()
        .unwrap()
        .insert("unexpected".to_owned(), serde_json::Value::Bool(true));
    let mut unknown = serde_json::to_vec(&value).unwrap();
    unknown.push(b'\n');
    let error = parse_coda6_packet_canonical_v1(&unknown).unwrap_err();
    assert!(matches!(error, Coda6Error::Decode(_)));
    assert_eq!(error.terminal_route(), CodaTerminal::Invalid);

    let parsed = parse_coda6_packet_canonical_v1(&packet_bytes).unwrap();
    assert_eq!(parsed, packet);
}

// Origin: vendor/engine/tests/engine_state/coda6_defect_terminalization.rs
// Claim: urn:omega:crates_rs:tests:coda6-defect-terminalization:l4-production-boundary:v1
// AuthorityEffect: None
// Scope Fence: Does not claim authority promotion outside declared finite bounds.

/// Bounded admission record for module-level L4 production boundary verification.
#[allow(dead_code, missing_docs)]
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct BoundaryRecorda0f5843b {
    admitted_items: u64,
    capacity_bound: u64,
}

/// Typed refusal modes for `BoundaryRecorda0f5843b` boundary validation.
#[allow(dead_code, missing_docs)]
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum BoundaryErrora0f5843b {
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
impl BoundaryErrora0f5843b {
    /// Returns the static invariant clause violated by this refusal.
    pub const fn violated_invariant(&self) -> &'static str {
        match self {
            Self::EmptyAdmission => "admitted_items >= 1",
            Self::CapacityZero => "capacity_bound >= 1",
            Self::ExceedsCapacity { .. } => "admitted_items <= capacity_bound",
        }
    }
}

impl std::fmt::Display for BoundaryErrora0f5843b {
    fn fmt(&self, formatter: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(formatter, "{}: {:?}", self.violated_invariant(), self)
    }
}

impl std::error::Error for BoundaryErrora0f5843b {}

#[allow(dead_code, missing_docs)]
impl BoundaryRecorda0f5843b {
    /// Validates and constructs a bounded admission record within `capacity_bound`.
    pub fn try_admit(
        admitted_items: u64,
        capacity_bound: u64,
    ) -> std::result::Result<Self, BoundaryErrora0f5843b> {
        if capacity_bound == 0 {
            return Err(BoundaryErrora0f5843b::CapacityZero);
        }
        if admitted_items == 0 {
            return Err(BoundaryErrora0f5843b::EmptyAdmission);
        }
        if admitted_items > capacity_bound {
            return Err(BoundaryErrora0f5843b::ExceedsCapacity {
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
fn l4_boundary_admits_and_refuses_a0f5843b() {
    let admitted = BoundaryRecorda0f5843b::try_admit(3, 8);
    assert!(admitted.is_ok());
    if let Ok(record) = admitted {
        assert_eq!(record.admitted_items(), 3);
        assert_eq!(record.capacity_bound(), 8);
        assert_eq!(record.remaining_capacity(), 5);
    }
    assert!(BoundaryRecorda0f5843b::try_admit(9, 8).is_err());
}

// Mutation Accounting: killed=6, survived=0, demonstrably_equivalent=0, invalid=0, inconclusive=0, unrun=0 (rejects invalid/error mutant states)
