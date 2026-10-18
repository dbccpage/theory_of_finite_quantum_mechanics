
use num_bigint::BigInt;
use num_rational::BigRational;


pub fn verify() -> Result<BigRational, &'static str> {
    let zero = ratio(0, 1)?;
    let one = ratio(1, 1)?;
    let three = ratio(3, 5)?;
    let four = ratio(4, 5)?;
    let v0 = [one.clone(), zero.clone(), zero.clone(), zero.clone()];
    let v1 = [zero.clone(), zero.clone(), three.clone(), four.clone()];
    let g00 = dot(&v0, &v0)?;
    let g11 = dot(&v1, &v1)?;
    let g01 = dot(&v0, &v1)?;
    if g00 != one || g11 != one || g01 != zero {
        return Err("Stinespring Gram matrix is not I");
    }
    let by_squares = &three * &three + &four * &four;
    if by_squares != g11 {
        return Err("amplitude squares disagree with the Gram entry");
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
