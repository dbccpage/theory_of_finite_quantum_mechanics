//! Campaign module contextuality_f2.
//!
//! The five-cycle exclusivity graph has independence number 2, by exhaustive
//! search of its 32 vertex subsets. The fractional assignment `1/2` on every
//! vertex sums to `5/2` and puts mass 1 on every edge, so the `F_2` packing
//! bound is not the fractional one.

use num_bigint::BigInt;
use num_rational::BigRational;

pub fn verify() -> Result<(usize, BigRational), &'static str> {
    let independence = max_independent_set()?;
    let fractional = ratio(5, 2)?;
    let edge = ratio(1, 2)? + ratio(1, 2)?;
    if independence != 2 || edge != ratio(1, 1)? || fractional <= ratio(independence as i64, 1)? {
        return Err("C5 exclusivity did not separate the integer and fractional bounds");
    }
    Ok((independence, fractional))
}

fn max_independent_set() -> Result<usize, &'static str> {
    let mut best = 0usize;
    for mask in 0..32u32 {
        let mut ok = true;
        let mut size = 0usize;
        for vertex in 0..5 {
            if (mask >> vertex) & 1 == 1 {
                size += 1;
                let neighbor = (vertex + 1) % 5;
                if (mask >> neighbor) & 1 == 1 {
                    ok = false;
                }
            }
        }
        if ok && size > best {
            best = size;
        }
    }
    Ok(best)
}

fn ratio(numer: i64, denom: i64) -> Result<BigRational, &'static str> {
    if denom == 0 {
        return Err("zero denominator");
    }
    Ok(BigRational::new(BigInt::from(numer), BigInt::from(denom)))
}
