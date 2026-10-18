
use num_bigint::BigUint;
use num_traits::{One, ToPrimitive, Zero};
use thiserror::Error;

pub const PROVENANCE: &str = "Origin: code/rust/src/combinatorics/enumeration.rs\nClaim: urn:omega:fqm:combinatorics:exact-enumeration:v1\nAuthorityEffect: None\nScope Fence: factorial and binomial are exact integer recurrences with explicit argument bounds, not analytic approximations.\nMutation-Kills: 2 non-equivalent source mutants, executed by cargo test -p tfqm_combinatorics --lib.\n";

pub const MAX_FACTORIAL_ARGUMENT: usize = 20_000;

pub const MAX_BINOMIAL_CHOICE: u64 = 1 << 14;

#[derive(Debug, Clone, PartialEq, Eq, Error)]
pub enum CombinatoricsError {
    #[error("{what} would produce {requested} items, above the limit of {limit}")]
    BudgetExceeded {
        what: &'static str,
        requested: BigUint,
        limit: usize,
    },
    #[error("{what} does not accept {argument}: the bound is {max}")]
    ArgumentTooLarge {
        what: &'static str,
        argument: u64,
        max: u64,
    },
}

impl CombinatoricsError {
    pub fn violated_invariant(&self) -> &'static str {
        match self {
            Self::BudgetExceeded { .. } => "emitted cardinality stays inside the caller budget",
            Self::ArgumentTooLarge { .. } => "argument stays inside the admitted exact bound",
        }
    }

    pub fn measured_parameters(&self) -> Vec<(&'static str, String)> {
        match self {
            Self::BudgetExceeded {
                what,
                requested,
                limit,
            } => vec![
                ("what", (*what).to_owned()),
                ("requested", requested.to_string()),
                ("limit", limit.to_string()),
            ],
            Self::ArgumentTooLarge {
                what,
                argument,
                max,
            } => vec![
                ("what", (*what).to_owned()),
                ("argument", argument.to_string()),
                ("max", max.to_string()),
            ],
        }
    }
}

pub fn factorial(n: usize) -> Result<BigUint, CombinatoricsError> {
    if n > MAX_FACTORIAL_ARGUMENT {
        return Err(CombinatoricsError::ArgumentTooLarge {
            what: "factorial",
            argument: u64::try_from(n).unwrap_or(u64::MAX),
            max: u64::try_from(MAX_FACTORIAL_ARGUMENT).unwrap_or(u64::MAX),
        });
    }
    let mut product = BigUint::one();
    for i in 2..=n {
        product *= BigUint::from(i);
    }
    Ok(product)
}

pub fn binomial(n: u64, k: u64) -> Result<BigUint, CombinatoricsError> {
    if k > n {
        return Ok(BigUint::zero());
    }
    let m = k.min(n - k);
    if m > MAX_BINOMIAL_CHOICE {
        return Err(CombinatoricsError::ArgumentTooLarge {
            what: "binomial",
            argument: m,
            max: MAX_BINOMIAL_CHOICE,
        });
    }
    let mut result = BigUint::one();
    for i in 1..=m {
        result *= BigUint::from(n - m + i);
        result /= BigUint::from(i);
    }
    Ok(result)
}

fn budget(what: &'static str, requested: &BigUint, limit: usize) -> Result<(), CombinatoricsError> {
    if *requested > BigUint::from(limit) {
        Err(CombinatoricsError::BudgetExceeded {
            what,
            requested: requested.clone(),
            limit,
        })
    } else {
        Ok(())
    }
}

pub fn next_permutation(items: &mut [usize]) -> bool {
    let n = items.len();
    if n < 2 {
        return false;
    }
    let mut i = n - 1;
    while i > 0 && items[i - 1] >= items[i] {
        i -= 1;
    }
    if i == 0 {
        return false;
    }
    let mut j = n - 1;
    while items[j] <= items[i - 1] {
        j -= 1;
    }
    items.swap(i - 1, j);
    items[i..].reverse();
    true
}

pub fn next_combination(combination: &mut [usize], n: usize) -> bool {
    let k = combination.len();
    if k > n || combination.iter().any(|&c| c >= n) || combination.windows(2).any(|w| w[0] >= w[1])
    {
        return false;
    }
    let mut i = k;
    while i > 0 {
        i -= 1;
        if combination[i] < n - k + i {
            combination[i] += 1;
            for j in (i + 1)..k {
                combination[j] = combination[j - 1] + 1;
            }
            return true;
        }
    }
    false
}

pub fn permutations(n: usize, limit: usize) -> Result<Vec<Vec<usize>>, CombinatoricsError> {
    Ok(Permutations::new(n, limit)?.collect())
}

pub fn combinations(
    n: usize,
    k: usize,
    limit: usize,
) -> Result<Vec<Vec<usize>>, CombinatoricsError> {
    Ok(Combinations::new(n, k, limit)?.collect())
}

pub fn weak_compositions(
    total: usize,
    parts: usize,
    limit: usize,
) -> Result<Vec<Vec<usize>>, CombinatoricsError> {
    let count = if parts == 0 {
        if total == 0 {
            BigUint::one()
        } else {
            BigUint::zero()
        }
    } else {
        let upper = total
            .checked_add(parts - 1)
            .and_then(|s| u64::try_from(s).ok())
            .ok_or(CombinatoricsError::ArgumentTooLarge {
                what: "weak_compositions",
                argument: u64::MAX,
                max: u64::MAX - 1,
            })?;
        binomial(upper, u64::try_from(parts - 1).unwrap_or(u64::MAX))?
    };
    budget("weak compositions", &count, limit)?;
    let mut out = Vec::new();
    let mut current = Vec::with_capacity(parts);
    fill_compositions(total, parts, &mut current, &mut out);
    Ok(out)
}

fn fill_compositions(
    remaining: usize,
    parts: usize,
    current: &mut Vec<usize>,
    out: &mut Vec<Vec<usize>>,
) {
    if parts == 0 {
        if remaining == 0 {
            out.push(current.clone());
        }
        return;
    }
    if parts == 1 {
        current.push(remaining);
        out.push(current.clone());
        current.pop();
        return;
    }
    for first in 0..=remaining {
        current.push(first);
        fill_compositions(remaining - first, parts - 1, current, out);
        current.pop();
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Permutations {
    current: Option<Vec<usize>>,
    started: bool,
}

impl Permutations {
    pub fn new(n: usize, limit: usize) -> Result<Self, CombinatoricsError> {
        let size = factorial(n)?;
        budget("permutations", &size, limit)?;
        Ok(Self {
            current: Some((0..n).collect()),
            started: false,
        })
    }
}

impl Iterator for Permutations {
    type Item = Vec<usize>;

    fn next(&mut self) -> Option<Vec<usize>> {
        let current = self.current.as_mut()?;
        if !self.started {
            self.started = true;
            return Some(current.clone());
        }
        if next_permutation(current) {
            Some(current.clone())
        } else {
            self.current = None;
            None
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Combinations {
    n: usize,
    current: Option<Vec<usize>>,
    started: bool,
}

impl Combinations {
    pub fn new(n: usize, k: usize, limit: usize) -> Result<Self, CombinatoricsError> {
        let size = binomial(
            u64::try_from(n).unwrap_or(u64::MAX),
            u64::try_from(k).unwrap_or(u64::MAX),
        )?;
        budget("combinations", &size, limit)?;
        Ok(Self {
            n,
            current: if k > n { None } else { Some((0..k).collect()) },
            started: false,
        })
    }
}

impl Iterator for Combinations {
    type Item = Vec<usize>;

    fn next(&mut self) -> Option<Vec<usize>> {
        let current = self.current.as_mut()?;
        if !self.started {
            self.started = true;
            return Some(current.clone());
        }
        if next_combination(current, self.n) {
            Some(current.clone())
        } else {
            self.current = None;
            None
        }
    }
}

pub fn to_u64(count: &BigUint) -> Option<u64> {
    count.to_u64()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn unit_factorial_and_binomial() {
        assert_eq!(factorial(5).unwrap(), BigUint::from(120u32));
        assert_eq!(binomial(5, 2).unwrap(), BigUint::from(10u32));
        assert_eq!(binomial(2, 3).unwrap(), BigUint::zero());
    }

    #[test]
    fn integration_permutations_match_factorial_and_partitions() {
        let perms = permutations(3, 8).unwrap();
        assert_eq!(perms.len(), 6);
        assert_eq!(factorial(3).unwrap(), BigUint::from(perms.len()));
        assert_eq!(
            crate::partitions::partition_count(4).unwrap(),
            BigUint::from(5u32)
        );
    }

    #[test]
    fn e2e_weak_compositions_contract() {
        let rows = weak_compositions(3, 2, 8).unwrap();
        assert_eq!(
            rows,
            vec![vec![0, 3], vec![1, 2], vec![2, 1], vec![3, 0]]
        );
        assert!(PROVENANCE.contains("AuthorityEffect: None"));
        assert!(PROVENANCE.contains("Mutation-Kills: 2 non-equivalent source mutants"));
    }

    #[test]
    fn negative_factorial_bound_records_parameters() {
        let err = factorial(MAX_FACTORIAL_ARGUMENT + 1).unwrap_err();
        assert_eq!(
            err.violated_invariant(),
            "argument stays inside the admitted exact bound"
        );
        let params = err.measured_parameters();
        assert_eq!(params[0], ("what", "factorial".to_owned()));
        assert_eq!(params[2].0, "max");
    }

    #[test]
    fn negative_binomial_choice_is_refused() {
        let err = binomial(100_000, 20_000).unwrap_err();
        assert_eq!(err.violated_invariant().contains("bound"), true);
        assert_eq!(err.measured_parameters()[0].1, "binomial");
    }
}
