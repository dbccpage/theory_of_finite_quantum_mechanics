//! Exact centralizers of a finite matrix family, with replayed commutation.
//! The linear equations use row-major matrix coordinates. All dimensions,
//! construction work, elimination work and basis storage are bounded before allocation.
//! AuthorityEffect: None.
use super::{charge, element_count, plus, times, ExactFieldError};
use super::{elimination, matrix};
use crate::linear_algebra::basic_matrix::{BasicMatrix, OperationLimits};
use crate::linear_algebra::scalars::{ExactRing, Field};

fn system<F: Field + ExactRing>(
    n: usize,
    generators: &[BasicMatrix<F>],
    limits: OperationLimits,
) -> Result<BasicMatrix<F>, ExactFieldError> {
    let vars = element_count(n, n)?;
    for g in generators {
        if g.shape() != (n, n) {
            return Err(ExactFieldError::ShapeMismatch {
                operation: "commutant",
                left: (n, n),
                right: g.shape(),
            });
        }
    }
    let rows = times(generators.len(), vars)?;
    let elements = element_count(rows, vars)?;
    let work = plus(
        times(2, elements)?,
        times(2, times(rows, times(vars, vars)?)?)?,
    )?;
    charge(limits, elements, work)?;
    matrix::from_fn_with_limits(rows, vars, limits, |r, c| {
        let g = &generators[r / vars];
        let equation = r % vars;
        let (i, j) = (equation / n, equation % n);
        let (k, l) = (c / n, c % n);
        let mut value = F::zero();
        if i == k {
            value = value.add(&g.as_slice()[l * n + j]);
        }
        if j == l {
            value = value.sub(&g.as_slice()[i * n + k]);
        }
        value
    })
}
/// Dimension of the common centralizer; an empty family centralizes every matrix.
pub fn commutant_dimension_with_limits<F: Field + ExactRing>(
    n: usize,
    generators: &[BasicMatrix<F>],
    limits: OperationLimits,
) -> Result<usize, ExactFieldError> {
    let vars = element_count(n, n)?;
    charge(limits, vars, 0)?;
    if generators.is_empty() {
        return Ok(vars);
    }
    let equations = system(n, generators, limits)?;
    Ok(vars - elimination::rank_with_limits(&equations, limits)?)
}
/// Construct an exact basis and independently replay every commutator.
pub fn commutant_basis_with_limits<F: Field + ExactRing>(
    n: usize,
    generators: &[BasicMatrix<F>],
    limits: OperationLimits,
) -> Result<Vec<BasicMatrix<F>>, ExactFieldError> {
    let vars = element_count(n, n)?;
    charge(limits, times(vars, vars)?, 0)?;
    let equations = system(n, generators, limits)?;
    let vectors = elimination::kernel_basis_with_limits(&equations, limits)?;
    charge(
        limits,
        times(vectors.len(), vars)?,
        times(
            4,
            times(
                generators.len(),
                times(vectors.len(), times(n, times(n, n)?)?)?,
            )?,
        )?,
    )?;
    let mut basis = super::reserve(vectors.len())?;
    for vector in vectors {
        let value = BasicMatrix::from_row_major(n, n, vector)?;
        for g in generators {
            if matrix::multiply_with_limits(&value, g, limits)?
                != matrix::multiply_with_limits(g, &value, limits)?
            {
                return Err(ExactFieldError::ReplayFailed {
                    operation: "commutant basis",
                });
            }
        }
        basis.push(value);
    }
    Ok(basis)
}
#[cfg(test)]
mod tests {
    use super::*;
    use num_rational::BigRational;
    fn q(v: i64) -> BigRational {
        BigRational::from_integer(v.into())
    }
    #[test]
    fn centralizer_detects_multiplicity_and_replays_a_complete_basis() {
        let limits = OperationLimits {
            max_elements: 10000,
            max_scalar_ops: 100000,
        };
        let distinct = matrix::diagonal(&[q(0), q(1), q(2)]).unwrap();
        let repeated = matrix::diagonal(&[q(0), q(0), q(1)]).unwrap();
        assert_eq!(
            commutant_dimension_with_limits::<BigRational>(3, &[], limits),
            Ok(9)
        );
        assert_eq!(
            commutant_dimension_with_limits(3, &[distinct], limits),
            Ok(3)
        );
        assert_eq!(
            commutant_dimension_with_limits(3, &[repeated.clone()], limits),
            Ok(5)
        );
        assert_eq!(
            commutant_basis_with_limits(3, &[repeated], limits)
                .unwrap()
                .len(),
            5
        );
        assert!(commutant_dimension_with_limits(
            3,
            &[matrix::identity::<BigRational>(2).unwrap()],
            limits
        )
        .is_err());
        assert!(commutant_dimension_with_limits::<BigRational>(usize::MAX, &[], limits).is_err());
        assert!(commutant_basis_with_limits::<BigRational>(
            3,
            &[],
            OperationLimits {
                max_elements: 8,
                max_scalar_ops: 1
            }
        )
        .is_err());
    }
}
