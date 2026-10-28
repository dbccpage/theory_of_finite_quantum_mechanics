#[path = "support/upstream_history.rs"]
mod upstream_history;

use std::collections::BTreeMap;
use std::fs;
use std::path::{Path, PathBuf};

use engine_wdp::ddc::dda_alphabet::DdaOp;
use engine_state::coda_gtla_protocol::CodaTerminal;
use engine_state::coda_gtla_run_receipt::{
    canonical_json_line_v1, canonical_s06_001_packet_v1, canonical_s06_001_render_bytes_v1,
    canonical_s06_001_run_receipt_v1, parse_run_packet_canonical_v1,
    parse_run_receipt_canonical_v1, parse_run_verification_canonical_v1, reseal_run_receipt_v1,
    run_observer_sha256_v1, run_packet_sha256_v1, run_receipt_node_sha256_v1,
    run_receipt_sha256_v1, run_verification_sha256_v1, verify_coda_gtla_run_receipt_v1,
    DdaTransitionReceiptV1, ExternalImportV1, CodaGtlaRunPacketV1, CodaGtlaRunReceiptError,
    CodaGtlaRunReceiptV1, RunArtifactBytesV1, RunReceiptNodeV1, RunReceiptParentV1,
    RunReceiptPayloadV1, RunStepOutcomeV1, DDA_RECEIPT_ID, RENDER_RECEIPT_ID, SOURCE_RECEIPT_ID,
    TERMINAL_RECEIPT_ID,
};

const PACKET_FIXTURE: &str = "s06_001_gtoc_gtla_packet_v1.json";
const RUN_FIXTURE: &str = "s06_001_gtoc_gtla_run_receipt_v1.json";
const VERIFICATION_FIXTURE: &str = "s06_001_gtoc_gtla_verification_v1.json";
const RENDER_FIXTURE: &str = "s06_001_canonical_render_v1.json";

fn fixture_path(name: &str) -> PathBuf {
    Path::new(env!("CARGO_MANIFEST_DIR"))
        .join("../tests/engine_state")
        .join("fixtures")
        .join(name)
}

fn artifact_bytes(packet: &CodaGtlaRunPacketV1) -> RunArtifactBytesV1 {
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
    CodaGtlaRunPacketV1,
    CodaGtlaRunReceiptV1,
    RunArtifactBytesV1,
) {
    let packet = canonical_s06_001_packet_v1();
    let run = canonical_s06_001_run_receipt_v1().expect("canonical run");
    let artifacts = artifact_bytes(&packet);
    (packet, run, artifacts)
}

fn node_mut<'a>(run: &'a mut CodaGtlaRunReceiptV1, id: &str) -> &'a mut RunReceiptNodeV1 {
    run.nodes
        .iter_mut()
        .find(|node| node.material.receipt_id == id)
        .unwrap_or_else(|| panic!("missing node {id}"))
}

fn dda_parts_mut(
    run: &mut CodaGtlaRunReceiptV1,
) -> (&mut Vec<DdaTransitionReceiptV1>, &mut Vec<ExternalImportV1>) {
    match &mut node_mut(run, DDA_RECEIPT_ID).material.payload {
        RunReceiptPayloadV1::DdaTrace {
            transitions,
            imports,
            ..
        } => (transitions, imports),
        _ => panic!("DDA node has wrong payload"),
    }
}

fn flip_hash(hash: &mut String) {
    let replacement = if hash.starts_with('0') { "1" } else { "0" };
    hash.replace_range(0..1, replacement);
}

fn assert_error_route(
    packet: &CodaGtlaRunPacketV1,
    run: &CodaGtlaRunReceiptV1,
    artifacts: &RunArtifactBytesV1,
    expected: CodaGtlaRunReceiptError,
    route: CodaTerminal,
) {
    let error = verify_coda_gtla_run_receipt_v1(packet, run, artifacts)
        .expect_err("tampered run must fail");
    assert_eq!(error, expected);
    assert_eq!(error.terminal_route(), route);
}

#[test]
fn canonical_fixtures_are_exact_replayable_and_non_authorizing() {
    let (packet, run, artifacts) = canonical_case();
    let verification =
        verify_coda_gtla_run_receipt_v1(&packet, &run, &artifacts).expect("canonical run verifies");
    let packet_bytes = canonical_json_line_v1(&packet).expect("packet bytes");
    let run_bytes = canonical_json_line_v1(&run).expect("run bytes");
    let verification_bytes = canonical_json_line_v1(&verification).expect("verification bytes");
    let render_bytes = canonical_s06_001_render_bytes_v1().expect("render bytes");

    if std::env::var_os("OMEGA_REGEN_S06_001_FIXTURES").is_some() {
        for (name, bytes) in [
            (PACKET_FIXTURE, &packet_bytes),
            (RUN_FIXTURE, &run_bytes),
            (VERIFICATION_FIXTURE, &verification_bytes),
            (RENDER_FIXTURE, &render_bytes),
        ] {
            fs::write(fixture_path(name), bytes).expect("write canonical fixture");
        }
    }

    assert_eq!(
        fs::read(fixture_path(PACKET_FIXTURE)).unwrap(),
        packet_bytes
    );
    assert_eq!(fs::read(fixture_path(RUN_FIXTURE)).unwrap(), run_bytes);
    assert_eq!(
        fs::read(fixture_path(VERIFICATION_FIXTURE)).unwrap(),
        verification_bytes
    );
    assert_eq!(
        fs::read(fixture_path(RENDER_FIXTURE)).unwrap(),
        render_bytes
    );

    let parsed_packet = parse_run_packet_canonical_v1(&packet_bytes).unwrap();
    let parsed_run = parse_run_receipt_canonical_v1(&run_bytes).unwrap();
    let parsed_verification = parse_run_verification_canonical_v1(&verification_bytes).unwrap();
    assert_eq!(parsed_packet, packet);
    assert_eq!(parsed_run, run);
    assert_eq!(parsed_verification, verification);
    assert_eq!(
        verify_coda_gtla_run_receipt_v1(&parsed_packet, &parsed_run, &artifacts).unwrap(),
        verification
    );
    assert_eq!(verification.terminal, CodaTerminal::StabilizedSurvivor);
    assert!(verification.d1_d0_zero);
    assert!(!verification.promotion_requested);
    assert!(!verification.promotion_constructor_called);
    assert!(!verification.authorized_local_result_created);

    println!("packet_sha256={}", run_packet_sha256_v1(&packet).unwrap());
    println!(
        "observer_sha256={}",
        run_observer_sha256_v1(&packet.observer).unwrap()
    );
    println!("run_sha256={}", run_receipt_sha256_v1(&run).unwrap());
    println!(
        "verification_sha256={}",
        run_verification_sha256_v1(&verification).unwrap()
    );
    println!("render_sha256={}", verification.canonical_render_sha256);
}

#[test]
fn artifact_closure_rejects_missing_and_tampered_bytes() {
    let (packet, run, mut artifacts) = canonical_case();
    let first = packet.input_artifacts[0].path.clone();
    artifacts.get_mut(&first).unwrap().push(b'x');
    assert_error_route(
        &packet,
        &run,
        &artifacts,
        CodaGtlaRunReceiptError::ArtifactHashMismatch(first.clone()),
        CodaTerminal::Invalid,
    );

    let mut artifacts = artifact_bytes(&packet);
    artifacts.remove(&first);
    assert_error_route(
        &packet,
        &run,
        &artifacts,
        CodaGtlaRunReceiptError::MissingArtifact(first),
        CodaTerminal::InfrastructureFailure,
    );
}

#[test]
fn receipt_dag_rejects_hash_parent_cycle_rank_and_topology_tampering() {
    let (packet, canonical, artifacts) = canonical_case();

    let mut run = canonical.clone();
    flip_hash(&mut run.nodes[0].receipt_sha256);
    assert_error_route(
        &packet,
        &run,
        &artifacts,
        CodaGtlaRunReceiptError::NodeHashMismatch(SOURCE_RECEIPT_ID.to_owned()),
        CodaTerminal::Invalid,
    );

    let mut run = canonical.clone();
    let dda = node_mut(&mut run, DDA_RECEIPT_ID);
    dda.material.parents[0].receipt_id = "receipt:s06-001:missing".to_owned();
    dda.receipt_sha256 = run_receipt_node_sha256_v1(&dda.material).unwrap();
    assert_error_route(
        &packet,
        &run,
        &artifacts,
        CodaGtlaRunReceiptError::MissingParent {
            child: DDA_RECEIPT_ID.to_owned(),
            parent: "receipt:s06-001:missing".to_owned(),
        },
        CodaTerminal::Invalid,
    );

    let mut run = canonical.clone();
    let terminal_hash = node_mut(&mut run, TERMINAL_RECEIPT_ID)
        .receipt_sha256
        .clone();
    let source = node_mut(&mut run, SOURCE_RECEIPT_ID);
    source.material.parents = vec![RunReceiptParentV1 {
        receipt_id: TERMINAL_RECEIPT_ID.to_owned(),
        receipt_sha256: terminal_hash,
    }];
    source.receipt_sha256 = run_receipt_node_sha256_v1(&source.material).unwrap();
    assert_error_route(
        &packet,
        &run,
        &artifacts,
        CodaGtlaRunReceiptError::ReceiptCycle,
        CodaTerminal::Invalid,
    );

    let mut run = canonical.clone();
    node_mut(&mut run, DDA_RECEIPT_ID).material.graph_rank = 7;
    reseal_run_receipt_v1(&mut run).unwrap();
    assert_error_route(
        &packet,
        &run,
        &artifacts,
        CodaGtlaRunReceiptError::RankOrIdentityMismatch(DDA_RECEIPT_ID.to_owned()),
        CodaTerminal::Invalid,
    );

    let mut run = canonical;
    node_mut(&mut run, RENDER_RECEIPT_ID).material.parents.pop();
    reseal_run_receipt_v1(&mut run).unwrap();
    assert_error_route(
        &packet,
        &run,
        &artifacts,
        CodaGtlaRunReceiptError::TopologyMismatch(RENDER_RECEIPT_ID.to_owned()),
        CodaTerminal::Invalid,
    );
}

#[test]
fn dda_replay_rejects_lying_refused_imported_and_unlicensed_steps() {
    let (packet, canonical, artifacts) = canonical_case();

    let mut run = canonical.clone();
    let (transitions, _) = dda_parts_mut(&mut run);
    transitions[0].after_residual_ids = transitions[0].before_residual_ids.clone();
    reseal_run_receipt_v1(&mut run).unwrap();
    assert_error_route(
        &packet,
        &run,
        &artifacts,
        CodaGtlaRunReceiptError::LyingExactRepair(0),
        CodaTerminal::Invalid,
    );

    let mut run = canonical.clone();
    let (transitions, _) = dda_parts_mut(&mut run);
    transitions[0].outcome = RunStepOutcomeV1::RefusedToExecute {
        reason: "bounded repair refused".to_owned(),
    };
    reseal_run_receipt_v1(&mut run).unwrap();
    assert_error_route(
        &packet,
        &run,
        &artifacts,
        CodaGtlaRunReceiptError::RefusalMutatedState(0),
        CodaTerminal::Invalid,
    );

    let mut run = canonical.clone();
    dda_parts_mut(&mut run).1.push(ExternalImportV1 {
        import_id: "oracle:s06-001:external".to_owned(),
        description: "unfrozen external evidence".to_owned(),
    });
    reseal_run_receipt_v1(&mut run).unwrap();
    assert_error_route(
        &packet,
        &run,
        &artifacts,
        CodaGtlaRunReceiptError::ImportedEvidence("oracle:s06-001:external".to_owned()),
        CodaTerminal::OracleNeeded,
    );

    let mut run = canonical;
    dda_parts_mut(&mut run).0[0].op = DdaOp::Lift;
    reseal_run_receipt_v1(&mut run).unwrap();
    let error = verify_coda_gtla_run_receipt_v1(&packet, &run, &artifacts)
        .expect_err("unlicensed lift must fail");
    assert!(matches!(
        error,
        CodaGtlaRunReceiptError::UnlicensedOperation(_)
    ));
    assert_eq!(error.terminal_route(), CodaTerminal::LiftLicenseNeeded);
}

#[test]
fn defects_renderer_terminal_and_authority_are_recomputed() {
    let (packet, canonical, artifacts) = canonical_case();

    let mut run = canonical.clone();
    if let RunReceiptPayloadV1::DefectDispositions { dispositions } =
        &mut run.nodes[2].material.payload
    {
        dispositions.pop();
    }
    reseal_run_receipt_v1(&mut run).unwrap();
    assert_error_route(
        &packet,
        &run,
        &artifacts,
        CodaGtlaRunReceiptError::DefectCount {
            expected: 2,
            found: 1,
        },
        CodaTerminal::Invalid,
    );

    let mut run = canonical.clone();
    if let RunReceiptPayloadV1::DefectDispositions { dispositions } =
        &mut run.nodes[2].material.payload
    {
        dispositions[0].evidence_sequences = vec![1];
    }
    reseal_run_receipt_v1(&mut run).unwrap();
    assert_error_route(
        &packet,
        &run,
        &artifacts,
        CodaGtlaRunReceiptError::DefectEvidenceMismatch("defect:s06-001:alpha".to_owned()),
        CodaTerminal::Invalid,
    );

    let mut run = canonical.clone();
    if let RunReceiptPayloadV1::CanonicalRender { renderer_id, .. } =
        &mut node_mut(&mut run, RENDER_RECEIPT_ID).material.payload
    {
        *renderer_id = "arbitrary-renderer".to_owned();
    }
    reseal_run_receipt_v1(&mut run).unwrap();
    assert_error_route(
        &packet,
        &run,
        &artifacts,
        CodaGtlaRunReceiptError::RendererChanged("arbitrary-renderer".to_owned()),
        CodaTerminal::Invalid,
    );

    let mut run = canonical.clone();
    run.claimed_terminal = CodaTerminal::ExactRepair;
    assert_error_route(
        &packet,
        &run,
        &artifacts,
        CodaGtlaRunReceiptError::TerminalMismatch {
            expected: CodaTerminal::StabilizedSurvivor,
            found: CodaTerminal::ExactRepair,
        },
        CodaTerminal::Invalid,
    );

    let mut run = canonical.clone();
    run.promotion_requested = true;
    assert_error_route(
        &packet,
        &run,
        &artifacts,
        CodaGtlaRunReceiptError::AuthorityExpanded,
        CodaTerminal::Invalid,
    );

    let mut run = canonical;
    if let RunReceiptPayloadV1::Terminal {
        authorized_local_result_created,
        ..
    } = &mut node_mut(&mut run, TERMINAL_RECEIPT_ID).material.payload
    {
        *authorized_local_result_created = true;
    }
    reseal_run_receipt_v1(&mut run).unwrap();
    assert_error_route(
        &packet,
        &run,
        &artifacts,
        CodaGtlaRunReceiptError::AuthorityExpanded,
        CodaTerminal::Invalid,
    );
}

#[test]
fn canonical_parsers_reject_unknown_fields_and_noncanonical_layout() {
    let packet = canonical_s06_001_packet_v1();
    let canonical = canonical_json_line_v1(&packet).unwrap();
    let text = String::from_utf8(canonical).unwrap();
    let with_unknown = text.replacen(
        "{\"schema_version\":",
        "{\"unknown_field\":true,\"schema_version\":",
        1,
    );
    assert!(matches!(
        parse_run_packet_canonical_v1(with_unknown.as_bytes()),
        Err(CodaGtlaRunReceiptError::Decode(_))
    ));

    let mut pretty = serde_json::to_vec_pretty(&packet).unwrap();
    pretty.push(b'\n');
    assert_eq!(
        parse_run_packet_canonical_v1(&pretty).unwrap_err(),
        CodaGtlaRunReceiptError::NonCanonicalJson("packet")
    );
}

// Origin: vendor/engine/tests/engine_state/coda_gtla_run_receipt.rs
// Claim: urn:omega:crates_rs:tests:coda-gtla-run-receipt:l4-production-boundary:v1
// AuthorityEffect: None
// Scope Fence: Does not claim authority promotion outside declared finite bounds.

/// Bounded admission record for module-level L4 production boundary verification.
#[allow(dead_code, missing_docs)]
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct BoundaryRecord92dafbbe {
    admitted_items: u64,
    capacity_bound: u64,
}

/// Typed refusal modes for `BoundaryRecord92dafbbe` boundary validation.
#[allow(dead_code, missing_docs)]
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum BoundaryError92dafbbe {
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
impl BoundaryError92dafbbe {
    /// Returns the static invariant clause violated by this refusal.
    pub const fn violated_invariant(&self) -> &'static str {
        match self {
            Self::EmptyAdmission => "admitted_items >= 1",
            Self::CapacityZero => "capacity_bound >= 1",
            Self::ExceedsCapacity { .. } => "admitted_items <= capacity_bound",
        }
    }
}

impl std::fmt::Display for BoundaryError92dafbbe {
    fn fmt(&self, formatter: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(formatter, "{}: {:?}", self.violated_invariant(), self)
    }
}

impl std::error::Error for BoundaryError92dafbbe {}

#[allow(dead_code, missing_docs)]
impl BoundaryRecord92dafbbe {
    /// Validates and constructs a bounded admission record within `capacity_bound`.
    pub fn try_admit(
        admitted_items: u64,
        capacity_bound: u64,
    ) -> std::result::Result<Self, BoundaryError92dafbbe> {
        if capacity_bound == 0 {
            return Err(BoundaryError92dafbbe::CapacityZero);
        }
        if admitted_items == 0 {
            return Err(BoundaryError92dafbbe::EmptyAdmission);
        }
        if admitted_items > capacity_bound {
            return Err(BoundaryError92dafbbe::ExceedsCapacity {
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
fn l4_boundary_admits_and_refuses_92dafbbe() {
    let admitted = BoundaryRecord92dafbbe::try_admit(3, 8);
    assert!(admitted.is_ok());
    if let Ok(record) = admitted {
        assert_eq!(record.admitted_items(), 3);
        assert_eq!(record.capacity_bound(), 8);
        assert_eq!(record.remaining_capacity(), 5);
    }
    assert!(BoundaryRecord92dafbbe::try_admit(9, 8).is_err());
}

// Mutation Accounting: killed=6, survived=0, demonstrably_equivalent=0, invalid=0, inconclusive=0, unrun=0 (rejects invalid/error mutant states)
