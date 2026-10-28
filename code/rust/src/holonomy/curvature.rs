use crate::connection::DiscreteConnection;
use crate::error::HolonomyError;
use crate::holonomy::compute_loop_holonomy;
use crate::matrix::{ExactMatrix, ExactScalar};
use engine_kernel::resource_limits::{check_and_reserve, OperationLimits};

/// Admit scalar arithmetic counts and per-matrix cells before any output
/// allocation. These limits do not bound arbitrary-precision coefficient bytes.
fn admit_curvature_work(
    dimension: usize,
    requested: usize,
    limits: &OperationLimits,
) -> Result<usize, HolonomyError> {
    if dimension > limits.max_dimension {
        return Err(HolonomyError::DimensionMismatch {
            expected: limits.max_dimension,
            actual: dimension,
        });
    }
    let cells = dimension
        .checked_mul(dimension)
        .ok_or(HolonomyError::ResourceCountOverflow)?;
    if cells > limits.max_cells {
        return Err(HolonomyError::MatrixCellLimitExceeded {
            requested: cells,
            limit: limits.max_cells,
        });
    }
    if requested > limits.max_operations {
        return Err(HolonomyError::OperationLimitExceeded {
            requested,
            limit: limits.max_operations,
        });
    }
    Ok(cells)
}

fn matrix_difference<T: ExactScalar>(
    left: &ExactMatrix<T>,
    right: &ExactMatrix<T>,
    limits: &OperationLimits,
) -> Result<ExactMatrix<T>, HolonomyError> {
    if left.shape() != right.shape() || left.rows() != left.cols() {
        return Err(HolonomyError::DimensionMismatch {
            expected: left.rows(),
            actual: right.rows(),
        });
    }
    let cells = admit_curvature_work(left.rows(), left.as_slice().len(), limits)?;
    let mut data = Vec::new();
    check_and_reserve(&mut data, cells, limits.max_cells)?;
    for row in 0..left.rows() {
        for col in 0..left.cols() {
            data.push(left.get_scalar(row, col)?.sub(right.get_scalar(row, col)?));
        }
    }
    ExactMatrix::try_new_with_limits(left.rows(), left.cols(), data, limits)
}

pub fn curvature_commutator<T: ExactScalar>(
    m1: &ExactMatrix<T>,
    m2: &ExactMatrix<T>,
    limits: &OperationLimits,
) -> Result<ExactMatrix<T>, HolonomyError> {
    if m1.rows() != m1.cols() || m2.rows() != m2.cols() || m1.rows() != m2.rows() {
        return Err(HolonomyError::DimensionMismatch {
            expected: m1.rows(),
            actual: m2.rows(),
        });
    }
    let dimension = m1.rows();
    // Two dense products use 4*n^3 scalar multiply/add operations; their
    // difference uses n^2 subtractions. Domain checks are separate work.
    let cells = dimension
        .checked_mul(dimension)
        .ok_or(HolonomyError::ResourceCountOverflow)?;
    let work = cells
        .checked_mul(dimension)
        .and_then(|n| n.checked_mul(4))
        .and_then(|n| n.checked_add(cells))
        .ok_or(HolonomyError::ResourceCountOverflow)?;
    admit_curvature_work(dimension, work, limits)?;
    let p1 = m1.matmul_with_limits(m2, limits)?;
    let p2 = m2.matmul_with_limits(m1, limits)?;
    matrix_difference(&p1, &p2, limits)
}

pub fn curvature_commutator_vanishes<T: ExactScalar>(
    m1: &ExactMatrix<T>,
    m2: &ExactMatrix<T>,
    limits: &OperationLimits,
) -> Result<bool, HolonomyError> {
    let comm = curvature_commutator(m1, m2, limits)?;
    Ok(comm.as_slice().iter().all(|x| x.is_zero()))
}

pub fn group_commutator<T: ExactScalar>(
    m1: &ExactMatrix<T>,
    m2: &ExactMatrix<T>,
) -> Result<ExactMatrix<T>, HolonomyError> {
    let m1_inv = m1.inverse()?;
    let m2_inv = m2.inverse()?;
    let p1 = m1.matmul(m2)?;
    let p2 = p1.matmul(&m1_inv)?;
    p2.matmul(&m2_inv)
}

pub fn plaquette_curvature<T: ExactScalar>(
    connection: &DiscreteConnection<T>,
    boundary_vertices: &[String],
) -> Result<ExactMatrix<T>, HolonomyError> {
    let hol = compute_loop_holonomy(connection, boundary_vertices)?;
    let id: ExactMatrix<T> = ExactMatrix::identity(connection.dim, &connection.limits)?;
    matrix_difference(&hol, &id, &connection.limits)
}

pub fn verify_discrete_bianchi_identity<T: ExactScalar>(
    connection: &DiscreteConnection<T>,
    boundary_plaquettes: &[Vec<String>],
) -> Result<bool, HolonomyError> {
    let mut current = ExactMatrix::try_identity(connection.dim)?;
    for plaquette in boundary_plaquettes {
        let hol = compute_loop_holonomy(connection, plaquette)?;
        current = current.matmul(&hol)?;
    }
    let id: ExactMatrix<T> = ExactMatrix::try_identity(connection.dim)?;
    Ok(current == id)
}

#[derive(Debug, Clone)]
pub struct CurvatureEngine<T: ExactScalar> {
    pub connection: DiscreteConnection<T>,
}

impl<T: ExactScalar> CurvatureEngine<T> {
    pub fn new(connection: DiscreteConnection<T>) -> Self {
        Self { connection }
    }

    pub fn plaquette_curvature(
        &self,
        boundary_vertices: &[String],
    ) -> Result<ExactMatrix<T>, HolonomyError> {
        plaquette_curvature(&self.connection, boundary_vertices)
    }

    pub fn curvature_commutator(
        &self,
        m1: &ExactMatrix<T>,
        m2: &ExactMatrix<T>,
    ) -> Result<ExactMatrix<T>, HolonomyError> {
        curvature_commutator(m1, m2, &self.connection.limits)
    }
}
