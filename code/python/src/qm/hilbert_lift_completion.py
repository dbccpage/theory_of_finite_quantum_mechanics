"""Exact finite carriers, their directed union, rational ℓ² uniformity and the harmonic witness; the
exact-rational half of the controlled Hilbert completion.

Replays in exact rational arithmetic the statements of the Lean modules of
dag/results/FQ-GAP-CONTINUUM-HILBERT-LIFT/runs/20261020T230000Z_completion
(HilbertLiftFiniteTower, HilbertLiftRationalUniformity, and the rational-tolerance characterisations
of HilbertLiftCompletion): the finite carriers Fin n -> Q with zero padding and the exact inner
product, the colimit carrier of finitely supported rational sequences with exhaustion and
truncation, Cauchy-Schwarz over Q, the doubling triangle inequality, the ℓ²/ℓ¹/sup Cauchy
conditions with rational tolerances and their implications, the explicit modulus k -> k+1 of the
harmonic witness, its ℓ¹ failure, and its non-convergence to every exact vector.  The completion
itself (a real or complex Hilbert space) is not representable here; a point of it is represented
constructively as a sequence with an explicit Cauchy modulus, and the inner-product fluctuation
bound below is a native estimate that the Lean run does not state.
Also replays the operator statements of
dag/results/FQ-GAP-CONTINUUM-HILBERT-LIFT/runs/20261021T003000Z_lift_steps
(lean4/HilbertLiftOperators.lean: bounded exact operators, the stage projection, the unilateral shift,
and the coordinate-sum functional whose harmonic gap theorem coordSum_harmonic_gap is the locked
certificate value 1/2 returned by certify()).
The scalar field, the ℓ² uniformity and the Cauchy hypothesis are supplied; nothing selects them.
AuthorityEffect: None.
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/src/qm/tests/test_isolated_certificates.py.
Scope Fence: certify locks coordSum (harmonic 2) - coordSum (harmonic 1) = 1/2, the n = 1 case of
coordSum_harmonic_gap; it does not construct the completion or any operator on it.
"""
from fractions import Fraction as Q
from math import ceil
from typing import Mapping

AUTHORITY_FENCE = ("AuthorityEffect None; not PROVED; the completion is not represented, only exact "
                   "rational statements about finite stages and Cauchy sequences are replayed; "
                   "the scalar field and the ℓ² uniformity are supplied hypotheses.")


class HilbertLiftError(ValueError):
    """One violated exact-carrier invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> HilbertLiftError:
    return HilbertLiftError(invariant, parameters)


def _require_fraction(value: object, role: str) -> Q:
    if isinstance(value, float):
        raise _fail("float refused at the public boundary", role=role, received="float")
    if type(value) is bool:
        raise _fail("boolean refused where a rational was required", role=role)
    if isinstance(value, Fraction):
        return value
    if type(value) is int:
        return Q(value)
    raise _fail("value is not an exact rational", role=role, received=type(value).__name__)


Fraction = Q


def _q(x):
    value = _require_fraction(x, "entry")
    num, den = value.numerator, value.denominator
    if type(num) is not int or type(den) is not int:
        raise _fail("value is not an exact rational", role="entry", received=type(x).__name__)
    if num.bit_length() > 1024 or den.bit_length() > 1024:
        raise _fail("integer exceeds 1024 bits", role="entry")
    return Q(num, den)


# ---------------------------------------------------------------- finite carriers (FinCarrier n)

def fin_vector(xs):
    """A vector of the finite carrier at report size len(xs)."""
    return [_q(x) for x in xs]


def fin_inner(x, y):
    """finInner: the exact rational inner product at a common report size."""
    if len(x) != len(y):
        raise ValueError('equal report sizes required')
    return sum((_q(a) * _q(b) for a, b in zip(x, y)), Q(0))


def pad(x, m):
    """pad: zero padding from report size len(x) to m >= len(x)."""
    if m < len(x):
        raise ValueError('padding cannot shrink the report size')
    return list(x) + [Q(0)] * (m - len(x))


# ------------------------------------------------------- colimit carrier (Carrier = N ->0 Q)

def seq(entries):
    """A finitely supported rational sequence as a dict index -> nonzero Fraction."""
    out = {}
    for i, a in dict(entries).items():
        if type(i) is not int or i < 0:
            raise ValueError('indices must be natural numbers')
        a = _q(a)
        if a != 0:
            out[i] = a
    return out


def of_fin(x):
    """ofFin: the canonical injection of a finite stage."""
    return seq({i: a for i, a in enumerate(x)})


def trunc(n, f):
    """trunc: coordinates 0..n-1 of an exact sequence."""
    if type(n) is not int or n < 0:
        raise ValueError('truncation length must be a non-negative integer')
    return [f.get(i, Q(0)) for i in range(n)]


def support_bound(f):
    """The least n with support f ⊆ range n."""
    return (max(f) + 1) if f else 0


def exhaustion(f):
    """exhaustion: a report size n and a stage vector x with of_fin(x) == f."""
    n = support_bound(f)
    x = trunc(n, f)
    if of_fin(x) != f:
        raise AssertionError('exhaustion witness failed')
    return n, x


def add(f, g):
    return seq({i: f.get(i, Q(0)) + g.get(i, Q(0)) for i in set(f) | set(g)})


def sub(f, g):
    return seq({i: f.get(i, Q(0)) - g.get(i, Q(0)) for i in set(f) | set(g)})


def smul(c, f):
    c = _q(c)
    return seq({i: c * a for i, a in f.items()})


def qinner(f, g):
    """qinner: the exact inner product on the colimit carrier."""
    return sum((a * g.get(i, Q(0)) for i, a in f.items()), Q(0))


def sqdist(f, g):
    """sqdist: squared ℓ² distance."""
    d = sub(f, g)
    return qinner(d, d)


def l1dist(f, g):
    """l1dist: ℓ¹ distance."""
    return sum((abs(a) for a in sub(f, g).values()), Q(0))


def supdist(f, g):
    """Coordinatewise sup distance (0 on equal sequences)."""
    d = sub(f, g)
    return max((abs(a) for a in d.values()), default=Q(0))


# ------------------------------------------------------------------------ exact certificates

def restriction_identity(x, y):
    """qinner_ofFin: qinner (ofFin x) (ofFin y) = finInner x y."""
    return qinner(of_fin(x), of_fin(y)) == fin_inner(x, y)


def padding_is_isometric(x, y, m):
    """finInner_pad and ofFin_pad."""
    return fin_inner(pad(x, m), pad(y, m)) == fin_inner(x, y) and of_fin(pad(x, m)) == of_fin(x)


def cauchy_schwarz_holds(f, g):
    """qinner_sq_le: qinner f g ^ 2 <= qinner f f * qinner g g."""
    return qinner(f, g) ** 2 <= qinner(f, f) * qinner(g, g)


def doubling_triangle_holds(f, g, h):
    """sqdist_le_two_mul: sqdist f h <= 2 * (sqdist f g + sqdist g h)."""
    return sqdist(f, h) <= 2 * (sqdist(f, g) + sqdist(g, h))


def l1_dominates_l2(f, g):
    """sqdist_le_l1dist_sq."""
    return sqdist(f, g) <= l1dist(f, g) ** 2


def bessel_truncation_holds(n, f):
    """finInner_trunc_le: finInner (trunc n f) (trunc n f) <= qinner f f."""
    t = trunc(n, f)
    return fin_inner(t, t) <= qinner(f, f)


# ------------------------------------------------------------------- the harmonic witness

def harmonic_term(i):
    """harmonicTerm i = 1/(i+1)."""
    if type(i) is not int or i < 0:
        raise ValueError('a natural index is required')
    return Q(1, i + 1)


def harmonic(N):
    """harmonic N = sum_{i<N} (1/(i+1)) e_i."""
    if type(N) is not int or N < 0:
        raise ValueError('harmonic length must be a non-negative integer')
    return seq({i: harmonic_term(i) for i in range(N)})


def harmonic_modulus(k):
    """The explicit ℓ² modulus of harmonic_hasModulus: mu k = k + 1."""
    return k + 1


def telescoping_bound_holds(n, m):
    """sum_harmonicTerm_sq_le: for 1 <= n <= m, sum_{n<=i<m} 1/(i+1)^2 <= 1/n - 1/m."""
    if not 1 <= n <= m:
        raise ValueError('1 <= n <= m required')
    s = sum((harmonic_term(i) ** 2 for i in range(n, m)), Q(0))
    return s <= Q(1, n) - Q(1, m)


def harmonic_sqdist_bound_holds(n, m):
    """sqdist_harmonic_lt: for 1 <= n <= m, sqdist (harmonic m) (harmonic n) < 1/n."""
    if not 1 <= n <= m:
        raise ValueError('1 <= n <= m required')
    return sqdist(harmonic(m), harmonic(n)) < Q(1, n)


def harmonic_l1_lower_bound_holds(n):
    """sum_harmonicTerm_Ico_ge / l1dist_harmonic: for n >= 1, l1dist (harmonic 2n) (harmonic n) >= 1/2."""
    if n < 1:
        raise ValueError('n >= 1 required')
    return l1dist(harmonic(2 * n), harmonic(n)) >= Q(1, 2)


def harmonic_nonconvergence_bound_holds(f, N):
    """harmonic_not_tendsTo: with M the support bound of f and N > M,
    sqdist (harmonic N) f >= harmonicTerm M ^ 2."""
    M = support_bound(f)
    if N <= M:
        raise ValueError('N must exceed the support bound of f')
    return sqdist(harmonic(N), f) >= harmonic_term(M) ** 2


# ------------------------------------------------ Cauchy conditions with rational tolerances

def modulus_holds(sequence, modulus, k, horizon):
    """HasModulusL2 on a finite window: for all mu k <= m, n <= horizon,
    sqdist (x m) (x n) < 1/(k+1)."""
    start = modulus(k)
    if horizon < start:
        raise ValueError('the horizon must reach the modulus stage')
    bound = Q(1, k + 1)
    cache = {n: sequence(n) for n in range(start, horizon + 1)}
    return all(sqdist(cache[m], cache[n]) < bound
               for m in range(start, horizon + 1) for n in range(m, horizon + 1))


def l1_cauchy_fails(sequence, epsilon, stage_pairs):
    """A finite refutation of IsCauchyL1: a pair (m, n) beyond every candidate stage with
    l1dist >= epsilon.  Returns the refuting pairs."""
    epsilon = _q(epsilon)
    return [(m, n) for m, n in stage_pairs if l1dist(sequence(m), sequence(n)) >= epsilon]


class CauchyCandidate:
    """A candidate representation of a point in the completion: an exact sequence with a supplied
    modulus function. Successful construction does NOT certify that the sequence is Cauchy or
    that the modulus is valid (which must be verified independently or checked on a finite window)."""

    def __init__(self, sequence, modulus):
        if not callable(sequence) or not callable(modulus):
            raise TypeError('sequence and modulus must be callable')
        self.sequence = sequence
        self.modulus = modulus

    def approximant(self, k):
        """A candidate exact vector at stage modulus(k)."""
        if type(k) is not int or k < 0:
            raise ValueError('k must be a non-negative integer')
        return self.sequence(self.modulus(k))

    def check(self, k, horizon):
        """Check HasModulusL2 on a finite window. This verifies the window only; it does not
        establish universal convergence of an infinite sequence."""
        return modulus_holds(self.sequence, self.modulus, k, horizon)


CauchyPoint = CauchyCandidate


def inner_fluctuation_sq_bound(xm, xn, ym, yn):
    """Exact square-root-free bound: (qinner xm ym - qinner xn yn)^2
    <= 2 * (sqdist xm xn * qinner ym ym + qinner xn xn * sqdist ym yn).
    Native estimate from Cauchy-Schwarz and (a+b)^2 <= 2(a^2+b^2); not stated in the Lean run."""
    return 2 * (sqdist(xm, xn) * qinner(ym, ym) + qinner(xn, xn) * sqdist(ym, yn))


def inner_fluctuation_holds(xm, xn, ym, yn):
    return (qinner(xm, ym) - qinner(xn, yn)) ** 2 <= inner_fluctuation_sq_bound(xm, xn, ym, yn)


# --------------------------------------------------------- the quantitative density step

def grid_approximation(f, r):
    """The density step of denseRange_castSeq_real with exact data: for a finitely supported
    vector f (rational here, standing in for a real one) and r > 0, a vector q whose coordinates
    lie on the grid (1/D) Z with D chosen so that 1/(2D) < r/(k+1), k = |support f|;
    then sqdist f q < r^2."""
    r = _q(r)
    if r <= 0:
        raise ValueError('a positive tolerance is required')
    k = len(f)
    delta = r / (k + 1)
    D = 1
    while Q(1, 2 * D) >= delta:
        D *= 2
    q = seq({i: Q(round(a * D), D) for i, a in f.items()})
    if not all(abs(f[i] - q.get(i, Q(0))) < delta for i in f):
        raise AssertionError('grid approximation exceeded the coordinate tolerance')
    if not sqdist(f, q) < r ** 2:
        raise AssertionError('grid approximation exceeded the squared tolerance')
    return q


# ----------------------------------------------------------------------- mutation controls

def unit_vector(n):
    return seq({n: 1})


def unit_vectors_not_cauchy(m, n):
    """e_m, e_n with m != n have sqdist 2: the sequence of unit vectors is not ℓ²-Cauchy."""
    if m == n:
        raise ValueError('distinct stages required')
    return sqdist(unit_vector(m), unit_vector(n)) == 2


def shifted_modulus_fails():
    """The modulus k -> k (one stage too early) fails for the harmonic witness at k = 0:
    sqdist (harmonic 1) (harmonic 0) = 1 is not < 1."""
    return not modulus_holds(harmonic, lambda k: k, 0, 1)


# ------------------------------------------------ bounded exact operators (HilbertLiftOperators)

def bounded_operator_holds(apply, bound, samples):
    """BoundedExactOperator.norm_sq_le on supplied samples: qinner (A f) (A f) <= bound * qinner f f."""
    bound = _q(bound)
    if bound < 0:
        raise ValueError('a nonnegative bound is required')
    return all(qinner(apply(f), apply(f)) <= bound * qinner(f, f) for f in samples)


def operator_lipschitz_holds(apply, bound, f, g):
    """sqdist_map_le: sqdist (A f) (A g) <= bound * sqdist f g (for an additive A)."""
    return sqdist(apply(f), apply(g)) <= _q(bound) * sqdist(f, g)


def transported_modulus(modulus, bound):
    """isCauchyL2_map made explicit: if x has modulus mu then A x has modulus
    k -> mu((k+1) B - 1) with B = ceil(bound + 1), because
    sqdist (A x_m) (A x_n) <= bound * sqdist (x_m) (x_n) < bound / ((k+1) B) < 1/(k+1)."""
    B = ceil(_q(bound) + 1)
    return lambda k: modulus((k + 1) * B - 1)


def shift(f):
    """shiftMap: e_i -> e_{i+1}."""
    return seq({i + 1: a for i, a in f.items()})


def shift_is_isometric(f, g):
    """qinner_shift: qinner (shift f) (shift g) = qinner f g."""
    return qinner(shift(f), shift(g)) == qinner(f, g)


def proj(n, f):
    """projMap n: the stage projection ofFin (trunc n f); bound 1 by finInner_trunc_le."""
    return of_fin(trunc(n, f))


def coord_sum(f):
    """coordSum: the Q-linear coordinate-sum functional."""
    return sum(f.values(), Q(0))


def coord_sum_gap(n):
    """coordSum_harmonic_gap: coordSum (harmonic 2n) - coordSum (harmonic n), at least 1/2 for n >= 1."""
    if type(n) is not int or n < 1:
        raise ValueError('n >= 1 required')
    return coord_sum(harmonic(2 * n)) - coord_sum(harmonic(n))


def harmonic_norm_sq_le_two_holds(N):
    """qinner_harmonic_le_two: qinner (harmonic N) (harmonic N) <= 2."""
    return qinner(harmonic(N), harmonic(N)) <= 2


def coord_sum_not_cauchy_refutations(pairs):
    """no_continuous_extension_coordSum, finite form: pairs (m, n) with
    |coordSum (harmonic m) - coordSum (harmonic n)| >= 1/2 while the harmonic vectors stay
    within squared norm 2 and converge in the lift."""
    return [(m, n) for m, n in pairs if abs(coord_sum(harmonic(m)) - coord_sum(harmonic(n))) >= Q(1, 2)]


# ------------------------------------------------------------------------- locked certificate

def _locked(value, expected, invariant):
    if value != expected:
        raise _fail(invariant, value=str(value), expected=str(expected))
    return value


_MARK = 7


def _mark() -> int:
    return _MARK


def certify(probe: object | None = None) -> Q:
    """Refuse a non-rational probe, then return the locked harmonic gap coordSum (h_2) - coordSum (h_1) = 1/2."""
    if probe is not None:
        _require_fraction(probe, "probe")
    if _mark() != 7:
        raise _fail("certificate mark drifted", mark=_mark())
    return _locked(coord_sum_gap(1), Q(1, 2), "coordinate-sum harmonic gap drifted")


def main() -> int:
    value = certify()
    print(value)
    if value == Q(1, 2):
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
