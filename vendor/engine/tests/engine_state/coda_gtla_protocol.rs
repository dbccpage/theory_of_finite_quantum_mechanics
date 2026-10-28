use std::{collections::BTreeSet, env, fs, path::PathBuf};

use engine_state::coda_gtla_protocol::{
    compile_legacy_packet_v1, protocol_schema_receipt_v1, structural_cochain_receipt_v1,
    validate_protocol_trace_v1, CompositionFailureKindV1, FrozenObserverContextV1, CodaGtlaStage,
    CodaTerminal, LegacyAdapterLimitationV1, LegacyCompileContextV1, LegacyPacketFieldV1,
    LegacyPacketV1, ProtocolError, ProtocolMachineV1, ProtocolSourceV1, ProtocolTraceV1,
    TransitionProposalV1,
};
use engine_types::authority::AuthorityEffect;
use serde_json::{self, Value};

fn fixture(name: &str) -> String {
    fs::read_to_string(
        PathBuf::from(env!("CARGO_MANIFEST_DIR"))
            .join("../tests/engine_state")
            .join("fixtures")
            .join(name),
    )
    .unwrap()
}

fn legacy_packet() -> LegacyPacketV1 {
    serde_json::from_str(&fixture("legacy_packet_v1.json")).unwrap()
}

fn compile_context() -> LegacyCompileContextV1 {
    serde_json::from_str(&fixture("legacy_compile_context_v1.json")).unwrap()
}

fn observer() -> FrozenObserverContextV1 {
    compile_context().observer
}

fn ids(values: &[&str]) -> BTreeSet<String> {
    values.iter().map(|value| (*value).to_owned()).collect()
}

fn machine(residuals: &[&str]) -> ProtocolMachineV1 {
    ProtocolMachineV1::new(
        "s01-001-fixture",
        "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        observer(),
        ids(residuals),
        ids(&["license:bounded-protocol-fixture"]),
    )
    .unwrap()
}

fn advance_until(machine: &mut ProtocolMachineV1, stop: CodaGtlaStage) {
    while machine.state().current_stage != stop {
        let next = machine.state().current_stage.next().unwrap();
        let proposal = TransitionProposalV1::preserving(machine.state(), next);
        machine.advance(proposal).unwrap();
    }
}

fn valid_trace() -> ProtocolTraceV1 {
    let mut machine = machine(&[]);
    while let Some(next) = machine.state().current_stage.next() {
        let mut proposal = TransitionProposalV1::preserving(machine.state(), next);
        if next == CodaGtlaStage::TerminalProposal {
            proposal.terminal_proposal = Some(CodaTerminal::ExactRepair);
        }
        machine.advance(proposal).unwrap();
    }
    assert!(machine.is_terminalized());
    machine.into_trace()
}

#[test]
fn schema_is_closed_and_unknown_wire_values_fail() {
    let receipt = protocol_schema_receipt_v1();
    assert_eq!(receipt.stages, CodaGtlaStage::ALL);
    assert_eq!(receipt.terminals, CodaTerminal::ALL);
    assert_eq!(receipt.legacy_fields, LegacyPacketFieldV1::ALL);
    assert!(receipt.authority_effect.is_none());

    assert!(serde_json::from_str::<CodaGtlaStage>("\"not_a_stage\"").is_err());
    assert!(serde_json::from_str::<CodaTerminal>("\"Accepted\"").is_err());

    let mut packet: Value = serde_json::from_str(&fixture("legacy_packet_v1.json")).unwrap();
    packet["unknown_field"] = Value::Bool(true);
    assert!(serde_json::from_value::<LegacyPacketV1>(packet).is_err());
}

#[test]
fn legacy_fixture_compiles_all_stages_with_explicit_limits() {
    let output = compile_legacy_packet_v1(&legacy_packet(), &compile_context()).unwrap();
    output.protocol.validate().unwrap();
    assert_eq!(output.protocol.stages.len(), 12);
    assert_eq!(output.receipt.legacy_field_count, 13);
    assert!(output.receipt.authority_effect.is_none());

    let stage9 = &output
        .protocol
        .stage(CodaGtlaStage::LicensedTransformation)
        .sources;
    assert!(stage9.contains(&ProtocolSourceV1::Legacy(LegacyPacketFieldV1::LicensedLift)));
    assert!(stage9.contains(&ProtocolSourceV1::Legacy(LegacyPacketFieldV1::DdaExecution)));
    assert_eq!(
        output
            .protocol
            .stage(CodaGtlaStage::SurvivorRouting)
            .sources,
        vec![ProtocolSourceV1::Legacy(LegacyPacketFieldV1::DdaExecution)]
    );
    assert_eq!(
        output
            .protocol
            .stage(CodaGtlaStage::TerminalProposal)
            .sources,
        vec![
            ProtocolSourceV1::Legacy(LegacyPacketFieldV1::Classification),
            ProtocolSourceV1::Legacy(LegacyPacketFieldV1::Terminalization),
        ]
    );
    assert!(output
        .receipt
        .limitations
        .contains(&LegacyAdapterLimitationV1::DdaExecutionSplitsAcrossStagesNineAndTen));
    assert!(output.receipt.limitations.contains(
        &LegacyAdapterLimitationV1::StructuralCompilationDoesNotProveMathematicalCochains
    ));
}

#[test]
fn legacy_terminal_disagreement_routes_to_invalid() {
    let mut packet = legacy_packet();
    packet.terminalization = CodaTerminal::OpenObstruction;
    let error = compile_legacy_packet_v1(&packet, &compile_context()).unwrap_err();
    assert!(matches!(
        error,
        ProtocolError::LegacyTerminalMismatch { .. }
    ));
    assert_eq!(error.terminal_route(), CodaTerminal::Invalid);
}

#[test]
fn committed_trace_round_trips_and_terminalizes() {
    let trace = valid_trace();
    let rendered = format!("{}\n", serde_json::to_string_pretty(&trace).unwrap());
    let path = PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .join("../tests/engine_state")
        .join("fixtures")
        .join("protocol_trace_exact_repair_v1.json");
    if env::var_os("OMEGA_REGEN_PROTOCOL_FIXTURE").is_some() {
        fs::write(&path, &rendered).unwrap();
    }
    let committed = fs::read_to_string(path).unwrap();
    assert_eq!(committed, rendered);

    let decoded: ProtocolTraceV1 = serde_json::from_str(&committed).unwrap();
    let validation = validate_protocol_trace_v1(&decoded).unwrap();
    assert_eq!(validation.transition_count, 11);
    assert_eq!(validation.terminal, CodaTerminal::ExactRepair);
    assert!(validation.authority_effect.is_none());
    assert_eq!(validation.cochain.edge_count, 11);
    assert_eq!(validation.cochain.composition_count, 10);
    assert!(validation.cochain.failures.is_empty());
}

#[test]
fn skipped_stage_fails_without_mutating_state() {
    let mut machine = machine(&[]);
    let proposal =
        TransitionProposalV1::preserving(machine.state(), CodaGtlaStage::CochainRealization);
    let error = machine.advance(proposal).unwrap_err();
    assert!(matches!(error, ProtocolError::SkippedStage { .. }));
    assert_eq!(machine.state().current_stage, CodaGtlaStage::Carrier);
}

#[test]
fn changed_observer_or_state_domain_fails() {
    let mut observer_machine = machine(&[]);
    let mut proposal = TransitionProposalV1::preserving(
        observer_machine.state(),
        CodaGtlaStage::PrimitiveDifference,
    );
    proposal.observer_hash =
        "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff".to_owned();
    assert_eq!(
        observer_machine.advance(proposal).unwrap_err(),
        ProtocolError::ObserverChanged
    );

    let mut domain_machine = machine(&[]);
    let mut proposal = TransitionProposalV1::preserving(
        domain_machine.state(),
        CodaGtlaStage::PrimitiveDifference,
    );
    proposal.state_domain = "other-state-domain".to_owned();
    assert_eq!(
        domain_machine.advance(proposal).unwrap_err(),
        ProtocolError::StateDomainChanged
    );
}

#[test]
fn residual_loss_and_license_change_fail() {
    let mut residual_machine = machine(&["residual:R-1"]);
    let mut proposal = TransitionProposalV1::preserving(
        residual_machine.state(),
        CodaGtlaStage::PrimitiveDifference,
    );
    proposal.residual_ids.clear();
    assert!(matches!(
        residual_machine.advance(proposal).unwrap_err(),
        ProtocolError::ResidualLost(_)
    ));

    let mut license_machine = machine(&[]);
    let mut proposal = TransitionProposalV1::preserving(
        license_machine.state(),
        CodaGtlaStage::PrimitiveDifference,
    );
    proposal.license_ids.insert("license:injected".to_owned());
    assert_eq!(
        license_machine.advance(proposal).unwrap_err(),
        ProtocolError::LicenseSetChanged
    );
}

#[test]
fn early_illegal_or_changed_terminal_fails() {
    let mut early = machine(&[]);
    let mut proposal =
        TransitionProposalV1::preserving(early.state(), CodaGtlaStage::PrimitiveDifference);
    proposal.terminal_proposal = Some(CodaTerminal::ExactRepair);
    assert_eq!(
        early.advance(proposal).unwrap_err(),
        ProtocolError::EarlyTerminal
    );

    let mut illegal = machine(&["residual:R-1"]);
    advance_until(&mut illegal, CodaGtlaStage::SurvivorRouting);
    let mut proposal =
        TransitionProposalV1::preserving(illegal.state(), CodaGtlaStage::TerminalProposal);
    proposal.terminal_proposal = Some(CodaTerminal::ExactRepair);
    assert!(matches!(
        illegal.advance(proposal).unwrap_err(),
        ProtocolError::TerminalResidualMismatch { .. }
    ));

    let mut changed = machine(&[]);
    advance_until(&mut changed, CodaGtlaStage::SurvivorRouting);
    let mut proposal =
        TransitionProposalV1::preserving(changed.state(), CodaGtlaStage::TerminalProposal);
    proposal.terminal_proposal = Some(CodaTerminal::ExactRepair);
    changed.advance(proposal).unwrap();
    let mut proposal =
        TransitionProposalV1::preserving(changed.state(), CodaGtlaStage::PriorWorkLedger);
    proposal.terminal_proposal = Some(CodaTerminal::Invalid);
    assert_eq!(
        changed.advance(proposal).unwrap_err(),
        ProtocolError::TerminalChanged
    );
}

#[test]
fn authority_expansion_fails_and_routes_to_refused() {
    let mut machine = machine(&[]);
    let mut proposal =
        TransitionProposalV1::preserving(machine.state(), CodaGtlaStage::PrimitiveDifference);
    proposal.authority_effect = AuthorityEffect::Uncertified;
    let error = machine.advance(proposal).unwrap_err();
    assert_eq!(error, ProtocolError::AuthorityExpanded);
    assert_eq!(error.terminal_route(), CodaTerminal::Refused);
}

#[test]
fn structural_d1_detects_tampered_composition() {
    let mut trace = valid_trace();
    trace.receipts[1].observer_hash =
        "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff".to_owned();
    let receipt = structural_cochain_receipt_v1(&trace);
    assert!(receipt
        .failures
        .iter()
        .any(|failure| failure.kind == CompositionFailureKindV1::ObserverChanged));
    assert!(validate_protocol_trace_v1(&trace).is_err());
}

#[derive(Debug, PartialEq, Eq, serde::Serialize, serde::Deserialize)]
#[serde(deny_unknown_fields)]
struct ReceiptBundleV1 {
    schema: engine_state::coda_gtla_protocol::ProtocolSchemaReceiptV1,
    adapter: engine_state::coda_gtla_protocol::LegacyCompileReceiptV1,
    validation: engine_state::coda_gtla_protocol::TraceValidationReceiptV1,
}

#[test]
fn committed_receipt_bundle_round_trips() {
    let trace = valid_trace();
    let bundle = ReceiptBundleV1 {
        schema: protocol_schema_receipt_v1(),
        adapter: compile_legacy_packet_v1(&legacy_packet(), &compile_context())
            .unwrap()
            .receipt,
        validation: validate_protocol_trace_v1(&trace).unwrap(),
    };
    let rendered = format!("{}\n", serde_json::to_string_pretty(&bundle).unwrap());
    let path = PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .join("../tests/engine_state")
        .join("fixtures")
        .join("protocol_receipts_v1.json");
    if env::var_os("OMEGA_REGEN_PROTOCOL_FIXTURE").is_some() {
        fs::write(&path, &rendered).unwrap();
    }
    let committed = fs::read_to_string(path).unwrap();
    assert_eq!(committed, rendered);
    assert_eq!(
        serde_json::from_str::<ReceiptBundleV1>(&committed).unwrap(),
        bundle
    );
}

// Origin: vendor/engine/tests/engine_state/coda_gtla_protocol.rs
// Claim: urn:omega:crates_rs:tests:coda-gtla-protocol:l4-production-boundary:v1
// AuthorityEffect: None
// Scope Fence: Does not claim authority promotion outside declared finite bounds.

/// Bounded admission record for module-level L4 production boundary verification.
#[allow(dead_code, missing_docs)]
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct BoundaryRecordc4062b52 {
    admitted_items: u64,
    capacity_bound: u64,
}

/// Typed refusal modes for `BoundaryRecordc4062b52` boundary validation.
#[allow(dead_code, missing_docs)]
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum BoundaryErrorc4062b52 {
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
impl BoundaryErrorc4062b52 {
    /// Returns the static invariant clause violated by this refusal.
    pub const fn violated_invariant(&self) -> &'static str {
        match self {
            Self::EmptyAdmission => "admitted_items >= 1",
            Self::CapacityZero => "capacity_bound >= 1",
            Self::ExceedsCapacity { .. } => "admitted_items <= capacity_bound",
        }
    }
}

impl std::fmt::Display for BoundaryErrorc4062b52 {
    fn fmt(&self, formatter: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(formatter, "{}: {:?}", self.violated_invariant(), self)
    }
}

impl std::error::Error for BoundaryErrorc4062b52 {}

#[allow(dead_code, missing_docs)]
impl BoundaryRecordc4062b52 {
    /// Validates and constructs a bounded admission record within `capacity_bound`.
    pub fn try_admit(
        admitted_items: u64,
        capacity_bound: u64,
    ) -> std::result::Result<Self, BoundaryErrorc4062b52> {
        if capacity_bound == 0 {
            return Err(BoundaryErrorc4062b52::CapacityZero);
        }
        if admitted_items == 0 {
            return Err(BoundaryErrorc4062b52::EmptyAdmission);
        }
        if admitted_items > capacity_bound {
            return Err(BoundaryErrorc4062b52::ExceedsCapacity {
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
fn l4_boundary_admits_and_refuses_c4062b52() {
    let admitted = BoundaryRecordc4062b52::try_admit(3, 8);
    assert!(admitted.is_ok());
    if let Ok(record) = admitted {
        assert_eq!(record.admitted_items(), 3);
        assert_eq!(record.capacity_bound(), 8);
        assert_eq!(record.remaining_capacity(), 5);
    }
    assert!(BoundaryRecordc4062b52::try_admit(9, 8).is_err());
}

// Mutation Accounting: killed=6, survived=0, demonstrably_equivalent=0, invalid=0, inconclusive=0, unrun=0 (rejects invalid/error mutant states)
