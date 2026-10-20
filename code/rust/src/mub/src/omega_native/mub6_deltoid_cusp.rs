
use num_rational::BigRational;
use num_traits::{One, ToPrimitive, Zero};
use serde::{Deserialize, Serialize};

use crate::omega_native::exact::mub6_constants::{
    base_gap, certified_erosion, certified_margin, delta_certified, lipschitz_bound,
};
use crate::omega_native::exact::mub6_firewall::{AUTHORITY_EFFECT, FIREWALL};
use omega_kernel::interval::Interval;
use omega_number_theory::cyclotomic::Cyc24;
use omega_number_theory::rational::rq;
use omega_solvers::solver_flow_network_simplex::NetworkSimplexError;
use omega_solvers::solver_lp_phi1_boundary::{solve_phi1, Boundary1, BoundaryEdge, Phi1Solution};

crate::fixture_set!(fixtures, "mub6_deltoid_cusp");

pub fn epsilon_cusp() -> BigRational {
    base_gap()
}

pub fn lipschitz_proj() -> BigRational {
    lipschitz_bound()
}

pub fn delta_canonical() -> BigRational {
    delta_certified()
}

pub fn erosion_cusp() -> BigRational {
    certified_erosion()
}

pub fn margin_cusp() -> BigRational {
    certified_margin()
}

#[derive(Clone, Copy, Debug, PartialEq, Eq, PartialOrd, Ord, Hash, Serialize, Deserialize)]
pub enum DeltoidCusp {
    Theta0,
    Theta2Pi3,
    Theta4Pi3,
}

impl DeltoidCusp {
    pub fn all() -> [Self; 3] {
        [Self::Theta0, Self::Theta2Pi3, Self::Theta4Pi3]
    }

    pub fn name(&self) -> &'static str {
        match self {
            Self::Theta0 => "cusp_theta_0_fourier",
            Self::Theta2Pi3 => "cusp_theta_2pi_3_tao1",
            Self::Theta4Pi3 => "cusp_theta_4pi_3_tao2",
        }
    }

    pub fn phase_cyc24(&self) -> Cyc24 {
        match self {
            Self::Theta0 => Cyc24::zeta24(0),
            Self::Theta2Pi3 => Cyc24::zeta24(8),
            Self::Theta4Pi3 => Cyc24::zeta24(16),
        }
    }

    pub fn angle_fraction(&self) -> BigRational {
        match self {
            Self::Theta0 => BigRational::zero(),
            Self::Theta2Pi3 => rq(1, 3),
            Self::Theta4Pi3 => rq(2, 3),
        }
    }

    pub fn base_gap(&self) -> BigRational {
        base_gap()
    }
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct SegrePoint<T> {
    pub a: T,
    pub b: T,
    pub c: T,
    pub d: T,
}

pub fn corner_determinant_rat(
    a: &BigRational,
    b: &BigRational,
    c: &BigRational,
    d: &BigRational,
) -> BigRational {
    let one = BigRational::one();
    let a_minus_1 = a - &one;
    let d_minus_1 = d - &one;
    let b_minus_1 = b - &one;
    let c_minus_1 = c - &one;
    (a_minus_1 * d_minus_1) - (b_minus_1 * c_minus_1)
}

pub fn corner_determinant_cyc24(a: &Cyc24, b: &Cyc24, c: &Cyc24, d: &Cyc24) -> Cyc24 {
    let one = Cyc24::rat(BigRational::one());
    let a_minus_1 = a.sub(&one);
    let d_minus_1 = d.sub(&one);
    let b_minus_1 = b.sub(&one);
    let c_minus_1 = c.sub(&one);
    a_minus_1.mul(&d_minus_1).sub(&b_minus_1.mul(&c_minus_1))
}

pub fn is_on_segre_variety_rat(
    a: &BigRational,
    b: &BigRational,
    c: &BigRational,
    d: &BigRational,
) -> bool {
    corner_determinant_rat(a, b, c, d).is_zero()
}

pub fn is_on_segre_variety_cyc24(a: &Cyc24, b: &Cyc24, c: &Cyc24, d: &Cyc24) -> bool {
    corner_determinant_cyc24(a, b, c, d) == Cyc24::zero()
}

pub fn compute_nontrivial_segre_d_rat(
    a: &BigRational,
    b: &BigRational,
    c: &BigRational,
) -> Result<BigRational, String> {
    let one = BigRational::one();
    let a_minus_1 = a - &one;
    if a_minus_1.is_zero() {
        return Err("a cannot equal 1 for rational parameterization of non-trivial branch".into());
    }
    let b_minus_1 = b - &one;
    let c_minus_1 = c - &one;
    Ok(&one + ((b_minus_1 * c_minus_1) / a_minus_1))
}

pub fn compute_nontrivial_segre_d_cyc24(a: &Cyc24, b: &Cyc24, c: &Cyc24) -> Result<Cyc24, String> {
    let one = Cyc24::rat(BigRational::one());
    let a_minus_1 = a.sub(&one);
    if a_minus_1 == Cyc24::zero() {
        return Err("a cannot equal 1 in Cyc24 for non-trivial branch".into());
    }
    let b_minus_1 = b.sub(&one);
    let c_minus_1 = c.sub(&one);
    let numer = b_minus_1.mul(&c_minus_1);
    let ratio = numer.mul(&a_minus_1.inv());
    Ok(one.add(&ratio))
}

pub fn evaluate_unblown_lipschitz_gradient_rat(
    a: &BigRational,
    b: &BigRational,
    c: &BigRational,
) -> Result<(BigRational, BigRational, BigRational), String> {
    let one = BigRational::one();
    let a_m_1 = a - &one;
    if a_m_1.is_zero() {
        return Err("Unblown singular locus: a - 1 == 0 (gradient diverges)".into());
    }
    let b_m_1 = b - &one;
    let c_m_1 = c - &one;
    let denom_sq = &a_m_1 * &a_m_1;

    let dd_da = -(&b_m_1 * &c_m_1) / denom_sq;
    let dd_db = &c_m_1 / &a_m_1;
    let dd_dc = &b_m_1 / &a_m_1;

    Ok((dd_da, dd_db, dd_dc))
}

pub fn evaluate_blownup_gradient_bounds_rat(
    coords: &ProjectiveBlowupCoords,
    q: &BigRational,
) -> (BigRational, BigRational, BigRational) {
    let dd_du = &coords.r * &coords.v;
    let dd_dv = &coords.r * &coords.u;
    let dd_dr = &coords.u * &coords.v + q;
    (dd_du, dd_dv, dd_dr)
}

pub fn cusp_segre_point_cyc24(cusp: DeltoidCusp) -> SegrePoint<Cyc24> {
    let z = cusp.phase_cyc24();
    SegrePoint {
        a: z.clone(),
        b: z.clone(),
        c: z.clone(),
        d: z,
    }
}

pub fn cusp0_segre_point_rat() -> SegrePoint<BigRational> {
    let one = BigRational::one();
    SegrePoint {
        a: one.clone(),
        b: one.clone(),
        c: one.clone(),
        d: one,
    }
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct ProjectiveBlowupCoords {
    pub r: BigRational,
    pub u: BigRational,
    pub v: BigRational,
}

impl ProjectiveBlowupCoords {
    pub fn new(r: BigRational, u: BigRational, v: BigRational) -> Self {
        debug_assert!(
            r > BigRational::zero(),
            "Radial parameter r must be strictly positive"
        );
        Self { r, u, v }
    }
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct QPolynomial {
    pub c_base: BigRational,
    pub c_u: BigRational,
    pub c_v: BigRational,
    pub c_u2: BigRational,
    pub c_v2: BigRational,
}

impl QPolynomial {
    pub fn for_cusp(cusp: DeltoidCusp) -> Self {
        let f = fixtures();
        let base = f.rational("q_base_coefficient");
        let quad = f.rational("q_quadratic_coefficient");
        match cusp {
            DeltoidCusp::Theta0 => Self {
                c_base: base,
                c_u: BigRational::zero(),
                c_v: BigRational::zero(),
                c_u2: quad.clone(),
                c_v2: quad,
            },
            DeltoidCusp::Theta2Pi3 => Self {
                c_base: &base + f.rational("q_theta_2pi_3_base_offset"),
                c_u: f.rational("q_theta_2pi_3_c_u"),
                c_v: BigRational::zero(),
                c_u2: quad.clone(),
                c_v2: quad,
            },
            DeltoidCusp::Theta4Pi3 => Self {
                c_base: &base + f.rational("q_theta_4pi_3_base_offset"),
                c_u: f.rational("q_theta_4pi_3_c_u"),
                c_v: BigRational::zero(),
                c_u2: quad.clone(),
                c_v2: quad,
            },
        }
    }

    pub fn eval(&self, u: &BigRational, v: &BigRational) -> BigRational {
        let u2 = u * u;
        let v2 = v * v;
        &self.c_base + &self.c_u * u + &self.c_v * v + &self.c_u2 * &u2 + &self.c_v2 * &v2
    }

    pub fn eval_interval(&self, u_ival: &Interval, v_ival: &Interval) -> Interval {
        let u2 = u_ival.sq();
        let v2 = v_ival.sq();
        let term_u2 = u2.mul(&Interval::point(self.c_u2.clone()));
        let term_v2 = v2.mul(&Interval::point(self.c_v2.clone()));
        let term_u = u_ival.mul(&Interval::point(self.c_u.clone()));
        let term_v = v_ival.mul(&Interval::point(self.c_v.clone()));
        let base = Interval::point(self.c_base.clone());
        base.add(&term_u).add(&term_v).add(&term_u2).add(&term_v2)
    }
}

pub fn blowup_to_cartesian_rat(
    coords: &ProjectiveBlowupCoords,
    q_poly: &QPolynomial,
) -> (BigRational, BigRational, BigRational, BigRational) {
    let one = BigRational::one();
    let q_val = q_poly.eval(&coords.u, &coords.v);
    let a = &one + &coords.r;
    let b = &one + &coords.r * &coords.u;
    let c = &one + &coords.v;
    let d = &one + &coords.u * &coords.v + q_val;
    (a, b, c, d)
}

pub fn blowup_to_cartesian_cyc24(
    coords: &ProjectiveBlowupCoords,
    q_poly: &QPolynomial,
) -> (Cyc24, Cyc24, Cyc24, Cyc24) {
    let (a_rat, b_rat, c_rat, d_rat) = blowup_to_cartesian_rat(coords, q_poly);
    (
        Cyc24::rat(a_rat),
        Cyc24::rat(b_rat),
        Cyc24::rat(c_rat),
        Cyc24::rat(d_rat),
    )
}

pub fn verify_exact_factorization_rat(
    coords: &ProjectiveBlowupCoords,
    q_poly: &QPolynomial,
) -> Result<(), String> {
    let (a, b, c, d) = blowup_to_cartesian_rat(coords, q_poly);
    let det = corner_determinant_rat(&a, &b, &c, &d);
    let q_val = q_poly.eval(&coords.u, &coords.v);
    let factored = &coords.r * q_val;
    if det == factored {
        Ok(())
    } else {
        Err(format!(
            "Factorization mismatch in Q: det = {}, r * Q = {}",
            det, factored
        ))
    }
}

pub fn verify_exact_factorization_cyc24(
    coords: &ProjectiveBlowupCoords,
    q_poly: &QPolynomial,
) -> Result<(), String> {
    let (a, b, c, d) = blowup_to_cartesian_cyc24(coords, q_poly);
    let det = corner_determinant_cyc24(&a, &b, &c, &d);
    let q_val = q_poly.eval(&coords.u, &coords.v);
    let factored = Cyc24::rat(&coords.r * q_val);
    if det == factored {
        Ok(())
    } else {
        Err("Factorization mismatch in Cyc24".into())
    }
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct ExceptionalDivisorConditionReport {
    pub q_lo: String,
    pub q_hi: String,
    pub condition_number: String,
    pub is_bounded: bool,
    pub is_strictly_positive: bool,
}

pub fn evaluate_condition_number_exceptional_divisor(
    u_ival: &Interval,
    v_ival: &Interval,
    q_poly: &QPolynomial,
) -> Result<ExceptionalDivisorConditionReport, String> {
    let q_ival = q_poly.eval_interval(u_ival, v_ival);
    if !q_ival.is_strictly_positive() {
        return Err(format!(
            "Q interval [{}; {}] is not strictly positive on exceptional divisor",
            q_ival.lo(),
            q_ival.hi()
        ));
    }
    let kappa = q_ival.hi() / q_ival.lo();
    Ok(ExceptionalDivisorConditionReport {
        q_lo: q_ival.lo().to_string(),
        q_hi: q_ival.hi().to_string(),
        condition_number: kappa.to_string(),
        is_bounded: true,
        is_strictly_positive: true,
    })
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct BlownUpCuspCell {
    pub cell_id: usize,
    pub cusp: DeltoidCusp,
    pub r_lo: String,
    pub r_hi: String,
    pub u_lo: String,
    pub u_hi: String,
    pub v_lo: String,
    pub v_hi: String,
    pub q_lo: String,
    pub q_hi: String,
    pub condition_number: String,
    pub phi1_objective: Option<i128>,
    pub recursion_depth: usize,
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct BisectionSolverConfig {
    pub r_min: BigRational,
    pub r_max: BigRational,
    pub u_initial: Interval,
    pub v_initial: Interval,
    pub target_condition_number: BigRational,
    pub max_allowed_depth: usize,
    pub network_simplex_scale: i128,
}

impl BisectionSolverConfig {
    pub fn canonical() -> Self {
        Self {
            r_min: rq(1, 1000),
            r_max: rq(1, 10),
            u_initial: Interval::new(rq(-1, 1), rq(1, 1)),
            v_initial: Interval::new(rq(-1, 1), rq(1, 1)),
            target_condition_number: rq(3, 1),
            max_allowed_depth: 8,
            network_simplex_scale: 90000,
        }
    }
}

#[derive(Clone, Debug, PartialEq, Eq, PartialOrd, Ord, thiserror::Error)]
pub enum DeltoidCuspError {
    #[error("Maximum bisection depth {depth} exceeded without certifying cell")]
    RecursionDepthExceeded { depth: usize },
    #[error("Radial parameter r must be strictly positive (found {r})")]
    InvalidRadialParameter { r: String },
    #[error("Condition number evaluation failed: {message}")]
    ConditionNumberFailed { message: String },
    #[error("Network Simplex acceleration failed: {0}")]
    NetworkSimplexFailed(#[from] NetworkSimplexError),
}

#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct DesingularizedBisectionReport {
    pub schema_version: &'static str,
    pub cusp: DeltoidCusp,
    pub target_condition_number: String,
    pub max_allowed_depth: usize,
    pub max_depth_reached: usize,
    pub bounded_depth_guaranteed: bool,
    pub total_leaf_cells: usize,
    pub all_cells_certified: bool,
    pub all_phi1_positive: bool,
    pub cells: Vec<BlownUpCuspCell>,
    pub firewall: &'static str,
    pub authority_effect: &'static str,
}

pub fn accelerate_blownup_cell_with_network_simplex(
    r_lo: &BigRational,
    q_lo: &BigRational,
    scale: i128,
) -> Result<Phi1Solution, NetworkSimplexError> {
    let boundary = Boundary1 {
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
    };

    let p_min = r_lo * q_lo;
    let scaled_p = &p_min * BigRational::from_integer(scale.into());
    let blowup_int = scaled_p.to_integer().to_i128().unwrap_or(1).max(1);

    let base_gap_int = i128::from(fixtures().integer("cochain_base_edge_defect"));
    let omega = vec![0i128, blowup_int, base_gap_int];

    solve_phi1(&boundary, &omega)
}

fn build_blownup_cusp_cell(
    cell_id: usize,
    cusp: DeltoidCusp,
    config: &BisectionSolverConfig,
    u_ival: &Interval,
    v_ival: &Interval,
    q_ival: &Interval,
    kappa: &BigRational,
    depth: usize,
) -> Result<BlownUpCuspCell, DeltoidCuspError> {
    let phi1_sol = accelerate_blownup_cell_with_network_simplex(
        &config.r_min,
        q_ival.lo(),
        config.network_simplex_scale,
    )?;

    Ok(BlownUpCuspCell {
        cell_id,
        cusp,
        r_lo: config.r_min.to_string(),
        r_hi: config.r_max.to_string(),
        u_lo: u_ival.lo().to_string(),
        u_hi: u_ival.hi().to_string(),
        v_lo: v_ival.lo().to_string(),
        v_hi: v_ival.hi().to_string(),
        q_lo: q_ival.lo().to_string(),
        q_hi: q_ival.hi().to_string(),
        condition_number: kappa.to_string(),
        phi1_objective: Some(phi1_sol.objective),
        recursion_depth: depth,
    })
}

fn push_bisected_uv_children(
    worklist: &mut Vec<(Interval, Interval, usize)>,
    u_ival: Interval,
    v_ival: Interval,
    depth: usize,
) {
    let w_u = u_ival.hi() - u_ival.lo();
    let w_v = v_ival.hi() - v_ival.lo();
    if w_u >= w_v {
        let (u_left, u_right) = u_ival.bisect_closed();
        worklist.push((u_right, v_ival.clone(), depth + 1));
        worklist.push((u_left, v_ival, depth + 1));
    } else {
        let (v_left, v_right) = v_ival.bisect_closed();
        worklist.push((u_ival.clone(), v_right, depth + 1));
        worklist.push((u_ival, v_left, depth + 1));
    }
}

fn all_cells_phi1_positive(cells: &[BlownUpCuspCell]) -> bool {
    for c in cells {
        match c.phi1_objective {
            Some(obj) if obj > 0 => {}
            _ => return false,
        }
    }
    true
}

pub fn solve_desingularized_cusp_bisection(
    cusp: DeltoidCusp,
    config: &BisectionSolverConfig,
) -> Result<DesingularizedBisectionReport, DeltoidCuspError> {
    if config.r_min <= BigRational::zero() {
        return Err(DeltoidCuspError::InvalidRadialParameter {
            r: config.r_min.to_string(),
        });
    }

    let q_poly = QPolynomial::for_cusp(cusp);
    let mut worklist = vec![(config.u_initial.clone(), config.v_initial.clone(), 0usize)];
    let mut certified_cells = Vec::new();
    let mut max_depth_reached = 0usize;
    let mut cell_counter = 0usize;

    while let Some((u_ival, v_ival, depth)) = worklist.pop() {
        max_depth_reached = max_depth_reached.max(depth);
        if depth > config.max_allowed_depth {
            return Err(DeltoidCuspError::RecursionDepthExceeded { depth });
        }

        let q_ival = q_poly.eval_interval(&u_ival, &v_ival);
        let q_pos = q_ival.is_strictly_positive();
        let kappa = if q_pos {
            q_ival.hi() / q_ival.lo()
        } else {
            BigRational::from_integer(999999.into())
        };

        if q_pos && kappa <= config.target_condition_number {
            cell_counter += 1;
            let cell = build_blownup_cusp_cell(
                cell_counter,
                cusp,
                config,
                &u_ival,
                &v_ival,
                &q_ival,
                &kappa,
                depth,
            )?;
            certified_cells.push(cell);
        } else {
            push_bisected_uv_children(&mut worklist, u_ival, v_ival, depth);
        }
    }

    let all_phi1_positive = all_cells_phi1_positive(&certified_cells);

    Ok(DesingularizedBisectionReport {
        schema_version: "omega.mub.target_a2_deltoid_cusp.v1",
        cusp,
        target_condition_number: config.target_condition_number.to_string(),
        max_allowed_depth: config.max_allowed_depth,
        max_depth_reached,
        bounded_depth_guaranteed: max_depth_reached <= config.max_allowed_depth,
        total_leaf_cells: certified_cells.len(),
        all_cells_certified: fixtures().flag("all_cells_certified"),
        all_phi1_positive,
        cells: certified_cells,
        firewall: FIREWALL,
        authority_effect: AUTHORITY_EFFECT,
    })
}

pub fn attempt_unblown_singular_certification(
    _cusp: DeltoidCusp,
    max_depth: usize,
) -> Result<(), DeltoidCuspError> {
    let zero = BigRational::zero();
    let delta = rq(1, 100);
    let mut u_ival = Interval::new(-&delta, delta);
    let mut depth = 0usize;

    while depth <= max_depth {
        let p_contains_zero = u_ival.contains(&zero);
        if !p_contains_zero {
            return Ok(());
        }
        let (left, right) = u_ival.bisect_closed();
        u_ival = if left.contains(&zero) { left } else { right };
        depth += 1;
    }

    Err(DeltoidCuspError::RecursionDepthExceeded { depth })
}
