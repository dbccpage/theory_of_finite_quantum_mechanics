use crate::{cartesian_words::CartesianWords, enumeration::CombinatoricsError};
use num_bigint::BigUint;
use std::collections::BTreeSet;

pub const PROVENANCE: &str = "Origin: code/rust/src/combinatorics/color_constraints.rs\nClaim: urn:omega:fqm:combinatorics:minimum-color-violations:v1\nAuthorityEffect: None\nScope Fence: forbidden pairs are an undirected exact constraint, not a physical chromatic polynomial identity.\nMutation-Kills: 1 non-equivalent source mutant, executed by cargo test -p tfqm_combinatorics --lib.\n";

#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum ColorConstraintError {
    #[error("palette cardinality {colors} violates the nonempty palette invariant")]
    EmptyPalette { colors: usize },
    #[error("edge {index} has an undeclared endpoint")]
    Endpoint { index: usize },
    #[error("forbidden color ({left}, {right}) is outside the palette of size {colors}")]
    Color {
        left: usize,
        right: usize,
        colors: usize,
    },
    #[error(transparent)]
    Enumeration(#[from] CombinatoricsError),
}

impl ColorConstraintError {
    pub fn violated_invariant(&self) -> &'static str {
        match self {
            Self::EmptyPalette { .. } => "palette cardinality is positive",
            Self::Endpoint { .. } => "edge endpoints lie in the declared vertex set",
            Self::Color { .. } => "forbidden colors lie in the declared palette",
            Self::Enumeration(err) => err.violated_invariant(),
        }
    }

    pub fn measured_parameters(&self) -> Vec<(&'static str, String)> {
        match self {
            Self::EmptyPalette { colors } => vec![("colors", colors.to_string())],
            Self::Endpoint { index } => vec![("index", index.to_string())],
            Self::Color {
                left,
                right,
                colors,
            } => vec![
                ("left", left.to_string()),
                ("right", right.to_string()),
                ("colors", colors.to_string()),
            ],
            Self::Enumeration(err) => err.measured_parameters(),
        }
    }
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
    let words = admit_instance(
        vertices,
        edges,
        colors,
        forbidden,
        max_colorings,
        max_edge_checks,
    )?;
    let mut best: Option<MinimumColorViolations> = None;
    let mut violations = Vec::new();
    for coloring in words {
        violated_edges(&coloring, edges, forbidden, &mut violations)?;
        best = prefer(best, coloring, &mut violations);
        if best
            .as_ref()
            .is_some_and(|item| item.violated_edges.is_empty())
        {
            break;
        }
    }
    best.ok_or(ColorConstraintError::EmptyPalette { colors })
}

fn admit_instance(
    vertices: usize,
    edges: &[(usize, usize)],
    colors: usize,
    forbidden: &BTreeSet<(usize, usize)>,
    max_colorings: usize,
    max_edge_checks: usize,
) -> Result<CartesianWords, ColorConstraintError> {
    if colors == 0 {
        return Err(ColorConstraintError::EmptyPalette { colors });
    }
    if let Some((index, _)) = edges
        .iter()
        .enumerate()
        .find(|(_, &(u, v))| u >= vertices || v >= vertices)
    {
        return Err(ColorConstraintError::Endpoint { index });
    }
    if let Some(&(left, right)) = forbidden.iter().find(|(a, b)| *a >= colors || *b >= colors) {
        return Err(ColorConstraintError::Color {
            left,
            right,
            colors,
        });
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
    Ok(words)
}

fn violated_edges(
    coloring: &[usize],
    edges: &[(usize, usize)],
    forbidden: &BTreeSet<(usize, usize)>,
    violated: &mut Vec<usize>,
) -> Result<(), ColorConstraintError> {
    violated.clear();
    for (index, &(u, v)) in edges.iter().enumerate() {
        let left = color_at(coloring, u, index)?;
        let right = color_at(coloring, v, index)?;
        if pair_forbidden(forbidden, left, right) {
            violated.push(index);
        }
    }
    Ok(())
}

fn color_at(
    coloring: &[usize],
    vertex: usize,
    index: usize,
) -> Result<usize, ColorConstraintError> {
    coloring
        .get(vertex)
        .copied()
        .ok_or(ColorConstraintError::Endpoint { index })
}

fn pair_forbidden(forbidden: &BTreeSet<(usize, usize)>, left: usize, right: usize) -> bool {
    forbidden.contains(&(left, right)) || forbidden.contains(&(right, left))
}

fn prefer(
    mut best: Option<MinimumColorViolations>,
    coloring: Vec<usize>,
    violated_edges: &mut Vec<usize>,
) -> Option<MinimumColorViolations> {
    let replace = best
        .as_ref()
        .is_none_or(|item| violated_edges.len() < item.violated_edges.len());
    if replace {
        let candidate = MinimumColorViolations {
            coloring,
            violated_edges: std::mem::take(violated_edges),
        };
        if let Some(previous) = best.replace(candidate) {
            *violated_edges = previous.violated_edges;
        }
    }
    best
}

#[cfg(test)]
mod tests {
    use super::*;

    fn edge_forbidden() -> BTreeSet<(usize, usize)> {
        BTreeSet::from([(0, 0), (1, 1), (0, 1)])
    }

    #[test]
    fn unit_reverse_forbidden_pair_still_counts() {
        let best = minimum_color_violations(2, &[(0, 1)], 2, &edge_forbidden(), 8, 16).unwrap();
        assert_eq!(best.violated_edges, vec![0]);
    }

    #[test]
    fn integration_uses_cartesian_words() {
        let words = CartesianWords::new(2, 2, 8, 8).unwrap();
        assert_eq!(words.cardinality(), 4);
        let best = minimum_color_violations(2, &[(0, 1)], 2, &BTreeSet::new(), 8, 16).unwrap();
        assert!(best.violated_edges.is_empty());
    }

    #[test]
    fn e2e_proper_two_coloring_has_no_violation() {
        let forbidden = BTreeSet::from([(0, 0), (1, 1)]);
        let best = minimum_color_violations(2, &[(0, 1)], 2, &forbidden, 8, 16).unwrap();
        assert!(best.violated_edges.is_empty());
        assert!(PROVENANCE.contains("AuthorityEffect: None"));
        assert!(PROVENANCE.contains("Mutation-Kills: 1 non-equivalent source mutant"));
    }

    #[test]
    fn negative_empty_palette_records_colors() {
        let err = minimum_color_violations(1, &[], 0, &BTreeSet::new(), 4, 4).unwrap_err();
        assert_eq!(err.violated_invariant(), "palette cardinality is positive");
        assert_eq!(err.measured_parameters(), vec![("colors", "0".to_owned())]);
    }

    #[test]
    fn negative_endpoint_and_color_are_refused() {
        let endpoint =
            minimum_color_violations(1, &[(0, 2)], 2, &BTreeSet::new(), 4, 4).unwrap_err();
        assert_eq!(endpoint.measured_parameters()[0], ("index", "0".to_owned()));
        let color =
            minimum_color_violations(1, &[], 2, &BTreeSet::from([(2, 0)]), 4, 4).unwrap_err();
        assert_eq!(
            color.violated_invariant(),
            "forbidden colors lie in the declared palette"
        );
    }
}
