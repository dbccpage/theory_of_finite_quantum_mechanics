use crate::connection::DiscreteConnection;
use crate::error::HolonomyError;
use crate::holonomy::compute_loop_holonomy;
use crate::matrix::{ExactMatrix, ExactScalar};
use omega_kernel::resource_limits::OperationLimits;

pub fn curvature_commutator<T: ExactScalar>(
    m1: &ExactMatrix<T>,
    m2: &ExactMatrix<T>,
    _limits: &OperationLimits,
) -> Result<ExactMatrix<T>, HolonomyError> {
    if m1.rows() != m1.cols() || m2.rows() != m2.cols() || m1.rows() != m2.rows() {
        return Err(HolonomyError::DimensionMismatch {
            expected: m1.rows(),
            actual: m2.rows(),
        });
    }
    let p1 = m1.matmul(m2)?;
    let p2 = m2.matmul(m1)?;

    let mut diff_data = Vec::new();
    let total = p1.as_slice().len();
    for i in 0..total {
        diff_data.push(p1.as_slice()[i].clone() - p2.as_slice()[i].clone());
    }
    ExactMatrix::try_new(m1.rows(), m1.cols(), diff_data)
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
    let id: ExactMatrix<T> = ExactMatrix::try_identity(connection.dim)?;
    let mut diff_data = Vec::new();
    for i in 0..hol.as_slice().len() {
        diff_data.push(hol.as_slice()[i].clone() - id.as_slice()[i].clone());
    }
    ExactMatrix::try_new(connection.dim, connection.dim, diff_data)
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
