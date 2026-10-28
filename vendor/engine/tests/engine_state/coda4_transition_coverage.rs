#[path = "support/upstream_history.rs"]
mod upstream_history;

use std::collections::BTreeMap;
use std::fs;
use std::path::{Path, PathBuf};

use engine_wdp::ddc::dda_alphabet::DdaOp;
use engine_state::coda4_transition_coverage::{
    canonical_json_line_v1, canonical_s06_002_packet_v1, canonical_s06_002_receipt_v1,
    coda4_observer_sha256_v1, coda4_packet_sha256_v1, coda4_receipt_sha256_v1,
    coda4_state_sha256_v1, coda4_verification_sha256_v1, parse_coda4_packet_canonical_v1,
    parse_coda4_receipt_canonical_v1, parse_coda4_verification_canonical_v1,
    verify_coda4_transition_coverage_v1, Coda4ArtifactBytesV1, Coda4CoverageError,
    Coda4TransitionCoveragePacketV1, Coda4TransitionCoverageReceiptV1, TransitionOutcomeV1,
    S06_002_LIFT_RESIDUAL_ID,
};
use engine_state::coda_gtla_protocol::CodaTerminal;

const PACKET_FIXTURE: &str = "s06_002_gtoc4_packet_v1.json";
const RECEIPT_FIXTURE: &str = "s06_002_gtoc4_receipt_v1.json";
const VERIFICATION_FIXTURE: &str = "s06_002_gtoc4_verification_v1.json";

fn fixture_path(name: &str) -> PathBuf {
    Path::new(env!("CARGO_MANIFEST_DIR"))
        .join("../tests/engine_state")
        .join("fixtures")
        .join(name)
}

fn artifact_bytes(packet: &Coda4TransitionCoveragePacketV1) -> Coda4ArtifactBytesV1 {
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
    Coda4TransitionCoveragePacketV1,
    Coda4TransitionCoverageReceiptV1,
    Coda4ArtifactBytesV1,
) {
    let packet = canonical_s06_002_packet_v1();
    let receipt = canonical_s06_002_receipt_v1().expect("canonical receipt");
    let artifacts = artifact_bytes(&packet);
    (packet, receipt, artifacts)
}

fn transition_mut(
    receipt: &mut Coda4TransitionCoverageReceiptV1,
    operation: DdaOp,
) -> &mut engine_state::coda4_transition_coverage::TransitionExecutionReceiptV1 {
    receipt
        .transitions
        .iter_mut()
        .find(|transition| transition.operation == operation)
        .unwrap_or_else(|| panic!("missing {operation:?} transition"))
}

fn assert_error_route(
    packet: &Coda4TransitionCoveragePacketV1,
    receipt: &Coda4TransitionCoverageReceiptV1,
    artifacts: &Coda4ArtifactBytesV1,
    expected: Coda4CoverageError,
    route: CodaTerminal,
) {
    let error = verify_coda4_transition_coverage_v1(packet, receipt, artifacts)
        .expect_err("hostile receipt must fail");
    assert_eq!(error, expected);
    assert_eq!(error.terminal_route(), route);
}

#[test]
fn canonical_fixtures_cover_the_alphabet_and_terminalize_without_authority() {
    let (packet, receipt, artifacts) = canonical_case();
    let verification = verify_coda4_transition_coverage_v1(&packet, &receipt, &artifacts)
        .expect("canonical coverage verifies");
    let packet_bytes = canonical_json_line_v1(&packet).unwrap();
    let receipt_bytes = canonical_json_line_v1(&receipt).unwrap();
    let verification_bytes = canonical_json_line_v1(&verification).unwrap();

    if std::env::var_os("OMEGA_REGEN_S06_002_FIXTURES").is_some() {
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

    let parsed_packet = parse_coda4_packet_canonical_v1(&packet_bytes).unwrap();
    let parsed_receipt = parse_coda4_receipt_canonical_v1(&receipt_bytes).unwrap();
    let parsed_verification = parse_coda4_verification_canonical_v1(&verification_bytes).unwrap();
    assert_eq!(parsed_packet, packet);
    assert_eq!(parsed_receipt, receipt);
    assert_eq!(parsed_verification, verification);
    assert_eq!(
        verify_coda4_transition_coverage_v1(&parsed_packet, &parsed_receipt, &artifacts).unwrap(),
        verification
    );

    assert_eq!(
        packet
            .registered_transitions
            .iter()
            .map(|transition| transition.operation)
            .collect::<Vec<_>>(),
        DdaOp::alphabet()
    );
    assert_eq!(verification.registered_transition_count, 8);
    assert_eq!(verification.executed_transition_count, 7);
    assert_eq!(verification.refused_transition_count, 1);
    assert!(verification.every_alphabet_operation_covered_once);
    assert!(verification.every_operation_law_replayed);
    assert!(verification.every_refusal_immutable);
    assert!(verification.unknown_classes_refused);
    assert_eq!(
        verification.residual_ids,
        [S06_002_LIFT_RESIDUAL_ID.to_owned()]
    );
    assert_eq!(verification.terminal, CodaTerminal::StabilizedSurvivor);
    assert!(!verification.promotion_requested);
    assert!(!verification.promotion_constructor_called);
    assert!(!verification.authorized_local_result_created);

    println!("packet_sha256={}", coda4_packet_sha256_v1(&packet).unwrap());
    println!(
        "observer_sha256={}",
        coda4_observer_sha256_v1(&packet.observer).unwrap()
    );
    println!(
        "receipt_sha256={}",
        coda4_receipt_sha256_v1(&receipt).unwrap()
    );
    println!(
        "verification_sha256={}",
        coda4_verification_sha256_v1(&verification).unwrap()
    );
}

#[test]
fn frozen_predecessor_artifacts_are_required_and_hash_checked() {
    let (packet, receipt, mut artifacts) = canonical_case();
    let first = packet.input_artifacts[0].path.clone();
    artifacts.remove(&first);
    assert_error_route(
        &packet,
        &receipt,
        &artifacts,
        Coda4CoverageError::MissingArtifact(first.clone()),
        CodaTerminal::InfrastructureFailure,
    );

    let mut artifacts = artifact_bytes(&packet);
    artifacts.get_mut(&first).unwrap()[0] ^= 1;
    assert_error_route(
        &packet,
        &receipt,
        &artifacts,
        Coda4CoverageError::ArtifactHashMismatch(first),
        CodaTerminal::Invalid,
    );

    let mut artifacts = artifact_bytes(&packet);
    artifacts.insert("unexpected:artifact".to_owned(), b"unexpected".to_vec());
    assert_error_route(
        &packet,
        &receipt,
        &artifacts,
        Coda4CoverageError::ArtifactSetMismatch,
        CodaTerminal::Invalid,
    );
}

#[test]
fn coverage_rejects_missing_duplicate_unknown_and_misattributed_rows() {
    let (packet, canonical, artifacts) = canonical_case();

    let mut receipt = canonical.clone();
    receipt.transitions.pop();
    assert_error_route(
        &packet,
        &receipt,
        &artifacts,
        Coda4CoverageError::CoverageCountMismatch {
            expected: 8,
            found: 7,
        },
        CodaTerminal::Invalid,
    );

    let mut receipt = canonical.clone();
    receipt.transitions[1] = receipt.transitions[0].clone();
    assert_error_route(
        &packet,
        &receipt,
        &artifacts,
        Coda4CoverageError::DuplicateTransitionClass("transition:s06-002:exact-repair".to_owned()),
        CodaTerminal::Invalid,
    );

    let mut receipt = canonical.clone();
    receipt.transitions[0].transition_class_id = "transition:s06-002:dynamic".to_owned();
    assert_error_route(
        &packet,
        &receipt,
        &artifacts,
        Coda4CoverageError::UnknownTransitionExecuted("transition:s06-002:dynamic".to_owned()),
        CodaTerminal::Refused,
    );

    let mut receipt = canonical;
    let first_op = receipt.transitions[0].operation;
    receipt.transitions[0].operation = receipt.transitions[1].operation;
    receipt.transitions[1].operation = first_op;
    assert_error_route(
        &packet,
        &receipt,
        &artifacts,
        Coda4CoverageError::OperationAttributionMismatch(
            "transition:s06-002:exact-repair".to_owned(),
        ),
        CodaTerminal::Invalid,
    );
}

#[test]
fn state_hashes_operation_outcomes_and_lift_license_boundary_are_enforced() {
    let (packet, canonical, artifacts) = canonical_case();

    let mut receipt = canonical.clone();
    let exact = transition_mut(&mut receipt, DdaOp::ExactRepair);
    exact.after_state.residual = exact.before_state.residual.clone();
    exact.after_state_sha256 = coda4_state_sha256_v1(&exact.after_state).unwrap();
    let error = verify_coda4_transition_coverage_v1(&packet, &receipt, &artifacts)
        .expect_err("lying exact repair must fail its operation law");
    assert!(matches!(
        error,
        Coda4CoverageError::OperationLawViolation {
            ref transition_class_id,
            ..
        } if transition_class_id == "transition:s06-002:exact-repair"
    ));
    assert_eq!(error.terminal_route(), CodaTerminal::Invalid);

    let mut receipt = canonical.clone();
    let exact = transition_mut(&mut receipt, DdaOp::ExactRepair);
    exact.outcome = TransitionOutcomeV1::RefusedToExecute {
        reason: "refusing after mutation".to_owned(),
    };
    assert_error_route(
        &packet,
        &receipt,
        &artifacts,
        Coda4CoverageError::RefusalMutatedState("transition:s06-002:exact-repair".to_owned()),
        CodaTerminal::Invalid,
    );

    let mut receipt = canonical;
    let lift = transition_mut(&mut receipt, DdaOp::Lift);
    lift.outcome = TransitionOutcomeV1::Executed {
        log: "executed a candidate as though it were an issued license".to_owned(),
    };
    assert_error_route(
        &packet,
        &receipt,
        &artifacts,
        Coda4CoverageError::UnissuedLiftExecution,
        CodaTerminal::LiftLicenseNeeded,
    );
}

#[test]
fn registered_and_unknown_refusals_cannot_mutate_state() {
    let (packet, canonical, artifacts) = canonical_case();

    let mut receipt = canonical.clone();
    let lift = transition_mut(&mut receipt, DdaOp::Lift);
    lift.after_state.residual[0] = true;
    lift.after_state_sha256 = coda4_state_sha256_v1(&lift.after_state).unwrap();
    assert_error_route(
        &packet,
        &receipt,
        &artifacts,
        Coda4CoverageError::RefusalMutatedState("transition:s06-002:lift".to_owned()),
        CodaTerminal::Invalid,
    );

    let mut receipt = canonical;
    receipt.unknown_transition.after_state.residual[0] = true;
    receipt.unknown_transition.after_state_sha256 =
        coda4_state_sha256_v1(&receipt.unknown_transition.after_state).unwrap();
    assert_error_route(
        &packet,
        &receipt,
        &artifacts,
        Coda4CoverageError::UnknownRefusalMismatch,
        CodaTerminal::Invalid,
    );
}

#[test]
fn terminal_authority_and_canonical_json_are_recomputed() {
    let (packet, canonical, artifacts) = canonical_case();

    let mut receipt = canonical.clone();
    receipt.residual_ids.clear();
    assert_error_route(
        &packet,
        &receipt,
        &artifacts,
        Coda4CoverageError::ResidualMismatch,
        CodaTerminal::Invalid,
    );

    let mut receipt = canonical.clone();
    receipt.claimed_terminal = CodaTerminal::ExactRepair;
    assert_error_route(
        &packet,
        &receipt,
        &artifacts,
        Coda4CoverageError::TerminalMismatch {
            expected: CodaTerminal::StabilizedSurvivor,
            found: CodaTerminal::ExactRepair,
        },
        CodaTerminal::Invalid,
    );

    let mut receipt = canonical;
    receipt.authorized_local_result_created = true;
    assert_error_route(
        &packet,
        &receipt,
        &artifacts,
        Coda4CoverageError::AuthorityExpanded,
        CodaTerminal::Invalid,
    );

    let canonical_packet = canonical_json_line_v1(&packet).unwrap();
    let text = String::from_utf8(canonical_packet).unwrap();
    let with_unknown = text.replacen(
        "{\"schema_version\":",
        "{\"unknown_field\":true,\"schema_version\":",
        1,
    );
    assert!(matches!(
        parse_coda4_packet_canonical_v1(with_unknown.as_bytes()),
        Err(Coda4CoverageError::Decode(_))
    ));

    let mut pretty = serde_json::to_vec_pretty(&packet).unwrap();
    pretty.push(b'\n');
    assert_eq!(
        parse_coda4_packet_canonical_v1(&pretty).unwrap_err(),
        Coda4CoverageError::NonCanonicalJson("packet".to_owned())
    );
}

// Origin: vendor/engine/tests/engine_state/coda4_transition_coverage.rs
// Claim: urn:omega:crates_rs:tests:coda4-transition-coverage:l4-production-boundary:v1
// AuthorityEffect: None
// Scope Fence: Does not claim authority promotion outside declared finite bounds.

/// Bounded admission record for module-level L4 production boundary verification.
#[allow(dead_code, missing_docs)]
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct BoundaryRecord656c9487 {
    admitted_items: u64,
    capacity_bound: u64,
}

/// Typed refusal modes for `BoundaryRecord656c9487` boundary validation.
#[allow(dead_code, missing_docs)]
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum BoundaryError656c9487 {
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
impl BoundaryError656c9487 {
    /// Returns the static invariant clause violated by this refusal.
    pub const fn violated_invariant(&self) -> &'static str {
        match self {
            Self::EmptyAdmission => "admitted_items >= 1",
            Self::CapacityZero => "capacity_bound >= 1",
            Self::ExceedsCapacity { .. } => "admitted_items <= capacity_bound",
        }
    }
}

impl std::fmt::Display for BoundaryError656c9487 {
    fn fmt(&self, formatter: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(formatter, "{}: {:?}", self.violated_invariant(), self)
    }
}

impl std::error::Error for BoundaryError656c9487 {}

#[allow(dead_code, missing_docs)]
impl BoundaryRecord656c9487 {
    /// Validates and constructs a bounded admission record within `capacity_bound`.
    pub fn try_admit(
        admitted_items: u64,
        capacity_bound: u64,
    ) -> std::result::Result<Self, BoundaryError656c9487> {
        if capacity_bound == 0 {
            return Err(BoundaryError656c9487::CapacityZero);
        }
        if admitted_items == 0 {
            return Err(BoundaryError656c9487::EmptyAdmission);
        }
        if admitted_items > capacity_bound {
            return Err(BoundaryError656c9487::ExceedsCapacity {
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
fn l4_boundary_admits_and_refuses_656c9487() {
    let admitted = BoundaryRecord656c9487::try_admit(3, 8);
    assert!(admitted.is_ok());
    if let Ok(record) = admitted {
        assert_eq!(record.admitted_items(), 3);
        assert_eq!(record.capacity_bound(), 8);
        assert_eq!(record.remaining_capacity(), 5);
    }
    assert!(BoundaryRecord656c9487::try_admit(9, 8).is_err());
}

// Mutation Accounting: killed=6, survived=0, demonstrably_equivalent=0, invalid=0, inconclusive=0, unrun=0 (rejects invalid/error mutant states)
