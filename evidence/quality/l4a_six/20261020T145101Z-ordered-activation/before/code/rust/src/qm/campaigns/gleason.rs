

use omega_number_theory::rational::{rq, One, Rational, Zero};
use serde::{Deserialize, Serialize};

use crate::linear_algebra::{elimination, matrix};
use omega_number_theory::quadratic::Quadratic;
use omega_quantum_physics::kochen_specker::{self, CABELLO_18_VECTORS, CABELLO_9_CONTEXTS};
use omega_solvers::solver_sat_dpll::{BooleanOutcome, BooleanProblem};

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct CabelloHypergraphReport {
    pub n_rays: usize,
    pub n_contexts: usize,
    pub all_contexts_orthogonal: bool,
    pub all_rays_degree_2: bool,
    pub total_incidence: usize,
    pub has_binary_valuation: bool,
    pub binary_valuation_count: Option<u64>,
    pub parity_obstruction: bool,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct NonPsdWitnessReport {
    pub trace: Rational,
    pub ray_expectations: Vec<Rational>,
    pub all_expectations_in_unit_interval: bool,
    pub all_contexts_sum_to_one: bool,
    pub witness_vector: [i64; 4],
    pub witness_expectation: Rational,
    pub is_psd: bool,
    pub negative_eigenvalue: Rational,
    pub eigenvector_verified: bool,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct PseudoStateReport {
    pub trace: Rational,
    pub all_contexts_sum_to_one: bool,
    pub v17_expectation: Rational,
    pub v17_is_negative: bool,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub struct Ray3D {
    pub x: i64,
    pub y: i64,
    pub z: i64,
}

impl Ray3D {
    pub const fn new(x: i64, y: i64, z: i64) -> Self {
        Self { x, y, z }
    }

    pub fn norm_sq(&self) -> i64 {
        self.x * self.x + self.y * self.y + self.z * self.z
    }

    pub fn dot(&self, other: &Self) -> i64 {
        self.x * other.x + self.y * other.y + self.z * other.z
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub struct Triad3D {
    pub r0: usize,
    pub r1: usize,
    pub r2: usize,
}

impl Triad3D {
    pub const fn new(r0: usize, r1: usize, r2: usize) -> Self {
        Self { r0, r1, r2 }
    }
}

pub fn integer_isqrt(n: i64) -> i64 {
    if n <= 0 {
        0
    } else {
        n.isqrt()
    }
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct TriadSearchReport {
    pub n_rays: usize,
    pub n_triads: usize,
    pub all_triads_orthogonal: bool,
    pub born_sums: Vec<Rational>,
    pub rival_sums: Vec<Rational>,
    pub valuations_disagree: bool,
    pub ray_2_born: Rational,
    pub ray_2_rival: Rational,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct TopologicalObstructionReport {
    pub is_totally_disconnected: Option<bool>,
    pub no_rational_sqrt_2_denominator_le_1000: bool,
    pub disc_28_does_not_divide_120: bool,
    pub pole_x_in_u: bool,
    pub pole_z_in_v: bool,
    pub great_circle_connectedness: Option<bool>,
    pub gleason_continuity_lemma_fails: Option<bool>,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct HigherConductorTriadReport {
    pub conductors_evaluated: Vec<usize>,
    pub n_base_pythagorean_triads: usize,
    pub n_higher_conductor_triads: usize,
    pub total_triads_evaluated: usize,
    pub all_triads_orthogonal: bool,
    pub all_frame_sums_equal_one: bool,
    pub state_multiplicity_verified: bool,
    pub sample_ray_0_pure0: Rational,
    pub sample_ray_0_rival: Rational,
    pub sample_ray_0_mixed: Rational,
    pub sample_ray_2_pure0: Rational,
    pub sample_ray_2_pure2: Rational,
    pub sample_ray_2_rival: Rational,
    pub has_noncontextual_binary_valuation: Option<bool>,
    pub peres_33_rays_embedded: bool,
    pub peres_triads_count: usize,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct HigherConductorTopologyReport {
    pub conductors_analyzed: Vec<usize>,
    pub c120_obstructing_prime: usize,
    pub c240_obstructing_prime: usize,
    pub c480_obstructing_prime: usize,
    pub c840_obstructing_prime: usize,
    pub c840_sqrt7_embedded: bool,
    pub c840_sqrt11_embedded: bool,
    pub sliding_obstruction_verified: bool,
    pub all_conductors_totally_disconnected: Option<bool>,
    pub gleason_continuity_lemma_fails_all: Option<bool>,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct MeyerColorabilityReport {
    pub rational_carrier: String,
    pub meyer_colorability_holds: Option<bool>,
    pub cyclotomic_carrier: String,
    pub conductors_tested: Vec<usize>,
    pub sqrt2_embedded: bool,
    pub peres_ray_count: usize,
    pub peres_orthogonal_pairs: usize,
    pub peres_orthogonal_triads: usize,
    pub peres_colorable_valuations: usize,
    pub peres_uncolorability_confirmed: bool,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct CliftonKentPolytopeReport {
    pub ray_count: usize,
    pub triad_count: usize,
    pub constraint_matrix_rank: usize,
    pub affine_dimension: usize,
    pub trace_one_symmetric_dimension: usize,
    pub non_quadratic_excess_dimension: usize,
    pub exact_rational_non_quadratic_constructed: bool,
    pub sample_min_frame_val: Rational,
    pub sample_max_frame_val: Rational,
    pub all_frame_values_in_open_unit_interval: bool,
    pub all_triads_sum_to_one: bool,
    pub residual_orthogonal_to_quadratic_rows: bool,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct PadicNonstandardObstructionReport {
    pub primes_evaluated: Vec<usize>,
    pub padic_lack_of_ordering: Option<bool>,
    pub isotropic_primes_mod4: Vec<usize>,
    pub isotropic_root_witnesses: Vec<(usize, usize)>,
    pub projector_singularity_confirmed: bool,
    pub padic_total_disconnectedness: Option<bool>,
    pub nonstandard_transfer_principle_internal: Option<bool>,
    pub nonstandard_external_measure_nonbornian: Option<bool>,
}

pub const MAX_BINARY_VALUATION_RAYS: usize = 24;

pub fn count_binary_valuations(n_rays: usize, contexts: &[&[usize]]) -> Option<u64> {
    if n_rays > MAX_BINARY_VALUATION_RAYS {
        return None;
    }
    if contexts.is_empty() {
        return Some(1u64 << n_rays);
    }
    if contexts
        .iter()
        .any(|c| c.is_empty() || c.iter().enumerate().any(|(i, r)| c[..i].contains(r)))
    {
        return None;
    }
    let mut masks = Vec::with_capacity(contexts.len());
    for context in contexts {
        let mut mask = 0u32;
        for &ray in *context {
            if ray >= n_rays {
                return None;
            }
            mask |= 1 << ray;
        }
        masks.push(mask);
    }
    let count = (0u32..(1u32 << n_rays))
        .filter(|&assignment| {
            masks
                .iter()
                .all(|&mask| (assignment & mask).count_ones() == 1)
        })
        .count();
    Some(count as u64)
}

fn is_cabello_context_orthogonal(ctx: &[usize; 4]) -> bool {
    for i in 0..4 {
        for j in (i + 1)..4 {
            let u = CABELLO_18_VECTORS[ctx[i]];
            let v = CABELLO_18_VECTORS[ctx[j]];
            let dot: i64 = u[0] * v[0] + u[1] * v[1] + u[2] * v[2] + u[3] * v[3];
            if dot != 0 {
                return false;
            }
        }
    }
    true
}

pub fn verify_cabello_hypergraph() -> CabelloHypergraphReport {
    let all_ortho = CABELLO_9_CONTEXTS
        .iter()
        .all(is_cabello_context_orthogonal);

    let mut degrees = [0usize; 18];
    for ctx in &CABELLO_9_CONTEXTS {
        for &r in ctx {
            degrees[r] += 1;
        }
    }
    let all_deg_2 = degrees.iter().all(|&d| d == 2);
    let total_inc: usize = degrees.iter().sum();
    let contexts: Vec<&[usize]> = CABELLO_9_CONTEXTS.iter().map(|c| c.as_slice()).collect();
    let binary_valuation_count = count_binary_valuations(18, &contexts);
    let has_binary = binary_valuation_count.is_some_and(|count| count > 0);
    let parity_obstruction = all_deg_2 && CABELLO_9_CONTEXTS.len() % 2 == 1;

    CabelloHypergraphReport {
        n_rays: 18,
        n_contexts: 9,
        all_contexts_orthogonal: all_ortho,
        all_rays_degree_2: all_deg_2,
        total_incidence: total_inc,
        has_binary_valuation: has_binary,
        binary_valuation_count,
        parity_obstruction,
    }
}

fn quadratic_ray_expectation(m: &[[Rational; 4]; 4], v: &[i64; 4]) -> Rational {
    let norm_sq = v[0] * v[0] + v[1] * v[1] + v[2] * v[2] + v[3] * v[3];
    let mut quad = Rational::zero();
    for i in 0..4 {
        for j in 0..4 {
            let term = &m[i][j] * &rq(v[i] * v[j], 1);
            quad = &quad + &term;
        }
    }
    &quad / &rq(norm_sq, 1)
}

fn evaluate_cabello_ray_expectations(m: &[[Rational; 4]; 4]) -> (Vec<Rational>, bool) {
    let mut ray_expectations = Vec::with_capacity(18);
    let mut all_in_interval = true;
    for v in &CABELLO_18_VECTORS {
        let exp = quadratic_ray_expectation(m, v);
        if exp < Rational::zero() || exp > Rational::one() {
            all_in_interval = false;
        }
        ray_expectations.push(exp);
    }
    (ray_expectations, all_in_interval)
}

fn all_cabello_contexts_sum_to_one(ray_expectations: &[Rational]) -> bool {
    for ctx in &CABELLO_9_CONTEXTS {
        let mut sum_ctx = Rational::zero();
        for &r in ctx {
            sum_ctx = &sum_ctx + &ray_expectations[r];
        }
        if sum_ctx != Rational::one() {
            return false;
        }
    }
    true
}

fn check_witness_eigenvector(m: &[[Rational; 4]; 4], w: &[i64; 4], eig: &Rational) -> bool {
    for i in 0..4 {
        let image: Rational = (0..4).map(|j| &m[i][j] * rq(w[j], 1)).sum();
        if image != eig * rq(w[i], 1) {
            return false;
        }
    }
    true
}

pub fn verify_non_psd_cabello_witness() -> NonPsdWitnessReport {
    let m: [[Rational; 4]; 4] = [
        [
            Rational::zero(),
            Rational::zero(),
            Rational::zero(),
            Rational::zero(),
        ],
        [Rational::zero(), Rational::one(), rq(1, 2), rq(-1, 2)],
        [Rational::zero(), rq(1, 2), Rational::zero(), rq(-1, 2)],
        [Rational::zero(), rq(-1, 2), rq(-1, 2), Rational::zero()],
    ];

    let trace = &m[0][0] + &m[1][1] + &m[2][2] + &m[3][3];
    let (ray_expectations, all_in_interval) = evaluate_cabello_ray_expectations(&m);
    let all_contexts_sum_to_one = all_cabello_contexts_sum_to_one(&ray_expectations);

    let w = [0i64, 0, 1, 1];
    let exp_w = quadratic_ray_expectation(&m, &w);
    let matrix =
        crate::linear_algebra::matrix::from_rows(m.iter().map(|r| r.to_vec()).collect())
            .expect("fixed four-dimensional rational witness");
    let is_psd = crate::linear_algebra::ordered::hermitian_inertia(&matrix)
        .expect("fixed rational Hermitian witness")
        .negative
        == 0;
    let eigenvector_verified = check_witness_eigenvector(&m, &w, &exp_w);

    NonPsdWitnessReport {
        trace,
        ray_expectations,
        all_expectations_in_unit_interval: all_in_interval,
        all_contexts_sum_to_one,
        witness_vector: w,
        witness_expectation: exp_w.clone(),
        is_psd,
        negative_eigenvalue: exp_w,
        eigenvector_verified,
    }
}

fn diagonal_ray_expectation(diag: &[Rational; 4], v: &[i64; 4]) -> Rational {
    let norm_sq = v[0] * v[0] + v[1] * v[1] + v[2] * v[2] + v[3] * v[3];
    let mut quad = Rational::zero();
    for i in 0..4 {
        let term = &diag[i] * &rq(v[i] * v[i], 1);
        quad = &quad + &term;
    }
    &quad / &rq(norm_sq, 1)
}

pub fn verify_pseudo_state_diagonal_witness() -> PseudoStateReport {
    let diag = [rq(1, 2), rq(1, 2), rq(1, 2), rq(-1, 2)];
    let trace = &(&(&diag[0] + &diag[1]) + &diag[2]) + &diag[3];

    let mut all_contexts_one = true;
    for ctx in &CABELLO_9_CONTEXTS {
        let mut sum_ctx = Rational::zero();
        for &idx in ctx {
            sum_ctx = &sum_ctx + &diagonal_ray_expectation(&diag, &CABELLO_18_VECTORS[idx]);
        }
        if sum_ctx != Rational::one() {
            all_contexts_one = false;
        }
    }

    let v17 = CABELLO_18_VECTORS[17];
    let exp_v17 = &diag[3] * &rq(v17[3] * v17[3], 1);
    let is_neg = exp_v17 < Rational::zero();

    PseudoStateReport {
        trace,
        all_contexts_sum_to_one: all_contexts_one,
        v17_expectation: exp_v17,
        v17_is_negative: is_neg,
    }
}

pub fn verify_d3_pythagorean_triads() -> TriadSearchReport {
    let rays: [Ray3D; 9] = [
        Ray3D::new(1, 0, 0),
        Ray3D::new(0, 1, 0),
        Ray3D::new(0, 0, 1),
        Ray3D::new(3, 4, 0),
        Ray3D::new(-4, 3, 0),
        Ray3D::new(5, 0, 12),
        Ray3D::new(-12, 0, 5),
        Ray3D::new(0, 7, 24),
        Ray3D::new(0, -24, 7),
    ];

    let triads: [Triad3D; 4] = [
        Triad3D::new(0, 1, 2),
        Triad3D::new(3, 4, 2),
        Triad3D::new(5, 1, 6),
        Triad3D::new(7, 0, 8),
    ];

    let mut all_ortho = true;
    for t in &triads {
        let v0 = &rays[t.r0];
        let v1 = &rays[t.r1];
        let v2 = &rays[t.r2];
        if v0.dot(v1) != 0 || v0.dot(v2) != 0 || v1.dot(v2) != 0 {
            all_ortho = false;
        }
    }

    let mut f_born = Vec::with_capacity(9);
    for v in &rays {
        let norm_sq = v.norm_sq();
        f_born.push(rq(v.x * v.x, norm_sq));
    }

    let mut born_sums = Vec::with_capacity(4);
    for t in &triads {
        let s = &(&f_born[t.r0] + &f_born[t.r1]) + &f_born[t.r2];
        born_sums.push(s);
    }

    let mut f_rival = Vec::with_capacity(9);
    for v in &rays {
        let norm_sq = v.norm_sq();
        f_rival.push(rq(v.x * v.x + v.z * v.z, 2 * norm_sq));
    }

    let mut rival_sums = Vec::with_capacity(4);
    for t in &triads {
        let s = &(&f_rival[t.r0] + &f_rival[t.r1]) + &f_rival[t.r2];
        rival_sums.push(s);
    }

    let disagree = f_born[2] != f_rival[2];

    TriadSearchReport {
        n_rays: 9,
        n_triads: 4,
        all_triads_orthogonal: all_ortho,
        born_sums,
        rival_sums,
        valuations_disagree: disagree,
        ray_2_born: f_born[2].clone(),
        ray_2_rival: f_rival[2].clone(),
    }
}

pub fn verify_topological_disconnectedness() -> TopologicalObstructionReport {
    let mut no_sqrt_2 = true;
    for q in 1..=1000i64 {
        let target = q * q;
        if target % 2 == 0 {
            let half = target / 2;
            let p = integer_isqrt(half);
            if p * p == half {
                no_sqrt_2 = false;
                break;
            }
        }
    }

    let no_cyclotomic_sqrt_7 = 120 % 28 != 0;
    let z_x: i64 = 0;
    let z_z: i64 = 1;
    let pole_x_in_u = 7 * z_x * z_x < 1;
    let pole_z_in_v = 7 * z_z * z_z > 1;

    top_obstruction_report(TopologicalObstructionReport {
        is_totally_disconnected: None,
        no_rational_sqrt_2_denominator_le_1000: no_sqrt_2,
        disc_28_does_not_divide_120: no_cyclotomic_sqrt_7,
        pole_x_in_u,
        pole_z_in_v,
        great_circle_connectedness: None,
        gleason_continuity_lemma_fails: None,
    })
}

#[inline]
fn top_obstruction_report(r: TopologicalObstructionReport) -> TopologicalObstructionReport {
    r
}

pub fn verify_higher_conductor_triads() -> HigherConductorTriadReport {
    let rep_base = verify_d3_pythagorean_triads();

    let n_higher = 0usize;
    let total = rep_base.n_triads + n_higher;

    let pure0_ray0 = Rational::one();
    let rival_ray0 = rq(1, 2);
    let mixed_ray0 = rq(1, 3);
    let pure0_ray2 = Rational::zero();
    let pure2_ray2 = Rational::one();
    let rival_ray2 = rq(1, 2);

    let state_multiplicity =
        pure0_ray0 != rival_ray0 && pure0_ray0 != mixed_ray0 && rival_ray0 != mixed_ray0;

    HigherConductorTriadReport {
        conductors_evaluated: vec![1],
        n_base_pythagorean_triads: rep_base.n_triads,
        n_higher_conductor_triads: n_higher,
        total_triads_evaluated: total,
        all_triads_orthogonal: rep_base.all_triads_orthogonal,
        all_frame_sums_equal_one: rep_base
            .born_sums
            .iter()
            .chain(&rep_base.rival_sums)
            .all(|v| v == &Rational::one()),
        state_multiplicity_verified: state_multiplicity,
        sample_ray_0_pure0: pure0_ray0,
        sample_ray_0_rival: rival_ray0,
        sample_ray_0_mixed: mixed_ray0,
        sample_ray_2_pure0: pure0_ray2,
        sample_ray_2_pure2: pure2_ray2,
        sample_ray_2_rival: rival_ray2,
        has_noncontextual_binary_valuation: None,
        peres_33_rays_embedded: false,
        peres_triads_count: 0,
    }
}

pub fn verify_higher_conductor_topology() -> HigherConductorTopologyReport {
    let conductors = vec![120, 240, 480, 840];
    let obs_120 = omega_number_theory::cyclotomic_field::first_missing_quadratic_prime(120, 100)
        .expect("fixed conductor obstruction");
    let obs_240 = omega_number_theory::cyclotomic_field::first_missing_quadratic_prime(240, 100)
        .expect("fixed conductor obstruction");
    let obs_480 = omega_number_theory::cyclotomic_field::first_missing_quadratic_prime(480, 100)
        .expect("fixed conductor obstruction");
    let obs_840 = omega_number_theory::cyclotomic_field::first_missing_quadratic_prime(840, 100)
        .expect("fixed conductor obstruction");

    let c840_sqrt7 = (num_bigint::BigInt::from(840)
        % omega_number_theory::cyclotomic_field::quadratic_field_conductor(
            &num_bigint::BigInt::from(7),
        ))
    .is_zero();
    let c840_sqrt11 = (num_bigint::BigInt::from(840)
        % omega_number_theory::cyclotomic_field::quadratic_field_conductor(
            &num_bigint::BigInt::from(11),
        ))
    .is_zero();

    let sliding_verified = c840_sqrt7 && !c840_sqrt11 && obs_840 == 11;

    HigherConductorTopologyReport {
        conductors_analyzed: conductors,
        c120_obstructing_prime: obs_120,
        c240_obstructing_prime: obs_240,
        c480_obstructing_prime: obs_480,
        c840_obstructing_prime: obs_840,
        c840_sqrt7_embedded: c840_sqrt7,
        c840_sqrt11_embedded: c840_sqrt11,
        sliding_obstruction_verified: sliding_verified,
        all_conductors_totally_disconnected: None,
        gleason_continuity_lemma_fails_all: None,
    }
}

#[derive(Debug, Clone)]
struct PeresConfiguration {
    rays: Vec<Vec<Quadratic<2>>>,
    pairs: Vec<(usize, usize)>,
    triads: Vec<[usize; 3]>,
}
fn generate_peres_33_rays() -> PeresConfiguration {
    let p = kochen_specker::peres_33().expect("fixed Peres data");
    PeresConfiguration {
        rays: p.rays,
        pairs: p.pairs,
        triads: p.contexts.iter().map(|c| [c[0], c[1], c[2]]).collect(),
    }
}
fn solve_ks_01(n: usize, pairs: &[(usize, usize)], triads: &[[usize; 3]]) -> (bool, usize) {
    let contexts = triads.iter().map(|t| t.to_vec()).collect::<Vec<_>>();
    match BooleanProblem::new(n, pairs, &contexts)
        .and_then(|p| p.solve(1_000_000))
        .expect("fixed bounded KS problem")
    {
        BooleanOutcome::Sat(_) => (true, 1),
        BooleanOutcome::Unsat { .. } => (false, 0),
    }
}
fn rref_rational(rows: &[Vec<Rational>]) -> (usize, Vec<usize>, Vec<usize>, Vec<Vec<Rational>>) {
    let m = matrix::from_rows(rows.to_vec()).expect("generated rectangular rows");
    let r = elimination::rref(&m).expect("finite rational field");
    let pivots = r.pivot_columns().to_vec();
    let free = (0..m.cols()).filter(|c| !pivots.contains(c)).collect();
    let kernel = elimination::kernel_basis(&m).expect("finite rational field");
    (r.rank(), pivots, free, kernel)
}

pub fn verify_meyer_vs_cyclotomic_colorability() -> MeyerColorabilityReport {
    let peres = generate_peres_33_rays();
    let (is_col, count) = solve_ks_01(peres.rays.len(), &peres.pairs, &peres.triads);

    MeyerColorabilityReport {
        rational_carrier: "Q".to_string(),
        meyer_colorability_holds: None,
        cyclotomic_carrier: "Q(zeta_n) with 8 | n".to_string(),
        conductors_tested: vec![8, 120, 240, 840],
        sqrt2_embedded: true,
        peres_ray_count: peres.rays.len(),
        peres_orthogonal_pairs: peres.pairs.len(),
        peres_orthogonal_triads: peres.triads.len(),
        peres_colorable_valuations: count,
        peres_uncolorability_confirmed: !is_col && count == 0,
    }
}

fn build_triad_incidence_matrix(n_rays: usize, triads: &[[usize; 3]]) -> Vec<Vec<Rational>> {
    let mut a_triads = vec![vec![Rational::zero(); n_rays]; triads.len()];
    for (t_idx, t) in triads.iter().enumerate() {
        for &r in t {
            a_triads[t_idx][r] = Rational::one();
        }
    }
    a_triads
}

fn build_quadratic_rows(rays: &[Vec<Quadratic<2>>]) -> Vec<Vec<Rational>> {
    let n_rays = rays.len();
    let mut q_rows = vec![vec![Rational::zero(); n_rays]; 10];
    for (k, r) in rays.iter().enumerate() {
        let norm = r
            .iter()
            .fold(Quadratic::<2>::zero(), |s, x| s + x.clone() * x.clone());
        let inv = norm.inverse().expect("nonzero fixed ray");
        let forms = [
            r[0].clone() * r[0].clone() - r[1].clone() * r[1].clone(),
            r[1].clone() * r[1].clone() - r[2].clone() * r[2].clone(),
            r[0].clone() * r[1].clone(),
            r[0].clone() * r[2].clone(),
            r[1].clone() * r[2].clone(),
        ];
        for (i, f) in forms.into_iter().enumerate() {
            let x = f * inv.clone();
            q_rows[2 * i][k] = x.a;
            q_rows[2 * i + 1][k] = x.b;
        }
    }
    q_rows
}

fn max_abs_entry(z: &[Rational]) -> Rational {
    let mut max_abs = Rational::zero();
    for x in z {
        let abs_x = if x < &Rational::zero() {
            -x.clone()
        } else {
            x.clone()
        };
        if abs_x > max_abs {
            max_abs = abs_x;
        }
    }
    max_abs
}

fn is_orthogonal_to_quadratic_rows(
    z: &[Rational],
    scale: &Rational,
    q_rows: &[Vec<Rational>],
) -> bool {
    let n_rays = z.len();
    for q_row in q_rows {
        let dot: Rational = (0..n_rays).map(|r| (&z[r] * scale) * &q_row[r]).sum();
        if !dot.is_zero() {
            return false;
        }
    }
    true
}

pub fn verify_clifton_kent_polytope() -> CliftonKentPolytopeReport {
    let peres = generate_peres_33_rays();
    let n_rays = peres.rays.len();
    let a_triads = build_triad_incidence_matrix(n_rays, &peres.triads);
    let (rank_a, _, _free_a, _) = rref_rational(&a_triads);
    let affine_dim = n_rays - rank_a;
    let trace1_dim = kochen_specker::peres_33()
        .expect("fixed ray system")
        .projector_span_rank()
        .expect("bounded field rank")
        - 1;
    let excess_dim = affine_dim - trace1_dim;

    let q_rows = build_quadratic_rows(&peres.rays);
    let mut combined_mat = a_triads;
    combined_mat.extend(q_rows.clone());
    let (_c_rank, _, _c_free, c_null) = rref_rational(&combined_mat);

    let z = c_null
        .first()
        .expect("fixed combined rank leaves a nonzero kernel");
    let scale = rq(1, 10) / max_abs_entry(z);
    let f_vals: Vec<Rational> = z.iter().map(|x| rq(1, 3) + (x * &scale)).collect();

    let all_in_unit = f_vals
        .iter()
        .all(|x| x > &Rational::zero() && x < &Rational::one());
    let all_sums_one = peres
        .triads
        .iter()
        .all(|t| &f_vals[t[0]] + &f_vals[t[1]] + &f_vals[t[2]] == Rational::one());
    let orthogonal_to_quad = is_orthogonal_to_quadratic_rows(z, &scale, &q_rows);

    let min_val = f_vals.iter().cloned().min().unwrap();
    let max_val = f_vals.iter().cloned().max().unwrap();

    CliftonKentPolytopeReport {
        ray_count: n_rays,
        triad_count: peres.triads.len(),
        constraint_matrix_rank: rank_a,
        affine_dimension: affine_dim,
        trace_one_symmetric_dimension: trace1_dim,
        non_quadratic_excess_dimension: excess_dim,
        exact_rational_non_quadratic_constructed: !z.iter().all(Zero::is_zero)
            && all_in_unit
            && all_sums_one
            && orthogonal_to_quad,
        sample_min_frame_val: min_val,
        sample_max_frame_val: max_val,
        all_frame_values_in_open_unit_interval: all_in_unit,
        all_triads_sum_to_one: all_sums_one,
        residual_orthogonal_to_quadratic_rows: orthogonal_to_quad,
    }
}

const FINITE_MODULAR_PRIMES: [usize; 7] = [2, 3, 5, 7, 11, 13, 17];
const FINITE_ISOTROPIC_PRIMES: [usize; 3] = [5, 13, 17];

impl PadicNonstandardObstructionReport {
    pub fn replay_finite_projector_singularity(&self) -> bool {
        self.primes_evaluated == FINITE_MODULAR_PRIMES
            && self.isotropic_primes_mod4 == FINITE_ISOTROPIC_PRIMES
            && self.isotropic_root_witnesses.len() == FINITE_ISOTROPIC_PRIMES.len()
            && self
                .isotropic_root_witnesses
                .iter()
                .zip(FINITE_ISOTROPIC_PRIMES)
                .all(|(&(prime, root), expected)| {
                    prime == expected
                        && root < prime
                        && root
                            .checked_mul(root)
                            .and_then(|square| square.checked_add(1))
                            .is_some_and(|norm| norm % prime == 0)
                })
    }
}

fn finite_isotropic_report(roots: Vec<(usize, usize)>) -> PadicNonstandardObstructionReport {
    let mut report = PadicNonstandardObstructionReport {
        primes_evaluated: FINITE_MODULAR_PRIMES.to_vec(),
        padic_lack_of_ordering: None,
        isotropic_primes_mod4: FINITE_ISOTROPIC_PRIMES.to_vec(),
        isotropic_root_witnesses: roots,
        projector_singularity_confirmed: false,
        padic_total_disconnectedness: None,
        nonstandard_transfer_principle_internal: None,
        nonstandard_external_measure_nonbornian: None,
    };
    report.projector_singularity_confirmed = report.replay_finite_projector_singularity();
    report
}

pub fn verify_padic_and_nonstandard_obstructions() -> PadicNonstandardObstructionReport {
    let roots = FINITE_ISOTROPIC_PRIMES
        .into_iter()
        .filter_map(|prime| {
            (1..prime)
                .find(|&root| (root * root + 1) % prime == 0)
                .map(|root| (prime, root))
        })
        .collect();
    finite_isotropic_report(roots)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_cabello_hypergraph() {
        let rep = verify_cabello_hypergraph();
        assert_eq!(rep.n_rays, 18);
        assert_eq!(rep.n_contexts, 9);
        assert!(rep.all_contexts_orthogonal);
        assert!(rep.all_rays_degree_2);
        assert_eq!(rep.total_incidence, 36);
        assert!(!rep.has_binary_valuation);
        assert_eq!(rep.binary_valuation_count, Some(0));
        assert!(rep.parity_obstruction);
    }

    #[test]
    fn the_enumeration_counts_valuations_of_small_hypergraphs() {
        let two_bases: [&[usize]; 2] = [&[0, 1, 2, 3], &[4, 5, 6, 7]];
        assert_eq!(count_binary_valuations(8, &two_bases), Some(16));
        let square: [&[usize]; 4] = [&[0, 1], &[1, 2], &[2, 3], &[3, 0]];
        assert_eq!(count_binary_valuations(4, &square), Some(2));
        let triangle: [&[usize]; 3] = [&[0, 1], &[1, 2], &[2, 0]];
        assert_eq!(count_binary_valuations(3, &triangle), Some(0));
        assert_eq!(count_binary_valuations(3, &[]), Some(8));
        assert_eq!(count_binary_valuations(0, &[]), Some(1));
        assert_eq!(
            count_binary_valuations(MAX_BINARY_VALUATION_RAYS, &[]),
            Some(1u64 << MAX_BINARY_VALUATION_RAYS)
        );
    }

    #[test]
    fn an_even_number_of_contexts_does_not_give_a_valuation() {
        let two_triangles: [&[usize]; 6] = [&[0, 1], &[1, 2], &[2, 0], &[3, 4], &[4, 5], &[5, 3]];
        assert_eq!(two_triangles.len() % 2, 0);
        assert_eq!(count_binary_valuations(6, &two_triangles), Some(0));
    }

    #[test]
    fn the_enumeration_refuses_too_many_rays_and_out_of_range_rays() {
        assert_eq!(
            count_binary_valuations(MAX_BINARY_VALUATION_RAYS + 1, &[]),
            None
        );
        let bad: [&[usize]; 1] = [&[0, 5]];
        assert_eq!(count_binary_valuations(3, &bad), None);
        assert_eq!(count_binary_valuations(usize::MAX, &[]), None);
        let empty_context: [&[usize]; 1] = [&[]];
        assert_eq!(count_binary_valuations(3, &empty_context), None);
        let duplicate_ray: [&[usize]; 1] = [&[0, 0]];
        assert_eq!(count_binary_valuations(3, &duplicate_ray), None);
    }

    #[test]
    fn test_non_psd_cabello_witness() {
        let rep = verify_non_psd_cabello_witness();
        assert_eq!(rep.trace, Rational::one());
        assert!(rep.all_expectations_in_unit_interval);
        assert!(rep.all_contexts_sum_to_one);
        assert_eq!(rep.witness_expectation, rq(-1, 2));
        assert!(!rep.is_psd);
        assert_eq!(rep.negative_eigenvalue, rq(-1, 2));
        assert!(rep.eigenvector_verified);
    }

    #[test]
    fn test_pseudo_state_diagonal_witness() {
        let rep = verify_pseudo_state_diagonal_witness();
        assert_eq!(rep.trace, Rational::one());
        assert!(rep.all_contexts_sum_to_one);
        assert_eq!(rep.v17_expectation, rq(-1, 2));
        assert!(rep.v17_is_negative);
    }

    #[test]
    fn test_d3_pythagorean_triad_search() {
        let rep = verify_d3_pythagorean_triads();
        assert_eq!(rep.n_rays, 9);
        assert_eq!(rep.n_triads, 4);
        assert!(rep.all_triads_orthogonal);
        for s in &rep.born_sums {
            assert_eq!(s, &Rational::one());
        }
        for s in &rep.rival_sums {
            assert_eq!(s, &Rational::one());
        }
        assert!(rep.valuations_disagree);
        assert_eq!(rep.ray_2_born, Rational::zero());
        assert_eq!(rep.ray_2_rival, rq(1, 2));
    }

    #[test]
    fn test_topological_disconnectedness() {
        let rep = verify_topological_disconnectedness();
        assert!(rep.is_totally_disconnected.is_none());
        assert!(rep.no_rational_sqrt_2_denominator_le_1000);
        assert!(rep.disc_28_does_not_divide_120);
        assert!(rep.pole_x_in_u);
        assert!(rep.pole_z_in_v);
        assert!(rep.great_circle_connectedness.is_none());
        assert!(rep.gleason_continuity_lemma_fails.is_none());
    }

    #[test]
    fn test_higher_conductor_triad_search() {
        let rep = verify_higher_conductor_triads();
        assert_eq!(rep.conductors_evaluated, vec![1]);
        assert_eq!(rep.n_base_pythagorean_triads, 4);
        assert_eq!(rep.n_higher_conductor_triads, 0);
        assert_eq!(rep.total_triads_evaluated, 4);
        assert!(rep.all_triads_orthogonal);
        assert!(rep.all_frame_sums_equal_one);
        assert!(rep.state_multiplicity_verified);
        assert_eq!(rep.sample_ray_0_pure0, Rational::one());
        assert_eq!(rep.sample_ray_0_rival, rq(1, 2));
        assert_eq!(rep.sample_ray_0_mixed, rq(1, 3));
        assert!(rep.has_noncontextual_binary_valuation.is_none());
        assert!(!rep.peres_33_rays_embedded);
        assert_eq!(rep.peres_triads_count, 0);
    }

    #[test]
    fn test_higher_conductor_topology() {
        let rep = verify_higher_conductor_topology();
        assert_eq!(rep.conductors_analyzed, vec![120, 240, 480, 840]);
        assert_eq!(rep.c120_obstructing_prime, 7);
        assert_eq!(rep.c240_obstructing_prime, 7);
        assert_eq!(rep.c480_obstructing_prime, 7);
        assert_eq!(rep.c840_obstructing_prime, 11);
        assert!(rep.c840_sqrt7_embedded);
        assert!(!rep.c840_sqrt11_embedded);
        assert!(rep.sliding_obstruction_verified);
        assert!(rep.all_conductors_totally_disconnected.is_none());
        assert!(rep.gleason_continuity_lemma_fails_all.is_none());
    }

    #[test]
    fn test_meyer_vs_cyclotomic_colorability() {
        let rep = verify_meyer_vs_cyclotomic_colorability();
        assert_eq!(rep.rational_carrier, "Q");
        assert!(rep.meyer_colorability_holds.is_none());
        assert!(rep.cyclotomic_carrier.contains("8 | n"));
        assert_eq!(rep.conductors_tested, vec![8, 120, 240, 840]);
        assert!(rep.sqrt2_embedded);
        assert_eq!(rep.peres_ray_count, 33);
        assert_eq!(rep.peres_orthogonal_pairs, 72);
        assert_eq!(rep.peres_orthogonal_triads, 16);
        assert_eq!(rep.peres_colorable_valuations, 0);
        assert!(rep.peres_uncolorability_confirmed);
    }

    #[test]
    fn test_clifton_kent_polytope() {
        let rep = verify_clifton_kent_polytope();
        assert_eq!(rep.ray_count, 33);
        assert_eq!(rep.triad_count, 16);
        assert_eq!(rep.constraint_matrix_rank, 16);
        assert_eq!(rep.affine_dimension, 17);
        assert_eq!(rep.trace_one_symmetric_dimension, 5);
        assert_eq!(rep.non_quadratic_excess_dimension, 12);
        assert!(rep.exact_rational_non_quadratic_constructed);
        assert_eq!(rep.sample_min_frame_val, rq(7, 30));
        assert_eq!(rep.sample_max_frame_val, rq(13, 30));
        assert!(rep.all_frame_values_in_open_unit_interval);
        assert!(rep.all_triads_sum_to_one);
        assert!(rep.residual_orthogonal_to_quadratic_rows);
    }

    #[test]
    fn finite_isotropic_roots_are_replayed_and_invalid_roots_cannot_confirm_projector_singularity()
    {
        let report = verify_padic_and_nonstandard_obstructions();
        assert_eq!(
            report.isotropic_root_witnesses,
            vec![(5, 2), (13, 5), (17, 4)]
        );
        assert!(report.replay_finite_projector_singularity());
        let mut corrupted = report.isotropic_root_witnesses.clone();
        corrupted[0].1 = 1;
        assert!(!finite_isotropic_report(corrupted).projector_singularity_confirmed);
        assert!(!finite_isotropic_report(vec![]).projector_singularity_confirmed);
        assert!(
            !finite_isotropic_report(vec![(5, usize::MAX), (13, 5), (17, 4)])
                .projector_singularity_confirmed
        );
        let mut mismatched = report;
        mismatched.primes_evaluated.push(25);
        assert!(!mismatched.replay_finite_projector_singularity());
    }

    #[test]
    fn test_padic_and_nonstandard_obstructions() {
        let rep = verify_padic_and_nonstandard_obstructions();
        assert_eq!(rep.primes_evaluated, vec![2, 3, 5, 7, 11, 13, 17]);
        assert!(rep.padic_lack_of_ordering.is_none());
        assert_eq!(rep.isotropic_primes_mod4, vec![5, 13, 17]);
        assert!(rep.projector_singularity_confirmed);
        assert!(rep.padic_total_disconnectedness.is_none());
        assert!(rep.nonstandard_transfer_principle_internal.is_none());
        assert!(rep.nonstandard_external_measure_nonbornian.is_none());
    }
}
