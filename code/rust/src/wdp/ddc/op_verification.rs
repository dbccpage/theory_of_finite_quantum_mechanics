
use engine_types::authority::AuthorityEffect;
use serde::{Deserialize, Serialize};

use crate::ddc::ddc_alphabet::{DdaOp, DdaStep, DdaTrace, StepOutcome};
use crate::ddc::degree_tower::{
    BinaryCochainSegment, DegreeDiagnostic, DegreeTowerError, DegreeTrichotomy,
};

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct CochainState {
    pub segment: BinaryCochainSegment,
    pub residual: Vec<bool>,
    pub adequate: bool,
}

impl CochainState {
    pub fn new(
        segment: BinaryCochainSegment,
        residual: Vec<bool>,
    ) -> Result<Self, DegreeTowerError> {
        Self::with_adequacy_state(segment, residual, true)
    }

    pub fn with_adequacy_state(
        segment: BinaryCochainSegment,
        residual: Vec<bool>,
        adequate: bool,
    ) -> Result<Self, DegreeTowerError> {
        if residual.len() != segment.residual_dim() {
            return Err(DegreeTowerError::InputDimensionMismatch {
                expected: segment.residual_dim(),
                actual: residual.len(),
            });
        }
        Ok(Self {
            segment,
            residual,
            adequate,
        })
    }

    pub fn with_adequacy(mut self, adequate: bool) -> Self {
        self.adequate = adequate;
        self
    }

    pub fn diagnose(&self) -> Result<DegreeDiagnostic, DegreeTowerError> {
        self.segment.diagnose(&self.residual)
    }

    pub fn same_carrier(&self, other: &Self) -> bool {
        self.segment == other.segment
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub enum OpViolation {
    ExactRepairLeftResidual {
        phi_after: usize,
        gamma_after: usize,
    },
    FixedCarrierOpChangedCarrier { op: DdaOp },
    ResidualProjectionChangedMass { phi_before: usize, phi_after: usize },
    InertOpMutatedState { op: DdaOp },
    TerminalizedOpenResidual { gamma: usize },
    CarrierUnchangedUnderRestructure { op: DdaOp },
    Malformed { reason: String },

    ExactRepairFromNonExactClass,
    ExactRepairLeftDefect,
    ResidualProjectionChangedClosure {
        gamma_before: usize,
        gamma_after: usize,
    },
    ContextExposureLoweredObstruction,
    MissingReceipt,
    MissingLossLedger,
    UnlicensedLift,
    LiftWithoutTrigger,
    MissingRefusalReason,
    BlindDetector,
    TerminalAbsorbing,
    RefusalAbsorbing,
    UnknownLetter,
}

impl OpViolation {
    pub fn code(&self) -> &'static str {
        match self {
            OpViolation::ExactRepairLeftResidual { .. } => "ExactRepairLeftResidual",
            OpViolation::FixedCarrierOpChangedCarrier { .. } => "FixedCarrierOpChangedCarrier",
            OpViolation::ResidualProjectionChangedMass { .. } => "ResidualProjectionChangedMass",
            OpViolation::InertOpMutatedState { .. } => "InertOpMutatedState",
            OpViolation::TerminalizedOpenResidual { .. } => "TerminalizedOpenResidual",
            OpViolation::CarrierUnchangedUnderRestructure { .. } => {
                "CarrierUnchangedUnderRestructure"
            }
            OpViolation::Malformed { .. } => "Malformed",
            OpViolation::ExactRepairFromNonExactClass => "ExactRepairFromNonExactClass",
            OpViolation::ExactRepairLeftDefect => "ExactRepairLeftDefect",
            OpViolation::ResidualProjectionChangedClosure { .. } => {
                "ResidualProjectionChangedClosure"
            }
            OpViolation::ContextExposureLoweredObstruction => "ContextExposureLoweredObstruction",
            OpViolation::MissingReceipt => "MissingReceipt",
            OpViolation::MissingLossLedger => "MissingLossLedger",
            OpViolation::UnlicensedLift => "UnlicensedLift",
            OpViolation::LiftWithoutTrigger => "LiftWithoutTrigger",
            OpViolation::MissingRefusalReason => "MissingRefusalReason",
            OpViolation::BlindDetector => "BlindDetector",
            OpViolation::TerminalAbsorbing => "TerminalAbsorbing",
            OpViolation::RefusalAbsorbing => "RefusalAbsorbing",
            OpViolation::UnknownLetter => "UnknownLetter",
        }
    }
}

impl std::fmt::Display for OpViolation {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.code())
    }
}

impl std::error::Error for OpViolation {}

impl From<DegreeTowerError> for OpViolation {
    fn from(e: DegreeTowerError) -> Self {
        OpViolation::Malformed {
            reason: format!("{e:?}"),
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Default, Serialize, Deserialize)]
pub struct StepWitness {
    #[serde(default)]
    pub receipt: bool,
    #[serde(default)]
    pub loss_ledger: bool,
    #[serde(default)]
    pub lift_licence: bool,
    #[serde(default)]
    pub reason: Option<String>,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct StepEvidence {
    pub op: DdaOp,
    pub before: DegreeDiagnostic,
    pub after: DegreeDiagnostic,
}

pub fn verify_step(
    step: &DdaStep,
    before: &CochainState,
    after: &CochainState,
) -> Result<StepEvidence, OpViolation> {
    verify_step_with_witness(step, before, after, None)
}

pub fn verify_step_with_witness(
    step: &DdaStep,
    before: &CochainState,
    after: &CochainState,
    witness: Option<&StepWitness>,
) -> Result<StepEvidence, OpViolation> {
    let before_diag = before.diagnose()?;
    let after_diag = after.diagnose()?;
    let evidence = StepEvidence {
        op: step.op,
        before: before_diag.clone(),
        after: after_diag.clone(),
    };

    if let StepOutcome::RefusedToExecute { .. } = &step.outcome {
        if before != after {
            return Err(OpViolation::InertOpMutatedState { op: step.op });
        }
        return Ok(evidence);
    }

    match step.op {
        DdaOp::ExactRepair => {
            if !before.same_carrier(after) {
                return Err(OpViolation::FixedCarrierOpChangedCarrier { op: step.op });
            }
            if before_diag.classification != DegreeTrichotomy::Exact || before_diag.gamma != 0 {
                return Err(OpViolation::ExactRepairFromNonExactClass);
            }
            if after_diag.classification != DegreeTrichotomy::Exact || after_diag.gamma != 0 {
                return Err(OpViolation::ExactRepairLeftResidual {
                    phi_after: after_diag.phi,
                    gamma_after: after_diag.gamma,
                });
            }
            if after.residual.iter().any(|&b| b) {
                return Err(OpViolation::ExactRepairLeftDefect);
            }
            if !before.adequate {
                return Err(OpViolation::BlindDetector);
            }
        }
        DdaOp::ResidualProjection => {
            if !before.same_carrier(after) {
                return Err(OpViolation::FixedCarrierOpChangedCarrier { op: step.op });
            }
            if before_diag.phi != after_diag.phi {
                return Err(OpViolation::ResidualProjectionChangedMass {
                    phi_before: before_diag.phi,
                    phi_after: after_diag.phi,
                });
            }
            if before_diag.gamma != after_diag.gamma {
                return Err(OpViolation::ResidualProjectionChangedClosure {
                    gamma_before: before_diag.gamma,
                    gamma_after: after_diag.gamma,
                });
            }
            if !before.adequate {
                return Err(OpViolation::BlindDetector);
            }
        }

        DdaOp::Integration => {
            if before != after {
                return Err(OpViolation::InertOpMutatedState { op: step.op });
            }
            if let Some(w) = witness {
                if !w.receipt {
                    return Err(OpViolation::MissingReceipt);
                }
            }
        }
        DdaOp::Refusal => {
            if before != after {
                return Err(OpViolation::InertOpMutatedState { op: step.op });
            }
            if let Some(w) = witness {
                match &w.reason {
                    Some(r) if crate::ddc::ddc_alphabet::RefusalReason::from_str_code(r).is_some() => {}
                    _ => return Err(OpViolation::MissingRefusalReason),
                }
            }
        }
        DdaOp::Terminalize => {
            if before != after {
                return Err(OpViolation::InertOpMutatedState { op: step.op });
            }
            if after_diag.gamma != 0 {
                return Err(OpViolation::TerminalizedOpenResidual {
                    gamma: after_diag.gamma,
                });
            }
            if !before.adequate {
                return Err(OpViolation::BlindDetector);
            }
        }

        DdaOp::ContextExposure => {
            if before.same_carrier(after) {
                return Err(OpViolation::CarrierUnchangedUnderRestructure { op: step.op });
            }
            if after_diag.phi < before_diag.phi || after_diag.gamma < before_diag.gamma {
                return Err(OpViolation::ContextExposureLoweredObstruction);
            }
        }
        DdaOp::Lift => {
            if before.same_carrier(after) {
                return Err(OpViolation::CarrierUnchangedUnderRestructure { op: step.op });
            }
            if let Some(w) = witness {
                if !w.lift_licence {
                    return Err(OpViolation::UnlicensedLift);
                }
                let is_closed = before_diag.classification == DegreeTrichotomy::StabilizedSurvivor
                    || (before_diag.classification != DegreeTrichotomy::Exact
                        && before_diag.gamma == 0);
                if !(is_closed || !before.adequate) {
                    return Err(OpViolation::LiftWithoutTrigger);
                }
            }
        }
        DdaOp::Descent => {
            if before.same_carrier(after) {
                return Err(OpViolation::CarrierUnchangedUnderRestructure { op: step.op });
            }
            if let Some(w) = witness {
                if !w.loss_ledger {
                    return Err(OpViolation::MissingLossLedger);
                }
            }
        }
    }

    Ok(evidence)
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize)]
pub enum ControlStatus {
    Open,
    Refused,
    Terminalized,
}

impl ControlStatus {
    pub fn as_str(&self) -> &'static str {
        match self {
            ControlStatus::Open => "Open",
            ControlStatus::Refused => "Refused",
            ControlStatus::Terminalized => "Terminalized",
        }
    }
}

#[derive(Debug, Clone)]
pub struct VerifiedTrace {
    trace: DdaTrace,
    evidence: Vec<StepEvidence>,
    state: CochainState,
    control: ControlStatus,
}

impl VerifiedTrace {
    pub fn new(initial: CochainState) -> Self {
        Self {
            trace: DdaTrace::new(),
            evidence: Vec::new(),
            state: initial,
            control: ControlStatus::Open,
        }
    }

    pub fn control(&self) -> ControlStatus {
        self.control
    }

    pub fn step(&mut self, step: DdaStep, next: CochainState) -> Result<&mut Self, OpViolation> {
        self.step_with_witness(step, next, None)
    }

    pub fn step_with_witness(
        &mut self,
        step: DdaStep,
        next: CochainState,
        witness: Option<&StepWitness>,
    ) -> Result<&mut Self, OpViolation> {
        if self.control == ControlStatus::Terminalized {
            return Err(OpViolation::TerminalAbsorbing);
        }
        if self.control == ControlStatus::Refused
            && step.op != DdaOp::ContextExposure
            && step.op != DdaOp::Lift
            && step.op != DdaOp::Terminalize
        {
            return Err(OpViolation::RefusalAbsorbing);
        }

        let ev = verify_step_with_witness(&step, &self.state, &next, witness)?;
        self.control = match step.op {
            DdaOp::Terminalize => ControlStatus::Terminalized,
            DdaOp::Refusal => ControlStatus::Refused,
            _ => {
                if matches!(step.outcome, StepOutcome::RefusedToExecute { .. }) {
                    ControlStatus::Refused
                } else if self.control == ControlStatus::Refused {
                    ControlStatus::Open
                } else {
                    self.control
                }
            }
        };
        if step.op == DdaOp::Terminalize {
            self.trace.emit_gated_terminal(step);
        } else {
            self.trace.emit(step);
        }
        self.evidence.push(ev);
        self.state = next;
        Ok(self)
    }

    pub fn step_inert(&mut self, step: DdaStep) -> Result<&mut Self, OpViolation> {
        let same = self.state.clone();
        self.step(step, same)
    }

    pub fn step_inert_with_witness(
        &mut self,
        step: DdaStep,
        witness: Option<&StepWitness>,
    ) -> Result<&mut Self, OpViolation> {
        let same = self.state.clone();
        self.step_with_witness(step, same, witness)
    }

    pub fn import(&mut self, what: impl Into<String>) -> &mut Self {
        self.trace.import(what);
        self
    }

    pub fn trace(&self) -> &DdaTrace {
        &self.trace
    }

    pub fn evidence(&self) -> &[StepEvidence] {
        &self.evidence
    }

    pub fn state(&self) -> &CochainState {
        &self.state
    }

    pub fn letters(&self) -> String {
        self.trace.letters()
    }

    pub fn authority_effect(&self) -> AuthorityEffect {
        AuthorityEffect::None
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::ddc::degree_tower::BinaryLinearMap;

    fn segment() -> BinaryCochainSegment {
        let d0 = BinaryLinearMap::from_rows(1, vec![vec![true], vec![false]]).unwrap();
        let d1 = BinaryLinearMap::from_rows(2, vec![vec![false, true]]).unwrap();
        BinaryCochainSegment::new(1, d0, d1).unwrap()
    }

    fn state(residual: Vec<bool>) -> CochainState {
        CochainState::new(segment(), residual).unwrap()
    }

    #[test]
    fn diagnoses_match_the_trichotomy() {
        assert_eq!(
            state(vec![false, false]).diagnose().unwrap().classification,
            DegreeTrichotomy::Exact
        );
        assert_eq!(state(vec![true, false]).diagnose().unwrap().phi, 0);
        let open = state(vec![false, true]).diagnose().unwrap();
        assert!(open.phi > 0 && open.gamma > 0);
        assert_eq!(open.classification, DegreeTrichotomy::Open);
    }


    #[test]
    fn honest_exact_repair_verifies() {
        let before = state(vec![true, false]);
        let after = state(vec![false, false]);
        let step = DdaStep::executed(DdaOp::ExactRepair, "discharged");
        let ev = verify_step(&step, &before, &after).unwrap();
        assert_eq!(ev.before.phi, 0);
        assert_eq!(ev.after.phi, 0);
    }

    #[test]
    fn exact_repair_from_non_exact_class_is_rejected() {
        let before = state(vec![false, true]);
        let after = state(vec![false, false]);
        let step = DdaStep::executed(DdaOp::ExactRepair, "class crossing edit");
        let err = verify_step(&step, &before, &after).unwrap_err();
        assert_eq!(err, OpViolation::ExactRepairFromNonExactClass);
    }

    #[test]
    fn lying_exact_repair_is_rejected() {
        let before = state(vec![true, false]);
        let after = state(vec![true, false]);
        let step = DdaStep::executed(DdaOp::ExactRepair, "repaired it, honest");
        match verify_step(&step, &before, &after) {
            Err(OpViolation::ExactRepairLeftDefect) => {}
            other => panic!("a lying E must be rejected with ExactRepairLeftDefect, got {other:?}"),
        }

        let after_open = state(vec![false, true]);
        match verify_step(&step, &before, &after_open) {
            Err(OpViolation::ExactRepairLeftResidual {
                phi_after,
                gamma_after,
            }) => {
                assert!(phi_after > 0);
                assert!(gamma_after > 0);
            }
            other => panic!(
                "E leaving residual must be rejected with ExactRepairLeftResidual, got {other:?}"
            ),
        }
    }

    fn survivor_segment() -> BinaryCochainSegment {
        let d0 = BinaryLinearMap::zero(1, 1);
        let d1 = BinaryLinearMap::zero(1, 1);
        BinaryCochainSegment::new(1, d0, d1).unwrap()
    }

    #[test]
    fn partial_repair_to_a_survivor_is_not_an_exact_repair() {
        let before = CochainState::new(survivor_segment(), vec![true]).unwrap();
        let diag = before.diagnose().unwrap();
        assert_eq!(diag.classification, DegreeTrichotomy::StabilizedSurvivor);
        assert!(diag.phi > 0 && diag.gamma == 0);

        let step = DdaStep::executed(DdaOp::ExactRepair, "mostly repaired");
        match verify_step(&step, &before, &before.clone()) {
            Err(OpViolation::ExactRepairFromNonExactClass) => {}
            other => panic!("E must reject a survivor as non-exact class, got {other:?}"),
        }
    }

    #[test]
    fn a_survivor_may_legitimately_terminalize() {
        let s = CochainState::new(survivor_segment(), vec![true]).unwrap();
        assert_eq!(
            s.diagnose().unwrap().classification,
            DegreeTrichotomy::StabilizedSurvivor
        );
        let step = DdaStep::executed(DdaOp::Terminalize, "sealed as ClosedSurvivor");
        assert!(
            verify_step(&step, &s, &s.clone()).is_ok(),
            "ClosedSurvivor must be sealable — it is a terminal, not a failure"
        );
    }

    #[test]
    fn exact_repair_may_not_restructure_the_carrier() {
        let before = state(vec![false, true]);
        let d0 =
            BinaryLinearMap::from_rows(2, vec![vec![true, false], vec![false, false]]).unwrap();
        let d1 = BinaryLinearMap::from_rows(2, vec![vec![false, true]]).unwrap();
        let other = CochainState::new(
            BinaryCochainSegment::new(1, d0, d1).unwrap(),
            vec![false, false],
        )
        .unwrap();
        let step = DdaStep::executed(DdaOp::ExactRepair, "repaired by changing the question");
        match verify_step(&step, &before, &other) {
            Err(OpViolation::FixedCarrierOpChangedCarrier { op }) => {
                assert_eq!(op, DdaOp::ExactRepair)
            }
            other => panic!("expected carrier violation, got {other:?}"),
        }
    }


    #[test]
    fn residual_projection_that_repairs_is_rejected() {
        let before = state(vec![false, true]);
        let after = state(vec![false, false]);
        let step = DdaStep::executed(DdaOp::ResidualProjection, "projected");
        match verify_step(&step, &before, &after) {
            Err(OpViolation::ResidualProjectionChangedMass {
                phi_before,
                phi_after,
            }) => {
                assert!(phi_before > phi_after)
            }
            other => panic!("expected mass violation, got {other:?}"),
        }
    }


    #[test]
    fn ledger_append_that_mutates_is_rejected() {
        let before = state(vec![false, true]);
        let after = state(vec![false, false]);
        let step = DdaStep::executed(DdaOp::Integration, "appended a receipt");
        match verify_step(&step, &before, &after) {
            Err(OpViolation::InertOpMutatedState { op }) => assert_eq!(op, DdaOp::Integration),
            other => panic!("expected inert violation, got {other:?}"),
        }
    }

    #[test]
    fn refusal_is_vacuously_verified_but_must_not_mutate() {
        let s = state(vec![false, true]);
        let refused = DdaStep::refused(DdaOp::Lift, "no non-destruction witness");
        assert!(verify_step(&refused, &s, &s.clone()).is_ok());
        let moved = state(vec![false, false]);
        assert!(matches!(
            verify_step(&refused, &s, &moved),
            Err(OpViolation::InertOpMutatedState { .. })
        ));
    }


    #[test]
    fn terminalizing_an_open_residual_is_rejected() {
        let s = state(vec![false, true]);
        assert_eq!(s.diagnose().unwrap().classification, DegreeTrichotomy::Open);
        let step = DdaStep::executed(DdaOp::Terminalize, "sealing anyway");
        match verify_step(&step, &s, &s.clone()) {
            Err(OpViolation::TerminalizedOpenResidual { gamma }) => assert!(gamma > 0),
            other => panic!("expected open-terminal violation, got {other:?}"),
        }
    }

    #[test]
    fn terminalizing_exact_is_allowed() {
        let s = state(vec![false, false]);
        let step = DdaStep::executed(DdaOp::Terminalize, "sealed");
        assert!(verify_step(&step, &s, &s.clone()).is_ok());
    }


    #[test]
    fn restructuring_op_that_restructures_nothing_is_rejected() {
        let s = state(vec![false, true]);
        for op in [DdaOp::ContextExposure, DdaOp::Descent, DdaOp::Lift] {
            let step = DdaStep::executed(op, "restructured (allegedly)");
            match verify_step(&step, &s, &s.clone()) {
                Err(OpViolation::CarrierUnchangedUnderRestructure { op: got }) => {
                    assert_eq!(got, op)
                }
                other => panic!("expected restructure violation for {op:?}, got {other:?}"),
            }
        }
    }


    #[test]
    fn verified_trace_threads_state_and_still_mints_nothing() {
        let mut vt = VerifiedTrace::new(state(vec![true, false]));
        vt.step(
            DdaStep::executed(DdaOp::ExactRepair, "discharge"),
            state(vec![false, false]),
        )
        .unwrap();
        vt.step_inert(DdaStep::executed(DdaOp::Integration, "receipt"))
            .unwrap();
        vt.step_inert(DdaStep::executed(DdaOp::Terminalize, "seal"))
            .unwrap();

        assert_eq!(vt.letters(), "E I T");
        assert_eq!(vt.evidence().len(), 3);
        assert_eq!(vt.evidence()[0].before.phi, 0);
        assert_eq!(vt.evidence()[0].after.phi, 0);
        assert_eq!(vt.authority_effect(), AuthorityEffect::None);
        assert_eq!(vt.control(), ControlStatus::Terminalized);
    }

    #[test]
    fn verified_trace_rejects_the_lie_and_leaves_state_untouched() {
        let mut vt = VerifiedTrace::new(state(vec![true, false]));
        let err = vt
            .step(
                DdaStep::executed(DdaOp::ExactRepair, "trust me"),
                state(vec![true, false]),
            )
            .unwrap_err();
        assert!(matches!(err, OpViolation::ExactRepairLeftDefect));
        assert_eq!(vt.letters(), "");
        assert_eq!(vt.state().residual, vec![true, false]);
    }
}
