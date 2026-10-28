
use num_bigint::BigInt;
use num_rational::BigRational;
use num_traits::{One, Signed, Zero};
use tfqm_number_theory::cyclotomic::GaussianRat;
use tfqm_number_theory::polynomial::euler_phi;
use tfqm_number_theory::rational::ri;

use linear_algebra::exact_field::{elimination, matrix as mx, ExactFieldError};

use crate::QMatrix;

pub const MAX_DIMENSION: usize = 32;
pub const MAX_UNIT_EXPONENT: u32 = 1 << 16;

#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum CayleyError {
    #[error("a square matrix of dimension 1..={MAX_DIMENSION} is required, got {rows}x{cols}")]
    Shape { rows: usize, cols: usize },
    #[error("the matrix is not skew-symmetric: entry ({row}, {col}) is not the negative of entry ({col}, {row})")]
    NotSkew { row: usize, col: usize },
    #[error("the matrix is not orthogonal: R^T R != I")]
    NotOrthogonal,
    #[error("I + tau X is singular")]
    Singular,
    #[error("I + R is singular: -1 is an eigenvalue of R, outside the Cayley chart")]
    EigenvalueMinusOne,
    #[error("the chart parameter must be nonzero")]
    ZeroParameter,
    #[error("the composite step has eigenvalue -1 and lies outside the Cayley chart")]
    OutsideChart,
    #[error("{0} is not a unit of Q(i): its squared modulus is not 1")]
    NotUnit(String),
    #[error("the exponent {exponent} exceeds the bound {bound}")]
    ExponentTooLarge { exponent: String, bound: u32 },
    #[error(transparent)]
    Matrix(#[from] ExactFieldError),
}

fn check_shape(m: &QMatrix) -> Result<usize, CayleyError> {
    if m.rows() != m.cols() || m.rows() == 0 || m.rows() > MAX_DIMENSION {
        return Err(CayleyError::Shape {
            rows: m.rows(),
            cols: m.cols(),
        });
    }
    Ok(m.rows())
}

pub fn skew_defect(x: &QMatrix) -> Option<(usize, usize)> {
    let (rows, cols) = x.shape();
    if rows != cols {
        return Some((0, 0));
    }
    for i in 0..rows {
        for j in i..cols {
            let a = &x.as_slice()[i * cols + j];
            let b = &x.as_slice()[j * cols + i];
            if a != &-b {
                return Some((i, j));
            }
        }
    }
    None
}

pub fn is_orthogonal(m: &QMatrix) -> bool {
    mx::transpose(m)
        .and_then(|t| mx::multiply(&t, m))
        .and_then(|product| mx::is_identity_matrix(&product))
        .unwrap_or(false)
}

pub fn is_special_orthogonal(m: &QMatrix) -> bool {
    is_orthogonal(m) && elimination::determinant(m).is_ok_and(|d| d.is_one())
}

pub fn cayley_transform(x: &QMatrix, tau: &BigRational) -> Result<QMatrix, CayleyError> {
    let n = check_shape(x)?;
    if let Some((row, col)) = skew_defect(x) {
        return Err(CayleyError::NotSkew { row, col });
    }
    let identity = mx::identity::<BigRational>(n)?;
    let tau_x = mx::scale(x, tau)?;
    let numerator = mx::sub(&identity, &tau_x)?;
    let denominator = mx::add(&identity, &tau_x)?;
    let inverse = match elimination::inverse(&denominator) {
        Ok(inverse) => inverse,
        Err(ExactFieldError::Singular { .. }) => return Err(CayleyError::Singular),
        Err(other) => return Err(other.into()),
    };
    Ok(mx::multiply(&numerator, &inverse)?)
}

pub fn cayley_inverse(r: &QMatrix, tau: &BigRational) -> Result<QMatrix, CayleyError> {
    let n = check_shape(r)?;
    if tau.is_zero() {
        return Err(CayleyError::ZeroParameter);
    }
    if !is_orthogonal(r) {
        return Err(CayleyError::NotOrthogonal);
    }
    let identity = mx::identity::<BigRational>(n)?;
    let shifted = mx::add(&identity, r)?;
    let inverse = match elimination::inverse(&shifted) {
        Ok(inverse) => inverse,
        Err(ExactFieldError::Singular { .. }) => return Err(CayleyError::EigenvalueMinusOne),
        Err(other) => return Err(other.into()),
    };
    let y = mx::multiply(&mx::sub(&identity, r)?, &inverse)?;
    Ok(mx::scale(&y, &(BigRational::one() / tau))?)
}

pub fn compose_steps(
    x: &QMatrix,
    s: &BigRational,
    t: &BigRational,
) -> Result<QMatrix, CayleyError> {
    let n = check_shape(x)?;
    if let Some((row, col)) = skew_defect(x) {
        return Err(CayleyError::NotSkew { row, col });
    }
    let identity = mx::identity::<BigRational>(n)?;
    let x2 = mx::multiply(x, x)?;
    let denominator = mx::add(&identity, &mx::scale(&x2, &(s * t))?)?;
    let inverse = match elimination::inverse(&denominator) {
        Ok(inverse) => inverse,
        Err(ExactFieldError::Singular { .. }) => return Err(CayleyError::OutsideChart),
        Err(other) => return Err(other.into()),
    };
    Ok(mx::scale(&mx::multiply(x, &inverse)?, &(s + t))?)
}

pub fn so_basis(n: usize) -> Result<Vec<QMatrix>, CayleyError> {
    if n == 0 || n > MAX_DIMENSION {
        return Err(CayleyError::Shape { rows: n, cols: n });
    }
    let mut basis = Vec::with_capacity(n * (n - 1) / 2);
    for i in 0..n {
        for j in (i + 1)..n {
            let mut m = mx::zeros::<BigRational>(n, n)?;
            m.set(i, j, ri(1)).map_err(ExactFieldError::from)?;
            m.set(j, i, ri(-1)).map_err(ExactFieldError::from)?;
            basis.push(m);
        }
    }
    Ok(basis)
}

pub fn cross_product_matrix(v: &[BigRational; 3]) -> Result<QMatrix, CayleyError> {
    let rows = vec![
        vec![ri(0), -&v[2], v[1].clone()],
        vec![v[2].clone(), ri(0), -&v[0]],
        vec![-&v[1], v[0].clone(), ri(0)],
    ];
    Ok(mx::from_rows(rows)?)
}

pub fn compose_circle_parameters(
    s: &BigRational,
    t: &BigRational,
) -> Result<BigRational, CayleyError> {
    let denominator = BigRational::one() - s * t;
    if denominator.is_zero() {
        return Err(CayleyError::OutsideChart);
    }
    Ok((s + t) / denominator)
}

pub fn is_unit(z: &GaussianRat) -> bool {
    z.norm_sq().is_one()
}

pub fn unit_from_parameter(t: &BigRational) -> GaussianRat {
    let t2 = t * t;
    let denominator = BigRational::one() + &t2;
    GaussianRat {
        re: (BigRational::one() - &t2) / &denominator,
        im: (t + t) / &denominator,
    }
}

pub fn parameter_of_unit(z: &GaussianRat) -> Result<Option<BigRational>, CayleyError> {
    if !is_unit(z) {
        return Err(CayleyError::NotUnit(format!("{}+{}i", z.re, z.im)));
    }
    let denominator = BigRational::one() + &z.re;
    if denominator.is_zero() {
        return Ok(None);
    }
    Ok(Some(&z.im / denominator))
}

pub fn unit_pow(u: &GaussianRat, k: &BigInt) -> Result<GaussianRat, CayleyError> {
    if !is_unit(u) {
        return Err(CayleyError::NotUnit(format!("{}+{}i", u.re, u.im)));
    }
    if k.abs() > BigInt::from(MAX_UNIT_EXPONENT) {
        return Err(CayleyError::ExponentTooLarge {
            exponent: k.to_string(),
            bound: MAX_UNIT_EXPONENT,
        });
    }
    let (mut base, mut exponent) = if k.is_negative() {
        (u.conj(), -k.clone())
    } else {
        (u.clone(), k.clone())
    };
    let two = BigInt::from(2);
    let mut acc = GaussianRat::one();
    while exponent.is_positive() {
        if (&exponent % &two).is_one() {
            acc = acc.mul(&base);
        }
        base = base.mul(&base);
        exponent /= &two;
    }
    Ok(acc)
}

pub fn gaussian_unit_order(u: &GaussianRat) -> Result<Option<usize>, CayleyError> {
    if !is_unit(u) {
        return Err(CayleyError::NotUnit(format!("{}+{}i", u.re, u.im)));
    }
    for n in (1..=6usize).filter(|&n| euler_phi(n) <= 2) {
        let exponent = BigInt::from(n);
        if unit_pow(u, &exponent)? == GaussianRat::one() {
            return Ok(Some(n));
        }
    }
    Ok(None)
}

#[cfg(test)]
mod tests {
    use super::*;
    use tfqm_number_theory::rational::rq;

    #[test]
    fn the_plane_cayley_transform_is_the_pythagorean_parametrisation() {
        let j = QMatrix::from_row_major(2, 2, vec![ri(0), ri(-1), ri(1), ri(0)]).unwrap();
        let r = cayley_transform(&j, &rq(1, 2)).unwrap();
        let expected =
            mx::from_rows(vec![vec![rq(3, 5), rq(4, 5)], vec![rq(-4, 5), rq(3, 5)]]).unwrap();
        assert_eq!(r, expected);
        assert!(is_special_orthogonal(&r));
    }

    #[test]
    fn circle_parameter_is_inverse_to_the_unit_chart_away_from_minus_one() {
        for t in [rq(0, 1), rq(1, 2), rq(-3, 7), rq(5, 1)] {
            let z = unit_from_parameter(&t);
            assert!(is_unit(&z));
            assert_eq!(parameter_of_unit(&z).unwrap(), Some(t));
        }
        let minus_one = GaussianRat::from_ints(-1, 0);
        assert_eq!(parameter_of_unit(&minus_one).unwrap(), None);
    }
}

pub fn compactified_circle_composition(
    left: Option<&BigRational>,
    right: Option<&BigRational>,
) -> Option<BigRational> {
    match (left, right) {
        (Some(s), Some(t)) => compose_circle_parameters(s, t).ok(),
        (None, None) => Some(BigRational::zero()),
        (None, Some(t)) | (Some(t), None) if t.is_zero() => None,
        (None, Some(t)) | (Some(t), None) => Some(-BigRational::one() / t),
    }
}
