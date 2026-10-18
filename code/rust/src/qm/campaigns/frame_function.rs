//! Campaign module frame_function.
//!
//! A frame function assigns `1/2, 1/3, 1/6` to one resolution of the identity
//! and the same multiset to a second resolution. Both sums equal 1, by the
//! rational sum and by the common denominator 6.

use num_bigint::BigInt;
use num_rational::BigRational;
use num_traits::One;

pub fn verify() -> Result<BigRational, &'static str> {
    let first = [ratio(1, 2)?, ratio(1, 3)?, ratio(1, 6)?];
    let second = [ratio(1, 6)?, ratio(1, 2)?, ratio(1, 3)?];
    let by_rational: BigRational = first.iter().sum();
    let by_denominator = ratio(3 + 2 + 1, 6)?;
    let second_sum: BigRational = second.iter().sum();
    if by_rational != by_denominator || second_sum != BigRational::one() {
        return Err("frame sums are not 1");
    }
    Ok(by_rational)
}

fn ratio(numer: i64, denom: i64) -> Result<BigRational, &'static str> {
    if denom == 0 {
        return Err("zero denominator");
    }
    Ok(BigRational::new(BigInt::from(numer), BigInt::from(denom)))
}
