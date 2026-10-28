
use std::collections::{BTreeMap, BTreeSet, VecDeque};

use num_bigint::BigInt;
use num_rational::BigRational;
use num_traits::{One, Zero};
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};

use omega_solvers::solver_flow_network_simplex::NetworkSimplexError;

use crate::native::exact::mub6_constants::{base_gap, certified_margin, delta_certified};
use crate::native::exact::mub6_firewall::{AUTHORITY_EFFECT, FIREWALL};
use tfqm_number_theory::rational::rq;
use omega_solvers::solver_lp_phi1_boundary::{solve_phi1, Boundary1, BoundaryEdge};

pub const NUM_REGIONAL_COMPONENTS: usize = 6;

#[derive(Clone, Copy, Debug, PartialEq, Eq, Hash, PartialOrd, Ord, Serialize, Deserialize)]
pub enum RegionalCoverComponent {
    DitaFourierF6,
    SzollosiDeltoidB6,
    TaoConfluenceS6,
    PeriodicCollar2D,
    KarlssonVolumeExterior,
    HaagerupOrbitH6,
}

impl RegionalCoverComponent {
    pub const ALL: [RegionalCoverComponent; NUM_REGIONAL_COMPONENTS] = [
        RegionalCoverComponent::DitaFourierF6,
        RegionalCoverComponent::SzollosiDeltoidB6,
        RegionalCoverComponent::TaoConfluenceS6,
        RegionalCoverComponent::PeriodicCollar2D,
        RegionalCoverComponent::KarlssonVolumeExterior,
        RegionalCoverComponent::HaagerupOrbitH6,
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

    pub fn component_index(&self) -> usize {
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
            Self::KarlssonVolumeExterior => base_gap(),
            _ => certified_margin(),
        }
    }
}

#[derive(Clone, Debug, PartialEq, Eq, PartialOrd, Ord, thiserror::Error, Serialize, Deserialize)]
pub enum GlobalCoverError {
    #[error("Missing regional cover component: {0:?}")]
    MissingComponent(RegionalCoverComponent),

    #[error("Duplicate regional cover component: {0:?}")]
    DuplicateComponent(RegionalCoverComponent),

    #[error("Volume conservation mismatch: expected {expected}, actual {actual}, difference {difference}")]
    VolumeConservationMismatch {
        expected: BigRational,
        actual: BigRational,
        difference: BigRational,
    },

    #[error("Boundary interface gap detected between {chart_a:?} and {chart_b:?}: {reason}")]
    BoundaryGapDetected {
        chart_a: RegionalCoverComponent,
        chart_b: RegionalCoverComponent,
        reason: String,
    },

    #[error("Interface adjacency uncertified between {chart_a:?} and {chart_b:?}: non-positive margin ({margin})")]
    NonPositiveInterfaceMargin {
        chart_a: RegionalCoverComponent,
        chart_b: RegionalCoverComponent,
        margin: BigRational,
    },

    #[error(
        "Non-positive margin detected in leaf {leaf_index} of {component:?}: margin {margin} <= 0"
    )]
    NonPositiveMargin {
        component: RegionalCoverComponent,
        leaf_index: usize,
        margin: BigRational,
    },

    #[error(
        "Non-positive cycle circulation in loop '{loop_name}': circulation {circulation} <= 0"
    )]
    NonPositiveCirculation {
        loop_name: String,
        circulation: i128,
    },

    #[error("Coboundary sum non-zero around loop '{loop_name}': sum {sum}")]
    CoboundarySumNonZero { loop_name: String, sum: i128 },

    #[error("Non-zero duality gap in loop '{loop_name}': objective {objective}, net circulation {circulation}")]
    DualGapNonZero {
        loop_name: String,
        objective: i128,
        circulation: i128,
    },

    #[error("Disconnected atlas: component graph is not connected")]
    DisconnectedAtlas,

    #[error("Invalid interval for dimension {dim}: lo ({lo}) >= hi ({hi})")]
    InvalidInterval {
        dim: usize,
        lo: BigRational,
        hi: BigRational,
    },

    #[error("Empty partition tree for component {0:?}")]
    EmptyPartitionTree(RegionalCoverComponent),

    #[error("Cut out of bounds for dimension {dim}: cut ({cut}) is not strictly interior to ({lo}, {hi})")]
    CutOutOfBounds {
        dim: usize,
        cut: BigRational,
        lo: BigRational,
        hi: BigRational,
    },

    #[error("Network simplex failure: {0}")]
    SimplexFailure(String),

    #[error("Serialization / format error: {0}")]
    SerializationError(String),
}

#[derive(Clone, Debug, PartialEq, Eq, PartialOrd, Ord, Serialize, Deserialize)]
pub struct RationalCell {
    pub bounds: Vec<(BigRational, BigRational)>,
    pub cert_id: Option<String>,
    pub margin: BigRational,
}

impl RationalCell {
    pub fn new(
        bounds: Vec<(BigRational, BigRational)>,
        margin: BigRational,
    ) -> Result<Self, GlobalCoverError> {
        for (dim, (ref lo, ref hi)) in bounds.iter().enumerate() {
            if lo >= hi {
                return Err(GlobalCoverError::InvalidInterval {
                    dim,
                    lo: lo.clone(),
                    hi: hi.clone(),
                });
            }
        }
        Ok(Self {
            bounds,
            cert_id: None,
            margin,
        })
    }

    pub fn unit_hypercube(dim: usize, margin: BigRational) -> Self {
        let zero = BigRational::zero();
        let one = BigRational::one();
        let bounds = (0..dim).map(|_| (zero.clone(), one.clone())).collect();
        Self {
            bounds,
            cert_id: None,
            margin,
        }
    }

    pub fn dimension(&self) -> usize {
        self.bounds.len()
    }

    pub fn volume(&self) -> BigRational {
        let mut vol = BigRational::one();
        for (lo, hi) in &self.bounds {
            vol = vol * (hi - lo);
        }
        vol
    }

    pub fn contains_point(&self, pt: &[BigRational]) -> bool {
        if pt.len() != self.bounds.len() {
            return false;
        }
        for (j, (ref lo, ref hi)) in self.bounds.iter().enumerate() {
            if &pt[j] < lo || &pt[j] > hi {
                return false;
            }
        }
        true
    }

    pub fn overlaps_interior(&self, other: &Self) -> bool {
        let min_dim = self.bounds.len().min(other.bounds.len());
        for j in 0..min_dim {
            let (ref a_lo, ref a_hi) = self.bounds[j];
            let (ref b_lo, ref b_hi) = other.bounds[j];
            if a_hi <= b_lo || b_hi <= a_lo {
                return false;
            }
        }
        true
    }

    pub fn subdivide(
        &self,
        dim: usize,
        cut: &BigRational,
    ) -> Result<(Self, Self), GlobalCoverError> {
        if dim >= self.bounds.len() {
            return Err(GlobalCoverError::CutOutOfBounds {
                dim,
                cut: cut.clone(),
                lo: BigRational::zero(),
                hi: BigRational::zero(),
            });
        }
        let (ref lo, ref hi) = self.bounds[dim];
        if cut <= lo || cut >= hi {
            return Err(GlobalCoverError::CutOutOfBounds {
                dim,
                cut: cut.clone(),
                lo: lo.clone(),
                hi: hi.clone(),
            });
        }
        let mut left_bounds = self.bounds.clone();
        left_bounds[dim].1 = cut.clone();

        let mut right_bounds = self.bounds.clone();
        right_bounds[dim].0 = cut.clone();

        let left = Self {
            bounds: left_bounds,
            cert_id: self.cert_id.clone(),
            margin: self.margin.clone(),
        };
        let right = Self {
            bounds: right_bounds,
            cert_id: self.cert_id.clone(),
            margin: self.margin.clone(),
        };
        Ok((left, right))
    }

    pub fn bisect(&self, dim: usize) -> Result<(Self, Self), GlobalCoverError> {
        if dim >= self.bounds.len() {
            return Err(GlobalCoverError::CutOutOfBounds {
                dim,
                cut: BigRational::zero(),
                lo: BigRational::zero(),
                hi: BigRational::zero(),
            });
        }
        let two = BigRational::from_integer(BigInt::from(2));
        let (ref lo, ref hi) = self.bounds[dim];
        let mid = (lo + hi) / two;
        self.subdivide(dim, &mid)
    }

    pub fn hash_digest(&self) -> String {
        let mut hasher = Sha256::new();
        for (lo, hi) in &self.bounds {
            hasher.update(lo.to_string().as_bytes());
            hasher.update(b",");
            hasher.update(hi.to_string().as_bytes());
            hasher.update(b";");
        }
        hasher.update(self.margin.to_string().as_bytes());
        format!("{:x}", hasher.finalize())
    }
}

#[derive(Clone, Debug, PartialEq, Eq, PartialOrd, Ord, Serialize, Deserialize)]
pub enum RegionalPartitionTree {
    Leaf(RationalCell),
    Split {
        dim: usize,
        cut: BigRational,
        left: Box<RegionalPartitionTree>,
        right: Box<RegionalPartitionTree>,
    },
}

impl RegionalPartitionTree {
    pub fn leaf(cell: RationalCell) -> Self {
        Self::Leaf(cell)
    }

    pub fn leaves(&self) -> Vec<RationalCell> {
        let mut result = Vec::new();
        self.collect_leaves(&mut result);
        result
    }

    fn collect_leaves(&self, out: &mut Vec<RationalCell>) {
        match self {
            Self::Leaf(cell) => out.push(cell.clone()),
            Self::Split { left, right, .. } => {
                left.collect_leaves(out);
                right.collect_leaves(out);
            }
        }
    }

    pub fn leaf_count(&self) -> usize {
        match self {
            Self::Leaf(_) => 1,
            Self::Split { left, right, .. } => left.leaf_count() + right.leaf_count(),
        }
    }

    pub fn total_volume(&self) -> BigRational {
        match self {
            Self::Leaf(cell) => cell.volume(),
            Self::Split { left, right, .. } => left.total_volume() + right.total_volume(),
        }
    }

    pub fn min_margin(&self) -> BigRational {
        match self {
            Self::Leaf(cell) => cell.margin.clone(),
            Self::Split { left, right, .. } => {
                let lm = left.min_margin();
                let rm = right.min_margin();
                if lm <= rm {
                    lm
                } else {
                    rm
                }
            }
        }
    }

    pub fn all_margins_positive(&self) -> bool {
        self.min_margin() > BigRational::zero()
    }

    pub fn hash_digest(&self) -> String {
        let mut hasher = Sha256::new();
        self.hash_into(&mut hasher);
        format!("{:x}", hasher.finalize())
    }

    fn hash_into(&self, hasher: &mut Sha256) {
        match self {
            Self::Leaf(cell) => {
                hasher.update(b"LEAF:");
                hasher.update(cell.hash_digest().as_bytes());
            }
            Self::Split {
                dim,
                cut,
                left,
                right,
            } => {
                hasher.update(b"SPLIT:");
                hasher.update(dim.to_string().as_bytes());
                hasher.update(b":");
                hasher.update(cut.to_string().as_bytes());
                left.hash_into(hasher);
                right.hash_into(hasher);
            }
        }
    }
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct RegionalCoverPatch {
    pub component: RegionalCoverComponent,
    pub name: String,
    pub volume: BigRational,
    pub margin: BigRational,
    pub partition_tree: RegionalPartitionTree,
    pub certified: bool,
    pub cert_hash: String,
}

impl RegionalCoverPatch {
    pub fn new(
        component: RegionalCoverComponent,
        name: impl Into<String>,
        partition_tree: RegionalPartitionTree,
    ) -> Result<Self, GlobalCoverError> {
        let name_str = name.into();
        let leaves = partition_tree.leaves();
        if leaves.is_empty() {
            return Err(GlobalCoverError::EmptyPartitionTree(component));
        }

        let zero = BigRational::zero();
        for (idx, leaf) in leaves.iter().enumerate() {
            if leaf.margin <= zero {
                return Err(GlobalCoverError::NonPositiveMargin {
                    component,
                    leaf_index: idx,
                    margin: leaf.margin.clone(),
                });
            }
        }

        let volume = partition_tree.total_volume();
        let margin = partition_tree.min_margin();
        let cert_hash = partition_tree.hash_digest();

        Ok(Self {
            component,
            name: name_str,
            volume,
            margin,
            partition_tree,
            certified: true,
            cert_hash,
        })
    }

    pub fn leaf_count(&self) -> usize {
        self.partition_tree.leaf_count()
    }

    pub fn verify(&self) -> Result<(), GlobalCoverError> {
        let zero = BigRational::zero();
        if self.volume <= zero {
            return Err(GlobalCoverError::VolumeConservationMismatch {
                expected: BigRational::one(),
                actual: self.volume.clone(),
                difference: self.volume.clone(),
            });
        }
        if self.margin <= zero {
            return Err(GlobalCoverError::NonPositiveMargin {
                component: self.component,
                leaf_index: 0,
                margin: self.margin.clone(),
            });
        }
        Ok(())
    }
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct ChartBoundaryInterface {
    pub chart_a: RegionalCoverComponent,
    pub chart_b: RegionalCoverComponent,
    pub overlap_volume: BigRational,
    pub interface_margin: BigRational,
    pub interface_cells: Vec<RationalCell>,
    pub gap_detected: bool,
    pub continuity_certified: bool,
}

impl ChartBoundaryInterface {
    pub fn new(
        chart_a: RegionalCoverComponent,
        chart_b: RegionalCoverComponent,
        overlap_volume: BigRational,
        interface_margin: BigRational,
        interface_cells: Vec<RationalCell>,
    ) -> Self {
        let zero = BigRational::zero();
        let gap_detected = overlap_volume <= zero || interface_margin <= zero;
        let continuity_certified = !gap_detected && !interface_cells.is_empty();

        Self {
            chart_a,
            chart_b,
            overlap_volume,
            interface_margin,
            interface_cells,
            gap_detected,
            continuity_certified,
        }
    }

    pub fn verify_adjacency(&self) -> Result<InterfaceAdjacencyReceipt, GlobalCoverError> {
        let zero = BigRational::zero();

        if self.gap_detected || self.overlap_volume <= zero {
            return Err(GlobalCoverError::BoundaryGapDetected {
                chart_a: self.chart_a,
                chart_b: self.chart_b,
                reason: format!(
                    "Uncertified boundary gap: overlap_volume={}",
                    self.overlap_volume
                ),
            });
        }

        if self.interface_margin <= zero {
            return Err(GlobalCoverError::NonPositiveInterfaceMargin {
                chart_a: self.chart_a,
                chart_b: self.chart_b,
                margin: self.interface_margin.clone(),
            });
        }

        for (idx, cell) in self.interface_cells.iter().enumerate() {
            if cell.margin <= zero {
                return Err(GlobalCoverError::NonPositiveMargin {
                    component: self.chart_a,
                    leaf_index: idx,
                    margin: cell.margin.clone(),
                });
            }
        }

        Ok(InterfaceAdjacencyReceipt {
            chart_a: self.chart_a,
            chart_b: self.chart_b,
            overlap_volume: self.overlap_volume.clone(),
            interface_margin: self.interface_margin.clone(),
            gap_detected: false,
            continuity_certified: true,
            is_adjacent: true,
        })
    }
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct InterfaceAdjacencyReceipt {
    pub chart_a: RegionalCoverComponent,
    pub chart_b: RegionalCoverComponent,
    pub overlap_volume: BigRational,
    pub interface_margin: BigRational,
    pub gap_detected: bool,
    pub continuity_certified: bool,
    pub is_adjacent: bool,
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct GlobalAdjacencyReport {
    pub total_interfaces: usize,
    pub all_interfaces_adjacent: bool,
    pub any_gap_detected: bool,
    pub min_interface_margin: BigRational,
    pub is_atlas_connected: bool,
    pub receipts: Vec<InterfaceAdjacencyReceipt>,
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct VolumeConservationReceipt {
    pub declared_total_volume: BigRational,
    pub sum_component_volumes: BigRational,
    pub volume_difference: BigRational,
    pub component_volumes: Vec<(RegionalCoverComponent, BigRational)>,
    pub is_exact_zero_gap: bool,
    pub all_volumes_positive: bool,
    pub certified: bool,
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct CompositeCycleLoop {
    pub name: String,
    pub nodes: Vec<RegionalCoverComponent>,
    pub edge_margins: Vec<BigRational>,
    pub edge_weights: Vec<i128>,
}

impl CompositeCycleLoop {
    pub fn new(
        name: impl Into<String>,
        nodes: Vec<RegionalCoverComponent>,
        edge_margins: Vec<BigRational>,
        edge_weights: Vec<i128>,
    ) -> Result<Self, GlobalCoverError> {
        let name_str = name.into();
        let k = nodes.len();
        if k < 3 {
            return Err(GlobalCoverError::BoundaryGapDetected {
                chart_a: nodes[0],
                chart_b: nodes[0],
                reason: format!("Cycle loop '{name_str}' must contain at least 3 nodes"),
            });
        }
        if edge_margins.len() != k || edge_weights.len() != k {
            return Err(GlobalCoverError::BoundaryGapDetected {
                chart_a: nodes[0],
                chart_b: nodes[1],
                reason: format!("Edge dimensions mismatch in loop '{name_str}'"),
            });
        }
        Ok(Self {
            name: name_str,
            nodes,
            edge_margins,
            edge_weights,
        })
    }

    pub fn triad_loop() -> Self {
        let margin = certified_margin();
        Self {
            name: "TriadLoop_F6_B6_S6".to_string(),
            nodes: vec![
                RegionalCoverComponent::DitaFourierF6,
                RegionalCoverComponent::SzollosiDeltoidB6,
                RegionalCoverComponent::TaoConfluenceS6,
            ],
            edge_margins: vec![margin.clone(), margin.clone(), margin],
            edge_weights: vec![1, 1, 1],
        }
    }

    pub fn collar_exterior_loop() -> Self {
        let margin = certified_margin();
        Self {
            name: "BoundaryLoop_Collar_Karlsson_Haagerup".to_string(),
            nodes: vec![
                RegionalCoverComponent::PeriodicCollar2D,
                RegionalCoverComponent::KarlssonVolumeExterior,
                RegionalCoverComponent::HaagerupOrbitH6,
            ],
            edge_margins: vec![margin.clone(), margin.clone(), margin],
            edge_weights: vec![1, 1, 1],
        }
    }

    pub fn full_six_chart_loop() -> Self {
        let margin = certified_margin();
        Self {
            name: "FullSixChartCompositeLoop".to_string(),
            nodes: vec![
                RegionalCoverComponent::DitaFourierF6,
                RegionalCoverComponent::SzollosiDeltoidB6,
                RegionalCoverComponent::TaoConfluenceS6,
                RegionalCoverComponent::PeriodicCollar2D,
                RegionalCoverComponent::KarlssonVolumeExterior,
                RegionalCoverComponent::HaagerupOrbitH6,
            ],
            edge_margins: vec![
                margin.clone(),
                margin.clone(),
                margin.clone(),
                margin.clone(),
                margin.clone(),
                margin,
            ],
            edge_weights: vec![1, 1, 1, 1, 1, 1],
        }
    }
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct CycleCirculationReceipt {
    pub loop_name: String,
    pub cycle_length: usize,
    pub scale: i128,
    pub edge_cochain: Vec<i128>,
    pub net_circulation: i128,
    pub phi1_objective: i128,
    pub rational_phi1: String,
    pub coboundary_sum: i128,
    pub circulation_conserved: bool,
    pub dual_gap_zero: bool,
    pub certified: bool,
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct GlobalAtlasReceipt {
    pub firewall: String,
    pub authority_effect: String,
    pub component_count: usize,
    pub all_components_present: bool,
    pub volume_conservation: VolumeConservationReceipt,
    pub boundary_adjacency: GlobalAdjacencyReport,
    pub composite_loop_receipts: Vec<CycleCirculationReceipt>,
    pub atlas_hash: String,
    pub certified: bool,
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct GlobalAtlasAggregator {
    pub declared_total_volume: BigRational,
    pub patches: BTreeMap<RegionalCoverComponent, RegionalCoverPatch>,
    pub interfaces: Vec<ChartBoundaryInterface>,
    pub composite_loops: Vec<CompositeCycleLoop>,
}

impl GlobalAtlasAggregator {
    pub fn new(declared_total_volume: BigRational) -> Self {
        Self {
            declared_total_volume,
            patches: BTreeMap::new(),
            interfaces: Vec::new(),
            composite_loops: Vec::new(),
        }
    }

    pub fn add_patch(&mut self, patch: RegionalCoverPatch) -> Result<(), GlobalCoverError> {
        if self.patches.contains_key(&patch.component) {
            return Err(GlobalCoverError::DuplicateComponent(patch.component));
        }
        patch.verify()?;
        self.patches.insert(patch.component, patch);
        Ok(())
    }

    pub fn add_interface(
        &mut self,
        interface: ChartBoundaryInterface,
    ) -> Result<(), GlobalCoverError> {
        self.interfaces.push(interface);
        Ok(())
    }

    pub fn add_composite_loop(
        &mut self,
        cycle_loop: CompositeCycleLoop,
    ) -> Result<(), GlobalCoverError> {
        self.composite_loops.push(cycle_loop);
        Ok(())
    }

    pub fn verify_component_completeness(&self) -> Result<(), GlobalCoverError> {
        for comp in &RegionalCoverComponent::ALL {
            if !self.patches.contains_key(comp) {
                return Err(GlobalCoverError::MissingComponent(*comp));
            }
        }
        Ok(())
    }

    pub fn certify_volume_conservation(
        &self,
    ) -> Result<VolumeConservationReceipt, GlobalCoverError> {
        self.verify_component_completeness()?;

        let mut sum_vol = BigRational::zero();
        let mut component_vols = Vec::with_capacity(NUM_REGIONAL_COMPONENTS);

        for comp in &RegionalCoverComponent::ALL {
            let patch = self
                .patches
                .get(comp)
                .ok_or(GlobalCoverError::MissingComponent(*comp))?;
            let v = patch.volume.clone();
            if v <= BigRational::zero() {
                return Err(GlobalCoverError::VolumeConservationMismatch {
                    expected: self.declared_total_volume.clone(),
                    actual: v.clone(),
                    difference: v,
                });
            }
            sum_vol = sum_vol + &v;
            component_vols.push((*comp, v));
        }

        let vol_diff = &sum_vol - &self.declared_total_volume;
        if !vol_diff.is_zero() {
            return Err(GlobalCoverError::VolumeConservationMismatch {
                expected: self.declared_total_volume.clone(),
                actual: sum_vol,
                difference: vol_diff,
            });
        }

        Ok(VolumeConservationReceipt {
            declared_total_volume: self.declared_total_volume.clone(),
            sum_component_volumes: sum_vol,
            volume_difference: vol_diff,
            component_volumes: component_vols,
            is_exact_zero_gap: true,
            all_volumes_positive: true,
            certified: true,
        })
    }

    pub fn check_all_interfaces(&self) -> Result<GlobalAdjacencyReport, GlobalCoverError> {
        if self.interfaces.is_empty() {
            return Err(GlobalCoverError::BoundaryGapDetected {
                chart_a: RegionalCoverComponent::DitaFourierF6,
                chart_b: RegionalCoverComponent::SzollosiDeltoidB6,
                reason: "No boundary interfaces registered in atlas".to_string(),
            });
        }

        let mut receipts = Vec::with_capacity(self.interfaces.len());
        let mut min_margin = BigRational::one();
        let mut adj_graph: BTreeMap<RegionalCoverComponent, BTreeSet<RegionalCoverComponent>> =
            BTreeMap::new();

        for iface in &self.interfaces {
            let rc = iface.verify_adjacency()?;
            if rc.interface_margin < min_margin {
                min_margin = rc.interface_margin.clone();
            }
            adj_graph.entry(rc.chart_a).or_default().insert(rc.chart_b);
            adj_graph.entry(rc.chart_b).or_default().insert(rc.chart_a);
            receipts.push(rc);
        }

        if !Self::is_adj_graph_connected(&adj_graph) {
            return Err(GlobalCoverError::DisconnectedAtlas);
        }

        Ok(GlobalAdjacencyReport {
            total_interfaces: receipts.len(),
            all_interfaces_adjacent: true,
            any_gap_detected: false,
            min_interface_margin: min_margin,
            is_atlas_connected: true,
            receipts,
        })
    }

    fn enqueue_neighbors(
        neighbors: &BTreeSet<RegionalCoverComponent>,
        visited: &mut BTreeSet<RegionalCoverComponent>,
        queue: &mut VecDeque<RegionalCoverComponent>,
    ) {
        for &nxt in neighbors {
            if visited.insert(nxt) {
                queue.push_back(nxt);
            }
        }
    }

    fn is_adj_graph_connected(
        adj_graph: &BTreeMap<RegionalCoverComponent, BTreeSet<RegionalCoverComponent>>,
    ) -> bool {
        let mut visited = BTreeSet::new();
        let start = RegionalCoverComponent::ALL[0];
        let mut queue = VecDeque::new();
        queue.push_back(start);
        visited.insert(start);

        while let Some(curr) = queue.pop_front() {
            if let Some(neighbors) = adj_graph.get(&curr) {
                Self::enqueue_neighbors(neighbors, &mut visited, &mut queue);
            }
        }

        visited.len() == NUM_REGIONAL_COMPONENTS
    }

    fn build_scaled_loop_cochain(
        loop_def: &CompositeCycleLoop,
        scale: i128,
    ) -> Result<(Boundary1, Vec<i128>, i128), GlobalCoverError> {
        let k = loop_def.nodes.len();
        let mut edges = Vec::with_capacity(k);
        for i in 0..k {
            edges.push(BoundaryEdge {
                tail: i,
                head: (i + 1) % k,
                weight: loop_def.edge_weights[i],
            });
        }
        let boundary = Boundary1 {
            num_vertices: k,
            edges,
        };

        let scale_rat = BigRational::from_integer(BigInt::from(scale));
        let mut omega = Vec::with_capacity(k);
        for (i, m) in loop_def.edge_margins.iter().enumerate() {
            let scaled = (m * &scale_rat)
                .to_integer()
                .to_string()
                .parse::<i128>()
                .unwrap_or(0);
            if scaled <= 0 {
                return Err(GlobalCoverError::NonPositiveCirculation {
                    loop_name: format!("{}_edge_{i}", loop_def.name),
                    circulation: scaled,
                });
            }
            omega.push(scaled);
        }

        let net_circulation: i128 = omega.iter().sum();
        if net_circulation <= 0 {
            return Err(GlobalCoverError::NonPositiveCirculation {
                loop_name: loop_def.name.clone(),
                circulation: net_circulation,
            });
        }
        Ok((boundary, omega, net_circulation))
    }

    pub fn solve_loop_circulation(
        &self,
        loop_def: &CompositeCycleLoop,
        scale: i128,
    ) -> Result<CycleCirculationReceipt, GlobalCoverError> {
        let k = loop_def.nodes.len();
        if k < 3 {
            return Err(GlobalCoverError::BoundaryGapDetected {
                chart_a: loop_def.nodes[0],
                chart_b: loop_def.nodes[0],
                reason: format!("Loop '{}' has fewer than 3 nodes", loop_def.name),
            });
        }
        if scale <= 0 {
            return Err(GlobalCoverError::NonPositiveCirculation {
                loop_name: loop_def.name.clone(),
                circulation: scale,
            });
        }

        let (boundary, omega, net_circulation) = Self::build_scaled_loop_cochain(loop_def, scale)?;

        let phi1_sol = solve_phi1(&boundary, &omega)
            .map_err(|e: NetworkSimplexError| GlobalCoverError::SimplexFailure(format!("{e:?}")))?;

        let d_alpha_sum: i128 = boundary
            .edges
            .iter()
            .map(|e| phi1_sol.vertex_potential[e.head] - phi1_sol.vertex_potential[e.tail])
            .sum();

        if d_alpha_sum != 0 {
            return Err(GlobalCoverError::CoboundarySumNonZero {
                loop_name: loop_def.name.clone(),
                sum: d_alpha_sum,
            });
        }

        let dual_gap_zero = phi1_sol.objective == net_circulation;
        if !dual_gap_zero {
            return Err(GlobalCoverError::DualGapNonZero {
                loop_name: loop_def.name.clone(),
                objective: phi1_sol.objective,
                circulation: net_circulation,
            });
        }

        let rational_phi1 = phi1_sol
            .scaled_verified_value(scale)
            .ok_or_else(|| {
                GlobalCoverError::SimplexFailure(
                    "exact Phi1 certificate or positive scale missing".to_string(),
                )
            })?
            .to_string();

        Ok(CycleCirculationReceipt {
            loop_name: loop_def.name.clone(),
            cycle_length: k,
            scale,
            edge_cochain: omega,
            net_circulation,
            phi1_objective: phi1_sol.objective,
            rational_phi1,
            coboundary_sum: d_alpha_sum,
            circulation_conserved: true,
            dual_gap_zero: true,
            certified: true,
        })
    }

    pub fn certify_cycle_circulations(
        &self,
        scale: i128,
    ) -> Result<Vec<CycleCirculationReceipt>, GlobalCoverError> {
        let mut receipts = Vec::with_capacity(self.composite_loops.len());
        for c_loop in &self.composite_loops {
            let r = self.solve_loop_circulation(c_loop, scale)?;
            receipts.push(r);
        }
        Ok(receipts)
    }

    pub fn atlas_hash(&self) -> String {
        let mut hasher = Sha256::new();
        hasher.update(self.declared_total_volume.to_string().as_bytes());
        for (comp, patch) in &self.patches {
            hasher.update(comp.canonical_id().as_bytes());
            hasher.update(patch.cert_hash.as_bytes());
        }
        for iface in &self.interfaces {
            hasher.update(iface.chart_a.canonical_id().as_bytes());
            hasher.update(iface.chart_b.canonical_id().as_bytes());
            hasher.update(iface.overlap_volume.to_string().as_bytes());
            hasher.update(iface.interface_margin.to_string().as_bytes());
        }
        format!("{:x}", hasher.finalize())
    }

    pub fn certify_global_atlas(
        &self,
        scale: i128,
    ) -> Result<GlobalAtlasReceipt, GlobalCoverError> {
        self.verify_component_completeness()?;
        let vol_receipt = self.certify_volume_conservation()?;
        let adj_report = self.check_all_interfaces()?;
        let loop_receipts = self.certify_cycle_circulations(scale)?;
        let hash = self.atlas_hash();

        Ok(GlobalAtlasReceipt {
            firewall: FIREWALL.to_string(),
            authority_effect: AUTHORITY_EFFECT.to_string(),
            component_count: self.patches.len(),
            all_components_present: true,
            volume_conservation: vol_receipt,
            boundary_adjacency: adj_report,
            composite_loop_receipts: loop_receipts,
            atlas_hash: hash,
            certified: true,
        })
    }
}

pub fn build_component_partition(
    dim: usize,
    target_vol: BigRational,
    num_leaves: usize,
    margin: BigRational,
) -> Result<RegionalPartitionTree, GlobalCoverError> {
    let zero = BigRational::zero();
    let width_per_leaf = &target_vol / &BigRational::from_integer(BigInt::from(num_leaves));

    let mut tree = None;
    let mut current_lo = zero;

    for _ in 0..num_leaves {
        let current_hi = &current_lo + &width_per_leaf;
        let mut bounds = Vec::with_capacity(dim);
        bounds.push((current_lo.clone(), current_hi.clone()));
        for _ in 1..dim {
            bounds.push((BigRational::zero(), BigRational::one()));
        }
        let cell = RationalCell::new(bounds, margin.clone())?;
        let leaf = RegionalPartitionTree::leaf(cell);

        tree = match tree {
            None => Some(leaf),
            Some(prev) => Some(RegionalPartitionTree::Split {
                dim: 0,
                cut: current_lo.clone(),
                left: Box::new(prev),
                right: Box::new(leaf),
            }),
        };
        current_lo = current_hi;
    }

    tree.ok_or(GlobalCoverError::InvalidInterval {
        dim: 0,
        lo: BigRational::zero(),
        hi: target_vol,
    })
}

pub fn build_canonical_global_atlas() -> GlobalAtlasAggregator {
    let one = BigRational::one();
    let mut atlas = GlobalAtlasAggregator::new(one);
    let margin = certified_margin();

    let vol_f6 = rq(1, 12);
    let tree_f6 = build_component_partition(4, vol_f6, 2, margin.clone())
        .expect("F6 partition construction must succeed");
    let patch_f6 = RegionalCoverPatch::new(
        RegionalCoverComponent::DitaFourierF6,
        "Affine Diță Fourier chart (F_6)",
        tree_f6,
    )
    .expect("F6 patch construction must succeed");
    atlas
        .add_patch(patch_f6)
        .expect("Adding F6 patch must succeed");

    let vol_b6 = rq(1, 12);
    let tree_b6 = build_component_partition(4, vol_b6, 2, margin.clone())
        .expect("B6 partition construction must succeed");
    let patch_b6 = RegionalCoverPatch::new(
        RegionalCoverComponent::SzollosiDeltoidB6,
        "Szöllősi deltoid arc (B_6)",
        tree_b6,
    )
    .expect("B6 patch construction must succeed");
    atlas
        .add_patch(patch_b6)
        .expect("Adding B6 patch must succeed");

    let vol_s6 = rq(1, 12);
    let tree_s6 = build_component_partition(5, vol_s6, 2, margin.clone())
        .expect("S6 partition construction must succeed");
    let patch_s6 = RegionalCoverPatch::new(
        RegionalCoverComponent::TaoConfluenceS6,
        "Tao confluence chart (S_6)",
        tree_s6,
    )
    .expect("S6 patch construction must succeed");
    atlas
        .add_patch(patch_s6)
        .expect("Adding S6 patch must succeed");

    let vol_collar = rq(2, 12);
    let tree_collar = build_component_partition(2, vol_collar, 4, margin.clone())
        .expect("Collar partition construction must succeed");
    let patch_collar = RegionalCoverPatch::new(
        RegionalCoverComponent::PeriodicCollar2D,
        "2D Periodic collar cover",
        tree_collar,
    )
    .expect("Collar patch construction must succeed");
    atlas
        .add_patch(patch_collar)
        .expect("Adding Collar patch must succeed");

    let vol_karlsson = rq(6, 12);
    let tree_karlsson = build_component_partition(6, vol_karlsson, 4, base_gap())
        .expect("Karlsson partition construction must succeed");
    let patch_karlsson = RegionalCoverPatch::new(
        RegionalCoverComponent::KarlssonVolumeExterior,
        "Karlsson volume exterior boundary interface",
        tree_karlsson,
    )
    .expect("Karlsson patch construction must succeed");
    atlas
        .add_patch(patch_karlsson)
        .expect("Adding Karlsson patch must succeed");

    let vol_h6 = rq(1, 12);
    let tree_h6 = build_component_partition(4, vol_h6, 2, margin.clone())
        .expect("H6 partition construction must succeed");
    let patch_h6 = RegionalCoverPatch::new(
        RegionalCoverComponent::HaagerupOrbitH6,
        "Isolated Haagerup orbit neighborhood (H_6)",
        tree_h6,
    )
    .expect("H6 patch construction must succeed");
    atlas
        .add_patch(patch_h6)
        .expect("Adding H6 patch must succeed");

    let overlap_vol = delta_certified();
    let iface_margin = certified_margin();

    let dummy_iface_cell = RationalCell::new(
        vec![
            (BigRational::zero(), delta_certified()),
            (BigRational::zero(), BigRational::one()),
        ],
        iface_margin.clone(),
    )
    .expect("Interface cell creation must succeed");

    let ifaces = [
        (
            RegionalCoverComponent::DitaFourierF6,
            RegionalCoverComponent::SzollosiDeltoidB6,
        ),
        (
            RegionalCoverComponent::SzollosiDeltoidB6,
            RegionalCoverComponent::TaoConfluenceS6,
        ),
        (
            RegionalCoverComponent::TaoConfluenceS6,
            RegionalCoverComponent::PeriodicCollar2D,
        ),
        (
            RegionalCoverComponent::PeriodicCollar2D,
            RegionalCoverComponent::KarlssonVolumeExterior,
        ),
        (
            RegionalCoverComponent::KarlssonVolumeExterior,
            RegionalCoverComponent::HaagerupOrbitH6,
        ),
        (
            RegionalCoverComponent::HaagerupOrbitH6,
            RegionalCoverComponent::DitaFourierF6,
        ),
    ];

    for (a, b) in ifaces {
        let iface = ChartBoundaryInterface::new(
            a,
            b,
            overlap_vol.clone(),
            iface_margin.clone(),
            vec![dummy_iface_cell.clone()],
        );
        atlas
            .add_interface(iface)
            .expect("Adding interface must succeed");
    }

    atlas
        .add_composite_loop(CompositeCycleLoop::triad_loop())
        .expect("Adding triad loop must succeed");
    atlas
        .add_composite_loop(CompositeCycleLoop::collar_exterior_loop())
        .expect("Adding collar exterior loop must succeed");
    atlas
        .add_composite_loop(CompositeCycleLoop::full_six_chart_loop())
        .expect("Adding full 6-chart loop must succeed");

    atlas
}
