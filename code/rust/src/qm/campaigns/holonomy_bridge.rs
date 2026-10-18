//! Campaign module holonomy_bridge.
//!
//! The modular generators `S` and `T` satisfy `S² = -I` and `(ST)³ = -I`.
//! Each identity is a matrix product, and `S⁴` is the identity by squaring
//! `S²` a second time.

pub fn verify() -> Result<[[i64; 2]; 2], &'static str> {
    let s = [[0i64, -1], [1, 0]];
    let t = [[1i64, 1], [0, 1]];
    let minus = [[-1i64, 0], [0, -1]];
    let s2 = mat_mul(&s, &s)?;
    if s2 != minus {
        return Err("S² is not -I");
    }
    let s4 = mat_mul(&s2, &s2)?;
    if s4 != [[1, 0], [0, 1]] {
        return Err("S⁴ is not I");
    }
    let st = mat_mul(&s, &t)?;
    let st2 = mat_mul(&st, &st)?;
    let st3 = mat_mul(&st2, &st)?;
    if st3 != minus {
        return Err("(ST)³ is not -I");
    }
    Ok(st3)
}

fn mat_mul(left: &[[i64; 2]; 2], right: &[[i64; 2]; 2]) -> Result<[[i64; 2]; 2], &'static str> {
    let mut out = [[0i64; 2]; 2];
    for i in 0..2 {
        for j in 0..2 {
            let mut slot = 0i64;
            for k in 0..2 {
                slot = slot
                    .checked_add(left[i][k].checked_mul(right[k][j]).ok_or("mul")?)
                    .ok_or("mul")?;
            }
            out[i][j] = slot;
        }
    }
    Ok(out)
}
