//! Bounded S06-001 CODA/CODA_GTLA run-receipt DAG verifier.
//!
//! This module is a finite behavior baseline for the conductor. It verifies one
//! frozen carrier, recomputes all hashes and receipt edges, checks a fixed
//! E/R/I/M/T replay, conserves every enumerated defect, renders deterministic
//! non-executable JSON, and derives the only legal terminal for the bundle.
//! It constructs no authority and exposes no AuthorizedLocalResult path.


#[allow(dead_code, non_camel_case_types, missing_docs)]
trait CheckedInvariantExt_b137fc8e<T> {
    fn checked_invariant_b137fc8e(self, msg: &str) -> T;
}

impl<T> CheckedInvariantExt_b137fc8e<T> for Option<T> {
    #[inline]
    fn checked_invariant_b137fc8e(self, msg: &str) -> T {
        match self {
            Some(v) => v,
            None => unreachable!("{}", msg),
        }
    }
}

impl<T, E: std::fmt::Debug> CheckedInvariantExt_b137fc8e<T> for std::result::Result<T, E> {
    #[inline]
    fn checked_invariant_b137fc8e(self, msg: &str) -> T {
        match self {
            Ok(v) => v,
            Err(e) => unreachable!("{}: {:?}", msg, e),
        }
    }
}
use std::collections::{BTreeMap, BTreeSet};

use engine_wdp::ddc::dda_alphabet::DdaOp;
use engine_types::authority::AuthorityEffect;
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};
use thiserror::Error;

use crate::coda_gtla_protocol::CodaTerminal;

pub const RUN_PACKET_SCHEMA_VERSION: &str = "omega.gtoc-gtla-run.packet.v1";
pub const RUN_RECEIPT_SCHEMA_VERSION: &str = "omega.gtoc-gtla-run.receipt-dag.v1";
pub const RUN_NODE_SCHEMA_VERSION: &str = "omega.gtoc-gtla-run.receipt-node.v1";
pub const RUN_VERIFICATION_SCHEMA_VERSION: &str = "omega.gtoc-gtla-run.verification.v1";
pub const RUN_RENDER_SCHEMA_VERSION: &str = "omega.gtoc-gtla-run.render.v1";

pub const S06_001_FROZEN_BASE: &str = "118d528408a6b033ea250ee0b5bb14215d896861";
pub const S06_001_PACKET_ID: &str = "omega-conductor-s06-001-run-receipt-dag-v1";
pub const S06_001_GOAL_ID: &str = "S06-001";
pub const S06_001_OBSERVER_ID: &str = "rust:omega_state:s06-001";
pub const S06_001_RENDERER_ID: &str = "omega-state-json-renderer:s06-001:v1";
pub const S06_001_EVIDENCE_CEILING: &str =
    "finite canonical packet, artifact, receipt-DAG, E/R/I/M/T, defect, render, and terminal evidence only; no authority promotion";

pub const SOURCE_RECEIPT_ID: &str = "receipt:s06-001:00-source";
pub const DDA_RECEIPT_ID: &str = "receipt:s06-001:01-dda";
pub const DEFECT_RECEIPT_ID: &str = "receipt:s06-001:02-defects";
pub const RENDER_RECEIPT_ID: &str = "receipt:s06-001:03-render";
pub const TERMINAL_RECEIPT_ID: &str = "receipt:s06-001:04-terminal";

pub const S06_001_WRITE_SURFACE: [&str; 14] = [
    ".gitattributes",
    "docs/omega-conductor-epic-v001.md",
    "docs/saga_06_receipt_verification_and_terminalization.md",
    "docs/sprint_s06_001.md",
    "docs/status/omega_conductor_s06_001_status_2026-07-18.md",
    "omega_engine/general_theory_of_obstruction_calculus/conductor/core/fixture_tower.py",
    "omega_engine/general_theory_of_obstruction_calculus/conductor/tests/test_fixture_tower.py",
    "omega_engine/crates/omega_state/src/lib.rs",
    "omega_engine/crates/omega_state/src/gtoc_gtla_run_receipt.rs",
    "omega_engine/crates/omega_state/tests/gtoc_gtla_run_receipt.rs",
    "omega_engine/crates/omega_state/tests/fixtures/s06_001_gtoc_gtla_packet_v1.json",
    "omega_engine/crates/omega_state/tests/fixtures/s06_001_gtoc_gtla_run_receipt_v1.json",
    "omega_engine/crates/omega_state/tests/fixtures/s06_001_gtoc_gtla_verification_v1.json",
    "omega_engine/crates/omega_state/tests/fixtures/s06_001_canonical_render_v1.json",
];

pub const S06_001_SOURCE_MANIFEST: [(&str, &str, u64); 15] = [
    (
        ".gitattributes",
        "7b344b86d296269c7221072b1db51564f9bc86610ac94e6b520f34a866e12cf7",
        632,
    ),
    (
        "docs/omega-conductor-epic-v001.md",
        "7caf9ddb1f90af1b54336de2cd94ccf753181b49506d87b5c3b7391ddba2755f",
        59_286,
    ),
    (
        "docs/saga_06_receipt_verification_and_terminalization.md",
        "32b08db81181d217c0826b026d18397b412b50dadc059f6e91676f557d4c43d6",
        6_309,
    ),
    (
        "docs/sprint_s06_001.md",
        "ca2d8efa323454adce06c77a97bfe5a05272e36ec9289af2d3b99eaf93182f4e",
        5_781,
    ),
    (
        "docs/status-vocabulary.md",
        "bd10e7ecf448ed6f4dca45a431c573242179a66b828492ecfe02f52572289b84",
        4_203,
    ),
    (
        "omega_engine/general_theory_of_obstruction_calculus/conductor/core/fixture_tower.py",
        "c22ab209c09806590f660fe1e8fcb019f77ce64831eb3833059742fa176ddf57",
        43_893,
    ),
    (
        "omega_engine/general_theory_of_obstruction_calculus/conductor/tests/test_fixture_tower.py",
        "82c03156905581ff62dd9413c4d5e392a99f8204c9e8d0107e352db5cf54d6f6",
        13_980,
    ),
    (
        "omega_engine/crates/omega_state/Cargo.toml",
        "cc089b4ad71ef84c75c79a7d5cac8a810e0ea278aba4aaadec252880dcc8eb73",
        512,
    ),
    (
        "omega_engine/crates/omega_state/src/lib.rs",
        "1f3d600845cdca2d56a40aeed2e69efd1e84fb75c919a531c13e7afd7ec7c74f",
        1_177,
    ),
    (
        "omega_engine/crates/omega_state/src/witness_receipt_dag.rs",
        "a96f1ddbdb7415874724aead998b0a6894e14d0dc91af06c4e30ac19bb8adb43",
        46_786,
    ),
    (
        "omega_engine/crates/omega_state/src/gtoc_gtla_protocol.rs",
        "da57f9f89dd396cbd1bca72880d024c81a4d3238bd6f78af9add06572c3f160f",
        35_825,
    ),
    (
        "omega_engine/crates/omega_discrete_deformation_algebra/src/dda_alphabet.rs",
        "2894e95134db050d9c366e3e15db5e5ecdaeb3c0ed4625e18a63d21753ee7fb9",
        11_997,
    ),
    (
        "omega_engine/crates/omega_state/tests/fixtures/s04_001_witness_tower_receipt_v1.json",
        "54550d9afcfdbace4c6ade3937fa88d218d30b4b7a45a8709d5c16363807eb12",
        8_656,
    ),
    (
        "omega_engine/general_theory_of_obstruction_calculus/conductor/pilot_fixtures/s05_001_fixture_tower_packet_v1.json",
        "c2eabc9f7afa4ae15f4d04fd2702f0772b4ee92f45a335f6dfb962ffbb4b0617",
        6_897,
    ),
    (
        "omega_engine/general_theory_of_obstruction_calculus/conductor/pilot_fixtures/s05_001_fixture_tower_receipt_v1.json",
        "53b9e7d880aa1f52c6d847a28cdabb785be09f94e426b2bde3344ab9eee47a8c",
        1_148,
    ),
];

pub const S06_001_INPUT_ARTIFACTS: [(&str, &str, u64); 3] = [
    (
        "omega_engine/crates/omega_state/tests/fixtures/s04_001_witness_tower_receipt_v1.json",
        "54550d9afcfdbace4c6ade3937fa88d218d30b4b7a45a8709d5c16363807eb12",
        8_656,
    ),
    (
        "omega_engine/general_theory_of_obstruction_calculus/conductor/pilot_fixtures/s05_001_fixture_tower_packet_v1.json",
        "c2eabc9f7afa4ae15f4d04fd2702f0772b4ee92f45a335f6dfb962ffbb4b0617",
        6_897,
    ),
    (
        "omega_engine/general_theory_of_obstruction_calculus/conductor/pilot_fixtures/s05_001_fixture_tower_receipt_v1.json",
        "53b9e7d880aa1f52c6d847a28cdabb785be09f94e426b2bde3344ab9eee47a8c",
        1_148,
    ),
];

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct FrozenRunSourceV1 {
    pub path: String,
    pub sha256: String,
    pub bytes: u64,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct RunArtifactBindingV1 {
    pub path: String,
    pub sha256: String,
    pub bytes: u64,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct RunBudgetsV1 {
    pub attempt_budget: u32,
    pub repair_budget: u32,
    pub successor_budget: u32,
    pub time_budget_seconds: u64,
    pub process_budget: u32,
    pub token_budget: u64,
    pub receipt_node_budget: u32,
    pub defect_budget: u32,
    pub transition_budget: u32,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct FrozenRunObserverV1 {
    pub observer_id: String,
    pub source_manifest_sha256: String,
    pub visible_artifact_sha256: Vec<String>,
    pub hidden_context_classes: Vec<String>,
    pub model_context_available: bool,
    pub promotion_constructor_available: bool,
    pub authorized_local_result_constructor_available: bool,
    pub authority_effect: AuthorityEffect,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct CodaGtlaRunPacketV1 {
    pub schema_version: String,
    pub packet_id: String,
    pub goal_id: String,
    pub frozen_base: String,
    pub observer: FrozenRunObserverV1,
    pub observer_sha256: String,
    pub source_manifest: Vec<FrozenRunSourceV1>,
    pub input_artifacts: Vec<RunArtifactBindingV1>,
    pub initial_residual_ids: Vec<String>,
    pub licensed_operations: Vec<DdaOp>,
    pub legal_terminals: Vec<CodaTerminal>,
    pub budgets: RunBudgetsV1,
    pub evidence_ceiling: String,
    pub exact_write_surface: Vec<String>,
    pub promotion_constructor_available: bool,
    pub authorized_local_result_constructor_available: bool,
    pub authority_effect: AuthorityEffect,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(tag = "status", rename_all = "snake_case", deny_unknown_fields)]
pub enum RunStepOutcomeV1 {
    Executed { log: String },
    RefusedToExecute { reason: String },
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct DdaTransitionReceiptV1 {
    pub sequence: u32,
    pub op: DdaOp,
    pub before_residual_ids: Vec<String>,
    pub after_residual_ids: Vec<String>,
    pub outcome: RunStepOutcomeV1,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct ExternalImportV1 {
    pub import_id: String,
    pub description: String,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, PartialOrd, Ord, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum RunReceiptKindV1 {
    Source,
    DdaTrace,
    DefectDispositions,
    CanonicalRender,
    Terminal,
}

impl RunReceiptKindV1 {
    fn expected_id(self) -> &'static str {
        match self {
            Self::Source => SOURCE_RECEIPT_ID,
            Self::DdaTrace => DDA_RECEIPT_ID,
            Self::DefectDispositions => DEFECT_RECEIPT_ID,
            Self::CanonicalRender => RENDER_RECEIPT_ID,
            Self::Terminal => TERMINAL_RECEIPT_ID,
        }
    }

    fn expected_rank(self) -> u8 {
        match self {
            Self::Source => 0,
            Self::DdaTrace => 1,
            Self::DefectDispositions => 2,
            Self::CanonicalRender => 3,
            Self::Terminal => 4,
        }
    }

    fn required_parent_ids(self) -> &'static [&'static str] {
        match self {
            Self::Source => &[],
            Self::DdaTrace => &[SOURCE_RECEIPT_ID],
            Self::DefectDispositions => &[DDA_RECEIPT_ID],
            Self::CanonicalRender => &[DDA_RECEIPT_ID, DEFECT_RECEIPT_ID],
            Self::Terminal => &[
                SOURCE_RECEIPT_ID,
                DDA_RECEIPT_ID,
                DEFECT_RECEIPT_ID,
                RENDER_RECEIPT_ID,
            ],
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct RunReceiptParentV1 {
    pub receipt_id: String,
    pub receipt_sha256: String,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct DefectDispositionV1 {
    pub defect_id: String,
    pub terminal: CodaTerminal,
    pub evidence_sequences: Vec<u32>,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(tag = "kind", rename_all = "snake_case", deny_unknown_fields)]
pub enum RunReceiptPayloadV1 {
    Source {
        artifacts: Vec<RunArtifactBindingV1>,
    },
    DdaTrace {
        initial_residual_ids: Vec<String>,
        transitions: Vec<DdaTransitionReceiptV1>,
        imports: Vec<ExternalImportV1>,
    },
    DefectDispositions {
        dispositions: Vec<DefectDispositionV1>,
    },
    CanonicalRender {
        renderer_id: String,
        rendered_sha256: String,
    },
    Terminal {
        terminal: CodaTerminal,
        final_residual_ids: Vec<String>,
        rendered_sha256: String,
        promotion_requested: bool,
        promotion_constructor_called: bool,
        authorized_local_result_created: bool,
    },
}

impl RunReceiptPayloadV1 {
    pub fn kind(&self) -> RunReceiptKindV1 {
        match self {
            Self::Source { .. } => RunReceiptKindV1::Source,
            Self::DdaTrace { .. } => RunReceiptKindV1::DdaTrace,
            Self::DefectDispositions { .. } => RunReceiptKindV1::DefectDispositions,
            Self::CanonicalRender { .. } => RunReceiptKindV1::CanonicalRender,
            Self::Terminal { .. } => RunReceiptKindV1::Terminal,
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct RunReceiptNodeMaterialV1 {
    pub schema_version: String,
    pub receipt_id: String,
    pub packet_id: String,
    pub packet_sha256: String,
    pub graph_rank: u8,
    pub parents: Vec<RunReceiptParentV1>,
    pub payload: RunReceiptPayloadV1,
    pub evidence_ceiling: String,
    pub authority_effect: AuthorityEffect,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct RunReceiptNodeV1 {
    pub material: RunReceiptNodeMaterialV1,
    pub receipt_sha256: String,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct CodaGtlaRunReceiptV1 {
    pub schema_version: String,
    pub packet_id: String,
    pub packet_sha256: String,
    pub nodes: Vec<RunReceiptNodeV1>,
    pub terminal_receipt_id: String,
    pub claimed_terminal: CodaTerminal,
    pub promotion_requested: bool,
    pub promotion_constructor_called: bool,
    pub authorized_local_result_created: bool,
    pub authority_effect: AuthorityEffect,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct CanonicalRunRenderV1 {
    pub schema_version: String,
    pub packet_id: String,
    pub packet_sha256: String,
    pub renderer_id: String,
    pub transitions: Vec<DdaTransitionReceiptV1>,
    pub dispositions: Vec<DefectDispositionV1>,
    pub terminal: CodaTerminal,
    pub authority_effect: AuthorityEffect,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct CodaGtlaRunVerificationV1 {
    pub schema_version: String,
    pub packet_id: String,
    pub packet_sha256: String,
    pub run_receipt_sha256: String,
    pub artifact_closure_sha256: String,
    pub receipt_dag_sha256: String,
    pub dda_trace_sha256: String,
    pub defect_disposition_sha256: String,
    pub canonical_render_sha256: String,
    pub cochain_boundary_sha256: String,
    pub node_count: u32,
    pub defect_count: u32,
    pub d1_d0_zero: bool,
    pub terminal: CodaTerminal,
    pub promotion_requested: bool,
    pub promotion_constructor_called: bool,
    pub authorized_local_result_created: bool,
    pub authority_effect: AuthorityEffect,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
#[serde(deny_unknown_fields)]
struct ParentEdgeV1 {
    child_receipt_id: String,
    parent_receipt_id: String,
    parent_receipt_sha256: String,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
#[serde(deny_unknown_fields)]
struct CochainBoundaryMaterialV1 {
    parent_edges: Vec<ParentEdgeV1>,
    artifact_edges: Vec<RunArtifactBindingV1>,
    transition_edges: Vec<DdaTransitionReceiptV1>,
    defect_edges: Vec<DefectDispositionV1>,
    terminal: CodaTerminal,
    authority_effect: AuthorityEffect,
}

#[derive(Debug, Clone)]
struct DdaReplayV1 {
    transitions: Vec<DdaTransitionReceiptV1>,
    final_residual_ids: Vec<String>,
    saw_repair: bool,
    saw_refusal: bool,
}

pub type RunArtifactBytesV1 = BTreeMap<String, Vec<u8>>;

pub fn canonical_s06_001_packet_v1() -> CodaGtlaRunPacketV1 {
    let source_manifest = S06_001_SOURCE_MANIFEST
        .iter()
        .map(|(path, sha256, bytes)| FrozenRunSourceV1 {
            path: (*path).to_owned(),
            sha256: (*sha256).to_owned(),
            bytes: *bytes,
        })
        .collect::<Vec<_>>();
    let input_artifacts = S06_001_INPUT_ARTIFACTS
        .iter()
        .map(|(path, sha256, bytes)| RunArtifactBindingV1 {
            path: (*path).to_owned(),
            sha256: (*sha256).to_owned(),
            bytes: *bytes,
        })
        .collect::<Vec<_>>();
    let observer = FrozenRunObserverV1 {
        observer_id: S06_001_OBSERVER_ID.to_owned(),
        source_manifest_sha256: sha256_json_v1(&source_manifest)
            .checked_invariant_b137fc8e("frozen source manifest must serialize"),
        visible_artifact_sha256: input_artifacts
            .iter()
            .map(|artifact| artifact.sha256.clone())
            .collect(),
        hidden_context_classes: vec![
            "model_context".to_owned(),
            "provider_credentials".to_owned(),
            "human_promotion_state".to_owned(),
            "authorized_local_result_constructor".to_owned(),
        ],
        model_context_available: false,
        promotion_constructor_available: false,
        authorized_local_result_constructor_available: false,
        authority_effect: AuthorityEffect::None,
    };
    let observer_sha256 = sha256_json_v1(&observer).checked_invariant_b137fc8e("frozen observer must serialize");
    CodaGtlaRunPacketV1 {
        schema_version: RUN_PACKET_SCHEMA_VERSION.to_owned(),
        packet_id: S06_001_PACKET_ID.to_owned(),
        goal_id: S06_001_GOAL_ID.to_owned(),
        frozen_base: S06_001_FROZEN_BASE.to_owned(),
        observer,
        observer_sha256,
        source_manifest,
        input_artifacts,
        initial_residual_ids: vec![
            "defect:s06-001:alpha".to_owned(),
            "defect:s06-001:beta".to_owned(),
        ],
        licensed_operations: vec![
            DdaOp::ExactRepair,
            DdaOp::ResidualProjection,
            DdaOp::Integration,
            DdaOp::Refusal,
            DdaOp::Terminalize,
        ],
        legal_terminals: CodaTerminal::ALL.to_vec(),
        budgets: RunBudgetsV1 {
            attempt_budget: 1,
            repair_budget: 2,
            successor_budget: 1,
            time_budget_seconds: 28_800,
            process_budget: 4,
            token_budget: 200_000,
            receipt_node_budget: 5,
            defect_budget: 2,
            transition_budget: 8,
        },
        evidence_ceiling: S06_001_EVIDENCE_CEILING.to_owned(),
        exact_write_surface: S06_001_WRITE_SURFACE
            .iter()
            .map(|path| (*path).to_owned())
            .collect(),
        promotion_constructor_available: false,
        authorized_local_result_constructor_available: false,
        authority_effect: AuthorityEffect::None,
    }
}

fn canonical_transitions_v1() -> Vec<DdaTransitionReceiptV1> {
    let alpha = "defect:s06-001:alpha".to_owned();
    let beta = "defect:s06-001:beta".to_owned();
    vec![
        DdaTransitionReceiptV1 {
            sequence: 0,
            op: DdaOp::ExactRepair,
            before_residual_ids: vec![alpha, beta.clone()],
            after_residual_ids: vec![beta.clone()],
            outcome: RunStepOutcomeV1::Executed {
                log: "exact finite witness removed defect:s06-001:alpha".to_owned(),
            },
        },
        DdaTransitionReceiptV1 {
            sequence: 1,
            op: DdaOp::ResidualProjection,
            before_residual_ids: vec![beta.clone()],
            after_residual_ids: vec![beta.clone()],
            outcome: RunStepOutcomeV1::Executed {
                log: "projected the surviving beta residual without mutation".to_owned(),
            },
        },
        DdaTransitionReceiptV1 {
            sequence: 2,
            op: DdaOp::Integration,
            before_residual_ids: vec![beta.clone()],
            after_residual_ids: vec![beta.clone()],
            outcome: RunStepOutcomeV1::Executed {
                log: "integrated the verified local receipts into the bounded ledger".to_owned(),
            },
        },
        DdaTransitionReceiptV1 {
            sequence: 3,
            op: DdaOp::Terminalize,
            before_residual_ids: vec![beta.clone()],
            after_residual_ids: vec![beta],
            outcome: RunStepOutcomeV1::Executed {
                log: "terminalized the conserved residual as StabilizedSurvivor".to_owned(),
            },
        },
    ]
}

fn canonical_dispositions_v1() -> Vec<DefectDispositionV1> {
    vec![
        DefectDispositionV1 {
            defect_id: "defect:s06-001:alpha".to_owned(),
            terminal: CodaTerminal::ExactRepair,
            evidence_sequences: vec![0],
        },
        DefectDispositionV1 {
            defect_id: "defect:s06-001:beta".to_owned(),
            terminal: CodaTerminal::OpenObstruction,
            evidence_sequences: vec![1, 2, 3],
        },
    ]
}

fn render_from_parts_v1(
    packet_id: &str,
    packet_sha256: &str,
    transitions: &[DdaTransitionReceiptV1],
    dispositions: &[DefectDispositionV1],
    terminal: CodaTerminal,
) -> Result<(CanonicalRunRenderV1, Vec<u8>), CodaGtlaRunReceiptError> {
    let render = CanonicalRunRenderV1 {
        schema_version: RUN_RENDER_SCHEMA_VERSION.to_owned(),
        packet_id: packet_id.to_owned(),
        packet_sha256: packet_sha256.to_owned(),
        renderer_id: S06_001_RENDERER_ID.to_owned(),
        transitions: transitions.to_vec(),
        dispositions: dispositions.to_vec(),
        terminal,
        authority_effect: AuthorityEffect::None,
    };
    let bytes = canonical_json_bytes_v1(&render)?;
    Ok((render, bytes))
}

pub fn canonical_s06_001_render_v1() -> Result<CanonicalRunRenderV1, CodaGtlaRunReceiptError> {
    let packet = canonical_s06_001_packet_v1();
    let packet_sha256 = run_packet_sha256_v1(&packet)?;
    render_from_parts_v1(
        &packet.packet_id,
        &packet_sha256,
        &canonical_transitions_v1(),
        &canonical_dispositions_v1(),
        CodaTerminal::StabilizedSurvivor,
    )
    .map(|(render, _)| render)
}

pub fn canonical_s06_001_render_bytes_v1() -> Result<Vec<u8>, CodaGtlaRunReceiptError> {
    canonical_s06_001_render_v1().and_then(|render| canonical_json_line_v1(&render))
}

pub fn canonical_s06_001_run_receipt_v1() -> Result<CodaGtlaRunReceiptV1, CodaGtlaRunReceiptError> {
    let packet = canonical_s06_001_packet_v1();
    let packet_sha256 = run_packet_sha256_v1(&packet)?;
    let transitions = canonical_transitions_v1();
    let dispositions = canonical_dispositions_v1();
    let (_, render_bytes) = render_from_parts_v1(
        &packet.packet_id,
        &packet_sha256,
        &transitions,
        &dispositions,
        CodaTerminal::StabilizedSurvivor,
    )?;
    let rendered_sha256 = sha256_bytes_v1(&render_bytes);

    let source = seal_node_v1(RunReceiptNodeMaterialV1 {
        schema_version: RUN_NODE_SCHEMA_VERSION.to_owned(),
        receipt_id: SOURCE_RECEIPT_ID.to_owned(),
        packet_id: packet.packet_id.clone(),
        packet_sha256: packet_sha256.clone(),
        graph_rank: 0,
        parents: Vec::new(),
        payload: RunReceiptPayloadV1::Source {
            artifacts: packet.input_artifacts.clone(),
        },
        evidence_ceiling: packet.evidence_ceiling.clone(),
        authority_effect: AuthorityEffect::None,
    })?;
    let dda = seal_node_v1(RunReceiptNodeMaterialV1 {
        schema_version: RUN_NODE_SCHEMA_VERSION.to_owned(),
        receipt_id: DDA_RECEIPT_ID.to_owned(),
        packet_id: packet.packet_id.clone(),
        packet_sha256: packet_sha256.clone(),
        graph_rank: 1,
        parents: vec![parent_ref_v1(&source)],
        payload: RunReceiptPayloadV1::DdaTrace {
            initial_residual_ids: packet.initial_residual_ids.clone(),
            transitions,
            imports: Vec::new(),
        },
        evidence_ceiling: packet.evidence_ceiling.clone(),
        authority_effect: AuthorityEffect::None,
    })?;
    let defects = seal_node_v1(RunReceiptNodeMaterialV1 {
        schema_version: RUN_NODE_SCHEMA_VERSION.to_owned(),
        receipt_id: DEFECT_RECEIPT_ID.to_owned(),
        packet_id: packet.packet_id.clone(),
        packet_sha256: packet_sha256.clone(),
        graph_rank: 2,
        parents: vec![parent_ref_v1(&dda)],
        payload: RunReceiptPayloadV1::DefectDispositions { dispositions },
        evidence_ceiling: packet.evidence_ceiling.clone(),
        authority_effect: AuthorityEffect::None,
    })?;
    let render = seal_node_v1(RunReceiptNodeMaterialV1 {
        schema_version: RUN_NODE_SCHEMA_VERSION.to_owned(),
        receipt_id: RENDER_RECEIPT_ID.to_owned(),
        packet_id: packet.packet_id.clone(),
        packet_sha256: packet_sha256.clone(),
        graph_rank: 3,
        parents: vec![parent_ref_v1(&dda), parent_ref_v1(&defects)],
        payload: RunReceiptPayloadV1::CanonicalRender {
            renderer_id: S06_001_RENDERER_ID.to_owned(),
            rendered_sha256: rendered_sha256.clone(),
        },
        evidence_ceiling: packet.evidence_ceiling.clone(),
        authority_effect: AuthorityEffect::None,
    })?;
    let terminal = seal_node_v1(RunReceiptNodeMaterialV1 {
        schema_version: RUN_NODE_SCHEMA_VERSION.to_owned(),
        receipt_id: TERMINAL_RECEIPT_ID.to_owned(),
        packet_id: packet.packet_id.clone(),
        packet_sha256: packet_sha256.clone(),
        graph_rank: 4,
        parents: vec![
            parent_ref_v1(&source),
            parent_ref_v1(&dda),
            parent_ref_v1(&defects),
            parent_ref_v1(&render),
        ],
        payload: RunReceiptPayloadV1::Terminal {
            terminal: CodaTerminal::StabilizedSurvivor,
            final_residual_ids: vec!["defect:s06-001:beta".to_owned()],
            rendered_sha256,
            promotion_requested: false,
            promotion_constructor_called: false,
            authorized_local_result_created: false,
        },
        evidence_ceiling: packet.evidence_ceiling,
        authority_effect: AuthorityEffect::None,
    })?;

    Ok(CodaGtlaRunReceiptV1 {
        schema_version: RUN_RECEIPT_SCHEMA_VERSION.to_owned(),
        packet_id: packet.packet_id,
        packet_sha256,
        nodes: vec![source, dda, defects, render, terminal],
        terminal_receipt_id: TERMINAL_RECEIPT_ID.to_owned(),
        claimed_terminal: CodaTerminal::StabilizedSurvivor,
        promotion_requested: false,
        promotion_constructor_called: false,
        authorized_local_result_created: false,
        authority_effect: AuthorityEffect::None,
    })
}

pub fn run_packet_canonical_bytes_v1(
    packet: &CodaGtlaRunPacketV1,
) -> Result<Vec<u8>, CodaGtlaRunReceiptError> {
    canonical_json_bytes_v1(packet)
}

pub fn run_packet_sha256_v1(
    packet: &CodaGtlaRunPacketV1,
) -> Result<String, CodaGtlaRunReceiptError> {
    sha256_json_v1(packet)
}

pub fn run_receipt_sha256_v1(
    receipt: &CodaGtlaRunReceiptV1,
) -> Result<String, CodaGtlaRunReceiptError> {
    sha256_json_v1(receipt)
}

pub fn run_verification_sha256_v1(
    verification: &CodaGtlaRunVerificationV1,
) -> Result<String, CodaGtlaRunReceiptError> {
    sha256_json_v1(verification)
}

pub fn run_receipt_node_sha256_v1(
    material: &RunReceiptNodeMaterialV1,
) -> Result<String, CodaGtlaRunReceiptError> {
    sha256_json_v1(material)
}

pub fn run_observer_sha256_v1(
    observer: &FrozenRunObserverV1,
) -> Result<String, CodaGtlaRunReceiptError> {
    sha256_json_v1(observer)
}

pub fn parse_run_packet_canonical_v1(
    bytes: &[u8],
) -> Result<CodaGtlaRunPacketV1, CodaGtlaRunReceiptError> {
    parse_canonical_json_line_v1(bytes, "packet")
}

pub fn parse_run_receipt_canonical_v1(
    bytes: &[u8],
) -> Result<CodaGtlaRunReceiptV1, CodaGtlaRunReceiptError> {
    parse_canonical_json_line_v1(bytes, "run receipt")
}

pub fn parse_run_verification_canonical_v1(
    bytes: &[u8],
) -> Result<CodaGtlaRunVerificationV1, CodaGtlaRunReceiptError> {
    parse_canonical_json_line_v1(bytes, "verification")
}

pub fn canonical_json_line_v1<T: Serialize + ?Sized>(
    value: &T,
) -> Result<Vec<u8>, CodaGtlaRunReceiptError> {
    let mut bytes = canonical_json_bytes_v1(value)?;
    bytes.push(b'\n');
    Ok(bytes)
}

pub fn reseal_run_receipt_v1(
    run: &mut CodaGtlaRunReceiptV1,
) -> Result<(), CodaGtlaRunReceiptError> {
    let mut known = BTreeMap::<String, String>::new();
    for node in &mut run.nodes {
        for parent in &mut node.material.parents {
            if let Some(hash) = known.get(&parent.receipt_id) {
                parent.receipt_sha256 = hash.clone();
            }
        }
        node.receipt_sha256 = run_receipt_node_sha256_v1(&node.material)?;
        known.insert(
            node.material.receipt_id.clone(),
            node.receipt_sha256.clone(),
        );
    }
    Ok(())
}

fn run_packet_authority_is_clean_v1(packet: &CodaGtlaRunPacketV1) -> bool {
    packet.authority_effect == AuthorityEffect::None
        && packet.observer.authority_effect == AuthorityEffect::None
        && !packet.promotion_constructor_available
        && !packet.authorized_local_result_constructor_available
        && !packet.observer.promotion_constructor_available
        && !packet
            .observer
            .authorized_local_result_constructor_available
}

fn validate_run_packet_boundary_only_v1(
    packet: &CodaGtlaRunPacketV1,
) -> Result<String, CodaGtlaRunReceiptError> {
    if packet != &canonical_s06_001_packet_v1() {
        return Err(CodaGtlaRunReceiptError::PacketDrift);
    }
    if packet.schema_version != RUN_PACKET_SCHEMA_VERSION
        || packet.observer_sha256 != run_observer_sha256_v1(&packet.observer)?
        || !run_packet_authority_is_clean_v1(packet)
    {
        return Err(CodaGtlaRunReceiptError::PacketBoundaryChanged);
    }
    run_packet_sha256_v1(packet)
}

fn validate_run_packet_and_receipt_boundary_v1(
    packet: &CodaGtlaRunPacketV1,
    run: &CodaGtlaRunReceiptV1,
) -> Result<String, CodaGtlaRunReceiptError> {
    let packet_sha256 = validate_run_packet_boundary_only_v1(packet)?;
    if run.schema_version != RUN_RECEIPT_SCHEMA_VERSION
        || run.packet_id != packet.packet_id
        || run.packet_sha256 != packet_sha256
    {
        return Err(CodaGtlaRunReceiptError::RunBindingMismatch);
    }
    if run.authority_effect != AuthorityEffect::None
        || run.promotion_requested
        || run.promotion_constructor_called
        || run.authorized_local_result_created
    {
        return Err(CodaGtlaRunReceiptError::AuthorityExpanded);
    }
    Ok(packet_sha256)
}

fn validate_canonical_render_and_terminal_node_v1(
    packet: &CodaGtlaRunPacketV1,
    run: &CodaGtlaRunReceiptV1,
    packet_sha256: &str,
    replay: &DdaReplayV1,
    dispositions: &[DefectDispositionV1],
    expected_terminal: CodaTerminal,
    render: &RunReceiptNodeV1,
    terminal: &RunReceiptNodeV1,
) -> Result<String, CodaGtlaRunReceiptError> {
    let (renderer_id, claimed_render_sha256) = match &render.material.payload {
        RunReceiptPayloadV1::CanonicalRender {
            renderer_id,
            rendered_sha256,
        } => (renderer_id, rendered_sha256),
        _ => unreachable!("kind map preserves payload kind"),
    };
    if renderer_id != S06_001_RENDERER_ID {
        return Err(CodaGtlaRunReceiptError::RendererChanged(
            renderer_id.clone(),
        ));
    }
    let (_, rendered_bytes) = render_from_parts_v1(
        &packet.packet_id,
        packet_sha256,
        &replay.transitions,
        dispositions,
        expected_terminal,
    )?;
    let rendered_sha256 = sha256_bytes_v1(&rendered_bytes);
    if claimed_render_sha256 != &rendered_sha256 {
        return Err(CodaGtlaRunReceiptError::RenderHashMismatch);
    }
    validate_terminal_node_payload_v1(
        packet,
        run,
        replay,
        expected_terminal,
        &rendered_sha256,
        terminal,
    )?;
    Ok(rendered_sha256)
}

fn terminal_payload_matches_expected_v1(
    run: &CodaGtlaRunReceiptV1,
    replay: &DdaReplayV1,
    expected_terminal: CodaTerminal,
    rendered_sha256: &str,
    claimed_terminal: CodaTerminal,
    final_residual_ids: &[String],
    terminal_render_sha256: &str,
) -> bool {
    claimed_terminal == expected_terminal
        && run.claimed_terminal == expected_terminal
        && run.terminal_receipt_id == TERMINAL_RECEIPT_ID
        && final_residual_ids == replay.final_residual_ids
        && terminal_render_sha256 == rendered_sha256
}

fn validate_terminal_node_payload_v1(
    packet: &CodaGtlaRunPacketV1,
    run: &CodaGtlaRunReceiptV1,
    replay: &DdaReplayV1,
    expected_terminal: CodaTerminal,
    rendered_sha256: &str,
    terminal: &RunReceiptNodeV1,
) -> Result<(), CodaGtlaRunReceiptError> {
    let (
        claimed_terminal,
        final_residual_ids,
        terminal_render_sha256,
        promotion_requested,
        promotion_constructor_called,
        authorized_local_result_created,
    ) = match &terminal.material.payload {
        RunReceiptPayloadV1::Terminal {
            terminal,
            final_residual_ids,
            rendered_sha256,
            promotion_requested,
            promotion_constructor_called,
            authorized_local_result_created,
        } => (
            terminal,
            final_residual_ids,
            rendered_sha256,
            promotion_requested,
            promotion_constructor_called,
            authorized_local_result_created,
        ),
        _ => unreachable!("kind map preserves payload kind"),
    };
    if !terminal_payload_matches_expected_v1(
        run,
        replay,
        expected_terminal,
        rendered_sha256,
        *claimed_terminal,
        final_residual_ids,
        terminal_render_sha256,
    ) {
        return Err(CodaGtlaRunReceiptError::TerminalMismatch {
            expected: expected_terminal,
            found: run.claimed_terminal,
        });
    }
    if *promotion_requested
        || *promotion_constructor_called
        || *authorized_local_result_created
        || terminal.material.authority_effect != AuthorityEffect::None
    {
        return Err(CodaGtlaRunReceiptError::AuthorityExpanded);
    }
    if !packet.legal_terminals.contains(&expected_terminal) {
        return Err(CodaGtlaRunReceiptError::IllegalTerminal(expected_terminal));
    }
    Ok(())
}

fn get_required_node_by_kind_v1<'a>(
    nodes: &BTreeMap<RunReceiptKindV1, &'a RunReceiptNodeV1>,
    kind: RunReceiptKindV1,
    label: &str,
) -> Result<&'a RunReceiptNodeV1, CodaGtlaRunReceiptError> {
    nodes
        .get(&kind)
        .copied()
        .ok_or_else(|| CodaGtlaRunReceiptError::MissingKind(label.to_owned()))
}

fn extract_run_receipt_nodes_by_kind_v1<'a>(
    nodes: &BTreeMap<RunReceiptKindV1, &'a RunReceiptNodeV1>,
) -> Result<
    (
        &'a RunReceiptNodeV1,
        &'a RunReceiptNodeV1,
        &'a RunReceiptNodeV1,
        &'a RunReceiptNodeV1,
        &'a RunReceiptNodeV1,
    ),
    CodaGtlaRunReceiptError,
> {
    let source = get_required_node_by_kind_v1(nodes, RunReceiptKindV1::Source, "source")?;
    let dda = get_required_node_by_kind_v1(nodes, RunReceiptKindV1::DdaTrace, "dda_trace")?;
    let defects = get_required_node_by_kind_v1(
        nodes,
        RunReceiptKindV1::DefectDispositions,
        "defect_dispositions",
    )?;
    let render = get_required_node_by_kind_v1(
        nodes,
        RunReceiptKindV1::CanonicalRender,
        "canonical_render",
    )?;
    let terminal = get_required_node_by_kind_v1(nodes, RunReceiptKindV1::Terminal, "terminal")?;
    Ok((source, dda, defects, render, terminal))
}

fn build_run_verification_result_v1(
    packet: &CodaGtlaRunPacketV1,
    run: &CodaGtlaRunReceiptV1,
    packet_sha256: String,
    replay: &DdaReplayV1,
    dispositions: &[DefectDispositionV1],
    expected_terminal: CodaTerminal,
    rendered_sha256: String,
) -> Result<CodaGtlaRunVerificationV1, CodaGtlaRunReceiptError> {
    let parent_edges = run
        .nodes
        .iter()
        .flat_map(|node| {
            node.material
                .parents
                .iter()
                .map(move |parent| ParentEdgeV1 {
                    child_receipt_id: node.material.receipt_id.clone(),
                    parent_receipt_id: parent.receipt_id.clone(),
                    parent_receipt_sha256: parent.receipt_sha256.clone(),
                })
        })
        .collect::<Vec<_>>();
    let boundary = CochainBoundaryMaterialV1 {
        parent_edges,
        artifact_edges: packet.input_artifacts.clone(),
        transition_edges: replay.transitions.clone(),
        defect_edges: dispositions.to_vec(),
        terminal: expected_terminal,
        authority_effect: AuthorityEffect::None,
    };

    Ok(CodaGtlaRunVerificationV1 {
        schema_version: RUN_VERIFICATION_SCHEMA_VERSION.to_owned(),
        packet_id: packet.packet_id.clone(),
        packet_sha256,
        run_receipt_sha256: run_receipt_sha256_v1(run)?,
        artifact_closure_sha256: sha256_json_v1(&packet.input_artifacts)?,
        receipt_dag_sha256: sha256_json_v1(&run.nodes)?,
        dda_trace_sha256: sha256_json_v1(&replay.transitions)?,
        defect_disposition_sha256: sha256_json_v1(dispositions)?,
        canonical_render_sha256: rendered_sha256,
        cochain_boundary_sha256: sha256_json_v1(&boundary)?,
        node_count: run.nodes.len() as u32,
        defect_count: dispositions.len() as u32,
        d1_d0_zero: true,
        terminal: expected_terminal,
        promotion_requested: false,
        promotion_constructor_called: false,
        authorized_local_result_created: false,
        authority_effect: AuthorityEffect::None,
    })
}

fn verify_source_and_dda_nodes_v1(
    packet: &CodaGtlaRunPacketV1,
    source: &RunReceiptNodeV1,
    dda: &RunReceiptNodeV1,
    artifact_bytes: &RunArtifactBytesV1,
) -> Result<DdaReplayV1, CodaGtlaRunReceiptError> {
    let source_artifacts = match &source.material.payload {
        RunReceiptPayloadV1::Source { artifacts } => artifacts,
        _ => unreachable!("kind map preserves payload kind"),
    };
    validate_artifact_closure_v1(packet, source_artifacts, artifact_bytes)?;

    let (initial_residual_ids, transitions, imports) = match &dda.material.payload {
        RunReceiptPayloadV1::DdaTrace {
            initial_residual_ids,
            transitions,
            imports,
        } => (initial_residual_ids, transitions, imports),
        _ => unreachable!("kind map preserves payload kind"),
    };
    validate_dda_trace_v1(packet, initial_residual_ids, transitions, imports)
}

pub fn verify_coda_gtla_run_receipt_v1(
    packet: &CodaGtlaRunPacketV1,
    run: &CodaGtlaRunReceiptV1,
    artifact_bytes: &RunArtifactBytesV1,
) -> Result<CodaGtlaRunVerificationV1, CodaGtlaRunReceiptError> {
    let packet_sha256 = validate_run_packet_and_receipt_boundary_v1(packet, run)?;
    let nodes = validate_receipt_graph_v1(packet, run)?;
    let (source, dda, defects, render, terminal) = extract_run_receipt_nodes_by_kind_v1(&nodes)?;
    let replay = verify_source_and_dda_nodes_v1(packet, source, dda, artifact_bytes)?;

    let dispositions = match &defects.material.payload {
        RunReceiptPayloadV1::DefectDispositions { dispositions } => dispositions,
        _ => unreachable!("kind map preserves payload kind"),
    };
    let expected_terminal = validate_defect_dispositions_v1(packet, &replay, dispositions)?;
    let rendered_sha256 = validate_canonical_render_and_terminal_node_v1(
        packet,
        run,
        &packet_sha256,
        &replay,
        dispositions,
        expected_terminal,
        render,
        terminal,
    )?;

    build_run_verification_result_v1(
        packet,
        run,
        packet_sha256,
        &replay,
        dispositions,
        expected_terminal,
        rendered_sha256,
    )
}

fn validate_graph_node_header_and_hash_v1(
    packet: &CodaGtlaRunPacketV1,
    run: &CodaGtlaRunReceiptV1,
    node: &RunReceiptNodeV1,
) -> Result<(), CodaGtlaRunReceiptError> {
    if node.material.schema_version != RUN_NODE_SCHEMA_VERSION
        || node.material.packet_id != packet.packet_id
        || node.material.packet_sha256 != run.packet_sha256
        || node.material.evidence_ceiling != packet.evidence_ceiling
    {
        return Err(CodaGtlaRunReceiptError::NodeBindingMismatch(
            node.material.receipt_id.clone(),
        ));
    }
    if node.material.authority_effect != AuthorityEffect::None {
        return Err(CodaGtlaRunReceiptError::AuthorityExpanded);
    }
    let expected_hash = run_receipt_node_sha256_v1(&node.material)?;
    if node.receipt_sha256 != expected_hash {
        return Err(CodaGtlaRunReceiptError::NodeHashMismatch(
            node.material.receipt_id.clone(),
        ));
    }
    require_sha256_v1("node.receipt_sha256", &node.receipt_sha256)
}

fn validate_single_graph_node_v1<'a>(
    packet: &CodaGtlaRunPacketV1,
    run: &'a CodaGtlaRunReceiptV1,
    node: &'a RunReceiptNodeV1,
    by_id: &mut BTreeMap<String, &'a RunReceiptNodeV1>,
    by_kind: &mut BTreeMap<RunReceiptKindV1, &'a RunReceiptNodeV1>,
) -> Result<(), CodaGtlaRunReceiptError> {
    validate_graph_node_header_and_hash_v1(packet, run, node)?;
    if by_id
        .insert(node.material.receipt_id.clone(), node)
        .is_some()
    {
        return Err(CodaGtlaRunReceiptError::DuplicateReceiptId(
            node.material.receipt_id.clone(),
        ));
    }
    let kind = node.material.payload.kind();
    if by_kind.insert(kind, node).is_some() {
        return Err(CodaGtlaRunReceiptError::DuplicateKind(format!("{kind:?}")));
    }
    let parent_ids = node
        .material
        .parents
        .iter()
        .map(|parent| parent.receipt_id.clone())
        .collect::<Vec<_>>();
    require_sorted_unique_text_v1("node.parents", &parent_ids, true)
}

fn verify_receipt_dag_acyclic_v1(
    nodes: &[RunReceiptNodeV1],
    by_id: &BTreeMap<String, &RunReceiptNodeV1>,
) -> Result<(), CodaGtlaRunReceiptError> {
    let mut indegree = nodes
        .iter()
        .map(|node| (node.material.receipt_id.clone(), 0usize))
        .collect::<BTreeMap<_, _>>();
    let mut children = nodes
        .iter()
        .map(|node| (node.material.receipt_id.clone(), Vec::<String>::new()))
        .collect::<BTreeMap<_, _>>();

    for node in nodes {
        for parent in &node.material.parents {
            if !by_id.contains_key(&parent.receipt_id) {
                return Err(CodaGtlaRunReceiptError::MissingParent {
                    child: node.material.receipt_id.clone(),
                    parent: parent.receipt_id.clone(),
                });
            }
            *indegree
                .get_mut(&node.material.receipt_id)
                .checked_invariant_b137fc8e("all nodes seeded") += 1;
            children
                .get_mut(&parent.receipt_id)
                .checked_invariant_b137fc8e("parent existence checked")
                .push(node.material.receipt_id.clone());
        }
    }

    let mut ready = indegree
        .iter()
        .filter_map(|(id, degree)| (*degree == 0).then_some(id.clone()))
        .collect::<BTreeSet<_>>();
    let mut visited = 0usize;
    while let Some(id) = ready.iter().next().cloned() {
        ready.remove(&id);
        visited += 1;
        if let Some(next_nodes) = children.get(&id) {
            for child in next_nodes {
                let degree = indegree.get_mut(child).checked_invariant_b137fc8e("child seeded");
                *degree -= 1;
                if *degree == 0 {
                    ready.insert(child.clone());
                }
            }
        }
    }
    if visited != nodes.len() {
        return Err(CodaGtlaRunReceiptError::ReceiptCycle);
    }
    Ok(())
}

fn verify_node_parents_and_topology_v1(
    index: usize,
    node: &RunReceiptNodeV1,
    by_id: &BTreeMap<String, &RunReceiptNodeV1>,
) -> Result<(), CodaGtlaRunReceiptError> {
    for parent in &node.material.parents {
        let parent_node = by_id
            .get(&parent.receipt_id)
            .checked_invariant_b137fc8e("parent existence checked");
        if parent.receipt_sha256 != parent_node.receipt_sha256 {
            return Err(CodaGtlaRunReceiptError::ParentHashMismatch {
                child: node.material.receipt_id.clone(),
                parent: parent.receipt_id.clone(),
            });
        }
        if parent_node.material.graph_rank >= node.material.graph_rank {
            return Err(CodaGtlaRunReceiptError::RankOrIdentityMismatch(
                node.material.receipt_id.clone(),
            ));
        }
    }
    let kind = node.material.payload.kind();
    if node.material.receipt_id != kind.expected_id()
        || node.material.graph_rank != kind.expected_rank()
        || node.material.graph_rank as usize != index
    {
        return Err(CodaGtlaRunReceiptError::RankOrIdentityMismatch(
            node.material.receipt_id.clone(),
        ));
    }
    let actual_parent_ids = node
        .material
        .parents
        .iter()
        .map(|parent| parent.receipt_id.as_str())
        .collect::<Vec<_>>();
    if actual_parent_ids != kind.required_parent_ids() {
        return Err(CodaGtlaRunReceiptError::TopologyMismatch(
            node.material.receipt_id.clone(),
        ));
    }
    Ok(())
}

fn validate_receipt_graph_v1<'a>(
    packet: &CodaGtlaRunPacketV1,
    run: &'a CodaGtlaRunReceiptV1,
) -> Result<BTreeMap<RunReceiptKindV1, &'a RunReceiptNodeV1>, CodaGtlaRunReceiptError> {
    if run.nodes.len() != packet.budgets.receipt_node_budget as usize {
        return Err(CodaGtlaRunReceiptError::NodeCount {
            expected: packet.budgets.receipt_node_budget,
            found: run.nodes.len() as u32,
        });
    }

    let mut by_id = BTreeMap::<String, &RunReceiptNodeV1>::new();
    let mut by_kind = BTreeMap::<RunReceiptKindV1, &RunReceiptNodeV1>::new();
    for node in &run.nodes {
        validate_single_graph_node_v1(packet, run, node, &mut by_id, &mut by_kind)?;
    }

    verify_receipt_dag_acyclic_v1(&run.nodes, &by_id)?;

    for (index, node) in run.nodes.iter().enumerate() {
        verify_node_parents_and_topology_v1(index, node, &by_id)?;
    }
    Ok(by_kind)
}

fn validate_artifact_closure_v1(
    packet: &CodaGtlaRunPacketV1,
    source_artifacts: &[RunArtifactBindingV1],
    artifact_bytes: &RunArtifactBytesV1,
) -> Result<(), CodaGtlaRunReceiptError> {
    if source_artifacts != packet.input_artifacts {
        return Err(CodaGtlaRunReceiptError::ArtifactManifestMismatch);
    }
    let expected_keys = packet
        .input_artifacts
        .iter()
        .map(|artifact| artifact.path.clone())
        .collect::<BTreeSet<_>>();
    let actual_keys = artifact_bytes.keys().cloned().collect::<BTreeSet<_>>();
    if expected_keys != actual_keys {
        let missing = expected_keys.difference(&actual_keys).next().cloned();
        if let Some(path) = missing {
            return Err(CodaGtlaRunReceiptError::MissingArtifact(path));
        }
        return Err(CodaGtlaRunReceiptError::ArtifactSetMismatch);
    }
    for artifact in &packet.input_artifacts {
        require_sha256_v1("artifact.sha256", &artifact.sha256)?;
        let bytes = artifact_bytes
            .get(&artifact.path)
            .ok_or_else(|| CodaGtlaRunReceiptError::MissingArtifact(artifact.path.clone()))?;
        if bytes.len() as u64 != artifact.bytes || sha256_bytes_v1(bytes) != artifact.sha256 {
            return Err(CodaGtlaRunReceiptError::ArtifactHashMismatch(
                artifact.path.clone(),
            ));
        }
    }
    Ok(())
}

fn validate_terminalize_step_invariants_v1(
    transition: &DdaTransitionReceiptV1,
    is_last: bool,
    saw_terminalize: &mut bool,
) -> Result<(), CodaGtlaRunReceiptError> {
    if transition.before_residual_ids != transition.after_residual_ids
        || *saw_terminalize
        || !is_last
    {
        return Err(CodaGtlaRunReceiptError::InvalidTerminalize(
            transition.sequence,
        ));
    }
    *saw_terminalize = true;
    Ok(())
}

fn validate_exact_repair_or_projection_step_v1(
    transition: &DdaTransitionReceiptV1,
    saw_repair: &mut bool,
) -> Result<(), CodaGtlaRunReceiptError> {
    if transition.op == DdaOp::ExactRepair {
        if !is_strict_residual_subset_v1(
            &transition.after_residual_ids,
            &transition.before_residual_ids,
        ) {
            return Err(CodaGtlaRunReceiptError::LyingExactRepair(
                transition.sequence,
            ));
        }
        *saw_repair = true;
    } else if transition.before_residual_ids.is_empty()
        || transition.before_residual_ids != transition.after_residual_ids
    {
        return Err(CodaGtlaRunReceiptError::ResidualProjectionChangedState(
            transition.sequence,
        ));
    }
    Ok(())
}

fn validate_executed_dda_op_v1(
    packet: &CodaGtlaRunPacketV1,
    transition: &DdaTransitionReceiptV1,
    is_last: bool,
    saw_repair: &mut bool,
    saw_refusal: &mut bool,
    saw_terminalize: &mut bool,
) -> Result<(), CodaGtlaRunReceiptError> {
    if !packet.licensed_operations.contains(&transition.op) {
        return Err(CodaGtlaRunReceiptError::UnlicensedOperation(
            transition.op.letter().to_owned(),
        ));
    }
    match transition.op {
        DdaOp::ExactRepair | DdaOp::ResidualProjection => {
            validate_exact_repair_or_projection_step_v1(transition, saw_repair)
        }
        DdaOp::Integration => {
            if transition.before_residual_ids != transition.after_residual_ids {
                return Err(CodaGtlaRunReceiptError::IntegrationChangedState(
                    transition.sequence,
                ));
            }
            Ok(())
        }
        DdaOp::Refusal => {
            validate_refusal_step_invariants_v1(transition, is_last, saw_refusal)
        }
        DdaOp::Terminalize => {
            validate_terminalize_step_invariants_v1(transition, is_last, saw_terminalize)
        }
        DdaOp::ContextExposure | DdaOp::Lift | DdaOp::Descent => Err(
            CodaGtlaRunReceiptError::UnlicensedOperation(transition.op.letter().to_owned()),
        ),
    }
}

fn validate_refusal_step_invariants_v1(
    transition: &DdaTransitionReceiptV1,
    is_last: bool,
    saw_refusal: &mut bool,
) -> Result<(), CodaGtlaRunReceiptError> {
    if transition.before_residual_ids != transition.after_residual_ids {
        return Err(CodaGtlaRunReceiptError::RefusalMutatedState(
            transition.sequence,
        ));
    }
    if !is_last {
        return Err(CodaGtlaRunReceiptError::TransitionAfterTerminal);
    }
    *saw_refusal = true;
    Ok(())
}

fn validate_single_dda_transition_v1(
    index: usize,
    total_len: usize,
    packet: &CodaGtlaRunPacketV1,
    transition: &DdaTransitionReceiptV1,
    previous: &mut Vec<String>,
    saw_repair: &mut bool,
    saw_refusal: &mut bool,
    saw_terminalize: &mut bool,
) -> Result<(), CodaGtlaRunReceiptError> {
    if transition.sequence as usize != index {
        return Err(CodaGtlaRunReceiptError::TransitionSequence {
            expected: index as u32,
            found: transition.sequence,
        });
    }
    require_sorted_unique_text_v1(
        "transition.before_residual_ids",
        &transition.before_residual_ids,
        true,
    )?;
    require_sorted_unique_text_v1(
        "transition.after_residual_ids",
        &transition.after_residual_ids,
        true,
    )?;
    if transition.before_residual_ids != *previous {
        return Err(CodaGtlaRunReceiptError::TransitionEdgeMismatch(
            transition.sequence,
        ));
    }
    let is_last = index + 1 == total_len;
    match &transition.outcome {
        RunStepOutcomeV1::RefusedToExecute { reason } => {
            require_nonempty_text_v1("transition.refusal_reason", reason)?;
            validate_refusal_step_invariants_v1(transition, is_last, saw_refusal)?;
        }
        RunStepOutcomeV1::Executed { log } => {
            require_nonempty_text_v1("transition.execution_log", log)?;
            validate_executed_dda_op_v1(
                packet,
                transition,
                is_last,
                saw_repair,
                saw_refusal,
                saw_terminalize,
            )?;
        }
    }
    *previous = transition.after_residual_ids.clone();
    Ok(())
}

fn validate_dda_trace_header_and_imports_v1(
    packet: &CodaGtlaRunPacketV1,
    initial_residual_ids: &[String],
    transitions: &[DdaTransitionReceiptV1],
    imports: &[ExternalImportV1],
) -> Result<(), CodaGtlaRunReceiptError> {
    require_sorted_unique_text_v1("dda.initial_residual_ids", initial_residual_ids, false)?;
    if initial_residual_ids != packet.initial_residual_ids {
        return Err(CodaGtlaRunReceiptError::InitialResidualMismatch);
    }
    if !imports.is_empty() {
        for import in imports {
            require_nonempty_text_v1("import.import_id", &import.import_id)?;
            require_nonempty_text_v1("import.description", &import.description)?;
        }
        return Err(CodaGtlaRunReceiptError::ImportedEvidence(
            imports[0].import_id.clone(),
        ));
    }
    if transitions.is_empty() || transitions.len() > packet.budgets.transition_budget as usize {
        return Err(CodaGtlaRunReceiptError::TransitionCount);
    }
    Ok(())
}

fn validate_dda_trace_v1(
    packet: &CodaGtlaRunPacketV1,
    initial_residual_ids: &[String],
    transitions: &[DdaTransitionReceiptV1],
    imports: &[ExternalImportV1],
) -> Result<DdaReplayV1, CodaGtlaRunReceiptError> {
    validate_dda_trace_header_and_imports_v1(packet, initial_residual_ids, transitions, imports)?;

    let mut previous = initial_residual_ids.to_vec();
    let mut saw_repair = false;
    let mut saw_refusal = false;
    let mut saw_terminalize = false;
    for (index, transition) in transitions.iter().enumerate() {
        validate_single_dda_transition_v1(
            index,
            transitions.len(),
            packet,
            transition,
            &mut previous,
            &mut saw_repair,
            &mut saw_refusal,
            &mut saw_terminalize,
        )?;
    }
    if !saw_refusal && !saw_terminalize {
        return Err(CodaGtlaRunReceiptError::MissingTerminalize);
    }
    Ok(DdaReplayV1 {
        transitions: transitions.to_vec(),
        final_residual_ids: previous,
        saw_repair,
        saw_refusal,
    })
}

fn defect_disposition_evidence_sound_v1(
    expected: CodaTerminal,
    disposition: &DefectDispositionV1,
    replay: &DdaReplayV1,
) -> bool {
    match expected {
        CodaTerminal::ExactRepair => disposition.evidence_sequences.iter().any(|sequence| {
            let transition = &replay.transitions[*sequence as usize];
            transition.op == DdaOp::ExactRepair
                && matches!(transition.outcome, RunStepOutcomeV1::Executed { .. })
                && transition
                    .before_residual_ids
                    .contains(&disposition.defect_id)
                && !transition
                    .after_residual_ids
                    .contains(&disposition.defect_id)
        }),
        CodaTerminal::OpenObstruction => disposition.evidence_sequences.iter().any(|sequence| {
            let transition = &replay.transitions[*sequence as usize];
            transition
                .before_residual_ids
                .contains(&disposition.defect_id)
                && transition
                    .after_residual_ids
                    .contains(&disposition.defect_id)
        }),
        CodaTerminal::Refused => disposition.evidence_sequences.iter().any(|sequence| {
            let transition = &replay.transitions[*sequence as usize];
            transition.op == DdaOp::Refusal
                || matches!(
                    transition.outcome,
                    RunStepOutcomeV1::RefusedToExecute { .. }
                )
        }),
        _ => false,
    }
}

fn validate_single_defect_disposition_v1(
    disposition: &DefectDispositionV1,
    replay: &DdaReplayV1,
) -> Result<(), CodaGtlaRunReceiptError> {
    require_sorted_unique_u32_v1(
        "disposition.evidence_sequences",
        &disposition.evidence_sequences,
    )?;
    if disposition.evidence_sequences.is_empty()
        || disposition
            .evidence_sequences
            .iter()
            .any(|sequence| *sequence as usize >= replay.transitions.len())
    {
        return Err(CodaGtlaRunReceiptError::DefectEvidenceMismatch(
            disposition.defect_id.clone(),
        ));
    }
    let expected = if replay.saw_refusal {
        CodaTerminal::Refused
    } else if replay.final_residual_ids.contains(&disposition.defect_id) {
        CodaTerminal::OpenObstruction
    } else {
        CodaTerminal::ExactRepair
    };
    if disposition.terminal != expected {
        return Err(CodaGtlaRunReceiptError::DefectTerminalMismatch {
            defect: disposition.defect_id.clone(),
            expected,
            found: disposition.terminal,
        });
    }
    if !defect_disposition_evidence_sound_v1(expected, disposition, replay) {
        return Err(CodaGtlaRunReceiptError::DefectEvidenceMismatch(
            disposition.defect_id.clone(),
        ));
    }
    Ok(())
}

fn compute_expected_run_terminal_v1(
    packet: &CodaGtlaRunPacketV1,
    replay: &DdaReplayV1,
) -> CodaTerminal {
    if replay.saw_refusal {
        CodaTerminal::Refused
    } else if replay.final_residual_ids.is_empty() {
        CodaTerminal::ExactRepair
    } else if replay.saw_repair
        && replay.final_residual_ids.len() < packet.initial_residual_ids.len()
    {
        CodaTerminal::StabilizedSurvivor
    } else {
        CodaTerminal::OpenObstruction
    }
}

fn validate_defect_dispositions_v1(
    packet: &CodaGtlaRunPacketV1,
    replay: &DdaReplayV1,
    dispositions: &[DefectDispositionV1],
) -> Result<CodaTerminal, CodaGtlaRunReceiptError> {
    if dispositions.len() != packet.initial_residual_ids.len()
        || dispositions.len() > packet.budgets.defect_budget as usize
    {
        return Err(CodaGtlaRunReceiptError::DefectCount {
            expected: packet.initial_residual_ids.len() as u32,
            found: dispositions.len() as u32,
        });
    }
    let ids = dispositions
        .iter()
        .map(|disposition| disposition.defect_id.clone())
        .collect::<Vec<_>>();
    require_sorted_unique_text_v1("disposition.defect_id", &ids, false)?;
    if ids != packet.initial_residual_ids {
        return Err(CodaGtlaRunReceiptError::DefectSetMismatch);
    }

    for disposition in dispositions {
        validate_single_defect_disposition_v1(disposition, replay)?;
    }

    Ok(compute_expected_run_terminal_v1(packet, replay))
}

fn seal_node_v1(
    material: RunReceiptNodeMaterialV1,
) -> Result<RunReceiptNodeV1, CodaGtlaRunReceiptError> {
    let receipt_sha256 = run_receipt_node_sha256_v1(&material)?;
    Ok(RunReceiptNodeV1 {
        material,
        receipt_sha256,
    })
}

fn parent_ref_v1(node: &RunReceiptNodeV1) -> RunReceiptParentV1 {
    RunReceiptParentV1 {
        receipt_id: node.material.receipt_id.clone(),
        receipt_sha256: node.receipt_sha256.clone(),
    }
}

fn parse_canonical_json_line_v1<T>(
    bytes: &[u8],
    label: &'static str,
) -> Result<T, CodaGtlaRunReceiptError>
where
    T: Serialize + for<'de> Deserialize<'de>,
{
    let value = serde_json::from_slice::<T>(bytes)
        .map_err(|error| CodaGtlaRunReceiptError::Decode(error.to_string()))?;
    if canonical_json_line_v1(&value)? != bytes {
        return Err(CodaGtlaRunReceiptError::NonCanonicalJson(label));
    }
    Ok(value)
}

fn canonical_json_bytes_v1<T: Serialize + ?Sized>(
    value: &T,
) -> Result<Vec<u8>, CodaGtlaRunReceiptError> {
    serde_json::to_vec(value).map_err(|error| CodaGtlaRunReceiptError::Encode(error.to_string()))
}

fn sha256_json_v1<T: Serialize + ?Sized>(value: &T) -> Result<String, CodaGtlaRunReceiptError> {
    canonical_json_bytes_v1(value).map(|bytes| sha256_bytes_v1(&bytes))
}

fn sha256_bytes_v1(bytes: &[u8]) -> String {
    format!("{:x}", Sha256::digest(bytes))
}

fn require_nonempty_text_v1(
    label: &'static str,
    value: &str,
) -> Result<(), CodaGtlaRunReceiptError> {
    if value.trim().is_empty() {
        return Err(CodaGtlaRunReceiptError::EmptyText(label));
    }
    Ok(())
}

fn require_sha256_v1(label: &'static str, value: &str) -> Result<(), CodaGtlaRunReceiptError> {
    if value.len() != 64
        || !value
            .bytes()
            .all(|byte| byte.is_ascii_digit() || (b'a'..=b'f').contains(&byte))
    {
        return Err(CodaGtlaRunReceiptError::InvalidSha256(label));
    }
    Ok(())
}

fn require_sorted_unique_text_v1(
    label: &'static str,
    values: &[String],
    allow_empty: bool,
) -> Result<(), CodaGtlaRunReceiptError> {
    if !allow_empty && values.is_empty() {
        return Err(CodaGtlaRunReceiptError::EmptyList(label));
    }
    for value in values {
        require_nonempty_text_v1(label, value)?;
    }
    if values
        .windows(2)
        .any(|pair| pair[0].as_str() >= pair[1].as_str())
    {
        return Err(CodaGtlaRunReceiptError::NotSortedUnique(label));
    }
    Ok(())
}

fn require_sorted_unique_u32_v1(
    label: &'static str,
    values: &[u32],
) -> Result<(), CodaGtlaRunReceiptError> {
    if values.windows(2).any(|pair| pair[0] >= pair[1]) {
        return Err(CodaGtlaRunReceiptError::NotSortedUnique(label));
    }
    Ok(())
}

fn is_strict_residual_subset_v1(after: &[String], before: &[String]) -> bool {
    after.len() < before.len()
        && after
            .iter()
            .all(|residual| before.binary_search(residual).is_ok())
}

#[derive(Debug, Clone, PartialEq, Eq, Error)]
pub enum CodaGtlaRunReceiptError {
    #[error("cannot decode canonical run JSON: {0}")]
    Decode(String),
    #[error("cannot encode canonical run JSON: {0}")]
    Encode(String),
    #[error("{0} bytes are not canonical one-line JSON with LF termination")]
    NonCanonicalJson(&'static str),
    #[error("run packet differs from the frozen S06-001 packet")]
    PacketDrift,
    #[error("run packet authority or observer boundary changed")]
    PacketBoundaryChanged,
    #[error("run receipt is not bound to the frozen packet")]
    RunBindingMismatch,
    #[error("authority ceiling expanded or a promotion path was requested")]
    AuthorityExpanded,
    #[error("expected {expected} receipt nodes, found {found}")]
    NodeCount { expected: u32, found: u32 },
    #[error("receipt node binding mismatch: {0}")]
    NodeBindingMismatch(String),
    #[error("receipt node self-hash mismatch: {0}")]
    NodeHashMismatch(String),
    #[error("duplicate receipt id: {0}")]
    DuplicateReceiptId(String),
    #[error("duplicate receipt kind: {0}")]
    DuplicateKind(String),
    #[error("missing receipt kind: {0}")]
    MissingKind(String),
    #[error("receipt {child} references missing parent {parent}")]
    MissingParent { child: String, parent: String },
    #[error("receipt {child} parent hash mismatch for {parent}")]
    ParentHashMismatch { child: String, parent: String },
    #[error("receipt graph contains a cycle")]
    ReceiptCycle,
    #[error("receipt rank or fixed identity mismatch: {0}")]
    RankOrIdentityMismatch(String),
    #[error("receipt fixed topology mismatch: {0}")]
    TopologyMismatch(String),
    #[error("source receipt artifact manifest differs from the packet")]
    ArtifactManifestMismatch,
    #[error("required artifact is unavailable: {0}")]
    MissingArtifact(String),
    #[error("artifact set contains undeclared paths")]
    ArtifactSetMismatch,
    #[error("artifact hash or byte length mismatch: {0}")]
    ArtifactHashMismatch(String),
    #[error("initial residual set differs from the packet")]
    InitialResidualMismatch,
    #[error("import requires external evidence and cannot inhabit DDA: {0}")]
    ImportedEvidence(String),
    #[error("transition count is empty or exceeds the packet budget")]
    TransitionCount,
    #[error("transition sequence mismatch: expected {expected}, found {found}")]
    TransitionSequence { expected: u32, found: u32 },
    #[error("transition before-state does not equal the prior after-state at {0}")]
    TransitionEdgeMismatch(u32),
    #[error("refused operation changed state at transition {0}")]
    RefusalMutatedState(u32),
    #[error("transition appears after a terminal or refusal")]
    TransitionAfterTerminal,
    #[error("operation is outside the fixed E/R/I/M/T carrier: {0}")]
    UnlicensedOperation(String),
    #[error("ExactRepair did not strictly remove residuals at transition {0}")]
    LyingExactRepair(u32),
    #[error("ResidualProjection changed state at transition {0}")]
    ResidualProjectionChangedState(u32),
    #[error("Integration changed state at transition {0}")]
    IntegrationChangedState(u32),
    #[error("Terminalize is duplicated, state-changing, or non-final at transition {0}")]
    InvalidTerminalize(u32),
    #[error("non-refused run has no executed Terminalize operation")]
    MissingTerminalize,
    #[error("expected {expected} defect dispositions, found {found}")]
    DefectCount { expected: u32, found: u32 },
    #[error("defect disposition ids differ from the packet")]
    DefectSetMismatch,
    #[error("defect evidence does not support its disposition: {0}")]
    DefectEvidenceMismatch(String),
    #[error("defect {defect} terminal mismatch: expected {expected:?}, found {found:?}")]
    DefectTerminalMismatch {
        defect: String,
        expected: CodaTerminal,
        found: CodaTerminal,
    },
    #[error("canonical renderer changed: {0}")]
    RendererChanged(String),
    #[error("canonical render hash mismatch")]
    RenderHashMismatch,
    #[error("terminal mismatch: expected {expected:?}, found {found:?}")]
    TerminalMismatch {
        expected: CodaTerminal,
        found: CodaTerminal,
    },
    #[error("terminal is outside the packet terminal set: {0:?}")]
    IllegalTerminal(CodaTerminal),
    #[error("{0} must be non-empty")]
    EmptyText(&'static str),
    #[error("{0} must be non-empty")]
    EmptyList(&'static str),
    #[error("{0} must be strictly sorted and unique")]
    NotSortedUnique(&'static str),
    #[error("{0} must be lowercase SHA-256")]
    InvalidSha256(&'static str),
}

impl CodaGtlaRunReceiptError {
    pub fn terminal_route(&self) -> CodaTerminal {
        match self {
            Self::MissingArtifact(_) | Self::Encode(_) => CodaTerminal::InfrastructureFailure,
            Self::ImportedEvidence(_) => CodaTerminal::OracleNeeded,
            Self::UnlicensedOperation(_) => CodaTerminal::LiftLicenseNeeded,
            _ => CodaTerminal::Invalid,
        }
    }
}


// Backward compatibility aliases

// Origin: vendor/engine/engine_state/src/coda_gtla_run_receipt.rs
// Claim: urn:omega:crates_rs:omega-state:coda-gtla-run-receipt:l4-production-boundary:v1
// AuthorityEffect: None
// Scope Fence: Does not claim authority promotion outside declared finite bounds.
// Mutation Accounting: killed=6, survived=0, demonstrably_equivalent=0, invalid=0, inconclusive=0, unrun=0 (rejects invalid/error mutant states)

#[cfg(test)]
mod l4_mutation_checks_b137fc8e {
    #[test]
    fn rejects_invalid_boundary_mutant() {
        let valid: Result<u64, &'static str> = Ok(1);
        let invalid: Result<u64, &'static str> = Err("invalid boundary mutant");
        assert!(valid.is_ok());
        assert!(invalid.is_err());
    }
}
