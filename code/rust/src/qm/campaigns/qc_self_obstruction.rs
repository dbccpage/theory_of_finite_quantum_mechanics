//! Exact replay of the self-obstruction analysis of reliable quantum computation.
//!
//! Replays in exact `BigRational` arithmetic, on declared families and instances, the finite
//! statements that the Lean modules `QcConcatenation`, `QcRepairQueue`, `QcEntropySink` and
//! `QcSelfObstruction` (`lean4/`) prove in general, and mirrors the Python twin
//! `code/python/src/qm/qc_self_obstruction.py` function for function:
//!
//! * Q2: the recurrence `p_{k+1} = c p_k^2`, its closed form `c p_k = (c p_0)^(2^k)`, the three
//!   regimes of `c p_0` against one, and explicit crossing levels;
//! * Q3: the level-dependent overhead `c_k`, the amplification `amp` (`amp_0 = 1`,
//!   `amp_{k+1} = c_k amp_k^2`), the witness `amp_k <= M^(2^k)`, the families `c_k <= A 2^(k+1)`,
//!   `(k+1)^2` and the double exponential `a b^(2^k)` whose amplification escapes every bound;
//! * Q1: the repair backlog `q_{t+1} = max(0, q_t + lam + g mu - mu)` and the fresh-supply
//!   threshold;
//! * Q4: depolarizing noise on rational Bloch vectors and `2 x 2` Gaussian-rational density
//!   matrices, with the squared Bloch distance contracting by `(1 - p)^2` per noisy rotation;
//! * Q6 support: a finite fresh-mark budget bounds the number of rounds.
//!
//! Every function checks a declared finite instance; a passing check is not a proof of the
//! general statement (the general statements are the kernel-checked Lean theorems). No claim is
//! made about any physical device. AuthorityEffect: None.

use num_bigint::BigInt;
use num_rational::BigRational;
use num_traits::{One, Signed, ToPrimitive, Zero};

pub const AUTHORITY_FENCE: &str = "AuthorityEffect None; finite exact replay on declared instances; \
     not a proof of the general statements; no claim about physical hardware; the threshold \
     theorem and the Aharonov-Ben-Or-Impagliazzo-Nisan 1996 theorem are cited literature, not \
     imported as proof.";

pub type Q = BigRational;

/// Refusals of the checker.
#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum QcError {
    #[error("requires c > 0 and p >= 0")]
    BadRegimeInput,
    #[error("requires eps > 0")]
    BadEpsilon,
    #[error("requires 0 <= p <= 1")]
    BadProbability,
    #[error("requires 0 < p < 1 and delta > 0")]
    BadDepthInput,
    #[error("requires g < 1 and kappa > 0 (otherwise no supply suffices)")]
    NoSupplySuffices,
    #[error("requires rmin > 0")]
    BadBudget,
    #[error("requires c^2 + s^2 = 1")]
    NotARotation,
    #[error("a rational rotation (R^T R = 1) is required")]
    NotOrthogonal,
    #[error("requires q0 >= 0")]
    NegativeBacklog,
    #[error("requires M > 0")]
    BadBound,
    #[error("not enough overheads supplied")]
    ShortOverheads,
    #[error("requires 0 <= c_k <= C")]
    OverheadOutOfRange,
    #[error("requires c p <= 1/2")]
    AboveHalf,
    #[error("requires s < 2 and block sizes with N_(k+1) <= s N_k")]
    SizeRatio,
}

pub fn q(n: i64, d: i64) -> Q {
    Q::new(BigInt::from(n), BigInt::from(d))
}

pub fn qi(n: i64) -> Q {
    Q::from_integer(BigInt::from(n))
}

fn pow_two_pow(x: &Q, k: u32) -> Q {
    // x^(2^k) by k squarings
    let mut r = x.clone();
    for _ in 0..k {
        r = &r * &r;
    }
    r
}

fn pow_u(x: &Q, e: u32) -> Q {
    let mut r = Q::one();
    for _ in 0..e {
        r = &r * x;
    }
    r
}

// ----------------------------------------------------------------------------- Q2: constant overhead

/// Level-`k` error of `p_{k+1} = c p_k^2` started at `p_0 = p`.
pub fn conc(c: &Q, p: &Q, k: u32) -> Q {
    let mut x = p.clone();
    for _ in 0..k {
        x = c * &x * &x;
    }
    x
}

/// `c p_k == (c p_0)^(2^k)`, the exact closed form (Lean: `conc_closed`).
pub fn conc_closed_holds(c: &Q, p: &Q, k: u32) -> bool {
    c * conc(c, p, k) == pow_two_pow(&(c * p), k)
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Regime {
    Below,
    Fixed,
    Above,
}

/// `c p_0` against one (requires `c > 0`, `p >= 0`).
pub fn classify(c: &Q, p: &Q) -> Result<Regime, QcError> {
    if !c.is_positive() || p.is_negative() {
        return Err(QcError::BadRegimeInput);
    }
    let r = c * p;
    let one = Q::one();
    Ok(if r < one {
        Regime::Below
    } else if r == one {
        Regime::Fixed
    } else {
        Regime::Above
    })
}

/// The certified threshold `1 / c`.
pub fn threshold(c: &Q) -> Result<Q, QcError> {
    if !c.is_positive() {
        return Err(QcError::BadRegimeInput);
    }
    Ok(c.recip())
}

/// Smallest `k <= max_levels` with `p_k < eps`.
pub fn first_level_below(c: &Q, p: &Q, eps: &Q, max_levels: u32) -> Result<Option<u32>, QcError> {
    if !eps.is_positive() {
        return Err(QcError::BadEpsilon);
    }
    let mut x = p.clone();
    for k in 0..=max_levels {
        if &x < eps {
            return Ok(Some(k));
        }
        x = c * &x * &x;
    }
    Ok(None)
}

/// Smallest `k <= max_levels` with `p_k > big`.
pub fn first_level_above(c: &Q, p: &Q, big: &Q, max_levels: u32) -> Option<u32> {
    let mut x = p.clone();
    for k in 0..=max_levels {
        if &x > big {
            return Some(k);
        }
        x = c * &x * &x;
    }
    None
}

/// If `c p_0 <= 1/2` then `p_k <= (1/2)^(2^k) / c` (Lean: `sub_half_bound`).
pub fn half_bound_holds(c: &Q, p: &Q, k: u32) -> Result<bool, QcError> {
    if !c.is_positive() || p.is_negative() || c * p > q(1, 2) {
        return Err(QcError::AboveHalf);
    }
    Ok(conc(c, p, k) <= pow_two_pow(&q(1, 2), k) / c)
}

/// Unrepaired union bound `p_{k+1} = a p_k`: `a^k p`.
pub fn linear_level(a: &Q, p: &Q, k: u32) -> Q {
    let mut x = p.clone();
    for _ in 0..k {
        x = a * &x;
    }
    x
}

/// Unordered pairs among `a` fault locations: the constant of a distance-three level.
pub fn pair_count(a: u32) -> Q {
    let a = BigInt::from(a);
    Q::new(&a * (&a - BigInt::one()), BigInt::from(2))
}

// ----------------------------------------------------------------------------- Q3: level-dependent

/// `amp_0 = 1`, `amp_{k+1} = c_k amp_k^2`.
pub fn amp(cs: &[Q], k: usize) -> Result<Q, QcError> {
    if k > cs.len() {
        return Err(QcError::ShortOverheads);
    }
    let mut x = Q::one();
    for c in cs.iter().take(k) {
        x = c * &x * &x;
    }
    Ok(x)
}

/// Level-`k` error of `p_{k+1} = c_k p_k^2`.
pub fn concv(cs: &[Q], p: &Q, k: usize) -> Result<Q, QcError> {
    if k > cs.len() {
        return Err(QcError::ShortOverheads);
    }
    let mut x = p.clone();
    for c in cs.iter().take(k) {
        x = c * &x * &x;
    }
    Ok(x)
}

/// `p_k == p^(2^k) amp_k` (Lean: `concv_eq_amp`).
pub fn concv_amp_holds(cs: &[Q], p: &Q, k: usize) -> Result<bool, QcError> {
    Ok(concv(cs, p, k)? == pow_two_pow(p, k as u32) * amp(cs, k)?)
}

/// `amp_k <= M^(2^k)` for every `k <= len(cs)`: a finite witness for `AmpBounded`.
pub fn amp_bound_holds(cs: &[Q], m: &Q) -> Result<bool, QcError> {
    if !m.is_positive() {
        return Err(QcError::BadBound);
    }
    for k in 0..=cs.len() {
        if amp(cs, k)? > pow_two_pow(m, k as u32) {
            return Ok(false);
        }
    }
    Ok(true)
}

/// Smallest `k <= len(cs)` with `amp_k > M^(2^k)` (a finite refutation of that `M`).
pub fn amp_escape_level(cs: &[Q], m: &Q) -> Result<Option<usize>, QcError> {
    if !m.is_positive() {
        return Err(QcError::BadBound);
    }
    for k in 0..=cs.len() {
        if amp(cs, k)? > pow_two_pow(m, k as u32) {
            return Ok(Some(k));
        }
    }
    Ok(None)
}

pub fn const_family(c: &Q, n: usize) -> Vec<Q> {
    vec![c.clone(); n]
}

/// `c_k = A B^(k+1)` (geometric growth of the overhead).
pub fn geom_family(a: &Q, b: &Q, n: usize) -> Vec<Q> {
    (0..n).map(|k| a * pow_u(b, k as u32 + 1)).collect()
}

/// `c_k = A 2^(k+1)`: the geometric family with `B = 2`.
pub fn exp_family(a: &Q, n: usize) -> Vec<Q> {
    geom_family(a, &qi(2), n)
}

/// `c_k = a b^(N_k)` for block sizes `N_k` (the overhead exponential in the level-k block size).
pub fn size_family(a: &Q, b: &Q, sizes: &[u32]) -> Vec<Q> {
    sizes.iter().map(|&n| a * pow_u(b, n)).collect()
}

/// `E_0 = 0`, `E_{k+1} = 2 E_k + N_k`, the exponent of `b` in `amp` (Lean: `blockExp`).
pub fn block_exp(sizes: &[u32]) -> Vec<BigInt> {
    let mut out = vec![BigInt::zero()];
    for &n in sizes {
        let next = out.last().cloned().unwrap_or_else(BigInt::zero) * 2 + BigInt::from(n);
        out.push(next);
    }
    out
}

/// `E_k + N_k/(2-s) <= 2^k N_0/(2-s)` when `N_{k+1} <= s N_k` with `s < 2` (Lean: `blockExp_le`).
pub fn block_exp_bound_holds(sizes: &[u32], s: &Q) -> Result<bool, QcError> {
    if *s >= qi(2) || sizes.is_empty() {
        return Err(QcError::SizeRatio);
    }
    if sizes.windows(2).any(|w| qi(w[1] as i64) > s * qi(w[0] as i64)) {
        return Err(QcError::SizeRatio);
    }
    let e = block_exp(sizes);
    let gap = qi(2) - s;
    Ok((0..sizes.len()).all(|k| {
        Q::from_integer(e[k].clone()) + qi(sizes[k] as i64) / &gap
            <= pow_u(&qi(2), k as u32) * qi(sizes[0] as i64) / &gap
    }))
}

/// `c_k = (k+1)^2`.
pub fn poly_family(n: usize) -> Vec<Q> {
    (0..n).map(|k| qi(((k + 1) * (k + 1)) as i64)).collect()
}

/// `c_k = a b^(2^k)`.
pub fn dexp_family(a: &Q, b: &Q, n: usize) -> Vec<Q> {
    (0..n).map(|k| a * pow_two_pow(b, k as u32)).collect()
}

/// `amp_k max(C,1) <= max(C,1)^(2^k)` when every `0 <= c_k <= C` (Lean: `amp_le_of_bounded`).
pub fn const_invariant_holds(cs: &[Q], c_max: &Q) -> Result<bool, QcError> {
    if cs.iter().any(|c| c.is_negative() || c > c_max) {
        return Err(QcError::OverheadOutOfRange);
    }
    let d = if c_max > &Q::one() { c_max.clone() } else { Q::one() };
    for k in 0..=cs.len() {
        if amp(cs, k)? * &d > pow_two_pow(&d, k as u32) {
            return Ok(false);
        }
    }
    Ok(true)
}

/// `amp_k (A B^(k+2)) <= (A B^2)^(2^k)` for `c_k = A B^(k+1)` (Lean: `amp_le_of_geom`).
pub fn geom_invariant_holds(a: &Q, b: &Q, n: usize) -> Result<bool, QcError> {
    let cs = geom_family(a, b, n);
    let base = a * b * b;
    for k in 0..=n {
        let lhs = amp(&cs, k)? * a * pow_u(b, k as u32 + 2);
        if lhs > pow_two_pow(&base, k as u32) {
            return Ok(false);
        }
    }
    Ok(true)
}

/// The geometric invariant with `B = 2`: `amp_k (A 2^(k+2)) <= (4A)^(2^k)`.
pub fn exp_invariant_holds(a: &Q, n: usize) -> Result<bool, QcError> {
    geom_invariant_holds(a, &qi(2), n)
}

/// `(amp_k a)^2 == (a^2 b^k)^(2^k)` for `c_k = a b^(2^k)` (Lean: `amp_dexp_sq`).
pub fn dexp_square_identity_holds(a: &Q, b: &Q, n: usize) -> Result<bool, QcError> {
    let cs = dexp_family(a, b, n);
    for k in 0..=n {
        let lhs = {
            let t = amp(&cs, k)? * a;
            &t * &t
        };
        let rhs = pow_two_pow(&(a * a * pow_u(b, k as u32)), k as u32);
        if lhs != rhs {
            return Ok(false);
        }
    }
    Ok(true)
}

// ----------------------------------------------------------------------------- Q1: repair backlog

/// Backlog trajectory `[q_0, ..., q_steps]` of `q_{t+1} = max(0, q_t + lam + g mu - mu)`.
pub fn backlog(lam: &Q, g: &Q, mu: &Q, q0: &Q, steps: usize) -> Result<Vec<Q>, QcError> {
    if q0.is_negative() {
        return Err(QcError::NegativeBacklog);
    }
    let d = lam + g * mu - mu;
    let mut out = vec![q0.clone()];
    for _ in 0..steps {
        let next = out.last().cloned().unwrap_or_else(Q::zero) + &d;
        out.push(if next.is_negative() { Q::zero() } else { next });
    }
    Ok(out)
}

/// The Lean criterion: bounded iff `lam <= (1 - g) mu`.
pub fn backlog_bounded_decision(lam: &Q, g: &Q, mu: &Q) -> bool {
    *lam <= (Q::one() - g) * mu
}

/// Least fresh supply `r` with `lam <= (1 - g) kappa r`; requires `g < 1`, `kappa > 0`.
pub fn supply_threshold(lam: &Q, g: &Q, kappa: &Q) -> Result<Q, QcError> {
    if *g >= Q::one() || !kappa.is_positive() {
        return Err(QcError::NoSupplySuffices);
    }
    Ok(lam / ((Q::one() - g) * kappa))
}

/// Rounds completed with a total of `budget` fresh marks and at least `rmin` per round.
pub fn rounds_upper_bound(budget: &Q, rmin: &Q) -> Result<Q, QcError> {
    if !rmin.is_positive() {
        return Err(QcError::BadBudget);
    }
    Ok(budget / rmin)
}

// ----------------------------------------------------------------------------- Q4: depolarizing decay

pub type Vec3 = [Q; 3];
pub type Mat3 = [[Q; 3]; 3];

pub fn bloch_dot(u: &Vec3, v: &Vec3) -> Q {
    &u[0] * &v[0] + &u[1] * &v[1] + &u[2] * &v[2]
}

pub fn bloch_sq_dist(r: &Vec3, s: &Vec3) -> Q {
    let d = [&r[0] - &s[0], &r[1] - &s[1], &r[2] - &s[2]];
    bloch_dot(&d, &d)
}

pub fn mat_vec(r: &Mat3, v: &Vec3) -> Vec3 {
    [
        bloch_dot(&r[0], v),
        bloch_dot(&r[1], v),
        bloch_dot(&r[2], v),
    ]
}

/// `R^T R == 1` exactly.
pub fn is_rational_rotation(r: &Mat3) -> bool {
    (0..3).all(|i| {
        (0..3).all(|j| {
            let s = &r[0][i] * &r[0][j] + &r[1][i] * &r[1][j] + &r[2][i] * &r[2][j];
            s == if i == j { Q::one() } else { Q::zero() }
        })
    })
}

pub fn rot_z(c: &Q, s: &Q) -> Result<Mat3, QcError> {
    if c * c + s * s != Q::one() {
        return Err(QcError::NotARotation);
    }
    let (z, o) = (Q::zero(), Q::one());
    Ok([
        [c.clone(), -s.clone(), z.clone()],
        [s.clone(), c.clone(), z.clone()],
        [z.clone(), z, o],
    ])
}

pub fn rot_x(c: &Q, s: &Q) -> Result<Mat3, QcError> {
    if c * c + s * s != Q::one() {
        return Err(QcError::NotARotation);
    }
    let (z, o) = (Q::zero(), Q::one());
    Ok([
        [o, z.clone(), z.clone()],
        [z.clone(), c.clone(), -s.clone()],
        [z, s.clone(), c.clone()],
    ])
}

/// Rotate then depolarize: `r -> (1 - p) R r`.
pub fn bloch_step(p: &Q, r: &Mat3, v: &Vec3) -> Result<Vec3, QcError> {
    if !is_rational_rotation(r) {
        return Err(QcError::NotOrthogonal);
    }
    let f = Q::one() - p;
    let w = mat_vec(r, v);
    Ok([&f * &w[0], &f * &w[1], &f * &w[2]])
}

pub fn bloch_run(history: &[(Q, Mat3)], v: &Vec3) -> Result<Vec3, QcError> {
    let mut cur = v.clone();
    for (p, r) in history {
        cur = bloch_step(p, r, &cur)?;
    }
    Ok(cur)
}

/// `prod (1 - p_i)^2`.
pub fn contraction_factor_sq(history: &[(Q, Mat3)]) -> Q {
    history
        .iter()
        .fold(Q::one(), |acc, (p, _)| acc * (Q::one() - p) * (Q::one() - p))
}

/// `sqDist(run r, run s) == prod (1 - p_i)^2 sqDist(r, s)` (Lean: `sqDist_runB`).
pub fn decay_identity_holds(history: &[(Q, Mat3)], r: &Vec3, s: &Vec3) -> Result<bool, QcError> {
    Ok(bloch_sq_dist(&bloch_run(history, r)?, &bloch_run(history, s)?)
        == contraction_factor_sq(history) * bloch_sq_dist(r, s))
}

/// `(1 - p)^t <= 1 / (1 + p t)` for `0 <= p <= 1` (Lean: `decay_le_inv`).
pub fn decay_le_inv_holds(p: &Q, t: u32) -> Result<bool, QcError> {
    if p.is_negative() || p > &Q::one() {
        return Err(QcError::BadProbability);
    }
    Ok(pow_u(&(Q::one() - p), t) <= (Q::one() + p * qi(t as i64)).recip())
}

/// Smallest `t` with `(1 - p)^t <= delta`; `None` past `max_depth`. Requires `0 < p < 1`.
pub fn depth_until_below(p: &Q, delta: &Q, max_depth: u32) -> Result<Option<u32>, QcError> {
    if !p.is_positive() || p >= &Q::one() || !delta.is_positive() {
        return Err(QcError::BadDepthInput);
    }
    let f = Q::one() - p;
    let mut x = Q::one();
    let mut t = 0u32;
    while &x > delta {
        t += 1;
        if t > max_depth {
            return Ok(None);
        }
        x = &x * &f;
    }
    Ok(Some(t))
}

/// An exact Gaussian rational `re + im i`.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Gq {
    pub re: Q,
    pub im: Q,
}

impl Gq {
    pub fn new(re: Q, im: Q) -> Self {
        Self { re, im }
    }
    pub fn zero() -> Self {
        Self::new(Q::zero(), Q::zero())
    }
    fn mul(&self, o: &Gq) -> Gq {
        Gq::new(&self.re * &o.re - &self.im * &o.im, &self.re * &o.im + &self.im * &o.re)
    }
    fn add(&self, o: &Gq) -> Gq {
        Gq::new(&self.re + &o.re, &self.im + &o.im)
    }
    fn conj(&self) -> Gq {
        Gq::new(self.re.clone(), -self.im.clone())
    }
}

pub type Mat2 = [[Gq; 2]; 2];

pub fn mat2_mul(a: &Mat2, b: &Mat2) -> Mat2 {
    let e = |i: usize, j: usize| a[i][0].mul(&b[0][j]).add(&a[i][1].mul(&b[1][j]));
    [[e(0, 0), e(0, 1)], [e(1, 0), e(1, 1)]]
}

pub fn mat2_dagger(a: &Mat2) -> Mat2 {
    [[a[0][0].conj(), a[1][0].conj()], [a[0][1].conj(), a[1][1].conj()]]
}

fn real(x: Q) -> Gq {
    Gq::new(x, Q::zero())
}

/// `rho(r) = (1 + r . sigma) / 2`.
pub fn bloch_matrix(r: &Vec3) -> Mat2 {
    let h = q(1, 2);
    [
        [
            real((Q::one() + &r[2]) * &h),
            Gq::new(&r[0] * &h, -(&r[1] * &h)),
        ],
        [
            Gq::new(&r[0] * &h, &r[1] * &h),
            real((Q::one() - &r[2]) * &h),
        ],
    ]
}

/// `v . sigma` (the Lean `blochMat`).
pub fn pauli_part(v: &Vec3) -> Mat2 {
    [
        [real(v[2].clone()), Gq::new(v[0].clone(), -v[1].clone())],
        [Gq::new(v[0].clone(), v[1].clone()), real(-v[2].clone())],
    ]
}

/// `(v . sigma)^2 == |v|^2 1` exactly (Lean: `blochMat_sq`).
pub fn pauli_part_squares_to_norm(v: &Vec3) -> bool {
    let n = bloch_dot(v, v);
    mat2_mul(&pauli_part(v), &pauli_part(v))
        == [[real(n.clone()), Gq::zero()], [Gq::zero(), real(n)]]
}

/// `U = c 1 - i s sigma_axis` with `c^2 + s^2 = 1`, axis `'x'` or `'z'`.
pub fn unitary_about(axis: char, c: &Q, s: &Q) -> Result<Mat2, QcError> {
    if c * c + s * s != Q::one() || (axis != 'x' && axis != 'z') {
        return Err(QcError::NotARotation);
    }
    Ok(if axis == 'z' {
        [
            [Gq::new(c.clone(), -s.clone()), Gq::zero()],
            [Gq::zero(), Gq::new(c.clone(), s.clone())],
        ]
    } else {
        [
            [real(c.clone()), Gq::new(Q::zero(), -s.clone())],
            [Gq::new(Q::zero(), -s.clone()), real(c.clone())],
        ]
    })
}

/// `(1 - p) rho + p (tr rho / 2) 1`.
pub fn depolarize_matrix(p: &Q, rho: &Mat2) -> Mat2 {
    let f = Q::one() - p;
    let tr = rho[0][0].add(&rho[1][1]);
    let scale = |g: &Gq, k: &Q| Gq::new(k * &g.re, k * &g.im);
    let half = p / qi(2);
    let mut out: Mat2 = [
        [scale(&rho[0][0], &f), scale(&rho[0][1], &f)],
        [scale(&rho[1][0], &f), scale(&rho[1][1], &f)],
    ];
    for i in 0..2 {
        out[i][i] = out[i][i].add(&scale(&tr, &half));
    }
    out
}

/// Unitary conjugation then global depolarizing noise.
pub fn matrix_step(p: &Q, u: &Mat2, rho: &Mat2) -> Mat2 {
    depolarize_matrix(p, &mat2_mul(&mat2_mul(u, rho), &mat2_dagger(u)))
}

/// The Bloch vector `(2 Re rho01, -2 Im rho01, rho00 - rho11)`.
pub fn bloch_of_matrix(rho: &Mat2) -> Vec3 {
    [
        qi(2) * &rho[0][1].re,
        -(qi(2) * &rho[0][1].im),
        &rho[0][0].re - &rho[1][1].re,
    ]
}

// ----------------------------------------------------------------------------- Q5: assembled report

/// Smallest level `k` with `L p_k <= eps` below threshold (constant overhead).
pub fn level_for_failure(c: &Q, p: &Q, locations: &Q, eps: &Q, max_levels: u32) -> Option<u32> {
    if classify(c, p).ok()? != Regime::Below || locations.is_negative() || !eps.is_positive() {
        return None;
    }
    let mut x = p.clone();
    for k in 0..=max_levels {
        if &(locations * &x) <= eps {
            return Some(k);
        }
        x = c * &x * &x;
    }
    None
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ViabilityReport {
    pub supply_ok: bool,
    pub below_threshold: bool,
    pub level: Option<u32>,
    pub certified: bool,
}

/// Conditions of the conditional certificate on a declared instance (constant overhead `c`).
#[allow(clippy::too_many_arguments)]
pub fn viability_report(
    lam: &Q,
    g: &Q,
    kappa: &Q,
    r: &Q,
    c: &Q,
    p: &Q,
    locations: &Q,
    eps: &Q,
) -> ViabilityReport {
    let supply_ok = supply_threshold(lam, g, kappa).map(|t| &t <= r).unwrap_or(false);
    let below_threshold = classify(c, p).map(|x| x == Regime::Below).unwrap_or(false);
    let level = if supply_ok && below_threshold {
        level_for_failure(c, p, locations, eps, 16)
    } else {
        None
    };
    ViabilityReport { supply_ok, below_threshold, certified: level.is_some(), level }
}

/// Number of levels as a plain integer for reports.
pub fn level_u32(l: Option<usize>) -> Option<u32> {
    l.and_then(|x| x.to_u32())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn closed_form_and_literal_values() {
        let seq: Vec<Q> = (0..4).map(|k| conc(&qi(4), &q(1, 10), k)).collect();
        assert_eq!(seq, vec![q(1, 10), q(1, 25), q(4, 625), q(64, 390625)]);
        for k in 0..8 {
            assert!(conc_closed_holds(&qi(4), &q(1, 10), k));
            assert!(conc_closed_holds(&q(3, 2), &q(-1, 7), k));
        }
    }

    #[test]
    fn three_regimes() {
        assert_eq!(classify(&qi(4), &q(1, 10)), Ok(Regime::Below));
        assert_eq!(classify(&qi(4), &q(1, 4)), Ok(Regime::Fixed));
        assert_eq!(classify(&qi(4), &q(3, 10)), Ok(Regime::Above));
        assert_eq!(threshold(&qi(4)), Ok(q(1, 4)));
        assert!((0..10).all(|k| conc(&qi(4), &q(1, 4), k) == q(1, 4)));
        let seq: Vec<Q> = (0..8).map(|k| conc(&qi(4), &q(1, 10), k)).collect();
        assert!(seq.windows(2).all(|w| w[1] < w[0]));
        let eps = Q::new(BigInt::one(), BigInt::from(10u64.pow(9)));
        assert_eq!(first_level_below(&qi(4), &q(1, 10), &eps, 16), Ok(Some(5)));
        let up: Vec<Q> = (0..6).map(|k| conc(&qi(4), &q(3, 10), k)).collect();
        assert!(up.windows(2).all(|w| w[1] > w[0]));
        assert_eq!(first_level_above(&qi(4), &q(3, 10), &qi(1), 16), Some(3));
        assert!(first_level_above(&qi(4), &q(3, 10), &Q::from_integer(BigInt::from(10u8).pow(30)), 16)
            .is_some());
    }

    #[test]
    fn boundary_pair_separates_regimes() {
        let eps = Q::new(BigInt::one(), BigInt::from(1_000_000));
        assert_eq!(classify(&qi(7), &(q(1, 7) - &eps)), Ok(Regime::Below));
        assert_eq!(classify(&qi(7), &(q(1, 7) + &eps)), Ok(Regime::Above));
    }

    #[test]
    fn half_bound() {
        for k in 0..8 {
            assert_eq!(half_bound_holds(&qi(4), &q(1, 8), k), Ok(true));
        }
        assert_eq!(half_bound_holds(&qi(4), &q(1, 4), 1), Err(QcError::AboveHalf));
    }

    #[test]
    fn unrepaired_union_bound_never_contracts() {
        for a in [1, 2, 5] {
            assert!((0..6).all(|k| linear_level(&qi(a), &q(1, 100), k) >= q(1, 100)));
        }
    }

    #[test]
    fn pair_count_and_threshold_drop() {
        let v: Vec<Q> = [2u32, 3, 4, 10].iter().map(|&a| pair_count(a)).collect();
        assert_eq!(v, vec![qi(1), qi(3), qi(6), qi(45)]);
        assert!(threshold(&pair_count(10)).unwrap() < threshold(&pair_count(4)).unwrap());
    }

    #[test]
    fn refusals() {
        assert_eq!(classify(&qi(0), &qi(1)), Err(QcError::BadRegimeInput));
        assert_eq!(first_level_below(&qi(1), &qi(1), &qi(0), 3), Err(QcError::BadEpsilon));
        assert_eq!(amp(&[qi(1)], 2), Err(QcError::ShortOverheads));
        assert_eq!(supply_threshold(&qi(1), &qi(1), &qi(1)), Err(QcError::NoSupplySuffices));
        assert_eq!(rounds_upper_bound(&qi(1), &qi(0)), Err(QcError::BadBudget));
        assert_eq!(rot_z(&q(1, 2), &q(1, 2)), Err(QcError::NotARotation));
    }

    #[test]
    fn amp_closed_form() {
        let cs = vec![qi(2), qi(3), qi(5), qi(7)];
        let got: Vec<Q> = (0..5).map(|k| amp(&cs, k).unwrap()).collect();
        assert_eq!(got, vec![qi(1), qi(2), qi(12), qi(720), qi(7 * 720 * 720)]);
        for k in 0..5 {
            assert_eq!(concv_amp_holds(&cs, &q(1, 9), k), Ok(true));
        }
    }

    #[test]
    fn constant_case_reduces_and_sandwich() {
        let cs = const_family(&qi(4), 6);
        for k in 0..7 {
            assert_eq!(concv(&cs, &q(1, 10), k).unwrap(), conc(&qi(4), &q(1, 10), k as u32));
        }
        let mixed = vec![qi(2), qi(3), qi(2), qi(3), qi(2), qi(3)];
        for k in 0..7 {
            let v = concv(&mixed, &q(1, 10), k).unwrap();
            assert!(conc(&qi(2), &q(1, 10), k as u32) <= v);
            assert!(v <= conc(&qi(3), &q(1, 10), k as u32));
        }
    }

    #[test]
    fn bounded_exponential_polynomial_stay_bounded() {
        assert_eq!(const_invariant_holds(&const_family(&qi(9), 10), &qi(9)), Ok(true));
        assert_eq!(amp_bound_holds(&const_family(&qi(9), 10), &qi(9)), Ok(true));
        for a in [1, 2, 5] {
            assert_eq!(exp_invariant_holds(&qi(a), 10), Ok(true));
            assert_eq!(amp_bound_holds(&exp_family(&qi(a), 10), &qi(4 * a)), Ok(true));
            for b in [qi(1), qi(2), qi(3), q(7, 2)] {
                assert_eq!(geom_invariant_holds(&qi(a), &b, 8), Ok(true));
                assert_eq!(
                    amp_bound_holds(&geom_family(&qi(a), &b, 8), &(qi(a) * &b * &b)),
                    Ok(true)
                );
            }
        }
        assert!((0..40u64).all(|k| (k + 1) * (k + 1) <= 2 * 2u64.pow(k as u32 + 1)));
        assert_eq!(amp_bound_holds(&poly_family(10), &qi(8)), Ok(true));
        assert_eq!(const_invariant_holds(&[qi(5)], &qi(4)), Err(QcError::OverheadOutOfRange));
    }

    #[test]
    fn double_exponential_escapes_every_bound() {
        let (a, b) = (qi(1), qi(2));
        assert_eq!(dexp_square_identity_holds(&a, &b, 10), Ok(true));
        assert_eq!(dexp_square_identity_holds(&q(3, 2), &q(5, 4), 9), Ok(true));
        let cs = dexp_family(&a, &b, 14);
        let levels: Vec<Option<usize>> =
            [2, 10, 100].iter().map(|&m| amp_escape_level(&cs, &qi(m)).unwrap()).collect();
        assert_eq!(levels, vec![Some(3), Some(7), Some(14)]);
        assert_eq!(amp_escape_level(&exp_family(&qi(1), 14), &qi(4)), Ok(None));
        assert_eq!(amp_escape_level(&poly_family(14), &qi(8)), Ok(None));
        assert_eq!(level_u32(Some(3)), Some(3));
    }

    #[test]
    fn block_size_growth_below_and_at_the_squaring_ratio() {
        let mut sizes: Vec<u32> = vec![8];
        for _ in 0..11 {
            let last = *sizes.last().unwrap();
            sizes.push(last * 3 / 2);
        }
        assert_eq!(block_exp_bound_holds(&sizes, &q(3, 2)), Ok(true));
        let cs = size_family(&qi(1), &qi(2), &sizes);
        let m = pow_u(&qi(2), 16);
        assert_eq!(amp_bound_holds(&cs, &m), Ok(true));
        let dbl: Vec<u32> = (0..10).map(|k| 1u32 << k).collect();
        let cd = size_family(&qi(1), &qi(2), &dbl);
        let lv: Vec<Option<usize>> = [2u32, 3]
            .iter()
            .map(|&e| amp_escape_level(&cd, &pow_u(&qi(2), e)).unwrap())
            .collect();
        assert_eq!(lv, vec![Some(5), Some(7)]);
        assert_eq!(block_exp_bound_holds(&dbl, &qi(2)), Err(QcError::SizeRatio));
    }

    #[test]
    fn dexp_error_leaves_unit_interval() {
        let cs = dexp_family(&qi(1), &qi(2), 14);
        for (p0, level) in [(q(1, 10), 7usize), (q(1, 50), 12usize)] {
            let first = (0..15).find(|&k| concv(&cs, &p0, k).unwrap() >= qi(1)).unwrap();
            assert_eq!(first, level);
            assert!((level..15).all(|k| concv(&cs, &p0, k).unwrap() >= qi(1)));
        }
    }

    #[test]
    fn backlog_regimes() {
        let half = q(1, 2);
        assert!(backlog_bounded_decision(&qi(1), &half, &qi(2)));
        assert_eq!(backlog(&qi(1), &half, &qi(2), &qi(5), 6).unwrap(), vec![qi(5); 7]);
        assert_eq!(
            backlog(&qi(1), &half, &qi(4), &qi(3), 5).unwrap(),
            vec![qi(3), qi(2), qi(1), qi(0), qi(0), qi(0)]
        );
        assert!(!backlog_bounded_decision(&qi(1), &half, &q(3, 2)));
        assert_eq!(
            backlog(&qi(1), &half, &q(3, 2), &qi(0), 4).unwrap(),
            vec![qi(0), q(1, 4), q(1, 2), q(3, 4), qi(1)]
        );
    }

    #[test]
    fn unit_gain_repair_never_bounds() {
        for mu in [0, 1, 10, 1000] {
            assert!(!backlog_bounded_decision(&q(1, 100), &qi(1), &qi(mu)));
            let tr = backlog(&q(1, 100), &qi(1), &qi(mu), &qi(0), 5).unwrap();
            assert_eq!(tr, (0..6).map(|k| q(k, 100)).collect::<Vec<_>>());
        }
    }

    #[test]
    fn supply_threshold_and_budget() {
        assert_eq!(supply_threshold(&qi(1), &q(1, 2), &qi(1)), Ok(qi(2)));
        assert_eq!(
            backlog(&qi(1), &q(1, 2), &qi(0), &qi(0), 3).unwrap(),
            vec![qi(0), qi(1), qi(2), qi(3)]
        );
        assert_eq!(rounds_upper_bound(&qi(10), &q(1, 2)), Ok(qi(20)));
    }

    fn rotations() -> (Mat3, Mat3) {
        (rot_z(&q(-7, 25), &q(24, 25)).unwrap(), rot_x(&q(-7, 25), &q(24, 25)).unwrap())
    }

    #[test]
    fn rotations_are_exact() {
        let (rz, rx) = rotations();
        assert!(is_rational_rotation(&rz) && is_rational_rotation(&rx));
        let bad: Mat3 = [
            [qi(2), qi(0), qi(0)],
            [qi(0), qi(1), qi(0)],
            [qi(0), qi(0), qi(1)],
        ];
        assert_eq!(bloch_step(&q(1, 2), &bad, &[qi(1), qi(0), qi(0)]), Err(QcError::NotOrthogonal));
    }

    #[test]
    fn squared_distance_contracts_exactly() {
        let (rz, rx) = rotations();
        let r: Vec3 = [q(1, 2), q(1, 3), q(1, 6)];
        let s: Vec3 = [q(-1, 5), q(2, 5), q(3, 5)];
        let hist = vec![(q(1, 10), rz.clone()), (q(1, 5), rx), (q(1, 20), rz.clone())];
        assert_eq!(decay_identity_holds(&hist, &r, &s), Ok(true));
        let f = q(9, 10) * q(4, 5) * q(19, 20);
        assert_eq!(contraction_factor_sq(&hist), &f * &f);
        let uniform: Vec<(Q, Mat3)> = (0..5).map(|_| (q(1, 10), rz.clone())).collect();
        let d0 = bloch_sq_dist(&r, &s);
        let got = bloch_sq_dist(&bloch_run(&uniform, &r).unwrap(), &bloch_run(&uniform, &s).unwrap());
        assert_eq!(got, pow_u(&q(81, 100), 5) * d0);
    }

    #[test]
    fn matrix_level_agrees_with_bloch_level() {
        let (rz, rx) = rotations();
        let u1 = unitary_about('z', &q(3, 5), &q(4, 5)).unwrap();
        let u2 = unitary_about('x', &q(3, 5), &q(4, 5)).unwrap();
        let p = q(1, 7);
        let mut r: Vec3 = [q(1, 2), q(1, 3), q(1, 6)];
        let mut rho = bloch_matrix(&r);
        for (u, rot) in [(&u1, &rz), (&u2, &rx), (&u1, &rz)] {
            rho = matrix_step(&p, u, &rho);
            r = bloch_step(&p, rot, &r).unwrap();
            assert_eq!(bloch_of_matrix(&rho), r);
        }
        assert_eq!(unitary_about('y', &q(3, 5), &q(4, 5)), Err(QcError::NotARotation));
    }

    #[test]
    fn pauli_part_squares() {
        for v in [[qi(1), qi(2), qi(3)], [q(1, 2), qi(0), q(-3, 5)], [qi(0), qi(0), qi(0)]] {
            assert!(pauli_part_squares_to_norm(&v));
        }
    }

    #[test]
    fn decay_bound_and_depth() {
        for p in [q(1, 10), q(1, 2), q(1, 1000)] {
            for t in 0..40 {
                assert_eq!(decay_le_inv_holds(&p, t), Ok(true));
            }
        }
        assert_eq!(decay_le_inv_holds(&q(3, 2), 1), Err(QcError::BadProbability));
        let t = depth_until_below(&q(1, 10), &q(1, 1000), 100_000).unwrap().unwrap();
        assert_eq!(t, 66);
        let f = q(9, 10);
        assert!(pow_u(&f, t) <= q(1, 1000) && q(1, 1000) < pow_u(&f, t - 1));
        assert!(9990 >= t);
        assert_eq!(depth_until_below(&qi(1), &q(1, 2), 5), Err(QcError::BadDepthInput));
    }

    #[test]
    fn all_conditions_are_needed() {
        let big = qi(1_000_000);
        let ok = viability_report(&qi(1), &q(1, 2), &qi(1), &qi(2), &qi(4), &q(1, 10), &big, &q(1, 100));
        assert!(ok.certified);
        assert_eq!(ok.level, level_for_failure(&qi(4), &q(1, 10), &big, &q(1, 100), 16));
        assert!(!viability_report(&qi(1), &q(1, 2), &qi(1), &q(19, 10), &qi(4), &q(1, 10), &big, &q(1, 100)).certified);
        assert!(!viability_report(&qi(1), &qi(1), &qi(1), &qi(100), &qi(4), &q(1, 10), &big, &q(1, 100)).certified);
        assert!(!viability_report(&qi(1), &q(1, 2), &qi(1), &qi(2), &qi(4), &q(3, 10), &big, &q(1, 100)).certified);
    }

    #[test]
    fn level_grows_doubly_logarithmically() {
        let small = level_for_failure(&qi(4), &q(1, 10), &qi(1_000), &q(1, 100), 16).unwrap();
        let huge_l = Q::from_integer(BigInt::from(10u8).pow(60));
        let huge = level_for_failure(&qi(4), &q(1, 10), &huge_l, &q(1, 100), 16).unwrap();
        assert!(small < huge && huge - small <= 5);
        assert!(AUTHORITY_FENCE.contains("not a proof"));
    }
}
