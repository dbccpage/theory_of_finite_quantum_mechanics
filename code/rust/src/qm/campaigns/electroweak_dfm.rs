
use num_bigint::BigInt;
use num_rational::BigRational;
use num_traits::One;

pub fn verify() -> Result<BigRational, &'static str> {
    let particles = electroweak_particles()?;
    verify_gell_mann_nishijima(&particles)?;
    let up_minus_down = &particles[2].2 - &particles[3].2;
    let t3_split = &particles[2].0 - &particles[3].0;
    if up_minus_down != t3_split || up_minus_down != BigRational::one() {
        return Err("doublet splitting is not 1");
    }
    Ok(up_minus_down)
}

fn particle(
    t3: (i64, i64),
    hyper: (i64, i64),
    charge: (i64, i64),
) -> Result<(BigRational, BigRational, BigRational), &'static str> {
    Ok((ratio(t3.0, t3.1)?, ratio(hyper.0, hyper.1)?, ratio(charge.0, charge.1)?))
}

fn electroweak_particles(
) -> Result<[(BigRational, BigRational, BigRational); 4], &'static str> {
    Ok([
        particle((1, 2), (-1, 1), (0, 1))?,
        particle((-1, 2), (-1, 1), (-1, 1))?,
        particle((1, 2), (1, 3), (2, 3))?,
        particle((-1, 2), (1, 3), (-1, 3))?,
    ])
}

fn verify_gell_mann_nishijima(
    particles: &[(BigRational, BigRational, BigRational)],
) -> Result<(), &'static str> {
    let two = ratio(2, 1)?;
    for (t3, hyper, charge) in particles {
        let predicted = t3 + hyper / &two;
        if &predicted != charge {
            return Err("Q is not T3 + Y/2");
        }
    }
    Ok(())
}

fn ratio(numer: i64, denom: i64) -> Result<BigRational, &'static str> {
    if denom == 0 {
        return Err("zero denominator");
    }
    Ok(BigRational::new(BigInt::from(numer), BigInt::from(denom)))
}
