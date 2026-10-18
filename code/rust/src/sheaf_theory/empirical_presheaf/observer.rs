
use num_traits::Zero;

use super::model::{EmpiricalModel, Scenario};
use super::{q, qr, AUTHORITY_EFFECT, EmpiricalError, Q};

pub const ADMISSIBILITY_NONCONTEXTUAL: &str = "noncontextual polytope conv(A)";
pub const NORM_L1: &str = "L1";
pub const LAYER_DIAGNOSTIC: &str = "WDP-CH10-D01 diagnostic";

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ObserverTuple {
    pub kernel: String,
    pub admissibility: String,
    pub norm: String,
    pub terminal: String,
    pub layer: String,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum KernelProfile {
    SupportPresheafOverCover,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum AdmissibilityProfile {
    NoncontextualPolytope,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum NormProfile {
    L1,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum TerminalProfile {
    RuleL1,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum LayerProfile {
    Diagnostic,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct L1EvaluationProfile {
    pub kernel: KernelProfile,
    pub admissibility: AdmissibilityProfile,
    pub norm: NormProfile,
    pub terminal: TerminalProfile,
    pub layer: LayerProfile,
}

impl ObserverTuple {
    pub fn l1_profile(&self, scenario: &Scenario) -> Result<L1EvaluationProfile, EmpiricalError> {
        let unsupported = |component: &'static str, declared: &str| {
            EmpiricalError::UnsupportedObserverComponent {
                component,
                declared: declared.to_string(),
            }
        };
        if self.kernel != scenario.kernel_label() {
            return Err(unsupported("kernel", &self.kernel));
        }
        if self.admissibility != ADMISSIBILITY_NONCONTEXTUAL {
            return Err(unsupported("admissibility", &self.admissibility));
        }
        if self.norm != NORM_L1 {
            return Err(unsupported("norm", &self.norm));
        }
        if self.terminal != TERMINAL_RULE_L1 {
            return Err(unsupported("terminal", &self.terminal));
        }
        if self.layer != LAYER_DIAGNOSTIC {
            return Err(unsupported("layer", &self.layer));
        }
        Ok(L1EvaluationProfile {
            kernel: KernelProfile::SupportPresheafOverCover,
            admissibility: AdmissibilityProfile::NoncontextualPolytope,
            norm: NormProfile::L1,
            terminal: TerminalProfile::RuleL1,
            layer: LayerProfile::Diagnostic,
        })
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Default)]
pub struct ObserverDraft {
    pub kernel: Option<String>,
    pub admissibility: Option<String>,
    pub norm: Option<String>,
    pub terminal: Option<String>,
    pub layer: Option<String>,
}

impl ObserverDraft {
    pub fn declare(self) -> Result<ObserverTuple, EmpiricalError> {
        fn component(value: Option<String>, name: &'static str) -> Result<String, EmpiricalError> {
            match value {
                Some(text) if !text.trim().is_empty() => Ok(text),
                _ => Err(EmpiricalError::UndeclaredObserverComponent(name)),
            }
        }
        Ok(ObserverTuple {
            kernel: component(self.kernel, "kernel")?,
            admissibility: component(self.admissibility, "admissibility")?,
            norm: component(self.norm, "norm")?,
            terminal: component(self.terminal, "terminal")?,
            layer: component(self.layer, "layer")?,
        })
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum EvaluationStatus {
    ExactRepair,
    ClosedResidual,
    OpenObstruction,
}

pub const TERMINAL_RULE_L1: &str = "defect = 0 -> ExactRepair; defect > 0 and a support-level global section exists -> ClosedResidual; defect > 0 and none exists -> OpenObstruction";

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct EvaluationReceipt {
    pub observer: ObserverTuple,
    pub profile: L1EvaluationProfile,
    pub claim: String,
    pub defect: Q,
    pub dual_witness: Vec<Q>,
    pub status: EvaluationStatus,
    pub authority_effect: &'static str,
}

pub fn evaluate_l1_claim(
    observer: ObserverDraft,
    claim: &str,
    model: &EmpiricalModel,
    pivots: usize,
) -> Result<EvaluationReceipt, EmpiricalError> {
    let observer = observer.declare()?;
    let profile = observer.l1_profile(model.scenario())?;
    let receipt = model.l1_defect(pivots)?;
    let status = if receipt.defect.is_zero() {
        EvaluationStatus::ExactRepair
    } else if model.is_strongly_contextual()? {
        EvaluationStatus::OpenObstruction
    } else {
        EvaluationStatus::ClosedResidual
    };
    Ok(EvaluationReceipt {
        observer,
        profile,
        claim: claim.to_string(),
        defect: receipt.defect,
        dual_witness: receipt.dual_witness,
        status,
        authority_effect: AUTHORITY_EFFECT,
    })
}

pub fn rational(numerator: i64, denominator: i64) -> Result<Q, EmpiricalError> {
    if denominator == 0 {
        return Err(EmpiricalError::ZeroDenominator);
    }
    Ok(qr(numerator, denominator))
}

pub fn integer(value: i64) -> Q {
    q(value)
}
