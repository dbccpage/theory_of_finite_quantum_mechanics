//! Plaquette curvature defect F_Box = U(partial Box) - I and Lie bracket commutators.
//!
//! AuthorityEffect: None.
//! Governing Rule: RULE[user_global] (Exact rational curvature defect, Bianchi identity).

use crate::connection::DiscreteConnection;
use crate::error::HolonomyError;
use crate::holonomy::compute_loop_holonomy;
use crate::matrix::{ExactMatrix, ExactScalar};
use omega_kernel::resource_limits::OperationLimits;

/// Computes the Lie bracket matrix commutator:
/// $$[M_1, M_2] = M_1 M_2 - M_2 M_1$$
pub fn curvature_commutator<T: ExactScalar>(
    m1: &ExactMatrix<T>,
    m2: &ExactMatrix<T>,
    _limits: &OperationLimits,
) -> Result<ExactMatrix<T>, HolonomyError> {
    if m1.rows != m1.cols || m2.rows != m2.cols || m1.rows != m2.rows {
        return Err(HolonomyError::DimensionMismatch {
            expected: m1.rows,
            actual: m2.rows,
        });
    }
    let p1 = m1.matmul(m2)?;
    let p2 = m2.matmul(m1)?;

    let mut diff_data = Vec::new();
    let total = p1.data.len();
    for i in 0..total {
        diff_data.push(p1.data[i].clone() - p2.data[i].clone());
    }
    ExactMatrix::try_new(m1.rows, m1.cols, diff_data)
}

/// Checks whether the matrix commutator vanishes: $[M_1, M_2] = 0$.
pub fn curvature_commutator_vanishes<T: ExactScalar>(
    m1: &ExactMatrix<T>,
    m2: &ExactMatrix<T>,
    limits: &OperationLimits,
) -> Result<bool, HolonomyError> {
    let comm = curvature_commutator(m1, m2, limits)?;
    Ok(comm.data.iter().all(|x| x.is_zero()))
}

/// Computes the group commutator:
/// $$(M_1, M_2) = M_1 M_2 M_1^{-1} M_2^{-1}$$
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

/// Computes the plaquette curvature defect:
/// $$F_\Box = U(\partial \Box) - I_d$$
pub fn plaquette_curvature<T: ExactScalar>(
    connection: &DiscreteConnection<T>,
    boundary_vertices: &[String],
) -> Result<ExactMatrix<T>, HolonomyError> {
    let hol = compute_loop_holonomy(connection, boundary_vertices)?;
    let id: ExactMatrix<T> = ExactMatrix::try_identity(connection.dim)?;
    let mut diff_data = Vec::new();
    for i in 0..hol.data.len() {
        diff_data.push(hol.data[i].clone() - id.data[i].clone());
    }
    ExactMatrix::try_new(connection.dim, connection.dim, diff_data)
}

/// Checks the discrete Bianchi identity on the boundary of a 3-cell.
///
/// Returns whether the ordered product of the holonomies of the given loops,
/// $$\prod_{f=1}^k U(\ell_f),$$
/// is the identity. For a closed 2-sphere made of oriented 2-cells
/// $\Box_1, \dots, \Box_k$, that product is $I_d$ for every connection only
/// when the loops are the face boundaries transported to one common base
/// point (each loop reaches its face along a path and returns the same way),
/// ordered and oriented so that together they trace the boundary of the
/// 3-cell: then the loops multiply to the trivial word, and so do their
/// holonomies. The function does not check this. Face loops based at their
/// own vertices do not qualify: for a nonabelian connection the product then
/// depends on the base points, and a `Q8` connection on a tetrahedron gives
/// $-1$ (`omega_quantum_physics/tests/repair_and_gravity/general_relativity_kinematical_shadows.rs`).
/// For an abelian connection neither the base points nor the order matter.
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

/// High-level curvature engine for discrete gauge fields.
#[derive(Debug, Clone)]
pub struct CurvatureEngine<T: ExactScalar> {
    pub connection: DiscreteConnection<T>,
}

impl<T: ExactScalar> CurvatureEngine<T> {
    pub fn new(connection: DiscreteConnection<T>) -> Self {
        Self { connection }
    }

    /// Computes plaquette curvature defect around boundary walk.
    pub fn plaquette_curvature(
        &self,
        boundary_vertices: &[String],
    ) -> Result<ExactMatrix<T>, HolonomyError> {
        plaquette_curvature(&self.connection, boundary_vertices)
    }

    /// Computes Lie bracket commutator between two connection matrices.
    pub fn curvature_commutator(
        &self,
        m1: &ExactMatrix<T>,
        m2: &ExactMatrix<T>,
    ) -> Result<ExactMatrix<T>, HolonomyError> {
        curvature_commutator(m1, m2, &self.connection.limits)
    }
}
