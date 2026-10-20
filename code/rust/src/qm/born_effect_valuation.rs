//! Exact effect-additive valuations on rational matrices: the Born trace form from effect
//! additivity, not from Gleason.
//!
//! Replays in exact rational arithmetic the Lean modules of
//! `dag/results/FQ-GAP-BORN-UNIQUENESS-GLEASON/runs/20261020T205000Z_effect_valuation_lean`
//! (`BornEffectValuation`, `BornLinearExtension`, `BornMatrixCarrier`,
//! `BornTraceRepresentation`, `BornPsdDecomposition`, `BornRationalSphereObstruction`) and
//! mirrors, function for function, the Python twin
//! `code/python/src/qm/born_effect_valuation.py`:
//!
//! * rational PSD certification by a Gram (LDLᵀ) decomposition `E = Σ_k d_k w_k w_kᵀ` with
//!   `d_k ≥ 0`, or an exact negative witness `x` with `xᵀ E x < 0`, built on the crate's
//!   [`ldlt`] (the Gram terms are the pivots and the columns of the unit lower factor);
//! * effects `0 ≤ E ≤ I` in the quadratic-form preorder (unit = identity) and the rank-one
//!   effects `x xᵀ / (x·x)`;
//! * the order-unit bound `⌈Σ|a_ij|⌉` and the midpoint extension
//!   `L(A) = 2t·v((A + tI)/(2t)) − t` of a valuation `v` to a rational linear functional,
//!   with its consistency across bounds;
//! * the representing matrix `ρ_ij = L(E_ji)` with `trace(ρE) = v(E)` and the Born certificate
//!   (`ρ` symmetric, PSD, trace 1, agreeing with `v` on the supplied effects);
//! * two mutation controls: a non-additive valuation (its extension depends on the bound) and
//!   a linear but non-positive valuation (its `ρ` is not PSD, with an exact witness);
//! * the parity frame function on rational rays of `S²`, which sums to 1 on every orthogonal
//!   triple of rays yet is reproduced by no quadratic form.
//!
//! The matrix algebra and its order are supplied; only the form of the valuation is derived.
//! No Gleason theorem is proved. AuthorityEffect: None.

use std::collections::BTreeSet;

use num_bigint::BigInt;
use num_traits::{One, Signed, Zero};

use crate::linear_algebra::basic_matrix::BasicMatrix;
use crate::linear_algebra::ordered::{ldlt, LdltOutcome};
use crate::linear_algebra::scalars::{validate_rational, RationalConstructionError};
use crate::linear_algebra::{q, ExactFieldError, Q};

pub const AUTHORITY_FENCE: &str = "AuthorityEffect None; not PROVED; no Gleason theorem is proved; \
     the matrix algebra and its order are supplied, only the form of the valuation is derived; \
     assumptions exposed.";

pub const PROVENANCE: &str = "Replays the Lean modules of \
     dag/results/FQ-GAP-BORN-UNIQUENESS-GLEASON/runs/20261020T205000Z_effect_valuation_lean \
     (BornEffectValuation, BornLinearExtension, BornMatrixCarrier, BornTraceRepresentation, \
     BornPsdDecomposition, BornRationalSphereObstruction) and the Python twin \
     code/python/src/qm/born_effect_valuation.py.";

/// A rational matrix as rows; every public entry point re-admits it through [`matrix`].
pub type Matrix = Vec<Vec<Q>>;
/// A rational vector; every public entry point re-admits it through [`vector`].
pub type Vector = Vec<Q>;
/// A valuation on rational matrices. The Born valuation [`born_valuation`] and the two
/// controls [`square_valuation`] and [`bad_linear_valuation`] all have this shape.
pub type Valuation<'a> = &'a dyn Fn(&Matrix) -> Q;
/// An integer triple; [`is_ray`] decides whether it is a rational ray of `S²`.
pub type Ray = [i64; 3];

#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum BornEffectValuationError {
    #[error("nonempty square matrix required")]
    NonSquareMatrix,
    #[error("nonempty vector required")]
    EmptyVector,
    #[error("nonempty linear system required")]
    EmptySystem,
    #[error("exact canonical rational entries required: {0}")]
    InexactEntry(#[from] RationalConstructionError),
    #[error("{operation}: dimension {expected} expected, got {got}")]
    DimensionMismatch {
        operation: &'static str,
        expected: usize,
        got: usize,
    },
    #[error("index {index} is outside dimension {dimension}")]
    IndexOutOfRange { index: usize, dimension: usize },
    #[error("symmetric matrix required")]
    NotSymmetric,
    #[error("nonzero vector required")]
    ZeroVector,
    #[error("positive bound required")]
    NonPositiveBound,
    #[error("effects and effect pairs with effect sums required")]
    NotAnEffect,
    #[error("ray required: an integer triple, not all even, with a square norm")]
    NotARay,
    #[error("linear algebra: {0}")]
    LinearAlgebra(#[from] ExactFieldError),
}

type Error = BornEffectValuationError;

// ============================================================================
// Exact-input admission and the matrix algebra (supplied, not derived)
// ============================================================================

/// Admit a nonempty square matrix of canonical rationals.
pub fn matrix(rows: &[Vec<Q>]) -> Result<Matrix, Error> {
    let n = rows.len();
    if n == 0 || rows.iter().any(|r| r.len() != n) {
        return Err(Error::NonSquareMatrix);
    }
    for x in rows.iter().flatten() {
        validate_rational(x)?;
    }
    Ok(rows.to_vec())
}

/// Admit a nonempty vector of canonical rationals.
pub fn vector(xs: &[Q]) -> Result<Vector, Error> {
    if xs.is_empty() {
        return Err(Error::EmptyVector);
    }
    for x in xs {
        validate_rational(x)?;
    }
    Ok(xs.to_vec())
}

fn same_length(operation: &'static str, expected: usize, got: usize) -> Result<(), Error> {
    if expected == got {
        Ok(())
    } else {
        Err(Error::DimensionMismatch {
            operation,
            expected,
            got,
        })
    }
}

fn same_shape(operation: &'static str, a: &Matrix, b: &Matrix) -> Result<(), Error> {
    same_length(operation, a.len(), b.len())?;
    for (ra, rb) in a.iter().zip(b) {
        same_length(operation, ra.len(), rb.len())?;
    }
    Ok(())
}

fn half() -> Q {
    Q::new(BigInt::one(), BigInt::from(2))
}

pub fn identity(n: usize) -> Matrix {
    (0..n)
        .map(|i| {
            (0..n)
                .map(|j| if i == j { Q::one() } else { Q::zero() })
                .collect()
        })
        .collect()
}

/// The matrix unit `E_ij` of dimension `n`.
pub fn single(n: usize, i: usize, j: usize) -> Result<Matrix, Error> {
    for index in [i, j] {
        if index >= n {
            return Err(Error::IndexOutOfRange {
                index,
                dimension: n,
            });
        }
    }
    Ok((0..n)
        .map(|r| {
            (0..n)
                .map(|c| if r == i && c == j { Q::one() } else { Q::zero() })
                .collect()
        })
        .collect())
}

pub fn add(a: &Matrix, b: &Matrix) -> Result<Matrix, Error> {
    same_shape("add", a, b)?;
    Ok(a.iter()
        .zip(b)
        .map(|(ra, rb)| ra.iter().zip(rb).map(|(x, y)| x + y).collect())
        .collect())
}

pub fn sub(a: &Matrix, b: &Matrix) -> Result<Matrix, Error> {
    same_shape("sub", a, b)?;
    Ok(a.iter()
        .zip(b)
        .map(|(ra, rb)| ra.iter().zip(rb).map(|(x, y)| x - y).collect())
        .collect())
}

pub fn scale(c: &Q, a: &Matrix) -> Matrix {
    a.iter()
        .map(|r| r.iter().map(|x| c * x).collect())
        .collect()
}

/// The transpose; like the twin's `zip(*A)`, columns beyond the shortest row are dropped.
pub fn transpose(a: &Matrix) -> Matrix {
    let cols = a.iter().map(Vec::len).min().unwrap_or(0);
    (0..cols)
        .map(|j| a.iter().map(|r| r[j].clone()).collect())
        .collect()
}

pub fn mat_vec(a: &Matrix, x: &[Q]) -> Result<Vector, Error> {
    a.iter()
        .map(|r| {
            same_length("mat_vec", r.len(), x.len())?;
            Ok(r.iter().zip(x).fold(Q::zero(), |acc, (p, v)| acc + p * v))
        })
        .collect()
}

pub fn dot(x: &[Q], y: &[Q]) -> Result<Q, Error> {
    same_length("dot", x.len(), y.len())?;
    Ok(x.iter().zip(y).fold(Q::zero(), |acc, (a, b)| acc + a * b))
}

pub fn outer(x: &[Q], y: &[Q]) -> Matrix {
    x.iter()
        .map(|a| y.iter().map(|b| a * b).collect())
        .collect()
}

pub fn trace(a: &Matrix) -> Q {
    a.iter()
        .enumerate()
        .filter_map(|(i, r)| r.get(i))
        .fold(Q::zero(), |acc, x| acc + x)
}

/// `trace(A B) = Σ_ij A_ij B_ji`; both matrices must be `n × n`.
pub fn trace_mul(a: &Matrix, b: &Matrix) -> Result<Q, Error> {
    let n = a.len();
    same_length("trace_mul", n, b.len())?;
    for r in a.iter().chain(b) {
        same_length("trace_mul", n, r.len())?;
    }
    let mut acc = Q::zero();
    for i in 0..n {
        for j in 0..n {
            acc = acc + &a[i][j] * &b[j][i];
        }
    }
    Ok(acc)
}

/// `xᵀ A x`.
pub fn quadratic_form(a: &Matrix, x: &[Q]) -> Result<Q, Error> {
    dot(x, &mat_vec(a, x)?)
}

pub fn is_symmetric(a: &Matrix) -> bool {
    *a == transpose(a)
}

/// `(A + Aᵀ)/2`.
pub fn symmetric_part(a: &Matrix) -> Result<Matrix, Error> {
    Ok(scale(&half(), &add(a, &transpose(a))?))
}

// ============================================================================
// Rational PSD certification: Gram (LDLᵀ) terms or an exact negative witness
// ============================================================================

/// The outcome of [`gram_decomposition`].
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum GramDecomposition {
    /// `E = Σ_k d_k w_k w_kᵀ` with every `d_k > 0` (zero pivots contribute no term).
    Psd { terms: Vec<(Q, Vector)> },
    /// `witnessᵀ E witness < 0`.
    NotPsd { witness: Vector },
}

fn to_basic(e: &Matrix) -> Result<BasicMatrix<Q>, Error> {
    let n = e.len();
    let data: Vec<Q> = e.iter().flatten().cloned().collect();
    Ok(BasicMatrix::from_row_major(n, n, data).map_err(ExactFieldError::from)?)
}

/// Gram terms `(d_k, w_k)` with `E == Σ d_k w_k w_kᵀ` and `d_k ≥ 0`, or a witness `x` with
/// `xᵀ E x < 0`. Refuses a non-symmetric matrix. The terms are read off the crate's exact
/// [`ldlt`]: `d_k` is the `k`-th pivot and `w_k` the `k`-th column of the unit lower factor.
pub fn gram_decomposition(e: &Matrix) -> Result<GramDecomposition, Error> {
    let e = matrix(e)?;
    if !is_symmetric(&e) {
        return Err(Error::NotSymmetric);
    }
    let n = e.len();
    let factor = ldlt(&to_basic(&e)?)?;
    match factor.outcome() {
        LdltOutcome::PositiveSemidefinite => {
            let lower = factor.unit_lower();
            let mut terms = Vec::new();
            for (k, pivot) in factor.pivots().iter().enumerate() {
                if pivot.is_zero() {
                    continue;
                }
                let mut w = Vec::with_capacity(n);
                for i in 0..n {
                    w.push(lower.get(i, k).map_err(ExactFieldError::from)?);
                }
                terms.push((pivot.clone(), w));
            }
            Ok(GramDecomposition::Psd { terms })
        }
        LdltOutcome::NegativePivot { witness, .. }
        | LdltOutcome::ZeroPivotWithNonzeroColumn { witness, .. } => {
            Ok(GramDecomposition::NotPsd {
                witness: witness.clone(),
            })
        }
    }
}

/// `true` when every `d_k ≥ 0` and `Σ d_k w_k w_kᵀ == E` exactly.
pub fn verify_gram(e: &Matrix, terms: &[(Q, Vector)]) -> Result<bool, Error> {
    let e = matrix(e)?;
    let n = e.len();
    let mut s: Matrix = vec![vec![Q::zero(); n]; n];
    for (d, w) in terms {
        validate_rational(d)?;
        if d < &Q::zero() {
            return Ok(false);
        }
        let w = vector(w)?;
        s = add(&s, &scale(d, &outer(&w, &w)))?;
    }
    Ok(s == e)
}

/// The replayable PSD certificate of a (not necessarily symmetric) matrix, decided on its
/// symmetric part.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum PsdCertificate {
    Psd {
        terms: Vec<(Q, Vector)>,
        reconstructs: bool,
    },
    NotPsd {
        witness: Vector,
        value: Q,
    },
}

impl PsdCertificate {
    pub fn is_psd(&self) -> bool {
        matches!(self, Self::Psd { .. })
    }
}

pub fn psd_certificate(e: &Matrix) -> Result<PsdCertificate, Error> {
    let e = matrix(e)?;
    let sym = symmetric_part(&e)?;
    match gram_decomposition(&sym)? {
        GramDecomposition::Psd { terms } => {
            let reconstructs = verify_gram(&sym, &terms)?;
            Ok(PsdCertificate::Psd {
                terms,
                reconstructs,
            })
        }
        GramDecomposition::NotPsd { witness } => {
            let value = quadratic_form(&e, &witness)?;
            Ok(PsdCertificate::NotPsd { witness, value })
        }
    }
}

pub fn is_psd(e: &Matrix) -> Result<bool, Error> {
    Ok(matches!(
        gram_decomposition(&symmetric_part(&matrix(e)?)?)?,
        GramDecomposition::Psd { .. }
    ))
}

/// `0 ≤ E ≤ I` in the quadratic-form preorder.
pub fn is_effect(e: &Matrix) -> Result<bool, Error> {
    let e = matrix(e)?;
    Ok(is_psd(&e)? && is_psd(&sub(&identity(e.len()), &e)?)?)
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct EffectCertificate {
    pub lower: PsdCertificate,
    pub upper: PsdCertificate,
    pub is_effect: bool,
}

pub fn effect_certificate(e: &Matrix) -> Result<EffectCertificate, Error> {
    let e = matrix(e)?;
    Ok(EffectCertificate {
        lower: psd_certificate(&e)?,
        upper: psd_certificate(&sub(&identity(e.len()), &e)?)?,
        is_effect: is_effect(&e)?,
    })
}

/// `x xᵀ / (x·x)`, the projector onto the ray of `x`.
pub fn rank_one_effect(x: &[Q]) -> Result<Matrix, Error> {
    let x = vector(x)?;
    let nrm = dot(&x, &x)?;
    if nrm.is_zero() {
        return Err(Error::ZeroVector);
    }
    Ok(scale(&nrm.recip(), &outer(&x, &x)))
}

// ============================================================================
// Order unit, midpoint extension, representing matrix, Born certificate
// ============================================================================

/// `⌈Σ|a_ij|⌉`, a `t` with `−t·I ≤ A ≤ t·I`.
pub fn order_unit_bound(a: &Matrix) -> Result<BigInt, Error> {
    let a = matrix(a)?;
    let total = a
        .iter()
        .flatten()
        .fold(Q::zero(), |acc, x| acc + x.abs());
    Ok(total.ceil().to_integer())
}

/// `−t·(x·x) ≤ xᵀ A x ≤ t·(x·x)`.
pub fn bounded_by(a: &Matrix, t: &Q, x: &[Q]) -> Result<bool, Error> {
    let a = matrix(a)?;
    validate_rational(t)?;
    let x = vector(x)?;
    let form = quadratic_form(&a, &x)?;
    let s = t * dot(&x, &x)?;
    Ok(-s.clone() <= form && form <= s)
}

/// `(A + t·I)/(2t)`, an effect whenever `−t·I ≤ A ≤ t·I`; refuses `t ≤ 0`.
pub fn midpoint(a: &Matrix, t: &Q) -> Result<Matrix, Error> {
    let a = matrix(a)?;
    validate_rational(t)?;
    if t <= &Q::zero() {
        return Err(Error::NonPositiveBound);
    }
    let two_t = t + t;
    Ok(scale(
        &two_t.recip(),
        &add(&a, &scale(t, &identity(a.len())))?,
    ))
}

fn evaluate(valuation: Valuation<'_>, e: &Matrix) -> Result<Q, Error> {
    let value = valuation(e);
    validate_rational(&value)?;
    Ok(value)
}

/// The midpoint extension `L(A) = 2t·v((A + tI)/(2t)) − t`; `t` defaults to
/// `order_unit_bound(A) + 1`.
pub fn extend(valuation: Valuation<'_>, a: &Matrix, t: Option<&Q>) -> Result<Q, Error> {
    let a = matrix(a)?;
    let t = match t {
        Some(t) => {
            validate_rational(t)?;
            t.clone()
        }
        None => Q::from_integer(order_unit_bound(&a)? + BigInt::one()),
    };
    let value = evaluate(valuation, &midpoint(&a, &t)?)?;
    let two_t = &t + &t;
    Ok(two_t * value - t)
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ExtensionConsistency {
    pub bounds: Vec<Q>,
    pub values: Vec<Q>,
    /// All extensions agree (false for an empty list of bounds, as for the twin).
    pub consistent: bool,
}

pub fn extension_consistency(
    valuation: Valuation<'_>,
    a: &Matrix,
    bounds: &[Q],
) -> Result<ExtensionConsistency, Error> {
    let values = bounds
        .iter()
        .map(|t| extend(valuation, a, Some(t)))
        .collect::<Result<Vec<Q>, Error>>()?;
    let consistent = values
        .first()
        .is_some_and(|first| values.iter().all(|v| v == first));
    Ok(ExtensionConsistency {
        bounds: bounds.to_vec(),
        values,
        consistent,
    })
}

/// `ρ_ij = L(E_ji)`, so that `trace(ρ A) = L(A)` for a linear `L`.
pub fn representing_matrix(valuation: Valuation<'_>, n: usize) -> Result<Matrix, Error> {
    let mut rho = Vec::with_capacity(n);
    for i in 0..n {
        let mut row = Vec::with_capacity(n);
        for j in 0..n {
            row.push(extend(valuation, &single(n, j, i)?, None)?);
        }
        rho.push(row);
    }
    Ok(rho)
}

/// An owned valuation; `&v` passes as a [`Valuation`].
pub type BoxedValuation = Box<dyn Fn(&Matrix) -> Q>;

/// The Born valuation `E ↦ trace(ρ E)`. The returned closure has the fixed shape
/// [`Valuation`], so a matrix of the wrong dimension is a caller error and panics; every
/// consumer in this module only ever applies it to matrices of `ρ`'s dimension.
pub fn born_valuation(rho: &Matrix) -> Result<BoxedValuation, Error> {
    let rho = matrix(rho)?;
    Ok(Box::new(move |e: &Matrix| {
        trace_mul(&rho, e).expect("born_valuation: the matrix must have the dimension of rho")
    }))
}

fn admitted_effect(operation: &'static str, n: usize, e: &Matrix) -> Result<Matrix, Error> {
    let e = matrix(e)?;
    same_length(operation, n, e.len())?;
    if !is_effect(&e)? {
        return Err(Error::NotAnEffect);
    }
    Ok(e)
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ValuationAxioms {
    pub unit: bool,
    pub nonneg: bool,
    pub additive: bool,
}

/// `v(I) = 1`, `v(E) ≥ 0` on the effects, `v(E + F) = v(E) + v(F)` on the pairs. Refuses a
/// non-effect, a pair whose sum is not an effect, or a matrix not of dimension `n`.
pub fn valuation_axioms(
    valuation: Valuation<'_>,
    n: usize,
    effects: &[Matrix],
    pairs: &[(Matrix, Matrix)],
) -> Result<ValuationAxioms, Error> {
    let effects = effects
        .iter()
        .map(|e| admitted_effect("valuation_axioms", n, e))
        .collect::<Result<Vec<Matrix>, Error>>()?;
    let mut sums = Vec::with_capacity(pairs.len());
    for (e, f) in pairs {
        let e = admitted_effect("valuation_axioms", n, e)?;
        let f = admitted_effect("valuation_axioms", n, f)?;
        let s = add(&e, &f)?;
        if !is_effect(&s)? {
            return Err(Error::NotAnEffect);
        }
        sums.push((e, f, s));
    }
    let unit = evaluate(valuation, &identity(n))? == Q::one();
    let mut nonneg = true;
    for e in &effects {
        if evaluate(valuation, e)? < Q::zero() {
            nonneg = false;
            break;
        }
    }
    let mut additive = true;
    for (e, f, s) in &sums {
        if evaluate(valuation, s)? != evaluate(valuation, e)? + evaluate(valuation, f)? {
            additive = false;
            break;
        }
    }
    Ok(ValuationAxioms {
        unit,
        nonneg,
        additive,
    })
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct BornCertificate {
    pub rho: Matrix,
    pub symmetric: bool,
    pub trace: Q,
    pub psd: bool,
    pub psd_certificate: PsdCertificate,
    pub agrees_on_effects: bool,
    pub effects_checked: usize,
}

/// The representing matrix of `valuation` in dimension `n` with its exact PSD certificate,
/// trace, symmetry, and agreement `trace(ρE) = v(E)` on the supplied effects.
pub fn born_certificate(
    valuation: Valuation<'_>,
    n: usize,
    effects: &[Matrix],
) -> Result<BornCertificate, Error> {
    let effects = effects
        .iter()
        .map(|e| admitted_effect("born_certificate", n, e))
        .collect::<Result<Vec<Matrix>, Error>>()?;
    let rho = representing_matrix(valuation, n)?;
    let psd_certificate = psd_certificate(&rho)?;
    let mut agrees_on_effects = true;
    for e in &effects {
        if trace_mul(&rho, e)? != evaluate(valuation, e)? {
            agrees_on_effects = false;
            break;
        }
    }
    Ok(BornCertificate {
        symmetric: is_symmetric(&rho),
        trace: trace(&rho),
        psd: psd_certificate.is_psd(),
        psd_certificate,
        agrees_on_effects,
        effects_checked: effects.len(),
        rho,
    })
}

// ============================================================================
// Mutation controls
// ============================================================================

/// Control: `E ↦ E_00²`, unit and nonnegative but not additive. Requires a nonempty matrix.
pub fn square_valuation(e: &Matrix) -> Q {
    let x = e
        .first()
        .and_then(|r| r.first())
        .expect("square_valuation: nonempty matrix required");
    x * x
}

/// Control: `E ↦ 2·E_00 − E_22`, linear with unit value 1 but not positive. Requires a `3 × 3`
/// matrix (the three-dimensional control).
pub fn bad_linear_valuation(e: &Matrix) -> Q {
    assert!(
        e.len() == 3 && e.iter().all(|r| r.len() == 3),
        "bad_linear_valuation: three-dimensional control"
    );
    q(2) * &e[0][0] - &e[2][2]
}

// ============================================================================
// The parity frame function on rational rays of S²
// ============================================================================

fn square_norm(v: &Ray) -> u128 {
    v.iter()
        .map(|x| {
            let u = u128::from(x.unsigned_abs());
            u * u
        })
        .sum()
}

/// An integer triple, not all even, whose square norm is a perfect square (so that `v/|v|`
/// is a rational point of `S²`).
pub fn is_ray(v: &Ray) -> bool {
    if v.iter().all(|x| x % 2 == 0) {
        return false;
    }
    let s = square_norm(v);
    let r = s.isqrt();
    r * r == s
}

/// `1` when the third coordinate is odd, else `0`. Refuses a non-ray.
pub fn parity(v: &Ray) -> Result<Q, Error> {
    if !is_ray(v) {
        return Err(Error::NotARay);
    }
    Ok(if v[2] % 2 != 0 { Q::one() } else { Q::zero() })
}

/// All rays with coordinates in `[-n, n]`, in lexicographic order.
pub fn rays_in_box(n: i64) -> Vec<Ray> {
    let mut out = Vec::new();
    for a in -n..=n {
        for b in -n..=n {
            for c in -n..=n {
                let v = [a, b, c];
                if is_ray(&v) {
                    out.push(v);
                }
            }
        }
    }
    out
}

fn integer_dot(u: &Ray, v: &Ray) -> i128 {
    u.iter()
        .zip(v)
        .map(|(a, b)| i128::from(*a) * i128::from(*b))
        .sum()
}

/// Every `(u, v, w)` with `u < v < w` in list order and pairwise zero dot products.
pub fn orthogonal_triples(rays: &[Ray]) -> Vec<(Ray, Ray, Ray)> {
    let mut out = Vec::new();
    for (i, u) in rays.iter().enumerate() {
        for (j, v) in rays.iter().enumerate().skip(i + 1) {
            if integer_dot(u, v) != 0 {
                continue;
            }
            for w in rays.iter().skip(j + 1) {
                if integer_dot(u, w) == 0 && integer_dot(v, w) == 0 {
                    out.push((*u, *v, *w));
                }
            }
        }
    }
    out
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ParityFrameCheck {
    pub box_size: i64,
    pub rays: usize,
    pub orthogonal_triples: usize,
    pub all_sum_to_one: bool,
    /// The distinct parity values taken on the rays, ascending.
    pub values: Vec<Q>,
}

/// Parity sums to 1 on every orthogonal triple of rays in the box `|coords| ≤ n`.
pub fn parity_frame_check(n: i64) -> Result<ParityFrameCheck, Error> {
    let rays = rays_in_box(n);
    let triples = orthogonal_triples(&rays);
    let mut all_sum_to_one = true;
    for (u, v, w) in &triples {
        if parity(u)? + parity(v)? + parity(w)? != Q::one() {
            all_sum_to_one = false;
            break;
        }
    }
    let values = rays
        .iter()
        .map(parity)
        .collect::<Result<BTreeSet<Q>, Error>>()?;
    Ok(ParityFrameCheck {
        box_size: n,
        rays: rays.len(),
        orthogonal_triples: triples.len(),
        all_sum_to_one,
        values: values.into_iter().collect(),
    })
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum LinearSystemOutcome {
    Inconsistent,
    /// One solution, with every free unknown set to `0`.
    Solution(Vector),
}

/// Exact Gauss–Jordan elimination on `rows · x = rhs`.
pub fn solve_linear_system(rows: &[Vec<Q>], rhs: &[Q]) -> Result<LinearSystemOutcome, Error> {
    let m = rows.len();
    if m == 0 {
        return Err(Error::EmptySystem);
    }
    same_length("solve_linear_system", m, rhs.len())?;
    let n = rows[0].len();
    let mut aug: Vec<Vec<Q>> = Vec::with_capacity(m);
    for (r, b) in rows.iter().zip(rhs) {
        same_length("solve_linear_system", n, r.len())?;
        let row = vector(r)?;
        validate_rational(b)?;
        let mut row = row;
        row.push(b.clone());
        aug.push(row);
    }
    let mut r = 0;
    let mut pivots = Vec::new();
    for c in 0..n {
        let Some(p) = (r..m).find(|&i| !aug[i][c].is_zero()) else {
            continue;
        };
        aug.swap(r, p);
        let inverse = aug[r][c].recip();
        for x in aug[r].iter_mut() {
            *x = &*x * &inverse;
        }
        let pivot_row = aug[r].clone();
        for (i, row) in aug.iter_mut().enumerate() {
            if i != r && !row[c].is_zero() {
                let factor = row[c].clone();
                for (x, y) in row.iter_mut().zip(&pivot_row) {
                    *x = &*x - &(&factor * y);
                }
            }
        }
        pivots.push(c);
        r += 1;
    }
    if aug
        .iter()
        .any(|row| row[..n].iter().all(Zero::is_zero) && !row[n].is_zero())
    {
        return Ok(LinearSystemOutcome::Inconsistent);
    }
    let mut solution = vec![Q::zero(); n];
    for (i, c) in pivots.iter().enumerate() {
        solution[*c] = aug[i][n].clone();
    }
    Ok(LinearSystemOutcome::Solution(solution))
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ParityQuadraticSystem {
    pub rays: Vec<Ray>,
    pub unknowns: [&'static str; 6],
    pub status: LinearSystemOutcome,
}

/// The linear system `vᵀ R v = parity(v)·|v|²` for a symmetric `R` in the unknowns
/// `(r00, r11, r22, r01, r02, r12)`; inconsistent on [`PARITY_WITNESS_RAYS`].
pub fn parity_quadratic_system(rays: &[Ray]) -> Result<ParityQuadraticSystem, Error> {
    let mut rows = Vec::with_capacity(rays.len());
    let mut rhs = Vec::with_capacity(rays.len());
    for v in rays {
        let p = parity(v)?;
        let [a, b, c] = v.map(q);
        rows.push(vec![
            &a * &a,
            &b * &b,
            &c * &c,
            q(2) * &a * &b,
            q(2) * &a * &c,
            q(2) * &b * &c,
        ]);
        rhs.push(p * (&a * &a + &b * &b + &c * &c));
    }
    let status = solve_linear_system(&rows, &rhs)?;
    Ok(ParityQuadraticSystem {
        rays: rays.to_vec(),
        unknowns: ["r00", "r11", "r22", "r01", "r02", "r12"],
        status,
    })
}

/// Six rays whose parity values admit no quadratic form; the first five alone do.
pub const PARITY_WITNESS_RAYS: [Ray; 6] = [
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 1],
    [3, 4, 0],
    [0, 3, 4],
    [0, 4, 3],
];

#[cfg(test)]
mod tests {
    use super::*;
    use crate::linear_algebra::ordered::{
        is_positive_semidefinite as inertia_is_psd, quadratic_form as basic_quadratic_form,
    };
    use crate::linear_algebra::scalars::qr;

    fn fr(n: i64, d: i64) -> Q {
        qr(n, d).expect("nonzero fixture denominator")
    }

    fn mi(rows: &[&[i64]]) -> Matrix {
        rows.iter()
            .map(|r| r.iter().map(|&x| q(x)).collect())
            .collect()
    }

    fn vi(xs: &[i64]) -> Vector {
        xs.iter().map(|&x| q(x)).collect()
    }

    fn rho2() -> Matrix {
        vec![vec![fr(1, 2), fr(1, 4)], vec![fr(1, 4), fr(1, 2)]]
    }

    fn rho3() -> Matrix {
        vec![
            vec![fr(1, 2), q(0), fr(1, 4)],
            vec![q(0), fr(1, 4), q(0)],
            vec![fr(1, 4), q(0), fr(1, 4)],
        ]
    }

    fn effects2() -> Vec<Matrix> {
        vec![
            identity(2),
            scale(&fr(1, 2), &identity(2)),
            rank_one_effect(&vi(&[3, 4])).unwrap(),
            rank_one_effect(&vi(&[1, -1])).unwrap(),
            single(2, 0, 0).unwrap(),
            vec![vec![fr(1, 3), fr(1, 6)], vec![fr(1, 6), fr(1, 3)]],
        ]
    }

    fn effects3() -> Vec<Matrix> {
        vec![
            identity(3),
            rank_one_effect(&vi(&[1, 2, 2])).unwrap(),
            rank_one_effect(&vi(&[2, -2, 1])).unwrap(),
            single(3, 1, 1).unwrap(),
            scale(&fr(1, 3), &identity(3)),
        ]
    }

    // ------------------------------------------------------------------ Gram

    #[test]
    fn test_psd_decomposition_reconstructs() {
        for e in [
            rho2(),
            rho3(),
            identity(3),
            mi(&[&[0, 0], &[0, 1]]),
            mi(&[&[1, 1], &[1, 1]]),
        ] {
            let GramDecomposition::Psd { terms } = gram_decomposition(&e).unwrap() else {
                panic!("expected psd for {e:?}");
            };
            assert!(verify_gram(&e, &terms).unwrap());
            assert!(terms.iter().all(|(d, _)| d > &Q::zero()));
            assert!(matches!(
                psd_certificate(&e).unwrap(),
                PsdCertificate::Psd {
                    reconstructs: true,
                    ..
                }
            ));
        }
    }

    #[test]
    fn test_negative_witness_is_exact() {
        for e in [
            mi(&[&[1, 2], &[2, 1]]),
            mi(&[&[0, 1], &[1, 0]]),
            mi(&[&[-1, 0], &[0, 1]]),
            mi(&[&[1, 0, 0], &[0, 0, 2], &[0, 2, 1]]),
        ] {
            let GramDecomposition::NotPsd { witness } = gram_decomposition(&e).unwrap() else {
                panic!("expected not_psd for {e:?}");
            };
            assert!(quadratic_form(&e, &witness).unwrap() < Q::zero());
            let PsdCertificate::NotPsd { witness: w, value } = psd_certificate(&e).unwrap()
            else {
                panic!("expected a witness for {e:?}");
            };
            assert_eq!(w, witness);
            assert_eq!(value, quadratic_form(&e, &witness).unwrap());
            assert!(value < Q::zero());
        }
    }

    #[test]
    fn test_nonsymmetric_refused_and_symmetric_part_used() {
        assert_eq!(
            gram_decomposition(&mi(&[&[1, 2], &[0, 1]])),
            Err(BornEffectValuationError::NotSymmetric)
        );
        assert!(is_psd(&mi(&[&[1, 2], &[0, 1]])).unwrap());
        assert!(!is_psd(&mi(&[&[1, 4], &[0, 1]])).unwrap());
    }

    /// Two independent exact routes agree: the LDLᵀ-based `is_psd` and the pivoted
    /// congruence inertia of `ordered`; every witness replays on the `BasicMatrix` form.
    #[test]
    fn test_is_psd_agrees_with_congruence_inertia_and_witnesses_replay() {
        let samples = [
            rho2(),
            rho3(),
            identity(3),
            mi(&[&[0, 0], &[0, 1]]),
            mi(&[&[1, 1], &[1, 1]]),
            mi(&[&[1, 2], &[2, 1]]),
            mi(&[&[0, 1], &[1, 0]]),
            mi(&[&[-1, 0], &[0, 1]]),
            mi(&[&[1, 0, 0], &[0, 0, 2], &[0, 2, 1]]),
            mi(&[&[2, 0, 0], &[0, 0, 0], &[0, 0, -1]]),
            mi(&[&[1, 1], &[1, 0]]),
            mi(&[&[1, 2], &[0, 1]]),
            mi(&[&[1, 4], &[0, 1]]),
            mi(&[&[1, -1, 0, 0], &[-1, 2, -1, 0], &[0, -1, 2, -1], &[0, 0, -1, 1]]),
        ];
        let (mut psd_count, mut not_psd_count) = (0, 0);
        for e in samples {
            let sym = symmetric_part(&e).unwrap();
            let basic = to_basic(&sym).unwrap();
            assert_eq!(is_psd(&e).unwrap(), inertia_is_psd(&basic).unwrap(), "{e:?}");
            match psd_certificate(&e).unwrap() {
                PsdCertificate::Psd {
                    terms,
                    reconstructs,
                } => {
                    psd_count += 1;
                    assert!(reconstructs);
                    assert_eq!(verify_gram(&sym, &terms).unwrap(), true);
                }
                PsdCertificate::NotPsd { witness, value } => {
                    not_psd_count += 1;
                    assert_eq!(basic_quadratic_form(&basic, &witness).unwrap(), value);
                    assert!(value < Q::zero());
                }
            }
        }
        assert!(psd_count >= 5 && not_psd_count >= 5, "both branches exercised");
    }

    // ------------------------------------------------------------------ effects

    #[test]
    fn test_effects() {
        for e in effects2().into_iter().chain(effects3()) {
            assert!(is_effect(&e).unwrap(), "{e:?}");
            let c = effect_certificate(&e).unwrap();
            assert!(c.is_effect && c.lower.is_psd() && c.upper.is_psd());
        }
        assert!(!is_effect(&scale(&q(2), &identity(2))).unwrap());
        assert!(!is_effect(&mi(&[&[1, 1], &[1, 0]])).unwrap());
        let c = effect_certificate(&scale(&q(2), &identity(2))).unwrap();
        assert!(!c.is_effect && c.lower.is_psd() && !c.upper.is_psd());
    }

    #[test]
    fn test_rank_one_effect_is_projector() {
        let p = rank_one_effect(&vi(&[3, 4])).unwrap();
        assert_eq!(
            p,
            vec![vec![fr(9, 25), fr(12, 25)], vec![fr(12, 25), fr(16, 25)]]
        );
        assert_eq!(trace(&p), q(1));
    }

    #[test]
    fn test_order_unit_bound() {
        let a = mi(&[&[1, 2], &[3, -4]]);
        let k = order_unit_bound(&a).unwrap();
        assert_eq!(k, BigInt::from(10));
        let t = Q::from_integer(k);
        for x in [
            vi(&[1, 0]),
            vi(&[0, 1]),
            vi(&[1, 1]),
            vi(&[2, -3]),
            vec![fr(1, 3), fr(5, 7)],
        ] {
            assert!(bounded_by(&a, &t, &x).unwrap(), "{x:?}");
        }
        assert!(!bounded_by(&a, &q(1), &vi(&[0, 1])).unwrap());
    }

    // ------------------------------------------------------------------ extension

    #[test]
    fn test_extension_is_independent_of_bound_and_recovers_rho() {
        for (rho, n) in [(rho2(), 2usize), (rho3(), 3usize)] {
            let v = born_valuation(&rho).unwrap();
            let bounds = [q(1), q(2), q(5), fr(7, 2)];
            for a in [
                identity(n),
                single(n, 0, 1).unwrap(),
                sub(&single(n, 0, 0).unwrap(), &scale(&q(3), &identity(n))).unwrap(),
            ] {
                let c = extension_consistency(&v, &a, &bounds).unwrap();
                assert!(c.consistent, "{a:?}");
                assert_eq!(c.bounds, bounds.to_vec());
                assert_eq!(c.values.len(), 4);
                assert_eq!(
                    extend(&v, &a, None).unwrap(),
                    trace_mul(&rho, &a).unwrap()
                );
            }
            assert_eq!(representing_matrix(&v, n).unwrap(), rho);
        }
    }

    #[test]
    fn test_born_certificate() {
        for (rho, n, effs) in [(rho2(), 2usize, effects2()), (rho3(), 3usize, effects3())] {
            let v = born_valuation(&rho).unwrap();
            let c = born_certificate(&v, n, &effs).unwrap();
            assert!(c.symmetric && c.psd && c.agrees_on_effects);
            assert_eq!(c.trace, q(1));
            assert_eq!(c.effects_checked, effs.len());
            assert_eq!(c.rho, rho);
            assert!(c.psd_certificate.is_psd());
        }
    }

    #[test]
    fn test_born_valuation_satisfies_axioms() {
        let v = born_valuation(&rho2()).unwrap();
        let pairs = vec![
            (
                scale(&fr(1, 2), &identity(2)),
                scale(&fr(1, 2), &identity(2)),
            ),
            (
                rank_one_effect(&vi(&[3, 4])).unwrap(),
                rank_one_effect(&vi(&[4, -3])).unwrap(),
            ),
            (single(2, 0, 0).unwrap(), single(2, 1, 1).unwrap()),
        ];
        assert_eq!(
            valuation_axioms(&v, 2, &effects2(), &pairs).unwrap(),
            ValuationAxioms {
                unit: true,
                nonneg: true,
                additive: true
            }
        );
    }

    #[test]
    fn test_non_additive_control_has_inconsistent_extension() {
        let pairs = vec![(
            scale(&fr(1, 2), &identity(2)),
            scale(&fr(1, 2), &identity(2)),
        )];
        assert_eq!(
            valuation_axioms(&square_valuation, 2, &effects2(), &pairs).unwrap(),
            ValuationAxioms {
                unit: true,
                nonneg: true,
                additive: false
            }
        );
        let c = extension_consistency(&square_valuation, &identity(2), &[q(1), q(2)]).unwrap();
        assert!(!c.consistent);
        assert_eq!(c.values, vec![q(1), fr(1, 4)]);
    }

    #[test]
    fn test_non_positive_control_has_non_psd_representative() {
        let c = born_certificate(&bad_linear_valuation, 3, &[]).unwrap();
        assert_eq!(c.trace, q(1));
        assert!(!c.psd);
        assert!(c.symmetric);
        assert_eq!(c.rho, mi(&[&[2, 0, 0], &[0, 0, 0], &[0, 0, -1]]));
        assert_eq!(
            c.psd_certificate,
            PsdCertificate::NotPsd {
                witness: vi(&[0, 0, 1]),
                value: q(-1)
            }
        );
    }

    #[test]
    fn test_unit_cannot_be_dropped() {
        let rho = rho2();
        let v = |e: &Matrix| trace_mul(&rho, e).unwrap() * q(2);
        let c = born_certificate(&v, 2, &[]).unwrap();
        assert_ne!(c.trace, q(1));
        // Without the unit axiom the extension is bound-dependent: L(A) = 2·trace(ρ₂A) + t,
        // and each ρ_ij uses t = order_unit_bound(E_ji) + 1 = 2, so ρ = 2ρ₂ + 2J, trace 6.
        assert_eq!(c.trace, q(6));
        assert!(!extension_consistency(&v, &identity(2), &[q(1), q(2)])
            .unwrap()
            .consistent);
    }

    // ------------------------------------------------------------------ rational sphere

    #[test]
    fn test_rays_and_parity() {
        assert!(is_ray(&[3, 4, 0]) && is_ray(&[1, 2, 2]) && is_ray(&[0, 0, 1]));
        assert!(!is_ray(&[2, 0, 0]));
        assert!(!is_ray(&[1, 1, 0]));
        assert!(!is_ray(&[0, 0, 0]));
        assert_eq!(
            (
                parity(&[0, 4, 3]).unwrap(),
                parity(&[0, 3, 4]).unwrap(),
                parity(&[2, 2, 1]).unwrap()
            ),
            (q(1), q(0), q(1))
        );
        assert_eq!(parity(&[0, 4, -3]).unwrap(), q(1));
        assert_eq!(parity(&[2, 0, 0]), Err(BornEffectValuationError::NotARay));
    }

    #[test]
    fn test_parity_is_a_frame_function_on_all_orthogonal_triples_in_box() {
        let c = parity_frame_check(5).unwrap();
        assert!(c.all_sum_to_one);
        assert!(c.orthogonal_triples > 10);
        assert_eq!(c.values, vec![q(0), q(1)]);
        assert_eq!(c.box_size, 5);
        assert_eq!(c.rays, rays_in_box(5).len());
        assert!(c.rays > 0);
    }

    #[test]
    fn test_parity_has_no_quadratic_representative() {
        let c = parity_quadratic_system(&PARITY_WITNESS_RAYS).unwrap();
        assert_eq!(c.status, LinearSystemOutcome::Inconsistent);
        assert_eq!(c.rays, PARITY_WITNESS_RAYS.to_vec());
        assert_eq!(c.unknowns, ["r00", "r11", "r22", "r01", "r02", "r12"]);
        let five = parity_quadratic_system(&PARITY_WITNESS_RAYS[..5]).unwrap();
        let LinearSystemOutcome::Solution(solution) = five.status else {
            panic!("the first five rays admit a quadratic form");
        };
        // r00 = 0, r11 = 0, r22 = 1, r01 = 0, r02 free (0), r12 = -2/3
        assert_eq!(solution, vec![q(0), q(0), q(1), q(0), q(0), fr(-2, 3)]);
    }

    // ------------------------------------------------------------------ guards and fence

    #[test]
    fn test_exact_input_guards_are_typed_refusals() {
        use BornEffectValuationError as E;
        assert_eq!(matrix(&[]), Err(E::NonSquareMatrix));
        assert_eq!(matrix(&[vi(&[1, 2])]), Err(E::NonSquareMatrix));
        assert_eq!(
            matrix(&[vec![q(1), q(2)], vec![q(3)]]),
            Err(E::NonSquareMatrix)
        );
        assert_eq!(vector(&[]), Err(E::EmptyVector));
        assert_eq!(
            matrix(&[vec![Q::new_raw(BigInt::from(2), BigInt::from(4))]]),
            Err(E::InexactEntry(RationalConstructionError::NonReduced))
        );
        assert_eq!(rank_one_effect(&vi(&[0, 0])), Err(E::ZeroVector));
        assert_eq!(midpoint(&identity(2), &q(0)), Err(E::NonPositiveBound));
        assert_eq!(midpoint(&identity(2), &q(-1)), Err(E::NonPositiveBound));
        assert_eq!(
            single(2, 2, 0),
            Err(E::IndexOutOfRange {
                index: 2,
                dimension: 2
            })
        );
        assert_eq!(
            trace_mul(&identity(2), &identity(3)),
            Err(E::DimensionMismatch {
                operation: "trace_mul",
                expected: 2,
                got: 3
            })
        );
        let v = born_valuation(&rho2()).unwrap();
        assert_eq!(
            valuation_axioms(&v, 2, &[scale(&q(2), &identity(2))], &[]),
            Err(E::NotAnEffect)
        );
        assert_eq!(
            valuation_axioms(&v, 2, &[], &[(identity(2), identity(2))]),
            Err(E::NotAnEffect)
        );
        assert_eq!(
            born_certificate(&v, 2, &[identity(3)]),
            Err(E::DimensionMismatch {
                operation: "born_certificate",
                expected: 2,
                got: 3
            })
        );
        assert_eq!(parity_quadratic_system(&[[1, 1, 0]]), Err(E::NotARay));
        assert_eq!(solve_linear_system(&[], &[]), Err(E::EmptySystem));
        assert!(born_valuation(&Vec::new()).is_err());
        assert!(verify_gram(&identity(2), &[(q(1), vi(&[1, 0, 0]))]).is_err());
        assert!(!verify_gram(&identity(2), &[(q(-1), vi(&[1, 0]))]).unwrap());
        assert!(!verify_gram(&identity(2), &[(q(1), vi(&[1, 0]))]).unwrap());
    }

    #[test]
    fn test_authority_fence_and_provenance() {
        assert!(AUTHORITY_FENCE.contains("AuthorityEffect None"));
        assert!(AUTHORITY_FENCE.contains("no Gleason theorem"));
        assert!(PROVENANCE.contains("20261020T205000Z_effect_valuation_lean"));
        assert!(PROVENANCE.contains("code/python/src/qm/born_effect_valuation.py"));
        for module in [
            "BornEffectValuation",
            "BornLinearExtension",
            "BornMatrixCarrier",
            "BornTraceRepresentation",
            "BornPsdDecomposition",
            "BornRationalSphereObstruction",
        ] {
            assert!(PROVENANCE.contains(module), "{module}");
        }
    }
}
