
use omega_policy::trichotomy::ObstructionDiagnosticClass;
use omega_types::{EvidenceCeiling, FactLabel};
use serde::Serialize;

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Serialize)]
pub enum MubFormulation {
    CompleteExistence,
    ExtensionAfterKBases,
    PinnedTripleWall,
    ProjectorPolytopeResidual,
    WeylBoard,
    ProductBasisObstruction,
    AlgebraicCyclotomicConstruction,
    SosPsdCertificate,
    FiniteCombinatorialBoard,
    BenchmarkVerifier,
    Other,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Serialize)]
pub enum ExactnessBoundary {
    ExactAlgebraic,
    ExactCombinatorial,
    ExactPsdCertificate,
    NumericalEvidenceOnly,
    Underdetermined,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Serialize)]
pub enum TransformationStatus {
    Allowed,
    Conditional,
    Forbidden,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Serialize)]
pub enum PrimitiveDifferenceKind {
    OrthonormalityDefect,
    MutualUnbiasednessDefect,
    ProjectorSimplexDefect,
    FourthVectorFeasibilityDefect,
    ProductCeilingDefect,
    WeylBoardDefect,
    SosCertificateDefect,
    PsdPositivityDefect,
    TransportClosureDefect,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Serialize)]
pub enum Computability {
    ExactNow,
    ExactIfArtifactSupplied,
    NumericalOnly,
    NotDeclared,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Serialize)]
pub enum ZeroRelKind {
    ExactAlgebraicEquality,
    ExactOrthonormality,
    ExactMutualUnbiasedness,
    ExactFourthVectorFeasibility,
    ExactWallAttainment,
    ExactPsdIdentity,
    ExactWeylBoardEquivalence,
    ExactRepairImageMembership,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Serialize)]
pub enum MubClaimKind {
    ExactInstanceSolution,
    PinnedTripleWallTheorem,
    FourthVectorObstruction,
    ProductVectorCeiling,
    WeylBoardSectorCap,
    RestrictedFamilyTheorem,
    CertificateBoundaryTheorem,
    LowDegreeSosNoGo,
    ExactBenchmarkVerifier,
    NumericalEvidence,
    CandidateSurvivor,
    Underdetermined,
    Refuted,
    TypedRefusal,
    GeneralMubTheorem,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Serialize)]
pub enum ClaimDisposition {
    ExactInstanceOnly,
    CandidateSurvivor,
    EvidenceOnly,
    Underdetermined,
    TypedRefusal,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Serialize)]
pub enum MubObstructionClass {
    PurePhaseArtifact,
    BasisLabelArtifact,
    SymmetryGaugeArtifact,
    ObserverHiddenDefect,
    NumericalArtifact,
    ExactAlgebraicSurvivor,
    ClosedFeasibilityObstruction,
    ClosureFailureObstruction,
    PsdCertificateSurvivor,
    WeylBoardSurvivor,
    UnderdeterminedCarrier,
    TypedRefusal,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct CorpusPull {
    pub encyclopedia_entries: Vec<&'static str>,
    pub candidate_entries: Vec<&'static str>,
    pub paper_sources: Vec<&'static str>,
    pub non_claims: Vec<&'static str>,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct MubCarrier {
    pub dimension: Option<usize>,
    pub fixed_bases: Option<usize>,
    pub object_kind: &'static str,
    pub coefficient_field: &'static str,
    pub exactness_boundary: ExactnessBoundary,
    pub observer: &'static str,
    pub terminalizer_preserves: Vec<&'static str>,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct TransformationLedgerEntry {
    pub name: &'static str,
    pub status: TransformationStatus,
    pub reason: &'static str,
    pub preserves: &'static str,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct PrimitiveDifferenceSpec {
    pub kind: PrimitiveDifferenceKind,
    pub domain: &'static str,
    pub codomain: &'static str,
    pub orientation: &'static str,
    pub computability: Computability,
    pub exact_field: &'static str,
    pub measures: &'static str,
    pub forgets: &'static str,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct ZeroRelDeclaration {
    pub kind: ZeroRelKind,
    pub relation: &'static str,
    pub field: &'static str,
    pub forbids: Vec<&'static str>,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct ObstructionLedgerEntry {
    pub target: &'static str,
    pub claim_kind: MubClaimKind,
    pub q1: &'static str,
    pub phi1: &'static str,
    pub gamma2: &'static str,
    pub obstruction_class: MubObstructionClass,
    pub omega_status: Option<ObstructionDiagnosticClass>,
    pub evidence_ceiling: EvidenceCeiling,
    pub authority_effect: FactLabel,
    pub boundary: &'static str,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct BenchmarkSelection {
    pub first_ladder_rung: &'static str,
    pub first_non_control_target: &'static str,
    pub reason: &'static str,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct MubPrimitiveMap {
    pub formulation: MubFormulation,
    pub corpus: CorpusPull,
    pub carrier: MubCarrier,
    pub primitive_differences: Vec<PrimitiveDifferenceSpec>,
    pub zero_rel: ZeroRelDeclaration,
    pub transformations: Vec<TransformationLedgerEntry>,
    pub obstruction_ledger: Vec<ObstructionLedgerEntry>,
    pub first_benchmark: BenchmarkSelection,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct MubClaimAssessment {
    pub target: &'static str,
    pub claim_kind: MubClaimKind,
    pub disposition: ClaimDisposition,
    pub evidence_ceiling: EvidenceCeiling,
    pub authority_effect: FactLabel,
    pub reason: &'static str,
}

pub fn first_run_primitive_map() -> MubPrimitiveMap {
    MubPrimitiveMap {
        formulation: MubFormulation::PinnedTripleWall,
        corpus: CorpusPull {
            encyclopedia_entries: vec![],
            candidate_entries: vec![
                "JUDG/ENC proposal: MUB pinned-triple feasibility carrier",
                "JUDG/ENC proposal: MUB projector-polytope residual map",
                "JUDG/ENC proposal: MUB certificate-boundary firebreak",
            ],
            paper_sources: vec![
                "900A Primitive Difference Monograph: difference, repair, residual, closure, terminal boundary",
                "000 Primitive Axiomatics: finite C0/C1/C2, Q1, Phi1, Gamma2, no authority from diagnostics",
                "000a When Obstruction Is Not Scalar: quantum/vector observer geometry is declared, not automatic",
                "024 Authority Firewall: evidence and authority remain separated",
                "028 Representation Abundance: representation-rich systems do not imply authority",
                "mub6-wall-paper-v1.pdf: exact pinned canonical d=6 wall, explicitly not MUB(6) resolution",
            ],
            non_claims: vec![
                "No canonical MUB ENC entry was found in the local encyclopedia.",
                "No general MUB(d) theorem is authorized by the local corpus.",
                "The d=6 pinned canonical wall is not a solution of MUB(6).",
                "Numerical d=10 evidence is not ZeroRel and not terminal authority.",
            ],
        },
        carrier: MubCarrier {
            dimension: Some(6),
            fixed_bases: Some(3),
            object_kind: "rank-one rays/projectors after the canonical product triple T0",
            coefficient_field: "Q(zeta_24)(sqrt5) for attainment; Q(sqrt2,sqrt3) for PSD certificate",
            exactness_boundary: ExactnessBoundary::ExactAlgebraic,
            observer: "projector-polytope residual observer R on Herm0(6)",
            terminalizer_preserves: vec![
                "unit-vector normalization",
                "orthonormality of the three fixed bases",
                "cross-basis overlap squared equals 1/6",
                "exact feasibility equality f(v)=W or f(v)=1",
                "certificate identity and exact PSD conditions",
            ],
        },
        primitive_differences: vec![
            PrimitiveDifferenceSpec {
                kind: PrimitiveDifferenceKind::OrthonormalityDefect,
                domain: "declared basis columns in C^6",
                codomain: "Gram(B)-I over the declared exact field",
                orientation: "zero means the basis is exactly orthonormal",
                computability: Computability::ExactNow,
                exact_field: "Q(zeta_24) subset of Q(zeta_24)(sqrt5)",
                measures: "basis self-consistency",
                forgets: "fourth-vector feasibility",
            },
            PrimitiveDifferenceSpec {
                kind: PrimitiveDifferenceKind::MutualUnbiasednessDefect,
                domain: "pairs of basis vectors from different fixed bases",
                codomain: "|<u,v>|^2 - 1/6",
                orientation: "zero means exact mutual unbiasedness",
                computability: Computability::ExactNow,
                exact_field: "Q(zeta_24)",
                measures: "cross-basis overlap nonuniformity",
                forgets: "projector residual closure and PSD certificate status",
            },
            PrimitiveDifferenceSpec {
                kind: PrimitiveDifferenceKind::FourthVectorFeasibilityDefect,
                domain: "unit ray v in C^6 after T0",
                codomain: "1 - f(v)",
                orientation: "zero means a fourth-vector candidate; positive means obstruction",
                computability: Computability::ExactNow,
                exact_field: "Q(zeta_24)(sqrt5) for the current witness",
                measures: "ray-level failure to be unbiased to all fixed bases",
                forgets: "whether six such rays glue into a full fourth basis",
            },
            PrimitiveDifferenceSpec {
                kind: PrimitiveDifferenceKind::PsdPositivityDefect,
                domain: "level-2 Veronese certificate matrix Q",
                codomain: "PSD/kernel/complement verification residual",
                orientation: "zero plus exact PSD establishes the upper-bound side",
                computability: Computability::ExactIfArtifactSupplied,
                exact_field: "Q(sqrt2,sqrt3)",
                measures: "certificate-boundary closure",
                forgets: "other triples and the general MUB(d) problem",
            },
        ],
        zero_rel: ZeroRelDeclaration {
            kind: ZeroRelKind::ExactWallAttainment,
            relation: "all declared polynomial, overlap, and PSD identities hold exactly in the declared fields",
            field: "Q(zeta_24)(sqrt5) and Q(sqrt2,sqrt3)",
            forbids: vec![
                "floating-point tolerance as equality",
                "PSLQ output as proof",
                "changing the pinned triple without certified equivalence",
                "promoting a fourth-vector wall to a general MUB(d) theorem",
            ],
        },
        transformations: vec![
            TransformationLedgerEntry {
                name: "global phase",
                status: TransformationStatus::Allowed,
                reason: "rays/projectors are phase invariant",
                preserves: "overlap moduli and Q_v",
            },
            TransformationLedgerEntry {
                name: "basis and vector permutations",
                status: TransformationStatus::Allowed,
                reason: "labels do not change the pinned feasibility problem",
                preserves: "Gram and overlap multisets",
            },
            TransformationLedgerEntry {
                name: "projector lift",
                status: TransformationStatus::Allowed,
                reason: "declared carrier is centered projectors in Herm0(6)",
                preserves: "ray feasibility as projector residual norm",
            },
            TransformationLedgerEntry {
                name: "Galois transport",
                status: TransformationStatus::Conditional,
                reason: "must preserve the target identity and positivity claims",
                preserves: "declared algebraic identity when separately checked",
            },
            TransformationLedgerEntry {
                name: "SOS/PSD lift",
                status: TransformationStatus::Conditional,
                reason: "certificate identity and exact PSD must be replayed",
                preserves: "upper-bound theorem only within the declared lift",
            },
            TransformationLedgerEntry {
                name: "numerical Newton polish",
                status: TransformationStatus::Forbidden,
                reason: "can propose witnesses but cannot satisfy ZeroRel",
                preserves: "nothing authority-bearing",
            },
            TransformationLedgerEntry {
                name: "CRT/Good-Thomas relabeling",
                status: TransformationStatus::Conditional,
                reason: "requires certified equivalence of the pinned carrier",
                preserves: "dimension/product structure only when explicitly proved",
            },
        ],
        obstruction_ledger: vec![
            ObstructionLedgerEntry {
                target: "d=6 canonical pinned triple T0 wall",
                claim_kind: MubClaimKind::PinnedTripleWallTheorem,
                q1: "projector residual quotient after phase/label/projector repair",
                phi1: "not formalized as Omega Phi1; pinned feasibility gap is 1 - W = (12 - 3*sqrt6)/100",
                gamma2: "certificate closure charge is zero only after exact PSD identity and kernel/complement replay",
                obstruction_class: MubObstructionClass::ClosedFeasibilityObstruction,
                omega_status: Some(ObstructionDiagnosticClass::ClosedResidual),
                evidence_ceiling: EvidenceCeiling::BoundaryChecked,
                authority_effect: FactLabel::EvidenceOnly,
                boundary: "source-level exact pinned-triple wall; this first-run map does not replay terminalization and is not a complete MUB(6) nonexistence theorem",
            },
            ObstructionLedgerEntry {
                target: "d=10 exploratory wall",
                claim_kind: MubClaimKind::NumericalEvidence,
                q1: "not terminalized in Omega-native exact carrier",
                phi1: "not certified",
                gamma2: "not certified",
                obstruction_class: MubObstructionClass::NumericalArtifact,
                omega_status: None,
                evidence_ceiling: EvidenceCeiling::ShapeOnly,
                authority_effect: FactLabel::EvidenceOnly,
                boundary: "evidence-only until exact carrier, ZeroRel, and certificate replay exist",
            },
            ObstructionLedgerEntry {
                target: "general MUB(N)",
                claim_kind: MubClaimKind::GeneralMubTheorem,
                q1: "underdetermined across dimensions and representations",
                phi1: "not defined without a carrier for all cases and repair class",
                gamma2: "not defined without a closure map for all cases and certificate family",
                obstruction_class: MubObstructionClass::UnderdeterminedCarrier,
                omega_status: None,
                evidence_ceiling: EvidenceCeiling::ExternalOracleRequired,
                authority_effect: FactLabel::EvidenceOnly,
                boundary: "typed refusal for any claim that finite pinned walls solve MUB(N)",
            },
        ],
        first_benchmark: BenchmarkSelection {
            first_ladder_rung: "d=2 complete-set control",
            first_non_control_target: "d=6 canonical pinned triple T0 wall",
            reason: "d=2 checks the exact verifier grammar; d=6 is the first nontrivial local artifact already represented in this crate",
        },
    }
}

pub fn assess_general_mub_n() -> MubClaimAssessment {
    MubClaimAssessment {
        target: "general MUB(N)",
        claim_kind: MubClaimKind::GeneralMubTheorem,
        disposition: ClaimDisposition::TypedRefusal,
        evidence_ceiling: EvidenceCeiling::ExternalOracleRequired,
        authority_effect: FactLabel::EvidenceOnly,
        reason: "No local ENC authority, carrier for all cases, exact ZeroRel family, or all-N certificate sequence is present. MUB(6) pinned-wall and d=10 evidence cannot be promoted to a general theorem.",
    }
}

pub fn assess_d6_pinned_wall(global_certificate_replayed: bool) -> MubClaimAssessment {
    if global_certificate_replayed {
        MubClaimAssessment {
            target: "d=6 canonical pinned triple T0 wall",
            claim_kind: MubClaimKind::PinnedTripleWallTheorem,
            disposition: ClaimDisposition::ExactInstanceOnly,
            evidence_ceiling: EvidenceCeiling::BoundaryChecked,
            authority_effect: FactLabel::FactOnly,
            reason: "Both exact attainment and the exact PSD upper-bound certificate have replayed for the pinned triple.",
        }
    } else {
        MubClaimAssessment {
            target: "d=6 canonical pinned triple T0 wall",
            claim_kind: MubClaimKind::PinnedTripleWallTheorem,
            disposition: ClaimDisposition::CandidateSurvivor,
            evidence_ceiling: EvidenceCeiling::LocalReplay,
            authority_effect: FactLabel::EvidenceOnly,
            reason: "The small exact Rust checks replay locally, but the large global certificate artifact has not been replayed in this run.",
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn first_run_has_no_canonical_mub_enc_authority() {
        let map = first_run_primitive_map();
        assert!(map.corpus.encyclopedia_entries.is_empty());
        assert!(map
            .corpus
            .candidate_entries
            .iter()
            .all(|entry| entry.starts_with("JUDG/ENC proposal")));
    }

    #[test]
    fn first_run_declares_exact_zero_rel_and_forbids_numeric_zero() {
        let map = first_run_primitive_map();
        assert_eq!(map.zero_rel.kind, ZeroRelKind::ExactWallAttainment);
        assert!(map
            .zero_rel
            .forbids
            .iter()
            .any(|rule| rule.contains("floating-point")));
    }

    #[test]
    fn general_mub_n_is_a_typed_refusal_not_a_theorem() {
        let assessment = assess_general_mub_n();
        assert_eq!(assessment.claim_kind, MubClaimKind::GeneralMubTheorem);
        assert_eq!(assessment.disposition, ClaimDisposition::TypedRefusal);
        assert_eq!(assessment.authority_effect, FactLabel::EvidenceOnly);
    }

    #[test]
    fn d6_wall_scope_does_not_claim_mub6_solution() {
        let map = first_run_primitive_map();
        let d6 = map
            .obstruction_ledger
            .iter()
            .find(|entry| entry.target.contains("d=6 canonical"))
            .expect("d=6 ledger entry present");
        assert_eq!(d6.claim_kind, MubClaimKind::PinnedTripleWallTheorem);
        assert!(d6.boundary.contains("not a complete MUB(6)"));
    }

    #[test]
    fn unreplayed_d6_global_certificate_remains_evidence_only() {
        let assessment = assess_d6_pinned_wall(false);
        assert_eq!(assessment.disposition, ClaimDisposition::CandidateSurvivor);
        assert_eq!(assessment.authority_effect, FactLabel::EvidenceOnly);
    }
}
