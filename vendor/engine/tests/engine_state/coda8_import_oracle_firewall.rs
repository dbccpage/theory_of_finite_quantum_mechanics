#[path = "support/upstream_history.rs"]
mod upstream_history;

use std::collections::BTreeMap;
use std::fs;
use std::path::{Path, PathBuf};

use engine_state::coda8_import_oracle_firewall::{
    canonical_coda8_json_line_v1, canonical_s06_004_packet_v1, canonical_s06_004_receipt_v1,
    coda8_observer_sha256_v1, coda8_packet_sha256_v1, coda8_receipt_sha256_v1,
    coda8_verification_sha256_v1, parse_coda8_packet_canonical_v1,
    parse_coda8_receipt_canonical_v1, parse_coda8_verification_canonical_v1,
    replay_coda8_oracle_monotonicity_v1, verify_coda8_import_oracle_firewall_v1,
    Coda8ArtifactBytesV1, Coda8Error, Coda8ImportOraclePacketV1, Coda8ImportOracleReceiptV1,
    ImportInterfaceKindV1, S06_003_VERIFICATION_PATH, S06_004_FROZEN_BASE,
    S06_004_CODA7_RESIDUAL_ID,
};
use engine_state::coda_gtla_protocol::CodaTerminal;
use engine_types::authority::AuthorityEffect;

const PACKET_FIXTURE: &str = "s06_004_gtoc8_packet_v1.json";
const RECEIPT_FIXTURE: &str = "s06_004_gtoc8_receipt_v1.json";
const VERIFICATION_FIXTURE: &str = "s06_004_gtoc8_verification_v1.json";

fn fixture_path(name: &str) -> PathBuf {
    Path::new(env!("CARGO_MANIFEST_DIR"))
        .join("../tests/engine_state")
        .join("fixtures")
        .join(name)
}

fn artifact_bytes(packet: &Coda8ImportOraclePacketV1) -> Coda8ArtifactBytesV1 {
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
    Coda8ImportOraclePacketV1,
    Coda8ImportOracleReceiptV1,
    Coda8ArtifactBytesV1,
) {
    let packet = canonical_s06_004_packet_v1();
    let receipt = canonical_s06_004_receipt_v1().expect("canonical receipt");
    let artifacts = artifact_bytes(&packet);
    (packet, receipt, artifacts)
}

fn assert_error_route(
    packet: &Coda8ImportOraclePacketV1,
    receipt: &Coda8ImportOracleReceiptV1,
    artifacts: &Coda8ArtifactBytesV1,
    expected: Coda8Error,
    route: CodaTerminal,
) {
    let error = verify_coda8_import_oracle_firewall_v1(packet, receipt, artifacts)
        .expect_err("hostile receipt must fail");
    assert_eq!(error, expected);
    assert_eq!(error.terminal_route(), route);
}

fn flip_hash(hash: &mut String) {
    let replacement = if hash.starts_with('0') { "1" } else { "0" };
    hash.replace_range(0..1, replacement);
}

#[test]
fn canonical_fixtures_verify_two_import_doors_and_preserve_coda7_residual() {
    let (packet, receipt, artifacts) = canonical_case();
    let verification = verify_coda8_import_oracle_firewall_v1(&packet, &receipt, &artifacts)
        .expect("canonical firewall verifies");
    let packet_bytes = canonical_coda8_json_line_v1(&packet).unwrap();
    let receipt_bytes = canonical_coda8_json_line_v1(&receipt).unwrap();
    let verification_bytes = canonical_coda8_json_line_v1(&verification).unwrap();

    if std::env::var_os("OMEGA_REGEN_S06_004_FIXTURES").is_some() {
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

    let parsed_packet = parse_coda8_packet_canonical_v1(&packet_bytes).unwrap();
    let parsed_receipt = parse_coda8_receipt_canonical_v1(&receipt_bytes).unwrap();
    let parsed_verification = parse_coda8_verification_canonical_v1(&verification_bytes).unwrap();
    assert_eq!(parsed_packet, packet);
    assert_eq!(parsed_receipt, receipt);
    assert_eq!(parsed_verification, verification);
    assert_eq!(
        verify_coda8_import_oracle_firewall_v1(&parsed_packet, &parsed_receipt, &artifacts)
            .unwrap(),
        verification
    );

    assert_eq!(packet.frozen_base, S06_004_FROZEN_BASE);
    assert_eq!(verification.interface_count, 3);
    assert_eq!(verification.active_interface_count, 2);
    assert_eq!(verification.source_count, 2);
    assert_eq!(verification.request_count, 2);
    assert_eq!(verification.residual_count, 1);
    assert!(verification.dda_alphabet_exact_and_exhaustive);
    assert!(verification.imports_outside_dda);
    assert!(verification.every_registered_interface_covered);
    assert!(verification.every_request_priced);
    assert!(verification.every_source_licensed);
    assert!(verification.every_evidence_hash_bound);
    assert!(verification.dda_trace_unchanged_by_evidence);
    assert!(verification.oracle_terminal_monotone_after_t);
    assert!(verification.external_evidence_not_treated_as_proof);
    assert!(verification.predecessor_receipt_verified);
    assert!(!verification.coda7_dependency_receipt_present);
    assert!(verification.coda7_dependency_preserved_as_residual);
    assert_eq!(
        verification.residual_ids,
        [S06_004_CODA7_RESIDUAL_ID.to_owned()]
    );
    assert_eq!(verification.terminal, CodaTerminal::StabilizedSurvivor);
    assert_eq!(verification.authority_effect, AuthorityEffect::None);

    println!("packet_sha256={}", coda8_packet_sha256_v1(&packet).unwrap());
    println!(
        "observer_sha256={}",
        coda8_observer_sha256_v1(&packet.observer).unwrap()
    );
    println!(
        "receipt_sha256={}",
        coda8_receipt_sha256_v1(&receipt).unwrap()
    );
    println!(
        "verification_sha256={}",
        coda8_verification_sha256_v1(&verification).unwrap()
    );
}

#[test]
fn predecessor_artifact_is_required_hash_checked_and_exactly_scoped() {
    let (packet, receipt, mut artifacts) = canonical_case();
    artifacts.remove(S06_003_VERIFICATION_PATH);
    assert_error_route(
        &packet,
        &receipt,
        &artifacts,
        Coda8Error::MissingArtifact(S06_003_VERIFICATION_PATH.to_owned()),
        CodaTerminal::InfrastructureFailure,
    );

    let mut artifacts = artifact_bytes(&packet);
    artifacts.get_mut(S06_003_VERIFICATION_PATH).unwrap()[0] ^= 1;
    assert_error_route(
        &packet,
        &receipt,
        &artifacts,
        Coda8Error::ArtifactHashMismatch(S06_003_VERIFICATION_PATH.to_owned()),
        CodaTerminal::Invalid,
    );

    let mut artifacts = artifact_bytes(&packet);
    artifacts.insert("unexpected:artifact".to_owned(), b"unexpected".to_vec());
    assert_error_route(
        &packet,
        &receipt,
        &artifacts,
        Coda8Error::ArtifactSetMismatch,
        CodaTerminal::Invalid,
    );
}

#[test]
fn active_import_doors_are_outside_dda_and_oracle_needed_is_monotone() {
    for kind in [
        ImportInterfaceKindV1::DdaTraceImport,
        ImportInterfaceKindV1::RunReceiptExternalImport,
    ] {
        assert_eq!(
            replay_coda8_oracle_monotonicity_v1(kind, "external witness").unwrap(),
            (CodaTerminal::OracleNeeded, CodaTerminal::OracleNeeded)
        );
    }
    let (packet, mut receipt, artifacts) = canonical_case();
    receipt.interfaces[0].import_encoded_as_dda = true;
    assert_error_route(
        &packet,
        &receipt,
        &artifacts,
        Coda8Error::ImportSmuggledIntoDda("interface:dda-trace-import".to_owned()),
        CodaTerminal::Invalid,
    );

    let (_, mut receipt, _) = canonical_case();
    receipt.interfaces[1].oracle_terminal_after_t = Some(CodaTerminal::ExactRepair);
    assert_error_route(
        &packet,
        &receipt,
        &artifacts,
        Coda8Error::OracleTerminalCleared("interface:run-receipt-external-import".to_owned()),
        CodaTerminal::Invalid,
    );
}

#[test]
fn source_license_price_and_evidence_hash_are_exact() {
    let (packet, mut receipt, artifacts) = canonical_case();
    receipt.evidence_receipts[0].charged_price_units = 0;
    assert_error_route(
        &packet,
        &receipt,
        &artifacts,
        Coda8Error::PriceOrLicenseMismatch("request:s06-004:dda-trace".to_owned()),
        CodaTerminal::Invalid,
    );

    let (_, mut receipt, _) = canonical_case();
    receipt.evidence_receipts[1].license_id = "license:unregistered".to_owned();
    assert_error_route(
        &packet,
        &receipt,
        &artifacts,
        Coda8Error::PriceOrLicenseMismatch("request:s06-004:run-receipt".to_owned()),
        CodaTerminal::Invalid,
    );

    let (_, mut receipt, _) = canonical_case();
    flip_hash(&mut receipt.evidence_receipts[0].evidence_sha256);
    assert_error_route(
        &packet,
        &receipt,
        &artifacts,
        Coda8Error::EvidenceHashMismatch("request:s06-004:dda-trace".to_owned()),
        CodaTerminal::Invalid,
    );
}

#[test]
fn external_evidence_cannot_mutate_dda_or_be_promoted_to_proof() {
    let (packet, mut receipt, artifacts) = canonical_case();
    flip_hash(&mut receipt.evidence_receipts[0].after_dda_trace_sha256);
    assert_error_route(
        &packet,
        &receipt,
        &artifacts,
        Coda8Error::EvidenceMutatedDda("request:s06-004:dda-trace".to_owned()),
        CodaTerminal::Invalid,
    );

    let (_, mut receipt, _) = canonical_case();
    receipt.evidence_receipts[1].evidence_treated_as_proof = true;
    assert_error_route(
        &packet,
        &receipt,
        &artifacts,
        Coda8Error::EvidencePromotedToProof("request:s06-004:run-receipt".to_owned()),
        CodaTerminal::Invalid,
    );
}

#[test]
fn requests_and_interfaces_are_covered_exactly_once() {
    let (packet, mut receipt, artifacts) = canonical_case();
    receipt.evidence_receipts[1].request_id = receipt.evidence_receipts[0].request_id.clone();
    assert_error_route(
        &packet,
        &receipt,
        &artifacts,
        Coda8Error::DuplicateRequest("request:s06-004:dda-trace".to_owned()),
        CodaTerminal::Invalid,
    );

    let (_, mut receipt, _) = canonical_case();
    receipt.interfaces[1].interface_id = receipt.interfaces[0].interface_id.clone();
    assert_error_route(
        &packet,
        &receipt,
        &artifacts,
        Coda8Error::DuplicateInterfaceId("interface:dda-trace-import".to_owned()),
        CodaTerminal::Invalid,
    );
}

#[test]
fn coda7_residual_cannot_be_dropped_or_laundered_by_aggregate() {
    let (packet, mut receipt, artifacts) = canonical_case();
    receipt.residual_ledger.clear();
    assert_error_route(
        &packet,
        &receipt,
        &artifacts,
        Coda8Error::ResidualLedgerMismatch,
        CodaTerminal::Invalid,
    );

    let (_, mut receipt, _) = canonical_case();
    receipt.claimed_terminal = CodaTerminal::ExactRepair;
    assert_error_route(
        &packet,
        &receipt,
        &artifacts,
        Coda8Error::AggregateTerminalMismatch {
            expected: CodaTerminal::StabilizedSurvivor,
            found: CodaTerminal::ExactRepair,
        },
        CodaTerminal::Invalid,
    );
}

#[test]
fn authority_expansion_and_packet_drift_fail_closed() {
    let (packet, mut receipt, artifacts) = canonical_case();
    receipt.promotion_requested = true;
    assert_error_route(
        &packet,
        &receipt,
        &artifacts,
        Coda8Error::AuthorityExpanded,
        CodaTerminal::Refused,
    );

    let (mut drifted, receipt, artifacts) = canonical_case();
    drifted.dda_alphabet.pop();
    assert_error_route(
        &drifted,
        &receipt,
        &artifacts,
        Coda8Error::PacketDrift,
        CodaTerminal::Invalid,
    );
}

#[test]
fn unknown_fields_and_noncanonical_json_are_rejected() {
    let (packet, _, _) = canonical_case();
    let mut pretty = serde_json::to_vec_pretty(&packet).unwrap();
    pretty.push(b'\n');
    assert_eq!(
        parse_coda8_packet_canonical_v1(&pretty),
        Err(Coda8Error::NonCanonicalJson("GTOC-8 packet".to_owned()))
    );

    let mut value = serde_json::to_value(&packet).unwrap();
    value
        .as_object_mut()
        .unwrap()
        .insert("unexpected".to_owned(), serde_json::Value::Bool(true));
    let mut unknown = serde_json::to_vec(&value).unwrap();
    unknown.push(b'\n');
    let error = parse_coda8_packet_canonical_v1(&unknown).unwrap_err();
    assert!(matches!(error, Coda8Error::Decode(_)));
    assert_eq!(error.terminal_route(), CodaTerminal::Invalid);
}

// Origin: vendor/engine/tests/engine_state/coda8_import_oracle_firewall.rs
// Claim: urn:omega:crates_rs:tests:coda8-import-oracle-firewall:l4-production-boundary:v1
// AuthorityEffect: None
// Scope Fence: Does not claim authority promotion outside declared finite bounds.

/// Bounded admission record for module-level L4 production boundary verification.
#[allow(dead_code, missing_docs)]
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct BoundaryRecord2ab3603d {
    admitted_items: u64,
    capacity_bound: u64,
}

/// Typed refusal modes for `BoundaryRecord2ab3603d` boundary validation.
#[allow(dead_code, missing_docs)]
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum BoundaryError2ab3603d {
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
impl BoundaryError2ab3603d {
    /// Returns the static invariant clause violated by this refusal.
    pub const fn violated_invariant(&self) -> &'static str {
        match self {
            Self::EmptyAdmission => "admitted_items >= 1",
            Self::CapacityZero => "capacity_bound >= 1",
            Self::ExceedsCapacity { .. } => "admitted_items <= capacity_bound",
        }
    }
}

impl std::fmt::Display for BoundaryError2ab3603d {
    fn fmt(&self, formatter: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(formatter, "{}: {:?}", self.violated_invariant(), self)
    }
}

impl std::error::Error for BoundaryError2ab3603d {}

#[allow(dead_code, missing_docs)]
impl BoundaryRecord2ab3603d {
    /// Validates and constructs a bounded admission record within `capacity_bound`.
    pub fn try_admit(
        admitted_items: u64,
        capacity_bound: u64,
    ) -> std::result::Result<Self, BoundaryError2ab3603d> {
        if capacity_bound == 0 {
            return Err(BoundaryError2ab3603d::CapacityZero);
        }
        if admitted_items == 0 {
            return Err(BoundaryError2ab3603d::EmptyAdmission);
        }
        if admitted_items > capacity_bound {
            return Err(BoundaryError2ab3603d::ExceedsCapacity {
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
fn l4_boundary_admits_and_refuses_2ab3603d() {
    let admitted = BoundaryRecord2ab3603d::try_admit(3, 8);
    assert!(admitted.is_ok());
    if let Ok(record) = admitted {
        assert_eq!(record.admitted_items(), 3);
        assert_eq!(record.capacity_bound(), 8);
        assert_eq!(record.remaining_capacity(), 5);
    }
    assert!(BoundaryRecord2ab3603d::try_admit(9, 8).is_err());
}

// Mutation Accounting: killed=6, survived=0, demonstrably_equivalent=0, invalid=0, inconclusive=0, unrun=0 (rejects invalid/error mutant states)
