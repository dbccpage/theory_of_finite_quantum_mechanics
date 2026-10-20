
use num_bigint::BigInt;
use num_rational::BigRational;
use num_traits::{One, ToPrimitive, Zero};
use serde::{Deserialize, Serialize};

use crate::omega_native::exact::mub6_firewall::{AUTHORITY_EFFECT, FIREWALL};
use crate::omega_native::exact::mub6_global_gluing::{
    circulation_gamma_threshold, is_nerve2, ModuliChart5,
};
use omega_number_theory::rational::rq;
use omega_solvers::solver_lp_phi1_boundary::{solve_phi1, Boundary1, BoundaryEdge};

pub const SCOPE: &str = "synthetic_edge_weights_no_geometric_or_curvature_bridge";
pub const DIM_2D: usize = 2;

pub const INTEGER_SCALE: i128 = 30000;

pub const SCALED_GAMMA_THRESHOLD: i128 = 72798;

#[derive(Clone, Debug, PartialEq, Eq, PartialOrd, Ord, thiserror::Error, Serialize, Deserialize)]
pub enum NerveChainingError {
    #[error("Invalid parameter: {0}")]
    InvalidParameter(String),

    #[error("Degenerate collar box: lo ({lo}) >= hi ({hi}) at dimension {dim}")]
    DegenerateBox {
        dim: usize,
        lo: BigRational,
        hi: BigRational,
    },

    #[error("Box bounds [{lo}, {hi}] exceed unit interval [0, 1] at dimension {dim}")]
    BoxOutOfBounds {
        dim: usize,
        lo: BigRational,
        hi: BigRational,
    },

    #[error("Invalid Nerve2 triple: ({0:?}, {1:?}, {2:?}) does not satisfy Nerve2 condition")]
    InvalidNerveTriangle(ModuliChart5, ModuliChart5, ModuliChart5),

    #[error("Orientation mismatch: edges do not form a closed cyclically oriented 3-cycle: {0}")]
    OrientationMismatch(String),

    #[error("Non-positive circulation: {circulation} <= 0 on triangle {triangle_name}")]
    NonPositiveCirculation {
        triangle_name: String,
        circulation: i128,
    },

    #[error("Circulation {phi1} < fixture threshold {threshold} on triangle {triangle_name}")]
    SubThresholdCirculation {
        triangle_name: String,
        phi1: BigRational,
        threshold: BigRational,
    },

    #[error("Non-zero coboundary sum around triangle {triangle_name}: {sum}")]
    NonZeroCoboundarySum { triangle_name: String, sum: i128 },

    #[error("Non-zero duality gap on triangle {triangle_name}: objective {objective} != l1_norm {l1_norm}")]
    DualityGapNonZero {
        triangle_name: String,
        objective: i128,
        l1_norm: i128,
    },

    #[error("Network simplex failure: {0}")]
    NetworkSimplexFailure(String),
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct CollarBox2D {
    pub bounds: [(BigRational, BigRational); DIM_2D],
    pub cell_id: String,
}

impl CollarBox2D {
    pub fn unit_square() -> Self {
        let zero = BigRational::zero();
        let one = BigRational::one();
        Self {
            bounds: [(zero.clone(), one.clone()), (zero, one)],
            cell_id: "collar_unit_square".to_string(),
        }
    }

    pub fn new(
        bounds: [(BigRational, BigRational); DIM_2D],
        cell_id: String,
    ) -> Result<Self, NerveChainingError> {
        let zero = BigRational::zero();
        let one = BigRational::one();

        for dim in 0..DIM_2D {
            let (ref lo, ref hi) = bounds[dim];
            if lo >= hi {
                return Err(NerveChainingError::DegenerateBox {
                    dim,
                    lo: lo.clone(),
                    hi: hi.clone(),
                });
            }
            if lo < &zero || hi > &one {
                return Err(NerveChainingError::BoxOutOfBounds {
                    dim,
                    lo: lo.clone(),
                    hi: hi.clone(),
                });
            }
        }

        Ok(Self { bounds, cell_id })
    }

    pub fn area(&self) -> BigRational {
        let w0 = &self.bounds[0].1 - &self.bounds[0].0;
        let w1 = &self.bounds[1].1 - &self.bounds[1].0;
        &w0 * &w1
    }

    pub fn center(&self) -> [BigRational; DIM_2D] {
        let two = BigRational::from_integer(BigInt::from(2));
        [
            &(&self.bounds[0].0 + &self.bounds[0].1) / &two,
            &(&self.bounds[1].0 + &self.bounds[1].1) / &two,
        ]
    }

    pub fn contains_point(&self, pt: &[BigRational; DIM_2D]) -> bool {
        pt[0] >= self.bounds[0].0
            && pt[0] <= self.bounds[0].1
            && pt[1] >= self.bounds[1].0
            && pt[1] <= self.bounds[1].1
    }

    pub fn split_dim(
        &self,
        dim: usize,
        cut: &BigRational,
    ) -> Result<(Self, Self), NerveChainingError> {
        if dim >= DIM_2D {
            return Err(NerveChainingError::InvalidParameter(format!(
                "Invalid split dimension: {dim}"
            )));
        }
        let (ref lo, ref hi) = self.bounds[dim];
        if cut <= lo || cut >= hi {
            return Err(NerveChainingError::InvalidParameter(format!(
                "Cut {cut} not strictly interior to [{lo}, {hi}] along dim {dim}"
            )));
        }

        let mut left_bounds = self.bounds.clone();
        left_bounds[dim] = (lo.clone(), cut.clone());
        let mut right_bounds = self.bounds.clone();
        right_bounds[dim] = (cut.clone(), hi.clone());

        let left = Self::new(left_bounds, format!("{}_L{}", self.cell_id, dim))?;
        let right = Self::new(right_bounds, format!("{}_R{}", self.cell_id, dim))?;
        Ok((left, right))
    }
}

pub fn build_canonical_collar_grid(
    divisions: usize,
) -> Result<Vec<CollarBox2D>, NerveChainingError> {
    if divisions == 0 {
        return Err(NerveChainingError::InvalidParameter(
            "divisions must be >= 1".to_string(),
        ));
    }
    let div_bi = BigInt::from(divisions);
    let count = divisions.checked_mul(divisions).ok_or_else(|| {
        NerveChainingError::InvalidParameter("Grid dimension overflow".to_string())
    })?;
    let mut boxes = Vec::with_capacity(count);
    let mut idx = 0;

    for i in 0..divisions {
        let u0 = BigRational::new(BigInt::from(i), div_bi.clone());
        let v0 = BigRational::new(BigInt::from(i + 1), div_bi.clone());
        for j in 0..divisions {
            let u1 = BigRational::new(BigInt::from(j), div_bi.clone());
            let v1 = BigRational::new(BigInt::from(j + 1), div_bi.clone());
            let b = CollarBox2D::new(
                [(u0.clone(), v0.clone()), (u1, v1)],
                format!("collar_grid_{i}_{j}_{idx}"),
            )?;
            boxes.push(b);
            idx += 1;
        }
    }
    Ok(boxes)
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct BoundaryNerveTriangle {
    pub name: String,
    pub nodes: [ModuliChart5; 3],
}

impl BoundaryNerveTriangle {
    pub fn new(name: String, nodes: [ModuliChart5; 3]) -> Result<Self, NerveChainingError> {
        let [c0, c1, c2] = nodes;
        if c0 == c1 || c1 == c2 || c2 == c0 {
            return Err(NerveChainingError::InvalidNerveTriangle(c0, c1, c2));
        }
        if !is_nerve2(c0, c1, c2) {
            return Err(NerveChainingError::InvalidNerveTriangle(c0, c1, c2));
        }
        Ok(Self { name, nodes })
    }

    pub fn from_directed_edges(
        name: String,
        edges: [(ModuliChart5, ModuliChart5); 3],
    ) -> Result<Self, NerveChainingError> {
        let [e0, e1, e2] = edges;
        if e0.1 != e1.0 || e1.1 != e2.0 || e2.1 != e0.0 {
            return Err(NerveChainingError::OrientationMismatch(format!(
                "Edges do not form a cyclically oriented 3-cycle: ({e0:?}, {e1:?}, {e2:?})"
            )));
        }
        Self::new(name, [e0.0, e1.0, e2.0])
    }

    pub fn deltoid() -> Self {
        Self {
            name: "delta_deltoid_0_1_2".to_string(),
            nodes: [
                ModuliChart5::SzollosiCurve,
                ModuliChart5::KarlssonManifold,
                ModuliChart5::DeltoidCusps,
            ],
        }
    }

    pub fn tao() -> Self {
        Self {
            name: "delta_tao_0_1_4".to_string(),
            nodes: [
                ModuliChart5::SzollosiCurve,
                ModuliChart5::KarlssonManifold,
                ModuliChart5::TaoConfluence,
            ],
        }
    }

    pub fn directed_edges(&self) -> [(ModuliChart5, ModuliChart5); 3] {
        let [c0, c1, c2] = self.nodes;
        [(c0, c1), (c1, c2), (c2, c0)]
    }

    pub fn canonical_edge_defects(&self) -> [BigRational; 3] {
        let d = rq(12133, 15000);
        [d.clone(), d.clone(), d]
    }
}

#[derive(Clone, Copy, Debug, PartialEq, Eq, PartialOrd, Ord, Serialize, Deserialize)]
pub enum CollarNerveInterfaceType {
    DeltoidBoundary,
    TaoBoundary,
}

impl CollarNerveInterfaceType {
    pub fn as_str(&self) -> &'static str {
        match self {
            Self::DeltoidBoundary => "deltoid_boundary",
            Self::TaoBoundary => "tao_boundary",
        }
    }
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct CollarBoxNerveBinding {
    pub box_2d: CollarBox2D,
    pub triangle: BoundaryNerveTriangle,
    pub interface_type: CollarNerveInterfaceType,
    pub edge_defects: [BigRational; 3],
}

pub fn connect_collar_box_to_nerve(
    box_2d: CollarBox2D,
    custom_defects: Option<[BigRational; 3]>,
) -> Result<CollarBoxNerveBinding, NerveChainingError> {
    let half = rq(1, 2);
    let (triangle, interface_type) = if box_2d.bounds[0].0 < half {
        (
            BoundaryNerveTriangle::deltoid(),
            CollarNerveInterfaceType::DeltoidBoundary,
        )
    } else {
        (
            BoundaryNerveTriangle::tao(),
            CollarNerveInterfaceType::TaoBoundary,
        )
    };

    let edge_defects = custom_defects.unwrap_or_else(|| triangle.canonical_edge_defects());
    let zero = BigRational::zero();
    for d in &edge_defects {
        if d <= &zero {
            return Err(NerveChainingError::InvalidParameter(
                "Edge defect must be strictly positive".to_string(),
            ));
        }
    }

    Ok(CollarBoxNerveBinding {
        box_2d,
        triangle,
        interface_type,
        edge_defects,
    })
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct CollarNerveChaining {
    pub bindings: Vec<CollarBoxNerveBinding>,
    pub total_area: BigRational,
}

impl CollarNerveChaining {
    pub fn from_grid(divisions: usize) -> Result<Self, NerveChainingError> {
        let boxes = build_canonical_collar_grid(divisions)?;
        let mut bindings = Vec::with_capacity(boxes.len());
        let mut total_area = BigRational::zero();

        for b in boxes {
            total_area += b.area();
            let binding = connect_collar_box_to_nerve(b, None)?;
            bindings.push(binding);
        }

        Ok(Self {
            bindings,
            total_area,
        })
    }
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct TriangularCirculationReport {
    pub triangle_name: String,
    pub nodes: [usize; 3],
    pub edges: [(usize, usize); 3],
    pub edge_defects_rational: [BigRational; 3],
    pub scaled_integer_cochain: [i128; 3],
    pub net_circulation_scaled: i128,
    pub phi1_objective_scaled: i128,
    pub phi1_rational: BigRational,
    pub coboundary_sum_scaled: i128,
    pub circulation_conserved: bool,
    pub dual_gap_zero: bool,
    pub phi1_ge_gamma: bool,
}

fn scale_single_defect(defect: &BigRational, scale: i128) -> Result<i128, NerveChainingError> {
    let scale_rat = BigRational::from_integer(BigInt::from(scale));
    let scaled = defect * &scale_rat;
    if !scaled.is_integer() {
        return Err(NerveChainingError::InvalidParameter(format!(
            "Defect {} is not integral at scale {scale}; refusing truncation",
            defect
        )));
    }
    let val = scaled.to_integer().to_i128().ok_or_else(|| {
        NerveChainingError::InvalidParameter("Scaled defect exceeds i128 range".to_string())
    })?;
    if val.checked_abs().map_or(true, |n| n > i128::MAX / 16) {
        return Err(NerveChainingError::InvalidParameter(
            "Scaled defect exceeds safe solver range".to_string(),
        ));
    }
    Ok(val)
}

fn scale_triangle_defects(
    triangle_name: &str,
    defects: &[BigRational; 3],
    scale: i128,
) -> Result<([i128; 3], i128), NerveChainingError> {
    let mut omega_int = [0i128; 3];
    for i in 0..3 {
        omega_int[i] = scale_single_defect(&defects[i], scale)?;
    }

    let net_circulation: i128 = omega_int.iter().try_fold(0i128, |sum, &weight| {
        sum.checked_add(weight).ok_or_else(|| {
            NerveChainingError::InvalidParameter("Scaled circulation overflow".to_string())
        })
    })?;
    if net_circulation <= 0 {
        return Err(NerveChainingError::NonPositiveCirculation {
            triangle_name: triangle_name.to_string(),
            circulation: net_circulation,
        });
    }
    Ok((omega_int, net_circulation))
}

fn compute_coboundary_sum(
    boundary: &Boundary1,
    vertex_potential: &[i128],
) -> Result<i128, NerveChainingError> {
    let mut sum = 0i128;
    for e in &boundary.edges {
        let difference = vertex_potential[e.head]
            .checked_sub(vertex_potential[e.tail])
            .ok_or_else(|| {
                NerveChainingError::InvalidParameter(
                    "Solver potential difference overflow".to_string(),
                )
            })?;
        sum = sum.checked_add(difference).ok_or_else(|| {
            NerveChainingError::InvalidParameter("Solver potential sum overflow".to_string())
        })?;
    }
    Ok(sum)
}

fn compute_residual_l1_norm(z: &[i128]) -> Result<i128, NerveChainingError> {
    let mut sum = 0i128;
    for &x in z {
        let magnitude = x.checked_abs().ok_or_else(|| {
            NerveChainingError::InvalidParameter("Residual magnitude overflow".to_string())
        })?;
        sum = sum.checked_add(magnitude).ok_or_else(|| {
            NerveChainingError::InvalidParameter("Residual norm overflow".to_string())
        })?;
    }
    Ok(sum)
}

fn canonical_triangle_boundary() -> Boundary1 {
    Boundary1 {
        num_vertices: 3,
        edges: vec![
            BoundaryEdge {
                tail: 0,
                head: 1,
                weight: 1,
            },
            BoundaryEdge {
                tail: 1,
                head: 2,
                weight: 1,
            },
            BoundaryEdge {
                tail: 2,
                head: 0,
                weight: 1,
            },
        ],
    }
}

fn verify_phi1_solution_invariants(
    triangle_name: &str,
    boundary: &Boundary1,
    vertex_potential: &[i128],
    z: &[i128],
    objective: i128,
    scaled_val: Option<BigRational>,
    net_circulation: i128,
) -> Result<(i128, BigRational), NerveChainingError> {
    let coboundary_sum = compute_coboundary_sum(boundary, vertex_potential)?;
    if coboundary_sum != 0 {
        return Err(NerveChainingError::NonZeroCoboundarySum {
            triangle_name: triangle_name.to_string(),
            sum: coboundary_sum,
        });
    }
    let l1_norm = compute_residual_l1_norm(z)?;
    if objective != net_circulation || objective != l1_norm {
        return Err(NerveChainingError::DualityGapNonZero {
            triangle_name: triangle_name.to_string(),
            objective,
            l1_norm,
        });
    }
    let phi1_rational = scaled_val.ok_or_else(|| {
        NerveChainingError::NetworkSimplexFailure(
            "exact Phi1 certificate or positive scale missing".to_string(),
        )
    })?;
    Ok((coboundary_sum, phi1_rational))
}

pub fn solve_triangular_circulation(
    triangle: &BoundaryNerveTriangle,
    edge_defects: Option<[BigRational; 3]>,
    scale: i128,
) -> Result<TriangularCirculationReport, NerveChainingError> {
    if scale <= 0 {
        return Err(NerveChainingError::InvalidParameter(
            "Scale must be strictly positive".to_string(),
        ));
    }

    let defects = edge_defects.unwrap_or_else(|| triangle.canonical_edge_defects());
    BoundaryNerveTriangle::new(triangle.name.clone(), triangle.nodes)?;
    let (omega_int, net_circulation) = scale_triangle_defects(&triangle.name, &defects, scale)?;

    let boundary = canonical_triangle_boundary();
    let phi1_sol = solve_phi1(&boundary, &omega_int)
        .map_err(|e| NerveChainingError::NetworkSimplexFailure(format!("{e:?}")))?;
    let (coboundary_sum, phi1_rational) = verify_phi1_solution_invariants(
        &triangle.name,
        &boundary,
        &phi1_sol.vertex_potential,
        &phi1_sol.z,
        phi1_sol.objective,
        phi1_sol.scaled_verified_value(scale),
        net_circulation,
    )?;

    let gamma = circulation_gamma_threshold();
    let phi1_ge_gamma = phi1_rational >= gamma;
    if !phi1_ge_gamma {
        return Err(NerveChainingError::SubThresholdCirculation {
            triangle_name: triangle.name.clone(),
            phi1: phi1_rational,
            threshold: gamma,
        });
    }

    let nodes = [
        triangle.nodes[0].to_index(),
        triangle.nodes[1].to_index(),
        triangle.nodes[2].to_index(),
    ];
    let edges = [
        (nodes[0], nodes[1]),
        (nodes[1], nodes[2]),
        (nodes[2], nodes[0]),
    ];

    Ok(TriangularCirculationReport {
        triangle_name: triangle.name.clone(),
        nodes,
        edges,
        edge_defects_rational: defects,
        scaled_integer_cochain: omega_int,
        net_circulation_scaled: net_circulation,
        phi1_objective_scaled: phi1_sol.objective,
        phi1_rational,
        coboundary_sum_scaled: coboundary_sum,
        circulation_conserved: coboundary_sum == 0,
        dual_gap_zero: phi1_sol.objective == net_circulation,
        phi1_ge_gamma,
    })
}

fn checked_gauge_diff(a: i128, b: i128) -> Result<i128, NerveChainingError> {
    a.checked_sub(b)
        .ok_or_else(|| NerveChainingError::InvalidParameter("Gauge difference overflow".to_string()))
}

fn compute_gauge_coboundary(alpha: &[i128; 3]) -> Result<([i128; 3], i128), NerveChainingError> {
    let d_alpha = [
        checked_gauge_diff(alpha[1], alpha[0])?,
        checked_gauge_diff(alpha[2], alpha[1])?,
        checked_gauge_diff(alpha[0], alpha[2])?,
    ];
    let mut sum = 0i128;
    for &value in &d_alpha {
        sum = sum
            .checked_add(value)
            .ok_or_else(|| NerveChainingError::InvalidParameter("Gauge sum overflow".to_string()))?;
    }
    Ok((d_alpha, sum))
}

pub fn verify_gauge_invariance(
    triangle: &BoundaryNerveTriangle,
    alpha: &[i128; 3],
    custom_defects: Option<[BigRational; 3]>,
    scale: i128,
) -> Result<bool, NerveChainingError> {
    let base_report = solve_triangular_circulation(triangle, custom_defects, scale)?;
    let (d_alpha, coboundary_sum) = compute_gauge_coboundary(alpha)?;
    if coboundary_sum != 0 {
        return Ok(false);
    }

    let mut shifted_defects = base_report.edge_defects_rational.clone();
    for i in 0..3 {
        let shift_rat = BigRational::new(BigInt::from(d_alpha[i]), BigInt::from(scale));
        shifted_defects[i] += shift_rat;
    }

    let shifted_report = solve_triangular_circulation(triangle, Some(shifted_defects), scale)?;
    Ok(
        shifted_report.net_circulation_scaled == base_report.net_circulation_scaled
            && shifted_report.phi1_objective_scaled == base_report.phi1_objective_scaled
            && shifted_report.phi1_rational == base_report.phi1_rational,
    )
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct NerveChainingMasterReport {
    pub firewall_line: String,
    pub authority_effect: String,
    pub scope: String,
    pub mathematical_certification: bool,
    pub collar_overlap_verified: bool,
    pub curvature_to_cochain_verified: bool,
    pub num_collar_boxes: usize,
    pub total_collar_area: BigRational,
    pub area_conserved: bool,
    pub triangular_reports: Vec<TriangularCirculationReport>,
    pub all_phi1_ge_gamma: bool,
    pub all_circulation_conserved: bool,
    pub all_dual_gaps_zero: bool,
    pub min_phi1_rational: BigRational,
    pub gamma_threshold: BigRational,
}

pub fn evaluate_nerve_chaining(
    divisions: usize,
    scale: i128,
) -> Result<NerveChainingMasterReport, NerveChainingError> {
    let chaining = CollarNerveChaining::from_grid(divisions)?;
    let area_conserved = chaining.total_area == BigRational::one();

    let tri_deltoid = BoundaryNerveTriangle::deltoid();
    let tri_tao = BoundaryNerveTriangle::tao();

    let rep_deltoid = solve_triangular_circulation(&tri_deltoid, None, scale)?;
    let rep_tao = solve_triangular_circulation(&tri_tao, None, scale)?;

    let triangular_reports = vec![rep_deltoid, rep_tao];

    let all_phi1_ge_gamma = triangular_reports.iter().all(|r| r.phi1_ge_gamma);
    let all_circulation_conserved = triangular_reports.iter().all(|r| r.circulation_conserved);
    let all_dual_gaps_zero = triangular_reports.iter().all(|r| r.dual_gap_zero);

    let min_phi1_rational = triangular_reports
        .iter()
        .map(|r| r.phi1_rational.clone())
        .min()
        .unwrap_or_else(BigRational::zero);

    let gamma_threshold = circulation_gamma_threshold();

    Ok(NerveChainingMasterReport {
        firewall_line: FIREWALL.to_string(),
        authority_effect: AUTHORITY_EFFECT.to_string(),
        scope: SCOPE.to_string(),
        mathematical_certification: false,
        collar_overlap_verified: false,
        curvature_to_cochain_verified: false,
        num_collar_boxes: chaining.bindings.len(),
        total_collar_area: chaining.total_area,
        area_conserved,
        triangular_reports,
        all_phi1_ge_gamma,
        all_circulation_conserved,
        all_dual_gaps_zero,
        min_phi1_rational,
        gamma_threshold,
    })
}
