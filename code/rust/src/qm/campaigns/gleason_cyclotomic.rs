//! Campaign module gleason_cyclotomic.
//!
//! In dimension 3 a symmetric frame assigns `1/3` to each basis vector, and
//! the three weights sum to 1. The same cyclotomic relation that makes the
//! cube roots of unity sum to zero is `(x-1)(x²+x+1) = x³-1`.

use num_bigint::BigInt;
use num_rational::BigRational;
use num_traits::One;

pub fn verify() -> Result<BigRational, &'static str> {
    let third = ratio(1, 3)?;
    let frame = &third + &third + &third;
    if frame != BigRational::one() {
        return Err("symmetric Gleason frame is not normalized");
    }
    let product = poly_mul(&[1, 1, 1], &[-1, 1])?;
    if product != vec![-1, 0, 0, 1] {
        return Err("cyclotomic factorization of x³-1 failed");
    }
    let mut coeffs = [1i64, 1, 1];
    let last = coeffs[2];
    coeffs[0] -= last;
    coeffs[1] -= last;
    coeffs[2] = 0;
    if coeffs != [0, 0, 0] {
        return Err("1+ζ+ζ² did not reduce");
    }
    Ok(frame)
}

fn ratio(numer: i64, denom: i64) -> Result<BigRational, &'static str> {
    if denom == 0 {
        return Err("zero denominator");
    }
    Ok(BigRational::new(BigInt::from(numer), BigInt::from(denom)))
}

fn poly_mul(left: &[i64], right: &[i64]) -> Result<Vec<i64>, &'static str> {
    let mut out = vec![0i64; left.len() + right.len() - 1];
    for (i, a) in left.iter().enumerate() {
        for (j, b) in right.iter().enumerate() {
            out[i + j] = out[i + j]
                .checked_add(a.checked_mul(*b).ok_or("mul")?)
                .ok_or("mul")?;
        }
    }
    Ok(out)
}
