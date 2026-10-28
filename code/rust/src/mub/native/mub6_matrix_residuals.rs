
use num_rational::BigRational;
use num_traits::{Signed, Zero};

use super::mub6_continuous_chaining::{build_multi_anchor_covering, MultiAnchorCover};
use super::mub6_continuous_chaining::{t_max_multi_anchor, t_min_multi_anchor};
use crate::native::exact::mub6_constants::delta_certified;
use tfqm_number_theory::cyclotomic::Cyc24;
use tfqm_number_theory::rational::rq;

pub const NUM_ANCHORS_CANONICAL: usize = 250;
pub const MISSING_EVIDENCE: &str = "MissingProofObligation: parameter-bound Szollosi matrices, verified derivative enclosures, and common-gauge continuation evidence are required";

pub fn compute_matrix_residual(h: &[Vec<Cyc24>]) -> Result<Vec<Vec<Cyc24>>, String> {
    if h.len() != 6 || h.iter().any(|row| row.len() != 6) {
        return Err("Matrix must be 6x6".into());
    }
    let mut residual = vec![vec![Cyc24::zero(); 6]; 6];
    for i in 0..6 {
        for j in 0..6 {
            let mut value = Cyc24::zero();
            for k in 0..6 {
                value = value.add(&h[i][k].mul(&h[j][k].conj()));
            }
            residual[i][j] = value.sub(&Cyc24::rat(rq(if i == j { 6 } else { 0 }, 1)));
        }
    }
    Ok(residual)
}

fn require_parameter(t: &BigRational) -> Result<(), String> {
    if t < &t_min_multi_anchor() || t > &t_max_multi_anchor() {
        return Err("Parameter outside the declared interval".into());
    }
    Ok(())
}

pub fn compute_2circulant_residual_matrix(
    t: &BigRational,
) -> Result<(BigRational, BigRational), String> {
    require_parameter(t)?;
    Err(MISSING_EVIDENCE.into())
}

pub fn compute_algebraic_derivative_bound(t: &BigRational) -> Result<BigRational, String> {
    require_parameter(t)?;
    Err(MISSING_EVIDENCE.into())
}

pub fn verify_continuation_step(
    t1: &BigRational,
    d1: &BigRational,
    t2: &BigRational,
    d2: &BigRational,
) -> bool {
    d1 > &BigRational::zero() && d2 > &BigRational::zero() && (t2 - t1).abs() <= d1 + d2
}

pub fn build_interval_cover(num_anchors: usize) -> Result<MultiAnchorCover, String> {
    let cover = build_multi_anchor_covering(num_anchors, &delta_certified())
        .map_err(|error| error.to_string())?;
    cover.audit().map_err(|error| error.to_string())?;
    Ok(cover)
}

pub fn build_matrix_residual_verifier(num_anchors: usize) -> Result<(), String> {
    if num_anchors < 80 {
        return Err("Invalid anchor count".into());
    }
    Err(MISSING_EVIDENCE.into())
}
