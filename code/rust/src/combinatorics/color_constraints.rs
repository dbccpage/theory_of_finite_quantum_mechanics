//! Budgeted finite coloring with a declared symmetric forbidden-pair relation.
//! Each listed edge occurrence contributes once, including loops and repetitions.
//! The minimizing coloring is exact; its violated edges are not claimed to form
//! a minimal unsatisfiable subgraph. AuthorityEffect: None.

use crate::{cartesian_words::CartesianWords, enumeration::CombinatoricsError};
use num_bigint::BigUint;
use std::collections::BTreeSet;

#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum ColorConstraintError {
    #[error("the declared palette must be nonempty")]
    EmptyPalette,
    #[error("edge {0} has an undeclared endpoint")]
    Endpoint(usize),
    #[error("a forbidden color is outside the declared palette")]
    Color,
    #[error(transparent)]
    Enumeration(#[from] CombinatoricsError),
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct MinimumColorViolations {
    pub coloring: Vec<usize>,
    pub violated_edges: Vec<usize>,
}

pub fn minimum_color_violations(
    vertices: usize,
    edges: &[(usize, usize)],
    colors: usize,
    forbidden: &BTreeSet<(usize, usize)>,
    max_colorings: usize,
    max_edge_checks: usize,
) -> Result<MinimumColorViolations, ColorConstraintError> {
    if colors == 0 {
        return Err(ColorConstraintError::EmptyPalette);
    }
    if let Some(i) = edges
        .iter()
        .position(|&(u, v)| u >= vertices || v >= vertices)
    {
        return Err(ColorConstraintError::Endpoint(i));
    }
    if forbidden.iter().any(|&(a, b)| a >= colors || b >= colors) {
        return Err(ColorConstraintError::Color);
    }
    let words = CartesianWords::new(colors, vertices, max_colorings, 4096)?;
    let checks = BigUint::from(words.cardinality()) * BigUint::from(edges.len());
    if checks > BigUint::from(max_edge_checks) {
        return Err(CombinatoricsError::BudgetExceeded {
            what: "coloring edge checks",
            requested: checks,
            limit: max_edge_checks,
        }
        .into());
    }
    let mut best: Option<MinimumColorViolations> = None;
    for coloring in words {
        let violated_edges: Vec<_> = edges
            .iter()
            .enumerate()
            .filter_map(|(i, &(u, v))| {
                let pair = (coloring[u], coloring[v]);
                (forbidden.contains(&pair) || forbidden.contains(&(pair.1, pair.0))).then_some(i)
            })
            .collect();
        if best
            .as_ref()
            .is_none_or(|b| violated_edges.len() < b.violated_edges.len())
        {
            best = Some(MinimumColorViolations {
                coloring,
                violated_edges,
            });
            if best.as_ref().is_some_and(|b| b.violated_edges.is_empty()) {
                break;
            }
        }
    }
    // A nonempty palette has at least one word, including at width zero.
    Ok(best.expect("nonempty palette and admitted Cartesian cardinality"))
}
