use crate::connection::DiscreteConnection;
use crate::error::HolonomyError;
use crate::graph::CellComplex;
use crate::matrix::{ExactMatrix, ExactScalar};
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct HolonomyLoop {
    pub vertices: Vec<String>,
}

impl HolonomyLoop {
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

    // Public connection storage can be edited or deserialized independently
    // of set_connection. Admit every selected transport before multiplying.
    for edge in path.windows(2) {
        let step = connection.get_step(&edge[0], &edge[1])?;
        if step.rows() != connection.dim || step.cols() != connection.dim {
            return Err(HolonomyError::DimensionMismatch {
                expected: connection.dim,
                actual: step.rows().max(step.cols()),
            });
        }
    }
    let mut current = ExactMatrix::identity(connection.dim, &connection.limits)?;
    for i in 0..(path.len() - 1) {
        let u = &path[i];
        let v = &path[i + 1];
        let step_mat = connection.get_step(u, v)?;
        current = step_mat.matmul_with_limits(&current, &connection.limits)?;
    }
    Ok(current)
}

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

pub fn wilson_loop_trace<T: ExactScalar>(
    connection: &DiscreteConnection<T>,
    loop_vertices: &[String],
) -> Result<T, HolonomyError> {
    let hol = compute_loop_holonomy(connection, loop_vertices)?;
    hol.trace()
}

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

#[derive(Debug, Clone)]
pub struct HolonomyEngine<T: ExactScalar> {
    pub connection: DiscreteConnection<T>,
}

impl<T: ExactScalar> HolonomyEngine<T> {
    pub fn new(connection: DiscreteConnection<T>) -> Self {
        Self { connection }
    }

    pub fn compute_holonomy(&self, loop_path: &[String]) -> Result<ExactMatrix<T>, HolonomyError> {
        compute_loop_holonomy(&self.connection, loop_path)
    }

    pub fn wilson_loop_trace(&self, loop_path: &[String]) -> Result<T, HolonomyError> {
        wilson_loop_trace(&self.connection, loop_path)
    }
}
