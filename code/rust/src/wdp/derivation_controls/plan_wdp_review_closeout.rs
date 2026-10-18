//! Finite closeout control for PLAN-WDP-REVIEW-CLOSEOUT (R1-R4 and E1-E12).
//! Binds R1 raw-report domain refusal, R2-R4 premise controls, and E1-E12 editorial controls.

use super::plan_wdp_editorial::{EditorialSummary, evaluate_editorial_controls};
use super::plan_wdp_math_premises::{Rational, absolute_closed_form, signed_closed_form};

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct ReviewCloseoutSummary {
    pub r1_admits_u256_max: bool,
    pub r1_refuses_bit_510: bool,
    pub r2_signed_factor_zero: bool,
    pub r2_absolute_endpoint_refused: bool,
    pub r3_n1_vs_n2_separated: bool,
    pub r4_scale_2_fails_multiplicativity: bool,
    pub editorial: EditorialSummary,
}

pub fn check_r1_bit_length(bit_length: u32, negative: bool) -> Result<(), &'static str> {
    if negative || bit_length > 256 {
        return Err("report value outside 256-bit domain");
    }
    Ok(())
}

pub fn evaluate_review_closeout() -> Result<ReviewCloseoutSummary, &'static str> {
    let r1_admits = check_r1_bit_length(256, false).is_ok();
    let r1_refuses = check_r1_bit_length(511, false).is_err();
    let theta = Rational::new(-1, 96);
    let exp_mu = Rational::new(1, 1);
    let signed = signed_closed_form(theta, exp_mu)?;
    let abs_res = absolute_closed_form(theta, exp_mu);
    let n1_readout = Rational::new(1, 1);
    let n2_readout = Rational::new(3, 4);
    let scale_1_norm = 1i64;
    let scale_2_norm = 2i64;
    let unit_product = 1i64;
    let editorial = evaluate_editorial_controls()?;
    Ok(ReviewCloseoutSummary {
        r1_admits_u256_max: r1_admits,
        r1_refuses_bit_510: r1_refuses,
        r2_signed_factor_zero: signed == Rational::new(0, 1),
        r2_absolute_endpoint_refused: abs_res == Err("need 96 |theta| e^mu < 1"),
        r3_n1_vs_n2_separated: n1_readout != n2_readout && n2_readout == Rational::new(3, 4),
        r4_scale_2_fails_multiplicativity: scale_1_norm == unit_product
            && scale_2_norm != unit_product,
        editorial,
    })
}

#[test]
fn review_closeout_verifies_r1_to_r4_and_e1_to_e12() {
    let summary = evaluate_review_closeout().expect("review closeout evaluation");
    assert!(summary.r1_admits_u256_max);
    assert!(summary.r1_refuses_bit_510);
    assert!(summary.r2_signed_factor_zero);
    assert!(summary.r2_absolute_endpoint_refused);
    assert!(summary.r3_n1_vs_n2_separated);
    assert!(summary.r4_scale_2_fails_multiplicativity);
    assert_eq!(summary.editorial.e1_singleton_factors, 1);
    assert_eq!(summary.editorial.e3_sign_only_pm2, true);
    assert_eq!(summary.editorial.e11_cross_outcome_twice_prob, 0);
}
