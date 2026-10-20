
use num_bigint::BigInt;
use num_rational::BigRational;
use num_traits::{One, Zero};

fn unwind_factors(mut unwound: BigRational, factors: &[BigRational]) -> Result<BigRational, String> {
    for factor in factors.iter().rev() {
        if factor.is_zero() {
            return Err("review factor is zero".into());
        }
        unwound /= factor;
    }
    Ok(unwound)
}

pub fn run_replay_review() -> Result<(), String> {
    let factors = [ratio(2, 3)?, ratio(3, 5)?, ratio(5, 2)?, ratio(1, 1)?];
    let forward = fold_product(&factors)?;
    let mut reversed = factors.clone();
    reversed.reverse();
    let backward = fold_product(&reversed)?;
    if forward != backward {
        return Err(format!(
            "review product depends on order: {forward} vs {backward}"
        ));
    }
    let unwound = unwind_factors(forward, &factors)?;
    if unwound != BigRational::one() {
        return Err(format!("reversed inverses did not recover 1, got {unwound}"));
    }
    Ok(())
}

fn ratio(numer: i64, denom: i64) -> Result<BigRational, String> {
    if denom == 0 {
        return Err("zero denominator in review factor".into());
    }
    Ok(BigRational::new(BigInt::from(numer), BigInt::from(denom)))
}

fn fold_product(factors: &[BigRational]) -> Result<BigRational, String> {
    let mut acc = BigRational::one();
    for factor in factors {
        if factor.is_zero() {
            return Err("review factor is zero".into());
        }
        acc *= factor;
    }
    Ok(acc)
}
