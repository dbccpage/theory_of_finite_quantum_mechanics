//! The finite carrier `Fin n = {0, ..., n-1}`.
//!
//! A carrier is determined by its cardinality, which is at least one. The field is
//! private: a value comes from [`FinN::try_new`], so a zero-point carrier cannot be spelled
//! and no consumer re-checks it. Products of carriers use row-major pair indexing, the
//! convention shared by [`crate::simplex::ProbabilitySimplex::product`],
//! [`crate::stochastic_map::StochasticMap::tensor`] and the joint tables of
//! [`crate::joint_table`]: the pair `(i, j)` of `Fin n x Fin m` has index `i * m + j`.
//!
//! AuthorityEffect: None.

use crate::error::ClassicalShadowError;

/// `left * right`, refusing a product that does not fit in `usize`.
///
/// Every size product in this crate (pair carriers, product distributions, tensor maps,
/// structural maps) goes through this one function.
pub(crate) fn checked_size_product(
    left: usize,
    right: usize,
) -> Result<usize, ClassicalShadowError> {
    left.checked_mul(right)
        .ok_or(ClassicalShadowError::SizeOverflow { left, right })
}

/// The finite set `{0, ..., n-1}` with `n >= 1`.
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub struct FinN {
    n: usize,
}

impl FinN {
    /// `Fin n`, refusing `n = 0`.
    pub fn try_new(n: usize) -> Result<Self, ClassicalShadowError> {
        if n == 0 {
            return Err(ClassicalShadowError::ZeroCardinality);
        }
        Ok(Self { n })
    }

    /// The number of points `n >= 1`.
    pub fn cardinality(&self) -> usize {
        self.n
    }

    /// The points `0, 1, ..., n-1` in order.
    pub fn elements(&self) -> std::ops::Range<usize> {
        0..self.n
    }

    /// Whether `index` names a point of the carrier.
    pub fn contains(&self, index: usize) -> bool {
        index < self.n
    }

    /// The product carrier `Fin n x Fin m = Fin (n m)`, refusing a size that overflows.
    pub fn product(&self, other: &FinN) -> Result<FinN, ClassicalShadowError> {
        Ok(FinN {
            n: checked_size_product(self.n, other.n)?,
        })
    }

    /// The row-major index `i * m + j` of the pair `(i, j)` in `self x other`.
    ///
    /// Refuses a point outside either factor, so the result is always a point of
    /// [`FinN::product`].
    pub fn pair_index(
        &self,
        other: &FinN,
        i: usize,
        j: usize,
    ) -> Result<usize, ClassicalShadowError> {
        if i >= self.n {
            return Err(ClassicalShadowError::IndexOutOfRange {
                index: i,
                bound: self.n,
            });
        }
        if j >= other.n {
            return Err(ClassicalShadowError::IndexOutOfRange {
                index: j,
                bound: other.n,
            });
        }
        // `i < n` and `j < m`, so `i * m + j < n * m`, which `product` checked.
        self.product(other)?;
        Ok(i * other.n + j)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn a_carrier_needs_a_point() {
        assert_eq!(FinN::try_new(0), Err(ClassicalShadowError::ZeroCardinality));
        assert_eq!(FinN::try_new(1).unwrap().cardinality(), 1);
    }

    #[test]
    fn elements_are_the_points_in_order_and_membership_matches() {
        let f = FinN::try_new(4).unwrap();
        assert_eq!(f.cardinality(), 4);
        assert_eq!(f.elements().collect::<Vec<_>>(), vec![0, 1, 2, 3]);
        assert!(f.contains(3));
        assert!(!f.contains(4));
    }

    #[test]
    fn the_product_carrier_has_the_product_cardinality_and_row_major_pairs() {
        let a = FinN::try_new(3).unwrap();
        let b = FinN::try_new(4).unwrap();
        assert_eq!(a.product(&b).unwrap().cardinality(), 12);
        // Every pair gets a distinct index in 0..12, and the order is row-major.
        let mut seen = vec![false; 12];
        for i in 0..3 {
            for j in 0..4 {
                let k = a.pair_index(&b, i, j).unwrap();
                assert_eq!(k, i * 4 + j);
                assert!(!seen[k], "pair ({i}, {j}) repeats index {k}");
                seen[k] = true;
            }
        }
        assert!(seen.iter().all(|&s| s));
    }

    #[test]
    fn pair_indices_outside_either_factor_are_refused() {
        let a = FinN::try_new(3).unwrap();
        let b = FinN::try_new(4).unwrap();
        assert_eq!(
            a.pair_index(&b, 3, 0),
            Err(ClassicalShadowError::IndexOutOfRange { index: 3, bound: 3 })
        );
        assert_eq!(
            a.pair_index(&b, 0, 4),
            Err(ClassicalShadowError::IndexOutOfRange { index: 4, bound: 4 })
        );
    }

    #[test]
    fn a_product_that_overflows_usize_is_refused_not_wrapped() {
        let big = FinN::try_new(usize::MAX).unwrap();
        let two = FinN::try_new(2).unwrap();
        assert_eq!(
            big.product(&two),
            Err(ClassicalShadowError::SizeOverflow {
                left: usize::MAX,
                right: 2
            })
        );
    }
}
