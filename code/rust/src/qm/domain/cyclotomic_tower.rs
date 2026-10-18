//! Cyclotomic tower domain types.
use crate::linear_algebra::scalars::Q;

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct CyclotomicTower {
    pub conductor: usize,
    pub degree: usize,
}
