//! Column-by-column Gaussian elimination over `BigRational`.
//!
//! Partial pivoting selects the pivot of greatest absolute value and tracks the
//! swap sign. A zero pivot makes the determinant `Ok(0)` and a solve
//! [`ExactError::Singular`]. No division is attempted on a zero pivot.
//!
//! AuthorityEffect: None.

#![forbid(unsafe_code)]

use super::ExactError;
use num_rational::BigRational;
use num_traits::{One, Signed, Zero};

pub fn determinant<const N: usize>(
    matrix: &[[BigRational; N]; N],
) -> Result<BigRational, ExactError> {
    if N == 0 {
        return Ok(BigRational::one());
    }
    let mut rows = matrix.clone();
    let mut sign = BigRational::one();
    for column in 0..N {
        let pivot_row = pivot_row(&rows, column);
        if rows[pivot_row][column].is_zero() {
            return Ok(BigRational::zero());
        }
        if pivot_row != column {
            rows.swap(column, pivot_row);
            sign = -sign;
        }
        eliminate_below(&mut rows, None, column);
    }
    let mut det = sign;
    for index in 0..N {
        det *= &rows[index][index];
    }
    Ok(det)
}

pub fn solve<const N: usize>(
    matrix: &[[BigRational; N]; N],
    rhs: &[BigRational; N],
) -> Result<[BigRational; N], ExactError> {
    if N == 0 {
        return Ok(std::array::from_fn(|_| BigRational::zero()));
    }
    let mut rows = matrix.clone();
    let mut values = rhs.clone();
    for column in 0..N {
        let pivot_row = pivot_row(&rows, column);
        if rows[pivot_row][column].is_zero() {
            return Err(ExactError::Singular);
        }
        if pivot_row != column {
            rows.swap(column, pivot_row);
            values.swap(column, pivot_row);
        }
        eliminate_below(&mut rows, Some(&mut values), column);
    }
    back_substitute(&rows, &values)
}

fn pivot_row<const N: usize>(rows: &[[BigRational; N]; N], column: usize) -> usize {
    let mut chosen = column;
    let mut best = rows[column][column].abs();
    for row in (column + 1)..N {
        let magnitude = rows[row][column].abs();
        if magnitude > best {
            best = magnitude;
            chosen = row;
        }
    }
    chosen
}

fn eliminate_below<const N: usize>(
    rows: &mut [[BigRational; N]; N],
    mut rhs: Option<&mut [BigRational; N]>,
    column: usize,
) {
    let pivot = rows[column][column].clone();
    for row in (column + 1)..N {
        let factor = rows[row][column].clone() / &pivot;
        rows[row][column] = BigRational::zero();
        for later in (column + 1)..N {
            let product = &factor * &rows[column][later];
            rows[row][later] -= product;
        }
        if let Some(values) = rhs.as_mut() {
            let product = &factor * &values[column];
            values[row] -= product;
        }
    }
}

fn back_substitute<const N: usize>(
    rows: &[[BigRational; N]; N],
    values: &[BigRational; N],
) -> Result<[BigRational; N], ExactError> {
    let mut solution = std::array::from_fn(|_| BigRational::zero());
    for row in (0..N).rev() {
        if rows[row][row].is_zero() {
            return Err(ExactError::Singular);
        }
        let mut sum = values[row].clone();
        for column in (row + 1)..N {
            sum -= &rows[row][column] * &solution[column];
        }
        solution[row] = sum / &rows[row][row];
    }
    Ok(solution)
}
