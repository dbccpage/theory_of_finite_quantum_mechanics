
use crate::ddc::dda_alphabet::{DdaOp, DdaStep, TraceTerminal};
use crate::prime_algos::prime_algorithm_1::LossLedger;
use crate::prime_algos::prime_scope::{
    digest, require_same_scope, short, ScopeBinding, ScopeMismatch,
};
use num_bigint::BigInt;
use num_rational::BigRational;
use num_traits::Zero;
use tfqm_functional::phi1::VerifiedExactPhi1;
use omega_kernel::evidence::Hash256;
use omega_types::authority::AuthorityEffect;
use serde::Serialize;
use std::collections::{BTreeMap, BTreeSet};
use std::fmt;

pub use crate::prime_algos::prime_scope::{BoundCarrierManifest, CallerAttested};


#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Gamma2Zero {
    scope: ScopeBinding,
}

impl Gamma2Zero {
    pub fn verify(gamma2: &BigRational, scope: ScopeBinding) -> Result<Self, TerminalRefusal> {
        if gamma2.is_zero() {
            Ok(Self { scope })
        } else {
            Err(TerminalRefusal::ClosureDefectNonZero {
                gamma2: gamma2.to_string(),
            })
        }
    }
    pub fn scope(&self) -> &ScopeBinding {
        &self.scope
    }
    pub fn commit(&self) -> Hash256 {
        digest("oeprm.gamma2.v1", &[&self.scope.commit().0])
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DetectorDescriptor {
    implementation: String,
    version: String,
    readout: String,
    carrier: Hash256,
    supported_degrees: Vec<usize>,
    config: Hash256,
}

impl DetectorDescriptor {
    pub fn new(
        implementation: impl Into<String>,
        version: impl Into<String>,
        readout: impl Into<String>,
        carrier: Hash256,
        supported_degrees: impl IntoIterator<Item = usize>,
        config: Hash256,
    ) -> Self {
        let mut supported_degrees: Vec<usize> = supported_degrees.into_iter().collect();
        supported_degrees.sort_unstable();
        supported_degrees.dedup();
        Self {
            implementation: implementation.into(),
            version: version.into(),
            readout: readout.into(),
            carrier,
            supported_degrees,
            config,
        }
    }

    pub fn supports(&self, degree: usize) -> bool {
        self.supported_degrees.contains(&degree)
    }

    pub fn supported_degrees(&self) -> &[usize] {
        &self.supported_degrees
    }

    pub fn id(&self) -> Hash256 {
        digest(
            DETECTOR_DOMAIN,
            &[
                self.implementation.as_bytes(),
                self.version.as_bytes(),
                self.readout.as_bytes(),
                &self.carrier.0,
                &self
                    .supported_degrees
                    .iter()
                    .flat_map(|d| (*d as u64).to_le_bytes())
                    .collect::<Vec<u8>>(),
                &self.config.0,
            ],
        )
    }

    pub fn carrier(&self) -> &Hash256 {
        &self.carrier
    }
    pub fn readout(&self) -> &str {
        &self.readout
    }
}

#[derive(Debug, Clone, Copy)]
pub struct RunSubject<'a> {
    pub input: &'a [u8],
    pub degree: usize,
    pub scope: &'a ScopeBinding,
}

pub trait Detector {
    fn descriptor(&self) -> &DetectorDescriptor;

    fn verdict(&self, subject: &RunSubject<'_>) -> Vec<u8>;
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub enum AdequacyRefusal {
    IdenticalInputs,
    RepeatabilityFailure,
    CoincidentVerdicts,
    CarrierMismatch { expected: String, declared: String },
    ClaimIsNotTheScopedResidual { expected: String, claim: String },
    DegreeNotSupported {
        degree: usize,
        supported: Vec<usize>,
    },
}

impl fmt::Display for AdequacyRefusal {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            AdequacyRefusal::IdenticalInputs => write!(f, "claim and counterclaim are identical"),
            AdequacyRefusal::RepeatabilityFailure => {
                write!(f, "detector answered differently on a repeat evaluation")
            }
            AdequacyRefusal::CoincidentVerdicts => {
                write!(f, "detector returned the same verdict for both inputs")
            }
            AdequacyRefusal::CarrierMismatch { expected, declared } => write!(
                f,
                "detector is configured for carrier {declared} but the site is {expected}"
            ),
            AdequacyRefusal::ClaimIsNotTheScopedResidual { expected, claim } => write!(
                f,
                "claim digests to {claim} but the scoped residual is {expected}"
            ),
            AdequacyRefusal::DegreeNotSupported { degree, supported } => write!(
                f,
                "detector declares degrees {supported:?} and was asked at {degree}"
            ),
        }
    }
}

impl std::error::Error for AdequacyRefusal {}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DetectorAdequacy {
    scope: ScopeBinding,
    degree: usize,
    detector: Hash256,
    claim: Hash256,
    counterclaim: Hash256,
}

impl DetectorAdequacy {
    pub fn by_running<D: Detector + ?Sized>(
        detector: &D,
        claim: &[u8],
        counterclaim: &[u8],
        degree: usize,
        scope: ScopeBinding,
    ) -> Result<Self, AdequacyRefusal> {
        if claim == counterclaim {
            return Err(AdequacyRefusal::IdenticalInputs);
        }

        let descriptor = detector.descriptor();
        if !descriptor.supports(degree) {
            return Err(AdequacyRefusal::DegreeNotSupported {
                degree,
                supported: descriptor.supported_degrees().to_vec(),
            });
        }
        if descriptor.carrier() != scope.carrier() {
            return Err(AdequacyRefusal::CarrierMismatch {
                expected: short(scope.carrier()),
                declared: short(descriptor.carrier()),
            });
        }

        let claim_digest = digest(ADEQUACY_DOMAIN, &[claim]);
        if &claim_digest != scope.residual() {
            return Err(AdequacyRefusal::ClaimIsNotTheScopedResidual {
                expected: short(scope.residual()),
                claim: short(&claim_digest),
            });
        }

        let claim_subject = RunSubject {
            input: claim,
            degree,
            scope: &scope,
        };
        let counter_subject = RunSubject {
            input: counterclaim,
            degree,
            scope: &scope,
        };

        let a = detector.verdict(&claim_subject);
        let b = detector.verdict(&counter_subject);
        if a != detector.verdict(&claim_subject) || b != detector.verdict(&counter_subject) {
            return Err(AdequacyRefusal::RepeatabilityFailure);
        }
        if a == b {
            return Err(AdequacyRefusal::CoincidentVerdicts);
        }

        Ok(Self {
            scope,
            degree,
            detector: descriptor.id(),
            claim: claim_digest,
            counterclaim: digest(ADEQUACY_DOMAIN, &[counterclaim]),
        })
    }

    pub fn detector(&self) -> &Hash256 {
        &self.detector
    }
    pub fn claim(&self) -> &Hash256 {
        &self.claim
    }
    pub fn counterclaim(&self) -> &Hash256 {
        &self.counterclaim
    }
    pub fn degree(&self) -> usize {
        self.degree
    }
    pub fn scope(&self) -> &ScopeBinding {
        &self.scope
    }

    pub fn commit(&self) -> Hash256 {
        digest(
            ADEQUACY_DOMAIN,
            &[
                &self.detector.0,
                &self.claim.0,
                &self.counterclaim.0,
                &(self.degree as u64).to_le_bytes(),
                &self.scope.commit().0,
            ],
        )
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ObligationWitness {
    scope: ScopeBinding,
    degree: usize,
    obligation: Hash256,
}

impl ObligationWitness {
    pub fn exhibit(obligation: Hash256, degree: usize, scope: ScopeBinding) -> Self {
        Self {
            scope,
            degree,
            obligation,
        }
    }
    pub fn degree(&self) -> usize {
        self.degree
    }
    pub fn scope(&self) -> &ScopeBinding {
        &self.scope
    }

    pub fn commit(&self) -> Hash256 {
        digest(
            EVIDENCE_DOMAIN,
            &[
                &self.obligation.0,
                &(self.degree as u64).to_le_bytes(),
                &self.scope.commit().0,
            ],
        )
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct SameCarrierExhaustion {
    scope: ScopeBinding,
    candidates_tried: usize,
}

impl SameCarrierExhaustion {
    pub fn by_searching<I, F>(
        candidates: I,
        mut repairs: F,
        scope: ScopeBinding,
    ) -> Result<Self, LiftRefusal>
    where
        I: IntoIterator,
        F: FnMut(&I::Item) -> bool,
    {
        let mut tried = 0usize;
        for candidate in candidates {
            tried += 1;
            if repairs(&candidate) {
                return Err(LiftRefusal::SameCarrierRepairExists {
                    at_candidate: tried,
                });
            }
        }
        if tried == 0 {
            return Err(LiftRefusal::EmptySearchSpace);
        }
        Ok(Self {
            scope,
            candidates_tried: tried,
        })
    }
    pub fn candidates_tried(&self) -> usize {
        self.candidates_tried
    }
    pub fn scope(&self) -> &ScopeBinding {
        &self.scope
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub enum LiftRefusal {
    SameCarrierRepairExists { at_candidate: usize },
    EmptySearchSpace,
}

impl fmt::Display for LiftRefusal {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            LiftRefusal::SameCarrierRepairExists { at_candidate } => write!(
                f,
                "candidate {at_candidate} repairs on the same carrier; no lift is licensed"
            ),
            LiftRefusal::EmptySearchSpace => {
                write!(f, "the same-carrier search space was empty, not exhausted")
            }
        }
    }
}

impl std::error::Error for LiftRefusal {}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct BoundLiftAdmission {
    scope: ScopeBinding,
    generators: usize,
    admission_digest: Hash256,
}

impl BoundLiftAdmission {
    pub fn bind(
        admission: &crate::prime_algos::licensed_lift_gate::LicensedLiftAdmission,
        exhaustion: &SameCarrierExhaustion,
        scope: ScopeBinding,
    ) -> Result<Self, LawRefusal> {
        require_same_scope("same-carrier exhaustion", exhaustion.scope(), &scope)
            .map_err(LawRefusal::Scope)?;
        if !admission.checklist().lift_checklist_complete() {
            return Err(LawRefusal::Violations(vec![Violation {
                law: AntiCheatLaw::NoLiftLaundering,
                detail: "lift admission checklist incomplete".into(),
            }]));
        }
        let admission_digest = digest(
            EVIDENCE_DOMAIN,
            &[serde_json::to_string(admission)
                .unwrap_or_default()
                .as_bytes()],
        );
        Ok(Self {
            scope,
            generators: admission.generators().len(),
            admission_digest,
        })
    }
    pub fn scope(&self) -> &ScopeBinding {
        &self.scope
    }

    pub fn commit(&self) -> Hash256 {
        digest(
            EVIDENCE_DOMAIN,
            &[
                &self.scope.commit().0,
                &(self.generators as u64).to_le_bytes(),
                &self.admission_digest.0,
            ],
        )
    }
}

pub fn d0_commitment(d0: &[Vec<BigRational>]) -> Hash256 {
    d0_digest(d0)
}

fn d0_digest(d0: &[Vec<BigRational>]) -> Hash256 {
    let mut parts: Vec<Vec<u8>> = Vec::new();
    parts.push((d0.len() as u64).to_le_bytes().to_vec());
    for row in d0 {
        parts.push((row.len() as u64).to_le_bytes().to_vec());
        for v in row {
            parts.push(v.to_string().into_bytes());
        }
    }
    let refs: Vec<&[u8]> = parts.iter().map(|p| p.as_slice()).collect();
    digest(RESIDUAL_DOMAIN, &refs)
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct CodaGtlaRefusal {
    reason: String,
    scope: ScopeBinding,
}

impl CodaGtlaRefusal {
    pub fn issued(reason: impl Into<String>, scope: ScopeBinding) -> Self {
        Self {
            reason: reason.into(),
            scope,
        }
    }
    pub fn reason(&self) -> &str {
        &self.reason
    }
    pub fn scope(&self) -> &ScopeBinding {
        &self.scope
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ResidualDelta {
    scope: ScopeBinding,
    before: BigRational,
    after: BigRational,
    measured_on: Hash256,
}

impl ResidualDelta {
    pub fn from_verified(
        before: &VerifiedExactPhi1,
        after: &VerifiedExactPhi1,
        scope: ScopeBinding,
    ) -> Result<Self, LawRefusal> {
        if before.d0() != after.d0() {
            return Err(LawRefusal::Violations(vec![Violation {
                law: AntiCheatLaw::ResidualNonIncrease,
                detail: format!(
                    "Phi_1 endpoints are over different d0 ({} vs {} rows);                      values in different quotients are not comparable",
                    before.d0().len(),
                    after.d0().len()
                ),
            }]));
        }
        Ok(Self {
            measured_on: d0_digest(before.d0()),
            scope,
            before: before.value().clone(),
            after: after.value().clone(),
        })
    }

    pub fn measured_on(&self) -> &Hash256 {
        &self.measured_on
    }

    pub fn commit(&self) -> Hash256 {
        digest(
            RESIDUAL_DOMAIN,
            &[
                &self.scope.commit().0,
                self.before.to_string().as_bytes(),
                self.after.to_string().as_bytes(),
                &self.measured_on.0,
            ],
        )
    }
    pub fn before_string(&self) -> String {
        self.before.to_string()
    }
    pub fn after_string(&self) -> String {
        self.after.to_string()
    }

    pub fn increases(&self) -> bool {
        self.after > self.before
    }
    pub fn delta(&self) -> BigRational {
        &self.after - &self.before
    }
    pub fn scope(&self) -> &ScopeBinding {
        &self.scope
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ObligationClosure {
    scope: ScopeBinding,
    highest_discharged: usize,
}

impl ObligationClosure {
    pub fn discharge(
        open_degrees: &[usize],
        highest_discharged: usize,
        scope: ScopeBinding,
    ) -> Result<Self, TerminalRefusal> {
        if open_degrees.is_empty() {
            Ok(Self {
                scope,
                highest_discharged,
            })
        } else {
            Err(TerminalRefusal::ObligationsOpen {
                degrees: open_degrees.to_vec(),
            })
        }
    }
    pub fn scope(&self) -> &ScopeBinding {
        &self.scope
    }
    pub fn highest_discharged(&self) -> usize {
        self.highest_discharged
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ObligationRegistry {
    scope: ScopeBinding,
    open_obligations: BTreeSet<usize>,
    discharged_obligations: BTreeSet<usize>,
}

impl ObligationRegistry {
    pub fn new(scope: ScopeBinding) -> Self {
        Self {
            scope,
            open_obligations: BTreeSet::new(),
            discharged_obligations: BTreeSet::new(),
        }
    }

    pub fn scope(&self) -> &ScopeBinding {
        &self.scope
    }

    pub fn register(&mut self, degree: usize) {
        self.open_obligations.insert(degree);
    }

    pub fn discharge(&mut self, degree: usize) {
        self.open_obligations.remove(&degree);
        self.discharged_obligations.insert(degree);
    }

    pub fn is_empty(&self) -> bool {
        self.open_obligations.is_empty()
    }

    pub fn open_degrees(&self) -> Vec<usize> {
        self.open_obligations.iter().copied().collect()
    }

    pub fn issue_terminal_permit(
        &self,
        scope: ScopeBinding,
        gamma2_zero: &Gamma2Zero,
    ) -> Result<TerminalPermit, TerminalRefusal> {
        require_same_scope("obligation registry", &self.scope, &scope)
            .map_err(TerminalRefusal::Scope)?;
        require_same_scope("gamma2 receipt", gamma2_zero.scope(), &scope)
            .map_err(TerminalRefusal::Scope)?;
        if !self.open_obligations.is_empty() {
            return Err(TerminalRefusal::ObligationsOpen {
                degrees: self.open_degrees(),
            });
        }
        let highest = self
            .discharged_obligations
            .iter()
            .copied()
            .max()
            .unwrap_or(0);
        let closure = ObligationClosure {
            scope: scope.clone(),
            highest_discharged: highest,
        };
        Ok(TerminalPermit {
            scope,
            closure,
            gamma2_digest: gamma2_zero.commit(),
        })
    }
}

#[derive(Debug, PartialEq, Eq)]
pub struct TerminalPermit {
    scope: ScopeBinding,
    closure: ObligationClosure,
    gamma2_digest: Hash256,
}

impl TerminalPermit {
    pub fn scope(&self) -> &ScopeBinding {
        &self.scope
    }

    pub fn closure(&self) -> &ObligationClosure {
        &self.closure
    }

    pub fn gamma2_digest(&self) -> &Hash256 {
        &self.gamma2_digest
    }
}


#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct Budget {
    total: String,
    floor: String,
    max_ops: usize,
    spent: usize,
}

impl Budget {
    pub fn declare(total: &BigRational, control_floor: &BigRational) -> Result<Self, LawRefusal> {
        if control_floor <= &BigRational::zero() || total < &BigRational::zero() {
            return Err(LawRefusal::Violations(vec![Violation {
                law: AntiCheatLaw::BoundedStopping,
                detail: format!(
                    "budget total {total} / floor {control_floor} does not bound the op count"
                ),
            }]));
        }
        let ops = (total / control_floor).floor();
        let max_ops = ops.to_integer().try_into().unwrap_or(usize::MAX);
        Ok(Self {
            total: total.to_string(),
            floor: control_floor.to_string(),
            max_ops,
            spent: 0,
        })
    }

    pub fn max_ops(&self) -> usize {
        self.max_ops
    }
    pub fn spent(&self) -> usize {
        self.spent
    }
    pub fn remaining(&self) -> usize {
        self.max_ops.saturating_sub(self.spent)
    }

    fn spend(&mut self) -> Result<(), Violation> {
        if self.spent >= self.max_ops {
            return Err(Violation {
                law: AntiCheatLaw::BoundedStopping,
                detail: format!(
                    "operation bound reached: {} of {} ops spent",
                    self.spent, self.max_ops
                ),
            });
        }
        self.spent += 1;
        Ok(())
    }
}


#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, PartialOrd, Ord, Serialize)]
#[serde(rename_all = "snake_case")]
pub enum AntiCheatLaw {
    NoDegreeLaundering,
    NoLiftLaundering,
    NoAnomalonEvasion,
    OldSkeletonPreservation,
    DetectorRevalidation,
    FirstUnresolvedDegreeHonesty,
    BoundedStopping,
    ResidualNonIncrease,
}

impl AntiCheatLaw {
    pub const SIX: [AntiCheatLaw; 6] = [
        AntiCheatLaw::NoDegreeLaundering,
        AntiCheatLaw::NoLiftLaundering,
        AntiCheatLaw::NoAnomalonEvasion,
        AntiCheatLaw::OldSkeletonPreservation,
        AntiCheatLaw::DetectorRevalidation,
        AntiCheatLaw::FirstUnresolvedDegreeHonesty,
    ];

    pub fn as_str(self) -> &'static str {
        match self {
            AntiCheatLaw::NoDegreeLaundering => "no_degree_laundering",
            AntiCheatLaw::NoLiftLaundering => "no_lift_laundering",
            AntiCheatLaw::NoAnomalonEvasion => "no_anomalon_evasion",
            AntiCheatLaw::OldSkeletonPreservation => "old_skeleton_preservation",
            AntiCheatLaw::DetectorRevalidation => "detector_revalidation",
            AntiCheatLaw::FirstUnresolvedDegreeHonesty => "first_unresolved_degree_honesty",
            AntiCheatLaw::BoundedStopping => "bounded_stopping",
            AntiCheatLaw::ResidualNonIncrease => "residual_non_increase",
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct Violation {
    pub law: AntiCheatLaw,
    pub detail: String,
}

impl fmt::Display for Violation {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}: {}", self.law.as_str(), self.detail)
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub enum LawRefusal {
    Violations(Vec<Violation>),
    Scope(ScopeMismatch),
    PermitMismatch {
        licensed_claim: String,
        presented_claim: String,
        licensed_evidence: String,
        presented_evidence: String,
    },
}

impl fmt::Display for LawRefusal {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            LawRefusal::Violations(v) => write!(
                f,
                "refused: {} law(s) violated [{}]",
                v.len(),
                v.iter()
                    .map(|x| x.law.as_str())
                    .collect::<Vec<_>>()
                    .join(", ")
            ),
            LawRefusal::Scope(m) => write!(f, "refused: {m}"),
            LawRefusal::PermitMismatch {
                licensed_claim,
                presented_claim,
                licensed_evidence,
                presented_evidence,
            } => write!(
                f,
                "refused: permit licenses claim {licensed_claim} under evidence \
                 {licensed_evidence}, but was presented with claim {presented_claim} \
                 under evidence {presented_evidence}"
            ),
        }
    }
}

impl std::error::Error for LawRefusal {}

impl LawRefusal {
    pub fn violations(&self) -> &[Violation] {
        match self {
            LawRefusal::Violations(v) => v,
            LawRefusal::Scope(_) | LawRefusal::PermitMismatch { .. } => &[],
        }
    }
}


#[derive(Debug, Clone, PartialEq, Eq)]
#[allow(clippy::large_enum_variant)]
pub enum StepOp {
    ExactRepair,
    ResidualProjection,
    ContextExposure,
    Integration,
    Lift(BoundLiftAdmission),
    Descent,
    Refusal,
}

impl StepOp {
    pub fn letter(&self) -> DdaOp {
        match self {
            StepOp::ExactRepair => DdaOp::ExactRepair,
            StepOp::ResidualProjection => DdaOp::ResidualProjection,
            StepOp::ContextExposure => DdaOp::ContextExposure,
            StepOp::Integration => DdaOp::Integration,
            StepOp::Lift(_) => DdaOp::Lift,
            StepOp::Descent => DdaOp::Descent,
            StepOp::Refusal => DdaOp::Refusal,
        }
    }
}

#[derive(Debug, PartialEq, Eq)]
pub struct StepPermit {
    scope: ScopeBinding,
    evidence: Hash256,
    licensed_claim: Hash256,
}

impl StepPermit {
    pub(crate) fn issue(scope: ScopeBinding, evidence: Hash256, claim: &StepClaim) -> Self {
        Self {
            scope,
            evidence,
            licensed_claim: claim.commit(),
        }
    }

    pub fn licensed_claim(&self) -> &Hash256 {
        &self.licensed_claim
    }

    pub fn binding(&self, claim: &StepClaim) -> Hash256 {
        digest(
            PERMIT_DOMAIN,
            &[&self.scope.commit().0, &self.evidence.0, &claim.commit().0],
        )
    }
    pub fn scope(&self) -> &ScopeBinding {
        &self.scope
    }
    pub fn evidence(&self) -> &Hash256 {
        &self.evidence
    }
}

#[derive(Debug, Clone)]
pub struct StepClaim {
    pub op: StepOp,
    pub residual_content: Hash256,
    pub residual_label: Hash256,
    pub degree: usize,
    pub skeleton: Hash256,
    pub loss_ledger: Option<LossLedger>,
    pub repacketized: bool,
    pub claims_above_n0_are_conditional: bool,
}

impl StepClaim {
    pub fn commit(&self) -> Hash256 {
        digest(
            CLAIM_DOMAIN,
            &[
                &[self.op.letter() as u8],
                &match &self.op {
                    StepOp::Lift(a) => a.commit(),
                    _ => Hash256([0; 32]),
                }
                .0,
                &self.residual_content.0,
                &self.residual_label.0,
                &(self.degree as u64).to_le_bytes(),
                &self.skeleton.0,
                &self
                    .loss_ledger
                    .as_ref()
                    .map_or(Hash256([0; 32]), |l| l.commit())
                    .0,
                &[
                    u8::from(self.repacketized),
                    u8::from(self.claims_above_n0_are_conditional),
                ],
            ],
        )
    }
}


#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct RefusalReceipt {
    pub step_index: usize,
    pub laws: Vec<AntiCheatLaw>,
    pub detail: String,
}

pub type ControlState = OpenControlState;

#[derive(Debug, PartialEq, Eq)]
pub struct OpenControlState {
    run: Hash256,
    manifest: BoundCarrierManifest,
    seen_residuals: BTreeMap<Vec<u8>, Hash256>,
    degree_window: usize,
    skeleton: Hash256,
    first_unresolved_degree: usize,
    steps_written: usize,
    tape_head: Option<Hash256>,
    budget: Budget,
    refusals: Vec<RefusalReceipt>,
}

impl OpenControlState {
    pub fn open(
        run: Hash256,
        carrier: Hash256,
        d0: Hash256,
        skeleton: Hash256,
        budget: Budget,
    ) -> Self {
        Self::open_manifest(
            run,
            BoundCarrierManifest::new(carrier, d0),
            skeleton,
            budget,
        )
    }

    pub fn open_manifest(
        run: Hash256,
        manifest: BoundCarrierManifest,
        skeleton: Hash256,
        budget: Budget,
    ) -> Self {
        Self {
            run,
            manifest,
            seen_residuals: BTreeMap::new(),
            degree_window: 1,
            skeleton,
            first_unresolved_degree: 1,
            steps_written: 0,
            tape_head: None,
            budget,
            refusals: Vec::new(),
        }
    }

    pub fn open_with_carrier_and_d0(
        run: Hash256,
        carrier: Hash256,
        d0: Hash256,
        skeleton: Hash256,
        budget: Budget,
    ) -> Self {
        Self::open(run, carrier, d0, skeleton, budget)
    }

    pub fn tape_head(&self) -> Option<&Hash256> {
        self.tape_head.as_ref()
    }
    pub fn steps_written(&self) -> usize {
        self.steps_written
    }
    pub fn degree_window(&self) -> usize {
        self.degree_window
    }
    pub fn first_unresolved_degree(&self) -> usize {
        self.first_unresolved_degree
    }
    pub fn budget(&self) -> &Budget {
        &self.budget
    }
    pub fn refusals(&self) -> &[RefusalReceipt] {
        &self.refusals
    }
    pub fn skeleton(&self) -> &Hash256 {
        &self.skeleton
    }
    pub fn carrier_manifest(&self) -> &BoundCarrierManifest {
        &self.manifest
    }
    pub fn carrier(&self) -> &Hash256 {
        self.manifest.carrier()
    }
    pub fn d0(&self) -> &Hash256 {
        self.manifest.d0()
    }

    pub fn scope_for(&self, residual: Hash256) -> ScopeBinding {
        ScopeBinding::new(
            self.run.clone(),
            self.manifest.clone(),
            residual,
            self.tape_head.clone(),
            self.steps_written,
        )
    }
}

pub type TerminalState = TerminalControlState;

#[derive(Debug, PartialEq, Eq)]
pub struct TerminalControlState {
    run: Hash256,
    manifest: BoundCarrierManifest,
    steps_written: usize,
    terminal_head: Hash256,
    budget: Budget,
}

impl TerminalControlState {
    pub fn run(&self) -> &Hash256 {
        &self.run
    }
    pub fn carrier_manifest(&self) -> &BoundCarrierManifest {
        &self.manifest
    }
    pub fn carrier(&self) -> &Hash256 {
        self.manifest.carrier()
    }
    pub fn d0(&self) -> &Hash256 {
        self.manifest.d0()
    }
    pub fn steps_written(&self) -> usize {
        self.steps_written
    }
    pub fn terminal_head(&self) -> &Hash256 {
        &self.terminal_head
    }
    pub fn terminal(&self) -> TraceTerminal {
        TraceTerminal::Terminalized
    }
    pub fn budget(&self) -> &Budget {
        &self.budget
    }
}


#[derive(Debug)]
pub struct ContinuationEvidence {
    pub outstanding_obligation: ObligationWitness,
    pub higher_obligation_witness: ObligationWitness,
    pub next_carrier_manifest: BoundCarrierManifest,
    pub adapter_ledger: LossLedger,
    pub detector: DetectorAdequacy,
    pub lift: Option<BoundLiftAdmission>,
    pub skeleton_preserved: bool,
    pub coda_gtla_refusal: Option<CodaGtlaRefusal>,
    pub residual: ResidualDelta,
}

impl ContinuationEvidence {
    pub fn next_carrier(&self) -> &Hash256 {
        self.next_carrier_manifest.carrier()
    }

    pub fn commit(&self) -> Hash256 {
        digest(
            EVIDENCE_DOMAIN,
            &[
                &self.outstanding_obligation.commit().0,
                &self.higher_obligation_witness.commit().0,
                &self.next_carrier_manifest.commit().0,
                &self.adapter_ledger.commit().0,
                &self.detector.commit().0,
                &self
                    .lift
                    .as_ref()
                    .map_or(Hash256([0; 32]), |l| l.commit())
                    .0,
                &[
                    u8::from(self.skeleton_preserved),
                    u8::from(self.coda_gtla_refusal.is_some()),
                    u8::from(self.lift.is_some()),
                ],
                &self.residual.commit().0,
            ],
        )
    }
}

pub const CONTINUATION_CONJUNCTS: [&str; 9] = [
    "outstanding_obligation",
    "higher_obligation_witness",
    "next_carrier_declared",
    "adapter_sound",
    "detector_adequate",
    "minimal_licensed_lift",
    "skeleton_preserved",
    "budget_available",
    "gtla_continuation_refusal",
];

pub fn can_continue_n(
    state: &mut ControlState,
    site: &ScopeBinding,
    claim: &StepClaim,
    ev: &ContinuationEvidence,
) -> Result<StepPermit, LawRefusal> {
    let mut v = check_laws(state, claim, ev);

    require_same_scope(
        "outstanding obligation",
        ev.outstanding_obligation.scope(),
        site,
    )
    .map_err(LawRefusal::Scope)?;
    require_same_scope(
        "higher obligation witness",
        ev.higher_obligation_witness.scope(),
        site,
    )
    .map_err(LawRefusal::Scope)?;
    require_same_scope("detector adequacy", ev.detector.scope(), site)
        .map_err(LawRefusal::Scope)?;
    if let Some(l) = &ev.lift {
        require_same_scope("lift admission", l.scope(), site).map_err(LawRefusal::Scope)?;
    }
    require_same_scope("adapter loss ledger", ev.adapter_ledger.scope(), site)
        .map_err(LawRefusal::Scope)?;

    if ev.higher_obligation_witness.degree() <= ev.outstanding_obligation.degree() {
        v.push(Violation {
            law: AntiCheatLaw::NoDegreeLaundering,
            detail: format!(
                "higher obligation at degree {} does not exceed current {}",
                ev.higher_obligation_witness.degree(),
                ev.outstanding_obligation.degree()
            ),
        });
    }
    if !ev.adapter_ledger.is_sound() {
        v.push(Violation {
            law: AntiCheatLaw::OldSkeletonPreservation,
            detail: "adapter loss ledger is not sound".into(),
        });
    }
    if !ev.skeleton_preserved && ev.adapter_ledger.is_empty() {
        v.push(Violation {
            law: AntiCheatLaw::OldSkeletonPreservation,
            detail: "skeleton not preserved and no loss booked".into(),
        });
    }
    require_same_scope("residual delta", ev.residual.scope(), site).map_err(LawRefusal::Scope)?;
    if ev.residual.measured_on() != state.d0() {
        return Err(LawRefusal::Violations(vec![Violation {
            law: AntiCheatLaw::ResidualNonIncrease,
            detail: format!(
                "residual measured on d0 {} but this run declares {}",
                short(ev.residual.measured_on()),
                short(state.d0())
            ),
        }]));
    }
    if ev.residual.increases() && ev.adapter_ledger.is_empty() {
        v.push(Violation {
            law: AntiCheatLaw::ResidualNonIncrease,
            detail: format!(
                "step raises Phi by {} with no audited loss ledger",
                ev.residual.delta()
            ),
        });
    }
    if let Some(r) = &ev.coda_gtla_refusal {
        v.push(Violation {
            law: AntiCheatLaw::BoundedStopping,
            detail: format!("GTLA continuation refusal is present: {}", r.reason()),
        });
    }
    if !v.is_empty() {
        return Err(LawRefusal::Violations(v));
    }
    if state.budget().remaining() == 0 {
        return Err(LawRefusal::Violations(vec![Violation {
            law: AntiCheatLaw::BoundedStopping,
            detail: format!(
                "operation bound reached: {} of {} ops spent",
                state.budget().spent(),
                state.budget().max_ops()
            ),
        }]));
    }
    Ok(StepPermit::issue(site.clone(), ev.commit(), claim))
}


pub fn check_laws(
    state: &ControlState,
    claim: &StepClaim,
    ev: &ContinuationEvidence,
) -> Vec<Violation> {
    let mut v = Vec::new();

    if claim.degree > state.degree_window {
        let w = &ev.higher_obligation_witness;
        if w.degree() < claim.degree {
            v.push(Violation {
                law: AntiCheatLaw::NoDegreeLaundering,
                detail: format!(
                    "degree rises to {} but the exhibited obligation is at {}",
                    claim.degree,
                    w.degree()
                ),
            });
        }
    }


    if let Some(first_label) = state
        .seen_residuals
        .get(claim.residual_content.0.as_slice())
    {
        if *first_label != claim.residual_label {
            v.push(Violation {
                law: AntiCheatLaw::NoAnomalonEvasion,
                detail: format!(
                    "residual {} first written as {}, now presented as {}",
                    short(&claim.residual_content),
                    short(first_label),
                    short(&claim.residual_label)
                ),
            });
        }
    }

    if claim.skeleton != state.skeleton {
        match &claim.loss_ledger {
            Some(l) if l.is_sound() => {
                let site = state.scope_for(claim.residual_content.clone());
                if !l.scope().same_subject(&site) {
                    v.push(Violation {
                        law: AntiCheatLaw::OldSkeletonPreservation,
                        detail: format!(
                            "loss ledger bound to [{}] but claim presented at [{}]",
                            l.scope(),
                            site
                        ),
                    });
                }
            }
            Some(_) => v.push(Violation {
                law: AntiCheatLaw::OldSkeletonPreservation,
                detail: "skeleton changed and the loss ledger is unsound".into(),
            }),
            None => v.push(Violation {
                law: AntiCheatLaw::OldSkeletonPreservation,
                detail: format!(
                    "skeleton changed {} -> {} with no loss ledger",
                    short(&state.skeleton),
                    short(&claim.skeleton)
                ),
            }),
        }
    }

    let needs_revalidation = claim.repacketized || claim.degree > state.degree_window;
    if needs_revalidation && ev.detector.degree() != claim.degree {
        v.push(Violation {
            law: AntiCheatLaw::DetectorRevalidation,
            detail: format!(
                "detector adequacy established at degree {} but the step is at {}; \
                 adequacy is degree-relative and does not transfer either way",
                ev.detector.degree(),
                claim.degree
            ),
        });
    }

    if claim.degree > state.first_unresolved_degree && !claim.claims_above_n0_are_conditional {
        v.push(Violation {
            law: AntiCheatLaw::FirstUnresolvedDegreeHonesty,
            detail: format!(
                "unconditional claim at degree {} while n0 = {} is unresolved",
                claim.degree, state.first_unresolved_degree
            ),
        });
    }

    v
}


const EVENT_DOMAIN: &str = "oeprm.event.v1";
const ADEQUACY_DOMAIN: &str = "oeprm.adequacy.v1";
const DETECTOR_DOMAIN: &str = "oeprm.detector.v1";
const EVIDENCE_DOMAIN: &str = "oeprm.evidence.v1";
const CLAIM_DOMAIN: &str = "oeprm.claim.v1";
const RESIDUAL_DOMAIN: &str = "oeprm.residual.v1";
const PERMIT_DOMAIN: &str = "oeprm.permit.v1";

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum EventKind {
    Step,
    Terminal(Hash256),
}

fn event_commit(
    prev: Option<&Hash256>,
    claim: Option<&StepClaim>,
    scope: &ScopeBinding,
    evidence: &Hash256,
    kind: EventKind,
) -> Hash256 {
    let empty: [u8; 0] = [];
    digest(
        EVENT_DOMAIN,
        &[
            prev.map_or(&empty[..], |h| &h.0[..]),
            &scope.commit().0,
            &evidence.0,
            &claim.map_or(Hash256([0; 32]), |c| c.commit()).0,
            &match &kind {
                EventKind::Step => [0u8; 32],
                EventKind::Terminal(h) => h.0,
            },
            &[match &kind {
                EventKind::Step => 0u8,
                EventKind::Terminal(_) => 1u8,
            }],
        ],
    )
}

fn admit_write(
    state: &ControlState,
    permit: &StepPermit,
    claim: &StepClaim,
    ev: &ContinuationEvidence,
) -> Result<ScopeBinding, LawRefusal> {
    let site = state.scope_for(claim.residual_content.clone());
    require_same_scope("step permit", permit.scope(), &site).map_err(LawRefusal::Scope)?;

    if permit.licensed_claim() != &claim.commit() || permit.evidence() != &ev.commit() {
        return Err(LawRefusal::PermitMismatch {
            licensed_claim: short(permit.licensed_claim()),
            presented_claim: short(&claim.commit()),
            licensed_evidence: short(permit.evidence()),
            presented_evidence: short(&ev.commit()),
        });
    }

    require_same_scope(
        "outstanding obligation",
        ev.outstanding_obligation.scope(),
        &site,
    )
    .map_err(LawRefusal::Scope)?;
    require_same_scope(
        "higher obligation witness",
        ev.higher_obligation_witness.scope(),
        &site,
    )
    .map_err(LawRefusal::Scope)?;
    require_same_scope("detector adequacy", ev.detector.scope(), &site)
        .map_err(LawRefusal::Scope)?;
    require_same_scope("adapter loss ledger", ev.adapter_ledger.scope(), &site)
        .map_err(LawRefusal::Scope)?;
    require_same_scope("residual delta", ev.residual.scope(), &site).map_err(LawRefusal::Scope)?;
    if let Some(l) = &ev.lift {
        require_same_scope("lift admission", l.scope(), &site).map_err(LawRefusal::Scope)?;
    }

    if ev.residual.measured_on() != state.d0() {
        return Err(LawRefusal::Violations(vec![Violation {
            law: AntiCheatLaw::ResidualNonIncrease,
            detail: format!(
                "residual measured on d0 {} but this run declares {}",
                short(ev.residual.measured_on()),
                short(state.d0())
            ),
        }]));
    }

    if let StepOp::Lift(bound) = &claim.op {
        require_same_scope("bound lift admission", bound.scope(), &site)
            .map_err(LawRefusal::Scope)?;
        match &ev.lift {
            Some(l) if l.commit() == bound.commit() => {}
            _ => {
                return Err(LawRefusal::Violations(vec![Violation {
                    law: AntiCheatLaw::NoLiftLaundering,
                    detail: "a Lift step must present the same admission in its evidence".into(),
                }]))
            }
        }
    }

    Ok(site)
}

pub fn write_step(
    state: &mut ControlState,
    permit: StepPermit,
    claim: &StepClaim,
    ev: &ContinuationEvidence,
) -> Result<DdaStep, LawRefusal> {
    let site = admit_write(state, &permit, claim, ev)?;

    let violations = check_laws(state, claim, ev);
    if !violations.is_empty() {
        state.refusals.push(RefusalReceipt {
            step_index: state.steps_written,
            laws: violations.iter().map(|x| x.law).collect(),
            detail: violations
                .iter()
                .map(|x| x.to_string())
                .collect::<Vec<_>>()
                .join("; "),
        });
        return Err(LawRefusal::Violations(violations));
    }

    if let Err(v) = state.budget.spend() {
        return Err(LawRefusal::Violations(vec![v]));
    }
    let head = event_commit(
        state.tape_head.as_ref(),
        Some(claim),
        &site,
        permit.evidence(),
        EventKind::Step,
    );
    state
        .seen_residuals
        .entry(claim.residual_content.0.to_vec())
        .or_insert_with(|| claim.residual_label.clone());
    state.degree_window = state.degree_window.max(claim.degree);
    state.skeleton = claim.skeleton.clone();
    if claim.repacketized {
        state.manifest = ev.next_carrier_manifest.clone();
    }
    state.steps_written += 1;
    state.tape_head = Some(head.clone());

    Ok(DdaStep::executed(
        claim.op.letter(),
        format!(
            "PRIME-ALGORITHM-002 step {} chain {}",
            state.steps_written,
            short(&head)
        ),
    ))
}


#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub enum TerminalRefusal {
    LawsViolated(Vec<Violation>),
    ClosureDefectNonZero {
        gamma2: String,
    },
    ObligationsOpen {
        degrees: Vec<usize>,
    },
    Scope(ScopeMismatch),
    Admission(LawRefusal),
}

impl fmt::Display for TerminalRefusal {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            TerminalRefusal::LawsViolated(v) => {
                write!(f, "terminal refused: {} law(s) violated", v.len())
            }
            TerminalRefusal::ClosureDefectNonZero { gamma2 } => {
                write!(
                    f,
                    "terminal refused: Gamma_2 = {gamma2} is not exactly zero"
                )
            }
            TerminalRefusal::ObligationsOpen { degrees } => {
                write!(f, "terminal refused: obligations open at {degrees:?}")
            }
            TerminalRefusal::Scope(m) => write!(f, "terminal refused: {m}"),
            TerminalRefusal::Admission(r) => write!(f, "terminal refused: {r}"),
        }
    }
}

impl std::error::Error for TerminalRefusal {}

fn terminal_commit(g2: &Gamma2Zero, closure: &ObligationClosure) -> Hash256 {
    digest(
        EVENT_DOMAIN,
        &[
            b"terminal",
            &g2.scope().commit().0,
            &closure.scope().commit().0,
            &(closure.highest_discharged() as u64).to_le_bytes(),
        ],
    )
}

pub fn terminalize(
    mut state: OpenControlState,
    permit: TerminalPermit,
    gamma2_zero: Gamma2Zero,
) -> Result<TerminalControlState, TerminalRefusal> {
    let site = state.scope_for(permit.scope().residual().clone());
    require_same_scope("terminal permit", permit.scope(), &site).map_err(TerminalRefusal::Scope)?;
    require_same_scope("gamma2 receipt", gamma2_zero.scope(), &site)
        .map_err(TerminalRefusal::Scope)?;

    if permit.gamma2_digest() != &gamma2_zero.commit() {
        return Err(TerminalRefusal::ClosureDefectNonZero {
            gamma2: format!(
                "permit gamma2 digest {} does not match receipt digest {}",
                short(permit.gamma2_digest()),
                short(&gamma2_zero.commit())
            ),
        });
    }

    if let Err(v) = state.budget.spend() {
        return Err(TerminalRefusal::LawsViolated(vec![v]));
    }
    let terminal_digest = terminal_commit(&gamma2_zero, permit.closure());
    let head = event_commit(
        state.tape_head.as_ref(),
        None,
        &site,
        permit.gamma2_digest(),
        EventKind::Terminal(terminal_digest),
    );
    let steps_written = state.steps_written + 1;
    Ok(TerminalControlState {
        run: state.run,
        manifest: state.manifest,
        steps_written,
        terminal_head: head,
        budget: state.budget,
    })
}

pub const AUTHORITY_EFFECT: AuthorityEffect = AuthorityEffect::None;

pub fn rational(n: i64) -> BigRational {
    BigRational::from_integer(BigInt::from(n))
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::prime_algos::prime_algorithm_1::LossLedger;

    fn h(n: u8) -> Hash256 {
        Hash256([n; 32])
    }

    struct ParityDetector(DetectorDescriptor);

    impl ParityDetector {
        fn on(carrier: Hash256) -> Self {
            Self(DetectorDescriptor::new(
                "test.parity",
                "v1",
                "parity_bit",
                carrier,
                [1usize, 2, 3],
                Hash256([0; 32]),
            ))
        }
    }

    impl Detector for ParityDetector {
        fn descriptor(&self) -> &DetectorDescriptor {
            &self.0
        }
        fn verdict(&self, subject: &RunSubject<'_>) -> Vec<u8> {
            vec![subject.input.iter().fold(0u8, |a, b| a ^ b) & 1]
        }
    }

    const ODD: &[u8] = &[1];
    const EVEN: &[u8] = &[0];

    fn desc(carrier: Hash256) -> DetectorDescriptor {
        DetectorDescriptor::new(
            "test.fixture",
            "v1",
            "fixture",
            carrier,
            [1usize, 2, 3],
            Hash256([0; 32]),
        )
    }

    fn odd_residual() -> Hash256 {
        digest(ADEQUACY_DOMAIN, &[ODD])
    }

    fn scope_for_claim(s: &ControlState, claim: &[u8]) -> ScopeBinding {
        s.scope_for(digest(ADEQUACY_DOMAIN, &[claim]))
    }

    fn std_ev(s: &ControlState, degree: usize) -> ContinuationEvidence {
        let site = scope_for_claim(s, ODD);
        ContinuationEvidence {
            outstanding_obligation: ObligationWitness::exhibit(h(5), 1, site.clone()),
            higher_obligation_witness: ObligationWitness::exhibit(
                h(6),
                degree.max(2),
                site.clone(),
            ),
            next_carrier_manifest: BoundCarrierManifest::new(h(2), fixture_d0()),
            adapter_ledger: LossLedger::empty(site.clone()),
            detector: adequacy(s, degree.min(3)),
            lift: None,
            skeleton_preserved: true,
            coda_gtla_refusal: None,
            residual: delta(5, 3, site),
        }
    }

    fn ev_with(
        s: &ControlState,
        obligation_degree: usize,
        detector_degree: usize,
    ) -> ContinuationEvidence {
        let site = scope_for_claim(s, ODD);
        ContinuationEvidence {
            outstanding_obligation: ObligationWitness::exhibit(h(5), 1, site.clone()),
            higher_obligation_witness: ObligationWitness::exhibit(
                h(6),
                obligation_degree,
                site.clone(),
            ),
            next_carrier_manifest: BoundCarrierManifest::new(h(2), fixture_d0()),
            adapter_ledger: LossLedger::empty(site.clone()),
            detector: adequacy(s, detector_degree),
            lift: None,
            skeleton_preserved: true,
            coda_gtla_refusal: None,
            residual: delta(5, 3, site),
        }
    }

    fn adequacy(s: &ControlState, degree: usize) -> DetectorAdequacy {
        DetectorAdequacy::by_running(
            &ParityDetector::on(h(2)),
            ODD,
            EVEN,
            degree,
            scope_for_claim(s, ODD),
        )
        .expect("parity separates odd from even on carrier h(2)")
    }

    fn fixture_d0() -> Hash256 {
        d0_digest(&[vec![rational(0)]])
    }

    fn budget() -> Budget {
        Budget::declare(&rational(100), &rational(1)).unwrap()
    }

    fn state() -> ControlState {
        ControlState::open(h(1), h(2), fixture_d0(), h(10), budget())
    }

    fn clean_claim(s: &ControlState) -> StepClaim {
        StepClaim {
            op: StepOp::ResidualProjection,
            residual_content: digest(ADEQUACY_DOMAIN, &[ODD]),
            residual_label: h(4),
            degree: 1,
            skeleton: s.skeleton().clone(),
            loss_ledger: None,
            repacketized: false,
            claims_above_n0_are_conditional: false,
        }
    }

    fn permit_for_claim(s: &ControlState, claim: &StepClaim) -> StepPermit {
        StepPermit::issue(
            s.scope_for(claim.residual_content.clone()),
            std_ev(s, claim.degree).commit(),
            claim,
        )
    }

    fn permit_for(s: &ControlState, residual: Hash256) -> StepPermit {
        let mut c = clean_claim(s);
        c.residual_content = residual.clone();
        StepPermit::issue(s.scope_for(residual), std_ev(s, c.degree).commit(), &c)
    }

    fn verified_phi1(v: i64) -> VerifiedExactPhi1 {
        use tfqm_functional::phi1::{ExactPhi1Certificate, Phi1Functional};
        Phi1Functional::verify_exact_certificate(ExactPhi1Certificate {
            omega: vec![rational(v)],
            d0: vec![vec![rational(0)]],
            weights: vec![rational(1)],
            alpha: vec![rational(0)],
            primal_residual: vec![rational(v)],
            dual_witness: vec![rational(1)],
            reported_value: rational(v),
        })
        .expect("fixture certificate must verify")
    }

    fn delta(before: i64, after: i64, scope: ScopeBinding) -> ResidualDelta {
        ResidualDelta::from_verified(&verified_phi1(before), &verified_phi1(after), scope)
            .expect("same d0, so the endpoints are comparable")
    }

    fn admitted_lift() -> crate::prime_algos::licensed_lift_gate::LicensedLiftAdmission {
        crate::prime_algos::licensed_lift_gate::step9_licensed_lift_gate(
            vec!["resolve_delta_0".into()],
            crate::prime_algos::licensed_lift_gate::NineUpLiftBits::all_true(),
            crate::prime_algos::licensed_lift_gate::PaperEr003LiftCertificate::demo(),
        )
        .expect("the demo certificate admits")
    }


    #[test]
    fn write_step_cannot_express_a_terminal() {
        let s = state();
        let ops = [
            StepOp::ExactRepair,
            StepOp::ResidualProjection,
            StepOp::ContextExposure,
            StepOp::Integration,
            StepOp::Descent,
            StepOp::Refusal,
        ];
        for op in ops {
            assert_ne!(
                op.letter(),
                DdaOp::Terminalize,
                "no StepOp may map to the terminalize letter"
            );
        }
        let _ = s;
    }

    #[test]
    fn gamma2_receipt_cannot_exist_for_a_live_obstruction() {
        let s = state();
        let scope = s.scope_for(h(3));
        Gamma2Zero::verify(&rational(1), scope.clone())
            .expect_err("Gamma_2 = 1 must not yield a receipt");
        let tiny = BigRational::new(BigInt::from(1), BigInt::from(1_000_000_000_i64));
        Gamma2Zero::verify(&tiny, scope.clone())
            .expect_err("no epsilon may round a nonzero defect into a receipt");
        Gamma2Zero::verify(&rational(0), scope).expect("exact zero must yield a receipt");
    }


    #[test]
    fn an_open_run_with_unresolved_obligations_cannot_terminalize() {
        let s = state();
        let scope = s.scope_for(h(3));
        let g2 = Gamma2Zero::verify(&rational(0), scope.clone()).unwrap();
        let mut reg = ObligationRegistry::new(scope.clone());
        reg.register(1);
        let err = reg
            .issue_terminal_permit(scope, &g2)
            .expect_err("an unresolved degree must block terminal permit");
        assert!(matches!(err, TerminalRefusal::ObligationsOpen { .. }));
    }

    #[test]
    fn terminalizes_only_with_closure_and_zero_defect() {
        let s = state();
        let scope = scope_for_claim(&s, ODD);
        let g2 = Gamma2Zero::verify(&rational(0), scope.clone()).unwrap();
        let reg = ObligationRegistry::new(scope.clone());
        let permit = reg
            .issue_terminal_permit(scope, &g2)
            .expect("permit issued");
        let t = terminalize(s, permit, g2).expect("clean terminal");
        assert_eq!(t.terminal(), TraceTerminal::Terminalized);
        assert_eq!(t.steps_written(), 1);
    }


    #[test]
    fn a_permit_for_another_residual_is_refused() {
        let mut s = state();
        let wrong = permit_for(&s, h(99));
        let claim = clean_claim(&s);
        let err = write_step(&mut s, wrong, &claim, &std_ev(&state(), claim.degree))
            .expect_err("permit bound elsewhere");
        assert!(matches!(err, LawRefusal::Scope(_)));
    }

    #[test]
    fn a_permit_cannot_be_replayed_against_a_moved_tape_head() {
        let mut s = state();
        let stale = permit_for(&s, odd_residual());
        let mut c = clean_claim(&s);
        let p = permit_for(&s, odd_residual());
        write_step(&mut s, p, &c, &std_ev(&state(), c.degree)).expect("first write");
        c.residual_content = h(3);
        let err = write_step(&mut s, stale, &c, &std_ev(&state(), c.degree))
            .expect_err("a permit from before the head moved must not be reusable");
        assert!(matches!(err, LawRefusal::Scope(_)));
    }


    #[test]
    fn a_lift_admission_cannot_authorize_another_residual() {
        let s = state();
        let scope_a = s.scope_for(h(3));
        let scope_b = s.scope_for(h(77));
        let exhaustion =
            SameCarrierExhaustion::by_searching(0..12, |_| false, scope_a.clone()).unwrap();
        let err = BoundLiftAdmission::bind(&admitted_lift(), &exhaustion, scope_b)
            .expect_err("a lift licensed for residual A must not bind at residual B");
        assert!(matches!(err, LawRefusal::Scope(_)));
    }

    #[test]
    fn a_lift_without_exhaustion_cannot_be_proved() {
        let s = state();
        assert!(
            SameCarrierExhaustion::by_searching(0..5, |c| *c == 2, s.scope_for(h(3))).is_err(),
            "a same-carrier repair exists, so no lift is licensed"
        );
        assert!(
            SameCarrierExhaustion::by_searching(0..0, |_: &i32| false, s.scope_for(h(3))).is_err(),
            "an empty space is not an exhausted one"
        );
        assert!(SameCarrierExhaustion::by_searching(0..5, |_| false, s.scope_for(h(3))).is_ok());
    }


    #[test]
    fn the_clean_claim_violates_no_law() {
        let s = state();
        assert_eq!(check_laws(&s, &clean_claim(&s), &std_ev(&s, 1)), Vec::new());
    }

    #[test]
    fn skeleton_change_without_a_loss_ledger_refuses() {
        let s = state();
        let mut c = clean_claim(&s);
        c.skeleton = h(200);
        let v = check_laws(&s, &c, &std_ev(&s, c.degree));
        assert!(v
            .iter()
            .any(|x| x.law == AntiCheatLaw::OldSkeletonPreservation));
    }

    #[test]
    fn skeleton_change_with_a_sound_loss_ledger_is_lawful() {
        let s = state();
        let mut c = clean_claim(&s);
        let site = s.scope_for(c.residual_content.clone());
        c.loss_ledger = Some(LossLedger::booked(vec![("dropped_2cells".into(), 3)], site));
        assert_eq!(check_laws(&s, &c, &std_ev(&s, c.degree)), Vec::new());
    }

    #[test]
    fn degree_rise_without_detector_revalidation_refuses() {
        let s = state();
        let mut c = clean_claim(&s);
        c.degree = 2;
        c.repacketized = false;
        c.claims_above_n0_are_conditional = true;
        let v = check_laws(&s, &c, &ev_with(&s, 2, 1));
        assert!(
            v.iter()
                .any(|x| x.law == AntiCheatLaw::DetectorRevalidation),
            "a degree rise must revalidate the detector even without repacketization"
        );
    }

    #[test]
    fn degree_rise_without_an_obligation_at_the_new_degree_refuses() {
        let s = state();
        let mut c = clean_claim(&s);
        c.degree = 2;
        c.claims_above_n0_are_conditional = true;
        let v = check_laws(&s, &c, &ev_with(&s, 1, 2));
        assert!(v.iter().any(|x| x.law == AntiCheatLaw::NoDegreeLaundering));
    }

    #[test]
    fn renaming_a_stable_residual_is_evasion() {
        let mut s = state();
        let c = clean_claim(&s);
        let p = permit_for(&s, odd_residual());
        write_step(&mut s, p, &c, &std_ev(&state(), c.degree)).expect("first write");

        let mut renamed = clean_claim(&s);
        renamed.residual_content = odd_residual();
        renamed.residual_label = h(88);
        let v = check_laws(&s, &renamed, &std_ev(&s, renamed.degree));
        assert!(
            v.iter().any(|x| x.law == AntiCheatLaw::NoAnomalonEvasion),
            "the same residual under a new label is evasion"
        );
    }

    #[test]
    fn the_same_residual_under_the_same_label_is_not_evasion() {
        let mut s = state();
        let c = clean_claim(&s);
        let p = permit_for(&s, odd_residual());
        write_step(&mut s, p, &c, &std_ev(&state(), c.degree)).expect("first write");
        let v = check_laws(&s, &c, &std_ev(&s, c.degree));
        assert!(!v.iter().any(|x| x.law == AntiCheatLaw::NoAnomalonEvasion));
    }

    #[test]
    fn unconditional_claims_above_n0_refuse() {
        let s = state();
        let mut c = clean_claim(&s);
        c.degree = 3;
        c.claims_above_n0_are_conditional = false;
        let v = check_laws(&s, &c, &std_ev(&s, c.degree));
        assert!(v
            .iter()
            .any(|x| x.law == AntiCheatLaw::FirstUnresolvedDegreeHonesty));
    }

    #[test]
    fn all_six_laws_are_reachable() {
        let mut reached: Vec<AntiCheatLaw> = Vec::new();
        let s = state();

        for law in AntiCheatLaw::SIX {
            let mut c = clean_claim(&s);
            let mut st = state();
            match law {
                AntiCheatLaw::NoDegreeLaundering => {
                    c.degree = 2;
                    c.claims_above_n0_are_conditional = true;
                }
                AntiCheatLaw::NoLiftLaundering => {
                    reached.push(law);
                    continue;
                }
                AntiCheatLaw::NoAnomalonEvasion => {
                    let p = permit_for(&st, odd_residual());
                    let cc = clean_claim(&st);
                    write_step(&mut st, p, &cc, &std_ev(&state(), cc.degree)).unwrap();
                    c.residual_label = h(88);
                    let v = check_laws(&st, &c, &std_ev(&st, c.degree));
                    assert!(v.iter().any(|x| x.law == law));
                    reached.push(law);
                    continue;
                }
                AntiCheatLaw::OldSkeletonPreservation => c.skeleton = h(201),
                AntiCheatLaw::DetectorRevalidation => {
                    c.degree = 2;
                    c.repacketized = true;
                    c.claims_above_n0_are_conditional = true;
                }
                AntiCheatLaw::FirstUnresolvedDegreeHonesty => {
                    c.degree = 3;
                }
                AntiCheatLaw::BoundedStopping | AntiCheatLaw::ResidualNonIncrease => continue,
            }
            let ev = match law {
                AntiCheatLaw::NoDegreeLaundering => ev_with(&s, 1, 3),
                AntiCheatLaw::DetectorRevalidation => ev_with(&s, 3, 1),
                _ => std_ev(&s, c.degree.min(3)),
            };
            let v = check_laws(&s, &c, &ev);
            assert!(
                v.iter().any(|x| x.law == law),
                "law {} is unreachable by any fixture",
                law.as_str()
            );
            reached.push(law);
        }
        assert_eq!(
            reached.len(),
            AntiCheatLaw::SIX.len(),
            "coverage denominator: every canonical law needs a reaching fixture"
        );
    }


    #[test]
    fn every_checked_field_changes_the_chain_head() {
        let s = state();
        let scope = s.scope_for(h(3));
        let base = clean_claim(&s);
        let ev = Hash256([0xEE; 32]);
        let base_head = event_commit(None, Some(&base), &scope, &ev, EventKind::Step);

        type Mutation = (&'static str, Box<dyn Fn(&mut StepClaim)>);
        let scope_for_m = scope.clone();
        let mutate: Vec<Mutation> = vec![
            ("op", Box::new(|c: &mut StepClaim| c.op = StepOp::Descent)),
            ("residual_content", Box::new(|c| c.residual_content = h(90))),
            ("residual_label", Box::new(|c| c.residual_label = h(91))),
            ("degree", Box::new(|c| c.degree = 5)),
            ("skeleton", Box::new(|c| c.skeleton = h(92))),
            ("repacketized", Box::new(|c| c.repacketized = true)),
            (
                "conditional",
                Box::new(|c| c.claims_above_n0_are_conditional = true),
            ),
            (
                "loss_ledger",
                Box::new(move |c| {
                    c.loss_ledger = Some(LossLedger::booked(
                        vec![("x".into(), 1)],
                        scope_for_m.clone(),
                    ))
                }),
            ),
        ];

        for (name, m) in mutate {
            let mut c = base.clone();
            m(&mut c);
            assert_ne!(
                base_head,
                event_commit(None, Some(&c), &scope, &ev, EventKind::Step),
                "changing {name} must change the chain head"
            );
        }
    }

    #[test]
    fn the_chain_depends_on_the_previous_head() {
        let s = state();
        let scope = s.scope_for(h(3));
        let c = clean_claim(&s);
        let ev = Hash256([0xEE; 32]);
        assert_ne!(
            event_commit(None, Some(&c), &scope, &ev, EventKind::Step),
            event_commit(Some(&h(55)), Some(&c), &scope, &ev, EventKind::Step)
        );
    }


    #[test]
    fn a_refused_step_records_a_receipt_without_moving_state() {
        let mut s = state();
        let before_head = s.tape_head().cloned();
        let before_degree = s.degree_window();
        let before_skeleton = s.skeleton().clone();

        let mut c = clean_claim(&s);
        c.skeleton = h(210);
        let p = permit_for_claim(&s, &c);
        let ev = std_ev(&s, c.degree);
        write_step(&mut s, p, &c, &ev).expect_err("must refuse");

        assert_eq!(s.tape_head().cloned(), before_head, "head must not move");
        assert_eq!(s.degree_window(), before_degree);
        assert_eq!(s.skeleton(), &before_skeleton);
        assert_eq!(s.steps_written(), 0);
        assert_eq!(s.refusals().len(), 1, "the attempt must be recorded");
        assert!(s.refusals()[0]
            .laws
            .contains(&AntiCheatLaw::OldSkeletonPreservation));
    }


    #[test]
    fn the_operation_bound_is_computed_and_enforced() {
        let b = Budget::declare(&rational(10), &rational(3)).unwrap();
        assert_eq!(b.max_ops(), 3, "floor(10/3) = 3");

        let mut s = ControlState::open(
            h(1),
            h(2),
            fixture_d0(),
            h(10),
            Budget::declare(&rational(1), &rational(1)).unwrap(),
        );
        assert_eq!(s.budget().max_ops(), 1);

        let site = scope_for_claim(&s, ODD);
        let claim = clean_claim(&s);
        let ev = std_ev(&s, 1);

        let p1 = can_continue_n(&mut s, &site, &claim, &ev).expect("first admits");
        assert_eq!(s.budget().spent(), 0, "issuance must not spend");

        write_step(&mut s, p1, &claim, &ev).expect("first write");
        assert_eq!(s.budget().spent(), 1, "the write spends");

        let err = can_continue_n(&mut s, &site, &claim, &ev)
            .expect_err("the operation bound is exhausted");
        assert!(err
            .violations()
            .iter()
            .any(|v| v.law == AntiCheatLaw::BoundedStopping));
    }

    #[test]
    fn a_residual_increase_without_an_audited_ledger_refuses() {
        let mut s = state();
        let site = scope_for_claim(&s, ODD);
        let ev = ContinuationEvidence {
            outstanding_obligation: ObligationWitness::exhibit(h(5), 1, site.clone()),
            higher_obligation_witness: ObligationWitness::exhibit(h(6), 2, site.clone()),
            next_carrier_manifest: BoundCarrierManifest::new(h(2), fixture_d0()),
            adapter_ledger: LossLedger::empty(site.clone()),
            detector: adequacy(&state(), 1),
            lift: None,
            skeleton_preserved: true,
            coda_gtla_refusal: None,
            residual: delta(3, 7, site.clone()),
        };
        let cc = clean_claim(&s);
        let err = can_continue_n(&mut s, &site, &cc, &ev).expect_err("Phi rose with no ledger");
        assert!(err
            .violations()
            .iter()
            .any(|v| v.law == AntiCheatLaw::ResidualNonIncrease));
    }

    #[test]
    fn a_residual_increase_with_an_audited_ledger_is_lawful() {
        let mut s = state();
        let site = scope_for_claim(&s, ODD);
        let ev = ContinuationEvidence {
            outstanding_obligation: ObligationWitness::exhibit(h(5), 1, site.clone()),
            higher_obligation_witness: ObligationWitness::exhibit(h(6), 2, site.clone()),
            next_carrier_manifest: BoundCarrierManifest::new(h(2), fixture_d0()),
            adapter_ledger: LossLedger::booked(vec![("coarsened_faces".into(), 4)], site.clone()),
            detector: adequacy(&state(), 1),
            lift: None,
            skeleton_preserved: true,
            coda_gtla_refusal: None,
            residual: delta(3, 7, site.clone()),
        };
        let cc = clean_claim(&s);
        can_continue_n(&mut s, &site, &cc, &ev).expect("an audited increase is permitted");
    }

    #[test]
    fn a_residual_delta_from_another_scope_is_refused() {
        let mut s = state();
        let site = s.scope_for(h(3));
        let elsewhere = s.scope_for(h(77));
        let ev = ContinuationEvidence {
            outstanding_obligation: ObligationWitness::exhibit(h(5), 1, site.clone()),
            higher_obligation_witness: ObligationWitness::exhibit(h(6), 2, site.clone()),
            next_carrier_manifest: BoundCarrierManifest::new(h(2), fixture_d0()),
            adapter_ledger: LossLedger::empty(site.clone()),
            detector: adequacy(&state(), 1),
            lift: None,
            skeleton_preserved: true,
            coda_gtla_refusal: None,
            residual: delta(5, 1, elsewhere),
        };
        let cc = clean_claim(&s);
        let err = can_continue_n(&mut s, &site, &cc, &ev).expect_err("delta bound elsewhere");
        assert!(matches!(err, LawRefusal::Scope(_)));
    }

    #[test]
    fn the_residual_delta_reports_the_verified_values() {
        let s = state();
        let d = delta(7, 2, s.scope_for(h(3)));
        assert!(!d.increases());
        assert_eq!(d.delta(), rational(-5));
    }

    #[test]
    fn phi1_endpoints_over_different_d0_are_not_comparable() {
        use tfqm_functional::phi1::{ExactPhi1Certificate, Phi1Functional};
        let two_edge = Phi1Functional::verify_exact_certificate(ExactPhi1Certificate {
            omega: vec![rational(1), rational(1)],
            d0: vec![vec![rational(0)], vec![rational(0)]],
            weights: vec![rational(1), rational(1)],
            alpha: vec![rational(0)],
            primal_residual: vec![rational(1), rational(1)],
            dual_witness: vec![rational(1), rational(1)],
            reported_value: rational(2),
        })
        .expect("two-edge certificate must verify");

        let s = state();
        let err = ResidualDelta::from_verified(&verified_phi1(1), &two_edge, s.scope_for(h(3)))
            .expect_err("different d0 must refuse");
        assert!(err
            .violations()
            .iter()
            .any(|v| v.law == AntiCheatLaw::ResidualNonIncrease));
    }

    #[test]
    fn a_constant_detector_cannot_establish_adequacy() {
        struct Constant(DetectorDescriptor);
        impl Detector for Constant {
            fn descriptor(&self) -> &DetectorDescriptor {
                &self.0
            }
            fn verdict(&self, _subject: &RunSubject<'_>) -> Vec<u8> {
                vec![7]
            }
        }
        let s = state();
        assert_eq!(
            DetectorAdequacy::by_running(
                &Constant(desc(h(2))),
                ODD,
                EVEN,
                1,
                scope_for_claim(&s, ODD)
            ),
            Err(AdequacyRefusal::CoincidentVerdicts),
            "a constant detector separates nothing"
        );
    }

    #[test]
    fn unequal_inputs_alone_do_not_mint_adequacy() {
        struct Constant(DetectorDescriptor);
        impl Detector for Constant {
            fn descriptor(&self) -> &DetectorDescriptor {
                &self.0
            }
            fn verdict(&self, _subject: &RunSubject<'_>) -> Vec<u8> {
                Vec::new()
            }
        }
        let s = state();
        assert_eq!(
            DetectorAdequacy::by_running(
                &Constant(desc(h(2))),
                b"a",
                b"b",
                1,
                scope_for_claim(&s, b"a")
            ),
            Err(AdequacyRefusal::CoincidentVerdicts),
            "two unequal literals must not be enough -- that was the old forgery"
        );
    }

    #[test]
    fn an_input_cannot_be_separated_from_itself() {
        let s = state();
        assert_eq!(
            DetectorAdequacy::by_running(
                &ParityDetector::on(h(2)),
                ODD,
                ODD,
                1,
                scope_for_claim(&s, ODD)
            ),
            Err(AdequacyRefusal::IdenticalInputs)
        );
    }

    #[test]
    fn a_nondeterministic_detector_cannot_establish_adequacy() {
        use std::cell::Cell;
        struct Flapping(Cell<u8>, DetectorDescriptor);
        impl Detector for Flapping {
            fn descriptor(&self) -> &DetectorDescriptor {
                &self.1
            }
            fn verdict(&self, _subject: &RunSubject<'_>) -> Vec<u8> {
                let n = self.0.get().wrapping_add(1);
                self.0.set(n);
                vec![n]
            }
        }
        let s = state();
        assert_eq!(
            DetectorAdequacy::by_running(
                &Flapping(Cell::new(0), desc(h(2))),
                ODD,
                EVEN,
                1,
                scope_for_claim(&s, ODD)
            ),
            Err(AdequacyRefusal::RepeatabilityFailure),
            "a detector that changes its answer witnesses nothing"
        );
    }

    #[test]
    fn a_real_detector_on_a_separable_pair_succeeds() {
        let s = state();
        let a = adequacy(&s, 1);
        assert_eq!(a.degree(), 1);
        assert_eq!(a.detector(), &ParityDetector::on(h(2)).descriptor().id());
        assert_ne!(
            a.claim(),
            a.counterclaim(),
            "the receipt must record which pair was separated"
        );
    }

    #[test]
    fn detector_identity_and_the_separated_pair_change_the_tape_head() {
        let s = state();
        let site = scope_for_claim(&s, ODD);
        let claim = clean_claim(&s);

        let base_ev = ContinuationEvidence {
            outstanding_obligation: ObligationWitness::exhibit(h(5), 1, site.clone()),
            higher_obligation_witness: ObligationWitness::exhibit(h(6), 2, site.clone()),
            next_carrier_manifest: BoundCarrierManifest::new(h(2), fixture_d0()),
            adapter_ledger: LossLedger::empty(site.clone()),
            detector: adequacy(&s, 1),
            lift: None,
            skeleton_preserved: true,
            coda_gtla_refusal: None,
            residual: delta(5, 3, site.clone()),
        };
        let base_head = event_commit(
            None,
            Some(&claim),
            &site,
            &base_ev.commit(),
            EventKind::Step,
        );

        let other_detector = DetectorAdequacy::by_running(
            &OtherParity(DetectorDescriptor::new(
                "test.parity.other",
                "v1",
                "parity_bit",
                h(2),
                [1usize],
                Hash256([0; 32]),
            )),
            ODD,
            EVEN,
            1,
            site.clone(),
        )
        .expect("the other detector also separates odd from even");
        assert_ne!(
            other_detector.detector(),
            base_ev.detector.detector(),
            "different descriptors must derive different ids"
        );
        let mut ev_a = ContinuationEvidence {
            detector: other_detector,
            ..clone_evidence(&base_ev, &site, &s)
        };
        ev_a.next_carrier_manifest = BoundCarrierManifest::new(h(2), fixture_d0());
        assert_ne!(
            base_head,
            event_commit(None, Some(&claim), &site, &ev_a.commit(), EventKind::Step),
            "changing the detector must change the tape head"
        );

        let other_pair =
            DetectorAdequacy::by_running(&ParityDetector::on(h(2)), ODD, &[0, 0], 1, site.clone())
                .expect("odd vs a different even input still separates");
        assert_ne!(
            other_pair.counterclaim(),
            base_ev.detector.counterclaim(),
            "a different counterclaim must be recorded"
        );
        let ev_b = ContinuationEvidence {
            detector: other_pair,
            ..clone_evidence(&base_ev, &site, &s)
        };
        assert_ne!(
            base_head,
            event_commit(None, Some(&claim), &site, &ev_b.commit(), EventKind::Step),
            "changing the separated pair must change the tape head"
        );
    }

    struct OtherParity(DetectorDescriptor);
    impl Detector for OtherParity {
        fn descriptor(&self) -> &DetectorDescriptor {
            &self.0
        }
        fn verdict(&self, subject: &RunSubject<'_>) -> Vec<u8> {
            vec![subject.input.iter().fold(0u8, |a, b| a ^ b) & 1]
        }
    }

    fn clone_evidence(
        src: &ContinuationEvidence,
        site: &ScopeBinding,
        s: &ControlState,
    ) -> ContinuationEvidence {
        let _ = src;
        ContinuationEvidence {
            outstanding_obligation: ObligationWitness::exhibit(h(5), 1, site.clone()),
            higher_obligation_witness: ObligationWitness::exhibit(h(6), 2, site.clone()),
            next_carrier_manifest: BoundCarrierManifest::new(h(2), fixture_d0()),
            adapter_ledger: LossLedger::empty(site.clone()),
            detector: adequacy(s, 1),
            lift: None,
            skeleton_preserved: true,
            coda_gtla_refusal: None,
            residual: delta(5, 3, site.clone()),
        }
    }

    #[test]
    fn identical_evidence_commits_identically() {
        let s = state();
        let site = scope_for_claim(&s, ODD);
        let a = clone_evidence(
            &clone_evidence(
                &ContinuationEvidence {
                    outstanding_obligation: ObligationWitness::exhibit(h(5), 1, site.clone()),
                    higher_obligation_witness: ObligationWitness::exhibit(h(6), 2, site.clone()),
                    next_carrier_manifest: BoundCarrierManifest::new(h(2), fixture_d0()),
                    adapter_ledger: LossLedger::empty(site.clone()),
                    detector: adequacy(&s, 1),
                    lift: None,
                    skeleton_preserved: true,
                    coda_gtla_refusal: None,
                    residual: delta(5, 3, site.clone()),
                },
                &site,
                &s,
            ),
            &site,
            &s,
        );
        let b = clone_evidence(&a, &site, &s);
        assert_eq!(a.commit(), b.commit());
    }

    #[test]
    fn a_detector_configured_for_another_carrier_is_refused() {
        let s = state();
        let err = DetectorAdequacy::by_running(
            &ParityDetector::on(h(99)),
            ODD,
            EVEN,
            1,
            scope_for_claim(&s, ODD),
        )
        .expect_err("a detector for carrier 99 must not answer at carrier 2");
        assert!(matches!(err, AdequacyRefusal::CarrierMismatch { .. }));
    }

    #[test]
    fn adequacy_for_one_residual_cannot_authorize_another() {
        let s = state();
        let err = DetectorAdequacy::by_running(
            &ParityDetector::on(h(2)),
            ODD,
            EVEN,
            1,
            s.scope_for(h(77)),
        )
        .expect_err("the claim must be the scoped residual");
        assert!(matches!(
            err,
            AdequacyRefusal::ClaimIsNotTheScopedResidual { .. }
        ));
    }

    #[test]
    fn a_detector_cannot_be_stamped_with_an_undeclared_degree() {
        let s = state();
        let refusal = DetectorAdequacy::by_running(
            &ParityDetector::on(h(2)),
            ODD,
            EVEN,
            9,
            scope_for_claim(&s, ODD),
        )
        .expect_err("degree 9 was never declared");
        assert!(matches!(
            refusal,
            AdequacyRefusal::DegreeNotSupported { degree: 9, .. }
        ));
    }

    #[test]
    fn a_declared_degree_is_accepted() {
        let s = state();
        assert!(DetectorAdequacy::by_running(
            &ParityDetector::on(h(2)),
            ODD,
            EVEN,
            3,
            scope_for_claim(&s, ODD),
        )
        .is_ok());
    }

    #[test]
    fn a_permit_cannot_be_spent_on_a_different_claim() {
        let mut s = state();
        let site = scope_for_claim(&s, ODD);
        let mut licensed = clean_claim(&s);
        licensed.residual_content = digest(ADEQUACY_DOMAIN, &[ODD]);
        let ev = std_ev(&s, 1);

        let permit = can_continue_n(&mut s, &site, &licensed, &ev).expect("degree-1 claim admits");

        let mut substituted = licensed.clone();
        substituted.degree = 9;

        let err = write_step(&mut s, permit, &substituted, &ev)
            .expect_err("a permit licenses one claim, not a scope");
        assert!(
            matches!(err, LawRefusal::PermitMismatch { .. }),
            "got {err}"
        );
        assert_eq!(s.steps_written(), 0, "nothing may be written");
    }

    #[test]
    fn a_permit_cannot_be_spent_under_different_evidence() {
        let mut s = state();
        let site = scope_for_claim(&s, ODD);
        let mut claim = clean_claim(&s);
        claim.residual_content = digest(ADEQUACY_DOMAIN, &[ODD]);
        let ev = std_ev(&s, 1);
        let permit = can_continue_n(&mut s, &site, &claim, &ev).expect("admits");

        let other_ev = ev_with(&s, 3, 3);
        let err = write_step(&mut s, permit, &claim, &other_ev)
            .expect_err("the evidence must be the evidence that licensed it");
        assert!(
            matches!(err, LawRefusal::PermitMismatch { .. }),
            "got {err}"
        );
    }

    #[test]
    fn a_refused_continuation_does_not_spend_budget() {
        let mut s = state();
        let site = scope_for_claim(&s, ODD);
        let claim = clean_claim(&s);
        let mut ev = std_ev(&s, 1);
        ev.coda_gtla_refusal = Some(CodaGtlaRefusal::issued("fixture refusal", site.clone()));

        let before = s.budget().spent();
        can_continue_n(&mut s, &site, &claim, &ev).expect_err("GTLA refusal blocks");
        assert_eq!(
            s.budget().spent(),
            before,
            "a refused continuation must not consume budget"
        );
    }

    #[test]
    fn a_permit_cannot_be_laundered_through_terminalize() {
        let s = state();
        let site = scope_for_claim(&s, ODD);
        let g2 = Gamma2Zero::verify(&rational(0), site.clone()).unwrap();
        let mut registry = ObligationRegistry::new(site.clone());
        registry.register(1);
        let err = registry
            .issue_terminal_permit(site.clone(), &g2)
            .expect_err("open obligation blocks permit");
        assert!(matches!(err, TerminalRefusal::ObligationsOpen { .. }));

        let clean_reg = ObligationRegistry::new(site.clone());
        let permit = clean_reg
            .issue_terminal_permit(site.clone(), &g2)
            .expect("permit issued");
        let foreign_site = s.scope_for(h(99));
        let g2_foreign = Gamma2Zero::verify(&rational(0), foreign_site.clone()).unwrap();
        let err = terminalize(s, permit, g2_foreign).expect_err("mismatched scope must refuse");
        assert!(matches!(err, TerminalRefusal::Scope(_)));
    }

    #[test]
    fn a_matching_permit_still_terminalizes() {
        let s = state();
        let site = scope_for_claim(&s, ODD);
        let g2 = Gamma2Zero::verify(&rational(0), site.clone()).unwrap();
        let registry = ObligationRegistry::new(site.clone());
        let permit = registry
            .issue_terminal_permit(site.clone(), &g2)
            .expect("permit issued");

        let t = terminalize(s, permit, g2).expect("matching pair");
        assert_eq!(t.terminal(), TraceTerminal::Terminalized);
        assert_eq!(t.steps_written(), 1);
    }

    #[test]
    fn a_lift_step_must_carry_its_own_admission() {
        let mut s = state();
        let site = scope_for_claim(&s, ODD);

        let ghost_manifest = BoundCarrierManifest::new(h(0xBB), h(0xBB));
        let ghost = ScopeBinding::new(h(0xAA), ghost_manifest, h(0xCC), Some(h(0xDD)), 0);
        let exhaustion =
            SameCarrierExhaustion::by_searching(0..1, |_: &i32| false, ghost.clone()).unwrap();
        let ghost_admission =
            BoundLiftAdmission::bind(&admitted_lift(), &exhaustion, ghost).unwrap();

        let mut claim = clean_claim(&s);
        claim.residual_content = digest(ADEQUACY_DOMAIN, &[ODD]);
        claim.op = StepOp::Lift(ghost_admission);
        let ev = std_ev(&s, 1);

        let permit = StepPermit::issue(site.clone(), ev.commit(), &claim);
        let err = write_step(&mut s, permit, &claim, &ev)
            .expect_err("a ghost admission must not ride a real permit");
        assert!(matches!(err, LawRefusal::Scope(_)), "got {err}");
        assert_eq!(s.steps_written(), 0);
    }

    #[test]
    fn a_terminal_and_a_step_do_not_share_a_head() {
        let s = state();
        let site = scope_for_claim(&s, ODD);
        let claim = clean_claim(&s);
        let ev = std_ev(&s, 1);
        let g2 = Gamma2Zero::verify(&rational(0), site.clone()).unwrap();
        let closure = ObligationClosure::discharge(&[], 1, site.clone()).unwrap();

        let step_head = event_commit(None, Some(&claim), &site, &ev.commit(), EventKind::Step);
        let terminal_head = event_commit(
            None,
            Some(&claim),
            &site,
            &ev.commit(),
            EventKind::Terminal(terminal_commit(&g2, &closure)),
        );
        assert_ne!(step_head, terminal_head);
    }

    #[test]
    fn terminal_evidence_changes_the_terminal_commitment() {
        let s = state();
        let site = scope_for_claim(&s, ODD);
        let g2 = Gamma2Zero::verify(&rational(0), site.clone()).unwrap();

        let a = terminal_commit(
            &g2,
            &ObligationClosure::discharge(&[], 1, site.clone()).unwrap(),
        );
        let b = terminal_commit(
            &g2,
            &ObligationClosure::discharge(&[], 7, site.clone()).unwrap(),
        );
        assert_ne!(a, b, "highest_discharged must be committed");
    }

    #[test]
    fn a_dropped_permit_does_not_consume_budget() {
        let mut s = state();
        let site = scope_for_claim(&s, ODD);
        let claim = clean_claim(&s);
        let ev = std_ev(&s, 1);

        for _ in 0..5 {
            let permit = can_continue_n(&mut s, &site, &claim, &ev).expect("admits");
            drop(permit);
        }
        assert_eq!(
            s.budget().spent(),
            0,
            "five issued-and-dropped permits must cost nothing"
        );
    }

    #[test]
    fn a_nonpositive_cost_floor_is_refused() {
        Budget::declare(&rational(10), &rational(0))
            .expect_err("a zero cost floor does not bound the op count");
    }

    #[test]
    fn the_nine_conjuncts_are_named() {
        assert_eq!(CONTINUATION_CONJUNCTS.len(), 9);
    }

    #[test]
    fn authority_effect_is_none() {
        assert_eq!(AUTHORITY_EFFECT, AuthorityEffect::None);
    }
}
