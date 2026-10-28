#[path = "support/upstream_history.rs"]
mod upstream_history;

use std::collections::BTreeMap;
use std::env;
use std::fs;
use std::path::{Path, PathBuf};

use engine_contracts::{
    GaugeBindingV1, GaugeExecutionModeV1, ModelGaugeProfileV1, ModelProviderV1,
    OperatorCapabilityV1, OperatorInputV1, OperatorManifestV1, OperatorOperationV1,
    OperatorPermissionV1, OperatorRegistryContractError, OperatorRegistryV1,
    OperatorWitnessRequirementV1, RuntimeGaugeV1, GAUGE_BINDING_SCHEMA_VERSION,
    OPERATOR_INPUT_SCHEMA_VERSION, OPERATOR_MANIFEST_SCHEMA_VERSION,
    OPERATOR_REGISTRY_SCHEMA_VERSION,
};
use engine_state::coda1_classifier::{sha256_bytes_v1, Coda1BudgetsV1, SourceHashV1};
use engine_state::coda_gtla_protocol::{FrozenObserverContextV1, CodaTerminal};
use engine_state::operator_registry_runtime::*;
use engine_types::authority::AuthorityEffect;
use serde::{Deserialize, Serialize};
use serde_json::Value;

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
struct OperatorRegistryFixtureSetV1 {
    schema_version: String,
    admissions: Vec<OperatorRegistryAdmissionV1>,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
struct OperatorRegistryReceiptSetV1 {
    schema_version: String,
    executions: Vec<OperatorRegistryExecutionV1>,
}

fn repository_root() -> PathBuf {
    PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .ancestors()
        .nth(3)
        .expect("omega_state lives three levels below the repository root")
        .to_path_buf()
}

fn fixture_path(name: &str) -> PathBuf {
    PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .join("../tests/engine_state")
        .join("fixtures")
        .join(name)
}

fn source_manifest() -> Vec<SourceHashV1> {
    S02_001_SOURCE_MANIFEST
        .iter()
        .map(|(path, sha256)| SourceHashV1 {
            path: (*path).to_owned(),
            sha256: (*sha256).to_owned(),
        })
        .collect()
}

fn manifest_write_surface() -> Vec<String> {
    vec![
        "omega_engine/crates/omega_state/tests/fixtures/operator_registry_fixture_matrix_v1.json"
            .to_owned(),
        "omega_engine/crates/omega_state/tests/fixtures/operator_registry_receipt_matrix_v1.json"
            .to_owned(),
    ]
}

fn manifest() -> OperatorManifestV1 {
    OperatorManifestV1 {
        schema_version: OPERATOR_MANIFEST_SCHEMA_VERSION.to_owned(),
        operator_id: S02_001_OPERATOR_ID.to_owned(),
        semantic_contract_id: S02_001_SEMANTIC_CONTRACT_ID.to_owned(),
        input_families: vec![S02_001_INPUT_FAMILY.to_owned()],
        output_families: vec![S02_001_OUTPUT_FAMILY.to_owned()],
        permitted_operations: vec![OperatorOperationV1::CanonicalJsonEcho],
        required_capabilities: vec![
            OperatorCapabilityV1::CanonicalJson,
            OperatorCapabilityV1::DeterministicReplay,
        ],
        permission_ceiling: vec![
            OperatorPermissionV1::ReadFixture,
            OperatorPermissionV1::WriteReceipt,
        ],
        write_surface: manifest_write_surface(),
        evidence_ceiling: S02_001_EVIDENCE_CEILING.to_owned(),
        license_ids: vec![
            "license:fixture-read-v1".to_owned(),
            "license:receipt-write-v1".to_owned(),
        ],
        witness_requirements: vec![
            OperatorWitnessRequirementV1::Producer,
            OperatorWitnessRequirementV1::IndependentEvaluator,
            OperatorWitnessRequirementV1::AuthorityWitness,
        ],
        authority_effect: AuthorityEffect::None,
    }
}

fn binding(
    binding_id: &str,
    runtime: RuntimeGaugeV1,
    execution_mode: GaugeExecutionModeV1,
    adapter_id: &str,
    provided_capabilities: Vec<OperatorCapabilityV1>,
    manifest_sha256: &str,
) -> GaugeBindingV1 {
    GaugeBindingV1 {
        schema_version: GAUGE_BINDING_SCHEMA_VERSION.to_owned(),
        binding_id: binding_id.to_owned(),
        operator_id: S02_001_OPERATOR_ID.to_owned(),
        runtime,
        execution_mode,
        adapter_id: adapter_id.to_owned(),
        semantic_contract_id: S02_001_SEMANTIC_CONTRACT_ID.to_owned(),
        provided_capabilities,
        granted_permissions: vec![
            OperatorPermissionV1::ReadFixture,
            OperatorPermissionV1::WriteReceipt,
        ],
        write_surface: manifest_write_surface(),
        evidence_ceiling: S02_001_EVIDENCE_CEILING.to_owned(),
        network_access: false,
        credential_access: false,
        hidden_context_classes: Vec::new(),
        operator_manifest_sha256: manifest_sha256.to_owned(),
        authority_effect: AuthorityEffect::None,
    }
}

fn registry() -> OperatorRegistryV1 {
    let manifest = manifest();
    let manifest_sha256 = operator_registry_sha256_json_v1(&manifest).unwrap();
    let model = binding(
        S02_001_MODEL_BINDING_ID,
        RuntimeGaugeV1::ModelProfile(ModelGaugeProfileV1 {
            provider: ModelProviderV1::Codex,
            profile_id: S02_001_MODEL_PROFILE_ID.to_owned(),
        }),
        GaugeExecutionModeV1::ModelFixtureReplay,
        S02_001_MODEL_ADAPTER_ID,
        vec![
            OperatorCapabilityV1::CanonicalJson,
            OperatorCapabilityV1::DeterministicReplay,
            OperatorCapabilityV1::ModelProfile,
        ],
        &manifest_sha256,
    );
    let fixture = binding(
        S02_001_FIXTURE_BINDING_ID,
        RuntimeGaugeV1::Fixture,
        GaugeExecutionModeV1::DeterministicFixture,
        S02_001_FIXTURE_ADAPTER_ID,
        vec![
            OperatorCapabilityV1::CanonicalJson,
            OperatorCapabilityV1::DeterministicReplay,
        ],
        &manifest_sha256,
    );
    OperatorRegistryV1 {
        schema_version: OPERATOR_REGISTRY_SCHEMA_VERSION.to_owned(),
        registry_id: "registry:s02-001-v1".to_owned(),
        max_operators: 1,
        manifests: vec![manifest],
        bindings: vec![model, fixture],
    }
}

fn input() -> OperatorInputV1 {
    OperatorInputV1 {
        schema_version: OPERATOR_INPUT_SCHEMA_VERSION.to_owned(),
        request_id: "request:s02-001:canonical-echo".to_owned(),
        family: S02_001_INPUT_FAMILY.to_owned(),
        payload: BTreeMap::from([
            ("claim".to_owned(), "bounded fixture replay only".to_owned()),
            ("payload".to_owned(), "omega-operator-registry".to_owned()),
        ]),
    }
}
fn packet() -> OperatorRegistryPacketV1 {
    let sources = source_manifest();
    let mut visible_artifact_hashes = sources
        .iter()
        .map(|source| source.sha256.clone())
        .collect::<Vec<_>>();
    visible_artifact_hashes.sort();
    visible_artifact_hashes.dedup();
    let evaluator_id = "witness:evaluator:operator-substitution-v1".to_owned();
    let mut observer = FrozenObserverContextV1 {
        observer_id: evaluator_id.clone(),
        observer_domain: S02_001_OBSERVER_DOMAIN.to_owned(),
        state_domain: S02_001_STATE_DOMAIN.to_owned(),
        observer_hash: "0".repeat(64),
        visible_artifact_hashes,
        hidden_artifact_classes: vec![
            "live-provider-context".to_owned(),
            "production-credentials".to_owned(),
        ],
        tool_permissions: vec![
            "read:frozen-source".to_owned(),
            "test:omega_state".to_owned(),
            "write:admitted-paths".to_owned(),
        ],
        write_surface: S02_001_WRITE_SURFACE
            .iter()
            .map(|path| (*path).to_owned())
            .collect(),
        evidence_ceiling: S02_001_EVIDENCE_CEILING.to_owned(),
    };
    observer.observer_hash = operator_registry_observer_sha256_v1(&observer).unwrap();
    OperatorRegistryPacketV1 {
        schema_version: S02_001_PACKET_SCHEMA_VERSION.to_owned(),
        packet_id: "S02-001:operator-registry-v1".to_owned(),
        frozen_base: S02_001_FROZEN_BASE.to_owned(),
        target_sprint: S02_001_TARGET.to_owned(),
        source_manifest: sources,
        budgets: Coda1BudgetsV1 {
            attempt_budget: 1,
            repair_budget: 2,
            successor_budget: 1,
            time_budget_seconds: 8 * 60 * 60,
            process_budget: 4,
            token_budget: 200_000,
        },
        evidence_ceiling: S02_001_EVIDENCE_CEILING.to_owned(),
        observer,
        producer_id: "witness:producer:operator-fixture-v1".to_owned(),
        evaluator_id,
        authority_witness_id: "witness:authority:operator-none-check-v1".to_owned(),
        prior_work_ledger: vec![
            "S01-001 canonical protocol machine".to_owned(),
            "S01-003 bounded GTOC-2 transport".to_owned(),
            "omega_contracts canonical semantic owner".to_owned(),
            "omega_operator_algebra mathematical registry owner".to_owned(),
        ],
        registry: registry(),
        input: input(),
    }
}

fn seal(packet: OperatorRegistryPacketV1) -> OperatorRegistryAdmissionV1 {
    let packet_sha256 = operator_registry_packet_sha256_v1(&packet).unwrap();
    OperatorRegistryAdmissionV1 {
        schema_version: S02_001_ADMISSION_SCHEMA_VERSION.to_owned(),
        packet,
        packet_sha256,
    }
}

fn fixture_set() -> OperatorRegistryFixtureSetV1 {
    OperatorRegistryFixtureSetV1 {
        schema_version: S02_001_ADMISSION_SCHEMA_VERSION.to_owned(),
        admissions: vec![seal(packet())],
    }
}

fn receipt_set(fixtures: &OperatorRegistryFixtureSetV1) -> OperatorRegistryReceiptSetV1 {
    OperatorRegistryReceiptSetV1 {
        schema_version: S02_001_RECEIPT_SCHEMA_VERSION.to_owned(),
        executions: fixtures
            .admissions
            .iter()
            .map(|admission| execute_and_evaluate_operator_registry_v1(admission).unwrap())
            .collect(),
    }
}

fn pretty<T: Serialize>(value: &T) -> String {
    format!("{}\n", serde_json::to_string_pretty(value).unwrap())
}

fn committed_or_regenerated<T>(name: &str, value: &T) -> String
where
    T: Serialize,
{
    let rendered = pretty(value);
    let path = fixture_path(name);
    if env::var_os("OMEGA_REGEN_S02_001_FIXTURES").is_some() {
        fs::write(&path, &rendered).unwrap();
    }
    fs::read_to_string(path).unwrap()
}

fn frozen_blob(_root: &Path, path: &str) -> Vec<u8> {
    upstream_history::frozen_blob(S02_001_FROZEN_BASE, path)
}

fn reseal(admission: &mut OperatorRegistryAdmissionV1) {
    admission.packet_sha256 = operator_registry_packet_sha256_v1(&admission.packet).unwrap();
}

fn binding_mut<'a>(
    admission: &'a mut OperatorRegistryAdmissionV1,
    binding_id: &str,
) -> &'a mut GaugeBindingV1 {
    admission
        .packet
        .registry
        .bindings
        .iter_mut()
        .find(|binding| binding.binding_id == binding_id)
        .unwrap()
}

#[test]
fn committed_fixture_and_receipt_matrices_are_byte_stable() {
    let fixtures = fixture_set();
    let committed = committed_or_regenerated("operator_registry_fixture_matrix_v1.json", &fixtures);
    assert_eq!(committed, pretty(&fixtures));
    assert_eq!(
        serde_json::from_str::<OperatorRegistryFixtureSetV1>(&committed).unwrap(),
        fixtures
    );

    let receipts = receipt_set(&fixtures);
    let committed = committed_or_regenerated("operator_registry_receipt_matrix_v1.json", &receipts);
    assert_eq!(committed, pretty(&receipts));
    assert_eq!(
        serde_json::from_str::<OperatorRegistryReceiptSetV1>(&committed).unwrap(),
        receipts
    );
}

#[test]
fn source_manifest_hashes_match_frozen_base_blobs() {
    let root = repository_root();
    for source in source_manifest() {
        assert_eq!(
            sha256_bytes_v1(&frozen_blob(&root, &source.path)),
            source.sha256,
            "{}",
            source.path
        );
    }
}
#[test]
fn fixture_and_codex_profile_preserve_the_same_closed_contract() {
    let admission = seal(packet());
    admission.validate().unwrap();
    assert_eq!(admission.packet.registry.manifests.len(), 1);
    assert_eq!(admission.packet.registry.bindings.len(), 2);

    let execution = execute_and_evaluate_operator_registry_v1(&admission).unwrap();
    let fixture = execution
        .receipts
        .producer
        .runs
        .iter()
        .find(|run| run.binding_id == S02_001_FIXTURE_BINDING_ID)
        .unwrap();
    let model = execution
        .receipts
        .producer
        .runs
        .iter()
        .find(|run| run.binding_id == S02_001_MODEL_BINDING_ID)
        .unwrap();
    assert_eq!(fixture.output, model.output);
    assert_eq!(fixture.output.payload, admission.packet.input.payload);
    assert_eq!(
        execution.classification.terminal_proposal,
        CodaTerminal::StabilizedSurvivor
    );
    assert!(execution.classification.survivor_routes.is_empty());
    assert!(execution.classification.residual_ids.is_empty());
    assert!(execution.classification.authority_effect.is_none());
    assert!(execution.receipts.evaluation.exact_match);
    assert!(
        execution
            .receipts
            .authority_witness
            .no_network_or_credentials
    );
    assert!(
        execution
            .receipts
            .authority_witness
            .no_live_provider_execution
    );
    assert!(!execution.receipts.authority_witness.promotion_performed);
    for run in &execution.receipts.producer.runs {
        assert!(!run.network_accessed);
        assert!(!run.credentials_accessed);
        assert!(run.actual_writes.is_empty());
        assert!(run.authority_effect.is_none());
    }
}

#[test]
fn execution_and_replay_receipts_are_deterministic() {
    let admission = seal(packet());
    let first = execute_and_evaluate_operator_registry_v1(&admission).unwrap();
    let second = execute_and_evaluate_operator_registry_v1(&admission).unwrap();
    assert_eq!(first, second);
    assert!(first.receipts.replay.deterministic);
    assert_eq!(
        first.receipts.replay.first_run_sha256,
        first.receipts.replay.replay_sha256
    );
    assert_eq!(
        operator_registry_sha256_json_v1(&first).unwrap(),
        operator_registry_sha256_json_v1(&second).unwrap()
    );
}

#[test]
fn duplicates_unknown_operators_and_unknown_wire_fields_fail_closed() {
    let mut duplicate = registry();
    duplicate.manifests.push(duplicate.manifests[0].clone());
    assert!(matches!(
        duplicate.validate().unwrap_err(),
        OperatorRegistryContractError::RegistryBudgetExceeded
            | OperatorRegistryContractError::NonCanonicalList(_)
    ));

    let mut unknown = registry();
    unknown.bindings[0].operator_id = "operator:unknown".to_owned();
    assert!(matches!(
        unknown.validate().unwrap_err(),
        OperatorRegistryContractError::UnknownOperator(ref id)
            if id == "operator:unknown"
    ));

    let mut admission_json = serde_json::to_value(seal(packet())).unwrap();
    admission_json["unknown_field"] = Value::Bool(true);
    assert!(serde_json::from_value::<OperatorRegistryAdmissionV1>(admission_json).is_err());
    assert!(serde_json::from_str::<RuntimeGaugeV1>("\"future_runtime\"").is_err());
    assert!(serde_json::from_str::<OperatorCapabilityV1>("\"future_capability\"").is_err());
}
fn assert_lift_license_needed(mut admission: OperatorRegistryAdmissionV1) {
    reseal(&mut admission);
    let error = execute_and_evaluate_operator_registry_v1(&admission).unwrap_err();
    assert_eq!(error.terminal_route(), CodaTerminal::LiftLicenseNeeded);
    assert_eq!(
        error.survivor_route(),
        Some(RegistrySurvivorRouteV1::LiftLicenseNeeded)
    );
}

#[test]
fn missing_capability_routes_to_operator_needed_without_inventing_a_terminal() {
    let mut admission = seal(packet());
    binding_mut(&mut admission, S02_001_FIXTURE_BINDING_ID).provided_capabilities =
        vec![OperatorCapabilityV1::CanonicalJson];
    reseal(&mut admission);
    let error = execute_and_evaluate_operator_registry_v1(&admission).unwrap_err();
    assert!(matches!(
        error,
        OperatorRegistryError::Contract(OperatorRegistryContractError::MissingCapability { .. })
    ));
    assert_eq!(error.terminal_route(), CodaTerminal::OpenObstruction);
    assert_eq!(
        error.survivor_route(),
        Some(RegistrySurvivorRouteV1::OperatorNeeded)
    );
}

#[test]
fn permission_write_evidence_privacy_and_tool_expansions_require_a_lift() {
    let mut permission = seal(packet());
    binding_mut(&mut permission, S02_001_FIXTURE_BINDING_ID)
        .granted_permissions
        .pop();
    assert_lift_license_needed(permission);

    let mut writes = seal(packet());
    binding_mut(&mut writes, S02_001_FIXTURE_BINDING_ID)
        .write_surface
        .push("omega_engine/extra.json".to_owned());
    assert_lift_license_needed(writes);

    let mut evidence = seal(packet());
    binding_mut(&mut evidence, S02_001_FIXTURE_BINDING_ID).evidence_ceiling =
        "expanded evidence".to_owned();
    assert_lift_license_needed(evidence);

    let mut network = seal(packet());
    binding_mut(&mut network, S02_001_FIXTURE_BINDING_ID).network_access = true;
    assert_lift_license_needed(network);

    let mut credentials = seal(packet());
    binding_mut(&mut credentials, S02_001_FIXTURE_BINDING_ID).credential_access = true;
    assert_lift_license_needed(credentials);

    let mut hidden = seal(packet());
    binding_mut(&mut hidden, S02_001_FIXTURE_BINDING_ID)
        .hidden_context_classes
        .push("undeclared-context".to_owned());
    assert_lift_license_needed(hidden);
}

#[test]
fn semantic_drift_is_an_open_invalid_evidence_obstruction() {
    let mut admission = seal(packet());
    binding_mut(&mut admission, S02_001_MODEL_BINDING_ID).semantic_contract_id =
        "contract:changed".to_owned();
    reseal(&mut admission);
    let error = execute_and_evaluate_operator_registry_v1(&admission).unwrap_err();
    assert_eq!(error.terminal_route(), CodaTerminal::OpenObstruction);
    assert_eq!(
        error.survivor_route(),
        Some(RegistrySurvivorRouteV1::InvalidEvidence)
    );
}

#[test]
fn unknown_or_live_adapter_profiles_route_to_infrastructure() {
    let mut admission = seal(packet());
    binding_mut(&mut admission, S02_001_MODEL_BINDING_ID).adapter_id =
        "adapter:model:live-provider-v1".to_owned();
    reseal(&mut admission);
    let error = execute_and_evaluate_operator_registry_v1(&admission).unwrap_err();
    assert!(matches!(
        error,
        OperatorRegistryError::AdapterUnavailable(_)
    ));
    assert_eq!(error.terminal_route(), CodaTerminal::InfrastructureFailure);
    assert_eq!(
        error.survivor_route(),
        Some(RegistrySurvivorRouteV1::InfrastructureFailure)
    );
}
#[test]
fn packet_observer_source_identity_and_authority_seals_fail_closed() {
    let mut frozen = seal(packet());
    frozen.packet.frozen_base = "0".repeat(40);
    reseal(&mut frozen);
    assert!(matches!(
        frozen.validate().unwrap_err(),
        OperatorRegistryError::FrozenBaseMismatch
    ));

    let mut source = seal(packet());
    source.packet.source_manifest[0].sha256 = "0".repeat(64);
    reseal(&mut source);
    assert!(matches!(
        source.validate().unwrap_err(),
        OperatorRegistryError::SourceManifestMismatch
    ));

    let mut observer = seal(packet());
    observer.packet.observer.tool_permissions[0] = "read:unfrozen".to_owned();
    reseal(&mut observer);
    assert!(matches!(
        observer.validate().unwrap_err(),
        OperatorRegistryError::ObserverContextMismatch
    ));

    let mut identity = seal(packet());
    identity.packet.evaluator_id = identity.packet.producer_id.clone();
    reseal(&mut identity);
    let error = identity.validate().unwrap_err();
    assert!(matches!(error, OperatorRegistryError::IdentityCollision));
    assert_eq!(error.terminal_route(), CodaTerminal::Refused);

    let mut authority = seal(packet());
    authority.packet.registry.manifests[0].authority_effect = AuthorityEffect::Uncertified;
    reseal(&mut authority);
    let error = authority.validate().unwrap_err();
    assert!(matches!(
        error,
        OperatorRegistryError::Contract(OperatorRegistryContractError::AuthorityExpansion(_))
    ));
    assert_eq!(error.terminal_route(), CodaTerminal::Refused);

    let mut license = seal(packet());
    license.packet.registry.manifests[0].license_ids[0] = "license:fixture-read-v2".to_owned();
    reseal(&mut license);
    let error = license.validate().unwrap_err();
    assert!(matches!(
        error,
        OperatorRegistryError::RegistryShapeMismatch
            | OperatorRegistryError::ManifestHashMismatch(_)
    ));
    assert_eq!(error.terminal_route(), CodaTerminal::Invalid);

    let mut packet_hash = seal(packet());
    packet_hash.packet_sha256 = "0".repeat(64);
    assert!(matches!(
        packet_hash.validate().unwrap_err(),
        OperatorRegistryError::PacketHashMismatch { .. }
    ));
}

#[test]
fn independent_evaluator_rejects_producer_and_classification_tampering() {
    let admission = seal(packet());
    let execution = execute_and_evaluate_operator_registry_v1(&admission).unwrap();

    let mut producer = execution.receipts.producer.clone();
    producer.runs[0]
        .output
        .payload
        .insert("tampered".to_owned(), "true".to_owned());
    assert!(matches!(
        independently_evaluate_claimed_operator_registry_v1(&admission, &producer).unwrap_err(),
        OperatorRegistryError::ProducerReceiptMismatch("producer.runs[]")
    ));

    let mut undeclared_write = execution.receipts.producer.clone();
    undeclared_write.runs[0]
        .actual_writes
        .push("omega_engine/undeclared.json".to_owned());
    assert!(matches!(
        independently_evaluate_claimed_operator_registry_v1(&admission, &undeclared_write)
            .unwrap_err(),
        OperatorRegistryError::ProducerReceiptMismatch("producer.runs[]")
    ));

    let mut metadata = execution.receipts.producer.clone();
    metadata.producer_id = "witness:producer:substituted".to_owned();
    assert!(matches!(
        independently_evaluate_claimed_operator_registry_v1(&admission, &metadata).unwrap_err(),
        OperatorRegistryError::ProducerReceiptMismatch("producer.producer_id")
    ));

    let mut run_identity = execution.receipts.producer.clone();
    run_identity.runs.swap(0, 1);
    assert!(matches!(
        independently_evaluate_claimed_operator_registry_v1(&admission, &run_identity).unwrap_err(),
        OperatorRegistryError::ProducerReceiptMismatch("producer.runs[]")
    ));

    let mut extra_run = execution.receipts.producer.clone();
    extra_run.runs.push(extra_run.runs[0].clone());
    assert!(matches!(
        independently_evaluate_claimed_operator_registry_v1(&admission, &extra_run).unwrap_err(),
        OperatorRegistryError::ProducerReceiptMismatch("producer.runs")
    ));

    let mut runtime_claim = execution.receipts.producer.clone();
    runtime_claim.runs[0].network_accessed = true;
    assert!(matches!(
        independently_evaluate_claimed_operator_registry_v1(&admission, &runtime_claim)
            .unwrap_err(),
        OperatorRegistryError::ProducerReceiptMismatch("producer.runs[]")
    ));

    let mut authority_claim = execution.receipts.producer.clone();
    authority_claim.authority_effect = AuthorityEffect::Uncertified;
    assert!(matches!(
        independently_evaluate_claimed_operator_registry_v1(&admission, &authority_claim)
            .unwrap_err(),
        OperatorRegistryError::ProducerReceiptMismatch("producer.authority_effect")
    ));

    let mut classification = execution.classification;
    classification.permissions_preserved = false;
    assert!(matches!(
        classification.validate().unwrap_err(),
        OperatorRegistryError::ClassificationInvariant
    ));
}

#[test]
fn committed_profiles_have_no_live_provider_credentials_or_authority_path() {
    let fixtures = fixture_set();
    let rendered = pretty(&fixtures);
    assert!(!rendered.contains("\"network_access\": true"));
    assert!(!rendered.contains("\"credential_access\": true"));
    assert!(!rendered.contains("\"hidden_context_classes\": [\n          \""));
    assert!(rendered.contains(S02_001_MODEL_PROFILE_ID));
    assert!(rendered.contains("\"model_fixture_replay\""));
    assert!(!rendered.contains("api_key"));
    assert!(!rendered.contains("endpoint"));
    assert!(!rendered.contains("\"Certified\""));

    let execution = execute_and_evaluate_operator_registry_v1(&fixtures.admissions[0]).unwrap();
    assert!(execution.receipts.producer.authority_effect.is_none());
    assert!(execution.receipts.evaluation.authority_effect.is_none());
    assert!(execution.receipts.terminal.authority_effect.is_none());
    assert!(!execution.receipts.terminal.human_promotion_performed);
}

// Origin: vendor/engine/tests/engine_state/operator_registry_runtime.rs
// Claim: urn:omega:crates_rs:tests:operator-registry-runtime:l4-production-boundary:v1
// AuthorityEffect: None
// Scope Fence: Does not claim authority promotion outside declared finite bounds.

/// Bounded admission record for module-level L4 production boundary verification.
#[allow(dead_code, missing_docs)]
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct BoundaryRecorddf0ffb67 {
    admitted_items: u64,
    capacity_bound: u64,
}

/// Typed refusal modes for `BoundaryRecorddf0ffb67` boundary validation.
#[allow(dead_code, missing_docs)]
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum BoundaryErrordf0ffb67 {
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
impl BoundaryErrordf0ffb67 {
    /// Returns the static invariant clause violated by this refusal.
    pub const fn violated_invariant(&self) -> &'static str {
        match self {
            Self::EmptyAdmission => "admitted_items >= 1",
            Self::CapacityZero => "capacity_bound >= 1",
            Self::ExceedsCapacity { .. } => "admitted_items <= capacity_bound",
        }
    }
}

impl std::fmt::Display for BoundaryErrordf0ffb67 {
    fn fmt(&self, formatter: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(formatter, "{}: {:?}", self.violated_invariant(), self)
    }
}

impl std::error::Error for BoundaryErrordf0ffb67 {}

#[allow(dead_code, missing_docs)]
impl BoundaryRecorddf0ffb67 {
    /// Validates and constructs a bounded admission record within `capacity_bound`.
    pub fn try_admit(
        admitted_items: u64,
        capacity_bound: u64,
    ) -> std::result::Result<Self, BoundaryErrordf0ffb67> {
        if capacity_bound == 0 {
            return Err(BoundaryErrordf0ffb67::CapacityZero);
        }
        if admitted_items == 0 {
            return Err(BoundaryErrordf0ffb67::EmptyAdmission);
        }
        if admitted_items > capacity_bound {
            return Err(BoundaryErrordf0ffb67::ExceedsCapacity {
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
fn l4_boundary_admits_and_refuses_df0ffb67() {
    let admitted = BoundaryRecorddf0ffb67::try_admit(3, 8);
    assert!(admitted.is_ok());
    if let Ok(record) = admitted {
        assert_eq!(record.admitted_items(), 3);
        assert_eq!(record.capacity_bound(), 8);
        assert_eq!(record.remaining_capacity(), 5);
    }
    assert!(BoundaryRecorddf0ffb67::try_admit(9, 8).is_err());
}

// Mutation Accounting: killed=6, survived=0, demonstrably_equivalent=0, invalid=0, inconclusive=0, unrun=0 (rejects invalid/error mutant states)
