"""QM-229, QM-230, QM-231: post-Newtonian light deflection and perihelion advance
over Q with rational interval enclosures, the three-qubit GHZ/Mermin algebra over
Q(i) with the deterministic-assignment bound, a four-tick Page-Wootters history
with a rational-Gaussian step unitary, Pythagorean phase damping, and the QWZ /
Haldane Dirac-point Chern parity formula over Q.

AuthorityEffect: None.

Every number is an exact rational or an element of Q(i).  The only transcendental
constant is pi, carried as a closed rational interval with exact endpoints.  The
Mercury perihelion advance in arcseconds does not involve pi: the pi of
6 pi G M / (a (1 - e^2) c^2) cancels the pi of the radian-to-arcsecond conversion,
so that number is an exact rational compared with its window by exact comparison.

Every audit stores computed values only.  The checks are properties that read
those values, so a report cannot carry a check that its own data contradicts.
An eigenvalue is exact or the build refuses with ``ReggeGravityGhzChernRefusal``.

Deviations from the roadmap text, recorded here so they are not silent:

* The Page-Wootters constraint ``(I_C (x) U - S (x) I_S) |Psi> = 0`` holds for
  the cyclic *lowering* shift ``S |t> = |t - 1 mod 4>`` and needs ``U^4 = I``;
  the raising shift is checked and recorded as failing on the same history.
* The Haldane phase diagram uses a declared rational ``s`` in place of ``sin
  phi``; the sign comparisons against ``3 sqrt(3) t_2 s`` are decided exactly
  by comparing ``M^2`` with ``27 t_2^2 s^2``, so no square root is evaluated.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import product

from .dressed_qed import RationalInterval, pi_interval
from .page_wootters import (
    Qi,
    QiMat,
    QiVec,
    qi_add,
    qi_comm,
    qi_dagger,
    qi_eye,
    qi_inner,
    qi_is_zero,
    qi_kron,
    qi_mat_eq,
    qi_matmul,
    qi_matvec,
    qi_scale,
    qi_sub,
    qi_trace,
    qi_zeros,
)


class ReggeGravityGhzChernRefusal(ValueError):
    """Typed refusal for inputs outside the declared rational domain."""


def qi_vec_is_zero(v: QiVec) -> bool:
    return all(x.is_zero() for x in v)


def qi_mat_pow(a: QiMat, n: int) -> QiMat:
    out = qi_eye(len(a))
    for _ in range(n):
        out = qi_matmul(out, a)
    return out


StressTensor = tuple[tuple[Fraction, ...], ...]


# ============================================================================
# QM-229: Post-Newtonian light deflection and perihelion advance over Q
# ============================================================================


@dataclass(frozen=True)
class SolarSystemInputs:
    """Declared rational inputs: IAU 2015 nominal solar GM and radius, CODATA c,
    IAU 2012 au, JPL Mercury elements (J2000), Julian century."""

    solar_gm_m3_s2: Fraction = Fraction(13271244 * 10**13, 1)
    speed_of_light_m_s: Fraction = Fraction(299792458, 1)
    solar_radius_m: Fraction = Fraction(695700000, 1)
    astronomical_unit_m: Fraction = Fraction(149597870700, 1)
    mercury_semi_major_axis_au: Fraction = Fraction(38709927, 10**8)
    mercury_eccentricity: Fraction = Fraction(20563593, 10**8)
    mercury_period_days: Fraction = Fraction(879691, 10**4)
    julian_century_days: Fraction = Fraction(36525, 1)
    deflection_window_arcsec: tuple[Fraction, Fraction] = (
        Fraction(1750, 1000),
        Fraction(1752, 1000),
    )
    newtonian_window_arcsec: tuple[Fraction, Fraction] = (
        Fraction(875, 1000),
        Fraction(876, 1000),
    )
    perihelion_window_arcsec_per_century: tuple[Fraction, Fraction] = (
        Fraction(4297, 100),
        Fraction(4299, 100),
    )


ARCSEC_PER_RADIAN_TIMES_PI = Fraction(648000)  # 180 * 3600; arcsec = rad * 648000 / pi


def ppn_deflection_factor(gamma: Fraction) -> Fraction:
    """(1 + gamma) / 2: the PPN light-deflection coefficient relative to GR."""
    return (1 + gamma) / 2


def ppn_perihelion_factor(gamma: Fraction, beta: Fraction) -> Fraction:
    """(2 + 2 gamma - beta) / 3: the PPN perihelion coefficient relative to GR."""
    return (2 + 2 * gamma - beta) / 3


def minkowski_trace(t: StressTensor) -> Fraction:
    """eta_{mu nu} T^{mu nu} with eta = diag(+1, -1, -1, -1)."""
    eta = (Fraction(1), Fraction(-1), Fraction(-1), Fraction(-1))
    return sum((eta[mu] * t[mu][mu] for mu in range(4)), Fraction(0))


def null_probe_stress_tensor(energy_density: Fraction) -> StressTensor:
    """T^{mu nu} = E k^mu k^nu with k = (1, 1, 0, 0): a null beam along x."""
    k = (Fraction(1), Fraction(1), Fraction(0), Fraction(0))
    return tuple(tuple(energy_density * k[mu] * k[nu] for nu in range(4)) for mu in range(4))


def dust_at_rest_stress_tensor(rest_density: Fraction) -> StressTensor:
    """T^{00} = rho and every other component zero."""
    return tuple(
        tuple(rest_density if (mu, nu) == (0, 0) else Fraction(0) for nu in range(4))
        for mu in range(4)
    )


def deflection_radians(
    gm: Fraction, c: Fraction, impact_parameter: Fraction, gamma: Fraction
) -> Fraction:
    """delta phi = (1 + gamma) / 2 * 4 G M / (c^2 b), an exact rational in radians."""
    if impact_parameter <= 0 or c <= 0:
        raise ReggeGravityGhzChernRefusal("deflection needs b > 0 and c > 0")
    return ppn_deflection_factor(gamma) * 4 * gm / (c * c * impact_parameter)


def radians_to_arcsec_interval(radians: Fraction, pi: RationalInterval) -> RationalInterval:
    return pi.reciprocal().scale(radians * ARCSEC_PER_RADIAN_TIMES_PI)


def perihelion_advance_arcsec_per_orbit(
    gm: Fraction, c: Fraction, a: Fraction, e: Fraction, gamma: Fraction, beta: Fraction
) -> Fraction:
    """6 pi G M / (a (1 - e^2) c^2) radians per orbit, converted to arcseconds:
    the pi cancels against 648000 / pi, leaving an exact rational."""
    if a <= 0 or e < 0 or e >= 1:
        raise ReggeGravityGhzChernRefusal("perihelion advance needs a > 0 and 0 <= e < 1")
    factor = ppn_perihelion_factor(gamma, beta)
    return factor * 6 * ARCSEC_PER_RADIAN_TIMES_PI * gm / (a * (1 - e * e) * c * c)


def _interval_in_window(iv: RationalInterval, window: tuple[Fraction, Fraction]) -> bool:
    return window[0] <= iv.lo and iv.hi <= window[1]


@dataclass(frozen=True)
class PostNewtonianAudit:
    """QM-229 values.  The checks are properties computed from these fields."""

    inputs: SolarSystemInputs
    null_probe_energy: Fraction
    null_probe_tensor: StressTensor
    dust_density: Fraction
    dust_tensor: StressTensor
    gr_deflection_factor: Fraction
    newtonian_deflection_factor: Fraction
    gr_deflection_rad: Fraction
    newtonian_deflection_rad: Fraction
    gr_deflection_arcsec: RationalInterval
    newtonian_deflection_arcsec: RationalInterval
    gr_perihelion_factor: Fraction
    brans_dicke_omega40_perihelion_factor: Fraction
    mercury_advance_arcsec_per_orbit: Fraction
    mercury_advance_arcsec_per_century: Fraction

    @property
    def null_probe_trace(self) -> Fraction:
        return minkowski_trace(self.null_probe_tensor)

    @property
    def dust_trace(self) -> Fraction:
        return minkowski_trace(self.dust_tensor)

    @property
    def null_probe_t00_equals_t11(self) -> bool:
        return self.null_probe_tensor[0][0] == self.null_probe_tensor[1][1]

    @property
    def gr_over_newton_deflection_ratio(self) -> Fraction:
        return self.gr_deflection_rad / self.newtonian_deflection_rad

    @property
    def gr_deflection_decimal(self) -> tuple[str, str]:
        lo, hi, _ = self.gr_deflection_arcsec.decimal_prefix(6)
        return lo, hi

    @property
    def newtonian_deflection_decimal(self) -> tuple[str, str]:
        lo, hi, _ = self.newtonian_deflection_arcsec.decimal_prefix(6)
        return lo, hi

    @property
    def mercury_advance_decimal(self) -> str:
        exact = RationalInterval.exact(self.mercury_advance_arcsec_per_century)
        return exact.decimal_prefix(6)[0]

    @property
    def gr_deflection_in_window(self) -> bool:
        return _interval_in_window(self.gr_deflection_arcsec, self.inputs.deflection_window_arcsec)

    @property
    def newtonian_deflection_in_window(self) -> bool:
        window = self.inputs.newtonian_window_arcsec
        return _interval_in_window(self.newtonian_deflection_arcsec, window)

    @property
    def mercury_advance_in_window(self) -> bool:
        lo, hi = self.inputs.perihelion_window_arcsec_per_century
        return lo <= self.mercury_advance_arcsec_per_century <= hi

    @property
    def passed(self) -> bool:
        return (
            self.null_probe_tensor == null_probe_stress_tensor(self.null_probe_energy)
            and self.null_probe_trace == 0
            and self.null_probe_t00_equals_t11
            and self.dust_tensor == dust_at_rest_stress_tensor(self.dust_density)
            and self.dust_trace == self.dust_density != 0
            and self.gr_deflection_factor == 1
            and self.newtonian_deflection_factor == Fraction(1, 2)
            and self.gr_over_newton_deflection_ratio == 2
            and self.gr_deflection_in_window
            and self.newtonian_deflection_in_window
            and self.gr_perihelion_factor == 1
            and self.brans_dicke_omega40_perihelion_factor == Fraction(62, 63)
            and self.mercury_advance_in_window
        )


def build_post_newtonian_audit(inputs: SolarSystemInputs | None = None) -> PostNewtonianAudit:
    inp = inputs or SolarSystemInputs()
    pi = pi_interval(20)
    gm, c, r_sun = inp.solar_gm_m3_s2, inp.speed_of_light_m_s, inp.solar_radius_m
    gr_rad = deflection_radians(gm, c, r_sun, Fraction(1))
    newton_rad = deflection_radians(gm, c, r_sun, Fraction(0))
    a_m = inp.mercury_semi_major_axis_au * inp.astronomical_unit_m
    per_orbit = perihelion_advance_arcsec_per_orbit(
        gm, c, a_m, inp.mercury_eccentricity, Fraction(1), Fraction(1)
    )
    omega = Fraction(40)
    bd_gamma = (1 + omega) / (2 + omega)
    null_energy = Fraction(7, 3)
    dust_density = Fraction(5, 2)
    return PostNewtonianAudit(
        inputs=inp,
        null_probe_energy=null_energy,
        null_probe_tensor=null_probe_stress_tensor(null_energy),
        dust_density=dust_density,
        dust_tensor=dust_at_rest_stress_tensor(dust_density),
        gr_deflection_factor=ppn_deflection_factor(Fraction(1)),
        newtonian_deflection_factor=ppn_deflection_factor(Fraction(0)),
        gr_deflection_rad=gr_rad,
        newtonian_deflection_rad=newton_rad,
        gr_deflection_arcsec=radians_to_arcsec_interval(gr_rad, pi),
        newtonian_deflection_arcsec=radians_to_arcsec_interval(newton_rad, pi),
        gr_perihelion_factor=ppn_perihelion_factor(Fraction(1), Fraction(1)),
        brans_dicke_omega40_perihelion_factor=ppn_perihelion_factor(bd_gamma, Fraction(1)),
        mercury_advance_arcsec_per_orbit=per_orbit,
        mercury_advance_arcsec_per_century=(
            per_orbit * inp.julian_century_days / inp.mercury_period_days
        ),
    )


# ============================================================================
# QM-230 (a): Three-qubit GHZ / Mermin algebra over Q(i)
# ============================================================================


def pauli_x() -> QiMat:
    z, o = Qi.from_int(0), Qi.from_int(1)
    return [[z, o], [o, z]]


def pauli_y() -> QiMat:
    z, i_unit = Qi.from_int(0), Qi.i()
    return [[z, -i_unit], [i_unit, z]]


def pauli_z() -> QiMat:
    z, o = Qi.from_int(0), Qi.from_int(1)
    return [[o, z], [z, -o]]


def kron3(a: QiMat, b: QiMat, c: QiMat) -> QiMat:
    return qi_kron(qi_kron(a, b), c)


def ghz_unnormalized() -> QiVec:
    """|000> + |111> over Q(i); the 1/sqrt(2) is omitted and never needed."""
    v = [Qi.from_int(0) for _ in range(8)]
    v[0] = Qi.from_int(1)
    v[7] = Qi.from_int(1)
    return v


def rayleigh_quotient(a: QiMat, v: QiVec) -> Qi:
    """<v, A v> / <v, v>; the denominator is a positive rational for v != 0."""
    den = qi_inner(v, v)
    if den.is_zero():
        raise ReggeGravityGhzChernRefusal("Rayleigh quotient of the zero vector")
    return qi_inner(v, qi_matvec(a, v)).scale(1 / den.re)


def exact_eigenvalue(a: QiMat, v: QiVec) -> Qi:
    """lambda with A v = lambda v exactly.  Refuses the zero vector and any v that
    is not an eigenvector of A; no stand-in value is ever returned."""
    lam = rayleigh_quotient(a, v)
    av = qi_matvec(a, v)
    if any(lhs != lam * rhs for lhs, rhs in zip(av, v, strict=True)):
        raise ReggeGravityGhzChernRefusal("vector is not an eigenvector of the operator")
    return lam


def mermin_operators() -> tuple[QiMat, QiMat, QiMat, QiMat]:
    """A1 = X Y Y, A2 = Y X Y, A3 = Y Y X and B = X X X."""
    x, y = pauli_x(), pauli_y()
    return kron3(x, y, y), kron3(y, x, y), kron3(y, y, x), kron3(x, x, x)


def mermin_operator(ops: tuple[QiMat, QiMat, QiMat, QiMat]) -> QiMat:
    """M = B - A1 - A2 - A3."""
    a1, a2, a3, b = ops
    return qi_sub(qi_sub(qi_sub(b, a1), a2), a3)


def mermin_deterministic_values() -> tuple[int, ...]:
    """x1 x2 x3 - x1 y2 y3 - y1 x2 y3 - y1 y2 x3 over all 64 assignments in {-1, +1}^6."""
    return tuple(
        x1 * x2 * x3 - x1 * y2 * y3 - y1 * x2 * y3 - y1 * y2 * x3
        for x1, y1, x2, y2, x3, y3 in product((-1, 1), repeat=6)
    )


@dataclass(frozen=True)
class GhzMerminAudit:
    """QM-230 (a) values: the 8x8 operators, the GHZ vector, their exact
    eigenvalues and the 64 deterministic values."""

    operators: tuple[QiMat, QiMat, QiMat, QiMat]
    ghz: QiVec
    ghz_eigenvalues: tuple[Qi, Qi, Qi, Qi]
    mermin_eigenvalue: Qi
    deterministic_values: tuple[int, ...]

    @property
    def operators_hermitian_and_involutive(self) -> bool:
        identity = qi_eye(8)
        return all(
            qi_mat_eq(qi_dagger(o), o) and qi_mat_eq(qi_matmul(o, o), identity)
            for o in self.operators
        )

    @property
    def operators_pairwise_commute(self) -> bool:
        return all(qi_is_zero(qi_comm(p, r)) for p in self.operators for r in self.operators)

    @property
    def product_a1a2a3_equals_minus_b(self) -> bool:
        a1, a2, a3, b = self.operators
        return qi_mat_eq(qi_matmul(qi_matmul(a1, a2), a3), qi_scale(Fraction(-1), b))

    @property
    def deterministic_max_abs(self) -> int:
        return max(abs(v) for v in self.deterministic_values)

    @property
    def quantum_exceeds_deterministic_bound(self) -> bool:
        lam = self.mermin_eigenvalue
        return lam.im == 0 and lam.re > self.deterministic_max_abs

    @property
    def passed(self) -> bool:
        expected = tuple(Qi.from_int(n) for n in (-1, -1, -1, 1))
        return (
            self.operators_hermitian_and_involutive
            and self.operators_pairwise_commute
            and self.product_a1a2a3_equals_minus_b
            and self.ghz_eigenvalues == expected
            and self.mermin_eigenvalue == Qi.from_int(4)
            and len(self.deterministic_values) == 64
            and self.deterministic_max_abs == 2
            and self.quantum_exceeds_deterministic_bound
        )


def build_ghz_mermin_audit() -> GhzMerminAudit:
    ops = mermin_operators()
    g = ghz_unnormalized()
    a1, a2, a3, b = ops
    return GhzMerminAudit(
        operators=ops,
        ghz=g,
        ghz_eigenvalues=(
            exact_eigenvalue(a1, g),
            exact_eigenvalue(a2, g),
            exact_eigenvalue(a3, g),
            exact_eigenvalue(b, g),
        ),
        mermin_eigenvalue=exact_eigenvalue(mermin_operator(ops), g),
        deterministic_values=mermin_deterministic_values(),
    )


# ============================================================================
# QM-230 (b): Four-tick Page-Wootters history over Q(i)
# ============================================================================


def clock_shift(dim: int, step: int) -> QiMat:
    """S |t> = |t + step mod dim>."""
    s = qi_zeros(dim)
    for t in range(dim):
        s[(t + step) % dim][t] = Qi.from_int(1)
    return s


def rational_gaussian_step_unitary() -> QiMat:
    """U = W diag(1, i) W^dagger with W = (1/5) [[3, 4i], [4i, 3]]: a non-diagonal
    unitary over Q(i) with U^4 = I."""
    w: QiMat = [
        [Qi(Fraction(3, 5)), Qi(Fraction(0), Fraction(4, 5))],
        [Qi(Fraction(0), Fraction(4, 5)), Qi(Fraction(3, 5))],
    ]
    d: QiMat = [[Qi.from_int(1), Qi.from_int(0)], [Qi.from_int(0), Qi.i()]]
    return qi_matmul(qi_matmul(w, d), qi_dagger(w))


def history_state(u: QiMat, psi0: QiVec, ticks: int) -> QiVec:
    """|Psi> = sum_t |t> (x) U^t |psi0> on Q(i)^(ticks * dim)."""
    out: QiVec = []
    for t in range(ticks):
        out.extend(qi_matvec(qi_mat_pow(u, t), psi0))
    return out


def page_wootters_residual(u: QiMat, history: QiVec, ticks: int, step: int) -> QiVec:
    """(I_C (x) U - S_step (x) I_S) |Psi>."""
    dim = len(u)
    constraint = qi_sub(qi_kron(qi_eye(ticks), u), qi_kron(clock_shift(ticks, step), qi_eye(dim)))
    return qi_matvec(constraint, history)


@dataclass(frozen=True)
class PageWoottersAudit:
    """QM-230 (b) values: the step unitary, the initial state, the history and the
    two constraint residuals."""

    step_unitary: QiMat
    initial_state: QiVec
    history: QiVec
    lowering_residual: QiVec
    raising_residual: QiVec

    @property
    def step_unitary_is_unitary(self) -> bool:
        u = self.step_unitary
        return qi_mat_eq(qi_matmul(qi_dagger(u), u), qi_eye(len(u)))

    @property
    def step_unitary_order_four(self) -> bool:
        u, identity = self.step_unitary, qi_eye(len(self.step_unitary))
        return qi_mat_eq(qi_mat_pow(u, 4), identity) and not qi_mat_eq(qi_mat_pow(u, 2), identity)

    @property
    def step_unitary_not_diagonal(self) -> bool:
        u = self.step_unitary
        return not (u[0][1].is_zero() and u[1][0].is_zero())

    @property
    def conditional_states_are_powers_of_u(self) -> bool:
        d = len(self.initial_state)
        ticks = len(self.history) // d
        return all(
            self.history[d * t : d * (t + 1)]
            == qi_matvec(qi_mat_pow(self.step_unitary, t), self.initial_state)
            for t in range(ticks)
        )

    @property
    def history_norm_sq_over_initial_norm_sq(self) -> Fraction:
        return qi_inner(self.history, self.history).re / qi_inner(
            self.initial_state, self.initial_state
        ).re

    @property
    def passed(self) -> bool:
        return (
            self.step_unitary_is_unitary
            and self.step_unitary_order_four
            and self.step_unitary_not_diagonal
            and qi_vec_is_zero(self.lowering_residual)
            and not qi_vec_is_zero(self.raising_residual)
            and self.conditional_states_are_powers_of_u
            and self.history_norm_sq_over_initial_norm_sq == 4
        )


def build_page_wootters_audit() -> PageWoottersAudit:
    u = rational_gaussian_step_unitary()
    psi0: QiVec = [Qi(Fraction(1)), Qi(Fraction(0))]
    history = history_state(u, psi0, 4)
    return PageWoottersAudit(
        step_unitary=u,
        initial_state=psi0,
        history=history,
        lowering_residual=page_wootters_residual(u, history, 4, -1),
        raising_residual=page_wootters_residual(u, history, 4, 1),
    )


# ============================================================================
# QM-230 (c): Pythagorean phase damping
# ============================================================================


def phase_damping_kraus(p: int, r: int, q: int) -> tuple[QiMat, QiMat]:
    """K0 = diag(1, p/q), K1 = diag(0, r/q) for a Pythagorean triple p^2 + r^2 = q^2."""
    if p <= 0 or r <= 0 or q <= 0 or p * p + r * r != q * q:
        raise ReggeGravityGhzChernRefusal(f"({p}, {r}, {q}) is not a Pythagorean triple")
    z = Qi.from_int(0)
    k0: QiMat = [[Qi.from_int(1), z], [z, Qi(Fraction(p, q))]]
    k1: QiMat = [[z, z], [z, Qi(Fraction(r, q))]]
    return k0, k1


def apply_kraus(kraus: tuple[QiMat, ...], rho: QiMat) -> QiMat:
    out = qi_zeros(len(rho))
    for k in kraus:
        out = qi_add(out, qi_matmul(qi_matmul(k, rho), qi_dagger(k)))
    return out


def plus_state_density() -> QiMat:
    """|+><+| = (1/2) [[1, 1], [1, 1]]."""
    half = Qi(Fraction(1, 2))
    return [[half, half], [half, half]]


@dataclass(frozen=True)
class PhaseDampingRun:
    """One triple: its Kraus pair and the states rho_0 = |+><+|, rho_1, rho_2, rho_3,
    each obtained by applying the channel to the one before."""

    triple: tuple[int, int, int]
    k0: QiMat
    k1: QiMat
    states: tuple[QiMat, ...]

    @property
    def trace_preserving(self) -> bool:
        k0, k1 = self.k0, self.k1
        total = qi_add(qi_matmul(qi_dagger(k0), k0), qi_matmul(qi_dagger(k1), k1))
        return qi_mat_eq(total, qi_eye(2))

    @property
    def states_follow_channel(self) -> bool:
        return all(
            qi_mat_eq(apply_kraus((self.k0, self.k1), before), after)
            for before, after in zip(self.states, self.states[1:], strict=False)
        )

    def coherence(self, n: int) -> Fraction:
        """2 Re rho_n[0][1], read from the stored state after n applications."""
        return 2 * self.states[n][0][1].re

    @property
    def dephasing_lambda(self) -> Fraction:
        _, r, q = self.triple
        return Fraction(r * r, q * q)

    @property
    def passed(self) -> bool:
        p, _, q = self.triple
        half = Qi(Fraction(1, 2))
        return (
            self.trace_preserving
            and self.states_follow_channel
            and len(self.states) == 4
            and all(
                s[0][1] == s[1][0] == Qi(Fraction(1, 2) * Fraction(p, q) ** n)
                and s[0][0] == s[1][1] == half
                and qi_trace(s) == Qi.from_int(1)
                for n, s in enumerate(self.states)
            )
        )


@dataclass(frozen=True)
class PhaseDampingAudit:
    """QM-230 (c) values: one run per Pythagorean triple."""

    runs: tuple[PhaseDampingRun, ...]

    @property
    def trace_preserving_all_triples(self) -> bool:
        return all(run.trace_preserving for run in self.runs)

    @property
    def passed(self) -> bool:
        first = self.runs[0]
        return (
            all(run.passed for run in self.runs)
            and first.triple == (3, 4, 5)
            and first.dephasing_lambda == Fraction(16, 25)
            and first.coherence(3) == Fraction(27, 125)
        )


PYTHAGOREAN_TRIPLES = ((3, 4, 5), (5, 12, 13), (8, 15, 17))


def build_phase_damping_audit() -> PhaseDampingAudit:
    runs: list[PhaseDampingRun] = []
    for p, r, q in PYTHAGOREAN_TRIPLES:
        k0, k1 = phase_damping_kraus(p, r, q)
        states = [plus_state_density()]
        for _ in range(3):
            states.append(apply_kraus((k0, k1), states[-1]))
        runs.append(PhaseDampingRun(triple=(p, r, q), k0=k0, k1=k1, states=tuple(states)))
    return PhaseDampingAudit(runs=tuple(runs))


# ============================================================================
# QM-231: QWZ / Haldane Dirac-point Chern parity over Q
# ============================================================================


def sgn(x: Fraction) -> int:
    return (x > 0) - (x < 0)


def qwz_dirac_masses(m: Fraction) -> tuple[tuple[int, int, Fraction], ...]:
    """At the four time-reversal-invariant momenta k = (n_x pi, n_y pi) the QWZ
    Dirac mass is m + cos k_x + cos k_y = m + (-1)^n_x + (-1)^n_y."""
    return tuple((nx, ny, m + (-1) ** nx + (-1) ** ny) for nx in (0, 1) for ny in (0, 1))


def qwz_chern_number(m: Fraction) -> int | None:
    """C_1(m) = (1/2) sum_{n_x, n_y} (-1)^(n_x + n_y) sgn(m + (-1)^n_x + (-1)^n_y);
    None when some Dirac mass vanishes (the gap is closed and C_1 is not defined)."""
    masses = qwz_dirac_masses(m)
    if any(mass == 0 for _, _, mass in masses):
        return None
    total = sum((-1) ** (nx + ny) * sgn(mass) for nx, ny, mass in masses)
    if total % 2 != 0:
        raise ReggeGravityGhzChernRefusal("odd Dirac-point parity sum")
    return total // 2


def haldane_chern_number(mass: Fraction, t2: Fraction, s: Fraction) -> int | None:
    """Haldane Dirac masses M -/+ 3 sqrt(3) t_2 s at K and K' (opposite chirality):
    C = (1/2) [sgn(M - D) - sgn(M + D)] with D = 3 sqrt(3) t_2 s, decided exactly by
    comparing M^2 with D^2 = 27 t_2^2 s^2.  None at a gap closing (M^2 = D^2)."""
    d_sq = 27 * t2 * t2 * s * s
    m_sq = mass * mass
    if m_sq == d_sq:
        return None
    if m_sq > d_sq:
        return 0
    return -sgn(t2 * s)


QWZ_KEY_MASSES = (Fraction(-3), Fraction(-1), Fraction(1), Fraction(3))
QWZ_CLOSING_CANDIDATES = (Fraction(-2), Fraction(0), Fraction(2))
QWZ_GAPPED_INTERVAL_SAMPLES = (
    (Fraction(-9, 2), Fraction(-5, 2), Fraction(-7, 3), Fraction(-201, 100)),
    (Fraction(-199, 100), Fraction(-3, 2), Fraction(-1, 7), Fraction(-1, 1000)),
    (Fraction(1, 1000), Fraction(2, 7), Fraction(3, 2), Fraction(199, 100)),
    (Fraction(201, 100), Fraction(7, 3), Fraction(5, 2), Fraction(9, 2)),
)
HALDANE_GRID = (Fraction(1, 3), Fraction(-2, 5), Fraction(7, 4), Fraction(-9, 2), Fraction(11, 7))


@dataclass(frozen=True)
class ChernParityAudit:
    """QM-231 values: (sample, C) pairs.  The checks are properties over them."""

    qwz_values: tuple[tuple[Fraction, int | None], ...]
    qwz_closings: tuple[tuple[Fraction, int | None], ...]
    qwz_interval_values: tuple[tuple[int | None, ...], ...]
    haldane_topological_sample: int | None
    haldane_topological_sample_reversed_s: int | None
    haldane_trivial_sample: int | None
    haldane_grid: tuple[tuple[tuple[Fraction, Fraction, Fraction], int | None], ...]
    haldane_degenerate: int | None

    @property
    def qwz_values_at_pm1_pm3(self) -> tuple[int | None, ...]:
        return tuple(c for _, c in self.qwz_values)

    @property
    def qwz_gap_closings(self) -> tuple[Fraction, ...]:
        return tuple(m for m, c in self.qwz_closings if c is None)

    @property
    def qwz_constant_inside_each_gapped_interval(self) -> bool:
        return all(len(set(vals)) == 1 and None not in vals for vals in self.qwz_interval_values)

    @property
    def qwz_jumps_across_closings(self) -> tuple[int, ...]:
        vals = self.qwz_values_at_pm1_pm3
        if None in vals:
            raise ReggeGravityGhzChernRefusal("a key mass sits on a gap closing")
        return tuple(abs(int(b or 0) - int(a or 0)) for a, b in zip(vals, vals[1:], strict=False))

    @property
    def qwz_dirac_points_closing_at_each(self) -> tuple[int, ...]:
        return tuple(
            sum(1 for _, _, mass in qwz_dirac_masses(m) if mass == 0)
            for m, _ in self.qwz_closings
        )

    @property
    def haldane_grid_never_closes_gap(self) -> bool:
        return all(c is not None for _, c in self.haldane_grid)

    @property
    def passed(self) -> bool:
        return (
            self.qwz_values_at_pm1_pm3 == (0, 1, -1, 0)
            and self.qwz_gap_closings == QWZ_CLOSING_CANDIDATES
            and self.qwz_constant_inside_each_gapped_interval
            and self.qwz_jumps_across_closings == (1, 2, 1)
            and self.qwz_dirac_points_closing_at_each == (1, 2, 1)
            and self.haldane_topological_sample == -1
            and self.haldane_topological_sample_reversed_s == 1
            and self.haldane_trivial_sample == 0
            and len(self.haldane_grid) == len(HALDANE_GRID) ** 3
            and self.haldane_grid_never_closes_gap
            and self.haldane_degenerate is None
        )


def build_chern_parity_audit() -> ChernParityAudit:
    t2 = Fraction(1, 10)
    return ChernParityAudit(
        qwz_values=tuple((m, qwz_chern_number(m)) for m in QWZ_KEY_MASSES),
        qwz_closings=tuple((m, qwz_chern_number(m)) for m in QWZ_CLOSING_CANDIDATES),
        qwz_interval_values=tuple(
            tuple(qwz_chern_number(m) for m in iv) for iv in QWZ_GAPPED_INTERVAL_SAMPLES
        ),
        haldane_topological_sample=haldane_chern_number(Fraction(1, 2), t2, Fraction(1)),
        haldane_topological_sample_reversed_s=haldane_chern_number(
            Fraction(1, 2), t2, Fraction(-1)
        ),
        haldane_trivial_sample=haldane_chern_number(Fraction(1), t2, Fraction(1)),
        haldane_grid=tuple(
            ((m, t, s), haldane_chern_number(m, t, s))
            for m in HALDANE_GRID
            for t in HALDANE_GRID
            for s in HALDANE_GRID
        ),
        haldane_degenerate=haldane_chern_number(Fraction(0), Fraction(0), Fraction(1)),
    )


# ============================================================================
# Combined control report
# ============================================================================


@dataclass(frozen=True)
class ReggeGravityGhzChernControlReport:
    """Combined QM-229 / QM-230 / QM-231 control report over Q and Q(i)."""

    control_ids: tuple[str, str, str]
    post_newtonian: PostNewtonianAudit
    ghz_mermin: GhzMerminAudit
    page_wootters: PageWoottersAudit
    phase_damping: PhaseDampingAudit
    chern_parity: ChernParityAudit

    @property
    def passed(self) -> bool:
        return (
            self.post_newtonian.passed
            and self.ghz_mermin.passed
            and self.page_wootters.passed
            and self.phase_damping.passed
            and self.chern_parity.passed
        )


def evaluate_regge_gravity_ghz_chern_control() -> ReggeGravityGhzChernControlReport:
    return ReggeGravityGhzChernControlReport(
        control_ids=("QM-229", "QM-230", "QM-231"),
        post_newtonian=build_post_newtonian_audit(),
        ghz_mermin=build_ghz_mermin_audit(),
        page_wootters=build_page_wootters_audit(),
        phase_damping=build_phase_damping_audit(),
        chern_parity=build_chern_parity_audit(),
    )
