//! Campaign module cptp_channel.
//!
//! Amplitude-damping Kraus operators with rational entries `3/5` and `4/5`.
//! Completeness `K0† K0 + K1† K1 = I` is the matrix sum, and it is also the
//! statement that the channel preserves the trace of a fixed density.

use num_bigint::BigInt;
use num_rational::BigRational;

pub fn verify() -> Result<BigRational, &'static str> {
    let one = ratio(1, 1)?;
    let zero = ratio(0, 1)?;
    let a = ratio(3, 5)?;
    let b = ratio(4, 5)?;
    let k0 = [row(one.clone(), zero.clone())?, row(zero.clone(), a.clone())?];
    let k1 = [row(zero.clone(), b.clone())?, row(zero.clone(), zero.clone())?];
    let completeness = mat_add(
        &mat_mul(&adjoint(&k0)?, &k0)?,
        &mat_mul(&adjoint(&k1)?, &k1)?,
    )?;
    let identity = [row(one.clone(), zero.clone())?, row(zero, one.clone())?];
    if completeness != identity {
        return Err("Kraus operators are not complete");
    }
    let half = ratio(1, 2)?;
    let quarter = ratio(1, 4)?;
    let rho = [row(half.clone(), quarter.clone())?, row(quarter, half)?];
    let image = mat_add(
        &mat_mul(&k0, &mat_mul(&rho, &adjoint(&k0)?)?)?,
        &mat_mul(&k1, &mat_mul(&rho, &adjoint(&k1)?)?)?,
    )?;
    if trace(&image)? != trace(&rho)? || trace(&rho)? != one {
        return Err("channel did not preserve the trace");
    }
    Ok(trace(&image)?)
}

fn ratio(numer: i64, denom: i64) -> Result<BigRational, &'static str> {
    if denom == 0 {
        return Err("zero denominator");
    }
    Ok(BigRational::new(BigInt::from(numer), BigInt::from(denom)))
}

type M = [BigRational; 2];

fn row(a: BigRational, b: BigRational) -> Result<M, &'static str> {
    Ok([a, b])
}

fn adjoint(matrix: &[M; 2]) -> Result<[M; 2], &'static str> {
    Ok([
        [matrix[0][0].clone(), matrix[1][0].clone()],
        [matrix[0][1].clone(), matrix[1][1].clone()],
    ])
}

fn mat_mul(left: &[M; 2], right: &[M; 2]) -> Result<[M; 2], &'static str> {
    let mut out = [
        [ratio(0, 1)?, ratio(0, 1)?],
        [ratio(0, 1)?, ratio(0, 1)?],
    ];
    for i in 0..2 {
        for j in 0..2 {
            out[i][j] = &left[i][0] * &right[0][j] + &left[i][1] * &right[1][j];
        }
    }
    Ok(out)
}

fn mat_add(left: &[M; 2], right: &[M; 2]) -> Result<[M; 2], &'static str> {
    Ok([
        [&left[0][0] + &right[0][0], &left[0][1] + &right[0][1]],
        [&left[1][0] + &right[1][0], &left[1][1] + &right[1][1]],
    ])
}

fn trace(matrix: &[M; 2]) -> Result<BigRational, &'static str> {
    Ok(&matrix[0][0] + &matrix[1][1])
}
