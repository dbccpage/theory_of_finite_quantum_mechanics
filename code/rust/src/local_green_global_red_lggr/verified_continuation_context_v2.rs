
use std::collections::BTreeMap;

use serde::{Deserialize, Serialize};

use crate::epk_engine::{
    calculate_metrics, evaluator_gluing_defect, BoundarySlice, CompositionRecord, EpkError,
    EpkMetrics, GluingDefect, TraceLedger,
};
use omega_types::authority::AuthorityEffect;
use omega_types::ceiling::EvidenceCeiling;
use omega_types::{DetectorCapacityEvidence, DetectorDeploymentDeclaration};

use crate::adequacy::{
    evaluate_detector_adequacy, DetectorAdequacyVerdict, DetectorAdequacyVerdictKind,
};
use crate::bound_measurement::CanonicalHasher;
use crate::ledger::EpkResidualLedger;
use crate::verdict::{classify, EvaluatorProvenance, LggrVerdict};

pub const V2_CONTEXT_SCHEMA: &str = "omega.epk.verified-continuation-context.v2";


#[derive(Debug, Clone, PartialEq, thiserror::Error)]
pub enum TypedRefusal {
    #[error("schema {found:?} refused; this verifier accepts only {expected}")]
    SchemaRefused {
        found: String,
        expected: &'static str,
    },
    #[error("no accepted intake receipt: Prime 001-I/000 admission was never established")]
    IntakeNotAccepted,
    #[error("intake receipt is bound to run {receipt_run}, packet declares {packet_run}")]
    IntakeRunMismatch {
        receipt_run: String,
        packet_run: String,
    },
    #[error("empty corpus")]
    EmptyCorpus,
    #[error("selected row {index} out of range for {len} records")]
    RowOutOfRange { index: usize, len: usize },
    #[error(
        "local evaluator trace mismatch on {record_id}: declared (l={declared_left}, \
         r={declared_right}), ledger has (l={ledger_left:?}, r={ledger_right:?})"
    )]
    LocalTraceMismatch {
        record_id: String,
        declared_left: bool,
        declared_right: bool,
        ledger_left: Option<bool>,
        ledger_right: Option<bool>,
    },
    #[error("no global evaluator trace for {record_id}: E_g cannot be replayed, so Exhibited is refused")]
    GlobalTraceMissing { record_id: String },
    #[error(
        "global evaluator trace mismatch on {record_id}: declared {declared}, replayed {replayed}"
    )]
    GlobalTraceMismatch {
        record_id: String,
        declared: bool,
        replayed: bool,
    },
    #[error("prior refusal {0:?} cannot be cleared by a later packet")]
    PriorRefusalNotMonotone(ContinuationBlockerV2),
    #[error("no trusted verifier for {capability}: the fact cannot be established")]
    NoTrustedVerifier { capability: &'static str },
    #[error("a declaration is required before capacity can be solved")]
    DeclarationMissing,
    #[error("capacity solver refused: {detail}")]
    CapacitySolverRefused { detail: String },
    #[error(transparent)]
    Metrics(#[from] EpkError),
}


#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct AcceptedIntakeReceipt {
    run_id: String,
    candidate_digest: String,
    witness_certificate: String,
    next_carrier: String,
}

impl AcceptedIntakeReceipt {
    pub fn admit(
        run_id: impl Into<String>,
        candidate_digest: impl Into<String>,
        witness_certificate: impl Into<String>,
        next_carrier: impl Into<String>,
    ) -> Option<Self> {
        let witness_certificate = witness_certificate.into();
        let next_carrier = next_carrier.into();
        if witness_certificate.is_empty() || next_carrier.is_empty() {
            return None;
        }
        Some(Self {
            run_id: run_id.into(),
            candidate_digest: candidate_digest.into(),
            witness_certificate,
            next_carrier,
        })
    }

    pub fn run_id(&self) -> &str {
        &self.run_id
    }
    pub fn candidate_digest(&self) -> &str {
        &self.candidate_digest
    }
    pub fn witness_certificate(&self) -> &str {
        &self.witness_certificate
    }
    pub fn next_carrier(&self) -> &str {
        &self.next_carrier
    }
    pub fn has_witness(&self) -> bool {
        !self.witness_certificate.is_empty()
    }
    pub fn next_carrier_declared(&self) -> bool {
        !self.next_carrier.is_empty()
    }
}


#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct TransportClaim {
    pub source_carrier: String,
    pub target_carrier: String,
    pub loss_ledger: Vec<String>,
}

#[derive(Debug, Clone, PartialEq, Serialize)]
pub struct ResidualPreservationWitness {
    source_carrier: String,
    target_carrier: String,
    source_ngd: f64,
    target_ngd: f64,
    preserved: bool,
    loss_ledger: Vec<String>,
}

impl ResidualPreservationWitness {
    fn from_measurement(claim: &TransportClaim, source_ngd: f64, measured_target: f64) -> Self {
        let preserved = measured_target.is_finite()
            && source_ngd.is_finite()
            && (measured_target - source_ngd).abs() <= f64::EPSILON
            && claim.loss_ledger.is_empty();
        Self {
            source_carrier: claim.source_carrier.clone(),
            target_carrier: claim.target_carrier.clone(),
            source_ngd,
            target_ngd: measured_target,
            preserved,
            loss_ledger: claim.loss_ledger.clone(),
        }
    }

    pub fn source_carrier(&self) -> &str {
        &self.source_carrier
    }
    pub fn target_carrier(&self) -> &str {
        &self.target_carrier
    }

    pub fn preserved(&self) -> bool {
        self.preserved
    }
    pub fn source_ngd(&self) -> f64 {
        self.source_ngd
    }
    pub fn target_ngd(&self) -> f64 {
        self.target_ngd
    }
    pub fn loss_ledger(&self) -> &[String] {
        &self.loss_ledger
    }
}


#[derive(Debug, Clone, Serialize)]
pub struct RawEvidencePacket {
    pub schema: String,
    pub run_id: String,
    pub accepted_intake: Option<AcceptedIntakeReceipt>,
    pub records: Vec<CompositionRecord>,
    pub trace_ledger: TraceLedger,
    pub boundary: BoundarySlice,
    pub declaration: Option<DetectorDeploymentDeclaration>,
    pub selected_row: usize,
    pub transport: Option<TransportClaim>,
    pub budget_remaining: f64,
    pub delta_control: f64,
    pub parent_receipt_hash: Option<String>,
    #[serde(rename = "gtla_refusal")]
    pub coda_gtla_refusal: bool,
}


pub trait AdmissionAuthority {
    fn confirm_admission(&self, receipt: &AcceptedIntakeReceipt) -> Result<(), TypedRefusal>;
}

pub trait GlobalEvaluatorReplay {
    fn replay_global(&self, record: &CompositionRecord) -> Result<bool, TypedRefusal>;
}

pub trait CapacitySolver {
    fn solve(
        &self,
        declaration: &DetectorDeploymentDeclaration,
        records: &[CompositionRecord],
        trace_ledger: &TraceLedger,
        boundary: &BoundarySlice,
    ) -> Result<DetectorCapacityEvidence, TypedRefusal>;
}

pub trait TransportVerifier {
    fn measure_target(&self, claim: &TransportClaim, source_ngd: f64) -> Result<f64, TypedRefusal>;
}

pub trait RefusalStore {
    fn standing_refusals(&self, run_id: &str) -> Vec<ContinuationBlockerV2>;
}

pub trait VerifierSuite {
    fn admission(&self) -> &dyn AdmissionAuthority;
    fn global_replay(&self) -> &dyn GlobalEvaluatorReplay;
    fn capacity(&self) -> &dyn CapacitySolver;
    fn transport(&self) -> &dyn TransportVerifier;
    fn refusals(&self) -> &dyn RefusalStore;
}

#[derive(Debug, Clone, Copy, Default)]
pub struct RefusingVerifierSuite;

impl AdmissionAuthority for RefusingVerifierSuite {
    fn confirm_admission(&self, _r: &AcceptedIntakeReceipt) -> Result<(), TypedRefusal> {
        Err(TypedRefusal::NoTrustedVerifier {
            capability: "admission",
        })
    }
}
impl GlobalEvaluatorReplay for RefusingVerifierSuite {
    fn replay_global(&self, _r: &CompositionRecord) -> Result<bool, TypedRefusal> {
        Err(TypedRefusal::NoTrustedVerifier {
            capability: "global evaluator replay",
        })
    }
}
impl CapacitySolver for RefusingVerifierSuite {
    fn solve(
        &self,
        _d: &DetectorDeploymentDeclaration,
        _r: &[CompositionRecord],
        _l: &TraceLedger,
        _b: &BoundarySlice,
    ) -> Result<DetectorCapacityEvidence, TypedRefusal> {
        Err(TypedRefusal::NoTrustedVerifier {
            capability: "capacity solver",
        })
    }
}
impl TransportVerifier for RefusingVerifierSuite {
    fn measure_target(&self, _c: &TransportClaim, _s: f64) -> Result<f64, TypedRefusal> {
        Err(TypedRefusal::NoTrustedVerifier {
            capability: "transport verifier",
        })
    }
}
impl RefusalStore for RefusingVerifierSuite {
    fn standing_refusals(&self, _run_id: &str) -> Vec<ContinuationBlockerV2> {
        vec![ContinuationBlockerV2::PriorRefusalStanding]
    }
}
impl VerifierSuite for RefusingVerifierSuite {
    fn admission(&self) -> &dyn AdmissionAuthority {
        self
    }
    fn global_replay(&self) -> &dyn GlobalEvaluatorReplay {
        self
    }
    fn capacity(&self) -> &dyn CapacitySolver {
        self
    }
    fn transport(&self) -> &dyn TransportVerifier {
        self
    }
    fn refusals(&self) -> &dyn RefusalStore {
        self
    }
}


#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, PartialOrd, Ord, Serialize, Deserialize)]
pub enum ContinuationBlockerV2 {
    IntakeNotAccepted,
    WitnessMissing,
    NextCarrierUndeclared,
    DetectorInadequate,
    AdapterNotPreserving,
    ProvenanceNotExhibited,
    BudgetExhausted,
    #[serde(rename = "GtlaRefusal")]
    CodaGtlaRefusal,
    PriorRefusalStanding,
}


#[derive(Debug, Clone, PartialEq, Serialize)]
pub struct VerifiedContinuationContextV2 {
    schema: &'static str,
    root_digest: String,
    run_id: String,
    metrics: EpkMetrics,
    ledger: EpkResidualLedger,
    #[serde(skip)]
    adequacy: DetectorAdequacyVerdict,
    adequacy_kind: DetectorAdequacyVerdictKind,
    defect: GluingDefect,
    record_id: String,
    verdict: LggrVerdict,
    provenance: EvaluatorProvenance,
    preservation: Option<ResidualPreservationWitness>,
    has_witness: bool,
    next_carrier_declared: bool,
    budget_remaining: f64,
    delta_control: f64,
    prior_refusals: Vec<ContinuationBlockerV2>,
    #[serde(rename = "gtla_refusal")]
    coda_gtla_refusal: bool,
    parent_receipt_hash: Option<String>,
}

impl VerifiedContinuationContextV2 {
    pub fn root_digest(&self) -> &str {
        &self.root_digest
    }
    pub fn run_id(&self) -> &str {
        &self.run_id
    }
    pub fn metrics(&self) -> &EpkMetrics {
        &self.metrics
    }
    pub fn ledger(&self) -> &EpkResidualLedger {
        &self.ledger
    }
    pub fn adequacy(&self) -> &DetectorAdequacyVerdict {
        &self.adequacy
    }
    pub fn defect(&self) -> &GluingDefect {
        &self.defect
    }
    pub fn record_id(&self) -> &str {
        &self.record_id
    }
    pub fn verdict(&self) -> &LggrVerdict {
        &self.verdict
    }
    pub fn provenance(&self) -> EvaluatorProvenance {
        self.provenance
    }
    pub fn preservation(&self) -> Option<&ResidualPreservationWitness> {
        self.preservation.as_ref()
    }
    pub fn authority_effect(&self) -> AuthorityEffect {
        AuthorityEffect::None
    }
    pub fn evidence_ceiling(&self) -> EvidenceCeiling {
        self.verdict
            .evidence_ceiling()
            .meet(EvidenceCeiling::BoundaryChecked)
    }
}


#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct ContinuationDecision {
    blockers: Vec<ContinuationBlockerV2>,
    root_digest: String,
}

impl ContinuationDecision {
    pub fn may_continue(&self) -> bool {
        self.blockers.is_empty()
    }
    pub fn blockers(&self) -> &[ContinuationBlockerV2] {
        &self.blockers
    }
    pub fn root_digest(&self) -> &str {
        &self.root_digest
    }
    pub fn authority_effect(&self) -> AuthorityEffect {
        AuthorityEffect::None
    }
    pub fn step_terminal(&self) -> &'static str {
        if self.may_continue() {
            "LOCAL_GREEN_FOR_SCOPE"
        } else {
            "TERMINAL_WITH_DEBT"
        }
    }
}


fn verify_intake<'a>(
    packet: &'a RawEvidencePacket,
    suite: &dyn VerifierSuite,
) -> Result<&'a AcceptedIntakeReceipt, TypedRefusal> {
    if packet.schema != V2_CONTEXT_SCHEMA {
        return Err(TypedRefusal::SchemaRefused {
            found: packet.schema.clone(),
            expected: V2_CONTEXT_SCHEMA,
        });
    }

    let intake = packet
        .accepted_intake
        .as_ref()
        .ok_or(TypedRefusal::IntakeNotAccepted)?;
    if intake.run_id() != packet.run_id {
        return Err(TypedRefusal::IntakeRunMismatch {
            receipt_run: intake.run_id().to_string(),
            packet_run: packet.run_id.clone(),
        });
    }
    suite.admission().confirm_admission(intake)?;
    Ok(intake)
}

fn verify_trace_ledger(packet: &RawEvidencePacket) -> Result<(), TypedRefusal> {
    for r in &packet.records {
        let l = packet
            .trace_ledger
            .get(&r.left_trace_id)
            .map(|t| t.evaluator_pass);
        let rt = packet
            .trace_ledger
            .get(&r.right_trace_id)
            .map(|t| t.evaluator_pass);
        if l != Some(r.local_left_pass) || rt != Some(r.local_right_pass) {
            return Err(TypedRefusal::LocalTraceMismatch {
                record_id: r.composed_trace_id.clone(),
                declared_left: r.local_left_pass,
                declared_right: r.local_right_pass,
                ledger_left: l,
                ledger_right: rt,
            });
        }
    }
    Ok(())
}

fn replay_global_traces(
    packet: &RawEvidencePacket,
    suite: &dyn VerifierSuite,
) -> Result<BTreeMap<String, bool>, TypedRefusal> {
    let mut replayed_global: BTreeMap<String, bool> = BTreeMap::new();
    for r in &packet.records {
        let replayed = suite.global_replay().replay_global(r)?;
        if replayed != r.global_pass {
            return Err(TypedRefusal::GlobalTraceMismatch {
                record_id: r.composed_trace_id.clone(),
                declared: r.global_pass,
                replayed,
            });
        }
        replayed_global.insert(r.composed_trace_id.clone(), replayed);
    }
    Ok(replayed_global)
}

fn hash_preservation_witness(
    h: &mut CanonicalHasher,
    preservation: Option<&ResidualPreservationWitness>,
) {
    match preservation {
        Some(w) => {
            h.u8_field("preservation", 1);
            h.str_field("preservation_source", w.source_carrier());
            h.str_field("preservation_target", w.target_carrier());
            h.f64_field("preservation_source_ngd", w.source_ngd());
            h.f64_field("preservation_target_ngd", w.target_ngd());
            h.u8_field("preservation_preserved", w.preserved() as u8);
            h.bytes(
                "preservation_loss_count",
                &(w.loss_ledger().len() as u64).to_be_bytes(),
            );
            for l in w.loss_ledger() {
                h.str_field("preservation_loss", l);
            }
        }
        None => {
            h.u8_field("preservation", 0);
        }
    }
}

fn compute_context_digest(
    packet: &RawEvidencePacket,
    intake: &AcceptedIntakeReceipt,
    replayed_global: &BTreeMap<String, bool>,
    adequacy: &DetectorAdequacyVerdict,
    row: usize,
    defect: &GluingDefect,
    ledger: &EpkResidualLedger,
    preservation: Option<&ResidualPreservationWitness>,
    standing: &[ContinuationBlockerV2],
) -> String {
    let mut h = CanonicalHasher::new(V2_CONTEXT_SCHEMA);
    h.str_field("run_id", &packet.run_id);
    h.str_field("intake_run", intake.run_id());
    h.str_field("intake_candidate", intake.candidate_digest());
    h.str_field("intake_witness", intake.witness_certificate());
    h.str_field("intake_next_carrier", intake.next_carrier());
    for r in &packet.records {
        h.str_field("row_id", &r.composed_trace_id);
        h.u8_field("row_l", r.local_left_pass as u8);
        h.u8_field("row_r", r.local_right_pass as u8);
        h.u8_field("row_g", r.global_pass as u8);
    }
    for (id, g) in replayed_global {
        h.str_field("replayed_id", id);
        h.u8_field("replayed_val", *g as u8);
    }
    h.str_field("boundary", &packet.boundary.name);
    h.str_field("adequacy_kind", adequacy_kind_tag(adequacy.kind()));
    h.str_field("adequacy_corpus", adequacy.observed_corpus_digest());
    h.opt_str("adequacy_declaration", adequacy.declaration_digest());
    h.opt_f64("adequacy_capacity", adequacy.capacity_value());
    h.opt_f64("adequacy_epsilon", adequacy.epsilon());
    h.bytes(
        "adequacy_failure_count",
        &(adequacy.structural_failures().len() as u64).to_be_bytes(),
    );
    for f in adequacy.structural_failures() {
        h.str_field("adequacy_failure", structural_failure_tag(f));
    }
    h.bytes("selected_row", &(row as u64).to_be_bytes());
    h.i8_field("delta_eval", defect.delta_eval);
    h.f64_field("ngd", ledger.ngd);
    h.opt_f64("nrke", ledger.nrke);
    hash_preservation_witness(&mut h, preservation);
    h.f64_field("budget_remaining", packet.budget_remaining);
    h.f64_field("delta_control", packet.delta_control);
    h.bytes(
        "standing_refusal_count",
        &(standing.len() as u64).to_be_bytes(),
    );
    for r in standing {
        h.str_field("standing_refusal", blocker_tag(*r));
    }
    h.u8_field("gtla_refusal", packet.coda_gtla_refusal as u8);
    h.opt_str("parent_receipt", packet.parent_receipt_hash.as_deref());
    h.finish()
}

fn resolve_preservation(
    packet: &RawEvidencePacket,
    suite: &dyn VerifierSuite,
    ledger: &EpkResidualLedger,
) -> Result<Option<ResidualPreservationWitness>, TypedRefusal> {
    match packet.transport.as_ref() {
        Some(claim) => {
            let measured = suite.transport().measure_target(claim, ledger.ngd)?;
            Ok(Some(ResidualPreservationWitness::from_measurement(
                claim, ledger.ngd, measured,
            )))
        }
        None => Ok(None),
    }
}

pub fn verify(
    packet: &RawEvidencePacket,
    suite: &dyn VerifierSuite,
) -> Result<VerifiedContinuationContextV2, TypedRefusal> {
    let intake = verify_intake(packet, suite)?;

    if packet.records.is_empty() {
        return Err(TypedRefusal::EmptyCorpus);
    }
    let row = packet.selected_row;
    let record = packet.records.get(row).ok_or(TypedRefusal::RowOutOfRange {
        index: row,
        len: packet.records.len(),
    })?;

    verify_trace_ledger(packet)?;
    let replayed_global = replay_global_traces(packet, suite)?;
    let provenance = EvaluatorProvenance::Exhibited;

    let declaration = packet
        .declaration
        .as_ref()
        .ok_or(TypedRefusal::DeclarationMissing)?;
    let solved_evidence = suite.capacity().solve(
        declaration,
        &packet.records,
        &packet.trace_ledger,
        &packet.boundary,
    )?;
    let adequacy = evaluate_detector_adequacy(
        Some(declaration),
        Some(&solved_evidence),
        &packet.records,
        &packet.trace_ledger,
        &packet.boundary,
    );

    let metrics = calculate_metrics(
        &packet.records,
        Some(&packet.trace_ledger),
        None,
        None,
        None,
    )?;
    let ledger = EpkResidualLedger::from_metrics(&metrics);
    let defect = evaluator_gluing_defect(record);
    let verdict = classify(&defect, Some(&adequacy), provenance)
        .expect("defects from evaluator_gluing_defect are well-formed");

    let preservation = resolve_preservation(packet, suite, &ledger)?;

    let standing = suite.refusals().standing_refusals(&packet.run_id);
    let root_digest = compute_context_digest(
        packet,
        intake,
        &replayed_global,
        &adequacy,
        row,
        &defect,
        &ledger,
        preservation.as_ref(),
        &standing,
    );

    Ok(VerifiedContinuationContextV2 {
        schema: V2_CONTEXT_SCHEMA,
        root_digest,
        run_id: packet.run_id.clone(),
        metrics,
        ledger,
        adequacy_kind: adequacy.kind(),
        adequacy,
        defect,
        record_id: record.composed_trace_id.clone(),
        verdict,
        provenance,
        preservation,
        has_witness: intake.has_witness(),
        next_carrier_declared: intake.next_carrier_declared(),
        budget_remaining: packet.budget_remaining,
        delta_control: packet.delta_control,
        prior_refusals: standing,
        coda_gtla_refusal: packet.coda_gtla_refusal,
        parent_receipt_hash: packet.parent_receipt_hash.clone(),
    })
}

fn structural_failure_core_tag(f: &crate::adequacy::DetectorStructuralFailure) -> Option<&'static str> {
    use crate::adequacy::DetectorStructuralFailure as F;
    match f {
        F::EmptyCorpus => Some("EmptyCorpus"),
        F::GlobalEqualsLocalProduct => Some("GlobalEqualsLocalProduct"),
        F::LocalProductConstant => Some("LocalProductConstant"),
        F::MissingNgdWitness => Some("MissingNgdWitness"),
        F::MissingLrgrWitness => Some("MissingLrgrWitness"),
        F::CarrierClosureVacuous => Some("CarrierClosureVacuous"),
        _ => None,
    }
}

fn structural_failure_extended_tag(f: &crate::adequacy::DetectorStructuralFailure) -> &'static str {
    use crate::adequacy::DetectorStructuralFailure as F;
    match f {
        F::EvaluatorConstant { .. } => "EvaluatorConstant",
        F::EvaluatorDoesNotSeparate { .. } => "EvaluatorDoesNotSeparate",
        F::ProjectionCollision { .. } => "ProjectionCollision",
        F::MissingBlindSpotDeclaration { .. } => "MissingBlindSpotDeclaration",
        _ => "OtherStructuralFailure",
    }
}

fn structural_failure_tag(f: &crate::adequacy::DetectorStructuralFailure) -> &'static str {
    structural_failure_core_tag(f).unwrap_or_else(|| structural_failure_extended_tag(f))
}

fn blocker_tag(b: ContinuationBlockerV2) -> &'static str {
    match b {
        ContinuationBlockerV2::IntakeNotAccepted => "IntakeNotAccepted",
        ContinuationBlockerV2::WitnessMissing => "WitnessMissing",
        ContinuationBlockerV2::NextCarrierUndeclared => "NextCarrierUndeclared",
        ContinuationBlockerV2::DetectorInadequate => "DetectorInadequate",
        ContinuationBlockerV2::AdapterNotPreserving => "AdapterNotPreserving",
        ContinuationBlockerV2::ProvenanceNotExhibited => "ProvenanceNotExhibited",
        ContinuationBlockerV2::BudgetExhausted => "BudgetExhausted",
        ContinuationBlockerV2::CodaGtlaRefusal => "GtlaRefusal",
        ContinuationBlockerV2::PriorRefusalStanding => "PriorRefusalStanding",
    }
}

fn adequacy_kind_tag(k: DetectorAdequacyVerdictKind) -> &'static str {
    match k {
        DetectorAdequacyVerdictKind::Undeclared => "Undeclared",
        DetectorAdequacyVerdictKind::StructuralInadequate => "StructuralInadequate",
        DetectorAdequacyVerdictKind::NumericalCounterevidence => "NumericalCounterevidence",
        DetectorAdequacyVerdictKind::NumericallySupported => "NumericallySupported",
        DetectorAdequacyVerdictKind::NumericalUnresolved => "NumericalUnresolved",
    }
}

fn collect_intake_and_adequacy_blockers(
    context: &VerifiedContinuationContextV2,
    blockers: &mut Vec<ContinuationBlockerV2>,
) {
    if !context.has_witness {
        blockers.push(ContinuationBlockerV2::WitnessMissing);
    }
    if !context.next_carrier_declared {
        blockers.push(ContinuationBlockerV2::NextCarrierUndeclared);
    }
    if context.adequacy_kind != DetectorAdequacyVerdictKind::NumericallySupported {
        blockers.push(ContinuationBlockerV2::DetectorInadequate);
    }
    match &context.preservation {
        Some(w) if w.preserved() => {}
        _ => blockers.push(ContinuationBlockerV2::AdapterNotPreserving),
    }
}

fn collect_runtime_blockers(
    context: &VerifiedContinuationContextV2,
    blockers: &mut Vec<ContinuationBlockerV2>,
) {
    if context.provenance != EvaluatorProvenance::Exhibited {
        blockers.push(ContinuationBlockerV2::ProvenanceNotExhibited);
    }
    let budget_exhausted = !context.budget_remaining.is_finite()
        || !context.delta_control.is_finite()
        || context.budget_remaining - context.delta_control < 0.0;
    if budget_exhausted {
        blockers.push(ContinuationBlockerV2::BudgetExhausted);
    }
    if context.coda_gtla_refusal {
        blockers.push(ContinuationBlockerV2::CodaGtlaRefusal);
    }
    if !context.prior_refusals.is_empty() {
        blockers.push(ContinuationBlockerV2::PriorRefusalStanding);
    }
}

pub fn decide(context: &VerifiedContinuationContextV2) -> ContinuationDecision {
    let mut blockers = Vec::new();
    collect_intake_and_adequacy_blockers(context, &mut blockers);
    collect_runtime_blockers(context, &mut blockers);
    blockers.sort_unstable();
    blockers.dedup();
    ContinuationDecision {
        blockers,
        root_digest: context.root_digest.clone(),
    }
}
