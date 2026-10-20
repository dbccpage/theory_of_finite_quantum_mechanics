
use num_bigint::BigInt;
use num_rational::BigRational;

pub fn verify() -> Result<BigRational, &'static str> {
    let (k0, k1) = kraus_pair()?;
    verify_kraus_completeness(&k0, &k1)?;
    let rho = sample_density()?;
    let image = apply_channel(&k0, &k1, &rho)?;
    verify_trace_preserved(&image, &rho)
}

fn verify_trace_preserved(image: &[M; 2], rho: &[M; 2]) -> Result<BigRational, &'static str> {
    let one = ratio(1, 1)?;
    let tr_img = trace(image)?;
    let tr_rho = trace(rho)?;
    if tr_img != tr_rho || tr_rho != one {
        return Err("channel did not preserve the trace");
    }
    Ok(tr_img)
}

fn kraus_pair() -> Result<([M; 2], [M; 2]), &'static str> {
    let one = ratio(1, 1)?;
    let zero = ratio(0, 1)?;
    let a = ratio(3, 5)?;
    let b = ratio(4, 5)?;
    let k0 = [row(one, zero.clone())?, row(zero.clone(), a)?];
    let k1 = [row(zero.clone(), b)?, row(zero.clone(), zero)?];
    Ok((k0, k1))
}

fn gram_term(k: &[M; 2]) -> Result<[M; 2], &'static str> {
    mat_mul(&adjoint(k)?, k)
}

fn verify_kraus_completeness(k0: &[M; 2], k1: &[M; 2]) -> Result<(), &'static str> {
    let one = ratio(1, 1)?;
    let zero = ratio(0, 1)?;
    let completeness = mat_add(&gram_term(k0)?, &gram_term(k1)?)?;
    let identity = [[one.clone(), zero.clone()], [zero, one]];
    if completeness != identity {
        return Err("Kraus operators are not complete");
    }
    Ok(())
}

fn sample_density() -> Result<[M; 2], &'static str> {
    let half = ratio(1, 2)?;
    let quarter = ratio(1, 4)?;
    Ok([row(half.clone(), quarter.clone())?, row(quarter, half)?])
}

fn apply_channel(k0: &[M; 2], k1: &[M; 2], rho: &[M; 2]) -> Result<[M; 2], &'static str> {
    let term0 = mat_mul(k0, &mat_mul(rho, &adjoint(k0)?)?)?;
    let term1 = mat_mul(k1, &mat_mul(rho, &adjoint(k1)?)?)?;
    mat_add(&term0, &term1)
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
