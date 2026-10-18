//! Campaign module derivation_closure.
//!
//! Differentiation on polynomials of degree at most 3. Leibniz's rule is
//! checked on a product, and the fourth derivative of a cubic is zero both
//! by iterating the derivative and by the degree drop.

pub fn verify() -> Result<Vec<i64>, &'static str> {
    let left = vec![1i64, 0, 1];
    let right = vec![2i64, 1];
    let product = poly_mul(&left, &right)?;
    let by_product = derivative(&product)?;
    let by_rule = poly_add(
        &poly_mul(&derivative(&left)?, &right)?,
        &poly_mul(&left, &derivative(&right)?)?,
    )?;
    if poly_trim(&by_product) != poly_trim(&by_rule) {
        return Err("Leibniz rule failed");
    }
    let cubic = vec![3i64, 1, 0, 2];
    let mut iterated = cubic.clone();
    for _ in 0..4 {
        iterated = derivative(&iterated)?;
    }
    let by_degree = vec![0i64];
    if poly_trim(&iterated) != by_degree {
        return Err("fourth derivative of a cubic is not zero");
    }
    Ok(poly_trim(&by_rule))
}

fn derivative(poly: &[i64]) -> Result<Vec<i64>, &'static str> {
    if poly.len() <= 1 {
        return Ok(vec![0]);
    }
    let mut out = Vec::with_capacity(poly.len() - 1);
    for (index, coeff) in poly.iter().enumerate().skip(1) {
        let factor = i64::try_from(index).map_err(|_| "degree")?;
        out.push(coeff.checked_mul(factor).ok_or("derivative")?);
    }
    Ok(out)
}

fn poly_mul(left: &[i64], right: &[i64]) -> Result<Vec<i64>, &'static str> {
    if left.is_empty() || right.is_empty() {
        return Ok(vec![0]);
    }
    let mut out = vec![0i64; left.len() + right.len() - 1];
    for (i, a) in left.iter().enumerate() {
        for (j, b) in right.iter().enumerate() {
            let term = a.checked_mul(*b).ok_or("mul")?;
            out[i + j] = out[i + j].checked_add(term).ok_or("mul")?;
        }
    }
    Ok(out)
}

fn poly_add(left: &[i64], right: &[i64]) -> Result<Vec<i64>, &'static str> {
    let n = left.len().max(right.len());
    let mut out = vec![0i64; n];
    for i in 0..n {
        let a = left.get(i).copied().unwrap_or(0);
        let b = right.get(i).copied().unwrap_or(0);
        out[i] = a.checked_add(b).ok_or("add")?;
    }
    Ok(out)
}

fn poly_trim(poly: &[i64]) -> Vec<i64> {
    let mut out = poly.to_vec();
    while out.len() > 1 && out.last() == Some(&0) {
        out.pop();
    }
    out
}
