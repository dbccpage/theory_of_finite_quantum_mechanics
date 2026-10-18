use crate::linear_algebra::matrix as mx;
use num_bigint::BigInt;
use num_integer::Integer;
use num_traits::One;
use omega_lie_theory::lorentz::{self, LorentzError};
use omega_number_theory::rational::ri;
use serde::{Deserialize, Serialize};
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct PowerSequenceItem {
    pub k: usize,
    pub gamma_num: BigInt,
    pub gamma_den: BigInt,
    pub lowest_terms: bool,
    pub height: BigInt,
    pub is_identity: bool,
}
pub fn power_sequence(max_k: usize) -> Result<Vec<PowerSequenceItem>, LorentzError> {
    let max = u64::try_from(max_k).unwrap_or(u64::MAX);
    lorentz::collinear_power_entries(&ri(2), max)?;
    let b = lorentz::boost(1, &ri(2), &[ri(1)])?;
    let mut current = mx::identity(2)?;
    let mut rows = Vec::with_capacity(max_k);
    for k in 1..=max_k {
        current = mx::multiply(&current, &b)?;
        let gamma = &current.as_slice()[0];
        let expected = lorentz::collinear_power_entries(&ri(2), k as u64)?.0;
        rows.push(PowerSequenceItem {
            k,
            gamma_num: gamma.numer().clone(),
            gamma_den: gamma.denom().clone(),
            lowest_terms: *gamma == expected && gamma.numer().gcd(gamma.denom()).is_one(),
            height: lorentz::height(&current),
            is_identity: mx::is_identity_matrix(&current)?,
        });
    }
    Ok(rows)
}
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct BoostOrderReceipt {
    pub rapidity_ratio: String,
    pub trace: String,
    pub finite_order: Option<usize>,
    pub powers: Vec<PowerSequenceItem>,
}
pub fn boost_order_receipt(depth: usize) -> Result<BoostOrderReceipt, LorentzError> {
    let b = lorentz::boost(1, &ri(2), &[ri(1)])?;
    Ok(BoostOrderReceipt {
        rapidity_ratio: "2".into(),
        trace: mx::trace(&b)?.to_string(),
        finite_order: omega_lie_theory::finite_order::finite_order(&b)?,
        powers: power_sequence(depth)?,
    })
}
