
use num_bigint::BigInt;
use num_rational::BigRational;


pub fn verify() -> Result<BigRational, &'static str> {
    let (v0, v1, by_squares) = stinespring_columns_and_squares()?;
    let g11 = verify_gram_identity(&v0, &v1)?;
    if by_squares != g11 {
        return Err("amplitude squares disagree with the Gram entry");
    }
    Ok(g11)
}

fn stinespring_columns_and_squares(
) -> Result<([BigRational; 4], [BigRational; 4], BigRational), &'static str> {
    let zero = ratio(0, 1)?;
    let one = ratio(1, 1)?;
    let three = ratio(3, 5)?;
    let four = ratio(4, 5)?;
    let by_squares = &three * &three + &four * &four;
    let v0 = [one, zero.clone(), zero.clone(), zero.clone()];
    let v1 = [zero.clone(), zero, three, four];
    Ok((v0, v1, by_squares))
}

fn verify_gram_identity(
    v0: &[BigRational; 4],
    v1: &[BigRational; 4],
) -> Result<BigRational, &'static str> {
    let zero = ratio(0, 1)?;
    let one = ratio(1, 1)?;
    let g00 = dot(v0, v0)?;
    let g11 = dot(v1, v1)?;
    let g01 = dot(v0, v1)?;
    if g00 != one || g11 != one || g01 != zero {
        return Err("Stinespring Gram matrix is not I");
    }
    Ok(g11)
}

fn dot(left: &[BigRational; 4], right: &[BigRational; 4]) -> Result<BigRational, &'static str> {
    let mut acc = ratio(0, 1)?;
    for index in 0..4 {
        acc += &left[index] * &right[index];
    }
    Ok(acc)
}

fn ratio(numer: i64, denom: i64) -> Result<BigRational, &'static str> {
    if denom == 0 {
        return Err("zero denominator");
    }
    Ok(BigRational::new(BigInt::from(numer), BigInt::from(denom)))
}
