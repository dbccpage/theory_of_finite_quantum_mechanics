
use num_bigint::BigInt;
use num_rational::BigRational;

pub fn verify() -> Result<BigRational, &'static str> {
    let mut amplitudes = [0i64; 8];
    amplitudes[0] = 1;
    amplitudes[7] = 1;
    let mut reduced = [[0i64; 2]; 2];
    for a in 0..2 {
        for b in 0..2 {
            for rest in 0..4 {
                let left = amplitudes[a * 4 + rest];
                let right = amplitudes[b * 4 + rest];
                reduced[a][b] = reduced[a][b]
                    .checked_add(left.checked_mul(right).ok_or("trace")?)
                    .ok_or("trace")?;
            }
        }
    }
    if reduced != [[1, 0], [0, 1]] {
        return Err("GHZ reduction is not diagonal");
    }
    let norm = reduced[0][0].checked_add(reduced[1][1]).ok_or("norm")?;
    let sq0 = reduced[0][0].checked_mul(reduced[0][0]).ok_or("purity")?;
    let sq1 = reduced[1][1].checked_mul(reduced[1][1]).ok_or("purity")?;
    let purity_num = sq0.checked_add(sq1).ok_or("purity")?;
    let by_schmidt = ratio(purity_num, norm.checked_mul(norm).ok_or("norm")?)?;
    let by_entries = ratio(1, 2)?;
    if by_schmidt != by_entries {
        return Err("GHZ purity readings disagree");
    }
    Ok(by_schmidt)
}

fn ratio(numer: i64, denom: i64) -> Result<BigRational, &'static str> {
    if denom == 0 {
        return Err("zero denominator");
    }
    Ok(BigRational::new(BigInt::from(numer), BigInt::from(denom)))
}
