
use omega_types::authority::AuthorityEffect;
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash, Serialize, Deserialize)]
pub enum DdcOp {
    ExactRepair,
    ResidualProjection,
    ContextExposure,
    Integration,
    Lift,
    Descent,
    Refusal,
    Terminalize,
}

pub type DdaOp = DdcOp;

impl DdcOp {
    pub fn letter(self) -> &'static str {
        match self {
            DdcOp::ExactRepair => "E",
            DdcOp::ResidualProjection => "R",
            DdcOp::ContextExposure => "C",
            DdcOp::Integration => "I",
            DdcOp::Lift => "Λ",
            DdcOp::Descent => "D",
            DdcOp::Refusal => "M",
            DdcOp::Terminalize => "T",
        }
    }

    pub fn from_letter(s: &str) -> Option<DdcOp> {
        match s {
            "E" => Some(DdcOp::ExactRepair),
            "R" => Some(DdcOp::ResidualProjection),
            "C" => Some(DdcOp::ContextExposure),
            "I" => Some(DdcOp::Integration),
            "Λ" | "\\Lambda" | "Lambda" | "Meta" => Some(DdcOp::Lift),
            "D" => Some(DdcOp::Descent),
            "M" => Some(DdcOp::Refusal),
            "T" => Some(DdcOp::Terminalize),
            _ => None,
        }
    }

    pub fn alphabet() -> [DdcOp; 8] {
        [
            DdcOp::ExactRepair,
            DdcOp::ResidualProjection,
            DdcOp::ContextExposure,
            DdcOp::Integration,
            DdcOp::Lift,
            DdcOp::Descent,
            DdcOp::Refusal,
            DdcOp::Terminalize,
        ]
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash, Serialize, Deserialize)]
pub enum RefusalReason {
    #[serde(rename = "REFUSED_INVALID_WITNESS")]
    RefusedInvalidWitness,
    #[serde(rename = "REFUSED_BUDGET_EXHAUSTED")]
    RefusedBudgetExhausted,
    #[serde(rename = "REFUSED_NON_ZERO_CURL")]
    RefusedNonZeroCurl,
    #[serde(rename = "REFUSED_UNLICENSED_LIFT")]
    RefusedUnlicensedLift,
    #[serde(rename = "REFUSED_LIFT_TRIGGER")]
    RefusedLiftTrigger,
    #[serde(rename = "REFUSED_MISSING_LOSS_LEDGER")]
    RefusedMissingLossLedger,
    #[serde(rename = "REFUSED_MISSING_RECEIPT")]
    RefusedMissingReceipt,
    #[serde(rename = "REFUSED_REQUIRES_LIFT")]
    RefusedRequiresLift,
    #[serde(rename = "REFUSED_DETECTOR_INADEQUATE")]
    RefusedDetectorInadequate,
    #[serde(rename = "REFUSED_OPEN_OBSTRUCTION")]
    RefusedOpenObstruction,
}

impl RefusalReason {
    pub fn as_str(self) -> &'static str {
        match self {
            RefusalReason::RefusedInvalidWitness => "REFUSED_INVALID_WITNESS",
            RefusalReason::RefusedBudgetExhausted => "REFUSED_BUDGET_EXHAUSTED",
            RefusalReason::RefusedNonZeroCurl => "REFUSED_NON_ZERO_CURL",
            RefusalReason::RefusedUnlicensedLift => "REFUSED_UNLICENSED_LIFT",
            RefusalReason::RefusedLiftTrigger => "REFUSED_LIFT_TRIGGER",
            RefusalReason::RefusedMissingLossLedger => "REFUSED_MISSING_LOSS_LEDGER",
            RefusalReason::RefusedMissingReceipt => "REFUSED_MISSING_RECEIPT",
            RefusalReason::RefusedRequiresLift => "REFUSED_REQUIRES_LIFT",
            RefusalReason::RefusedDetectorInadequate => "REFUSED_DETECTOR_INADEQUATE",
            RefusalReason::RefusedOpenObstruction => "REFUSED_OPEN_OBSTRUCTION",
        }
    }

    pub fn from_str_code(s: &str) -> Option<Self> {
        match s {
            "REFUSED_INVALID_WITNESS" => Some(RefusalReason::RefusedInvalidWitness),
            "REFUSED_BUDGET_EXHAUSTED" => Some(RefusalReason::RefusedBudgetExhausted),
            "REFUSED_NON_ZERO_CURL" => Some(RefusalReason::RefusedNonZeroCurl),
            "REFUSED_UNLICENSED_LIFT" => Some(RefusalReason::RefusedUnlicensedLift),
            "REFUSED_LIFT_TRIGGER" => Some(RefusalReason::RefusedLiftTrigger),
            "REFUSED_MISSING_LOSS_LEDGER" => Some(RefusalReason::RefusedMissingLossLedger),
            "REFUSED_MISSING_RECEIPT" => Some(RefusalReason::RefusedMissingReceipt),
            "REFUSED_REQUIRES_LIFT" => Some(RefusalReason::RefusedRequiresLift),
            "REFUSED_DETECTOR_INADEQUATE" => Some(RefusalReason::RefusedDetectorInadequate),
            "REFUSED_OPEN_OBSTRUCTION" => Some(RefusalReason::RefusedOpenObstruction),
            _ => None,
        }
    }
}

impl std::fmt::Display for RefusalReason {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.write_str(self.as_str())
    }
}

impl From<&str> for RefusalReason {
    fn from(s: &str) -> Self {
        if let Some(r) = Self::from_str_code(s) {
            return r;
        }
        let lower = s.to_lowercase();
        if lower.contains("lift") {
            Self::RefusedUnlicensedLift
        } else if lower.contains("budget") {
            Self::RefusedBudgetExhausted
        } else if lower.contains("curl") || lower.contains("exact") {
            Self::RefusedNonZeroCurl
        } else if lower.contains("ledger") || lower.contains("loss") {
            Self::RefusedMissingLossLedger
        } else if lower.contains("receipt") {
            Self::RefusedMissingReceipt
        } else if lower.contains("detector")
            || lower.contains("inadequate")
            || lower.contains("blind")
        {
            Self::RefusedDetectorInadequate
        } else if lower.contains("open") || lower.contains("obstruction") {
            Self::RefusedOpenObstruction
        } else {
            Self::RefusedInvalidWitness
        }
    }
}

impl From<String> for RefusalReason {
    fn from(s: String) -> Self {
        Self::from(s.as_str())
    }
}

impl From<&String> for RefusalReason {
    fn from(s: &String) -> Self {
        Self::from(s.as_str())
    }
}

#[derive(Debug, Clone, PartialEq, Eq, PartialOrd, Ord, Hash, Serialize, Deserialize)]
pub enum StepOutcome {
    Executed { log: String },
    RefusedToExecute { reason: RefusalReason },
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct DdcStep {
    pub op: DdcOp,
    pub outcome: StepOutcome,
}

pub type DdaStep = DdcStep;

impl DdcStep {
    pub fn executed(op: DdcOp, log: impl Into<String>) -> Self {
        Self {
            op,
            outcome: StepOutcome::Executed { log: log.into() },
        }
    }

    pub fn refused(op: DdcOp, reason: impl Into<RefusalReason>) -> Self {
        Self {
            op,
            outcome: StepOutcome::RefusedToExecute {
                reason: reason.into(),
            },
        }
    }

    pub fn is_executed(&self) -> bool {
        matches!(self.outcome, StepOutcome::Executed { .. })
    }
}

#[derive(Debug, Clone, PartialEq, Eq, PartialOrd, Ord, Hash, Serialize, Deserialize)]
pub enum TraceTerminal {
    Open,
    Terminalized,
    UnverifiedTerminal,
    Refused,
    OracleNeeded { import: String },
}

#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize)]
pub struct DdcTrace {
    steps: Vec<DdcStep>,
    oracle: Option<String>,
    gated_terminal: bool,
}

pub type DdaTrace = DdcTrace;

impl DdcTrace {
    pub fn new() -> Self {
        Self {
            steps: Vec::new(),
            oracle: None,
            gated_terminal: false,
        }
    }

    pub fn emit(&mut self, step: DdcStep) -> &mut Self {
        self.steps.push(step);
        self
    }

    pub fn emit_gated_terminal(&mut self, step: DdcStep) -> &mut Self {
        self.gated_terminal = true;
        self.steps.push(step);
        self
    }

    pub fn import(&mut self, what: impl Into<String>) -> &mut Self {
        self.oracle = Some(what.into());
        self
    }

    pub fn steps(&self) -> &[DdcStep] {
        &self.steps
    }

    pub fn letters(&self) -> String {
        self.steps
            .iter()
            .map(|s| s.op.letter())
            .collect::<Vec<_>>()
            .join(" ")
    }

    pub fn terminal(&self) -> TraceTerminal {
        if let Some(import) = &self.oracle {
            return TraceTerminal::OracleNeeded {
                import: import.clone(),
            };
        }
        for step in self.steps.iter().rev() {
            match (step.op, step.is_executed()) {
                (DdcOp::Terminalize, true) => {
                    if self.gated_terminal {
                        return TraceTerminal::Terminalized;
                    } else {
                        return TraceTerminal::UnverifiedTerminal;
                    }
                }
                (DdcOp::Refusal, true) => return TraceTerminal::Refused,
                _ => {}
            }
        }
        TraceTerminal::Open
    }

    pub fn authority_effect(&self) -> AuthorityEffect {
        AuthorityEffect::None
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn alphabet_is_the_eight_spine_letters() {
        let letters: Vec<&str> = DdcOp::alphabet().iter().map(|o| o.letter()).collect();
        assert_eq!(letters, ["E", "R", "C", "I", "Λ", "D", "M", "T"]);
    }

    #[test]
    fn ddc_every_step_carries_log_or_refusal() {
        let e = DdcStep::executed(DdcOp::ExactRepair, "discharged defect on e_3");
        let m = DdcStep::refused(DdcOp::Lift, "no non-destruction witness");
        assert!(e.is_executed());
        assert!(!m.is_executed());
        match m.outcome {
            StepOutcome::RefusedToExecute { reason } => {
                assert_eq!(reason, RefusalReason::RefusedInvalidWitness);
            }
            _ => panic!("expected refusal"),
        }
    }

    #[test]
    fn trace_records_letters_in_order() {
        let mut t = DdcTrace::new();
        t.emit(DdcStep::executed(
            DdcOp::ContextExposure,
            "carrier declared",
        ))
        .emit(DdcStep::executed(DdcOp::ExactRepair, "antiderivative"))
        .emit(DdcStep::executed(DdcOp::Descent, "refine P_n -> P_2n"));
        assert_eq!(t.letters(), "C E D");
        assert_eq!(t.terminal(), TraceTerminal::Open);
    }

    #[test]
    fn terminalize_sets_terminalized() {
        let mut t = DdcTrace::new();
        t.emit_gated_terminal(DdcStep::executed(DdcOp::Terminalize, "sealed 1000/3"));
        assert_eq!(t.terminal(), TraceTerminal::Terminalized);
    }

    #[test]
    fn raw_terminalize_yields_unverified_terminal() {
        let mut t = DdcTrace::new();
        t.emit(DdcStep::executed(DdcOp::Terminalize, "sealed 1000/3"));
        assert_eq!(t.terminal(), TraceTerminal::UnverifiedTerminal);
    }

    #[test]
    fn typed_refusal_is_a_valid_terminal() {
        let mut t = DdcTrace::new();
        t.emit(DdcStep::executed(
            DdcOp::Refusal,
            "Dirichlet: debt #4 unpayable",
        ));
        assert_eq!(t.terminal(), TraceTerminal::Refused);
    }

    #[test]
    fn refused_terminalize_does_not_terminalize() {
        let mut t = DdcTrace::new();
        t.emit(DdcStep::refused(DdcOp::Terminalize, "no witness support"));
        assert_eq!(t.terminal(), TraceTerminal::Open);
    }

    #[test]
    fn ddc_import_forces_oracle_needed() {
        let mut t = DdcTrace::new();
        t.emit(DdcStep::executed(DdcOp::ContextExposure, "window"))
            .import("Gleason's theorem");
        match t.terminal() {
            TraceTerminal::OracleNeeded { import } => assert_eq!(import, "Gleason's theorem"),
            other => panic!("expected OracleNeeded, got {other:?}"),
        }
    }

    #[test]
    fn ddc_oracle_cannot_be_terminalized_away() {
        let mut t = DdcTrace::new();
        t.import("continuum path integral")
            .emit_gated_terminal(DdcStep::executed(DdcOp::Terminalize, "claiming a seal"));
        assert!(matches!(t.terminal(), TraceTerminal::OracleNeeded { .. }));
    }

    #[test]
    fn ddc_no_trace_mints_authority() {
        let empty = DdcTrace::new();
        assert_eq!(empty.authority_effect(), AuthorityEffect::None);

        let mut sealed = DdcTrace::new();
        for op in DdcOp::alphabet() {
            if op == DdcOp::Terminalize {
                sealed.emit_gated_terminal(DdcStep::executed(op, "log"));
            } else {
                sealed.emit(DdcStep::executed(op, "log"));
            }
        }
        assert_eq!(sealed.terminal(), TraceTerminal::Terminalized);
        assert_eq!(
            sealed.authority_effect(),
            AuthorityEffect::None,
            "DDC No-Authority Firewall: a well-typed, fully terminalized trace still mints nothing"
        );
    }

    #[test]
    fn backward_compatibility_aliases_match() {
        let op: DdaOp = DdcOp::ExactRepair;
        let step: DdaStep = DdcStep::executed(op, "compat");
        let mut trace: DdaTrace = DdcTrace::new();
        trace.emit(step);
        assert_eq!(trace.letters(), "E");
    }
}
