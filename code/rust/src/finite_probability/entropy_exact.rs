//! Exact rational spectrum calculations; Baker remains an explicit hypothesis.
use num_bigint::BigInt;
use num_integer::Integer;
use num_rational::BigRational as Q;
use num_traits::{One, Signed, Zero};
pub struct Term {
    pub mode: &'static str,
    pub values: Vec<Q>,
}
pub struct Certificate {
    pub spectrum: Vec<Q>,
    pub denominator: BigInt,
    pub weights: Vec<BigInt>,
    pub terms: usize,
    pub purity: Q,
    pub deficit: Q,
    pub integer_sums: Vec<BigInt>,
    pub powers: Vec<Q>,
    pub bounds: Vec<Term>,
    pub lower: Q,
    pub upper: Q,
    pub width: Q,
    pub classification: &'static str,
}
fn power(q: &Q, n: usize) -> Q {
    (0..n).fold(Q::one(), |a, _| a * q)
}
pub fn certify(p: Vec<Q>, terms: usize) -> Result<Certificate, &'static str> {
    if p.is_empty()
        || terms == 0
        || terms > 256
        || p.iter().any(|x| {
            x.is_negative() || !x.denom().is_positive() || !x.numer().gcd(x.denom()).is_one()
        })
        || p.iter().cloned().sum::<Q>() != Q::one()
    {
        return Err("normalized exact spectrum and finite positive budget required");
    }
    let denominator = p.iter().fold(BigInt::one(), |d, x| d.lcm(x.denom()));
    let weights: Vec<_> = p
        .iter()
        .map(|x| x.numer() * (&denominator / x.denom()))
        .collect();
    let purity = p.iter().map(|x| x * x).sum::<Q>();
    let deficit = Q::one() - &purity;
    let classification = if purity.is_one() { "PURE" } else { "MIXED" };
    let integer_sums = (2..=4)
        .map(|k| weights.iter().map(|w| w.pow(k)).sum())
        .collect();
    let powers = (2..=4)
        .map(|k| p.iter().map(|x| power(x, k)).sum())
        .collect();
    let mut bounds = vec![];
    let mut lower = Q::zero();
    let mut upper = Q::zero();
    for x in &p {
        if x.is_zero() {
            bounds.push(Term {
                mode: "zero_weight",
                values: vec![Q::zero(); 5],
            });
            continue;
        }
        let t = (x - Q::one()) / (x + Q::one());
        let mut s = Q::zero();
        let mut term = t.clone();
        let square = &t * &t;
        for k in 0..terms {
            s += &term / Q::from_integer((2 * k + 1).into());
            term *= &square;
        }
        s *= Q::from_integer(2.into());
        let tail = Q::from_integer(2.into()) * term.abs()
            / (Q::from_integer((2 * terms + 1).into()) * (Q::one() - &square));
        let lo = -x * &s;
        let hi = &lo + x * &tail;
        lower += &lo;
        upper += &hi;
        bounds.push(Term {
            mode: "positive_weight",
            values: vec![t, s, tail, lo, hi],
        });
    }
    let width = &upper - &lower;
    Ok(Certificate {
        spectrum: p,
        denominator,
        weights,
        terms,
        purity,
        deficit,
        integer_sums,
        powers,
        bounds,
        lower,
        upper,
        width,
        classification,
    })
}
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn natural_log_half_is_between_two_thirds_and_one() {
        let h = Q::new(1.into(), 2.into());
        let c = certify(vec![h.clone(), h], 12).unwrap();
        assert!(c.lower > Q::new(2.into(), 3.into()) && c.upper < Q::one());
        assert_eq!(c.classification, "MIXED");
    }
    #[test]
    fn zero_weight_is_never_logged() {
        let c = certify(vec![Q::zero(), Q::one()], 8).unwrap();
        assert_eq!(c.lower, Q::zero());
        assert_eq!(c.upper, Q::zero());
        assert_eq!(c.bounds[0].mode, "zero_weight");
    }
    #[test]
    fn invalid_spectrum_and_budget_refused() {
        assert!(certify(vec![Q::one(), Q::one()], 8).is_err());
        assert!(certify(vec![Q::one()], 0).is_err());
    }
}
