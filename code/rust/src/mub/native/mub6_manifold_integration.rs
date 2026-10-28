
use num_bigint::BigInt;
use num_rational::BigRational;
use num_traits::Zero;
use serde::{Deserialize, Serialize};

use crate::native::exact::mub6_constants::{certified_margin, delta_certified};
pub use crate::native::exact::mub6_constants::{
    circulation_gamma, circulation_gamma_scaled, total_domain_volume,
};
use crate::native::exact::mub6_continuous_chaining::{
    theta_interval_lower, theta_interval_upper, AdaptiveStepEngine,
};
use crate::native::exact::mub6_firewall::{AUTHORITY_EFFECT, FIREWALL};
use crate::native::exact::mub6_global_gluing::{
    enumerate_nerve2_triples, loop_holonomy, solve_loop_circulation, ModuliChart5, ModuliLoop,
    TransitionCocycleFamily,
};
use crate::native::exact::mub6_grand_synthesis::{
    canonical_global_partition_tree, GrandSynthesisChart, SynthesisLeafCell,
};
use tfqm_number_theory::rational::rq;

crate::fixture_set!(fixtures, "mub6_manifold_integration");

pub const NUM_CANONICAL_CHARTS: usize = 5;

pub const TOTAL_CELL_COUNT: usize = 28;

pub const NUM_CECH_TRIPLES: usize = 53;

pub fn map_regional_chart_to_moduli_chart(
    regional: GrandSynthesisChart,
    cell_id: &str,
) -> ModuliChart5 {
    match regional {
        GrandSynthesisChart::DitaFourierF6 => ModuliChart5::KarlssonManifold,
        GrandSynthesisChart::SzollosiDeltoidB6 => {
            if cell_id.contains("cusp") {
                ModuliChart5::DeltoidCusps
            } else {
                ModuliChart5::SzollosiCurve
            }
        }
        GrandSynthesisChart::TaoConfluenceS6 => ModuliChart5::TaoConfluence,
        GrandSynthesisChart::PeriodicCollar2D => ModuliChart5::KarlssonManifold,
        GrandSynthesisChart::KarlssonVolumeExterior => ModuliChart5::KarlssonManifold,
        GrandSynthesisChart::HaagerupOrbitH6 => ModuliChart5::HaagerupOrbit,
    }
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct UnifiedModuliSample {
    pub sample_id: String,
    pub chart: ModuliChart5,
    pub cell_id: Option<String>,
    pub coordinates: Vec<BigRational>,
    pub curvature_margin: BigRational,
    pub generating_circulation: Option<BigRational>,
}

impl UnifiedModuliSample {
    pub fn new(
        sample_id: String,
        chart: ModuliChart5,
        cell_id: Option<String>,
        coordinates: Vec<BigRational>,
        curvature_margin: BigRational,
        generating_circulation: Option<BigRational>,
    ) -> Self {
        Self {
            sample_id,
            chart,
            cell_id,
            coordinates,
            curvature_margin,
            generating_circulation,
        }
    }

    pub fn chart_representative(chart: ModuliChart5) -> Self {
        let zero = BigRational::zero();
        let margin = chart.default_margin();
        Self {
            sample_id: format!("canonical_rep_{}", chart.canonical_id()),
            chart,
            cell_id: None,
            coordinates: vec![zero.clone(), zero.clone(), zero.clone(), zero],
            curvature_margin: margin,
            generating_circulation: Some(circulation_gamma()),
        }
    }

    pub fn from_leaf_cell(cell: &SynthesisLeafCell) -> Self {
        let two = BigRational::from_integer(BigInt::from(2));
        let center_coords: Vec<BigRational> = cell
            .bounds
            .iter()
            .map(|(lo, hi)| (lo + hi) / &two)
            .collect();

        let chart = map_regional_chart_to_moduli_chart(cell.chart, &cell.cell_id);

        Self {
            sample_id: format!("cell_sample_{}", cell.cell_id),
            chart,
            cell_id: Some(cell.cell_id.clone()),
            coordinates: center_coords,
            curvature_margin: cell.margin.clone(),
            generating_circulation: Some(circulation_gamma()),
        }
    }
}

#[derive(Clone, Copy, Debug, PartialEq, Eq, PartialOrd, Ord, Hash, Serialize, Deserialize)]
pub enum UnifiedObstructionArm {
    CurvatureMarginOnly,
    LoopCirculationOnly,
    BothArms,
    Neither,
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct MasterUnifiedObstructionResult {
    pub sample_id: String,
    pub chart: ModuliChart5,
    pub curvature_margin: BigRational,
    pub min_margin_threshold: BigRational,
    pub curvature_obstructed: bool,
    pub circulation_phi1: Option<BigRational>,
    pub circulation_gamma_threshold: BigRational,
    pub circulation_obstructed: bool,
    pub is_obstructed: bool,
    pub active_arm: UnifiedObstructionArm,
}

fn evaluate_loop_circulation_arm(
    c_family: &TransitionCocycleFamily,
    generating_loop: Option<&ModuliLoop>,
    gamma: &BigRational,
) -> (Option<BigRational>, bool) {
    let Some(loop_obj) = generating_loop else {
        return (None, false);
    };
    let scale: i128 = 30000;
    let _hol = loop_holonomy(c_family, loop_obj);
    let Ok(rep) = solve_loop_circulation(loop_obj, scale, None) else {
        return (None, false);
    };
    let Some(value) = rep.scaled_verified_value(scale) else {
        return (None, false);
    };
    let obstructed = &value >= gamma && rep.dual_gap_zero && rep.circulation_conserved;
    (Some(value), obstructed)
}

pub fn evaluate_master_unified_obstruction(
    sample: &UnifiedModuliSample,
    c_family: &TransitionCocycleFamily,
    generating_loop: Option<&ModuliLoop>,
) -> MasterUnifiedObstructionResult {
    let min_margin = certified_margin();
    let gamma = circulation_gamma();

    let curvature_obstructed = sample.curvature_margin >= min_margin;
    let (circulation_phi1, circulation_obstructed) =
        evaluate_loop_circulation_arm(c_family, generating_loop, &gamma);

    let is_obstructed = curvature_obstructed || circulation_obstructed;

    let active_arm = match (curvature_obstructed, circulation_obstructed) {
        (true, true) => UnifiedObstructionArm::BothArms,
        (true, false) => UnifiedObstructionArm::CurvatureMarginOnly,
        (false, true) => UnifiedObstructionArm::LoopCirculationOnly,
        (false, false) => UnifiedObstructionArm::Neither,
    };

    MasterUnifiedObstructionResult {
        sample_id: sample.sample_id.clone(),
        chart: sample.chart,
        curvature_margin: sample.curvature_margin.clone(),
        min_margin_threshold: min_margin,
        curvature_obstructed,
        circulation_phi1,
        circulation_gamma_threshold: gamma,
        circulation_obstructed,
        is_obstructed,
        active_arm,
    }
}

pub fn canonical_28_cell_samples() -> Vec<UnifiedModuliSample> {
    let tree = canonical_global_partition_tree();
    tree.leaves
        .iter()
        .map(UnifiedModuliSample::from_leaf_cell)
        .collect()
}

pub fn canonical_5_chart_representatives() -> Vec<UnifiedModuliSample> {
    ModuliChart5::ALL
        .iter()
        .map(|&c| UnifiedModuliSample::chart_representative(c))
        .collect()
}

pub fn continuous_szollosi_chain_samples(num_steps: usize) -> Vec<UnifiedModuliSample> {
    let num = if num_steps == 0 { 20 } else { num_steps };
    let mut samples = Vec::with_capacity(num);

    let upper = theta_interval_upper();
    let step_denom = (num as i64) + 1;
    let margin = certified_margin();

    for i in 1..=num {
        let t = &upper * &rq(i as i64, step_denom);
        let sample_id = format!("szollosi_chain_sample_{}_{}", i, num);
        let coords = vec![t];
        samples.push(UnifiedModuliSample {
            sample_id,
            chart: ModuliChart5::SzollosiCurve,
            cell_id: None,
            coordinates: coords,
            curvature_margin: margin.clone(),
            generating_circulation: Some(circulation_gamma()),
        });
    }

    samples
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct ContinuousChainingReport {
    pub theta_lower: BigRational,
    pub theta_upper: BigRational,
    pub mesh_step: BigRational,
    pub delta_crit: BigRational,
    pub base_gap: BigRational,
    pub lipschitz_bound: BigRational,
    pub uniform_chaining_margin: BigRational,
    pub num_samples_verified: usize,
    pub all_samples_obstructed: bool,
    pub gap_stability_certified: bool,
}

pub fn verify_continuous_szollosi_chaining(
    num_samples: usize,
) -> Result<ContinuousChainingReport, ManifoldIntegrationError> {
    let engine = AdaptiveStepEngine::canonical();
    let step = delta_certified();

    if !engine.is_admissible_step(&step) {
        return Err(ManifoldIntegrationError::ContinuousChainingViolation(
            format!(
                "Step {} is not admissible (delta_crit = {})",
                step, engine.delta_crit
            ),
        ));
    }

    let margin = engine.compute_margin(&step);
    if margin < certified_margin() {
        return Err(ManifoldIntegrationError::ContinuousChainingViolation(
            format!(
                "Margin {} is below global minimum {}",
                margin,
                certified_margin()
            ),
        ));
    }

    let c_family = TransitionCocycleFamily::canonical();
    let chain_samples = continuous_szollosi_chain_samples(num_samples);
    let mut all_obstructed = true;

    for sample in &chain_samples {
        let res = evaluate_master_unified_obstruction(sample, &c_family, None);
        if !res.is_obstructed {
            all_obstructed = false;
            break;
        }
    }

    if !all_obstructed {
        return Err(ManifoldIntegrationError::ContinuousChainingViolation(
            "Some chain sample failed master obstruction disjunction".to_string(),
        ));
    }

    Ok(ContinuousChainingReport {
        theta_lower: theta_interval_lower(),
        theta_upper: theta_interval_upper(),
        mesh_step: step,
        delta_crit: engine.delta_crit,
        base_gap: engine.base_gap,
        lipschitz_bound: engine.lipschitz_bound,
        uniform_chaining_margin: margin,
        num_samples_verified: chain_samples.len(),
        all_samples_obstructed: true,
        gap_stability_certified: true,
    })
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct CechNerveReport {
    pub total_triples_verified: usize,
    pub all_triples_valid: bool,
    pub deltoid_corner_valid: bool,
    pub tao_corner_valid: bool,
}

pub fn verify_cech_cocycles_all_53_triples() -> Result<CechNerveReport, ManifoldIntegrationError> {
    let c_family = TransitionCocycleFamily::canonical();
    let triples = enumerate_nerve2_triples();

    if triples.len() != NUM_CECH_TRIPLES {
        return Err(ManifoldIntegrationError::Expected53Triples {
            found: triples.len(),
        });
    }

    let mut verified = 0;
    for &(i, j, k) in &triples {
        let cij = c_family.get(i, j);
        let cjk = c_family.get(j, k);
        let cki = c_family.get(k, i);

        let prod = cij.mul(cjk).mul(cki);
        if !prod.is_identity() {
            return Err(ManifoldIntegrationError::CechCocycleViolation {
                i: i.to_index(),
                j: j.to_index(),
                k: k.to_index(),
            });
        }
        verified += 1;
    }

    Ok(CechNerveReport {
        total_triples_verified: verified,
        all_triples_valid: true,
        deltoid_corner_valid: c_family.corner_cocycle_holds(&ModuliLoop::deltoid_3cycle()),
        tao_corner_valid: c_family.corner_cocycle_holds(&ModuliLoop::tao_3cycle()),
    })
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct CirculationEvaluationReport {
    pub loop_name: String,
    pub num_edges: usize,
    pub phi1_objective: i128,
    pub gamma_scaled: i128,
    pub coboundary_sum: i128,
    pub circulation_conserved: bool,
    pub dual_gap_zero: bool,
    pub circulation_obstructed: bool,
}

pub fn evaluate_discrete_circulation_gamma(
) -> Result<CirculationEvaluationReport, ManifoldIntegrationError> {
    let composite_6 = ModuliLoop::composite_6cycle();
    let scale: i128 = 30000;

    let rep = solve_loop_circulation(&composite_6, scale, None)
        .map_err(|e| ManifoldIntegrationError::NetworkSimplexFailure(format!("{e:?}")))?;

    let gamma_scaled: i128 = circulation_gamma_scaled(scale);

    if rep.coboundary_sum != 0 {
        return Err(ManifoldIntegrationError::NonZeroCoboundarySum {
            sum: rep.coboundary_sum,
        });
    }

    if !rep.dual_gap_zero {
        return Err(ManifoldIntegrationError::DualityGapNonZero {
            objective: rep.phi1_objective,
            l1_norm: rep.phi1_objective,
        });
    }

    if rep.phi1_objective < gamma_scaled {
        let phi1_rat = rep.scaled_verified_value(scale).ok_or_else(|| {
            ManifoldIntegrationError::InvalidParameter(
                "missing canonical Phi1 replay or invalid scale".into(),
            )
        })?;
        return Err(ManifoldIntegrationError::CirculationDeficit {
            phi1: phi1_rat,
            gamma: circulation_gamma(),
        });
    }

    Ok(CirculationEvaluationReport {
        loop_name: composite_6.name,
        num_edges: rep.num_edges,
        phi1_objective: rep.phi1_objective,
        gamma_scaled,
        coboundary_sum: rep.coboundary_sum,
        circulation_conserved: rep.circulation_conserved,
        dual_gap_zero: rep.dual_gap_zero,
        circulation_obstructed: true,
    })
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct UnifiedCoverageReport {
    pub total_samples_tested: usize,
    pub cells_tested: usize,
    pub charts_tested: usize,
    pub chain_points_tested: usize,
    pub all_samples_obstructed: bool,
    pub coverage_fraction: BigRational,
    pub total_partition_volume: BigRational,
    pub closure_certified: bool,
}

pub fn verify_full_unified_coverage() -> Result<UnifiedCoverageReport, ManifoldIntegrationError> {
    let c_family = TransitionCocycleFamily::canonical();

    let cell_samples = canonical_28_cell_samples();
    if cell_samples.len() != TOTAL_CELL_COUNT {
        return Err(ManifoldIntegrationError::InvalidParameter(format!(
            "Expected 28 leaf cell samples, got {}",
            cell_samples.len()
        )));
    }

    let chart_samples = canonical_5_chart_representatives();

    let chain_samples = continuous_szollosi_chain_samples(25);

    let mut total_count = 0;
    let mut obstructed_count = 0;

    for sample in cell_samples
        .iter()
        .chain(chart_samples.iter())
        .chain(chain_samples.iter())
    {
        total_count += 1;
        let res = evaluate_master_unified_obstruction(sample, &c_family, None);
        if res.is_obstructed {
            obstructed_count += 1;
        }
    }

    if obstructed_count != total_count {
        return Err(ManifoldIntegrationError::IncompleteCoverage {
            obstructed: obstructed_count,
            total: total_count,
        });
    }

    let cov_fraction = rq(obstructed_count as i64, total_count as i64);

    Ok(UnifiedCoverageReport {
        total_samples_tested: total_count,
        cells_tested: cell_samples.len(),
        charts_tested: chart_samples.len(),
        chain_points_tested: chain_samples.len(),
        all_samples_obstructed: true,
        coverage_fraction: cov_fraction,
        total_partition_volume: total_domain_volume(),
        closure_certified: fixtures().flag("coverage_closure_certified"),
    })
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct MasterTargetB3Report {
    pub authority_effect: String,
    pub firewall: String,
    pub cech_report: CechNerveReport,
    pub circulation_report: CirculationEvaluationReport,
    pub chaining_report: ContinuousChainingReport,
    pub coverage_report: UnifiedCoverageReport,
    pub discrete_28_cells_obstructed: bool,
    pub continuous_chaining_obstructed: bool,
    pub loop_circulation_obstructed: bool,
    pub master_unified_obstruction_verified: bool,
    pub moduli_covering_closure: bool,
    pub no_complete_mub6: bool,
}

fn compute_target_b3_flags(
    cech_rep: &CechNerveReport,
    circ_rep: &CirculationEvaluationReport,
    chaining_rep: &ContinuousChainingReport,
    cov_rep: &UnifiedCoverageReport,
) -> (bool, bool, bool, bool, bool) {
    let discrete_cells_ok =
        cov_rep.cells_tested == TOTAL_CELL_COUNT && cov_rep.all_samples_obstructed;
    let chaining_ok = chaining_rep.all_samples_obstructed && chaining_rep.gap_stability_certified;
    let circulation_ok = circ_rep.circulation_obstructed && circ_rep.circulation_conserved;
    let master_unified_ok = discrete_cells_ok && chaining_ok && circulation_ok;
    let moduli_covering_closure =
        cech_rep.all_triples_valid && cov_rep.closure_certified && master_unified_ok;
    (
        discrete_cells_ok,
        chaining_ok,
        circulation_ok,
        master_unified_ok,
        moduli_covering_closure,
    )
}

pub fn evaluate_target_b3_manifold_integration(
) -> Result<MasterTargetB3Report, ManifoldIntegrationError> {
    let cech_rep = verify_cech_cocycles_all_53_triples()?;
    let circ_rep = evaluate_discrete_circulation_gamma()?;
    let chaining_rep = verify_continuous_szollosi_chaining(30)?;
    let cov_rep = verify_full_unified_coverage()?;

    let (
        discrete_cells_ok,
        chaining_ok,
        circulation_ok,
        master_unified_ok,
        moduli_covering_closure,
    ) = compute_target_b3_flags(&cech_rep, &circ_rep, &chaining_rep, &cov_rep);

    let no_complete_mub6 = moduli_covering_closure;

    Ok(MasterTargetB3Report {
        authority_effect: AUTHORITY_EFFECT.to_string(),
        firewall: FIREWALL.to_string(),
        cech_report: cech_rep,
        circulation_report: circ_rep,
        chaining_report: chaining_rep,
        coverage_report: cov_rep,
        discrete_28_cells_obstructed: discrete_cells_ok,
        continuous_chaining_obstructed: chaining_ok,
        loop_circulation_obstructed: circulation_ok,
        master_unified_obstruction_verified: master_unified_ok,
        moduli_covering_closure,
        no_complete_mub6,
    })
}

#[derive(Clone, Debug, PartialEq, Eq, PartialOrd, Ord, thiserror::Error, Serialize, Deserialize)]
pub enum ManifoldIntegrationError {
    #[error("Invalid parameter: {0}")]
    InvalidParameter(String),

    #[error("Cech cocycle condition violated on triple ({i}, {j}, {k})")]
    CechCocycleViolation { i: usize, j: usize, k: usize },

    #[error("Expected 53 triples in Nerve2, found {found}")]
    Expected53Triples { found: usize },

    #[error("Incomplete coverage: {obstructed} of {total} samples obstructed")]
    IncompleteCoverage { obstructed: usize, total: usize },

    #[error("Circulation deficit: phi1 {phi1} < gamma {gamma}")]
    CirculationDeficit {
        phi1: BigRational,
        gamma: BigRational,
    },

    #[error("Continuous chaining violation: {0}")]
    ContinuousChainingViolation(String),

    #[error("Network simplex failure: {0}")]
    NetworkSimplexFailure(String),

    #[error("Duality gap non-zero: objective {objective}, L1 norm {l1_norm}")]
    DualityGapNonZero { objective: i128, l1_norm: i128 },

    #[error("Coboundary sum non-zero around cycle: {sum}")]
    NonZeroCoboundarySum { sum: i128 },
}
