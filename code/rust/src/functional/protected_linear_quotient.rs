//! The minimal report for a declared finite family of rational linear questions.
//! Qx=Qy iff their canonical row-space reports agree. An operator T descends
//! precisely when it transports the source question kernel into the target
//! kernel. This concerns declared linear answers, not ultimate physical substance.

use linear_algebra::backend::basic_matrix::{BasicMatrix, MatrixError, OperationLimits};
use linear_algebra::exact_field::elimination::rref_with_limits;
use num_rational::BigRational as Q;
use num_traits::{One, Zero};
use thiserror::Error;

pub type Matrix = BasicMatrix<Q>;

#[derive(Debug, Error)]
pub enum QuotientError {
    #[error(transparent)]
    Matrix(#[from] MatrixError),
    #[error("question/operator profile requires nonempty shapes at most 32 and valid rational denominators")]
    Profile,
    #[error("exact row-space computation refused")]
    Elimination,
    #[error("operator endpoints differ from their declared question carriers")]
    Shape,
    #[error("operator sends a source-invisible difference to a visible target answer")]
    VisibleKernel,
    #[error("exact decoder or section identity failed")]
    Replay,
}

fn valid(m: &Matrix) -> Result<(), QuotientError> {
    if m.rows() == 0 || m.cols() == 0 || m.rows() > 32 || m.cols() > 32 {
        return Err(QuotientError::Profile);
    }
    for i in 0..m.rows() {
        for j in 0..m.cols() {
            let x = m.get_ref(i, j)?;
            if x.denom() <= &0.into() || x.numer().bits() > 1024 || x.denom().bits() > 1024 {
                return Err(QuotientError::Profile);
            }
        }
    }
    Ok(())
}
fn identity(n: usize) -> Result<Matrix, QuotientError> {
    Ok(crate::loss_curvature::identity_matrix(n)?)
}
fn zero(m: &Matrix) -> Result<bool, QuotientError> {
    for i in 0..m.rows() {
        for j in 0..m.cols() {
            if !m.get_ref(i, j)?.is_zero() {
                return Ok(false);
            }
        }
    }
    Ok(true)
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ReportQuotient {
    questions: Matrix,
    report: Matrix,
    section: Matrix,
    decoder: Matrix,
    kernel_projection: Matrix,
}

impl ReportQuotient {
    pub fn new(questions: Matrix) -> Result<Self, QuotientError> {
        valid(&questions)?;
        let reduced = rref_with_limits(
            &questions,
            OperationLimits {
                max_elements: 1024,
                max_scalar_ops: 500_000,
            },
        )
        .map_err(|_| QuotientError::Elimination)?;
        let rank = reduced.rank();
        let report = Matrix::try_from_fn_result(rank, questions.cols(), |i, j| {
            reduced.matrix().get_ref(i, j).cloned()
        })?;
        let section = Matrix::try_from_fn(questions.cols(), rank, |i, j| {
            if i == reduced.pivot_columns()[j] {
                Q::one()
            } else {
                Q::zero()
            }
        })?;
        let decoder = questions.mul(&section)?;
        let kernel_projection = identity(questions.cols())?.sub(&section.mul(&report)?)?;
        if decoder.mul(&report)? != questions
            || report.mul(&section)? != identity(rank)?
            || !zero(&report.mul(&kernel_projection)?)?
        {
            return Err(QuotientError::Replay);
        }
        Ok(Self {
            questions,
            report,
            section,
            decoder,
            kernel_projection,
        })
    }
    pub fn questions(&self) -> &Matrix {
        &self.questions
    }
    pub fn report(&self) -> &Matrix {
        &self.report
    }
    pub fn section(&self) -> &Matrix {
        &self.section
    }
    pub fn decoder(&self) -> &Matrix {
        &self.decoder
    }
    pub fn kernel_projection(&self) -> &Matrix {
        &self.kernel_projection
    }
    pub fn state_dimension(&self) -> usize {
        self.questions.cols()
    }
    pub fn report_dimension(&self) -> usize {
        self.report.rows()
    }

    /// Exact iff criterion, with a unique report map recomputed from T.
    pub fn descend(&self, target: &Self, operator: &Matrix) -> Result<Matrix, QuotientError> {
        valid(operator)?;
        if operator.shape() != (target.state_dimension(), self.state_dimension()) {
            return Err(QuotientError::Shape);
        }
        let observed = target.report.mul(operator)?;
        if !zero(&observed.mul(&self.kernel_projection)?)? {
            return Err(QuotientError::VisibleKernel);
        }
        let descended = observed.mul(&self.section)?;
        if descended.mul(&self.report)? != observed {
            return Err(QuotientError::Replay);
        }
        Ok(descended)
    }
}
