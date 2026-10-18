//! Exact unitary Cayley charts and their phase-shifted atlas.
//!
//! C_tau(H)=(I-i tau H)(I+i tau H)^-1 for Hermitian H. The inverse chart
//! H=i(U-I)(U+I)^-1 refuses eigenvalue -1. A declared scalar unit phase u
//! changes the chart to u C(H), so its cut locus is eigenvalue -u; multiple
//! charts admit operators excluded by a particular choice of phase.
//! Elimination and its typed singularity data come from linear algebra.
//!
//! AuthorityEffect: None.
use crate::scalar::{is_hermitian, is_unitary, ComplexField};
use linear_algebra::backend::basic_matrix::BasicMatrix;
use linear_algebra::exact_field::{elimination, matrix as mx, ExactFieldError};
use omega_number_theory::rational::Rational;

#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum UnitaryCayleyError {
    #[error("the chart requires a square matrix of dimension 1..=32")]
    Shape,
    #[error("the generator is not Hermitian")]
    NotHermitian,
    #[error("the step is not unitary")]
    NotUnitary,
    #[error("the scalar field does not contain i")]
    MissingImaginaryUnit,
    #[error("the operator has the excluded eigenvalue of this chart")]
    CutLocus { kernel_dimension: usize },
    #[error("the declared chart phase has nonunit norm")]
    NonUnitPhase,
    #[error(transparent)]
    Matrix(#[from] ExactFieldError),
}
fn size<F: ComplexField>(m: &BasicMatrix<F>) -> Result<usize, UnitaryCayleyError> {
    if m.rows() == 0 || m.rows() > 32 || m.rows() != m.cols() {
        return Err(UnitaryCayleyError::Shape);
    }
    Ok(m.rows())
}
pub fn cayley_unitary<F: ComplexField>(
    h: &BasicMatrix<F>,
    tau: &Rational,
) -> Result<BasicMatrix<F>, UnitaryCayleyError> {
    let n = size(h)?;
    if !is_hermitian(h)? {
        return Err(UnitaryCayleyError::NotHermitian);
    }
    let i = F::imaginary_unit().ok_or(UnitaryCayleyError::MissingImaginaryUnit)?;
    let scaled = mx::scale(h, &i.mul(&F::from_rational(tau)))?;
    let identity = mx::identity(n)?;
    Ok(mx::multiply(
        &mx::sub(&identity, &scaled)?,
        &elimination::inverse(&mx::add(&identity, &scaled)?)?,
    )?)
}
pub fn cayley_generator<F: ComplexField>(
    u: &BasicMatrix<F>,
) -> Result<BasicMatrix<F>, UnitaryCayleyError> {
    let n = size(u)?;
    if !is_unitary(u)? {
        return Err(UnitaryCayleyError::NotUnitary);
    }
    let identity = mx::identity(n)?;
    let shifted = mx::add(u, &identity)?;
    let rank = elimination::rank(&shifted)?;
    if rank < n {
        return Err(UnitaryCayleyError::CutLocus {
            kernel_dimension: n - rank,
        });
    }
    let i = F::imaginary_unit().ok_or(UnitaryCayleyError::MissingImaginaryUnit)?;
    Ok(mx::scale(
        &mx::multiply(&mx::sub(u, &identity)?, &elimination::inverse(&shifted)?)?,
        &i,
    )?)
}
pub fn phase_chart_generator<F: ComplexField>(
    u: &BasicMatrix<F>,
    phase: &F,
) -> Result<BasicMatrix<F>, UnitaryCayleyError> {
    if phase.mul(&phase.conjugate()) != F::one() {
        return Err(UnitaryCayleyError::NonUnitPhase);
    }
    cayley_generator(&mx::scale(u, &phase.conjugate())?)
}
pub fn phase_chart_step<F: ComplexField>(
    h: &BasicMatrix<F>,
    phase: &F,
) -> Result<BasicMatrix<F>, UnitaryCayleyError> {
    if phase.mul(&phase.conjugate()) != F::one() {
        return Err(UnitaryCayleyError::NonUnitPhase);
    }
    Ok(mx::scale(
        &cayley_unitary(h, &Rational::from_integer(1.into()))?,
        phase,
    )?)
}
pub fn compose_generators<F: ComplexField>(
    h: &BasicMatrix<F>,
    s: &Rational,
    t: &Rational,
) -> Result<BasicMatrix<F>, UnitaryCayleyError> {
    let a = cayley_unitary(h, s)?;
    let b = cayley_unitary(h, t)?;
    cayley_generator(&mx::multiply(&a, &b)?)
}
