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
            value = value.try_add(&g.as_slice()[l * n + j])?;
        }
        if j == l {
            value = value.try_sub(&g.as_slice()[i * n + k])?;
        }
        value
    })
}
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
fn combined_basis_budget(n: usize, generators: usize) -> Result<(usize, usize), ExactFieldError> {
    let vars = element_count(n, n)?;
    let rows = times(generators, vars)?;
    let equation_elements = element_count(rows, vars)?;
    let construction_ops = plus(
        times(2, equation_elements)?,
        times(2, times(rows, times(vars, vars)?)?)?,
    )?;
    let kernel_elements = equation_elements.max(element_count(vars, vars)?);
    let kernel_ops = elimination::reduction_cost(rows, vars)?;
    let stored_basis = element_count(vars, vars)?;
    let replay_ops = times(
        4,
        times(generators, times(vars, times(n, times(n, n)?)?)?)?,
    )?;
    let elements = plus(
        plus(plus(stored_basis, equation_elements)?, kernel_elements)?,
        stored_basis,
    )?;
    let ops = plus(plus(construction_ops, kernel_ops)?, replay_ops)?;
    Ok((elements, ops))
}

pub fn commutant_basis_with_limits<F: Field + ExactRing>(
    n: usize,
    generators: &[BasicMatrix<F>],
    limits: OperationLimits,
) -> Result<Vec<BasicMatrix<F>>, ExactFieldError> {
    let (elements, ops) = combined_basis_budget(n, generators.len())?;
    charge(limits, elements, ops)?;
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
    use num_traits::Zero;
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

    #[test]
    fn the_basis_budget_is_an_aggregate_of_construction_elimination_and_replay() {
        let generator = matrix::from_rows(vec![vec![q(7)]]).unwrap();
        assert!(commutant_basis_with_limits(
            1,
            &[generator],
            OperationLimits {
                max_elements: 1,
                max_scalar_ops: 4,
            }
        )
        .is_err());
    }

    #[test]
    fn a_nilpotent_centralizer_and_a_scalar_center_are_spanned_and_independent() {
        let limits = OperationLimits {
            max_elements: 10000,
            max_scalar_ops: 100000,
        };
        let nilpotent = matrix::from_rows(vec![vec![q(0), q(1)], vec![q(0), q(0)]]).unwrap();
        let basis = commutant_basis_with_limits(2, &[nilpotent], limits).unwrap();
        assert_eq!(basis.len(), 2);
        for matrix in &basis {
            let entries = matrix.as_slice();
            assert_eq!(entries[0], entries[3]);
            assert_eq!(entries[2], q(0));
        }
        let stacked = matrix::from_rows(
            basis
                .iter()
                .map(|matrix| matrix.as_slice().to_vec())
                .collect(),
        )
        .unwrap();
        assert_eq!(elimination::rank(&stacked).unwrap(), basis.len());

        let lower = matrix::from_rows(vec![vec![q(0), q(0)], vec![q(1), q(0)]]).unwrap();
        let upper = matrix::from_rows(vec![vec![q(0), q(1)], vec![q(0), q(0)]]).unwrap();
        let center = commutant_basis_with_limits(2, &[lower, upper], limits).unwrap();
        assert_eq!(center.len(), 1);
        let entries = center[0].as_slice();
        assert_eq!(entries[0], entries[3]);
        assert!(entries[1].is_zero() && entries[2].is_zero());
        assert!(!entries[0].is_zero());
    }
}
