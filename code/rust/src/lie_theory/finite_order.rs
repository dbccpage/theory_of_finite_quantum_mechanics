
use num_bigint::BigInt;
use num_rational::BigRational;
use num_traits::One;
use omega_number_theory::polynomial::{
    cyclotomic_polynomial, euler_phi, Polynomial, PolynomialError,
};
use omega_number_theory::rational::checked_lcm_usize;

use linear_algebra::exact_field::{characteristic_polynomial, matrix as mx, ExactFieldError};

use crate::QMatrix;

pub const MAX_DIMENSION: usize = 16;

#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum FiniteOrderError {
    #[error("a square matrix of dimension 1..={MAX_DIMENSION} is required, got {rows}x{cols}")]
    Shape { rows: usize, cols: usize },
    #[error("cyclotomic factorisation degree bound {bound} exceeds {MAX_DIMENSION}")]
    DegreeBound { bound: usize },
    #[error("polynomial degree {degree} exceeds declared degree bound {bound}")]
    PolynomialDegree { degree: usize, bound: usize },
    #[error("the least common multiple of the eigenvalue orders overflows")]
    Overflow,
    #[error(transparent)]
    Polynomial(#[from] PolynomialError),
    #[error(transparent)]
    Matrix(#[from] ExactFieldError),
}

pub fn cyclotomic_factorisation(
    polynomial: &Polynomial<BigRational>,
    degree_bound: usize,
) -> Result<Option<Vec<(usize, usize)>>, FiniteOrderError> {
    if degree_bound > MAX_DIMENSION {
        return Err(FiniteOrderError::DegreeBound {
            bound: degree_bound,
        });
    }
    if let Some(degree) = polynomial.degree() {
        if degree > degree_bound {
            return Err(FiniteOrderError::PolynomialDegree {
                degree,
                bound: degree_bound,
            });
        }
    }
    let mut remaining = polynomial.clone();
    let mut factors = Vec::new();
    for k in 1..=(2 * degree_bound * degree_bound).max(1) {
        if euler_phi(k) > degree_bound {
            continue;
        }
        let phi_k = cyclotomic_polynomial(k)?;
        let mut multiplicity = 0usize;
        loop {
            let phi_degree = phi_k.degree().unwrap_or(0);
            if !matches!(remaining.degree(), Some(d) if d >= phi_degree) {
                break;
            }
            let (quotient, remainder) = remaining.div_rem(&phi_k)?;
            if !remainder.is_zero() {
                break;
            }
            remaining = quotient;
            multiplicity += 1;
        }
        if multiplicity > 0 {
            factors.push((k, multiplicity));
        }
    }
    if remaining.degree() == Some(0) && remaining.coefficient(0) == BigRational::one() {
        Ok(Some(factors))
    } else {
        Ok(None)
    }
}

pub fn finite_order(m: &QMatrix) -> Result<Option<usize>, FiniteOrderError> {
    let n = m.rows();
    if m.rows() != m.cols() || n == 0 || n > MAX_DIMENSION {
        return Err(FiniteOrderError::Shape {
            rows: m.rows(),
            cols: m.cols(),
        });
    }
    let coefficients = characteristic_polynomial::characteristic_polynomial(m)?;
    if coefficients.iter().any(|c| !c.is_integer()) {
        return Ok(None);
    }
    let chi = Polynomial::from_coefficients(coefficients);
    let Some(factors) = cyclotomic_factorisation(&chi, n)? else {
        return Ok(None);
    };
    let mut candidate = 1usize;
    for (k, _) in &factors {
        candidate = checked_lcm_usize(candidate, *k).ok_or(FiniteOrderError::Overflow)?;
    }
    let power = mx::power(
        m,
        u64::try_from(candidate).map_err(|_| FiniteOrderError::Overflow)?,
    )?;
    Ok(mx::is_identity_matrix(&power)?.then_some(candidate))
}

pub fn rational_cosines_of_finite_order_rotations() -> Result<Vec<BigRational>, FiniteOrderError> {
    let mut cosines: Vec<BigRational> = Vec::new();
    for k in 1..=6usize {
        if euler_phi(k) > 2 {
            continue;
        }
        let phi_k = cyclotomic_polynomial(k)?;
        let cosine = match phi_k.degree() {
            Some(1) => -phi_k.coefficient(0),
            Some(2) => -phi_k.coefficient(1) / BigRational::from_integer(BigInt::from(2)),
            _ => continue,
        };
        if !cosines.contains(&cosine) {
            cosines.push(cosine);
        }
    }
    cosines.sort();
    Ok(cosines)
}

#[cfg(test)]
mod tests {
    use super::*;
    use omega_number_theory::rational::{ri, rq};

    fn mat(rows: &[&[i64]]) -> QMatrix {
        let cols = rows[0].len();
        QMatrix::from_row_major(
            rows.len(),
            cols,
            rows.iter().flat_map(|r| r.iter().map(|&v| ri(v))).collect(),
        )
        .unwrap()
    }

    #[test]
    fn niven_set_is_derived_from_the_cyclotomic_polynomials() {
        assert_eq!(
            rational_cosines_of_finite_order_rotations().unwrap(),
            vec![ri(-1), rq(-1, 2), ri(0), rq(1, 2), ri(1)]
        );
    }

    #[test]
    fn direct_polynomial_entry_refuses_overflowing_and_false_degree_bounds() {
        let quadratic = cyclotomic_polynomial(3).unwrap();
        assert_eq!(
            cyclotomic_factorisation(&quadratic, usize::MAX),
            Err(FiniteOrderError::DegreeBound { bound: usize::MAX })
        );
        assert_eq!(
            cyclotomic_factorisation(&quadratic, 1),
            Err(FiniteOrderError::PolynomialDegree {
                degree: 2,
                bound: 1
            })
        );
        assert_eq!(
            cyclotomic_factorisation(&quadratic, 2).unwrap(),
            Some(vec![(3, 1)])
        );
        assert_eq!(
            cyclotomic_factorisation(&Polynomial::from_coefficients(vec![ri(1)]), 0).unwrap(),
            Some(vec![])
        );
    }

    #[test]
    fn small_matrices_of_known_order() {
        assert_eq!(finite_order(&mat(&[&[1, 0], &[0, 1]])).unwrap(), Some(1));
        assert_eq!(finite_order(&mat(&[&[-1, 0], &[0, -1]])).unwrap(), Some(2));
        assert_eq!(finite_order(&mat(&[&[0, -1], &[1, 0]])).unwrap(), Some(4));
        assert_eq!(
            finite_order(&mat(&[&[0, 0, 1], &[1, 0, 0], &[0, 1, 0]])).unwrap(),
            Some(3)
        );
        assert_eq!(finite_order(&mat(&[&[0, -1], &[1, 1]])).unwrap(), Some(6));
        assert_eq!(finite_order(&mat(&[&[0, -1], &[1, -1]])).unwrap(), Some(3));
        let five = mat(&[
            &[0, 0, 0, 0, 1],
            &[1, 0, 0, 0, 0],
            &[0, 1, 0, 0, 0],
            &[0, 0, 1, 0, 0],
            &[0, 0, 0, 1, 0],
        ]);
        assert_eq!(finite_order(&five).unwrap(), Some(5));
    }

    #[test]
    fn matrices_of_infinite_order_are_decided_without_a_bound() {
        let rotation =
            QMatrix::from_row_major(2, 2, vec![rq(3, 5), rq(-4, 5), rq(4, 5), rq(3, 5)]).unwrap();
        assert_eq!(finite_order(&rotation).unwrap(), None);
        assert_eq!(finite_order(&mat(&[&[2, 1], &[1, 1]])).unwrap(), None);
        assert_eq!(finite_order(&mat(&[&[1, 1], &[0, 1]])).unwrap(), None);
        assert_eq!(
            finite_order(
                &QMatrix::from_row_major(2, 2, vec![rq(1, 2), ri(0), ri(0), ri(2)]).unwrap()
            )
            .unwrap(),
            None
        );
    }

    #[test]
    fn the_decision_agrees_with_direct_powers_up_to_the_order() {
        let candidates = [
            mat(&[&[0, -1], &[1, 0]]),
            mat(&[&[0, -1], &[1, 1]]),
            mat(&[&[0, -1], &[1, -1]]),
            mat(&[&[1, 1], &[0, 1]]),
            mat(&[&[2, 1], &[1, 1]]),
            mat(&[&[0, 1, 0], &[0, 0, 1], &[1, 0, 0]]),
        ];
        for m in candidates {
            let by_powers =
                (1..=12u64).find(|&k| mx::is_identity_matrix(&mx::power(&m, k).unwrap()).unwrap());
            let decided = finite_order(&m).unwrap();
            match decided {
                Some(order) => assert_eq!(by_powers, Some(order as u64)),
                None => assert_eq!(by_powers, None),
            }
        }
    }

    #[test]
    fn shapes_are_refused() {
        assert!(matches!(
            finite_order(&QMatrix::zero(2, 3).unwrap()),
            Err(FiniteOrderError::Shape { .. })
        ));
        assert!(matches!(
            finite_order(&QMatrix::zero(0, 0).unwrap()),
            Err(FiniteOrderError::Shape { .. })
        ));
        let big = MAX_DIMENSION + 1;
        assert!(matches!(
            finite_order(&QMatrix::zero(big, big).unwrap()),
            Err(FiniteOrderError::Shape { .. })
        ));
    }

    #[test]
    fn cyclotomic_factorisation_reports_multiplicities() {
        let p = Polynomial::from_i64s(&[1, -1, 0, -1, 1]);
        let factors = cyclotomic_factorisation(&p, 4).unwrap().unwrap();
        assert_eq!(factors, vec![(1, 2), (3, 1)]);
        assert_eq!(
            cyclotomic_factorisation(&Polynomial::from_i64s(&[-2, 0, 1]), 2).unwrap(),
            None
        );
    }
}

pub fn gaussian_finite_order(
    matrix: &linear_algebra::backend::basic_matrix::BasicMatrix<
        omega_number_theory::cyclotomic::GaussianRat,
    >,
) -> Result<Option<usize>, FiniteOrderError> {
    let n = matrix.rows();
    if n == 0 || n != matrix.cols() || n > MAX_DIMENSION / 2 {
        return Err(FiniteOrderError::Shape {
            rows: n,
            cols: matrix.cols(),
        });
    }
    let realification = mx::from_fn(2 * n, 2 * n, |r, c| {
        let z = matrix
            .get_ref(r % n, c % n)
            .expect("bounded realification index");
        match (r < n, c < n) {
            (true, true) | (false, false) => z.re.clone(),
            (true, false) => -z.im.clone(),
            (false, true) => z.im.clone(),
        }
    })?;
    finite_order(&realification)
}

#[cfg(test)]
mod dynamics_laws {

    use super::*;
    use omega_number_theory::cyclotomic::GaussianRat;
    use omega_number_theory::rational::{ri, rq};
    #[test]
    fn gaussian_order_decision_preserves_the_faithful_realification() {
        let phase = GaussianRat {
            re: ri(0),
            im: ri(1),
        };
        let root = mx::diagonal(&[phase]).unwrap();
        assert_eq!(gaussian_finite_order(&root).unwrap(), Some(4));
        let infinite = mx::diagonal(&[GaussianRat {
            re: rq(3, 5),
            im: rq(4, 5),
        }])
        .unwrap();
        assert_eq!(gaussian_finite_order(&infinite).unwrap(), None);
        assert!(
            gaussian_finite_order(&mx::identity::<GaussianRat>(MAX_DIMENSION).unwrap()).is_err()
        );
    }
}
