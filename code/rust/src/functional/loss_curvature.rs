
use linear_algebra::backend::basic_matrix::{BasicMatrix, MatrixError};
use num_rational::BigRational as Q;
use num_traits::{One, Signed, Zero};
use thiserror::Error;

pub type Matrix = BasicMatrix<Q>;

#[derive(Debug, Error)]
pub enum LossError {
    #[error(transparent)]
    Matrix(#[from] MatrixError),
    #[error("incompatible or empty endpoint shapes")]
    Shape,
    #[error("rational entries require positive denominators")]
    Rational,
    #[error("the separation margin must be positive")]
    Margin,
    #[error("the direct map does not annihilate the input difference")]
    DirectNotCollapsed,
    #[error("the composed path does not meet the requested separation")]
    NotSeparated,
}

fn valid(values: &[Q]) -> Result<(), LossError> {
    if values.iter().any(|x| x.denom() <= &0.into()) {
        return Err(LossError::Rational);
    }
    Ok(())
}

fn valid_matrix(m: &Matrix) -> Result<(), LossError> {
    if m.rows() == 0 || m.cols() == 0 {
        return Err(LossError::Shape);
    }
    for i in 0..m.rows() {
        for j in 0..m.cols() {
            valid(std::slice::from_ref(m.get_ref(i, j)?))?;
        }
    }
    Ok(())
}

use crate::phi1::l1_mass as l1;

pub(crate) fn identity_matrix(n: usize) -> Result<Matrix, MatrixError> {
    Matrix::try_from_fn(n, n, |i, j| if i == j { Q::one() } else { Q::zero() })
}

fn linf(v: &[Q]) -> Q {
    v.iter().fold(Q::zero(), |m, x| m.max(x.abs()))
}

use crate::phi1::dot;

pub fn matrix_norms(m: &Matrix) -> Result<(Q, Q), LossError> {
    valid_matrix(m)?;
    let mut induced_l1 = Q::zero();
    let mut entry_l1 = Q::zero();
    for j in 0..m.cols() {
        let mut column = Q::zero();
        for i in 0..m.rows() {
            column += m.get_ref(i, j)?.abs();
        }
        entry_l1 += &column;
        induced_l1 = induced_l1.max(column);
    }
    Ok((induced_l1, entry_l1))
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct QuestionLoss {
    collapsed: bool,
    question_difference: Q,
    image_difference: Vec<Q>,
}

impl QuestionLoss {
    pub fn collapsed(&self) -> bool {
        self.collapsed
    }
    pub fn question_difference(&self) -> &Q {
        &self.question_difference
    }
    pub fn image_difference(&self) -> &[Q] {
        &self.image_difference
    }
}

pub fn inspect_question_loss(
    map: &Matrix,
    x: &[Q],
    y: &[Q],
    question: &[Q],
) -> Result<QuestionLoss, LossError> {
    valid_matrix(map)?;
    if x.len() != map.cols() || y.len() != x.len() || question.len() != x.len() {
        return Err(LossError::Shape);
    }
    valid(x)?;
    valid(y)?;
    valid(question)?;
    let difference: Vec<Q> = x.iter().zip(y).map(|(a, b)| a - b).collect();
    let image_difference = map.mul_vec(&difference)?;
    Ok(QuestionLoss {
        collapsed: image_difference.iter().all(Zero::is_zero),
        question_difference: dot(question, &difference),
        image_difference,
    })
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct SeparationBound {
    curvature: Matrix,
    answer_separation: Q,
    induced_l1: Q,
    entry_l1: Q,
    induced_lower_bound: Q,
    entry_lower_bound: Q,
}

impl SeparationBound {
    pub fn curvature(&self) -> &Matrix {
        &self.curvature
    }
    pub fn answer_separation(&self) -> &Q {
        &self.answer_separation
    }
    pub fn induced_l1(&self) -> &Q {
        &self.induced_l1
    }
    pub fn entry_l1(&self) -> &Q {
        &self.entry_l1
    }
    pub fn induced_lower_bound(&self) -> &Q {
        &self.induced_lower_bound
    }
    pub fn entry_lower_bound(&self) -> &Q {
        &self.entry_lower_bound
    }
}

pub fn verify_path_separation(
    composed: &Matrix,
    direct: &Matrix,
    difference: &[Q],
    question: &[Q],
    margin: &Q,
) -> Result<SeparationBound, LossError> {
    valid_matrix(composed)?;
    valid_matrix(direct)?;
    if composed.shape() != direct.shape()
        || difference.len() != direct.cols()
        || question.len() != direct.rows()
    {
        return Err(LossError::Shape);
    }
    valid(difference)?;
    valid(question)?;
    valid(std::slice::from_ref(margin))?;
    if margin <= &Q::zero() {
        return Err(LossError::Margin);
    }
    if direct.mul_vec(difference)?.iter().any(|x| !x.is_zero()) {
        return Err(LossError::DirectNotCollapsed);
    }
    let answer_separation = dot(question, &composed.mul_vec(difference)?).abs();
    if &answer_separation < margin {
        return Err(LossError::NotSeparated);
    }
    let curvature = composed.sub(direct)?;
    let (induced_l1, entry_l1) = matrix_norms(&curvature)?;
    let qnorm = linf(question);
    let induced_lower_bound = margin / (&qnorm * l1(difference));
    let entry_lower_bound = margin / (&qnorm * linf(difference));
    Ok(SeparationBound {
        curvature,
        answer_separation,
        induced_l1,
        entry_l1,
        induced_lower_bound,
        entry_lower_bound,
    })
}

pub fn verify_triangle_separation(
    first: &Matrix,
    second: &Matrix,
    direct: &Matrix,
    difference: &[Q],
    question: &[Q],
    margin: &Q,
) -> Result<SeparationBound, LossError> {
    valid_matrix(first)?;
    valid_matrix(second)?;
    let composed = first.mul(second)?;
    verify_path_separation(&composed, direct, difference, question, margin)
}
