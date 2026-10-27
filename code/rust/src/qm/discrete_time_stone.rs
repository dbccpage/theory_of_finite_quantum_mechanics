//! Discrete time on the finite carrier: the ℤ-action `k ↦ Uᵏ` of one rational rotation step,
//! and the exact obstruction to a ℚ-parameter group through it.
//!
//! Replays in exact rational arithmetic the Lean specification
//! `dag/results/FQ-GAP-STONE-CONTINUOUS-TIME/runs/20261020T225000Z_discrete_time_spec/DiscreteTimeStoneSpec.lean`
//! (namespace `BornFinite.DiscreteTime`) for node FQ-GAP-STONE-CONTINUOUS-TIME and mirrors,
//! function for function, the Python twin `code/python/src/qm/discrete_time_stone.py`.
//! Specified there: the ℚ-parameter group `QParamGroup` (`U 0 = 1`, `U (s + t) = U s * U t`),
//! the discrete evolution `discreteEvolution u k = u ^ k` with `discreteEvolution_add`,
//! `discreteEvolution_zero`, `discreteEvolution_neg`, its restriction `U_int` /
//! `U_eq_discreteEvolution`, the necessity `U_inv_nat` / `roots_of_all_orders`
//! (`U (1/m) ^ m = U 1`), and generator non-uniqueness `sq_root_neg`, `neg_ne_self_of_ne_zero`,
//! `half_step_not_unique`, `matrix_half_step_not_unique`. Derived there: `R345_orthogonal`,
//! `R345_det`, `R345_pow_orthogonal`, `four_fifths_not_rat_square` (via `four_fifths_den` and
//! `nat_mul_self_ne_five`), `no_rational_half_step` and `no_qparam_group_through_R345`.
//! This module replays those statements exactly:
//!
//! * rational rotations `[[c, −s], [s, c]]` with `c² + s² = 1` and their exact ℤ-orbit `Uᵏ`,
//!   `−kmax ≤ k ≤ kmax` (negative powers by transpose), with `(Uᵏ)ᵀ Uᵏ = I`, the group law on
//!   the window and `U⁻ᵏ = (Uᵏ)ᵀ` replayed;
//! * the half-angle criterion: a rational rotation has a rational rotation square root iff
//!   `(1 + c)/2` is a rational square `p²`, and then exactly the pair `±rotation(p, s/(2p))`;
//! * the necessary roots of a ℚ-parameter group `U` with `U(1) = R`: `U(1/m)ᵐ = R`, decided for
//!   `m = 2ʲ` by iterating the half-step on every branch;
//! * the commutant form of any square root of a `2 × 2` matrix with irreducible characteristic
//!   polynomial: `V = pI + rJ` with `J = R − (tr R/2)·I`, and `V² = R ⇔ p² + κr² = tr R/2 ∧
//!   2pr = 1 ⇔ p² = (tr R/2 ± √det R)/2`; for the Pythagorean step `R345 = rotation(3/5, 4/5)`
//!   the required square is `4/5`, not a rational square, although `R345²` has the half-steps
//!   `±R345`;
//! * the sign pair of every square root (`(−V)² = V²` and `−V ≠ V` for `V ≠ 0`): no canonical
//!   generator;
//! * the order of a rotation on a finite window: `rotation(0, 1)` has order 4 while `R345`
//!   never returns, consistent with the kernel-checked
//!   `fq_gap_stone_rational_rotation_infinite_order_and_zi_non_field_obstruction`
//!   (`lean4/DerivationDagQMClosure.lean`) and the scalar
//!   `U1PowerMapInjectivity.u345_infinite_order` cited by the specification.
//!
//! Continuous time and generator selection are not derived: a ℚ-parameter group with
//! `U(1) = R345` would need `U(1/2)`, a rational half-step, which does not exist. The general
//! triviality of ℚ-parameter groups over ℚ(i) is the open obligation recorded by the
//! specification (unique factorisation in ℤ[i]). AuthorityEffect: None.

use num_bigint::BigInt;
use num_traits::{One, Zero};

use crate::linear_algebra::scalars::{validate_rational, RationalConstructionError};
use crate::linear_algebra::{q, Q};
use crate::number_theory::rational::sqrt_exact;

pub const AUTHORITY_FENCE: &str = "AuthorityEffect None; not PROVED; no continuous-time group and no \
     generator is derived on the finite carrier; the Z-action of one rational step is supplied and \
     the absence of a rational half-step of R345 is decided exactly; assumptions exposed.";

pub const PROVENANCE: &str = "Replays the Lean specification \
     dag/results/FQ-GAP-STONE-CONTINUOUS-TIME/runs/20261020T225000Z_discrete_time_spec/DiscreteTimeStoneSpec.lean \
     (node FQ-GAP-STONE-CONTINUOUS-TIME, namespace BornFinite.DiscreteTime: QParamGroup, \
     discreteEvolution, U_int, U_eq_discreteEvolution, U_inv_nat, roots_of_all_orders, sq_root_neg, \
     neg_ne_self_of_ne_zero, half_step_not_unique, matrix_half_step_not_unique, R345_orthogonal, \
     R345_det, R345_pow_orthogonal, four_fifths_not_rat_square, no_rational_half_step, \
     no_qparam_group_through_R345), the kernel-checked \
     fq_gap_stone_rational_rotation_infinite_order_and_zi_non_field_obstruction of \
     lean4/DerivationDagQMClosure.lean, and the Python twin \
     code/python/src/qm/discrete_time_stone.py.";

/// A rational matrix as rows; every public entry point re-admits it through [`matrix2`].
pub type Matrix = Vec<Vec<Q>>;

#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum DiscreteTimeStoneError {
    #[error("exact canonical rational entries required: {0}")]
    InexactEntry(#[from] RationalConstructionError),
    #[error("2x2 rational matrix required")]
    NotTwoByTwo,
    #[error("rational point of the unit circle required: c^2 + s^2 = {norm}")]
    NotOnCircle { norm: Q },
    #[error("rational rotation [[c, -s], [s, c]] with c^2 + s^2 = 1 required")]
    NotARotation,
    #[error("negative powers need an orthogonal matrix")]
    NotOrthogonal,
    #[error("power-of-two root order required, got {0}")]
    NotAPowerOfTwo(u64),
    #[error("positive bound required")]
    NonPositiveBound,
    #[error("irreducible characteristic polynomial required")]
    ReducibleCharacteristicPolynomial,
}

type Error = DiscreteTimeStoneError;

/// `n/d` for a nonzero literal denominator.
fn fr(n: i64, d: i64) -> Q {
    Q::new(BigInt::from(n), BigInt::from(d))
}

fn half(x: Q) -> Q {
    x / q(2)
}

// ============================================================================
// Exact-input admission and the 2 × 2 matrix algebra (supplied, not derived)
// ============================================================================

/// Admit a `2 × 2` matrix of canonical rationals.
pub fn matrix2(rows: &[Vec<Q>]) -> Result<Matrix, Error> {
    if rows.len() != 2 || rows.iter().any(|r| r.len() != 2) {
        return Err(Error::NotTwoByTwo);
    }
    for x in rows.iter().flatten() {
        validate_rational(x)?;
    }
    Ok(rows.to_vec())
}

pub fn identity() -> Matrix {
    vec![vec![Q::one(), Q::zero()], vec![Q::zero(), Q::one()]]
}

pub fn zero() -> Matrix {
    vec![vec![Q::zero(), Q::zero()], vec![Q::zero(), Q::zero()]]
}

pub fn mul(a: &[Vec<Q>], b: &[Vec<Q>]) -> Result<Matrix, Error> {
    let (a, b) = (matrix2(a)?, matrix2(b)?);
    Ok((0..2)
        .map(|i| {
            (0..2)
                .map(|j| &a[i][0] * &b[0][j] + &a[i][1] * &b[1][j])
                .collect()
        })
        .collect())
}

pub fn transpose(a: &[Vec<Q>]) -> Result<Matrix, Error> {
    let a = matrix2(a)?;
    Ok(vec![
        vec![a[0][0].clone(), a[1][0].clone()],
        vec![a[0][1].clone(), a[1][1].clone()],
    ])
}

pub fn neg(a: &[Vec<Q>]) -> Result<Matrix, Error> {
    Ok(matrix2(a)?
        .iter()
        .map(|r| r.iter().map(|x| -x).collect())
        .collect())
}

pub fn trace(a: &[Vec<Q>]) -> Result<Q, Error> {
    let a = matrix2(a)?;
    Ok(&a[0][0] + &a[1][1])
}

pub fn det(a: &[Vec<Q>]) -> Result<Q, Error> {
    let a = matrix2(a)?;
    Ok(&a[0][0] * &a[1][1] - &a[0][1] * &a[1][0])
}

/// `Aᵀ A = I`.
pub fn is_orthogonal(a: &[Vec<Q>]) -> Result<bool, Error> {
    Ok(mul(&transpose(a)?, a)? == identity())
}

/// `[[c, −s], [s, c]]` for a rational point `(c, s)` of the unit circle; any other `(c, s)` is
/// refused.
pub fn rotation(c: &Q, s: &Q) -> Result<Matrix, Error> {
    validate_rational(c)?;
    validate_rational(s)?;
    let norm = c * c + s * s;
    if !norm.is_one() {
        return Err(Error::NotOnCircle { norm });
    }
    Ok(vec![vec![c.clone(), -s], vec![s.clone(), c.clone()]])
}

/// `(c, s)` with `R == rotation(c, s)`; refuses every other matrix.
pub fn rotation_point(r: &[Vec<Q>]) -> Result<(Q, Q), Error> {
    let r = matrix2(r)?;
    let (c, s) = (r[0][0].clone(), r[1][0].clone());
    if r[0][1] != -&s || r[1][1] != c || &c * &c + &s * &s != Q::one() {
        return Err(Error::NotARotation);
    }
    Ok((c, s))
}

/// The Pythagorean step `rotation(3/5, 4/5)`.
pub fn r345() -> Matrix {
    vec![vec![fr(3, 5), fr(-4, 5)], vec![fr(4, 5), fr(3, 5)]]
}

/// `Rᵏ` for an integer `k`; `R⁻¹ = Rᵀ`, so a negative `k` needs an orthogonal `R` (refused
/// otherwise). Lean: `discreteEvolution`, `discreteEvolution_neg`.
pub fn zpow(r: &[Vec<Q>], k: i64) -> Result<Matrix, Error> {
    let mut base = matrix2(r)?;
    if k < 0 {
        if !is_orthogonal(&base)? {
            return Err(Error::NotOrthogonal);
        }
        base = transpose(&base)?;
    }
    let mut e = k.unsigned_abs();
    let mut p = identity();
    while e > 0 {
        if e & 1 == 1 {
            p = mul(&p, &base)?;
        }
        base = mul(&base, &base)?;
        e >>= 1;
    }
    Ok(p)
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DiscreteEvolution {
    pub kmax: u32,
    pub exponents: Vec<i64>,
    /// `Uᵏ` in the order of `exponents`.
    pub orbit: Vec<Matrix>,
    pub all_orthogonal: bool,
    pub group_law: bool,
    pub inverse_is_transpose: bool,
}

/// The exact ℤ-orbit `Uᵏ`, `−kmax ≤ k ≤ kmax`, of one orthogonal step `U = R`: every power is
/// orthogonal, `Uⁱ Uʲ = Uⁱ⁺ʲ` on the window, and `U⁻ᵏ = (Uᵏ)ᵀ`. Lean: `discreteEvolution_add`,
/// `discreteEvolution_zero`, `discreteEvolution_neg`, `R345_pow_orthogonal`.
pub fn discrete_evolution(r: &[Vec<Q>], kmax: u32) -> Result<DiscreteEvolution, Error> {
    let r = matrix2(r)?;
    if !is_orthogonal(&r)? {
        return Err(Error::NotOrthogonal);
    }
    let k = i64::from(kmax);
    let exponents: Vec<i64> = (-k..=k).collect();
    let orbit = exponents
        .iter()
        .map(|&e| zpow(&r, e))
        .collect::<Result<Vec<Matrix>, Error>>()?;
    let (n, offset) = (orbit.len(), kmax as usize);
    let mut all_orthogonal = true;
    for u in &orbit {
        if !is_orthogonal(u)? {
            all_orthogonal = false;
            break;
        }
    }
    let mut group_law = true;
    'pairs: for i in 0..n {
        for j in 0..n {
            // index of exponent (i − kmax) + (j − kmax) is i + j − kmax when it lies in the window
            if i + j >= offset && i + j - offset < n && mul(&orbit[i], &orbit[j])? != orbit[i + j - offset]
            {
                group_law = false;
                break 'pairs;
            }
        }
    }
    let mut inverse_is_transpose = true;
    for i in 0..n {
        if orbit[n - 1 - i] != transpose(&orbit[i])? {
            inverse_is_transpose = false;
            break;
        }
    }
    Ok(DiscreteEvolution {
        kmax,
        exponents,
        orbit,
        all_orthogonal,
        group_law,
        inverse_is_transpose,
    })
}

// ============================================================================
// Rational squares and the half-angle criterion
// ============================================================================

/// The nonnegative rational `r` with `r² = x`, or `None` (negative `x` included); decided
/// exactly on the reduced numerator and denominator by the crate's `sqrt_exact`. Lean:
/// `four_fifths_not_rat_square` via `four_fifths_den` and `nat_mul_self_ne_five`.
pub fn rational_sqrt(x: &Q) -> Result<Option<Q>, Error> {
    validate_rational(x)?;
    Ok(sqrt_exact(x))
}

pub fn is_rational_square(x: &Q) -> Result<bool, Error> {
    Ok(rational_sqrt(x)?.is_some())
}

/// The rational rotations `V` with `V² = rotation(c, s)`: `None` unless `(1 + c)/2` is a
/// rational square `p²`, and then exactly the pair `±rotation(p, s/(2p))` (with `s/(2p)` read
/// as `1` when `p = 0`: `rotation(−1, 0) = rotation(0, ±1)²`). Lean: `no_rational_half_step`
/// for `R345`.
pub fn half_step(c: &Q, s: &Q) -> Result<Option<[Matrix; 2]>, Error> {
    let (c, s) = rotation_point(&rotation(c, s)?)?;
    let Some(p) = rational_sqrt(&half(Q::one() + c))? else {
        return Ok(None);
    };
    let r = if p.is_zero() {
        Q::one()
    } else {
        s / (q(2) * &p)
    };
    Ok(Some([rotation(&p, &r)?, rotation(&-&p, &-&r)?]))
}

pub fn has_rational_half_step(c: &Q, s: &Q) -> Result<bool, Error> {
    Ok(half_step(c, s)?.is_some())
}

/// The outcome of [`qparam_necessary_roots`].
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum RootChain {
    /// No rational square root exists at `depth` for the circle point `at`, whose half-angle
    /// square `(1 + c)/2 = required_square` is not a rational square.
    Obstructed {
        m: u64,
        depth: u32,
        at: (Q, Q),
        required_square: Q,
    },
    /// The `2^depth` rational `m`-th roots, as circle points.
    Roots {
        m: u64,
        depth: u32,
        roots: Vec<(Q, Q)>,
    },
}

/// A ℚ-parameter group `U` with `U(1) = R` restricts to `k ↦ Rᵏ` on ℤ and needs `U(1/m)` with
/// `U(1/m)ᵐ = R`. For a rational rotation `R` and `m = 2ʲ` this is decided exactly by iterating
/// [`half_step`] on every branch. Lean: `QParamGroup`, `U_eq_discreteEvolution`, `U_inv_nat`,
/// `roots_of_all_orders`.
pub fn qparam_necessary_roots(r: &[Vec<Q>], m: u64) -> Result<RootChain, Error> {
    let point = rotation_point(r)?;
    if !m.is_power_of_two() {
        return Err(Error::NotAPowerOfTwo(m));
    }
    let depth = m.trailing_zeros();
    let mut level = vec![point];
    for j in 1..=depth {
        let mut next = Vec::with_capacity(2 * level.len());
        for (a, b) in &level {
            match half_step(a, b)? {
                None => {
                    return Ok(RootChain::Obstructed {
                        m,
                        depth: j,
                        at: (a.clone(), b.clone()),
                        required_square: half(Q::one() + a),
                    })
                }
                Some(pair) => {
                    for v in &pair {
                        next.push(rotation_point(v)?);
                    }
                }
            }
        }
        level = next;
    }
    Ok(RootChain::Roots {
        m,
        depth,
        roots: level,
    })
}

// ============================================================================
// The commutant route, independent of the rotation structure
// ============================================================================

/// `x² − tr(R)·x + det(R)` is irreducible over ℚ iff `tr(R)² − 4·det(R)` is not a rational
/// square.
pub fn irreducible_char_poly(r: &[Vec<Q>]) -> Result<bool, Error> {
    let r = matrix2(r)?;
    let (t, d) = (trace(&r)?, det(&r)?);
    Ok(!is_rational_square(&(&t * &t - q(4) * d))?)
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct CommutantHalfStepCandidates {
    pub half_trace: Q,
    pub det: Q,
    /// `J² = κ·I`.
    pub kappa: Q,
    /// `J = R − (tr R/2)·I`.
    pub j: Matrix,
    /// `(tr R/2 ± √det R)/2`, descending; empty when `det R` is not a rational square.
    pub candidate_p_squares: Vec<Q>,
    /// Every rational `V` with `V V = R`, replayed.
    pub roots: Vec<Matrix>,
}

/// Every `V` with `V² = R` commutes with `R`; when the characteristic polynomial of `R` is
/// irreducible the commutant is `ℚ[R] = span{I, J}` with `J = R − (tr R/2)·I` and `J² = κ·I`,
/// `κ = (tr R)²/4 − det R`. For `V = pI + rJ`: `V² = R ⇔ p² + κr² = tr R/2 ∧ 2pr = 1 ⇔
/// p² = (tr R/2 ± √det R)/2 ∧ r = 1/(2p)`. For a rotation `p² = (1 + c)/2`, the half-angle
/// criterion, reached without using the rotation structure. Lean: the commutation step of
/// `no_rational_half_step` (`V * R345 = R345 * V` forces `V = !![p, -r; r, p]`).
pub fn commutant_half_step_candidates(
    r: &[Vec<Q>],
) -> Result<CommutantHalfStepCandidates, Error> {
    let r = matrix2(r)?;
    if !irreducible_char_poly(&r)? {
        return Err(Error::ReducibleCharacteristicPolynomial);
    }
    let t = half(trace(&r)?);
    let d = det(&r)?;
    let j: Matrix = (0..2)
        .map(|i| {
            (0..2)
                .map(|c| if i == c { &r[i][c] - &t } else { r[i][c].clone() })
                .collect()
        })
        .collect();
    let kappa = &t * &t - &d;
    let mut candidate_p_squares = Vec::new();
    if let Some(rd) = rational_sqrt(&d)? {
        candidate_p_squares.push(half(&t + &rd));
        let low = half(&t - &rd);
        if !candidate_p_squares.contains(&low) {
            candidate_p_squares.push(low);
        }
    }
    let mut roots = Vec::new();
    for ps in &candidate_p_squares {
        let Some(p) = rational_sqrt(ps)? else {
            continue;
        };
        if p.is_zero() {
            continue;
        }
        for pp in [p.clone(), -&p] {
            let rr = Q::one() / (q(2) * &pp);
            let v: Matrix = (0..2)
                .map(|i| {
                    (0..2)
                        .map(|c| {
                            let diagonal = if i == c { pp.clone() } else { Q::zero() };
                            diagonal + &rr * &j[i][c]
                        })
                        .collect()
                })
                .collect();
            if mul(&v, &v)? == r {
                roots.push(v);
            }
        }
    }
    Ok(CommutantHalfStepCandidates {
        half_trace: t,
        det: d,
        kappa,
        j,
        candidate_p_squares,
        roots,
    })
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct NoRationalHalfStepCertificate {
    /// `(1 + c)/2`, the value `p²` must take.
    pub required_square: Q,
    pub is_rational_square: bool,
}

/// For `R = rotation(c, s)`: `V = [[p, −r], [r, p]]` (the commutant form) squares to `R` iff
/// `p² − r² = c ∧ 2pr = s`, which forces `p² + r² = 1` and `p² = (1 + c)/2`; the required
/// square is reported with its exact decision. For `R345` it is `4/5`, not a rational square.
/// Lean: `no_rational_half_step`, `four_fifths_not_rat_square`.
pub fn no_rational_half_step_certificate(
    r: &[Vec<Q>],
) -> Result<NoRationalHalfStepCertificate, Error> {
    let (c, _) = rotation_point(r)?;
    let required_square = half(Q::one() + c);
    let square = is_rational_square(&required_square)?;
    Ok(NoRationalHalfStepCertificate {
        required_square,
        is_rational_square: square,
    })
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct SquareRootPair {
    pub u: Matrix,
    pub v: Matrix,
    pub neg_v: Matrix,
    pub neg_squares_to_u: bool,
    pub distinct: bool,
    pub v_nonzero: bool,
}

/// With `U = V V`: `(−V)(−V) = U` as well and `−V ≠ V` whenever `V ≠ 0`, so a square root of a
/// step is never unique. Lean: `sq_root_neg`, `neg_ne_self_of_ne_zero`, `half_step_not_unique`,
/// `matrix_half_step_not_unique`.
pub fn square_root_pairs(v: &[Vec<Q>]) -> Result<SquareRootPair, Error> {
    let v = matrix2(v)?;
    let u = mul(&v, &v)?;
    let neg_v = neg(&v)?;
    Ok(SquareRootPair {
        neg_squares_to_u: mul(&neg_v, &neg_v)? == u,
        distinct: neg_v != v,
        v_nonzero: v != zero(),
        u,
        v,
        neg_v,
    })
}

/// The least `k` in `1..=max_k` with `rotation(c, s)ᵏ = I`, or `None`; `rotation(0, 1)` has
/// order 4 while `R345` never returns on any finite window. Lean:
/// `U1PowerMapInjectivity.u345_infinite_order` (cited by the specification); kernel:
/// `fq_gap_stone_rational_rotation_infinite_order_and_zi_non_field_obstruction`.
pub fn rotation_order(c: &Q, s: &Q, max_k: u32) -> Result<Option<u32>, Error> {
    let r = rotation(c, s)?;
    if max_k == 0 {
        return Err(Error::NonPositiveBound);
    }
    let mut p = identity();
    for k in 1..=max_k {
        p = mul(&p, &r)?;
        if p == identity() {
            return Ok(Some(k));
        }
    }
    Ok(None)
}

// ============================================================================
// What is specified and what is derived
// ============================================================================

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Specification {
    pub node: &'static str,
    pub specified: &'static str,
    pub continuity: &'static str,
    pub generator_selection: &'static str,
    pub relationship: &'static str,
    pub derived: &'static str,
    pub open: &'static str,
    pub authority_effect: &'static str,
}

/// What node FQ-GAP-STONE-CONTINUOUS-TIME specifies, what this module derives, and what stays
/// open; nothing here is a theorem about a continuum. Lean: `QParamGroup`,
/// `no_qparam_group_through_R345`, and the open obligation in the module header.
pub fn specification() -> Specification {
    Specification {
        node: "FQ-GAP-STONE-CONTINUOUS-TIME",
        specified: "discrete evolution is the Z-action k -> U^k of one orthogonal step U on the \
                    finite carrier",
        continuity: "no topology on the finite carrier; the strongest finite notion is a \
                     Q-parameter group",
        generator_selection: "square roots of a step come in pairs ±V; no canonical generator",
        relationship: "a Q-parameter group restricts to the Z-action of its unit step and \
                       requires roots of every order; the Pythagorean rotation has no rational \
                       half-step, so no Q-parameter group of rational 2x2 matrices passes \
                       through it; continuous time needs a carrier extension (sqrt 5)",
        derived: "orbit orthogonality and the group law on every finite window; the half-angle \
                  criterion and its sign pair; the required square 4/5 for R345; the order of a \
                  rotation on a finite window",
        open: "the general triviality of Q-parameter groups over Q(i) is not proved (needs \
               unique factorisation in Z[i])",
        authority_effect: "None",
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn mi(rows: &[&[i64]]) -> Matrix {
        rows.iter()
            .map(|r| r.iter().map(|&x| q(x)).collect())
            .collect()
    }

    /// `R345² = rotation(−7/25, 24/25)`.
    fn r2() -> Matrix {
        rotation(&fr(-7, 25), &fr(24, 25)).unwrap()
    }

    fn neg_r345() -> Matrix {
        neg(&r345()).unwrap()
    }

    // ------------------------------------------------------------------ orbit

    #[test]
    fn test_rotation_and_point() {
        assert_eq!(rotation(&fr(3, 5), &fr(4, 5)).unwrap(), r345());
        assert_eq!(rotation_point(&r345()).unwrap(), (fr(3, 5), fr(4, 5)));
        assert!(is_orthogonal(&r345()).unwrap());
        assert_eq!(det(&r345()).unwrap(), q(1));
        assert_eq!(trace(&r345()).unwrap(), fr(6, 5));
        assert_eq!(rotation(&q(1), &q(0)).unwrap(), identity());
    }

    #[test]
    fn test_orbit_orthogonality_for_k_in_minus_6_to_6() {
        let e = discrete_evolution(&r345(), 6).unwrap();
        assert_eq!(e.kmax, 6);
        assert_eq!(e.exponents, (-6..=6).collect::<Vec<i64>>());
        assert_eq!(e.orbit.len(), 13);
        assert!(e.all_orthogonal && e.group_law && e.inverse_is_transpose);
        assert_eq!(e.orbit[6], identity());
        assert_eq!(e.orbit[7], r345());
        assert_eq!(e.orbit[5], transpose(&r345()).unwrap());
        assert_eq!(zpow(&r345(), 2).unwrap(), r2());
        assert_eq!(zpow(&r345(), -1).unwrap(), transpose(&r345()).unwrap());
        assert_eq!(zpow(&r345(), 0).unwrap(), identity());
        assert_eq!(
            mul(&zpow(&r345(), -3).unwrap(), &zpow(&r345(), 3).unwrap()).unwrap(),
            identity()
        );
        // sine numerators of R345^k, k = 1..4: the kernel theorem's nonzero witnesses
        let numerators: Vec<Q> = (1..=4u32)
            .map(|k| &zpow(&r345(), i64::from(k)).unwrap()[1][0] * q(5i64.pow(k)))
            .collect();
        assert_eq!(numerators, vec![q(4), q(24), q(44), q(-336)]);
        for k in -6..=6 {
            assert!(is_orthogonal(&zpow(&r345(), k).unwrap()).unwrap(), "{k}");
        }
        let e0 = discrete_evolution(&rotation(&q(0), &q(1)).unwrap(), 0).unwrap();
        assert_eq!(e0.orbit, vec![identity()]);
        assert!(e0.group_law && e0.inverse_is_transpose);
    }

    #[test]
    fn test_rotation_order() {
        assert_eq!(rotation_order(&q(0), &q(1), 10).unwrap(), Some(4));
        assert_eq!(rotation_order(&fr(3, 5), &fr(4, 5), 50).unwrap(), None);
        assert_eq!(rotation_order(&q(1), &q(0), 5).unwrap(), Some(1));
        assert_eq!(rotation_order(&q(-1), &q(0), 5).unwrap(), Some(2));
        assert_eq!(rotation_order(&q(0), &q(1), 3).unwrap(), None);
    }

    // ------------------------------------------------------------------ half-step

    #[test]
    fn test_is_rational_square() {
        let decided: Vec<bool> = [fr(4, 5), fr(9, 25), q(0), q(1), q(2), q(-1)]
            .iter()
            .map(|x| is_rational_square(x).unwrap())
            .collect();
        assert_eq!(decided, vec![false, true, true, true, false, false]);
        assert_eq!(rational_sqrt(&fr(9, 25)).unwrap(), Some(fr(3, 5)));
        assert_eq!(rational_sqrt(&fr(4, 5)).unwrap(), None);
        assert_eq!(rational_sqrt(&q(-1)).unwrap(), None);
        assert_eq!(rational_sqrt(&fr(49, 4)).unwrap(), Some(fr(7, 2)));
    }

    #[test]
    fn test_half_step_outcomes() {
        assert_eq!(half_step(&fr(3, 5), &fr(4, 5)).unwrap(), None);
        assert!(!has_rational_half_step(&fr(3, 5), &fr(4, 5)).unwrap());
        let hs = half_step(&fr(-7, 25), &fr(24, 25)).unwrap().unwrap();
        assert_eq!(hs, [r345(), neg_r345()]);
        assert!(has_rational_half_step(&fr(-7, 25), &fr(24, 25)).unwrap());
        for v in &hs {
            assert_eq!(mul(v, v).unwrap(), r2());
        }
        assert_eq!(
            half_step(&q(1), &q(0)).unwrap(),
            Some([identity(), neg(&identity()).unwrap()])
        );
        assert_eq!(
            half_step(&q(-1), &q(0)).unwrap(),
            Some([
                rotation(&q(0), &q(1)).unwrap(),
                rotation(&q(0), &q(-1)).unwrap()
            ])
        );
        assert_eq!(half_step(&q(0), &q(1)).unwrap(), None);
        let quarter = rotation(&q(0), &q(1)).unwrap();
        assert_eq!(
            mul(&quarter, &quarter).unwrap(),
            rotation(&q(-1), &q(0)).unwrap()
        );
    }

    #[test]
    fn test_qparam_root_chain_fails_at_the_first_step_for_r345() {
        assert_eq!(
            qparam_necessary_roots(&r345(), 2).unwrap(),
            RootChain::Obstructed {
                m: 2,
                depth: 1,
                at: (fr(3, 5), fr(4, 5)),
                required_square: fr(4, 5)
            }
        );
        assert!(matches!(
            qparam_necessary_roots(&r345(), 4).unwrap(),
            RootChain::Obstructed { m: 4, depth: 1, .. }
        ));
        assert_eq!(
            qparam_necessary_roots(&r2(), 2).unwrap(),
            RootChain::Roots {
                m: 2,
                depth: 1,
                roots: vec![(fr(3, 5), fr(4, 5)), (fr(-3, 5), fr(-4, 5))]
            }
        );
        let RootChain::Obstructed { depth, at, .. } = qparam_necessary_roots(&r2(), 4).unwrap()
        else {
            panic!("R345^2 has no rational fourth root");
        };
        assert_eq!((depth, at), (2, (fr(3, 5), fr(4, 5))));
        assert_eq!(
            qparam_necessary_roots(&r345(), 1).unwrap(),
            RootChain::Roots {
                m: 1,
                depth: 0,
                roots: vec![(fr(3, 5), fr(4, 5))]
            }
        );
        let RootChain::Roots { roots, .. } = qparam_necessary_roots(&identity(), 4).unwrap()
        else {
            panic!("the identity has rational fourth roots");
        };
        assert_eq!(
            roots,
            vec![(q(1), q(0)), (q(-1), q(0)), (q(0), q(1)), (q(0), q(-1))]
        );
    }

    #[test]
    fn test_commutant_candidates_and_certificate() {
        let c = commutant_half_step_candidates(&r345()).unwrap();
        assert_eq!(c.half_trace, fr(3, 5));
        assert_eq!(c.det, q(1));
        assert_eq!(c.kappa, fr(-16, 25));
        assert_eq!(
            c.j,
            vec![vec![q(0), fr(-4, 5)], vec![fr(4, 5), q(0)]]
        );
        assert_eq!(c.candidate_p_squares, vec![fr(4, 5), fr(-1, 5)]);
        assert!(c.roots.is_empty());
        let c2 = commutant_half_step_candidates(&r2()).unwrap();
        assert_eq!(c2.candidate_p_squares, vec![fr(9, 25), fr(-16, 25)]);
        assert_eq!(c2.roots, vec![r345(), neg_r345()]);
        let g = commutant_half_step_candidates(&mi(&[&[0, -2], &[2, 0]])).unwrap();
        assert_eq!(g.candidate_p_squares, vec![q(1), q(-1)]);
        assert_eq!(
            g.roots,
            vec![mi(&[&[1, -1], &[1, 1]]), mi(&[&[-1, 1], &[-1, -1]])]
        );
        let h = commutant_half_step_candidates(&mi(&[&[1, 2], &[3, 4]])).unwrap();
        assert!(h.candidate_p_squares.is_empty() && h.roots.is_empty());
        assert_eq!(
            no_rational_half_step_certificate(&r345()).unwrap(),
            NoRationalHalfStepCertificate {
                required_square: fr(4, 5),
                is_rational_square: false
            }
        );
        assert_eq!(
            no_rational_half_step_certificate(&r2()).unwrap(),
            NoRationalHalfStepCertificate {
                required_square: fr(9, 25),
                is_rational_square: true
            }
        );
        assert!(irreducible_char_poly(&r345()).unwrap());
        assert!(irreducible_char_poly(&rotation(&q(0), &q(1)).unwrap()).unwrap());
        assert!(!irreducible_char_poly(&identity()).unwrap());
        assert!(!irreducible_char_poly(&mi(&[&[2, 0], &[0, 3]])).unwrap());
    }

    #[test]
    fn test_square_root_pairs() {
        let p = square_root_pairs(&r345()).unwrap();
        assert_eq!((p.u, p.v, p.neg_v), (r2(), r345(), neg_r345()));
        assert!(p.neg_squares_to_u && p.distinct && p.v_nonzero);
        let z = square_root_pairs(&zero()).unwrap();
        assert!(z.neg_squares_to_u);
        assert!(!z.distinct && !z.v_nonzero);
    }

    // ------------------------------------------------------------------ guards and fence

    #[test]
    fn test_refusals_are_typed_and_never_panic() {
        use DiscreteTimeStoneError as E;
        assert_eq!(matrix2(&mi(&[&[1, 2, 3], &[4, 5, 6]])), Err(E::NotTwoByTwo));
        assert_eq!(matrix2(&mi(&[&[1, 2]])), Err(E::NotTwoByTwo));
        assert_eq!(
            matrix2(&mi(&[&[1, 2], &[3, 4], &[5, 6]])),
            Err(E::NotTwoByTwo)
        );
        assert_eq!(matrix2(&[]), Err(E::NotTwoByTwo));
        assert_eq!(
            mul(&mi(&[&[1, 2, 3], &[4, 5, 6], &[7, 8, 9]]), &identity()),
            Err(E::NotTwoByTwo)
        );
        assert_eq!(square_root_pairs(&mi(&[&[1, 2]])), Err(E::NotTwoByTwo));
        assert_eq!(
            commutant_half_step_candidates(&mi(&[&[1, 2, 3], &[4, 5, 6], &[7, 8, 9]])),
            Err(E::NotTwoByTwo)
        );
        assert_eq!(rotation(&q(1), &q(1)), Err(E::NotOnCircle { norm: q(2) }));
        assert_eq!(
            rotation(&fr(1, 2), &fr(1, 2)),
            Err(E::NotOnCircle { norm: fr(1, 2) })
        );
        assert_eq!(half_step(&q(1), &q(1)), Err(E::NotOnCircle { norm: q(2) }));
        assert_eq!(
            rotation_order(&q(1), &q(1), 5),
            Err(E::NotOnCircle { norm: q(2) })
        );
        assert_eq!(rotation_point(&mi(&[&[1, 2], &[3, 4]])), Err(E::NotARotation));
        assert_eq!(
            rotation_point(&vec![vec![fr(3, 5), fr(4, 5)], vec![fr(4, 5), fr(3, 5)]]),
            Err(E::NotARotation)
        );
        assert_eq!(
            qparam_necessary_roots(&mi(&[&[1, 2], &[3, 4]]), 2),
            Err(E::NotARotation)
        );
        assert_eq!(
            no_rational_half_step_certificate(&mi(&[&[1, 2], &[3, 4]])),
            Err(E::NotARotation)
        );
        assert_eq!(zpow(&mi(&[&[1, 2], &[3, 4]]), -1), Err(E::NotOrthogonal));
        assert_eq!(
            discrete_evolution(&mi(&[&[1, 2], &[3, 4]]), 2),
            Err(E::NotOrthogonal)
        );
        assert_eq!(qparam_necessary_roots(&r345(), 3), Err(E::NotAPowerOfTwo(3)));
        assert_eq!(qparam_necessary_roots(&r345(), 0), Err(E::NotAPowerOfTwo(0)));
        assert_eq!(
            commutant_half_step_candidates(&identity()),
            Err(E::ReducibleCharacteristicPolynomial)
        );
        assert_eq!(
            commutant_half_step_candidates(&mi(&[&[2, 0], &[0, 3]])),
            Err(E::ReducibleCharacteristicPolynomial)
        );
        assert_eq!(rotation_order(&q(0), &q(1), 0), Err(E::NonPositiveBound));
        let raw = Q::new_raw(BigInt::from(2), BigInt::from(4));
        assert_eq!(
            is_rational_square(&raw),
            Err(E::InexactEntry(RationalConstructionError::NonReduced))
        );
        assert_eq!(
            rotation(&raw, &q(0)),
            Err(E::InexactEntry(RationalConstructionError::NonReduced))
        );
        assert_eq!(
            matrix2(&[vec![raw.clone(), q(0)], vec![q(0), q(1)]]),
            Err(E::InexactEntry(RationalConstructionError::NonReduced))
        );
    }

    #[test]
    fn test_zpow_of_a_non_orthogonal_matrix_is_still_defined_for_nonnegative_k() {
        let shear = mi(&[&[1, 1], &[0, 1]]);
        assert_eq!(zpow(&shear, 3).unwrap(), mi(&[&[1, 3], &[0, 1]]));
        assert_eq!(zpow(&shear, 0).unwrap(), identity());
    }

    #[test]
    fn test_specification_strings_fence_and_provenance() {
        let s = specification();
        assert_eq!(s.node, "FQ-GAP-STONE-CONTINUOUS-TIME");
        assert_eq!(s.authority_effect, "None");
        assert_eq!(
            s.continuity,
            "no topology on the finite carrier; the strongest finite notion is a Q-parameter group"
        );
        assert_eq!(
            s.generator_selection,
            "square roots of a step come in pairs ±V; no canonical generator"
        );
        assert_eq!(
            s.relationship,
            "a Q-parameter group restricts to the Z-action of its unit step and requires roots \
             of every order; the Pythagorean rotation has no rational half-step, so no \
             Q-parameter group of rational 2x2 matrices passes through it; continuous time \
             needs a carrier extension (sqrt 5)"
        );
        assert_eq!(
            s.open,
            "the general triviality of Q-parameter groups over Q(i) is not proved (needs unique \
             factorisation in Z[i])"
        );
        assert!(s.derived.contains("4/5") && s.specified.contains("Z-action"));
        assert!(AUTHORITY_FENCE.contains("AuthorityEffect None"));
        assert!(AUTHORITY_FENCE.contains("no continuous-time group"));
        assert!(PROVENANCE.contains("20261020T225000Z_discrete_time_spec/DiscreteTimeStoneSpec.lean"));
        assert!(PROVENANCE.contains("fq_gap_stone_rational_rotation_infinite_order_and_zi_non_field_obstruction"));
        assert!(PROVENANCE.contains("code/python/src/qm/discrete_time_stone.py"));
        for theorem in [
            "BornFinite.DiscreteTime",
            "QParamGroup",
            "discreteEvolution",
            "U_eq_discreteEvolution",
            "roots_of_all_orders",
            "sq_root_neg",
            "half_step_not_unique",
            "R345_pow_orthogonal",
            "four_fifths_not_rat_square",
            "no_rational_half_step",
            "no_qparam_group_through_R345",
        ] {
            assert!(PROVENANCE.contains(theorem), "{theorem}");
        }
    }
}
