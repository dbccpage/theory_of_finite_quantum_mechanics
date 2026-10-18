//! Campaign module stinespring.
//!
//! An isometry `V: C^2 → C^2 ⊗ C^2` with
//! `V|0⟩ = |00⟩` and `V|1⟩ = (3/5)|10⟩ + (4/5)|11⟩`.
//! The Gram matrix is the identity, and the sum of squared amplitudes on the
//! second column is the same 1.

use num_bigint::BigInt;
use num_rational::BigRational;


pub fn verify() -> Result<BigRational, &'static str> {
    let zero = ratio(0, 1)?;
    let one = ratio(1, 1)?;
    let three = ratio(3, 5)?;
    let four = ratio(4, 5)?;
    // Columns are V|0⟩ and V|1⟩ in order |00⟩, |01⟩, |10⟩, |11⟩.
    let v0 = [one.clone(), zero.clone(), zero.clone(), zero.clone()];
    let v1 = [zero.clone(), zero.clone(), three.clone(), four.clone()];
    let g00 = dot(&v0, &v0)?;
    let g11 = dot(&v1, &v1)?;
    let g01 = dot(&v0, &v1)?;
    if g00 != one || g11 != one || g01 != zero {
        return Err("Stinespring Gram matrix is not I");
    }
    let by_squares = &three * &three + &four * &four;
    if by_squares != g11 {
        return Err("amplitude squares disagree with the Gram entry");
    }
    Ok(g11)
}

fn dot(left: &[BigRational; 4], right: &[BigRational; 4]) -> Result<BigRational, &'static str> {
    let mut acc = ratio(0, 1)?;
    for index in 0..4 {
        acc += &left[index] * &right[index];
    }
    Ok(acc)
}

fn ratio(numer: i64, denom: i64) -> Result<BigRational, &'static str> {
    if denom == 0 {
        return Err("zero denominator");
    }
    Ok(BigRational::new(BigInt::from(numer), BigInt::from(denom)))
}
