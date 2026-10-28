
use num_bigint::BigInt;
use num_rational::BigRational;
use num_traits::{One, Zero};
use serde::{Deserialize, Serialize};

use crate::native::exact::d6_exact_curvature_cochain::D;
use crate::native::exact::mub6_matrix6::Matrix6;
pub use crate::native::exact::mub6_matrix6::{
    cross_ratio_at, enumerate_225_submatrices, evaluate_all_225_cross_ratios, root24_exponent,
    Submatrix2Index, NUM_SUBMATRICES_225,
};
use engine_number_theory::cyclotomic::Cyc24;
use engine_number_theory::rational::ri;
use engine_number_theory::rational::rq;

pub const TAO_PHASES: [[i64; D]; D] = [
    [0, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 2, 2],
    [0, 1, 0, 2, 2, 1],
    [0, 1, 2, 0, 1, 2],
    [0, 2, 2, 1, 0, 1],
    [0, 2, 1, 2, 1, 0],
];

pub fn tao_s6_matrix() -> Matrix6 {
    let w0 = Cyc24::rat(ri(1));
    let w1 = Cyc24::zeta24(8);
    let w2 = Cyc24::zeta24(16);
    let w = [&w0, &w1, &w2];

    std::array::from_fn(|i| std::array::from_fn(|j| w[TAO_PHASES[i][j] as usize].clone()))
}

pub fn confluence_point_theta_star() -> [Cyc24; 5] {
    std::array::from_fn(|_| Cyc24::rat(ri(1)))
}

pub fn tao_chart_eval(u: &[Cyc24; 5]) -> Matrix6 {
    let s6 = tao_s6_matrix();
    let mut out = s6;
    for p in 0..5 {
        let idx = p + 1;
        out[idx][idx] = out[idx][idx].mul(&u[p]);
    }
    out
}

pub fn tao_chart_eval_discrete(exponents: &[i32; 5]) -> Matrix6 {
    let u: [Cyc24; 5] = std::array::from_fn(|p| Cyc24::zeta24(exponents[p]));
    tao_chart_eval(&u)
}

pub fn extract_cross_ratio_exponents(m: &Matrix6) -> Result<Vec<i64>, String> {
    let crs = evaluate_all_225_cross_ratios(m);
    let mut exponents = Vec::with_capacity(NUM_SUBMATRICES_225);
    for (idx, cr) in crs.iter().enumerate() {
        match root24_exponent(cr) {
            Some(e) => exponents.push(e),
            None => {
                return Err(format!(
                    "Cross-ratio at index {idx} is not an exact 24th root of unity"
                ))
            }
        }
    }
    Ok(exponents)
}

pub fn verify_confluence_evaluation() -> bool {
    let theta_star = confluence_point_theta_star();
    let phi_star = tao_chart_eval(&theta_star);
    let s6 = tao_s6_matrix();

    for i in 0..D {
        for j in 0..D {
            if phi_star[i][j] != s6[i][j] {
                return false;
            }
        }
    }
    true
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct TargetA6VerificationReport {
    pub schema_version: String,
    pub authority_effect: String,
    pub firewall: String,
    pub confluence_evaluated_identically: bool,
    pub total_submatrices: usize,
    pub exponents_match_receipt: bool,
    pub all_exponents_cubic_mod24: bool,
    pub no_exponent_minus_one: bool,
    pub no_submatrix_orthogonal: bool,
    pub neighborhood_certificate_valid: bool,
    pub neighborhood_radius: String,
    pub min_distance_to_minus_one: String,
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct RationalBox5D {
    pub radius: BigRational,
}

impl RationalBox5D {
    pub fn new(radius: BigRational) -> Self {
        assert!(
            radius > BigRational::zero(),
            "Radius must be strictly positive"
        );
        Self { radius }
    }
}

pub fn verify_local_rational_neighborhood_certificate(r: BigRational) -> (bool, BigRational) {
    let one = BigRational::one();
    let two = BigRational::from(BigInt::from(2));

    let max_pert = &two * &r + &r * &r;

    if max_pert < one {
        let min_dist = &one - &max_pert;
        (true, min_dist)
    } else {
        (false, BigRational::zero())
    }
}

pub fn solve_target_a6(expected_receipt_exponents: &[i64]) -> TargetA6VerificationReport {
    let confluence_ok = verify_confluence_evaluation();
    let s6 = tao_s6_matrix();
    let computed_exponents = extract_cross_ratio_exponents(&s6)
        .expect("All cross-ratios of S_6 must be exact 24th roots of unity");

    let match_receipt = computed_exponents == expected_receipt_exponents;
    let all_cubic = computed_exponents.iter().all(|e| *e % 8 == 0);
    let no_minus_one = computed_exponents.iter().all(|e| *e != 12);
    let no_ortho = no_minus_one;

    let r_cert = rq(1, 24);
    let (cert_valid, min_dist) = verify_local_rational_neighborhood_certificate(r_cert.clone());

    TargetA6VerificationReport {
        schema_version: "omega.mub.target-a6-tao-chart.v1".to_string(),
        authority_effect: "None".to_string(),
        firewall: "stated region only; mints no authority".to_string(),
        confluence_evaluated_identically: confluence_ok,
        total_submatrices: computed_exponents.len(),
        exponents_match_receipt: match_receipt,
        all_exponents_cubic_mod24: all_cubic,
        no_exponent_minus_one: no_minus_one,
        no_submatrix_orthogonal: no_ortho,
        neighborhood_certificate_valid: cert_valid,
        neighborhood_radius: r_cert.to_string(),
        min_distance_to_minus_one: min_dist.to_string(),
    }
}
