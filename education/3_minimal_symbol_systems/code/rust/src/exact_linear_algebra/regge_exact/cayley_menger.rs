//! Cayley-Menger determinants and the rational signed 4-volume.
//!
//! For dimension `d`, the bordered matrix `B` is `(d+2)×(d+2)` and
//! `V² = (-1)^{d+1} / (2^d (d!)²) · det(B)`.
//! The signed 4-volume is `det(v1-v0 | … | v4-v0) / 24`, which lies in `Q`
//! when the vertices do. No square root is taken.
//!
//! AuthorityEffect: None.

#![forbid(unsafe_code)]

use super::gaussian;
use super::q_i64;
use super::ExactError;
use num_rational::BigRational;
use num_traits::{One, Zero};

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct CayleyMengerResult {
    pub dimension: u8,
    pub determinant: BigRational,
    pub volume_squared: BigRational,
}

pub fn cayley_menger(
    dimension: u8,
    squared_lengths: &[[BigRational; 5]; 5],
) -> Result<CayleyMengerResult, ExactError> {
    if !(1..=4).contains(&dimension) {
        return Err(ExactError::Dimension {
            expected: "1..=4",
            got: dimension,
        });
    }
    let last = usize::from(dimension);
    // A d-simplex has d + 1 vertices, indexed `0..=d`.
    let vertices = last + 1;
    for i in 0..=last {
        if !squared_lengths[i][i].is_zero() {
            return Err(ExactError::Degenerate);
        }
        for j in 0..=last {
            if squared_lengths[i][j] != squared_lengths[j][i] {
                return Err(ExactError::Degenerate);
            }
        }
    }
    let determinant = match dimension {
        1 => bordered_det::<3>(squared_lengths, vertices)?,
        2 => bordered_det::<4>(squared_lengths, vertices)?,
        3 => bordered_det::<5>(squared_lengths, vertices)?,
        4 => bordered_det::<6>(squared_lengths, vertices)?,
        _ => unreachable!("dimension was checked"),
    };
    let volume_squared = volume_squared_from_det(dimension, &determinant)?;
    Ok(CayleyMengerResult {
        dimension,
        determinant,
        volume_squared,
    })
}

/// `det(v1-v0 | v2-v0 | v3-v0 | v4-v0) / 24`.
pub fn signed_volume_4(verts: &[[BigRational; 4]; 5]) -> Result<BigRational, ExactError> {
    let mut columns: [[BigRational; 4]; 4] =
        std::array::from_fn(|_| std::array::from_fn(|_| BigRational::zero()));
    for column in 0..4 {
        for row in 0..4 {
            columns[row][column] = &verts[column + 1][row] - &verts[0][row];
        }
    }
    let det = gaussian::determinant(&columns)?;
    Ok(det / q_i64(24))
}

fn bordered_det<const N: usize>(
    squared_lengths: &[[BigRational; 5]; 5],
    dimension: usize,
) -> Result<BigRational, ExactError> {
    let mut bordered: [[BigRational; N]; N] =
        std::array::from_fn(|_| std::array::from_fn(|_| BigRational::zero()));
    for index in 1..N {
        bordered[0][index] = BigRational::one();
        bordered[index][0] = BigRational::one();
    }
    for row in 0..dimension {
        for column in 0..dimension {
            bordered[row + 1][column + 1] = squared_lengths[row][column].clone();
        }
    }
    gaussian::determinant(&bordered)
}

fn volume_squared_from_det(
    dimension: u8,
    determinant: &BigRational,
) -> Result<BigRational, ExactError> {
    let mut factorial = BigRational::one();
    for value in 1..=i64::from(dimension) {
        factorial *= q_i64(value);
    }
    let mut two_power = BigRational::one();
    let two = q_i64(2);
    for _ in 0..dimension {
        two_power *= &two;
    }
    let denominator = &two_power * &factorial * &factorial;
    if denominator.is_zero() {
        return Err(ExactError::DivisionByZero);
    }
    // (-1)^{d+1}
    let signed = if dimension % 2 == 0 {
        -determinant
    } else {
        determinant.clone()
    };
    Ok(signed / denominator)
}
