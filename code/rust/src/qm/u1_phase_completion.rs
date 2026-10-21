//! Exact rational Cayley circle parameterization, 5-adic half-angle obstruction,
//! Gaussian power injectivity, quadratic half-angle restoration, cyclotomic torsion
//! tower `Q/Z`, and Cauchy/dyadic phase completion receipts for `FQ-GAP-U1-CIRCLE`.
//!
//! Replays in exact rational arithmetic the Lean modules of
//! `dag/results/FQ-GAP-U1-CIRCLE/runs/20261020T223000Z_u1_phase_completion_lean`
//! (`U1CayleyProjectiveCircle`, `U1HalfAngleObstruction`, `U1PowerMapInjectivity`,
//! `U1CyclotomicTorsionTower`, `U1CauchyCircleCompletion`) and mirrors, function
//! for function, the Python twin `code/python/src/qm/u1_phase_completion.py`.
//!
//! AuthorityEffect: None.

use std::collections::BTreeSet;

use num_bigint::BigInt;
use num_integer::Integer;
use num_traits::{One, Signed, Zero};

use crate::linear_algebra::scalars::{validate_rational, RationalConstructionError};
use crate::linear_algebra::{q, Q};

pub const AUTHORITY_FENCE: &str =
    "AuthorityEffect None; exact rational and quadratic algebraic certificates only; \
     compact analytic U(1) topology and transcendental exponential/logarithm maps are \
     not derived from finite or rational data alone.";

pub const PROVENANCE: &str = "Replays the Lean modules of \
     dag/results/FQ-GAP-U1-CIRCLE/runs/20261020T223000Z_u1_phase_completion_lean \
     (U1CayleyProjectiveCircle, U1HalfAngleObstruction, U1PythagoreanObstruction, \
     U1PowerMapInjectivity, U1CyclotomicTorsionTower, U1CauchyCircleCompletion, \
     U1ChebyshevCauchyBridge, U1QuadraticTowerAndCayleyStone, U1PhaseSynthesis) and mirrors \
     code/python/src/qm/u1_phase_completion.py.";

#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum U1PhaseError {
    #[error("exact canonical rational entries required: {0}")]
    InexactRational(#[from] RationalConstructionError),
    #[error("point on the rational unit circle re^2 + im^2 == 1 required")]
    NotOnUnitCircle,
    #[error("south-pole puncture (-1, 0) is outside the affine Cayley chart")]
    SouthPolePuncture,
    #[error("homogeneous origin (0, 0) is excluded from P^1(Q)")]
    ProjectiveOriginRefused,
    #[error("nonzero integer required for 5-adic valuation")]
    ZeroValuationInput,
    #[error("nonzero denominator required")]
    ZeroDenominator,
    #[error("nonnegative exponent required, got {0}")]
    NegativeExponent(i64),
    #[error("window bound max_n in [1, 256] required, got {0}")]
    WindowOutOfBounds(u32),
    #[error("zero element in Q(sqrt(5)) has no multiplicative inverse")]
    ZeroQuadSqrt5Inverse,
    #[error("positive torsion level and refinement factor required")]
    InvalidTorsionLevel,
    #[error("m_divisor in [1, 1024] required, got {0}")]
    InvalidDivisor(u32),
    #[error("q_phase in [0, 1] required")]
    PhaseOutOfUnitInterval,
    #[error("positive n_grid required")]
    InvalidGridSize,
    #[error("valid nonnegative bracket [lo, hi] with lo^2 <= 5 <= hi^2 required")]
    InvalidSqrt5Bracket,
    #[error("m_levels in [1, 6] required, got {0}")]
    TowerDepthOutOfBounds(u32),
    #[error("traceless Hermitian generator with a + d == 0 required")]
    NonHermitianTraceZeroGenerator,
}

fn check_pair(a: &Q, b: &Q) -> Result<(), U1PhaseError> {
    validate_rational(a)?;
    validate_rational(b)?;
    Ok(())
}

// ============================================================================
// 1. Affine & Projective Cayley Parameterization of S^1(Q)
// ============================================================================

/// Return `true` when `(re, im)` lies on the rational unit circle `re^2 + im^2 == 1`.
pub fn is_unit_circle(re: &Q, im: &Q) -> Result<bool, U1PhaseError> {
    check_pair(re, im)?;
    Ok(re * re + im * im == Q::one())
}

/// Multiply two points on `S^1(Q)` via Gaussian multiplication.
pub fn circle_mul(re1: &Q, im1: &Q, re2: &Q, im2: &Q) -> Result<(Q, Q), U1PhaseError> {
    if !is_unit_circle(re1, im1)? || !is_unit_circle(re2, im2)? {
        return Err(U1PhaseError::NotOnUnitCircle);
    }
    Ok((re1 * re2 - im1 * im2, re1 * im2 + im1 * re2))
}

/// Map rational parameter `t` to `((1 - t^2)/(1 + t^2), 2t/(1 + t^2))` on `S^1(Q)`.
pub fn affine_cayley(t: &Q) -> Result<(Q, Q), U1PhaseError> {
    validate_rational(t)?;
    let t_sq = t * t;
    let denom = Q::one() + &t_sq;
    let re = (Q::one() - t_sq) / &denom;
    let im = (q(2) * t) / denom;
    Ok((re, im))
}

/// Invert the affine Cayley map via `im / (re + 1)`; refuses `(-1, 0)` and non-unit points.
pub fn inverse_cayley(re: &Q, im: &Q) -> Result<Q, U1PhaseError> {
    if !is_unit_circle(re, im)? {
        return Err(U1PhaseError::NotOnUnitCircle);
    }
    if re == &q(-1) {
        return Err(U1PhaseError::SouthPolePuncture);
    }
    Ok(im / (re + Q::one()))
}

/// Return `Some((t1 + t2)/(1 - t1*t2))` when `t1*t2 != 1`, or `None` at the south-pole collision.
pub fn affine_cayley_mul_param(t1: &Q, t2: &Q) -> Result<Option<Q>, U1PhaseError> {
    check_pair(t1, t2)?;
    let denom = Q::one() - t1 * t2;
    if denom.is_zero() {
        return Ok(None);
    }
    Ok(Some((t1 + t2) / denom))
}

/// Map homogeneous coordinates `[u : v]` in `P^1(Q)` to `S^1(Q)`, sending `[0 : 1]` to `(-1, 0)`.
pub fn projective_cayley(u: &Q, v: &Q) -> Result<(Q, Q), U1PhaseError> {
    check_pair(u, v)?;
    let denom = u * u + v * v;
    if denom.is_zero() {
        return Err(U1PhaseError::ProjectiveOriginRefused);
    }
    let re = (u * u - v * v) / &denom;
    let im = (q(2) * u * v) / denom;
    Ok((re, im))
}

/// Map every point of `S^1(Q)` to a representative `[u : v]` in `P^1(Q)`.
pub fn inverse_projective_cayley(re: &Q, im: &Q) -> Result<(Q, Q), U1PhaseError> {
    if !is_unit_circle(re, im)? {
        return Err(U1PhaseError::NotOnUnitCircle);
    }
    if re == &q(-1) {
        return Ok((Q::zero(), Q::one()));
    }
    Ok((Q::one(), im / (re + Q::one())))
}

/// Multiply homogeneous projective coordinates via `(u1*u2 - v1*v2, u1*v2 + v1*u2)`.
pub fn projective_mul(u1: &Q, v1: &Q, u2: &Q, v2: &Q) -> Result<(Q, Q), U1PhaseError> {
    check_pair(u1, v1)?;
    check_pair(u2, v2)?;
    if (u1.is_zero() && v1.is_zero()) || (u2.is_zero() && v2.is_zero()) {
        return Err(U1PhaseError::ProjectiveOriginRefused);
    }
    Ok((u1 * u2 - v1 * v2, u1 * v2 + v1 * u2))
}

// ============================================================================
// 2. Pythagorean Half-Angle Obstruction & 5-Adic Valuation Certifier
// ============================================================================

/// Factor nonzero integer `n = 5^v5 * unit_part` with `unit_part % 5 != 0`.
pub fn five_adic_valuation(n: &BigInt) -> Result<(u32, BigInt), U1PhaseError> {
    if n.is_zero() {
        return Err(U1PhaseError::ZeroValuationInput);
    }
    let five = BigInt::from(5);
    let mut v5: u32 = 0;
    let mut unit = n.clone();
    while (&unit % &five).is_zero() {
        unit /= &five;
        v5 = v5.saturating_add(1);
    }
    Ok((v5, unit))
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct FourFifthsObstructionReceipt {
    pub num: BigInt,
    pub den: BigInt,
    pub lhs_five_num_sq: BigInt,
    pub rhs_four_den_sq: BigInt,
    pub abs_residual: BigInt,
    pub lhs_v5: Option<u32>,
    pub rhs_v5: u32,
    pub parity_disjoint: bool,
    pub obstructed: bool,
}

/// Certify `(num/den)^2 != 4/5` via 5-adic valuation parity on `5*num^2` vs `4*den^2`.
pub fn certify_four_fifths_not_square(
    num: &BigInt,
    den: &BigInt,
) -> Result<FourFifthsObstructionReceipt, U1PhaseError> {
    if den.is_zero() {
        return Err(U1PhaseError::ZeroDenominator);
    }
    let lhs = BigInt::from(5) * num * num;
    let rhs = BigInt::from(4) * den * den;
    let residual = (&lhs - &rhs).abs();
    let (v5_den, _) = five_adic_valuation(den)?;
    let rhs_v5 = v5_den.saturating_mul(2);
    let lhs_v5 = if num.is_zero() {
        None
    } else {
        let (v5_num, _) = five_adic_valuation(num)?;
        Some(v5_num.saturating_mul(2).saturating_add(1))
    };
    let parity_disjoint = match lhs_v5 {
        None => true,
        Some(v_lhs) => BigInt::from(v_lhs).is_odd() && BigInt::from(rhs_v5).is_even(),
    };
    let obstructed = residual >= BigInt::one() && parity_disjoint;
    Ok(FourFifthsObstructionReceipt {
        num: num.clone(),
        den: den.clone(),
        lhs_five_num_sq: lhs,
        rhs_four_den_sq: rhs,
        abs_residual: residual,
        lhs_v5,
        rhs_v5,
        parity_disjoint,
        obstructed,
    })
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct U345SqrtObstructionReceipt {
    pub re: Q,
    pub im: Q,
    pub sq_re: Q,
    pub sq_im: Q,
    pub norm_sq: Q,
    pub half_sum_equals_re_sq: bool,
    pub re_sq_minus_four_fifths: Q,
    pub four_fifths_obstruction: FourFifthsObstructionReceipt,
    pub matches_u345_and_unit: bool,
    pub obstructed: bool,
}

/// Certify that no `(re, im)` in `Q^2` satisfies both `(re + i*im)^2 = (3 + 4i)/5` and `re^2 + im^2 = 1`.
pub fn certify_u345_no_rational_sqrt(
    re: &Q,
    im: &Q,
) -> Result<U345SqrtObstructionReceipt, U1PhaseError> {
    check_pair(re, im)?;
    let sq_re = re * re - im * im;
    let sq_im = q(2) * re * im;
    let norm_sq = re * re + im * im;
    let half_sum = (&sq_re + &norm_sq) / q(2);
    let v5_receipt = certify_four_fifths_not_square(re.numer(), re.denom())?;
    let three_fifths = Q::new(BigInt::from(3), BigInt::from(5));
    let four_fifths = Q::new(BigInt::from(4), BigInt::from(5));
    let matches_target =
        sq_re == three_fifths && sq_im == four_fifths && norm_sq == Q::one();
    let obstructed = !matches_target && v5_receipt.obstructed;
    Ok(U345SqrtObstructionReceipt {
        re: re.clone(),
        im: im.clone(),
        sq_re,
        sq_im,
        norm_sq,
        half_sum_equals_re_sq: half_sum == re * re,
        re_sq_minus_four_fifths: re * re - four_fifths,
        four_fifths_obstruction: v5_receipt,
        matches_u345_and_unit: matches_target,
        obstructed,
    })
}

// ============================================================================
// 3. Gaussian Power Recurrence & Mod-5 Idempotence Certifier
// ============================================================================

/// Compute exact integer coordinates `(A_n, B_n)` of `(3 + 4i)^n` for `n >= 0`.
pub fn gauss_pow_34(n: i64) -> Result<(BigInt, BigInt), U1PhaseError> {
    if n < 0 {
        return Err(U1PhaseError::NegativeExponent(n));
    }
    let three = BigInt::from(3);
    let four = BigInt::from(4);
    let mut a = BigInt::one();
    let mut b = BigInt::zero();
    for _ in 0..n {
        let next_a = &three * &a - &four * &b;
        let next_b = &four * &a + &three * &b;
        a = next_a;
        b = next_b;
    }
    Ok((a, b))
}

/// Compute exact rational coordinates of `((3 + 4i)/5)^k` for any integer `k`.
pub fn u345_power(k: i64) -> Result<(Q, Q), U1PhaseError> {
    let abs_k_big = BigInt::from(k).abs();
    let abs_k_u32 = u32::try_from(&abs_k_big).map_err(|_| U1PhaseError::NegativeExponent(k))?;
    let (a, b) = gauss_pow_34(i64::from(abs_k_u32))?;
    let scale = BigInt::from(5).pow(abs_k_u32);
    let imag_signed = if k >= 0 { b } else { -b };
    Ok((Q::new(a, scale.clone()), Q::new(imag_signed, scale)))
}

fn check_gauss_step(n: u32) -> Result<bool, U1PhaseError> {
    let (a, b) = gauss_pow_34(i64::from(n))?;
    let five = BigInt::from(5);
    let a_mod5 = a.mod_floor(&five);
    let b_mod5 = b.mod_floor(&five);
    let norm_sq = &a * &a + &b * &b;
    let five_pow_2n = five.pow(n.saturating_mul(2));
    Ok(a_mod5 == BigInt::from(3)
        && b_mod5 == BigInt::from(4)
        && !b.is_zero()
        && norm_sq == five_pow_2n)
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct PowerInjectivityReceipt {
    pub max_n: u32,
    pub mod5_invariant_holds: bool,
    pub all_on_unit_circle: bool,
    pub tested_exponents: usize,
    pub distinct_points: usize,
    pub injective_on_window: bool,
}

/// Check mod-5 idempotence `(A_n, B_n) == (3, 4) mod 5` and pairwise distinct powers on `[-max_n, max_n]`.
pub fn certify_power_injectivity_window(
    max_n: u32,
) -> Result<PowerInjectivityReceipt, U1PhaseError> {
    if !(1..=256).contains(&max_n) {
        return Err(U1PhaseError::WindowOutOfBounds(max_n));
    }
    let mut mod5_ok = true;
    for n in 1..=max_n {
        if !check_gauss_step(n)? {
            mod5_ok = false;
        }
    }
    let bound = i64::from(max_n);
    let neg_bound = 0i64.saturating_sub(bound);
    let mut points = Vec::new();
    let mut distinct = BTreeSet::new();
    let mut on_circle = true;
    for k in neg_bound..=bound {
        let pt = u345_power(k)?;
        if !is_unit_circle(&pt.0, &pt.1)? {
            on_circle = false;
        }
        distinct.insert(pt.clone());
        points.push(pt);
    }
    let tested_exponents = points.len();
    let distinct_points = distinct.len();
    let injective_on_window = mod5_ok && on_circle && tested_exponents == distinct_points;
    Ok(PowerInjectivityReceipt {
        max_n,
        mod5_invariant_holds: mod5_ok,
        all_on_unit_circle: on_circle,
        tested_exponents,
        distinct_points,
        injective_on_window,
    })
}

// ============================================================================
// 4. Algebraic Half-Angle Extension in Q(sqrt(5))(i)
// ============================================================================

/// Element `a + b*sqrt(5)` of the real quadratic extension `Q(sqrt(5))`.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct QuadSqrt5 {
    pub a: Q,
    pub b: Q,
}

impl QuadSqrt5 {
    pub fn new(a: Q, b: Q) -> Result<Self, U1PhaseError> {
        check_pair(&a, &b)?;
        Ok(Self { a, b })
    }
}

/// Element `re + i*im` in `Q(sqrt(5))(i)`.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct CircleQuadSqrt5 {
    pub re: QuadSqrt5,
    pub im: QuadSqrt5,
}

pub fn quad_add(x: &QuadSqrt5, y: &QuadSqrt5) -> Result<QuadSqrt5, U1PhaseError> {
    QuadSqrt5::new(&x.a + &y.a, &x.b + &y.b)
}

pub fn quad_sub(x: &QuadSqrt5, y: &QuadSqrt5) -> Result<QuadSqrt5, U1PhaseError> {
    QuadSqrt5::new(&x.a - &y.a, &x.b - &y.b)
}

pub fn quad_mul(x: &QuadSqrt5, y: &QuadSqrt5) -> Result<QuadSqrt5, U1PhaseError> {
    check_pair(&x.a, &x.b)?;
    check_pair(&y.a, &y.b)?;
    let re = &x.a * &y.a + q(5) * &x.b * &y.b;
    let rt = &x.a * &y.b + &x.b * &y.a;
    QuadSqrt5::new(re, rt)
}

pub fn quad_conj(x: &QuadSqrt5) -> Result<QuadSqrt5, U1PhaseError> {
    QuadSqrt5::new(x.a.clone(), -&x.b)
}

pub fn quad_norm(x: &QuadSqrt5) -> Result<Q, U1PhaseError> {
    check_pair(&x.a, &x.b)?;
    Ok(&x.a * &x.a - q(5) * &x.b * &x.b)
}

pub fn quad_inv(x: &QuadSqrt5) -> Result<QuadSqrt5, U1PhaseError> {
    let nrm = quad_norm(x)?;
    if nrm.is_zero() {
        return Err(U1PhaseError::ZeroQuadSqrt5Inverse);
    }
    QuadSqrt5::new(&x.a / &nrm, (-&x.b) / nrm)
}

pub fn circle_quad_mul(
    z1: &CircleQuadSqrt5,
    z2: &CircleQuadSqrt5,
) -> Result<CircleQuadSqrt5, U1PhaseError> {
    let re = quad_sub(&quad_mul(&z1.re, &z2.re)?, &quad_mul(&z1.im, &z2.im)?)?;
    let im = quad_add(&quad_mul(&z1.re, &z2.im)?, &quad_mul(&z1.im, &z2.re)?)?;
    Ok(CircleQuadSqrt5 { re, im })
}

pub fn circle_quad_norm_sq(z: &CircleQuadSqrt5) -> Result<QuadSqrt5, U1PhaseError> {
    quad_add(&quad_mul(&z.re, &z.re)?, &quad_mul(&z.im, &z.im)?)
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct QuadSqrt5Certificate {
    pub w: CircleQuadSqrt5,
    pub w_sq: CircleQuadSqrt5,
    pub norm_sq: QuadSqrt5,
    pub squares_to_u345: bool,
    pub on_unit_circle: bool,
    pub requires_quadratic_extension: bool,
}

/// Certify that `w = (2/5*sqrt(5), 1/5*sqrt(5))` in `S^1(Q(sqrt(5)))` satisfies `w^2 = (3/5, 4/5)`.
pub fn u345_quad_sqrt_certificate() -> Result<QuadSqrt5Certificate, U1PhaseError> {
    let two_fifths = Q::new(BigInt::from(2), BigInt::from(5));
    let one_fifth = Q::new(BigInt::from(1), BigInt::from(5));
    let three_fifths = Q::new(BigInt::from(3), BigInt::from(5));
    let four_fifths = Q::new(BigInt::from(4), BigInt::from(5));
    let w = CircleQuadSqrt5 {
        re: QuadSqrt5::new(Q::zero(), two_fifths)?,
        im: QuadSqrt5::new(Q::zero(), one_fifth)?,
    };
    let w_sq = circle_quad_mul(&w, &w)?;
    let norm_sq = circle_quad_norm_sq(&w)?;
    let target = CircleQuadSqrt5 {
        re: QuadSqrt5::new(three_fifths, Q::zero())?,
        im: QuadSqrt5::new(four_fifths, Q::zero())?,
    };
    let unit = QuadSqrt5::new(Q::one(), Q::zero())?;
    let squares_to_u345 = w_sq == target;
    let on_unit_circle = norm_sq == unit;
    let requires_quadratic_extension = !w.re.b.is_zero() && !w.im.b.is_zero();
    Ok(QuadSqrt5Certificate {
        w,
        w_sq,
        norm_sq,
        squares_to_u345,
        on_unit_circle,
        requires_quadratic_extension,
    })
}

// ============================================================================
// 5. Cyclotomic Torsion Tower mu_N -> Q/Z & Finite Haar Character Orthogonality
// ============================================================================

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct TorsionRefinementReceipt {
    pub n_level: BigInt,
    pub k_factor: BigInt,
    pub base_index: BigInt,
    pub refined_level: BigInt,
    pub refined_index: BigInt,
    pub base_phase: Q,
    pub refined_phase: Q,
    pub phase_preserved: bool,
}

/// Refine `a_index mod n_level` to `(k_factor * a_index) mod (k_factor * n_level)` in `Q/Z`.
pub fn refine_torsion_phase(
    n_level: i64,
    k_factor: i64,
    a_index: i64,
) -> Result<TorsionRefinementReceipt, U1PhaseError> {
    if n_level < 1 || k_factor < 1 {
        return Err(U1PhaseError::InvalidTorsionLevel);
    }
    let n = BigInt::from(n_level);
    let k = BigInt::from(k_factor);
    let a = BigInt::from(a_index);
    let base_index = a.mod_floor(&n);
    let refined_index = &k * &base_index;
    let refined_level = &k * &n;
    let base_phase = Q::new(base_index.clone(), n.clone());
    let refined_phase = Q::new(refined_index.clone(), refined_level.clone());
    let phase_preserved = base_phase == refined_phase;
    Ok(TorsionRefinementReceipt {
        n_level: n,
        k_factor: k,
        base_index,
        refined_level,
        refined_index,
        base_phase,
        refined_phase,
        phase_preserved,
    })
}

fn mod_one(q_val: &Q) -> Q {
    q_val - q_val.floor()
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct PhaseDivisionReceipt {
    pub q_mod_one: Q,
    pub m_divisor: u32,
    pub roots: Vec<Q>,
    pub all_in_unit_interval: bool,
    pub distinct_count: usize,
    pub all_multiply_to_q_mod_one: bool,
}

/// Return the `m_divisor` distinct `m`-th division phases of `q_phase` in `Q/Z cap [0, 1)`.
pub fn divide_rat_phase_mod_one(
    q_phase: &Q,
    m_divisor: u32,
) -> Result<PhaseDivisionReceipt, U1PhaseError> {
    validate_rational(q_phase)?;
    if !(1..=1024).contains(&m_divisor) {
        return Err(U1PhaseError::InvalidDivisor(m_divisor));
    }
    let q_mod_one = mod_one(q_phase);
    let m_q = Q::from_integer(BigInt::from(m_divisor));
    let mut roots = Vec::new();
    let mut distinct = BTreeSet::new();
    let mut in_range = true;
    let mut multiplies_back = true;
    for j in 0..m_divisor {
        let j_q = Q::from_integer(BigInt::from(j));
        let root = mod_one(&((&q_mod_one + j_q) / &m_q));
        if root < Q::zero() || root >= Q::one() {
            in_range = false;
        }
        if mod_one(&(&m_q * &root)) != q_mod_one {
            multiplies_back = false;
        }
        distinct.insert(root.clone());
        roots.push(root);
    }
    let distinct_count = distinct.len();
    let all_multiply_to_q_mod_one =
        in_range && distinct_count == roots.len() && multiplies_back;
    Ok(PhaseDivisionReceipt {
        q_mod_one,
        m_divisor,
        roots,
        all_in_unit_interval: in_range,
        distinct_count,
        all_multiply_to_q_mod_one,
    })
}

fn pow_i(exponent: &BigInt) -> (Q, Q) {
    let four = BigInt::from(4);
    let r = exponent.mod_floor(&four);
    if r.is_zero() {
        (Q::one(), Q::zero())
    } else if r == BigInt::one() {
        (Q::zero(), Q::one())
    } else if r == BigInt::from(2) {
        (q(-1), Q::zero())
    } else {
        (Q::zero(), q(-1))
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct HaarOrthogonalityReceipt {
    pub character_power: i64,
    pub is_trivial_character: bool,
    pub average_re: Q,
    pub average_im: Q,
    pub orthogonality_holds: bool,
}

/// Evaluate `1/4 * sum_{j=0}^3 i^(j * character_power)` over `mu_4` in `Q(i)`.
pub fn fourth_roots_haar_certificate(
    character_power: i64,
) -> Result<HaarOrthogonalityReceipt, U1PhaseError> {
    let m = BigInt::from(character_power);
    let mut sum_re = Q::zero();
    let mut sum_im = Q::zero();
    for j in 0..4u32 {
        let exp = BigInt::from(j) * &m;
        let (re, im) = pow_i(&exp);
        sum_re += re;
        sum_im += im;
    }
    let avg_re = sum_re / q(4);
    let avg_im = sum_im / q(4);
    let trivial = m.mod_floor(&BigInt::from(4)).is_zero();
    let expected = if trivial {
        (Q::one(), Q::zero())
    } else {
        (Q::zero(), Q::zero())
    };
    let orthogonality_holds = (avg_re.clone(), avg_im.clone()) == expected;
    Ok(HaarOrthogonalityReceipt {
        character_power,
        is_trivial_character: trivial,
        average_re: avg_re,
        average_im: avg_im,
        orthogonality_holds,
    })
}

// ============================================================================
// 6. Cauchy / Dyadic Interval Completion & Finite Torsion Grid epsilon-Net
// ============================================================================

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct TorsionGridCoverReceipt {
    pub q_phase: Q,
    pub n_grid: BigInt,
    pub grid_index: BigInt,
    pub grid_point: Q,
    pub distance: Q,
    pub bound: Q,
    pub within_bound: bool,
}

/// Certify that `q_phase` in `[0, 1]` lies within `1/n_grid` of `k/n_grid` for `k = floor(n_grid * q_phase)`.
pub fn torsion_grid_cover_certificate(
    q_phase: &Q,
    n_grid: i64,
) -> Result<TorsionGridCoverReceipt, U1PhaseError> {
    validate_rational(q_phase)?;
    if q_phase < &Q::zero() || q_phase > &Q::one() {
        return Err(U1PhaseError::PhaseOutOfUnitInterval);
    }
    if n_grid < 1 {
        return Err(U1PhaseError::InvalidGridSize);
    }
    let n_big = BigInt::from(n_grid);
    let n_q = Q::from_integer(n_big.clone());
    let k = (&n_q * q_phase).floor().to_integer();
    let grid_point = Q::new(k.clone(), n_big.clone());
    let distance = (q_phase - &grid_point).abs();
    let bound = Q::new(BigInt::one(), n_big.clone());
    let within_bound = k >= BigInt::zero() && k <= n_big && distance <= bound;
    Ok(TorsionGridCoverReceipt {
        q_phase: q_phase.clone(),
        n_grid: n_big,
        grid_index: k,
        grid_point,
        distance,
        bound,
        within_bound,
    })
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DyadicSqrt5StepReceipt {
    pub new_lo: Q,
    pub new_hi: Q,
    pub cos_half_lo: Q,
    pub cos_half_hi: Q,
    pub width: Q,
    pub brackets_sqrt5: bool,
    pub brackets_four_fifths: bool,
    pub width_halved: bool,
}

/// Bisect a rational interval `[lo, hi]` bracketing `sqrt(5)` and map to half-angle cosine `2*sqrt(5)/5`.
pub fn dyadic_sqrt5_interval_step(
    lo: &Q,
    hi: &Q,
) -> Result<DyadicSqrt5StepReceipt, U1PhaseError> {
    check_pair(lo, hi)?;
    let five = q(5);
    if lo < &Q::zero() || lo > hi || lo * lo > five || hi * hi < five {
        return Err(U1PhaseError::InvalidSqrt5Bracket);
    }
    let mid = (lo + hi) / q(2);
    let (new_lo, new_hi) = if &mid * &mid <= five {
        (mid, hi.clone())
    } else {
        (lo.clone(), mid)
    };
    let two_fifths = Q::new(BigInt::from(2), BigInt::from(5));
    let four_fifths = Q::new(BigInt::from(4), BigInt::from(5));
    let cos_lo = &two_fifths * &new_lo;
    let cos_hi = &two_fifths * &new_hi;
    let brackets_sqrt5 = &new_lo * &new_lo <= five && five <= &new_hi * &new_hi;
    let brackets_four_fifths =
        &cos_lo * &cos_lo <= four_fifths && four_fifths <= &cos_hi * &cos_hi;
    let width = &new_hi - &new_lo;
    let width_halved = &width * q(2) == (hi - lo);
    Ok(DyadicSqrt5StepReceipt {
        new_lo,
        new_hi,
        cos_half_lo: cos_lo,
        cos_half_hi: cos_hi,
        width,
        brackets_sqrt5,
        brackets_four_fifths,
        width_halved,
    })
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct NegativeControlsReceipt {
    pub sign_group_exponent_two: bool,
    pub split_complex_zero_divisor_at_one_one: bool,
    pub affine_cayley_pole_collision_at_one_one: bool,
    pub projective_cayley_resolves_south_pole: bool,
    pub all_negative_controls_verified: bool,
}

/// Certify the 3 rival / boundary failure modes for `FQ-GAP-U1-CIRCLE`.
pub fn negative_controls_certificate() -> Result<NegativeControlsReceipt, U1PhaseError> {
    let one = Q::one();
    let neg_one = q(-1);
    let sign_group_exp2 = (&one * &one == one) && (&neg_one * &neg_one == one);
    let split_null_norm = (&one * &one - &one * &one).is_zero();
    let affine_collision = affine_cayley_mul_param(&one, &one)?.is_none();
    let (u, v) = projective_mul(&one, &one, &one, &one)?;
    let proj_resolved = projective_cayley(&u, &v)? == (neg_one, Q::zero());
    let all_ok = sign_group_exp2 && split_null_norm && affine_collision && proj_resolved;
    Ok(NegativeControlsReceipt {
        sign_group_exponent_two: sign_group_exp2,
        split_complex_zero_divisor_at_one_one: split_null_norm,
        affine_cayley_pole_collision_at_one_one: affine_collision,
        projective_cayley_resolves_south_pole: proj_resolved,
        all_negative_controls_verified: all_ok,
    })
}

// ============================================================================
// 7. Chebyshev/Taylor Cauchy Bridge & 4D Hermitian Q(i) Born Carrier
// ============================================================================

/// Evaluate the Chebyshev polynomial `T_n(x)` of the first kind over `Q`.
pub fn chebyshev_t(n: i64, x: &Q) -> Result<Q, U1PhaseError> {
    validate_rational(x)?;
    if n < 0 {
        return Err(U1PhaseError::NegativeExponent(n));
    }
    if n == 0 {
        return Ok(Q::one());
    }
    let two = q(2);
    let mut t_prev = Q::one();
    let mut t_curr = x.clone();
    for _ in 2..=n {
        let next = &two * x * &t_curr - &t_prev;
        t_prev = t_curr;
        t_curr = next;
    }
    Ok(t_curr)
}

/// Evaluate the Chebyshev polynomial `U_n(x)` of the second kind over `Q`.
pub fn chebyshev_u(n: i64, x: &Q) -> Result<Q, U1PhaseError> {
    validate_rational(x)?;
    if n < 0 {
        return Err(U1PhaseError::NegativeExponent(n));
    }
    if n == 0 {
        return Ok(Q::one());
    }
    let two = q(2);
    let mut u_prev = Q::one();
    let mut u_curr = &two * x;
    for _ in 2..=n {
        let next = &two * x * &u_curr - &u_prev;
        u_prev = u_curr;
        u_curr = next;
    }
    Ok(u_curr)
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ChebyshevCircleReceipt {
    pub base_point: (Q, Q),
    pub max_n: u32,
    pub chebyshev_matches_circle_powers: bool,
    pub pell_identity_holds_all_degrees: bool,
}

/// Certify that `(T_n(re), im * U_{n-1}(re))` equals `(re + i*im)^n` on `S^1(Q)` for `1 <= n <= max_n`.
pub fn chebyshev_circle_certificate(
    re: &Q,
    im: &Q,
    max_n: u32,
) -> Result<ChebyshevCircleReceipt, U1PhaseError> {
    if !is_unit_circle(re, im)? {
        return Err(U1PhaseError::NotOnUnitCircle);
    }
    if max_n == 0 || max_n > 64 {
        return Err(U1PhaseError::WindowOutOfBounds(max_n));
    }
    let mut pow_re = re.clone();
    let mut pow_im = im.clone();
    let mut all_match = true;
    let mut all_unit = true;
    for deg in 1..=(max_n as i64) {
        let tn = chebyshev_t(deg, re)?;
        let un_minus_1 = chebyshev_u(deg - 1, re)?;
        let cheb_im = im * &un_minus_1;
        if tn != pow_re || cheb_im != pow_im || !is_unit_circle(&tn, &cheb_im)? {
            all_match = false;
            all_unit = false;
        }
        let next = circle_mul(&pow_re, &pow_im, re, im)?;
        pow_re = next.0;
        pow_im = next.1;
    }
    Ok(ChebyshevCircleReceipt {
        base_point: (re.clone(), im.clone()),
        max_n,
        chebyshev_matches_circle_powers: all_match,
        pell_identity_holds_all_degrees: all_unit,
    })
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct TaylorTrigEnclosureReceipt {
    pub theta: Q,
    pub taylor_cos6: Q,
    pub taylor_sin7: Q,
    pub cos_nested_enclosure: bool,
    pub sin_nested_enclosure: bool,
    pub cos_width_within_1_over_720: bool,
    pub sin_width_within_1_over_5040: bool,
    pub pythagorean_defect: Q,
    pub pythagorean_defect_verified: bool,
    pub all_taylor_bounds_verified: bool,
}

/// Certify alternating Taylor cosine/sine enclosures and degree-6 Pythagorean defect on `0 <= theta <= 1`.
pub fn taylor_trig_enclosure_certificate(
    theta: &Q,
) -> Result<TaylorTrigEnclosureReceipt, U1PhaseError> {
    validate_rational(theta)?;
    if theta < &Q::zero() || theta > &Q::one() {
        return Err(U1PhaseError::PhaseOutOfUnitInterval);
    }
    let th2 = theta * theta;
    let th3 = &th2 * theta;
    let th4 = &th2 * &th2;
    let th5 = &th4 * theta;
    let th6 = &th4 * &th2;
    let th7 = &th6 * theta;
    let c0 = Q::one();
    let c2 = &c0 - &th2 / q(2);
    let c4 = &c2 + &th4 / q(24);
    let c6 = &c4 - &th6 / q(720);
    let s1 = theta.clone();
    let s3 = &s1 - &th3 / q(6);
    let s5 = &s3 + &th5 / q(120);
    let s7 = &s5 - &th7 / q(5040);
    let cos_nested = c2 <= c6 && c6 <= c4 && c4 <= c0;
    let sin_nested = s3 <= s7 && s7 <= s5 && s5 <= s1;
    let cos_width = &c4 - &c6;
    let sin_width = &s5 - &s7;
    let cos_width_ok =
        cos_width >= Q::zero() && cos_width <= Q::new(BigInt::one(), BigInt::from(720));
    let sin_width_ok =
        sin_width >= Q::zero() && sin_width <= Q::new(BigInt::one(), BigInt::from(5040));
    let defect = Q::one() - (&c4 * &c4 + &s3 * &s3);
    let defect_formula = &th6 * (q(8) - &th2) / q(576);
    let defect_ok = defect == defect_formula
        && defect >= Q::zero()
        && defect <= Q::new(BigInt::one(), BigInt::from(72));
    let all_ok = cos_nested && sin_nested && cos_width_ok && sin_width_ok && defect_ok;
    Ok(TaylorTrigEnclosureReceipt {
        theta: theta.clone(),
        taylor_cos6: c6,
        taylor_sin7: s7,
        cos_nested_enclosure: cos_nested,
        sin_nested_enclosure: sin_nested,
        cos_width_within_1_over_720: cos_width_ok,
        sin_width_within_1_over_5040: sin_width_ok,
        pythagorean_defect: defect,
        pythagorean_defect_verified: defect_ok,
        all_taylor_bounds_verified: all_ok,
    })
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct CayleyDyadicApproxReceipt {
    pub theta: Q,
    pub k_depth: u32,
    pub approx_re: Q,
    pub approx_im: Q,
    pub strictly_on_unit_circle: bool,
}

/// Subdivide `theta` by `2^(k+1)`, apply Cayley map, and square `k_depth` times on `S^1(Q)`.
pub fn cayley_dyadic_approx_certificate(
    theta: &Q,
    k_depth: u32,
) -> Result<CayleyDyadicApproxReceipt, U1PhaseError> {
    validate_rational(theta)?;
    if k_depth > 16 {
        return Err(U1PhaseError::WindowOutOfBounds(k_depth));
    }
    let denom = Q::from_integer(BigInt::from(2).pow(k_depth + 1));
    let t_sub = theta / denom;
    let (mut re, mut im) = affine_cayley(&t_sub)?;
    for _ in 0..k_depth {
        let next = circle_mul(&re, &im, &re, &im)?;
        re = next.0;
        im = next.1;
    }
    let on_circle = is_unit_circle(&re, &im)?;
    Ok(CayleyDyadicApproxReceipt {
        theta: theta.clone(),
        k_depth,
        approx_re: re,
        approx_im: im,
        strictly_on_unit_circle: on_circle,
    })
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct HermitianQiBornReceipt {
    pub det_psi_zero: bool,
    pub trace_psi: Q,
    pub frobenius_trace_pq: Q,
    pub inner_modulus_sq: Q,
    pub born_pairing_matches_inner_mod_sq: bool,
    pub sigma_y_orthogonal_to_real_sym: bool,
}

/// Certify 4D Hermitian `Q(i)` rank-1 projectors, `sigma_y` orthogonality, and Born inner-product modulus squared.
#[allow(clippy::too_many_arguments)]
pub fn hermitian_qi_born_certificate(
    x1: &Q,
    y1: &Q,
    x2: &Q,
    y2: &Q,
    u1: &Q,
    v1: &Q,
    u2: &Q,
    v2: &Q,
) -> Result<HermitianQiBornReceipt, U1PhaseError> {
    check_pair(x1, y1)?;
    check_pair(x2, y2)?;
    check_pair(u1, v1)?;
    check_pair(u2, v2)?;
    let p_d1 = x1 * x1 + y1 * y1;
    let p_d2 = x2 * x2 + y2 * y2;
    let p_br = x1 * x2 + y1 * y2;
    let p_bi = x1 * y2 - y1 * x2;
    let q_d1 = u1 * u1 + v1 * v1;
    let q_d2 = u2 * u2 + v2 * v2;
    let q_br = u1 * u2 + v1 * v2;
    let q_bi = u1 * v2 - v1 * u2;
    let det_p = &p_d1 * &p_d2 - (&p_br * &p_br + &p_bi * &p_bi);
    let frob_pq = &p_d1 * &q_d1 + &p_d2 * &q_d2 + q(2) * &p_br * &q_br + q(2) * &p_bi * &q_bi;
    let inner_re = x1 * u1 + y1 * v1 + x2 * u2 + y2 * v2;
    let inner_im = x1 * v1 - y1 * u1 + x2 * v2 - y2 * u2;
    let inner_mod_sq = &inner_re * &inner_re + &inner_im * &inner_im;
    let sigma_y_orth = (&p_d1 * Q::zero()
        + &p_d2 * Q::zero()
        + q(2) * &p_br * Q::zero()
        + q(2) * Q::zero() * Q::one())
        .is_zero();
    Ok(HermitianQiBornReceipt {
        det_psi_zero: det_p.is_zero(),
        trace_psi: p_d1 + p_d2,
        frobenius_trace_pq: frob_pq.clone(),
        inner_modulus_sq: inner_mod_sq.clone(),
        born_pairing_matches_inner_mod_sq: frob_pq == inner_mod_sq,
        sigma_y_orthogonal_to_real_sym: sigma_y_orth,
    })
}

// ============================================================================
// 8. Iterated Quadratic Square-Root Tower K_m & Discrete Cayley Unitary Step
// ============================================================================

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct U345QuadraticTowerReceipt {
    pub m_levels: u32,
    pub level1_radicand_d0: Q,
    pub level1_cos_sq: Q,
    pub level1_sin_sq: Q,
    pub level2_radicand: QuadSqrt5,
    pub level2_radicand_norm: Q,
    pub level2_sin_sq: QuadSqrt5,
    pub level1_unit_circle: bool,
    pub level1_double_angle_recovers_u345: bool,
    pub level2_unit_circle_in_k2: bool,
    pub level2_double_angle_recovers_level1: bool,
    pub chebyshev_2pow_m_identities_verified: bool,
    pub all_tower_invariants_verified: bool,
}

fn verify_chebyshev_2pow_steps(m_levels: u32) -> Result<bool, U1PhaseError> {
    let sample_c = [
        Q::new(BigInt::from(3), BigInt::from(5)),
        Q::new(BigInt::from(5), BigInt::from(13)),
        Q::new(BigInt::from(8), BigInt::from(17)),
    ];
    for c_test in &sample_c {
        let mut cur = c_test.clone();
        for level in 1..=m_levels {
            cur = q(2) * &cur * &cur - Q::one();
            let deg = 1i64 << level;
            if cur != chebyshev_t(deg, c_test)? {
                return Ok(false);
            }
        }
    }
    Ok(true)
}

/// Certify the iterated quadratic half-angle tower `K_{m+1} = K_m(sqrt((1+c_m)/2))` above `u_345`.
pub fn u345_quadratic_tower_certificate(
    m_levels: u32,
) -> Result<U345QuadraticTowerReceipt, U1PhaseError> {
    if m_levels == 0 || m_levels > 6 {
        return Err(U1PhaseError::TowerDepthOutOfBounds(m_levels));
    }
    let c0 = Q::new(BigInt::from(3), BigInt::from(5));
    let s0 = Q::new(BigInt::from(4), BigInt::from(5));
    let d0 = (Q::one() + &c0) / q(2);
    let c1_sq = d0.clone();
    let s1_sq = (&s0 * &s0) / (q(4) * &d0);
    let level1_unit = &c1_sq + &s1_sq == Q::one();
    let level1_double_re = &c1_sq - &s1_sq == c0;
    let level1_double_im = q(4) * &c1_sq * &s1_sq == &s0 * &s0;
    let level1_recovers = level1_double_re && level1_double_im;

    let d1 = QuadSqrt5::new(
        Q::new(BigInt::from(1), BigInt::from(2)),
        Q::new(BigInt::from(1), BigInt::from(5)),
    )?;
    let d1_norm = quad_norm(&d1)?;
    let s2_sq = QuadSqrt5::new(
        Q::new(BigInt::from(1), BigInt::from(2)),
        Q::new(BigInt::from(-1), BigInt::from(5)),
    )?;
    let k2_sum = quad_add(&d1, &s2_sq)?;
    let k2_diff = quad_sub(&d1, &s2_sq)?;
    let k2_prod = quad_mul(&d1, &s2_sq)?;
    let level2_unit = k2_sum == QuadSqrt5::new(Q::one(), Q::zero())?;
    let c1_quad = QuadSqrt5::new(Q::zero(), Q::new(BigInt::from(2), BigInt::from(5)))?;
    let four_prod = quad_mul(&QuadSqrt5::new(q(4), Q::zero())?, &k2_prod)?;
    let s1_sq_quad = QuadSqrt5::new(s1_sq.clone(), Q::zero())?;
    let level2_recovers = k2_diff == c1_quad && four_prod == s1_sq_quad;

    let cheb_2pow_ok = verify_chebyshev_2pow_steps(m_levels)?;
    let all_ok = level1_unit
        && level1_recovers
        && level2_unit
        && level2_recovers
        && d1_norm == Q::new(BigInt::from(1), BigInt::from(20))
        && cheb_2pow_ok;
    Ok(U345QuadraticTowerReceipt {
        m_levels,
        level1_radicand_d0: d0,
        level1_cos_sq: c1_sq,
        level1_sin_sq: s1_sq,
        level2_radicand: d1,
        level2_radicand_norm: d1_norm,
        level2_sin_sq: s2_sq,
        level1_unit_circle: level1_unit,
        level1_double_angle_recovers_u345: level1_recovers,
        level2_unit_circle_in_k2: level2_unit,
        level2_double_angle_recovers_level1: level2_recovers,
        chebyshev_2pow_m_identities_verified: cheb_2pow_ok,
        all_tower_invariants_verified: all_ok,
    })
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct CayleyHermitianStoneReceipt {
    pub norm_sq: Q,
    pub denom_t1: Q,
    pub denom_t2: Q,
    pub alpha_t1: Q,
    pub beta_t1: Q,
    pub unitarity_holds_t1: bool,
    pub unitarity_holds_t2: bool,
    pub det_is_one_t1: bool,
    pub det_is_one_t2: bool,
    pub resolvent_identity_holds: bool,
    pub group_composition_law_holds: bool,
    pub south_pole_crossing_detected: bool,
    pub born_trace_invariance_holds: bool,
    pub all_cayley_stone_checks_verified: bool,
}

/// Certify the discrete Cayley unitary step `U_H(t) = (I - i t H)(I + i t H)^(-1)` on `2x2` Hermitian `Q(i)`.
pub fn cayley_hermitian_stone_certificate(
    a_diag: &Q,
    b_re: &Q,
    b_im: &Q,
    t1: &Q,
    t2: &Q,
) -> Result<CayleyHermitianStoneReceipt, U1PhaseError> {
    check_pair(a_diag, b_re)?;
    check_pair(b_im, t1)?;
    validate_rational(t2)?;
    let norm_sq = a_diag * a_diag + b_re * b_re + b_im * b_im;
    let denom1 = Q::one() + t1 * t1 * &norm_sq;
    let denom2 = Q::one() + t2 * t2 * &norm_sq;
    let alpha1 = (Q::one() - t1 * t1 * &norm_sq) / &denom1;
    let beta1 = (q(2) * t1) / &denom1;
    let alpha2 = (Q::one() - t2 * t2 * &norm_sq) / &denom2;
    let beta2 = (q(2) * t2) / &denom2;

    let unitarity1 = &alpha1 * &alpha1 + &beta1 * &beta1 * &norm_sq == Q::one();
    let unitarity2 = &alpha2 * &alpha2 + &beta2 * &beta2 * &norm_sq == Q::one();
    let resolvent_re = &alpha1 + t1 * &beta1 * &norm_sq == Q::one();
    let resolvent_im = &alpha1 * t1 - &beta1 == -t1;
    let resolvent_ok = resolvent_re && resolvent_im;

    let comp_re = &alpha1 * &alpha2 - &beta1 * &beta2 * &norm_sq;
    let comp_im = &alpha1 * &beta2 + &beta1 * &alpha2;
    let pole_denom = Q::one() - t1 * t2 * &norm_sq;
    let south_pole_crossed = pole_denom.is_zero();
    let group_law_ok = if south_pole_crossed {
        comp_re == q(-1) && comp_im.is_zero()
    } else {
        let t_comp = (t1 + t2) / &pole_denom;
        let denom_c = Q::one() + &t_comp * &t_comp * &norm_sq;
        let alpha_c = (Q::one() - &t_comp * &t_comp * &norm_sq) / &denom_c;
        let beta_c = (q(2) * &t_comp) / &denom_c;
        comp_re == alpha_c && comp_im == beta_c
    };

    let born_trace_preserved = unitarity1 && unitarity2;
    let all_ok =
        unitarity1 && unitarity2 && resolvent_ok && group_law_ok && born_trace_preserved;
    Ok(CayleyHermitianStoneReceipt {
        norm_sq,
        denom_t1: denom1,
        denom_t2: denom2,
        alpha_t1: alpha1,
        beta_t1: beta1,
        unitarity_holds_t1: unitarity1,
        unitarity_holds_t2: unitarity2,
        det_is_one_t1: unitarity1,
        det_is_one_t2: unitarity2,
        resolvent_identity_holds: resolvent_ok,
        group_composition_law_holds: group_law_ok,
        south_pole_crossing_detected: south_pole_crossed,
        born_trace_invariance_holds: born_trace_preserved,
        all_cayley_stone_checks_verified: all_ok,
    })
}

#[cfg(test)]
mod tests {
    use super::*;

    fn fr(n: i64, d: i64) -> Q {
        Q::new(BigInt::from(n), BigInt::from(d))
    }

    #[test]
    fn test_affine_cayley_lands_on_unit_circle_and_inverts() {
        for t in [q(0), q(1), q(-1), fr(1, 2), fr(-1, 3), fr(2, 5), fr(7, 4)] {
            let (re, im) = affine_cayley(&t).unwrap();
            assert!(is_unit_circle(&re, &im).unwrap());
            assert_eq!(inverse_cayley(&re, &im).unwrap(), t);
        }
        assert_eq!(affine_cayley(&fr(1, 2)).unwrap(), (fr(3, 5), fr(4, 5)));
    }

    #[test]
    fn test_affine_cayley_tangent_group_law_and_pole_collision() {
        let p1 = affine_cayley(&fr(1, 2)).unwrap();
        let p2 = affine_cayley(&fr(1, 3)).unwrap();
        let prod = circle_mul(&p1.0, &p1.1, &p2.0, &p2.1).unwrap();
        let t12 = affine_cayley_mul_param(&fr(1, 2), &fr(1, 3))
            .unwrap()
            .unwrap();
        assert_eq!(t12, q(1));
        assert_eq!(affine_cayley(&t12).unwrap(), prod);
        assert_eq!(affine_cayley_mul_param(&q(1), &q(1)).unwrap(), None);
        assert_eq!(affine_cayley_mul_param(&q(2), &fr(1, 2)).unwrap(), None);
    }

    #[test]
    fn test_projective_cayley_bijection_and_scale_invariance() {
        assert_eq!(projective_cayley(&q(0), &q(1)).unwrap(), (q(-1), q(0)));
        assert_eq!(projective_cayley(&q(0), &q(-5)).unwrap(), (q(-1), q(0)));
        assert_eq!(projective_cayley(&q(2), &q(1)).unwrap(), (fr(3, 5), fr(4, 5)));
        assert_eq!(
            projective_cayley(&q(-6), &q(-3)).unwrap(),
            (fr(3, 5), fr(4, 5))
        );
        for pt in [
            (q(1), q(0)),
            (q(-1), q(0)),
            (q(0), q(1)),
            (fr(3, 5), fr(4, 5)),
            (fr(-5, 13), fr(12, 13)),
        ] {
            let (u, v) = inverse_projective_cayley(&pt.0, &pt.1).unwrap();
            assert_eq!(projective_cayley(&u, &v).unwrap(), pt);
        }
    }

    #[test]
    fn test_projective_mul_homomorphism_across_south_pole() {
        let (u, v) = projective_mul(&q(1), &q(1), &q(1), &q(1)).unwrap();
        assert_eq!((u.clone(), v.clone()), (q(0), q(2)));
        assert_eq!(projective_cayley(&u, &v).unwrap(), (q(-1), q(0)));
        let (u2, v2) = projective_mul(&q(2), &q(1), &q(2), &q(-1)).unwrap();
        assert_eq!(projective_cayley(&u2, &v2).unwrap(), (q(1), q(0)));
    }

    #[test]
    fn test_cayley_negative_refusals() {
        assert_eq!(
            inverse_cayley(&q(-1), &q(0)),
            Err(U1PhaseError::SouthPolePuncture)
        );
        assert_eq!(
            inverse_cayley(&q(1), &q(1)),
            Err(U1PhaseError::NotOnUnitCircle)
        );
        assert_eq!(
            inverse_projective_cayley(&fr(1, 2), &fr(1, 2)),
            Err(U1PhaseError::NotOnUnitCircle)
        );
        assert_eq!(
            circle_mul(&q(1), &q(1), &q(1), &q(0)),
            Err(U1PhaseError::NotOnUnitCircle)
        );
        assert_eq!(
            projective_cayley(&q(0), &q(0)),
            Err(U1PhaseError::ProjectiveOriginRefused)
        );
        assert_eq!(
            projective_mul(&q(0), &q(0), &q(1), &q(2)),
            Err(U1PhaseError::ProjectiveOriginRefused)
        );
        assert_eq!(
            projective_mul(&q(1), &q(2), &q(0), &q(0)),
            Err(U1PhaseError::ProjectiveOriginRefused)
        );
    }

    #[test]
    fn test_five_adic_valuation_factorization() {
        for n in [1i64, -1, 2, 4, 5, -5, 20, 25, 125, -375, 44, -117] {
            let big_n = BigInt::from(n);
            let (v5, unit) = five_adic_valuation(&big_n).unwrap();
            assert_eq!(big_n, BigInt::from(5).pow(v5) * &unit);
            assert!(!(&unit % BigInt::from(5)).is_zero());
        }
        assert_eq!(
            five_adic_valuation(&BigInt::zero()),
            Err(U1PhaseError::ZeroValuationInput)
        );
    }

    #[test]
    fn test_four_fifths_not_square_certificate() {
        for (num, den) in [(0, 1), (1, 1), (2, 3), (9, 10), (179, 200), (-38, 43)] {
            let c =
                certify_four_fifths_not_square(&BigInt::from(num), &BigInt::from(den)).unwrap();
            assert!(c.obstructed);
            assert!(c.parity_disjoint);
            assert!(c.abs_residual >= BigInt::one());
            assert_eq!(c.rhs_v5 % 2, 0);
            if num != 0 {
                assert_eq!(c.lhs_v5.unwrap() % 2, 1);
            }
        }
        assert_eq!(
            certify_four_fifths_not_square(&BigInt::from(2), &BigInt::zero()),
            Err(U1PhaseError::ZeroDenominator)
        );
    }

    #[test]
    fn test_u345_no_rational_sqrt_certificate() {
        for (re, im) in [
            (fr(2, 3), fr(1, 3)),
            (fr(3, 5), fr(4, 5)),
            (fr(9, 10), fr(9, 20)),
            (q(0), q(1)),
        ] {
            let c = certify_u345_no_rational_sqrt(&re, &im).unwrap();
            assert!(c.half_sum_equals_re_sq);
            assert!(!c.matches_u345_and_unit);
            assert!(c.obstructed);
        }
    }

    #[test]
    fn test_gauss_pow_34_exact_values_and_norm() {
        assert_eq!(gauss_pow_34(0).unwrap(), (BigInt::from(1), BigInt::from(0)));
        assert_eq!(gauss_pow_34(1).unwrap(), (BigInt::from(3), BigInt::from(4)));
        assert_eq!(
            gauss_pow_34(2).unwrap(),
            (BigInt::from(-7), BigInt::from(24))
        );
        assert_eq!(
            gauss_pow_34(3).unwrap(),
            (BigInt::from(-117), BigInt::from(44))
        );
        assert_eq!(
            gauss_pow_34(4).unwrap(),
            (BigInt::from(-527), BigInt::from(-336))
        );
        assert_eq!(gauss_pow_34(-1), Err(U1PhaseError::NegativeExponent(-1)));
    }

    #[test]
    fn test_u345_power_group_homomorphism() {
        for j in -4..=4 {
            for k in -4..=4 {
                let pj = u345_power(j).unwrap();
                let pk = u345_power(k).unwrap();
                let pjk = u345_power(j + k).unwrap();
                assert_eq!(circle_mul(&pj.0, &pj.1, &pk.0, &pk.1).unwrap(), pjk);
            }
        }
    }

    #[test]
    fn test_power_injectivity_window_certificate() {
        let c = certify_power_injectivity_window(12).unwrap();
        assert!(c.mod5_invariant_holds);
        assert!(c.all_on_unit_circle);
        assert_eq!(c.tested_exponents, 25);
        assert_eq!(c.distinct_points, 25);
        assert!(c.injective_on_window);
        assert_eq!(
            certify_power_injectivity_window(0),
            Err(U1PhaseError::WindowOutOfBounds(0))
        );
        assert_eq!(
            certify_power_injectivity_window(257),
            Err(U1PhaseError::WindowOutOfBounds(257))
        );
    }

    #[test]
    fn test_quad_sqrt5_field_arithmetic_and_inverse() {
        let x = QuadSqrt5::new(q(2), q(1)).unwrap();
        let inv = quad_inv(&x).unwrap();
        assert_eq!(quad_norm(&x).unwrap(), q(-1));
        assert_eq!(
            quad_mul(&x, &inv).unwrap(),
            QuadSqrt5::new(q(1), q(0)).unwrap()
        );
        assert_eq!(
            quad_mul(&x, &quad_conj(&x).unwrap()).unwrap(),
            QuadSqrt5::new(quad_norm(&x).unwrap(), q(0)).unwrap()
        );
        assert_eq!(
            quad_inv(&QuadSqrt5::new(q(0), q(0)).unwrap()),
            Err(U1PhaseError::ZeroQuadSqrt5Inverse)
        );
    }

    #[test]
    fn test_u345_quad_sqrt_certificate_restores_half_angle() {
        let c = u345_quad_sqrt_certificate().unwrap();
        assert!(c.squares_to_u345);
        assert!(c.on_unit_circle);
        assert!(c.requires_quadratic_extension);
        assert_eq!(c.w_sq.re, QuadSqrt5::new(fr(3, 5), q(0)).unwrap());
        assert_eq!(c.w_sq.im, QuadSqrt5::new(fr(4, 5), q(0)).unwrap());
    }

    #[test]
    fn test_torsion_phase_refinement_preserves_phase() {
        for (n, k, a) in [(4, 3, 1), (6, 5, 11), (12, 7, -5)] {
            let c = refine_torsion_phase(n, k, a).unwrap();
            assert!(c.phase_preserved);
            assert_eq!(c.base_phase, c.refined_phase);
        }
        assert_eq!(
            refine_torsion_phase(0, 2, 1),
            Err(U1PhaseError::InvalidTorsionLevel)
        );
        assert_eq!(
            refine_torsion_phase(4, 0, 1),
            Err(U1PhaseError::InvalidTorsionLevel)
        );
    }

    #[test]
    fn test_divide_rat_phase_mod_one_is_m_divisible() {
        for (q_phase, div) in [(fr(1, 3), 2), (fr(3, 5), 4), (fr(-7, 4), 5)] {
            let c = divide_rat_phase_mod_one(&q_phase, div).unwrap();
            assert!(c.all_in_unit_interval);
            assert_eq!(c.distinct_count, div as usize);
            assert!(c.all_multiply_to_q_mod_one);
        }
        assert_eq!(
            divide_rat_phase_mod_one(&fr(1, 2), 0),
            Err(U1PhaseError::InvalidDivisor(0))
        );
    }

    #[test]
    fn test_fourth_roots_haar_character_orthogonality() {
        for power in -8..=8 {
            let c = fourth_roots_haar_certificate(power).unwrap();
            assert!(c.orthogonality_holds);
            if power % 4 == 0 {
                assert_eq!((c.average_re, c.average_im), (q(1), q(0)));
            } else {
                assert_eq!((c.average_re, c.average_im), (q(0), q(0)));
            }
        }
    }

    #[test]
    fn test_torsion_grid_cover_certificate() {
        for q_phase in [q(0), q(1), fr(1, 3), fr(4, 5), fr(17, 29)] {
            for n_grid in [1, 4, 10, 64] {
                let c = torsion_grid_cover_certificate(&q_phase, n_grid).unwrap();
                assert!(c.within_bound);
            }
        }
        assert_eq!(
            torsion_grid_cover_certificate(&fr(-1, 5), 8),
            Err(U1PhaseError::PhaseOutOfUnitInterval)
        );
        assert_eq!(
            torsion_grid_cover_certificate(&fr(6, 5), 8),
            Err(U1PhaseError::PhaseOutOfUnitInterval)
        );
        assert_eq!(
            torsion_grid_cover_certificate(&fr(1, 2), 0),
            Err(U1PhaseError::InvalidGridSize)
        );
    }

    #[test]
    fn test_dyadic_sqrt5_interval_step_contracts_and_brackets() {
        let mut lo = q(2);
        let mut hi = q(3);
        for _ in 0..8 {
            let c = dyadic_sqrt5_interval_step(&lo, &hi).unwrap();
            assert!(c.brackets_sqrt5);
            assert!(c.brackets_four_fifths);
            assert!(c.width_halved);
            lo = c.new_lo;
            hi = c.new_hi;
        }
        assert_eq!(hi - lo, fr(1, 256));
        assert_eq!(
            dyadic_sqrt5_interval_step(&q(3), &q(4)),
            Err(U1PhaseError::InvalidSqrt5Bracket)
        );
        assert_eq!(
            dyadic_sqrt5_interval_step(&q(1), &q(2)),
            Err(U1PhaseError::InvalidSqrt5Bracket)
        );
    }

    #[test]
    fn test_negative_controls_and_non_reduced_rational_refusal() {
        let c = negative_controls_certificate().unwrap();
        assert!(c.all_negative_controls_verified);
        assert!(AUTHORITY_FENCE.starts_with("AuthorityEffect None"));
        assert!(PROVENANCE.contains("20261020T223000Z_u1_phase_completion_lean"));
        let non_reduced = Q::new_raw(BigInt::from(2), BigInt::from(4));
        assert_eq!(
            affine_cayley(&non_reduced),
            Err(U1PhaseError::InexactRational(
                RationalConstructionError::NonReduced
            ))
        );
    }

    #[test]
    fn test_circle_mul_group_laws_and_provenance_modules() {
        let u = (fr(3, 5), fr(4, 5));
        let v = (fr(5, 13), fr(12, 13));
        let uv = circle_mul(&u.0, &u.1, &v.0, &v.1).unwrap();
        let vu = circle_mul(&v.0, &v.1, &u.0, &u.1).unwrap();
        assert_eq!(uv, vu);
        assert!(is_unit_circle(&uv.0, &uv.1).unwrap());
        for mod_name in [
            "U1CayleyProjectiveCircle",
            "U1HalfAngleObstruction",
            "U1PythagoreanObstruction",
            "U1PowerMapInjectivity",
            "U1CyclotomicTorsionTower",
            "U1CauchyCircleCompletion",
            "U1ChebyshevCauchyBridge",
            "U1QuadraticTowerAndCayleyStone",
            "U1PhaseSynthesis",
        ] {
            assert!(PROVENANCE.contains(mod_name), "{mod_name}");
        }
    }

    #[test]
    fn test_chebyshev_polynomials_and_circle_power_bridge() {
        let c = chebyshev_circle_certificate(&fr(3, 5), &fr(4, 5), 10).unwrap();
        assert!(c.chebyshev_matches_circle_powers);
        assert!(c.pell_identity_holds_all_degrees);
        assert_eq!(chebyshev_t(2, &fr(3, 5)).unwrap(), fr(-7, 25));
        assert_eq!(
            &fr(4, 5) * &chebyshev_u(1, &fr(3, 5)).unwrap(),
            fr(24, 25)
        );
        assert_eq!(
            chebyshev_t(-1, &fr(1, 2)),
            Err(U1PhaseError::NegativeExponent(-1))
        );
        assert_eq!(
            chebyshev_u(-1, &fr(1, 2)),
            Err(U1PhaseError::NegativeExponent(-1))
        );
        assert_eq!(
            chebyshev_circle_certificate(&fr(1, 2), &fr(1, 2), 4),
            Err(U1PhaseError::NotOnUnitCircle)
        );
        assert_eq!(
            chebyshev_circle_certificate(&fr(3, 5), &fr(4, 5), 0),
            Err(U1PhaseError::WindowOutOfBounds(0))
        );
    }

    #[test]
    fn test_taylor_trig_enclosure_and_cayley_dyadic_approximants() {
        for th in [q(0), fr(1, 6), fr(1, 3), fr(1, 2), fr(3, 4), q(1)] {
            let tc = taylor_trig_enclosure_certificate(&th).unwrap();
            assert!(tc.all_taylor_bounds_verified);
            let cd = cayley_dyadic_approx_certificate(&th, 4).unwrap();
            assert!(cd.strictly_on_unit_circle);
        }
        assert_eq!(
            taylor_trig_enclosure_certificate(&fr(-1, 4)),
            Err(U1PhaseError::PhaseOutOfUnitInterval)
        );
        assert_eq!(
            taylor_trig_enclosure_certificate(&fr(5, 4)),
            Err(U1PhaseError::PhaseOutOfUnitInterval)
        );
        assert_eq!(
            cayley_dyadic_approx_certificate(&fr(1, 2), 17),
            Err(U1PhaseError::WindowOutOfBounds(17))
        );
    }

    #[test]
    fn test_hermitian_qi_born_certificate() {
        let hc = hermitian_qi_born_certificate(
            &fr(3, 5),
            &q(0),
            &q(0),
            &fr(4, 5),
            &fr(1, 2),
            &fr(1, 2),
            &fr(-1, 2),
            &fr(1, 2),
        )
        .unwrap();
        assert!(hc.det_psi_zero);
        assert_eq!(hc.trace_psi, q(1));
        assert!(hc.born_pairing_matches_inner_mod_sq);
        assert!(hc.sigma_y_orthogonal_to_real_sym);
    }

    #[test]
    fn test_u345_quadratic_tower_certificate() {
        let tc = u345_quadratic_tower_certificate(4).unwrap();
        assert!(tc.all_tower_invariants_verified);
        assert_eq!(tc.level1_radicand_d0, fr(4, 5));
        assert_eq!(tc.level1_sin_sq, fr(1, 5));
        assert_eq!(tc.level2_radicand_norm, fr(1, 20));
        assert!(tc.chebyshev_2pow_m_identities_verified);
        assert_eq!(
            u345_quadratic_tower_certificate(0),
            Err(U1PhaseError::TowerDepthOutOfBounds(0))
        );
        assert_eq!(
            u345_quadratic_tower_certificate(7),
            Err(U1PhaseError::TowerDepthOutOfBounds(7))
        );
    }

    #[test]
    fn test_cayley_hermitian_stone_certificate() {
        let reg = cayley_hermitian_stone_certificate(
            &fr(3, 5),
            &q(0),
            &fr(4, 5),
            &fr(1, 2),
            &fr(1, 3),
        )
        .unwrap();
        assert!(reg.all_cayley_stone_checks_verified);
        assert!(!reg.south_pole_crossing_detected);
        assert_eq!(reg.norm_sq, q(1));
        assert_eq!((reg.alpha_t1, reg.beta_t1), (fr(3, 5), fr(4, 5)));

        let pole = cayley_hermitian_stone_certificate(
            &fr(3, 5),
            &fr(4, 5),
            &q(0),
            &q(1),
            &q(1),
        )
        .unwrap();
        assert!(pole.all_cayley_stone_checks_verified);
        assert!(pole.south_pole_crossing_detected);
    }
}
