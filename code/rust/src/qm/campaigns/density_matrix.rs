//! Campaign module density_matrix.
//!
//! The Hermitian matrix with diagonal `1/2` and off-diagonal `1/6` has trace 1
//! and positive determinant, so both eigenvalues are positive. Purity from the
//! entries equals purity from `tr² - 2 det`.

use num_bigint::BigInt;
use num_rational::BigRational;
use num_traits::{One, Zero};

pub fn verify() -> Result<BigRational, &'static str> {
    let a = ratio(1, 2)?;
    let b = ratio(1, 6)?;
    let trace = &a + &a;
    let det = &a * &a - &b * &b;
    if trace != BigRational::one() || det <= BigRational::zero() {
        return Err("matrix is not a positive trace-one state");
    }
    let by_entries = &a * &a + &b * &b + &b * &b + &a * &a;
    let by_spectrum = &trace * &trace - ratio(2, 1)? * &det;
    if by_entries != by_spectrum {
        return Err("purity readings disagree");
    }
    Ok(by_entries)
}

fn ratio(numer: i64, denom: i64) -> Result<BigRational, &'static str> {
    if denom == 0 {
        return Err("zero denominator");
    }
    Ok(BigRational::new(BigInt::from(numer), BigInt::from(denom)))
}
