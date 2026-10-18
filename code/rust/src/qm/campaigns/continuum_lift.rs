//! Campaign module continuum_lift.
//!
//! The quadratic samples `0, 1, 4, 9` have constant second difference 2.
//! Newton's binomial series from those differences reproduces the last sample.

pub fn verify() -> Result<i64, &'static str> {
    let samples = [0i64, 1, 4, 9];
    let first = differences(&samples)?;
    let second = differences(&first)?;
    let third = differences(&second)?;
    if second.iter().any(|value| *value != 2) || third.iter().any(|value| *value != 0) {
        return Err("second difference of n² is not the constant 2");
    }
    let lifted = newton(&samples, 3)?;
    if lifted != samples[3] {
        return Err("Newton lift missed the sample");
    }
    Ok(lifted)
}

fn differences(values: &[i64]) -> Result<Vec<i64>, &'static str> {
    if values.len() < 2 {
        return Err("need two samples");
    }
    let mut out = Vec::with_capacity(values.len() - 1);
    for pair in values.windows(2) {
        out.push(pair[1].checked_sub(pair[0]).ok_or("difference overflow")?);
    }
    Ok(out)
}

fn newton(samples: &[i64], at: usize) -> Result<i64, &'static str> {
    let d0 = samples[0];
    let d1 = samples[1].checked_sub(samples[0]).ok_or("diff")?;
    let d2_a = samples[2].checked_sub(samples[1]).ok_or("diff")?;
    let d2 = d2_a.checked_sub(d1).ok_or("diff")?;
    let binom1 = i64::try_from(at).map_err(|_| "index")?;
    let binom2 = binom1
        .checked_mul(binom1.checked_sub(1).ok_or("binom")?)
        .ok_or("binom")?
        / 2;
    let term1 = binom1.checked_mul(d1).ok_or("term")?;
    let term2 = binom2.checked_mul(d2).ok_or("term")?;
    d0.checked_add(term1).and_then(|v| v.checked_add(term2)).ok_or("newton")
}
