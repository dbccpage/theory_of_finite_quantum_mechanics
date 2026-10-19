//! Exact rational matrices for retained finite certificates. AuthorityEffect: None.
use num_integer::Integer;
use num_rational::BigRational as Q;
use num_traits::{One, Signed, Zero};
pub type Matrix = Vec<Vec<Q>>;
pub type Result<T> = std::result::Result<T, &'static str>;

pub fn validate(a: &Matrix) -> Result<()> {
    if a.is_empty() || a[0].is_empty() || a.iter().any(|r| r.len() != a[0].len()) {
        return Err("nonempty rectangular matrix required");
    }
    if a.iter()
        .flatten()
        .any(|q| !q.denom().is_positive() || !q.numer().gcd(q.denom()).is_one())
    {
        return Err("canonical rational entries required");
    }
    Ok(())
}
pub fn eye(n: usize) -> Matrix {
    (0..n)
        .map(|i| {
            (0..n)
                .map(|j| if i == j { Q::one() } else { Q::zero() })
                .collect()
        })
        .collect()
}
pub fn transpose(a: &Matrix) -> Result<Matrix> {
    validate(a)?;
    Ok((0..a[0].len())
        .map(|j| a.iter().map(|r| r[j].clone()).collect())
        .collect())
}
pub fn scale(c: &Q, a: &Matrix) -> Result<Matrix> {
    validate(a)?;
    if !c.denom().is_positive() || !c.numer().gcd(c.denom()).is_one() {
        return Err("canonical rational scalar required");
    }
    Ok(a.iter()
        .map(|r| r.iter().map(|q| c * q).collect())
        .collect())
}
pub fn add(a: &Matrix, b: &Matrix) -> Result<Matrix> {
    validate(a)?;
    validate(b)?;
    if (a.len(), a[0].len()) != (b.len(), b[0].len()) {
        return Err("matrix shape mismatch");
    }
    Ok(a.iter()
        .zip(b)
        .map(|(r, s)| r.iter().zip(s).map(|(x, y)| x + y).collect())
        .collect())
}
pub fn multiply(a: &Matrix, b: &Matrix) -> Result<Matrix> {
    validate(a)?;
    validate(b)?;
    if a[0].len() != b.len() {
        return Err("matrix product shape mismatch");
    }
    Ok((0..a.len())
        .map(|i| {
            (0..b[0].len())
                .map(|j| (0..b.len()).map(|k| &a[i][k] * &b[k][j]).sum())
                .collect()
        })
        .collect())
}
pub fn tensor(a: &Matrix, b: &Matrix) -> Result<Matrix> {
    validate(a)?;
    validate(b)?;
    Ok(a.iter()
        .flat_map(|r| {
            b.iter().map(move |s| {
                r.iter()
                    .flat_map(|x| s.iter().map(move |y| x * y))
                    .collect()
            })
        })
        .collect())
}
pub fn trace(a: &Matrix) -> Result<Q> {
    validate(a)?;
    if a.len() != a[0].len() {
        return Err("square matrix required");
    }
    Ok((0..a.len()).map(|i| a[i][i].clone()).sum())
}
pub fn determinant(a: &Matrix) -> Result<Q> {
    validate(a)?;
    if a.len() != a[0].len() {
        return Err("square matrix required");
    }
    let mut a = a.clone();
    let mut det = Q::one();
    for j in 0..a.len() {
        let Some(p) = (j..a.len()).find(|&i| !a[i][j].is_zero()) else {
            return Ok(Q::zero());
        };
        if p != j {
            a.swap(j, p);
            det = -det;
        }
        let c = a[j][j].clone();
        det *= &c;
        for i in j + 1..a.len() {
            let f = &a[i][j] / &c;
            for k in j + 1..a.len() {
                let term = &f * &a[j][k];
                a[i][k] -= term;
            }
        }
    }
    Ok(det)
}
pub fn is_psd(a: &Matrix) -> Result<bool> {
    if a != &transpose(a)? {
        return Err("symmetric matrix required");
    }
    if a.len() > 16 {
        return Err("principal-minor checker limited to dimension 16");
    }
    for mask in 1..(1usize << a.len()) {
        let indices: Vec<_> = (0..a.len()).filter(|i| mask & (1 << i) != 0).collect();
        let minor = indices
            .iter()
            .map(|&i| indices.iter().map(|&j| a[i][j].clone()).collect())
            .collect();
        if determinant(&minor)?.is_negative() {
            return Ok(false);
        }
    }
    Ok(true)
}
