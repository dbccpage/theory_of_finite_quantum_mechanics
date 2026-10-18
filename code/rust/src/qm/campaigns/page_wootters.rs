
use num_bigint::BigInt;
use num_rational::BigRational;
use num_traits::One;

pub fn verify() -> Result<BigRational, &'static str> {
    let psi = [ratio(3, 5)?, ratio(4, 5)?];
    let mut history = [[ratio(0, 1)?, ratio(0, 1)?], [ratio(0, 1)?, ratio(0, 1)?], [ratio(0, 1)?, ratio(0, 1)?]];
    let mut state = psi.clone();
    for tick in 0..3 {
        history[tick] = state.clone();
        state = [state[1].clone(), state[0].clone()];
    }
    let conditional = &history[1];
    let flipped = [psi[1].clone(), psi[0].clone()];
    if conditional != &flipped {
        return Err("clock conditioning did not apply X");
    }
    let mut marginals = Vec::new();
    for tick in &history {
        marginals.push(&tick[0] * &tick[0] + &tick[1] * &tick[1]);
    }
    let stationary = marginals.first().ok_or("empty")?;
    if marginals.iter().any(|weight| weight != stationary) {
        return Err("clock marginals are not stationary");
    }
    let total: BigRational = marginals.iter().sum();
    let norm = &psi[0] * &psi[0] + &psi[1] * &psi[1];
    if total != &norm * &ratio(3, 1)? || norm != BigRational::one() {
        return Err("history norm is not three copies of the system norm");
    }
    Ok(total)
}

fn ratio(numer: i64, denom: i64) -> Result<BigRational, &'static str> {
    if denom == 0 {
        return Err("zero denominator");
    }
    Ok(BigRational::new(BigInt::from(numer), BigInt::from(denom)))
}
