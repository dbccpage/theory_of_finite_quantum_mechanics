use linear_algebra::backend::basic_matrix::{BasicMatrix, MatrixError, OperationLimits};
use linear_algebra::exact_field::{ExactFieldError, involution as star, matrix as mx};
use omega_category_theory::finite_path::{FinitePathCategory, PathError};
use omega_number_theory::cyclotomic::GaussianRat;

#[derive(Debug, Clone, thiserror::Error)]
pub enum PathAlgebraError {
    #[error(transparent)]
    Path(#[from] PathError),
    #[error(transparent)]
    Matrix(#[from] ExactFieldError),
    #[error(transparent)]
    Storage(#[from] MatrixError),
    #[error("coefficient vector has the wrong path dimension")]
    CoefficientLength,
    #[error("matrix has the wrong path-space shape")]
    Shape,
    #[error("path pair has different origins")]
    DifferentOrigins,
    #[error("unknown origin vertex")]
    UnknownOrigin,
    #[error("matrix is outside the regular path algebra image")]
    OutsidePathAlgebra,
    #[error("matrix is outside the origin-block star algebra")]
    OutsideCompletion,
}

#[derive(Debug, Clone)]
pub struct FinitePathAlgebra {
    paths: FinitePathCategory,
}
impl FinitePathAlgebra {
    pub fn new(paths: FinitePathCategory) -> Self {
        Self { paths }
    }
    pub fn paths(&self) -> &FinitePathCategory {
        &self.paths
    }
    pub fn dimension(&self) -> usize {
        self.paths.paths().len()
    }
    pub fn block_sizes(&self) -> Vec<usize> {
        self.paths.origin_path_counts()
    }
    pub fn completion_dimension(&self) -> usize {
        self.block_sizes().iter().map(|n| n * n).sum()
    }
    pub fn origin_is_path_faithful(&self, vertex: usize) -> Result<bool, PathAlgebraError> {
        if vertex >= self.paths.vertices() {
            return Err(PathAlgebraError::UnknownOrigin);
        }
        Ok((0..self.paths.vertices()).all(|target| {
            self.paths
                .paths()
                .iter()
                .any(|p| p.source() == vertex && p.target() == target)
        }))
    }
    fn shape(&self, a: &BasicMatrix<GaussianRat>) -> Result<(), PathAlgebraError> {
        if a.rows() != self.dimension() || a.cols() != self.dimension() {
            return Err(PathAlgebraError::Shape);
        }
        Ok(())
    }
    pub fn basis_left(
        &self,
        p: usize,
        limits: OperationLimits,
    ) -> Result<BasicMatrix<GaussianRat>, PathAlgebraError> {
        self.paths.path(p)?;
        let mut result = mx::zeros_with_limits(self.dimension(), self.dimension(), limits)?;
        for q in 0..self.dimension() {
            if let Some(pq) = self.paths.compose(q, p)? {
                result.set(pq, q, GaussianRat::one())?;
            }
        }
        Ok(result)
    }
    pub fn left_regular(
        &self,
        a: &[GaussianRat],
        limits: OperationLimits,
    ) -> Result<BasicMatrix<GaussianRat>, PathAlgebraError> {
        if a.len() != self.dimension() {
            return Err(PathAlgebraError::CoefficientLength);
        }
        let mut result = mx::zeros_with_limits(self.dimension(), self.dimension(), limits)?;
        for (p, value) in a.iter().enumerate() {
            for q in 0..self.dimension() {
                if let Some(pq) = self.paths.compose(q, p)? {
                    result.set(pq, q, value.clone())?;
                }
            }
        }
        Ok(result)
    }
    pub fn recover_coefficients(
        &self,
        a: &BasicMatrix<GaussianRat>,
        limits: OperationLimits,
    ) -> Result<Vec<GaussianRat>, PathAlgebraError> {
        self.shape(a)?;
        let values = self
            .paths
            .paths()
            .iter()
            .enumerate()
            .map(|(p, path)| a.get_ref(p, path.source()).cloned())
            .collect::<Result<Vec<_>, _>>()?;
        if self.left_regular(&values, limits)? != *a {
            return Err(PathAlgebraError::OutsidePathAlgebra);
        }
        Ok(values)
    }
    pub fn identity_path_projection(
        &self,
        vertex: usize,
        limits: OperationLimits,
    ) -> Result<BasicMatrix<GaussianRat>, PathAlgebraError> {
        if vertex >= self.paths.vertices() {
            return Err(PathAlgebraError::UnknownOrigin);
        }
        let mut result = self.basis_left(vertex, limits)?;
        for (e, edge) in self.paths.edges().iter().enumerate() {
            if edge.target == vertex {
                let l = self.basis_left(self.paths.edge_path(e)?, limits)?;
                result = mx::sub(
                    &result,
                    &mx::multiply_with_limits(&l, &star::adjoint(&l)?, limits)?,
                )?;
            }
        }
        Ok(result)
    }
    pub fn matrix_unit(
        &self,
        p: usize,
        q: usize,
        limits: OperationLimits,
    ) -> Result<BasicMatrix<GaussianRat>, PathAlgebraError> {
        let source = self.paths.path(p)?.source();
        if self.paths.path(q)?.source() != source {
            return Err(PathAlgebraError::DifferentOrigins);
        }
        let lp = self.basis_left(p, limits)?;
        let vacuum = self.identity_path_projection(source, limits)?;
        let lq = star::adjoint(&self.basis_left(q, limits)?)?;
        Ok(mx::multiply_with_limits(
            &mx::multiply_with_limits(&lp, &vacuum, limits)?,
            &lq,
            limits,
        )?)
    }
    pub fn central_origin_projection(
        &self,
        vertex: usize,
        limits: OperationLimits,
    ) -> Result<BasicMatrix<GaussianRat>, PathAlgebraError> {
        if vertex >= self.paths.vertices() {
            return Err(PathAlgebraError::UnknownOrigin);
        }
        let mut result = mx::zeros_with_limits(self.dimension(), self.dimension(), limits)?;
        for (i, p) in self.paths.paths().iter().enumerate() {
            if p.source() == vertex {
                result.set(i, i, GaussianRat::one())?;
            }
        }
        Ok(result)
    }
    pub fn is_in_completion(&self, a: &BasicMatrix<GaussianRat>) -> Result<bool, PathAlgebraError> {
        self.shape(a)?;
        for (i, p) in self.paths.paths().iter().enumerate() {
            for (j, q) in self.paths.paths().iter().enumerate() {
                if p.source() != q.source() && !a.get_ref(i, j)?.is_zero() {
                    return Ok(false);
                }
            }
        }
        Ok(true)
    }
    pub fn restrict_origin(
        &self,
        a: &BasicMatrix<GaussianRat>,
        vertex: usize,
    ) -> Result<BasicMatrix<GaussianRat>, PathAlgebraError> {
        if vertex >= self.paths.vertices() {
            return Err(PathAlgebraError::UnknownOrigin);
        }
        if !self.is_in_completion(a)? {
            return Err(PathAlgebraError::OutsideCompletion);
        }
        let indices: Vec<_> = self
            .paths
            .paths()
            .iter()
            .enumerate()
            .filter_map(|(i, p)| (p.source() == vertex).then_some(i))
            .collect();
        Ok(BasicMatrix::try_from_fn_result::<_, MatrixError>(
            indices.len(),
            indices.len(),
            |i, j| a.get_ref(indices[i], indices[j]).cloned(),
        )?)
    }
}
