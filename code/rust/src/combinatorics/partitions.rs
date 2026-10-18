//! Integer partitions and the sizes of permutation conjugacy classes.
//!
//! A partition of `n` is listed as its parts in non-increasing order. The
//! enumeration order is fixed: largest first part first, then recursively the
//! same order on the rest, so the partitions of 3 come as `[3]`, `[2, 1]`,
//! `[1, 1, 1]`. The number of partitions is computed exactly before any is
//! built, and the walk is refused above the caller's limit.
//!
//! A partition is also the cycle type of a permutation of `n` points;
//! [`conjugacy_class_size`] counts the permutations with exactly that type,
//! `n! / prod(L^c_L * c_L!)`.
//!
//! AuthorityEffect: None.

use crate::enumeration::{factorial, CombinatoricsError};
use num_bigint::BigUint;
use num_traits::{One, Zero};
use std::collections::BTreeMap;

/// Largest `n` for which [`partition_count`] and [`partitions`] are computed.
pub const MAX_PARTITION_ARGUMENT: usize = 1_000;

fn admit(n: usize) -> Result<(), CombinatoricsError> {
    if n > MAX_PARTITION_ARGUMENT {
        return Err(CombinatoricsError::ArgumentTooLarge {
            what: "partitions",
            argument: u64::try_from(n).unwrap_or(u64::MAX),
            max: MAX_PARTITION_ARGUMENT as u64,
        });
    }
    Ok(())
}

/// The number of partitions of `n` exactly (`p(0) = 1`), by the recurrence
/// that adds one allowed part size at a time.
pub fn partition_count(n: usize) -> Result<BigUint, CombinatoricsError> {
    admit(n)?;
    let mut ways = vec![BigUint::zero(); n + 1];
    ways[0] = BigUint::one();
    for part in 1..=n {
        for total in part..=n {
            let previous = ways[total - part].clone();
            ways[total] += previous;
        }
    }
    Ok(ways.swap_remove(n))
}

/// Every partition of `n`, parts non-increasing, in the order described in
/// the module documentation. Refused when `p(n) > limit`.
pub fn partitions(n: usize, limit: usize) -> Result<Vec<Vec<usize>>, CombinatoricsError> {
    let count = partition_count(n)?;
    if count > BigUint::from(limit) {
        return Err(CombinatoricsError::BudgetExceeded {
            what: "partitions",
            requested: count,
            limit,
        });
    }
    let mut out = Vec::new();
    let mut current = Vec::new();
    fill(n, n, &mut current, &mut out);
    Ok(out)
}

fn fill(remaining: usize, largest: usize, current: &mut Vec<usize>, out: &mut Vec<Vec<usize>>) {
    if remaining == 0 {
        out.push(current.clone());
        return;
    }
    for part in (1..=remaining.min(largest)).rev() {
        current.push(part);
        fill(remaining - part, part, current, out);
        current.pop();
    }
}

/// How many permutations of `parts.iter().sum()` points have exactly these
/// cycle lengths. Every part must be positive; order of parts is ignored.
pub fn conjugacy_class_size(parts: &[usize]) -> Result<BigUint, CombinatoricsError> {
    if parts.contains(&0) {
        return Err(CombinatoricsError::ArgumentTooLarge {
            what: "cycle length (must be positive)",
            argument: 0,
            max: 0,
        });
    }
    let n = parts
        .iter()
        .try_fold(0usize, |acc, &p| acc.checked_add(p))
        .ok_or(CombinatoricsError::ArgumentTooLarge {
            what: "sum of cycle lengths",
            argument: u64::MAX,
            max: u64::MAX - 1,
        })?;
    let mut multiplicity: BTreeMap<usize, usize> = BTreeMap::new();
    for &p in parts {
        *multiplicity.entry(p).or_default() += 1;
    }
    let mut centralizer = BigUint::one();
    for (&length, &count) in &multiplicity {
        centralizer *= BigUint::from(length).pow(u32::try_from(count).unwrap_or(u32::MAX));
        centralizer *= factorial(count)?;
    }
    Ok(factorial(n)? / centralizer)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn small_partitions_are_listed_in_the_declared_order() {
        assert_eq!(partitions(0, 1).unwrap(), vec![Vec::<usize>::new()]);
        assert_eq!(
            partitions(4, 5).unwrap(),
            vec![vec![4], vec![3, 1], vec![2, 2], vec![2, 1, 1], vec![1, 1, 1, 1]]
        );
    }

    #[test]
    fn zero_cycle_length_is_refused() {
        assert!(conjugacy_class_size(&[2, 0]).is_err());
    }
}
