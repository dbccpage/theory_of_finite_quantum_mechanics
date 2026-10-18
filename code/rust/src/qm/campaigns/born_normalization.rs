//! Campaign module born_normalization.
//!
//! A diagonal rational state with entries `1/2, 1/2` has trace 1. Its purity
//! is the sum of squares of the diagonal and the sum of squares of the
//! eigenvalues, both `1/2`.

use num_bigint::BigInt;
use num_rational::BigRational;
use num_traits::One;

pub fn verify() -> Result<BigRational, &'static str> {
    let half = ratio(1, 2)?;
    let weights = [half.clone(), half];
    let trace: BigRational = weights.iter().sum();
    if trace != BigRational::one() {
        return Err("Born weights do not sum to 1");
    }
    let by_entries: BigRational = weights.iter().map(|p| p * p).sum();
    let by_spectrum = &weights[0] * &weights[0] + &weights[1] * &weights[1];
    if by_entries != by_spectrum || by_entries != ratio(1, 2)? {
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
