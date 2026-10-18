//! Local deterministic vertices of a declared finite measurement scenario.
//! Contexts name jointly read variables; each assignment contributes one point mass
//! per context. This carrier construction makes no convex or contextuality verdict.
use omega_number_theory::rational::{ri, Rational};

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct LocalVertexLimits {
    pub assignments: usize,
    pub coordinates: usize,
    pub entries: usize,
}
#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum LocalVertexError {
    #[error("a finite scenario needs 1..=20 variables with positive outcome counts and nonempty contexts")]
    InvalidCarrier,
    #[error("context {0} is empty, duplicated, or names an unavailable variable")]
    InvalidContext(usize),
    #[error("the declared contexts do not cover the variables")]
    IncompleteCover,
    #[error("the deterministic vertex enumeration exceeds its declared limits")]
    Budget,
}
/// Outcome order inside context c is its bit pattern in the listed variable order.
/// All sizes are checked against declared budgets before allocation or enumeration.
pub fn binary_local_vertices(
    variables: usize,
    contexts: &[Vec<usize>],
    limits: LocalVertexLimits,
) -> Result<Vec<Vec<Rational>>, LocalVertexError> {
    if !(1..=20).contains(&variables) || contexts.is_empty() || contexts.len() > 256 {
        return Err(LocalVertexError::InvalidCarrier);
    }
    finite_local_vertices(&vec![2; variables], contexts, limits)
}

/// Mixed-radix generalization. `outcomes[v]` is the positive outcome count for
/// variable v; variable 0 (and the first variable in each context) varies fastest.
/// Enumerates ALL assignments, never a sampled support. Binary callers retain
/// their original enumeration order and domain bounds.
pub fn finite_local_vertices(
    outcomes: &[usize],
    contexts: &[Vec<usize>],
    limits: LocalVertexLimits,
) -> Result<Vec<Vec<Rational>>, LocalVertexError> {
    if outcomes.is_empty()
        || outcomes.len() > 20
        || outcomes.contains(&0)
        || contexts.is_empty()
        || contexts.len() > 256
    {
        return Err(LocalVertexError::InvalidCarrier);
    }
    let mut strides = Vec::with_capacity(outcomes.len());
    let mut assignments = 1usize;
    for &count in outcomes {
        strides.push(assignments);
        assignments = assignments
            .checked_mul(count)
            .ok_or(LocalVertexError::Budget)?;
    }
    let mut covered = vec![false; outcomes.len()];
    let mut coordinates = 0usize;
    let mut offsets = Vec::with_capacity(contexts.len());
    for (i, c) in contexts.iter().enumerate() {
        if c.is_empty()
            || c.iter()
                .enumerate()
                .any(|(k, &v)| v >= outcomes.len() || c[..k].contains(&v))
        {
            return Err(LocalVertexError::InvalidContext(i));
        }
        let mut size = 1usize;
        for &v in c {
            covered[v] = true;
            size = size
                .checked_mul(outcomes[v])
                .ok_or(LocalVertexError::Budget)?;
        }
        offsets.push(coordinates);
        coordinates = coordinates
            .checked_add(size)
            .ok_or(LocalVertexError::Budget)?;
    }
    if covered.iter().any(|&x| !x) {
        return Err(LocalVertexError::IncompleteCover);
    }
    if assignments > limits.assignments
        || coordinates > limits.coordinates
        || assignments
            .checked_mul(coordinates)
            .is_none_or(|n| n > limits.entries)
    {
        return Err(LocalVertexError::Budget);
    }
    let mut vertices = Vec::with_capacity(assignments);
    for assignment in 0..assignments {
        let mut point = vec![ri(0); coordinates];
        for (c, &offset) in contexts.iter().zip(&offsets) {
            let (mut local, mut stride) = (0, 1);
            for &v in c {
                local += ((assignment / strides[v]) % outcomes[v]) * stride;
                stride *= outcomes[v]; // bounded above by the checked context size
            }
            point[offset + local] = ri(1);
        }
        vertices.push(point);
    }
    Ok(vertices)
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn bell_vertices_are_point_tables_on_every_context() {
        let c = vec![vec![0, 2], vec![0, 3], vec![1, 2], vec![1, 3]];
        let limits = LocalVertexLimits {
            assignments: 16,
            coordinates: 16,
            entries: 256,
        };
        let v = binary_local_vertices(4, &c, limits).unwrap();
        assert_eq!(v.len(), 16);
        for p in v {
            for row in p.chunks_exact(4) {
                assert_eq!(row.iter().cloned().sum::<Rational>(), ri(1));
                assert_eq!(row.iter().filter(|q| *q == &ri(1)).count(), 1);
            }
        }
    }
    #[test]
    fn vertex_carrier_refuses_bad_contexts_and_budget_before_work() {
        let limits = LocalVertexLimits {
            assignments: 4,
            coordinates: 4,
            entries: 16,
        };
        assert!(matches!(
            binary_local_vertices(2, &[vec![0, 0], vec![1]], limits),
            Err(LocalVertexError::InvalidContext(_))
        ));
        assert_eq!(
            binary_local_vertices(2, &[vec![0]], limits),
            Err(LocalVertexError::IncompleteCover)
        );
        assert_eq!(
            binary_local_vertices(
                2,
                &[vec![0, 1]],
                LocalVertexLimits {
                    entries: 15,
                    ..limits
                }
            ),
            Err(LocalVertexError::Budget)
        );
    }
}
