//! Path holonomy, loop products, Wilson loop traces, and topological cycle pairings.
//!
//! AuthorityEffect: None.
//! Governing Rule: RULE[user_global] (Ordered product evaluation, Zero-Float Law).

use crate::connection::DiscreteConnection;
use crate::error::HolonomyError;
use crate::graph::CellComplex;
use crate::matrix::{ExactMatrix, ExactScalar};
use serde::{Deserialize, Serialize};

/// Strongly typed closed loop on a discrete cell complex.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct HolonomyLoop {
    pub vertices: Vec<String>,
}

impl HolonomyLoop {
    /// Constructs a validated closed loop.
    ///
    /// Rejects paths with length < 2 with `MalformedPath`.
    /// Rejects open paths (start != end) with `OpenLoop`.
    pub fn try_new(vertices: Vec<String>) -> Result<Self, HolonomyError> {
        if vertices.len() < 2 {
            return Err(HolonomyError::MalformedPath {
                length: vertices.len(),
            });
        }
        let start = vertices.first().unwrap();
        let end = vertices.last().unwrap();
        if start != end {
            return Err(HolonomyError::OpenLoop {
                start: start.clone(),
                end: end.clone(),
            });
        }
        Ok(Self { vertices })
    }
}

/// Computes the discrete path-ordered holonomy operator along an oriented path:
/// $$U(\gamma) = U(e_k) \cdot U(e_{k-1}) \cdots U(e_1)$$
pub fn compute_path_holonomy<T: ExactScalar>(
    connection: &DiscreteConnection<T>,
    path: &[String],
) -> Result<ExactMatrix<T>, HolonomyError> {
    if path.len() < 2 {
        return Err(HolonomyError::EmptyPath);
    }
    if path.len() > connection.limits.max_path_length {
        return Err(HolonomyError::PathLengthExceeded {
            length: path.len(),
            limit: connection.limits.max_path_length,
        });
    }

    let mut current = ExactMatrix::try_identity(connection.dim)?;
    for i in 0..(path.len() - 1) {
        let u = &path[i];
        let v = &path[i + 1];
        let step_mat = connection.get_step(u, v)?;
        // Sequential composition: current = step_mat * current
        current = step_mat.matmul(&current)?;
    }
    Ok(current)
}

/// Computes the closed loop holonomy operator:
/// $$U(\gamma) = \prod_{e \in \gamma} U(e)$$
///
/// Precedence: checks loop closure ($v_0 = v_k$) before evaluating transport.
pub fn compute_loop_holonomy<T: ExactScalar>(
    connection: &DiscreteConnection<T>,
    loop_vertices: &[String],
) -> Result<ExactMatrix<T>, HolonomyError> {
    if loop_vertices.len() < 2 {
        return Err(HolonomyError::MalformedPath {
            length: loop_vertices.len(),
        });
    }
    let start = &loop_vertices[0];
    let end = &loop_vertices[loop_vertices.len() - 1];
    if start != end {
        return Err(HolonomyError::OpenLoop {
            start: start.clone(),
            end: end.clone(),
        });
    }
    compute_path_holonomy(connection, loop_vertices)
}

/// Computes the exact Wilson loop trace:
/// $$W(\gamma) = \operatorname{Tr}(U(\gamma)) \in F$$
pub fn wilson_loop_trace<T: ExactScalar>(
    connection: &DiscreteConnection<T>,
    loop_vertices: &[String],
) -> Result<T, HolonomyError> {
    let hol = compute_loop_holonomy(connection, loop_vertices)?;
    hol.trace()
}

/// Verifies whether the connection is pure-gauge flat on all 2-cells of the cell complex.
pub fn is_flat<T: ExactScalar>(
    connection: &DiscreteConnection<T>,
    complex: &CellComplex,
) -> Result<bool, HolonomyError> {
    let id: ExactMatrix<T> = ExactMatrix::try_identity(connection.dim)?;
    for face in &complex.faces {
        let hol = compute_loop_holonomy(connection, &face.boundary_vertices)?;
        if hol != id {
            return Ok(false);
        }
    }
    Ok(true)
}

/// Evaluates cycle homology pairings for a set of closed cycle generators in $H_1(X, \mathbb{Z})$.
pub fn cycle_homology_pairing<T: ExactScalar>(
    connection: &DiscreteConnection<T>,
    cycles: &[Vec<String>],
) -> Result<Vec<ExactMatrix<T>>, HolonomyError> {
    let mut pairings = Vec::new();
    for cycle in cycles {
        let hol = compute_loop_holonomy(connection, cycle)?;
        pairings.push(hol);
    }
    Ok(pairings)
}

/// High-level engine interface wrapping connection and path algorithms.
#[derive(Debug, Clone)]
pub struct HolonomyEngine<T: ExactScalar> {
    pub connection: DiscreteConnection<T>,
}

impl<T: ExactScalar> HolonomyEngine<T> {
    pub fn new(connection: DiscreteConnection<T>) -> Self {
        Self { connection }
    }

    /// Direct loop holonomy computation matching reference oracle interface.
    pub fn compute_holonomy(&self, loop_path: &[String]) -> Result<ExactMatrix<T>, HolonomyError> {
        compute_loop_holonomy(&self.connection, loop_path)
    }

    /// Direct Wilson loop trace evaluation.
    pub fn wilson_loop_trace(&self, loop_path: &[String]) -> Result<T, HolonomyError> {
        wilson_loop_trace(&self.connection, loop_path)
    }
}
