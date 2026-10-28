
use num_rational::BigRational;
use num_traits::{Signed, Zero};
use serde::{Deserialize, Serialize};
use std::ops::Sub;
use thiserror::Error;

use engine_types::{
    AuthorityTerminal, ObstructionDiagnosticClass, Outcome, RefusalSource, ResidualTerminal,
};


#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct DualWitness {
    pub witness_id: String,
    pub dual_vector: Vec<BigRational>,
    pub certificate_hash: String,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct FocSignature {
    pub phi_1: BigRational,
    pub gamma_2: BigRational,
    pub dual_witness: Option<DualWitness>,
    pub duality_gap: BigRational,
    pub trichotomy: ObstructionDiagnosticClass,
}

impl FocSignature {
    pub fn new_exact() -> Self {
        Self {
            phi_1: BigRational::zero(),
            gamma_2: BigRational::zero(),
            dual_witness: None,
            duality_gap: BigRational::zero(),
            trichotomy: ObstructionDiagnosticClass::ExactRepair,
        }
    }

    pub fn new_obstructed(phi_1: BigRational, gamma_2: BigRational, witness: DualWitness) -> Self {
        let trichotomy = if gamma_2.is_zero() {
            ObstructionDiagnosticClass::ClosedResidual
        } else {
            ObstructionDiagnosticClass::ActiveClosureFailure
        };
        Self {
            phi_1,
            gamma_2,
            dual_witness: Some(witness),
            duality_gap: BigRational::zero(),
            trichotomy,
        }
    }

    pub fn is_exact(&self) -> bool {
        self.phi_1.is_zero() && self.gamma_2.is_zero() && self.duality_gap.is_zero()
    }
}

pub trait IntoCochainComplex {
    fn carrier_locus(&self) -> String;
    fn coboundary_0(&self, c0: &[BigRational]) -> Vec<BigRational>;
    fn coboundary_1(&self, c1: &[BigRational]) -> Vec<BigRational>;
    fn evaluate_foc(&self, c1: &[BigRational]) -> Result<FocSignature, CodaError>;
}


#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct LossEntry {
    pub slot: String,
    pub dropped_degree: usize,
    pub rationale: String,
}

#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct LossLedger {
    pub entries: Vec<LossEntry>,
}

impl LossLedger {
    pub fn record_loss(
        &mut self,
        slot: impl Into<String>,
        degree: usize,
        rationale: impl Into<String>,
    ) {
        self.entries.push(LossEntry {
            slot: slot.into(),
            dropped_degree: degree,
            rationale: rationale.into(),
        });
    }

    pub fn is_lossless(&self) -> bool {
        self.entries.is_empty()
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct TransportCertificate {
    pub source_locus: String,
    pub target_locus: String,
    pub commutation_defect: BigRational,
    pub loss_ledger: LossLedger,
    pub is_retraction: bool,
}


#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct ContinuumShadow<XCont, XFin> {
    pub continuum_concept_id: String,
    pub finite_profile: XFin,
    pub fiber_constancy_witness: String,
    pub _marker: std::marker::PhantomData<XCont>,
}


#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct MetricSeparation {
    pub epsilon_mesh: BigRational,
    pub separation_distance: BigRational,
    pub anti_collapse_passed: bool,
}

impl MetricSeparation {
    pub fn check(
        separation_distance: BigRational,
        epsilon: BigRational,
    ) -> Result<Self, CodaError> {
        let threshold = &epsilon * BigRational::from_integer(2.into());
        if separation_distance <= threshold {
            return Err(CodaError::MetricCollapse(format!(
                "Separation {} <= 2*epsilon {}",
                separation_distance, threshold
            )));
        }
        Ok(Self {
            epsilon_mesh: epsilon,
            separation_distance,
            anti_collapse_passed: true,
        })
    }
}


#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct Enclosure<G> {
    pub lo: G,
    pub hi: G,
}

impl<G: PartialOrd + Sub<Output = G> + Clone> Enclosure<G> {
    pub fn new(lo: G, hi: G) -> Result<Self, CodaError> {
        if lo > hi {
            return Err(CodaError::InvalidEnclosure("lo must be <= hi".into()));
        }
        Ok(Self { lo, hi })
    }

    pub fn diameter(&self) -> G {
        self.hi.clone() - self.lo.clone()
    }
}

impl Enclosure<BigRational> {
    pub fn midpoint(&self) -> BigRational {
        (&self.lo + &self.hi) / BigRational::from_integer(2.into())
    }

    pub fn contains_with_bound(&self, x: &BigRational) -> bool {
        let mid = self.midpoint();
        let half_width = self.diameter() / BigRational::from_integer(2.into());
        let diff = (x - &mid).abs();
        diff <= half_width && x >= &self.lo && x <= &self.hi
    }
}


#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct AnomalonRecord {
    pub anomalon_id: String,
    pub residual_class_hash: String,
    pub phi_1: BigRational,
    pub dual_witness_hash: String,
    pub carrier_locus: String,
    pub created_at: String,
}

#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct AnomalonRegister {
    pub records: Vec<AnomalonRecord>,
}

impl AnomalonRegister {
    pub fn commit(&mut self, record: AnomalonRecord) {
        self.records.push(record);
    }

    pub fn find(&self, id: &str) -> Option<&AnomalonRecord> {
        self.records.iter().find(|r| r.anomalon_id == id)
    }
}


#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct OverlapGluing<T> {
    pub left_slot: T,
    pub shared_slot_left: String,
    pub shared_slot_right: String,
    pub right_slot: T,
}

impl<T: Clone> OverlapGluing<T> {
    pub fn glue(self) -> Result<(T, String, T), CodaError> {
        if self.shared_slot_left != self.shared_slot_right {
            return Err(CodaError::IncompatibleOverlap(format!(
                "Shared slot mismatch: '{}' != '{}'",
                self.shared_slot_left, self.shared_slot_right
            )));
        }
        Ok((self.left_slot, self.shared_slot_left, self.right_slot))
    }
}


#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct FdaPacket<T> {
    pub carrier: String,
    pub evidence: T,
    pub dual_witness: DualWitness,
    pub transport_trace: Vec<String>,
    pub lift_license: String,
    pub proposer_id: String,
    pub authorizer_id: String,
    pub budget_remaining: u64,
}

pub struct SevenHaltGuards;

impl SevenHaltGuards {
    pub fn verify<T>(packet: &FdaPacket<T>) -> Result<(), CodaError> {
        if packet.carrier.is_empty() {
            return Err(CodaError::HaltGuardFailed("Empty carrier".into()));
        }
        if packet.dual_witness.witness_id.is_empty() {
            return Err(CodaError::HaltGuardFailed("Invalid dual witness".into()));
        }
        if packet.lift_license.is_empty() {
            return Err(CodaError::HaltGuardFailed("Missing lift license".into()));
        }
        if packet.transport_trace.is_empty() {
            return Err(CodaError::HaltGuardFailed("Empty transport trace".into()));
        }
        if packet.budget_remaining == 0 {
            return Err(CodaError::HaltGuardFailed("Budget exhausted".into()));
        }
        if packet.proposer_id == packet.authorizer_id {
            return Err(CodaError::RoleSplitViolation(format!(
                "proposer '{}' cannot self-authorize",
                packet.proposer_id
            )));
        }
        Ok(())
    }
}


#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct CryptographicGrant {
    pub key_id: String,
    pub signature_hex: String,
    pub timestamp: String,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct TerminalRefusal {
    pub code: String,
    pub reason: String,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum CodaGtlaOutcome<T> {
    Authorized(T, CryptographicGrant),
    ResidualTrapped(AnomalonRecord),
    Refused(TerminalRefusal),
}

impl<T> CodaGtlaOutcome<T> {
    pub fn to_outcome(&self) -> Outcome {
        match self {
            CodaGtlaOutcome::Authorized(_, _) => Outcome::Terminal(AuthorityTerminal::ExactRuleDerived),
            CodaGtlaOutcome::ResidualTrapped(_) => Outcome::Residual(ResidualTerminal::ClosedResidual),
            CodaGtlaOutcome::Refused(_) => Outcome::Refused(RefusalSource::Refusal),
        }
    }
}


#[derive(Debug, Error, PartialEq, Eq)]
pub enum CodaError {
    #[error("Metric collapse error: {0}")]
    MetricCollapse(String),

    #[error("Invalid enclosure: {0}")]
    InvalidEnclosure(String),

    #[error("Incompatible overlap: {0}")]
    IncompatibleOverlap(String),

    #[error("Role split violation: {0}")]
    RoleSplitViolation(String),

    #[error("Halt guard failed: {0}")]
    HaltGuardFailed(String),

    #[error("Evaluation error: {0}")]
    Evaluation(String),
}
