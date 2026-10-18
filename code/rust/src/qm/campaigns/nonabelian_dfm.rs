//! Campaign module nonabelian_dfm.
//!
//! `S3` as the semidirect product `C3 ⋊ C2`, with `s r s^{-1} = r^{-1}`.
//! The relation is the multiplication table, and every triple associates.

pub fn verify() -> Result<usize, &'static str> {
    let r = (1u8, 0u8);
    let s = (0u8, 1u8);
    let srs = mul(mul(s, r)?, s)?;
    let r_inv = (2u8, 0u8);
    if srs != r_inv {
        return Err("s r s is not r inverse");
    }
    let mut checked = 0usize;
    for a in elements() {
        for b in elements() {
            for c in elements() {
                let left = mul(mul(a, b)?, c)?;
                let right = mul(a, mul(b, c)?)?;
                if left != right {
                    return Err("S3 multiplication is not associative");
                }
                checked += 1;
            }
        }
    }
    if checked != 216 {
        return Err("not every triple was checked");
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
