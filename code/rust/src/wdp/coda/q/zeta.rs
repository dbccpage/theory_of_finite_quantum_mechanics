use serde::{Deserialize, Serialize};

use super::admission::{AdmissionDecision, QAdmissionGate, QAdmissionRequest};
use super::packet::{QPacket, QTerminal};
use omega_types::q_continuum::{ObstructionKind, Residual};

/// Zeta/RH claim family under the Q firewall.
#[derive(Clone, Copy, Debug, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub enum ZetaRhClaimKind {
    /// Ihara-zeta / graph-Weil analog: finite regular graph shadow and Ramanujan locus.
    IharaGraphRhAnalog,
    /// Classical Riemann Hypothesis for the Riemann zeta function zeta(s).
    ClassicalRiemannHypothesis,
}

/// Direction of the proposed transport between source and finite shadow.
#[derive(Clone, Copy, Debug, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub enum ZetaTransportDirection {
    /// Continuum/source material projects to a declared finite graph/Ihara shadow.
    SourceToShadow,
    /// A finite shadow is claimed to decode or prove its continuum/classical source.
    ShadowDecodesSource,
    /// Source claim appears without a declared finite bridge.
    SourceOnly,
}

/// One zeta/RH candidate routed through Q admission.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct ZetaRhCandidate {
    pub claim_kind: ZetaRhClaimKind,
    pub direction: ZetaTransportDirection,
    pub packet: QPacket,
    pub admission: QAdmissionRequest,
}

impl ZetaRhCandidate {
    pub fn new(
        claim_kind: ZetaRhClaimKind,
        direction: ZetaTransportDirection,
        packet: QPacket,
        admission: QAdmissionRequest,
    ) -> Self {
        Self {
            claim_kind,
            direction,
            packet,
            admission,
        }
    }
}

/// Zeta/RH firewall decision.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct ZetaRhDecision {
    pub admission: AdmissionDecision,
    pub crosses_to_gttc: bool,
}

/// Q firewall for graph/Ihara RH analogs versus classical RH claims.
#[derive(Clone, Copy, Debug, Default, PartialEq, Eq)]
pub struct ZetaRhFirewall;

impl ZetaRhFirewall {
    pub fn new() -> Self {
        Self
    }

    pub fn classify(&self, candidate: &ZetaRhCandidate) -> ZetaRhDecision {
        match (candidate.claim_kind, candidate.direction) {
            (ZetaRhClaimKind::ClassicalRiemannHypothesis, _) => self.refuse_classical_rh(candidate),
            (_, ZetaTransportDirection::ShadowDecodesSource) => {
                self.refuse_shadow_decoding(candidate)
            }
            (ZetaRhClaimKind::IharaGraphRhAnalog, _) => self.classify_graph_analog(candidate),
        }
    }

    fn classify_graph_analog(&self, candidate: &ZetaRhCandidate) -> ZetaRhDecision {
        let admission =
            QAdmissionGate::new().classify_admission(&candidate.packet, &candidate.admission);
        let crosses_to_gttc = candidate.direction == ZetaTransportDirection::SourceToShadow
            && admission.residual.is_none()
            && matches!(
                admission.terminal_status,
                QTerminal::QHeld | QTerminal::ConditionalSupport
            );

        ZetaRhDecision {
            admission,
            crosses_to_gttc,
        }
    }

    fn refuse_classical_rh(&self, candidate: &ZetaRhCandidate) -> ZetaRhDecision {
        ZetaRhDecision {
            admission: AdmissionDecision {
                candidate_id: candidate.admission.candidate_id.clone(),
                kind: candidate.admission.kind,
                terminal_status: QTerminal::Refused,
                obligations: vec![
                    "classical RH needs its own finite bridge; graph/Ihara shadow is not a proof route".to_string(),
                    "record refusal/residual instead of promoting tower zeta to zeta(s)".to_string(),
                ],
                residual: Some(Residual::new(
                    format!("residual:zeta:{}:classical-rh", candidate.admission.candidate_id),
                    candidate.admission.candidate_id.clone(),
                    ObstructionKind::NonFiniteProjection,
                    "classical Riemann Hypothesis claim is not admitted from an Ihara/graph zeta finite shadow",
                )),
            },
            crosses_to_gttc: false,
        }
    }

    fn refuse_shadow_decoding(&self, candidate: &ZetaRhCandidate) -> ZetaRhDecision {
        ZetaRhDecision {
            admission: AdmissionDecision {
                candidate_id: candidate.admission.candidate_id.clone(),
                kind: candidate.admission.kind,
                terminal_status: QTerminal::OpenResidual,
                obligations: vec![
                    "reverse the transport: source-to-shadow projection is allowed, shadow-to-source decoding is not".to_string(),
                    "supply an independent bridge if a source claim is intended".to_string(),
                ],
                residual: Some(Residual::new(
                    format!("residual:zeta:{}:direction", candidate.admission.candidate_id),
                    candidate.admission.candidate_id.clone(),
                    ObstructionKind::AnalogyBreak,
                    "finite zeta shadow forgets its source and cannot decode classical RH or the Q-held continuum source",
                )),
            },
            crosses_to_gttc: false,
        }
    }
}
