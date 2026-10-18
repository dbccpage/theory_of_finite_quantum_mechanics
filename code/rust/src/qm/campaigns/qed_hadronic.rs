//! Campaign module qed_hadronic.
//!
//! The leading hadronic `R` ratio for three colors and three light quarks is
//! `Nc Σ e_q²`. The sum of squared charges is `6/9` by fractions and `18/9`
//! after clearing the common denominator and multiplying by the colors.

use num_bigint::BigInt;
use num_rational::BigRational;

pub fn verify() -> Result<BigRational, &'static str> {
    let charges = [ratio(2, 3)?, ratio(-1, 3)?, ratio(-1, 3)?];
    let mut by_fractions = ratio(0, 1)?;
    for charge in &charges {
        by_fractions += charge * charge;
    }
    let colors = ratio(3, 1)?;
    let ratio_r = &colors * &by_fractions;
    let cleared = ratio(3 * (4 + 1 + 1), 9)?;
    if by_fractions != ratio(6, 9)? || ratio_r != cleared || ratio_r != ratio(2, 1)? {
        return Err("hadronic charge sum is not 2");
    }
    Ok(ratio_r)
}

fn ratio(numer: i64, denom: i64) -> Result<BigRational, &'static str> {
    if denom == 0 {
        return Err("zero denominator");
    }
    Ok(BigRational::new(BigInt::from(numer), BigInt::from(denom)))
}
