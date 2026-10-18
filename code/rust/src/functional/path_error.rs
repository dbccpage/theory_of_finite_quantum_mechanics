
use crate::loss_curvature::{matrix_norms, LossError, Matrix};
use num_rational::BigRational as Q;
use num_traits::Zero;
use thiserror::Error;

#[derive(Debug, Error)]
pub enum PathErrorRefusal {
    #[error(transparent)]
    Owner(#[from] LossError),
    #[error("path profile requires equal lengths in 1..=16 and matching nonempty endpoint shapes in 1..=16")]
    Shape,
    #[error("path inputs require at most 1024 numerator/denominator bits")]
    ScalarProfile,
    #[error("telescoping residual replay failed")]
    Replay,
}

fn identity(n: usize) -> Result<Matrix, PathErrorRefusal> {
    crate::loss_curvature::identity_matrix(n)
        .map_err(LossError::from)
        .map_err(PathErrorRefusal::from)
}
fn product(path: &[Matrix], dimension: usize) -> Result<Matrix, PathErrorRefusal> {
    let mut out = identity(dimension)?;
    for m in path {
        out = m.mul(&out).map_err(LossError::from)?;
    }
    Ok(out)
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct PathErrorBound {
    first: Vec<Matrix>,
    second: Vec<Matrix>,
    residual: Matrix,
    terms: Vec<Matrix>,
    bound: Q,
    actual_norm: Q,
}
impl PathErrorBound {
    pub fn first(&self) -> &[Matrix] {
        &self.first
    }
    pub fn second(&self) -> &[Matrix] {
        &self.second
    }
    pub fn residual(&self) -> &Matrix {
        &self.residual
    }
    pub fn terms(&self) -> &[Matrix] {
        &self.terms
    }
    pub fn bound(&self) -> &Q {
        &self.bound
    }
    pub fn actual_norm(&self) -> &Q {
        &self.actual_norm
    }
}

pub fn certify_path_error(
    first: &[Matrix],
    second: &[Matrix],
) -> Result<PathErrorBound, PathErrorRefusal> {
    if first.is_empty() || first.len() > 16 || first.len() != second.len() {
        return Err(PathErrorRefusal::Shape);
    }
    for (i, (a, b)) in first.iter().zip(second).enumerate() {
        if a.shape() != b.shape()
            || a.rows() > 16
            || a.cols() > 16
            || (i > 0 && first[i - 1].rows() != a.cols())
        {
            return Err(PathErrorRefusal::Shape);
        }
        for m in [a, b] {
            for row in 0..m.rows() {
                for col in 0..m.cols() {
                    let q = m.get_ref(row, col).map_err(LossError::from)?;
                    if q.numer().bits() > 1024 || q.denom().bits() > 1024 {
                        return Err(PathErrorRefusal::ScalarProfile);
                    }
                }
            }
            matrix_norms(m)?;
        }
    }
    let source = first[0].cols();
    let target = first[first.len() - 1].rows();
    let residual = product(first, source)?
        .sub(&product(second, source)?)
        .map_err(LossError::from)?;
    let mut sum = Matrix::try_from_fn(target, source, |_, _| Q::zero()).map_err(LossError::from)?;
    let mut terms = Vec::new();
    let mut bound = Q::zero();
    for i in 0..first.len() {
        let prefix = product(&first[i + 1..], first[i].rows())?;
        let suffix = product(&second[..i], source)?;
        let local = first[i].sub(&second[i]).map_err(LossError::from)?;
        let term = prefix
            .mul(&local)
            .map_err(LossError::from)?
            .mul(&suffix)
            .map_err(LossError::from)?;
        bound += matrix_norms(&prefix)?.0 * matrix_norms(&local)?.0 * matrix_norms(&suffix)?.0;
        sum = sum.add(&term).map_err(LossError::from)?;
        terms.push(term);
    }
    let actual_norm = matrix_norms(&residual)?.0;
    if sum != residual || actual_norm > bound {
        return Err(PathErrorRefusal::Replay);
    }
    Ok(PathErrorBound {
        first: first.to_vec(),
        second: second.to_vec(),
        residual,
        terms,
        bound,
        actual_norm,
    })
}
