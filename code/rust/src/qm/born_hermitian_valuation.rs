//! Exact effect-additive valuations on Gaussian-rational Hermitian matrices: the Born trace
//! form over `ℚ(i)` from effect additivity, not from Gleason.
//!
//! The Hermitian twin of [`super::born_effect_valuation`], replayed in exact arithmetic over
//! the Gaussian rationals for the carrier of
//! `dag/results/FQ-GAP-BORN-UNIQUENESS-GLEASON/runs/20261020T224000Z_gaussian_hermitian_carrier`,
//! mirroring, function for function, the Python twin
//! `code/python/src/qm/born_hermitian_valuation.py`:
//!
//! * Hermitian PSD certification by a Gram (`L D L*`) decomposition `E = Σ_k d_k w_k w_k*`
//!   with real pivots `d_k ≥ 0`, or an exact negative witness `x` with `x* E x < 0`, both
//!   read off the crate's [`hermitian_ldl`] (the crate's one Hermitian `L D L*`; the rational
//!   twin reads the symmetric [`ldlt`](crate::linear_algebra::ordered::ldlt) the same way);
//! * effects `0 ≤ E ≤ I` in the Hermitian-form preorder (unit = identity) and the rank-one
//!   effects `x x* / (x·x)`;
//! * the order-unit bound `⌈Σ(|re a_ij| + |im a_ij|)⌉` and the midpoint extension
//!   `L(A) = 2t·v((A + tI)/(2t)) − t` of a real-valued valuation `v` to a real-linear
//!   functional, with its consistency across bounds;
//! * the representing matrix `ρ_ji = L(E_ij) − i·L(i·E_ij)` with `re(trace(ρE)) = v(E)`,
//!   recovered one matrix unit at a time along the directions `1` and `i`, and the Born
//!   certificate (`ρ` Hermitian, PSD, real trace 1, agreeing with `v` on the supplied
//!   effects);
//! * three mutation controls: a non-additive valuation (its extension depends on the bound),
//!   a linear but non-positive valuation (its `ρ` is not PSD, with an exact witness), and a
//!   unital real-linear valuation that reads the skew-Hermitian direction `i·E_01` (its `ρ`
//!   is neither Hermitian nor PSD).
//!
//! The `*`-algebra and its order are supplied; only the form of the valuation is derived.
//! No Gleason theorem is proved. AuthorityEffect: None.
//!
//! Scalars: the crate's [`GaussianRational`] (canonical parts by construction, `Result`-valued
//! `Semiring`/`Ring`/`Involution` arithmetic). A refused scalar operation surfaces as the
//! typed `Scalar` error, a refused matrix operation as `LinearAlgebra`; nothing panics on
//! caller data.

use num_bigint::BigInt;
use num_traits::{Signed, Zero};

use crate::linear_algebra::basic_matrix::BasicMatrix;
use crate::linear_algebra::ordered::{hermitian_ldl, LdltOutcome};
use crate::linear_algebra::scalars::{
    validate_rational, Involution, RationalConstructionError, Ring, ScalarError, Semiring,
};
use crate::linear_algebra::{q, ExactFieldError, GaussianRational, Q};

pub const AUTHORITY_FENCE: &str = "AuthorityEffect None; not PROVED; no Gleason theorem is proved; \
     the matrix algebra and its order are supplied, only the form of the valuation is derived; \
     assumptions exposed.";

pub const PROVENANCE: &str = "Hermitian twin over the Gaussian rationals of the carrier of \
     dag/results/FQ-GAP-BORN-UNIQUENESS-GLEASON/runs/20261020T224000Z_gaussian_hermitian_carrier; \
     mirrors the Python twin code/python/src/qm/born_hermitian_valuation.py and the rational \
     module code/rust/src/qm/born_effect_valuation.rs.";

// ============================================================================
// Types and errors
// ============================================================================

/// A Gaussian-rational matrix as rows; every public entry point re-admits it through
/// [`matrix`].
pub type Matrix = Vec<Vec<GaussianRational>>;
/// A Gaussian-rational vector; every public entry point re-admits it through [`vector`].
pub type Vector = Vec<GaussianRational>;
/// A real-valued valuation on Gaussian-rational matrices, refusing (never panicking on) a
/// matrix outside its domain. The Born valuation [`born_valuation`] and the three controls
/// [`square_valuation`], [`bad_linear_valuation`] and [`imaginary_leak_valuation`] all have
/// this shape; an imaginary value is unrepresentable by type.
pub type Valuation<'a> = &'a dyn Fn(&Matrix) -> Result<Q, BornHermitianValuationError>;
/// An owned valuation; `&v` passes as a [`Valuation`].
pub type BoxedValuation = Box<dyn Fn(&Matrix) -> Result<Q, BornHermitianValuationError>>;

#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum BornHermitianValuationError {
    #[error("nonempty square matrix required")]
    NonSquareMatrix,
    #[error("nonempty vector required")]
    EmptyVector,
    #[error("exact canonical rational parts required: {0}")]
    InexactEntry(#[from] RationalConstructionError),
    #[error("{operation}: dimension {expected} expected, got {got}")]
    DimensionMismatch {
        operation: &'static str,
        expected: usize,
        got: usize,
    },
    #[error("{operation}: dimension at least {minimum} required, got {got}")]
    DimensionTooSmall {
        operation: &'static str,
        minimum: usize,
        got: usize,
    },
    #[error("index {index} is outside dimension {dimension}")]
    IndexOutOfRange { index: usize, dimension: usize },
    #[error("hermitian matrix required")]
    NotHermitian,
    #[error("nonzero vector required")]
    ZeroVector,
    #[error("positive bound required")]
    NonPositiveBound,
    #[error("effects and effect pairs with effect sums required")]
    NotAnEffect,
    #[error("scalar arithmetic refused: {0}")]
    Scalar(#[from] ScalarError),
    #[error("linear algebra: {0}")]
    LinearAlgebra(#[from] ExactFieldError),
}

type Error = BornHermitianValuationError;

// ============================================================================
// Scalars, exact-input admission and the *-algebra (supplied, not derived)
// ============================================================================

fn g_zero() -> GaussianRational {
    GaussianRational::from_integers(0, 0)
}

fn g_one() -> GaussianRational {
    GaussianRational::from_integers(1, 0)
}

/// The imaginary unit.
fn g_i() -> GaussianRational {
    GaussianRational::from_integers(0, 1)
}

/// `x + 0·i`; refuses a non-canonical `x`.
pub fn from_real(x: &Q) -> Result<GaussianRational, Error> {
    Ok(GaussianRational::new(x.clone(), q(0))?)
}

/// Admit a nonempty square matrix of Gaussian rationals.
pub fn matrix(rows: &[Vec<GaussianRational>]) -> Result<Matrix, Error> {
    let n = rows.len();
    if n == 0 || rows.iter().any(|r| r.len() != n) {
        return Err(Error::NonSquareMatrix);
    }
    for x in rows.iter().flatten() {
        x.validate()?;
    }
    Ok(rows.to_vec())
}

/// Admit a nonempty vector of Gaussian rationals.
pub fn vector(xs: &[GaussianRational]) -> Result<Vector, Error> {
    if xs.is_empty() {
        return Err(Error::EmptyVector);
    }
    for x in xs {
        x.validate()?;
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
    Q::new(BigInt::from(1), BigInt::from(2))
}

fn zeros(n: usize) -> Matrix {
    vec![vec![g_zero(); n]; n]
}

pub fn identity(n: usize) -> Matrix {
    (0..n)
        .map(|i| {
            (0..n)
                .map(|j| if i == j { g_one() } else { g_zero() })
                .collect()
        })
        .collect()
}

/// `c·E_ij`, the matrix unit of dimension `n` scaled by `c` (the twin's `single(n,i,j,c)`).
pub fn single(n: usize, i: usize, j: usize, c: &GaussianRational) -> Result<Matrix, Error> {
    for index in [i, j] {
        if index >= n {
            return Err(Error::IndexOutOfRange {
                index,
                dimension: n,
            });
        }
    }
    c.validate()?;
    Ok((0..n)
        .map(|r| {
            (0..n)
                .map(|k| if r == i && k == j { c.clone() } else { g_zero() })
                .collect()
        })
        .collect())
}

/// Entrywise `op` on two matrices already known to share a shape.
fn entrywise(
    a: &Matrix,
    b: &Matrix,
    op: impl Fn(&GaussianRational, &GaussianRational) -> Result<GaussianRational, ScalarError>,
) -> Result<Matrix, Error> {
    a.iter()
        .zip(b)
        .map(|(ra, rb)| {
            ra.iter()
                .zip(rb)
                .map(|(x, y)| op(x, y).map_err(Error::from))
                .collect::<Result<Vector, Error>>()
        })
        .collect()
}

pub fn add(a: &Matrix, b: &Matrix) -> Result<Matrix, Error> {
    same_shape("add", a, b)?;
    entrywise(a, b, |x, y| x.try_add(y))
}

pub fn sub(a: &Matrix, b: &Matrix) -> Result<Matrix, Error> {
    same_shape("sub", a, b)?;
    entrywise(a, b, |x, y| x.try_sub(y))
}

/// `c·A`.
pub fn scale(c: &GaussianRational, a: &Matrix) -> Result<Matrix, Error> {
    a.iter()
        .map(|r| {
            r.iter()
                .map(|x| c.try_mul(x).map_err(Error::from))
                .collect::<Result<Vector, Error>>()
        })
        .collect()
}

/// `A*`, the conjugate transpose of an admitted square matrix.
pub fn adjoint(a: &Matrix) -> Result<Matrix, Error> {
    let cols = a.iter().map(Vec::len).min().unwrap_or(0);
    (0..cols)
        .map(|j| {
            a.iter()
                .map(|r| r[j].try_conj().map_err(Error::from))
                .collect::<Result<Vector, Error>>()
        })
        .collect()
}

/// `Σ r_i x_i`, bilinear.
fn dot(r: &[GaussianRational], x: &[GaussianRational]) -> Result<GaussianRational, Error> {
    let mut acc = g_zero();
    for (p, v) in r.iter().zip(x) {
        acc = acc.try_add(&p.try_mul(v)?)?;
    }
    Ok(acc)
}

pub fn mat_vec(a: &Matrix, x: &[GaussianRational]) -> Result<Vector, Error> {
    a.iter()
        .map(|r| {
            same_length("mat_vec", r.len(), x.len())?;
            dot(r, x)
        })
        .collect()
}

/// `Σ conj(x_i) y_i`, conjugate-linear in the first slot.
pub fn inner(x: &[GaussianRational], y: &[GaussianRational]) -> Result<GaussianRational, Error> {
    same_length("inner", x.len(), y.len())?;
    let mut acc = g_zero();
    for (a, b) in x.iter().zip(y) {
        acc = acc.try_add(&a.try_conj()?.try_mul(b)?)?;
    }
    Ok(acc)
}

/// `x y*`, with entries `x_i conj(y_j)`.
pub fn outer(x: &[GaussianRational], y: &[GaussianRational]) -> Result<Matrix, Error> {
    let mut out = Vec::with_capacity(x.len());
    for a in x {
        let mut row = Vec::with_capacity(y.len());
        for b in y {
            row.push(a.try_mul(&b.try_conj()?)?);
        }
        out.push(row);
    }
    Ok(out)
}

pub fn trace(a: &Matrix) -> Result<GaussianRational, Error> {
    let mut acc = g_zero();
    for (i, r) in a.iter().enumerate() {
        if let Some(x) = r.get(i) {
            acc = acc.try_add(x)?;
        }
    }
    Ok(acc)
}

/// `trace(A B) = Σ_ij A_ij B_ji`; both matrices must be `n × n`.
pub fn trace_mul(a: &Matrix, b: &Matrix) -> Result<GaussianRational, Error> {
    let n = a.len();
    same_length("trace_mul", n, b.len())?;
    for r in a.iter().chain(b) {
        same_length("trace_mul", n, r.len())?;
    }
    let mut acc = g_zero();
    for i in 0..n {
        for j in 0..n {
            acc = acc.try_add(&a[i][j].try_mul(&b[j][i])?)?;
        }
    }
    Ok(acc)
}

/// `x* A x = Σ conj(x_i) (A x)_i`.
pub fn hermitian_form(a: &Matrix, x: &[GaussianRational]) -> Result<GaussianRational, Error> {
    inner(x, &mat_vec(a, x)?)
}

/// `re(x* A x)`, the Hermitian form of the Hermitian part of `A`.
pub fn re_hermitian_form(a: &Matrix, x: &[GaussianRational]) -> Result<Q, Error> {
    Ok(hermitian_form(a, x)?.real().clone())
}

/// `A == A*`.
pub fn is_hermitian(a: &Matrix) -> bool {
    adjoint(a).is_ok_and(|adj| adj == *a)
}

/// `(A + A*)/2`.
pub fn hermitian_part(a: &Matrix) -> Result<Matrix, Error> {
    scale(&from_real(&half())?, &add(a, &adjoint(a)?)?)
}

// ============================================================================
// Hermitian PSD certification: Gram (L D L*) terms or an exact negative witness
// ============================================================================

/// The outcome of [`gram_decomposition`].
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum GramDecomposition {
    /// `E = Σ_k d_k w_k w_k*` with every real `d_k > 0` (zero pivots contribute no term).
    Psd { terms: Vec<(Q, Vector)> },
    /// `witness* E witness < 0`.
    NotPsd { witness: Vector },
}

fn to_basic(e: &Matrix) -> Result<BasicMatrix<GaussianRational>, Error> {
    let n = e.len();
    let data: Vec<GaussianRational> = e.iter().flatten().cloned().collect();
    Ok(BasicMatrix::from_row_major(n, n, data).map_err(ExactFieldError::from)?)
}

/// Gram terms `(d_k, w_k)` with `E == Σ d_k w_k w_k*` and real `d_k ≥ 0`, or a witness `x`
/// with `x* E x < 0`. Refuses a non-Hermitian matrix. The terms are read off the crate's exact
/// [`hermitian_ldl`]: `d_k` is the `k`-th (real) pivot and `w_k` the `k`-th column of the unit
/// lower factor; a zero pivot with a zero Schur column contributes no term.
///
/// Witnesses. A negative pivot `d_p < 0` is witnessed by the solution `x` of `L* x = e_p`,
/// with `x* E x = d_p`, exactly as the Python twin. A zero pivot whose Schur column has a
/// nonzero entry `c` in row `j` (Schur diagonal `m`) is witnessed by the crate's solution of
/// `L* x = −(m+1)/(2c)·e_p + e_j`, whose form is exactly `−1`; the twin instead lifts
/// `e_p − t·c·e_j` (`t = 1` for `m ≤ 0`, else `1/m`) with form `|c|²·t·(t·m − 2)`. Both are
/// exact negative directions; the tests pin the crate's vectors and replay the twin's.
pub fn gram_decomposition(e: &Matrix) -> Result<GramDecomposition, Error> {
    let e = matrix(e)?;
    if !is_hermitian(&e) {
        return Err(Error::NotHermitian);
    }
    let n = e.len();
    let factor = hermitian_ldl(&to_basic(&e)?)?;
    match factor.outcome() {
        LdltOutcome::PositiveSemidefinite => {
            let lower = factor.unit_lower();
            let mut terms = Vec::new();
            for (k, pivot) in factor.pivots().iter().enumerate() {
                if pivot.try_is_zero()? {
                    continue;
                }
                let mut w = Vec::with_capacity(n);
                for i in 0..n {
                    w.push(lower.get(i, k).map_err(ExactFieldError::from)?);
                }
                terms.push((pivot.real().clone(), w));
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

/// `true` when every `d_k ≥ 0` and `Σ d_k w_k w_k* == E` exactly; a witness of the wrong
/// length is refused.
pub fn verify_gram(e: &Matrix, terms: &[(Q, Vector)]) -> Result<bool, Error> {
    let e = matrix(e)?;
    let n = e.len();
    let mut s = zeros(n);
    for (d, w) in terms {
        validate_rational(d)?;
        let w = vector(w)?;
        same_length("verify_gram", n, w.len())?;
        if d < &q(0) {
            return Ok(false);
        }
        s = add(&s, &scale(&from_real(d)?, &outer(&w, &w)?)?)?;
    }
    Ok(s == e)
}

/// The replayable PSD certificate of a (not necessarily Hermitian) matrix, decided on its
/// Hermitian part; the witness value is `re(x* E x)` on the matrix itself.
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
    let h = hermitian_part(&e)?;
    match gram_decomposition(&h)? {
        GramDecomposition::Psd { terms } => {
            let reconstructs = verify_gram(&h, &terms)?;
            Ok(PsdCertificate::Psd {
                terms,
                reconstructs,
            })
        }
        GramDecomposition::NotPsd { witness } => {
            let value = re_hermitian_form(&e, &witness)?;
            Ok(PsdCertificate::NotPsd { witness, value })
        }
    }
}

pub fn is_psd(e: &Matrix) -> Result<bool, Error> {
    Ok(matches!(
        gram_decomposition(&hermitian_part(&matrix(e)?)?)?,
        GramDecomposition::Psd { .. }
    ))
}

/// `0 ≤ E ≤ I` in the Hermitian-form preorder.
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
    let lower = psd_certificate(&e)?;
    let upper = psd_certificate(&sub(&identity(e.len()), &e)?)?;
    Ok(EffectCertificate {
        is_effect: lower.is_psd() && upper.is_psd(),
        lower,
        upper,
    })
}

/// `x x* / (x·x)`, the projector onto the ray of `x`.
pub fn rank_one_effect(x: &[GaussianRational]) -> Result<Matrix, Error> {
    let x = vector(x)?;
    let nrm = inner(&x, &x)?.real().clone();
    if nrm.is_zero() {
        return Err(Error::ZeroVector);
    }
    scale(&from_real(&nrm.recip())?, &outer(&x, &x)?)
}

// ============================================================================
// Order unit, midpoint extension, representing matrix, Born certificate
// ============================================================================

/// `⌈Σ(|re a_ij| + |im a_ij|)⌉`, a `t` with `−t·I ≤ A ≤ t·I`.
pub fn order_unit_bound(a: &Matrix) -> Result<BigInt, Error> {
    let a = matrix(a)?;
    let total = a
        .iter()
        .flatten()
        .fold(q(0), |acc, x| acc + x.real().abs() + x.imag().abs());
    Ok(total.ceil().to_integer())
}

/// `−t·(x·x) ≤ re(x* A x) ≤ t·(x·x)`.
pub fn bounded_by(a: &Matrix, t: &Q, x: &[GaussianRational]) -> Result<bool, Error> {
    let a = matrix(a)?;
    validate_rational(t)?;
    let x = vector(x)?;
    let form = re_hermitian_form(&a, &x)?;
    let s = t * inner(&x, &x)?.real();
    Ok(-s.clone() <= form && form <= s)
}

/// `(A + t·I)/(2t)`, an effect whenever `−t·I ≤ A ≤ t·I`; refuses `t ≤ 0`.
pub fn midpoint(a: &Matrix, t: &Q) -> Result<Matrix, Error> {
    let a = matrix(a)?;
    validate_rational(t)?;
    if t <= &q(0) {
        return Err(Error::NonPositiveBound);
    }
    let two_t = t + t;
    scale(
        &from_real(&two_t.recip())?,
        &add(&a, &scale(&from_real(t)?, &identity(a.len()))?)?,
    )
}

fn evaluate(valuation: Valuation<'_>, e: &Matrix) -> Result<Q, Error> {
    let value = valuation(e)?;
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
        None => Q::from_integer(order_unit_bound(&a)? + BigInt::from(1)),
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

/// `ρ_ji = L(E_ij) − i·L(i·E_ij)` with `L` the midpoint extension, so that
/// `re(trace(ρ A)) = L(A)` for a real-linear `L`.
pub fn representing_matrix(valuation: Valuation<'_>, n: usize) -> Result<Matrix, Error> {
    let mut rho = Vec::with_capacity(n);
    for j in 0..n {
        let mut row = Vec::with_capacity(n);
        for i in 0..n {
            let along_one = extend(valuation, &single(n, i, j, &g_one())?, None)?;
            let along_i = extend(valuation, &single(n, i, j, &g_i())?, None)?;
            row.push(GaussianRational::new(along_one, -along_i)?);
        }
        rho.push(row);
    }
    Ok(rho)
}

/// The Born valuation `E ↦ re(trace(ρ E))`; a matrix not of `ρ`'s dimension is refused as
/// `DimensionMismatch`.
pub fn born_valuation(rho: &Matrix) -> Result<BoxedValuation, Error> {
    let rho = matrix(rho)?;
    Ok(Box::new(move |e: &Matrix| {
        Ok(trace_mul(&rho, &matrix(e)?)?.real().clone())
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
    let unit = evaluate(valuation, &identity(n))? == q(1);
    let mut nonneg = true;
    for e in &effects {
        if evaluate(valuation, e)? < q(0) {
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
    pub hermitian: bool,
    pub trace: GaussianRational,
    pub trace_real: bool,
    pub psd: bool,
    pub psd_certificate: PsdCertificate,
    pub agrees_on_effects: bool,
    pub effects_checked: usize,
}

/// The representing matrix of `valuation` in dimension `n` with its exact PSD certificate,
/// trace (and whether it is real), Hermiticity, and agreement `re(trace(ρE)) = v(E)` on the
/// supplied effects.
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
        if trace_mul(&rho, e)?.real() != &evaluate(valuation, e)? {
            agrees_on_effects = false;
            break;
        }
    }
    let tr = trace(&rho)?;
    Ok(BornCertificate {
        hermitian: is_hermitian(&rho),
        trace_real: tr.imag().is_zero(),
        trace: tr,
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

/// Control: `E ↦ re(E_00)²`, unit and nonnegative but not additive. Refuses an empty or
/// non-square matrix.
pub fn square_valuation(e: &Matrix) -> Result<Q, Error> {
    let e = matrix(e)?;
    Ok(e[0][0].real() * e[0][0].real())
}

/// Control: `E ↦ 2·re(E_00) − re(E_22)`, real-linear with unit value 1 but not positive.
/// Refuses a matrix that is not `3 × 3` (the three-dimensional control).
pub fn bad_linear_valuation(e: &Matrix) -> Result<Q, Error> {
    let e = matrix(e)?;
    same_length("bad_linear_valuation", 3, e.len())?;
    Ok(q(2) * e[0][0].real() - e[2][2].real())
}

/// Control: `E ↦ re(E_00) + im(E_01)`, unital and real-linear, but it reads the
/// skew-Hermitian direction `i·E_01`: its representing matrix is neither Hermitian nor PSD.
/// Refuses a matrix smaller than `2 × 2`.
pub fn imaginary_leak_valuation(e: &Matrix) -> Result<Q, Error> {
    let e = matrix(e)?;
    if e.len() < 2 {
        return Err(Error::DimensionTooSmall {
            operation: "imaginary_leak_valuation",
            minimum: 2,
            got: e.len(),
        });
    }
    Ok(e[0][0].real() + e[0][1].imag())
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::linear_algebra::ordered::hermitian_is_positive_semidefinite;
    use crate::linear_algebra::scalars::{qr, Field};

    fn fr(n: i64, d: i64) -> Q {
        qr(n, d).expect("nonzero fixture denominator")
    }

    /// `re + im·i` from integer parts.
    fn gi(re: i64, im: i64) -> GaussianRational {
        GaussianRational::from_integers(re, im)
    }

    /// `(a/b) + (c/d)·i`.
    fn gf(a: i64, b: i64, c: i64, d: i64) -> GaussianRational {
        GaussianRational::new(fr(a, b), fr(c, d)).expect("canonical fixture parts")
    }

    /// `x + 0·i` for a canonical fixture rational.
    fn re(x: &Q) -> GaussianRational {
        from_real(x).expect("canonical fixture rational")
    }

    fn mi(rows: &[&[(i64, i64)]]) -> Matrix {
        rows.iter()
            .map(|r| r.iter().map(|&(re, im)| gi(re, im)).collect())
            .collect()
    }

    fn vi(xs: &[(i64, i64)]) -> Vector {
        xs.iter().map(|&(re, im)| gi(re, im)).collect()
    }

    fn unit(n: usize, i: usize, j: usize) -> Matrix {
        single(n, i, j, &gi(1, 0)).unwrap()
    }

    fn scaled(c: &GaussianRational, a: &Matrix) -> Matrix {
        scale(c, a).unwrap()
    }

    fn mat_mul(a: &Matrix, b: &Matrix) -> Matrix {
        let n = a.len();
        (0..n)
            .map(|i| {
                (0..n)
                    .map(|j| {
                        let mut acc = gi(0, 0);
                        for k in 0..n {
                            acc = acc.try_add(&a[i][k].try_mul(&b[k][j]).unwrap()).unwrap();
                        }
                        acc
                    })
                    .collect()
            })
            .collect()
    }

    /// RHO2 = [[1/2, 1/4−1/4i], [1/4+1/4i, 1/2]].
    fn rho2() -> Matrix {
        vec![
            vec![gf(1, 2, 0, 1), gf(1, 4, -1, 4)],
            vec![gf(1, 4, 1, 4), gf(1, 2, 0, 1)],
        ]
    }

    /// RHO3 = [[1/2, 0, 1/4i], [0, 1/4, 0], [−1/4i, 0, 1/4]].
    fn rho3() -> Matrix {
        vec![
            vec![gf(1, 2, 0, 1), gi(0, 0), gf(0, 1, 1, 4)],
            vec![gi(0, 0), gf(1, 4, 0, 1), gi(0, 0)],
            vec![gf(0, 1, -1, 4), gi(0, 0), gf(1, 4, 0, 1)],
        ]
    }

    /// HERM2 = [[1/3, 1/6+1/6i], [1/6−1/6i, 1/3]].
    fn herm2() -> Matrix {
        vec![
            vec![gf(1, 3, 0, 1), gf(1, 6, 1, 6)],
            vec![gf(1, 6, -1, 6), gf(1, 3, 0, 1)],
        ]
    }

    /// SKEW2 = [[1/2, 1/4i], [0, 1/2]], an effect that is not Hermitian.
    fn skew2() -> Matrix {
        vec![
            vec![gf(1, 2, 0, 1), gf(0, 1, 1, 4)],
            vec![gi(0, 0), gf(1, 2, 0, 1)],
        ]
    }

    fn effects2() -> Vec<Matrix> {
        vec![
            identity(2),
            scaled(&re(&fr(1, 2)), &identity(2)),
            rank_one_effect(&vi(&[(3, 0), (0, 4)])).unwrap(),
            rank_one_effect(&vi(&[(1, 1), (1, 0)])).unwrap(),
            unit(2, 0, 0),
            herm2(),
            skew2(),
        ]
    }

    fn effects3() -> Vec<Matrix> {
        vec![
            identity(3),
            rank_one_effect(&vi(&[(1, 0), (0, 2), (2, 0)])).unwrap(),
            rank_one_effect(&vi(&[(2, 0), (-2, 0), (0, 1)])).unwrap(),
            rank_one_effect(&vi(&[(1, 1), (1, -1), (0, 0)])).unwrap(),
            unit(3, 1, 1),
            scaled(&re(&fr(1, 3)), &identity(3)),
        ]
    }

    /// Deterministic Gaussian rationals with numerators in `[-5, 5]` and denominators in
    /// `[1, 4]` (the twin's distribution; a different pseudo-random stream).
    fn random_matrices(n: usize, count: usize, seed: u64) -> Vec<Matrix> {
        let mut state = seed.wrapping_mul(6_364_136_223_846_793_005).wrapping_add(1);
        let mut next = |lo: i64, hi: i64| -> i64 {
            state = state
                .wrapping_mul(6_364_136_223_846_793_005)
                .wrapping_add(1_442_695_040_888_963_407);
            let span = (hi - lo + 1) as u64;
            lo + ((state >> 33) % span) as i64
        };
        (0..count)
            .map(|_| {
                (0..n)
                    .map(|_| {
                        (0..n)
                            .map(|_| {
                                let re = fr(next(-5, 5), next(1, 4));
                                let im = fr(next(-5, 5), next(1, 4));
                                GaussianRational::new(re, im).expect("canonical parts")
                            })
                            .collect()
                    })
                    .collect()
            })
            .collect()
    }

    // ------------------------------------------------------------------ Gaussian scalars

    /// The crate scalar's exact arithmetic on the twin's fixtures (the twin's `repr` has no
    /// counterpart: the crate scalar prints through `Debug`).
    #[test]
    fn test_gaussian_arithmetic() {
        let a = gf(3, 5, 4, 5);
        let i = gi(0, 1);
        assert_eq!(i.try_mul(&i).unwrap(), gi(-1, 0));
        assert_eq!(a.try_mul(&a.try_conj().unwrap()).unwrap(), gi(1, 0));
        assert_eq!(a.norm_sq(), q(1));
        assert_eq!(gi(1, 2).try_div(&gi(3, 4)).unwrap(), gf(11, 25, 2, 25));
        assert_eq!(gi(1, 0).try_div(&i).unwrap(), gi(0, -1));
        assert_eq!(gi(2, 0).try_sub(&i).unwrap(), gi(2, -1));
        assert_eq!(i.try_mul(&re(&fr(1, 2))).unwrap(), gf(0, 1, 1, 2));
        let sum = [i.clone(), gi(1, 0), i.clone()]
            .iter()
            .fold(gi(0, 0), |acc, x| acc.try_add(x).unwrap());
        assert_eq!(sum, gi(1, 2));
        assert!(gi(0, 0).try_is_zero().unwrap() && !i.try_is_zero().unwrap());
        assert!(gi(2, 0).imag().is_zero() && !i.imag().is_zero());
        assert_ne!(i, gi(1, 0));
        assert_eq!(
            gi(1, 0).try_div(&gi(0, 0)),
            Err(ScalarError::DivisionByZero)
        );
        assert_eq!(from_real(&fr(1, 2)).unwrap(), gf(1, 2, 0, 1));
        assert_eq!(
            from_real(&Q::new_raw(BigInt::from(2), BigInt::from(4))),
            Err(BornHermitianValuationError::InexactEntry(
                RationalConstructionError::NonReduced
            ))
        );
    }

    #[test]
    fn test_matrix_helpers() {
        let a = mi(&[&[(1, 0), (2, 3)], &[(0, -1), (4, 0)]]);
        assert_eq!(
            adjoint(&a).unwrap(),
            mi(&[&[(1, 0), (0, 1)], &[(2, -3), (4, 0)]])
        );
        assert!(!is_hermitian(&a));
        assert!(is_hermitian(&hermitian_part(&a).unwrap()));
        assert!(is_hermitian(&rho2()) && is_hermitian(&rho3()));
        assert_eq!(
            inner(&vi(&[(1, 0), (0, 1)]), &vi(&[(0, 1), (1, 0)])).unwrap(),
            gi(0, 0)
        );
        assert_eq!(inner(&vi(&[(0, 1)]), &vi(&[(0, 1)])).unwrap(), gi(1, 0));
        assert_eq!(
            outer(&vi(&[(1, 0), (0, 1)]), &vi(&[(1, 0), (0, 1)])).unwrap(),
            mi(&[&[(1, 0), (0, -1)], &[(0, 1), (1, 0)]])
        );
        assert_eq!(trace(&rho2()).unwrap(), gi(1, 0));
        assert_eq!(
            trace_mul(&rho2(), &unit(2, 0, 1)).unwrap(),
            gf(1, 4, 1, 4)
        );
        assert_eq!(
            hermitian_form(&a, &vi(&[(1, 0), (0, 1)])).unwrap(),
            gi(1, 2)
        );
        assert_eq!(re_hermitian_form(&a, &vi(&[(1, 0), (0, 1)])).unwrap(), q(1));
        assert_eq!(
            single(2, 0, 1, &gi(0, 1)).unwrap(),
            mi(&[&[(0, 0), (0, 1)], &[(0, 0), (0, 0)]])
        );
        assert_eq!(sub(&identity(2), &identity(2)).unwrap(), zeros(2));
    }

    // ------------------------------------------------------------------ Gram

    #[test]
    fn test_psd_decomposition_reconstructs() {
        for e in [
            rho2(),
            rho3(),
            herm2(),
            identity(3),
            mi(&[&[(0, 0), (0, 0)], &[(0, 0), (1, 0)]]),
            mi(&[&[(1, 0), (0, 1)], &[(0, -1), (1, 0)]]),
            mi(&[&[(2, 0), (1, 1)], &[(1, -1), (1, 0)]]),
        ] {
            let GramDecomposition::Psd { terms } = gram_decomposition(&e).unwrap() else {
                panic!("expected psd for {e:?}");
            };
            assert!(verify_gram(&e, &terms).unwrap());
            assert!(terms.iter().all(|(d, _)| d >= &q(0)));
        }
        assert_eq!(
            psd_certificate(&rho2()).unwrap(),
            PsdCertificate::Psd {
                terms: vec![
                    (fr(1, 2), vec![gi(1, 0), gf(1, 2, 1, 2)]),
                    (fr(1, 4), vec![gi(0, 0), gi(1, 0)]),
                ],
                reconstructs: true,
            }
        );
    }

    /// Negative-pivot witnesses coincide with the Python twin's table (the lifted unit
    /// vectors). Zero-pivot witnesses are the crate's `x·e_p + e_j` with `x = −(m+1)/(2c)`
    /// and form exactly `−1`, where the twin lifts `e_p − t·c·e_j` (form `|c|²·t·(t·m − 2)`):
    /// the crate's vector and value are pinned exactly, the twin's replays as a second
    /// negative direction.
    #[test]
    fn test_negative_witness_is_exact() {
        // (matrix, crate witness, its form value, twin witness, its form value)
        let cases: Vec<(Matrix, Vector, GaussianRational, Vector, GaussianRational)> = vec![
            (
                mi(&[&[(0, 0), (1, 0)], &[(1, 0), (0, 0)]]),
                vec![gf(-1, 2, 0, 1), gi(1, 0)],
                gi(-1, 0),
                vi(&[(1, 0), (-1, 0)]),
                gi(-2, 0),
            ),
            (
                mi(&[&[(0, 0), (0, 1)], &[(0, -1), (0, 0)]]),
                vec![gf(0, 1, -1, 2), gi(1, 0)],
                gi(-1, 0),
                vi(&[(1, 0), (0, 1)]),
                gi(-2, 0),
            ),
            (
                mi(&[&[(0, 0), (1, 1)], &[(1, -1), (2, 0)]]),
                vec![gf(-3, 4, -3, 4), gi(1, 0)],
                gi(-1, 0),
                vec![gi(1, 0), gf(-1, 2, 1, 2)],
                gi(-1, 0),
            ),
            (
                mi(&[
                    &[(1, 0), (0, 0), (0, 0)],
                    &[(0, 0), (0, 0), (0, 2)],
                    &[(0, 0), (0, -2), (1, 0)],
                ]),
                vec![gi(0, 0), gf(0, 1, -1, 2), gi(1, 0)],
                gi(-1, 0),
                vi(&[(0, 0), (1, 0), (0, 2)]),
                gi(-4, 0),
            ),
            (
                mi(&[&[(1, 0), (0, 2)], &[(0, -2), (1, 0)]]),
                vi(&[(0, -2), (1, 0)]),
                gi(-3, 0),
                vi(&[(0, -2), (1, 0)]),
                gi(-3, 0),
            ),
            (
                mi(&[&[(-1, 0), (0, 0)], &[(0, 0), (1, 0)]]),
                vi(&[(1, 0), (0, 0)]),
                gi(-1, 0),
                vi(&[(1, 0), (0, 0)]),
                gi(-1, 0),
            ),
            (
                mi(&[&[(1, 0), (1, -1)], &[(1, 1), (1, 0)]]),
                vi(&[(-1, 1), (1, 0)]),
                gi(-1, 0),
                vi(&[(-1, 1), (1, 0)]),
                gi(-1, 0),
            ),
        ];
        for (e, x, value, twin, twin_value) in cases {
            let GramDecomposition::NotPsd { witness } = gram_decomposition(&e).unwrap() else {
                panic!("expected not_psd for {e:?}");
            };
            assert_eq!(witness, vector(&x).unwrap());
            assert_eq!(hermitian_form(&e, &witness).unwrap(), value);
            assert!(value.imag().is_zero() && value.real() < &q(0));
            assert_eq!(hermitian_form(&e, &twin).unwrap(), twin_value);
            assert!(twin_value.imag().is_zero() && twin_value.real() < &q(0));
            let PsdCertificate::NotPsd { witness: w, value: v } = psd_certificate(&e).unwrap()
            else {
                panic!("expected a witness for {e:?}");
            };
            assert_eq!(w, witness);
            assert_eq!(&v, value.real());
        }
    }

    /// Zero pivot with off-diagonal `c` and lower diagonal `m` (`E = [[0, c̄], [c, m]]`): the
    /// crate's witness is `[x, 1]` with `x = −(m+1)/(2c)` and form exactly `−1`; the twin's
    /// `[1, −t·c]` (`t = 1` for `m ≤ 0`, else `1/m`) has form `|c|²·t·(t·m − 2) < 0` and
    /// replays as a second negative direction.
    #[test]
    fn test_zero_pivot_witness_formula() {
        for (c, mm) in [
            (gi(1, 1), q(0)),
            (gi(1, 1), q(2)),
            (gi(0, -3), q(-1)),
            (gf(2, 3, -1, 5), fr(7, 3)),
        ] {
            let e = vec![
                vec![gi(0, 0), c.try_conj().unwrap()],
                vec![c.clone(), re(&mm)],
            ];
            let GramDecomposition::NotPsd { witness } = gram_decomposition(&e).unwrap() else {
                panic!("expected not_psd for {e:?}");
            };
            let x = re(&-(&mm + q(1)))
                .try_div(&gi(2, 0).try_mul(&c).unwrap())
                .unwrap();
            assert_eq!(witness, vec![x, gi(1, 0)]);
            assert_eq!(hermitian_form(&e, &witness).unwrap(), gi(-1, 0));
            let t = if mm <= q(0) { q(1) } else { mm.recip() };
            let twin = vec![gi(1, 0), c.try_mul(&re(&t)).unwrap().try_neg().unwrap()];
            let expected = c.norm_sq() * &t * (&t * &mm - q(2));
            assert!(expected < q(0));
            assert_eq!(hermitian_form(&e, &twin).unwrap(), re(&expected));
        }
    }

    #[test]
    fn test_nonhermitian_refused_and_hermitian_part_used() {
        use BornHermitianValuationError as E;
        assert_eq!(
            gram_decomposition(&mi(&[&[(1, 0), (0, 2)], &[(0, 0), (1, 0)]])),
            Err(E::NotHermitian)
        );
        assert_eq!(
            gram_decomposition(&mi(&[&[(1, 0), (0, 1)], &[(0, 1), (1, 0)]])),
            Err(E::NotHermitian)
        );
        assert!(is_psd(&mi(&[&[(1, 0), (0, 2)], &[(0, 0), (1, 0)]])).unwrap());
        assert!(!is_psd(&mi(&[&[(1, 0), (0, 4)], &[(0, 0), (1, 0)]])).unwrap());
        assert_eq!(
            psd_certificate(&mi(&[&[(1, 0), (0, 4)], &[(0, 0), (1, 0)]])).unwrap(),
            PsdCertificate::NotPsd {
                witness: vi(&[(0, -2), (1, 0)]),
                value: q(-3),
            }
        );
    }

    /// Two exact routes of the crate agree: the Gram route through the unpivoted
    /// `hermitian_ldl` and the pivoted Hermitian congruence inertia; every witness replays.
    #[test]
    fn test_is_psd_agrees_with_hermitian_inertia_and_witnesses_replay() {
        let samples = [
            rho2(),
            rho3(),
            herm2(),
            skew2(),
            identity(3),
            mi(&[&[(0, 0), (0, 0)], &[(0, 0), (1, 0)]]),
            mi(&[&[(1, 0), (0, 1)], &[(0, -1), (1, 0)]]),
            mi(&[&[(2, 0), (1, 1)], &[(1, -1), (1, 0)]]),
            mi(&[&[(0, 0), (1, 0)], &[(1, 0), (0, 0)]]),
            mi(&[&[(0, 0), (1, 1)], &[(1, -1), (2, 0)]]),
            mi(&[&[(1, 0), (0, 2)], &[(0, -2), (1, 0)]]),
            mi(&[&[(-1, 0), (0, 0)], &[(0, 0), (1, 0)]]),
            mi(&[&[(1, 0), (0, 2)], &[(0, 0), (1, 0)]]),
            mi(&[&[(1, 0), (0, 4)], &[(0, 0), (1, 0)]]),
            mi(&[
                &[(1, 0), (0, 0), (0, 0)],
                &[(0, 0), (0, 0), (0, 2)],
                &[(0, 0), (0, -2), (1, 0)],
            ]),
            mi(&[&[(1, 0), (0, 1)], &[(0, -1), (0, 0)]]),
        ];
        let (mut psd_count, mut not_psd_count) = (0, 0);
        for e in samples {
            let h = hermitian_part(&e).unwrap();
            assert_eq!(
                is_psd(&e).unwrap(),
                hermitian_is_positive_semidefinite(&to_basic(&h).unwrap()).unwrap(),
                "{e:?}"
            );
            match psd_certificate(&e).unwrap() {
                PsdCertificate::Psd {
                    terms,
                    reconstructs,
                } => {
                    psd_count += 1;
                    assert!(reconstructs);
                    assert!(verify_gram(&h, &terms).unwrap());
                }
                PsdCertificate::NotPsd { witness, value } => {
                    not_psd_count += 1;
                    assert_eq!(re_hermitian_form(&e, &witness).unwrap(), value);
                    assert_eq!(hermitian_form(&h, &witness).unwrap(), re(&value));
                    assert!(value < q(0));
                }
            }
        }
        assert!(psd_count >= 6 && not_psd_count >= 6, "both branches exercised");
    }

    // ------------------------------------------------------------------ effects

    #[test]
    fn test_effects() {
        for e in effects2().into_iter().chain(effects3()) {
            assert!(is_effect(&e).unwrap(), "{e:?}");
        }
        assert!(!is_effect(&scaled(&gi(2, 0), &identity(2))).unwrap());
        assert!(!is_effect(&mi(&[&[(1, 0), (0, 1)], &[(0, -1), (0, 0)]])).unwrap());
        assert!(!is_effect(&mi(&[&[(1, 0), (0, 1)], &[(0, -1), (1, 0)]])).unwrap());
    }

    #[test]
    fn test_rank_one_effect_is_projector() {
        let cases = [
            (
                vi(&[(3, 0), (0, 4)]),
                vec![
                    vec![gf(9, 25, 0, 1), gf(0, 1, -12, 25)],
                    vec![gf(0, 1, 12, 25), gf(16, 25, 0, 1)],
                ],
            ),
            (
                vi(&[(1, 1), (1, 0)]),
                vec![
                    vec![gf(2, 3, 0, 1), gf(1, 3, 1, 3)],
                    vec![gf(1, 3, -1, 3), gf(1, 3, 0, 1)],
                ],
            ),
        ];
        for (x, p) in cases {
            let e = rank_one_effect(&x).unwrap();
            assert_eq!(e, p);
            assert_eq!(trace(&e).unwrap(), gi(1, 0));
            assert!(is_hermitian(&e));
            assert_eq!(mat_mul(&e, &e), e);
        }
    }

    #[test]
    fn test_order_unit_bound() {
        let a = mi(&[&[(1, 0), (0, 2)], &[(3, -1), (-4, 0)]]);
        let k = order_unit_bound(&a).unwrap();
        assert_eq!(k, BigInt::from(11));
        let t = Q::from_integer(k);
        for x in [
            vi(&[(1, 0), (0, 0)]),
            vi(&[(0, 0), (1, 0)]),
            vi(&[(1, 0), (0, 1)]),
            vi(&[(2, -3), (1, 0)]),
            vec![gf(1, 3, 0, 1), gf(0, 1, 5, 7)],
        ] {
            assert!(bounded_by(&a, &t, &x).unwrap(), "{x:?}");
        }
        assert!(!bounded_by(&a, &fr(1, 10), &vi(&[(0, 0), (1, 0)])).unwrap());
    }

    // ------------------------------------------------------------------ extension

    #[test]
    fn test_extension_is_independent_of_bound_and_recovers_rho() {
        for (rho, n) in [(rho2(), 2usize), (rho3(), 3usize)] {
            let v = born_valuation(&rho).unwrap();
            let bounds = [q(1), q(2), q(5), fr(7, 2)];
            for a in [
                identity(n),
                unit(n, 0, 1),
                single(n, 0, 1, &gi(0, 1)).unwrap(),
                sub(&unit(n, 0, 0), &scaled(&gi(3, 1), &identity(n))).unwrap(),
            ] {
                let c = extension_consistency(&v, &a, &bounds).unwrap();
                assert!(c.consistent, "{a:?}");
                assert_eq!(c.bounds, bounds.to_vec());
                assert_eq!(c.values.len(), 4);
                assert_eq!(
                    extend(&v, &a, None).unwrap(),
                    trace_mul(&rho, &a).unwrap().real().clone()
                );
            }
            assert_eq!(representing_matrix(&v, n).unwrap(), rho);
        }
    }

    #[test]
    fn test_representing_matrix_reproduces_extension_on_random_matrices() {
        let born2 = born_valuation(&rho2()).unwrap();
        let born3 = born_valuation(&rho3()).unwrap();
        let cases: [(Valuation<'_>, usize); 4] = [
            (&born2, 2),
            (&imaginary_leak_valuation, 2),
            (&born3, 3),
            (&bad_linear_valuation, 3),
        ];
        for (v, n) in cases {
            let rho = representing_matrix(v, n).unwrap();
            for a in random_matrices(n, 6, n as u64) {
                assert_eq!(
                    extend(v, &a, None).unwrap(),
                    trace_mul(&rho, &a).unwrap().real().clone()
                );
                assert_eq!(extend(v, &a, None).unwrap(), v(&a).unwrap());
            }
        }
    }

    #[test]
    fn test_born_certificate() {
        for (rho, n, effs) in [(rho2(), 2usize, effects2()), (rho3(), 3usize, effects3())] {
            let v = born_valuation(&rho).unwrap();
            let c = born_certificate(&v, n, &effs).unwrap();
            assert!(c.hermitian && c.trace_real && c.psd && c.agrees_on_effects);
            assert!(matches!(
                c.psd_certificate,
                PsdCertificate::Psd {
                    reconstructs: true,
                    ..
                }
            ));
            assert_eq!(c.trace, gi(1, 0));
            assert_eq!(c.effects_checked, effs.len());
            assert_eq!(c.rho, rho);
        }
    }

    #[test]
    fn test_born_valuation_satisfies_axioms() {
        let v = born_valuation(&rho2()).unwrap();
        let pairs = vec![
            (
                scaled(&re(&fr(1, 2)), &identity(2)),
                scaled(&re(&fr(1, 2)), &identity(2)),
            ),
            (
                rank_one_effect(&vi(&[(3, 0), (0, 4)])).unwrap(),
                rank_one_effect(&vi(&[(0, 4), (3, 0)])).unwrap(),
            ),
            (
                rank_one_effect(&vi(&[(1, 1), (1, 0)])).unwrap(),
                rank_one_effect(&vi(&[(1, 0), (-1, 1)])).unwrap(),
            ),
            (unit(2, 0, 0), unit(2, 1, 1)),
        ];
        for (e, f) in &pairs[1..] {
            assert_eq!(add(e, f).unwrap(), identity(2));
        }
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
    fn test_born_valuation_is_blind_to_the_skew_part() {
        let v = born_valuation(&rho2()).unwrap();
        let h = hermitian_part(&skew2()).unwrap();
        assert!(!is_hermitian(&skew2()));
        assert!(is_effect(&skew2()).unwrap() && is_effect(&h).unwrap());
        assert_eq!(v(&skew2()).unwrap(), v(&h).unwrap());
        assert_eq!(v(&skew2()).unwrap(), fr(7, 16));
        assert_ne!(
            imaginary_leak_valuation(&skew2()).unwrap(),
            imaginary_leak_valuation(&h).unwrap()
        );
        assert_eq!(
            (
                imaginary_leak_valuation(&skew2()).unwrap(),
                imaginary_leak_valuation(&h).unwrap()
            ),
            (fr(3, 4), fr(5, 8))
        );
    }

    #[test]
    fn test_non_additive_control_has_inconsistent_extension() {
        let pairs = vec![(
            scaled(&re(&fr(1, 2)), &identity(2)),
            scaled(&re(&fr(1, 2)), &identity(2)),
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
        assert_eq!(c.trace, gi(1, 0));
        assert!(c.trace_real && c.hermitian && !c.psd);
        assert_eq!(
            c.rho,
            mi(&[
                &[(2, 0), (0, 0), (0, 0)],
                &[(0, 0), (0, 0), (0, 0)],
                &[(0, 0), (0, 0), (-1, 0)],
            ])
        );
        assert_eq!(
            c.psd_certificate,
            PsdCertificate::NotPsd {
                witness: vi(&[(0, 0), (0, 0), (1, 0)]),
                value: q(-1)
            }
        );
    }

    #[test]
    fn test_imaginary_leak_control_is_unital_additive_but_not_hermitian_nor_psd() {
        let v: Valuation<'_> = &imaginary_leak_valuation;
        let c = born_certificate(v, 2, &effects2()).unwrap();
        assert_eq!(c.rho, mi(&[&[(1, 0), (0, 0)], &[(0, -1), (0, 0)]]));
        assert!(!c.hermitian);
        assert_eq!(c.trace, gi(1, 0));
        assert!(c.trace_real);
        assert!(!c.psd);
        assert!(c.agrees_on_effects);
        assert_eq!(c.effects_checked, effects2().len());
        assert_eq!(
            c.psd_certificate,
            PsdCertificate::NotPsd {
                witness: vec![gf(0, 1, -1, 2), gi(1, 0)],
                value: fr(-1, 4)
            }
        );
        assert_eq!(
            hermitian_part(&representing_matrix(v, 2).unwrap()).unwrap(),
            vec![
                vec![gi(1, 0), gf(0, 1, 1, 2)],
                vec![gf(0, 1, -1, 2), gi(0, 0)],
            ]
        );
        let pairs = vec![
            (
                scaled(&re(&fr(1, 2)), &identity(2)),
                scaled(&re(&fr(1, 2)), &identity(2)),
            ),
            (
                rank_one_effect(&vi(&[(3, 0), (0, 4)])).unwrap(),
                rank_one_effect(&vi(&[(0, 4), (3, 0)])).unwrap(),
            ),
        ];
        assert_eq!(
            valuation_axioms(v, 2, &effects2(), &pairs).unwrap(),
            ValuationAxioms {
                unit: true,
                nonneg: false,
                additive: true
            }
        );
        let witness = rank_one_effect(&[gf(0, 1, -1, 2), gi(1, 0)]).unwrap();
        assert!(is_effect(&witness).unwrap());
        assert_eq!(v(&witness).unwrap(), fr(-1, 5));
        assert_eq!(
            v(&rank_one_effect(&vi(&[(3, 0), (0, 4)])).unwrap()).unwrap(),
            fr(-3, 25)
        );
    }

    #[test]
    fn test_unit_cannot_be_dropped() {
        let rho = rho2();
        let v = |e: &Matrix| -> Result<Q, BornHermitianValuationError> {
            Ok(trace_mul(&rho, &matrix(e)?)?.real() * q(2))
        };
        let c = born_certificate(&v, 2, &[]).unwrap();
        assert_ne!(c.trace, gi(1, 0));
        // Without the unit axiom the extension is bound-dependent: L(A) = 2·re(trace(ρ₂A)) + t,
        // and each unit direction uses t = order_unit_bound + 1 = 2, so
        // ρ_ji = (2·re ρ_ji + 2) − i·(−2·im ρ_ji + 2) = 2ρ_ji + 2 − 2i and trace ρ = 6 − 4i.
        assert_eq!(c.trace, gi(6, -4));
        assert!(!c.trace_real);
        assert!(!extension_consistency(&v, &identity(2), &[q(1), q(2)])
            .unwrap()
            .consistent);
    }

    #[test]
    fn test_effect_certificate_is_consistent_with_its_parts() {
        for e in [
            identity(2),
            scaled(&gi(2, 0), &identity(2)),
            mi(&[&[(1, 0), (0, 1)], &[(0, -1), (0, 0)]]),
            rank_one_effect(&vi(&[(3, 0), (0, 4)])).unwrap(),
            skew2(),
            herm2(),
        ] {
            let c = effect_certificate(&e).unwrap();
            assert_eq!(c.is_effect, c.lower.is_psd() && c.upper.is_psd());
            assert_eq!(c.is_effect, is_effect(&e).unwrap());
        }
    }

    // ------------------------------------------------------------------ guards and fence

    /// The twin's `test_shape_mismatches_are_refused_not_truncated` and
    /// `test_inexact_inputs_refused`, as typed refusals.
    #[test]
    fn test_shape_mismatches_and_inexact_inputs_are_typed_refusals() {
        use BornHermitianValuationError as E;
        let v = born_valuation(&rho2()).unwrap();
        assert_eq!(
            born_certificate(&v, 2, &[identity(3)]),
            Err(E::DimensionMismatch {
                operation: "born_certificate",
                expected: 2,
                got: 3
            })
        );
        assert!(matches!(
            valuation_axioms(&v, 2, &[identity(3)], &[]),
            Err(E::DimensionMismatch { .. })
        ));
        assert!(matches!(
            valuation_axioms(&v, 2, &[], &[(identity(2), identity(3))]),
            Err(E::DimensionMismatch { .. })
        ));
        assert_eq!(
            v(&identity(3)),
            Err(E::DimensionMismatch {
                operation: "trace_mul",
                expected: 2,
                got: 3
            })
        );
        assert_eq!(
            verify_gram(
                &mi(&[&[(1, 0), (0, 0)], &[(0, 0), (0, 0)]]),
                &[(q(1), vi(&[(1, 0), (0, 0), (5, 0)]))]
            ),
            Err(E::DimensionMismatch {
                operation: "verify_gram",
                expected: 2,
                got: 3
            })
        );
        assert!(matches!(
            bounded_by(
                &mi(&[&[(1, 0), (0, 0)], &[(0, 0), (100, 0)]]),
                &q(1),
                &vi(&[(1, 0)])
            ),
            Err(E::DimensionMismatch { .. })
        ));
        assert!(matches!(
            trace_mul(&identity(2), &identity(3)),
            Err(E::DimensionMismatch { .. })
        ));
        assert!(matches!(
            add(&identity(2), &identity(3)),
            Err(E::DimensionMismatch { .. })
        ));
        assert!(matches!(
            sub(&identity(2), &mi(&[&[(1, 0), (2, 0), (3, 0)]])),
            Err(E::DimensionMismatch { .. })
        ));
        assert!(matches!(
            inner(&vi(&[(1, 0), (2, 0)]), &vi(&[(1, 0)])),
            Err(E::DimensionMismatch { .. })
        ));
        assert!(matches!(
            mat_vec(&identity(2), &vi(&[(1, 0)])),
            Err(E::DimensionMismatch { .. })
        ));
        assert_eq!(
            single(2, 2, 0, &gi(1, 0)),
            Err(E::IndexOutOfRange {
                index: 2,
                dimension: 2
            })
        );
        assert_eq!(
            matrix(&[vi(&[(1, 0), (2, 0)]), vi(&[(3, 0)])]),
            Err(E::NonSquareMatrix)
        );
        assert_eq!(matrix(&[]), Err(E::NonSquareMatrix));
        assert_eq!(matrix(&[vi(&[(1, 0), (2, 0)])]), Err(E::NonSquareMatrix));
        assert_eq!(vector(&[]), Err(E::EmptyVector));
        assert_eq!(rank_one_effect(&vi(&[(0, 0), (0, 0)])), Err(E::ZeroVector));
        assert_eq!(midpoint(&identity(2), &q(0)), Err(E::NonPositiveBound));
        assert_eq!(midpoint(&identity(2), &q(-1)), Err(E::NonPositiveBound));
        assert_eq!(
            bad_linear_valuation(&identity(2)),
            Err(E::DimensionMismatch {
                operation: "bad_linear_valuation",
                expected: 3,
                got: 2
            })
        );
        assert_eq!(
            imaginary_leak_valuation(&identity(1)),
            Err(E::DimensionTooSmall {
                operation: "imaginary_leak_valuation",
                minimum: 2,
                got: 1
            })
        );
        // The twin's `extend(lambda E: I, ...)` refusal: an imaginary value is unrepresentable
        // by type here, so the admission guard on the valuation's value is exercised with a
        // non-canonical rational instead.
        let raw_valued = |_: &Matrix| -> Result<Q, E> {
            Ok(Q::new_raw(BigInt::from(2), BigInt::from(4)))
        };
        assert_eq!(
            extend(&raw_valued, &identity(2), None),
            Err(E::InexactEntry(RationalConstructionError::NonReduced))
        );
        // The twin's non-canonical matrix entries are unconstructible here: the crate scalar
        // refuses them at construction, and every rational parameter is re-admitted.
        let raw = Q::new_raw(BigInt::from(2), BigInt::from(4));
        assert_eq!(
            GaussianRational::new(raw.clone(), q(0)),
            Err(RationalConstructionError::NonReduced)
        );
        assert_eq!(
            GaussianRational::new(q(0), Q::new_raw(BigInt::from(1), BigInt::from(-2))),
            Err(RationalConstructionError::NegativeDenominator)
        );
        assert_eq!(
            midpoint(&identity(2), &raw),
            Err(E::InexactEntry(RationalConstructionError::NonReduced))
        );
        assert_eq!(
            bounded_by(&identity(2), &raw, &vi(&[(1, 0), (0, 0)])),
            Err(E::InexactEntry(RationalConstructionError::NonReduced))
        );
        assert_eq!(
            verify_gram(&identity(2), &[(raw.clone(), vi(&[(1, 0), (0, 0)]))]),
            Err(E::InexactEntry(RationalConstructionError::NonReduced))
        );
        assert_eq!(
            extend(&v, &identity(2), Some(&raw)),
            Err(E::InexactEntry(RationalConstructionError::NonReduced))
        );
        assert_eq!(
            valuation_axioms(&v, 2, &[scaled(&gi(2, 0), &identity(2))], &[]),
            Err(E::NotAnEffect)
        );
        assert_eq!(
            valuation_axioms(&v, 2, &[], &[(identity(2), identity(2))]),
            Err(E::NotAnEffect)
        );
        assert!(born_valuation(&Vec::new()).is_err());
        assert!(!verify_gram(&identity(2), &[(q(-1), vi(&[(1, 0), (0, 0)]))]).unwrap());
        assert!(!verify_gram(&identity(2), &[(q(1), vi(&[(1, 0), (0, 0)]))]).unwrap());
    }

    /// A valuation applied outside its domain is a typed refusal, never a panic, through
    /// every public consumer that forwards a caller-chosen dimension.
    #[test]
    fn test_valuations_refuse_wrong_dimensions_without_panicking() {
        use BornHermitianValuationError as E;
        let v = born_valuation(&rho2()).unwrap();
        assert!(matches!(
            born_certificate(&v, 3, &[]),
            Err(E::DimensionMismatch { .. })
        ));
        assert!(matches!(
            born_certificate(&v, 1, &[]),
            Err(E::DimensionMismatch { .. })
        ));
        assert!(matches!(
            representing_matrix(&v, 3),
            Err(E::DimensionMismatch { .. })
        ));
        assert!(matches!(
            extend(&v, &identity(3), None),
            Err(E::DimensionMismatch { .. })
        ));
        assert!(matches!(
            extension_consistency(&v, &identity(3), &[q(1)]),
            Err(E::DimensionMismatch { .. })
        ));
        assert!(matches!(
            valuation_axioms(&v, 3, &[], &[]),
            Err(E::DimensionMismatch { .. })
        ));
        assert_eq!(square_valuation(&Vec::new()), Err(E::NonSquareMatrix));
        assert_eq!(
            square_valuation(&vec![vi(&[(1, 0), (2, 0)])]),
            Err(E::NonSquareMatrix)
        );
        assert_eq!(
            square_valuation(&scaled(&re(&fr(1, 2)), &identity(2))),
            Ok(fr(1, 4))
        );
        assert_eq!(bad_linear_valuation(&Vec::new()), Err(E::NonSquareMatrix));
        assert_eq!(bad_linear_valuation(&identity(3)), Ok(q(1)));
        assert_eq!(imaginary_leak_valuation(&Vec::new()), Err(E::NonSquareMatrix));
        assert_eq!(imaginary_leak_valuation(&identity(3)), Ok(q(1)));
        assert!(matches!(
            born_certificate(&bad_linear_valuation, 2, &[]),
            Err(E::DimensionMismatch { .. })
        ));
        assert!(matches!(
            born_certificate(&imaginary_leak_valuation, 1, &[]),
            Err(E::DimensionTooSmall { .. })
        ));
        assert_eq!(
            born_certificate(&square_valuation, 0, &[]).map(|c| c.rho),
            Err(E::NonSquareMatrix)
        );
        assert_eq!(
            gram_decomposition(&Vec::new()),
            Err(E::NonSquareMatrix)
        );
        assert_eq!(hermitian_part(&Vec::new()), Ok(Vec::new()));
    }

    #[test]
    fn test_authority_fence_and_provenance() {
        assert!(AUTHORITY_FENCE.contains("AuthorityEffect None"));
        assert!(AUTHORITY_FENCE.contains("no Gleason theorem"));
        assert!(AUTHORITY_FENCE.contains("only the form of the valuation is derived"));
        assert!(PROVENANCE.contains(
            "dag/results/FQ-GAP-BORN-UNIQUENESS-GLEASON/runs/20261020T224000Z_gaussian_hermitian_carrier"
        ));
        assert!(PROVENANCE.contains("code/python/src/qm/born_hermitian_valuation.py"));
    }
}
