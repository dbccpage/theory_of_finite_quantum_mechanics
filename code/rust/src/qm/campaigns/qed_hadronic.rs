
use num_bigint::BigInt;
use num_rational::BigRational;

pub fn verify() -> Result<BigRational, &'static str> {
    let by_fractions = quark_charge_squares_sum()?;
    let colors = ratio(3, 1)?;
    let ratio_r = &colors * &by_fractions;
    let cleared = ratio(3 * (4 + 1 + 1), 9)?;
    if by_fractions != ratio(6, 9)? || ratio_r != cleared || ratio_r != ratio(2, 1)? {
        return Err("hadronic charge sum is not 2");
    }
    Ok(ratio_r)
}

fn quark_charge_squares_sum() -> Result<BigRational, &'static str> {
    let q_up = ratio(2, 3)?;
    let q_down = ratio(-1, 3)?;
    let mut sum = ratio(0, 1)?;
    for charge in [&q_up, &q_down, &q_down] {
        sum += charge * charge;
    }
    Ok(sum)
}

fn ratio(numer: i64, denom: i64) -> Result<BigRational, &'static str> {
    if denom == 0 {
        return Err("zero denominator");
    }
    Ok(BigRational::new(BigInt::from(numer), BigInt::from(denom)))
}
