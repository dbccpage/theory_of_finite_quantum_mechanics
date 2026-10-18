
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct CyclotomicTower {
    pub conductor: usize,
    pub degree: usize,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct CyclotomicCoeffs {
    pub conductor: usize,
    pub coeffs: Vec<i64>,
}

impl CyclotomicTower {
    pub fn new(conductor: usize) -> Result<Self, &'static str> {
        let degree = euler_totient(conductor)?;
        Ok(Self { conductor, degree })
    }
}

impl CyclotomicCoeffs {
    pub fn try_new(conductor: usize, coeffs: Vec<i64>) -> Result<Self, &'static str> {
        if conductor == 0 || coeffs.len() != conductor {
            return Err("cyclotomic coefficient length must equal the conductor");
        }
        Ok(Self { conductor, coeffs })
    }

    pub fn add(&self, other: &Self) -> Result<Self, &'static str> {
        if self.conductor != other.conductor || self.coeffs.len() != other.coeffs.len() {
            return Err("cyclotomic conductors differ");
        }
        let mut coeffs = Vec::with_capacity(self.coeffs.len());
        for (left, right) in self.coeffs.iter().zip(other.coeffs.iter()) {
            coeffs.push(
                left.checked_add(*right)
                    .ok_or("cyclotomic coefficient overflow")?,
            );
        }
        Ok(Self {
            conductor: self.conductor,
            coeffs,
        })
    }

    pub fn reduce_prime(&self) -> Result<Self, &'static str> {
        let p = self.conductor;
        if p < 2 || !is_prime(p) || self.coeffs.len() != p {
            return Err("reduction requires a prime conductor");
        }
        let last = self.coeffs[p - 1];
        let mut coeffs = vec![0i64; p];
        for i in 0..(p - 1) {
            coeffs[i] = self.coeffs[i]
                .checked_sub(last)
                .ok_or("cyclotomic reduction overflow")?;
        }
        Ok(Self {
            conductor: p,
            coeffs,
        })
    }
}

pub fn prime_relation_vanishes() -> Result<(), &'static str> {
    let one = CyclotomicCoeffs::try_new(3, vec![1, 0, 0])?;
    let zeta = CyclotomicCoeffs::try_new(3, vec![0, 1, 0])?;
    let zeta2 = CyclotomicCoeffs::try_new(3, vec![0, 0, 1])?;
    let sum = one.add(&zeta)?.add(&zeta2)?.reduce_prime()?;
    if sum.coeffs.iter().any(|c| *c != 0) {
        return Err("1+ζ+ζ^2 did not reduce to 0");
    }
    let factor = poly_mul(&[1, 1, 1], &[-1, 1])?;
    if factor != vec![-1, 0, 0, 1] {
        return Err("cyclotomic factorization of x^3-1 failed");
    }
    let tower = CyclotomicTower::new(3)?;
    if tower.degree != 2 {
        return Err("φ(3) is not 2");
    }
    Ok(())
}

fn euler_totient(n: usize) -> Result<usize, &'static str> {
    if n == 0 {
        return Err("conductor 0 has no totient");
    }
    let mut count = 0usize;
    for k in 1..=n {
        if coprime(k, n) {
            count += 1;
        }
    }
    let mut formula = n;
    let mut rest = n;
    let mut p = 2usize;
    while p * p <= rest {
        if rest % p == 0 {
            formula = formula / p * (p - 1);
            while rest % p == 0 {
                rest /= p;
            }
        }
        p += 1;
    }
    if rest > 1 {
        formula = formula / rest * (rest - 1);
    }
    if count != formula {
        return Err("totient count disagrees with the product formula");
    }
    Ok(count)
}

fn coprime(mut a: usize, mut b: usize) -> bool {
    while b != 0 {
        let r = a % b;
        a = b;
        b = r;
    }
    a == 1
}

fn is_prime(n: usize) -> bool {
    if n < 2 {
        return false;
    }
    let mut d = 2usize;
    while d * d <= n {
        if n % d == 0 {
            return false;
        }
        d += 1;
    }
    true
}

fn poly_mul(left: &[i64], right: &[i64]) -> Result<Vec<i64>, &'static str> {
    if left.is_empty() || right.is_empty() {
        return Ok(vec![0]);
    }
    let mut out = vec![0i64; left.len() + right.len() - 1];
    for (i, a) in left.iter().enumerate() {
        for (j, b) in right.iter().enumerate() {
            let term = a.checked_mul(*b).ok_or("polynomial overflow")?;
            out[i + j] = out[i + j].checked_add(term).ok_or("polynomial overflow")?;
        }
    }
    Ok(out)
}
