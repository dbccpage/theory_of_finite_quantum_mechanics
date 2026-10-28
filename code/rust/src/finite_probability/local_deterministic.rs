use tfqm_number_theory::rational::{ri, Rational};

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

fn validate_inputs(
    outcomes: &[usize],
    contexts: &[Vec<usize>],
) -> Result<(), LocalVertexError> {
    if outcomes.is_empty()
        || outcomes.len() > 20
        || outcomes.contains(&0)
        || contexts.is_empty()
        || contexts.len() > 256
    {
        return Err(LocalVertexError::InvalidCarrier);
    }
    Ok(())
}

fn compute_strides(outcomes: &[usize]) -> Result<(Vec<usize>, usize), LocalVertexError> {
    let mut strides = Vec::with_capacity(outcomes.len());
    let mut assignments = 1usize;
    for &count in outcomes {
        strides.push(assignments);
        assignments = assignments
            .checked_mul(count)
            .ok_or(LocalVertexError::Budget)?;
    }
    Ok((strides, assignments))
}

fn validate_context_indices(
    c: &[usize],
    num_outcomes: usize,
    index: usize,
) -> Result<(), LocalVertexError> {
    if c.is_empty()
        || c.iter()
            .enumerate()
            .any(|(k, &v)| v >= num_outcomes || c[..k].contains(&v))
    {
        return Err(LocalVertexError::InvalidContext(index));
    }
    Ok(())
}

fn compute_context_offsets(
    outcomes: &[usize],
    contexts: &[Vec<usize>],
) -> Result<(Vec<usize>, usize), LocalVertexError> {
    let mut covered = vec![false; outcomes.len()];
    let mut coordinates = 0usize;
    let mut offsets = Vec::with_capacity(contexts.len());
    for (i, c) in contexts.iter().enumerate() {
        validate_context_indices(c, outcomes.len(), i)?;
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
    Ok((offsets, coordinates))
}

fn validate_limits(
    assignments: usize,
    coordinates: usize,
    limits: LocalVertexLimits,
) -> Result<(), LocalVertexError> {
    if assignments > limits.assignments || coordinates > limits.coordinates {
        return Err(LocalVertexError::Budget);
    }
    if assignments
        .checked_mul(coordinates)
        .is_none_or(|n| n > limits.entries)
    {
        return Err(LocalVertexError::Budget);
    }
    Ok(())
}

fn enumerate_vertices(
    assignments: usize,
    coordinates: usize,
    outcomes: &[usize],
    contexts: &[Vec<usize>],
    strides: &[usize],
    offsets: &[usize],
) -> Vec<Vec<Rational>> {
    let mut vertices = Vec::with_capacity(assignments);
    for assignment in 0..assignments {
        let mut point = vec![ri(0); coordinates];
        for (c, &offset) in contexts.iter().zip(offsets) {
            let (mut local, mut stride) = (0, 1);
            for &v in c {
                local += ((assignment / strides[v]) % outcomes[v]) * stride;
                stride *= outcomes[v];
            }
            point[offset + local] = ri(1);
        }
        vertices.push(point);
    }
    vertices
}

pub fn finite_local_vertices(
    outcomes: &[usize],
    contexts: &[Vec<usize>],
    limits: LocalVertexLimits,
) -> Result<Vec<Vec<Rational>>, LocalVertexError> {
    validate_inputs(outcomes, contexts)?;
    let (strides, assignments) = compute_strides(outcomes)?;
    let (offsets, coordinates) = compute_context_offsets(outcomes, contexts)?;
    validate_limits(assignments, coordinates, limits)?;
    Ok(enumerate_vertices(
        assignments,
        coordinates,
        outcomes,
        contexts,
        &strides,
        &offsets,
    ))
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
