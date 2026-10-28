
use engine_types::{
    AuthorityEffectLevel, ConvergenceCertificate, EvidenceCeiling, RefinementRelation,
    RefinementTower, ShadowKind, SpectralTopology, CONVERGENCE_CERTIFICATE_SCHEMA,
};
use serde::Serialize;
use thiserror::Error;

use super::{ContinuumDebt, QError, QPacket, QTerminal};

#[derive(Clone, Debug, PartialEq, Eq, Serialize)]
pub struct SpectralConvergenceBinding {
    bound_packet: QPacket,
    tower: RefinementTower,
    convergence_certificate: ConvergenceCertificate,
    continuum_debt: ContinuumDebt,
    evidence_ceiling: EvidenceCeiling,
    authority_effect: AuthorityEffectLevel,
}

impl SpectralConvergenceBinding {
    pub fn bound_packet(&self) -> &QPacket {
        &self.bound_packet
    }

    pub fn tower(&self) -> &RefinementTower {
        &self.tower
    }

    pub fn convergence_certificate(&self) -> &ConvergenceCertificate {
        &self.convergence_certificate
    }

    pub fn continuum_debt(&self) -> &ContinuumDebt {
        &self.continuum_debt
    }

    pub fn evidence_ceiling(&self) -> EvidenceCeiling {
        self.evidence_ceiling
    }

    pub fn authority_effect(&self) -> AuthorityEffectLevel {
        self.authority_effect
    }
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize)]
pub struct SpectralMembraneDecision {
    packet: QPacket,
    terminal: QTerminal,
    continuum_debt: ContinuumDebt,
    binding: Option<SpectralConvergenceBinding>,
    evidence_ceiling: EvidenceCeiling,
    authority_effect: AuthorityEffectLevel,
}

impl SpectralMembraneDecision {
    pub fn packet(&self) -> &QPacket {
        &self.packet
    }

    pub fn terminal(&self) -> QTerminal {
        self.terminal
    }

    pub fn continuum_debt(&self) -> &ContinuumDebt {
        &self.continuum_debt
    }

    pub fn binding(&self) -> Option<&SpectralConvergenceBinding> {
        self.binding.as_ref()
    }

    pub fn evidence_ceiling(&self) -> EvidenceCeiling {
        self.evidence_ceiling
    }

    pub fn authority_effect(&self) -> AuthorityEffectLevel {
        self.authority_effect
    }
}

#[derive(Clone, Debug, PartialEq, Eq, Error)]
pub enum SpectralMembraneError {
    #[error("invalid Q packet: {0}")]
    InvalidPacket(QError),
    #[error("certificate schema mismatch: expected {expected}, got {actual}")]
    CertificateSchemaMismatch {
        expected: &'static str,
        actual: String,
    },
    #[error("certificate family id mismatch: tower {tower}, certificate {certificate}")]
    FamilyIdMismatch { tower: String, certificate: String },
    #[error("certificate family kind mismatch: tower {tower:?}, certificate {certificate:?}")]
    FamilyKindMismatch {
        tower: ShadowKind,
        certificate: ShadowKind,
    },
    #[error("certificate topology mismatch: tower {tower:?}, certificate {certificate:?}")]
    TopologyMismatch {
        tower: SpectralTopology,
        certificate: SpectralTopology,
    },
    #[error("certificate tower digest mismatch: tower {tower}, certificate {certificate}")]
    TowerDigestMismatch { tower: String, certificate: String },
    #[error("convergence certificate attempted authority effect {actual:?}")]
    CertificateAuthorityMismatch { actual: AuthorityEffectLevel },
    #[error("internally rendered continuum debt is invalid: {0}")]
    RenderedDebtInvalid(QError),
}

#[derive(Clone, Copy, Debug, Default, PartialEq, Eq)]
pub struct SpectralMembrane;

impl SpectralMembrane {
    pub fn decide(
        packet: QPacket,
        tower: &RefinementTower,
        certificate: Option<&ConvergenceCertificate>,
    ) -> Result<SpectralMembraneDecision, SpectralMembraneError> {
        packet
            .validate_mandatory()
            .map_err(SpectralMembraneError::InvalidPacket)?;

        match certificate {
            None => Ok(SpectralMembraneDecision {
                packet,
                terminal: QTerminal::OracleNeeded,
                continuum_debt: render_continuum_debt(tower, None),
                binding: None,
                evidence_ceiling: EvidenceCeiling::ShapeOnly,
                authority_effect: AuthorityEffectLevel::None,
            }),
            Some(certificate) => {
                validate_binding_identity(tower, certificate)?;
                let continuum_debt = render_continuum_debt(tower, Some(certificate));
                continuum_debt
                    .validate_for_admission()
                    .map_err(SpectralMembraneError::RenderedDebtInvalid)?;
                let binding = SpectralConvergenceBinding {
                    bound_packet: packet.clone(),
                    tower: tower.clone(),
                    convergence_certificate: certificate.clone(),
                    continuum_debt: continuum_debt.clone(),
                    evidence_ceiling: EvidenceCeiling::ShapeOnly,
                    authority_effect: AuthorityEffectLevel::None,
                };

                Ok(SpectralMembraneDecision {
                    packet,
                    terminal: QTerminal::ConditionalSupport,
                    continuum_debt,
                    binding: Some(binding),
                    evidence_ceiling: EvidenceCeiling::ShapeOnly,
                    authority_effect: AuthorityEffectLevel::None,
                })
            }
        }
    }
}

fn validate_binding_identity(
    tower: &RefinementTower,
    certificate: &ConvergenceCertificate,
) -> Result<(), SpectralMembraneError> {
    if certificate.schema() != CONVERGENCE_CERTIFICATE_SCHEMA {
        return Err(SpectralMembraneError::CertificateSchemaMismatch {
            expected: CONVERGENCE_CERTIFICATE_SCHEMA,
            actual: certificate.schema().to_string(),
        });
    }
    if tower.family().id() != certificate.family_id() {
        return Err(SpectralMembraneError::FamilyIdMismatch {
            tower: tower.family().id().to_string(),
            certificate: certificate.family_id().to_string(),
        });
    }
    if tower.family().kind() != certificate.family_kind() {
        return Err(SpectralMembraneError::FamilyKindMismatch {
            tower: tower.family().kind(),
            certificate: certificate.family_kind(),
        });
    }
    if tower.family().topology() != certificate.topology() {
        return Err(SpectralMembraneError::TopologyMismatch {
            tower: tower.family().topology(),
            certificate: certificate.topology(),
        });
    }

    let tower_digest = tower.digest_sha256();
    if tower_digest != certificate.tower_digest_sha256() {
        return Err(SpectralMembraneError::TowerDigestMismatch {
            tower: tower_digest,
            certificate: certificate.tower_digest_sha256().to_string(),
        });
    }
    if certificate.authority_effect() != AuthorityEffectLevel::None {
        return Err(SpectralMembraneError::CertificateAuthorityMismatch {
            actual: certificate.authority_effect(),
        });
    }
    Ok(())
}

fn render_continuum_debt(
    tower: &RefinementTower,
    certificate: Option<&ConvergenceCertificate>,
) -> ContinuumDebt {
    let family = tower.family();
    let topology = topology_label(family.topology());
    let certificate_route = certificate.map(|certificate| {
        format!(
            "schema={};tower_digest_sha256={};family_id={};family_kind={};topology={};\
             mode_index={};receipt_kind={:?};source_binding_status={};source_binding_check={};theorems={}",
            certificate.schema(),
            certificate.tower_digest_sha256(),
            certificate.family_id(),
            shadow_kind_label(certificate.family_kind()),
            topology_label(certificate.topology()),
            certificate.mode_index(),
            certificate.theorem_receipt().kind(),
            certificate.theorem_receipt().source_binding_status(),
            certificate.theorem_receipt().replay_command(),
            certificate.theorem_receipt().theorem_names().join(","),
        )
    });
    let descent_trigger = certificate.map_or_else(
        || {
            format!(
                "supply typed ConvergenceCertificate for family_id={};then check its source bindings;\
                 native Lean replay remains a separate obligation",
                family.id(),
            )
        },
        |certificate| {
            format!(
                "check source bindings for ordered_finite_prefix mode_index={} with {};source_binding_status={}",
                certificate.mode_index(),
                certificate.theorem_receipt().replay_command(),
                certificate.theorem_receipt().source_binding_status(),
            )
        },
    );

    ContinuumDebt {
        finite_shadow: Some(format!(
            "family_id={};family_kind={};declared_object={};tower_digest_sha256={}",
            family.id(),
            shadow_kind_label(family.kind()),
            family.declared_object(),
            tower.digest_sha256(),
        )),
        refinement_relation: Some(refinement_relation_label(tower.relation()).to_string()),
        declared_topology: Some(topology.to_string()),
        convergence_certificate_route: certificate_route,
        descent_trigger: Some(descent_trigger),
    }
}

fn shadow_kind_label(kind: ShadowKind) -> &'static str {
    match kind {
        ShadowKind::UniformCycle => "uniform_cycle",
        ShadowKind::CellCenteredNeumannPath => "cell_centered_neumann_path",
        ShadowKind::PeriodicLumpedFiniteVolume => "periodic_lumped_finite_volume",
    }
}

fn refinement_relation_label(relation: RefinementRelation) -> &'static str {
    match relation {
        RefinementRelation::ExactUniformSubdivision => "exact_uniform_subdivision",
        RefinementRelation::CommonLimitComparison => "common_limit_comparison",
    }
}

fn topology_label(topology: SpectralTopology) -> &'static str {
    match topology {
        SpectralTopology::OrderedFinitePrefix => "ordered_finite_prefix",
    }
}
