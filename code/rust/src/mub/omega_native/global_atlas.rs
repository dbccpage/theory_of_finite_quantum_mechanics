//! Global MUB(6) atlas gate.
//!
//! This is the certificate shape needed to turn pinned-wall work into a full
//! MUB(6) no-go. Current receipts are audited as candidate sources, but none is
//! accepted as an exhaustive triple-class atlas.

use std::path::Path;

use serde::Serialize;
use serde_json::Value;

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Serialize)]
pub enum AtlasStatus {
    Certified,
    /// The declaration checklist is well formed. It is not verified evidence.
    DeclaredChecklist,
    MissingProofObligation,
    InvalidCertificate,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Serialize)]
pub enum CandidateCoverRole {
    PinnedSymmetryOrbit,
    ProjectorPolytopeScout,
    TransportClosureReceipt,
    Unknown,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Serialize)]
pub enum CandidateCoverVerdict {
    UsefulLocalEvidence,
    NumericalOnly,
    NotGlobalCover,
    Missing,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct CandidateCoverAudit {
    pub role: CandidateCoverRole,
    pub relative_path: &'static str,
    pub verdict: CandidateCoverVerdict,
    pub reason: &'static str,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct AtlasPatchCertificate {
    pub class_id: &'static str,
    pub representative: &'static str,
    pub transport_to_wall_lane: &'static str,
    pub wall_certificate: &'static str,
    pub loss_ledger_closed: bool,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct GlobalMub6AtlasCertificate {
    pub exhaustive_triple_cover: bool,
    pub class_count: usize,
    pub patches: Vec<AtlasPatchCertificate>,
    pub overlap_compatibility: bool,
    pub basis_gluing: bool,
    pub zero_rel_preserved: bool,
    pub terminalizer_preserved: bool,
}

/// The atlas obligations an assessment established, one flag per obligation.
///
/// `Certified` implies every flag; the flags let callers pass on exactly what
/// was established instead of fanning one status out to each obligation.
#[derive(Debug, Clone, Copy, Default, PartialEq, Eq, Serialize)]
pub struct GlobalAtlasEvidence {
    pub exhaustive_triple_cover: bool,
    pub wall_certificate_for_every_class: bool,
    pub overlap_compatibility: bool,
    pub basis_gluing: bool,
    pub zero_rel_preserved: bool,
    pub terminalizer_preserved: bool,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct GlobalAtlasAssessment {
    pub status: AtlasStatus,
    pub evidence: GlobalAtlasEvidence,
    pub accepted_patch_count: usize,
    pub candidate_sources: Vec<CandidateCoverAudit>,
    pub discharged_obligations: Vec<&'static str>,
    pub missing_obligations: Vec<&'static str>,
}

pub fn assess_current_global_atlas(crate_root: &Path) -> GlobalAtlasAssessment {
    let candidate_sources = vec![
        audit_stabilizer_orbit(crate_root),
        audit_projector_polytope_invariants(crate_root),
        audit_projector_polytope_symmetry_orbit(crate_root),
        audit_transport_closure(crate_root),
    ];

    GlobalAtlasAssessment {
        status: AtlasStatus::MissingProofObligation,
        evidence: GlobalAtlasEvidence::default(),
        accepted_patch_count: 0,
        candidate_sources,
        discharged_obligations: vec![],
        missing_obligations: vec![
            "proof-carrying exhaustive atlas of admissible MUB(6) triples",
            "one wall-certified transport patch for every atlas class",
            "patch-intersection compatibility for atlas patches",
            "basis-gluing theorem from classwise fourth-vector obstruction to no complete MUB(6)",
            "CODA-MUR loss ledger proving ZeroRel and terminalizer preservation across representation changes",
            "C3 atlas coherence object for cover completeness, commuting transport squares, wall-certificate transport, ZeroRel preservation, and terminalizer preservation",
        ],
    }
}

pub fn verify_global_mub6_atlas_certificate(
    certificate: &GlobalMub6AtlasCertificate,
) -> GlobalAtlasAssessment {
    let mut missing = Vec::new();
    if !certificate.exhaustive_triple_cover {
        missing.push("proof-carrying exhaustive atlas of admissible MUB(6) triples");
    }
    if certificate.class_count == 0 {
        missing.push("nonempty atlas class list");
    }
    let patch_for_every_class = certificate.patches.len() == certificate.class_count;
    if !patch_for_every_class {
        missing.push("one wall-certified transport patch for every atlas class");
    }
    let every_ledger_closed = certificate
        .patches
        .iter()
        .all(|patch| patch.loss_ledger_closed);
    if !every_ledger_closed {
        missing.push("closed loss ledger for every atlas transport patch");
    }
    if !certificate.overlap_compatibility {
        missing.push("patch-intersection compatibility for atlas patches");
    }
    if !certificate.basis_gluing {
        missing.push(
            "basis-gluing theorem from classwise fourth-vector obstruction to no complete MUB(6)",
        );
    }
    if !certificate.zero_rel_preserved {
        missing.push("ZeroRel preservation across all atlas transports");
    }
    if !certificate.terminalizer_preserved {
        missing.push("terminalizer preservation across all atlas transports");
    }
    let c3_coherent = certificate.exhaustive_triple_cover
        && certificate.class_count > 0
        && certificate.patches.len() == certificate.class_count
        && certificate
            .patches
            .iter()
            .all(|patch| patch.loss_ledger_closed)
        && certificate.overlap_compatibility
        && certificate.zero_rel_preserved
        && certificate.terminalizer_preserved;
    if !c3_coherent {
        missing.push("C3 atlas coherence object for cover completeness, commuting transport squares, wall-certificate transport, ZeroRel preservation, and terminalizer preservation");
    }
    let identifiers_ok = atlas_identifiers_are_unique(&certificate.patches);
    if !identifiers_ok {
        missing.push("unique nonempty class, representative, transport, and wall identifiers");
    } else if missing.is_empty() {
        missing.push(
            "verified transport, wall, cover, and gluing bindings are not attached to these declarations",
        );
    }

    let status = if !identifiers_ok {
        AtlasStatus::InvalidCertificate
    } else if missing.len() == 1 && missing[0].contains("not attached") {
        AtlasStatus::DeclaredChecklist
    } else {
        AtlasStatus::MissingProofObligation
    };
    let discharged = if status == AtlasStatus::Certified {
        vec![
            "exhaustive MUB(6) triple atlas",
            "wall-certified transport patch for every atlas class",
            "atlas overlap compatibility",
            "basis-gluing theorem",
            "ZeroRel and terminalizer preservation across atlas transports",
        ]
    } else {
        vec![]
    };

    GlobalAtlasAssessment {
        status,
        evidence: GlobalAtlasEvidence {
            exhaustive_triple_cover: certificate.exhaustive_triple_cover,
            wall_certificate_for_every_class: certificate.class_count > 0
                && patch_for_every_class
                && every_ledger_closed,
            overlap_compatibility: certificate.overlap_compatibility,
            basis_gluing: certificate.basis_gluing,
            zero_rel_preserved: certificate.zero_rel_preserved,
            terminalizer_preserved: certificate.terminalizer_preserved,
        },
        accepted_patch_count: certificate.patches.len(),
        candidate_sources: vec![],
        discharged_obligations: discharged,
        missing_obligations: missing,
    }
}

fn atlas_identifiers_are_unique(patches: &[AtlasPatchCertificate]) -> bool {
    let mut seen = std::collections::BTreeSet::new();
    patches.iter().all(|patch| {
        let fields = [
            patch.class_id,
            patch.representative,
            patch.transport_to_wall_lane,
            patch.wall_certificate,
        ];
        !fields.iter().any(|field| field.is_empty()) && seen.insert(patch.class_id)
    })
}

fn audit_stabilizer_orbit(crate_root: &Path) -> CandidateCoverAudit {
    let relative_path = "../mub/public-export/evidence/d6-stabilizer-orbit-census-2026-06-11.json";
    match read_json(crate_root, relative_path) {
        Some(value) if has_non_claim(&value, "orbit_equals_maximizer_set_is_seeded_sweep_evidence_not_a_theorem") => {
            CandidateCoverAudit {
                role: CandidateCoverRole::PinnedSymmetryOrbit,
                relative_path,
                verdict: CandidateCoverVerdict::NotGlobalCover,
                reason: "receipt is a pinned stabilizer/orbit census and explicitly does not prove orbit completeness as a theorem",
            }
        }
        Some(_) => CandidateCoverAudit {
            role: CandidateCoverRole::PinnedSymmetryOrbit,
            relative_path,
            verdict: CandidateCoverVerdict::UsefulLocalEvidence,
            reason: "receipt exists but does not declare an exhaustive triple-class cover",
        },
        None => missing_audit(CandidateCoverRole::PinnedSymmetryOrbit, relative_path),
    }
}

fn audit_projector_polytope_invariants(crate_root: &Path) -> CandidateCoverAudit {
    let relative_path =
        "../mub/public-export/evidence/projector-polytope-invariants-2026-06-11.json";
    match read_json(crate_root, relative_path) {
        Some(value)
            if value
                .get("method")
                .and_then(Value::as_str)
                .is_some_and(|method| method.contains("numerical evidence not theorems")) =>
        {
            CandidateCoverAudit {
                role: CandidateCoverRole::ProjectorPolytopeScout,
                relative_path,
                verdict: CandidateCoverVerdict::NumericalOnly,
                reason: "projector-polytope invariant receipt states sampled walls are numerical evidence, not theorems",
            }
        }
        Some(_) => CandidateCoverAudit {
            role: CandidateCoverRole::ProjectorPolytopeScout,
            relative_path,
            verdict: CandidateCoverVerdict::NotGlobalCover,
            reason: "projector-polytope receipt does not provide proof-carrying atlas patches",
        },
        None => missing_audit(CandidateCoverRole::ProjectorPolytopeScout, relative_path),
    }
}

fn audit_projector_polytope_symmetry_orbit(crate_root: &Path) -> CandidateCoverAudit {
    let relative_path =
        "../mub/public-export/evidence/projector-polytope-symmetry-orbit-2026-06-11.json";
    match read_json(crate_root, relative_path) {
        Some(value) if has_non_claim(&value, "newton_polish_certifies_a_stationary_point_not_global_optimality") => {
            CandidateCoverAudit {
                role: CandidateCoverRole::ProjectorPolytopeScout,
                relative_path,
                verdict: CandidateCoverVerdict::NumericalOnly,
                reason: "symmetry-orbit receipt records stationary/numerical evidence, not global optimality or triple-cover proof",
            }
        }
        Some(_) => CandidateCoverAudit {
            role: CandidateCoverRole::ProjectorPolytopeScout,
            relative_path,
            verdict: CandidateCoverVerdict::NotGlobalCover,
            reason: "symmetry-orbit receipt does not provide exhaustive triple cover",
        },
        None => missing_audit(CandidateCoverRole::ProjectorPolytopeScout, relative_path),
    }
}

fn audit_transport_closure(crate_root: &Path) -> CandidateCoverAudit {
    let relative_path = "../mub/public-export/evidence/transport-closure-exact-2026-06-12.json";
    match read_json(crate_root, relative_path) {
        Some(value)
            if value
                .pointer("/theorem/transport_closed_deterministically")
                .and_then(Value::as_bool)
                == Some(true) =>
        {
            CandidateCoverAudit {
                role: CandidateCoverRole::TransportClosureReceipt,
                relative_path,
                verdict: CandidateCoverVerdict::UsefulLocalEvidence,
                reason: "receipt checks deterministic transport only inside the pinned H-symmetry certificate lane",
            }
        }
        Some(_) => CandidateCoverAudit {
            role: CandidateCoverRole::TransportClosureReceipt,
            relative_path,
            verdict: CandidateCoverVerdict::NotGlobalCover,
            reason: "transport receipt is present but does not certify global triple cover",
        },
        None => missing_audit(CandidateCoverRole::TransportClosureReceipt, relative_path),
    }
}

fn missing_audit(role: CandidateCoverRole, relative_path: &'static str) -> CandidateCoverAudit {
    CandidateCoverAudit {
        role,
        relative_path,
        verdict: CandidateCoverVerdict::Missing,
        reason: "candidate receipt is missing",
    }
}

fn read_json(crate_root: &Path, relative_path: &str) -> Option<Value> {
    let path = crate_root.join(relative_path);
    let bytes = std::fs::read(path).ok()?;
    serde_json::from_slice(&bytes).ok()
}

fn has_non_claim(value: &Value, needle: &str) -> bool {
    value
        .get("non_claims")
        .and_then(Value::as_array)
        .is_some_and(|claims| claims.iter().any(|claim| claim.as_str() == Some(needle)))
}

#[cfg(test)]
mod tests {
    use super::*;

    fn crate_root() -> &'static Path {
        Path::new(env!("CARGO_MANIFEST_DIR"))
    }

    #[test]
    fn current_receipts_do_not_form_global_atlas() {
        let assessment = assess_current_global_atlas(crate_root());
        assert_eq!(assessment.status, AtlasStatus::MissingProofObligation);
        assert_eq!(assessment.evidence, GlobalAtlasEvidence::default());
        assert_eq!(assessment.accepted_patch_count, 0);
        assert_eq!(assessment.candidate_sources.len(), 4);
        for source in &assessment.candidate_sources {
            if !crate_root().join(source.relative_path).exists() {
                assert_eq!(source.verdict, CandidateCoverVerdict::Missing);
            }
        }
        assert!(assessment
            .missing_obligations
            .iter()
            .any(|obligation| obligation.contains("exhaustive atlas")));
    }

    #[test]
    fn complete_atlas_shape_would_certify_full_cover_gate() {
        let certificate = GlobalMub6AtlasCertificate {
            exhaustive_triple_cover: true,
            class_count: 1,
            patches: vec![AtlasPatchCertificate {
                class_id: "toy-class",
                representative: "toy-representative",
                transport_to_wall_lane: "toy-transport",
                wall_certificate: "toy-wall-certificate",
                loss_ledger_closed: true,
            }],
            overlap_compatibility: true,
            basis_gluing: true,
            zero_rel_preserved: true,
            terminalizer_preserved: true,
        };
        let assessment = verify_global_mub6_atlas_certificate(&certificate);
        assert_eq!(assessment.status, AtlasStatus::DeclaredChecklist);
        assert!(assessment
            .missing_obligations
            .iter()
            .any(|obligation| obligation.contains("not attached")));
        assert!(assessment.evidence.exhaustive_triple_cover);
        assert!(assessment.evidence.wall_certificate_for_every_class);
        assert!(assessment.evidence.basis_gluing);
    }

    #[test]
    fn atlas_shape_rejects_missing_patch_and_gluing() {
        let certificate = GlobalMub6AtlasCertificate {
            exhaustive_triple_cover: true,
            class_count: 1,
            patches: vec![],
            overlap_compatibility: true,
            basis_gluing: false,
            zero_rel_preserved: true,
            terminalizer_preserved: true,
        };
        let assessment = verify_global_mub6_atlas_certificate(&certificate);
        assert_eq!(assessment.status, AtlasStatus::MissingProofObligation);
        // Each obligation is reported on its own rather than inherited from
        // the overall status.
        assert!(assessment.evidence.exhaustive_triple_cover);
        assert!(assessment.evidence.overlap_compatibility);
        assert!(!assessment.evidence.wall_certificate_for_every_class);
        assert!(!assessment.evidence.basis_gluing);
        assert!(assessment
            .missing_obligations
            .iter()
            .any(|obligation| obligation.contains("every atlas class")));
        assert!(assessment
            .missing_obligations
            .iter()
            .any(|obligation| obligation.contains("basis-gluing")));
    }
}
