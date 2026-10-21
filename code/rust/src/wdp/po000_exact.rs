//! Exact scalar, matrix and real-root kernels for the PO-000 `24 g^2`
//! short-time defect chain (`po000_24g2.rs`).
//!
//! * [`Cx`] is a Gaussian rational `re + i im` with `BigRational` parts.
//! * [`Mat`] is a dense square matrix over [`Cx`], with Kronecker products,
//!   qubit partial traces and support embeddings.
//! * [`Poly`] is a univariate polynomial over `BigRational`. Sturm chains,
//!   Yun square-free factorisation and bisection place every real root in a
//!   closed rational interval [`Iv`].
//!
//! Trace norms and operator norms of Hermitian matrices are returned as
//! rational intervals. Their correctness rests on Sturm's theorem applied to
//! the exact Faddeev--LeVerrier characteristic polynomial; the root count is
//! checked against the degree, so every eigenvalue (with multiplicity) is
//! accounted for. A root is returned as a point interval when a short rational
//! inside its isolating interval is an exact zero of the polynomial.
//!
//! No binary floating point is used anywhere in this module.

use num_bigint::BigInt;
use num_rational::BigRational;
use num_traits::{One, Signed, Zero};

/// Exact rational scalar.
pub type Q = BigRational;

/// Integer as an exact rational.
pub fn qi(n: i64) -> Q {
    BigRational::from_integer(BigInt::from(n))
}

/// `n / d` as an exact rational. Fixture constants only: `d` must be nonzero.
pub fn qr(n: i64, d: i64) -> Q {
    BigRational::new(BigInt::from(n), BigInt::from(d))
}

/// `2^-bits` as an exact rational (used as a bisection width).
pub fn two_pow_neg(bits: u32) -> Q {
    BigRational::new(BigInt::one(), BigInt::one() << bits)
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum ExactError {
    Shape,
    NotHermitian,
    ImaginaryCharPoly,
    InexactDivision,
    ZeroDivisor,
    RootCountMismatch,
    NoSplitPoint,
    SeriesOrder,
    InvalidInstance(&'static str),
}

/// Gaussian rational `re + i im`.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Cx {
    pub re: Q,
    pub im: Q,
}

impl Cx {
    pub fn new(re: Q, im: Q) -> Self {
        Self { re, im }
    }
    pub fn real(re: Q) -> Self {
        Self::new(re, Q::zero())
    }
    pub fn zero() -> Self {
        Self::real(Q::zero())
    }
    pub fn one() -> Self {
        Self::real(Q::one())
    }
    pub fn i() -> Self {
        Self::new(Q::zero(), Q::one())
    }
    pub fn add(&self, o: &Cx) -> Cx {
        Cx::new(&self.re + &o.re, &self.im + &o.im)
    }
    pub fn sub(&self, o: &Cx) -> Cx {
        Cx::new(&self.re - &o.re, &self.im - &o.im)
    }
    pub fn mul(&self, o: &Cx) -> Cx {
        Cx::new(
            &self.re * &o.re - &self.im * &o.im,
            &self.re * &o.im + &self.im * &o.re,
        )
    }
    pub fn scale(&self, s: &Q) -> Cx {
        Cx::new(&self.re * s, &self.im * s)
    }
    pub fn conj(&self) -> Cx {
        Cx::new(self.re.clone(), -self.im.clone())
    }
    /// Multiply by `-i`: `(re + i im)(-i) = im - i re`.
    pub fn mul_neg_i(&self) -> Cx {
        Cx::new(self.im.clone(), -self.re.clone())
    }
    pub fn is_zero(&self) -> bool {
        self.re.is_zero() && self.im.is_zero()
    }
}

/// Dense square matrix over Gaussian rationals, row-major.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Mat {
    n: usize,
    a: Vec<Cx>,
}

impl Mat {
    pub fn zeros(n: usize) -> Self {
        Self { n, a: vec![Cx::zero(); n * n] }
    }
    pub fn identity(n: usize) -> Self {
        Self::from_fn(n, |i, j| if i == j { Cx::one() } else { Cx::zero() })
    }
    pub fn from_fn(n: usize, f: impl Fn(usize, usize) -> Cx) -> Self {
        let mut a = Vec::with_capacity(n * n);
        for i in 0..n {
            for j in 0..n {
                a.push(f(i, j));
            }
        }
        Self { n, a }
    }
    /// Row-major entries; refuses a length that is not `n * n`.
    pub fn from_entries(n: usize, a: Vec<Cx>) -> Result<Self, ExactError> {
        if a.len() != n * n {
            return Err(ExactError::Shape);
        }
        Ok(Self { n, a })
    }
    pub fn dim(&self) -> usize {
        self.n
    }
    pub fn get(&self, i: usize, j: usize) -> &Cx {
        &self.a[i * self.n + j]
    }
    fn zip(&self, o: &Mat, f: impl Fn(&Cx, &Cx) -> Cx) -> Mat {
        Mat { n: self.n, a: self.a.iter().zip(o.a.iter()).map(|(x, y)| f(x, y)).collect() }
    }
    pub fn add(&self, o: &Mat) -> Mat {
        self.zip(o, Cx::add)
    }
    pub fn sub(&self, o: &Mat) -> Mat {
        self.zip(o, Cx::sub)
    }
    pub fn scale(&self, s: &Q) -> Mat {
        Mat { n: self.n, a: self.a.iter().map(|x| x.scale(s)).collect() }
    }
    pub fn scale_cx(&self, s: &Cx) -> Mat {
        Mat { n: self.n, a: self.a.iter().map(|x| x.mul(s)).collect() }
    }
    pub fn mul_neg_i(&self) -> Mat {
        Mat { n: self.n, a: self.a.iter().map(Cx::mul_neg_i).collect() }
    }
    pub fn mul(&self, o: &Mat) -> Mat {
        let n = self.n;
        let mut out = Mat::zeros(n);
        for i in 0..n {
            for k in 0..n {
                let x = self.get(i, k);
                if x.is_zero() {
                    continue;
                }
                for j in 0..n {
                    let y = o.get(k, j);
                    if !y.is_zero() {
                        out.a[i * n + j] = out.a[i * n + j].add(&x.mul(y));
                    }
                }
            }
        }
        out
    }
    /// `[self, o] = self o - o self`.
    pub fn comm(&self, o: &Mat) -> Mat {
        self.mul(o).sub(&o.mul(self))
    }
    /// `{self, o} = self o + o self`.
    pub fn anti(&self, o: &Mat) -> Mat {
        self.mul(o).add(&o.mul(self))
    }
    pub fn dagger(&self) -> Mat {
        Mat::from_fn(self.n, |i, j| self.get(j, i).conj())
    }
    pub fn trace(&self) -> Cx {
        (0..self.n).fold(Cx::zero(), |acc, i| acc.add(self.get(i, i)))
    }
    pub fn kron(&self, o: &Mat) -> Mat {
        let m = o.n;
        Mat::from_fn(self.n * m, |i, j| self.get(i / m, j / m).mul(o.get(i % m, j % m)))
    }
    pub fn is_zero(&self) -> bool {
        self.a.iter().all(Cx::is_zero)
    }
    pub fn is_hermitian(&self) -> bool {
        *self == self.dagger()
    }
}

fn bit(x: usize, site: usize, nsites: usize) -> usize {
    (x >> (nsites - 1 - site)) & 1
}

fn sub_index(x: usize, sites: &[usize], nsites: usize) -> usize {
    sites.iter().fold(0, |acc, &s| (acc << 1) | bit(x, s, nsites))
}

fn env_index(x: usize, sites: &[usize], nsites: usize) -> usize {
    (0..nsites).filter(|s| !sites.contains(s)).fold(0, |acc, s| (acc << 1) | bit(x, s, nsites))
}

fn check_sites(sites: &[usize], nsites: usize) -> Result<(), ExactError> {
    let distinct = sites.iter().enumerate().all(|(i, s)| !sites[..i].contains(s));
    if nsites == 0 || nsites > 12 || !distinct || sites.iter().any(|&s| s >= nsites) {
        return Err(ExactError::Shape);
    }
    Ok(())
}

/// Embed a local qubit operator on `support` (site 0 most significant) into
/// the full `2^nsites` space as `local (x) I`.
pub fn embed(local: &Mat, support: &[usize], nsites: usize) -> Result<Mat, ExactError> {
    check_sites(support, nsites)?;
    if local.n != 1 << support.len() {
        return Err(ExactError::Shape);
    }
    Ok(Mat::from_fn(1 << nsites, |x, y| {
        if env_index(x, support, nsites) == env_index(y, support, nsites) {
            local.get(sub_index(x, support, nsites), sub_index(y, support, nsites)).clone()
        } else {
            Cx::zero()
        }
    }))
}

/// Partial trace onto the qubits `keep`, in the given order.
pub fn ptrace(m: &Mat, keep: &[usize], nsites: usize) -> Result<Mat, ExactError> {
    check_sites(keep, nsites)?;
    if m.n != 1 << nsites {
        return Err(ExactError::Shape);
    }
    let k = 1 << keep.len();
    let mut out = Mat::zeros(k);
    for x in 0..m.n {
        for y in 0..m.n {
            if env_index(x, keep, nsites) == env_index(y, keep, nsites) {
                let (i, j) = (sub_index(x, keep, nsites), sub_index(y, keep, nsites));
                out.a[i * k + j] = out.a[i * k + j].add(m.get(x, y));
            }
        }
    }
    Ok(out)
}

/// Closed rational interval `[lo, hi]`.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Iv {
    pub lo: Q,
    pub hi: Q,
}

impl Iv {
    pub fn new(a: Q, b: Q) -> Self {
        if a <= b {
            Self { lo: a, hi: b }
        } else {
            Self { lo: b, hi: a }
        }
    }
    pub fn point(x: Q) -> Self {
        Self { lo: x.clone(), hi: x }
    }
    pub fn zero() -> Self {
        Self::point(Q::zero())
    }
    pub fn is_point(&self) -> bool {
        self.lo == self.hi
    }
    pub fn contains(&self, x: &Q) -> bool {
        &self.lo <= x && x <= &self.hi
    }
    pub fn add(&self, o: &Iv) -> Iv {
        Iv { lo: &self.lo + &o.lo, hi: &self.hi + &o.hi }
    }
    /// Product of two intervals of nonnegative reals.
    pub fn mul_nonneg(&self, o: &Iv) -> Iv {
        Iv { lo: &self.lo * &o.lo, hi: &self.hi * &o.hi }
    }
    /// Scale by a nonnegative rational.
    pub fn scale_nonneg(&self, s: &Q) -> Iv {
        Iv { lo: &self.lo * s, hi: &self.hi * s }
    }
    /// Enclosure of `max(x, y)`.
    pub fn max(&self, o: &Iv) -> Iv {
        Iv {
            lo: if self.lo >= o.lo { self.lo.clone() } else { o.lo.clone() },
            hi: if self.hi >= o.hi { self.hi.clone() } else { o.hi.clone() },
        }
    }
    /// Enclosure of `|x|` for `x` in the interval.
    pub fn abs(&self) -> Iv {
        if !self.lo.is_negative() {
            self.clone()
        } else if !self.hi.is_positive() {
            Iv { lo: -self.hi.clone(), hi: -self.lo.clone() }
        } else {
            let m = if -self.lo.clone() >= self.hi { -self.lo.clone() } else { self.hi.clone() };
            Iv { lo: Q::zero(), hi: m }
        }
    }
}

/// Polynomial over `Q`, coefficients from low to high degree, trimmed.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Poly {
    c: Vec<Q>,
}

impl Poly {
    pub fn new(mut c: Vec<Q>) -> Self {
        while c.last().is_some_and(Zero::is_zero) {
            c.pop();
        }
        Self { c }
    }
    pub fn coeffs(&self) -> &[Q] {
        &self.c
    }
    pub fn is_zero(&self) -> bool {
        self.c.is_empty()
    }
    pub fn degree(&self) -> Option<usize> {
        self.c.len().checked_sub(1)
    }
    fn lead(&self) -> Q {
        self.c.last().cloned().unwrap_or_else(Q::zero)
    }
    pub fn eval(&self, x: &Q) -> Q {
        self.c.iter().rev().fold(Q::zero(), |acc, a| acc * x + a)
    }
    pub fn deriv(&self) -> Poly {
        Poly::new(self.c.iter().enumerate().skip(1).map(|(k, a)| a * qi(k as i64)).collect())
    }
    pub fn sub(&self, o: &Poly) -> Poly {
        let n = self.c.len().max(o.c.len());
        let z = Q::zero();
        Poly::new((0..n).map(|k| self.c.get(k).unwrap_or(&z) - o.c.get(k).unwrap_or(&z)).collect())
    }
    pub fn monic(&self) -> Poly {
        let l = self.lead();
        if l.is_zero() {
            return self.clone();
        }
        Poly::new(self.c.iter().map(|a| a / &l).collect())
    }
    pub fn divrem(&self, d: &Poly) -> Result<(Poly, Poly), ExactError> {
        let dd = d.degree().ok_or(ExactError::ZeroDivisor)?;
        let dl = d.lead();
        let mut r = self.c.clone();
        let mut quo = vec![Q::zero(); self.c.len().saturating_sub(dd).max(1)];
        while r.len() > dd && !r.is_empty() {
            let shift = r.len() - 1 - dd;
            let coef = r[r.len() - 1].clone() / &dl;
            for (k, dk) in d.c.iter().enumerate() {
                r[shift + k] -= &coef * dk;
            }
            quo[shift] = coef;
            r.pop();
            while r.last().is_some_and(Zero::is_zero) {
                r.pop();
            }
        }
        Ok((Poly::new(quo), Poly::new(r)))
    }
    pub fn exact_div(&self, d: &Poly) -> Result<Poly, ExactError> {
        let (quo, rem) = self.divrem(d)?;
        if rem.is_zero() {
            Ok(quo)
        } else {
            Err(ExactError::InexactDivision)
        }
    }
    /// Monic greatest common divisor.
    pub fn gcd(a: &Poly, b: &Poly) -> Result<Poly, ExactError> {
        let (mut x, mut y) = (a.clone(), b.clone());
        while !y.is_zero() {
            let (_, r) = x.divrem(&y)?;
            x = y;
            y = r;
        }
        Ok(x.monic())
    }
}

/// Characteristic polynomial `det(x I - m)` by Faddeev--LeVerrier. For a
/// Hermitian matrix the coefficients are real; an imaginary part is refused.
pub fn charpoly(m: &Mat) -> Result<Poly, ExactError> {
    let n = m.n;
    let mut c = vec![Cx::zero(); n + 1];
    c[n] = Cx::one();
    let mut mk = Mat::zeros(n);
    for k in 1..=n {
        mk = m.mul(&mk).add(&Mat::identity(n).scale_cx(&c[n - k + 1]));
        c[n - k] = m.mul(&mk).trace().scale(&(-qr(1, k as i64)));
    }
    if c.iter().any(|x| !x.im.is_zero()) {
        return Err(ExactError::ImaginaryCharPoly);
    }
    Ok(Poly::new(c.into_iter().map(|x| x.re).collect()))
}

/// Yun square-free factorisation: `(a_i, i)` with `p = lead * prod a_i^i`.
pub fn squarefree_parts(p: &Poly) -> Result<Vec<(Poly, usize)>, ExactError> {
    let p = p.monic();
    let mut out = Vec::new();
    if p.degree().unwrap_or(0) == 0 {
        return Ok(out);
    }
    let dp = p.deriv();
    let a0 = Poly::gcd(&p, &dp)?;
    let mut b = p.exact_div(&a0)?;
    let mut d = dp.exact_div(&a0)?.sub(&b.deriv());
    let mut i = 1;
    while b.degree().unwrap_or(0) > 0 {
        let a = Poly::gcd(&b, &d)?;
        let bn = b.exact_div(&a)?;
        let cn = d.exact_div(&a)?;
        d = cn.sub(&bn.deriv());
        if a.degree().unwrap_or(0) > 0 {
            out.push((a, i));
        }
        b = bn;
        i += 1;
    }
    Ok(out)
}

fn sturm_chain(f: &Poly) -> Result<Vec<Poly>, ExactError> {
    let mut chain = vec![f.clone(), f.deriv()];
    loop {
        let len = chain.len();
        let (_, r) = chain[len - 2].divrem(&chain[len - 1])?;
        if r.is_zero() {
            return Ok(chain);
        }
        chain.push(Poly::new(r.coeffs().iter().map(|a| -a.clone()).collect()));
    }
}

fn sign_changes(chain: &[Poly], x: &Q) -> usize {
    let signs: Vec<bool> = chain
        .iter()
        .map(|p| p.eval(x))
        .filter(|v| !v.is_zero())
        .map(|v| v.is_positive())
        .collect();
    signs.windows(2).filter(|w| w[0] != w[1]).count()
}

/// A short rational strictly inside the open interval `(lo, hi)`, `lo < hi`,
/// found by continued fractions. Used only as a candidate exact root.
pub fn simplest_between(lo: &Q, hi: &Q) -> Q {
    if lo.is_negative() && hi.is_positive() {
        Q::zero()
    } else if !lo.is_negative() {
        simplest_pos(lo, Some(hi))
    } else {
        -simplest_pos(&-hi.clone(), Some(&-lo.clone()))
    }
}

fn simplest_pos(lo: &Q, hi: Option<&Q>) -> Q {
    let n = lo.floor();
    let cand = &n + Q::one();
    match hi {
        None => cand,
        Some(h) if &cand < h => cand,
        Some(h) => {
            let inner_lo = (h - &n).recip();
            let inner = if *lo == n {
                simplest_pos(&inner_lo, None)
            } else {
                simplest_pos(&inner_lo, Some(&(lo - &n).recip()))
            };
            n + inner.recip()
        }
    }
}

fn split_point(f: &Poly, lo: &Q, hi: &Q) -> Result<Q, ExactError> {
    let deg = f.degree().unwrap_or(0) as i64;
    for den in 2..(deg + 4) {
        for num in 1..den {
            let m = lo + (hi - lo) * qr(num, den);
            if !f.eval(&m).is_zero() {
                return Ok(m);
            }
        }
    }
    Err(ExactError::NoSplitPoint)
}

fn refine(f: &Poly, mut lo: Q, mut hi: Q, eps: &Q) -> Iv {
    let lo_pos = f.eval(&lo).is_positive();
    loop {
        let s = simplest_between(&lo, &hi);
        if f.eval(&s).is_zero() {
            return Iv::point(s);
        }
        if &hi - &lo <= *eps {
            return Iv { lo, hi };
        }
        let m = (&lo + &hi) / qi(2);
        let fm = f.eval(&m);
        if fm.is_zero() {
            return Iv::point(m);
        }
        if fm.is_positive() == lo_pos {
            lo = m;
        } else {
            hi = m;
        }
    }
}

/// Isolate and refine the real roots of a square-free polynomial with
/// `f(0) != 0`, on `(-B, 0)` and `(0, B)` with the strict Cauchy bound `B`.
fn isolate(f: &Poly, eps: &Q) -> Result<Vec<Iv>, ExactError> {
    let lead = f.lead();
    let bound = f.c.iter().rev().skip(1).map(|a| (a / &lead).abs()).fold(Q::zero(), |m, x| {
        if x > m { x } else { m }
    }) + Q::one();
    let chain = sturm_chain(f)?;
    let mut stack = vec![(-bound.clone(), Q::zero()), (Q::zero(), bound)];
    let mut out = Vec::new();
    while let Some((lo, hi)) = stack.pop() {
        let count = sign_changes(&chain, &lo).saturating_sub(sign_changes(&chain, &hi));
        if count == 1 {
            out.push(refine(f, lo, hi, eps));
        } else if count > 1 {
            let m = split_point(f, &lo, &hi)?;
            stack.push((lo, m.clone()));
            stack.push((m, hi));
        }
    }
    Ok(out)
}

/// Every real root of `p` as an interval with its multiplicity. Refused if
/// the multiplicities do not add up to the degree (a non-real root).
pub fn real_roots(p: &Poly, eps: &Q) -> Result<Vec<(Iv, usize)>, ExactError> {
    let mut out = Vec::new();
    for (f, mult) in squarefree_parts(p)? {
        let mut f = f;
        if f.eval(&Q::zero()).is_zero() {
            out.push((Iv::zero(), mult));
            f = f.exact_div(&Poly::new(vec![Q::zero(), Q::one()]))?;
        }
        if f.degree().unwrap_or(0) > 0 {
            out.extend(isolate(&f, eps)?.into_iter().map(|iv| (iv, mult)));
        }
    }
    let total: usize = out.iter().map(|(_, m)| m).sum();
    if Some(total) != p.degree() {
        return Err(ExactError::RootCountMismatch);
    }
    Ok(out)
}

/// Spectrum of a Hermitian matrix as rational intervals with multiplicity.
pub fn spectrum(h: &Mat, eps: &Q) -> Result<Vec<(Iv, usize)>, ExactError> {
    if !h.is_hermitian() {
        return Err(ExactError::NotHermitian);
    }
    real_roots(&charpoly(h)?, eps)
}

/// Trace norm `sum |lambda_i|` of a Hermitian matrix, as a rational enclosure.
pub fn trace_norm(h: &Mat, eps: &Q) -> Result<Iv, ExactError> {
    Ok(spectrum(h, eps)?
        .into_iter()
        .fold(Iv::zero(), |acc, (iv, m)| acc.add(&iv.abs().scale_nonneg(&qi(m as i64)))))
}

/// Operator norm `max |lambda_i|` of a Hermitian matrix, as an enclosure.
pub fn op_norm(h: &Mat, eps: &Q) -> Result<Iv, ExactError> {
    Ok(spectrum(h, eps)?.into_iter().fold(Iv::zero(), |acc, (iv, _)| acc.max(&iv.abs())))
}

#[cfg(test)]
mod tests {
    use super::*;

    fn eps() -> Q {
        two_pow_neg(40)
    }

    #[test]
    fn unit_charpoly_and_roots_of_heisenberg_bond() -> Result<(), ExactError> {
        // XX + YY + ZZ has spectrum {1, 1, 1, -3}.
        let x = Mat::from_entries(2, vec![Cx::zero(), Cx::one(), Cx::one(), Cx::zero()])?;
        let y = Mat::from_entries(2, vec![Cx::zero(), Cx::i().scale(&qi(-1)), Cx::i(), Cx::zero()])?;
        let z = Mat::from_entries(2, vec![Cx::one(), Cx::zero(), Cx::zero(), Cx::real(qi(-1))])?;
        let h = x.kron(&x).add(&y.kron(&y)).add(&z.kron(&z));
        let roots = spectrum(&h, &eps())?;
        assert!(roots.contains(&(Iv::point(qi(1)), 3)));
        assert!(roots.contains(&(Iv::point(qi(-3)), 1)));
        assert_eq!(op_norm(&h, &eps())?, Iv::point(qi(3)));
        assert_eq!(trace_norm(&h, &eps())?, Iv::point(qi(6)));
        Ok(())
    }

    #[test]
    fn unit_irrational_root_is_enclosed_by_sturm() -> Result<(), ExactError> {
        // x^2 - 2: the positive root is enclosed, never returned as a point.
        let p = Poly::new(vec![qi(-2), Q::zero(), qi(1)]);
        let roots = real_roots(&p, &eps())?;
        assert_eq!(roots.len(), 2);
        for (iv, m) in roots {
            assert_eq!(m, 1);
            assert!(!iv.is_point());
            assert!(&iv.hi - &iv.lo <= eps());
            let a = iv.abs();
            assert!(&a.lo * &a.lo <= qi(2) && qi(2) <= &a.hi * &a.hi);
        }
        Ok(())
    }

    #[test]
    fn negative_non_real_roots_are_refused() {
        // x^2 + 1 has no real root, so the count check refuses it.
        let p = Poly::new(vec![qi(1), Q::zero(), qi(1)]);
        assert_eq!(real_roots(&p, &eps()), Err(ExactError::RootCountMismatch));
    }

    #[test]
    fn unit_partial_trace_inverts_kron() -> Result<(), ExactError> {
        let a = Mat::from_entries(2, vec![Cx::real(qr(2, 3)), Cx::new(qr(1, 6), qr(1, 6)), Cx::new(qr(1, 6), qr(-1, 6)), Cx::real(qr(1, 3))])?;
        let b = Mat::from_entries(2, vec![Cx::real(qr(1, 4)), Cx::zero(), Cx::zero(), Cx::real(qr(3, 4))])?;
        let ab = a.kron(&b);
        assert_eq!(ptrace(&ab, &[0], 2)?, a);
        assert_eq!(ptrace(&ab, &[1], 2)?, b);
        assert_eq!(embed(&a, &[0], 2)?, a.kron(&Mat::identity(2)));
        Ok(())
    }
}
