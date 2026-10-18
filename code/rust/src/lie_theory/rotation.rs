
use std::hash::Hash;
use std::ops::Neg;

use linear_algebra::backend::basic_matrix::{BasicMatrix, MatrixError, Numeric};
use num_rational::BigRational;
use num_traits::One;
use omega_number_theory::polynomial::euler_phi;
use omega_number_theory::quadratic::Quadratic;
use omega_number_theory::rational::{ri, rq};

use crate::finite_group::{FiniteGroup, GroupError};

pub const MAX_ROTATION_GROUP_ORDER: usize = 120;

#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum RotationError {
    #[error("the matrix is not a rotation of space: it is not 3x3, or M^T M != I, or det M != 1")]
    NotRotation,
    #[error("the axis must be nonzero")]
    ZeroAxis,
    #[error("cos^2 + (sin/|v|)^2 |v|^2 != 1: the parameters do not describe a rotation")]
    NotUnitCircle,
    #[error("the cyclic group C_{0} has no realisation in SO(3, Q): it needs a trace 1 + 2 cos(2 pi / {0}) outside Q")]
    NoRationalRealisation(usize),
    #[error("the dihedral group D_{0} is not built over Q here")]
    UnsupportedDihedral(usize),
    #[error(transparent)]
    Group(#[from] GroupError),
    #[error(transparent)]
    Matrix(#[from] MatrixError),
}

pub trait RotationScalar: Numeric + One + Hash + Eq + Neg<Output = Self> {}
impl<T> RotationScalar for T where T: Numeric + One + Hash + Eq + Neg<Output = T> {}

fn entry<F: Clone>(m: &BasicMatrix<F>, r: usize, c: usize) -> F {
    m.as_slice()[r * m.cols() + c].clone()
}

fn det3<F: RotationScalar>(m: &BasicMatrix<F>) -> F {
    let e = |r: usize, c: usize| entry(m, r, c);
    e(0, 0) * (e(1, 1) * e(2, 2) - e(1, 2) * e(2, 1))
        - e(0, 1) * (e(1, 0) * e(2, 2) - e(1, 2) * e(2, 0))
        + e(0, 2) * (e(1, 0) * e(2, 1) - e(1, 1) * e(2, 0))
}

fn identity3<F: RotationScalar>() -> Result<BasicMatrix<F>, MatrixError> {
    BasicMatrix::try_from_fn(3, 3, |r, c| if r == c { F::one() } else { F::zero() })
}

pub fn is_rotation<F: RotationScalar>(m: &BasicMatrix<F>) -> bool {
    if m.shape() != (3, 3) {
        return false;
    }
    let Ok(transposed) = m.try_transpose() else {
        return false;
    };
    let (Ok(product), Ok(identity)) = (transposed.mul(m), identity3::<F>()) else {
        return false;
    };
    product == identity && det3(m) == F::one()
}

pub fn rotation_group<F: RotationScalar>(
    generators: &[BasicMatrix<F>],
) -> Result<FiniteGroup<BasicMatrix<F>>, RotationError> {
    if generators.iter().any(|g| !is_rotation(g)) {
        return Err(RotationError::NotRotation);
    }
    Ok(FiniteGroup::generated(
        generators,
        identity3::<F>()?,
        |a, b| {
            a.mul(b)
                .expect("the product of two 3x3 matrices of a closed set has a valid shape")
        },
        |m| m.as_slice().to_vec(),
        MAX_ROTATION_GROUP_ORDER,
    )?)
}

fn integer_matrix(rows: [[i64; 3]; 3]) -> BasicMatrix<BigRational> {
    BasicMatrix::from_row_major(3, 3, rows.iter().flatten().map(|&v| ri(v)).collect())
        .expect("a 3x3 array has nine entries")
}

pub fn tetrahedral_group() -> Result<FiniteGroup<BasicMatrix<BigRational>>, RotationError> {
    rotation_group(&[
        integer_matrix([[-1, 0, 0], [0, -1, 0], [0, 0, 1]]),
        integer_matrix([[0, 0, 1], [1, 0, 0], [0, 1, 0]]),
    ])
}

pub fn octahedral_group() -> Result<FiniteGroup<BasicMatrix<BigRational>>, RotationError> {
    rotation_group(&[
        integer_matrix([[0, -1, 0], [1, 0, 0], [0, 0, 1]]),
        integer_matrix([[1, 0, 0], [0, 0, -1], [0, 1, 0]]),
    ])
}

pub fn icosahedral_group() -> Result<FiniteGroup<BasicMatrix<Quadratic<5>>>, RotationError> {
    let q = |n: i64| Quadratic::<5>::from_ints(n, 0);
    let half = Quadratic::<5>::new(rq(1, 2), rq(0, 1));
    let phi = Quadratic::<5>::golden_ratio();
    let inverse_phi = Quadratic::<5>::golden_ratio_conjugate().neg();
    let matrix = |rows: [[Quadratic<5>; 3]; 3]| {
        BasicMatrix::from_row_major(3, 3, rows.into_iter().flatten().collect())
    };
    let s = matrix([[q(1), q(0), q(0)], [q(0), q(-1), q(0)], [q(0), q(0), q(-1)]])?;
    let t = matrix([[q(0), q(0), q(1)], [q(1), q(0), q(0)], [q(0), q(1), q(0)]])?;
    let r = matrix([
        [-half.clone(), &half * &phi, &half * &inverse_phi],
        [&half * &phi, &half * &inverse_phi, half.clone()],
        [&half * &inverse_phi, half.clone(), -(&half * &phi)],
    ])?;
    rotation_group(&[s, t, r])
}

pub fn rational_axis_angle_rotation(
    axis: &[BigRational; 3],
    cos: &BigRational,
    sin_over_norm: &BigRational,
) -> Result<BasicMatrix<BigRational>, RotationError> {
    let norm_squared = axis.iter().fold(ri(0), |acc, a| acc + a * a);
    if norm_squared == ri(0) {
        return Err(RotationError::ZeroAxis);
    }
    if cos * cos + sin_over_norm * sin_over_norm * &norm_squared != ri(1) {
        return Err(RotationError::NotUnitCircle);
    }
    let k = (ri(1) - cos) / &norm_squared;
    let cross = [
        [ri(0), -&axis[2], axis[1].clone()],
        [axis[2].clone(), ri(0), -&axis[0]],
        [-&axis[1], axis[0].clone(), ri(0)],
    ];
    let mut data = Vec::with_capacity(9);
    for r in 0..3 {
        for c in 0..3 {
            let diagonal = if r == c { cos.clone() } else { ri(0) };
            data.push(diagonal + &k * &axis[r] * &axis[c] + sin_over_norm * &cross[r][c]);
        }
    }
    let m = BasicMatrix::from_row_major(3, 3, data)?;
    if !is_rotation(&m) {
        return Err(RotationError::NotRotation);
    }
    Ok(m)
}

pub fn cyclic_rotation_group(
    m: usize,
) -> Result<FiniteGroup<BasicMatrix<BigRational>>, RotationError> {
    let generator = match m {
        1 => rational_axis_angle_rotation(&[ri(0), ri(0), ri(1)], &ri(1), &ri(0))?,
        2 => rational_axis_angle_rotation(&[ri(0), ri(0), ri(1)], &ri(-1), &ri(0))?,
        3 => rational_axis_angle_rotation(&[ri(1), ri(1), ri(1)], &rq(-1, 2), &rq(1, 2))?,
        4 => rational_axis_angle_rotation(&[ri(0), ri(0), ri(1)], &ri(0), &ri(1))?,
        6 => rational_axis_angle_rotation(&[ri(1), ri(1), ri(1)], &rq(1, 2), &rq(1, 2))?,
        _ => return Err(RotationError::NoRationalRealisation(m)),
    };
    rotation_group(&[generator])
}

pub fn dihedral_rotation_group(
    m: usize,
) -> Result<FiniteGroup<BasicMatrix<BigRational>>, RotationError> {
    let (turn, perpendicular_axis) = match m {
        2 => (
            rational_axis_angle_rotation(&[ri(0), ri(0), ri(1)], &ri(-1), &ri(0))?,
            [ri(1), ri(0), ri(0)],
        ),
        3 => (
            rational_axis_angle_rotation(&[ri(1), ri(1), ri(1)], &rq(-1, 2), &rq(1, 2))?,
            [ri(1), ri(-1), ri(0)],
        ),
        4 => (
            rational_axis_angle_rotation(&[ri(0), ri(0), ri(1)], &ri(0), &ri(1))?,
            [ri(1), ri(0), ri(0)],
        ),
        6 => (
            rational_axis_angle_rotation(&[ri(1), ri(1), ri(1)], &rq(1, 2), &rq(1, 2))?,
            [ri(1), ri(-1), ri(0)],
        ),
        _ => return Err(RotationError::UnsupportedDihedral(m)),
    };
    let half_turn = rational_axis_angle_rotation(&perpendicular_axis, &ri(-1), &ri(0))?;
    rotation_group(&[turn, half_turn])
}

pub fn real_subfield_conductor(k: usize) -> usize {
    if k == 0 || euler_phi(k) <= 2 {
        1
    } else if k % 4 == 2 {
        k / 2
    } else {
        k
    }
}

pub fn trace_field_conductor(element_orders: impl IntoIterator<Item = usize>) -> usize {
    element_orders
        .into_iter()
        .map(real_subfield_conductor)
        .fold(1, |acc, c| {
            omega_number_theory::rational::checked_lcm_usize(acc, c).unwrap_or(usize::MAX)
        })
}

pub fn rotation_trace_is_rational(k: usize) -> bool {
    k >= 1 && euler_phi(k) <= 2
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct IcosahedralTraceField {
    pub order_census: std::collections::BTreeMap<usize, usize>,
    pub nonrational_traces: usize,
    pub order_five_elements: usize,
    pub all_nonrational_traces_satisfy_minimal_polynomial: bool,
    pub conductor: usize,
}

pub fn icosahedral_trace_field() -> Result<IcosahedralTraceField, RotationError> {
    let group = icosahedral_group()?;
    let mut census = std::collections::BTreeMap::new();
    let mut irrational = 0;
    let mut order_five = 0;
    let mut polynomial_holds = true;
    for (i, m) in group.elements().iter().enumerate() {
        let order = group.element_order(i)?;
        *census.entry(order).or_insert(0) += 1;
        order_five += usize::from(order == 5);
        let trace = entry(m, 0, 0) + entry(m, 1, 1) + entry(m, 2, 2);
        if !trace.is_rational() {
            irrational += 1;
            polynomial_holds &= trace.clone() * trace.clone() - trace == Quadratic::<5>::one();
        }
    }
    let orders: Vec<_> = census.keys().copied().collect();
    Ok(IcosahedralTraceField {
        order_census: census,
        nonrational_traces: irrational,
        order_five_elements: order_five,
        all_nonrational_traces_satisfy_minimal_polynomial: polynomial_holds,
        conductor: trace_field_conductor(orders),
    })
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn conductors_of_the_real_cyclotomic_subfields() {
        assert_eq!(
            (1..=4).map(real_subfield_conductor).collect::<Vec<_>>(),
            vec![1, 1, 1, 1]
        );
        assert_eq!(real_subfield_conductor(6), 1);
        assert_eq!(real_subfield_conductor(5), 5);
        assert_eq!(real_subfield_conductor(10), 5);
        assert_eq!(real_subfield_conductor(8), 8);
        assert_eq!(real_subfield_conductor(12), 12);
        assert_eq!(trace_field_conductor([1, 2, 3, 5]), 5);
        assert_eq!(trace_field_conductor([1, 2, 3, 4]), 1);
    }
}
