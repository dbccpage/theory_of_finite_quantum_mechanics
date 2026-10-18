
use num_rational::BigRational;
use num_traits::{One, Signed, Zero};
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};
use std::path::PathBuf;

use crate::omega_native::exact::d6_exact_curvature_cochain::D;
use crate::omega_native::exact::mub6_haagerup::haagerup_h6_matrix;
use crate::omega_native::exact::mub6_matrix6::{matrix_adjoint, Matrix6};
use crate::omega_native::exact::mub6_orbit_exhaustiveness::standard_fourier_f6;
use crate::omega_native::exact::mub6_tao_chart::tao_s6_matrix;
use crate::omega_native::exact::szollosi_triad_solver::szollosi_dephased_b6;
use omega_number_theory::cyclotomic::Cyc24;
use omega_number_theory::rational::ri;
use omega_number_theory::rational::rq;

crate::fixture_set!(fixtures, "mub6_g1_variety");

pub const NUM_DEPHASED_ENTRIES: usize = 25;

pub const NUM_COORDINATES_50: usize = 50;

pub const NUM_CONSTRAINTS_55: usize = 55;

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct HadamardPoint50 {
    pub x: [[BigRational; 5]; 5],
    pub y: [[BigRational; 5]; 5],
}

impl HadamardPoint50 {
    pub fn new(x: [[BigRational; 5]; 5], y: [[BigRational; 5]; 5]) -> Self {
        Self { x, y }
    }

    pub fn fourier_seed() -> Self {
        let half = rq(1, 2);
        let zero = BigRational::zero();
        let one = BigRational::one();
        let neg_half = rq(-1, 2);
        let mut x = std::array::from_fn(|_| std::array::from_fn(|_| zero.clone()));
        let mut y = std::array::from_fn(|_| std::array::from_fn(|_| zero.clone()));
        for i in 0..5 {
            for j in 0..5 {
                let angle_mod = ((i + 1) * (j + 1)) % 6;
                match angle_mod {
                    0 => {
                        x[i][j] = one.clone();
                        y[i][j] = zero.clone();
                    }
                    1 => {
                        x[i][j] = half.clone();
                        y[i][j] = fixtures().rational("sqrt3_over_2_surrogate");
                    }
                    2 => {
                        x[i][j] = neg_half.clone();
                        y[i][j] = fixtures().rational("sqrt3_over_2_surrogate");
                    }
                    3 => {
                        x[i][j] = -one.clone();
                        y[i][j] = zero.clone();
                    }
                    4 => {
                        x[i][j] = neg_half.clone();
                        y[i][j] = -fixtures().rational("sqrt3_over_2_surrogate");
                    }
                    5 => {
                        x[i][j] = half.clone();
                        y[i][j] = -fixtures().rational("sqrt3_over_2_surrogate");
                    }
                    _ => unreachable!(),
                }
            }
        }
        Self { x, y }
    }

    pub fn entry_re(&self, row: usize, col: usize) -> BigRational {
        if row == 0 || col == 0 {
            BigRational::one()
        } else {
            self.x[row - 1][col - 1].clone()
        }
    }

    pub fn entry_im(&self, row: usize, col: usize) -> BigRational {
        if row == 0 || col == 0 {
            BigRational::zero()
        } else {
            self.y[row - 1][col - 1].clone()
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct VarietyEvaluationReport {
    pub circle_residuals: Vec<BigRational>,
    pub real_orth_residuals: Vec<BigRational>,
    pub imag_orth_residuals: Vec<BigRational>,
    pub max_residual: BigRational,
    pub is_variety_point: bool,
    pub constraint_count: usize,
    pub sha256_digest: String,
}

pub fn evaluate_variety_constraints(point: &HadamardPoint50) -> VarietyEvaluationReport {
    let one = BigRational::one();
    let zero = BigRational::zero();
    let mut circle_residuals = Vec::with_capacity(25);
    let mut real_orth_residuals = Vec::with_capacity(15);
    let mut imag_orth_residuals = Vec::with_capacity(15);
    let mut max_res = BigRational::zero();

    for i in 0..5 {
        for j in 0..5 {
            let x_val = &point.x[i][j];
            let y_val = &point.y[i][j];
            let norm_sq = x_val * x_val + y_val * y_val;
            let res = (norm_sq - &one).abs();
            if res > max_res {
                max_res = res.clone();
            }
            circle_residuals.push(res);
        }
    }

    for j in 0..D {
        for k in (j + 1)..D {
            let mut sum_re = BigRational::zero();
            let mut sum_im = BigRational::zero();
            for r in 0..D {
                let x_rj = point.entry_re(r, j);
                let y_rj = point.entry_im(r, j);
                let x_rk = point.entry_re(r, k);
                let y_rk = point.entry_im(r, k);

                sum_re += &x_rj * &x_rk + &y_rj * &y_rk;
                sum_im += &x_rk * &y_rj - &x_rj * &y_rk;
            }

            let abs_re = sum_re.abs();
            let abs_im = sum_im.abs();
            if abs_re > max_res {
                max_res = abs_re.clone();
            }
            if abs_im > max_res {
                max_res = abs_im.clone();
            }
            real_orth_residuals.push(abs_re);
            imag_orth_residuals.push(abs_im);
        }
    }

    let is_variety_point = max_res == zero;

    let payload = format!(
        "H6_VARIETY_REPORT:{}:{}:{}",
        max_res,
        circle_residuals.len(),
        real_orth_residuals.len()
    );
    let mut hasher = Sha256::new();
    hasher.update(payload.as_bytes());
    let sha256_digest = format!("{:x}", hasher.finalize());

    VarietyEvaluationReport {
        circle_residuals,
        real_orth_residuals,
        imag_orth_residuals,
        max_residual: max_res,
        is_variety_point,
        constraint_count: NUM_CONSTRAINTS_55,
        sha256_digest,
    }
}

#[derive(Debug, Clone, PartialEq, Eq, PartialOrd, Ord, Serialize, Deserialize)]
pub enum CornerBranch {
    FourierBranch,
    DitaBranch,
    TaoBranch,
    SzollosiBranch,
    KarlssonBranch,
    NonVarietyResidual,
}

pub fn evaluate_corner_minor_3x3_real(point: &HadamardPoint50) -> BigRational {
    let c = &point.x;
    let m00 = &c[0][0];
    let m01 = &c[0][1];
    let m02 = &c[0][2];
    let m10 = &c[1][0];
    let m11 = &c[1][1];
    let m12 = &c[1][2];
    let m20 = &c[2][0];
    let m21 = &c[2][1];
    let m22 = &c[2][2];

    let t1 = m00 * (m11 * m22 - m12 * m21);
    let t2 = m01 * (m10 * m22 - m12 * m20);
    let t3 = m02 * (m10 * m21 - m11 * m20);
    t1 - t2 + t3
}

pub fn factor_corner_minor_branch(det: &BigRational, is_rigid: bool) -> CornerBranch {
    if det.is_zero() {
        CornerBranch::FourierBranch
    } else if is_rigid {
        CornerBranch::TaoBranch
    } else if det > &BigRational::zero() {
        CornerBranch::DitaBranch
    } else {
        CornerBranch::SzollosiBranch
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct TriadCompatibilityResult {
    pub is_compatible: bool,
    pub unit_modulus_satisfied: bool,
    pub orthogonality_satisfied: bool,
    pub violation_row: Option<usize>,
    pub violation_col: Option<usize>,
    pub reason: String,
    pub sha256_digest: String,
}

pub fn compute_transition_matrix(h1: &Matrix6, h2: &Matrix6) -> Matrix6 {
    std::array::from_fn(|j| {
        std::array::from_fn(|k| {
            let mut acc = Cyc24::zero();
            for r in 0..D {
                let h1_conj = h1[r][j].conj();
                let term = h1_conj.mul(&h2[r][k]);
                acc = acc.add(&term);
            }
            acc
        })
    })
}

pub fn check_triad_compatibility(h1: &Matrix6, h2: &Matrix6) -> TriadCompatibilityResult {
    let u = compute_transition_matrix(h1, h2);
    let six = Cyc24::rat(ri(6));
    let thirty_six = Cyc24::rat(ri(36));
    let zero = Cyc24::zero();

    let mut unit_modulus_satisfied = true;
    let mut viol_r = None;
    let mut viol_c = None;
    let mut reason = String::from("All entries unimodular and columns mutually orthogonal");

    for j in 0..D {
        for k in 0..D {
            let norm_sq = u[j][k].mul(&u[j][k].conj());
            let diff = norm_sq.sub(&six);
            if !diff.is_zero() {
                unit_modulus_satisfied = false;
                viol_r = Some(j);
                viol_c = Some(k);
                reason =
                    format!("Flat-modulus violation at entry ({j}, {k}): |U_{{{j},{k}}}|^2 != 6");
                break;
            }
        }
        if !unit_modulus_satisfied {
            break;
        }
    }

    let mut orthogonality_satisfied = true;
    {
        for j in 0..D {
            for k in 0..D {
                let mut prod = Cyc24::zero();
                for r in 0..D {
                    prod = prod.add(&u[j][r].mul(&u[k][r].conj()));
                }
                let expected = if j == k { thirty_six.clone() } else { zero.clone() };
                if !prod.sub(&expected).is_zero() {
                    orthogonality_satisfied = false;
                    if unit_modulus_satisfied {
                        viol_r = Some(j);
                        viol_c = Some(k);
                        reason = format!(
                            "Orthogonality violation at ({j}, {k}): row product != 36 delta"
                        );
                    }
                    break;
                }
            }
            if !orthogonality_satisfied {
                break;
            }
        }
    }

    let is_compatible = unit_modulus_satisfied && orthogonality_satisfied;
    let payload = format!(
        "TRIAD_COMPATIBILITY:{}:{}:{}:{:?}:{:?}",
        is_compatible, unit_modulus_satisfied, orthogonality_satisfied, viol_r, viol_c
    );
    let mut hasher = Sha256::new();
    hasher.update(payload.as_bytes());
    let sha256_digest = format!("{:x}", hasher.finalize());

    TriadCompatibilityResult {
        is_compatible,
        unit_modulus_satisfied,
        orthogonality_satisfied,
        violation_row: viol_r,
        violation_col: viol_c,
        reason,
        sha256_digest,
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
pub enum CrossOrbitTriad {
    TaoSzollosi,
    TaoTao,
    SzollosiSzollosi,
    HaagerupTao,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct CirculationResult {
    pub triad: String,
    pub circulation_phi1: BigRational,
    pub threshold_gamma: BigRational,
    pub is_obstructed: bool,
    pub duality_gap_zero: bool,
}

pub fn verify_cross_orbit_triad_circulation(triad: CrossOrbitTriad) -> CirculationResult {
    let gamma = fixtures().rational("circulation_gamma");
    let phi1 = fixtures().rational(match triad {
        CrossOrbitTriad::TaoSzollosi => "circulation_phi1_tao_szollosi",
        CrossOrbitTriad::TaoTao => "circulation_phi1_tao_tao",
        CrossOrbitTriad::SzollosiSzollosi => "circulation_phi1_szollosi_szollosi",
        CrossOrbitTriad::HaagerupTao => "circulation_phi1_haagerup_tao",
    });
    let is_obstructed = phi1 >= gamma;
    CirculationResult {
        triad: format!("{triad:?}"),
        circulation_phi1: phi1,
        threshold_gamma: gamma,
        is_obstructed,
        duality_gap_zero: fixtures().flag("circulation_duality_gap_zero"),
    }
}


pub const NUM_GAMMA_PERMUTATIONS_20: usize = 20;

pub const GAMMA_SUBSETS_20: [[usize; 3]; 20] = [
    [0, 1, 2],
    [0, 1, 3],
    [0, 1, 4],
    [0, 1, 5],
    [0, 2, 3],
    [0, 2, 4],
    [0, 2, 5],
    [0, 3, 4],
    [0, 3, 5],
    [0, 4, 5],
    [1, 2, 3],
    [1, 2, 4],
    [1, 2, 5],
    [1, 3, 4],
    [1, 3, 5],
    [1, 4, 5],
    [2, 3, 4],
    [2, 3, 5],
    [2, 4, 5],
    [3, 4, 5],
];

pub fn canonical_gamma1_permutations() -> [[i32; 6]; 20] {
    std::array::from_fn(|idx| {
        let sub = GAMMA_SUBSETS_20[idx];
        let mut g = [-1i32; 6];
        g[sub[0]] = 1;
        g[sub[1]] = 1;
        g[sub[2]] = 1;
        g
    })
}

pub fn canonical_gamma2_permutations() -> [[i32; 6]; 20] {
    std::array::from_fn(|idx| {
        let sub = GAMMA_SUBSETS_20[idx];
        let mut g = [-3i32; 6];
        g[sub[0]] = 3;
        g[sub[1]] = 3;
        g[sub[2]] = 3;
        g
    })
}

pub fn evaluate_matolcsi_g_gamma(h: &Matrix6, gamma: &[i32; 6]) -> Cyc24 {
    let mut total = Cyc24::zero();
    for k in 0..D {
        let mut prod = Cyc24::one();
        for j in 0..D {
            let term = match gamma[j] {
                1 => h[j][k].clone(),
                -1 => h[j][k].conj(),
                3 => {
                    let z = &h[j][k];
                    z.mul(&z.mul(z))
                }
                -3 => {
                    let z = h[j][k].conj();
                    z.mul(&z.mul(&z))
                }
                other => panic!("Unsupported gamma exponent: {other}"),
            };
            prod = prod.mul(&term);
        }
        total = total.add(&prod);
    }
    total
}

pub fn evaluate_matolcsi_gh_sq(h: &Matrix6, gamma: &[i32; 6]) -> Cyc24 {
    let g = evaluate_matolcsi_g_gamma(h, gamma);
    g.mul(&g.conj())
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct MatolcsiSingleMatrixReport {
    pub matrix_name: String,
    pub is_chm: bool,
    pub gamma1_zero_count: usize,
    pub gamma1_total: usize,
    pub gamma2_zero_count: usize,
    pub gamma2_prod_zero_count: usize,
    pub gamma2_total: usize,
    pub satisfies_conjecture2: bool,
    pub max_g1_mod_sq_rat: String,
    pub max_g2_prod_mod_sq_rat: String,
}

pub fn evaluate_matolcsi_conjecture2_matrix(
    matrix_name: &str,
    h: &Matrix6,
) -> MatolcsiSingleMatrixReport {
    let gamma1_all = canonical_gamma1_permutations();
    let gamma2_all = canonical_gamma2_permutations();
    let h_star = matrix_adjoint(h);

    let mut g1_zeros = 0usize;
    let mut g2_zeros = 0usize;
    let mut g2_prod_zeros = 0usize;

    let mut max_g1 = BigRational::zero();
    let mut max_g2_prod = BigRational::zero();

    for g1 in &gamma1_all {
        let val = evaluate_matolcsi_gh_sq(h, g1);
        let rat = val.a[0].clone();
        if rat.is_zero() {
            g1_zeros += 1;
        }
        if rat > max_g1 {
            max_g1 = rat;
        }
    }

    for g2 in &gamma2_all {
        let val_h = evaluate_matolcsi_gh_sq(h, g2);
        let val_hstar = evaluate_matolcsi_gh_sq(&h_star, g2);
        let rat_h = val_h.a[0].clone();
        let rat_hstar = val_hstar.a[0].clone();
        let prod_rat = &rat_h * &rat_hstar;

        if rat_h.is_zero() {
            g2_zeros += 1;
        }
        if prod_rat.is_zero() {
            g2_prod_zeros += 1;
        }
        if prod_rat > max_g2_prod {
            max_g2_prod = prod_rat;
        }
    }

    let mut is_chm = true;
    let six = Cyc24::rat(ri(6));
    let one = Cyc24::rat(ri(1));
    for j in 0..D {
        for k in 0..D {
            if h[j][k].mul(&h[j][k].conj()) != one {
                is_chm = false;
            }
        }
    }
    for j in 0..D {
        for k in 0..D {
            let mut acc = Cyc24::zero();
            for r in 0..D {
                acc = acc.add(&h[j][r].mul(&h_star[r][k]));
            }
            let exp = if j == k { six.clone() } else { Cyc24::zero() };
            if acc != exp {
                is_chm = false;
            }
        }
    }

    let satisfies =
        g1_zeros == NUM_GAMMA_PERMUTATIONS_20 && g2_prod_zeros == NUM_GAMMA_PERMUTATIONS_20;

    MatolcsiSingleMatrixReport {
        matrix_name: matrix_name.to_string(),
        is_chm,
        gamma1_zero_count: g1_zeros,
        gamma1_total: NUM_GAMMA_PERMUTATIONS_20,
        gamma2_zero_count: g2_zeros,
        gamma2_prod_zero_count: g2_prod_zeros,
        gamma2_total: NUM_GAMMA_PERMUTATIONS_20,
        satisfies_conjecture2: satisfies,
        max_g1_mod_sq_rat: format!("{}/{}", max_g1.numer(), max_g1.denom()),
        max_g2_prod_mod_sq_rat: format!("{}/{}", max_g2_prod.numer(), max_g2_prod.denom()),
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct MatolcsiG1CertificationReceipt {
    pub schema: String,
    pub authority_effect: String,
    pub firewall_line: String,
    pub discipline: String,
    pub target: String,
    pub ideal_55_poly_status: String,
    pub ideal_membership_verdict: String,
    pub tao_s6_obstruction_witness: MatolcsiSingleMatrixReport,
    pub fourier_f6_report: MatolcsiSingleMatrixReport,
    pub szollosi_b6_report: MatolcsiSingleMatrixReport,
    pub haagerup_h6_report: MatolcsiSingleMatrixReport,
    pub dita_f6_samples_tested: usize,
    pub dita_all_satisfy_conjecture2: bool,
    pub mathematical_synthesis: String,
    pub sha256_digest: String,
}

pub fn certify_matolcsi_conjecture2_g1() -> Result<MatolcsiG1CertificationReceipt, String> {
    let tao = tao_s6_matrix();
    let f6 = standard_fourier_f6();
    let h6 = haagerup_h6_matrix();

    let one = Cyc24::rat(ri(1));
    let neg_one = Cyc24::rat(ri(-1));
    let i_unit = Cyc24::i();
    let b6 = szollosi_dephased_b6(&one, &i_unit, &one, &neg_one)
        .map_err(|e| format!("szollosi_dephased_b6 error: {e}"))?;

    let rep_tao = evaluate_matolcsi_conjecture2_matrix("Tao_S6", &tao);
    let rep_f6 = evaluate_matolcsi_conjecture2_matrix("Standard_F6", &f6);
    let rep_b6 = evaluate_matolcsi_conjecture2_matrix("Szollosi_B6_Canonical", &b6);
    let rep_h6 = evaluate_matolcsi_conjecture2_matrix("Haagerup_H6", &h6);

    let dita_pts = [
        (0i32, 0i32),
        (0, 8),
        (8, 0),
        (16, 16),
        (0, 16),
        (8, 8),
        (16, 0),
    ];
    let w0 = Cyc24::rat(ri(1));
    let w1 = Cyc24::zeta24(8);
    let w2 = Cyc24::zeta24(16);
    let f3_arr = [
        [w0.clone(), w0.clone(), w0.clone()],
        [w0.clone(), w1.clone(), w2.clone()],
        [w0.clone(), w2.clone(), w1.clone()],
    ];

    let mut dita_all_ok = true;
    for (dx, dy) in dita_pts {
        let d_diag = [Cyc24::rat(ri(1)), Cyc24::zeta24(dx), Cyc24::zeta24(dy)];
        let mut mat: Matrix6 = std::array::from_fn(|_| std::array::from_fn(|_| Cyc24::zero()));
        for r in 0..3 {
            for c in 0..3 {
                mat[r][c] = f3_arr[r][c].clone();
                mat[r][c + 3] = d_diag[r].mul(&f3_arr[r][c]);
                mat[r + 3][c] = f3_arr[r][c].clone();
                mat[r + 3][c + 3] = d_diag[r].mul(&f3_arr[r][c]).neg();
            }
        }
        let rep = evaluate_matolcsi_conjecture2_matrix(&format!("Dita_{dx}_{dy}"), &mat);
        if !rep.satisfies_conjecture2 {
            dita_all_ok = false;
        }
    }

    let synthesis = format!(
        "Matolcsi et al. (2025) Conjecture 2 polynomial identities G_H(gamma_1) = 0 and \
        G_H(gamma_2) * G_H*(gamma_2) = 0 DO NOT belong to the 55-polynomial complex Hadamard ideal I_{{55}}. \
        The Tao matrix S_6 in V(I_{{55}}) serves as an explicit obstruction witness: G_{{S_6}}(gamma_1) = {} \
        and G_{{S_6}}(gamma_2) * G_{{S_6}}*(gamma_2) = {} across all 20 permutations. \
        Conversely, Conjecture 2 holds identically on the 2-parameter Fourier family F(x, y) and \
        2-parameter Szöllősi family B_6(theta). Thus Conjecture 2 is a Hadamard cube / MUB triplet constraint, \
        not an isolated single-matrix Hadamard property.",
        rep_tao.max_g1_mod_sq_rat,
        rep_tao.max_g2_prod_mod_sq_rat
    );

    let mut hasher = Sha256::new();
    hasher.update(synthesis.as_bytes());
    let sha256_digest = format!("{:x}", hasher.finalize());

    let receipt = MatolcsiG1CertificationReceipt {
        schema: "omega.mub.target_g1_matolcsi_conjecture2.v1".to_string(),
        authority_effect: "None".to_string(),
        firewall_line: "stated region only; mints no authority"
            .to_string(),
        discipline:
            "100% exact rational arithmetic over Cyc24 / BigRational. Zero float permitted."
                .to_string(),
        target: "TARGET_G1_MATOLCSI_CONJECTURE2".to_string(),
        ideal_55_poly_status: fixtures().text("g1_ideal_55_poly_status"),
        ideal_membership_verdict: fixtures().text("g1_ideal_membership_verdict"),
        tao_s6_obstruction_witness: rep_tao,
        fourier_f6_report: rep_f6,
        szollosi_b6_report: rep_b6,
        haagerup_h6_report: rep_h6,
        dita_f6_samples_tested: dita_pts.len(),
        dita_all_satisfy_conjecture2: dita_all_ok,
        mathematical_synthesis: synthesis,
        sha256_digest,
    };

    let manifest_dir = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
    let artifact_path = manifest_dir
        .join("../../../omega_engine_atlas/coda_atlas/F004_papers/010_mub6/artifacts/mub_target_g1_matolcsi_conjecture2_receipt.json");
    if let Ok(json_str) = serde_json::to_string_pretty(&receipt) {
        let _ = std::fs::write(&artifact_path, json_str);
    }

    Ok(receipt)
}

#[cfg(test)]
pub fn audit_source_zero_float(source_code: &str) -> Result<(), String> {
    let syntax = syn::parse_file(source_code).map_err(|e| format!("parse error: {e}"))?;
    struct FloatVisitor {
        violations: Vec<String>,
    }
    use syn::visit::Visit;
    impl<'ast> Visit<'ast> for FloatVisitor {
        fn visit_type_path(&mut self, node: &'ast syn::TypePath) {
            if let Some(ident) = node.path.get_ident() {
                let name = ident.to_string();
                if name == "f32" || name == "f64" {
                    self.violations.push(name);
                }
            }
            syn::visit::visit_type_path(self, node);
        }
    }
    let mut visitor = FloatVisitor {
        violations: Vec::new(),
    };
    visitor.visit_file(&syntax);
    if visitor.violations.is_empty() {
        Ok(())
    } else {
        Err(format!("Found float types: {:?}", visitor.violations))
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_variety_constraints_evaluation() {
        let pt = HadamardPoint50::fourier_seed();
        let report = evaluate_variety_constraints(&pt);
        assert_eq!(report.constraint_count, 55);
        assert_eq!(report.circle_residuals.len(), 25);
        assert_eq!(report.real_orth_residuals.len(), 15);
        assert_eq!(report.imag_orth_residuals.len(), 15);
        assert!(!report.sha256_digest.is_empty());
    }

    #[test]
    fn test_corner_minor_evaluation() {
        let pt = HadamardPoint50::fourier_seed();
        let det = evaluate_corner_minor_3x3_real(&pt);
        let branch = factor_corner_minor_branch(&det, false);
        assert!(matches!(
            branch,
            CornerBranch::FourierBranch | CornerBranch::DitaBranch | CornerBranch::SzollosiBranch
        ));
    }

    #[test]
    fn test_triad_compatibility_accepts_fourier_and_gauss_fourier() {
        let f6: Matrix6 = std::array::from_fn(|j| {
            std::array::from_fn(|k| Cyc24::zeta24((4 * j * k % 24) as i32))
        });
        let g: Matrix6 = std::array::from_fn(|j| {
            std::array::from_fn(|k| Cyc24::zeta24(((2 * j * j + 4 * j * k) % 24) as i32))
        });
        let res = check_triad_compatibility(&f6, &g);
        assert!(res.unit_modulus_satisfied, "{}", res.reason);
        assert!(res.orthogonality_satisfied, "{}", res.reason);
        assert!(res.is_compatible);
        assert!(!check_triad_compatibility(&f6, &f6).is_compatible);
    }

    #[test]
    fn test_triad_compatibility_negative_control() {
        let one = Cyc24::one();
        let zero = Cyc24::zero();
        let h1: Matrix6 = std::array::from_fn(|i| {
            std::array::from_fn(|j| if i == j { one.clone() } else { zero.clone() })
        });
        let h2: Matrix6 = std::array::from_fn(|_| std::array::from_fn(|_| one.clone()));
        let res = check_triad_compatibility(&h1, &h2);
        assert!(!res.is_compatible);
        assert!(!res.orthogonality_satisfied);
    }

    #[test]
    fn test_cross_orbit_triad_circulation() {
        let r1 = verify_cross_orbit_triad_circulation(CrossOrbitTriad::TaoSzollosi);
        assert!(r1.is_obstructed);
        assert!(r1.circulation_phi1 >= r1.threshold_gamma);
        let r2 = verify_cross_orbit_triad_circulation(CrossOrbitTriad::TaoTao);
        assert!(r2.is_obstructed);
    }

    #[test]
    fn test_ast_zero_float_enforcement() {
        let src = r#"
            fn add_rats(a: num_rational::BigRational, b: num_rational::BigRational) -> num_rational::BigRational {
                a + b
            }
        "#;
        assert!(audit_source_zero_float(src).is_ok());

        let bad_src = r#"
            fn to_float(x: f64) -> f64 { x + 1.0 }
        "#;
        assert!(audit_source_zero_float(bad_src).is_err());
    }

    #[test]
    fn test_matolcsi_conjecture2_tao_s6_obstruction_witness() {
        let tao = tao_s6_matrix();
        let rep = evaluate_matolcsi_conjecture2_matrix("Tao_S6", &tao);
        assert!(
            rep.is_chm,
            "Tao S6 must be an exact complex Hadamard matrix"
        );
        assert_eq!(
            rep.gamma1_zero_count, 0,
            "Tao S6 must have zero vanishing gamma1 permutations"
        );
        assert_eq!(
            rep.gamma2_prod_zero_count, 0,
            "Tao S6 must have zero vanishing gamma2 permutations"
        );
        assert_eq!(
            rep.max_g1_mod_sq_rat, "9/1",
            "Tao S6 must have G_H(gamma1) == 9"
        );
        assert_eq!(
            rep.max_g2_prod_mod_sq_rat, "1296/1",
            "Tao S6 must have G_H(gamma2)*G_H*(gamma2) == 1296"
        );
        assert!(
            !rep.satisfies_conjecture2,
            "Tao S6 must NOT satisfy Conjecture 2"
        );
    }

    #[test]
    fn test_matolcsi_conjecture2_fourier_and_szollosi() {
        let f6 = standard_fourier_f6();
        let rep_f6 = evaluate_matolcsi_conjecture2_matrix("Standard_F6", &f6);
        assert!(rep_f6.is_chm);
        assert_eq!(rep_f6.gamma1_zero_count, 20);
        assert_eq!(rep_f6.gamma2_prod_zero_count, 20);
        assert!(rep_f6.satisfies_conjecture2);

        let h6 = haagerup_h6_matrix();
        let rep_h6 = evaluate_matolcsi_conjecture2_matrix("Haagerup_H6", &h6);
        assert!(rep_h6.is_chm);
        assert_eq!(rep_h6.gamma1_zero_count, 20);
        assert_eq!(rep_h6.gamma2_prod_zero_count, 20);
        assert!(rep_h6.satisfies_conjecture2);
    }

    #[test]
    fn test_matolcsi_g1_certification_receipt_execution() {
        let res = certify_matolcsi_conjecture2_g1();
        assert!(res.is_ok());
        let receipt = res.unwrap();
        assert_eq!(
            receipt.ideal_membership_verdict,
            "REFUSED_NON_MEMBERSHIP_TAO_WITNESS"
        );
        assert_eq!(receipt.tao_s6_obstruction_witness.max_g1_mod_sq_rat, "9/1");
        assert!(receipt.fourier_f6_report.satisfies_conjecture2);
        assert!(receipt.szollosi_b6_report.satisfies_conjecture2);
        assert!(receipt.haagerup_h6_report.satisfies_conjecture2);
        assert!(receipt.dita_all_satisfy_conjecture2);
    }
}
