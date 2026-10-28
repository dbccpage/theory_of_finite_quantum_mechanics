
use nalgebra::{DMatrix, SymmetricEigen};
use num_rational::BigRational;
use num_traits::ToPrimitive;
use serde::Serialize;

use crate::native::exact::d6_exact_sos_real::{
    real_moment_fibers, real_norm4_gram, real_obstruction_gram,
};
use crate::native::float_check::d6_gtfoc_wall_cross_validation::certified_wall_w;
use crate::native::exact::mub6_cyclotomic_enclosure::real_imag_decompose;
use engine_number_theory::cyclotomic::Cyc24;

const DEFAULT_FEASIBILITY_TOL: f64 = 1.0e-7;
const DEFAULT_ITERATIONS: usize = 24;
const DEFAULT_EIGEN_FLOOR: f64 = 0.0;
const MATERIAL_NEGATIVE_EIGEN_TOL: f64 = 1.0e-10;
const DEFAULT_LOW_RANK_FACTOR_RANK: usize = 48;
const LOW_RANK_INITIAL_NOISE: f64 = 1.0e-4;
const LOW_RANK_ADAM_STEP: f64 = 2.0e-2;
const LOW_RANK_ADAM_BETA1: f64 = 0.9;
const LOW_RANK_ADAM_BETA2: f64 = 0.999;
const LOW_RANK_ADAM_EPS: f64 = 1.0e-8;
const FLOAT_DUAL_FEASIBILITY_TOL: f64 = 1.0e-8;
const FLOAT_DUAL_SEPARATION_TOL: f64 = 1.0e-10;

#[derive(Clone, Copy, Debug, PartialEq, Eq, PartialOrd, Ord, Serialize)]
pub enum FloatProjectionBackend {
    DouglasRachford,
    Dykstra,
    SpectralAscent,
    LowRankFactor,
}

impl FloatProjectionBackend {
    fn method(self) -> &'static str {
        match self {
            FloatProjectionBackend::DouglasRachford => {
                "Untrusted f64 Douglas-Rachford projection between the Stage A affine moment constraints and the PSD cone"
            }
            FloatProjectionBackend::Dykstra => {
                "Untrusted f64 Dykstra alternating projection between the Stage A affine moment constraints and the PSD cone"
            }
            FloatProjectionBackend::SpectralAscent => {
                "Untrusted f64 projected spectral ascent on the Stage A affine moment-kernel tangent"
            }
            FloatProjectionBackend::LowRankFactor => {
                "Untrusted f64 low-rank factor search Q = R R^T against the Stage A affine moment constraints"
            }
        }
    }
}

#[derive(Clone, Debug, PartialEq)]
pub struct FloatSdpConfig {
    pub margin: f64,
    pub iterations: usize,
    pub feasibility_tol: f64,
    pub eigen_floor: f64,
    pub backend: FloatProjectionBackend,
}

impl FloatSdpConfig {
    pub fn for_margin(margin: f64) -> Self {
        Self {
            margin,
            iterations: DEFAULT_ITERATIONS,
            feasibility_tol: DEFAULT_FEASIBILITY_TOL,
            eigen_floor: DEFAULT_EIGEN_FLOOR,
            backend: FloatProjectionBackend::DouglasRachford,
        }
    }
}

#[derive(Clone, Debug, PartialEq, Serialize)]
pub struct FloatSdpReport {
    pub target: &'static str,
    pub method: &'static str,
    pub backend: FloatProjectionBackend,
    pub margin: f64,
    pub invariant_systems_sanity_margin: f64,
    pub margin_gap_to_sanity: f64,
    pub iterations: usize,
    pub affine_residual_initial: f64,
    pub affine_l2_residual_initial: f64,
    pub affine_residual_final: f64,
    pub affine_l2_residual_final: f64,
    pub min_eigen_initial: f64,
    pub min_eigen_final: f64,
    pub max_eigen_final: f64,
    pub negative_eigenvalue_mass_final: f64,
    pub negative_eigenvalue_count_final: usize,
    pub relative_step_final: f64,
    pub spectral_tangent_pressure_norm_final: f64,
    pub dual_separation_value_final: f64,
    pub float_dual_separation_observed: bool,
    pub residual_dual_min_eigen_final: f64,
    pub residual_dual_objective_final: f64,
    pub float_residual_dual_observed: bool,
    pub feasible_by_float_tolerance: bool,
    pub has_exact_certificate: bool,
    pub has_full_mub6_authority: bool,
    pub boundary: &'static str,
}

#[derive(Clone, Debug, PartialEq)]
pub struct FloatSdpState {
    pub report: FloatSdpReport,
    pub gram: Vec<Vec<f64>>,
}

#[derive(Clone, Debug, PartialEq, Serialize)]
pub struct FloatMarginScan {
    pub reports: Vec<FloatSdpReport>,
    pub best_feasible_margin: Option<f64>,
    pub invariant_systems_sanity_margin: f64,
    pub boundary: &'static str,
}

#[derive(Clone, Debug)]
struct MomentEntry {
    row: usize,
    col: usize,
    weight: f64,
}

#[derive(Clone, Debug)]
struct MomentFiber {
    entries: Vec<MomentEntry>,
    denominator: f64,
}

#[derive(Clone, Debug)]
struct FloatMomentProblem {
    n: usize,
    base: Vec<Vec<f64>>,
    norm4: Vec<Vec<f64>>,
    fibers: Vec<MomentFiber>,
}

#[derive(Clone, Copy, Debug, PartialEq)]
struct SpectrumSummary {
    min: f64,
    max: f64,
    negative_mass: f64,
    negative_count: usize,
}

#[derive(Clone, Copy, Debug, PartialEq)]
struct SpectralDualDiagnostic {
    tangent_pressure_norm: f64,
    separation_value: f64,
    float_separation_observed: bool,
}

#[derive(Clone, Copy, Debug, PartialEq)]
struct ResidualDualDiagnostic {
    min_eigen: f64,
    objective: f64,
    float_separation_observed: bool,
}

pub fn invariant_systems_sanity_margin() -> f64 {
    (1.0 - certified_wall_w()) * (5.0 / 6.0)
}

pub fn run_float_sdp_probe(config: FloatSdpConfig) -> FloatSdpState {
    assert!(config.margin.is_finite(), "Stage B margin must be finite");
    assert!(
        config.feasibility_tol.is_finite() && config.feasibility_tol > 0.0,
        "Stage B feasibility tolerance must be positive and finite"
    );
    let problem = FloatMomentProblem::new();
    let target = problem.target_matrix(config.margin);
    let initial_spectrum = spectrum_summary(&target);
    let initial_affine = problem.max_affine_residual(&target, config.margin);
    let initial_affine_l2 = problem.affine_l2_residual(&target, config.margin);

    let (candidate, relative_step) = match config.backend {
        FloatProjectionBackend::DouglasRachford => run_douglas_rachford(
            &problem,
            target,
            config.margin,
            config.iterations,
            config.eigen_floor,
        ),
        FloatProjectionBackend::Dykstra => run_dykstra(
            &problem,
            target,
            config.margin,
            config.iterations,
            config.eigen_floor,
        ),
        FloatProjectionBackend::SpectralAscent => {
            run_spectral_ascent(&problem, target, config.margin, config.iterations)
        }
        FloatProjectionBackend::LowRankFactor => run_low_rank_factor(
            &problem,
            target,
            config.margin,
            config.iterations,
            config.feasibility_tol,
        ),
    };
    let final_affine = problem.max_affine_residual(&candidate, config.margin);
    let final_affine_l2 = problem.affine_l2_residual(&candidate, config.margin);
    let final_spectrum = spectrum_summary(&candidate);
    let spectral_diagnostic = spectral_dual_diagnostic(&problem, &candidate);
    let residual_dual_diagnostic = residual_dual_diagnostic(&problem, &candidate, config.margin);
    let feasible_by_float_tolerance =
        final_affine <= config.feasibility_tol && final_spectrum.min >= -config.feasibility_tol;
    let sanity_margin = invariant_systems_sanity_margin();

    FloatSdpState {
        gram: candidate,
        report: FloatSdpReport {
            target: "d=6 canonical-triple T0 real SOS Gram feasibility",
            method: config.backend.method(),
            backend: config.backend,
            margin: config.margin,
            invariant_systems_sanity_margin: sanity_margin,
            margin_gap_to_sanity: sanity_margin - config.margin,
            iterations: config.iterations,
            affine_residual_initial: initial_affine,
            affine_l2_residual_initial: initial_affine_l2,
            affine_residual_final: final_affine,
            affine_l2_residual_final: final_affine_l2,
            min_eigen_initial: initial_spectrum.min,
            min_eigen_final: final_spectrum.min,
            max_eigen_final: final_spectrum.max,
            negative_eigenvalue_mass_final: final_spectrum.negative_mass,
            negative_eigenvalue_count_final: final_spectrum.negative_count,
            relative_step_final: relative_step,
            spectral_tangent_pressure_norm_final: spectral_diagnostic.tangent_pressure_norm,
            dual_separation_value_final: spectral_diagnostic.separation_value,
            float_dual_separation_observed: spectral_diagnostic.float_separation_observed,
            residual_dual_min_eigen_final: residual_dual_diagnostic.min_eigen,
            residual_dual_objective_final: residual_dual_diagnostic.objective,
            float_residual_dual_observed: residual_dual_diagnostic.float_separation_observed,
            feasible_by_float_tolerance,
            has_exact_certificate: false,
            has_full_mub6_authority: false,
            boundary: "Stage B diagnostic only: f64 projection output is not a certificate. Stage C must round/project over Q(zeta_24), prove the exact identity, check c > 0, and pass is_psd_cyc24 before any wall authority exists.",
        },
    }
}

pub fn run_float_margin_scan(margins: &[f64], mut config: FloatSdpConfig) -> FloatMarginScan {
    let mut reports = Vec::with_capacity(margins.len());
    let mut best_feasible_margin = None;
    for &margin in margins {
        config.margin = margin;
        let state = run_float_sdp_probe(config.clone());
        if state.report.feasible_by_float_tolerance {
            best_feasible_margin =
                Some(best_feasible_margin.map_or(margin, |best: f64| best.max(margin)));
        }
        reports.push(state.report);
    }
    FloatMarginScan {
        reports,
        best_feasible_margin,
        invariant_systems_sanity_margin: invariant_systems_sanity_margin(),
        boundary:
            "Float scan only: useful for Stage C candidate selection, never for theorem authority.",
    }
}

pub fn run_default_float_margin_scan() -> FloatMarginScan {
    let sanity = invariant_systems_sanity_margin();
    let margins = [
        0.0,
        1.0e-4,
        5.0e-4,
        1.0e-3,
        5.0e-3,
        0.5 * sanity,
        0.9 * sanity,
    ];
    run_float_margin_scan(
        &margins,
        FloatSdpConfig {
            margin: 0.0,
            iterations: 96,
            feasibility_tol: DEFAULT_FEASIBILITY_TOL,
            eigen_floor: DEFAULT_EIGEN_FLOOR,
            backend: FloatProjectionBackend::DouglasRachford,
        },
    )
}

pub fn run_default_dykstra_float_margin_scan() -> FloatMarginScan {
    let sanity = invariant_systems_sanity_margin();
    let margins = [
        0.0,
        1.0e-4,
        5.0e-4,
        1.0e-3,
        5.0e-3,
        0.5 * sanity,
        0.9 * sanity,
    ];
    run_float_margin_scan(
        &margins,
        FloatSdpConfig {
            margin: 0.0,
            iterations: 96,
            feasibility_tol: DEFAULT_FEASIBILITY_TOL,
            eigen_floor: DEFAULT_EIGEN_FLOOR,
            backend: FloatProjectionBackend::Dykstra,
        },
    )
}

pub fn run_default_spectral_float_margin_scan() -> FloatMarginScan {
    let sanity = invariant_systems_sanity_margin();
    let margins = [
        0.0,
        1.0e-4,
        5.0e-4,
        1.0e-3,
        5.0e-3,
        0.5 * sanity,
        0.9 * sanity,
    ];
    run_float_margin_scan(
        &margins,
        FloatSdpConfig {
            margin: 0.0,
            iterations: 64,
            feasibility_tol: DEFAULT_FEASIBILITY_TOL,
            eigen_floor: DEFAULT_EIGEN_FLOOR,
            backend: FloatProjectionBackend::SpectralAscent,
        },
    )
}

pub fn run_default_low_rank_float_margin_scan() -> FloatMarginScan {
    let sanity = invariant_systems_sanity_margin();
    let margins = [
        0.0,
        1.0e-4,
        5.0e-4,
        1.0e-3,
        5.0e-3,
        0.5 * sanity,
        0.9 * sanity,
    ];
    run_float_margin_scan(
        &margins,
        FloatSdpConfig {
            margin: 0.0,
            iterations: 128,
            feasibility_tol: DEFAULT_FEASIBILITY_TOL,
            eigen_floor: DEFAULT_EIGEN_FLOOR,
            backend: FloatProjectionBackend::LowRankFactor,
        },
    )
}

pub fn cyc24_real_to_f64(z: &Cyc24) -> f64 {
    let (re, im) = real_imag_decompose(z);
    let im_value = subfield_coefficients_to_f64(&im);
    debug_assert!(
        im_value.abs() <= 1.0e-8,
        "expected a real Cyc24 entry, got imaginary part {im_value}"
    );
    subfield_coefficients_to_f64(&re)
}

impl FloatMomentProblem {
    fn new() -> Self {
        let base = matrix_cyc24_to_f64(&real_obstruction_gram());
        let norm4 = matrix_cyc24_to_f64(&real_norm4_gram());
        let n = base.len();
        let fibers = real_moment_fibers()
            .into_values()
            .map(|pairs| {
                let entries: Vec<MomentEntry> = pairs
                    .into_iter()
                    .map(|(row, col)| MomentEntry {
                        row,
                        col,
                        weight: symmetric_entry_weight(row, col),
                    })
                    .collect();
                let denominator = entries.iter().map(|entry| entry.weight).sum();
                MomentFiber {
                    entries,
                    denominator,
                }
            })
            .collect();
        Self {
            n,
            base,
            norm4,
            fibers,
        }
    }

    fn target_matrix(&self, margin: f64) -> Vec<Vec<f64>> {
        let mut out = vec![vec![0.0; self.n]; self.n];
        for r in 0..self.n {
            for c in 0..self.n {
                out[r][c] = self.base[r][c] - margin * self.norm4[r][c];
            }
        }
        out
    }

    fn target_fiber_sum(&self, fiber: &MomentFiber, margin: f64) -> f64 {
        fiber
            .entries
            .iter()
            .map(|entry| {
                entry.weight
                    * (self.base[entry.row][entry.col] - margin * self.norm4[entry.row][entry.col])
            })
            .sum()
    }

    fn fiber_sum(&self, matrix: &[Vec<f64>], fiber: &MomentFiber) -> f64 {
        fiber
            .entries
            .iter()
            .map(|entry| entry.weight * matrix[entry.row][entry.col])
            .sum()
    }

    fn project_affine(&self, matrix: &mut [Vec<f64>], margin: f64) {
        for fiber in &self.fibers {
            let residual = self.fiber_sum(matrix, fiber) - self.target_fiber_sum(fiber, margin);
            let correction = residual / fiber.denominator;
            for entry in &fiber.entries {
                matrix[entry.row][entry.col] -= correction;
                matrix[entry.col][entry.row] = matrix[entry.row][entry.col];
            }
        }
    }

    fn project_tangent(&self, matrix: &mut [Vec<f64>]) {
        for fiber in &self.fibers {
            let residual = self.fiber_sum(matrix, fiber);
            let correction = residual / fiber.denominator;
            for entry in &fiber.entries {
                matrix[entry.row][entry.col] -= correction;
                matrix[entry.col][entry.row] = matrix[entry.row][entry.col];
            }
        }
    }

    fn max_affine_residual(&self, matrix: &[Vec<f64>], margin: f64) -> f64 {
        self.fibers
            .iter()
            .map(|fiber| {
                (self.fiber_sum(matrix, fiber) - self.target_fiber_sum(fiber, margin)).abs()
            })
            .fold(0.0, f64::max)
    }

    fn affine_l2_residual(&self, matrix: &[Vec<f64>], margin: f64) -> f64 {
        self.fibers
            .iter()
            .map(|fiber| {
                let residual = self.fiber_sum(matrix, fiber) - self.target_fiber_sum(fiber, margin);
                residual * residual
            })
            .sum::<f64>()
            .sqrt()
    }

    fn affine_residuals(&self, matrix: &[Vec<f64>], margin: f64) -> Vec<f64> {
        self.fibers
            .iter()
            .map(|fiber| self.fiber_sum(matrix, fiber) - self.target_fiber_sum(fiber, margin))
            .collect()
    }

    fn dual_matrix_from_coefficients(&self, coefficients: &[f64]) -> Vec<Vec<f64>> {
        assert_eq!(
            coefficients.len(),
            self.fibers.len(),
            "one dual coefficient per affine moment fiber"
        );
        let mut matrix = zero_matrix(self.n);
        for (coefficient, fiber) in coefficients.iter().zip(self.fibers.iter()) {
            for entry in &fiber.entries {
                matrix[entry.row][entry.col] += coefficient;
                if entry.row != entry.col {
                    matrix[entry.col][entry.row] += coefficient;
                }
            }
        }
        matrix
    }

    fn target_dual_objective(&self, coefficients: &[f64], margin: f64) -> f64 {
        coefficients
            .iter()
            .zip(self.fibers.iter())
            .map(|(coefficient, fiber)| coefficient * self.target_fiber_sum(fiber, margin))
            .sum()
    }
}

fn run_douglas_rachford(
    problem: &FloatMomentProblem,
    target: Vec<Vec<f64>>,
    margin: f64,
    iterations: usize,
    eigen_floor: f64,
) -> (Vec<Vec<f64>>, f64) {
    let mut x = target;
    let mut relative_step = 0.0;
    for _ in 0..iterations {
        let (psd, _) = project_psd(&x, eigen_floor);
        let mut reflected = matrix_linear_combination(2.0, &psd, -1.0, &x);
        problem.project_affine(&mut reflected, margin);
        let next = matrix_linear_combination(
            1.0,
            &x,
            1.0,
            &matrix_linear_combination(1.0, &reflected, -1.0, &psd),
        );
        relative_step = relative_frobenius_step(&next, &x);
        x = next;
    }

    let (mut candidate, _) = project_psd(&x, eigen_floor);
    problem.project_affine(&mut candidate, margin);
    (candidate, relative_step)
}

fn run_dykstra(
    problem: &FloatMomentProblem,
    target: Vec<Vec<f64>>,
    margin: f64,
    iterations: usize,
    eigen_floor: f64,
) -> (Vec<Vec<f64>>, f64) {
    let n = target.len();
    let mut x = target;
    let mut psd_residual = zero_matrix(n);
    let mut affine_residual = zero_matrix(n);
    let mut relative_step = 0.0;

    for _ in 0..iterations {
        let psd_input = matrix_linear_combination(1.0, &x, 1.0, &psd_residual);
        let (psd, _) = project_psd(&psd_input, eigen_floor);
        psd_residual = matrix_linear_combination(1.0, &psd_input, -1.0, &psd);

        let affine_input = matrix_linear_combination(1.0, &psd, 1.0, &affine_residual);
        let mut next = affine_input.clone();
        problem.project_affine(&mut next, margin);
        affine_residual = matrix_linear_combination(1.0, &affine_input, -1.0, &next);

        relative_step = relative_frobenius_step(&next, &x);
        x = next;
    }

    (x, relative_step)
}

fn run_low_rank_factor(
    problem: &FloatMomentProblem,
    target: Vec<Vec<f64>>,
    margin: f64,
    iterations: usize,
    feasibility_tol: f64,
) -> (Vec<Vec<f64>>, f64) {
    let rank = DEFAULT_LOW_RANK_FACTOR_RANK.min(problem.n);
    let mut factors = psd_factor(&target, rank, margin.abs() > 0.0);
    let mut best_factors = factors.clone();
    let (_, mut best_l2, _) = low_rank_residual_gradient(problem, &factors, margin);
    let mut adam_m = zero_factor(problem.n, rank);
    let mut adam_v = zero_factor(problem.n, rank);
    let mut beta1_power = 1.0;
    let mut beta2_power = 1.0;
    let mut relative_step = 0.0;

    for iter in 1..=iterations {
        let (max_residual, l2_residual, gradient) =
            low_rank_residual_gradient(problem, &factors, margin);
        if l2_residual < best_l2 {
            best_l2 = l2_residual;
            best_factors = factors.clone();
        }
        if max_residual <= feasibility_tol {
            break;
        }

        beta1_power *= LOW_RANK_ADAM_BETA1;
        beta2_power *= LOW_RANK_ADAM_BETA2;
        let step = LOW_RANK_ADAM_STEP / (1.0 + (iter as f64 / 200.0)).sqrt();
        let previous = factors.clone();
        for row in 0..problem.n {
            for col in 0..rank {
                let g = gradient[row][col];
                adam_m[row][col] =
                    LOW_RANK_ADAM_BETA1 * adam_m[row][col] + (1.0 - LOW_RANK_ADAM_BETA1) * g;
                adam_v[row][col] =
                    LOW_RANK_ADAM_BETA2 * adam_v[row][col] + (1.0 - LOW_RANK_ADAM_BETA2) * g * g;
                let m_hat = adam_m[row][col] / (1.0 - beta1_power);
                let v_hat = adam_v[row][col] / (1.0 - beta2_power);
                factors[row][col] -= step * m_hat / (v_hat.sqrt() + LOW_RANK_ADAM_EPS);
            }
        }
        relative_step = relative_factor_step(&factors, &previous);
    }

    let (_, final_l2, _) = low_rank_residual_gradient(problem, &factors, margin);
    if final_l2 < best_l2 {
        best_factors = factors;
    }
    (factor_gram(&best_factors), relative_step)
}

fn psd_factor(matrix: &[Vec<f64>], rank: usize, add_noise_columns: bool) -> Vec<Vec<f64>> {
    let n = matrix.len();
    let sym = DMatrix::from_fn(n, n, |r, c| 0.5 * (matrix[r][c] + matrix[c][r]));
    let eig = SymmetricEigen::new(sym);
    let mut order: Vec<usize> = (0..n).collect();
    order.sort_by(|&a, &b| {
        eig.eigenvalues[b]
            .partial_cmp(&eig.eigenvalues[a])
            .unwrap_or(std::cmp::Ordering::Equal)
    });

    let mut factors = zero_factor(n, rank);
    let mut col = 0;
    for idx in order {
        if col >= rank {
            break;
        }
        let lambda = eig.eigenvalues[idx];
        if lambda <= 0.0 {
            continue;
        }
        let scale = lambda.sqrt();
        for row in 0..n {
            factors[row][col] = scale * eig.eigenvectors[(row, idx)];
        }
        col += 1;
    }

    if add_noise_columns {
        for noise_col in col..rank {
            for row in 0..n {
                let phase = ((row + 1) * (noise_col + 3)) as f64;
                factors[row][noise_col] =
                    LOW_RANK_INITIAL_NOISE * (phase.sin() + 0.5 * (0.37 * phase).cos());
            }
        }
    }
    factors
}

fn accumulate_fiber_entry_gradient(
    row: usize,
    col: usize,
    rank: usize,
    residual: f64,
    factors: &[Vec<f64>],
    gradient: &mut [Vec<f64>],
) {
    if row == col {
        for k in 0..rank {
            gradient[row][k] += 2.0 * residual * factors[row][k];
        }
    } else {
        for k in 0..rank {
            gradient[row][k] += 2.0 * residual * factors[col][k];
            gradient[col][k] += 2.0 * residual * factors[row][k];
        }
    }
}

fn low_rank_residual_gradient(
    problem: &FloatMomentProblem,
    factors: &[Vec<f64>],
    margin: f64,
) -> (f64, f64, Vec<Vec<f64>>) {
    let rank = factors.first().map_or(0, Vec::len);
    let mut gradient = zero_factor(problem.n, rank);
    let mut max_residual = 0.0_f64;
    let mut l2_sq = 0.0;

    for fiber in &problem.fibers {
        let mut fiber_value = 0.0;
        for entry in &fiber.entries {
            fiber_value += entry.weight * row_dot(&factors[entry.row], &factors[entry.col]);
        }
        let residual = fiber_value - problem.target_fiber_sum(fiber, margin);
        max_residual = max_residual.max(residual.abs());
        l2_sq += residual * residual;

        for entry in &fiber.entries {
            accumulate_fiber_entry_gradient(
                entry.row,
                entry.col,
                rank,
                residual,
                factors,
                &mut gradient,
            );
        }
    }

    (max_residual, l2_sq.sqrt(), gradient)
}

fn row_dot(left: &[f64], right: &[f64]) -> f64 {
    left.iter().zip(right.iter()).map(|(a, b)| a * b).sum()
}

fn factor_gram(factors: &[Vec<f64>]) -> Vec<Vec<f64>> {
    let n = factors.len();
    let mut out = vec![vec![0.0; n]; n];
    for r in 0..n {
        for c in 0..=r {
            out[r][c] = row_dot(&factors[r], &factors[c]);
        }
    }
    for r in 0..n {
        for c in 0..r {
            out[c][r] = out[r][c];
        }
    }
    out
}

fn zero_factor(n: usize, rank: usize) -> Vec<Vec<f64>> {
    vec![vec![0.0; rank]; n]
}

fn relative_factor_step(next: &[Vec<f64>], prev: &[Vec<f64>]) -> f64 {
    let mut diff_sq = 0.0;
    let mut prev_sq = 0.0;
    for row in 0..next.len() {
        for col in 0..next[row].len() {
            let diff = next[row][col] - prev[row][col];
            diff_sq += diff * diff;
            prev_sq += prev[row][col] * prev[row][col];
        }
    }
    diff_sq.sqrt() / prev_sq.sqrt().max(1.0)
}

fn try_spectral_step_sign(
    problem: &FloatMomentProblem,
    x: &mut Vec<Vec<f64>>,
    direction: &[Vec<f64>],
    current: SpectrumSummary,
    margin: f64,
    trial_step: f64,
) -> Option<f64> {
    for direction_sign in [1.0, -1.0] {
        let mut next = matrix_linear_combination(1.0, x, direction_sign * trial_step, direction);
        problem.project_affine(&mut next, margin);
        let next_summary = spectrum_summary(&next);
        if spectral_progress(next_summary, current) {
            let rel = relative_frobenius_step(&next, x);
            *x = next;
            return Some(rel);
        }
    }
    None
}

fn try_spectral_line_search(
    problem: &FloatMomentProblem,
    x: &mut Vec<Vec<f64>>,
    direction: &[Vec<f64>],
    current: SpectrumSummary,
    margin: f64,
    step: &mut f64,
) -> Option<f64> {
    let mut trial_step = *step;
    for _ in 0..24 {
        if let Some(rel) =
            try_spectral_step_sign(problem, x, direction, current, margin, trial_step)
        {
            *step = (trial_step * 1.15).min(2.0);
            return Some(rel);
        }
        trial_step *= 0.5;
    }
    None
}

fn run_spectral_ascent(
    problem: &FloatMomentProblem,
    target: Vec<Vec<f64>>,
    margin: f64,
    iterations: usize,
) -> (Vec<Vec<f64>>, f64) {
    let mut x = target;
    let mut step = 0.25;
    let mut relative_step = 0.0;

    for _ in 0..iterations {
        let (mut direction, current) = spectral_pressure_direction(&x);
        problem.project_tangent(&mut direction);
        let direction_norm = frobenius_norm(&direction);
        if direction_norm <= 1.0e-14 {
            break;
        }
        scale_matrix(&mut direction, 1.0 / direction_norm);

        match try_spectral_line_search(problem, &mut x, &direction, current, margin, &mut step) {
            Some(rel) => relative_step = rel,
            None => break,
        }
    }

    (x, relative_step)
}

fn spectral_progress(next: SpectrumSummary, current: SpectrumSummary) -> bool {
    if current.negative_mass > 1.0e-12 {
        next.negative_mass < current.negative_mass - 1.0e-12
    } else {
        next.min > current.min + 1.0e-12
    }
}

fn summarize_eigenvalues(eigenvalues: &[f64]) -> (SpectrumSummary, f64) {
    let mut summary = SpectrumSummary {
        min: f64::INFINITY,
        max: f64::NEG_INFINITY,
        negative_mass: 0.0,
        negative_count: 0,
    };
    let mut has_material_negative = false;
    for &lambda in eigenvalues {
        summary.min = summary.min.min(lambda);
        summary.max = summary.max.max(lambda);
        if lambda < 0.0 {
            summary.negative_mass += -lambda;
            summary.negative_count += 1;
        }
        if lambda < -MATERIAL_NEGATIVE_EIGEN_TOL {
            has_material_negative = true;
        }
    }
    let cutoff = if has_material_negative {
        -MATERIAL_NEGATIVE_EIGEN_TOL
    } else {
        summary.min + 1.0e-9
    };
    (summary, cutoff)
}

fn accumulate_eigenvector_outer_lower(
    out: &mut [Vec<f64>],
    eigenvectors: &DMatrix<f64>,
    k: usize,
) {
    let n = out.len();
    for r in 0..n {
        let vr = eigenvectors[(r, k)];
        for c in 0..=r {
            out[r][c] += vr * eigenvectors[(c, k)];
        }
    }
}

fn spectral_pressure_direction(matrix: &[Vec<f64>]) -> (Vec<Vec<f64>>, SpectrumSummary) {
    let n = matrix.len();
    let sym = DMatrix::from_fn(n, n, |r, c| 0.5 * (matrix[r][c] + matrix[c][r]));
    let eig = SymmetricEigen::new(sym);
    let (summary, cutoff) = summarize_eigenvalues(eig.eigenvalues.as_slice());

    let mut out = vec![vec![0.0; n]; n];
    for k in 0..n {
        if eig.eigenvalues[k] <= cutoff {
            accumulate_eigenvector_outer_lower(&mut out, &eig.eigenvectors, k);
        }
    }
    for r in 0..n {
        for c in 0..r {
            out[c][r] = out[r][c];
        }
    }
    (out, summary)
}

fn spectral_dual_diagnostic(
    problem: &FloatMomentProblem,
    matrix: &[Vec<f64>],
) -> SpectralDualDiagnostic {
    let (mut pressure, summary) = spectral_pressure_direction(matrix);
    let separation_value = trace_inner(&pressure, matrix);
    problem.project_tangent(&mut pressure);
    let tangent_pressure_norm = frobenius_norm(&pressure);
    SpectralDualDiagnostic {
        tangent_pressure_norm,
        separation_value,
        float_separation_observed: summary.negative_mass > 1.0e-10
            && tangent_pressure_norm <= 1.0e-8
            && separation_value < -1.0e-10,
    }
}

fn residual_dual_diagnostic(
    problem: &FloatMomentProblem,
    matrix: &[Vec<f64>],
    margin: f64,
) -> ResidualDualDiagnostic {
    let residuals = problem.affine_residuals(matrix, margin);
    let residual_l2 = residuals
        .iter()
        .map(|value| value * value)
        .sum::<f64>()
        .sqrt();
    if residual_l2 <= DEFAULT_FEASIBILITY_TOL {
        return ResidualDualDiagnostic {
            min_eigen: 0.0,
            objective: 0.0,
            float_separation_observed: false,
        };
    }

    let positive = normalized_residual_dual_summary(problem, &residuals, margin);
    let negative_residuals: Vec<f64> = residuals.iter().map(|value| -value).collect();
    let negative = normalized_residual_dual_summary(problem, &negative_residuals, margin);

    if negative.float_separation_observed
        || (!positive.float_separation_observed && negative.objective < positive.objective)
    {
        negative
    } else {
        positive
    }
}

fn normalized_residual_dual_summary(
    problem: &FloatMomentProblem,
    coefficients: &[f64],
    margin: f64,
) -> ResidualDualDiagnostic {
    let dual_matrix = problem.dual_matrix_from_coefficients(coefficients);
    let norm = frobenius_norm(&dual_matrix);
    if norm <= 1.0e-14 {
        return ResidualDualDiagnostic {
            min_eigen: 0.0,
            objective: 0.0,
            float_separation_observed: false,
        };
    }

    let scale = 1.0 / norm;
    let scaled_coefficients: Vec<f64> = coefficients.iter().map(|value| scale * value).collect();
    let scaled_matrix = scale_matrix_owned(&dual_matrix, scale);
    let summary = spectrum_summary(&scaled_matrix);
    let objective = problem.target_dual_objective(&scaled_coefficients, margin);
    ResidualDualDiagnostic {
        min_eigen: summary.min,
        objective,
        float_separation_observed: summary.min >= -FLOAT_DUAL_FEASIBILITY_TOL
            && objective < -FLOAT_DUAL_SEPARATION_TOL,
    }
}

fn symmetric_entry_weight(row: usize, col: usize) -> f64 {
    if row == col {
        1.0
    } else {
        2.0
    }
}

fn matrix_cyc24_to_f64(matrix: &[Vec<Cyc24>]) -> Vec<Vec<f64>> {
    matrix
        .iter()
        .map(|row| row.iter().map(cyc24_real_to_f64).collect())
        .collect()
}

fn subfield_coefficients_to_f64(coeffs: &[BigRational; 4]) -> f64 {
    let sqrt2 = 2.0_f64.sqrt();
    let sqrt3 = 3.0_f64.sqrt();
    let sqrt6 = 6.0_f64.sqrt();
    rational_to_f64(&coeffs[0])
        + rational_to_f64(&coeffs[1]) * sqrt2
        + rational_to_f64(&coeffs[2]) * sqrt3
        + rational_to_f64(&coeffs[3]) * sqrt6
}

fn rational_to_f64(x: &BigRational) -> f64 {
    x.to_f64()
        .expect("BigRational coefficient outside f64 range")
}

fn project_psd(matrix: &[Vec<f64>], floor: f64) -> (Vec<Vec<f64>>, SpectrumSummary) {
    let n = matrix.len();
    let sym = DMatrix::from_fn(n, n, |r, c| 0.5 * (matrix[r][c] + matrix[c][r]));
    let eig = SymmetricEigen::new(sym);
    let mut summary = SpectrumSummary {
        min: f64::INFINITY,
        max: f64::NEG_INFINITY,
        negative_mass: 0.0,
        negative_count: 0,
    };
    for &lambda in eig.eigenvalues.iter() {
        summary.min = summary.min.min(lambda);
        summary.max = summary.max.max(lambda);
        if lambda < 0.0 {
            summary.negative_mass += -lambda;
            summary.negative_count += 1;
        }
    }

    let mut out = vec![vec![0.0; n]; n];
    for k in 0..n {
        let lambda = eig.eigenvalues[k].max(floor);
        if lambda == 0.0 {
            continue;
        }
        for r in 0..n {
            let vr = eig.eigenvectors[(r, k)];
            for c in 0..=r {
                out[r][c] += lambda * vr * eig.eigenvectors[(c, k)];
            }
        }
    }
    for r in 0..n {
        for c in 0..r {
            out[c][r] = out[r][c];
        }
    }
    (out, summary)
}

fn spectrum_summary(matrix: &[Vec<f64>]) -> SpectrumSummary {
    let n = matrix.len();
    let sym = DMatrix::from_fn(n, n, |r, c| 0.5 * (matrix[r][c] + matrix[c][r]));
    let eig = SymmetricEigen::new(sym);
    let mut summary = SpectrumSummary {
        min: f64::INFINITY,
        max: f64::NEG_INFINITY,
        negative_mass: 0.0,
        negative_count: 0,
    };
    for &lambda in eig.eigenvalues.iter() {
        summary.min = summary.min.min(lambda);
        summary.max = summary.max.max(lambda);
        if lambda < 0.0 {
            summary.negative_mass += -lambda;
            summary.negative_count += 1;
        }
    }
    summary
}

fn zero_matrix(n: usize) -> Vec<Vec<f64>> {
    vec![vec![0.0; n]; n]
}

fn frobenius_norm(matrix: &[Vec<f64>]) -> f64 {
    matrix
        .iter()
        .flat_map(|row| row.iter())
        .map(|value| value * value)
        .sum::<f64>()
        .sqrt()
}

fn scale_matrix(matrix: &mut [Vec<f64>], scale: f64) {
    for row in matrix {
        for value in row {
            *value *= scale;
        }
    }
}

fn scale_matrix_owned(matrix: &[Vec<f64>], scale: f64) -> Vec<Vec<f64>> {
    matrix
        .iter()
        .map(|row| row.iter().map(|value| scale * value).collect())
        .collect()
}

fn matrix_linear_combination(
    left_scale: f64,
    left: &[Vec<f64>],
    right_scale: f64,
    right: &[Vec<f64>],
) -> Vec<Vec<f64>> {
    let n = left.len();
    let mut out = vec![vec![0.0; n]; n];
    for r in 0..n {
        for c in 0..n {
            out[r][c] = left_scale * left[r][c] + right_scale * right[r][c];
        }
    }
    out
}

fn trace_inner(left: &[Vec<f64>], right: &[Vec<f64>]) -> f64 {
    let mut acc = 0.0;
    for r in 0..left.len() {
        for c in 0..left.len() {
            acc += left[r][c] * right[r][c];
        }
    }
    acc
}

fn relative_frobenius_step(next: &[Vec<f64>], prev: &[Vec<f64>]) -> f64 {
    let mut diff_sq = 0.0;
    let mut prev_sq = 0.0;
    for r in 0..next.len() {
        for c in 0..next.len() {
            let diff = next[r][c] - prev[r][c];
            diff_sq += diff * diff;
            prev_sq += prev[r][c] * prev[r][c];
        }
    }
    diff_sq.sqrt() / prev_sq.sqrt().max(1.0)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn affine_projection_enforces_moment_constraints() {
        let problem = FloatMomentProblem::new();
        let margin = 0.01;
        let mut matrix = problem.target_matrix(margin);
        matrix[0][0] += 0.25;
        matrix[0][1] -= 0.125;
        matrix[1][0] = matrix[0][1];
        assert!(problem.max_affine_residual(&matrix, margin) > 1.0e-3);
        problem.project_affine(&mut matrix, margin);
        assert!(problem.max_affine_residual(&matrix, margin) <= 1.0e-10);
    }

    #[test]
    fn zero_margin_probe_is_float_feasible_but_not_authority() {
        let mut config = FloatSdpConfig::for_margin(0.0);
        config.iterations = 4;
        let state = run_float_sdp_probe(config);
        assert!(state.report.affine_residual_final <= 1.0e-8);
        assert!(state.report.min_eigen_final >= -1.0e-7);
        assert!(state.report.feasible_by_float_tolerance);
        assert!(!state.report.has_exact_certificate);
        assert!(!state.report.has_full_mub6_authority);
        assert_eq!(
            state.report.backend,
            FloatProjectionBackend::DouglasRachford
        );
        assert!(state.report.boundary.contains("Stage C"));
    }

    #[test]
    fn dykstra_zero_margin_probe_is_float_feasible_but_not_authority() {
        let mut config = FloatSdpConfig::for_margin(0.0);
        config.backend = FloatProjectionBackend::Dykstra;
        config.iterations = 4;
        let state = run_float_sdp_probe(config);
        assert!(state.report.affine_residual_final <= 1.0e-8);
        assert!(state.report.min_eigen_final >= -1.0e-7);
        assert!(state.report.feasible_by_float_tolerance);
        assert_eq!(state.report.backend, FloatProjectionBackend::Dykstra);
        assert!(!state.report.has_exact_certificate);
        assert!(!state.report.has_full_mub6_authority);
    }

    #[test]
    fn low_rank_zero_margin_probe_is_psd_float_feasible_but_not_authority() {
        let mut config = FloatSdpConfig::for_margin(0.0);
        config.backend = FloatProjectionBackend::LowRankFactor;
        config.iterations = 0;
        let state = run_float_sdp_probe(config);
        assert!(state.report.affine_residual_final <= 1.0e-8);
        assert!(state.report.min_eigen_final >= -1.0e-7);
        assert!(state.report.feasible_by_float_tolerance);
        assert!(!state.report.float_residual_dual_observed);
        assert_eq!(state.report.backend, FloatProjectionBackend::LowRankFactor);
        assert!(!state.report.has_exact_certificate);
        assert!(!state.report.has_full_mub6_authority);
    }

    #[test]
    fn low_rank_positive_margin_probe_is_psd_scaffold_only() {
        let mut config = FloatSdpConfig::for_margin(1.0e-4);
        config.backend = FloatProjectionBackend::LowRankFactor;
        config.iterations = 4;
        let state = run_float_sdp_probe(config);
        assert_eq!(state.gram.len(), 78);
        assert_eq!(state.gram[0].len(), 78);
        assert!(state.report.affine_residual_final.is_finite());
        assert!(state.report.residual_dual_min_eigen_final.is_finite());
        assert!(state.report.residual_dual_objective_final.is_finite());
        assert!(!state.report.float_residual_dual_observed);
        assert!(state.report.min_eigen_final >= -1.0e-7);
        assert_eq!(state.report.backend, FloatProjectionBackend::LowRankFactor);
        assert!(!state.report.has_exact_certificate);
        assert!(!state.report.has_full_mub6_authority);
    }

    #[test]
    fn spectral_ascent_zero_margin_probe_is_float_feasible_but_not_authority() {
        let mut config = FloatSdpConfig::for_margin(0.0);
        config.backend = FloatProjectionBackend::SpectralAscent;
        config.iterations = 4;
        let state = run_float_sdp_probe(config);
        assert!(state.report.affine_residual_final <= 1.0e-8);
        assert!(state.report.min_eigen_final >= -1.0e-7);
        assert!(state.report.feasible_by_float_tolerance);
        assert!(!state.report.float_dual_separation_observed);
        assert_eq!(state.report.backend, FloatProjectionBackend::SpectralAscent);
        assert!(!state.report.has_exact_certificate);
        assert!(!state.report.has_full_mub6_authority);
    }

    #[test]
    fn positive_margin_probe_runs_as_untrusted_diagnostic() {
        let mut config = FloatSdpConfig::for_margin(1.0e-3);
        config.iterations = 3;
        let state = run_float_sdp_probe(config);
        assert_eq!(state.gram.len(), 78);
        assert_eq!(state.gram[0].len(), 78);
        assert!(state.report.affine_residual_final.is_finite());
        assert!(state.report.min_eigen_final.is_finite());
        assert!(!state.report.has_exact_certificate);
        assert!(!state.report.has_full_mub6_authority);
    }

    #[test]
    fn spectral_ascent_positive_margin_probe_records_pressure_without_authority() {
        let mut config = FloatSdpConfig::for_margin(1.0e-4);
        config.backend = FloatProjectionBackend::SpectralAscent;
        config.iterations = 8;
        let state = run_float_sdp_probe(config);
        assert_eq!(state.gram.len(), 78);
        assert_eq!(state.gram[0].len(), 78);
        assert!(state.report.affine_residual_final <= 1.0e-8);
        assert!(state.report.min_eigen_final.is_finite());
        assert!(state
            .report
            .spectral_tangent_pressure_norm_final
            .is_finite());
        assert!(state.report.dual_separation_value_final < -1.0e-10);
        assert!(!state.report.float_dual_separation_observed);
        assert_eq!(state.report.backend, FloatProjectionBackend::SpectralAscent);
        assert!(!state.report.has_exact_certificate);
        assert!(!state.report.has_full_mub6_authority);
    }

    #[test]
    fn invariant_systems_margin_is_sanity_target_only() {
        let sanity = invariant_systems_sanity_margin();
        assert!(sanity > 0.03 && sanity < 0.04);
        let scan = run_float_margin_scan(
            &[0.0, 1.0e-3],
            FloatSdpConfig {
                margin: 0.0,
                iterations: 2,
                feasibility_tol: 1.0e-7,
                eigen_floor: 0.0,
                backend: FloatProjectionBackend::DouglasRachford,
            },
        );
        assert_eq!(scan.reports.len(), 2);
        assert_eq!(scan.invariant_systems_sanity_margin, sanity);
        assert!(scan.boundary.contains("Float scan only"));
    }

    #[test]
    #[ignore = "diagnostic: runs the bounded Stage B f64 margin scan and prints JSON"]
    fn stage_b_float_margin_scan_diagnostic() {
        let scan = run_default_float_margin_scan();
        eprintln!(
            "{}",
            serde_json::to_string_pretty(&scan).expect("serialize Stage B diagnostic scan")
        );
        assert!(!scan.reports.is_empty());
        assert!(scan.boundary.contains("Float scan only"));
    }

    #[test]
    #[ignore = "diagnostic: runs the bounded Stage B f64 Dykstra margin scan and prints JSON"]
    fn stage_b_dykstra_margin_scan_diagnostic() {
        let scan = run_default_dykstra_float_margin_scan();
        eprintln!(
            "{}",
            serde_json::to_string_pretty(&scan).expect("serialize Stage B Dykstra scan")
        );
        assert!(!scan.reports.is_empty());
        assert!(scan
            .reports
            .iter()
            .all(|report| report.backend == FloatProjectionBackend::Dykstra));
        assert!(scan.boundary.contains("Float scan only"));
    }

    #[test]
    #[ignore = "diagnostic: runs the bounded Stage B f64 spectral-ascent margin scan and prints JSON"]
    fn stage_b_spectral_margin_scan_diagnostic() {
        let scan = run_default_spectral_float_margin_scan();
        eprintln!(
            "{}",
            serde_json::to_string_pretty(&scan).expect("serialize Stage B spectral scan")
        );
        assert!(!scan.reports.is_empty());
        assert!(scan
            .reports
            .iter()
            .all(|report| report.backend == FloatProjectionBackend::SpectralAscent));
        assert!(scan.boundary.contains("Float scan only"));
    }

    #[test]
    #[ignore = "diagnostic: runs the bounded Stage B f64 low-rank factor margin scan and prints JSON"]
    fn stage_b_low_rank_margin_scan_diagnostic() {
        let scan = run_default_low_rank_float_margin_scan();
        eprintln!(
            "{}",
            serde_json::to_string_pretty(&scan).expect("serialize Stage B low-rank scan")
        );
        assert!(!scan.reports.is_empty());
        assert!(scan
            .reports
            .iter()
            .all(|report| report.backend == FloatProjectionBackend::LowRankFactor));
        assert!(scan.boundary.contains("Float scan only"));
    }
}
