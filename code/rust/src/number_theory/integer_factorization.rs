use num_bigint::{BigInt, BigUint};
use num_integer::Integer;
use num_traits::{One, ToPrimitive, Zero};
use std::collections::BTreeMap;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct FactorizationBudget {
    pub max_operations: u64,
}
impl Default for FactorizationBudget {
    fn default() -> Self {
        Self {
            max_operations: 1_000_000,
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum FactorizationError {
    #[error("a strictly positive integer is required")]
    NonPositive,
    #[error("exact factorisation exhausted its {limit} operation budget")]
    Exhausted { limit: u64 },
    #[error("the multiplicity of prime {prime} exceeds the u32 result carrier")]
    MultiplicityOverflow { prime: BigUint },
}

fn record_factor(
    factors: &mut BTreeMap<BigUint, u32>,
    prime: BigUint,
) -> Result<(), FactorizationError> {
    let multiplicity = factors.entry(prime.clone()).or_default();
    *multiplicity = multiplicity
        .checked_add(1)
        .ok_or(FactorizationError::MultiplicityOverflow { prime })?;
    Ok(())
}

struct Work {
    remaining: u64,
    limit: u64,
}
impl Work {
    fn step(&mut self) -> Result<(), FactorizationError> {
        if self.remaining == 0 {
            return Err(FactorizationError::Exhausted { limit: self.limit });
        }
        self.remaining -= 1;
        Ok(())
    }
    fn pow_mod(&mut self, mut a: u64, mut e: u64, n: u64) -> Result<u64, FactorizationError> {
        let mut result = 1;
        while e != 0 {
            self.step()?;
            if e & 1 == 1 {
                result = ((u128::from(result) * u128::from(a)) % u128::from(n)) as u64;
            }
            e >>= 1;
            if e != 0 {
                a = ((u128::from(a) * u128::from(a)) % u128::from(n)) as u64;
            }
        }
        Ok(result)
    }
    fn miller_rabin_witness(
        &mut self,
        a: u64,
        d: u64,
        s: u32,
        n: u64,
    ) -> Result<bool, FactorizationError> {
        if a % n == 0 {
            return Ok(false);
        }
        let mut x = self.pow_mod(a % n, d, n)?;
        if x == 1 || x == n - 1 {
            return Ok(false);
        }
        for _ in 1..s {
            self.step()?;
            x = ((u128::from(x) * u128::from(x)) % u128::from(n)) as u64;
            if x == n - 1 {
                return Ok(false);
            }
        }
        Ok(true)
    }

    fn prime64(&mut self, n: u64) -> Result<bool, FactorizationError> {
        self.step()?;
        if n < 2 {
            return Ok(false);
        }
        for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37] {
            self.step()?;
            if n == p {
                return Ok(true);
            }
            if n % p == 0 {
                return Ok(false);
            }
        }
        let s = (n - 1).trailing_zeros();
        let d = (n - 1) >> s;
        for a in [2, 325, 9375, 28178, 450775, 9780504, 1795265022] {
            if self.miller_rabin_witness(a, d, s, n)? {
                return Ok(false);
            }
        }
        Ok(true)
    }
    fn split64(&mut self, n: u64) -> Result<u64, FactorizationError> {
        for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37] {
            if n % p == 0 {
                return Ok(p);
            }
        }
        let modulus = u128::from(n);
        for seed in 1..=64u64 {
            let f = |x: u64| ((u128::from(x) * u128::from(x) + u128::from(seed)) % modulus) as u64;
            let (mut x, mut y, mut gcd) = (2, 2, 1);
            while gcd == 1 {
                self.step()?;
                x = f(x);
                y = f(f(y));
                gcd = x.abs_diff(y).gcd(&n);
            }
            if gcd != n {
                return Ok(gcd);
            }
        }
        let mut d = 41;
        while d <= n / d {
            self.step()?;
            if n % d == 0 {
                return Ok(d);
            }
            d += 2;
        }
        Ok(n)
    }
    fn factor64(
        &mut self,
        n: u64,
        out: &mut BTreeMap<BigUint, u32>,
    ) -> Result<(), FactorizationError> {
        if n == 1 {
            return Ok(());
        }
        if self.prime64(n)? {
            return record_factor(out, BigUint::from(n));
        }
        let d = self.split64(n)?;
        self.factor64(d, out)?;
        self.factor64(n / d, out)
    }
}

pub fn factor_natural(
    value: &BigUint,
    budget: FactorizationBudget,
) -> Result<BTreeMap<BigUint, u32>, FactorizationError> {
    if value.is_zero() {
        return Err(FactorizationError::NonPositive);
    }
    let mut work = Work {
        remaining: budget.max_operations,
        limit: budget.max_operations,
    };
    factor_with_work(value, &mut work)
}

fn strip_divisor_factor(
    rest: &mut BigUint,
    d: &BigUint,
    factors: &mut BTreeMap<BigUint, u32>,
    work: &mut Work,
) -> Result<(), FactorizationError> {
    while (&*rest % d).is_zero() {
        work.step()?;
        *rest /= d;
        record_factor(factors, d.clone())?;
    }
    Ok(())
}

fn factor_with_work(
    value: &BigUint,
    work: &mut Work,
) -> Result<BTreeMap<BigUint, u32>, FactorizationError> {
    let mut factors = BTreeMap::new();
    let mut rest = value.clone();
    let mut d = BigUint::from(2u8);
    while rest > BigUint::one() {
        if let Some(n) = rest.to_u64() {
            work.factor64(n, &mut factors)?;
            return Ok(factors);
        }
        work.step()?;
        if &d * &d > rest {
            record_factor(&mut factors, rest)?;
            return Ok(factors);
        }
        strip_divisor_factor(&mut rest, &d, &mut factors, work)?;
        d += if d == BigUint::from(2u8) { 1u8 } else { 2u8 };
    }
    Ok(factors)
}

pub fn factor_integer(
    value: &BigInt,
    budget: FactorizationBudget,
) -> Result<BTreeMap<BigUint, u32>, FactorizationError> {
    let value = value
        .to_biguint()
        .filter(|v| !v.is_zero())
        .ok_or(FactorizationError::NonPositive)?;
    factor_natural(&value, budget)
}

pub fn is_prime_u64(n: u64, budget: FactorizationBudget) -> Result<bool, FactorizationError> {
    Work {
        remaining: budget.max_operations,
        limit: budget.max_operations,
    }
    .prime64(n)
}

pub fn factor_positive_rational(
    value: &num_rational::BigRational,
    budget: FactorizationBudget,
) -> Result<BTreeMap<BigUint, i64>, FactorizationError> {
    let numerator = value
        .numer()
        .to_biguint()
        .filter(|n| !n.is_zero())
        .ok_or(FactorizationError::NonPositive)?;
    let denominator = value
        .denom()
        .to_biguint()
        .ok_or(FactorizationError::NonPositive)?;
    let mut work = Work {
        remaining: budget.max_operations,
        limit: budget.max_operations,
    };
    let positive = factor_with_work(&numerator, &mut work)?;
    let negative = factor_with_work(&denominator, &mut work)?;
    let mut factors: BTreeMap<BigUint, i64> = positive
        .into_iter()
        .map(|(p, e)| (p, i64::from(e)))
        .collect();
    for (p, e) in negative {
        *factors.entry(p).or_default() -= i64::from(e);
    }
    factors.retain(|_, e| *e != 0);
    Ok(factors)
}
