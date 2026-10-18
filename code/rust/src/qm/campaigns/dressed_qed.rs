//! Campaign module dressed_qed.
//!
//! A one-loop dressing with vacuum polarization `Π = 1/10`. The dressed
//! coupling is `e0² / (1 - Π)`, and multiplying back by `1 - Π` recovers the
//! bare coupling. The same quotient is `Z3 e0²` with `Z3 = 1/(1-Π)`.

use num_bigint::BigInt;
use num_rational::BigRational;
use num_traits::Zero;

pub fn verify() -> Result<BigRational, &'static str> {
    let bare = ratio(1, 137)?;
    let pi = ratio(1, 10)?;
    let one = ratio(1, 1)?;
    let residue = &one - &pi;
    if residue.is_zero() {
        return Err("polarization saturated the propagator");
    }
    let dressed = &bare / &residue;
    let recovered = &dressed * &residue;
    let z3 = &one / &residue;
    let by_factor = &z3 * &bare;
    if recovered != bare || by_factor != dressed {
        return Err("dressed coupling does not undo");
    }
    Ok(dressed)
}

fn ratio(numer: i64, denom: i64) -> Result<BigRational, &'static str> {
    if denom == 0 {
        return Err("zero denominator");
    }
    Ok(BigRational::new(BigInt::from(numer), BigInt::from(denom)))
}
