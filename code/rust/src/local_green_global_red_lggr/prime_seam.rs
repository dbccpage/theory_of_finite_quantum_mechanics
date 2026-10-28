
use serde::{Deserialize, Serialize};

use engine_types::authority::AuthorityEffect;
use engine_types::ceiling::EvidenceCeiling;

use crate::epk_engine::GluingDefect;
use engine_policy::trichotomy::ObstructionDiagnosticClass;

use crate::adequacy::DetectorAdequacyVerdictKind;
use crate::bound_measurement::{verdict_tag, CanonicalHasher};
use crate::ledger::EpkResidualLedger;
use crate::verdict::LggrVerdict;

pub const LGGR_EPK_OBSERVATION_SCHEMA: &str = "omega.epk.lggr-observation.v1";
pub const PRIME_DESCENT_RECEIPT_SCHEMA: &str = "omega.epk.prime-descent-receipt.v1";

pub const V1_SCHEMA_DISPOSITION: &str = "REJECTED_UNSOUND";

pub const V1_QUARANTINE_REASON: &str = "v1 evidence binding is incomplete: the \
measurement digest omits the adequacy report, so a supported measurement accepts \
an unsupported observation. Quarantined pending VerifiedContinuationContextV2.";


#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub enum PrimeIntakeOutcome {
    AcceptDeclaration,
    RefusedMissingCarrier,
    RefusedMissingObserver,
    RefusedMissingWitness,
    AdapterInadequate,
}

impl PrimeIntakeOutcome {
    pub fn as_declared_str(&self) -> &'static str {
        match self {
            Self::AcceptDeclaration => "ACCEPT_DECLARATION",
            Self::RefusedMissingCarrier => "REFUSED_MISSING_CARRIER",
            Self::RefusedMissingObserver => "REFUSED_MISSING_OBSERVER",
            Self::RefusedMissingWitness => "REFUSED_MISSING_WITNESS",
            Self::AdapterInadequate => "ADAPTER_INADEQUATE",
        }
    }

    pub fn is_refusal(&self) -> bool {
        !matches!(self, Self::AcceptDeclaration)
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct CandidateDeclaration {
    pub artifact_id: String,
    pub locus_id: String,
    pub problem_family: String,
    pub primitive_difference_proposal: String,
    pub carrier_proposal: String,
    pub zero_rel_proposal: String,
    pub observer_proposal: String,
    pub witness_available: bool,
    pub quotient_or_refusal: String,
    pub adapter_confidence: String,
    pub status: String,
}

impl CandidateDeclaration {
    pub fn evaluate_intake(&self) -> PrimeIntakeOutcome {
        if self.carrier_proposal.is_empty() {
            return PrimeIntakeOutcome::RefusedMissingCarrier;
        }
        if self.observer_proposal.is_empty() {
            return PrimeIntakeOutcome::RefusedMissingObserver;
        }
        if !self.witness_available {
            return PrimeIntakeOutcome::RefusedMissingWitness;
        }
        if self.adapter_confidence == "inadequate" {
            return PrimeIntakeOutcome::AdapterInadequate;
        }
        PrimeIntakeOutcome::AcceptDeclaration
    }

    pub fn authority_effect(&self) -> AuthorityEffect {
        AuthorityEffect::None
    }
}


#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub enum PrimeDeclarationOutcome {
    AcceptDeclaration,
    RefuseMissingGrounding,
    RefuseMissingCarrier,
    RefuseMissingObserver,
    RefuseMissingPrimitiveDifference,
    RefuseMissingZeroRel,
    RefuseMissingWitness,
}

impl PrimeDeclarationOutcome {
    pub fn as_declared_str(&self) -> &'static str {
        match self {
            Self::AcceptDeclaration => "ACCEPT_DECLARATION",
            Self::RefuseMissingGrounding => "REFUSE_MISSING_GROUNDING",
            Self::RefuseMissingCarrier => "REFUSE_MISSING_CARRIER",
            Self::RefuseMissingObserver => "REFUSE_MISSING_OBSERVER",
            Self::RefuseMissingPrimitiveDifference => "REFUSE_MISSING_PRIMITIVE_DIFFERENCE",
            Self::RefuseMissingZeroRel => "REFUSE_MISSING_ZERO_REL",
            Self::RefuseMissingWitness => "REFUSE_MISSING_WITNESS",
        }
    }

    pub fn is_refusal(&self) -> bool {
        !matches!(self, Self::AcceptDeclaration)
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Default, Serialize, Deserialize)]
pub struct PrimeDeclarationOrder {
    pub step0_grounding_hash: String,
    pub step1_carrier_declared: bool,
    pub step2_observer_id: String,
    pub step3_primitive_difference_declared: bool,
    pub step4_zero_rel_rule: String,
    pub step5_witness_certificate: Option<String>,
    pub step6_quotient_policy: String,
}

impl PrimeDeclarationOrder {
    pub fn validate(&self) -> PrimeDeclarationOutcome {
        if self.step0_grounding_hash.is_empty() {
            return PrimeDeclarationOutcome::RefuseMissingGrounding;
        }
        if !self.step1_carrier_declared {
            return PrimeDeclarationOutcome::RefuseMissingCarrier;
        }
        if self.step2_observer_id.is_empty() {
            return PrimeDeclarationOutcome::RefuseMissingObserver;
        }
        if !self.step3_primitive_difference_declared {
            return PrimeDeclarationOutcome::RefuseMissingPrimitiveDifference;
        }
        if self.step4_zero_rel_rule.is_empty() {
            return PrimeDeclarationOutcome::RefuseMissingZeroRel;
        }
        match &self.step5_witness_certificate {
            None => PrimeDeclarationOutcome::RefuseMissingWitness,
            Some(cert) if cert.is_empty() => PrimeDeclarationOutcome::RefuseMissingWitness,
            Some(_) => PrimeDeclarationOutcome::AcceptDeclaration,
        }
    }
}


#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub enum AdequacyKindProjection {
    NotEvaluated,
    Undeclared,
    StructuralInadequate,
    NumericalCounterevidence,
    NumericallySupported,
    NumericalUnresolved,
}

impl AdequacyKindProjection {
    pub fn from_kind(kind: DetectorAdequacyVerdictKind) -> Self {
        match kind {
            DetectorAdequacyVerdictKind::Undeclared => Self::Undeclared,
            DetectorAdequacyVerdictKind::StructuralInadequate => Self::StructuralInadequate,
            DetectorAdequacyVerdictKind::NumericalCounterevidence => Self::NumericalCounterevidence,
            DetectorAdequacyVerdictKind::NumericallySupported => Self::NumericallySupported,
            DetectorAdequacyVerdictKind::NumericalUnresolved => Self::NumericalUnresolved,
        }
    }

    pub fn as_tag(&self) -> &'static str {
        match self {
            Self::NotEvaluated => "NotEvaluated",
            Self::Undeclared => "Undeclared",
            Self::StructuralInadequate => "StructuralInadequate",
            Self::NumericalCounterevidence => "NumericalCounterevidence",
            Self::NumericallySupported => "NumericallySupported",
            Self::NumericalUnresolved => "NumericalUnresolved",
        }
    }

    pub fn permits_detector_adequate(&self) -> bool {
        matches!(self, Self::NumericallySupported)
    }
}

#[derive(Debug, Clone, PartialEq, Serialize)]
pub struct LggrEpkObservation {
    schema: String,
    ledger: EpkResidualLedger,
    verdict: LggrVerdict,
    adequacy_kind: AdequacyKindProjection,
    observed_corpus_digest: Option<String>,
    record_id: String,
    defect: GluingDefect,
    obstruction_status: Option<ObstructionDiagnosticClass>,
}

impl LggrEpkObservation {
    #[allow(clippy::too_many_arguments)]
    pub(crate) fn new_bound(
        ledger: EpkResidualLedger,
        verdict: LggrVerdict,
        adequacy_kind: AdequacyKindProjection,
        corpus_digest: String,
        record_id: String,
        defect: GluingDefect,
        obstruction_status: Option<ObstructionDiagnosticClass>,
    ) -> Self {
        Self {
            schema: LGGR_EPK_OBSERVATION_SCHEMA.to_string(),
            ledger,
            verdict,
            adequacy_kind,
            observed_corpus_digest: Some(corpus_digest),
            record_id,
            defect,
            obstruction_status,
        }
    }

    pub fn record_id(&self) -> &str {
        &self.record_id
    }

    pub fn defect(&self) -> &GluingDefect {
        &self.defect
    }

    pub fn obstruction_status(&self) -> Option<ObstructionDiagnosticClass> {
        self.obstruction_status
    }

    pub fn schema(&self) -> &str {
        &self.schema
    }

    pub fn ledger(&self) -> &EpkResidualLedger {
        &self.ledger
    }

    pub fn verdict(&self) -> &LggrVerdict {
        &self.verdict
    }

    pub fn adequacy_kind(&self) -> AdequacyKindProjection {
        self.adequacy_kind
    }

    pub fn observed_corpus_digest(&self) -> Option<&str> {
        self.observed_corpus_digest.as_deref()
    }

    pub fn authority_effect(&self) -> AuthorityEffect {
        AuthorityEffect::None
    }

    pub fn evidence_ceiling(&self) -> EvidenceCeiling {
        self.verdict
            .evidence_ceiling()
            .meet(EvidenceCeiling::BoundaryChecked)
    }

    pub fn detector_adequate(&self) -> bool {
        self.adequacy_kind.permits_detector_adequate()
            && !matches!(
                self.verdict,
                LggrVerdict::GreenOracleNeeded { .. } | LggrVerdict::OracleExtractedUnsound { .. }
            )
    }
}


#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct PrimeDescentReceipt {
    pub schema: String,
    pub source_carrier: String,
    pub target_carrier: String,
    pub observed_corpus_digest: String,
    pub residual_preservation_verified: bool,
    pub loss_ledger: Vec<String>,
    pub receipt_hash: String,
}

impl PrimeDescentReceipt {
    pub fn recomputed_hash(&self, observation: &LggrEpkObservation) -> String {
        descent_receipt_hash(
            &self.source_carrier,
            &self.target_carrier,
            &self.observed_corpus_digest,
            self.residual_preservation_verified,
            &self.loss_ledger,
            observation,
        )
    }

    pub fn authority_effect(&self) -> AuthorityEffect {
        AuthorityEffect::None
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct VerifiedDescentReceipt(PrimeDescentReceipt);

impl VerifiedDescentReceipt {
    pub(crate) fn seal(receipt: PrimeDescentReceipt) -> Self {
        Self(receipt)
    }

    pub fn receipt(&self) -> &PrimeDescentReceipt {
        &self.0
    }

    pub fn residual_preservation_verified(&self) -> bool {
        self.0.residual_preservation_verified
    }

    pub fn observed_corpus_digest(&self) -> &str {
        &self.0.observed_corpus_digest
    }

    pub fn receipt_hash(&self) -> &str {
        &self.0.receipt_hash
    }

    pub fn authority_effect(&self) -> AuthorityEffect {
        AuthorityEffect::None
    }
}

pub(crate) fn descent_receipt_hash(
    source_carrier: &str,
    target_carrier: &str,
    observed_corpus_digest: &str,
    residual_preservation_verified: bool,
    loss_ledger: &[String],
    observation: &LggrEpkObservation,
) -> String {
    let mut h = CanonicalHasher::new(PRIME_DESCENT_RECEIPT_SCHEMA);
    h.str_field("source_carrier", source_carrier);
    h.str_field("target_carrier", target_carrier);
    h.str_field("observed_corpus_digest", observed_corpus_digest);
    h.u8_field(
        "residual_preservation_verified",
        residual_preservation_verified as u8,
    );
    h.str_field("record_id", observation.record_id());
    let d = observation.defect();
    h.i8_field("delta_eval", d.delta_eval);
    h.u8_field("local_product", d.local_product as u8);
    h.u8_field("global_pass", d.global_pass as u8);
    h.str_field("verdict", verdict_tag(observation.verdict()));
    h.str_field("adequacy_kind", observation.adequacy_kind().as_tag());
    h.str_field(
        "obstruction_status",
        match observation.obstruction_status() {
            None => "None",
            Some(ObstructionDiagnosticClass::ExactRepair) => "ExactRepair",
            Some(ObstructionDiagnosticClass::ClosedResidual) => "ClosedResidual",
            Some(ObstructionDiagnosticClass::ActiveClosureFailure) => "ActiveClosureFailure",
        },
    );
    h.f64_field("ngd", observation.ledger().ngd);
    h.opt_f64("nrke", observation.ledger().nrke);
    h.bytes("loss_ledger_len", &(loss_ledger.len() as u64).to_be_bytes());
    for line in loss_ledger {
        h.str_field("loss", line);
    }
    h.finish()
}


#[derive(Debug, Clone, Copy, PartialEq, Serialize, Deserialize)]
pub struct PrimeBudget {
    pub budget: f64,
    pub delta_control: f64,
}

impl PrimeBudget {
    pub fn new(budget: f64, delta_control: f64) -> Self {
        Self {
            budget,
            delta_control,
        }
    }

    pub fn has_budget(&self) -> bool {
        if !self.budget.is_finite() || !self.delta_control.is_finite() {
            return false;
        }
        self.budget - self.delta_control >= 0.0
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, PartialOrd, Ord, Serialize, Deserialize)]
pub enum ContinuationBlocker {
    V1SchemaQuarantined,
    ObligationMissing,
    WitnessMissing,
    NextCarrierUndeclared,
    AdapterUnsound,
    DetectorInadequate,
    MinimalLiftMissing,
    SkeletonNotPreserved,
    BudgetExhausted,
    #[serde(rename = "GtlaRefusal")]
    CodaGtlaRefusal,
}

impl ContinuationBlocker {
    pub fn as_str(&self) -> &'static str {
        match self {
            Self::V1SchemaQuarantined => "V1SchemaQuarantined",
            Self::ObligationMissing => "ObligationMissing",
            Self::WitnessMissing => "WitnessMissing",
            Self::NextCarrierUndeclared => "NextCarrierUndeclared",
            Self::AdapterUnsound => "AdapterUnsound",
            Self::DetectorInadequate => "DetectorInadequate",
            Self::MinimalLiftMissing => "MinimalLiftMissing",
            Self::SkeletonNotPreserved => "SkeletonNotPreserved",
            Self::BudgetExhausted => "BudgetExhausted",
            Self::CodaGtlaRefusal => "GtlaRefusal",
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct ContinuationEvidence {
    corpus_digest: String,
    receipt_hash: String,
    detector_adequate: bool,
    adapter_sound: bool,
}

impl ContinuationEvidence {
    pub(crate) fn seal(
        corpus_digest: String,
        receipt_hash: String,
        detector_adequate: bool,
        adapter_sound: bool,
    ) -> Self {
        Self {
            corpus_digest,
            receipt_hash,
            detector_adequate,
            adapter_sound,
        }
    }

    pub fn corpus_digest(&self) -> &str {
        &self.corpus_digest
    }

    pub fn receipt_hash(&self) -> &str {
        &self.receipt_hash
    }

    pub fn detector_adequate(&self) -> bool {
        self.detector_adequate
    }

    pub fn adapter_sound(&self) -> bool {
        self.adapter_sound
    }
}

#[derive(Debug, Clone, PartialEq, Serialize)]
pub struct PrimeContinuationInputs {
    evidence: ContinuationEvidence,
    has_obligation: bool,
    has_witness: bool,
    next_carrier_declared: bool,
    minimal_lift: bool,
    skeleton_preserved: bool,
    #[serde(rename = "gtla_refusal")]
    coda_gtla_refusal: bool,
    budget: PrimeBudget,
}

impl PrimeContinuationInputs {
    #[allow(clippy::too_many_arguments)]
    pub fn from_evidence(
        evidence: ContinuationEvidence,
        budget: PrimeBudget,
        has_obligation: bool,
        has_witness: bool,
        next_carrier_declared: bool,
        minimal_lift: bool,
        skeleton_preserved: bool,
        coda_gtla_refusal: bool,
    ) -> Self {
        Self {
            evidence,
            has_obligation,
            has_witness,
            next_carrier_declared,
            minimal_lift,
            skeleton_preserved,
            coda_gtla_refusal,
            budget,
        }
    }

    pub fn evidence(&self) -> &ContinuationEvidence {
        &self.evidence
    }

    pub fn evaluate(&self) -> PrimeContinuation {
        let mut blockers = Vec::new();
        blockers.push(ContinuationBlocker::V1SchemaQuarantined);
        if !self.has_obligation {
            blockers.push(ContinuationBlocker::ObligationMissing);
        }
        if !self.has_witness {
            blockers.push(ContinuationBlocker::WitnessMissing);
        }
        if !self.next_carrier_declared {
            blockers.push(ContinuationBlocker::NextCarrierUndeclared);
        }
        if !self.evidence.adapter_sound() {
            blockers.push(ContinuationBlocker::AdapterUnsound);
        }
        if !self.evidence.detector_adequate() {
            blockers.push(ContinuationBlocker::DetectorInadequate);
        }
        if !self.minimal_lift {
            blockers.push(ContinuationBlocker::MinimalLiftMissing);
        }
        if !self.skeleton_preserved {
            blockers.push(ContinuationBlocker::SkeletonNotPreserved);
        }
        if !self.budget.has_budget() {
            blockers.push(ContinuationBlocker::BudgetExhausted);
        }
        if self.coda_gtla_refusal {
            blockers.push(ContinuationBlocker::CodaGtlaRefusal);
        }
        blockers.sort_unstable();
        blockers.dedup();
        PrimeContinuation { blockers }
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct PrimeContinuation {
    blockers: Vec<ContinuationBlocker>,
}

impl PrimeContinuation {
    pub fn may_continue(&self) -> bool {
        self.blockers.is_empty()
    }

    pub fn is_quarantined(&self) -> bool {
        self.blockers
            .contains(&ContinuationBlocker::V1SchemaQuarantined)
    }

    pub fn disposition(&self) -> &'static str {
        if self.is_quarantined() {
            "ExternalVerifierRequired"
        } else {
            "Proposed"
        }
    }

    pub fn blockers(&self) -> &[ContinuationBlocker] {
        &self.blockers
    }

    pub fn authority_effect(&self) -> AuthorityEffect {
        AuthorityEffect::None
    }

    pub const TERMINAL_WITH_DEBT: &'static str = "TERMINAL_WITH_DEBT";
    pub const LOCAL_GREEN_FOR_SCOPE: &'static str = "LOCAL_GREEN_FOR_SCOPE";

    pub fn step_terminal(&self) -> &'static str {
        if self.may_continue() {
            Self::LOCAL_GREEN_FOR_SCOPE
        } else {
            Self::TERMINAL_WITH_DEBT
        }
    }

    pub fn to_canonical_result(&self) -> CanContinueResult {
        if self.may_continue() {
            CanContinueResult::permitted(self.step_terminal(), self.disposition())
        } else {
            CanContinueResult::refused(
                self.blockers()
                    .iter()
                    .map(|b| b.as_str().to_string())
                    .collect(),
                self.step_terminal(),
                self.disposition(),
            )
        }
    }
}

pub use engine_types::prime::CanContinueResult;

impl From<&PrimeContinuation> for CanContinueResult {
    fn from(c: &PrimeContinuation) -> Self {
        c.to_canonical_result()
    }
}

impl From<PrimeContinuation> for CanContinueResult {
    fn from(c: PrimeContinuation) -> Self {
        c.to_canonical_result()
    }
}


pub trait PrimeIntakePort {
    fn evaluate_intake(&self, candidate: &CandidateDeclaration) -> PrimeIntakeOutcome;
    fn validate_declaration_order(&self, order: &PrimeDeclarationOrder) -> PrimeDeclarationOutcome;
}

pub trait PrimeDescentPort {
    fn descend(&self, observation: &LggrEpkObservation) -> PrimeDescentReceipt;
}

pub trait PrimeContinuationPort {
    fn can_continue(&self, inputs: &PrimeContinuationInputs) -> CanContinueResult;
}

#[derive(Debug, Clone, Copy, Default)]
pub struct ReferencePrimePorts;

impl PrimeIntakePort for ReferencePrimePorts {
    fn evaluate_intake(&self, candidate: &CandidateDeclaration) -> PrimeIntakeOutcome {
        candidate.evaluate_intake()
    }
    fn validate_declaration_order(&self, order: &PrimeDeclarationOrder) -> PrimeDeclarationOutcome {
        order.validate()
    }
}

impl PrimeContinuationPort for ReferencePrimePorts {
    fn can_continue(&self, inputs: &PrimeContinuationInputs) -> CanContinueResult {
        inputs.evaluate().to_canonical_result()
    }
}
