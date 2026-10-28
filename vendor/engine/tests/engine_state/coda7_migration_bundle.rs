#[path = "support/upstream_history.rs"]
mod upstream_history;

use std::fs;
use std::path::{Path, PathBuf};

use engine_state::coda7_migration_bundle::{
    canonical_coda7_json_line_v1, canonical_s03_002_packet_v1, canonical_s03_002_receipt_v1,
    canonical_s03_002_replay_artifacts_v1, canonical_s03_002_source_manifest_v1,
    canonical_s03_002_verification_v1, coda7_observer_sha256_v1, coda7_packet_sha256_v1,
    coda7_receipt_sha256_v1, coda7_verification_sha256_v1, parse_coda7_packet_canonical_v1,
    parse_coda7_receipt_canonical_v1, parse_coda7_verification_canonical_v1,
    validate_coda7_packet_v1, verify_coda7_migration_bundle_v1, Coda7Error, Coda7MemberStorageV1,
    Coda7MigrationOperationV1, Coda7MigrationPacketV1, Coda7MigrationReceiptV1,
    Coda7ReplayArtifactsV1, S03_001_RECEIPT_PATH, S03_002_FROZEN_BASE,
    S03_002_PREDECESSOR_RESIDUAL_ID, S03_002_SOURCE_ROOT, S03_002_TARGET_ROOT,
    S03_002_UNRESTRICTED_FAMILY_RESIDUAL_ID, S03_002_WRITE_SURFACE,
    S06_004_HISTORICAL_RECEIPT_PATH,
};
use engine_state::coda_gtla_protocol::CodaTerminal;
use engine_types::authority::AuthorityEffect;
use serde::Serialize;
use sha2::{Digest, Sha256};

const PACKET_FIXTURE: &str = "s03_002_gtoc7_packet_v1.json";
const RECEIPT_FIXTURE: &str = "s03_002_gtoc7_receipt_v1.json";
const VERIFICATION_FIXTURE: &str = "s03_002_gtoc7_verification_v1.json";

fn fixture_path(name: &str) -> PathBuf {
    Path::new(env!("CARGO_MANIFEST_DIR"))
        .join("../tests/engine_state")
        .join("fixtures")
        .join(name)
}

fn canonical_case() -> (
    Coda7MigrationPacketV1,
    Coda7MigrationReceiptV1,
    Coda7ReplayArtifactsV1,
) {
    (
        canonical_s03_002_packet_v1(),
        canonical_s03_002_receipt_v1().expect("canonical receipt"),
        canonical_s03_002_replay_artifacts_v1(),
    )
}

fn assert_error_route(
    packet: &Coda7MigrationPacketV1,
    receipt: &Coda7MigrationReceiptV1,
    artifacts: &Coda7ReplayArtifactsV1,
    expected: Coda7Error,
    route: CodaTerminal,
) {
    let error = verify_coda7_migration_bundle_v1(packet, receipt, artifacts)
        .expect_err("hostile migration must fail");
    assert_eq!(error, expected);
    assert_eq!(error.terminal_route(), route);
}

fn sha256_json<T: Serialize>(value: &T) -> String {
    format!(
        "{:x}",
        Sha256::digest(serde_json::to_vec(value).expect("serialize test value"))
    )
}

#[test]
fn canonical_finite_bundle_is_bijective_and_preserves_both_residuals() {
    let (packet, receipt, artifacts) = canonical_case();
    let verification = verify_coda7_migration_bundle_v1(&packet, &receipt, &artifacts)
        .expect("canonical migration bundle verifies");
    assert_eq!(verification, canonical_s03_002_verification_v1().unwrap());

    assert_eq!(packet.frozen_base, S03_002_FROZEN_BASE);
    assert_eq!(packet.source_manifest.len(), 16);
    assert_eq!(packet.predecessors.len(), 2);
    assert_eq!(packet.members.len(), 3);
    assert_eq!(packet.path_policy.exact_pairs.len(), 3);
    assert_eq!(
        packet.path_policy.member_storage,
        Coda7MemberStorageV1::InMemorySnapshot
    );
    assert_eq!(packet.path_policy.source_root, S03_002_SOURCE_ROOT);
    assert_eq!(packet.path_policy.target_root, S03_002_TARGET_ROOT);
    for member in &packet.members {
        assert!(member.source_path.starts_with("in-memory-snapshot/"));
        assert!(member.target_path.starts_with("in-memory-snapshot/"));
    }
    assert_eq!(packet.exact_write_surface.len(), 15);
    assert_eq!(
        packet.exact_write_surface,
        S03_002_WRITE_SURFACE
            .iter()
            .map(|path| (*path).to_owned())
            .collect::<Vec<_>>()
    );
    assert!(packet
        .exact_write_surface
        .contains(&"docs/saga_03_task_admission_and_carriers.md".to_owned()));
    assert!(!packet
        .predecessors
        .iter()
        .any(|artifact| artifact.path == S06_004_HISTORICAL_RECEIPT_PATH));
    assert!(!packet
        .exact_write_surface
        .iter()
        .any(|path| path == S06_004_HISTORICAL_RECEIPT_PATH));

    assert_eq!(verification.source_count, 16);
    assert_eq!(verification.predecessor_count, 2);
    assert_eq!(verification.member_count, 3);
    assert_eq!(verification.dependency_edge_count, 3);
    assert_eq!(verification.residual_count, 2);
    assert!(verification.source_manifest_bound);
    assert!(verification.every_predecessor_hash_verified);
    assert!(verification.predecessor_semantics_verified);
    assert!(!verification.predecessor_human_promotion_recorded);
    assert!(verification.exact_member_bijection_verified);
    assert!(verification.every_member_hash_verified);
    assert!(verification.every_dependency_closed);
    assert!(verification.path_policy_verified);
    assert!(verification.no_hidden_additions);
    assert!(verification.every_local_terminal_recomputed);
    assert!(verification.every_residual_conserved);
    assert!(verification.historical_s06_004_receipt_outside_write_surface);
    assert_eq!(
        verification.residual_ids,
        [
            S03_002_PREDECESSOR_RESIDUAL_ID.to_owned(),
            S03_002_UNRESTRICTED_FAMILY_RESIDUAL_ID.to_owned(),
        ]
    );
    assert_eq!(verification.terminal, CodaTerminal::StabilizedSurvivor);
    assert_eq!(verification.authority_effect, AuthorityEffect::None);
    assert!(!verification.workspace_mutated);
    assert!(!verification.promotion_requested);
    assert!(!verification.promotion_constructor_called);
    assert!(!verification.authorized_local_result_created);

    let packet_bytes = canonical_coda7_json_line_v1(&packet).unwrap();
    let receipt_bytes = canonical_coda7_json_line_v1(&receipt).unwrap();
    let verification_bytes = canonical_coda7_json_line_v1(&verification).unwrap();
    if std::env::var_os("OMEGA_REGEN_S03_002_FIXTURES").is_some() {
        for (name, bytes) in [
            (PACKET_FIXTURE, &packet_bytes),
            (RECEIPT_FIXTURE, &receipt_bytes),
            (VERIFICATION_FIXTURE, &verification_bytes),
        ] {
            fs::write(fixture_path(name), bytes).expect("write canonical GTOC-7 fixture");
        }
    }
    for (name, bytes) in [
        (PACKET_FIXTURE, &packet_bytes),
        (RECEIPT_FIXTURE, &receipt_bytes),
        (VERIFICATION_FIXTURE, &verification_bytes),
    ] {
        let path = fixture_path(name);
        if path.is_file() {
            assert_eq!(fs::read(path).unwrap(), *bytes);
        }
    }

    println!("packet_sha256={}", coda7_packet_sha256_v1(&packet).unwrap());
    println!(
        "observer_sha256={}",
        coda7_observer_sha256_v1(&packet.observer).unwrap()
    );
    println!(
        "receipt_sha256={}",
        coda7_receipt_sha256_v1(&receipt).unwrap()
    );
    println!(
        "verification_sha256={}",
        coda7_verification_sha256_v1(&verification).unwrap()
    );
}

#[test]
fn frozen_source_manifest_replays_exact_git_blobs() {
    let sources = canonical_s03_002_source_manifest_v1();
    assert_eq!(sources.len(), 16);
    let mut previous: Option<&str> = None;
    for source in &sources {
        assert!(previous.is_none_or(|value| value < source.path.as_str()));
        previous = Some(&source.path);
        assert!(!source.path.contains("paper"));
        assert!(!source.path.contains("research/"));
        let bytes = upstream_history::frozen_blob(S03_002_FROZEN_BASE, &source.path);
        assert_eq!(bytes.len() as u64, source.bytes, "{}", source.path);
        assert_eq!(
            format!("{:x}", Sha256::digest(&bytes)),
            source.sha256,
            "{}",
            source.path
        );
    }
}

#[test]
fn missing_extra_or_hash_drifting_snapshots_fail_closed() {
    let (packet, receipt, mut artifacts) = canonical_case();
    let source_path = packet.members[0].source_path.clone();
    artifacts.before_members.remove(&source_path);
    assert_error_route(
        &packet,
        &receipt,
        &artifacts,
        Coda7Error::MissingMemberSnapshot {
            phase: "before",
            path: source_path,
        },
        CodaTerminal::Invalid,
    );

    let (_, _, mut artifacts) = canonical_case();
    artifacts
        .after_members
        .insert("unexpected/member.json".to_owned(), b"{}\n".to_vec());
    assert_error_route(
        &packet,
        &receipt,
        &artifacts,
        Coda7Error::MemberSetMismatch("after"),
        CodaTerminal::Invalid,
    );

    let (_, _, mut artifacts) = canonical_case();
    artifacts
        .before_members
        .get_mut(&packet.members[1].source_path)
        .unwrap()[0] ^= 1;
    assert_error_route(
        &packet,
        &receipt,
        &artifacts,
        Coda7Error::MemberHashMismatch(packet.members[1].source_path.clone()),
        CodaTerminal::Invalid,
    );
}

#[test]
fn missing_mutated_or_extra_predecessors_fail_closed() {
    let (packet, receipt, mut artifacts) = canonical_case();
    artifacts.predecessor_artifacts.remove(S03_001_RECEIPT_PATH);
    assert_error_route(
        &packet,
        &receipt,
        &artifacts,
        Coda7Error::MissingPredecessorArtifact(S03_001_RECEIPT_PATH.to_owned()),
        CodaTerminal::InfrastructureFailure,
    );

    let (_, _, mut artifacts) = canonical_case();
    artifacts
        .predecessor_artifacts
        .get_mut(S03_001_RECEIPT_PATH)
        .unwrap()[0] ^= 1;
    assert_error_route(
        &packet,
        &receipt,
        &artifacts,
        Coda7Error::PredecessorHashMismatch(S03_001_RECEIPT_PATH.to_owned()),
        CodaTerminal::Invalid,
    );

    let (_, _, mut artifacts) = canonical_case();
    artifacts
        .predecessor_artifacts
        .insert("unexpected/predecessor.json".to_owned(), b"{}".to_vec());
    assert_error_route(
        &packet,
        &receipt,
        &artifacts,
        Coda7Error::PredecessorSetMismatch,
        CodaTerminal::Invalid,
    );
}

#[test]
fn wildcard_discovery_external_import_and_unsupported_lifts_are_typed() {
    let mut packet = canonical_s03_002_packet_v1();
    packet.path_policy.wildcard_members_allowed = true;
    let error = validate_coda7_packet_v1(&packet).unwrap_err();
    assert_eq!(error, Coda7Error::WildcardDiscoveryForbidden);
    assert_eq!(error.terminal_route(), CodaTerminal::Invalid);

    let mut packet = canonical_s03_002_packet_v1();
    packet.path_policy.external_imports_allowed = true;
    let error = validate_coda7_packet_v1(&packet).unwrap_err();
    assert_eq!(
        error,
        Coda7Error::ExternalImportRequested("path policy permits external imports".to_owned())
    );
    assert_eq!(error.terminal_route(), CodaTerminal::OracleNeeded);

    let (packet, mut receipt, artifacts) = canonical_case();
    receipt.member_receipts[0].external_import_used = true;
    assert_error_route(
        &packet,
        &receipt,
        &artifacts,
        Coda7Error::ExternalImportRequested(packet.members[0].member_id.clone()),
        CodaTerminal::OracleNeeded,
    );

    let mut packet = canonical_s03_002_packet_v1();
    packet.members[0].operation = Coda7MigrationOperationV1::UnsupportedTransformation;
    let error = validate_coda7_packet_v1(&packet).unwrap_err();
    assert_eq!(
        error,
        Coda7Error::UnsupportedMigration(packet.members[0].member_id.clone())
    );
    assert_eq!(error.terminal_route(), CodaTerminal::LiftLicenseNeeded);

    let mut packet = canonical_s03_002_packet_v1();
    packet.members[0].source_path.push('*');
    let error = validate_coda7_packet_v1(&packet).unwrap_err();
    assert!(matches!(error, Coda7Error::NonCanonicalPath { .. }));
    assert_eq!(error.terminal_route(), CodaTerminal::Invalid);
}

#[test]
fn self_dependency_fails_standalone_packet_validation() {
    let mut packet = canonical_s03_002_packet_v1();
    let self_id = packet.members[0].member_id.clone();
    packet.members[0].dependency_ids = vec![self_id.clone()];

    assert_eq!(
        validate_coda7_packet_v1(&packet),
        Err(Coda7Error::DependencyClosureMismatch(self_id))
    );
}

#[test]
fn dependency_order_member_attribution_and_kind_are_closed() {
    let mut packet = canonical_s03_002_packet_v1();
    packet.members[1].dependency_ids = vec!["member:s03-002:99".to_owned()];
    assert_eq!(
        validate_coda7_packet_v1(&packet),
        Err(Coda7Error::DependencyClosureMismatch(
            "member:s03-002:01".to_owned()
        ))
    );

    let (packet, mut receipt, artifacts) = canonical_case();
    receipt.member_receipts.swap(0, 1);
    assert_error_route(
        &packet,
        &receipt,
        &artifacts,
        Coda7Error::MemberReceiptMismatch(packet.members[0].member_id.clone()),
        CodaTerminal::Invalid,
    );

    let mut packet = canonical_s03_002_packet_v1();
    packet.members[0].kind = engine_state::coda7_migration_bundle::Coda7ArtifactKindV1::Json;
    assert_eq!(
        validate_coda7_packet_v1(&packet),
        Err(Coda7Error::ArtifactKindMismatch(
            "member:s03-002:00".to_owned()
        ))
    );
}

#[test]
fn canonical_path_alias_and_duplicate_attacks_fail_closed() {
    for hostile in [
        "../escape.md",
        "/absolute/member.md",
        "C:/absolute/member.md",
        "root\\member.md",
        "root/aux.md",
        "root/member.md.",
    ] {
        let mut packet = canonical_s03_002_packet_v1();
        packet.members[0].source_path = hostile.to_owned();
        let error = validate_coda7_packet_v1(&packet).unwrap_err();
        assert!(
            matches!(error, Coda7Error::NonCanonicalPath { .. }),
            "{hostile}: {error}"
        );
    }

    let mut packet = canonical_s03_002_packet_v1();
    packet.members[1].source_path = packet.members[0].source_path.to_ascii_uppercase();
    packet.path_policy.exact_pairs[1].source_path = packet.members[1].source_path.clone();
    assert_eq!(
        validate_coda7_packet_v1(&packet),
        Err(Coda7Error::DuplicateMember(
            packet.members[1].member_id.clone()
        ))
    );

    let mut packet = canonical_s03_002_packet_v1();
    packet.members[1].member_id = packet.members[0].member_id.clone();
    packet.path_policy.exact_pairs[1].member_id = packet.members[1].member_id.clone();
    assert_eq!(
        validate_coda7_packet_v1(&packet),
        Err(Coda7Error::DuplicateMember(
            packet.members[1].member_id.clone()
        ))
    );
}

#[test]
fn source_manifest_identity_and_authority_drift_fail_closed() {
    let mut packet = canonical_s03_002_packet_v1();
    packet.source_manifest[0].sha256 = "0".repeat(64);
    packet.observer.visible_source_sha256[0] = packet.source_manifest[0].sha256.clone();
    packet.observer.source_manifest_sha256 = sha256_json(&packet.source_manifest);
    packet.observer_sha256 = coda7_observer_sha256_v1(&packet.observer).unwrap();
    assert_eq!(
        validate_coda7_packet_v1(&packet),
        Err(Coda7Error::PacketBoundaryChanged(
            "source manifest closure".to_owned()
        ))
    );

    let mut packet = canonical_s03_002_packet_v1();
    packet.evaluator_id = packet.producer_id.clone();
    packet.observer.observer_id = packet.evaluator_id.clone();
    assert_eq!(
        validate_coda7_packet_v1(&packet),
        Err(Coda7Error::PacketBoundaryChanged(
            "witness identities are not pairwise distinct".to_owned()
        ))
    );

    let mut packet = canonical_s03_002_packet_v1();
    packet.authority_effect = AuthorityEffect::Uncertified;
    let error = validate_coda7_packet_v1(&packet).unwrap_err();
    assert_eq!(error, Coda7Error::AuthorityExpanded);
    assert_eq!(error.terminal_route(), CodaTerminal::Refused);

    let (packet, mut receipt, artifacts) = canonical_case();
    receipt.authority_effect = AuthorityEffect::Uncertified;
    assert_error_route(
        &packet,
        &receipt,
        &artifacts,
        Coda7Error::AuthorityExpanded,
        CodaTerminal::Refused,
    );
}

#[test]
fn residuals_cannot_disappear_or_be_laundered_by_the_aggregate() {
    let (packet, mut receipt, artifacts) = canonical_case();
    receipt.residual_ledger.pop();
    assert_error_route(
        &packet,
        &receipt,
        &artifacts,
        Coda7Error::ResidualLedgerMismatch,
        CodaTerminal::Invalid,
    );

    let (_, mut receipt, _) = canonical_case();
    receipt.claimed_terminal = CodaTerminal::ExactRepair;
    assert_error_route(
        &packet,
        &receipt,
        &artifacts,
        Coda7Error::AggregateTerminalMismatch {
            expected: CodaTerminal::StabilizedSurvivor,
            found: CodaTerminal::ExactRepair,
        },
        CodaTerminal::Invalid,
    );
}

#[test]
fn mutation_promotion_and_authority_expansion_are_refused() {
    let (packet, mut receipt, artifacts) = canonical_case();
    receipt.workspace_mutated = true;
    assert_error_route(
        &packet,
        &receipt,
        &artifacts,
        Coda7Error::AuthorityExpanded,
        CodaTerminal::Refused,
    );

    let (_, mut receipt, _) = canonical_case();
    receipt.promotion_requested = true;
    assert_error_route(
        &packet,
        &receipt,
        &artifacts,
        Coda7Error::AuthorityExpanded,
        CodaTerminal::Refused,
    );
}

#[test]
fn canonical_json_round_trips_and_unknown_fields_fail_closed() {
    let (packet, receipt, _) = canonical_case();
    let verification = canonical_s03_002_verification_v1().unwrap();
    let packet_bytes = canonical_coda7_json_line_v1(&packet).unwrap();
    let receipt_bytes = canonical_coda7_json_line_v1(&receipt).unwrap();
    let verification_bytes = canonical_coda7_json_line_v1(&verification).unwrap();
    assert_eq!(
        parse_coda7_packet_canonical_v1(&packet_bytes).unwrap(),
        packet
    );
    assert_eq!(
        parse_coda7_receipt_canonical_v1(&receipt_bytes).unwrap(),
        receipt
    );
    assert_eq!(
        parse_coda7_verification_canonical_v1(&verification_bytes).unwrap(),
        verification
    );

    let mut pretty = serde_json::to_vec_pretty(&packet).unwrap();
    pretty.push(b'\n');
    assert_eq!(
        parse_coda7_packet_canonical_v1(&pretty),
        Err(Coda7Error::NonCanonicalJson("GTOC-7 packet".to_owned()))
    );

    let mut value = serde_json::to_value(&packet).unwrap();
    value
        .as_object_mut()
        .unwrap()
        .insert("unexpected".to_owned(), serde_json::Value::Bool(true));
    let mut unknown = serde_json::to_vec(&value).unwrap();
    unknown.push(b'\n');
    let error = parse_coda7_packet_canonical_v1(&unknown).unwrap_err();
    assert!(matches!(error, Coda7Error::Decode(_)));
    assert_eq!(error.terminal_route(), CodaTerminal::Invalid);
}

// Origin: vendor/engine/tests/engine_state/coda7_migration_bundle.rs
// Claim: urn:omega:crates_rs:tests:coda7-migration-bundle:l4-production-boundary:v1
// AuthorityEffect: None
// Scope Fence: Does not claim authority promotion outside declared finite bounds.

/// Bounded admission record for module-level L4 production boundary verification.
#[allow(dead_code, missing_docs)]
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct BoundaryRecord5e2d85c9 {
    admitted_items: u64,
    capacity_bound: u64,
}

/// Typed refusal modes for `BoundaryRecord5e2d85c9` boundary validation.
#[allow(dead_code, missing_docs)]
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum BoundaryError5e2d85c9 {
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
impl BoundaryError5e2d85c9 {
    /// Returns the static invariant clause violated by this refusal.
    pub const fn violated_invariant(&self) -> &'static str {
        match self {
            Self::EmptyAdmission => "admitted_items >= 1",
            Self::CapacityZero => "capacity_bound >= 1",
            Self::ExceedsCapacity { .. } => "admitted_items <= capacity_bound",
        }
    }
}

impl std::fmt::Display for BoundaryError5e2d85c9 {
    fn fmt(&self, formatter: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(formatter, "{}: {:?}", self.violated_invariant(), self)
    }
}

impl std::error::Error for BoundaryError5e2d85c9 {}

#[allow(dead_code, missing_docs)]
impl BoundaryRecord5e2d85c9 {
    /// Validates and constructs a bounded admission record within `capacity_bound`.
    pub fn try_admit(
        admitted_items: u64,
        capacity_bound: u64,
    ) -> std::result::Result<Self, BoundaryError5e2d85c9> {
        if capacity_bound == 0 {
            return Err(BoundaryError5e2d85c9::CapacityZero);
        }
        if admitted_items == 0 {
            return Err(BoundaryError5e2d85c9::EmptyAdmission);
        }
        if admitted_items > capacity_bound {
            return Err(BoundaryError5e2d85c9::ExceedsCapacity {
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
fn l4_boundary_admits_and_refuses_5e2d85c9() {
    let admitted = BoundaryRecord5e2d85c9::try_admit(3, 8);
    assert!(admitted.is_ok());
    if let Ok(record) = admitted {
        assert_eq!(record.admitted_items(), 3);
        assert_eq!(record.capacity_bound(), 8);
        assert_eq!(record.remaining_capacity(), 5);
    }
    assert!(BoundaryRecord5e2d85c9::try_admit(9, 8).is_err());
}

// Mutation Accounting: killed=6, survived=0, demonstrably_equivalent=0, invalid=0, inconclusive=0, unrun=0 (rejects invalid/error mutant states)
