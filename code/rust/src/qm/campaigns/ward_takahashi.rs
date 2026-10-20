
use num_bigint::BigInt;
use num_rational::BigRational;

pub fn verify() -> Result<BigRational, &'static str> {
    let s0 = sample_triple((2, 1), (3, 2), (-1, 4))?;
    let s1 = sample_triple((-5, 3), (1, 6), (2, 1))?;
    for (momentum, transfer, mass) in [s0, s1] {
        verify_ward_sample(&momentum, &transfer, &mass)?;
    }
    ratio(1, 1)
}

fn sample_triple(
    p: (i64, i64),
    q: (i64, i64),
    m: (i64, i64),
) -> Result<(BigRational, BigRational, BigRational), &'static str> {
    Ok((ratio(p.0, p.1)?, ratio(q.0, q.1)?, ratio(m.0, m.1)?))
}

fn verify_ward_sample(
    momentum: &BigRational,
    transfer: &BigRational,
    mass: &BigRational,
) -> Result<(), &'static str> {
    let left = inverse(&(momentum + transfer), mass)? - inverse(momentum, mass)?;
    let cancelled = (momentum + transfer - mass) - (momentum - mass);
    if &left != transfer || &cancelled != transfer {
        return Err("Ward identity failed");
    }
    Ok(())
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
