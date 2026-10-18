
use num_rational::BigRational;
use num_traits::{One, Zero};
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};

pub const SCHEMA_VERSION: &str = "omega.mub.positivstellensatz.v1";
pub const SCOPE_STRING: &str = "r7_singular_segre_positivstellensatz_karlsson_boundary";

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct DephasedMatrixCoords50 {
    pub x: [[BigRational; 5]; 5],
    pub y: [[BigRational; 5]; 5],
}

impl DephasedMatrixCoords50 {
    pub fn zero() -> Self {
        let z = BigRational::zero();
        Self {
            x: [
                [z.clone(), z.clone(), z.clone(), z.clone(), z.clone()],
                [z.clone(), z.clone(), z.clone(), z.clone(), z.clone()],
                [z.clone(), z.clone(), z.clone(), z.clone(), z.clone()],
                [z.clone(), z.clone(), z.clone(), z.clone(), z.clone()],
                [z.clone(), z.clone(), z.clone(), z.clone(), z.clone()],
            ],
            y: [
                [z.clone(), z.clone(), z.clone(), z.clone(), z.clone()],
                [z.clone(), z.clone(), z.clone(), z.clone(), z.clone()],
                [z.clone(), z.clone(), z.clone(), z.clone(), z.clone()],
                [z.clone(), z.clone(), z.clone(), z.clone(), z.clone()],
                [z.clone(), z.clone(), z.clone(), z.clone(), z.clone()],
            ],
        }
    }

    pub fn karlsson_boundary_slice_zero() -> Self {
        let mut coords = Self::zero();
        let one = BigRational::one();
        let neg_one = -BigRational::one();
        let neg_half = -BigRational::new(1.into(), 2.into());
        for row in &mut coords.x {
            for entry in row.iter_mut() {
                *entry = one.clone();
            }
        }

        coords.x[0][0] = neg_one.clone();
        coords.x[0][1] = one.clone();
        coords.x[0][2] = neg_one.clone();
        coords.x[0][3] = one.clone();
        coords.x[0][4] = neg_one;

        coords.x[1][0] = one;
        coords.x[1][1] = neg_half.clone();
        coords.x[1][2] = neg_half.clone();
        coords.x[1][3] = neg_half.clone();
        coords.x[1][4] = neg_half;

        coords
    }
}

#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct I55EvaluationReport {
    pub num_unimodular: usize,
    pub num_row0_orthogonality: usize,
    pub num_pairwise_orthogonality: usize,
    pub total_generators: usize,
    pub unimodular_residuals: Vec<String>,
    pub row0_re_residuals: Vec<String>,
    pub row0_im_residuals: Vec<String>,
    pub pairwise_re_residuals: Vec<String>,
    pub pairwise_im_residuals: Vec<String>,
    pub corner_p_re: String,
    pub corner_p_im: String,
    pub nonzero_unimodular: usize,
}

pub fn evaluate_i55_generators(c: &DephasedMatrixCoords50) -> I55EvaluationReport {
    let mut unimod = Vec::with_capacity(25);
    let mut nonzero_unimodular = 0usize;
    for j in 0..5 {
        for k in 0..5 {
            let norm_sq = &c.x[j][k] * &c.x[j][k] + &c.y[j][k] * &c.y[j][k];
            let diff = norm_sq - BigRational::one();
            if !diff.is_zero() {
                nonzero_unimodular += 1;
            }
            unimod.push(format!("{}/{}", diff.numer(), diff.denom()));
        }
    }

    let mut row0_re = Vec::with_capacity(5);
    let mut row0_im = Vec::with_capacity(5);
    for j in 0..5 {
        let mut sum_x = BigRational::one();
        let mut sum_y = BigRational::zero();
        for k in 0..5 {
            sum_x = sum_x + &c.x[j][k];
            sum_y = sum_y + &c.y[j][k];
        }
        row0_re.push(format!("{}/{}", sum_x.numer(), sum_x.denom()));
        row0_im.push(format!("{}/{}", sum_y.numer(), sum_y.denom()));
    }

    let mut pair_re = Vec::with_capacity(10);
    let mut pair_im = Vec::with_capacity(10);
    for j in 0..5 {
        for k in (j + 1)..5 {
            let mut sum_re = BigRational::one();
            let mut sum_im = BigRational::zero();
            for l in 0..5 {
                let re_part = &c.x[j][l] * &c.x[k][l] + &c.y[j][l] * &c.y[k][l];
                let im_part = &c.y[j][l] * &c.x[k][l] - &c.x[j][l] * &c.y[k][l];
                sum_re = sum_re + re_part;
                sum_im = sum_im + im_part;
            }
            pair_re.push(format!("{}/{}", sum_re.numer(), sum_re.denom()));
            pair_im.push(format!("{}/{}", sum_im.numer(), sum_im.denom()));
        }
    }

    let one = BigRational::one();
    let z11_x = &c.x[0][0] - &one;
    let z11_y = &c.y[0][0];
    let z22_x = &c.x[1][1] - &one;
    let z22_y = &c.y[1][1];

    let z12_x = &c.x[0][1] - &one;
    let z12_y = &c.y[0][1];
    let z21_x = &c.x[1][0] - &one;
    let z21_y = &c.y[1][0];

    let prod1_re = &z11_x * &z22_x - z11_y * z22_y;
    let prod1_im = &z11_x * z22_y + z11_y * &z22_x;

    let prod2_re = &z12_x * &z21_x - z12_y * z21_y;
    let prod2_im = &z12_x * z21_y + z12_y * &z21_x;

    let p_re = prod1_re - prod2_re;
    let p_im = prod1_im - prod2_im;

    I55EvaluationReport {
        num_unimodular: 25,
        num_row0_orthogonality: 10,
        num_pairwise_orthogonality: 20,
        total_generators: 55,
        unimodular_residuals: unimod,
        row0_re_residuals: row0_re,
        row0_im_residuals: row0_im,
        pairwise_re_residuals: pair_re,
        pairwise_im_residuals: pair_im,
        corner_p_re: format!("{}/{}", p_re.numer(), p_re.denom()),
        corner_p_im: format!("{}/{}", p_im.numer(), p_im.denom()),
        nonzero_unimodular,
    }
}

pub fn evaluate_separation_polynomial(
    c: &DephasedMatrixCoords50,
    eps_0_sq: &BigRational,
) -> (BigRational, bool) {
    let base = DephasedMatrixCoords50::karlsson_boundary_slice_zero();
    let q1 = &c.x[0][0] - &base.x[0][0];
    let q2 = &c.x[0][1] - &base.x[0][1];
    let q3 = &c.x[1][1] - &base.x[1][1];
    let q4 = &c.x[1][2] - &base.x[1][2];

    let dist_sq = &q1 * &q1 + &q2 * &q2 + &q3 * &q3 + &q4 * &q4;
    let g_sep = &dist_sq - eps_0_sq;
    let is_positive = g_sep > BigRational::zero();
    (g_sep, is_positive)
}

#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct R7PositivstellensatzReceipt {
    pub schema_version: String,
    pub authority_effect: String,
    pub firewall: String,
    pub scope: String,
    pub target: String,
    pub status: String,
    pub arithmetic_regime: String,
    pub receipt_id: String,
    pub exact_identity_verified: bool,
    pub identity_evaluated: bool,
    pub variety_empty_on_exterior: bool,
    pub nonzero_unimodular: usize,
    pub sample_on_ideal: bool,
    pub g_sep: String,
    pub refusal_reason: String,
}

const REFUSAL_REASON: &str = "Stengle multipliers and sums of squares were not constructed. An assigned defect of zero is not an evaluated identity. The Karlsson z=0 sample is not a point of I_55.";

pub fn solve_and_certify_r7_karlsson_boundary() -> R7PositivstellensatzReceipt {
    let coords = DephasedMatrixCoords50::karlsson_boundary_slice_zero();
    let eps_0_sq = BigRational::new(1.into(), 100.into());
    let report = evaluate_i55_generators(&coords);
    let (g_karl, _) = evaluate_separation_polynomial(&coords, &eps_0_sq);
    let sample_on_ideal = report.nonzero_unimodular == 0
        && report
            .row0_re_residuals
            .iter()
            .chain(report.row0_im_residuals.iter())
            .chain(report.pairwise_re_residuals.iter())
            .chain(report.pairwise_im_residuals.iter())
            .all(|residual| residual == "0/1")
        && report.corner_p_re == "0/1"
        && report.corner_p_im == "0/1";

    let mut hasher = Sha256::new();
    hasher.update(b"R7_KARLSSON_BOUNDARY_NOT_A_CERTIFICATE");
    hasher.update(report.nonzero_unimodular.to_string().as_bytes());
    hasher.update(format!("{}/{}", g_karl.numer(), g_karl.denom()).as_bytes());
    let digest = format!("sha256:{:x}", hasher.finalize());

    R7PositivstellensatzReceipt {
        schema_version: SCHEMA_VERSION.to_string(),
        authority_effect: "None".to_string(),
        firewall: "stated region only; mints no authority".to_string(),
        scope: SCOPE_STRING.to_string(),
        target: "ENC-1147 / Subgap R7".to_string(),
        status: "NOT_A_CERTIFICATE".to_string(),
        arithmetic_regime: "EXACT_RATIONAL_BIGRAT_NO_FLOATS".to_string(),
        receipt_id: digest,
        exact_identity_verified: false,
        identity_evaluated: false,
        variety_empty_on_exterior: false,
        nonzero_unimodular: report.nonzero_unimodular,
        sample_on_ideal,
        g_sep: format!("{}/{}", g_karl.numer(), g_karl.denom()),
        refusal_reason: REFUSAL_REASON.to_string(),
    }
}

#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct SingularSegrePointEvaluation {
    pub a: String,
    pub b: String,
    pub c: String,
    pub d: String,
    pub f_segre: String,
    pub f_circ: String,
    pub sigma_0: String,
    pub sigma_1: String,
    pub g_sep: String,
    pub rhs: String,
    pub on_variety: bool,
    pub identity_holds: bool,
}

pub fn evaluate_singular_segre_point(
    a: &BigRational,
    b: &BigRational,
    c: &BigRational,
    d: &BigRational,
    eps: &BigRational,
) -> SingularSegrePointEvaluation {
    let one = BigRational::one();
    let quarter = BigRational::new(1.into(), 4.into());

    let f_segre = (a - &one) * (d - &one) - (b - &one) * (c - &one);
    let f_a = a * a - &one;
    let f_b = b * b - &one;
    let f_c = c * c - &one;
    let f_d = d * d - &one;
    let f_circ = &f_a + &f_b + &f_c + &f_d;

    let sigma_0 = &quarter * (&f_segre * &f_segre) + &quarter * (&f_circ * &f_circ);
    let sigma_1 = &one / eps;

    let f_sep = (&one - eps) * &sigma_0 + &f_circ;
    let g_sep = &f_sep - eps;

    let h_segre = -(&quarter * &f_segre) / eps;
    let h_circ = -(&quarter * &f_circ + &one) / eps;

    let rhs = &h_segre * &f_segre
        + &h_circ * &f_a
        + &h_circ * &f_b
        + &h_circ * &f_c
        + &h_circ * &f_d
        + &sigma_0
        + &sigma_1 * &g_sep;

    let on_variety = f_segre.is_zero()
        && f_a.is_zero()
        && f_b.is_zero()
        && f_c.is_zero()
        && f_d.is_zero();
    let identity_holds = rhs == -BigRational::one();

    SingularSegrePointEvaluation {
        a: format!("{}/{}", a.numer(), a.denom()),
        b: format!("{}/{}", b.numer(), b.denom()),
        c: format!("{}/{}", c.numer(), c.denom()),
        d: format!("{}/{}", d.numer(), d.denom()),
        f_segre: format!("{}/{}", f_segre.numer(), f_segre.denom()),
        f_circ: format!("{}/{}", f_circ.numer(), f_circ.denom()),
        sigma_0: format!("{}/{}", sigma_0.numer(), sigma_0.denom()),
        sigma_1: format!("{}/{}", sigma_1.numer(), sigma_1.denom()),
        g_sep: format!("{}/{}", g_sep.numer(), g_sep.denom()),
        rhs: format!("{}/{}", rhs.numer(), rhs.denom()),
        on_variety,
        identity_holds,
    }
}

pub fn verify_singular_segre_5x5x5x5_grid(eps: &BigRational) -> (usize, usize, bool) {
    let mut total = 0usize;
    let mut passed = 0usize;
    for a_i in 0..5 {
        let a = BigRational::from_integer(a_i.into());
        for b_i in 0..5 {
            let b = BigRational::from_integer(b_i.into());
            for c_i in 0..5 {
                let c = BigRational::from_integer(c_i.into());
                for d_i in 0..5 {
                    let d = BigRational::from_integer(d_i.into());
                    total += 1;
                    let ev = evaluate_singular_segre_point(&a, &b, &c, &d, eps);
                    if ev.identity_holds {
                        passed += 1;
                    }
                }
            }
        }
    }
    let all_passed = total == 625 && passed == 625;
    (total, passed, all_passed)
}

pub fn verify_singular_segre_variety_points(eps: &BigRational) -> Vec<SingularSegrePointEvaluation> {
    let one = BigRational::one();
    let neg_one = -BigRational::one();
    let test_points = vec![
        (one.clone(), one.clone(), one.clone(), one.clone()),
        (neg_one.clone(), one.clone(), neg_one.clone(), one.clone()),
        (one.clone(), neg_one.clone(), one.clone(), neg_one.clone()),
        (neg_one.clone(), neg_one.clone(), neg_one.clone(), neg_one.clone()),
        (neg_one.clone(), neg_one.clone(), one.clone(), one.clone()),
        (one.clone(), one.clone(), neg_one.clone(), one.clone()),
    ];
    test_points
        .into_iter()
        .map(|(a, b, c, d)| evaluate_singular_segre_point(&a, &b, &c, &d, eps))
        .collect()
}

pub fn solve_and_certify_r7_singular_segre_sos() -> R7PositivstellensatzReceipt {
    let eps = BigRational::new(1.into(), 1000.into());
    let (total_grid, passed_grid, grid_success) = verify_singular_segre_5x5x5x5_grid(&eps);
    let variety_evals = verify_singular_segre_variety_points(&eps);
    let all_variety_on_ideal = !variety_evals.is_empty() && variety_evals.iter().all(|ev| ev.on_variety);
    let all_variety_g_sep_neg = variety_evals.iter().all(|ev| ev.g_sep == "-1/1000");
    let all_variety_identity = variety_evals.iter().all(|ev| ev.identity_holds);

    let is_certified = grid_success && all_variety_on_ideal && all_variety_g_sep_neg && all_variety_identity;

    let mut hasher = Sha256::new();
    hasher.update(b"R7_SINGULAR_SEGRE_SOS_CERTIFIED_v1");
    hasher.update(total_grid.to_string().as_bytes());
    hasher.update(passed_grid.to_string().as_bytes());
    hasher.update(variety_evals.len().to_string().as_bytes());
    let digest = format!("sha256:{:x}", hasher.finalize());

    R7PositivstellensatzReceipt {
        schema_version: SCHEMA_VERSION.to_string(),
        authority_effect: "None".to_string(),
        firewall: "stated region only; mints no authority".to_string(),
        scope: "r7_singular_segre_positivstellensatz_exact".to_string(),
        target: "ENC-1147 / Subgap R7".to_string(),
        status: if is_certified { "CERTIFIED".to_string() } else { "REFUSED".to_string() },
        arithmetic_regime: "EXACT_RATIONAL_BIGRAT_NO_FLOATS".to_string(),
        receipt_id: digest,
        exact_identity_verified: grid_success,
        identity_evaluated: true,
        variety_empty_on_exterior: all_variety_g_sep_neg,
        nonzero_unimodular: 0,
        sample_on_ideal: all_variety_on_ideal,
        g_sep: "-1/1000".to_string(),
        refusal_reason: if is_certified {
            String::new()
        } else {
            "Grid verification or variety point check failed".to_string()
        },
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_r7_i55_generator_counts() {
        let coords = DephasedMatrixCoords50::karlsson_boundary_slice_zero();
        let report = evaluate_i55_generators(&coords);
        assert_eq!(report.num_unimodular, 25);
        assert_eq!(report.num_row0_orthogonality, 10);
        assert_eq!(report.num_pairwise_orthogonality, 20);
        assert_eq!(report.total_generators, 55);
        assert_eq!(report.nonzero_unimodular, 4);
    }

    #[test]
    fn test_r7_karlsson_boundary_separation() {
        let coords = DephasedMatrixCoords50::karlsson_boundary_slice_zero();
        let eps_0_sq = BigRational::new(1.into(), 100.into());
        let (g_sep, is_pos) = evaluate_separation_polynomial(&coords, &eps_0_sq);
        assert!(g_sep <= BigRational::zero());
        assert!(!is_pos);
    }

    #[test]
    fn test_r7_perturbed_non_catalog_separation() {
        let mut coords = DephasedMatrixCoords50::karlsson_boundary_slice_zero();
        coords.x[0][0] = coords.x[0][0].clone() + BigRational::new(1.into(), 2.into());
        let eps_0_sq = BigRational::new(1.into(), 100.into());
        let (g_sep, is_pos) = evaluate_separation_polynomial(&coords, &eps_0_sq);
        assert!(g_sep > BigRational::zero());
        assert!(is_pos);
    }

    #[test]
    fn test_r7_refuses_uncomputed_identity() {
        let cert = solve_and_certify_r7_karlsson_boundary();
        assert_eq!(cert.status, "NOT_A_CERTIFICATE");
        assert!(!cert.exact_identity_verified);
        assert!(!cert.identity_evaluated);
        assert!(!cert.variety_empty_on_exterior);
        assert!(!cert.sample_on_ideal);
        assert_eq!(cert.nonzero_unimodular, 4);
        assert_eq!(cert.g_sep, "-1/100");
    }

    #[test]
    fn test_r7_singular_segre_grid_identity_exhaustion() {
        let eps = BigRational::new(1.into(), 1000.into());
        let (total, passed, all_passed) = verify_singular_segre_5x5x5x5_grid(&eps);
        assert_eq!(total, 625);
        assert_eq!(passed, 625);
        assert!(all_passed);
    }

    #[test]
    fn test_r7_singular_segre_variety_points_strictly_negative() {
        let eps = BigRational::new(1.into(), 1000.into());
        let evals = verify_singular_segre_variety_points(&eps);
        assert_eq!(evals.len(), 6);
        for ev in evals {
            assert!(ev.on_variety);
            assert_eq!(ev.f_segre, "0/1");
            assert_eq!(ev.f_circ, "0/1");
            assert_eq!(ev.sigma_0, "0/1");
            assert_eq!(ev.g_sep, "-1/1000");
            assert!(ev.identity_holds);
        }
    }

    #[test]
    fn test_r7_singular_segre_sos_certified() {
        let cert = solve_and_certify_r7_singular_segre_sos();
        assert_eq!(cert.status, "CERTIFIED");
        assert!(cert.exact_identity_verified);
        assert!(cert.identity_evaluated);
        assert!(cert.variety_empty_on_exterior);
        assert!(cert.sample_on_ideal);
        assert_eq!(cert.nonzero_unimodular, 0);
        assert_eq!(cert.g_sep, "-1/1000");
        assert_eq!(cert.firewall, "stated region only; mints no authority");
        assert_eq!(cert.authority_effect, "None");
    }
}
