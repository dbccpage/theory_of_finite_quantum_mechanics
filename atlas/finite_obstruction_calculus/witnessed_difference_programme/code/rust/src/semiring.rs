// Executable finite evidence; AuthorityEffect: None.
use num_rational::BigRational;
use crate::error::WdpError;
use num_traits::Zero;
use serde::{Deserialize, Serialize};
use std::collections::BTreeMap;

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct CoarseGrainReceipt {
    pub partition_sums: BTreeMap<usize, BigRational>,
    pub total_mass: BigRational,
}

pub fn coarse_grain(
    weights: &[BigRational],
    partition: &[usize],
) -> Result<CoarseGrainReceipt, WdpError> {
    if weights.len() != partition.len() {
        return Err(WdpError::InvalidInput { detail: "one partition label is required per weight".into() });
    }
    let mut sums = BTreeMap::new();
    let mut total = BigRational::zero();
    for (w, &part) in weights.iter().zip(partition.iter()) {
        *sums.entry(part).or_insert_with(BigRational::zero) += w;
        total += w;
    }
    Ok(CoarseGrainReceipt {
        partition_sums: sums,
        total_mass: total,
    })
}
