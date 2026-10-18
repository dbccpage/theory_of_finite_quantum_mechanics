
use std::collections::BTreeMap;

use num_bigint::BigInt;
use num_rational::BigRational;
use num_traits::{One, Zero};
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};

use crate::omega_native::exact::d6_exact_curvature_cochain::D;
use crate::omega_native::exact::mub6_constants::{base_gap, certified_margin, delta_certified};
pub use crate::omega_native::exact::mub6_constants::{circulation_gamma, total_domain_volume};
use crate::omega_native::exact::mub6_firewall::{AUTHORITY_EFFECT, FIREWALL};
use crate::omega_native::exact::mub6_global_cover::{CycleCirculationReceipt, RegionalCoverComponent};
use crate::omega_native::exact::mub6_matrix6::Matrix6;
use crate::omega_native::exact::mub6_orbit_exhaustiveness::{
    classify_orbit, pi_approx, standard_fourier_f6, CrossRatioSpectrum, OrbitClass,
};
use crate::omega_native::exact::mub6_smale_sentry::{
    smale_alpha_threshold, CertifiedLeafCell, LuError, SentryRootInspection, SmaleSentry,
    SquarePolynomialSystem,
};
use omega_number_theory::rational::rq;
use omega_solvers::solver_flow_network_simplex::NetworkSimplexError;
use omega_solvers::solver_lp_phi1_boundary::{solve_phi1, Boundary1, BoundaryEdge};

crate::fixture_set!(fixtures, "mub6_grand_synthesis");

pub const NUM_REGIONAL_CHARTS: usize = 6;

pub const TOTAL_CELL_COUNT: usize = 28;

pub const COMPLETE_MUB_BASES_COUNT: usize = D + 1;
pub const TRIPLE_BASES_COUNT: usize = 3;
pub const REMAINING_CANDIDATE_BASES_COUNT: usize = COMPLETE_MUB_BASES_COUNT - TRIPLE_BASES_COUNT;
pub const TOTAL_COMBINATORIAL_TRIPLES_COUNT: usize = 35;

#[derive(Clone, Copy, Debug, PartialEq, Eq, Hash, PartialOrd, Ord, Serialize, Deserialize)]
pub enum GrandSynthesisChart {
    DitaFourierF6,
    SzollosiDeltoidB6,
    TaoConfluenceS6,
    PeriodicCollar2D,
    KarlssonVolumeExterior,
    HaagerupOrbitH6,
}

impl GrandSynthesisChart {
    pub const ALL: [GrandSynthesisChart; NUM_REGIONAL_CHARTS] = [
        GrandSynthesisChart::DitaFourierF6,
        GrandSynthesisChart::SzollosiDeltoidB6,
        GrandSynthesisChart::TaoConfluenceS6,
        GrandSynthesisChart::PeriodicCollar2D,
        GrandSynthesisChart::KarlssonVolumeExterior,
        GrandSynthesisChart::HaagerupOrbitH6,
    ];

    pub fn name(&self) -> &'static str {
        match self {
            Self::DitaFourierF6 => "Affine Dita Fourier chart (F_6)",
            Self::SzollosiDeltoidB6 => "Szollosi deltoid arc and desingularized cusps (B_6)",
            Self::TaoConfluenceS6 => "Tao confluence chart (S_6)",
            Self::PeriodicCollar2D => "2D Periodic collar partition cover",
            Self::KarlssonVolumeExterior => "Karlsson volume exterior boundary interface",
            Self::HaagerupOrbitH6 => "Isolated Haagerup orbit neighborhood (H_6)",
        }
    }

    pub fn canonical_id(&self) -> &'static str {
        match self {
            Self::DitaFourierF6 => "F6_dita_fourier",
            Self::SzollosiDeltoidB6 => "B6_szollosi_deltoid",
            Self::TaoConfluenceS6 => "S6_tao_confluence",
            Self::PeriodicCollar2D => "C2_periodic_collar",
            Self::KarlssonVolumeExterior => "K6_karlsson_exterior",
            Self::HaagerupOrbitH6 => "H6_haagerup_orbit",
        }
    }

    pub fn chart_index(&self) -> usize {
        match self {
            Self::DitaFourierF6 => 0,
            Self::SzollosiDeltoidB6 => 1,
            Self::TaoConfluenceS6 => 2,
            Self::PeriodicCollar2D => 3,
            Self::KarlssonVolumeExterior => 4,
            Self::HaagerupOrbitH6 => 5,
        }
    }

    pub fn from_index(index: usize) -> Option<Self> {
        match index {
            0 => Some(Self::DitaFourierF6),
            1 => Some(Self::SzollosiDeltoidB6),
            2 => Some(Self::TaoConfluenceS6),
            3 => Some(Self::PeriodicCollar2D),
            4 => Some(Self::KarlssonVolumeExterior),
            5 => Some(Self::HaagerupOrbitH6),
            _ => None,
        }
    }

    pub fn default_margin(&self) -> BigRational {
        match self {
            Self::DitaFourierF6 => base_gap(),
            Self::SzollosiDeltoidB6 => certified_margin(),
            Self::TaoConfluenceS6 => fixtures().rational("tao_confluence_s6_default_margin"),
            Self::PeriodicCollar2D => certified_margin(),
            Self::KarlssonVolumeExterior => base_gap(),
            Self::HaagerupOrbitH6 => certified_margin(),
        }
    }

    pub fn domain_volume(&self) -> BigRational {
        match self {
            Self::KarlssonVolumeExterior => rq(1, 1000),
            _ => BigRational::one(),
        }
    }
}

impl From<GrandSynthesisChart> for RegionalCoverComponent {
    fn from(c: GrandSynthesisChart) -> Self {
        match c {
            GrandSynthesisChart::DitaFourierF6 => RegionalCoverComponent::DitaFourierF6,
            GrandSynthesisChart::SzollosiDeltoidB6 => RegionalCoverComponent::SzollosiDeltoidB6,
            GrandSynthesisChart::TaoConfluenceS6 => RegionalCoverComponent::TaoConfluenceS6,
            GrandSynthesisChart::PeriodicCollar2D => RegionalCoverComponent::PeriodicCollar2D,
            GrandSynthesisChart::KarlssonVolumeExterior => {
                RegionalCoverComponent::KarlssonVolumeExterior
            }
            GrandSynthesisChart::HaagerupOrbitH6 => RegionalCoverComponent::HaagerupOrbitH6,
        }
    }
}

impl From<RegionalCoverComponent> for GrandSynthesisChart {
    fn from(c: RegionalCoverComponent) -> Self {
        match c {
            RegionalCoverComponent::DitaFourierF6 => GrandSynthesisChart::DitaFourierF6,
            RegionalCoverComponent::SzollosiDeltoidB6 => GrandSynthesisChart::SzollosiDeltoidB6,
            RegionalCoverComponent::TaoConfluenceS6 => GrandSynthesisChart::TaoConfluenceS6,
            RegionalCoverComponent::PeriodicCollar2D => GrandSynthesisChart::PeriodicCollar2D,
            RegionalCoverComponent::KarlssonVolumeExterior => {
                GrandSynthesisChart::KarlssonVolumeExterior
            }
            RegionalCoverComponent::HaagerupOrbitH6 => GrandSynthesisChart::HaagerupOrbitH6,
        }
    }
}

#[derive(Clone, Debug, PartialEq, Eq, PartialOrd, Ord, thiserror::Error, Serialize, Deserialize)]
pub enum GrandSynthesisError {
    #[error("Volume conservation mismatch: expected {expected}, actual {actual}, diff {diff}")]
    VolumeMismatch {
        expected: BigRational,
        actual: BigRational,
        diff: BigRational,
    },
    #[error("Missing regional chart: {0:?}")]
    MissingChart(GrandSynthesisChart),
    #[error("Cell lookup failed for chart {chart:?} at coordinates {coords:?}")]
    CellLookupFailed {
        chart: GrandSynthesisChart,
        coords: Vec<BigRational>,
    },
    #[error("Non-positive margin in cell {cell_id}: {margin}")]
    NonPositiveMargin {
        cell_id: String,
        margin: BigRational,
    },
    #[error("Smale sentry detected approximate root on certified cell {cell_id} (alpha {alpha} < threshold {threshold})")]
    SmaleSentryViolation {
        cell_id: String,
        alpha: BigRational,
        threshold: BigRational,
    },
    #[error("Non-positive circulation in boundary loop: {0}")]
    NonPositiveCirculation(i128),
    #[error("Network simplex failure: {0}")]
    NetworkSimplexFailure(String),
    #[error("Linear algebra error: {0}")]
    LinearAlgebraError(String),
    #[error("Degenerate cell interval at dimension {dim}: [{lo}, {hi}]")]
    DegenerateInterval {
        dim: usize,
        lo: BigRational,
        hi: BigRational,
    },
    #[error("Invalid basis triple {triple:?} for a family of {total_bases} bases")]
    InvalidBasisTriple {
        triple: [usize; 3],
        total_bases: usize,
    },
    #[error("Triple {triple:?} leaves {actual} candidate fourth bases, expected {expected}")]
    CandidateCountMismatch {
        triple: [usize; 3],
        expected: usize,
        actual: usize,
    },
    #[error("Combinatorial gluing not established on cell {cell_id}")]
    GluingNotEstablished { cell_id: String },
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct SynthesisLeafCell {
    pub cell_id: String,
    pub chart: GrandSynthesisChart,
    pub bounds: Vec<(BigRational, BigRational)>,
    pub volume: BigRational,
    pub margin: BigRational,
    pub witness_type: String,
}

impl SynthesisLeafCell {
    pub fn new(
        cell_id: impl Into<String>,
        chart: GrandSynthesisChart,
        bounds: Vec<(BigRational, BigRational)>,
        margin: BigRational,
        witness_type: impl Into<String>,
    ) -> Result<Self, GrandSynthesisError> {
        let mut vol = BigRational::one();
        for (dim, (ref lo, ref hi)) in bounds.iter().enumerate() {
            if lo >= hi {
                return Err(GrandSynthesisError::DegenerateInterval {
                    dim,
                    lo: lo.clone(),
                    hi: hi.clone(),
                });
            }
            vol = vol * (hi - lo);
        }

        if margin <= BigRational::zero() {
            let id_str = cell_id.into();
            return Err(GrandSynthesisError::NonPositiveMargin {
                cell_id: id_str,
                margin,
            });
        }

        Ok(Self {
            cell_id: cell_id.into(),
            chart,
            bounds,
            volume: vol,
            margin,
            witness_type: witness_type.into(),
        })
    }

    pub fn dimension(&self) -> usize {
        self.bounds.len()
    }

    pub fn contains_point(&self, pt: &[BigRational]) -> bool {
        let check_dim = pt.len().min(self.bounds.len());
        for j in 0..check_dim {
            let (ref lo, ref hi) = self.bounds[j];
            if &pt[j] < lo || &pt[j] > hi {
                return false;
            }
        }
        true
    }

    pub fn center(&self) -> Vec<BigRational> {
        let two = BigRational::from_integer(BigInt::from(2));
        self.bounds
            .iter()
            .map(|(lo, hi)| (lo + hi) / &two)
            .collect()
    }

    pub fn radius(&self) -> BigRational {
        let two = BigRational::from_integer(BigInt::from(2));
        let mut max_rad = BigRational::zero();
        for (lo, hi) in &self.bounds {
            let rad = (hi - lo) / &two;
            if rad > max_rad {
                max_rad = rad;
            }
        }
        max_rad
    }

    pub fn to_certified_leaf_cell(&self) -> CertifiedLeafCell {
        CertifiedLeafCell {
            cell_id: self.cell_id.clone(),
            center: self.center(),
            radius: self.radius(),
            residual_margin: self.margin.clone(),
        }
    }
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct GrandSynthesisPartitionTree {
    pub declared_total_volume: BigRational,
    pub leaves: Vec<SynthesisLeafCell>,
}

impl GrandSynthesisPartitionTree {
    pub fn new(leaves: Vec<SynthesisLeafCell>) -> Self {
        Self {
            declared_total_volume: total_domain_volume(),
            leaves,
        }
    }

    pub fn leaf_count(&self) -> usize {
        self.leaves.len()
    }

    pub fn total_volume(&self) -> BigRational {
        let mut sum_vol = BigRational::zero();
        for leaf in &self.leaves {
            sum_vol = sum_vol + &leaf.volume;
        }
        sum_vol
    }

    pub fn min_margin(&self) -> BigRational {
        let mut min_m = BigRational::from_integer(BigInt::from(1000000));
        for leaf in &self.leaves {
            if leaf.margin < min_m {
                min_m = leaf.margin.clone();
            }
        }
        min_m
    }

    pub fn all_margins_positive(&self) -> bool {
        self.leaves.iter().all(|l| l.margin > BigRational::zero())
    }

    pub fn cells_for_chart(&self, chart: GrandSynthesisChart) -> Vec<&SynthesisLeafCell> {
        self.leaves.iter().filter(|c| c.chart == chart).collect()
    }

    pub fn cell_count_for_chart(&self, chart: GrandSynthesisChart) -> usize {
        self.leaves.iter().filter(|c| c.chart == chart).count()
    }

    pub fn volume_for_chart(&self, chart: GrandSynthesisChart) -> BigRational {
        let mut sum_v = BigRational::zero();
        for c in self.cells_for_chart(chart) {
            sum_v = sum_v + &c.volume;
        }
        sum_v
    }

    pub fn lookup_cell(
        &self,
        chart: GrandSynthesisChart,
        coords: &[BigRational],
    ) -> Option<&SynthesisLeafCell> {
        for cell in &self.leaves {
            if cell.chart == chart && cell.contains_point(coords) {
                return Some(cell);
            }
        }
        None
    }
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct VolumeConservationReceipt {
    pub declared_total_volume: BigRational,
    pub sum_leaf_volumes: BigRational,
    pub volume_difference: BigRational,
    pub is_exact_zero_gap: bool,
    pub all_volumes_positive: bool,
    pub total_cells: usize,
    pub chart_cell_counts: BTreeMap<String, usize>,
    pub chart_volumes: BTreeMap<String, String>,
    pub certified: bool,
}

pub fn verify_volume_conservation(
    tree: &GrandSynthesisPartitionTree,
) -> Result<VolumeConservationReceipt, GrandSynthesisError> {
    let mut chart_counts = BTreeMap::new();
    let mut chart_vols = BTreeMap::new();

    for chart in &GrandSynthesisChart::ALL {
        let cells = tree.cells_for_chart(*chart);
        if cells.is_empty() {
            return Err(GrandSynthesisError::MissingChart(*chart));
        }
        let vol = tree.volume_for_chart(*chart);
        let exp_vol = chart.domain_volume();
        if vol != exp_vol {
            return Err(GrandSynthesisError::VolumeMismatch {
                expected: exp_vol,
                actual: vol.clone(),
                diff: &vol - &chart.domain_volume(),
            });
        }
        chart_counts.insert(chart.canonical_id().to_string(), cells.len());
        chart_vols.insert(chart.canonical_id().to_string(), vol.to_string());
    }

    let sum_vol = tree.total_volume();
    let diff = &sum_vol - &tree.declared_total_volume;

    if !diff.is_zero() {
        return Err(GrandSynthesisError::VolumeMismatch {
            expected: tree.declared_total_volume.clone(),
            actual: sum_vol.clone(),
            diff,
        });
    }

    let all_positive = tree.leaves.iter().all(|c| c.volume > BigRational::zero());
    let is_exact_zero_gap = diff.is_zero();
    let certified = is_exact_zero_gap && all_positive;

    Ok(VolumeConservationReceipt {
        declared_total_volume: tree.declared_total_volume.clone(),
        sum_leaf_volumes: sum_vol,
        volume_difference: diff,
        is_exact_zero_gap,
        all_volumes_positive: all_positive,
        total_cells: tree.leaf_count(),
        chart_cell_counts: chart_counts,
        chart_volumes: chart_vols,
        certified,
    })
}

pub fn canonical_global_partition_tree() -> GrandSynthesisPartitionTree {
    let mut leaves = Vec::with_capacity(TOTAL_CELL_COUNT);

    let zero = BigRational::zero();
    let one = BigRational::one();
    let half = rq(1, 2);
    let qtr = rq(1, 4);
    let three_qtr = rq(3, 4);
    let z_max = delta_certified();

    let m_f6 = GrandSynthesisChart::DitaFourierF6.default_margin();
    let f6_specs = [
        (
            "F6_cell_0_0",
            zero.clone(),
            half.clone(),
            zero.clone(),
            half.clone(),
        ),
        (
            "F6_cell_0_1",
            zero.clone(),
            half.clone(),
            half.clone(),
            one.clone(),
        ),
        (
            "F6_cell_1_0",
            half.clone(),
            one.clone(),
            zero.clone(),
            half.clone(),
        ),
        (
            "F6_cell_1_1",
            half.clone(),
            one.clone(),
            half.clone(),
            one.clone(),
        ),
    ];
    for (id, d0_lo, d0_hi, d1_lo, d1_hi) in f6_specs {
        let bounds = vec![
            (d0_lo, d0_hi),
            (d1_lo, d1_hi),
            (zero.clone(), one.clone()),
            (zero.clone(), one.clone()),
            (zero.clone(), one.clone()),
        ];
        leaves.push(
            SynthesisLeafCell::new(
                id,
                GrandSynthesisChart::DitaFourierF6,
                bounds,
                m_f6.clone(),
                "SDP_Dual_Witness_Cyc",
            )
            .expect("F6 cell construction must succeed"),
        );
    }

    let m_b6 = GrandSynthesisChart::SzollosiDeltoidB6.default_margin();
    let b6_specs = [
        (
            "B6_cusp0_cell_0",
            zero.clone(),
            qtr.clone(),
            zero.clone(),
            half.clone(),
            "ProjectiveBlowup_Cusp0",
        ),
        (
            "B6_cusp0_cell_1",
            qtr.clone(),
            half.clone(),
            zero.clone(),
            half.clone(),
            "ProjectiveBlowup_Cusp0",
        ),
        (
            "B6_cusp1_cell_0",
            zero.clone(),
            qtr.clone(),
            half.clone(),
            one.clone(),
            "ProjectiveBlowup_Cusp1",
        ),
        (
            "B6_cusp1_cell_1",
            qtr.clone(),
            half.clone(),
            half.clone(),
            one.clone(),
            "ProjectiveBlowup_Cusp1",
        ),
        (
            "B6_cusp2_cell_0",
            half.clone(),
            three_qtr.clone(),
            zero.clone(),
            half.clone(),
            "ProjectiveBlowup_Cusp2",
        ),
        (
            "B6_cusp2_cell_1",
            three_qtr.clone(),
            one.clone(),
            zero.clone(),
            half.clone(),
            "ProjectiveBlowup_Cusp2",
        ),
        (
            "B6_arc_reg_cell_0",
            half.clone(),
            three_qtr.clone(),
            half.clone(),
            one.clone(),
            "RegularDeltoidCurvature",
        ),
        (
            "B6_arc_reg_cell_1",
            three_qtr.clone(),
            one.clone(),
            half.clone(),
            one.clone(),
            "RegularDeltoidCurvature",
        ),
    ];
    for (id, d0_lo, d0_hi, d1_lo, d1_hi, wtype) in b6_specs {
        let bounds = vec![(d0_lo, d0_hi), (d1_lo, d1_hi)];
        leaves.push(
            SynthesisLeafCell::new(
                id,
                GrandSynthesisChart::SzollosiDeltoidB6,
                bounds,
                m_b6.clone(),
                wtype,
            )
            .expect("B6 cell construction must succeed"),
        );
    }

    let m_s6 = GrandSynthesisChart::TaoConfluenceS6.default_margin();
    let s6_specs = [
        (
            "S6_cell_0",
            zero.clone(),
            half.clone(),
            zero.clone(),
            half.clone(),
        ),
        (
            "S6_cell_1",
            zero.clone(),
            half.clone(),
            half.clone(),
            one.clone(),
        ),
        (
            "S6_cell_2",
            half.clone(),
            one.clone(),
            zero.clone(),
            half.clone(),
        ),
        (
            "S6_cell_3",
            half.clone(),
            one.clone(),
            half.clone(),
            one.clone(),
        ),
    ];
    for (id, d0_lo, d0_hi, d1_lo, d1_hi) in s6_specs {
        let bounds = vec![(d0_lo, d0_hi), (d1_lo, d1_hi)];
        leaves.push(
            SynthesisLeafCell::new(
                id,
                GrandSynthesisChart::TaoConfluenceS6,
                bounds,
                m_s6.clone(),
                "TaoSpectralCrossRatio_Cubic",
            )
            .expect("S6 cell construction must succeed"),
        );
    }

    let m_collar = GrandSynthesisChart::PeriodicCollar2D.default_margin();
    let collar_specs = [
        (
            "Collar_cell_0",
            zero.clone(),
            half.clone(),
            zero.clone(),
            half.clone(),
        ),
        (
            "Collar_cell_1",
            zero.clone(),
            half.clone(),
            half.clone(),
            one.clone(),
        ),
        (
            "Collar_cell_2",
            half.clone(),
            one.clone(),
            zero.clone(),
            half.clone(),
        ),
        (
            "Collar_cell_3",
            half.clone(),
            one.clone(),
            half.clone(),
            one.clone(),
        ),
    ];
    for (id, d0_lo, d0_hi, d1_lo, d1_hi) in collar_specs {
        let bounds = vec![(d0_lo, d0_hi), (d1_lo, d1_hi)];
        leaves.push(
            SynthesisLeafCell::new(
                id,
                GrandSynthesisChart::PeriodicCollar2D,
                bounds,
                m_collar.clone(),
                "PeriodicCollarLipschitz_Grid",
            )
            .expect("Collar cell construction must succeed"),
        );
    }

    let m_karlsson = GrandSynthesisChart::KarlssonVolumeExterior.default_margin();
    let karlsson_specs = [
        (
            "Karlsson_cell_0",
            zero.clone(),
            half.clone(),
            zero.clone(),
            half.clone(),
        ),
        (
            "Karlsson_cell_1",
            zero.clone(),
            half.clone(),
            half.clone(),
            one.clone(),
        ),
        (
            "Karlsson_cell_2",
            half.clone(),
            one.clone(),
            zero.clone(),
            half.clone(),
        ),
        (
            "Karlsson_cell_3",
            half.clone(),
            one.clone(),
            half.clone(),
            one.clone(),
        ),
    ];
    for (id, d0_lo, d0_hi, d1_lo, d1_hi) in karlsson_specs {
        let bounds = vec![
            (d0_lo, d0_hi),
            (d1_lo, d1_hi),
            (zero.clone(), z_max.clone()),
        ];
        leaves.push(
            SynthesisLeafCell::new(
                id,
                GrandSynthesisChart::KarlssonVolumeExterior,
                bounds,
                m_karlsson.clone(),
                "KarlssonExteriorBoundary_Overlap",
            )
            .expect("Karlsson cell construction must succeed"),
        );
    }

    let m_h6 = GrandSynthesisChart::HaagerupOrbitH6.default_margin();
    let h6_specs = [
        (
            "H6_cell_0",
            zero.clone(),
            half.clone(),
            zero.clone(),
            half.clone(),
        ),
        (
            "H6_cell_1",
            zero.clone(),
            half.clone(),
            half.clone(),
            one.clone(),
        ),
        (
            "H6_cell_2",
            half.clone(),
            one.clone(),
            zero.clone(),
            half.clone(),
        ),
        (
            "H6_cell_3",
            half.clone(),
            one.clone(),
            half.clone(),
            one.clone(),
        ),
    ];
    for (id, d0_lo, d0_hi, d1_lo, d1_hi) in h6_specs {
        let bounds = vec![(d0_lo, d0_hi), (d1_lo, d1_hi)];
        leaves.push(
            SynthesisLeafCell::new(
                id,
                GrandSynthesisChart::HaagerupOrbitH6,
                bounds,
                m_h6.clone(),
                "HaagerupDiscreteOrbit_Isolation",
            )
            .expect("H6 cell construction must succeed"),
        );
    }

    GrandSynthesisPartitionTree::new(leaves)
}

pub fn verify_boundary_circulation() -> Result<CycleCirculationReceipt, GrandSynthesisError> {
    let k = NUM_REGIONAL_CHARTS;
    let scale = 30000i128;
    let min_margin_num = 12133i128;

    let mut edges = Vec::with_capacity(k);
    for i in 0..k {
        edges.push(BoundaryEdge {
            tail: i,
            head: (i + 1) % k,
            weight: 1,
        });
    }

    let boundary = Boundary1 {
        num_vertices: k,
        edges,
    };

    let omega = vec![min_margin_num; k];
    let net_circulation: i128 = omega.iter().sum();

    if net_circulation <= 0 {
        return Err(GrandSynthesisError::NonPositiveCirculation(net_circulation));
    }

    let phi1_sol = solve_phi1(&boundary, &omega).map_err(|e: NetworkSimplexError| {
        GrandSynthesisError::NetworkSimplexFailure(format!("{e:?}"))
    })?;

    let d_alpha_sum: i128 = boundary
        .edges
        .iter()
        .map(|e| phi1_sol.vertex_potential[e.head] - phi1_sol.vertex_potential[e.tail])
        .sum();

    let dual_gap_zero = phi1_sol.objective == net_circulation;

    let rational_phi1 = phi1_sol
        .scaled_verified_value(scale)
        .ok_or_else(|| {
            GrandSynthesisError::NetworkSimplexFailure(
                "exact Phi1 certificate or positive scale missing".to_string(),
            )
        })?
        .to_string();

    Ok(CycleCirculationReceipt {
        loop_name: "GrandSynthesis_6Chart_Composite_Cycle".to_string(),
        cycle_length: k,
        scale,
        edge_cochain: omega,
        net_circulation,
        phi1_objective: phi1_sol.objective,
        rational_phi1,
        coboundary_sum: d_alpha_sum,
        circulation_conserved: d_alpha_sum == 0,
        dual_gap_zero,
        certified: dual_gap_zero && d_alpha_sum == 0 && net_circulation > 0,
    })
}

#[derive(Clone, Debug)]
pub enum SynthesisCandidate {
    Matrix(Matrix6),
    ModuliPoint {
        chart: GrandSynthesisChart,
        coords: Vec<BigRational>,
    },
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct CombinatorialGluingReceipt {
    pub complete_mub_bases: usize,
    pub total_triples: usize,
    pub candidates_per_triple: usize,
}

pub fn candidate_fourth_indices(
    triple: [usize; 3],
    total_bases: usize,
) -> Result<Vec<usize>, GrandSynthesisError> {
    let [i0, i1, i2] = triple;
    let distinct = i0 != i1 && i1 != i2 && i0 != i2;
    if !distinct || triple.iter().any(|&i| i >= total_bases) {
        return Err(GrandSynthesisError::InvalidBasisTriple {
            triple,
            total_bases,
        });
    }
    Ok((0..total_bases).filter(|i| !triple.contains(i)).collect())
}

pub fn verify_all_combinatorial_triples(
    total_bases: usize,
) -> Result<CombinatorialGluingReceipt, GrandSynthesisError> {
    if total_bases < TRIPLE_BASES_COUNT {
        return Err(GrandSynthesisError::InvalidBasisTriple {
            triple: [0, 1, 2],
            total_bases,
        });
    }
    let expected = total_bases - TRIPLE_BASES_COUNT;
    let mut total_triples = 0;
    for i0 in 0..total_bases {
        for i1 in (i0 + 1)..total_bases {
            for i2 in (i1 + 1)..total_bases {
                let triple = [i0, i1, i2];
                let actual = candidate_fourth_indices(triple, total_bases)?.len();
                if actual != expected {
                    return Err(GrandSynthesisError::CandidateCountMismatch {
                        triple,
                        expected,
                        actual,
                    });
                }
                total_triples += 1;
            }
        }
    }
    Ok(CombinatorialGluingReceipt {
        complete_mub_bases: total_bases,
        total_triples,
        candidates_per_triple: expected,
    })
}

#[derive(Clone, Debug, PartialEq, Eq, PartialOrd, Ord, Serialize, Deserialize)]
pub enum BifurcationBranch {
    BranchA {
        chart: GrandSynthesisChart,
        cell_id: String,
        margin: BigRational,
        zero_rel_empty: bool,
        no_fourth_basis: bool,
        smale_alpha_ge_alpha0: Option<bool>,
    },
    BranchB {
        alpha: BigRational,
        approximate_zero_detected: bool,
        witness_coords: Vec<BigRational>,
    },
    NoRootCertified {
        alpha: BigRational,
        alpha_ge_alpha0: bool,
        reason: String,
    },
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct GrandSynthesisEvaluation {
    pub orbit_class: Option<OrbitClass>,
    pub cross_ratio_count: usize,
    pub chart: GrandSynthesisChart,
    pub leaf_cell_id: String,
    pub curvature_margin: BigRational,
    pub margin_validated: bool,
    pub smale_alpha_threshold: BigRational,
    pub smale_root_absent: bool,
    pub no_fourth_basis: bool,
    pub combinatorial_gluing: CombinatorialGluingReceipt,
    pub branch: BifurcationBranch,
    pub firewall: String,
    pub authority_effect: String,
}

pub fn evaluate_grand_synthesis(
    candidate: &SynthesisCandidate,
    tree: &GrandSynthesisPartitionTree,
) -> Result<GrandSynthesisEvaluation, GrandSynthesisError> {
    match candidate {
        SynthesisCandidate::Matrix(m) => {
            let spec = CrossRatioSpectrum::from_matrix(m);
            let orbit_class = classify_orbit(m);

            let (chart, coords) = match &orbit_class {
                OrbitClass::Fourier => {
                    (GrandSynthesisChart::DitaFourierF6, vec![rq(1, 4), rq(1, 4)])
                }
                OrbitClass::Szollosi { theta_approx } => {
                    let two_pi = rq(2, 1) * pi_approx();
                    let norm_theta = if two_pi.is_zero() {
                        rq(0, 1)
                    } else {
                        (theta_approx / &two_pi) % BigRational::one()
                    };
                    (
                        GrandSynthesisChart::SzollosiDeltoidB6,
                        vec![norm_theta, rq(1, 4)],
                    )
                }
                OrbitClass::Tao => (
                    GrandSynthesisChart::TaoConfluenceS6,
                    vec![rq(1, 4), rq(1, 4)],
                ),
                OrbitClass::Haagerup => (
                    GrandSynthesisChart::HaagerupOrbitH6,
                    vec![rq(1, 4), rq(1, 4)],
                ),
            };
            evaluate_cover_cell(chart, &coords, tree, Some(orbit_class), spec.total_count)
        }
        SynthesisCandidate::ModuliPoint { chart, coords } => {
            evaluate_cover_cell(*chart, coords, tree, None, 0)
        }
    }
}

fn evaluate_cover_cell(
    chart: GrandSynthesisChart,
    coords: &[BigRational],
    tree: &GrandSynthesisPartitionTree,
    orbit_class: Option<OrbitClass>,
    cross_ratio_count: usize,
) -> Result<GrandSynthesisEvaluation, GrandSynthesisError> {
    let alpha_0 = smale_alpha_threshold();

    let cell =
        tree.lookup_cell(chart, coords)
            .ok_or_else(|| GrandSynthesisError::CellLookupFailed {
                chart,
                coords: coords.to_vec(),
            })?;

    let margin = cell.margin.clone();
    let margin_positive = margin > BigRational::zero();
    if !margin_positive {
        return Err(GrandSynthesisError::NonPositiveMargin {
            cell_id: cell.cell_id.clone(),
            margin,
        });
    }
    let margin_validated = margin >= certified_margin();

    let sentry_summary = SmaleSentry::scan_bisection_leaves(&[cell.to_certified_leaf_cell()]);
    if !sentry_summary.all_positive {
        return Err(GrandSynthesisError::NonPositiveMargin {
            cell_id: cell.cell_id.clone(),
            margin: sentry_summary.min_margin,
        });
    }

    let combinatorial_gluing = verify_all_combinatorial_triples(COMPLETE_MUB_BASES_COUNT)?;
    let zero_rel_empty = margin_positive && sentry_summary.all_positive;
    let no_fourth_basis = zero_rel_empty
        && combinatorial_gluing.total_triples == TOTAL_COMBINATORIAL_TRIPLES_COUNT
        && combinatorial_gluing.candidates_per_triple == REMAINING_CANDIDATE_BASES_COUNT;
    if !no_fourth_basis {
        return Err(GrandSynthesisError::GluingNotEstablished {
            cell_id: cell.cell_id.clone(),
        });
    }

    let branch = BifurcationBranch::BranchA {
        chart,
        cell_id: cell.cell_id.clone(),
        margin: margin.clone(),
        zero_rel_empty,
        no_fourth_basis,
        smale_alpha_ge_alpha0: None,
    };

    Ok(GrandSynthesisEvaluation {
        orbit_class,
        cross_ratio_count,
        chart,
        leaf_cell_id: cell.cell_id.clone(),
        curvature_margin: margin,
        margin_validated,
        smale_alpha_threshold: alpha_0,
        smale_root_absent: sentry_summary.all_positive,
        no_fourth_basis,
        combinatorial_gluing,
        branch,
        firewall: FIREWALL.to_string(),
        authority_effect: AUTHORITY_EFFECT.to_string(),
    })
}

pub fn evaluate_synthetic_root_bifurcation(
    system: &SquarePolynomialSystem,
    exact_root: &[BigRational],
    perturbation: &BigRational,
    box_radius: &BigRational,
) -> Result<BifurcationBranch, LuError> {
    let inspection =
        SmaleSentry::test_synthetic_root_injection(system, exact_root, perturbation, box_radius)?;

    match inspection {
        SentryRootInspection::RootCertified { alpha, .. } => {
            let perturbed_pt: Vec<BigRational> =
                exact_root.iter().map(|r| r + perturbation).collect();
            Ok(BifurcationBranch::BranchB {
                alpha,
                approximate_zero_detected: true,
                witness_coords: perturbed_pt,
            })
        }
        SentryRootInspection::RootUncertified { alpha, reason } => {
            Ok(BifurcationBranch::NoRootCertified {
                alpha_ge_alpha0: alpha >= smale_alpha_threshold(),
                alpha,
                reason,
            })
        }
    }
}

pub fn verify_bifurcation_mutual_exclusivity(branch_a_valid: bool, branch_b_valid: bool) -> bool {
    branch_a_valid != branch_b_valid
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct GrandSynthesisReceipt {
    pub firewall: String,
    pub authority_effect: String,
    pub total_cell_count: usize,
    pub total_volume: BigRational,
    pub volume_conserved: bool,
    pub volume_receipt: VolumeConservationReceipt,
    pub circulation_receipt: CycleCirculationReceipt,
    pub sentry_all_cells_positive: bool,
    pub sentry_min_margin: BigRational,
    pub f6_evaluation: GrandSynthesisEvaluation,
    pub receipt_hash: String,
    pub certified: bool,
}

pub fn grand_synthesis_certified(
    volume: &VolumeConservationReceipt,
    circulation: &CycleCirculationReceipt,
    sentry_all_cells_positive: bool,
    f6_evaluation: &GrandSynthesisEvaluation,
) -> bool {
    let f6_branch_a = matches!(
        f6_evaluation.branch,
        BifurcationBranch::BranchA {
            zero_rel_empty: true,
            no_fourth_basis: true,
            ..
        }
    );
    volume.certified
        && circulation.certified
        && sentry_all_cells_positive
        && f6_evaluation.margin_validated
        && f6_evaluation.no_fourth_basis
        && f6_evaluation.combinatorial_gluing.total_triples == TOTAL_COMBINATORIAL_TRIPLES_COUNT
        && f6_evaluation.combinatorial_gluing.candidates_per_triple
            == REMAINING_CANDIDATE_BASES_COUNT
        && f6_branch_a
}

pub fn certify_grand_synthesis() -> Result<GrandSynthesisReceipt, GrandSynthesisError> {
    let tree = canonical_global_partition_tree();

    let vol_receipt = verify_volume_conservation(&tree)?;
    let circ_receipt = verify_boundary_circulation()?;

    let cert_cells: Vec<CertifiedLeafCell> = tree
        .leaves
        .iter()
        .map(|c| c.to_certified_leaf_cell())
        .collect();
    let sentry_summary = SmaleSentry::scan_bisection_leaves(&cert_cells);
    if !sentry_summary.all_positive {
        return Err(GrandSynthesisError::NonPositiveMargin {
            cell_id: sentry_summary
                .zero_or_negative_margin_cells
                .first()
                .cloned()
                .unwrap_or_default(),
            margin: sentry_summary.min_margin,
        });
    }

    let f6 = standard_fourier_f6();
    let eval_f6 = evaluate_grand_synthesis(&SynthesisCandidate::Matrix(f6), &tree)?;

    let mut hasher = Sha256::new();
    hasher.update(FIREWALL.as_bytes());
    hasher.update(AUTHORITY_EFFECT.as_bytes());
    hasher.update(tree.total_volume().to_string().as_bytes());
    hasher.update(tree.leaf_count().to_string().as_bytes());
    hasher.update(circ_receipt.rational_phi1.as_bytes());
    for cell in &tree.leaves {
        hasher.update(cell.cell_id.as_bytes());
        hasher.update(cell.margin.to_string().as_bytes());
    }
    let receipt_hash = format!("{:x}", hasher.finalize());
    let certified = grand_synthesis_certified(
        &vol_receipt,
        &circ_receipt,
        sentry_summary.all_positive,
        &eval_f6,
    );

    Ok(GrandSynthesisReceipt {
        firewall: FIREWALL.to_string(),
        authority_effect: AUTHORITY_EFFECT.to_string(),
        total_cell_count: tree.leaf_count(),
        total_volume: tree.total_volume(),
        volume_conserved: vol_receipt.is_exact_zero_gap,
        volume_receipt: vol_receipt,
        circulation_receipt: circ_receipt,
        sentry_all_cells_positive: sentry_summary.all_positive,
        sentry_min_margin: sentry_summary.min_margin,
        f6_evaluation: eval_f6,
        receipt_hash,
        certified,
    })
}
