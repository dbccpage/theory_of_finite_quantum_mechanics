
use num_bigint::BigInt;
use num_rational::BigRational;
use num_traits::Zero;

pub fn run_verify_exec() -> Result<(), String> {
    let a = ratio(1, 2)?;
    let b = ratio(1, 3)?;
    let c = ratio(1, 6)?;
    let left = (&a + &b) + &c;
    let right = &a + (&b + &c);
    let scaled = &left * &ratio(6, 1)?;
    let cleared = ratio(3 + 2 + 1, 1)?;
    if left != right || scaled != cleared || left.is_zero() {
        return Err(format!(
            "execution disagreement: left {left}, right {right}, scaled {scaled}"
        ));
    }
    Ok(())
}

fn ratio(numer: i64, denom: i64) -> Result<BigRational, String> {
    if denom == 0 {
        return Err("zero denominator in exec literal".into());
    }
    Ok(BigRational::new(BigInt::from(numer), BigInt::from(denom)))
}
