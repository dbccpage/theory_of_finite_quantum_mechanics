//! Campaign module everett_tree.
//!
//! A root splits into branches of weight `1/2, 1/2`, and the second branch
//! splits into `1/3` and `2/3` of its own weight. The leaf weights sum to 1,
//! and each parent's weight equals the sum of its children.

use num_bigint::BigInt;
use num_rational::BigRational;
use num_traits::One;

pub fn verify() -> Result<BigRational, &'static str> {
    let half = ratio(1, 2)?;
    let left = half.clone();
    let right_a = &half * &ratio(1, 3)?;
    let right_b = &half * &ratio(2, 3)?;
    let leaves = &left + &right_a + &right_b;
    let right = &right_a + &right_b;
    if leaves != BigRational::one() || right != half {
        return Err("branch weights do not conserve the parent");
    }
    Ok(leaves)
}

fn ratio(numer: i64, denom: i64) -> Result<BigRational, &'static str> {
    if denom == 0 {
        return Err("zero denominator");
    }
    Ok(BigRational::new(BigInt::from(numer), BigInt::from(denom)))
}
