
use serde::{Deserialize, Serialize};

use crate::epk_engine::GluingDefect;
use omega_types::authority::AuthorityEffect;
use omega_types::ceiling::EvidenceCeiling;

use crate::adequacy::{
    DetectorAdequacyVerdict, DetectorAdequacyVerdictKind, DetectorStructuralFailure,
    DetectorUndeclaredReason,
};

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub enum EvaluatorProvenance {
    Exhibited,
    OracleExtracted,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, PartialOrd, Ord, Serialize, Deserialize)]
pub enum GreenUnsoundReason {
    AdequacyUndeclared,
    CapacityEvidenceMissing,
    AlignedValidatorFamily,
    ConstantEvaluator,
    ConstantLocalProduct,
    NoNegativeDefectWitness,
    NoLocalGreenGlobalRedWitness,
    VacuousCarrierClosure,
    EvaluatorDoesNotSeparate,
    ProjectionCollision,
    BlindSpotsUndeclared,
    OtherStructuralInadequacy,
    CapacityCounterevidence,
    CapacityUnresolved,
}

impl GreenUnsoundReason {
    fn from_structural(failure: &DetectorStructuralFailure) -> Self {
        match failure {
            DetectorStructuralFailure::GlobalEqualsLocalProduct => Self::AlignedValidatorFamily,
            DetectorStructuralFailure::EvaluatorConstant { .. } => Self::ConstantEvaluator,
            DetectorStructuralFailure::LocalProductConstant => Self::ConstantLocalProduct,
            DetectorStructuralFailure::MissingNgdWitness => Self::NoNegativeDefectWitness,
            DetectorStructuralFailure::MissingLrgrWitness => Self::NoLocalGreenGlobalRedWitness,
            DetectorStructuralFailure::CarrierClosureVacuous => Self::VacuousCarrierClosure,
            DetectorStructuralFailure::EvaluatorDoesNotSeparate { .. } => {
                Self::EvaluatorDoesNotSeparate
            }
            DetectorStructuralFailure::ProjectionCollision { .. } => Self::ProjectionCollision,
            DetectorStructuralFailure::MissingBlindSpotDeclaration { .. } => {
                Self::BlindSpotsUndeclared
            }
            _ => Self::OtherStructuralInadequacy,
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum LggrVerdictError {
    #[error("evaluator gluing defect out of range: delta_eval = {0}, expected -1, 0, or +1")]
    DefectOutOfRange(i8),
    #[error(
        "malformed gluing defect: delta_eval = {delta_eval} but global_pass = {global_pass} and \
         local_product = {local_product} imply {implied}"
    )]
    DefectInternallyInconsistent {
        delta_eval: i8,
        global_pass: bool,
        local_product: bool,
        implied: i8,
    },
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum LggrVerdict {
    Red { defect: GluingDefect },
    PositiveGluingDefect { defect: GluingDefect },
    GreenOracleNeeded {
        defect: GluingDefect,
        reasons: Vec<GreenUnsoundReason>,
    },
    GreenNumericallySupported { defect: GluingDefect },
    OracleExtractedUnsound { defect: GluingDefect },
}

impl LggrVerdict {
    pub fn authority_effect(&self) -> AuthorityEffect {
        AuthorityEffect::None
    }

    pub fn evidence_ceiling(&self) -> EvidenceCeiling {
        let raw = match self {
            Self::Red { .. } | Self::PositiveGluingDefect { .. } => {
                EvidenceCeiling::BoundaryChecked
            }
            Self::GreenNumericallySupported { .. } => EvidenceCeiling::LocalReplay,
            Self::GreenOracleNeeded { .. } | Self::OracleExtractedUnsound { .. } => {
                EvidenceCeiling::ShapeOnly
            }
        };
        raw.meet(EvidenceCeiling::BoundaryChecked)
    }

    pub fn is_sound_detection(&self) -> bool {
        matches!(self, Self::Red { .. })
    }

    pub fn certifies_closure(&self) -> bool {
        false
    }

    pub fn defect(&self) -> &GluingDefect {
        match self {
            Self::Red { defect }
            | Self::PositiveGluingDefect { defect }
            | Self::GreenOracleNeeded { defect, .. }
            | Self::GreenNumericallySupported { defect }
            | Self::OracleExtractedUnsound { defect } => defect,
        }
    }
}

fn green_unsound_reasons(adequacy: &DetectorAdequacyVerdict) -> Vec<GreenUnsoundReason> {
    let mut reasons: Vec<GreenUnsoundReason> = match adequacy.kind() {
        DetectorAdequacyVerdictKind::NumericallySupported => Vec::new(),
        DetectorAdequacyVerdictKind::Undeclared => {
            vec![match adequacy.undeclared_reason() {
                Some(DetectorUndeclaredReason::CapacityEvidenceMissing) => {
                    GreenUnsoundReason::CapacityEvidenceMissing
                }
                _ => GreenUnsoundReason::AdequacyUndeclared,
            }]
        }
        DetectorAdequacyVerdictKind::StructuralInadequate => {
            let projected: Vec<GreenUnsoundReason> = adequacy
                .structural_failures()
                .iter()
                .map(GreenUnsoundReason::from_structural)
                .collect();
            if projected.is_empty() {
                vec![GreenUnsoundReason::OtherStructuralInadequacy]
            } else {
                projected
            }
        }
        DetectorAdequacyVerdictKind::NumericalCounterevidence => {
            vec![GreenUnsoundReason::CapacityCounterevidence]
        }
        DetectorAdequacyVerdictKind::NumericalUnresolved => {
            vec![GreenUnsoundReason::CapacityUnresolved]
        }
    };
    reasons.sort_unstable();
    reasons.dedup();
    reasons
}

pub fn classify(
    defect: &GluingDefect,
    adequacy: Option<&DetectorAdequacyVerdict>,
    provenance: EvaluatorProvenance,
) -> Result<LggrVerdict, LggrVerdictError> {
    let implied = defect.global_pass as i8 - defect.local_product as i8;
    if !matches!(defect.delta_eval, -1..=1) {
        return Err(LggrVerdictError::DefectOutOfRange(defect.delta_eval));
    }
    if defect.delta_eval != implied {
        return Err(LggrVerdictError::DefectInternallyInconsistent {
            delta_eval: defect.delta_eval,
            global_pass: defect.global_pass,
            local_product: defect.local_product,
            implied,
        });
    }

    if provenance == EvaluatorProvenance::OracleExtracted {
        return Ok(LggrVerdict::OracleExtractedUnsound { defect: *defect });
    }

    match defect.delta_eval {
        -1 => Ok(LggrVerdict::Red { defect: *defect }),
        1 => Ok(LggrVerdict::PositiveGluingDefect { defect: *defect }),
        _ => {
            let reasons = match adequacy {
                None => vec![GreenUnsoundReason::AdequacyUndeclared],
                Some(verdict) => green_unsound_reasons(verdict),
            };
            if reasons.is_empty() {
                Ok(LggrVerdict::GreenNumericallySupported { defect: *defect })
            } else {
                Ok(LggrVerdict::GreenOracleNeeded {
                    defect: *defect,
                    reasons,
                })
            }
        }
    }
}
