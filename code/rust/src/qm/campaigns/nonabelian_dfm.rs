
pub fn verify() -> Result<usize, &'static str> {
    let r = (1u8, 0u8);
    let s = (0u8, 1u8);
    if mul(mul(s, r)?, s)? != (2u8, 0u8) {
        return Err("s r s is not r inverse");
    }
    let checked = verify_s3_associativity()?;
    if checked != 216 {
        return Err("not every triple was checked");
    }
    Ok(checked)
}

fn verify_s3_pair(a: (u8, u8), b: (u8, u8)) -> Result<usize, &'static str> {
    let ab = mul(a, b)?;
    let mut count = 0usize;
    for c in elements() {
        let left = mul(ab, c)?;
        let right = mul(a, mul(b, c)?)?;
        if left != right {
            return Err("S3 multiplication is not associative");
        }
        count += 1;
    }
    Ok(count)
}

fn verify_s3_associativity() -> Result<usize, &'static str> {
    let mut checked = 0usize;
    for a in elements() {
        for b in elements() {
            checked += verify_s3_pair(a, b)?;
        }
    }
    Ok(checked)
}

fn elements() -> [(u8, u8); 6] {
    [
        (0, 0),
        (1, 0),
        (2, 0),
        (0, 1),
        (1, 1),
        (2, 1),
    ]
}

fn mul(left: (u8, u8), right: (u8, u8)) -> Result<(u8, u8), &'static str> {
    let (i1, j1) = left;
    let (i2, j2) = right;
    if i1 > 2 || i2 > 2 || j1 > 1 || j2 > 1 {
        return Err("not an S3 element");
    }
    if j1 == 0 {
        Ok(((i1 + i2) % 3, j2))
    } else {
        let i = (i1 + (3 - i2)) % 3;
        let j = (1 + j2) % 2;
        Ok((i, j))
    }
}
