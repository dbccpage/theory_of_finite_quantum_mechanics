//! Campaign module quadratic_readout.
//!
//! A symmetric integer form `x ↦ x^T A x`. The polarization identity
//! `f(x+y) - f(x-y) = 4 x^T A y` is checked against the bilinear readout.

pub fn verify() -> Result<i64, &'static str> {
    let form = [[2i64, 1], [1, 3]];
    let x = [1i64, 0];
    let y = [1i64, 1];
    let plus = [x[0] + y[0], x[1] + y[1]];
    let minus = [x[0] - y[0], x[1] - y[1]];
    let polarized = quadratic(&form, &plus)?.checked_sub(quadratic(&form, &minus)?).ok_or("sub")?;
    let bilinear = 4i64
        .checked_mul(dot(&x, &apply(&form, &y)?)?)
        .ok_or("scale")?;
    if polarized != bilinear {
        return Err("polarization identity failed");
    }
    Ok(polarized)
}

fn quadratic(form: &[[i64; 2]; 2], vector: &[i64; 2]) -> Result<i64, &'static str> {
    dot(vector, &apply(form, vector)?)
}

fn apply(form: &[[i64; 2]; 2], vector: &[i64; 2]) -> Result<[i64; 2], &'static str> {
    Ok([
        form[0][0]
            .checked_mul(vector[0])
            .and_then(|v| form[0][1].checked_mul(vector[1]).and_then(|t| v.checked_add(t)))
            .ok_or("apply")?,
        form[1][0]
            .checked_mul(vector[0])
            .and_then(|v| form[1][1].checked_mul(vector[1]).and_then(|t| v.checked_add(t)))
            .ok_or("apply")?,
    ])
}

fn dot(left: &[i64; 2], right: &[i64; 2]) -> Result<i64, &'static str> {
    left[0]
        .checked_mul(right[0])
        .and_then(|v| left[1].checked_mul(right[1]).and_then(|t| v.checked_add(t)))
        .ok_or("dot")
}
