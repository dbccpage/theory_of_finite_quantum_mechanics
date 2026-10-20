
use num_bigint::BigInt;
use num_rational::BigRational;
use num_traits::One;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct QubitDensity {
    pub a: (i64, i64),
    pub b: (i64, i64),
    pub c: (i64, i64),
    pub d: (i64, i64),
}

pub fn standard_qubit() -> Result<QubitDensity, &'static str> {
    Ok(QubitDensity {
        a: (1, 2),
        b: (1, 6),
        c: (1, 6),
        d: (1, 2),
    })
}

pub fn trace_and_purity(state: &QubitDensity) -> Result<(BigRational, BigRational), &'static str> {
    let a = rat(state.a)?;
    let b = rat(state.b)?;
    let c = rat(state.c)?;
    let d = rat(state.d)?;
    if b != c {
        return Err("density is not Hermitian");
    }
    let trace = &a + &d;
    let det = &a * &d - &b * &c;
    let by_spectrum = &trace * &trace - rat((2, 1))? * &det;
    let by_entries = &a * &a + &b * &c + &c * &b + &d * &d;
    if by_spectrum != by_entries {
        return Err("purity readings disagree");
    }
    Ok((trace, by_entries))
}

pub fn standard_qubit_is_a_state() -> Result<(), &'static str> {
    let (trace, purity) = trace_and_purity(&standard_qubit()?)?;
    if trace != BigRational::one() {
        return Err("trace is not 1");
    }
    let half = rat((1, 2))?;
    let sixth = rat((1, 6))?;
    let det = &half * &half - &sixth * &sixth;
    if det <= BigRational::from_integer(BigInt::from(0)) {
        return Err("determinant is not positive");
    }
    if purity != rat((5, 9))? {
        return Err("purity is not 5/9");
    }
    Ok(())
}

fn rat(pair: (i64, i64)) -> Result<BigRational, &'static str> {
    if pair.1 == 0 {
        return Err("zero denominator");
    }
    Ok(BigRational::new(BigInt::from(pair.0), BigInt::from(pair.1)))
}
