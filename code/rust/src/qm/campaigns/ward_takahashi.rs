
use num_bigint::BigInt;
use num_rational::BigRational;

pub fn verify() -> Result<BigRational, &'static str> {
    let samples = [(ratio(2, 1)?, ratio(3, 2)?, ratio(-1, 4)?), (ratio(-5, 3)?, ratio(1, 6)?, ratio(2, 1)?)];
    for (momentum, transfer, mass) in samples {
        let left = inverse(&(&momentum + &transfer), &mass)? - inverse(&momentum, &mass)?;
        let cancelled = (&momentum + &transfer - &mass) - (&momentum - &mass);
        if left != transfer || cancelled != transfer {
            return Err("Ward identity failed");
        }
    }
    Ok(ratio(1, 1)?)
}

fn inverse(momentum: &BigRational, mass: &BigRational) -> Result<BigRational, &'static str> {
    Ok(momentum - mass)
}

fn ratio(numer: i64, denom: i64) -> Result<BigRational, &'static str> {
    if denom == 0 {
        return Err("zero denominator");
    }
    Ok(BigRational::new(BigInt::from(numer), BigInt::from(denom)))
}
