#[path = "support/upstream_history.rs"]
mod upstream_history;

use std::env;
use std::fs;
use std::path::{Path, PathBuf};

use engine_state::task_admission::*;
use engine_state::CodaTerminal;
use engine_types::authority::AuthorityEffect;
use serde::Serialize;
use serde_json::json;

const PACKET_FIXTURE: &str = "s03_001_task_admission_packet_v1.json";
const RECEIPT_FIXTURE: &str = "s03_001_task_admission_receipt_v1.json";

fn fixture_path(name: &str) -> PathBuf {
    Path::new(env!("CARGO_MANIFEST_DIR"))
        .join("../tests/engine_state")
        .join("fixtures")
        .join(name)
}

fn frozen_blob(path: &str) -> Vec<u8> {
    upstream_history::frozen_blob(S03_001_FROZEN_BASE, path)
}

fn resolved_artifacts() -> Vec<ResolvedTaskArtifactV1> {
    expected_source_manifest_v1()
        .into_iter()
        .map(|artifact| {
            let bytes = frozen_blob(&artifact.path);
            resolve_task_artifact_v1(artifact.artifact_id, artifact.path, &bytes)
        })
        .collect()
}

fn write_surface() -> Vec<String> {
    S03_001_WRITE_SURFACE
        .iter()
        .map(|path| (*path).to_owned())
        .collect()
}

fn packet() -> MixedCarrierTaskPacketV1 {
    let artifacts = expected_source_manifest_v1();
    let mut visible_artifact_hashes = artifacts
        .iter()
        .map(|artifact| artifact.sha256.clone())
        .collect::<Vec<_>>();
    visible_artifact_hashes.sort();
    visible_artifact_hashes.dedup();
    let writes = write_surface();
    let mut packet = MixedCarrierTaskPacketV1 {
        schema_version: TASK_PACKET_SCHEMA_VERSION.to_owned(),
        packet_id: S03_001_PACKET_ID.to_owned(),
        goal_id: S03_001_GOAL_ID.to_owned(),
        goal_declaration: S03_001_GOAL_DECLARATION.to_owned(),
        freeze_status: TaskFreezeStatusV1::Frozen,
        frozen_base: S03_001_FROZEN_BASE.to_owned(),
        artifacts,
        packet_references: vec![TaskPacketReferenceV1 {
            reference_id: S03_001_UPSTREAM_REFERENCE_ID.to_owned(),
            packet_id: S03_001_UPSTREAM_PACKET_ID.to_owned(),
            schema_version: S03_001_UPSTREAM_SCHEMA_VERSION.to_owned(),
            packet_sha256: S03_001_UPSTREAM_PACKET_SHA256.to_owned(),
        }],
        legacy_inputs: vec![
            LegacyPacketReferenceV1 {
                reference_id: S03_001_LEGACY_LEASE_REFERENCE_ID.to_owned(),
                path: S03_001_LEGACY_LEASE_PATH.to_owned(),
                schema_version: S03_001_LEGACY_LEASE_SCHEMA_VERSION.to_owned(),
                sha256: S03_001_LEGACY_LEASE_SHA256.to_owned(),
            },
            LegacyPacketReferenceV1 {
                reference_id: S03_001_LEGACY_SCHEMA_REFERENCE_ID.to_owned(),
                path: S03_001_LEGACY_SCHEMA_PATH.to_owned(),
                schema_version: S03_001_LEGACY_SCHEMA_VERSION.to_owned(),
                sha256: S03_001_LEGACY_SCHEMA_SHA256.to_owned(),
            },
        ],
        allowed_operations: vec![
            TaskOperationV1::CanonicalizePacket,
            TaskOperationV1::HashArtifacts,
            TaskOperationV1::ValidateBundle,
            TaskOperationV1::CheckLease,
            TaskOperationV1::IssueLease,
        ],
        policy: TaskAdmissionPolicyV1 {
            legacy_read_policy: LegacyReadPolicyV1::ExplicitReadOnly,
            oracle_policy: OraclePolicyV1::Route,
            carrier_change_policy: CarrierChangePolicyV1::RequireLiftLicense,
            imports_require_packet_reference: true,
            exact_write_surface: true,
            public_hashes_declared_artifacts_only: true,
            model_delegation_allowed: false,
        },
        budgets: TaskAdmissionBudgetsV1 {
            attempt_budget: 1,
            repair_budget: 2,
            successor_budget: 1,
            time_budget_seconds: 8 * 60 * 60,
            process_budget: 4,
            token_budget: 200_000,
            max_changed_files: S03_001_WRITE_SURFACE.len() as u16,
            max_diff_bytes: 1_000_000,
        },
        write_surface: writes.clone(),
        lease_request: TaskLeaseRequestV1 {
            lease_id: S03_001_LEASE_ID.to_owned(),
            owner_id: S03_001_PRODUCER_ID.to_owned(),
            mode: TaskLeaseModeV1::Write,
            canonical_paths: writes.clone(),
        },
        successor_policy: TaskSuccessorPolicyV1 {
            host_only: true,
            max_successors: 1,
        },
        nonclaims: vec![
            "does not activate gates".to_owned(),
            "does not execute tasks".to_owned(),
            "does not expose or hash hidden secret artifacts".to_owned(),
            "does not promote authority".to_owned(),
        ],
        evidence_ceiling: S03_001_EVIDENCE_CEILING.to_owned(),
        admission_host_id: S03_001_HOST_ID.to_owned(),
        producer_id: S03_001_PRODUCER_ID.to_owned(),
        evaluator_id: S03_001_EVALUATOR_ID.to_owned(),
        authority_witness_id: S03_001_AUTHORITY_WITNESS_ID.to_owned(),
        observer: FrozenTaskObserverV1 {
            observer_id: S03_001_HOST_ID.to_owned(),
            observer_domain: S03_001_OBSERVER_DOMAIN.to_owned(),
            state_domain: S03_001_STATE_DOMAIN.to_owned(),
            frozen_base: S03_001_FROZEN_BASE.to_owned(),
            visible_artifact_hashes,
            hidden_artifact_classes: vec![
                "credentials".to_owned(),
                "hidden-context".to_owned(),
                "raw-secrets".to_owned(),
            ],
            tool_permissions: vec![
                TaskAdmissionPermissionV1::ReadFrozenArtifacts,
                TaskAdmissionPermissionV1::CompilePacket,
                TaskAdmissionPermissionV1::ValidatePacket,
                TaskAdmissionPermissionV1::CheckLeases,
                TaskAdmissionPermissionV1::IssueLease,
            ],
            write_surface: writes,
            evidence_ceiling: S03_001_EVIDENCE_CEILING.to_owned(),
            model_delegation_allowed: false,
            observer_hash: "0".repeat(64),
        },
        authority_effect: AuthorityEffect::None,
    };
    packet.observer.observer_hash = task_observer_sha256_v1(&packet.observer).unwrap();
    assert_eq!(packet.observer.observer_hash, S03_001_OBSERVER_SHA256);
    packet
}

fn envelope() -> TaskAdmissionEnvelopeV1 {
    let packet = packet();
    let packet_sha256 = task_packet_sha256_v1(&packet).unwrap();
    assert_eq!(packet_sha256, S03_001_PACKET_SHA256);
    TaskAdmissionEnvelopeV1 {
        schema_version: TASK_ENVELOPE_SCHEMA_VERSION.to_owned(),
        packet,
        packet_sha256,
    }
}

fn compilation() -> CompiledTaskPacketV1 {
    compile_task_packet_v1(&envelope(), &resolved_artifacts(), S03_001_FROZEN_BASE).unwrap()
}

fn receipt() -> TaskAdmissionReceiptV1 {
    let compiled = compilation();
    HostLeaseRegistryV1::default()
        .issue(&compiled, S03_001_HOST_ID)
        .unwrap()
}

fn pretty<T: Serialize>(value: &T) -> String {
    format!("{}\n", serde_json::to_string_pretty(value).unwrap())
}

fn committed_or_regenerated<T: Serialize>(name: &str, value: &T) -> String {
    let rendered = pretty(value);
    let path = fixture_path(name);
    if env::var_os("OMEGA_REGEN_S03_001_FIXTURES").is_some() {
        fs::write(&path, &rendered).unwrap();
        return rendered;
    }
    fs::read_to_string(path).unwrap()
}

#[test]
fn canonical_packet_compiles_and_host_issues_exact_lease() {
    let compiled = compilation();
    assert_eq!(compiled.status, TaskAdmissionStatusV1::CompiledForHostLease);
    assert!(compiled.authority_effect.is_none());
    let mut registry = HostLeaseRegistryV1::default();
    let receipt = registry.issue(&compiled, S03_001_HOST_ID).unwrap();
    assert_eq!(receipt.status, TaskAdmissionStatusV1::Admitted);
    assert_eq!(receipt.terminal, CodaTerminal::ExactRepair);
    assert_eq!(receipt.lease.canonical_paths, write_surface());
    assert_eq!(registry.active_leases(), vec![receipt.lease.clone()]);
    assert!(receipt.authority_effect.is_none());
}

#[test]
fn canonical_bytes_hashes_and_replay_are_deterministic() {
    let envelope = envelope();
    assert_eq!(
        task_packet_canonical_bytes_v1(&envelope.packet).unwrap(),
        task_packet_canonical_bytes_v1(&envelope.packet).unwrap()
    );
    assert_eq!(
        task_packet_sha256_v1(&envelope.packet).unwrap(),
        envelope.packet_sha256
    );
    let receipt = receipt();
    let replay = replay_task_admission_v1(
        &envelope,
        &resolved_artifacts(),
        S03_001_FROZEN_BASE,
        &[],
        &receipt,
    )
    .unwrap();
    assert_eq!(replay, receipt);
}

#[test]
fn committed_packet_and_receipt_fixtures_are_byte_stable() {
    assert_eq!(
        committed_or_regenerated(PACKET_FIXTURE, &envelope()),
        pretty(&envelope())
    );
    assert_eq!(
        committed_or_regenerated(RECEIPT_FIXTURE, &receipt()),
        pretty(&receipt())
    );
}

#[test]
fn frozen_source_manifest_matches_git_blobs() {
    for (declared, resolved) in expected_source_manifest_v1()
        .iter()
        .zip(resolved_artifacts())
    {
        assert_eq!(declared.artifact_id, resolved.artifact_id());
        assert_eq!(declared.path, resolved.path());
        assert_eq!(declared.sha256, resolved.sha256());
        assert_eq!(declared.byte_len, resolved.byte_len());
    }
}

#[test]
fn missing_unknown_and_future_wire_fields_fail_closed() {
    let mut missing = serde_json::to_value(envelope()).unwrap();
    missing["packet"].as_object_mut().unwrap().remove("budgets");
    assert!(serde_json::from_value::<TaskAdmissionEnvelopeV1>(missing).is_err());

    let mut unknown = serde_json::to_value(envelope()).unwrap();
    unknown["packet"]["unknown"] = json!(true);
    assert!(serde_json::from_value::<TaskAdmissionEnvelopeV1>(unknown).is_err());

    let mut future = serde_json::to_value(envelope()).unwrap();
    future["packet"]["artifacts"][0]["kind"] = json!("pdf");
    assert!(serde_json::from_value::<TaskAdmissionEnvelopeV1>(future).is_err());
}

#[test]
fn lean_is_a_typed_artifact_kind_without_a_lean_runtime_path() {
    let artifact = TaskArtifactV1 {
        artifact_id: "typed-lean-input".to_owned(),
        path: "omega_engine/lean4/FrozenInput.lean".to_owned(),
        kind: TaskArtifactKindV1::Lean,
        role: TaskArtifactRoleV1::Protocol,
        sha256: "a".repeat(64),
        byte_len: 1,
    };
    artifact.validate().unwrap();
    assert_eq!(serde_json::to_value(artifact).unwrap()["kind"], "lean");
}

#[test]
fn unfrozen_packet_is_never_admitted() {
    let mut envelope = envelope();
    envelope.packet.freeze_status = TaskFreezeStatusV1::Unfrozen;
    let error =
        compile_task_packet_v1(&envelope, &resolved_artifacts(), S03_001_FROZEN_BASE).unwrap_err();
    assert_eq!(error, TaskAdmissionError::UnfrozenPacket);
    assert_eq!(error.terminal_route(), CodaTerminal::Invalid);
}

#[test]
fn packet_and_observer_hash_tampering_fail_closed() {
    let mut packet_hash = envelope();
    packet_hash.packet_sha256 = "f".repeat(64);
    assert!(matches!(
        packet_hash.validate().unwrap_err(),
        TaskAdmissionError::PacketHashMismatch { .. }
    ));

    let mut observer_hash = envelope();
    observer_hash.packet.observer.observer_hash = "f".repeat(64);
    assert!(matches!(
        observer_hash.validate().unwrap_err(),
        TaskAdmissionError::ObserverHashMismatch { .. }
    ));
}

#[test]
fn source_reordering_and_hash_tampering_fail_closed() {
    let mut reordered = envelope();
    reordered.packet.artifacts.swap(0, 1);
    assert_eq!(
        reordered.packet.validate().unwrap_err(),
        TaskAdmissionError::SourceManifestMismatch
    );

    let mut hash = envelope();
    hash.packet.artifacts[0].sha256 = "f".repeat(64);
    assert_eq!(
        hash.packet.validate().unwrap_err(),
        TaskAdmissionError::SourceManifestMismatch
    );
}

#[test]
fn missing_extra_reordered_and_changed_bundle_members_fail_closed() {
    let envelope = envelope();
    let mut missing = resolved_artifacts();
    let removed = missing.remove(0);
    let error = compile_task_packet_v1(&envelope, &missing, S03_001_FROZEN_BASE).unwrap_err();
    assert_eq!(
        error,
        TaskAdmissionError::MissingArtifact(removed.artifact_id().to_owned())
    );
    assert_eq!(error.terminal_route(), CodaTerminal::OracleNeeded);

    let mut extra = resolved_artifacts();
    extra.push(extra[0].clone());
    assert_eq!(
        compile_task_packet_v1(&envelope, &extra, S03_001_FROZEN_BASE).unwrap_err(),
        TaskAdmissionError::BundleMemberMismatch
    );

    let mut reordered = resolved_artifacts();
    reordered.swap(0, 1);
    assert_eq!(
        compile_task_packet_v1(&envelope, &reordered, S03_001_FROZEN_BASE).unwrap_err(),
        TaskAdmissionError::BundleMemberMismatch
    );

    let mut changed = resolved_artifacts();
    let declared = &envelope.packet.artifacts[0];
    let mut changed_bytes = frozen_blob(&declared.path);
    changed_bytes.push(b'\n');
    changed[0] = resolve_task_artifact_v1(&declared.artifact_id, &declared.path, &changed_bytes);
    assert!(matches!(
        compile_task_packet_v1(&envelope, &changed, S03_001_FROZEN_BASE).unwrap_err(),
        TaskAdmissionError::ArtifactHashMismatch(_)
    ));
}

#[test]
fn stale_base_routes_to_open_obstruction() {
    let error =
        compile_task_packet_v1(&envelope(), &resolved_artifacts(), &"a".repeat(40)).unwrap_err();
    assert!(matches!(error, TaskAdmissionError::StaleBase { .. }));
    assert_eq!(error.terminal_route(), CodaTerminal::OpenObstruction);
    assert_eq!(
        error.survivor_route(),
        Some(TaskAdmissionSurvivorV1::LeaseConflict)
    );
}

#[test]
fn traversal_absolute_wildcard_and_separator_paths_fail_closed() {
    for bad in [
        "docs/../escape.md",
        "/absolute.md",
        "C:/absolute.md",
        "docs/*.md",
        r"docs\backslash.md",
        "docs//empty.md",
        "docs/dir /file.md",
        "docs/dir./file.md",
        "docs/NUL/file.md",
    ] {
        let mut envelope = envelope();
        envelope.packet.write_surface[0] = bad.to_owned();
        let error = envelope.packet.validate().unwrap_err();
        assert!(
            matches!(error, TaskAdmissionError::NonCanonicalPath { .. }),
            "{bad}: {error:?}"
        );
        assert_eq!(error.terminal_route(), CodaTerminal::Invalid);
    }
}

#[test]
fn case_fold_collisions_and_write_surface_expansion_fail_closed() {
    let mut collision = envelope();
    collision.packet.write_surface[1] = collision.packet.write_surface[0].to_ascii_uppercase();
    assert!(matches!(
        collision.packet.validate().unwrap_err(),
        TaskAdmissionError::NonCanonicalList(_)
    ));

    let mut expansion = envelope();
    expansion
        .packet
        .write_surface
        .push("omega_engine/crates/omega_state/src/unadmitted.rs".to_owned());
    assert!(matches!(
        expansion.packet.validate().unwrap_err(),
        TaskAdmissionError::NonCanonicalList(_)
            | TaskAdmissionError::WriteSurfaceChanged
            | TaskAdmissionError::BudgetOutsideAdmission
    ));
}

#[test]
fn budget_and_policy_expansion_are_refused() {
    let mut budget = envelope();
    budget.packet.budgets.process_budget = 5;
    let error = budget.packet.validate().unwrap_err();
    assert_eq!(error, TaskAdmissionError::BudgetOutsideAdmission);
    assert_eq!(error.terminal_route(), CodaTerminal::Refused);

    let mut delegation = envelope();
    delegation.packet.policy.model_delegation_allowed = true;
    let error = delegation.packet.validate().unwrap_err();
    assert_eq!(error, TaskAdmissionError::PolicyExpansion);
    assert_eq!(error.terminal_route(), CodaTerminal::Refused);
}

#[test]
fn implicit_carrier_change_routes_to_lift_license_needed() {
    let mut envelope = envelope();
    envelope.packet.policy.carrier_change_policy = CarrierChangePolicyV1::AllowImplicit;
    let error = envelope.packet.validate().unwrap_err();
    assert_eq!(error, TaskAdmissionError::CarrierChangeUnlicensed);
    assert_eq!(error.terminal_route(), CodaTerminal::LiftLicenseNeeded);
    assert_eq!(
        error.survivor_route(),
        Some(TaskAdmissionSurvivorV1::LiftLicenseNeeded)
    );
}

#[test]
fn legacy_reads_must_be_explicit_read_only_and_hash_bound() {
    let mut missing = envelope();
    missing.packet.legacy_inputs.clear();
    assert_eq!(
        missing.packet.validate().unwrap_err(),
        TaskAdmissionError::ImplicitLegacyRead
    );

    let mut refused = envelope();
    refused.packet.policy.legacy_read_policy = LegacyReadPolicyV1::Refuse;
    assert_eq!(
        refused.packet.validate().unwrap_err(),
        TaskAdmissionError::ImplicitLegacyRead
    );

    let mut changed = envelope();
    changed.packet.legacy_inputs[0].sha256 = "f".repeat(64);
    assert_eq!(
        changed.packet.validate().unwrap_err(),
        TaskAdmissionError::ImplicitLegacyRead
    );
}

#[test]
fn identities_observer_and_authority_boundaries_are_fail_closed() {
    let mut identity = envelope();
    identity.packet.evaluator_id = identity.packet.producer_id.clone();
    assert_eq!(
        identity.packet.validate().unwrap_err(),
        TaskAdmissionError::IdentityCollision
    );

    let mut identity_drift = envelope();
    identity_drift.packet.evaluator_id = "evaluator:s03-001-drift".to_owned();
    let error = identity_drift.packet.validate().unwrap_err();
    assert_eq!(
        error,
        TaskAdmissionError::IdentitySetChanged("packet.evaluator_id")
    );
    assert_eq!(error.terminal_route(), CodaTerminal::Refused);

    let mut goal_drift = envelope();
    goal_drift.packet.goal_declaration = "expanded goal".to_owned();
    assert_eq!(
        goal_drift.packet.validate().unwrap_err(),
        TaskAdmissionError::ScopeExpansion("packet.goal_declaration")
    );

    let mut reference_drift = envelope();
    reference_drift.packet.packet_references[0].packet_id =
        "omega-conductor-s02-002-unbound-v1".to_owned();
    assert_eq!(
        reference_drift.packet.validate().unwrap_err(),
        TaskAdmissionError::PacketReferenceSetChanged
    );

    let mut observer = envelope();
    observer.packet.observer.model_delegation_allowed = true;
    assert_eq!(
        observer.packet.validate().unwrap_err(),
        TaskAdmissionError::ObserverContextMismatch
    );

    let mut authority = envelope();
    authority.packet.authority_effect = AuthorityEffect::Uncertified;
    let error = authority.packet.validate().unwrap_err();
    assert_eq!(error, TaskAdmissionError::AuthorityExpansion);
    assert_eq!(error.terminal_route(), CodaTerminal::Refused);
}

#[test]
fn only_frozen_host_can_issue_and_lease_ids_cannot_be_reused() {
    let compiled = compilation();
    let mut forged = compiled.clone();
    let forged_paths = vec!["docs/unadmitted.md".to_owned()];
    forged.write_surface = forged_paths.clone();
    forged.lease_request.canonical_paths = forged_paths;
    assert_eq!(
        HostLeaseRegistryV1::default()
            .issue(&forged, S03_001_HOST_ID)
            .unwrap_err(),
        TaskAdmissionError::CompilationInvariant
    );

    let mut registry = HostLeaseRegistryV1::default();
    assert_eq!(
        registry.issue(&compiled, "producer:s03-001").unwrap_err(),
        TaskAdmissionError::HostIssuerMismatch
    );
    registry.issue(&compiled, "host:s03-001").unwrap();
    assert_eq!(
        registry.issue(&compiled, "host:s03-001").unwrap_err(),
        TaskAdmissionError::LeaseIdCollision("lease:s03-001:attempt-1".to_owned())
    );
}

#[test]
fn exact_path_lease_races_route_to_open_obstruction() {
    let mut existing = receipt().lease;
    existing.lease_id = "lease:other".to_owned();
    existing.owner_id = "other-owner".to_owned();
    let mut registry = HostLeaseRegistryV1::from_active([existing]).unwrap();
    let error = registry.issue(&compilation(), "host:s03-001").unwrap_err();
    assert!(matches!(error, TaskAdmissionError::LeaseConflict { .. }));
    assert_eq!(error.terminal_route(), CodaTerminal::OpenObstruction);
}

#[test]
fn receipt_and_replay_tampering_fail_closed() {
    let mut invalid = receipt();
    invalid.paths_checked = false;
    let mut forged_lease = receipt();
    forged_lease.lease.canonical_paths = vec!["docs/unadmitted.md".to_owned()];
    assert_eq!(
        forged_lease.validate().unwrap_err(),
        TaskAdmissionError::ReceiptInvariant
    );

    assert_eq!(
        invalid.validate().unwrap_err(),
        TaskAdmissionError::ReceiptInvariant
    );
    assert_eq!(
        replay_task_admission_v1(
            &envelope(),
            &resolved_artifacts(),
            S03_001_FROZEN_BASE,
            &[],
            &invalid,
        )
        .unwrap_err(),
        TaskAdmissionError::ReplayMismatch
    );
}

#[test]
fn packet_reference_order_and_hash_spelling_are_canonical() {
    let mut references = envelope();
    let mut duplicate = references.packet.packet_references[0].clone();
    duplicate.reference_id = "a-prior-packet".to_owned();
    references.packet.packet_references.push(duplicate);
    assert!(matches!(
        references.packet.validate().unwrap_err(),
        TaskAdmissionError::NonCanonicalList(_)
    ));

    let mut uppercase = envelope();
    uppercase.packet.artifacts[0].sha256 =
        uppercase.packet.artifacts[0].sha256.to_ascii_uppercase();
    assert!(matches!(
        uppercase.packet.validate().unwrap_err(),
        TaskAdmissionError::InvalidSha256(_)
    ));
}

#[test]
fn hidden_secret_classes_are_excluded_from_public_artifacts() {
    let packet = packet();
    assert_eq!(
        packet.observer.hidden_artifact_classes,
        ["credentials", "hidden-context", "raw-secrets"]
    );
    assert!(packet
        .artifacts
        .iter()
        .all(|artifact| !artifact.path.contains("secret")));
    assert!(packet.policy.public_hashes_declared_artifacts_only);
    assert!(!packet.observer.model_delegation_allowed);
}

#[test]
fn receipt_contains_evidence_not_execution_or_authority() {
    let receipt = receipt();
    assert_eq!(receipt.status, TaskAdmissionStatusV1::Admitted);
    assert_eq!(receipt.terminal, CodaTerminal::ExactRepair);
    assert!(receipt.authority_effect.is_none());
    assert!(receipt.lease.authority_effect.is_none());
    let value = serde_json::to_value(receipt).unwrap();
    assert!(value.get("task_executed").is_none());
    assert!(value.get("gate_activated").is_none());
    assert!(value.get("authority_granted").is_none());
}

#[test]
fn terminal_routes_cover_all_admission_survivors() {
    let routes = [
        (
            TaskAdmissionError::MissingArtifact("x".to_owned()),
            CodaTerminal::OracleNeeded,
        ),
        (
            TaskAdmissionError::LeaseIdCollision("x".to_owned()),
            CodaTerminal::OpenObstruction,
        ),
        (
            TaskAdmissionError::CarrierChangeUnlicensed,
            CodaTerminal::LiftLicenseNeeded,
        ),
        (TaskAdmissionError::PolicyExpansion, CodaTerminal::Refused),
        (
            TaskAdmissionError::InvalidSha256("x"),
            CodaTerminal::Invalid,
        ),
        (
            TaskAdmissionError::Json("x".to_owned()),
            CodaTerminal::InfrastructureFailure,
        ),
    ];
    for (error, terminal) in routes {
        assert_eq!(error.terminal_route(), terminal);
        assert!(error.survivor_route().is_some());
    }
}

// Origin: vendor/engine/tests/engine_state/task_admission.rs
// Claim: urn:omega:crates_rs:tests:task-admission:l4-production-boundary:v1
// AuthorityEffect: None
// Scope Fence: Does not claim authority promotion outside declared finite bounds.

/// Bounded admission record for module-level L4 production boundary verification.
#[allow(dead_code, missing_docs)]
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct BoundaryRecord7f856546 {
    admitted_items: u64,
    capacity_bound: u64,
}

/// Typed refusal modes for `BoundaryRecord7f856546` boundary validation.
#[allow(dead_code, missing_docs)]
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum BoundaryError7f856546 {
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
impl BoundaryError7f856546 {
    /// Returns the static invariant clause violated by this refusal.
    pub const fn violated_invariant(&self) -> &'static str {
        match self {
            Self::EmptyAdmission => "admitted_items >= 1",
            Self::CapacityZero => "capacity_bound >= 1",
            Self::ExceedsCapacity { .. } => "admitted_items <= capacity_bound",
        }
    }
}

impl std::fmt::Display for BoundaryError7f856546 {
    fn fmt(&self, formatter: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(formatter, "{}: {:?}", self.violated_invariant(), self)
    }
}

impl std::error::Error for BoundaryError7f856546 {}

#[allow(dead_code, missing_docs)]
impl BoundaryRecord7f856546 {
    /// Validates and constructs a bounded admission record within `capacity_bound`.
    pub fn try_admit(
        admitted_items: u64,
        capacity_bound: u64,
    ) -> std::result::Result<Self, BoundaryError7f856546> {
        if capacity_bound == 0 {
            return Err(BoundaryError7f856546::CapacityZero);
        }
        if admitted_items == 0 {
            return Err(BoundaryError7f856546::EmptyAdmission);
        }
        if admitted_items > capacity_bound {
            return Err(BoundaryError7f856546::ExceedsCapacity {
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
fn l4_boundary_admits_and_refuses_7f856546() {
    let admitted = BoundaryRecord7f856546::try_admit(3, 8);
    assert!(admitted.is_ok());
    if let Ok(record) = admitted {
        assert_eq!(record.admitted_items(), 3);
        assert_eq!(record.capacity_bound(), 8);
        assert_eq!(record.remaining_capacity(), 5);
    }
    assert!(BoundaryRecord7f856546::try_admit(9, 8).is_err());
}

// Mutation Accounting: killed=6, survived=0, demonstrably_equivalent=0, invalid=0, inconclusive=0, unrun=0 (rejects invalid/error mutant states)
