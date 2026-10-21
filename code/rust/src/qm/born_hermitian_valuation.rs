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
//!   with real pivots `d_k ≥ 0`, or an exact negative witness `x` with `x* E x < 0` lifted
//!   through the conjugate unit lower factor;
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
//! Scalars: the module carries its own plain-operator Gaussian rational [`Gq`] (public
//! canonical-`Q` parts, admitted at every public entry point exactly as the twin admits raw
//! `Q` entries), with lossless conversions to and from the crate's
//! [`GaussianRational`], whose `Result`-valued trait arithmetic would otherwise obscure the
//! Hermitian elimination. The two agree on products, conjugates, norms and inverses (tested).

use std::fmt;
use std::ops::{Add, Mul, Neg, Sub};

use num_bigint::BigInt;
use num_traits::{One, Signed, Zero};

use crate::linear_algebra::scalars::{validate_rational, RationalConstructionError};
use crate::linear_algebra::{q, GaussianRational, Q};

pub const AUTHORITY_FENCE: &str = "AuthorityEffect None; not PROVED; no Gleason theorem is proved; \
     the matrix algebra and its order are supplied, only the form of the valuation is derived; \
     assumptions exposed.";

pub const PROVENANCE: &str = "Hermitian twin over the Gaussian rationals of the carrier of \
     dag/results/FQ-GAP-BORN-UNIQUENESS-GLEASON/runs/20261020T224000Z_gaussian_hermitian_carrier; \
     mirrors the Python twin code/python/src/qm/born_hermitian_valuation.py and the rational \
     module code/rust/src/qm/born_effect_valuation.rs.";

// ============================================================================
// Gaussian rationals with plain operators
// ============================================================================

/// A Gaussian rational `re + im·i` with exact rational parts. The parts are raw `Q` values
/// exactly as the rational twin's matrix entries are; every public matrix or vector entry
/// point re-admits them through [`matrix`] / [`vector`] (`InexactEntry` on a non-canonical
/// part).
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Gq {
    pub re: Q,
    pub im: Q,
}

impl Gq {
    pub fn new(re: Q, im: Q) -> Self {
        Self { re, im }
    }

    /// The real Gaussian rational `re + 0·i`.
    pub fn real(re: Q) -> Self {
        Self {
            re,
            im: Q::zero(),
        }
    }

    pub fn from_integers(re: i64, im: i64) -> Self {
        Self {
            re: q(re),
            im: q(im),
        }
    }

    pub fn zero() -> Self {
        Self::from_integers(0, 0)
    }

    pub fn one() -> Self {
        Self::from_integers(1, 0)
    }

    /// The imaginary unit.
    pub fn i() -> Self {
        Self::from_integers(0, 1)
    }

    pub fn conj(&self) -> Self {
        Self {
            re: self.re.clone(),
            im: -&self.im,
        }
    }

    /// `re² + im²`.
    pub fn norm_sq(&self) -> Q {
        &self.re * &self.re + &self.im * &self.im
    }

    pub fn is_zero(&self) -> bool {
        self.re.is_zero() && self.im.is_zero()
    }

    pub fn is_real(&self) -> bool {
        self.im.is_zero()
    }

    /// `self / rhs = self · conj(rhs) / |rhs|²`; refuses a zero divisor.
    pub fn try_div(&self, rhs: &Gq) -> Result<Gq, BornHermitianValuationError> {
        let n = rhs.norm_sq();
        if n.is_zero() {
            return Err(BornHermitianValuationError::DivisionByZero);
        }
        Ok(&(self * &rhs.conj()) * &n.recip())
    }
}

macro_rules! gq_binop {
    ($trait:ident, $method:ident, |$a:ident, $b:ident| $body:expr) => {
        impl $trait<&Gq> for &Gq {
            type Output = Gq;
            fn $method(self, rhs: &Gq) -> Gq {
                let ($a, $b) = (self, rhs);
                $body
            }
        }
        impl $trait<Gq> for &Gq {
            type Output = Gq;
            fn $method(self, rhs: Gq) -> Gq {
                self.$method(&rhs)
            }
        }
        impl $trait<&Gq> for Gq {
            type Output = Gq;
            fn $method(self, rhs: &Gq) -> Gq {
                (&self).$method(rhs)
            }
        }
        impl $trait for Gq {
            type Output = Gq;
            fn $method(self, rhs: Gq) -> Gq {
                (&self).$method(&rhs)
            }
        }
    };
}

gq_binop!(Add, add, |a, b| Gq {
    re: &a.re + &b.re,
    im: &a.im + &b.im,
});
gq_binop!(Sub, sub, |a, b| Gq {
    re: &a.re - &b.re,
    im: &a.im - &b.im,
});
gq_binop!(Mul, mul, |a, b| Gq {
    re: &a.re * &b.re - &a.im * &b.im,
    im: &a.re * &b.im + &a.im * &b.re,
});

/// Scaling by a rational.
impl Mul<&Q> for &Gq {
    type Output = Gq;
    fn mul(self, rhs: &Q) -> Gq {
        Gq {
            re: &self.re * rhs,
            im: &self.im * rhs,
        }
    }
}

impl Neg for &Gq {
    type Output = Gq;
    fn neg(self) -> Gq {
        Gq {
            re: -&self.re,
            im: -&self.im,
        }
    }
}

impl Neg for Gq {
    type Output = Gq;
    fn neg(self) -> Gq {
        -&self
    }
}

/// `re`, `im i`, or `re±|im|i`, as the Python twin's `repr`.
impl fmt::Display for Gq {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        if self.im.is_zero() {
            write!(f, "{}", self.re)
        } else if self.re.is_zero() {
            write!(f, "{}i", self.im)
        } else {
            let sign = if self.im.is_positive() { "+" } else { "-" };
            write!(f, "{}{}{}i", self.re, sign, self.im.abs())
        }
    }
}

impl From<&GaussianRational> for Gq {
    fn from(g: &GaussianRational) -> Self {
        Self::new(g.real().clone(), g.imag().clone())
    }
}

impl From<GaussianRational> for Gq {
    fn from(g: GaussianRational) -> Self {
        Self::from(&g)
    }
}

/// The crate scalar admits only canonical parts, so the conversion is fallible on a raw
/// non-canonical part (and lossless otherwise).
impl TryFrom<&Gq> for GaussianRational {
    type Error = RationalConstructionError;
    fn try_from(g: &Gq) -> Result<Self, Self::Error> {
        GaussianRational::new(g.re.clone(), g.im.clone())
    }
}

impl TryFrom<Gq> for GaussianRational {
    type Error = RationalConstructionError;
    fn try_from(g: Gq) -> Result<Self, Self::Error> {
        Self::try_from(&g)
    }
}

// ============================================================================
// Types and errors
// ============================================================================

/// A Gaussian-rational matrix as rows; every public entry point re-admits it through
/// [`matrix`].
pub type Matrix = Vec<Vec<Gq>>;
/// A Gaussian-rational vector; every public entry point re-admits it through [`vector`].
pub type Vector = Vec<Gq>;
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
    #[error("division by zero Gaussian rational")]
    DivisionByZero,
}

type Error = BornHermitianValuationError;

// ============================================================================
// Exact-input admission and the *-algebra (supplied, not derived)
// ============================================================================

fn validate_gq(x: &Gq) -> Result<(), Error> {
    validate_rational(&x.re)?;
    validate_rational(&x.im)?;
    Ok(())
}

/// Admit a nonempty square matrix of canonical Gaussian rationals.
pub fn matrix(rows: &[Vec<Gq>]) -> Result<Matrix, Error> {
    let n = rows.len();
    if n == 0 || rows.iter().any(|r| r.len() != n) {
        return Err(Error::NonSquareMatrix);
    }
    for x in rows.iter().flatten() {
        validate_gq(x)?;
    }
    Ok(rows.to_vec())
}

/// Admit a nonempty vector of canonical Gaussian rationals.
pub fn vector(xs: &[Gq]) -> Result<Vector, Error> {
    if xs.is_empty() {
        return Err(Error::EmptyVector);
    }
    for x in xs {
        validate_gq(x)?;
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

fn zeros(n: usize) -> Matrix {
    vec![vec![Gq::zero(); n]; n]
}

fn unit_vector(n: usize, p: usize) -> Vector {
    (0..n)
        .map(|i| if i == p { Gq::one() } else { Gq::zero() })
        .collect()
}

pub fn identity(n: usize) -> Matrix {
    (0..n)
        .map(|i| {
            (0..n)
                .map(|j| if i == j { Gq::one() } else { Gq::zero() })
                .collect()
        })
        .collect()
}

/// `c·E_ij`, the matrix unit of dimension `n` scaled by `c` (the twin's `single(n,i,j,c)`).
pub fn single(n: usize, i: usize, j: usize, c: &Gq) -> Result<Matrix, Error> {
    for index in [i, j] {
        if index >= n {
            return Err(Error::IndexOutOfRange {
                index,
                dimension: n,
            });
        }
    }
    validate_gq(c)?;
    Ok((0..n)
        .map(|r| {
            (0..n)
                .map(|k| if r == i && k == j { c.clone() } else { Gq::zero() })
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

pub fn scale(c: &Gq, a: &Matrix) -> Matrix {
    a.iter()
        .map(|r| r.iter().map(|x| c * x).collect())
        .collect()
}

/// `A*`, the conjugate transpose of an admitted square matrix.
pub fn adjoint(a: &Matrix) -> Matrix {
    let cols = a.iter().map(Vec::len).min().unwrap_or(0);
    (0..cols)
        .map(|j| a.iter().map(|r| r[j].conj()).collect())
        .collect()
}

pub fn mat_vec(a: &Matrix, x: &[Gq]) -> Result<Vector, Error> {
    a.iter()
        .map(|r| {
            same_length("mat_vec", r.len(), x.len())?;
            Ok(r.iter().zip(x).fold(Gq::zero(), |acc, (p, v)| acc + p * v))
        })
        .collect()
}

/// `Σ conj(x_i) y_i`, conjugate-linear in the first slot.
pub fn inner(x: &[Gq], y: &[Gq]) -> Result<Gq, Error> {
    same_length("inner", x.len(), y.len())?;
    Ok(x.iter()
        .zip(y)
        .fold(Gq::zero(), |acc, (a, b)| acc + a.conj() * b))
}

/// `x y*`, with entries `x_i conj(y_j)`.
pub fn outer(x: &[Gq], y: &[Gq]) -> Matrix {
    x.iter()
        .map(|a| y.iter().map(|b| a * b.conj()).collect())
        .collect()
}

pub fn trace(a: &Matrix) -> Gq {
    a.iter()
        .enumerate()
        .filter_map(|(i, r)| r.get(i))
        .fold(Gq::zero(), |acc, x| acc + x)
}

/// `trace(A B) = Σ_ij A_ij B_ji`; both matrices must be `n × n`.
pub fn trace_mul(a: &Matrix, b: &Matrix) -> Result<Gq, Error> {
    let n = a.len();
    same_length("trace_mul", n, b.len())?;
    for r in a.iter().chain(b) {
        same_length("trace_mul", n, r.len())?;
    }
    let mut acc = Gq::zero();
    for i in 0..n {
        for j in 0..n {
            acc = acc + &a[i][j] * &b[j][i];
        }
    }
    Ok(acc)
}

/// `x* A x = Σ conj(x_i) (A x)_i`.
pub fn hermitian_form(a: &Matrix, x: &[Gq]) -> Result<Gq, Error> {
    inner(x, &mat_vec(a, x)?)
}

/// `re(x* A x)`, the Hermitian form of the Hermitian part of `A`.
pub fn re_hermitian_form(a: &Matrix, x: &[Gq]) -> Result<Q, Error> {
    Ok(hermitian_form(a, x)?.re)
}

pub fn is_hermitian(a: &Matrix) -> bool {
    *a == adjoint(a)
}

/// `(A + A*)/2`.
pub fn hermitian_part(a: &Matrix) -> Result<Matrix, Error> {
    Ok(scale(&Gq::real(half()), &add(a, &adjoint(a))?))
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

/// Solve `L* x = y` on the pivoted coordinates: `x_k = −Σ_{i>k} conj(w_k[i]) x_i` for the
/// recorded terms `(k, d_k, w_k)` in reverse order, so that `x* E x` reduces to the form on
/// the unpivoted coordinates of `y`.
fn lift_witness(terms: &[(usize, Q, Vector)], mut x: Vector) -> Vector {
    for (k, _, w) in terms.iter().rev() {
        let acc = w
            .iter()
            .zip(&x)
            .skip(k + 1)
            .fold(Gq::zero(), |acc, (wi, xi)| acc + wi.conj() * xi);
        if let Some(slot) = x.get_mut(*k) {
            *slot = -acc;
        }
    }
    x
}

/// Gram terms `(d_k, w_k)` with `E == Σ d_k w_k w_k*` and real `d_k ≥ 0`, or a witness `x`
/// with `x* E x < 0`. Refuses a non-Hermitian matrix.
///
/// A negative pivot `E_pp < 0` is witnessed by the lifted `e_p`. A zero pivot with a nonzero
/// off-diagonal `c = E_jp` is witnessed by the lifted `e_p + s·e_j`, whose form is
/// `2·re(conj(c)·s) + |s|²·m` with `m = E_jj`; `s = −t·c` gives `|c|²·t·(t·m − 2) < 0` for
/// `t = 1` (`m ≤ 0`) or `t = 1/m` (`m > 0`), exactly as the Python twin.
pub fn gram_decomposition(e: &Matrix) -> Result<GramDecomposition, Error> {
    let e = matrix(e)?;
    if !is_hermitian(&e) {
        return Err(Error::NotHermitian);
    }
    let n = e.len();
    let mut m = e;
    let mut terms: Vec<(usize, Q, Vector)> = Vec::new();
    for p in 0..n {
        let piv = m[p][p].re.clone();
        if piv < Q::zero() {
            return Ok(GramDecomposition::NotPsd {
                witness: lift_witness(&terms, unit_vector(n, p)),
            });
        }
        if piv.is_zero() {
            for j in (p + 1)..n {
                let c = m[j][p].clone();
                if !c.is_zero() {
                    let mm = m[j][j].re.clone();
                    let t = if mm <= Q::zero() {
                        Q::one()
                    } else {
                        mm.recip()
                    };
                    let mut y = unit_vector(n, p);
                    y[j] = -(&c * &t);
                    return Ok(GramDecomposition::NotPsd {
                        witness: lift_witness(&terms, y),
                    });
                }
            }
            continue;
        }
        let inverse = piv.recip();
        let w: Vector = (0..n).map(|i| &m[i][p] * &inverse).collect();
        m = sub(&m, &scale(&Gq::real(piv.clone()), &outer(&w, &w)))?;
        terms.push((p, piv, w));
    }
    Ok(GramDecomposition::Psd {
        terms: terms.into_iter().map(|(_, d, w)| (d, w)).collect(),
    })
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
        if d < &Q::zero() {
            return Ok(false);
        }
        s = add(&s, &scale(&Gq::real(d.clone()), &outer(&w, &w)))?;
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
pub fn rank_one_effect(x: &[Gq]) -> Result<Matrix, Error> {
    let x = vector(x)?;
    let nrm = inner(&x, &x)?.re;
    if nrm.is_zero() {
        return Err(Error::ZeroVector);
    }
    Ok(scale(&Gq::real(nrm.recip()), &outer(&x, &x)))
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
        .fold(Q::zero(), |acc, x| acc + x.re.abs() + x.im.abs());
    Ok(total.ceil().to_integer())
}

/// `−t·(x·x) ≤ re(x* A x) ≤ t·(x·x)`.
pub fn bounded_by(a: &Matrix, t: &Q, x: &[Gq]) -> Result<bool, Error> {
    let a = matrix(a)?;
    validate_rational(t)?;
    let x = vector(x)?;
    let form = re_hermitian_form(&a, &x)?;
    let s = t * inner(&x, &x)?.re;
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
        &Gq::real(two_t.recip()),
        &add(&a, &scale(&Gq::real(t.clone()), &identity(a.len())))?,
    ))
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

/// `ρ_ji = L(E_ij) − i·L(i·E_ij)` with `L` the midpoint extension, so that
/// `re(trace(ρ A)) = L(A)` for a real-linear `L`.
pub fn representing_matrix(valuation: Valuation<'_>, n: usize) -> Result<Matrix, Error> {
    let mut rho = Vec::with_capacity(n);
    for j in 0..n {
        let mut row = Vec::with_capacity(n);
        for i in 0..n {
            let along_one = extend(valuation, &single(n, i, j, &Gq::one())?, None)?;
            let along_i = extend(valuation, &single(n, i, j, &Gq::i())?, None)?;
            row.push(Gq::new(along_one, -along_i));
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
        Ok(trace_mul(&rho, &matrix(e)?)?.re)
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
    pub hermitian: bool,
    pub trace: Gq,
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
        if trace_mul(&rho, e)?.re != evaluate(valuation, e)? {
            agrees_on_effects = false;
            break;
        }
    }
    let tr = trace(&rho);
    Ok(BornCertificate {
        hermitian: is_hermitian(&rho),
        trace_real: tr.is_real(),
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
    Ok(&e[0][0].re * &e[0][0].re)
}

/// Control: `E ↦ 2·re(E_00) − re(E_22)`, real-linear with unit value 1 but not positive.
/// Refuses a matrix that is not `3 × 3` (the three-dimensional control).
pub fn bad_linear_valuation(e: &Matrix) -> Result<Q, Error> {
    let e = matrix(e)?;
    same_length("bad_linear_valuation", 3, e.len())?;
    Ok(q(2) * &e[0][0].re - &e[2][2].re)
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
    Ok(&e[0][0].re + &e[0][1].im)
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::linear_algebra::basic_matrix::BasicMatrix;
    use crate::linear_algebra::ordered::hermitian_is_positive_semidefinite;
    use crate::linear_algebra::scalars::{qr, Field, Involution, Ring, Semiring};

    fn fr(n: i64, d: i64) -> Q {
        qr(n, d).expect("nonzero fixture denominator")
    }

    /// `re + im·i` from integer parts.
    fn gi(re: i64, im: i64) -> Gq {
        Gq::from_integers(re, im)
    }

    /// `(a/b) + (c/d)·i`.
    fn gf(a: i64, b: i64, c: i64, d: i64) -> Gq {
        Gq::new(fr(a, b), fr(c, d))
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
        single(n, i, j, &Gq::one()).unwrap()
    }

    fn mat_mul(a: &Matrix, b: &Matrix) -> Matrix {
        let n = a.len();
        (0..n)
            .map(|i| {
                (0..n)
                    .map(|j| (0..n).fold(Gq::zero(), |acc, k| acc + &a[i][k] * &b[k][j]))
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
            vec![gf(1, 2, 0, 1), Gq::zero(), gf(0, 1, 1, 4)],
            vec![Gq::zero(), gf(1, 4, 0, 1), Gq::zero()],
            vec![gf(0, 1, -1, 4), Gq::zero(), gf(1, 4, 0, 1)],
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
            vec![Gq::zero(), gf(1, 2, 0, 1)],
        ]
    }

    fn effects2() -> Vec<Matrix> {
        vec![
            identity(2),
            scale(&Gq::real(fr(1, 2)), &identity(2)),
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
            scale(&Gq::real(fr(1, 3)), &identity(3)),
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
                                Gq::new(re, im)
                            })
                            .collect()
                    })
                    .collect()
            })
            .collect()
    }

    // ------------------------------------------------------------------ Gaussian scalars

    #[test]
    fn test_gaussian_arithmetic_and_display() {
        let a = gf(3, 5, 4, 5);
        assert_eq!(a.to_string(), "3/5+4/5i");
        assert_eq!(
            [
                Gq::i().to_string(),
                gi(2, 0).to_string(),
                gf(0, 1, -1, 2).to_string(),
                gf(1, 4, -1, 4).to_string()
            ],
            ["1i", "2", "-1/2i", "1/4-1/4i"]
        );
        assert_eq!(Gq::i() * Gq::i(), gi(-1, 0));
        assert_eq!(&a * &a.conj(), Gq::one());
        assert_eq!(a.norm_sq(), q(1));
        assert_eq!(gi(1, 2).try_div(&gi(3, 4)).unwrap(), gf(11, 25, 2, 25));
        assert_eq!(Gq::one().try_div(&Gq::i()).unwrap(), -Gq::i());
        assert_eq!(gi(2, 0) - Gq::i(), gi(2, -1));
        assert_eq!(&Gq::i() * &fr(1, 2), gf(0, 1, 1, 2));
        assert_eq!(
            [Gq::i(), Gq::one(), Gq::i()]
                .iter()
                .fold(Gq::zero(), |acc, x| acc + x),
            gi(1, 2)
        );
        assert!(Gq::zero().is_zero() && !Gq::i().is_zero());
        assert!(gi(2, 0).is_real() && !Gq::i().is_real());
        assert_ne!(Gq::i(), Gq::one());
        assert_eq!(
            Gq::one().try_div(&Gq::zero()),
            Err(BornHermitianValuationError::DivisionByZero)
        );
    }

    /// The local plain-operator scalar agrees with the crate's `GaussianRational` on
    /// products, conjugates, norms and inverses, and converts losslessly both ways.
    #[test]
    fn test_gq_agrees_with_gaussian_rational() {
        let samples = [
            gi(1, 2),
            gi(3, 4),
            gf(3, 5, 4, 5),
            gf(-1, 2, 7, 3),
            Gq::i(),
            gi(-2, 0),
        ];
        for a in &samples {
            let ga = GaussianRational::try_from(a).unwrap();
            assert_eq!(Gq::from(&ga), *a);
            assert_eq!(Gq::from(ga.try_conj().unwrap()), a.conj());
            assert_eq!(ga.norm_sq(), a.norm_sq());
            assert_eq!(
                Gq::from(ga.try_inv().unwrap()),
                Gq::one().try_div(a).unwrap()
            );
            for b in &samples {
                let gb = GaussianRational::try_from(b).unwrap();
                assert_eq!(Gq::from(ga.try_mul(&gb).unwrap()), a * b);
                assert_eq!(Gq::from(ga.try_add(&gb).unwrap()), a + b);
                assert_eq!(Gq::from(ga.try_sub(&gb).unwrap()), a - b);
                assert_eq!(
                    Gq::from(ga.try_div(&gb).unwrap()),
                    a.try_div(b).unwrap()
                );
            }
        }
        let raw = Gq::new(Q::new_raw(BigInt::from(2), BigInt::from(4)), q(0));
        assert_eq!(
            GaussianRational::try_from(raw),
            Err(RationalConstructionError::NonReduced)
        );
    }

    #[test]
    fn test_matrix_helpers() {
        let a = mi(&[&[(1, 0), (2, 3)], &[(0, -1), (4, 0)]]);
        assert_eq!(adjoint(&a), mi(&[&[(1, 0), (0, 1)], &[(2, -3), (4, 0)]]));
        assert!(!is_hermitian(&a));
        assert!(is_hermitian(&hermitian_part(&a).unwrap()));
        assert!(is_hermitian(&rho2()) && is_hermitian(&rho3()));
        assert_eq!(
            inner(&vi(&[(1, 0), (0, 1)]), &vi(&[(0, 1), (1, 0)])).unwrap(),
            Gq::zero()
        );
        assert_eq!(inner(&vi(&[(0, 1)]), &vi(&[(0, 1)])).unwrap(), Gq::one());
        assert_eq!(
            outer(&vi(&[(1, 0), (0, 1)]), &vi(&[(1, 0), (0, 1)])),
            mi(&[&[(1, 0), (0, -1)], &[(0, 1), (1, 0)]])
        );
        assert_eq!(trace(&rho2()), Gq::one());
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
            single(2, 0, 1, &Gq::i()).unwrap(),
            mi(&[&[(0, 0), (0, 1)], &[(0, 0), (0, 0)]])
        );
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
                    (fr(1, 2), vec![Gq::one(), gf(1, 2, 1, 2)]),
                    (fr(1, 4), vec![Gq::zero(), Gq::one()]),
                ],
                reconstructs: true,
            }
        );
    }

    #[test]
    fn test_negative_witness_is_exact() {
        let cases: Vec<(Matrix, Vector, Gq)> = vec![
            (
                mi(&[&[(0, 0), (1, 0)], &[(1, 0), (0, 0)]]),
                vi(&[(1, 0), (-1, 0)]),
                gi(-2, 0),
            ),
            (
                mi(&[&[(0, 0), (0, 1)], &[(0, -1), (0, 0)]]),
                vi(&[(1, 0), (0, 1)]),
                gi(-2, 0),
            ),
            (
                mi(&[&[(0, 0), (1, 1)], &[(1, -1), (2, 0)]]),
                vec![Gq::one(), gf(-1, 2, 1, 2)],
                gi(-1, 0),
            ),
            (
                mi(&[
                    &[(1, 0), (0, 0), (0, 0)],
                    &[(0, 0), (0, 0), (0, 2)],
                    &[(0, 0), (0, -2), (1, 0)],
                ]),
                vi(&[(0, 0), (1, 0), (0, 2)]),
                gi(-4, 0),
            ),
            (
                mi(&[&[(1, 0), (0, 2)], &[(0, -2), (1, 0)]]),
                vi(&[(0, -2), (1, 0)]),
                gi(-3, 0),
            ),
            (
                mi(&[&[(-1, 0), (0, 0)], &[(0, 0), (1, 0)]]),
                vi(&[(1, 0), (0, 0)]),
                gi(-1, 0),
            ),
            (
                mi(&[&[(1, 0), (1, -1)], &[(1, 1), (1, 0)]]),
                vi(&[(-1, 1), (1, 0)]),
                gi(-1, 0),
            ),
        ];
        for (e, x, value) in cases {
            let GramDecomposition::NotPsd { witness } = gram_decomposition(&e).unwrap() else {
                panic!("expected not_psd for {e:?}");
            };
            assert_eq!(witness, vector(&x).unwrap());
            assert_eq!(hermitian_form(&e, &witness).unwrap(), value);
            assert!(value.is_real() && value.re < q(0));
            let PsdCertificate::NotPsd { witness: w, value: v } = psd_certificate(&e).unwrap()
            else {
                panic!("expected a witness for {e:?}");
            };
            assert_eq!(w, witness);
            assert_eq!(v, value.re);
        }
    }

    /// Zero pivot with off-diagonal `c` and lower diagonal `m`: witness `[1, −t·c]` with
    /// `t = 1` (`m ≤ 0`) or `1/m`, and form `|c|²·t·(t·m − 2)`.
    #[test]
    fn test_zero_pivot_witness_formula() {
        for (c, mm) in [
            (gi(1, 1), q(0)),
            (gi(1, 1), q(2)),
            (gi(0, -3), q(-1)),
            (gf(2, 3, -1, 5), fr(7, 3)),
        ] {
            let e = vec![
                vec![Gq::zero(), c.conj()],
                vec![c.clone(), Gq::real(mm.clone())],
            ];
            let t = if mm <= q(0) { q(1) } else { mm.recip() };
            let GramDecomposition::NotPsd { witness } = gram_decomposition(&e).unwrap() else {
                panic!("expected not_psd for {e:?}");
            };
            assert_eq!(witness, vec![Gq::one(), -(&c * &t)]);
            let expected = c.norm_sq() * &t * (&t * &mm - q(2));
            assert_eq!(hermitian_form(&e, &witness).unwrap(), Gq::real(expected));
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

    /// Two independent exact routes agree: the Gram-based `is_psd` and the crate's Hermitian
    /// congruence inertia on `BasicMatrix<GaussianRational>`; every witness replays.
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
            let n = h.len();
            let data: Vec<GaussianRational> = h
                .iter()
                .flatten()
                .map(|x| GaussianRational::try_from(x).unwrap())
                .collect();
            let basic = BasicMatrix::from_row_major(n, n, data).unwrap();
            assert_eq!(
                is_psd(&e).unwrap(),
                hermitian_is_positive_semidefinite(&basic).unwrap(),
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
                    assert_eq!(hermitian_form(&h, &witness).unwrap(), Gq::real(value.clone()));
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
        assert!(!is_effect(&scale(&gi(2, 0), &identity(2))).unwrap());
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
            assert_eq!(trace(&e), Gq::one());
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
                single(n, 0, 1, &Gq::i()).unwrap(),
                sub(&unit(n, 0, 0), &scale(&gi(3, 1), &identity(n))).unwrap(),
            ] {
                let c = extension_consistency(&v, &a, &bounds).unwrap();
                assert!(c.consistent, "{a:?}");
                assert_eq!(c.bounds, bounds.to_vec());
                assert_eq!(c.values.len(), 4);
                assert_eq!(
                    extend(&v, &a, None).unwrap(),
                    trace_mul(&rho, &a).unwrap().re
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
                assert_eq!(extend(v, &a, None).unwrap(), trace_mul(&rho, &a).unwrap().re);
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
            assert_eq!(c.trace, Gq::one());
            assert_eq!(c.effects_checked, effs.len());
            assert_eq!(c.rho, rho);
        }
    }

    #[test]
    fn test_born_valuation_satisfies_axioms() {
        let v = born_valuation(&rho2()).unwrap();
        let pairs = vec![
            (
                scale(&Gq::real(fr(1, 2)), &identity(2)),
                scale(&Gq::real(fr(1, 2)), &identity(2)),
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
            scale(&Gq::real(fr(1, 2)), &identity(2)),
            scale(&Gq::real(fr(1, 2)), &identity(2)),
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
        assert_eq!(c.trace, Gq::one());
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
        assert_eq!(c.trace, Gq::one());
        assert!(c.trace_real);
        assert!(!c.psd);
        assert!(c.agrees_on_effects);
        assert_eq!(c.effects_checked, effects2().len());
        assert_eq!(
            c.psd_certificate,
            PsdCertificate::NotPsd {
                witness: vec![gf(0, 1, -1, 2), Gq::one()],
                value: fr(-1, 4)
            }
        );
        assert_eq!(
            hermitian_part(&representing_matrix(v, 2).unwrap()).unwrap(),
            vec![
                vec![Gq::one(), gf(0, 1, 1, 2)],
                vec![gf(0, 1, -1, 2), Gq::zero()],
            ]
        );
        let pairs = vec![
            (
                scale(&Gq::real(fr(1, 2)), &identity(2)),
                scale(&Gq::real(fr(1, 2)), &identity(2)),
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
        let witness = rank_one_effect(&[gf(0, 1, -1, 2), Gq::one()]).unwrap();
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
            Ok(trace_mul(&rho, &matrix(e)?)?.re * q(2))
        };
        let c = born_certificate(&v, 2, &[]).unwrap();
        assert_ne!(c.trace, Gq::one());
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
            scale(&gi(2, 0), &identity(2)),
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
            single(2, 2, 0, &Gq::one()),
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
        let raw = Gq::new(Q::new_raw(BigInt::from(2), BigInt::from(4)), q(0));
        assert_eq!(
            matrix(&[vec![raw.clone()]]),
            Err(E::InexactEntry(RationalConstructionError::NonReduced))
        );
        assert_eq!(
            vector(&[raw.clone()]),
            Err(E::InexactEntry(RationalConstructionError::NonReduced))
        );
        assert_eq!(
            single(2, 0, 0, &raw),
            Err(E::InexactEntry(RationalConstructionError::NonReduced))
        );
        let raw_imag = Gq::new(q(0), Q::new_raw(BigInt::from(1), BigInt::from(-2)));
        assert_eq!(
            matrix(&[vec![raw_imag]]),
            Err(E::InexactEntry(RationalConstructionError::NegativeDenominator))
        );
        assert_eq!(
            valuation_axioms(&v, 2, &[scale(&gi(2, 0), &identity(2))], &[]),
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
            square_valuation(&scale(&Gq::real(fr(1, 2)), &identity(2))),
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
