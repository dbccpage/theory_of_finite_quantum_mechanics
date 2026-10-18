//! Rational Taylor enclosure arithmetic for w(s)=2 exp(is)+exp(-2is).
//! This does not identify a CHM family or establish a MUB curvature bound.
//! Evidence: test_deltoid_cusp_asymptotics.rs. AuthorityEffect: None.

use num_rational::BigRational;
use num_traits::{One, Zero};
use serde::{Deserialize, Serialize};

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct TaylorLagrangeEnclosureReport {
    pub delta: String,
    pub polynomial_re_interval: [String; 2],
    pub polynomial_im_interval: [String; 2],
    pub lagrange_rem_re_bound: String,
    pub lagrange_rem_im_bound: String,
    pub total_re_interval: [String; 2],
    pub total_im_interval: [String; 2],
}

pub fn evaluate_taylor_lagrange_enclosure(
    delta: &BigRational,
) -> Result<TaylorLagrangeEnclosureReport, String> {
    // On [0,1], 3-3u+3u^2/4 decreases for u=s^2, while
    // s^3-s^5/4 increases. Outside this range endpoint evaluation
    // alone is not a valid enclosure method.
    if delta < &BigRational::zero() || delta > &BigRational::one() {
        return Err("Taylor enclosure requires 0 <= delta <= 1".into());
    }
    let q = |a: i64, b: i64| BigRational::new(a.into(), b.into());
    let d2 = delta * delta;
    let d3 = &d2 * delta;
    let d4 = &d2 * &d2;
    let d5 = &d4 * delta;
    let d6 = &d3 * &d3;
    let d7 = &d6 * delta;
    let re_hi = q(3, 1);
    let re_lo = &re_hi - q(3, 1) * d2 + q(3, 4) * d4;
    let im_hi = d3 - q(1, 4) * d5;
    let im_lo = -&im_hi;
    // Componentwise Lagrange majorants: (2+2^6)/6! and (2+2^7)/7!.
    let re_rem = q(11, 120) * d6;
    let im_rem = q(13, 504) * d7;
    Ok(TaylorLagrangeEnclosureReport {
        delta: delta.to_string(),
        polynomial_re_interval: [re_lo.to_string(), re_hi.to_string()],
        polynomial_im_interval: [im_lo.to_string(), im_hi.to_string()],
        lagrange_rem_re_bound: re_rem.to_string(),
        lagrange_rem_im_bound: im_rem.to_string(),
        total_re_interval: [
            (&re_lo - &re_rem).to_string(),
            (&re_hi + &re_rem).to_string(),
        ],
        total_im_interval: [
            (&im_lo - &im_rem).to_string(),
            (&im_hi + &im_rem).to_string(),
        ],
    })
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct DeltoidCuspAsymptoticsReport {
    pub schema_version: String,
    pub scope: String,
    pub authority_effect: String,
    pub firewall: String,
    pub taylor_lagrange_enclosure: TaylorLagrangeEnclosureReport,
    pub mub_curvature_bound_established: bool,
    pub missing_obligations: Vec<String>,
}

pub fn solve_deltoid_cusp_asymptotics() -> DeltoidCuspAsymptoticsReport {
    DeltoidCuspAsymptoticsReport {
        schema_version: "omega.mub.deltoid-taylor-model.v2".into(),
        scope: "scalar_hypocycloid_local_coordinate_enclosure_only".into(),
        authority_effect: "None".into(),
        firewall: "stated region only; mints no authority".into(),
        taylor_lagrange_enclosure: evaluate_taylor_lagrange_enclosure(&BigRational::new(
            1.into(),
            1000.into(),
        ))
        .unwrap(),
        mub_curvature_bound_established: false,
        missing_obligations: vec![
            "identify the intended CHM family and its cusp chart".into(),
            "bound the concrete curvature functional over a stated candidate domain".into(),
        ],
    }
}
