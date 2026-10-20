
use num_bigint::BigInt;
use num_rational::BigRational;
use omega_contracts::mub_domain_ownership::{
    CANONICAL_MUB_DOMAIN_OWNER_V1, MUB_OWNERSHIP_CONTRACT_ID_V1,
};
use omega_functional::gamma2::{ExactCochainComplexQ, ExactGamma2Error};
use omega_functional::phi1::ExactPhi1Certificate;
use omega_homotopy_type_theory::primitive_difference::PrimitiveDifference;
use omega_policy::trichotomy::ObstructionDiagnosticClass;
pub use omega_state::CodaTerminal;
use omega_types::authority::AuthorityEffect;
use omega_wdp::coda::coda_gtla::{
    bind_domain_evidence, evaluate_exact, validate_primitive_difference, CodaExactInput,
    CodaGtlaEvaluation, CodaGtlaEvaluationError, DomainEvidenceBindingError,
    PrimitiveDifferenceReceiptError,
};
use serde::{Deserialize, Serialize};

use crate::omega_native::exact::mub6_basis_extension_packet::{
    discharge_t0_with_vector_cover, Mub6OdpInstance,
};

const ADAPTER_NAMESPACE: &str = "omega_mub::mub6_runtime_adapter_v1";

#[derive(Debug, Clone, Copy, PartialEq, PartialOrd, Serialize, Deserialize)]
#[serde(tag = "kind", rename_all = "snake_case")]
pub enum Mub6RuntimeEvidenceV1 {
    FixedT0 { cover_discharged: bool },
    FloatingDiagnostic { objective: f64 },
}

#[derive(Debug, Clone, Copy, PartialEq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Mub6RuntimeRequestV1 {
    pub evidence: Mub6RuntimeEvidenceV1,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash, Serialize)]
#[serde(rename_all = "snake_case")]
enum Mub6CarrierPointV1 {
    CoverDischarged,
    ClosedFixedTriple,
    HostileClosureDefect,
}

impl Mub6CarrierPointV1 {
    const ALL: [Self; 3] = [
        Self::CoverDischarged,
        Self::ClosedFixedTriple,
        Self::HostileClosureDefect,
    ];
}

#[derive(Debug, Clone, Copy)]
struct Mub6CarrierDifferenceV1;

impl PrimitiveDifference for Mub6CarrierDifferenceV1 {
    type Carrier = Mub6CarrierPointV1;
    type Diff = bool;

    fn delta(&self, x: &Self::Carrier, y: &Self::Carrier) -> Self::Diff {
        x != y
    }

    fn zero(&self, difference: &Self::Diff) -> bool {
        !difference
    }
}

#[derive(Debug, thiserror::Error)]
pub enum Mub6RuntimeAdapterError {
    #[error("malformed MUB6 runtime request: {0}")]
    Malformed(serde_json::Error),
    #[error("floating MUB evidence cannot enter the exact runtime")]
    FloatingEvidenceRefused,
    #[error("canonical MUB6 replay failed")]
    ReplayFailed,
    #[error("canonical MUB6 cover could not be replayed: {0}")]
    Cover(String),
    #[error("MUB6 manifest serialization failed: {0}")]
    Manifest(serde_json::Error),
    #[error(transparent)]
    Binding(#[from] DomainEvidenceBindingError),
    #[error(transparent)]
    Primitive(#[from] PrimitiveDifferenceReceiptError),
    #[error(transparent)]
    Complex(#[from] ExactGamma2Error),
    #[error(transparent)]
    Evaluation(#[from] CodaGtlaEvaluationError),
}

impl Mub6RuntimeAdapterError {
    pub fn terminal(&self) -> CodaTerminal {
        match self {
            Self::Malformed(_) | Self::FloatingEvidenceRefused => CodaTerminal::Refused,
            Self::Cover(_) => CodaTerminal::InfrastructureFailure,
            Self::ReplayFailed
            | Self::Manifest(_)
            | Self::Binding(_)
            | Self::Primitive(_)
            | Self::Complex(_)
            | Self::Evaluation(_) => CodaTerminal::Invalid,
        }
    }
}

#[derive(Debug)]
pub struct Mub6RuntimeEvaluationV1 {
    case: Mub6CarrierPointV1,
    tuple_hash: String,
    replay_hash: String,
    terminal: CodaTerminal,
    authority_effect: AuthorityEffect,
    evaluation: CodaGtlaEvaluation,
}

impl Mub6RuntimeEvaluationV1 {
    pub fn terminal(&self) -> CodaTerminal {
        self.terminal
    }

    pub fn authority_effect(&self) -> &AuthorityEffect {
        &self.authority_effect
    }

    pub fn tuple_hash(&self) -> &str {
        &self.tuple_hash
    }

    pub fn replay_hash(&self) -> &str {
        &self.replay_hash
    }

    pub fn evaluation(&self) -> &CodaGtlaEvaluation {
        &self.evaluation
    }

    pub fn cover_discharged(&self) -> bool {
        self.case == Mub6CarrierPointV1::CoverDischarged
    }
}

fn rational(value: i64) -> BigRational {
    BigRational::from_integer(BigInt::from(value))
}

fn exact_evidence(
    case: Mub6CarrierPointV1,
) -> Result<(ExactPhi1Certificate, ExactCochainComplexQ, Vec<BigRational>), ExactGamma2Error> {
    let d0 = vec![vec![rational(1)], vec![rational(1)], vec![rational(0)]];
    let (omega, alpha, residual, dual, reported, d1) = match case {
        Mub6CarrierPointV1::CoverDischarged => (
            vec![rational(1), rational(1), rational(0)],
            vec![rational(1)],
            vec![rational(0), rational(0), rational(0)],
            vec![rational(0), rational(0), rational(0)],
            rational(0),
            vec![vec![rational(1), rational(-1), rational(0)]],
        ),
        Mub6CarrierPointV1::ClosedFixedTriple => (
            vec![rational(0), rational(0), rational(1)],
            vec![rational(0)],
            vec![rational(0), rational(0), rational(1)],
            vec![rational(0), rational(0), rational(1)],
            rational(1),
            vec![vec![rational(1), rational(-1), rational(0)]],
        ),
        Mub6CarrierPointV1::HostileClosureDefect => (
            vec![rational(0), rational(0), rational(1)],
            vec![rational(0)],
            vec![rational(0), rational(0), rational(1)],
            vec![rational(0), rational(0), rational(1)],
            rational(1),
            vec![vec![rational(0), rational(0), rational(1)]],
        ),
    };
    let certificate = ExactPhi1Certificate {
        omega,
        d0: d0.clone(),
        weights: vec![rational(1); 3],
        alpha,
        primal_residual: residual.clone(),
        dual_witness: dual,
        reported_value: reported,
    };
    let complex = ExactCochainComplexQ::try_new(1, 3, 1, d0, d1)?;
    Ok((certificate, complex, residual))
}

fn terminal_for(class: ObstructionDiagnosticClass) -> CodaTerminal {
    match class {
        ObstructionDiagnosticClass::ExactRepair => CodaTerminal::ExactRepair,
        ObstructionDiagnosticClass::ClosedResidual => CodaTerminal::StabilizedSurvivor,
        ObstructionDiagnosticClass::ActiveClosureFailure => CodaTerminal::OpenObstruction,
    }
}

fn instantiate_replayed_case(
    case: Mub6CarrierPointV1,
) -> Result<Mub6OdpInstance, Mub6RuntimeAdapterError> {
    let instance = match case {
        Mub6CarrierPointV1::CoverDischarged => {
            discharge_t0_with_vector_cover()
                .map_err(Mub6RuntimeAdapterError::Cover)?
                .instance
        }
        Mub6CarrierPointV1::ClosedFixedTriple | Mub6CarrierPointV1::HostileClosureDefect => {
            Mub6OdpInstance::instantiate_t0("s16-003-mub6-t0-runtime")
        }
    };
    if !instance.replay().ok {
        return Err(Mub6RuntimeAdapterError::ReplayFailed);
    }
    Ok(instance)
}

fn serialize_case_manifests(
    case: Mub6CarrierPointV1,
    instance: &Mub6OdpInstance,
    certificate: &ExactPhi1Certificate,
    complex: &ExactCochainComplexQ,
    residual: &[BigRational],
) -> Result<(Vec<u8>, Vec<u8>), Mub6RuntimeAdapterError> {
    let carrier_manifest = serde_json::to_vec(&(
        MUB_OWNERSHIP_CONTRACT_ID_V1,
        CANONICAL_MUB_DOMAIN_OWNER_V1,
        instance.dimension,
        instance.fixed_vector_count,
        instance.basis_count,
        &instance.tuple_hash,
        instance.field_model,
        instance.residual_definition_id,
    ))
    .map_err(Mub6RuntimeAdapterError::Manifest)?;
    let evidence_manifest = serde_json::to_vec(&(
        case,
        certificate,
        complex,
        residual,
        &instance.replay_hash,
    ))
    .map_err(Mub6RuntimeAdapterError::Manifest)?;
    Ok((carrier_manifest, evidence_manifest))
}

fn evaluate_exact_case(
    case: Mub6CarrierPointV1,
) -> Result<Mub6RuntimeEvaluationV1, Mub6RuntimeAdapterError> {
    let instance = instantiate_replayed_case(case)?;
    let (certificate, complex, residual) = exact_evidence(case)?;
    let (carrier_manifest, evidence_manifest) =
        serialize_case_manifests(case, &instance, &certificate, &complex, &residual)?;
    let binding = bind_domain_evidence(ADAPTER_NAMESPACE, &carrier_manifest, &evidence_manifest)?;
    let primitive_receipt = validate_primitive_difference(
        &Mub6CarrierDifferenceV1,
        Mub6CarrierPointV1::ALL.to_vec(),
        binding.carrier_hash().clone(),
    )?;
    let evaluation = evaluate_exact(CodaExactInput::new(
        primitive_receipt,
        certificate,
        complex,
        residual,
        binding.into_packet_args(),
    ))?;
    let terminal = terminal_for(evaluation.status());

    Ok(Mub6RuntimeEvaluationV1 {
        case,
        tuple_hash: instance.tuple_hash,
        replay_hash: instance.replay_hash,
        terminal,
        authority_effect: AuthorityEffect::None,
        evaluation,
    })
}

pub fn evaluate_mub6_request(
    request: Mub6RuntimeRequestV1,
) -> Result<Mub6RuntimeEvaluationV1, Mub6RuntimeAdapterError> {
    match request.evidence {
        Mub6RuntimeEvidenceV1::FixedT0 { cover_discharged } => {
            evaluate_exact_case(if cover_discharged {
                Mub6CarrierPointV1::CoverDischarged
            } else {
                Mub6CarrierPointV1::ClosedFixedTriple
            })
        }
        Mub6RuntimeEvidenceV1::FloatingDiagnostic { .. } => {
            Err(Mub6RuntimeAdapterError::FloatingEvidenceRefused)
        }
    }
}

pub fn evaluate_mub6_json(
    bytes: &[u8],
) -> Result<Mub6RuntimeEvaluationV1, Mub6RuntimeAdapterError> {
    let request = serde_json::from_slice(bytes).map_err(Mub6RuntimeAdapterError::Malformed)?;
    evaluate_mub6_request(request)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn hostile_exact_closure_fixture_routes_open_without_authority() {
        let result = evaluate_exact_case(Mub6CarrierPointV1::HostileClosureDefect).unwrap();
        assert_eq!(result.terminal(), CodaTerminal::OpenObstruction);
        assert!(result.authority_effect().is_none());
        assert_eq!(
            result.evaluation().status(),
            ObstructionDiagnosticClass::ActiveClosureFailure
        );
    }
}
