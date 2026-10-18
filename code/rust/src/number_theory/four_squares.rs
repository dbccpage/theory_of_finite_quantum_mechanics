
use crate::rational::Rational;
use num_bigint::BigInt;
use num_traits::{One, Signed, Zero};

#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum FourSquaresError {
    #[error("the argument is negative")]
    Negative,
    #[error("four-square search exhausted its declared budget")]
    BudgetExhausted,
    #[error("computed square decomposition failed its exact replay")]
    Replay,
}

fn charge(remaining: &mut u64) -> Result<(), FourSquaresError> {
    *remaining = remaining
        .checked_sub(1)
        .ok_or(FourSquaresError::BudgetExhausted)?;
    Ok(())
}

pub fn four_squares(n: &BigInt, budget: u64) -> Result<[BigInt; 4], FourSquaresError> {
    if n.is_negative() {
        return Err(FourSquaresError::Negative);
    }
    if budget == 0 {
        return Err(FourSquaresError::BudgetExhausted);
    }
    let mut remaining = budget;
    let mut a = n.sqrt();
    loop {
        charge(&mut remaining)?;
        let r1 = n - &a * &a;
        let mut b = r1.sqrt().min(a.clone());
        loop {
            charge(&mut remaining)?;
            let r2 = &r1 - &b * &b;
            let mut c = r2.sqrt().min(b.clone());
            loop {
                charge(&mut remaining)?;
                let r3 = &r2 - &c * &c;
                let d = r3.sqrt();
                if &d * &d == r3 && d <= c {
                    let answer = [a, b, c, d];
                    let sum: BigInt = answer.iter().map(|s| s * s).sum();
                    return if &sum == n {
                        Ok(answer)
                    } else {
                        Err(FourSquaresError::Replay)
                    };
                }
                if c.is_zero() {
                    break;
                }
                c -= BigInt::one();
            }
            if b.is_zero() {
                break;
            }
            b -= BigInt::one();
        }
        if a.is_zero() {
            return Err(FourSquaresError::Replay);
        }
        a -= BigInt::one();
    }
}

pub fn rational_square_split(
    weight: &Rational,
    budget: u64,
) -> Result<Vec<Rational>, FourSquaresError> {
    if weight.is_negative() {
        return Err(FourSquaresError::Negative);
    }
    if budget == 0 {
        return Err(FourSquaresError::BudgetExhausted);
    }
    let product = weight.numer() * weight.denom();
    let squares = four_squares(&product, budget)?;
    let coefficients: Vec<_> = squares
        .into_iter()
        .filter(|x| !x.is_zero())
        .map(|x| Rational::new(x, weight.denom().clone()))
        .collect();
    if coefficients.iter().map(|x| x * x).sum::<Rational>() != *weight {
        return Err(FourSquaresError::Replay);
    }
    Ok(coefficients)
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn all_small_integers_replay_the_four_square_identity() {
        for n in 0..150 {
            let n = BigInt::from(n);
            let s = four_squares(&n, 100_000).unwrap();
            assert_eq!(s.iter().map(|x| x * x).sum::<BigInt>(), n);
        }
    }
    #[test]
    fn rational_weights_split_without_an_extension_field() {
        for (a, b) in [(1, 3), (2, 7), (3, 4), (1, 1), (0, 1)] {
            let q = Rational::new(a.into(), b.into());
            let s = rational_square_split(&q, 100_000).unwrap();
            assert!(s.len() <= 4);
            assert_eq!(s.iter().map(|x| x * x).sum::<Rational>(), q);
        }
        assert_eq!(
            four_squares(&BigInt::from(1), 0),
            Err(FourSquaresError::BudgetExhausted)
        );
        assert_eq!(
            four_squares(&BigInt::from(-1), 100),
            Err(FourSquaresError::Negative)
        );
    }
}
