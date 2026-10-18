//! Campaign module interference.
//!
//! Two rational amplitudes. The probability of the sum expands as
//! `|a|² + |b|² + 2ab`, and that expansion equals `(a+b)²`. The cross term
//! is what the incoherent sum leaves out.

use num_bigint::BigInt;
use num_rational::BigRational;

pub fn verify() -> Result<BigRational, &'static str> {
    let a = ratio(3, 5)?;
    let b = ratio(-4, 5)?;
    let coherent = (&a + &b) * (&a + &b);
    let expanded = &a * &a + &b * &b + ratio(2, 1)? * &a * &b;
    let incoherent = &a * &a + &b * &b;
    if coherent != expanded {
        return Err("interference expansion failed");
    }
    if expanded == incoherent {
        return Err("cross term vanished");
    }
    let cross = &expanded - &incoherent;
    if cross != ratio(2, 1)? * &a * &b {
        return Err("cross term is not 2ab");
    }
    Ok(coherent)
}

fn ratio(numer: i64, denom: i64) -> Result<BigRational, &'static str> {
    if denom == 0 {
        return Err("zero denominator");
    }
    Ok(BigRational::new(BigInt::from(numer), BigInt::from(denom)))
}
