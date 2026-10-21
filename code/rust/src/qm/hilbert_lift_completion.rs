//! Exact finite carriers, their directed union, the rational ℓ² uniformity and the harmonic
//! witness: the exact-rational half of the controlled Hilbert completion.
//!
//! Replays in exact rational arithmetic the statements of the Lean modules of
//! `dag/results/FQ-GAP-CONTINUUM-HILBERT-LIFT/runs/20261020T230000Z_completion`
//! (`HilbertLiftFiniteTower`, `HilbertLiftRationalUniformity`, and the rational-tolerance
//! characterisations of `HilbertLiftCompletion`) and mirrors, function for function, the Python
//! twin `code/python/src/qm/hilbert_lift_completion.py`:
//!
//! * finite carriers `Fin n → ℚ` with zero padding (isometric, functorial) and the exact inner
//!   product; the colimit carrier of finitely supported rational sequences with the canonical
//!   injections, truncation, exhaustion and the Bessel-type truncation inequality;
//! * Cauchy–Schwarz over `ℚ`, the doubling triangle inequality for squared distances
//!   (`sqdist f h ≤ 2 (sqdist f g + sqdist g h)`, no square root), and ℓ¹ ≥ ℓ² ≥ sup;
//! * the harmonic witness `h_N = Σ_{i<N} (1/(i+1)) e_i` with the explicit ℓ² modulus `k ↦ k+1`,
//!   the telescoping bound `Σ_{n≤i<m} 1/(i+1)² ≤ 1/n − 1/m`, the ℓ¹ failure
//!   `l1dist(h_{2n}, h_n) ≥ 1/2`, and the non-convergence bound `sqdist(h_N, f) ≥ 1/(M+1)²`
//!   for every exact `f` supported below `M < N`;
//! * a point of the completion represented constructively as a sequence with an explicit
//!   modulus, an exact square-root-free bound on the fluctuation of inner products along two
//!   such sequences (a native estimate not stated in the Lean run), and the quantitative density
//!   step (grid approximation with `sqdist f q < r²`);
//! * mutation controls: unit vectors are not ℓ²-Cauchy, and the shifted modulus `k ↦ k` fails;
//! * the operator statements of `lean4/HilbertLiftOperators.lean`
//!   (`dag/results/FQ-GAP-CONTINUUM-HILBERT-LIFT/runs/20261021T003000Z_lift_steps`): bounded
//!   exact operators `qinner (A f) (A f) ≤ C qinner f f` and their Lipschitz consequence, the
//!   transported Cauchy modulus, the unilateral shift (isometric) and the stage projection
//!   (bound 1), and the coordinate-sum functional with its harmonic gap
//!   `coordSum (h_{2n}) − coordSum (h_n) ≥ 1/2` beside `qinner (h_N) (h_N) ≤ 2`; `certify`
//!   locks the `n = 1` gap `1/2`.
//!
//! The completion itself (a real or complex Hilbert space) is not represented; the scalar field,
//! the ℓ² uniformity and the Cauchy hypothesis are supplied, not derived.  AuthorityEffect: None.

use std::collections::BTreeMap;

use num_bigint::BigInt;
use num_traits::{One, Signed, ToPrimitive, Zero};

use crate::linear_algebra::{q, Q};

pub const AUTHORITY_FENCE: &str = "AuthorityEffect None; not PROVED; the completion is not \
     represented, only exact rational statements about finite stages and Cauchy sequences are \
     replayed; the scalar field and the ℓ² uniformity are supplied hypotheses.";

pub const PROVENANCE: &str = "Replays the Lean modules of \
     dag/results/FQ-GAP-CONTINUUM-HILBERT-LIFT/runs/20261020T230000Z_completion \
     (HilbertLiftFiniteTower, HilbertLiftRationalUniformity, HilbertLiftCompletion) and the \
     Python twin code/python/src/qm/hilbert_lift_completion.py.";

#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum HilbertLiftError {
    #[error("equal report sizes required")]
    ReportSizeMismatch,
    #[error("padding cannot shrink the report size")]
    PaddingShrinks,
    #[error("1 <= n <= m required")]
    StageOrder,
    #[error("n >= 1 required")]
    StagePositive,
    #[error("the horizon must reach the modulus stage")]
    HorizonBeforeModulus,
    #[error("N must exceed the support bound of f")]
    StageNotBeyondSupport,
    #[error("a positive tolerance is required")]
    NonpositiveTolerance,
    #[error("distinct stages required")]
    EqualStages,
    #[error("a nonnegative bound is required")]
    NegativeBound,
    #[error("the bound block does not fit a machine integer")]
    BoundNotRepresentable,
    #[error("coordinate-sum harmonic gap drifted")]
    CertificateDrift,
}

fn qn(n: usize) -> Q {
    Q::from_integer(BigInt::from(n as u64))
}

fn qinv(n: usize) -> Q {
    Q::new(BigInt::one(), BigInt::from(n as u64))
}

fn sq(a: &Q) -> Q {
    a * a
}

/// A finitely supported rational sequence: index → nonzero entry (zeros are stripped).
#[derive(Debug, Clone, PartialEq, Eq, Default)]
pub struct ExactSeq(BTreeMap<usize, Q>);

impl ExactSeq {
    pub fn from_entries<I: IntoIterator<Item = (usize, Q)>>(entries: I) -> Self {
        let mut map = BTreeMap::new();
        for (i, a) in entries {
            if !a.is_zero() {
                map.insert(i, a);
            }
        }
        ExactSeq(map)
    }

    pub fn get(&self, i: usize) -> Q {
        self.0.get(&i).cloned().unwrap_or_else(|| q(0))
    }

    pub fn entries(&self) -> impl Iterator<Item = (&usize, &Q)> {
        self.0.iter()
    }

    /// Size of the support.
    pub fn support_size(&self) -> usize {
        self.0.len()
    }

    /// The least `n` with support ⊆ `range n`.
    pub fn support_bound(&self) -> usize {
        self.0.keys().next_back().map_or(0, |m| m + 1)
    }

    fn indices_with(&self, other: &ExactSeq) -> Vec<usize> {
        let mut idx: Vec<usize> = self.0.keys().chain(other.0.keys()).cloned().collect();
        idx.sort_unstable();
        idx.dedup();
        idx
    }
}

// ------------------------------------------------------------------ finite carriers

/// `finInner`: the exact rational inner product at a common report size.
pub fn fin_inner(x: &[Q], y: &[Q]) -> Result<Q, HilbertLiftError> {
    if x.len() != y.len() {
        return Err(HilbertLiftError::ReportSizeMismatch);
    }
    Ok(x.iter().zip(y).fold(q(0), |acc, (a, b)| acc + a * b))
}

/// `pad`: zero padding from report size `x.len()` to `m`.
pub fn pad(x: &[Q], m: usize) -> Result<Vec<Q>, HilbertLiftError> {
    if m < x.len() {
        return Err(HilbertLiftError::PaddingShrinks);
    }
    let mut out = x.to_vec();
    out.resize(m, q(0));
    Ok(out)
}

/// `ofFin`: the canonical injection of a finite stage.
pub fn of_fin(x: &[Q]) -> ExactSeq {
    ExactSeq::from_entries(x.iter().cloned().enumerate())
}

/// `trunc`: coordinates `0..n` of an exact sequence.
pub fn trunc(n: usize, f: &ExactSeq) -> Vec<Q> {
    (0..n).map(|i| f.get(i)).collect()
}

/// `exhaustion`: a report size `n` and a stage vector `x` with `of_fin(x) == f`.
pub fn exhaustion(f: &ExactSeq) -> (usize, Vec<Q>) {
    let n = f.support_bound();
    (n, trunc(n, f))
}

pub fn add(f: &ExactSeq, g: &ExactSeq) -> ExactSeq {
    ExactSeq::from_entries(f.indices_with(g).into_iter().map(|i| (i, f.get(i) + g.get(i))))
}

pub fn sub(f: &ExactSeq, g: &ExactSeq) -> ExactSeq {
    ExactSeq::from_entries(f.indices_with(g).into_iter().map(|i| (i, f.get(i) - g.get(i))))
}

pub fn smul(c: &Q, f: &ExactSeq) -> ExactSeq {
    ExactSeq::from_entries(f.entries().map(|(i, a)| (*i, c * a)))
}

/// `qinner`: the exact inner product on the colimit carrier.
pub fn qinner(f: &ExactSeq, g: &ExactSeq) -> Q {
    f.entries().fold(q(0), |acc, (i, a)| acc + a * g.get(*i))
}

/// `sqdist`: squared ℓ² distance.
pub fn sqdist(f: &ExactSeq, g: &ExactSeq) -> Q {
    let d = sub(f, g);
    qinner(&d, &d)
}

/// `l1dist`: ℓ¹ distance.
pub fn l1dist(f: &ExactSeq, g: &ExactSeq) -> Q {
    sub(f, g).entries().fold(q(0), |acc, (_, a)| acc + a.abs())
}

/// Coordinatewise sup distance (zero on equal sequences).
pub fn supdist(f: &ExactSeq, g: &ExactSeq) -> Q {
    sub(f, g)
        .entries()
        .map(|(_, a)| a.abs())
        .fold(q(0), |acc, a| if a > acc { a } else { acc })
}

// ------------------------------------------------------------------ exact certificates

/// `qinner_ofFin`: `qinner (ofFin x) (ofFin y) = finInner x y`.
pub fn restriction_identity(x: &[Q], y: &[Q]) -> Result<bool, HilbertLiftError> {
    Ok(qinner(&of_fin(x), &of_fin(y)) == fin_inner(x, y)?)
}

/// `finInner_pad` and `ofFin_pad`.
pub fn padding_is_isometric(x: &[Q], y: &[Q], m: usize) -> Result<bool, HilbertLiftError> {
    let (px, py) = (pad(x, m)?, pad(y, m)?);
    Ok(fin_inner(&px, &py)? == fin_inner(x, y)? && of_fin(&px) == of_fin(x))
}

/// `qinner_sq_le`: Cauchy–Schwarz over `ℚ`.
pub fn cauchy_schwarz_holds(f: &ExactSeq, g: &ExactSeq) -> bool {
    sq(&qinner(f, g)) <= qinner(f, f) * qinner(g, g)
}

/// `sqdist_le_two_mul`: the doubling triangle inequality.
pub fn doubling_triangle_holds(f: &ExactSeq, g: &ExactSeq, h: &ExactSeq) -> bool {
    sqdist(f, h) <= q(2) * (sqdist(f, g) + sqdist(g, h))
}

/// `sqdist_le_l1dist_sq`.
pub fn l1_dominates_l2(f: &ExactSeq, g: &ExactSeq) -> bool {
    sqdist(f, g) <= sq(&l1dist(f, g))
}

/// `finInner_trunc_le`: the Bessel-type truncation inequality.
pub fn bessel_truncation_holds(n: usize, f: &ExactSeq) -> bool {
    let t = trunc(n, f);
    fin_inner(&t, &t).map_or(false, |v| v <= qinner(f, f))
}

// ------------------------------------------------------------------ the harmonic witness

/// `harmonicTerm i = 1/(i+1)`.
pub fn harmonic_term(i: usize) -> Q {
    qinv(i + 1)
}

/// `harmonic N = Σ_{i<N} (1/(i+1)) e_i`.
pub fn harmonic(n: usize) -> ExactSeq {
    ExactSeq::from_entries((0..n).map(|i| (i, harmonic_term(i))))
}

/// The explicit ℓ² modulus of `harmonic_hasModulus`: `μ k = k + 1`.
pub fn harmonic_modulus(k: usize) -> usize {
    k + 1
}

/// `sum_harmonicTerm_sq_le`: for `1 ≤ n ≤ m`, `Σ_{n≤i<m} 1/(i+1)² ≤ 1/n − 1/m`.
pub fn telescoping_bound_holds(n: usize, m: usize) -> Result<bool, HilbertLiftError> {
    if !(1 <= n && n <= m) {
        return Err(HilbertLiftError::StageOrder);
    }
    let s = (n..m).fold(q(0), |acc, i| acc + sq(&harmonic_term(i)));
    Ok(s <= qinv(n) - qinv(m))
}

/// `sqdist_harmonic_lt`: for `1 ≤ n ≤ m`, `sqdist (harmonic m) (harmonic n) < 1/n`.
pub fn harmonic_sqdist_bound_holds(n: usize, m: usize) -> Result<bool, HilbertLiftError> {
    if !(1 <= n && n <= m) {
        return Err(HilbertLiftError::StageOrder);
    }
    Ok(sqdist(&harmonic(m), &harmonic(n)) < qinv(n))
}

/// `sum_harmonicTerm_Ico_ge` with `l1dist_harmonic`: for `n ≥ 1`,
/// `l1dist (harmonic 2n) (harmonic n) ≥ 1/2`.
pub fn harmonic_l1_lower_bound_holds(n: usize) -> Result<bool, HilbertLiftError> {
    if n < 1 {
        return Err(HilbertLiftError::StagePositive);
    }
    Ok(l1dist(&harmonic(2 * n), &harmonic(n)) >= qinv(2))
}

/// `harmonic_not_tendsTo`: with `M` the support bound of `f` and `N > M`,
/// `sqdist (harmonic N) f ≥ harmonicTerm M ^ 2`.
pub fn harmonic_nonconvergence_bound_holds(
    f: &ExactSeq,
    n: usize,
) -> Result<bool, HilbertLiftError> {
    let m = f.support_bound();
    if n <= m {
        return Err(HilbertLiftError::StageNotBeyondSupport);
    }
    Ok(sqdist(&harmonic(n), f) >= sq(&harmonic_term(m)))
}

// ------------------------------------------------ Cauchy conditions with rational tolerances

/// `HasModulusL2` on a finite window: for all `μ k ≤ m, n ≤ horizon`,
/// `sqdist (x m) (x n) < 1/(k+1)`.
pub fn modulus_holds<S, M>(
    sequence: S,
    modulus: M,
    k: usize,
    horizon: usize,
) -> Result<bool, HilbertLiftError>
where
    S: Fn(usize) -> ExactSeq,
    M: Fn(usize) -> usize,
{
    let start = modulus(k);
    if horizon < start {
        return Err(HilbertLiftError::HorizonBeforeModulus);
    }
    let bound = qinv(k + 1);
    let stages: Vec<ExactSeq> = (start..=horizon).map(&sequence).collect();
    for (a, xm) in stages.iter().enumerate() {
        for xn in stages.iter().skip(a) {
            if sqdist(xm, xn) >= bound {
                return Ok(false);
            }
        }
    }
    Ok(true)
}

/// A finite refutation of `IsCauchyL1`: the stage pairs whose ℓ¹ distance is at least `epsilon`.
pub fn l1_cauchy_refutations<S: Fn(usize) -> ExactSeq>(
    sequence: S,
    epsilon: &Q,
    pairs: &[(usize, usize)],
) -> Vec<(usize, usize)> {
    pairs
        .iter()
        .cloned()
        .filter(|(m, n)| l1dist(&sequence(*m), &sequence(*n)) >= *epsilon)
        .collect()
}

/// A point of the completion represented constructively: an exact sequence with an explicit ℓ²
/// modulus.  Nothing here claims that the limit is an exact vector.
pub struct CauchyPoint<S, M> {
    pub sequence: S,
    pub modulus: M,
}

impl<S: Fn(usize) -> ExactSeq, M: Fn(usize) -> usize> CauchyPoint<S, M> {
    /// An exact vector within squared distance `1/(k+1)` of every later stage.
    pub fn approximant(&self, k: usize) -> ExactSeq {
        (self.sequence)((self.modulus)(k))
    }

    pub fn check(&self, k: usize, horizon: usize) -> Result<bool, HilbertLiftError> {
        modulus_holds(&self.sequence, &self.modulus, k, horizon)
    }
}

/// Exact square-root-free bound:
/// `(qinner xm ym − qinner xn yn)² ≤ 2 (sqdist xm xn · qinner ym ym + qinner xn xn · sqdist ym yn)`.
/// A native estimate from Cauchy–Schwarz and `(a+b)² ≤ 2(a²+b²)`; not stated in the Lean run.
pub fn inner_fluctuation_sq_bound(xm: &ExactSeq, xn: &ExactSeq, ym: &ExactSeq, yn: &ExactSeq) -> Q {
    q(2) * (sqdist(xm, xn) * qinner(ym, ym) + qinner(xn, xn) * sqdist(ym, yn))
}

pub fn inner_fluctuation_holds(xm: &ExactSeq, xn: &ExactSeq, ym: &ExactSeq, yn: &ExactSeq) -> bool {
    sq(&(qinner(xm, ym) - qinner(xn, yn))) <= inner_fluctuation_sq_bound(xm, xn, ym, yn)
}

// --------------------------------------------------------- the quantitative density step

/// The density step of `denseRange_castSeq_real` with exact data: for a finitely supported
/// vector `f` and `r > 0`, a vector `q` on the grid `(1/D) ℤ` with `D` chosen so that
/// `1/(2D) < r/(k+1)`, `k = |support f|`; then `sqdist f q < r²`.
pub fn grid_approximation(f: &ExactSeq, r: &Q) -> Result<ExactSeq, HilbertLiftError> {
    if *r <= q(0) {
        return Err(HilbertLiftError::NonpositiveTolerance);
    }
    let delta = r / qn(f.support_size() + 1);
    let mut d = BigInt::one();
    while Q::new(BigInt::one(), &d * BigInt::from(2u8)) >= delta {
        d *= BigInt::from(2u8);
    }
    let approx = ExactSeq::from_entries(f.entries().map(|(i, a)| {
        let scaled = a * Q::from_integer(d.clone());
        (*i, Q::new(scaled.round().to_integer(), d.clone()))
    }));
    for (i, a) in f.entries() {
        if (a - approx.get(*i)).abs() >= delta {
            return Err(HilbertLiftError::NonpositiveTolerance);
        }
    }
    if sqdist(f, &approx) >= sq(r) {
        return Err(HilbertLiftError::NonpositiveTolerance);
    }
    Ok(approx)
}

// ------------------------------------------------------------------- mutation controls

pub fn unit_vector(n: usize) -> ExactSeq {
    ExactSeq::from_entries([(n, q(1))])
}

/// `e_m, e_n` with `m ≠ n` have `sqdist 2`: the unit vectors are not ℓ²-Cauchy.
pub fn unit_vectors_not_cauchy(m: usize, n: usize) -> Result<bool, HilbertLiftError> {
    if m == n {
        return Err(HilbertLiftError::EqualStages);
    }
    Ok(sqdist(&unit_vector(m), &unit_vector(n)) == q(2))
}

/// The modulus `k ↦ k` (one stage too early) fails for the harmonic witness at `k = 0`:
/// `sqdist (harmonic 1) (harmonic 0) = 1` is not `< 1`.
pub fn shifted_modulus_fails() -> bool {
    matches!(modulus_holds(harmonic, |k| k, 0, 1), Ok(false))
}

// ------------------------------------------------ bounded exact operators (HilbertLiftOperators)

/// `BoundedExactOperator.norm_sq_le` on supplied samples: `qinner (A f) (A f) ≤ bound · qinner f f`.
pub fn bounded_operator_holds<A: Fn(&ExactSeq) -> ExactSeq>(
    apply: A,
    bound: &Q,
    samples: &[ExactSeq],
) -> Result<bool, HilbertLiftError> {
    if *bound < q(0) {
        return Err(HilbertLiftError::NegativeBound);
    }
    Ok(samples.iter().all(|f| {
        let af = apply(f);
        qinner(&af, &af) <= bound * qinner(f, f)
    }))
}

/// `sqdist_map_le`: `sqdist (A f) (A g) ≤ bound · sqdist f g` (for an additive `A`).
pub fn operator_lipschitz_holds<A: Fn(&ExactSeq) -> ExactSeq>(
    apply: A,
    bound: &Q,
    f: &ExactSeq,
    g: &ExactSeq,
) -> bool {
    sqdist(&apply(f), &apply(g)) <= bound * sqdist(f, g)
}

/// The block `B = ⌈bound + 1⌉` used by [`transported_modulus`].
pub fn bound_block(bound: &Q) -> Result<usize, HilbertLiftError> {
    if *bound < q(0) {
        return Err(HilbertLiftError::NegativeBound);
    }
    (bound + q(1))
        .ceil()
        .to_integer()
        .to_usize()
        .ok_or(HilbertLiftError::BoundNotRepresentable)
}

/// `isCauchyL2_map` made explicit: if `x` has modulus `μ` then `A x` has modulus
/// `k ↦ μ((k+1) B − 1)`, since `sqdist (A x_m) (A x_n) ≤ bound / ((k+1) B) < 1/(k+1)`.
pub fn transported_modulus<M: Fn(usize) -> usize>(modulus: M, block: usize) -> impl Fn(usize) -> usize {
    move |k| modulus((k + 1) * block - 1)
}

/// `shiftMap`: `e_i ↦ e_{i+1}`.
pub fn shift(f: &ExactSeq) -> ExactSeq {
    ExactSeq::from_entries(f.entries().map(|(i, a)| (i + 1, a.clone())))
}

/// `qinner_shift`: `qinner (shift f) (shift g) = qinner f g`.
pub fn shift_is_isometric(f: &ExactSeq, g: &ExactSeq) -> bool {
    qinner(&shift(f), &shift(g)) == qinner(f, g)
}

/// `projMap n`: the stage projection `ofFin (trunc n f)`, bound `1` by `finInner_trunc_le`.
pub fn proj(n: usize, f: &ExactSeq) -> ExactSeq {
    of_fin(&trunc(n, f))
}

/// `coordSum`: the `ℚ`-linear coordinate-sum functional.
pub fn coord_sum(f: &ExactSeq) -> Q {
    f.entries().fold(q(0), |acc, (_, a)| acc + a)
}

/// `coordSum_harmonic_gap`: `coordSum (harmonic 2n) − coordSum (harmonic n)`, at least `1/2` for
/// `n ≥ 1`.
pub fn coord_sum_gap(n: usize) -> Result<Q, HilbertLiftError> {
    if n < 1 {
        return Err(HilbertLiftError::StagePositive);
    }
    Ok(coord_sum(&harmonic(2 * n)) - coord_sum(&harmonic(n)))
}

/// `qinner_harmonic_le_two`: `qinner (harmonic N) (harmonic N) ≤ 2`.
pub fn harmonic_norm_sq_le_two_holds(n: usize) -> bool {
    qinner(&harmonic(n), &harmonic(n)) <= q(2)
}

/// `no_continuous_extension_coordSum`, finite form: the pairs `(m, n)` with
/// `|coordSum (harmonic m) − coordSum (harmonic n)| ≥ 1/2`.
pub fn coord_sum_not_cauchy_refutations(pairs: &[(usize, usize)]) -> Vec<(usize, usize)> {
    pairs
        .iter()
        .cloned()
        .filter(|(m, n)| (coord_sum(&harmonic(*m)) - coord_sum(&harmonic(*n))).abs() >= qinv(2))
        .collect()
}

/// The locked certificate value: `coordSum (harmonic 2) − coordSum (harmonic 1) = 1/2`
/// (`coordSum_harmonic_gap` at `n = 1`), mirroring `certify` of the Python twin.
pub fn certify() -> Result<Q, HilbertLiftError> {
    let value = coord_sum_gap(1)?;
    if value != qinv(2) {
        return Err(HilbertLiftError::CertificateDrift);
    }
    Ok(value)
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::linear_algebra::scalars::qr;

    fn r(n: i64, d: i64) -> Q {
        qr(n, d).expect("declared nonzero denominator")
    }

    fn x() -> Vec<Q> {
        vec![q(1), r(1, 2), q(-3)]
    }

    fn y() -> Vec<Q> {
        vec![q(2), q(0), r(1, 3)]
    }

    fn f() -> ExactSeq {
        ExactSeq::from_entries([(0, q(1)), (2, r(-1, 2)), (5, q(3))])
    }

    fn g() -> ExactSeq {
        ExactSeq::from_entries([(1, r(2, 7)), (2, q(1)), (9, q(-1))])
    }

    fn h() -> ExactSeq {
        ExactSeq::from_entries([(0, q(-2)), (5, r(1, 3))])
    }

    #[test]
    fn padding_is_isometric_and_cocone() {
        for m in [3, 4, 7] {
            assert_eq!(padding_is_isometric(&x(), &y(), m), Ok(true));
        }
        assert_eq!(pad(&x(), 2), Err(HilbertLiftError::PaddingShrinks));
        assert_eq!(pad(&pad(&x(), 4).unwrap(), 6).unwrap(), pad(&x(), 6).unwrap());
        assert_eq!(pad(&x(), 3).unwrap(), x());
    }

    #[test]
    fn restriction_identity_holds() {
        assert_eq!(restriction_identity(&x(), &y()), Ok(true));
        assert_eq!(fin_inner(&x(), &y()), Ok(q(1)));
        assert_eq!(fin_inner(&x(), &[q(1)]), Err(HilbertLiftError::ReportSizeMismatch));
    }

    #[test]
    fn exhaustion_and_truncation() {
        for s in [f(), g(), h(), ExactSeq::default()] {
            let (n, v) = exhaustion(&s);
            assert_eq!(of_fin(&v), s);
            assert_eq!(trunc(n, &of_fin(&v)), v);
        }
        assert_eq!(exhaustion(&ExactSeq::default()).0, 0);
    }

    #[test]
    fn bessel_truncation() {
        for n in 0..12 {
            assert!(bessel_truncation_holds(n, &f()));
        }
        let t = trunc(6, &f());
        assert_eq!(fin_inner(&t, &t).unwrap(), qinner(&f(), &f()));
    }

    #[test]
    fn bilinearity_symmetry_positivity() {
        assert_eq!(qinner(&f(), &g()), qinner(&g(), &f()));
        assert_eq!(qinner(&add(&f(), &g()), &h()), qinner(&f(), &h()) + qinner(&g(), &h()));
        assert_eq!(qinner(&smul(&r(-3, 4), &f()), &g()), r(-3, 4) * qinner(&f(), &g()));
        assert!(qinner(&f(), &f()) >= q(0));
        assert_eq!(qinner(&ExactSeq::default(), &ExactSeq::default()), q(0));
    }

    #[test]
    fn cauchy_schwarz_and_doubling_triangle() {
        for (a, b) in [(f(), g()), (g(), h()), (f(), f()), (ExactSeq::default(), g())] {
            assert!(cauchy_schwarz_holds(&a, &b));
        }
        assert!(doubling_triangle_holds(&f(), &g(), &h()));
        assert!(l1_dominates_l2(&f(), &g()));
        assert_eq!(sqdist(&f(), &g()), sqdist(&g(), &f()));
        assert_eq!(sqdist(&f(), &f()), q(0));
        assert!(sq(&supdist(&f(), &g())) <= sqdist(&f(), &g()));
    }

    #[test]
    fn telescoping_and_sqdist_bounds() {
        for n in 1..9 {
            for m in n..20 {
                assert_eq!(telescoping_bound_holds(n, m), Ok(true));
                assert_eq!(harmonic_sqdist_bound_holds(n, m), Ok(true));
            }
        }
        assert_eq!(telescoping_bound_holds(0, 3), Err(HilbertLiftError::StageOrder));
        assert_eq!(harmonic_sqdist_bound_holds(4, 3), Err(HilbertLiftError::StageOrder));
    }

    #[test]
    fn explicit_modulus() {
        for k in 0..6 {
            assert_eq!(modulus_holds(harmonic, harmonic_modulus, k, harmonic_modulus(k) + 12), Ok(true));
        }
        let point = CauchyPoint { sequence: harmonic, modulus: harmonic_modulus };
        assert_eq!(point.approximant(2), harmonic(3));
        assert_eq!(point.check(3, 15), Ok(true));
        assert_eq!(point.check(3, 2), Err(HilbertLiftError::HorizonBeforeModulus));
    }

    #[test]
    fn not_l1_cauchy() {
        for n in 1..10 {
            assert_eq!(harmonic_l1_lower_bound_holds(n), Ok(true));
        }
        assert_eq!(harmonic_l1_lower_bound_holds(0), Err(HilbertLiftError::StagePositive));
        let pairs: Vec<(usize, usize)> = (1..10).map(|n| (2 * n, n)).collect();
        assert_eq!(l1_cauchy_refutations(harmonic, &r(1, 2), &pairs), pairs);
    }

    #[test]
    fn no_exact_limit() {
        for s in [f(), g(), h(), ExactSeq::default()] {
            let m = s.support_bound();
            for n in (m + 1)..(m + 8) {
                assert_eq!(harmonic_nonconvergence_bound_holds(&s, n), Ok(true));
            }
        }
        assert_eq!(
            harmonic_nonconvergence_bound_holds(&f(), 3),
            Err(HilbertLiftError::StageNotBeyondSupport)
        );
    }

    #[test]
    fn inner_fluctuation_bound() {
        for m in 1..8 {
            for n in m..12 {
                assert!(inner_fluctuation_holds(&harmonic(m), &harmonic(n), &harmonic(m + 1), &harmonic(n + 2)));
                assert!(inner_fluctuation_holds(&harmonic(m), &harmonic(n), &f(), &g()));
            }
        }
    }

    #[test]
    fn grid_approximation_meets_tolerance() {
        let target = ExactSeq::from_entries([(0, r(355, 113)), (3, r(-22, 7)), (7, r(1, 1_000_003))]);
        for tol in [q(1), r(1, 10), r(1, 1000)] {
            let approx = grid_approximation(&target, &tol).unwrap();
            assert!(sqdist(&target, &approx) < sq(&tol));
        }
        assert_eq!(grid_approximation(&target, &q(0)), Err(HilbertLiftError::NonpositiveTolerance));
    }

    #[test]
    fn mutation_controls() {
        assert_eq!(unit_vectors_not_cauchy(3, 4), Ok(true));
        assert_eq!(unit_vectors_not_cauchy(3, 3), Err(HilbertLiftError::EqualStages));
        assert!(shifted_modulus_fails());
    }

    #[test]
    fn fences_are_declared() {
        assert!(AUTHORITY_FENCE.contains("AuthorityEffect None"));
        assert!(PROVENANCE.contains("20261020T230000Z_completion"));
    }

    #[test]
    fn shift_and_projection_are_bounded() {
        let samples = vec![f(), g(), h(), harmonic(7), ExactSeq::default()];
        assert_eq!(bounded_operator_holds(shift, &q(1), &samples), Ok(true));
        assert_eq!(bounded_operator_holds(|v| proj(3, v), &q(1), &samples), Ok(true));
        assert_eq!(bounded_operator_holds(|v| smul(&r(-3, 2), v), &r(9, 4), &samples), Ok(true));
        assert_eq!(bounded_operator_holds(|v| smul(&q(2), v), &q(1), &samples), Ok(false));
        assert_eq!(bounded_operator_holds(shift, &q(-1), &samples), Err(HilbertLiftError::NegativeBound));
        for (a, b) in [(f(), g()), (g(), h()), (harmonic(4), harmonic(9))] {
            assert!(shift_is_isometric(&a, &b));
            assert!(operator_lipschitz_holds(shift, &q(1), &a, &b));
            assert!(operator_lipschitz_holds(|v| proj(3, v), &q(1), &a, &b));
        }
    }

    #[test]
    fn transported_modulus_works() {
        let block = bound_block(&q(1)).unwrap();
        assert_eq!(block, 2);
        let mu = transported_modulus(harmonic_modulus, block);
        for k in 0..4 {
            assert_eq!(modulus_holds(|n| shift(&harmonic(n)), &mu, k, mu(k) + 10), Ok(true));
        }
        let block3 = bound_block(&r(5, 2)).unwrap();
        assert_eq!(block3, 4);
        let mu3 = transported_modulus(harmonic_modulus, block3);
        assert_eq!(mu3(0), harmonic_modulus(3));
        assert_eq!(modulus_holds(|n| smul(&r(3, 2), &harmonic(n)), &mu3, 1, mu3(1) + 10), Ok(true));
        assert_eq!(bound_block(&q(-1)), Err(HilbertLiftError::NegativeBound));
    }

    #[test]
    fn coord_sum_gap_and_bounded_norms() {
        assert_eq!(coord_sum(&f()), r(7, 2));
        assert_eq!(coord_sum(&add(&f(), &g())), coord_sum(&f()) + coord_sum(&g()));
        for n in 1..12 {
            assert!(coord_sum_gap(n).unwrap() >= qinv(2));
        }
        for n in 0..40 {
            assert!(harmonic_norm_sq_le_two_holds(n));
        }
        let pairs: Vec<(usize, usize)> = (1..8).map(|n| (2 * n, n)).collect();
        assert_eq!(coord_sum_not_cauchy_refutations(&pairs), pairs);
        assert_eq!(coord_sum_gap(0), Err(HilbertLiftError::StagePositive));
    }

    #[test]
    fn certificate_value() {
        assert_eq!(certify(), Ok(qinv(2)));
    }
}
