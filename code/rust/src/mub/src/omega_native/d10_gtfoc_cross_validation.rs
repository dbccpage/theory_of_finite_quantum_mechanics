
use linear_algebra::linear_algebra::complex_matrix::{CVector, ComplexMatrix, C64};
use omega_functional::{
    MubFeasibilityWallDiagnosticIntervalAttempt, MubFeasibilityWallFunctional,
    MubFeasibilityWallTargetComparison,
};
use serde::Serialize;
use std::collections::{BTreeMap, VecDeque};
use std::sync::OnceLock;

use crate::omega_native::float_check::gtfoc_float_wall::{
    inner, norm, probabilities, projected_s_gradient, qubit_x_basis, qubit_y_basis,
    residual_square_sum, root_of_unity, seeded_unit_vector, tensor_vec, zero_vec,
};

type C = C64;
type Vector = CVector;
type Matrix = ComplexMatrix;

const D: usize = 10;
const BASIS_COUNT: usize = 3;
const COLUMN_COUNT: usize = 30;
const TARGET_PHI1: f64 = 0.022445681481245097;
const TARGET_W10: f64 = 0.9775543185187549;

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Serialize)]
pub enum MatchStatus {
    Match,
    Mismatch,
    NotCertified,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Serialize)]
pub enum D10GtfocTrichotomyClass {
    ClosedSurvivor,
    ExactRepair,
    OpenObstruction,
    NotCertified,
}

#[derive(Debug, Clone, PartialEq, Serialize)]
pub struct D10GtfocMatchItem<T> {
    pub status: MatchStatus,
    pub computed: T,
    pub expected: T,
    pub tolerance: f64,
    pub note: &'static str,
}

#[derive(Debug, Clone, PartialEq, Serialize)]
pub struct D10GtfocResidualCochain {
    pub c0_description: &'static str,
    pub c1_description: &'static str,
    pub c2_description: &'static str,
    pub c0_dim: usize,
    pub c1_dim: usize,
    pub c2_dim: usize,
    pub ray_locus_dim: usize,
    pub q1_dim: usize,
    pub d1_basis_sum_linf: f64,
    pub phase_gauge_dim: usize,
    pub continuous_symmetry_dim_seen: usize,
}

#[derive(Debug, Clone, PartialEq, Serialize)]
pub struct D10NamedAntiunitaryTransport {
    pub status: MatchStatus,
    pub qubit_transport: Option<String>,
    pub quint_transport: Option<String>,
    pub note: &'static str,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Serialize)]
pub enum D10GtfocTerminalVerdictKind {
    CrossValidatedF64Only,
    Mismatch,
}

#[derive(Debug, Clone, PartialEq, Serialize)]
pub struct D10GtfocTerminalVerdict {
    pub kind: D10GtfocTerminalVerdictKind,
    pub cross_validated: bool,
    pub has_diagnostic_interval_attempt: bool,
    pub diagnostic_interval_contains_targets: bool,
    pub has_exact_phi_wall_certificate: bool,
    pub has_global_wall_certificate: bool,
    pub has_full_mub10_authority: bool,
    pub missing_proof_obligations: Vec<&'static str>,
    pub note: &'static str,
}

#[derive(Debug, Clone, PartialEq, Serialize)]
pub struct D10GtfocCrossValidationReport {
    pub target: &'static str,
    pub method: &'static str,
    pub wall_value: f64,
    pub wall_comparison: MubFeasibilityWallTargetComparison,
    pub wall_interval_attempt: MubFeasibilityWallDiagnosticIntervalAttempt,
    pub phi1: D10GtfocMatchItem<f64>,
    pub class: D10GtfocMatchItem<D10GtfocTrichotomyClass>,
    pub ray_locus_dim: D10GtfocMatchItem<usize>,
    pub z2_real_structure: D10GtfocMatchItem<usize>,
    pub named_antiunitary_word_match: D10GtfocMatchItem<bool>,
    pub named_antiunitary_transport: D10NamedAntiunitaryTransport,
    pub derived_qubit_word: String,
    pub derived_quint_word: String,
    pub clifford_elements_scanned: usize,
    pub unitary_fixers: D10GtfocMatchItem<usize>,
    pub antiunitary_fixers: D10GtfocMatchItem<usize>,
    pub real_fixed_locus_dim: usize,
    pub ray_dof: usize,
    pub low_degree_closed_form_status: MatchStatus,
    pub cochain: D10GtfocResidualCochain,
    pub overall: MatchStatus,
    pub terminal_verdict: D10GtfocTerminalVerdict,
    pub certified_digits: usize,
    pub boundary: &'static str,
}

#[derive(Debug, Clone)]
struct CliffordCensus {
    elements_scanned: usize,
    unitary_fixers: usize,
    antiunitary_fixers: usize,
    antiunitary_involution_count: usize,
    named_antiunitary_word_matches: usize,
    named_antiunitary_transport: D10NamedAntiunitaryTransport,
    derived_qubit_word: String,
    derived_quint_word: String,
    real_fixed_locus_dim: usize,
}

#[derive(Debug, Clone)]
struct CliffordElement {
    matrix: Matrix,
    word: String,
}

pub fn d10_gtfoc_cross_validation_report() -> &'static D10GtfocCrossValidationReport {
    static REPORT: OnceLock<D10GtfocCrossValidationReport> = OnceLock::new();
    REPORT.get_or_init(run_d10_gtfoc_cross_validation)
}

pub fn run_d10_gtfoc_cross_validation() -> D10GtfocCrossValidationReport {
    let columns = canonical_d10_columns();
    let maximizer = optimize_wall_candidate(&columns);
    let probabilities = probabilities(&columns, &maximizer);
    let wall = MubFeasibilityWallFunctional::evaluate_probabilities(&probabilities, 0.1)
        .expect("finite d=10 MUB wall functional");
    let wall_value = wall.wall_value;
    let phi_value = wall.obstruction_value;
    let wall_comparison = MubFeasibilityWallFunctional::compare_targets_f64_diagnostic(
        &wall,
        TARGET_PHI1,
        TARGET_W10,
        2.5e-10,
    )
    .expect("finite d=10 MUB wall target comparison");
    let wall_interval_attempt =
        MubFeasibilityWallFunctional::diagnostic_interval_attempt(&wall, &wall_comparison)
            .expect("finite d=10 MUB wall diagnostic interval attempt");
    let omega: Vec<f64> = probabilities.iter().map(|p| p - 0.1).collect();
    let d1_linf = basis_sum_linf(&omega);
    let census = full_clifford_census(&maximizer);

    let phi_match = wall_comparison.obstruction_matches;
    let wall_match = wall_comparison.wall_matches;
    let class_value = if phi_value > 1e-12 && d1_linf < 1e-10 {
        D10GtfocTrichotomyClass::ClosedSurvivor
    } else if phi_value <= 1e-12 {
        D10GtfocTrichotomyClass::ExactRepair
    } else {
        D10GtfocTrichotomyClass::OpenObstruction
    };
    let class_match = class_value == D10GtfocTrichotomyClass::ClosedSurvivor;
    let ray_locus_dim = census.real_fixed_locus_dim.saturating_sub(1);
    let ray_locus_match = ray_locus_dim == 9;
    let z2_match = census.antiunitary_involution_count == 1
        && census.unitary_fixers == 0
        && census.antiunitary_fixers == 1;
    let named_word_match = census.named_antiunitary_word_matches == 1;
    let named_transport_match = census.named_antiunitary_transport.status == MatchStatus::Match;
    let overall = if phi_match
        && wall_match
        && class_match
        && ray_locus_match
        && z2_match
        && named_transport_match
    {
        MatchStatus::Match
    } else {
        MatchStatus::Mismatch
    };

    D10GtfocCrossValidationReport {
        target: "d=10 canonical-triple fourth-vector wall",
        method: "Omega-native f64 CODA-FOC/DDA residual cochain plus omega_functional wall scalar/comparison plus full Cl(2) tensor Cl(5) stabilizer census",
        wall_value,
        wall_comparison: wall_comparison.clone(),
        wall_interval_attempt: wall_interval_attempt.clone(),
        phi1: D10GtfocMatchItem {
            status: status(phi_match),
            computed: phi_value,
            expected: TARGET_PHI1,
            tolerance: wall_comparison.tolerance,
            note: "Phi1 is the normalized squared residual 1 - f(v*) computed by omega_functional; f64 diagnostic comparison only certifies by the declared tolerance.",
        },
        class: D10GtfocMatchItem {
            status: status(class_match),
            computed: class_value,
            expected: D10GtfocTrichotomyClass::ClosedSurvivor,
            tolerance: 0.0,
            note: "ClosedSurvivor means nonzero quotient residual with d1 omega = 0 under the three basis-sum closures.",
        },
        ray_locus_dim: D10GtfocMatchItem {
            status: status(ray_locus_match),
            computed: ray_locus_dim,
            expected: 9,
            tolerance: 0.0,
            note: "Real-dimension count of the K-real fixed locus modulo the one phase/ray gauge (10 - 1 = 9). This is NOT a computed cohomology H1: no ker/im quotient of a cochain map is taken here.",
        },
        z2_real_structure: D10GtfocMatchItem {
            status: status(z2_match),
            computed: census.antiunitary_involution_count,
            expected: 1,
            tolerance: 0.0,
            note: "The C0-level finite symmetry scan sees exactly one antiunitary involution and no nontrivial unitary fixer.",
        },
        named_antiunitary_word_match: D10GtfocMatchItem {
            status: status(named_word_match),
            computed: named_word_match,
            expected: true,
            tolerance: 0.0,
            note: "Literal equality between the DDA-derived fixer word and the named HXZ tensor V representative under local sign/order conventions.",
        },
        named_antiunitary_transport: census.named_antiunitary_transport.clone(),
        derived_qubit_word: census.derived_qubit_word.clone(),
        derived_quint_word: census.derived_quint_word.clone(),
        clifford_elements_scanned: census.elements_scanned,
        unitary_fixers: D10GtfocMatchItem {
            status: status(census.unitary_fixers == 0),
            computed: census.unitary_fixers,
            expected: 0,
            tolerance: 0.0,
            note: "Nontrivial projective unitary fixers in Cl(2) tensor Cl(5).",
        },
        antiunitary_fixers: D10GtfocMatchItem {
            status: status(census.antiunitary_fixers == 1),
            computed: census.antiunitary_fixers,
            expected: 1,
            tolerance: 0.0,
            note: "Projective antiunitary fixers U conjugation with |<v,U conj(v)>| = 1 at f64 tolerance.",
        },
        real_fixed_locus_dim: census.real_fixed_locus_dim,
        ray_dof: ray_locus_dim,
        low_degree_closed_form_status: MatchStatus::NotCertified,
        cochain: D10GtfocResidualCochain {
            c0_description: "phase gauge plus finite Clifford/antiunitary carrier symmetries preserving the canonical triple",
            c1_description: "30 residual coordinates omega_j = |<c_j,v>|^2 - 1/10 plus K-real deformation coordinates at the survivor",
            c2_description: "three exact basis-sum closures sum_{j in basis b} omega_j = 0",
            c0_dim: 1,
            c1_dim: COLUMN_COUNT,
            c2_dim: BASIS_COUNT,
            ray_locus_dim,
            q1_dim: COLUMN_COUNT,
            d1_basis_sum_linf: d1_linf,
            phase_gauge_dim: 1,
            continuous_symmetry_dim_seen: 0,
        },
        overall,
        terminal_verdict: terminal_verdict(overall, &wall_comparison, &wall_interval_attempt),
        certified_digits: if phi_match && wall_match {
            wall_comparison.certified_digits
        } else {
            0
        },
        boundary: "Cross-validation evidence only: f64 diagnostic comparison, no exact Phi/W10 certificate, no global d=10 wall certificate, no low-degree closed-form proof, and no complete MUB(10) theorem authority.",
    }
}

fn status(ok: bool) -> MatchStatus {
    if ok {
        MatchStatus::Match
    } else {
        MatchStatus::Mismatch
    }
}

fn terminal_verdict(
    overall: MatchStatus,
    wall_comparison: &MubFeasibilityWallTargetComparison,
    wall_interval_attempt: &MubFeasibilityWallDiagnosticIntervalAttempt,
) -> D10GtfocTerminalVerdict {
    let cross_validated = overall == MatchStatus::Match;
    let mut missing_proof_obligations = Vec::new();
    if !wall_comparison.has_exact_certificate {
        missing_proof_obligations.push("exact Phi1/W10 certificate");
    }
    if !wall_comparison.has_global_upper_bound_certificate {
        missing_proof_obligations.push("global d=10 wall upper-bound certificate");
    }
    missing_proof_obligations.push("complete MUB(10) theorem authority");

    let interval_contains_targets = wall_interval_attempt.obstruction.contains_target
        && wall_interval_attempt.wall.contains_target;

    D10GtfocTerminalVerdict {
        kind: if cross_validated {
            D10GtfocTerminalVerdictKind::CrossValidatedF64Only
        } else {
            D10GtfocTerminalVerdictKind::Mismatch
        },
        cross_validated,
        has_diagnostic_interval_attempt: true,
        diagnostic_interval_contains_targets: interval_contains_targets,
        has_exact_phi_wall_certificate: wall_comparison.has_exact_certificate,
        has_global_wall_certificate: wall_comparison.has_global_upper_bound_certificate,
        has_full_mub10_authority: false,
        missing_proof_obligations,
        note: "Terminal verdict for this loop: CODA-FOC cross-validates the canonical-triple d=10 wall data at f64 diagnostic authority only.",
    }
}

fn canonical_d10_columns() -> Vec<Vector> {
    let mut columns = Vec::with_capacity(COLUMN_COUNT);
    for idx in 0..D {
        let mut v = zero_vec(D);
        v[idx] = C::new(1.0, 0.0);
        columns.push(v);
    }

    let x2 = qubit_x_basis();
    let y2 = qubit_y_basis();
    let q0 = quint_q_basis(0);
    let q1 = quint_q_basis(1);
    for qb in &x2 {
        for qt in &q0 {
            columns.push(tensor_vec(qb, qt));
        }
    }
    for qb in &y2 {
        for qt in &q1 {
            columns.push(tensor_vec(qb, qt));
        }
    }
    columns
}

fn quint_q_basis(a: i32) -> Vec<Vector> {
    let mut columns = Vec::with_capacity(5);
    let scale = 1.0 / 5.0_f64.sqrt();
    for m in 0..5_i32 {
        let mut col = zero_vec(5);
        for j in 0..5_i32 {
            let exp = a * j * j + m * j;
            col[j as usize] = root_of_unity(5, exp) * scale;
        }
        columns.push(col);
    }
    columns
}

fn optimize_wall_candidate(columns: &[Vector]) -> Vector {
    let mut best = zero_vec(D);
    let mut best_s = f64::INFINITY;
    for seed in 0..96_u64 {
        let mut v = seeded_unit_vector(seed, D);
        let mut s = residual_square_sum(columns, &v);
        let mut step: f64 = 0.08;
        for _ in 0..2500 {
            let grad = projected_s_gradient(columns, &v);
            let grad_norm = norm(&grad);
            if grad_norm < 1e-13 {
                break;
            }
            let mut accepted = false;
            for _ in 0..16 {
                let candidate = normalize(&Vector::from_vec(
                    v.iter()
                        .zip(&grad)
                        .map(|(vi, gi)| *vi - step * *gi)
                        .collect::<Vec<_>>(),
                ));
                let candidate_s = residual_square_sum(columns, &candidate);
                if candidate_s < s {
                    v = candidate;
                    s = candidate_s;
                    step = (step * 1.08).min(0.5);
                    accepted = true;
                    break;
                }
                step *= 0.5;
            }
            if !accepted || step < 1e-14 {
                break;
            }
        }
        if s < best_s {
            best_s = s;
            best = v;
        }
    }
    best
}

fn basis_sum_linf(omega: &[f64]) -> f64 {
    let mut max = 0.0_f64;
    for basis in 0..BASIS_COUNT {
        let sum: f64 = omega[basis * D..(basis + 1) * D].iter().sum();
        max = max.max(sum.abs());
    }
    max
}

fn full_clifford_census(v: &Vector) -> CliffordCensus {
    let cl2 = labeled_projective_clifford_group(2);
    let cl5 = labeled_projective_clifford_group(5);
    assert_eq!(cl2.len(), 24);
    assert_eq!(cl5.len(), 3000);

    let v_conj = Vector::from_vec(v.iter().map(|z| z.conj()).collect());
    let mut elements_scanned = 0;
    let mut unitary_fixers = 0;
    let mut antiunitary_fixers = 0;
    let mut antiunitary_involution_count = 0;
    let mut named_antiunitary_word_matches = 0;
    let mut derived_qubit_word = String::new();
    let mut derived_quint_word = String::new();
    let mut derived_qubit_matrix = None;
    let mut derived_quint_matrix = None;
    let mut real_fixed_locus_dim = 0;
    let identity = identity(D);
    let named_antiunitary_targets = named_antiunitary_targets();

    for q in &cl2 {
        for r in &cl5 {
            elements_scanned += 1;
            let u = kron_mat(&q.matrix, 2, &r.matrix, 5);
            if !projectively_close(&u, &identity, 1e-8) {
                let uv = mat_vec(&u, D, v);
                if alignment(v, &uv) > 1.0 - 1e-8 {
                    unitary_fixers += 1;
                }
            }
            let ukv = mat_vec(&u, D, &v_conj);
            if alignment(v, &ukv) > 1.0 - 1e-8 {
                antiunitary_fixers += 1;
                if derived_qubit_word.is_empty() {
                    derived_qubit_word = q.word.clone();
                    derived_quint_word = r.word.clone();
                    derived_qubit_matrix = Some(q.matrix.clone());
                    derived_quint_matrix = Some(r.matrix.clone());
                }
                if named_antiunitary_targets
                    .iter()
                    .any(|target| projectively_close(&u, target, 1e-8))
                {
                    named_antiunitary_word_matches += 1;
                }
                let u_conj = u
                    .conjugate()
                    .expect("finite ComplexMatrix conjugate should be valid");
                let k2 = mat_mul(&u, &u_conj, D);
                if projectively_close(&k2, &identity, 1e-8) {
                    antiunitary_involution_count += 1;
                    real_fixed_locus_dim = D;
                }
            }
        }
    }

    let named_antiunitary_transport = match (&derived_qubit_matrix, &derived_quint_matrix) {
        (Some(q), Some(r)) => named_antiunitary_transport(q, r, &cl2, &cl5),
        _ => D10NamedAntiunitaryTransport {
            status: MatchStatus::Mismatch,
            qubit_transport: None,
            quint_transport: None,
            note: "No antiunitary fixer was available for named-word transport comparison.",
        },
    };

    CliffordCensus {
        elements_scanned,
        unitary_fixers,
        antiunitary_fixers,
        antiunitary_involution_count,
        named_antiunitary_word_matches,
        named_antiunitary_transport,
        derived_qubit_word,
        derived_quint_word,
        real_fixed_locus_dim,
    }
}
#[derive(Debug, Clone)]
struct StringMatrix {
    label: String,
    matrix: Matrix,
}

fn named_antiunitary_transport(
    derived_q: &Matrix,
    derived_r: &Matrix,
    cl2: &[CliffordElement],
    cl5: &[CliffordElement],
) -> D10NamedAntiunitaryTransport {
    let qubit_transport = first_qubit_named_transport(derived_q, cl2);
    let quint_transport = first_quint_named_transport(derived_r, cl5);
    D10NamedAntiunitaryTransport {
        status: status(qubit_transport.is_some() && quint_transport.is_some()),
        qubit_transport,
        quint_transport,
        note: "Clifford antiunitary conjugacy transport: G U conj(G)^-1 = G U G^T matches a named HXZ and V representative under tested convention variants.",
    }
}

fn first_qubit_named_transport(derived_q: &Matrix, cl2: &[CliffordElement]) -> Option<String> {
    let mut hits = Vec::new();
    for (target_label, target) in qubit_hxz_candidates() {
        for g in cl2 {
            let transported = antiunitary_conjugate(&g.matrix, derived_q, 2);
            if projectively_close(&transported, &target, 1e-8) {
                hits.push(format!("target={}; transport={}", target_label, g.word));
            }
        }
    }
    hits.sort();
    hits.into_iter().next()
}

fn first_quint_named_transport(derived_r: &Matrix, cl5: &[CliffordElement]) -> Option<String> {
    let mut hits = Vec::new();
    for target in quint_v_candidates() {
        for g in cl5 {
            let transported = antiunitary_conjugate(&g.matrix, derived_r, 5);
            if projectively_close(&transported, &target.matrix, 1e-8) {
                hits.push(format!("target={}; transport={}", target.label, g.word));
            }
        }
    }
    hits.sort();
    hits.into_iter().next()
}

fn quadratic_phase(dim: usize, a: i32, b: i32) -> Matrix {
    let mut data = zero_mat_data(dim);
    for j in 0..dim {
        let j_i = j as i32;
        data[j * dim + j] = root_of_unity(dim as i32, a * j_i * j_i + b * j_i);
    }
    matrix_from_row_major(dim, data)
}

fn qubit_hxz_candidates() -> Vec<(&'static str, Matrix)> {
    let h = fourier(2);
    let x = shift(2);
    let z = phase(2);
    let candidates = vec![
        ("H X Z", vec![h.clone(), x.clone(), z.clone()]),
        ("H Z X", vec![h.clone(), z.clone(), x.clone()]),
        ("X H Z", vec![x.clone(), h.clone(), z.clone()]),
        ("X Z H", vec![x.clone(), z.clone(), h.clone()]),
        ("Z H X", vec![z.clone(), h.clone(), x.clone()]),
        ("Z X H", vec![z, x, h]),
    ];
    let mut out = Vec::new();
    for (label, seq) in candidates {
        out.push((label, word_right(2, &seq)));
        out.push((label, word_left(2, &seq)));
    }
    out
}

fn quint_v_candidates() -> Vec<StringMatrix> {
    let mut out = Vec::new();
    for x_sign in [-1, 1] {
        for z_sign in [-1, 1] {
            for f_sign in [-1, 1] {
                for a in 0..5 {
                    for b in 0..5 {
                        let s = quadratic_phase(5, a, b);
                        let quint_word = vec![
                            phase_signed(5, z_sign),
                            s.clone(),
                            shift_signed(5, x_sign),
                            s.clone(),
                            fourier_signed(5, f_sign),
                            s.clone(),
                            fourier_signed(5, f_sign),
                            s.clone(),
                            fourier_signed(5, f_sign),
                            s.clone(),
                            s.clone(),
                        ];
                        for order in ["right", "left"] {
                            let matrix = if order == "right" {
                                word_right(5, &quint_word)
                            } else {
                                word_left(5, &quint_word)
                            };
                            out.push(StringMatrix {
                                label: format!(
                                    "order={}; x={}; z={}; f={}; S=a*j^2+b*j with a={}, b={}",
                                    order, x_sign, z_sign, f_sign, a, b
                                ),
                                matrix,
                            });
                        }
                    }
                }
            }
        }
    }
    out
}
fn named_antiunitary_targets() -> Vec<Matrix> {
    let mut targets = Vec::new();
    let signs = [-1, 1];
    for x_sign in signs {
        for z_sign in signs {
            for f_sign in signs {
                for s_sign in signs {
                    let qubit_word = vec![fourier(2), shift(2), phase(2)];
                    let quint_word = vec![
                        phase_signed(5, z_sign),
                        odd_shear_signed(5, s_sign),
                        shift_signed(5, x_sign),
                        odd_shear_signed(5, s_sign),
                        fourier_signed(5, f_sign),
                        odd_shear_signed(5, s_sign),
                        fourier_signed(5, f_sign),
                        odd_shear_signed(5, s_sign),
                        fourier_signed(5, f_sign),
                        odd_shear_signed(5, s_sign),
                        odd_shear_signed(5, s_sign),
                    ];
                    let qubit_targets = [word_right(2, &qubit_word), word_left(2, &qubit_word)];
                    let quint_targets = [word_right(5, &quint_word), word_left(5, &quint_word)];
                    for q in &qubit_targets {
                        for r in &quint_targets {
                            targets.push(kron_mat(q, 2, r, 5));
                        }
                    }
                }
            }
        }
    }
    targets
}

fn word_right(dim: usize, generators: &[Matrix]) -> Matrix {
    let mut acc = identity(dim);
    for generator in generators {
        acc = mat_mul(&acc, generator, dim);
    }
    canonical_projective(&acc)
}

fn word_left(dim: usize, generators: &[Matrix]) -> Matrix {
    let mut acc = identity(dim);
    for generator in generators {
        acc = mat_mul(generator, &acc, dim);
    }
    canonical_projective(&acc)
}

fn labeled_projective_clifford_group(dim: usize) -> Vec<CliffordElement> {
    let generators = if dim == 2 {
        vec![
            ("X2", shift(2)),
            ("Z2", phase(2)),
            ("F2", fourier(2)),
            ("S2", qubit_phase()),
        ]
    } else {
        vec![
            ("X5", shift(dim)),
            ("Z5", phase(dim)),
            ("F5", fourier(dim)),
            ("S5", odd_shear(dim)),
        ]
    };
    let id = identity(dim);
    let mut seen = BTreeMap::new();
    let mut queue = VecDeque::new();
    let key = projective_key(&id);
    let identity_element = CliffordElement {
        matrix: id,
        word: "I".to_string(),
    };
    seen.insert(key, identity_element.clone());
    queue.push_back(identity_element);

    while let Some(current) = queue.pop_front() {
        for (label, generator) in &generators {
            let next_matrix = canonical_projective(&mat_mul(generator, &current.matrix, dim));
            let key = projective_key(&next_matrix);
            if !seen.contains_key(&key) {
                let word = if current.word == "I" {
                    label.to_string()
                } else {
                    format!("{} {}", label, current.word)
                };
                let next = CliffordElement {
                    matrix: next_matrix,
                    word,
                };
                seen.insert(key, next.clone());
                queue.push_back(next);
            }
        }
    }
    let mut out = seen.into_values().collect::<Vec<_>>();
    out.sort_by(|left, right| left.word.cmp(&right.word));
    out
}
fn shift_signed(dim: usize, sign: i32) -> Matrix {
    let mut data = zero_mat_data(dim);
    for j in 0..dim {
        let row = if sign >= 0 {
            (j + 1) % dim
        } else {
            (j + dim - 1) % dim
        };
        data[row * dim + j] = C::new(1.0, 0.0);
    }
    matrix_from_row_major(dim, data)
}

fn phase_signed(dim: usize, sign: i32) -> Matrix {
    let mut data = zero_mat_data(dim);
    for j in 0..dim {
        data[j * dim + j] = root_of_unity(dim as i32, sign * j as i32);
    }
    matrix_from_row_major(dim, data)
}

fn fourier_signed(dim: usize, sign: i32) -> Matrix {
    let mut data = zero_mat_data(dim);
    let scale = 1.0 / (dim as f64).sqrt();
    for j in 0..dim {
        for k in 0..dim {
            data[j * dim + k] = root_of_unity(dim as i32, sign * (j * k) as i32) * scale;
        }
    }
    matrix_from_row_major(dim, data)
}

fn odd_shear_signed(dim: usize, sign: i32) -> Matrix {
    let mut data = zero_mat_data(dim);
    for j in 0..dim {
        let j_i = j as i32;
        let exp = sign * j_i * (j_i - 1) / 2;
        data[j * dim + j] = root_of_unity(dim as i32, exp);
    }
    matrix_from_row_major(dim, data)
}
fn shift(dim: usize) -> Matrix {
    let mut data = zero_mat_data(dim);
    for j in 0..dim {
        data[((j + 1) % dim) * dim + j] = C::new(1.0, 0.0);
    }
    matrix_from_row_major(dim, data)
}

fn phase(dim: usize) -> Matrix {
    let mut data = zero_mat_data(dim);
    for j in 0..dim {
        data[j * dim + j] = root_of_unity(dim as i32, j as i32);
    }
    matrix_from_row_major(dim, data)
}

fn fourier(dim: usize) -> Matrix {
    let mut data = zero_mat_data(dim);
    let scale = 1.0 / (dim as f64).sqrt();
    for j in 0..dim {
        for k in 0..dim {
            data[j * dim + k] = root_of_unity(dim as i32, (j * k) as i32) * scale;
        }
    }
    matrix_from_row_major(dim, data)
}

fn qubit_phase() -> Matrix {
    matrix_from_row_major(
        2,
        vec![
            C::new(1.0, 0.0),
            C::new(0.0, 0.0),
            C::new(0.0, 0.0),
            C::new(0.0, 1.0),
        ],
    )
}

fn odd_shear(dim: usize) -> Matrix {
    let mut data = zero_mat_data(dim);
    for j in 0..dim {
        let j_i = j as i32;
        let exp = j_i * (j_i - 1) / 2;
        data[j * dim + j] = root_of_unity(dim as i32, exp);
    }
    matrix_from_row_major(dim, data)
}

fn kron_mat(a: &Matrix, da: usize, b: &Matrix, db: usize) -> Matrix {
    let dim = da * db;
    let mut out = zero_mat_data(dim);
    for ar in 0..da {
        for ac in 0..da {
            for br in 0..db {
                for bc in 0..db {
                    let row = ar * db + br;
                    let col = ac * db + bc;
                    out[row * dim + col] = matrix_get(a, ar, ac) * matrix_get(b, br, bc);
                }
            }
        }
    }
    matrix_from_row_major(dim, out)
}

fn mat_vec(m: &Matrix, dim: usize, v: &Vector) -> Vector {
    let mut out = zero_vec(dim);
    for r in 0..dim {
        let mut sum = C::new(0.0, 0.0);
        for c in 0..dim {
            sum += matrix_get(m, r, c) * v[c];
        }
        out[r] = sum;
    }
    out
}

fn mat_mul(a: &Matrix, b: &Matrix, dim: usize) -> Matrix {
    debug_assert_eq!(a.shape(), (dim, dim));
    debug_assert_eq!(b.shape(), (dim, dim));
    a.mul(b)
        .expect("square ComplexMatrix multiplication should be valid")
}

fn antiunitary_conjugate(unitary_g: &Matrix, antiunitary_u: &Matrix, dim: usize) -> Matrix {
    let left = mat_mul(unitary_g, antiunitary_u, dim);
    let transposed = unitary_g
        .transpose()
        .expect("finite ComplexMatrix transpose should be valid");
    mat_mul(&left, &transposed, dim)
}

fn canonical_projective(m: &Matrix) -> Matrix {
    let pivot = m
        .as_slice()
        .iter()
        .find(|z| z.norm() > 1e-10)
        .copied()
        .unwrap_or(C::new(1.0, 0.0));
    let phase = pivot / pivot.norm();
    matrix_from_row_major(m.rows(), m.as_slice().iter().map(|z| *z / phase).collect())
}

fn projective_key(m: &Matrix) -> Vec<i64> {
    let c = canonical_projective(m);
    c.as_slice()
        .iter()
        .flat_map(|z| [(z.re / 1e-8).round() as i64, (z.im / 1e-8).round() as i64])
        .collect()
}

fn projectively_close(a: &Matrix, b: &Matrix, tol: f64) -> bool {
    let ca = canonical_projective(a);
    let cb = canonical_projective(b);
    ca.as_slice()
        .iter()
        .zip(cb.as_slice().iter())
        .all(|(x, y)| (*x - *y).norm() < tol)
}

fn identity(dim: usize) -> Matrix {
    Matrix::identity(dim).expect("finite identity matrix")
}

fn zero_mat_data(dim: usize) -> Vec<C> {
    vec![C::new(0.0, 0.0); dim * dim]
}

fn matrix_from_row_major(dim: usize, data: Vec<C>) -> Matrix {
    Matrix::from_row_major(dim, dim, data).expect("finite square ComplexMatrix")
}

fn matrix_get(matrix: &Matrix, row: usize, col: usize) -> C {
    matrix
        .get(row, col)
        .expect("ComplexMatrix index should be in bounds")
}
fn alignment(left: &Vector, right: &Vector) -> f64 {
    inner(left, right).norm() / (norm(left) * norm(right))
}

fn normalize(v: &Vector) -> Vector {
    let n = norm(v);
    Vector::from_vec(v.iter().map(|z| *z / n).collect())
}

#[cfg(test)]
mod tests {
    use super::*;
    use omega_functional::MubFeasibilityWallEvidenceKind;

    #[test]
    fn d10_gtfoc_rebuilds_canonical_triple_columns() {
        let columns = canonical_d10_columns();
        assert_eq!(columns.len(), COLUMN_COUNT);
        for column in &columns {
            assert!((norm(column) - 1.0).abs() < 1e-12);
        }
    }

    #[test]
    fn d10_clifford_closure_has_expected_projective_sizes() {
        assert_eq!(labeled_projective_clifford_group(2).len(), 24);
        assert_eq!(labeled_projective_clifford_group(5).len(), 3000);
    }

    fn derived_factor_fixers(maximizer: &Vector) -> (Matrix, Matrix) {
        let v_conj = Vector::from_vec(maximizer.iter().map(|z| z.conj()).collect());
        let cl2 = labeled_projective_clifford_group(2);
        let cl5 = labeled_projective_clifford_group(5);
        let mut found = None;
        for q in &cl2 {
            for r in &cl5 {
                let u = kron_mat(&q.matrix, 2, &r.matrix, 5);
                let ukv = mat_vec(&u, D, &v_conj);
                if alignment(maximizer, &ukv) > 1.0 - 1e-8 {
                    found = Some((q.matrix.clone(), r.matrix.clone()));
                }
            }
        }
        found.expect("unique antiunitary factor fixer")
    }

    #[test]
    #[ignore = "expensive antiunitary conjugacy transport audit"]
    fn d10_gtfoc_searches_named_word_antiunitary_conjugacy() {
        let columns = canonical_d10_columns();
        let maximizer = optimize_wall_candidate(&columns);
        let (derived_q, derived_r) = derived_factor_fixers(&maximizer);
        let cl2 = labeled_projective_clifford_group(2);
        let cl5 = labeled_projective_clifford_group(5);
        let qubit_candidates = qubit_hxz_candidates();
        let quint_candidates = quint_v_candidates();

        let mut qubit_hits = Vec::new();
        for (q_label, q_target) in &qubit_candidates {
            for g in &cl2 {
                let transported = antiunitary_conjugate(&g.matrix, &derived_q, 2);
                if projectively_close(&transported, q_target, 1e-8) {
                    qubit_hits.push(format!("target={}; transport={}", q_label, g.word));
                }
            }
        }

        let mut quint_hits = Vec::new();
        for target in &quint_candidates {
            for g in &cl5 {
                let transported = antiunitary_conjugate(&g.matrix, &derived_r, 5);
                if projectively_close(&transported, &target.matrix, 1e-8) {
                    quint_hits.push(format!("target={}; transport={}", target.label, g.word));
                }
            }
        }

        eprintln!(
            "d10_named_qubit_conjugacy_hit_count={} sample={:?}",
            qubit_hits.len(),
            qubit_hits.iter().take(4).collect::<Vec<_>>()
        );
        eprintln!(
            "d10_named_quint_conjugacy_hit_count={} sample={:?}",
            quint_hits.len(),
            quint_hits.iter().take(4).collect::<Vec<_>>()
        );
        assert!(!qubit_hits.is_empty());
        assert!(!quint_hits.is_empty());
    }
    #[test]
    #[ignore = "expensive HXZ tensor V convention transport audit"]
    fn d10_gtfoc_searches_named_word_convention_transport() {
        let columns = canonical_d10_columns();
        let maximizer = optimize_wall_candidate(&columns);
        let v_conj = Vector::from_vec(maximizer.iter().map(|z| z.conj()).collect());
        let cl2 = labeled_projective_clifford_group(2);
        let cl5 = labeled_projective_clifford_group(5);
        let mut derived = None;
        for q in &cl2 {
            for r in &cl5 {
                let u = kron_mat(&q.matrix, 2, &r.matrix, 5);
                let ukv = mat_vec(&u, D, &v_conj);
                if alignment(&maximizer, &ukv) > 1.0 - 1e-8 {
                    derived = Some(u);
                }
            }
        }
        let derived = derived.expect("unique antiunitary fixer matrix");

        let mut matches = Vec::new();
        let qubit_candidates = qubit_hxz_candidates();
        for (q_label, q) in &qubit_candidates {
            for x_sign in [-1, 1] {
                for z_sign in [-1, 1] {
                    for f_sign in [-1, 1] {
                        for a in 0..5 {
                            for b in 0..5 {
                                let s = quadratic_phase(5, a, b);
                                let quint_word = vec![
                                    phase_signed(5, z_sign),
                                    s.clone(),
                                    shift_signed(5, x_sign),
                                    s.clone(),
                                    fourier_signed(5, f_sign),
                                    s.clone(),
                                    fourier_signed(5, f_sign),
                                    s.clone(),
                                    fourier_signed(5, f_sign),
                                    s.clone(),
                                    s.clone(),
                                ];
                                for order in ["right", "left"] {
                                    let r = if order == "right" {
                                        word_right(5, &quint_word)
                                    } else {
                                        word_left(5, &quint_word)
                                    };
                                    let candidate = kron_mat(q, 2, &r, 5);
                                    if projectively_close(&candidate, &derived, 1e-8) {
                                        matches.push(format!(
                                            "q={}; order={}; x={}; z={}; f={}; S=a*j^2+b*j with a={}, b={}",
                                            q_label, order, x_sign, z_sign, f_sign, a, b
                                        ));
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }

        eprintln!("d10_named_word_convention_matches={:?}", matches);
        assert!(matches.is_empty());
    }
    #[test]
    fn d10_gtfoc_cross_validation_records_named_word_mismatch_at_f64_precision() {
        let report = run_d10_gtfoc_cross_validation();
        eprintln!(
            "d10_gtfoc_report phi1={:.17} wall={:.17} d1_linf={:.3e} ray_locus={} unitary_fixers={} antiunitary_fixers={} antiunitary_involutions={} named_word_match={} named_transport={:?} q_word={} r_word={} q_transport={:?} r_transport={:?} real_fixed_locus_dim={} overall={:?}",
            report.phi1.computed,
            report.wall_value,
            report.cochain.d1_basis_sum_linf,
            report.ray_locus_dim.computed,
            report.unitary_fixers.computed,
            report.antiunitary_fixers.computed,
            report.z2_real_structure.computed,
            report.named_antiunitary_word_match.computed,
            report.named_antiunitary_transport.status,
            report.derived_qubit_word,
            report.derived_quint_word,
            report.named_antiunitary_transport.qubit_transport,
            report.named_antiunitary_transport.quint_transport,
            report.real_fixed_locus_dim,
            report.overall
        );
        assert_eq!(report.overall, MatchStatus::Match);
        assert_eq!(
            report.terminal_verdict.kind,
            D10GtfocTerminalVerdictKind::CrossValidatedF64Only
        );
        assert!(report.terminal_verdict.cross_validated);
        assert!(report.terminal_verdict.has_diagnostic_interval_attempt);
        assert!(report.terminal_verdict.diagnostic_interval_contains_targets);
        assert!(report.wall_interval_attempt.obstruction.contains_target);
        assert!(report.wall_interval_attempt.wall.contains_target);
        assert!(!report.wall_interval_attempt.certifies_exact_value);
        assert!(!report.wall_interval_attempt.certifies_global_upper_bound);
        assert!(!report.terminal_verdict.has_exact_phi_wall_certificate);
        assert!(!report.terminal_verdict.has_global_wall_certificate);
        assert!(!report.terminal_verdict.has_full_mub10_authority);
        assert!(report
            .terminal_verdict
            .missing_proof_obligations
            .contains(&"exact Phi1/W10 certificate"));
        assert_eq!(
            report.wall_comparison.evidence_kind,
            MubFeasibilityWallEvidenceKind::F64Diagnostic
        );
        assert_eq!(report.wall_comparison.certified_digits, 9);
        assert!(!report.wall_comparison.has_exact_certificate);
        assert!(!report.wall_comparison.has_global_upper_bound_certificate);
        assert_eq!(report.phi1.status, MatchStatus::Match);
        assert_eq!(
            report.class.computed,
            D10GtfocTrichotomyClass::ClosedSurvivor
        );
        assert_eq!(report.ray_locus_dim.computed, 9);
        assert_eq!(report.clifford_elements_scanned, 24 * 3000);
        assert_eq!(report.unitary_fixers.computed, 0);
        assert_eq!(report.antiunitary_fixers.computed, 1);
        eprintln!(
            "d10 reference-run words (diagnostic, not asserted): derived_qubit={:?} derived_quint={:?} qubit_transport={:?} quint_transport={:?}",
            report.derived_qubit_word,
            report.derived_quint_word,
            report.named_antiunitary_transport.qubit_transport,
            report.named_antiunitary_transport.quint_transport
        );
        assert_eq!(
            report.named_antiunitary_word_match.status,
            MatchStatus::Mismatch
        );
        assert_eq!(
            report.named_antiunitary_transport.status,
            MatchStatus::Match
        );
        assert_eq!(report.real_fixed_locus_dim, 10);
        assert!(report.cochain.d1_basis_sum_linf < 1e-10);
        assert!(report.boundary.contains("no complete MUB(10)"));
    }
}
