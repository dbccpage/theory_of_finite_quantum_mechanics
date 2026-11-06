"""QM-226, QM-227, QM-228: tree-level QED scattering ratios over Q, weak charged
currents with exact chiral projectors, the muon-decay Fermi constant as a rational
interval enclosure, an exact unitary CKM matrix over Q(i) with its Jarlskog
invariant, the Adler-Bell-Jackiw pi^0 -> gamma gamma colour factor, and the
Gell-Mann-Okubo octet and decuplet mass relations over Q.

AuthorityEffect: None.

Every number below is an exact rational or an element of Q(i).  The Gaussian
rationals and matrix helpers are the shared ones of
``page_wootters_tsirelson_wigner_control``; the Dirac-basis gammas are the ones
of ``dirac_ward_takahashi_control``, moved to the Weyl basis by a rational change
of basis.  Audit records hold computed values; every check is a property that
recomputes from those values.  Any quantity
that involves pi, a logarithm or a square root is carried as a closed rational
interval with exact endpoints (``RationalInterval``); no float enters the
computation.  Enclosures certify membership, not equality.

Deviations from the roadmap text, recorded here so they are not silent:

* Bhabha and Moller are related by the crossing ``s <-> u`` (the incoming
  electron crossed to an outgoing positron), not ``s <-> t``.  The ``s <-> t``
  swap is checked and recorded as failing on a rational counterexample.
* The unitarity triangle is the ``d``-``b`` column triangle
  ``z_k = V_{k d} V_{k b}^*`` summed over the up-type rows ``k in {u, c, t}``.
* The window ``[7.60, 7.85] eV`` for ``Gamma(pi^0 -> gamma gamma)`` is read as
  the experimental band around the PDG value ``7.72 eV``; the theoretical
  enclosure is derived from declared input intervals and is compared with it.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import isqrt

from finite_qm.use_cases import dirac_ward_takahashi_control as dwt
from finite_qm.use_cases.dressed_qed_g2_control import RationalInterval, pi_interval
from finite_qm.use_cases.page_wootters_tsirelson_wigner_control import (
    Qi,
    QiMat,
    QiVec,
    qi_add,
    qi_dagger,
    qi_eye,
    qi_mat_eq,
    qi_matmul,
    qi_matvec,
    qi_scale,
    qi_sub,
    qi_trace,
    qi_zeros,
)


class QedWeakHadronicRefusal(ValueError):
    """Typed refusal for inputs outside the declared rational domain."""


# ============================================================================
# Rational interval helpers: logarithm and square root enclosures
# ============================================================================


def atanh_series_interval(z: Fraction, terms: int) -> RationalInterval:
    """Enclose atanh(z) = sum_{k>=0} z^(2k+1) / (2k+1) for 0 <= z < 1 in Q.

    The tail after ``terms`` summands is bounded by
    ``z^(2K+1) / ((2K+1) (1 - z^2))`` (a geometric majorant), so the returned
    interval ``[partial, partial + tail]`` contains atanh(z).
    """
    if z < 0 or z >= 1:
        raise QedWeakHadronicRefusal(f"atanh enclosure needs 0 <= z < 1, got {z}")
    if terms < 1:
        raise QedWeakHadronicRefusal("atanh enclosure needs at least one term")
    partial = Fraction(0)
    power = z
    for k in range(terms):
        partial += power / (2 * k + 1)
        power *= z * z
    tail = power / ((2 * terms + 1) * (1 - z * z))
    return RationalInterval(partial, partial + tail)


def ln_interval(r: Fraction, terms: int = 40) -> RationalInterval:
    """Enclose ln(r) for a positive rational r in Q.

    Writes ``r = 2^k * y`` with ``1 <= y < 2`` using exact arithmetic, then
    ``ln r = k ln 2 + 2 atanh((y - 1) / (y + 1))`` with ``ln 2 = 2 atanh(1/3)``.
    """
    if r <= 0:
        raise QedWeakHadronicRefusal(f"ln enclosure needs r > 0, got {r}")
    k = 0
    y = Fraction(r)
    while y >= 2:
        y /= 2
        k += 1
    while y < 1:
        y *= 2
        k -= 1
    ln2 = atanh_series_interval(Fraction(1, 3), terms).scale(2)
    z = (y - 1) / (y + 1)
    ln_y = atanh_series_interval(z, terms).scale(2)
    return ln2.scale(k) + ln_y


def sqrt_interval(iv: RationalInterval, digits: int = 12) -> RationalInterval:
    """Enclose sqrt over a non-negative rational interval with exact endpoints.

    The endpoints are decimal rationals ``lo = a / 10^d`` and ``hi = b / 10^d``
    chosen so that ``lo^2 <= iv.lo`` and ``hi^2 >= iv.hi``; both inequalities are
    re-checked exactly before returning.
    """
    if iv.lo < 0:
        raise QedWeakHadronicRefusal("sqrt enclosure needs a non-negative interval")
    scale = 10 ** (2 * digits)
    lo_floor = iv.lo.numerator * scale // iv.lo.denominator
    hi_ceil = -(-iv.hi.numerator * scale // iv.hi.denominator)
    lo = Fraction(isqrt(lo_floor), 10**digits)
    hi = Fraction(isqrt(hi_ceil) + 1, 10**digits)
    if lo * lo > iv.lo or hi * hi < iv.hi:
        raise QedWeakHadronicRefusal("sqrt enclosure endpoint check failed")
    return RationalInterval(lo, hi)


# ============================================================================
# Q(i) helpers the shared module does not carry
# ============================================================================


def qi_norm_sq(z: Qi) -> Fraction:
    """|z|^2 = re^2 + im^2."""
    return z.re * z.re + z.im * z.im


def qi_inverse(z: Qi) -> Qi:
    """1 / z = conj(z) / |z|^2; refuses z = 0."""
    n = qi_norm_sq(z)
    if n == 0:
        raise QedWeakHadronicRefusal("inverse of zero in Q(i)")
    return Qi(z.re / n, -z.im / n)


def qi_times(c: Qi, a: QiMat) -> QiMat:
    """Entrywise c * a for a Gaussian-rational scalar c (the shared ``qi_scale`` takes a rational)."""
    return [[c * x for x in row] for row in a]


def qi_vec_is_zero(v: QiVec) -> bool:
    return all(x.is_zero() for x in v)


def qi_diag(entries: tuple[int, ...]) -> QiMat:
    out = qi_zeros(len(entries))
    for k, val in enumerate(entries):
        out[k][k] = Qi.from_int(val)
    return out


def qi_mat3_inverse(a: QiMat) -> QiMat:
    """Exact inverse of a 3x3 matrix over Q(i) by the adjugate formula."""
    if len(a) != 3:
        raise QedWeakHadronicRefusal("adjugate inverse implemented for 3x3 only")

    def minor(r: int, c: int) -> Qi:
        rows = [i for i in range(3) if i != r]
        cols = [j for j in range(3) if j != c]
        return a[rows[0]][cols[0]] * a[rows[1]][cols[1]] - a[rows[0]][cols[1]] * a[rows[1]][cols[0]]

    cof = [[minor(r, c) if (r + c) % 2 == 0 else -minor(r, c) for c in range(3)] for r in range(3)]
    det = a[0][0] * cof[0][0] + a[0][1] * cof[0][1] + a[0][2] * cof[0][2]
    det_inv = qi_inverse(det)
    return [[cof[c][r] * det_inv for c in range(3)] for r in range(3)]


# ============================================================================
# QM-226: Tree-level QED scattering ratios over Q
# ============================================================================


def klein_nishina_frequency_ratio(x: Fraction, u: Fraction) -> Fraction:
    """eta(x, u) = 1 / (1 + x (1 - u)): scattered-to-incident photon frequency ratio."""
    if x < 0:
        raise QedWeakHadronicRefusal(f"photon energy ratio x must be >= 0, got {x}")
    if u < -1 or u > 1:
        raise QedWeakHadronicRefusal(f"scattering cosine u must lie in [-1, 1], got {u}")
    return Fraction(1) / (1 + x * (1 - u))


def klein_nishina_ratio(x: Fraction, u: Fraction) -> Fraction:
    """R_KN(x, u) = (1/2) eta^2 (eta + 1/eta - (1 - u^2)), the Klein-Nishina
    differential cross section in units of r_e^2."""
    eta = klein_nishina_frequency_ratio(x, u)
    return eta * eta * (eta + Fraction(1) / eta - (1 - u * u)) / 2


def thomson_limit_ratio(u: Fraction) -> Fraction:
    """R_KN(0, u) = (1 + u^2) / 2."""
    return (1 + u * u) / 2


def thomson_angular_integral() -> Fraction:
    """Exact integral of (3/8)(1 + u^2) over u in [-1, 1] via the antiderivative
    (3/8)(u + u^3 / 3); the value 1 is what makes sigma_T = (8 pi / 3) r_e^2."""

    def antiderivative(u: Fraction) -> Fraction:
        return Fraction(3, 8) * (u + u * u * u / 3)

    return antiderivative(Fraction(1)) - antiderivative(Fraction(-1))


def bhabha_reduced_amplitude(s: Fraction, t: Fraction, u: Fraction) -> Fraction:
    """Massless tree-level Bhabha e+ e- -> e+ e- reduced squared amplitude ratio."""
    _check_mandelstam(s, t, u)
    return 2 * ((s * s + u * u) / (t * t) + 2 * u * u / (s * t) + (t * t + u * u) / (s * s))


def moller_reduced_amplitude(s: Fraction, t: Fraction, u: Fraction) -> Fraction:
    """Massless tree-level Moller e- e- -> e- e- reduced squared amplitude ratio."""
    _check_mandelstam(s, t, u)
    return 2 * ((s * s + u * u) / (t * t) + 2 * s * s / (t * u) + (s * s + t * t) / (u * u))


def _check_mandelstam(s: Fraction, t: Fraction, u: Fraction) -> None:
    if s + t + u != 0:
        raise QedWeakHadronicRefusal(f"massless Mandelstam invariants need s + t + u = 0, got {s + t + u}")
    if s == 0 or t == 0 or u == 0:
        raise QedWeakHadronicRefusal("reduced amplitudes have poles at s = 0, t = 0 or u = 0")


KN_GRID_X: tuple[Fraction, ...] = (Fraction(1, 10), Fraction(1), Fraction(2))
KN_GRID_U: tuple[Fraction, ...] = (Fraction(-1), Fraction(0), Fraction(1))
KN_FORWARD_X: tuple[Fraction, ...] = (Fraction(1, 10), Fraction(1), Fraction(2), Fraction(7, 3), Fraction(1000))
THOMSON_U: tuple[Fraction, ...] = (
    Fraction(-1),
    Fraction(0),
    Fraction(1),
    Fraction(1, 2),
    Fraction(-3, 7),
    Fraction(5, 13),
)
MANDELSTAM_POINTS: tuple[tuple[Fraction, Fraction], ...] = (
    (Fraction(5), Fraction(-2)),
    (Fraction(7, 3), Fraction(-1, 2)),
    (Fraction(11), Fraction(-4)),
    (Fraction(13, 2), Fraction(-9, 4)),
)


@dataclass(frozen=True)
class QedTreeLevelAudit:
    """QM-226 audit record: computed Compton, Thomson, Bhabha and Moller values over Q."""

    kn_samples: tuple[tuple[Fraction, Fraction, Fraction], ...]
    kn_forward_values: tuple[Fraction, ...]
    thomson_pairs: tuple[tuple[Fraction, Fraction], ...]
    thomson_angular_integral: Fraction
    crossing_s_u_pairs: tuple[tuple[Fraction, Fraction], ...]
    moller_t_u_pairs: tuple[tuple[Fraction, Fraction], ...]
    s_t_swap_values: tuple[Fraction, Fraction]

    @property
    def kn_forward_unity(self) -> bool:
        return all(r == 1 for r in self.kn_forward_values)

    @property
    def thomson_limit_matches_closed_form(self) -> bool:
        return all(a == b for a, b in self.thomson_pairs)

    @property
    def crossing_s_u_holds(self) -> bool:
        return all(a == b for a, b in self.crossing_s_u_pairs)

    @property
    def moller_t_u_symmetric(self) -> bool:
        return all(a == b for a, b in self.moller_t_u_pairs)

    @property
    def s_t_swap_fails(self) -> bool:
        return self.s_t_swap_values[0] != self.s_t_swap_values[1]

    @property
    def passed(self) -> bool:
        return (
            self.kn_forward_unity
            and self.thomson_limit_matches_closed_form
            and self.thomson_angular_integral == 1
            and self.crossing_s_u_holds
            and self.moller_t_u_symmetric
            and self.s_t_swap_fails
        )


def build_qed_tree_level_audit() -> QedTreeLevelAudit:
    s0, t0 = MANDELSTAM_POINTS[0]
    u0 = -s0 - t0
    return QedTreeLevelAudit(
        kn_samples=tuple((x, u, klein_nishina_ratio(x, u)) for x in KN_GRID_X for u in KN_GRID_U),
        kn_forward_values=tuple(klein_nishina_ratio(x, Fraction(1)) for x in KN_FORWARD_X),
        thomson_pairs=tuple((klein_nishina_ratio(Fraction(0), u), thomson_limit_ratio(u)) for u in THOMSON_U),
        thomson_angular_integral=thomson_angular_integral(),
        crossing_s_u_pairs=tuple(
            (bhabha_reduced_amplitude(s, t, -s - t), moller_reduced_amplitude(-s - t, t, s))
            for s, t in MANDELSTAM_POINTS
        ),
        moller_t_u_pairs=tuple(
            (moller_reduced_amplitude(s, t, -s - t), moller_reduced_amplitude(s, -s - t, t))
            for s, t in MANDELSTAM_POINTS
        ),
        s_t_swap_values=(bhabha_reduced_amplitude(s0, t0, u0), moller_reduced_amplitude(t0, s0, u0)),
    )


# ============================================================================
# QM-227 (a): Weyl-basis Dirac algebra and chiral projectors over Q(i)
# ============================================================================


MINKOWSKI_DIAGONAL: tuple[int, int, int, int] = (1, -1, -1, -1)


def _from_dirac_module(a: dwt.Mat4Qi) -> QiMat:
    """Copy a matrix of ``dirac_ward_takahashi_control.Qi`` entries into the shared Qi."""
    return [[Qi(x.re, x.im) for x in row] for row in a]


def dirac_to_weyl_blocks() -> tuple[QiMat, QiMat]:
    """V = [[I, -I], [I, I]] and V^T with V V^T = 2 I.  V / sqrt(2) is orthogonal; its two
    factors of 1/sqrt(2) multiply to 1/2, so the change of basis stays inside Q(i)."""
    o, z, m = Qi.from_int(1), Qi.from_int(0), Qi.from_int(-1)
    v = [[o, z, m, z], [z, o, z, m], [o, z, o, z], [z, o, z, o]]
    vt = [[o, z, o, z], [z, o, z, o], [m, z, o, z], [z, m, z, o]]
    return v, vt


def dirac_gammas_weyl() -> tuple[QiMat, QiMat, QiMat, QiMat]:
    """gamma_W = (1/2) V gamma_D V^T from the Dirac-basis ``dirac_gamma_matrices()``:
    gamma^0 = [[0, I], [I, 0]] and gamma^k = [[0, sigma_k], [-sigma_k, 0]]."""
    v, vt = dirac_to_weyl_blocks()
    out = [
        qi_scale(Fraction(1, 2), qi_matmul(qi_matmul(v, _from_dirac_module(g)), vt))
        for g in dwt.dirac_gamma_matrices()
    ]
    return out[0], out[1], out[2], out[3]


def clifford_anticommutator(gammas: tuple[QiMat, ...], mu: int, nu: int) -> QiMat:
    """gamma^mu gamma^nu + gamma^nu gamma^mu."""
    return qi_add(qi_matmul(gammas[mu], gammas[nu]), qi_matmul(gammas[nu], gammas[mu]))


def gamma5(gammas: tuple[QiMat, QiMat, QiMat, QiMat]) -> QiMat:
    """gamma_5 = i gamma^0 gamma^1 gamma^2 gamma^3."""
    g0, g1, g2, g3 = gammas
    return qi_times(Qi.i(), qi_matmul(qi_matmul(g0, g1), qi_matmul(g2, g3)))


def chiral_projectors(g5: QiMat) -> tuple[QiMat, QiMat]:
    """P_L = (I - gamma_5) / 2 and P_R = (I + gamma_5) / 2."""
    identity = qi_eye(4)
    return qi_scale(Fraction(1, 2), qi_sub(identity, g5)), qi_scale(Fraction(1, 2), qi_add(identity, g5))


def chiral_test_spinor() -> QiVec:
    """The fixed spinor used for the V-A current check."""
    return [
        Qi(Fraction(3, 5), Fraction(4, 5)),
        Qi(Fraction(-1, 2), Fraction(2, 7)),
        Qi(Fraction(5, 13), Fraction(-12, 13)),
        Qi(Fraction(1, 3), Fraction(1, 9)),
    ]


@dataclass(frozen=True)
class ChiralProjectorAudit:
    """QM-227 (a) audit record: the Weyl gammas, gamma_5 and the V-A projectors."""

    gammas: tuple[QiMat, QiMat, QiMat, QiMat]
    gamma5: QiMat
    p_left: QiMat
    p_right: QiMat
    spinor: QiVec

    @property
    def clifford_relations_hold(self) -> bool:
        identity = qi_eye(4)
        return all(
            qi_mat_eq(
                clifford_anticommutator(self.gammas, mu, nu),
                qi_scale(Fraction(2 * MINKOWSKI_DIAGONAL[mu]), identity) if mu == nu else qi_zeros(4),
            )
            for mu in range(4)
            for nu in range(4)
        )

    @property
    def gamma5_is_diag_m1_m1_p1_p1(self) -> bool:
        return qi_mat_eq(self.gamma5, qi_diag((-1, -1, 1, 1)))

    @property
    def gamma5_squares_to_identity(self) -> bool:
        return qi_mat_eq(qi_matmul(self.gamma5, self.gamma5), qi_eye(4))

    @property
    def gamma5_anticommutes_with_all_gammas(self) -> bool:
        return all(
            qi_mat_eq(qi_add(qi_matmul(g, self.gamma5), qi_matmul(self.gamma5, g)), qi_zeros(4)) for g in self.gammas
        )

    @property
    def projectors_idempotent_orthogonal_complete(self) -> bool:
        pl, pr = self.p_left, self.p_right
        return (
            qi_mat_eq(qi_matmul(pl, pl), pl)
            and qi_mat_eq(qi_matmul(pr, pr), pr)
            and qi_mat_eq(qi_matmul(pl, pr), qi_zeros(4))
            and qi_mat_eq(qi_matmul(pr, pl), qi_zeros(4))
            and qi_mat_eq(qi_add(pl, pr), qi_eye(4))
        )

    @property
    def projector_traces(self) -> tuple[Qi, Qi]:
        return qi_trace(self.p_left), qi_trace(self.p_right)

    @property
    def v_minus_a_current_kills_right_handed(self) -> bool:
        right = qi_matvec(self.p_right, self.spinor)
        return qi_vec_is_zero(qi_matvec(self.p_left, right)) and all(
            qi_vec_is_zero(qi_matvec(qi_matmul(g, self.p_left), right)) for g in self.gammas
        )

    @property
    def passed(self) -> bool:
        return (
            self.clifford_relations_hold
            and self.gamma5_is_diag_m1_m1_p1_p1
            and self.gamma5_squares_to_identity
            and self.gamma5_anticommutes_with_all_gammas
            and self.projectors_idempotent_orthogonal_complete
            and self.projector_traces == (Qi.from_int(2), Qi.from_int(2))
            and self.v_minus_a_current_kills_right_handed
        )


def build_chiral_projector_audit() -> ChiralProjectorAudit:
    gammas = dirac_gammas_weyl()
    g5 = gamma5(gammas)
    pl, pr = chiral_projectors(g5)
    return ChiralProjectorAudit(gammas=gammas, gamma5=g5, p_left=pl, p_right=pr, spinor=chiral_test_spinor())


# ============================================================================
# QM-227 (b): Muon decay phase space and the Fermi constant enclosure
# ============================================================================


@dataclass(frozen=True)
class MuonDecayInputs:
    """Declared rational inputs (CODATA 2018 electron mass and constants, PDG muon mass and lifetime)."""

    electron_mass_mev: Fraction = Fraction(51099895, 10**8)
    muon_mass_mev: Fraction = Fraction(1056583755, 10**7)
    muon_lifetime_s: Fraction = Fraction(21969811, 10**13)
    planck_constant_j_s: Fraction = Fraction(662607015, 10**42)
    elementary_charge_c: Fraction = Fraction(1602176634, 10**28)
    inverse_fine_structure: Fraction = Fraction(137035999084, 10**9)
    window_lo_gev_minus2: Fraction = Fraction(11663, 10**9)
    window_hi_gev_minus2: Fraction = Fraction(11665, 10**9)


def muon_recoil_polynomial(x: Fraction) -> Fraction:
    """f_0(x) = 1 - 8x + 8x^3 - x^4, the polynomial part of the muon phase-space factor."""
    return 1 - 8 * x + 8 * x**3 - x**4


@dataclass(frozen=True)
class MuonDecayFermiConstantAudit:
    """QM-227 (b) audit record: f(x) and G_F / (hbar c)^3 as rational enclosures."""

    mass_ratio_sq_x: Fraction
    recoil_polynomial_f0: Fraction
    ln_x_enclosure: RationalInterval
    recoil_log_term_enclosure: RationalInterval
    phase_space_f_enclosure: RationalInterval
    one_loop_kinoshita_sirlin_dq_enclosure: RationalInterval
    fermi_constant_sq_enclosure: RationalInterval
    fermi_constant_gev_minus2_enclosure: RationalInterval
    window_lo: Fraction
    window_hi: Fraction

    @property
    def dq_negative(self) -> bool:
        return self.one_loop_kinoshita_sirlin_dq_enclosure.hi < 0

    @property
    def fermi_constant_in_window(self) -> bool:
        gf = self.fermi_constant_gev_minus2_enclosure
        return self.window_lo <= gf.lo and gf.hi <= self.window_hi

    @property
    def fermi_constant_decimal(self) -> tuple[str, str]:
        lo, hi, _ = self.fermi_constant_gev_minus2_enclosure.decimal_prefix(9)
        return lo, hi

    @property
    def passed(self) -> bool:
        return self.dq_negative and self.fermi_constant_in_window


def build_muon_decay_audit(inputs: MuonDecayInputs | None = None) -> MuonDecayFermiConstantAudit:
    inp = inputs or MuonDecayInputs()
    x = (inp.electron_mass_mev / inp.muon_mass_mev) ** 2
    f0 = muon_recoil_polynomial(x)
    ln_x = ln_interval(x, 40)
    log_term = ln_x.scale(-12 * x * x)
    f_x = RationalInterval.exact(f0) + log_term

    pi = pi_interval(20)
    alpha = Fraction(1) / inp.inverse_fine_structure
    dq = (RationalInterval.exact(alpha) * (RationalInterval.exact(Fraction(25, 4)) - pi.pow(2))).scale(
        Fraction(1, 2)
    ) * pi.reciprocal()

    hbar_gev_s = RationalInterval.exact(
        inp.planck_constant_j_s / (2 * inp.elementary_charge_c * 10**9)
    ) * pi.reciprocal()
    m_mu_gev = inp.muon_mass_mev / 1000
    denominator = RationalInterval.exact(inp.muon_lifetime_s * m_mu_gev**5) * f_x * (
        RationalInterval.exact(Fraction(1)) + dq
    )
    gf_sq = RationalInterval.exact(Fraction(192)) * pi.pow(3) * hbar_gev_s * denominator.reciprocal()

    return MuonDecayFermiConstantAudit(
        mass_ratio_sq_x=x,
        recoil_polynomial_f0=f0,
        ln_x_enclosure=ln_x,
        recoil_log_term_enclosure=log_term,
        phase_space_f_enclosure=f_x,
        one_loop_kinoshita_sirlin_dq_enclosure=dq,
        fermi_constant_sq_enclosure=gf_sq,
        fermi_constant_gev_minus2_enclosure=sqrt_interval(gf_sq, 14),
        window_lo=inp.window_lo_gev_minus2,
        window_hi=inp.window_hi_gev_minus2,
    )


# ============================================================================
# QM-227 (c): Exact unitary CKM matrix over Q(i) by a Cayley transform
# ============================================================================


WOLFENSTEIN_LAMBDA = Fraction(9, 40)
WOLFENSTEIN_A = Fraction(4, 5)


def ckm_skew_hermitian_generator() -> QiMat:
    """Skew-Hermitian generator tuned so that V = (I - A)(I + A)^(-1) sits near the
    Wolfenstein point lambda = 9/40, A_W = 4/5 (V = I - 2A + O(A^2))."""
    a12 = Qi(Fraction(-9, 80))
    a23 = Qi(Fraction(-81, 4000))
    a13 = Qi(Fraction(-29, 40000), Fraction(317, 200000))
    zero = Qi.from_int(0)
    return [
        [zero, a12, a13],
        [-a12.conj(), zero, a23],
        [-a13.conj(), -a23.conj(), zero],
    ]


def cayley_transform(generator: QiMat) -> QiMat:
    """V = (I - A)(I + A)^(-1) over Q(i); unitary whenever A is skew-Hermitian."""
    identity = qi_eye(len(generator))
    return qi_matmul(qi_sub(identity, generator), qi_mat3_inverse(qi_add(identity, generator)))


def jarlskog_invariant(v: QiMat, rows: tuple[int, int], cols: tuple[int, int]) -> Fraction:
    """J = Im(V_{a c} V_{b d} V_{a d}^* V_{b c}^*) for row pair (a, b) and column pair (c, d)."""
    a, b = rows
    c, d = cols
    return (v[a][c] * v[b][d] * v[a][d].conj() * v[b][c].conj()).im


def ckm_db_triangle(v: QiMat) -> tuple[Qi, Qi, Qi]:
    """Unitarity-triangle sides z_k = V_{k d} V_{k b}^* for k in {u, c, t}."""
    z = tuple(v[k][0] * v[k][2].conj() for k in range(3))
    return z[0], z[1], z[2]


def _within_ten_percent(got: Fraction, target: Fraction) -> bool:
    """|V|^2 within (1 +- 1/10)^2 of target^2, compared on squares: 81/100 <= got / target <= 121/100."""
    return Fraction(81, 100) * target <= got <= Fraction(121, 100) * target


@dataclass(frozen=True)
class CkmUnitarityAudit:
    """QM-227 (c) audit record: the generator, the Cayley transform and its Jarlskog invariant."""

    generator: QiMat
    ckm: QiMat
    jarlskog_ud_cs: Fraction

    @property
    def generator_skew_hermitian(self) -> bool:
        return qi_mat_eq(qi_dagger(self.generator), qi_scale(Fraction(-1), self.generator))

    @property
    def unitary_both_sides(self) -> bool:
        v, identity = self.ckm, qi_eye(3)
        return qi_mat_eq(qi_matmul(qi_dagger(v), v), identity) and qi_mat_eq(qi_matmul(v, qi_dagger(v)), identity)

    @property
    def triangle(self) -> tuple[Qi, Qi, Qi]:
        return ckm_db_triangle(self.ckm)

    @property
    def triangle_closes(self) -> bool:
        z = self.triangle
        return (z[0] + z[1] + z[2]).is_zero()

    @property
    def jarlskog_quartets_agree(self) -> bool:
        pairs = ((0, 1), (0, 2), (1, 2))
        return all(
            abs(jarlskog_invariant(self.ckm, r, c)) == abs(self.jarlskog_ud_cs) for r in pairs for c in pairs
        )

    @property
    def abs_vus_sq(self) -> Fraction:
        return qi_norm_sq(self.ckm[0][1])

    @property
    def abs_vcb_sq(self) -> Fraction:
        return qi_norm_sq(self.ckm[1][2])

    @property
    def vus_vcb_within_ten_percent(self) -> bool:
        lam_sq = WOLFENSTEIN_LAMBDA * WOLFENSTEIN_LAMBDA
        a_lam2_sq = (WOLFENSTEIN_A * lam_sq) ** 2
        return _within_ten_percent(self.abs_vus_sq, lam_sq) and _within_ten_percent(self.abs_vcb_sq, a_lam2_sq)

    @property
    def passed(self) -> bool:
        return (
            self.generator_skew_hermitian
            and self.unitary_both_sides
            and self.triangle_closes
            and self.jarlskog_ud_cs != 0
            and self.jarlskog_quartets_agree
            and self.vus_vcb_within_ten_percent
        )


def build_ckm_unitarity_audit() -> CkmUnitarityAudit:
    generator = ckm_skew_hermitian_generator()
    v = cayley_transform(generator)
    return CkmUnitarityAudit(generator=generator, ckm=v, jarlskog_ud_cs=jarlskog_invariant(v, (0, 1), (0, 1)))


# ============================================================================
# QM-228 (a): Adler-Bell-Jackiw pi^0 -> gamma gamma colour factor
# ============================================================================


@dataclass(frozen=True)
class PionDecayInputs:
    """Declared rational inputs: PDG pi^0 mass, f_pi(130) = 130.2 +- 0.8 MeV (so f_pi^2 = f(130)^2 / 2),
    CODATA alpha, and the experimental band around the PDG rate 7.72 eV."""

    pion_mass_mev: Fraction = Fraction(1349768, 10**4)
    f_pi_130_lo_mev: Fraction = Fraction(1294, 10)
    f_pi_130_hi_mev: Fraction = Fraction(1310, 10)
    inverse_fine_structure: Fraction = Fraction(137035999084, 10**9)
    experimental_band_lo_ev: Fraction = Fraction(760, 100)
    experimental_band_hi_ev: Fraction = Fraction(785, 100)
    pdg_central_ev: Fraction = Fraction(772, 100)


def abj_colour_factor(n_c: int) -> Fraction:
    """S_pi0(N_c) = N_c (Q_u^2 - Q_d^2) with Q_u = 2/3 and Q_d = -1/3."""
    if n_c < 1:
        raise QedWeakHadronicRefusal("colour number must be a positive integer")
    return n_c * (Fraction(2, 3) ** 2 - Fraction(-1, 3) ** 2)


def pion_two_photon_rate_ev(s: Fraction, inputs: PionDecayInputs | None = None) -> RationalInterval:
    """Gamma(pi^0 -> gamma gamma) in eV: alpha^2 m_pi^3 S^2 / (64 pi^3 f_pi^2), as an enclosure."""
    inp = inputs or PionDecayInputs()
    pi = pi_interval(20)
    alpha = Fraction(1) / inp.inverse_fine_structure
    f130 = RationalInterval(inp.f_pi_130_lo_mev, inp.f_pi_130_hi_mev)
    f_pi_sq = (f130 * f130).scale(Fraction(1, 2))
    prefactor = RationalInterval.exact(alpha * alpha * inp.pion_mass_mev**3 / 64) * pi.pow(3).reciprocal()
    return (prefactor * f_pi_sq.reciprocal()).scale(s * s * 10**6)


@dataclass(frozen=True)
class AbjAnomalyAudit:
    """QM-228 (a) audit record: triangle colour factors and the pi^0 rate enclosures."""

    s_pi0_nc3: Fraction
    s_pi0_nc1: Fraction
    rate_nc3_ev_enclosure: RationalInterval
    rate_nc1_ev_enclosure: RationalInterval
    experimental_band: tuple[Fraction, Fraction]
    pdg_central_ev: Fraction

    @property
    def rate_ratio_nc3_over_nc1(self) -> Fraction:
        return (self.s_pi0_nc3 / self.s_pi0_nc1) ** 2

    @property
    def nc3_enclosure_contains_pdg_central(self) -> bool:
        return self.rate_nc3_ev_enclosure.contains(self.pdg_central_ev)

    @property
    def nc3_enclosure_overlaps_experimental_band(self) -> bool:
        lo, hi = self.experimental_band
        r3 = self.rate_nc3_ev_enclosure
        return r3.lo <= hi and lo <= r3.hi

    @property
    def nc1_enclosure_below_experimental_band(self) -> bool:
        return self.rate_nc1_ev_enclosure.hi < self.experimental_band[0]

    @property
    def passed(self) -> bool:
        return (
            self.s_pi0_nc3 == 1
            and self.s_pi0_nc1 == Fraction(1, 3)
            and self.rate_ratio_nc3_over_nc1 == 9
            and self.nc3_enclosure_contains_pdg_central
            and self.nc3_enclosure_overlaps_experimental_band
            and self.nc1_enclosure_below_experimental_band
        )


def build_abj_anomaly_audit(inputs: PionDecayInputs | None = None) -> AbjAnomalyAudit:
    inp = inputs or PionDecayInputs()
    s3 = abj_colour_factor(3)
    s1 = abj_colour_factor(1)
    return AbjAnomalyAudit(
        s_pi0_nc3=s3,
        s_pi0_nc1=s1,
        rate_nc3_ev_enclosure=pion_two_photon_rate_ev(s3, inp),
        rate_nc1_ev_enclosure=pion_two_photon_rate_ev(s1, inp),
        experimental_band=(inp.experimental_band_lo_ev, inp.experimental_band_hi_ev),
        pdg_central_ev=inp.pdg_central_ev,
    )


# ============================================================================
# QM-228 (b): Gell-Mann-Okubo octet and decuplet relations over Q
# ============================================================================


MassCoefficients = tuple[Fraction, Fraction, Fraction]


def su3_mass_coefficients(isospin: Fraction, hypercharge: Fraction) -> MassCoefficients:
    """M = M_0 + M_1 Y + M_2 (I (I + 1) - Y^2 / 4) is linear in (M_0, M_1, M_2); its
    coefficient vector at (I, Y) is (1, Y, I (I + 1) - Y^2 / 4)."""
    return Fraction(1), hypercharge, isospin * (isospin + 1) - hypercharge * hypercharge / 4


OCTET_QUANTUM_NUMBERS: dict[str, tuple[Fraction, Fraction]] = {
    "N": (Fraction(1, 2), Fraction(1)),
    "Lambda": (Fraction(0), Fraction(0)),
    "Sigma": (Fraction(1), Fraction(0)),
    "Xi": (Fraction(1, 2), Fraction(-1)),
}

DECUPLET_HYPERCHARGES: tuple[Fraction, ...] = (Fraction(1), Fraction(0), Fraction(-1), Fraction(-2))


def gmo_octet_relation_coefficients() -> MassCoefficients:
    """Coefficients of 2 (M_N + M_Xi) - (3 M_Lambda + M_Sigma) in (M_0, M_1, M_2).  All three
    are zero, so the octet relation holds for every mass operator of this form."""
    c = {name: su3_mass_coefficients(iso, y) for name, (iso, y) in OCTET_QUANTUM_NUMBERS.items()}
    out = tuple(2 * (c["N"][k] + c["Xi"][k]) - 3 * c["Lambda"][k] - c["Sigma"][k] for k in range(3))
    return out[0], out[1], out[2]


def gmo_decuplet_second_differences() -> tuple[MassCoefficients, MassCoefficients]:
    """Second differences of the decuplet coefficient vectors along Y = 1, 0, -1, -2 with
    I = Y / 2 + 1.  Both are zero, so the decuplet is equally spaced for every operator."""
    c = [su3_mass_coefficients(y / 2 + 1, y) for y in DECUPLET_HYPERCHARGES]

    def second(j: int) -> MassCoefficients:
        d = tuple(c[j + 2][k] - 2 * c[j + 1][k] + c[j][k] for k in range(3))
        return d[0], d[1], d[2]

    return second(0), second(1)


@dataclass(frozen=True)
class BaryonMassInputs:
    """PDG isospin-averaged octet and decuplet masses in MeV (exact integer-ratio rationals)."""

    nucleon: Fraction = (Fraction(93827208816, 10**8) + Fraction(93956542052, 10**8)) / 2
    lambda_: Fraction = Fraction(1115683, 1000)
    sigma: Fraction = (Fraction(118937, 100) + Fraction(1192642, 1000) + Fraction(1197449, 1000)) / 3
    xi: Fraction = (Fraction(131486, 100) + Fraction(132171, 100)) / 2
    delta: Fraction = Fraction(1232, 1)
    sigma_star: Fraction = (Fraction(138283, 100) + Fraction(13837, 10) + Fraction(13872, 10)) / 3
    xi_star: Fraction = (Fraction(153180, 100) + Fraction(1535, 1)) / 2
    omega: Fraction = Fraction(167245, 100)


@dataclass(frozen=True)
class GellMannOkuboAudit:
    """QM-228 (b) audit record.  The identities are exact coefficient vectors; the PDG
    content is the two sides of the octet relation, the decuplet spacings and the
    Omega prediction, with their residuals."""

    octet_coefficients: MassCoefficients
    decuplet_second_differences: tuple[MassCoefficients, MassCoefficients]
    octet_lhs_2_n_plus_xi: Fraction
    octet_rhs_3_lambda_plus_sigma: Fraction
    decuplet_spacings_pdg: tuple[Fraction, Fraction, Fraction]
    omega_equal_spacing_prediction: Fraction
    omega_pdg: Fraction

    @property
    def octet_identity_for_every_operator(self) -> bool:
        return all(c == 0 for c in self.octet_coefficients)

    @property
    def decuplet_equal_spacing_for_every_operator(self) -> bool:
        return all(c == 0 for row in self.decuplet_second_differences for c in row)

    @property
    def octet_fractional_residual(self) -> Fraction:
        return abs(self.octet_rhs_3_lambda_plus_sigma - self.octet_lhs_2_n_plus_xi) / self.octet_rhs_3_lambda_plus_sigma

    @property
    def omega_fractional_residual(self) -> Fraction:
        return abs(self.omega_equal_spacing_prediction - self.omega_pdg) / self.omega_pdg

    @property
    def passed(self) -> bool:
        return (
            self.octet_identity_for_every_operator
            and self.decuplet_equal_spacing_for_every_operator
            and self.octet_fractional_residual <= Fraction(6, 1000)
            and self.omega_fractional_residual <= Fraction(1, 100)
        )


def build_gell_mann_okubo_audit(inputs: BaryonMassInputs | None = None) -> GellMannOkuboAudit:
    inp = inputs or BaryonMassInputs()
    return GellMannOkuboAudit(
        octet_coefficients=gmo_octet_relation_coefficients(),
        decuplet_second_differences=gmo_decuplet_second_differences(),
        octet_lhs_2_n_plus_xi=2 * (inp.nucleon + inp.xi),
        octet_rhs_3_lambda_plus_sigma=3 * inp.lambda_ + inp.sigma,
        decuplet_spacings_pdg=(inp.sigma_star - inp.delta, inp.xi_star - inp.sigma_star, inp.omega - inp.xi_star),
        omega_equal_spacing_prediction=inp.xi_star + (inp.xi_star - inp.sigma_star),
        omega_pdg=inp.omega,
    )


# ============================================================================
# Combined control report
# ============================================================================


@dataclass(frozen=True)
class QedWeakHadronicControlReport:
    """Combined QM-226 / QM-227 / QM-228 control report over Q and Q(i)."""

    control_ids: tuple[str, str, str]
    qed_tree_level: QedTreeLevelAudit
    chiral_projectors: ChiralProjectorAudit
    muon_decay: MuonDecayFermiConstantAudit
    ckm: CkmUnitarityAudit
    abj_anomaly: AbjAnomalyAudit
    gell_mann_okubo: GellMannOkuboAudit

    @property
    def passed(self) -> bool:
        return (
            self.qed_tree_level.passed
            and self.chiral_projectors.passed
            and self.muon_decay.passed
            and self.ckm.passed
            and self.abj_anomaly.passed
            and self.gell_mann_okubo.passed
        )


def evaluate_qed_weak_hadronic_control() -> QedWeakHadronicControlReport:
    return QedWeakHadronicControlReport(
        control_ids=("QM-226", "QM-227", "QM-228"),
        qed_tree_level=build_qed_tree_level_audit(),
        chiral_projectors=build_chiral_projector_audit(),
        muon_decay=build_muon_decay_audit(),
        ckm=build_ckm_unitarity_audit(),
        abj_anomaly=build_abj_anomaly_audit(),
        gell_mann_okubo=build_gell_mann_okubo_audit(),
    )
