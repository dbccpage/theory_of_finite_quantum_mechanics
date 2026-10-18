//! Declared observer, L1 evaluation profile, and exact rational constructors.

use num_traits::Zero;

use super::model::{EmpiricalModel, Scenario};
use super::{q, qr, AUTHORITY_EFFECT, EmpiricalError, Q};

/// The one admissibility class [`evaluate_l1_claim`] implements.
pub const ADMISSIBILITY_NONCONTEXTUAL: &str = "noncontextual polytope conv(A)";
/// The one norm [`evaluate_l1_claim`] implements.
pub const NORM_L1: &str = "L1";
/// The one layer [`evaluate_l1_claim`] reports at: the diagnostic layer of
/// `WDP-CH10-D01`. A receipt at any other layer is not this evaluator's.
pub const LAYER_DIAGNOSTIC: &str = "WDP-CH10-D01 diagnostic";

/// The five declared observer components: kernel, admissibility, norm,
/// terminal rule and layer. A receipt is issued only against a complete tuple
/// that [`ObserverTuple::l1_profile`] binds to the evaluator's own profile.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ObserverTuple {
    pub kernel: String,
    pub admissibility: String,
    pub norm: String,
    pub terminal: String,
    pub layer: String,
}

/// The kernel [`evaluate_l1_claim`] reads.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum KernelProfile {
    /// The support presheaf of the model over its maximal-context cover.
    SupportPresheafOverCover,
}

/// The admissibility class [`evaluate_l1_claim`] measures distance to.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum AdmissibilityProfile {
    /// `conv(A)`: the noncontextual polytope of the scenario.
    NoncontextualPolytope,
}

/// The norm [`evaluate_l1_claim`] computes.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum NormProfile {
    L1,
}

/// The terminal rule [`evaluate_l1_claim`] applies.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum TerminalProfile {
    /// [`TERMINAL_RULE_L1`].
    RuleL1,
}

/// The layer [`evaluate_l1_claim`] reports at.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum LayerProfile {
    /// The diagnostic layer of `WDP-CH10-D01`; no authority grade.
    Diagnostic,
}

/// The evaluation profile [`evaluate_l1_claim`] implements, built from a
/// declared tuple by exact match against the scenario under evaluation. The
/// evaluator computes nothing outside this profile, so a declaration outside
/// it is refused rather than copied into a receipt that computed something
/// else.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct L1EvaluationProfile {
    pub kernel: KernelProfile,
    pub admissibility: AdmissibilityProfile,
    pub norm: NormProfile,
    pub terminal: TerminalProfile,
    pub layer: LayerProfile,
}

impl ObserverTuple {
    /// Bind the declared tuple to the profile of [`evaluate_l1_claim`] on
    /// `scenario`. Each component must name the one choice the evaluator
    /// implements; the first that does not is refused by name.
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

/// A draft tuple; [`ObserverDraft::declare`] names the first missing
/// component. `None`, the empty string and whitespace are all undeclared, as
/// in the Python observer contract of the three-role gate.
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

/// Diagnostic terminal of an L1 evaluation, declared by the terminal rule
/// [`TERMINAL_RULE_L1`].
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum EvaluationStatus {
    /// Defect zero: the model lies in the admitted (noncontextual) polytope.
    ExactRepair,
    /// Positive defect, but a global section of the support presheaf exists.
    ClosedResidual,
    /// Positive defect and no global section of the support presheaf.
    OpenObstruction,
}

/// The terminal rule applied by [`evaluate_l1_claim`], spelled out so that a
/// receipt can quote it as its `terminal` component.
pub const TERMINAL_RULE_L1: &str = "defect = 0 -> ExactRepair; defect > 0 and a support-level global section exists -> ClosedResidual; defect > 0 and none exists -> OpenObstruction";

/// Executable receipt `(claim, defect, phi*, status)` under a declared
/// observer bound to the evaluator's profile.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct EvaluationReceipt {
    pub observer: ObserverTuple,
    /// The typed profile the declaration was bound to before arithmetic ran.
    pub profile: L1EvaluationProfile,
    pub claim: String,
    pub defect: Q,
    pub dual_witness: Vec<Q>,
    pub status: EvaluationStatus,
    pub authority_effect: &'static str,
}

/// Evaluate the L1 distance of a model from the noncontextual polytope under
/// a fully declared observer. An undeclared or blank component is refused,
/// then a component the evaluator does not implement is refused, both before
/// any arithmetic runs; the receipt always carries `AuthorityEffect: None`.
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

/// Convenience constructors for exact rationals in tests and callers.
pub fn rational(numerator: i64, denominator: i64) -> Result<Q, EmpiricalError> {
    if denominator == 0 {
        return Err(EmpiricalError::ZeroDenominator);
    }
    Ok(qr(numerator, denominator))
}

pub fn integer(value: i64) -> Q {
    q(value)
}
