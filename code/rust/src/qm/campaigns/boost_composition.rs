use crate::linear_algebra::matrix as mx;
use num_bigint::BigInt;
use omega_lie_theory::lorentz::{self, LorentzError};
use omega_number_theory::rational::{ri, Rational};
use serde::{Deserialize, Serialize};
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct IterationStep {
    pub k: usize,
    pub is_identity: bool,
    pub height: BigInt,
}
pub fn iterate_frozen_pair(depth: usize) -> Result<Vec<IterationStep>, LorentzError> {
    lorentz::collinear_power_entries(&ri(2), u64::try_from(depth).unwrap_or(u64::MAX))?;
    let x = lorentz::boost(2, &ri(2), &[ri(1), ri(0)])?;
    let y = lorentz::boost(2, &ri(2), &[ri(0), ri(1)])?;
    let m = mx::multiply(&x, &y)?;
    let mut current = mx::identity(3)?;
    let mut rows = Vec::with_capacity(depth);
    for k in 1..=depth {
        current = mx::multiply(&current, &m)?;
        rows.push(IterationStep {
            k,
            is_identity: mx::is_identity_matrix(&current)?,
            height: lorentz::height(&current),
        });
    }
    Ok(rows)
}
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct CensusResult {
    pub rapidity_count: usize,
    pub direction_count: usize,
    pub total_boost_pairs_enumerated: usize,
    pub finite_order_pairs: usize,
    pub finite_order_collinear_pairs: usize,
    pub finite_order_noncollinear_pairs: usize,
}
pub fn enumerate_boost_pair_space(max_m: usize) -> Result<CensusResult, LorentzError> {
    let c = lorentz::thomas_wigner_census(max_m, &lorentz::standard_plane_directions())?;
    Ok(CensusResult {
        rapidity_count: c.rapidity_count,
        direction_count: c.direction_count,
        total_boost_pairs_enumerated: c.pairs,
        finite_order_pairs: c.finite_order_pairs,
        finite_order_collinear_pairs: c.finite_order_collinear_pairs,
        finite_order_noncollinear_pairs: c.finite_order_noncollinear_pairs,
    })
}
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CompositionReceipt {
    pub cosine: Rational,
    pub sine: Rational,
    pub rotation_order: Option<usize>,
    pub census: CensusResult,
}
pub fn composition_receipt(max_m: usize) -> Result<CompositionReceipt, LorentzError> {
    let x = lorentz::boost(2, &ri(2), &[ri(1), ri(0)])?;
    let y = lorentz::boost(2, &ri(2), &[ri(0), ri(1)])?;
    let rotation = lorentz::thomas_wigner_rotation(&x, &y)?;
    Ok(CompositionReceipt {
        cosine: lorentz::rotation_cosine(&rotation)?,
        sine: rotation.as_slice()[7].clone(),
        rotation_order: omega_lie_theory::finite_order::finite_order(&rotation)?,
        census: enumerate_boost_pair_space(max_m)?,
    })
}
