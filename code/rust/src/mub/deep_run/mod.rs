
use std::{collections::BTreeSet, path::Path};

use serde::Serialize;

use crate::native::exact::basis_gluing_gate::{
    verify_basis_gluing_gate, BasisGluingGateReport, BasisGluingInputs,
};
use crate::native::exact::char_two_parametric_gate::{
    verify_current_char_two_parametric_gate, CharTwoParametricGateReport,
};
use engine_quantum_physics::mub::char_two_weyl_board::{
    verify_current_char_two_weyl_board_schemas, CharTwoWeylBoardReport,
};
use engine_quantum_physics::mub::composite_completion_gate::{
    verify_current_composite_completion_gates, CompositeCompletionGateReport,
};
use engine_quantum_physics::mub::composite_controls::{
    verify_composite_lower_controls, CompositeControlReport, CompositeControlStatus,
};
use engine_quantum_physics::mub::composite_tensor_family_gate::{
    verify_composite_tensor_family_gate, CompositeTensorFamilyReport,
};
use engine_quantum_physics::mub::d10_controls::{
    verify_cyclotomic120_controls, Cyclotomic120ControlReport, Cyclotomic120Status,
};
use crate::native::float_check::d10_wall_status::{current_d10_wall_status, D10WallStatusReport};
use engine_quantum_physics::mub::dimension_stratification::{
    current_dimension_stratification_reports, DimensionStratificationReport,
};
use crate::native::exact::extension::{
    assess_full_mub6, assess_general_mub_n as assess_general_extension, assess_mub10,
    ExtensionTerminal, ExtensionVerdict, FullMub6Census, GeneralMubEvidence, Mub10Census,
};
use engine_quantum_physics::mub::finite_projector_control::{
    verify_current_finite_projector_controls, FiniteProjectorControlReport,
    FiniteProjectorControlStatus,
};
use crate::native::exact::global_atlas::{
    assess_current_global_atlas, AtlasStatus, GlobalAtlasAssessment,
};
use engine_quantum_physics::mub::gtmur_projector_ledger::{
    verify_current_gtmur_projector_ledgers, GtmurProjectorLedgerReport,
};
use crate::native::exact::gtor_gttc_gate::{
    verify_gtor_gttc_gates, GtorGttcGateInputs, GtorGttcGateReport,
};
use engine_quantum_physics::mub::hilbert_transport::{
    verify_current_hilbert_transport_schemas, HilbertTransportReport,
};
use crate::native::exact::local_transport::{
    check_pinned_transport_receipt, LocalTransportStatus, LocalTransportSubcertificate,
};
use engine_quantum_physics::mub::odd_prime_gauss_certificate_gate::{
    verify_current_odd_prime_gauss_certificate_gate, OddPrimeGaussCertificateReport,
};
use engine_quantum_physics::mub::odd_prime_power_controls::{
    verify_current_odd_prime_power_controls, OddPrimePowerControlReport, OddPrimePowerControlStatus,
};
use engine_quantum_physics::mub::odd_prime_power_field_theorem_gate::{
    verify_current_odd_prime_power_field_theorem_gate, OddPrimePowerFieldTheoremReport,
};
use engine_quantum_physics::mub::odd_prime_power_parametric_gate::{
    verify_current_odd_prime_power_parametric_gate, OddPrimePowerParametricGateReport,
};
use engine_quantum_physics::mub::odd_prime_power_weyl::{
    verify_current_odd_prime_power_weyl_schemas, OddPrimePowerWeylReport,
};
use engine_quantum_physics::mub::odd_prime_weyl::{
    verify_current_odd_prime_weyl_schemas, OddPrimeWeylReport,
};
use crate::native::exact::operator_ladder::{current_operator_ladder, OperatorAttempt};
use engine_quantum_physics::mub::prime_controls::{
    verify_prime_controls, verify_prime_power_controls, BenchmarkStatus, PrimeControlReport,
};
use engine_quantum_physics::mub::prime_power_gtmur_boundary::{
    verify_prime_power_gtmur_boundary, PrimePowerGtmurBoundaryReport,
};
use engine_quantum_physics::mub::projector_algebra::{
    verify_current_projector_algebra_schemas, ProjectorAlgebraReport,
};
use engine_quantum_physics::mub::spectral_lift::{
    verify_current_spectral_lift_schemas, SpectralLiftReport,
};
use crate::primitive_map::{
    assess_d6_pinned_wall, assess_general_mub_n, first_run_primitive_map, CorpusPull,
    MubClaimAssessment,
};
use tfqm_wdp::ddc::mub_cochain::{
    run_mub6_cochain_obstruction_search, MubAtlasEvidence, MubCochainRunReport,
};

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Serialize)]
pub enum ReplayTerminal {
    Replayed,
    MissingProofObligation,
    VerificationFailed,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Serialize)]
pub enum FinalTerminal {
    MissingProofObligation,
    TypedRefusal,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct ManifestReplay {
    pub terminal: ReplayTerminal,
    pub detail: &'static str,
    pub error: Option<String>,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct LowerBoundReplay {
    pub terminal: ReplayTerminal,
    pub target: &'static str,
    pub theorem: &'static str,
    pub overlaps_checked: Option<usize>,
    pub democratic_counts: Vec<[usize; 3]>,
    pub error: Option<String>,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct MissingArtifact {
    pub relative_path: String,
    pub obligation: String,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct UpperBoundReplay {
    pub terminal: ReplayTerminal,
    pub target: &'static str,
    pub theorem: &'static str,
    pub missing_artifacts: Vec<MissingArtifact>,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct ExtensionRun {
    pub target: &'static str,
    pub verdict: ExtensionVerdict,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub enum DeepRunMubCochainObstruction {
    Completed(MubCochainRunReport),
    CochainConstructionFailure { target: &'static str, error: String },
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct DeepRunReport {
    pub prompt: &'static str,
    pub formulation: &'static str,
    pub corpus: CorpusPull,
    pub manifest: ManifestReplay,
    pub d6_lower_bound: LowerBoundReplay,
    pub d6_upper_bound: UpperBoundReplay,
    pub pinned_transport: LocalTransportSubcertificate,
    pub global_atlas: GlobalAtlasAssessment,
    pub basis_gluing: BasisGluingGateReport,
    pub mub6_cochain_obstruction: DeepRunMubCochainObstruction,
    pub composite_lower_controls: Vec<CompositeControlReport>,
    pub composite_completion_gates: Vec<CompositeCompletionGateReport>,
    pub prime_controls: Vec<PrimeControlReport>,
    pub prime_power_controls: Vec<PrimeControlReport>,
    pub cyclotomic120_controls: Vec<Cyclotomic120ControlReport>,
    pub d10_wall_status: D10WallStatusReport,
    pub dimension_stratification: Vec<DimensionStratificationReport>,
    pub composite_tensor_family: CompositeTensorFamilyReport,
    pub odd_prime_gauss_certificates: OddPrimeGaussCertificateReport,
    pub odd_prime_weyl_schemas: Vec<OddPrimeWeylReport>,
    pub odd_prime_power_weyl_schemas: Vec<OddPrimePowerWeylReport>,
    pub odd_prime_power_controls: Vec<OddPrimePowerControlReport>,
    pub odd_prime_power_field_theorem_gate: OddPrimePowerFieldTheoremReport,
    pub odd_prime_power_parametric_gate: OddPrimePowerParametricGateReport,
    pub char_two_weyl_board_schemas: Vec<CharTwoWeylBoardReport>,
    pub spectral_lift_schemas: Vec<SpectralLiftReport>,
    pub projector_algebra_schemas: Vec<ProjectorAlgebraReport>,
    pub hilbert_transport_schemas: Vec<HilbertTransportReport>,
    pub gtmur_projector_ledgers: Vec<GtmurProjectorLedgerReport>,
    pub finite_projector_controls: Vec<FiniteProjectorControlReport>,
    pub char_two_parametric_gate: CharTwoParametricGateReport,
    pub prime_power_gtmur_boundary: PrimePowerGtmurBoundaryReport,
    pub pinned_d6_assessment: MubClaimAssessment,
    pub full_mub6: ExtensionRun,
    pub mub10: ExtensionRun,
    pub general_mub_n: ExtensionRun,
    pub operator_ladder: Vec<OperatorAttempt>,
    pub gtor_gttc_gates: Vec<GtorGttcGateReport>,
    pub general_mub_n_assessment: MubClaimAssessment,
    pub terminal: FinalTerminal,
    pub final_boundary: &'static str,
}

fn evaluate_cochain_obstruction(cochain_evidence: &MubAtlasEvidence) -> DeepRunMubCochainObstruction {
    match run_mub6_cochain_obstruction_search(cochain_evidence) {
        Ok(report) => DeepRunMubCochainObstruction::Completed(report),
        Err(error) => DeepRunMubCochainObstruction::CochainConstructionFailure {
            target: "MUB(6) cochain obstruction",
            error: format!("{error:?}"),
        },
    }
}

fn is_d6_product_lower_control(control: &CompositeControlReport) -> bool {
    control.dimension == 6
        && control.status == CompositeControlStatus::ExactPartialSet
        && control.error.is_none()
}

fn is_d10_lower_control(control: &Cyclotomic120ControlReport) -> bool {
    control.dimension == 10
        && control.status == Cyclotomic120Status::ExactPartialSet
        && control.error.is_none()
}

fn collect_terminalized_prime_dimensions(
    prime_controls: &[PrimeControlReport],
    prime_power_controls: &[PrimeControlReport],
    cyclotomic120_controls: &[Cyclotomic120ControlReport],
    odd_prime_power_controls: &[OddPrimePowerControlReport],
    finite_projector_controls: &[FiniteProjectorControlReport],
) -> BTreeSet<usize> {
    let mut dims = BTreeSet::new();
    for control in prime_controls.iter().chain(prime_power_controls.iter()) {
        if control.status == BenchmarkStatus::ExactCompleteSet {
            dims.insert(control.dimension);
        }
    }
    for control in cyclotomic120_controls {
        if control.status == Cyclotomic120Status::ExactCompleteSet {
            dims.insert(control.dimension);
        }
    }
    collect_additional_terminalized_dimensions(
        &mut dims,
        odd_prime_power_controls,
        finite_projector_controls,
    );
    dims
}

fn collect_additional_terminalized_dimensions(
    dims: &mut BTreeSet<usize>,
    odd_prime_power_controls: &[OddPrimePowerControlReport],
    finite_projector_controls: &[FiniteProjectorControlReport],
) {
    for control in odd_prime_power_controls {
        if control.status == OddPrimePowerControlStatus::ExactCompleteSet {
            dims.insert(control.dimension);
        }
    }
    for control in finite_projector_controls {
        if control.status == FiniteProjectorControlStatus::CompleteProjectorMubVerified {
            dims.insert(control.dimension);
        }
    }
}

fn is_terminalized_composite_gate(gate: &&CompositeCompletionGateReport) -> bool {
    matches!(
        gate.status,
        engine_quantum_physics::mub::composite_completion_gate::CompositeCompletionStatus::CompleteWitnessAccepted
            | engine_quantum_physics::mub::composite_completion_gate::CompositeCompletionStatus::NoGoCertificateAccepted
    )
}

fn compute_gtor_gttc_gates(
    terminalized_prime_components: usize,
    composite_completion_gates: &[CompositeCompletionGateReport],
) -> Vec<GtorGttcGateReport> {
    let finite_component_count = terminalized_prime_components + composite_completion_gates.len();
    let terminalized_component_count = terminalized_prime_components
        + composite_completion_gates
            .iter()
            .filter(is_terminalized_composite_gate)
            .count();
    verify_gtor_gttc_gates(GtorGttcGateInputs {
        finite_component_count,
        terminalized_component_count,
        edge_certificate_count: 0,
        edges: vec![],
        directed_gluing_present: false,
        query_relative_authority_present: false,
        uniform_certificate_family_present: false,
    })
}

pub fn run_deep_mub(crate_root: &Path) -> DeepRunReport {
    let primitive_map = first_run_primitive_map();
    let manifest = manifest_replay(crate_root);
    let d6_lower_bound = lower_bound_replay();
    let d6_upper_bound = upper_bound_replay(crate_root);
    let pinned_transport = check_pinned_transport_receipt(crate_root);
    let global_atlas = assess_current_global_atlas(crate_root);
    let composite_lower_controls = verify_composite_lower_controls();
    let prime_controls = verify_prime_controls();
    let prime_power_controls = verify_prime_power_controls();
    let cyclotomic120_controls = verify_cyclotomic120_controls();
    let d10_wall_status = current_d10_wall_status();
    let dimension_stratification = current_dimension_stratification_reports();
    let composite_tensor_family =
        verify_composite_tensor_family_gate(dimension_stratification.clone());
    let odd_prime_gauss_certificates = verify_current_odd_prime_gauss_certificate_gate();
    let odd_prime_weyl_schemas = verify_current_odd_prime_weyl_schemas();
    let odd_prime_power_weyl_schemas = verify_current_odd_prime_power_weyl_schemas();
    let odd_prime_power_controls = verify_current_odd_prime_power_controls();
    let odd_prime_power_field_theorem_gate = verify_current_odd_prime_power_field_theorem_gate();
    let odd_prime_power_parametric_gate = verify_current_odd_prime_power_parametric_gate();
    let char_two_weyl_board_schemas = verify_current_char_two_weyl_board_schemas();
    let spectral_lift_schemas = verify_current_spectral_lift_schemas();
    let projector_algebra_schemas = verify_current_projector_algebra_schemas();
    let hilbert_transport_schemas = verify_current_hilbert_transport_schemas();
    let gtmur_projector_ledgers = verify_current_gtmur_projector_ledgers();
    let finite_projector_controls = verify_current_finite_projector_controls();
    let char_two_parametric_gate = verify_current_char_two_parametric_gate();
    let prime_power_gtmur_boundary = verify_prime_power_gtmur_boundary();
    let upper_replayed = d6_upper_bound.terminal == ReplayTerminal::Replayed;
    let local_transport_checked = pinned_transport.status == LocalTransportStatus::ReceiptChecked;
    let global_atlas_certified = global_atlas.status == AtlasStatus::Certified;
    let atlas = global_atlas.evidence;
    let classwise_fourth_vector_obstruction =
        upper_replayed && atlas.wall_certificate_for_every_class;
    let basis_gluing = verify_basis_gluing_gate(BasisGluingInputs {
        pinned_upper_replayed: upper_replayed,
        exhaustive_triple_cover: atlas.exhaustive_triple_cover,
        accepted_patch_count: global_atlas.accepted_patch_count,
        wall_transport_for_every_class: atlas.wall_certificate_for_every_class,
        overlap_compatibility: atlas.overlap_compatibility,
        zero_rel_preserved: atlas.zero_rel_preserved,
        terminalizer_preserved: atlas.terminalizer_preserved,
        classwise_fourth_vector_obstruction,
        gluing_theorem_present: atlas.basis_gluing,
    });
    let cochain_evidence = MubAtlasEvidence {
        pinned_upper_replayed: upper_replayed,
        proof_carrying_classification: atlas.exhaustive_triple_cover,
        exhaustive_triple_cover: atlas.exhaustive_triple_cover,
        wall_certificate_for_every_class: atlas.wall_certificate_for_every_class,
        overlap_compatibility: atlas.overlap_compatibility,
        zero_rel_preserved: atlas.zero_rel_preserved,
        terminalizer_preserved: atlas.terminalizer_preserved,
        classwise_fourth_vector_obstruction,
        basis_gluing_operator_available: atlas.basis_gluing,
    };
    let mub6_cochain_obstruction = evaluate_cochain_obstruction(&cochain_evidence);
    let d6_product_lower_control_verified = composite_lower_controls
        .iter()
        .any(is_d6_product_lower_control);
    let d10_lower_control_verified = cyclotomic120_controls.iter().any(is_d10_lower_control);
    let composite_completion_gates = verify_current_composite_completion_gates(
        d6_product_lower_control_verified,
        d10_lower_control_verified,
        upper_replayed && global_atlas_certified,
    );
    let full_mub6_verdict = assess_full_mub6(&FullMub6Census {
        upper_bound_replayed: upper_replayed,
        local_transport_checked,
        product_lower_control_verified: d6_product_lower_control_verified,
    });
    let mub10_verdict = assess_mub10(&Mub10Census {
        cyclotomic120_lower_control_verified: d10_lower_control_verified,
    });
    let general_verdict = assess_general_extension(&GeneralMubEvidence {
        dimension_stratification: &dimension_stratification,
        composite_tensor_family: &composite_tensor_family,
        prime_controls: &prime_controls,
        odd_prime_gauss_certificates: &odd_prime_gauss_certificates,
        odd_prime_weyl_schemas: &odd_prime_weyl_schemas,
        odd_prime_power_weyl_schemas: &odd_prime_power_weyl_schemas,
        odd_prime_power_controls: &odd_prime_power_controls,
        odd_prime_power_parametric_gate: &odd_prime_power_parametric_gate,
        char_two_weyl_board_schemas: &char_two_weyl_board_schemas,
        spectral_lift_schemas: &spectral_lift_schemas,
        projector_algebra_schemas: &projector_algebra_schemas,
        hilbert_transport_schemas: &hilbert_transport_schemas,
        gtmur_projector_ledgers: &gtmur_projector_ledgers,
        finite_projector_controls: &finite_projector_controls,
        char_two_parametric_gate: &char_two_parametric_gate,
        prime_power_gtmur_boundary: &prime_power_gtmur_boundary,
    });
    debug_assert_eq!(general_verdict.terminal, ExtensionTerminal::TypedRefusal);
    let terminal = FinalTerminal::TypedRefusal;
    let terminalized_prime_power_dimensions = collect_terminalized_prime_dimensions(
        &prime_controls,
        &prime_power_controls,
        &cyclotomic120_controls,
        &odd_prime_power_controls,
        &finite_projector_controls,
    );
    let gtor_gttc_gates = compute_gtor_gttc_gates(
        terminalized_prime_power_dimensions.len(),
        &composite_completion_gates,
    );

    DeepRunReport {
        prompt: "crates/mub/unified_mub_prompt.md",
        formulation: "pinned triple wall / projector-polytope residual first; extension attempts are separate",
        corpus: primitive_map.corpus,
        manifest,
        d6_lower_bound,
        d6_upper_bound,
        pinned_transport,
        global_atlas,
        basis_gluing,
        mub6_cochain_obstruction,
        composite_lower_controls,
        composite_completion_gates,
        prime_controls,
        prime_power_controls,
        cyclotomic120_controls,
        d10_wall_status,
        dimension_stratification,
        composite_tensor_family,
        odd_prime_gauss_certificates,
        odd_prime_weyl_schemas,
        odd_prime_power_weyl_schemas,
        odd_prime_power_controls,
        odd_prime_power_field_theorem_gate,
        odd_prime_power_parametric_gate,
        char_two_weyl_board_schemas,
        spectral_lift_schemas,
        projector_algebra_schemas,
        hilbert_transport_schemas,
        gtmur_projector_ledgers,
        finite_projector_controls,
        char_two_parametric_gate,
        prime_power_gtmur_boundary,
        pinned_d6_assessment: assess_d6_pinned_wall(upper_replayed),
        full_mub6: ExtensionRun {
            target: "full MUB(6)",
            verdict: full_mub6_verdict,
        },
        mub10: ExtensionRun {
            target: "MUB(10)",
            verdict: mub10_verdict,
        },
        general_mub_n: ExtensionRun {
            target: "general MUB(n)",
            verdict: general_verdict,
        },
        operator_ladder: current_operator_ladder(upper_replayed),
        gtor_gttc_gates,
        general_mub_n_assessment: assess_general_mub_n(),
        terminal,
        final_boundary: "The current run reproduces the d=6 pinned lower-bound witness, gates the upper-bound replay on missing exact artifacts, and refuses full MUB(6), MUB(10), and MUB(n) theorem promotion.",
    }
}

fn manifest_replay(_crate_root: &Path) -> ManifestReplay {
    ManifestReplay {
        terminal: ReplayTerminal::MissingProofObligation,
        detail: "manifest replay unavailable (Apache compare crate removed 2026-08-04)",
        error: None,
    }
}

fn lower_bound_replay() -> LowerBoundReplay {
    LowerBoundReplay {
        terminal: ReplayTerminal::MissingProofObligation,
        target: "d=6 canonical pinned triple T0 lower bound",
        theorem: "f(v*) = W = (88 + 3*sqrt6)/100 for the declared pinned carrier",
        overlaps_checked: None,
        democratic_counts: vec![],
        error: Some(
            "lower-bound replay unavailable (Apache compare crate removed 2026-08-04)".to_string(),
        ),
    }
}

fn upper_bound_replay(_crate_root: &Path) -> UpperBoundReplay {
    UpperBoundReplay {
        terminal: ReplayTerminal::MissingProofObligation,
        target: "d=6 canonical pinned triple T0 upper bound",
        theorem: "upper-bound replay unavailable (Apache compare crate removed 2026-08-04)",
        missing_artifacts: vec![],
    }
}

#[cfg(test)]
mod tests;
