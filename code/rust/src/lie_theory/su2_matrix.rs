use crate::pauli_symplectic::{pauli, Pauli, PauliError};
use crate::scalar::{dagger, is_unitary};
use crate::su2::{Quaternion, Su2Error};
use linear_algebra::backend::basic_matrix::BasicMatrix;
use linear_algebra::exact_field::{matrix as mx, ExactFieldError};
use num_traits::One;
use tfqm_number_theory::cyclotomic::GaussianRat;
use tfqm_number_theory::rational::{ri, Rational};

#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum SpinLiftError {
    #[error("the quaternion has squared norm {0}, not one")]
    NotUnitQuaternion(Rational),
    #[error("the matrix must be a 2x2 unitary")]
    NotQubitUnitary,
    #[error("the adjoint trace has a non-real component")]
    NonRealAdjoint,
    #[error(transparent)]
    Quaternion(#[from] Su2Error),
    #[error(transparent)]
    Pauli(#[from] PauliError),
    #[error(transparent)]
    Matrix(#[from] ExactFieldError),
}

pub fn unit_quaternion_matrix(
    q: &[Rational; 4],
) -> Result<BasicMatrix<GaussianRat>, SpinLiftError> {
    let norm: Rational = q.iter().map(|x| x * x).sum();
    if norm != Rational::one() {
        return Err(SpinLiftError::NotUnitQuaternion(norm));
    }
    let [a, b, c, d] = q;
    Ok(BasicMatrix::from_row_major(
        2,
        2,
        vec![
            GaussianRat {
                re: a.clone(),
                im: -d,
            },
            GaussianRat { re: -c, im: -b },
            GaussianRat {
                re: c.clone(),
                im: -b,
            },
            GaussianRat {
                re: a.clone(),
                im: d.clone(),
            },
        ],
    )
    .map_err(ExactFieldError::from)?)
}

pub fn adjoint_su2(u: &BasicMatrix<GaussianRat>) -> Result<BasicMatrix<Rational>, SpinLiftError> {
    if u.shape() != (2, 2) || !is_unitary(u)? {
        return Err(SpinLiftError::NotQubitUnitary);
    }
    let basis = [
        pauli::<GaussianRat>(Pauli::X)?,
        pauli(Pauli::Y)?,
        pauli(Pauli::Z)?,
    ];
    let ud = dagger(u)?;
    let mut result = mx::zeros(3, 3)?;
    for j in 0..3 {
        let image = mx::multiply(&mx::multiply(u, &basis[j])?, &ud)?;
        for k in 0..3 {
            let t = mx::trace(&mx::multiply(&basis[k], &image)?)?;
            if t.im != ri(0) {
                return Err(SpinLiftError::NonRealAdjoint);
            }
            result
                .set(k, j, t.re / ri(2))
                .map_err(ExactFieldError::from)?;
        }
    }
    Ok(result)
}

pub fn matrix_spin_lift(
    r: &BasicMatrix<Rational>,
) -> Result<BasicMatrix<GaussianRat>, SpinLiftError> {
    let Quaternion { w, x, y, z } = crate::su2::spin_lift(r)?;
    unit_quaternion_matrix(&[w, x, y, z])
}

pub fn quaternion_group_matrices() -> Result<Vec<BasicMatrix<GaussianRat>>, SpinLiftError> {
    let group = crate::su2::quaternion_group()?;
    let mut units = group.elements().to_vec();
    units.sort_by_key(|q| {
        for (axis, value) in [&q.w, &q.x, &q.y, &q.z].iter().enumerate() {
            if **value == ri(1) {
                return 2 * axis;
            }
            if **value == ri(-1) {
                return 2 * axis + 1;
            }
        }
        8
    });
    units
        .iter()
        .map(|q| unit_quaternion_matrix(&[q.w.clone(), q.x.clone(), q.y.clone(), q.z.clone()]))
        .collect()
}
