//! Shared fixtures for the unit tests of this crate.
//!
//! Test code only. Nothing here is part of the public interface.
//!
//! AuthorityEffect: None.

use omega_number_theory::rational::rq;

use crate::simplex::ProbabilitySimplex;
use crate::stochastic_map::StochasticMap;

/// Every way to write `total` as an ordered sum of `parts` nonnegative integers.
pub(crate) fn compositions(total: i64, parts: usize) -> Vec<Vec<i64>> {
    if parts == 1 {
        return vec![vec![total]];
    }
    let mut out = Vec::new();
    for head in 0..=total {
        for mut tail in compositions(total - head, parts - 1) {
            let mut v = vec![head];
            v.append(&mut tail);
            out.push(v);
        }
    }
    out
}

/// Every simplex on `n` points whose masses are multiples of `1 / grid`.
pub(crate) fn grid_simplices(grid: i64, n: usize) -> Vec<ProbabilitySimplex> {
    compositions(grid, n)
        .into_iter()
        .map(|c| {
            ProbabilitySimplex::try_new(c.into_iter().map(|k| rq(k, grid)).collect())
                .expect("a composition of the grid total is a simplex")
        })
        .collect()
}

/// A simplex from `(numerator, denominator)` pairs.
pub(crate) fn simplex(masses: &[(i64, i64)]) -> ProbabilitySimplex {
    ProbabilitySimplex::try_new(masses.iter().map(|&(n, d)| rq(n, d)).collect())
        .expect("the masses of a test fixture form a simplex")
}

/// A stochastic map from rows of `(numerator, denominator)` pairs.
pub(crate) fn stochastic(rows: &[&[(i64, i64)]]) -> StochasticMap {
    let entries: Vec<Vec<_>> = rows
        .iter()
        .map(|row| row.iter().map(|&(n, d)| rq(n, d)).collect())
        .collect();
    StochasticMap::try_from_rows(entries.len(), entries[0].len(), entries, "fixture")
        .expect("the rows of a test fixture are stochastic")
}
