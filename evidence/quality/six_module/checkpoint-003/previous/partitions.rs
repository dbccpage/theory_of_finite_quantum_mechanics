
use crate::enumeration::{factorial, CombinatoricsError};
use num_bigint::BigUint;
use num_traits::{One, Zero};
use std::collections::BTreeMap;

pub const PROVENANCE: &str = "Origin: code/rust/src/combinatorics/partitions.rs\nClaim: urn:omega:fqm:combinatorics:integer-partition-certificate:v1\nAuthorityEffect: None\nScope Fence: partition counts are the exact recurrence values, not asymptotic Hardy-Ramanujan approximations.\nMutation-Kills: 2 non-equivalent source mutants, executed by cargo test -p tfqm_combinatorics --lib.\n";

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
        let count = multiplicity.entry(p).or_default();
        *count = count.checked_add(1).ok_or(CombinatoricsError::ArgumentTooLarge {
            what: "cycle multiplicity",
            argument: u64::MAX,
            max: u64::MAX - 1,
        })?;
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
    fn unit_partition_count_four() {
        assert_eq!(partition_count(4).unwrap(), BigUint::from(5u32));
    }

    #[test]
    fn integration_conjugacy_uses_factorial() {
        let size = conjugacy_class_size(&[4]).unwrap();
        assert_eq!(size, factorial(4).unwrap() / BigUint::from(4u32));
        assert_eq!(size, BigUint::from(6u32));
    }

    #[test]
    fn e2e_listed_partitions_match_the_count() {
        let listed = partitions(4, 5).unwrap();
        assert_eq!(listed.len(), 5);
        assert!(PROVENANCE.contains("AuthorityEffect: None"));
        assert!(PROVENANCE.contains("Mutation-Kills: 2 non-equivalent source mutants"));
    }

    #[test]
    fn zero_cycle_length_is_refused() {
        let err = conjugacy_class_size(&[2, 0]).unwrap_err();
        assert_eq!(
            err.violated_invariant(),
            "argument stays inside the admitted exact bound"
        );
        assert_eq!(err.measured_parameters()[1], ("argument", "0".to_owned()));
    }

    #[test]
    fn negative_partition_budget_records_limit() {
        let err = partitions(4, 1).unwrap_err();
        assert_eq!(
            err.violated_invariant(),
            "emitted cardinality stays inside the caller budget"
        );
        assert_eq!(err.measured_parameters()[2], ("limit", "1".to_owned()));
    }
}
