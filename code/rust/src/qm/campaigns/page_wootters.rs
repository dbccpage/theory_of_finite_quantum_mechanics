
use num_bigint::BigInt;
use num_rational::BigRational;
use num_traits::One;

pub fn verify() -> Result<BigRational, &'static str> {
    let psi = [ratio(3, 5)?, ratio(4, 5)?];
    let history = build_clock_history(&psi)?;
    let total = verify_stationary_marginals(&history)?;
    let norm = &psi[0] * &psi[0] + &psi[1] * &psi[1];
    if total != &norm * &ratio(3, 1)? || norm != BigRational::one() {
        return Err("history norm is not three copies of the system norm");
    }
    Ok(total)
}

fn build_clock_history(psi: &[BigRational; 2]) -> Result<[[BigRational; 2]; 3], &'static str> {
    let zero = ratio(0, 1)?;
    let mut history = [
        [zero.clone(), zero.clone()],
        [zero.clone(), zero.clone()],
        [zero.clone(), zero],
    ];
    let mut state = psi.clone();
    for slot in &mut history {
        *slot = state.clone();
        state = [state[1].clone(), state[0].clone()];
    }
    let flipped = [psi[1].clone(), psi[0].clone()];
    if history[1] != flipped {
        return Err("clock conditioning did not apply X");
    }
    Ok(history)
}

fn verify_stationary_marginals(history: &[[BigRational; 2]; 3]) -> Result<BigRational, &'static str> {
    let mut marginals = Vec::with_capacity(3);
    for tick in history {
        marginals.push(&tick[0] * &tick[0] + &tick[1] * &tick[1]);
    }
    let stationary = marginals.first().ok_or("empty")?;
    if marginals.iter().any(|weight| weight != stationary) {
        return Err("clock marginals are not stationary");
    }
    Ok(marginals.into_iter().sum())
}

fn ratio(numer: i64, denom: i64) -> Result<BigRational, &'static str> {
    if denom == 0 {
        return Err("zero denominator");
    }
    Ok(BigRational::new(BigInt::from(numer), BigInt::from(denom)))
}
