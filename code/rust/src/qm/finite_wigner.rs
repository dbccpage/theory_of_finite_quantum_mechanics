//! Exact replay of the finite Wigner theorem over `ℚ(i)ⁿ`: a map of nonzero vectors that
//! preserves transition probabilities is, ray by ray, a linear or conjugate-linear similarity.
//!
//! Replays in exact Gaussian-rational arithmetic the Lean modules of
//! `dag/results/L1-IMP-LINEAR-ISOMETRIC-DYNAMICS/runs/20261021T190000Z_finite_wigner`
//! (`FiniteWignerKernel`, `FiniteWignerTheorem`, `FiniteWignerSimilarity`,
//! `GaussRatAutomorphisms`, installed under `lean4/`) and mirrors, function for function, the
//! Python twin `code/python/src/qm/finite_wigner.py`:
//!
//! * the inner product `ip(x, y) = Σ conj(x_k)·y_k`, the squared norm `vnorm(x) = re ip(x, x)`
//!   and the transition probability `tp(x, y) = |ip(x, y)|² / (vnorm x · vnorm y)`, read also as
//!   the Born value `re(y* P_x y) / vnorm y` of the rank-one effect `P_x = x x* / vnorm x`;
//! * the twist `twist(+1, x) = x`, `twist(−1, x) = conj x`; similarities `Fᴴ F = d·I` with the
//!   first offending entry as witness, their inverses `(1/d)·Fᴴ`, and the ray maps
//!   `x ↦ c(x)·F·twist(eps, x)` with a nonzero scalar `c(x)` per vector (ray freedom);
//! * the reconstruction of `(F, d, eps)` from a map through the probes `e_i`, `e_i0 + e_j` and
//!   `e_i0 + i·e_j` (sign consistency forced by the pair `e_i0 + i·e_j + i·e_k`,
//!   `e_i0 + e_j + e_k`), with a tagged witness (`zero_image`, `orthogonality`, `alignment` with
//!   its sub-tag, `sign`, `consistency`) for the first probe on which the map is not
//!   transition-probability preserving; the pairwise check `tp(T x, T y) = tp(x, y)` on supplied
//!   probes; and the check that a map is induced by `(F, eps)` on supplied samples (stages 1
//!   and 2 of the theorem replayed on finite data, not for every `x`);
//! * the unitary normalisation: `F/c` is `ℚ(i)`-unitary iff `d = |c|²` is a sum of two rational
//!   squares, decided by the primes `≡ 3 (mod 4)` of `num·den` and witnessed by composing
//!   Fermat representations with the Brahmagupta–Fibonacci identity; the countermodel [`f3`]
//!   (`d = 3`) induces a transition-probability preserving ray map that no `ℚ(i)`-unitary or
//!   antiunitary induces.
//!
//! The carrier `ℚ(i)ⁿ`, its inner product and the transition probability are supplied;
//! transition-probability preservation (with `T x ≠ 0` for `x ≠ 0`) is the hypothesis; only the
//! form of the map — a similarity `F` with scale `d` and a sign `eps`, up to a nonzero scalar per
//! ray — is derived. No continuity is used and no unitarity is claimed. AuthorityEffect: None.
//!
//! Scalars: the crate's `Q` (canonical `BigRational`, admitted through `validate_rational`) and
//! [`GaussianRational`] (`Result`-valued arithmetic). Nothing panics on caller data; the
//! reconstruction calls the supplied map only on the listed probes.

use num_bigint::BigInt;
use num_integer::{Integer, Roots};
use num_traits::{Signed, Zero};

use crate::linear_algebra::scalars::{
    validate_rational, Field, Involution, RationalConstructionError, Ring, ScalarError, Semiring,
};
use crate::linear_algebra::{q, GaussianRational, Q};

pub const AUTHORITY_FENCE: &str = "AuthorityEffect None; not PROVED; the carrier Q(i)^n, its \
     inner product and the transition probability are supplied; transition-probability \
     preservation is the hypothesis; only the form of the map (a linear or conjugate-linear \
     similarity up to a nonzero scalar per ray) is derived; no unitarity is claimed; \
     assumptions exposed.";

pub const PROVENANCE: &str = "Replays the Lean modules of \
     dag/results/L1-IMP-LINEAR-ISOMETRIC-DYNAMICS/runs/20261021T190000Z_finite_wigner \
     (FiniteWignerKernel, FiniteWignerTheorem, FiniteWignerSimilarity, GaussRatAutomorphisms) \
     and the Python twin code/python/src/qm/finite_wigner.py.";

/// A Gaussian-rational square matrix as rows; every public entry point re-admits it through
/// [`hmatrix`].
pub type HMatrix = Vec<Vec<GaussianRational>>;
/// A Gaussian-rational carrier vector; every public entry point re-admits it through
/// [`hvector`].
pub type HVector = Vec<GaussianRational>;
/// A map `T : ℚ(i)ⁿ → ℚ(i)ⁿ` under test, refusing (never panicking on) inputs outside its
/// domain; its images are re-admitted by every consumer.
pub type RayMap<'a> = &'a dyn Fn(&HVector) -> Result<HVector, FiniteWignerError>;
/// An owned map; `&t` passes as a [`RayMap`].
pub type BoxedRayMap = Box<dyn Fn(&HVector) -> Result<HVector, FiniteWignerError>>;

#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum FiniteWignerError {
    #[error("nonempty square matrix required")]
    NonSquareMatrix,
    #[error("nonempty vector required")]
    EmptyVector,
    #[error("exact canonical rational entries required: {0}")]
    InexactEntry(#[from] RationalConstructionError),
    #[error("scalar arithmetic: {0}")]
    Scalar(#[from] ScalarError),
    #[error("{operation}: dimension {expected} expected, got {got}")]
    DimensionMismatch {
        operation: &'static str,
        expected: usize,
        got: usize,
    },
    #[error("index {index} is outside dimension {dimension}")]
    IndexOutOfRange { index: usize, dimension: usize },
    #[error("a permutation of 0..{0} is required")]
    NotAPermutation(usize),
    #[error("distinct probe indices required")]
    IndicesNotDistinct,
    #[error("at least one block required")]
    NoBlocks,
    #[error("a sign eps in {{+1, -1}} is required, got {0}")]
    InvalidSign(i8),
    #[error("nonzero vector required")]
    ZeroVector,
    #[error("basis vector {index} is zero")]
    ZeroBasisVector { index: usize },
    #[error("basis vectors {i} and {j} are not orthogonal")]
    NotOrthogonal {
        i: usize,
        j: usize,
        ip: GaussianRational,
    },
    #[error("the vector is not in the span of the supplied basis")]
    NotInSpan { residual: HVector },
    #[error("similarity required: entry ({i}, {j}) of F^H F is not the expected one")]
    NotSimilarity {
        i: usize,
        j: usize,
        entry: GaussianRational,
        expected: GaussianRational,
    },
    #[error("positive rational scale required")]
    NonPositiveScale(Q),
    #[error("no Fermat representation of {0} as a sum of two squares was found")]
    NoFermatRepresentation(BigInt),
}

type Error = FiniteWignerError;

/// Outcome of [`similarity_certificate`].
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum SimilarityVerdict {
    /// `Fᴴ F = d·I` with `d = re (Fᴴ F)_00 > 0`.
    Similarity { d: Q },
    /// The first entry (row-major) of `Fᴴ F` that differs from `d·I`; a non-positive diagonal
    /// `d` makes `(0, 0)` offending.
    NotSimilarity {
        i: usize,
        j: usize,
        entry: GaussianRational,
        expected: GaussianRational,
    },
}

impl SimilarityVerdict {
    /// The Python twin's verdict tag.
    pub fn tag(&self) -> &'static str {
        match self {
            Self::Similarity { .. } => "similarity",
            Self::NotSimilarity { .. } => "not_similarity",
        }
    }
}

/// The first failed probe of [`reconstruct`]: each one contradicts transition-probability
/// preservation (by the Lean theorem for `Consistency`, directly for the others).
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum TpWitness {
    /// `T(probe) = 0` for a nonzero probe (the hypothesis `T x ≠ 0` fails).
    ZeroImage { probe: HVector },
    /// `ip(T e_i, T e_j) = ip ≠ 0` although `tp(e_i, e_j) = 0`.
    Orthogonality {
        i: usize,
        j: usize,
        ip: GaussianRational,
    },
    /// The image of `probe` has `coordinates` (w.r.t. `g_k = T e_k` for the probe
    /// `e_i0 + e_j`, w.r.t. the aligned frame `f` for `e_i0 + i·e_j`) that break the equation
    /// named by `failure`.
    Alignment {
        j: usize,
        failure: AlignmentFailure,
        probe: HVector,
        coordinates: HVector,
    },
    /// The relative phase `u = b'/a'` (both nonzero) of the image of `probe = e_i0 + i·e_j`
    /// violates `|u|² = 1` or `|1 + u|² = 2`, i.e. `u ∉ {i, −i}`.
    Sign {
        j: usize,
        probe: HVector,
        u: GaussianRational,
    },
    /// `eps_j ≠ eps_k`; the probe `e_i0 + i·e_j + i·e_k` forces agreement.
    Consistency {
        j: usize,
        k: usize,
        eps_j: i8,
        eps_k: i8,
        probe: HVector,
    },
}

/// The failed equation of an alignment probe (the Python twin's sub-tag, [`Self::kind`]).
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum AlignmentFailure {
    /// Step 2: the coordinate `z_k ≠ 0` at the first `k ∉ {i0, j}` (`tp(e_i0 + e_j, e_k) = 0`
    /// fails).
    Support { k: usize, z_k: GaussianRational },
    /// Step 2: `a = 0` or `b = 0` (`tp = 1/2` against `e_i0` or `e_j` fails).
    Vanishing {
        a: GaussianRational,
        b: GaussianRational,
    },
    /// Step 2: `lhs = |a|²·vnorm(g_i0) ≠ |b|²·vnorm(g_j) = rhs` (both equal `vnorm(h_j)/2` when
    /// `tp = 1/2` holds against `e_i0` and `e_j`).
    Balance { lhs: Q, rhs: Q },
    /// Step 3: as `Support`, for the probe `e_i0 + i·e_j` in the aligned frame `f`.
    PhaseSupport { k: usize, z_k: GaussianRational },
    /// Step 3: as `Vanishing`, for `(a', b')` in the aligned frame `f`.
    PhaseVanishing {
        a: GaussianRational,
        b: GaussianRational,
    },
}

impl AlignmentFailure {
    /// The Python twin's alignment sub-tag.
    pub fn kind(&self) -> &'static str {
        match self {
            Self::Support { .. } => "support",
            Self::Vanishing { .. } => "vanishing",
            Self::Balance { .. } => "balance",
            Self::PhaseSupport { .. } => "phase_support",
            Self::PhaseVanishing { .. } => "phase_vanishing",
        }
    }
}

impl TpWitness {
    /// The Python twin's witness tag.
    pub fn tag(&self) -> &'static str {
        match self {
            Self::ZeroImage { .. } => "zero_image",
            Self::Orthogonality { .. } => "orthogonality",
            Self::Alignment { .. } => "alignment",
            Self::Sign { .. } => "sign",
            Self::Consistency { .. } => "consistency",
        }
    }
}

/// Outcome of [`reconstruct`].
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum ReconstructionVerdict {
    /// `F` (columns `f_0, …, f_{n−1}`) with `Fᴴ F = d·I` and the common sign `eps`.
    Reconstructed { f: HMatrix, d: Q, eps: i8 },
    NotTpPreserving(TpWitness),
}

impl ReconstructionVerdict {
    /// The Python twin's verdict tag.
    pub fn tag(&self) -> &'static str {
        match self {
            Self::Reconstructed { .. } => "reconstructed",
            Self::NotTpPreserving(_) => "not_tp_preserving",
        }
    }
}

/// Outcome of [`verify_induced`].
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum InducedVerdict {
    /// Every sample image is a nonzero multiple of `F·twist(eps, x)`.
    Induced,
    /// The first sample `x` whose `image = T x` is not a nonzero multiple of
    /// `direction = F·twist(eps, x)`.
    NotInduced {
        x: HVector,
        image: HVector,
        direction: HVector,
    },
}

impl InducedVerdict {
    /// The Python twin's verdict tag.
    pub fn tag(&self) -> &'static str {
        match self {
            Self::Induced => "induced",
            Self::NotInduced { .. } => "not_induced",
        }
    }
}

/// Outcome of [`tp_defect`].
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum TpDefectVerdict {
    /// `tp(T x, T y) = tp(x, y)` for every pair of supplied probes.
    TpPreserved,
    /// The first probe with `T x = 0`.
    ZeroImage { x: HVector },
    /// The first pair (in probe order) with `before = tp(x, y) ≠ tp(T x, T y) = after`.
    TpDefect {
        x: HVector,
        y: HVector,
        before: Q,
        after: Q,
    },
}

impl TpDefectVerdict {
    /// The Python twin's verdict tag.
    pub fn tag(&self) -> &'static str {
        match self {
            Self::TpPreserved => "tp_preserved",
            Self::ZeroImage { .. } => "zero_image",
            Self::TpDefect { .. } => "tp_defect",
        }
    }
}

/// Outcome of [`sum_of_two_rational_squares`].
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum TwoSquaresVerdict {
    /// `a² + b² = d` with `a, b ≥ 0`.
    Representable { a: Q, b: Q },
    /// `p ≡ 3 (mod 4)` divides `num·den` to an odd power (the smallest such prime).
    NotRepresentable { p: BigInt },
}

impl TwoSquaresVerdict {
    /// The Python twin's verdict tag.
    pub fn tag(&self) -> &'static str {
        match self {
            Self::Representable { .. } => "representable",
            Self::NotRepresentable { .. } => "not_representable",
        }
    }
}

/// Outcome of [`unitary_normalisation`].
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum UnitaryVerdict {
    /// `|c|² = d` and `u = F/c` with `uᴴ u = I`.
    Unitary { c: GaussianRational, u: HMatrix },
    /// The scale `d` of the similarity is not a norm from `ℚ(i)`, obstructed by the prime `p`.
    NotANorm { d: Q, p: BigInt },
    /// `F` is not a similarity (the witness of [`similarity_certificate`]).
    NotSimilarity {
        i: usize,
        j: usize,
        entry: GaussianRational,
        expected: GaussianRational,
    },
}

impl UnitaryVerdict {
    /// The Python twin's verdict tag.
    pub fn tag(&self) -> &'static str {
        match self {
            Self::Unitary { .. } => "unitary",
            Self::NotANorm { .. } => "not_a_norm",
            Self::NotSimilarity { .. } => "not_similarity",
        }
    }
}

// ============================================================================
// Exact-input admission and the *-algebra of Q(i)^n (supplied, not derived)
// ============================================================================

fn g_zero() -> GaussianRational {
    GaussianRational::from_integers(0, 0)
}

fn g_one() -> GaussianRational {
    GaussianRational::from_integers(1, 0)
}

/// The imaginary unit `i`.
pub fn gi() -> GaussianRational {
    GaussianRational::from_integers(0, 1)
}

/// `x + 0·i`; refuses a non-canonical `x`.
fn from_real(x: &Q) -> Result<GaussianRational, Error> {
    Ok(GaussianRational::new(x.clone(), q(0))?)
}

/// Admit a nonempty square Gaussian-rational matrix.
pub fn hmatrix(rows: &[Vec<GaussianRational>]) -> Result<HMatrix, Error> {
    let n = rows.len();
    if n == 0 || rows.iter().any(|r| r.len() != n) {
        return Err(Error::NonSquareMatrix);
    }
    for x in rows.iter().flatten() {
        x.validate()?;
    }
    Ok(rows.to_vec())
}

/// Admit a nonempty Gaussian-rational vector.
pub fn hvector(xs: &[GaussianRational]) -> Result<HVector, Error> {
    if xs.is_empty() {
        return Err(Error::EmptyVector);
    }
    for x in xs {
        x.validate()?;
    }
    Ok(xs.to_vec())
}

/// Admit a sign `eps ∈ {+1, −1}`.
fn sign(eps: i8) -> Result<i8, Error> {
    if eps == 1 || eps == -1 {
        Ok(eps)
    } else {
        Err(Error::InvalidSign(eps))
    }
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

fn index_in(index: usize, dimension: usize) -> Result<(), Error> {
    if index < dimension {
        Ok(())
    } else {
        Err(Error::IndexOutOfRange { index, dimension })
    }
}

/// `z / r` for a nonzero rational `r`.
fn div_real(z: &GaussianRational, r: &Q) -> Result<GaussianRational, Error> {
    if r.is_zero() {
        return Err(ScalarError::DivisionByZero.into());
    }
    Ok(GaussianRational::new(z.real() / r, z.imag() / r)?)
}

fn scale_vector(c: &GaussianRational, x: &[GaussianRational]) -> Result<HVector, Error> {
    let mut out = Vec::with_capacity(x.len());
    for z in x {
        out.push(c.try_mul(z)?);
    }
    Ok(out)
}

/// `c·A`.
fn scale_matrix(c: &GaussianRational, a: &[Vec<GaussianRational>]) -> Result<HMatrix, Error> {
    let mut out = Vec::with_capacity(a.len());
    for row in a {
        out.push(scale_vector(c, row)?);
    }
    Ok(out)
}

/// `Σ conj(x_k)·y_k` on vectors already known to share a length.
fn ip(x: &[GaussianRational], y: &[GaussianRational]) -> Result<GaussianRational, Error> {
    let mut acc = g_zero();
    for (a, b) in x.iter().zip(y) {
        acc = acc.try_add(&a.try_conj()?.try_mul(b)?)?;
    }
    Ok(acc)
}

/// `Σ |x_k|²`.
fn norm(x: &[GaussianRational]) -> Q {
    x.iter().fold(q(0), |acc, z| acc + z.norm_sq())
}

/// `F·x` on shapes already checked.
fn mv(f: &[Vec<GaussianRational>], x: &[GaussianRational]) -> Result<HVector, Error> {
    let mut out = Vec::with_capacity(f.len());
    for row in f {
        let mut acc = g_zero();
        for (a, b) in row.iter().zip(x) {
            acc = acc.try_add(&a.try_mul(b)?)?;
        }
        out.push(acc);
    }
    Ok(out)
}

/// `A·B` on square matrices of one size.
fn mm(a: &[Vec<GaussianRational>], b: &[Vec<GaussianRational>]) -> Result<HMatrix, Error> {
    let n = a.len();
    let mut out = Vec::with_capacity(n);
    for row in a {
        let mut out_row = Vec::with_capacity(n);
        for j in 0..n {
            let mut acc = g_zero();
            for (k, x) in row.iter().enumerate() {
                acc = acc.try_add(&x.try_mul(&b[k][j])?)?;
            }
            out_row.push(acc);
        }
        out.push(out_row);
    }
    Ok(out)
}

/// `Fᴴ` of an admitted square matrix.
fn adjoint(f: &[Vec<GaussianRational>]) -> Result<HMatrix, Error> {
    let n = f.len();
    let mut out = Vec::with_capacity(n);
    for j in 0..n {
        let mut row = Vec::with_capacity(n);
        for frow in f {
            row.push(frow[j].try_conj()?);
        }
        out.push(row);
    }
    Ok(out)
}

fn twist_raw(eps: i8, x: &[GaussianRational]) -> Result<HVector, Error> {
    if eps == 1 {
        return Ok(x.to_vec());
    }
    let mut out = Vec::with_capacity(x.len());
    for z in x {
        out.push(z.try_conj()?);
    }
    Ok(out)
}

/// The Gaussian identity.
pub fn identity(n: usize) -> HMatrix {
    (0..n)
        .map(|i| (0..n).map(|j| if i == j { g_one() } else { g_zero() }).collect())
        .collect()
}

/// `c·e_i` in `ℚ(i)ⁿ` (the twin's `unit_vector(n, i, c=1)`).
pub fn unit_vector(n: usize, i: usize, c: &GaussianRational) -> Result<HVector, Error> {
    index_in(i, n)?;
    c.validate()?;
    Ok((0..n).map(|k| if k == i { c.clone() } else { g_zero() }).collect())
}

/// `ip(x, y) = Σ conj(x_k)·y_k`, conjugate-linear in the first slot.
pub fn inner(x: &[GaussianRational], y: &[GaussianRational]) -> Result<GaussianRational, Error> {
    let x = hvector(x)?;
    let y = hvector(y)?;
    same_length("inner", x.len(), y.len())?;
    ip(&x, &y)
}

/// `vnorm(x) = re ip(x, x) = Σ |x_k|²`.
pub fn vnorm(x: &[GaussianRational]) -> Result<Q, Error> {
    Ok(norm(&hvector(x)?))
}

fn tp_raw(x: &[GaussianRational], y: &[GaussianRational]) -> Result<Q, Error> {
    let nx = norm(x);
    let ny = norm(y);
    if nx.is_zero() || ny.is_zero() {
        return Err(Error::ZeroVector);
    }
    Ok(ip(x, y)?.norm_sq() / (nx * ny))
}

/// `tp(x, y) = |ip(x, y)|² / (vnorm x · vnorm y)`, a rational in `[0, 1]`; refuses a zero
/// vector.
pub fn transition_probability(x: &[GaussianRational], y: &[GaussianRational]) -> Result<Q, Error> {
    let x = hvector(x)?;
    let y = hvector(y)?;
    same_length("transition_probability", x.len(), y.len())?;
    tp_raw(&x, &y)
}

/// The rank-one effect `P_x = x x* / vnorm x` (entries `x_r conj(x_c) / vnorm x`); refuses
/// `x = 0`.
pub fn rank_one_effect(x: &[GaussianRational]) -> Result<HMatrix, Error> {
    let x = hvector(x)?;
    let nx = norm(&x);
    if nx.is_zero() {
        return Err(Error::ZeroVector);
    }
    let inv = from_real(&nx.recip())?;
    let mut out = Vec::with_capacity(x.len());
    for a in &x {
        let mut row = Vec::with_capacity(x.len());
        for b in &x {
            row.push(a.try_mul(&b.try_conj()?)?.try_mul(&inv)?);
        }
        out.push(row);
    }
    Ok(out)
}

/// The Born readout `re(y* P_x y) / vnorm y` of the rank-one effect `P_x` in the state `y`;
/// equals [`transition_probability`] (`hf_rankOne` of the Born carrier).
pub fn born_transition(x: &[GaussianRational], y: &[GaussianRational]) -> Result<Q, Error> {
    let p = rank_one_effect(x)?;
    let y = hvector(y)?;
    same_length("born_transition", p.len(), y.len())?;
    let ny = norm(&y);
    if ny.is_zero() {
        return Err(Error::ZeroVector);
    }
    Ok(ip(&y, &mv(&p, &y)?)?.real() / ny)
}

/// `y` is a nonzero multiple of a nonzero `x`: `ip(x, y)·x = vnorm(x)·y`.
fn same_ray_raw(x: &[GaussianRational], y: &[GaussianRational]) -> Result<bool, Error> {
    let nx = norm(x);
    if nx.is_zero() || norm(y).is_zero() {
        return Ok(false);
    }
    let c = ip(x, y)?;
    let nxg = from_real(&nx)?;
    for (a, b) in x.iter().zip(y) {
        if c.try_mul(a)? != nxg.try_mul(b)? {
            return Ok(false);
        }
    }
    Ok(true)
}

/// `x` and `y` are nonzero and `y = μ·x` (then `μ ≠ 0`): `ip(x, y)·x = vnorm(x)·y`, i.e.
/// `tp(x, y) = 1`.
pub fn same_ray(x: &[GaussianRational], y: &[GaussianRational]) -> Result<bool, Error> {
    let x = hvector(x)?;
    let y = hvector(y)?;
    same_length("same_ray", x.len(), y.len())?;
    same_ray_raw(&x, &y)
}

/// `twist(+1, x) = x`, `twist(−1, x) = conj x` componentwise.
pub fn twist(eps: i8, x: &[GaussianRational]) -> Result<HVector, Error> {
    let eps = sign(eps)?;
    twist_raw(eps, &hvector(x)?)
}

/// `Fᴴ`, the conjugate transpose.
pub fn conj_transpose(f: &[Vec<GaussianRational>]) -> Result<HMatrix, Error> {
    adjoint(&hmatrix(f)?)
}

/// `F·x`.
pub fn mat_vec(f: &[Vec<GaussianRational>], x: &[GaussianRational]) -> Result<HVector, Error> {
    let f = hmatrix(f)?;
    let x = hvector(x)?;
    same_length("mat_vec", f.len(), x.len())?;
    mv(&f, &x)
}

/// `A·B` for square matrices of one size.
pub fn mat_mul(a: &[Vec<GaussianRational>], b: &[Vec<GaussianRational>]) -> Result<HMatrix, Error> {
    let a = hmatrix(a)?;
    let b = hmatrix(b)?;
    same_length("mat_mul", a.len(), b.len())?;
    mm(&a, &b)
}

/// `F·twist(eps, x)`.
pub fn apply(f: &[Vec<GaussianRational>], eps: i8, x: &[GaussianRational]) -> Result<HVector, Error> {
    let f = hmatrix(f)?;
    let eps = sign(eps)?;
    let x = hvector(x)?;
    same_length("apply", f.len(), x.len())?;
    mv(&f, &twist_raw(eps, &x)?)
}

// ============================================================================
// Similarities: certificate, inverse, coordinates in an orthogonal frame
// ============================================================================

/// `Fᴴ F`: entry `(i, j)` is `ip(column i, column j)`.
pub fn gram(f: &[Vec<GaussianRational>]) -> Result<HMatrix, Error> {
    let f = hmatrix(f)?;
    mm(&adjoint(&f)?, &f)
}

/// `Fᴴ F = d·I` with `d = re (Fᴴ F)_00 > 0`, or the first offending entry (row-major) with its
/// expected value `d·δ_ij`; a non-positive `d` makes `(0, 0)` offending (a zero first column
/// is reported with entry and expected value both `0`).
pub fn similarity_certificate(f: &[Vec<GaussianRational>]) -> Result<SimilarityVerdict, Error> {
    let m = gram(f)?;
    let d = m[0][0].real().clone();
    let dg = from_real(&d)?;
    for (i, row) in m.iter().enumerate() {
        for (j, entry) in row.iter().enumerate() {
            let expected = if i == j { dg.clone() } else { g_zero() };
            if *entry != expected || (i == j && !d.is_positive()) {
                return Ok(SimilarityVerdict::NotSimilarity {
                    i,
                    j,
                    entry: entry.clone(),
                    expected,
                });
            }
        }
    }
    Ok(SimilarityVerdict::Similarity { d })
}

/// `F⁻¹ = (1/d)·Fᴴ` of a similarity; refuses a non-similarity with its witness.
pub fn inverse_similarity(f: &[Vec<GaussianRational>]) -> Result<HMatrix, Error> {
    let f = hmatrix(f)?;
    match similarity_certificate(&f)? {
        SimilarityVerdict::Similarity { d } => scale_matrix(&from_real(&d.recip())?, &adjoint(&f)?),
        SimilarityVerdict::NotSimilarity {
            i,
            j,
            entry,
            expected,
        } => Err(Error::NotSimilarity {
            i,
            j,
            entry,
            expected,
        }),
    }
}

/// The diagonal matrix with the given entries.
pub fn diagonal(entries: &[GaussianRational]) -> Result<HMatrix, Error> {
    let v = hvector(entries)?;
    let n = v.len();
    Ok((0..n)
        .map(|i| (0..n).map(|j| if i == j { v[i].clone() } else { g_zero() }).collect())
        .collect())
}

/// `[[a, −conj b], [b, conj a]]`, a similarity of scale `|a|² + |b|²` when `(a, b) ≠ (0, 0)`.
pub fn quaternion_block(a: &GaussianRational, b: &GaussianRational) -> Result<HMatrix, Error> {
    a.validate()?;
    b.validate()?;
    Ok(vec![
        vec![a.clone(), b.try_conj()?.try_neg()?],
        vec![b.clone(), a.try_conj()?],
    ])
}

/// The block-diagonal sum of nonempty square blocks, in order.
pub fn block_diagonal(blocks: &[HMatrix]) -> Result<HMatrix, Error> {
    if blocks.is_empty() {
        return Err(Error::NoBlocks);
    }
    let bs = blocks.iter().map(|b| hmatrix(b)).collect::<Result<Vec<_>, _>>()?;
    let n = bs.iter().map(Vec::len).sum();
    let mut m = vec![vec![g_zero(); n]; n];
    let mut k = 0;
    for b in &bs {
        for (i, row) in b.iter().enumerate() {
            for (j, a) in row.iter().enumerate() {
                m[k + i][k + j] = a.clone();
            }
        }
        k += b.len();
    }
    Ok(m)
}

fn coordinates_raw(basis: &[HVector], y: &[GaussianRational]) -> Result<HVector, Error> {
    let n = basis.len();
    let norms: Vec<Q> = basis.iter().map(|v| norm(v)).collect();
    if let Some(index) = norms.iter().position(|nv| nv.is_zero()) {
        return Err(Error::ZeroBasisVector { index });
    }
    for i in 0..n {
        for j in i + 1..n {
            let c = ip(&basis[i], &basis[j])?;
            if !c.try_is_zero()? {
                return Err(Error::NotOrthogonal { i, j, ip: c });
            }
        }
    }
    let mut z = Vec::with_capacity(n);
    for (v, nv) in basis.iter().zip(&norms) {
        z.push(div_real(&ip(v, y)?, nv)?);
    }
    let mut sum = vec![g_zero(); y.len()];
    for (zk, v) in z.iter().zip(basis) {
        for (s, a) in sum.iter_mut().zip(v) {
            *s = s.try_add(&zk.try_mul(a)?)?;
        }
    }
    if sum.as_slice() != y {
        let mut residual = Vec::with_capacity(y.len());
        for (a, b) in y.iter().zip(&sum) {
            residual.push(a.try_sub(b)?);
        }
        return Err(Error::NotInSpan { residual });
    }
    Ok(z)
}

/// The coordinates `z_i = ip(f_i, y) / vnorm(f_i)` of `y` in a frame of `n` pairwise orthogonal
/// nonzero vectors of length `n`, checked by `Σ z_i f_i = y`; refuses a zero or non-orthogonal
/// frame vector, or a `y` outside the span, with the witness in the error.
pub fn coordinates(f: &[HVector], y: &[GaussianRational]) -> Result<HVector, Error> {
    let n = f.len();
    if n == 0 {
        return Err(Error::EmptyVector);
    }
    let mut basis = Vec::with_capacity(n);
    for v in f {
        let v = hvector(v)?;
        same_length("coordinates", n, v.len())?;
        basis.push(v);
    }
    let y = hvector(y)?;
    same_length("coordinates", n, y.len())?;
    coordinates_raw(&basis, &y)
}

// ============================================================================
// The finite Wigner reconstruction (steps 1-5 of the Lean proof)
// ============================================================================

/// `T(x)`, re-admitted as a vector of length `n`.
fn image_of(t: RayMap<'_>, x: &HVector, n: usize) -> Result<HVector, Error> {
    let y = hvector(&t(x)?)?;
    same_length("ray map image", n, y.len())?;
    Ok(y)
}

/// `e_i0 + c·e_j` (`i0 ≠ j`, both in range).
fn pair_probe(n: usize, i0: usize, j: usize, c: GaussianRational) -> HVector {
    let mut v = vec![g_zero(); n];
    v[i0] = g_one();
    v[j] = c;
    v
}

/// `e_i0 + c·e_j` for `j ≠ i0`: the probes `e_i0 + e_j` (step 2) and `e_i0 + i·e_j` (step 3).
pub fn probe(n: usize, i0: usize, j: usize, c: &GaussianRational) -> Result<HVector, Error> {
    index_in(i0, n)?;
    index_in(j, n)?;
    c.validate()?;
    if i0 == j {
        return Err(Error::IndicesNotDistinct);
    }
    Ok(pair_probe(n, i0, j, c.clone()))
}

/// The probes of steps 1–3: every `e_m`, then `e_i0 + e_j` and `e_i0 + i·e_j` for every
/// `j ≠ i0`.
pub fn reconstruction_probes(n: usize, i0: usize) -> Result<Vec<HVector>, Error> {
    if n == 0 {
        return Err(Error::EmptyVector);
    }
    index_in(i0, n)?;
    let one = g_one();
    let others: Vec<usize> = (0..n).filter(|&j| j != i0).collect();
    let mut out = Vec::with_capacity(3 * n - 2);
    for m in 0..n {
        out.push(unit_vector(n, m, &one)?);
    }
    out.extend(others.iter().map(|&j| pair_probe(n, i0, j, g_one())));
    out.extend(others.iter().map(|&j| pair_probe(n, i0, j, gi())));
    Ok(out)
}

/// The step-4 pair `(e_i0 + i·e_j + i·e_k, e_i0 + e_j + e_k)` with `tp = 5/9`; the images
/// forced by `eps_j ≠ eps_k` have `tp = 1/9`.
pub fn consistency_probes(n: usize, i0: usize, j: usize, k: usize) -> Result<(HVector, HVector), Error> {
    for index in [i0, j, k] {
        index_in(index, n)?;
    }
    if i0 == j || i0 == k || j == k {
        return Err(Error::IndicesNotDistinct);
    }
    let mut phased = pair_probe(n, i0, j, gi());
    phased[k] = gi();
    let mut flat = pair_probe(n, i0, j, g_one());
    flat[k] = g_one();
    Ok((phased, flat))
}

/// The failure of coordinates that must be `a·e_i0 + b·e_j` with `a, b ≠ 0`: the first
/// nonzero coordinate outside `{i0, j}`, else a vanishing `a` or `b`.
fn two_term(
    z: &[GaussianRational],
    i0: usize,
    j: usize,
    phase: bool,
) -> Result<Option<AlignmentFailure>, Error> {
    for (k, c) in z.iter().enumerate() {
        if k != i0 && k != j && !c.try_is_zero()? {
            let z_k = c.clone();
            return Ok(Some(if phase {
                AlignmentFailure::PhaseSupport { k, z_k }
            } else {
                AlignmentFailure::Support { k, z_k }
            }));
        }
    }
    if z[i0].try_is_zero()? || z[j].try_is_zero()? {
        let (a, b) = (z[i0].clone(), z[j].clone());
        return Ok(Some(if phase {
            AlignmentFailure::PhaseVanishing { a, b }
        } else {
            AlignmentFailure::Vanishing { a, b }
        }));
    }
    Ok(None)
}

fn refused(w: TpWitness) -> Result<ReconstructionVerdict, Error> {
    Ok(ReconstructionVerdict::NotTpPreserving(w))
}

/// The finite Wigner theorem replayed on a supplied map `t` of `ℚ(i)ⁿ` with reference index
/// `i0`:
///
/// 1. `g_i = T e_i`, nonzero and pairwise orthogonal;
/// 2. for `j ≠ i0`, `h_j = T(e_i0 + e_j) = a·g_i0 + b·g_j` with `a, b ≠ 0` and
///    `|a|²·vnorm(g_i0) = |b|²·vnorm(g_j)`; `f_i0 = g_i0`, `f_j = (b/a)·g_j`, so every
///    `vnorm(f_j) = d := vnorm(g_i0)` and `h_j = a·(f_i0 + f_j)`;
/// 3. for `j ≠ i0`, `T(e_i0 + i·e_j) = a'·f_i0 + b'·f_j` with `a', b' ≠ 0` and
///    `u = b'/a' ∈ {i, −i}`, giving `eps_j = +1` for `u = i` and `−1` for `u = −i`;
/// 4. every `eps_j` equals `eps_j0`, `j0` the first index `≠ i0` (`eps = +1` when `n = 1`);
///    a disagreement is refuted by [`consistency_probes`];
/// 5. `F` has columns `f_0, …, f_{n−1}` and `Fᴴ F = d·I`.
///
/// Returns `(F, d, eps)` or the witness of the first failed probe among
/// [`reconstruction_probes`]. For `T x = c(x)·F0·twist(eps, x)` the result is `F = λ·F0`,
/// `d = |λ|²·d0` with `λ = c(e_i0)`. Only these probes are evaluated: a reconstructed triple is
/// a necessary condition, checked further on samples by [`verify_induced`].
pub fn reconstruct(t: RayMap<'_>, n: usize, i0: usize) -> Result<ReconstructionVerdict, Error> {
    if n == 0 {
        return Err(Error::EmptyVector);
    }
    index_in(i0, n)?;
    let one = g_one();
    // Step 1: the images of the unit vectors.
    let mut g: Vec<HVector> = Vec::with_capacity(n);
    for k in 0..n {
        let probe = unit_vector(n, k, &one)?;
        let image = image_of(t, &probe, n)?;
        if norm(&image).is_zero() {
            return refused(TpWitness::ZeroImage { probe });
        }
        g.push(image);
    }
    for i in 0..n {
        for j in i + 1..n {
            let c = ip(&g[i], &g[j])?;
            if !c.try_is_zero()? {
                return refused(TpWitness::Orthogonality { i, j, ip: c });
            }
        }
    }
    let others: Vec<usize> = (0..n).filter(|&j| j != i0).collect();
    // Step 2: align the frame through the probes e_i0 + e_j.
    let mut f = g.clone();
    for &j in &others {
        let probe = pair_probe(n, i0, j, g_one());
        let h = image_of(t, &probe, n)?;
        if norm(&h).is_zero() {
            return refused(TpWitness::ZeroImage { probe });
        }
        let z = coordinates_raw(&g, &h)?;
        if let Some(failure) = two_term(&z, i0, j, false)? {
            return refused(TpWitness::Alignment {
                j,
                failure,
                probe,
                coordinates: z,
            });
        }
        let lhs = z[i0].norm_sq() * norm(&g[i0]);
        let rhs = z[j].norm_sq() * norm(&g[j]);
        if lhs != rhs {
            return refused(TpWitness::Alignment {
                j,
                failure: AlignmentFailure::Balance { lhs, rhs },
                probe,
                coordinates: z,
            });
        }
        f[j] = scale_vector(&z[j].try_div(&z[i0])?, &g[j])?;
    }
    let d = norm(&g[i0]);
    // Step 3: the relative phase of the probes e_i0 + i e_j.
    let mut signs: Vec<(usize, i8)> = Vec::with_capacity(others.len());
    for &j in &others {
        let probe = pair_probe(n, i0, j, gi());
        let image = image_of(t, &probe, n)?;
        if norm(&image).is_zero() {
            return refused(TpWitness::ZeroImage { probe });
        }
        let z = coordinates_raw(&f, &image)?;
        if let Some(failure) = two_term(&z, i0, j, true)? {
            return refused(TpWitness::Alignment {
                j,
                failure,
                probe,
                coordinates: z,
            });
        }
        let u = z[j].try_div(&z[i0])?;
        if u.norm_sq() != q(1) || g_one().try_add(&u)?.norm_sq() != q(2) {
            return refused(TpWitness::Sign { j, probe, u });
        }
        signs.push((j, if u == gi() { 1 } else { -1 }));
    }
    // Step 4: one sign for all coordinates.
    let eps = match signs.first() {
        None => 1,
        Some(&(j, eps_j)) => {
            for &(k, eps_k) in &signs[1..] {
                if eps_k != eps_j {
                    let (probe, _) = consistency_probes(n, i0, j, k)?;
                    return refused(TpWitness::Consistency {
                        j,
                        k,
                        eps_j,
                        eps_k,
                        probe,
                    });
                }
            }
            eps_j
        }
    };
    // Step 5: F[r][c] = f_c[r].
    let matrix: HMatrix = (0..n)
        .map(|r| (0..n).map(|c| f[c][r].clone()).collect())
        .collect();
    debug_assert!(matches!(
        similarity_certificate(&matrix),
        Ok(SimilarityVerdict::Similarity { d: ref s }) if *s == d
    ));
    Ok(ReconstructionVerdict::Reconstructed { f: matrix, d, eps })
}

/// For every (nonzero, admitted) sample `x`, `T x` is a nonzero multiple of `F·twist(eps, x)`
/// (exact cross check `ip(w, Tx)·w = vnorm(w)·Tx`), or the first sample where it is not.
/// Refuses a zero sample.
pub fn verify_induced(
    t: RayMap<'_>,
    f: &[Vec<GaussianRational>],
    eps: i8,
    samples: &[HVector],
) -> Result<InducedVerdict, Error> {
    let f = hmatrix(f)?;
    let eps = sign(eps)?;
    let n = f.len();
    let mut xs = Vec::with_capacity(samples.len());
    for x in samples {
        let x = hvector(x)?;
        same_length("verify_induced", n, x.len())?;
        if norm(&x).is_zero() {
            return Err(Error::ZeroVector);
        }
        xs.push(x);
    }
    for x in xs {
        let direction = mv(&f, &twist_raw(eps, &x)?)?;
        let image = image_of(t, &x, n)?;
        if !same_ray_raw(&direction, &image)? {
            return Ok(InducedVerdict::NotInduced {
                x,
                image,
                direction,
            });
        }
    }
    Ok(InducedVerdict::Induced)
}

/// `tp(T x, T y) = tp(x, y)` for every pair of supplied nonzero probes, or the first probe with
/// a zero image, or the first offending pair (in probe order) with both values.
pub fn tp_defect(t: RayMap<'_>, probes: &[HVector]) -> Result<TpDefectVerdict, Error> {
    let mut xs = Vec::with_capacity(probes.len());
    for x in probes {
        let x = hvector(x)?;
        if norm(&x).is_zero() {
            return Err(Error::ZeroVector);
        }
        xs.push(x);
    }
    let mut ys = Vec::with_capacity(xs.len());
    for x in &xs {
        let y = image_of(t, x, x.len())?;
        if norm(&y).is_zero() {
            return Ok(TpDefectVerdict::ZeroImage { x: x.clone() });
        }
        ys.push(y);
    }
    for a in 0..xs.len() {
        for b in a + 1..xs.len() {
            let before = transition_probability(&xs[a], &xs[b])?;
            let after = tp_raw(&ys[a], &ys[b])?;
            if before != after {
                return Ok(TpDefectVerdict::TpDefect {
                    x: xs[a].clone(),
                    y: xs[b].clone(),
                    before,
                    after,
                });
            }
        }
    }
    Ok(TpDefectVerdict::TpPreserved)
}

/// The deterministic nonzero ray scalar of the Python twin,
/// `c(x) = (1 + s mod 2) + ((s mod 3) − 1)·i` with
/// `s = Σ_k (k + 1)·(num re x_k + 2·num im x_k)` (numerators in lowest terms, floor residues).
pub fn ray_scalar(x: &[GaussianRational]) -> Result<GaussianRational, Error> {
    let x = hvector(x)?;
    let mut s = BigInt::from(0);
    for (k, z) in x.iter().enumerate() {
        s += BigInt::from(k + 1) * (z.real().numer() + BigInt::from(2) * z.imag().numer());
    }
    let re = BigInt::from(1) + s.mod_floor(&BigInt::from(2));
    let im = s.mod_floor(&BigInt::from(3)) - BigInt::from(1);
    Ok(GaussianRational::new(Q::from_integer(re), Q::from_integer(im))?)
}

/// The ray map `T x = c(x)·F·twist(eps, x)` with the ray scalar [`ray_scalar`], exercising the
/// ray freedom; transition-probability preserving whenever `F` is a similarity.
pub fn induced_ray_map(f: &[Vec<GaussianRational>], eps: i8) -> Result<BoxedRayMap, Error> {
    let f = hmatrix(f)?;
    let eps = sign(eps)?;
    Ok(Box::new(move |x: &HVector| {
        let x = hvector(x)?;
        same_length("induced_ray_map", f.len(), x.len())?;
        scale_vector(&ray_scalar(&x)?, &mv(&f, &twist_raw(eps, &x)?)?)
    }))
}

// ============================================================================
// Unitary normalisation: sums of two rational squares
// ============================================================================

/// Trial-division factorisation of `m ≥ 1` into increasing primes with exponents.
fn factorise(m: &BigInt) -> Vec<(BigInt, u64)> {
    let mut m = m.clone();
    let mut out = Vec::new();
    let mut p = BigInt::from(2);
    while &p * &p <= m {
        let mut e = 0u64;
        while (&m % &p).is_zero() {
            m /= &p;
            e += 1;
        }
        if e > 0 {
            out.push((p.clone(), e));
        }
        p += 1u32;
    }
    if m > BigInt::from(1) {
        out.push((m, 1));
    }
    out
}

/// `p = s² + t²` with the least `s ≥ 1` (bounded search `s² ≤ p`).
fn fermat_pair(p: &BigInt) -> Result<(BigInt, BigInt), Error> {
    let mut s = BigInt::from(1);
    while &s * &s <= *p {
        let r = p - &s * &s;
        let t = Roots::sqrt(&r);
        if &t * &t == r {
            return Ok((s, t));
        }
        s += 1u32;
    }
    Err(Error::NoFermatRepresentation(p.clone()))
}

/// `d = a² + b²` with rational `a, b ≥ 0`, or the smallest prime `p ≡ 3 (mod 4)` dividing
/// `num·den` (lowest terms) to an odd power. The witness composes, prime by prime in
/// increasing order, `2 = 1² + 1²`, the Fermat pair of each prime `≡ 1 (mod 4)` and `p² = p² + 0²`
/// for each pair of primes `≡ 3 (mod 4)` by the Brahmagupta–Fibonacci identity
/// `(x² + y²)(s² + t²) = (xs − yt)² + (xt + ys)²`, giving `X² + Y² = num·den`, then
/// `(a, b) = (|X|, |Y|)/den`. Refuses a non-positive `d`.
pub fn sum_of_two_rational_squares(d: &Q) -> Result<TwoSquaresVerdict, Error> {
    validate_rational(d)?;
    if !d.is_positive() {
        return Err(Error::NonPositiveScale(d.clone()));
    }
    let den = d.denom().clone();
    let factors = factorise(&(d.numer() * &den));
    let four = BigInt::from(4);
    let three = BigInt::from(3);
    for (p, e) in &factors {
        if p.mod_floor(&four) == three && e % 2 == 1 {
            return Ok(TwoSquaresVerdict::NotRepresentable { p: p.clone() });
        }
    }
    let (mut x, mut y) = (BigInt::from(1), BigInt::from(0));
    for (p, e) in &factors {
        let (s, t, times) = if *p == BigInt::from(2) {
            (BigInt::from(1), BigInt::from(1), *e)
        } else if p.mod_floor(&four) == three {
            (p.clone(), BigInt::from(0), e / 2)
        } else {
            let (s, t) = fermat_pair(p)?;
            (s, t, *e)
        };
        for _ in 0..times {
            let nx = &x * &s - &y * &t;
            let ny = &x * &t + &y * &s;
            x = nx;
            y = ny;
        }
    }
    let a = Q::new(x.abs(), den.clone());
    let b = Q::new(y.abs(), den);
    debug_assert!(&a * &a + &b * &b == *d);
    Ok(TwoSquaresVerdict::Representable { a, b })
}

/// `F = c·U` with `U` unitary (`Uᴴ U = I`) iff the scale `d` of the similarity `F` is a norm
/// `|c|²` from `ℚ(i)`; otherwise the obstructing prime, or the similarity witness.
pub fn unitary_normalisation(f: &[Vec<GaussianRational>]) -> Result<UnitaryVerdict, Error> {
    let f = hmatrix(f)?;
    let d = match similarity_certificate(&f)? {
        SimilarityVerdict::Similarity { d } => d,
        SimilarityVerdict::NotSimilarity {
            i,
            j,
            entry,
            expected,
        } => {
            return Ok(UnitaryVerdict::NotSimilarity {
                i,
                j,
                entry,
                expected,
            })
        }
    };
    match sum_of_two_rational_squares(&d)? {
        TwoSquaresVerdict::NotRepresentable { p } => Ok(UnitaryVerdict::NotANorm { d, p }),
        TwoSquaresVerdict::Representable { a, b } => {
            let c = GaussianRational::new(a, b)?;
            let u = scale_matrix(&c.try_inv()?, &f)?;
            debug_assert!(matches!(
                similarity_certificate(&u),
                Ok(SimilarityVerdict::Similarity { d: ref one }) if *one == q(1)
            ));
            Ok(UnitaryVerdict::Unitary { c, u })
        }
    }
}

// ============================================================================
// Named matrices
// ============================================================================

/// The permutation matrix `P_σ` with `P_σ e_j = e_{σ(j)}`, so `P_σ x = permute(σ, x)`
/// (`(permute σ x)[i] = x[σ⁻¹(i)]`, the H006 envelope); unitary (`d = 1`).
pub fn permutation_matrix(sigma: &[usize]) -> Result<HMatrix, Error> {
    let n = sigma.len();
    let mut seen = vec![false; n];
    if n == 0 {
        return Err(Error::NotAPermutation(0));
    }
    for &k in sigma {
        if k >= n || seen[k] {
            return Err(Error::NotAPermutation(n));
        }
        seen[k] = true;
    }
    Ok((0..n)
        .map(|i| {
            (0..n)
                .map(|j| if sigma[j] == i { g_one() } else { g_zero() })
                .collect()
        })
        .collect())
}

/// `F3 = [[1, −1+i], [1+i, 1]]` with `F3ᴴ F3 = 3·I`: 3 is not a sum of two rational squares,
/// so the ray map of `F3` is induced by no `ℚ(i)`-unitary or antiunitary.
pub fn f3() -> HMatrix {
    vec![
        vec![g_one(), GaussianRational::from_integers(-1, 1)],
        vec![GaussianRational::from_integers(1, 1), g_one()],
    ]
}

/// `[[1, 1], [1, −1]]` with scale `2 = |1 + i|²`, so `hadamard2 / (1 + i)` is unitary.
pub fn hadamard2() -> HMatrix {
    vec![
        vec![g_one(), g_one()],
        vec![g_one(), GaussianRational::from_integers(-1, 0)],
    ]
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::qm::inner_product_uniqueness::{all_permutations, permute};

    fn fr(a: i64, b: i64) -> Q {
        Q::new(BigInt::from(a), BigInt::from(b))
    }

    fn gq(re: i64, im: i64) -> GaussianRational {
        GaussianRational::from_integers(re, im)
    }

    fn e(n: usize, i: usize) -> HVector {
        unit_vector(n, i, &gq(1, 0)).unwrap()
    }

    fn v(entries: &[(i64, i64)]) -> HVector {
        entries.iter().map(|&(a, b)| gq(a, b)).collect()
    }

    /// Deterministic linear congruential source for small fixture integers.
    struct Lcg(u64);
    impl Lcg {
        fn next(&mut self) -> u64 {
            self.0 = self.0.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);
            self.0 >> 33
        }
        fn int(&mut self, lo: i64, hi: i64) -> i64 {
            lo + (self.next() % ((hi - lo + 1) as u64)) as i64
        }
        fn rat(&mut self) -> Q {
            fr(self.int(-4, 4), self.int(1, 3))
        }
        fn gauss(&mut self) -> GaussianRational {
            GaussianRational::new(self.rat(), self.rat()).unwrap()
        }
        fn nonzero_gauss(&mut self) -> GaussianRational {
            loop {
                let z = self.gauss();
                if !z.norm_sq().is_zero() {
                    return z;
                }
            }
        }
        fn vector(&mut self, n: usize) -> HVector {
            loop {
                let x: HVector = (0..n).map(|_| self.gauss()).collect();
                if !norm(&x).is_zero() {
                    return x;
                }
            }
        }
        fn phase(&mut self) -> GaussianRational {
            [gq(1, 0), gq(0, 1), gq(-1, 0), gq(0, -1)][self.int(0, 3) as usize].clone()
        }
        fn perm(&mut self, n: usize) -> Vec<usize> {
            let mut p: Vec<usize> = (0..n).collect();
            for k in (1..n).rev() {
                p.swap(k, self.int(0, k as i64) as usize);
            }
            p
        }
    }

    fn diag(entries: &[GaussianRational]) -> HMatrix {
        diagonal(entries).unwrap()
    }

    fn phases(r: &mut Lcg, n: usize) -> HMatrix {
        let p: Vec<GaussianRational> = (0..n).map(|_| r.phase()).collect();
        diag(&p)
    }

    /// `λ·(P D) B (D' P')` with `B` block diagonal of 2×2 blocks `[[a, −conj b], [b, conj a]]`
    /// (and a 1×1 block `c` for odd `n`) of one scale `s² + t²`, `P, P'` permutation matrices
    /// and `D, D'` diagonal unit phases; returns the matrix and its predicted scale.
    fn block_similarity(r: &mut Lcg, n: usize) -> (HMatrix, Q) {
        let (s, t) = loop {
            let s = r.int(0, 3);
            let t = r.int(0, 3);
            if s != 0 || t != 0 {
                break (s, t);
            }
        };
        let mut blocks = Vec::new();
        for _ in 0..n / 2 {
            let (x, y) = if r.int(0, 1) == 0 { (s, t) } else { (t, s) };
            let a = r.phase().try_mul(&gq(x, 0)).unwrap();
            let c = r.phase().try_mul(&gq(y, 0)).unwrap();
            blocks.push(quaternion_block(&a, &c).unwrap());
        }
        if n % 2 == 1 {
            blocks.push(vec![vec![r.phase().try_mul(&gq(s, t)).unwrap()]]);
        }
        let b = block_diagonal(&blocks).unwrap();
        let lam = r.nonzero_gauss();
        let left = mat_mul(&permutation_matrix(&r.perm(n)).unwrap(), &phases(r, n)).unwrap();
        let right = mat_mul(&phases(r, n), &permutation_matrix(&r.perm(n)).unwrap()).unwrap();
        let m = mat_mul(&mat_mul(&left, &b).unwrap(), &right).unwrap();
        (scale_matrix(&lam, &m).unwrap(), q(s * s + t * t) * lam.norm_sq())
    }

    /// The identity map except `T(special) = value`.
    fn patched(
        special: HVector,
        value: HVector,
    ) -> impl Fn(&HVector) -> Result<HVector, FiniteWignerError> {
        move |x: &HVector| if *x == special { Ok(value.clone()) } else { Ok(x.clone()) }
    }

    fn samples(r: &mut Lcg, n: usize, count: usize) -> Vec<HVector> {
        let mut out = vec![e(n, 0)];
        if n >= 2 {
            out.push(pair_probe(n, 0, 1, gi()));
            out.push(pair_probe(n, 0, 1, gq(1, 0)));
        }
        out.extend((0..count).map(|_| r.vector(n)));
        out
    }

    #[test]
    fn named_matrices_are_similarities_with_the_stated_scales() {
        assert_eq!(similarity_certificate(&f3()).unwrap(), SimilarityVerdict::Similarity { d: q(3) });
        assert_eq!(similarity_certificate(&hadamard2()).unwrap(), SimilarityVerdict::Similarity { d: q(2) });
        assert_eq!(
            mat_mul(&conj_transpose(&f3()).unwrap(), &f3()).unwrap(),
            scale_matrix(&gq(3, 0), &identity(2)).unwrap()
        );
        let mut r = Lcg(1);
        for n in 1..=4 {
            for s in all_permutations(n) {
                let p = permutation_matrix(&s).unwrap();
                assert_eq!(similarity_certificate(&p).unwrap(), SimilarityVerdict::Similarity { d: q(1) });
                let x = r.vector(n);
                assert_eq!(mat_vec(&p, &x).unwrap(), permute(&s, &x).unwrap());
                for j in 0..n {
                    assert_eq!(mat_vec(&p, &e(n, j)).unwrap(), e(n, s[j]));
                }
            }
        }
    }

    #[test]
    fn block_built_similarities_have_the_predicted_scale() {
        let mut r = Lcg(2);
        for n in 1..=4 {
            for _ in 0..12 {
                let (f, d) = block_similarity(&mut r, n);
                assert_eq!(similarity_certificate(&f).unwrap(), SimilarityVerdict::Similarity { d: d.clone() });
                assert_eq!(
                    mat_mul(&conj_transpose(&f).unwrap(), &f).unwrap(),
                    scale_matrix(&from_real(&d).unwrap(), &identity(n)).unwrap()
                );
            }
        }
    }

    #[test]
    fn products_of_similarities_multiply_the_scales() {
        let mut r = Lcg(3);
        assert_eq!(
            similarity_certificate(&mat_mul(&f3(), &hadamard2()).unwrap()).unwrap(),
            SimilarityVerdict::Similarity { d: q(6) }
        );
        for n in 1..=4 {
            for _ in 0..5 {
                let (a, da) = block_similarity(&mut r, n);
                let (b, db) = block_similarity(&mut r, n);
                let p = permutation_matrix(&r.perm(n)).unwrap();
                let prod = mat_mul(&mat_mul(&a, &p).unwrap(), &b).unwrap();
                assert_eq!(similarity_certificate(&prod).unwrap(), SimilarityVerdict::Similarity { d: da * db });
            }
        }
    }

    #[test]
    fn non_similarities_are_refused_with_the_first_offending_entry() {
        let diag12 = diag(&[gq(1, 0), gq(2, 0)]);
        let shear = vec![v(&[(1, 0), (1, 0)]), v(&[(0, 0), (1, 0)])];
        let zero_column = vec![v(&[(0, 0), (1, 0)]), v(&[(0, 0), (0, 0)])];
        let cases = [
            (diag12, (1, 1, gq(4, 0), gq(1, 0))),
            (shear, (0, 1, gq(1, 0), gq(0, 0))),
            (zero_column, (0, 0, gq(0, 0), gq(0, 0))),
        ];
        for (m, (i, j, entry, expected)) in cases {
            let verdict = similarity_certificate(&m).unwrap();
            assert_eq!(verdict.tag(), "not_similarity");
            assert_eq!(verdict, SimilarityVerdict::NotSimilarity { i, j, entry, expected });
        }
        assert_eq!(
            similarity_certificate(&[vec![gq(0, 0)]]).unwrap(),
            SimilarityVerdict::NotSimilarity { i: 0, j: 0, entry: gq(0, 0), expected: gq(0, 0) }
        );
    }

    #[test]
    fn transition_probability_properties() {
        let mut r = Lcg(4);
        for n in 1..=4 {
            for i in 0..n {
                for j in 0..n {
                    let expected = if i == j { q(1) } else { q(0) };
                    assert_eq!(transition_probability(&e(n, i), &e(n, j)).unwrap(), expected);
                }
            }
            for _ in 0..15 {
                let x = r.vector(n);
                let y = r.vector(n);
                let t = transition_probability(&x, &y).unwrap();
                assert!(t >= q(0) && t <= q(1));
                assert_eq!(transition_probability(&y, &x).unwrap(), t);
                assert_eq!(transition_probability(&x, &x).unwrap(), q(1));
                let a = r.nonzero_gauss();
                let b = r.nonzero_gauss();
                let ax = scale_vector(&a, &x).unwrap();
                let by = scale_vector(&b, &y).unwrap();
                assert_eq!(transition_probability(&ax, &by).unwrap(), t);
                assert_eq!(transition_probability(&x, &ax).unwrap(), q(1));
                assert_eq!(
                    t.clone(),
                    inner(&x, &y).unwrap().norm_sq() / (vnorm(&x).unwrap() * vnorm(&y).unwrap())
                );
                assert_eq!(t.is_zero(), inner(&x, &y).unwrap().try_is_zero().unwrap());
            }
        }
        assert_eq!(transition_probability(&v(&[(1, 0), (1, 0)]), &v(&[(1, 0), (0, 0)])).unwrap(), fr(1, 2));
        assert_eq!(transition_probability(&v(&[(1, 0), (0, 1)]), &v(&[(1, 0), (0, -1)])).unwrap(), q(0));
    }

    #[test]
    fn born_transition_reads_the_rank_one_effect() {
        let mut r = Lcg(5);
        for n in 1..=4 {
            for _ in 0..10 {
                let x = r.vector(n);
                let y = r.vector(n);
                assert_eq!(born_transition(&x, &y).unwrap(), transition_probability(&x, &y).unwrap());
                let p = rank_one_effect(&x).unwrap();
                assert_eq!(mat_mul(&p, &p).unwrap(), p);
                assert_eq!(conj_transpose(&p).unwrap(), p);
                assert_eq!(mat_vec(&p, &x).unwrap(), x);
            }
        }
    }

    #[test]
    fn zero_vectors_and_shapes_are_refused() {
        let z = v(&[(0, 0), (0, 0)]);
        let x = v(&[(1, 0), (0, 1)]);
        assert_eq!(transition_probability(&z, &x), Err(Error::ZeroVector));
        assert_eq!(transition_probability(&x, &z), Err(Error::ZeroVector));
        assert_eq!(born_transition(&z, &x), Err(Error::ZeroVector));
        assert_eq!(born_transition(&x, &z), Err(Error::ZeroVector));
        assert_eq!(rank_one_effect(&z), Err(Error::ZeroVector));
        assert!(matches!(
            transition_probability(&x, &v(&[(1, 0)])),
            Err(Error::DimensionMismatch { expected: 2, got: 1, .. })
        ));
        assert!(matches!(inner(&x, &v(&[(1, 0)])), Err(Error::DimensionMismatch { .. })));
        assert_eq!(inner(&[], &[]), Err(Error::EmptyVector));
        assert_eq!(vnorm(&[]), Err(Error::EmptyVector));
        assert!(matches!(mat_vec(&f3(), &v(&[(1, 0)])), Err(Error::DimensionMismatch { .. })));
        assert!(matches!(apply(&f3(), 1, &v(&[(1, 0); 3])), Err(Error::DimensionMismatch { .. })));
        assert!(matches!(mat_mul(&f3(), &identity(3)), Err(Error::DimensionMismatch { .. })));
        assert_eq!(hmatrix(&[v(&[(1, 0), (0, 0)])]), Err(Error::NonSquareMatrix));
        assert_eq!(hmatrix(&[]), Err(Error::NonSquareMatrix));
        assert_eq!(conj_transpose(&[v(&[(1, 0), (2, 0)])]), Err(Error::NonSquareMatrix));
        assert_eq!(similarity_certificate(&[]), Err(Error::NonSquareMatrix));
    }

    #[test]
    fn similarities_preserve_tp_for_both_twists() {
        let mut r = Lcg(6);
        for n in 1..=4 {
            for _ in 0..8 {
                let (f, d) = block_similarity(&mut r, n);
                let dg = from_real(&d).unwrap();
                let x = r.vector(n);
                let y = r.vector(n);
                let tp = transition_probability(&x, &y).unwrap();
                let fx = mat_vec(&f, &x).unwrap();
                let fy = mat_vec(&f, &y).unwrap();
                assert_eq!(inner(&fx, &fy).unwrap(), dg.try_mul(&inner(&x, &y).unwrap()).unwrap());
                assert_eq!(vnorm(&fx).unwrap(), &d * vnorm(&x).unwrap());
                let cx = twist(-1, &x).unwrap();
                let cy = twist(-1, &y).unwrap();
                assert_eq!(transition_probability(&cx, &cy).unwrap(), tp);
                for eps in [1i8, -1] {
                    let ax = apply(&f, eps, &x).unwrap();
                    let ay = apply(&f, eps, &y).unwrap();
                    assert_eq!(transition_probability(&ax, &ay).unwrap(), tp);
                    let t = induced_ray_map(&f, eps).unwrap();
                    assert_eq!(transition_probability(&t(&x).unwrap(), &t(&y).unwrap()).unwrap(), tp);
                }
            }
        }
    }

    #[test]
    fn reconstruct_recovers_the_similarity_up_to_the_ray_scalar() {
        let mut r = Lcg(7);
        for n in 1..=4 {
            for eps in [1i8, -1] {
                for i0 in 0..n {
                    for _ in 0..2 {
                        let (f, d) = block_similarity(&mut r, n);
                        let t = induced_ray_map(&f, eps).unwrap();
                        let lam = ray_scalar(&e(n, i0)).unwrap();
                        assert!(!lam.norm_sq().is_zero());
                        let verdict = reconstruct(&t, n, i0).unwrap();
                        assert_eq!(verdict.tag(), "reconstructed");
                        let ReconstructionVerdict::Reconstructed { f: f2, d: d2, eps: eps2 } = verdict else {
                            panic!("an induced ray map is reconstructed");
                        };
                        assert_eq!(f2, scale_matrix(&lam, &f).unwrap());
                        assert_eq!(d2, &d * lam.norm_sq());
                        assert_eq!(eps2, if n == 1 { 1 } else { eps });
                        assert_eq!(similarity_certificate(&f2).unwrap(), SimilarityVerdict::Similarity { d: d2 });
                        let xs = samples(&mut r, n, 6);
                        assert_eq!(verify_induced(&t, &f2, eps2, &xs).unwrap(), InducedVerdict::Induced);
                    }
                }
            }
        }
    }

    #[test]
    fn verify_induced_detects_a_wrong_sign_and_a_wrong_matrix() {
        let mut r = Lcg(8);
        for n in 2..=4 {
            for eps in [1i8, -1] {
                let (f, _) = block_similarity(&mut r, n);
                let t = induced_ray_map(&f, eps).unwrap();
                let ReconstructionVerdict::Reconstructed { f: f2, eps: eps2, .. } = reconstruct(&t, n, 0).unwrap()
                else {
                    panic!("an induced ray map is reconstructed");
                };
                let xs = samples(&mut r, n, 4);
                let wrong_sign = verify_induced(&t, &f2, -eps2, &xs).unwrap();
                assert_eq!(wrong_sign.tag(), "not_induced");
                let InducedVerdict::NotInduced { x, image, direction } = wrong_sign else {
                    panic!("the conjugate twist is not induced");
                };
                assert_eq!(x, pair_probe(n, 0, 1, gi()));
                assert_eq!(image, t(&x).unwrap());
                assert_eq!(direction, apply(&f2, -eps2, &x).unwrap());
                let mut stretch = vec![gq(1, 0); n];
                stretch[1] = gq(2, 0);
                let wrong_matrix = mat_mul(&f2, &diag(&stretch)).unwrap();
                assert!(matches!(
                    verify_induced(&t, &wrong_matrix, eps2, &[e(n, 0), pair_probe(n, 0, 1, gq(1, 0))]).unwrap(),
                    InducedVerdict::NotInduced { x, .. } if x == pair_probe(n, 0, 1, gq(1, 0))
                ));
            }
        }
    }

    #[test]
    fn diagonal_rescaling_is_refused_with_an_alignment_witness() {
        let d12 = diag(&[gq(1, 0), gq(2, 0)]);
        let t = move |x: &HVector| mat_vec(&d12, x);
        let verdict = reconstruct(&t, 2, 0).unwrap();
        assert_eq!(verdict.tag(), "not_tp_preserving");
        let ReconstructionVerdict::NotTpPreserving(w) = verdict else {
            panic!("diag(1, 2) is refused");
        };
        assert_eq!(w.tag(), "alignment");
        assert_eq!(
            w,
            TpWitness::Alignment {
                j: 1,
                failure: AlignmentFailure::Balance { lhs: q(1), rhs: q(4) },
                probe: v(&[(1, 0), (1, 0)]),
                coordinates: v(&[(1, 0), (1, 0)]),
            }
        );
        if let TpWitness::Alignment { failure, .. } = &w {
            assert_eq!(failure.kind(), "balance");
        }
        assert_eq!(
            reconstruct(&t, 2, 1).unwrap(),
            ReconstructionVerdict::NotTpPreserving(TpWitness::Alignment {
                j: 0,
                failure: AlignmentFailure::Balance { lhs: q(4), rhs: q(1) },
                probe: v(&[(1, 0), (1, 0)]),
                coordinates: v(&[(1, 0), (1, 0)]),
            })
        );
        let tp_before = transition_probability(&e(2, 0), &v(&[(1, 0), (1, 0)])).unwrap();
        let tp_after = transition_probability(&t(&e(2, 0)).unwrap(), &t(&v(&[(1, 0), (1, 0)])).unwrap()).unwrap();
        assert_eq!((tp_before, tp_after), (fr(1, 2), fr(1, 5)));
        let leak = patched(v(&[(1, 0), (1, 0), (0, 0)]), v(&[(1, 0), (1, 0), (1, 0)]));
        assert_eq!(
            reconstruct(&leak, 3, 0).unwrap(),
            ReconstructionVerdict::NotTpPreserving(TpWitness::Alignment {
                j: 1,
                failure: AlignmentFailure::Support { k: 2, z_k: gq(1, 0) },
                probe: v(&[(1, 0), (1, 0), (0, 0)]),
                coordinates: v(&[(1, 0), (1, 0), (1, 0)]),
            })
        );
        let flat = patched(v(&[(1, 0), (1, 0)]), v(&[(1, 0), (0, 0)]));
        assert_eq!(
            reconstruct(&flat, 2, 0).unwrap(),
            ReconstructionVerdict::NotTpPreserving(TpWitness::Alignment {
                j: 1,
                failure: AlignmentFailure::Vanishing { a: gq(1, 0), b: gq(0, 0) },
                probe: v(&[(1, 0), (1, 0)]),
                coordinates: v(&[(1, 0), (0, 0)]),
            })
        );
        let phase_leak = patched(v(&[(1, 0), (0, 1), (0, 0)]), v(&[(1, 0), (0, 1), (0, 3)]));
        assert_eq!(
            reconstruct(&phase_leak, 3, 0).unwrap(),
            ReconstructionVerdict::NotTpPreserving(TpWitness::Alignment {
                j: 1,
                failure: AlignmentFailure::PhaseSupport { k: 2, z_k: gq(0, 3) },
                probe: v(&[(1, 0), (0, 1), (0, 0)]),
                coordinates: v(&[(1, 0), (0, 1), (0, 3)]),
            })
        );
        for (a, b) in [((0, 0), (1, 0)), ((1, 0), (0, 0))] {
            let lost = patched(v(&[(1, 0), (0, 1)]), v(&[a, b]));
            let w = match reconstruct(&lost, 2, 0).unwrap() {
                ReconstructionVerdict::NotTpPreserving(w) => w,
                other => panic!("unexpected verdict {other:?}"),
            };
            assert_eq!(w.tag(), "alignment");
            let failure = AlignmentFailure::PhaseVanishing { a: gq(a.0, a.1), b: gq(b.0, b.1) };
            assert_eq!(failure.kind(), "phase_vanishing");
            assert_eq!(
                w,
                TpWitness::Alignment { j: 1, failure, probe: v(&[(1, 0), (0, 1)]), coordinates: v(&[a, b]) }
            );
        }
    }

    #[test]
    fn conjugating_one_coordinate_is_refused_with_a_consistency_witness() {
        let t = |x: &HVector| -> Result<HVector, FiniteWignerError> {
            Ok(vec![x[0].clone(), x[1].clone(), x[2].try_conj()?])
        };
        let w = match reconstruct(&t, 3, 0).unwrap() {
            ReconstructionVerdict::NotTpPreserving(w) => w,
            other => panic!("unexpected verdict {other:?}"),
        };
        assert_eq!(w.tag(), "consistency");
        assert_eq!(
            w,
            TpWitness::Consistency { j: 1, k: 2, eps_j: 1, eps_k: -1, probe: v(&[(1, 0), (0, 1), (0, 1)]) }
        );
        assert_eq!(
            reconstruct(&t, 3, 1).unwrap(),
            ReconstructionVerdict::NotTpPreserving(TpWitness::Consistency {
                j: 0,
                k: 2,
                eps_j: 1,
                eps_k: -1,
                probe: v(&[(0, 1), (1, 0), (0, 1)]),
            })
        );
        // With the conjugated coordinate as reference the probes agree; the samples refuse it.
        assert_eq!(
            reconstruct(&t, 3, 2).unwrap(),
            ReconstructionVerdict::Reconstructed { f: identity(3), d: q(1), eps: 1 }
        );
        assert_eq!(
            verify_induced(&t, &identity(3), 1, &[e(3, 0), v(&[(1, 0), (0, 0), (0, 1)])]).unwrap(),
            InducedVerdict::NotInduced {
                x: v(&[(1, 0), (0, 0), (0, 1)]),
                image: v(&[(1, 0), (0, 0), (0, -1)]),
                direction: v(&[(1, 0), (0, 0), (0, 1)]),
            }
        );
    }

    #[test]
    fn conjugating_one_of_two_coordinates_passes_the_probes_but_is_not_induced() {
        let t = |x: &HVector| -> Result<HVector, FiniteWignerError> { Ok(vec![x[0].clone(), x[1].try_conj()?]) };
        assert_eq!(
            reconstruct(&t, 2, 0).unwrap(),
            ReconstructionVerdict::Reconstructed { f: identity(2), d: q(1), eps: -1 }
        );
        let x = v(&[(1, 0), (0, 1)]);
        let y = v(&[(0, 1), (1, 0)]);
        assert_eq!(transition_probability(&x, &y).unwrap(), q(0));
        assert_eq!(transition_probability(&t(&x).unwrap(), &t(&y).unwrap()).unwrap(), q(1));
        assert_eq!(
            verify_induced(&t, &identity(2), -1, &[x, y.clone()]).unwrap(),
            InducedVerdict::NotInduced { x: y, image: v(&[(0, 1), (1, 0)]), direction: v(&[(0, -1), (1, 0)]) }
        );
    }

    #[test]
    fn non_orthogonal_and_zero_images_are_witnessed() {
        let shear = vec![v(&[(1, 0), (1, 0)]), v(&[(0, 0), (1, 0)])];
        let t = move |x: &HVector| mat_vec(&shear, x);
        let verdict = reconstruct(&t, 2, 0).unwrap();
        assert_eq!(
            verdict,
            ReconstructionVerdict::NotTpPreserving(TpWitness::Orthogonality { i: 0, j: 1, ip: gq(1, 0) })
        );
        if let ReconstructionVerdict::NotTpPreserving(w) = verdict {
            assert_eq!(w.tag(), "orthogonality");
        }
        let singular = vec![v(&[(1, 0), (0, 0)]), v(&[(0, 0), (0, 0)])];
        let s = move |x: &HVector| mat_vec(&singular, x);
        assert_eq!(
            reconstruct(&s, 2, 0).unwrap(),
            ReconstructionVerdict::NotTpPreserving(TpWitness::ZeroImage { probe: e(2, 1) })
        );
        let kill = patched(v(&[(1, 0), (1, 0)]), v(&[(0, 0), (0, 0)]));
        let w = match reconstruct(&kill, 2, 0).unwrap() {
            ReconstructionVerdict::NotTpPreserving(w) => w,
            other => panic!("unexpected verdict {other:?}"),
        };
        assert_eq!(w.tag(), "zero_image");
        assert_eq!(w, TpWitness::ZeroImage { probe: v(&[(1, 0), (1, 0)]) });
    }

    #[test]
    fn wrong_relative_phases_give_a_sign_witness() {
        for (value, u) in [((1, 0), gq(1, 0)), ((0, 2), gq(0, 2)), ((1, 1), gq(1, 1)), ((-1, 0), gq(-1, 0))] {
            let t = patched(v(&[(1, 0), (0, 1)]), v(&[(1, 0), value]));
            let w = match reconstruct(&t, 2, 0).unwrap() {
                ReconstructionVerdict::NotTpPreserving(w) => w,
                other => panic!("unexpected verdict {other:?}"),
            };
            assert_eq!(w.tag(), "sign");
            assert_eq!(w, TpWitness::Sign { j: 1, probe: v(&[(1, 0), (0, 1)]), u });
        }
        let t = patched(v(&[(1, 0), (0, 1)]), v(&[(2, 0), (0, -2)]));
        assert_eq!(
            reconstruct(&t, 2, 0).unwrap(),
            ReconstructionVerdict::Reconstructed { f: identity(2), d: q(1), eps: -1 }
        );
    }

    #[test]
    fn map_errors_and_bad_images_propagate() {
        let failing = |_: &HVector| -> Result<HVector, FiniteWignerError> { Err(Error::ZeroVector) };
        assert_eq!(reconstruct(&failing, 2, 0), Err(Error::ZeroVector));
        let long = |x: &HVector| -> Result<HVector, FiniteWignerError> {
            let mut y = x.clone();
            y.push(gq(0, 0));
            Ok(y)
        };
        assert_eq!(
            reconstruct(&long, 2, 0),
            Err(Error::DimensionMismatch { operation: "ray map image", expected: 2, got: 3 })
        );
        let empty = |_: &HVector| -> Result<HVector, FiniteWignerError> { Ok(vec![]) };
        assert_eq!(reconstruct(&empty, 2, 0), Err(Error::EmptyVector));
        let ident = |x: &HVector| -> Result<HVector, FiniteWignerError> { Ok(x.clone()) };
        assert_eq!(reconstruct(&ident, 0, 0), Err(Error::EmptyVector));
        assert_eq!(reconstruct(&ident, 2, 2), Err(Error::IndexOutOfRange { index: 2, dimension: 2 }));
        assert_eq!(verify_induced(&ident, &identity(2), 1, &[v(&[(0, 0), (0, 0)])]), Err(Error::ZeroVector));
        assert!(matches!(
            verify_induced(&ident, &identity(2), 1, &[v(&[(1, 0)])]),
            Err(Error::DimensionMismatch { .. })
        ));
        assert_eq!(verify_induced(&ident, &identity(2), 0, &[]), Err(Error::InvalidSign(0)));
        assert_eq!(verify_induced(&long, &identity(2), 1, &[e(2, 0)]), Err(Error::DimensionMismatch {
            operation: "ray map image",
            expected: 2,
            got: 3
        }));
        assert!(matches!(induced_ray_map(&f3(), 0), Err(Error::InvalidSign(0))));
        assert!(matches!(induced_ray_map(&[], 1), Err(Error::NonSquareMatrix)));
        let t = induced_ray_map(&f3(), 1).unwrap();
        assert!(matches!(t(&v(&[(1, 0)])), Err(Error::DimensionMismatch { .. })));
        assert_eq!(t(&vec![]), Err(Error::EmptyVector));
    }

    #[test]
    fn f3_countermodel_is_tp_preserving_but_not_unitary() {
        let mut r = Lcg(9);
        for eps in [1i8, -1] {
            let t = induced_ray_map(&f3(), eps).unwrap();
            for _ in 0..10 {
                let x = r.vector(2);
                let y = r.vector(2);
                assert_eq!(
                    transition_probability(&t(&x).unwrap(), &t(&y).unwrap()).unwrap(),
                    transition_probability(&x, &y).unwrap()
                );
            }
            let ReconstructionVerdict::Reconstructed { f, d, eps: eps2 } = reconstruct(&t, 2, 0).unwrap() else {
                panic!("the F3 ray map is reconstructed");
            };
            // λ = ray_scalar(e_0) = 2, so d = |λ|²·3 = 12, still obstructed by 3.
            assert_eq!(ray_scalar(&e(2, 0)).unwrap(), gq(2, 0));
            assert_eq!((d.clone(), eps2), (q(12), eps));
            assert_eq!(f, scale_matrix(&gq(2, 0), &f3()).unwrap());
            assert_eq!(unitary_normalisation(&f).unwrap(), UnitaryVerdict::NotANorm { d: q(12), p: BigInt::from(3) });
            let xs = samples(&mut r, 2, 5);
            assert_eq!(verify_induced(&t, &f, eps, &xs).unwrap(), InducedVerdict::Induced);
        }
        let verdict = unitary_normalisation(&f3()).unwrap();
        assert_eq!(verdict.tag(), "not_a_norm");
        assert_eq!(verdict, UnitaryVerdict::NotANorm { d: q(3), p: BigInt::from(3) });
        let both = block_diagonal(&[f3(), f3()]).unwrap();
        assert_eq!(both[2], vec![gq(0, 0), gq(0, 0), gq(1, 0), gq(-1, 1)]);
        assert_eq!(similarity_certificate(&both).unwrap(), SimilarityVerdict::Similarity { d: q(3) });
        let t = induced_ray_map(&both, -1).unwrap();
        let ReconstructionVerdict::Reconstructed { f, d, eps } = reconstruct(&t, 4, 2).unwrap() else {
            panic!("F3 ⊕ F3 is reconstructed");
        };
        // λ = ray_scalar(e_2) = 2 − i, |λ|² = 5.
        assert_eq!(ray_scalar(&e(4, 2)).unwrap(), gq(2, -1));
        assert_eq!((d.clone(), eps), (q(15), -1));
        assert_eq!(f, scale_matrix(&gq(2, -1), &both).unwrap());
        assert_eq!(unitary_normalisation(&f).unwrap(), UnitaryVerdict::NotANorm { d, p: BigInt::from(3) });
    }

    #[test]
    fn sums_of_two_rational_squares_are_witnessed() {
        let cases = [
            (q(1), q(1), q(0)),
            (q(2), q(1), q(1)),
            (q(5), q(1), q(2)),
            (q(9), q(3), q(0)),
            (fr(9, 4), q(0), fr(3, 2)),
            (q(13), q(2), q(3)),
            (q(50), q(7), q(1)),
            (fr(65, 13), q(1), q(2)),
            (fr(25, 2), fr(7, 2), fr(1, 2)),
        ];
        for (d, a, b) in &cases {
            let verdict = sum_of_two_rational_squares(d).unwrap();
            assert_eq!(verdict.tag(), "representable");
            assert_eq!(verdict, TwoSquaresVerdict::Representable { a: a.clone(), b: b.clone() });
            assert_eq!(a * a + b * b, *d);
        }
    }

    #[test]
    fn primes_three_mod_four_to_odd_powers_obstruct() {
        for (d, p) in [(q(3), 3), (q(7), 7), (q(12), 3), (q(21), 3), (fr(3, 4), 3), (q(6), 3), (q(63), 7), (fr(5, 11), 11)] {
            let verdict = sum_of_two_rational_squares(&d).unwrap();
            assert_eq!(verdict.tag(), "not_representable");
            assert_eq!(verdict, TwoSquaresVerdict::NotRepresentable { p: BigInt::from(p) });
        }
        assert_eq!(sum_of_two_rational_squares(&q(0)), Err(Error::NonPositiveScale(q(0))));
        assert_eq!(sum_of_two_rational_squares(&q(-2)), Err(Error::NonPositiveScale(q(-2))));
        assert_eq!(
            sum_of_two_rational_squares(&Q::new_raw(BigInt::from(2), BigInt::from(4))),
            Err(Error::InexactEntry(RationalConstructionError::NonReduced))
        );
    }

    #[test]
    fn two_squares_verdict_agrees_with_integer_brute_force() {
        for num in 1..=40i64 {
            for den in 1..=12i64 {
                let d = fr(num, den);
                let m: i64 = (d.numer() * d.denom()).try_into().unwrap();
                let brute = (0..=m)
                    .take_while(|x| x * x <= m)
                    .any(|x| (0..=m).take_while(|y| y * y <= m - x * x).any(|y| x * x + y * y == m));
                match sum_of_two_rational_squares(&d).unwrap() {
                    TwoSquaresVerdict::Representable { a, b } => {
                        assert!(brute, "{d} reported representable");
                        assert_eq!(&a * &a + &b * &b, d);
                        assert!(!a.is_negative() && !b.is_negative());
                    }
                    TwoSquaresVerdict::NotRepresentable { p } => {
                        assert!(!brute, "{d} reported obstructed by {p}");
                        let p: i64 = p.try_into().unwrap();
                        assert_eq!(p % 4, 3);
                        let (mut rest, mut e) = (m, 0);
                        while rest % p == 0 {
                            rest /= p;
                            e += 1;
                        }
                        assert_eq!(e % 2, 1);
                    }
                }
            }
        }
    }

    #[test]
    fn unitary_normalisation_of_named_matrices() {
        let verdict = unitary_normalisation(&hadamard2()).unwrap();
        assert_eq!(verdict.tag(), "unitary");
        let UnitaryVerdict::Unitary { c, u } = verdict else {
            panic!("hadamard2 normalises");
        };
        assert_eq!(c, gq(1, 1));
        assert_eq!(u, scale_matrix(&GaussianRational::new(fr(1, 2), fr(-1, 2)).unwrap(), &hadamard2()).unwrap());
        assert_eq!(mat_mul(&conj_transpose(&u).unwrap(), &u).unwrap(), identity(2));
        for s in all_permutations(3) {
            let p = permutation_matrix(&s).unwrap();
            assert_eq!(unitary_normalisation(&p).unwrap(), UnitaryVerdict::Unitary { c: gq(1, 0), u: p });
        }
        let UnitaryVerdict::Unitary { c, u } = unitary_normalisation(&scale_matrix(&gq(2, 0), &identity(2)).unwrap()).unwrap()
        else {
            panic!("2·I normalises");
        };
        assert_eq!(c.norm_sq(), q(4));
        assert_eq!(mat_mul(&conj_transpose(&u).unwrap(), &u).unwrap(), identity(2));
        let mut r = Lcg(10);
        for n in 1..=4 {
            for _ in 0..6 {
                let (f, d) = block_similarity(&mut r, n);
                match unitary_normalisation(&f).unwrap() {
                    UnitaryVerdict::Unitary { c, u } => {
                        assert_eq!(c.norm_sq(), d);
                        assert_eq!(mat_mul(&conj_transpose(&u).unwrap(), &u).unwrap(), identity(n));
                        assert_eq!(scale_matrix(&c, &u).unwrap(), f);
                    }
                    other => panic!("block similarities have norm scales, got {other:?}"),
                }
            }
        }
        assert_eq!(
            unitary_normalisation(&[v(&[(1, 0), (1, 0)]), v(&[(0, 0), (1, 0)])]).unwrap(),
            UnitaryVerdict::NotSimilarity { i: 0, j: 1, entry: gq(1, 0), expected: gq(0, 0) }
        );
    }

    #[test]
    fn inverse_similarity_is_two_sided() {
        let mut r = Lcg(11);
        for n in 1..=4 {
            for _ in 0..6 {
                let (f, _) = block_similarity(&mut r, n);
                let inv = inverse_similarity(&f).unwrap();
                assert_eq!(mat_mul(&f, &inv).unwrap(), identity(n));
                assert_eq!(mat_mul(&inv, &f).unwrap(), identity(n));
            }
        }
        let inv = inverse_similarity(&f3()).unwrap();
        assert_eq!(inv, scale_matrix(&from_real(&fr(1, 3)).unwrap(), &conj_transpose(&f3()).unwrap()).unwrap());
        assert_eq!(mat_mul(&f3(), &inv).unwrap(), identity(2));
        assert_eq!(
            inverse_similarity(&diag(&[gq(1, 0), gq(2, 0)])),
            Err(Error::NotSimilarity { i: 1, j: 1, entry: gq(4, 0), expected: gq(1, 0) })
        );
    }

    #[test]
    fn coordinates_expand_in_orthogonal_frames_and_refuse_bad_ones() {
        let mut r = Lcg(12);
        for n in 1..=4 {
            for _ in 0..6 {
                let (f, _) = block_similarity(&mut r, n);
                let cols: Vec<HVector> = (0..n).map(|c| (0..n).map(|k| f[k][c].clone()).collect()).collect();
                let y = r.vector(n);
                let z = coordinates(&cols, &y).unwrap();
                let mut sum = vec![gq(0, 0); n];
                for (zk, col) in z.iter().zip(&cols) {
                    for (s, a) in sum.iter_mut().zip(col) {
                        *s = s.try_add(&zk.try_mul(a).unwrap()).unwrap();
                    }
                }
                assert_eq!(sum, y);
                assert_eq!(z, mat_vec(&inverse_similarity(&f).unwrap(), &y).unwrap());
            }
        }
        assert_eq!(
            coordinates(&[v(&[(1, 0), (0, 0)]), v(&[(1, 0), (1, 0)])], &e(2, 0)),
            Err(Error::NotOrthogonal { i: 0, j: 1, ip: gq(1, 0) })
        );
        assert_eq!(
            coordinates(&[v(&[(1, 0), (0, 0)]), v(&[(0, 0), (0, 0)])], &e(2, 0)),
            Err(Error::ZeroBasisVector { index: 1 })
        );
        assert!(matches!(
            coordinates(&[v(&[(1, 0), (0, 0)]), v(&[(0, 0)])], &e(2, 0)),
            Err(Error::DimensionMismatch { .. })
        ));
        assert!(matches!(coordinates(&[e(2, 0), e(2, 1)], &e(3, 0)), Err(Error::DimensionMismatch { .. })));
        assert_eq!(coordinates(&[], &e(2, 0)), Err(Error::EmptyVector));
        assert_eq!(coordinates(&[e(2, 1), e(2, 0)], &v(&[(3, 1), (0, 2)])).unwrap(), v(&[(0, 2), (3, 1)]));
    }

    #[test]
    fn dimension_one_has_a_single_ray() {
        let f = vec![v(&[(2, -1)])];
        assert_eq!(similarity_certificate(&f).unwrap(), SimilarityVerdict::Similarity { d: q(5) });
        let mut r = Lcg(13);
        for eps in [1i8, -1] {
            let t = induced_ray_map(&f, eps).unwrap();
            // λ = ray_scalar(e_0) = 2: F = [[2·(2 − i)]] = [[4 − 2i]], d = 4·5 = 20, eps = +1.
            assert_eq!(
                reconstruct(&t, 1, 0).unwrap(),
                ReconstructionVerdict::Reconstructed { f: vec![v(&[(4, -2)])], d: q(20), eps: 1 }
            );
            let xs = samples(&mut r, 1, 5);
            for sign in [1i8, -1] {
                assert_eq!(verify_induced(&t, &[v(&[(4, -2)])], sign, &xs).unwrap(), InducedVerdict::Induced);
            }
        }
        let x = r.vector(1);
        let y = r.vector(1);
        assert_eq!(transition_probability(&x, &y).unwrap(), q(1));
        assert_eq!(
            unitary_normalisation(&[v(&[(1, 1)])]).unwrap(),
            UnitaryVerdict::Unitary { c: gq(1, 1), u: vec![v(&[(1, 0)])] }
        );
        assert_eq!(
            unitary_normalisation(&[v(&[(3, 0)])]).unwrap(),
            UnitaryVerdict::Unitary { c: gq(3, 0), u: vec![v(&[(1, 0)])] }
        );
        assert_eq!(
            unitary_normalisation(&[v(&[(0, 0)])]).unwrap(),
            UnitaryVerdict::NotSimilarity { i: 0, j: 0, entry: gq(0, 0), expected: gq(0, 0) }
        );
        assert_eq!(inverse_similarity(&f).unwrap(), vec![vec![GaussianRational::new(fr(2, 5), fr(1, 5)).unwrap()]]);
    }

    #[test]
    fn dimension_two_hadamard_reconstructs_with_both_references() {
        for eps in [1i8, -1] {
            let t = induced_ray_map(&hadamard2(), eps).unwrap();
            for (i0, lam, d) in [(0, gq(2, 0), q(8)), (1, gq(1, 1), q(4))] {
                assert_eq!(ray_scalar(&e(2, i0)).unwrap(), lam);
                assert_eq!(
                    reconstruct(&t, 2, i0).unwrap(),
                    ReconstructionVerdict::Reconstructed {
                        f: scale_matrix(&lam, &hadamard2()).unwrap(),
                        d,
                        eps,
                    }
                );
            }
        }
    }

    #[test]
    fn probes_and_pairwise_tp_defects_replay_the_lean_probes() {
        assert_eq!(
            reconstruction_probes(3, 1).unwrap(),
            vec![
                e(3, 0),
                e(3, 1),
                e(3, 2),
                v(&[(1, 0), (1, 0), (0, 0)]),
                v(&[(0, 0), (1, 0), (1, 0)]),
                v(&[(0, 1), (1, 0), (0, 0)]),
                v(&[(0, 0), (1, 0), (0, 1)]),
            ]
        );
        assert_eq!(reconstruction_probes(1, 0).unwrap(), vec![e(1, 0)]);
        assert_eq!(reconstruction_probes(0, 0), Err(Error::EmptyVector));
        assert_eq!(probe(3, 0, 2, &gi()).unwrap(), v(&[(1, 0), (0, 0), (0, 1)]));
        assert_eq!(probe(3, 1, 1, &gi()), Err(Error::IndicesNotDistinct));
        assert_eq!(probe(2, 0, 2, &gi()), Err(Error::IndexOutOfRange { index: 2, dimension: 2 }));
        let (phased, flat) = consistency_probes(3, 0, 1, 2).unwrap();
        assert_eq!((phased.clone(), flat.clone()), (v(&[(1, 0), (0, 1), (0, 1)]), v(&[(1, 0), (1, 0), (1, 0)])));
        assert_eq!(transition_probability(&phased, &flat).unwrap(), fr(5, 9));
        assert_eq!(consistency_probes(3, 0, 1, 1), Err(Error::IndicesNotDistinct));
        // eps_1 = +1, eps_2 = −1: the consistency pair drops from 5/9 to 1/9.
        let conj2 = |x: &HVector| -> Result<HVector, FiniteWignerError> {
            Ok(vec![x[0].clone(), x[1].clone(), x[2].try_conj()?])
        };
        let defect = tp_defect(&conj2, &[phased.clone(), flat.clone()]).unwrap();
        assert_eq!(defect.tag(), "tp_defect");
        assert_eq!(defect, TpDefectVerdict::TpDefect { x: phased, y: flat, before: fr(5, 9), after: fr(1, 9) });
        assert_eq!(tp_defect(&conj2, &reconstruction_probes(3, 0).unwrap()).unwrap(), TpDefectVerdict::TpPreserved);
        let d12 = diag(&[gq(1, 0), gq(2, 0)]);
        let stretch = move |x: &HVector| mat_vec(&d12, x);
        assert_eq!(
            tp_defect(&stretch, &reconstruction_probes(2, 0).unwrap()).unwrap(),
            TpDefectVerdict::TpDefect { x: e(2, 0), y: v(&[(1, 0), (1, 0)]), before: fr(1, 2), after: fr(1, 5) }
        );
        let singular = vec![v(&[(1, 0), (0, 0)]), v(&[(0, 0), (0, 0)])];
        let s = move |x: &HVector| mat_vec(&singular, x);
        let zero = tp_defect(&s, &[e(2, 0), e(2, 1)]).unwrap();
        assert_eq!(zero.tag(), "zero_image");
        assert_eq!(zero, TpDefectVerdict::ZeroImage { x: e(2, 1) });
        assert_eq!(tp_defect(&s, &[v(&[(0, 0), (0, 0)])]), Err(Error::ZeroVector));
        let mut r = Lcg(14);
        for n in 1..=4 {
            let (f, _) = block_similarity(&mut r, n);
            for eps in [1i8, -1] {
                let t = induced_ray_map(&f, eps).unwrap();
                let mut probes = reconstruction_probes(n, n - 1).unwrap();
                probes.extend((0..4).map(|_| r.vector(n)));
                let preserved = tp_defect(&t, &probes).unwrap();
                assert_eq!(preserved.tag(), "tp_preserved");
                assert_eq!(preserved, TpDefectVerdict::TpPreserved);
            }
        }
    }

    #[test]
    fn helper_matrices_and_rays() {
        let a = gq(1, 2);
        let b = gq(-2, 1);
        let block = quaternion_block(&a, &b).unwrap();
        assert_eq!(block, vec![vec![gq(1, 2), gq(2, 1)], vec![gq(-2, 1), gq(1, -2)]]);
        assert_eq!(similarity_certificate(&block).unwrap(), SimilarityVerdict::Similarity { d: q(10) });
        assert_eq!(gram(&f3()).unwrap(), diag(&[gq(3, 0), gq(3, 0)]));
        assert_eq!(gram(&hadamard2()).unwrap(), scale_matrix(&gq(2, 0), &identity(2)).unwrap());
        assert_eq!(diagonal(&[gq(1, 0), gq(0, 1)]).unwrap(), vec![v(&[(1, 0), (0, 0)]), v(&[(0, 0), (0, 1)])]);
        assert_eq!(diagonal(&[]), Err(Error::EmptyVector));
        let sum = block_diagonal(&[hadamard2(), vec![v(&[(0, 1)])]]).unwrap();
        assert_eq!(
            sum,
            vec![v(&[(1, 0), (1, 0), (0, 0)]), v(&[(1, 0), (-1, 0), (0, 0)]), v(&[(0, 0), (0, 0), (0, 1)])]
        );
        assert_eq!(block_diagonal(&[]), Err(Error::NoBlocks));
        assert_eq!(block_diagonal(&[vec![v(&[(1, 0), (0, 0)])]]), Err(Error::NonSquareMatrix));
        let x = v(&[(1, 0), (0, 1)]);
        assert!(same_ray(&x, &scale_vector(&gq(2, -3), &x).unwrap()).unwrap());
        assert!(!same_ray(&x, &v(&[(1, 0), (0, -1)])).unwrap());
        assert!(!same_ray(&x, &v(&[(0, 0), (0, 0)])).unwrap());
        assert!(!same_ray(&v(&[(0, 0), (0, 0)]), &x).unwrap());
        assert!(matches!(same_ray(&x, &e(3, 0)), Err(Error::DimensionMismatch { .. })));
        let mut r = Lcg(15);
        for n in 1..=4 {
            for _ in 0..5 {
                let x = r.vector(n);
                let y = r.vector(n);
                assert_eq!(same_ray(&x, &y).unwrap(), transition_probability(&x, &y).unwrap() == q(1));
            }
        }
    }

    #[test]
    fn twist_unit_vectors_signs_and_permutations_are_admitted() {
        let x = v(&[(1, 2), (-3, 0), (0, -1)]);
        assert_eq!(twist(1, &x).unwrap(), x);
        assert_eq!(twist(-1, &x).unwrap(), v(&[(1, -2), (-3, 0), (0, 1)]));
        assert_eq!(twist(-1, &twist(-1, &x).unwrap()).unwrap(), x);
        assert_eq!(twist(0, &x), Err(Error::InvalidSign(0)));
        assert_eq!(apply(&identity(3), 2, &x), Err(Error::InvalidSign(2)));
        assert_eq!(twist(1, &[]), Err(Error::EmptyVector));
        assert_eq!(unit_vector(3, 1, &gi()).unwrap(), v(&[(0, 0), (0, 1), (0, 0)]));
        assert_eq!(unit_vector(2, 2, &gi()), Err(Error::IndexOutOfRange { index: 2, dimension: 2 }));
        assert_eq!(apply(&identity(3), -1, &x).unwrap(), twist(-1, &x).unwrap());
        assert_eq!(permutation_matrix(&[0, 0]), Err(Error::NotAPermutation(2)));
        assert_eq!(permutation_matrix(&[1, 2]), Err(Error::NotAPermutation(2)));
        assert_eq!(permutation_matrix(&[]), Err(Error::NotAPermutation(0)));
        assert_eq!(
            mat_mul(&permutation_matrix(&[1, 2, 0]).unwrap(), &permutation_matrix(&[1, 2, 0]).unwrap()).unwrap(),
            permutation_matrix(&[2, 0, 1]).unwrap()
        );
        // s = 1·(1 + 2·2) + 2·(−3 + 0) + 3·(0 + 2·(−1)) = −7: (1 + 1) + (2 − 1)·i.
        assert_eq!(ray_scalar(&x).unwrap(), gq(2, 1));
        assert_eq!(ray_scalar(&v(&[(0, 0)])).unwrap(), gq(1, -1));
        assert_eq!(ray_scalar(&[GaussianRational::new(fr(5, 3), fr(-1, 2)).unwrap()]).unwrap(), gq(2, -1));
        for n in 1..=4 {
            for i in 0..n {
                assert!(!ray_scalar(&e(n, i)).unwrap().norm_sq().is_zero());
            }
        }
    }

    #[test]
    fn authority_fence_and_provenance_are_stated() {
        assert!(AUTHORITY_FENCE.starts_with("AuthorityEffect None"));
        assert!(AUTHORITY_FENCE.contains("no unitarity is claimed"));
        assert!(PROVENANCE.contains("20261021T190000Z_finite_wigner"));
        assert!(PROVENANCE.contains("code/python/src/qm/finite_wigner.py"));
    }
}
