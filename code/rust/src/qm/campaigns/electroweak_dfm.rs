//! Campaign module electroweak_dfm.
//!
//! Electric charge `Q = T3 + Y/2` on the lepton and quark doublets. Each
//! charge is checked from the formula, and the doublet splitting `Q_up - Q_down`
//! equals the `T3` splitting because the hypercharges match.

use num_bigint::BigInt;
use num_rational::BigRational;
use num_traits::One;

pub fn verify() -> Result<BigRational, &'static str> {
    let particles = [
        (ratio(1, 2)?, ratio(-1, 1)?, ratio(0, 1)?),
        (ratio(-1, 2)?, ratio(-1, 1)?, ratio(-1, 1)?),
        (ratio(1, 2)?, ratio(1, 3)?, ratio(2, 3)?),
        (ratio(-1, 2)?, ratio(1, 3)?, ratio(-1, 3)?),
    ];
    for (t3, hyper, charge) in &particles {
        let predicted = t3 + hyper / ratio(2, 1)?;
        if &predicted != charge {
            return Err("Q is not T3 + Y/2");
        }
    }
    let up_minus_down = &particles[2].2 - &particles[3].2;
    let t3_split = &particles[2].0 - &particles[3].0;
    if up_minus_down != t3_split || up_minus_down != BigRational::one() {
        return Err("doublet splitting is not 1");
    }
    Ok(up_minus_down)
}

fn ratio(numer: i64, denom: i64) -> Result<BigRational, &'static str> {
    if denom == 0 {
        return Err("zero denominator");
    }
    Ok(BigRational::new(BigInt::from(numer), BigInt::from(denom)))
}
