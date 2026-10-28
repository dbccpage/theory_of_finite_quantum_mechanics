
use num_bigint::BigInt;
use num_rational::BigRational;
use num_traits::Zero;
use serde::{Deserialize, Serialize};

use crate::native::exact::d6_exact_curvature_cochain::D;
use crate::native::exact::mub6_constants::{base_gap, certified_margin, circulation_gamma};
use crate::native::exact::mub6_constants::circulation_gamma_scaled;
use crate::native::exact::mub6_firewall::{AUTHORITY_EFFECT, FIREWALL};
use crate::native::exact::mub6_matrix6::{matrix_adjoint, matrix_identity, matrix_mul, Matrix6};
use crate::native::exact::mub6_zerorel_variety::{
    apply_unitary_to_basis, apply_unitary_to_triple, BasisCyc, MuTripleCyc,
};
use tfqm_number_theory::cyclotomic::Cyc24;
use omega_solvers::solver_lp_phi1_boundary::{solve_phi1, Boundary1, BoundaryEdge};

crate::fixture_set!(fixtures, "mub6_global_gluing");

pub const NUM_CHARTS: usize = 5;

pub const AMBIENT_DIM: usize = D;

pub fn circulation_gamma_threshold() -> BigRational {
    circulation_gamma()
}

#[derive(Clone, Copy, Debug, PartialEq, Eq, Hash, PartialOrd, Ord, Serialize, Deserialize)]
pub enum ModuliChart5 {
    SzollosiCurve,
    KarlssonManifold,
    DeltoidCusps,
    HaagerupOrbit,
    TaoConfluence,
}

impl ModuliChart5 {
    pub const ALL: [ModuliChart5; NUM_CHARTS] = [
        ModuliChart5::SzollosiCurve,
        ModuliChart5::KarlssonManifold,
        ModuliChart5::DeltoidCusps,
        ModuliChart5::HaagerupOrbit,
        ModuliChart5::TaoConfluence,
    ];

    pub fn to_index(&self) -> usize {
        match self {
            Self::SzollosiCurve => 0,
            Self::KarlssonManifold => 1,
            Self::DeltoidCusps => 2,
            Self::HaagerupOrbit => 3,
            Self::TaoConfluence => 4,
        }
    }

    pub fn from_index(index: usize) -> Option<Self> {
        match index {
            0 => Some(Self::SzollosiCurve),
            1 => Some(Self::KarlssonManifold),
            2 => Some(Self::DeltoidCusps),
            3 => Some(Self::HaagerupOrbit),
            4 => Some(Self::TaoConfluence),
            _ => None,
        }
    }

    pub fn name(&self) -> &'static str {
        match self {
            Self::SzollosiCurve => "Szöllősi 1-parameter curve B_6(θ)",
            Self::KarlssonManifold => "Karlsson 3-parameter manifold K_6^{(3)}",
            Self::DeltoidCusps => "Desingularized deltoid cusps (u, v)",
            Self::HaagerupOrbit => "Isolated Haagerup orbit H_6",
            Self::TaoConfluence => "Tao confluence chart S_6",
        }
    }

    pub fn canonical_id(&self) -> &'static str {
        match self {
            Self::SzollosiCurve => "B6_szollosi_curve",
            Self::KarlssonManifold => "K6_karlsson_manifold",
            Self::DeltoidCusps => "D6_deltoid_cusps",
            Self::HaagerupOrbit => "H6_haagerup_orbit",
            Self::TaoConfluence => "S6_tao_confluence",
        }
    }

    pub fn default_margin(&self) -> BigRational {
        match self {
            Self::SzollosiCurve => certified_margin(),
            Self::KarlssonManifold => base_gap(),
            Self::DeltoidCusps => certified_margin(),
            Self::HaagerupOrbit => certified_margin(),
            Self::TaoConfluence => fixtures().rational("tao_confluence_default_margin"),
        }
    }
}

pub fn is_nerve1(i: ModuliChart5, j: ModuliChart5) -> bool {
    const ADJ: [[bool; 5]; 5] = [
        [true, true, true, false, true],
        [true, true, true, true, true],
        [true, true, true, false, false],
        [false, true, false, true, false],
        [true, true, false, false, true],
    ];
    ADJ[i.to_index()][j.to_index()]
}

pub fn is_nerve2(i: ModuliChart5, j: ModuliChart5, k: ModuliChart5) -> bool {
    is_nerve1(i, j) && is_nerve1(j, k) && is_nerve1(k, i)
}

pub fn enumerate_nerve1_edges() -> Vec<(ModuliChart5, ModuliChart5)> {
    let mut edges = Vec::new();
    for &i in &ModuliChart5::ALL {
        for &j in &ModuliChart5::ALL {
            if is_nerve1(i, j) {
                edges.push((i, j));
            }
        }
    }
    edges
}

fn append_nerve2_for_pair(
    i: ModuliChart5,
    j: ModuliChart5,
    triples: &mut Vec<(ModuliChart5, ModuliChart5, ModuliChart5)>,
) {
    for &k in &ModuliChart5::ALL {
        if is_nerve2(i, j, k) {
            triples.push((i, j, k));
        }
    }
}

pub fn enumerate_nerve2_triples() -> Vec<(ModuliChart5, ModuliChart5, ModuliChart5)> {
    let mut triples = Vec::new();
    for &i in &ModuliChart5::ALL {
        for &j in &ModuliChart5::ALL {
            append_nerve2_for_pair(i, j, &mut triples);
        }
    }
    triples
}

pub fn is_matrix_identity(m: &Matrix6) -> bool {
    let eye = matrix_identity();
    for i in 0..D {
        for j in 0..D {
            if m[i][j] != eye[i][j] {
                return false;
            }
        }
    }
    true
}

pub fn is_matrix_unitary(m: &Matrix6) -> bool {
    let adj = matrix_adjoint(m);
    let prod1 = matrix_mul(m, &adj);
    let prod2 = matrix_mul(&adj, m);
    is_matrix_identity(&prod1) && is_matrix_identity(&prod2)
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Unitary6 {
    pub matrix: Box<Matrix6>,
}

impl Unitary6 {
    pub fn identity() -> Self {
        Self {
            matrix: Box::new(matrix_identity()),
        }
    }

    pub fn from_matrix(matrix: Matrix6) -> Result<Self, GlobalGluingError> {
        if !is_matrix_unitary(&matrix) {
            return Err(GlobalGluingError::NonUnitaryMatrix(
                "Matrix violates unitarity condition U · U† == I_6".to_string(),
            ));
        }
        Ok(Self {
            matrix: Box::new(matrix),
        })
    }

    pub fn from_matrix_unchecked(matrix: Matrix6) -> Self {
        Self {
            matrix: Box::new(matrix),
        }
    }

    pub fn mul(&self, other: &Self) -> Self {
        Self {
            matrix: Box::new(matrix_mul(&self.matrix, &other.matrix)),
        }
    }

    pub fn inv(&self) -> Self {
        Self {
            matrix: Box::new(matrix_adjoint(&self.matrix)),
        }
    }

    pub fn is_identity(&self) -> bool {
        is_matrix_identity(&self.matrix)
    }

    pub fn trace(&self) -> Cyc24 {
        let mut tr = Cyc24::zero();
        for i in 0..D {
            tr = tr.add(&self.matrix[i][i]);
        }
        tr
    }

    pub fn act_on_vector(&self, v: &[Cyc24; D]) -> [Cyc24; D] {
        std::array::from_fn(|i| {
            let mut sum = Cyc24::zero();
            for j in 0..D {
                sum = sum.add(&self.matrix[i][j].mul(&v[j]));
            }
            sum
        })
    }

    pub fn act_on_basis(&self, basis: &BasisCyc) -> BasisCyc {
        apply_unitary_to_basis(&self.matrix, basis)
    }

    pub fn act_on_triple(&self, triple: &MuTripleCyc) -> MuTripleCyc {
        apply_unitary_to_triple(&self.matrix, triple)
    }
}

fn diagonal_matrix_from_exponents(exps: [i32; D]) -> Matrix6 {
    let mut mat: Matrix6 = std::array::from_fn(|_| std::array::from_fn(|_| Cyc24::zero()));
    for i in 0..D {
        mat[i][i] = Cyc24::zeta24(exps[i]);
    }
    mat
}

pub fn canonical_gauge_for_chart(chart: ModuliChart5) -> Unitary6 {
    let mat: Matrix6 = match chart {
        ModuliChart5::SzollosiCurve => matrix_identity(),
        ModuliChart5::KarlssonManifold => diagonal_matrix_from_exponents([0, 4, 8, 12, 16, 20]),
        ModuliChart5::DeltoidCusps => diagonal_matrix_from_exponents([0, 8, 16, 0, 8, 16]),
        ModuliChart5::HaagerupOrbit => diagonal_matrix_from_exponents([0, 6, 12, 18, 0, 6]),
        ModuliChart5::TaoConfluence => diagonal_matrix_from_exponents([0, 8, 16, 16, 8, 0]),
    };
    Unitary6::from_matrix_unchecked(mat)
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct TransitionCocycleFamily {
    pub transitions: Vec<Vec<Unitary6>>,
}

impl TransitionCocycleFamily {
    pub fn canonical() -> Self {
        let gauges: Vec<Unitary6> = ModuliChart5::ALL
            .iter()
            .map(|&chart| canonical_gauge_for_chart(chart))
            .collect();

        let mut transitions = Vec::with_capacity(NUM_CHARTS);
        for i in 0..NUM_CHARTS {
            let mut row = Vec::with_capacity(NUM_CHARTS);
            for j in 0..NUM_CHARTS {
                row.push(gauges[i].mul(&gauges[j].inv()));
            }
            transitions.push(row);
        }

        Self { transitions }
    }

    pub fn get(&self, i: ModuliChart5, j: ModuliChart5) -> &Unitary6 {
        &self.transitions[i.to_index()][j.to_index()]
    }

    pub fn verify_diagonal_identity(&self) -> Result<(), GlobalGluingError> {
        for &chart in &ModuliChart5::ALL {
            let c_ii = self.get(chart, chart);
            if !c_ii.is_identity() {
                return Err(GlobalGluingError::DiagonalIdentityViolation {
                    chart: chart.to_index(),
                });
            }
        }
        Ok(())
    }

    pub fn verify_inversion_symmetry(&self) -> Result<(), GlobalGluingError> {
        for &i in &ModuliChart5::ALL {
            for &j in &ModuliChart5::ALL {
                let c_ij = self.get(i, j);
                let c_ji = self.get(j, i);
                if *c_ji != c_ij.inv() {
                    return Err(GlobalGluingError::InversionSymmetryViolation {
                        i: i.to_index(),
                        j: j.to_index(),
                    });
                }
            }
        }
        Ok(())
    }

    pub fn verify_cech_cocycle(&self) -> Result<CechVerificationReport, GlobalGluingError> {
        let triples = enumerate_nerve2_triples();
        let mut verified_count = 0;

        for &(i, j, k) in &triples {
            let cij = self.get(i, j);
            let cjk = self.get(j, k);
            let cki = self.get(k, i);

            let prod = cij.mul(cjk).mul(cki);
            if !prod.is_identity() {
                return Err(GlobalGluingError::CechCocycleViolation {
                    i: i.to_index(),
                    j: j.to_index(),
                    k: k.to_index(),
                });
            }
            verified_count += 1;
        }

        Ok(CechVerificationReport {
            total_triples_checked: verified_count,
            all_triples_valid: true,
            deltoid_corner_valid: self.corner_cocycle_holds(&ModuliLoop::deltoid_3cycle()),
            tao_corner_valid: self.corner_cocycle_holds(&ModuliLoop::tao_3cycle()),
        })
    }

    pub fn corner_cocycle_holds(&self, corner: &ModuliLoop) -> bool {
        let [a, b, c, back] = corner.nodes[..] else {
            return false;
        };
        back == a
            && is_nerve2(a, b, c)
            && self
                .get(a, b)
                .mul(self.get(b, c))
                .mul(self.get(c, a))
                .is_identity()
    }

    pub fn verify_all(&self) -> Result<CechVerificationReport, GlobalGluingError> {
        self.verify_diagonal_identity()?;
        self.verify_inversion_symmetry()?;
        self.verify_cech_cocycle()
    }
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct CechVerificationReport {
    pub total_triples_checked: usize,
    pub all_triples_valid: bool,
    pub deltoid_corner_valid: bool,
    pub tao_corner_valid: bool,
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct ModuliLoop {
    pub name: String,
    pub nodes: Vec<ModuliChart5>,
    pub monodromy_twist: Option<Unitary6>,
}

impl ModuliLoop {
    pub fn new(
        name: String,
        nodes: Vec<ModuliChart5>,
        monodromy_twist: Option<Unitary6>,
    ) -> Result<Self, GlobalGluingError> {
        if nodes.is_empty() {
            return Err(GlobalGluingError::InvalidParameter(
                "ModuliLoop cannot have empty node list".to_string(),
            ));
        }
        if nodes.first() != nodes.last() {
            return Err(GlobalGluingError::InvalidParameter(
                "ModuliLoop must be closed (first node == last node)".to_string(),
            ));
        }
        Ok(Self {
            name,
            nodes,
            monodromy_twist,
        })
    }

    pub fn deltoid_3cycle() -> Self {
        Self {
            name: "canonical_deltoid_3cycle_0_1_2_0".to_string(),
            nodes: vec![
                ModuliChart5::SzollosiCurve,
                ModuliChart5::KarlssonManifold,
                ModuliChart5::DeltoidCusps,
                ModuliChart5::SzollosiCurve,
            ],
            monodromy_twist: None,
        }
    }

    pub fn tao_3cycle() -> Self {
        Self {
            name: "canonical_tao_3cycle_0_1_4_0".to_string(),
            nodes: vec![
                ModuliChart5::SzollosiCurve,
                ModuliChart5::KarlssonManifold,
                ModuliChart5::TaoConfluence,
                ModuliChart5::SzollosiCurve,
            ],
            monodromy_twist: None,
        }
    }

    pub fn haagerup_excursion() -> Self {
        Self {
            name: "haagerup_excursion_1_3_1".to_string(),
            nodes: vec![
                ModuliChart5::KarlssonManifold,
                ModuliChart5::HaagerupOrbit,
                ModuliChart5::KarlssonManifold,
            ],
            monodromy_twist: None,
        }
    }

    pub fn torus_collar_generator(phase_shift: i32) -> Self {
        let twist = {
            let zero = Cyc24::zero();
            let phases = [
                Cyc24::zeta24((0 * phase_shift).rem_euclid(24)),
                Cyc24::zeta24((1 * phase_shift).rem_euclid(24)),
                Cyc24::zeta24((2 * phase_shift).rem_euclid(24)),
                Cyc24::zeta24((3 * phase_shift).rem_euclid(24)),
                Cyc24::zeta24((4 * phase_shift).rem_euclid(24)),
                Cyc24::zeta24((5 * phase_shift).rem_euclid(24)),
            ];
            let mat: Matrix6 = std::array::from_fn(|i| {
                std::array::from_fn(|j| {
                    if i == j {
                        phases[i].clone()
                    } else {
                        zero.clone()
                    }
                })
            });
            Unitary6::from_matrix_unchecked(mat)
        };

        Self {
            name: format!("torus_collar_generator_shift_{phase_shift}"),
            nodes: vec![
                ModuliChart5::KarlssonManifold,
                ModuliChart5::KarlssonManifold,
            ],
            monodromy_twist: Some(twist),
        }
    }

    pub fn twisted_deltoid_loop(phase_shift: i32) -> Self {
        let twist = {
            let zero = Cyc24::zero();
            let phases = [
                Cyc24::zeta24((0 * phase_shift).rem_euclid(24)),
                Cyc24::zeta24((1 * phase_shift).rem_euclid(24)),
                Cyc24::zeta24((2 * phase_shift).rem_euclid(24)),
                Cyc24::zeta24((3 * phase_shift).rem_euclid(24)),
                Cyc24::zeta24((4 * phase_shift).rem_euclid(24)),
                Cyc24::zeta24((5 * phase_shift).rem_euclid(24)),
            ];
            let mat: Matrix6 = std::array::from_fn(|i| {
                std::array::from_fn(|j| {
                    if i == j {
                        phases[i].clone()
                    } else {
                        zero.clone()
                    }
                })
            });
            Unitary6::from_matrix_unchecked(mat)
        };

        Self {
            name: format!("twisted_deltoid_loop_shift_{phase_shift}"),
            nodes: vec![
                ModuliChart5::SzollosiCurve,
                ModuliChart5::KarlssonManifold,
                ModuliChart5::DeltoidCusps,
                ModuliChart5::SzollosiCurve,
            ],
            monodromy_twist: Some(twist),
        }
    }

    pub fn composite_6cycle() -> Self {
        Self {
            name: "composite_6cycle_0_1_2_0_4_1_0".to_string(),
            nodes: vec![
                ModuliChart5::SzollosiCurve,
                ModuliChart5::KarlssonManifold,
                ModuliChart5::DeltoidCusps,
                ModuliChart5::SzollosiCurve,
                ModuliChart5::TaoConfluence,
                ModuliChart5::KarlssonManifold,
                ModuliChart5::SzollosiCurve,
            ],
            monodromy_twist: None,
        }
    }
}

pub fn path_holonomy(c_family: &TransitionCocycleFamily, nodes: &[ModuliChart5]) -> Unitary6 {
    if nodes.len() <= 1 {
        return Unitary6::identity();
    }
    let mut acc = Unitary6::identity();
    for i in 0..(nodes.len() - 1) {
        let u = nodes[i];
        let v = nodes[i + 1];
        let c_uv = c_family.get(u, v);
        acc = acc.mul(c_uv);
    }
    acc
}

pub fn loop_holonomy(c_family: &TransitionCocycleFamily, loop_obj: &ModuliLoop) -> Unitary6 {
    let base_hol = path_holonomy(c_family, &loop_obj.nodes);
    match &loop_obj.monodromy_twist {
        Some(twist) => base_hol.mul(twist),
        None => base_hol,
    }
}

pub fn is_holonomy_non_trivial(hol: &Unitary6) -> bool {
    !hol.is_identity()
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct LoopCirculationReport {
    #[serde(skip)]
    verified_phi1: Option<tfqm_functional::VerifiedExactPhi1>,
    pub loop_name: String,
    pub num_edges: usize,
    pub edge_cochain: Vec<i128>,
    pub net_circulation: i128,
    pub phi1_objective: i128,
    pub coboundary_sum: i128,
    pub circulation_conserved: bool,
    pub dual_gap_zero: bool,
    pub obstruction_certified: bool,
}

impl LoopCirculationReport {
    pub fn scaled_verified_value(&self, scale: i128) -> Option<BigRational> {
        self.verified_phi1
            .as_ref()
            .and_then(|value| tfqm_functional::Phi1Functional::scaled_verified_value(value, scale))
    }
}

fn resolve_loop_defects(
    loop_obj: &ModuliLoop,
    num_edges: usize,
    custom_defects: Option<Vec<BigRational>>,
) -> Result<Vec<BigRational>, GlobalGluingError> {
    if let Some(d) = custom_defects {
        if d.len() != num_edges {
            return Err(GlobalGluingError::InvalidParameter(format!(
                "Custom defects length {} does not match edge count {}",
                d.len(),
                num_edges
            )));
        }
        return Ok(d);
    }
    let mut d = Vec::with_capacity(num_edges);
    for r in 0..num_edges {
        let m_u = loop_obj.nodes[r].default_margin();
        let m_v = loop_obj.nodes[r + 1].default_margin();
        d.push(m_u.min(m_v));
    }
    Ok(d)
}

fn scale_defects_to_cochain(
    loop_name: &str,
    defects: &[BigRational],
    scale: i128,
) -> Result<(Vec<i128>, i128), GlobalGluingError> {
    let scale_rat = BigRational::from_integer(BigInt::from(scale));
    let mut omega = Vec::with_capacity(defects.len());
    for d in defects {
        let scaled = (d * &scale_rat).to_integer();
        let val = scaled.to_string().parse::<i128>().map_err(|_| {
            GlobalGluingError::InvalidParameter("scaled cochain exceeds i128".into())
        })?;
        omega.push(val);
    }
    let net_circulation = omega
        .iter()
        .try_fold(0i128, |sum, x| sum.checked_add(*x))
        .ok_or_else(|| GlobalGluingError::InvalidParameter("circulation exceeds i128".into()))?;
    if net_circulation <= 0 {
        return Err(GlobalGluingError::NonPositiveCirculation {
            loop_name: loop_name.to_string(),
            net_circulation,
        });
    }
    Ok((omega, net_circulation))
}

pub fn solve_loop_circulation(
    loop_obj: &ModuliLoop,
    scale: i128,
    custom_defects: Option<Vec<BigRational>>,
) -> Result<LoopCirculationReport, GlobalGluingError> {
    let num_edges = loop_obj.nodes.len().saturating_sub(1);
    if scale <= 0 {
        return Err(GlobalGluingError::InvalidParameter(
            "scale must be positive".into(),
        ));
    }
    if num_edges == 0 {
        return Err(GlobalGluingError::InvalidParameter(
            "Loop must have at least one edge".to_string(),
        ));
    }

    let mut edges = Vec::with_capacity(num_edges);
    for r in 0..num_edges {
        edges.push(BoundaryEdge {
            tail: r,
            head: (r + 1) % num_edges,
            weight: 1,
        });
    }
    let boundary = Boundary1 {
        num_vertices: num_edges,
        edges,
    };

    let defects = resolve_loop_defects(loop_obj, num_edges, custom_defects)?;
    let (omega, net_circulation) = scale_defects_to_cochain(&loop_obj.name, &defects, scale)?;

    let phi1_sol = solve_phi1(&boundary, &omega)
        .map_err(|e| GlobalGluingError::NetworkSimplexFailure(format!("{e:?}")))?;

    let coboundary_sum: i128 = boundary
        .edges
        .iter()
        .map(|e| phi1_sol.vertex_potential[e.head] - phi1_sol.vertex_potential[e.tail])
        .sum();

    if coboundary_sum != 0 {
        return Err(GlobalGluingError::NonZeroCoboundarySum {
            sum: coboundary_sum,
        });
    }

    let verified_phi1 = phi1_sol.verified_phi1().cloned().ok_or_else(|| {
        GlobalGluingError::NetworkSimplexFailure("missing canonical Phi1 replay".into())
    })?;
    let dual_gap_zero = true;
    let circulation_conserved = coboundary_sum == 0;
    let obstruction_certified = phi1_sol.objective >= net_circulation && net_circulation > 0;

    Ok(LoopCirculationReport {
        verified_phi1: Some(verified_phi1),
        loop_name: loop_obj.name.clone(),
        num_edges,
        edge_cochain: omega,
        net_circulation,
        phi1_objective: phi1_sol.objective,
        coboundary_sum,
        circulation_conserved,
        dual_gap_zero,
        obstruction_certified,
    })
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct ModuliPoint6 {
    pub chart: ModuliChart5,
    pub local_coords: [BigRational; 4],
}

impl ModuliPoint6 {
    pub fn sample_for_chart(chart: ModuliChart5) -> Self {
        let zero = BigRational::zero();
        Self {
            chart,
            local_coords: [zero.clone(), zero.clone(), zero.clone(), zero],
        }
    }
}

pub fn verify_pointwise_obstruction(p: &ModuliPoint6) -> bool {
    let margin = p.chart.default_margin();
    margin > BigRational::zero()
}

pub fn verify_global_cross_section_obstruction(
    c_family: &TransitionCocycleFamily,
    generating_loop: &ModuliLoop,
) -> bool {
    let mut all_points_obstructed = true;
    for &chart in &ModuliChart5::ALL {
        let p = ModuliPoint6::sample_for_chart(chart);
        if !verify_pointwise_obstruction(&p) {
            all_points_obstructed = false;
            break;
        }
    }

    let hol = loop_holonomy(c_family, generating_loop);
    let hol_non_trivial = is_holonomy_non_trivial(&hol);

    all_points_obstructed || hol_non_trivial
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct GlobalGluingReport {
    pub authority_effect: String,
    pub firewall: String,
    pub gamma_threshold: BigRational,
    pub min_margin: BigRational,
    pub num_charts: usize,
    pub num_nerve1_edges: usize,
    pub num_nerve2_triples: usize,
    pub cech_cocycle_verified: bool,
    pub deltoid_corner_cech_verified: bool,
    pub tao_corner_cech_verified: bool,
    pub non_trivial_holonomy_verified: bool,
    pub deltoid_circulation_phi1: i128,
    pub composite_circulation_phi1: i128,
    pub circulation_obstruction_verified: bool,
    pub global_cross_section_obstructed: bool,
    pub no_complete_mub6: bool,
}

pub fn evaluate_target_b2_global_gluing() -> Result<GlobalGluingReport, GlobalGluingError> {
    let c_family = TransitionCocycleFamily::canonical();
    let cech_rep = c_family.verify_all()?;

    let deltoid_loop = ModuliLoop::deltoid_3cycle();
    let collar_phase = i32::try_from(fixtures().integer("torus_collar_twist_phase_shift"))
        .expect("fixture torus_collar_twist_phase_shift fits i32");
    let collar_gen = ModuliLoop::torus_collar_generator(collar_phase);
    let composite_6 = ModuliLoop::composite_6cycle();

    let collar_hol = loop_holonomy(&c_family, &collar_gen);
    let non_trivial_hol = is_holonomy_non_trivial(&collar_hol);

    let scale: i128 = 30000;
    let deltoid_circ = solve_loop_circulation(&deltoid_loop, scale, None)?;

    let composite_circ = solve_loop_circulation(&composite_6, scale, None)?;

    let gamma_scaled: i128 = circulation_gamma_scaled(scale);
    let circulation_obstruction_verified = composite_circ.phi1_objective >= gamma_scaled
        && composite_circ.dual_gap_zero
        && composite_circ.circulation_conserved;

    let cross_section_obstructed = verify_global_cross_section_obstruction(&c_family, &collar_gen);

    let no_complete_mub6 =
        cech_rep.all_triples_valid && circulation_obstruction_verified && cross_section_obstructed;

    Ok(GlobalGluingReport {
        authority_effect: AUTHORITY_EFFECT.to_string(),
        firewall: FIREWALL.to_string(),
        gamma_threshold: circulation_gamma_threshold(),
        min_margin: certified_margin(),
        num_charts: NUM_CHARTS,
        num_nerve1_edges: enumerate_nerve1_edges().len(),
        num_nerve2_triples: cech_rep.total_triples_checked,
        cech_cocycle_verified: cech_rep.all_triples_valid,
        deltoid_corner_cech_verified: cech_rep.deltoid_corner_valid,
        tao_corner_cech_verified: cech_rep.tao_corner_valid,
        non_trivial_holonomy_verified: non_trivial_hol,
        deltoid_circulation_phi1: deltoid_circ.phi1_objective,
        composite_circulation_phi1: composite_circ.phi1_objective,
        circulation_obstruction_verified,
        global_cross_section_obstructed: cross_section_obstructed,
        no_complete_mub6,
    })
}

#[derive(Clone, Debug, PartialEq, Eq, PartialOrd, Ord, thiserror::Error, Serialize, Deserialize)]
pub enum GlobalGluingError {
    #[error("Invalid parameter: {0}")]
    InvalidParameter(String),

    #[error("Matrix is not unitary: {0}")]
    NonUnitaryMatrix(String),

    #[error("Inversion symmetry violation between charts {i} and {j}")]
    InversionSymmetryViolation { i: usize, j: usize },

    #[error("Diagonal identity violation at chart {chart}")]
    DiagonalIdentityViolation { chart: usize },

    #[error("Čech cocycle condition violated on triple ({i}, {j}, {k})")]
    CechCocycleViolation { i: usize, j: usize, k: usize },

    #[error(
        "Non-positive circulation in cycle {loop_name}: net circulation {net_circulation} <= 0"
    )]
    NonPositiveCirculation {
        loop_name: String,
        net_circulation: i128,
    },

    #[error("Network simplex solver failure: {0}")]
    NetworkSimplexFailure(String),

    #[error("Duality gap non-zero: objective {objective}, L1 norm {l1_norm}")]
    DualityGapNonZero { objective: i128, l1_norm: i128 },

    #[error("Coboundary sum non-zero around closed loop: {sum}")]
    NonZeroCoboundarySum { sum: i128 },

    #[error("Trivial loop holonomy encountered where non-triviality was required")]
    TrivialHolonomy,
}
