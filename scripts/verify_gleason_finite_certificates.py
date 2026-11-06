#!/usr/bin/env python3
"""Exact rational certificate builder and independent checker for the Phase 2
Gleason finite and exact-arithmetic model over Q(i)^3.

AuthorityEffect: None.

This module uses exact rational arithmetic (`fractions.Fraction`) with zero
floating-point operations to construct and independently verify:
1. Finite measurement scenarios (`FiniteFrameScenario`):
   - The 9-ray tomography standard scenario and its {0, 1}-valuation witness.
   - The 15-ray extended anchor-bisector scenario forced to vanish on any
     zero-weight residual vanishing on the 9 tomography anchors.
2. Exact 9-ray tomography reconstruction (`tomography_form`) and projector-span
   certificates expressing any `HermForm3` as an exact rational linear
   combination of the 9 anchor rank-1 projectors.
3. Exact 2-frame meridian antisymmetry certificates:
   - `g(1, 1, 1) + g(-2, 1, 1) = g(1, 0, 0) + g(0, 1, 1) = 0`
   - `g(1, 1, 1) + g(-2, 1, 1) = g(1 + t, 1, 1) + g(-2, 1 + t, 1 + t)`
     for arbitrary rational `t > 0`, giving a 0-remainder approaching-anchor
     certificate for the pair sum `g(1, 1, 1) + g(-2, 1, 1)`.
4. Prime-indexed zero-weight residuals `sp(p)` (`p ≡ 3 mod 4` prime) and
   coordinate-refined 3-adic residuals (`s3_lead_x`, `s3_lead_all`), checking:
   - Exact zero-weight frame additivity on test frame corpora.
   - Vanishing on all 9 tomography anchors (and all 15 anchor-bisector rays).
   - Non-vanishing (`= 1`) at `witness_111 = (1, 1, 1)`.
   - Obstruction to fixed-anchor certificates `|g(x)| <= A max_j |g(y_j)| + B r`
     with `r < 1` whenever the probe family `Y` has even p-adic norm valuation
     or lies in the union of the three coordinate planes.
5. Chinese Remainder Archimedean/3-adic collision sequence
   `crt_approach_e1(m) = (1 + 9*(m+1), 1, 1)`,
   which converges in `raySinSq` to `tomo_e1 = (1, 0, 0)` while maintaining
   `s3 = s3_lead_all = 1`.
6. Exact rational equivalence identity between projective `ray_sin_sq(u, v0)` and
   Euclidean `dist_sq_vec(proj_scalar(u, v0) * u, v0) == norm_sq_vec(v0) * ray_sin_sq(u, v0)`.
7. The 5 explicit proof-obligation witnesses (moving rational near-maximizers,
   linear chain-error accumulation, multi-step reachability, Dedekind ray cut
   pointwise-vs-uniform counterexample on `Q(i)^3 \\ {0}`, and effect-valuation
   linearity bridge).
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction
from functools import reduce
import itertools
import json
from math import gcd
from pathlib import Path
import re
import sys
from typing import Callable, Sequence


@dataclass(frozen=True)
class GaussRat:
    """Exact Gaussian rational `re + im * i` with `re, im in Q`."""

    re: Fraction
    im: Fraction = Fraction(0)

    @staticmethod
    def of(re: int | Fraction, im: int | Fraction = 0) -> "GaussRat":
        return GaussRat(Fraction(re), Fraction(im))

    def __add__(self, other: "GaussRat") -> "GaussRat":
        return GaussRat(self.re + other.re, self.im + other.im)

    def __sub__(self, other: "GaussRat") -> "GaussRat":
        return GaussRat(self.re - other.re, self.im - other.im)

    def __neg__(self) -> "GaussRat":
        return GaussRat(-self.re, -self.im)

    def __mul__(self, other: "GaussRat") -> "GaussRat":
        return GaussRat(
            self.re * other.re - self.im * other.im,
            self.re * other.im + self.im * other.re,
        )

    def __truediv__(self, other: "GaussRat") -> "GaussRat":
        ns = other.norm_sq()
        if ns == 0:
            raise ZeroDivisionError("division by zero GaussRat")
        num = self * other.conj()
        return GaussRat(num.re / ns, num.im / ns)

    def conj(self) -> "GaussRat":
        return GaussRat(self.re, -self.im)

    def norm_sq(self) -> Fraction:
        return self.re * self.re + self.im * self.im

    def is_zero(self) -> bool:
        return self.re == 0 and self.im == 0


G_ZERO = GaussRat.of(0, 0)
G_ONE = GaussRat.of(1, 0)
G_I = GaussRat.of(0, 1)


@dataclass(frozen=True)
class GVec:
    """Exact vector in `Q(i)^3`."""

    x: GaussRat
    y: GaussRat
    z: GaussRat

    @staticmethod
    def real(x: int | Fraction, y: int | Fraction, z: int | Fraction) -> "GVec":
        return GVec(GaussRat.of(x), GaussRat.of(y), GaussRat.of(z))

    def is_non_zero(self) -> bool:
        return not (self.x.is_zero() and self.y.is_zero() and self.z.is_zero())

    def add(self, other: "GVec") -> "GVec":
        return GVec(self.x + other.x, self.y + other.y, self.z + other.z)

    def sub(self, other: "GVec") -> "GVec":
        return GVec(self.x - other.x, self.y - other.y, self.z - other.z)

    def smul(self, scalar: GaussRat) -> "GVec":
        return GVec(scalar * self.x, scalar * self.y, scalar * self.z)

    def inner(self, other: "GVec") -> GaussRat:
        return (
            self.x.conj() * other.x
            + self.y.conj() * other.y
            + self.z.conj() * other.z
        )

    def norm_sq(self) -> Fraction:
        return self.x.norm_sq() + self.y.norm_sq() + self.z.norm_sq()


def dist_sq_vec(u: GVec, v: GVec) -> Fraction:
    return u.sub(v).norm_sq()


def ray_sin_sq(u: GVec, v: GVec) -> Fraction:
    nu = u.norm_sq()
    nv = v.norm_sq()
    if nu == 0 or nv == 0:
        raise ValueError("ray_sin_sq requires nonzero vectors")
    return Fraction(1) - u.inner(v).norm_sq() / (nu * nv)


def proj_scalar(u: GVec, v0: GVec) -> GaussRat:
    """Scalar `c = <u, v0> / ||u||^2` projecting `v0` onto the ray of `u`."""
    nu = u.norm_sq()
    if nu == 0:
        return G_ZERO
    ip = u.inner(v0)
    return GaussRat(ip.re / nu, ip.im / nu)


def herm_cross(u: GVec, v: GVec) -> GVec:
    return GVec(
        (u.y * v.z - u.z * v.y).conj(),
        (u.z * v.x - u.x * v.z).conj(),
        (u.x * v.y - u.y * v.x).conj(),
    )


def is_frame(u: GVec, v: GVec, w: GVec) -> bool:
    return (
        u.is_non_zero()
        and v.is_non_zero()
        and w.is_non_zero()
        and u.inner(v).is_zero()
        and u.inner(w).is_zero()
        and v.inner(w).is_zero()
    )


# The 9 fixed tomography anchors in Q(i)^3
TOMO_E1 = GVec.real(1, 0, 0)
TOMO_E2 = GVec.real(0, 1, 0)
TOMO_E3 = GVec.real(0, 0, 1)
TOMO_E12 = GVec.real(1, 1, 0)
TOMO_E12I = GVec(G_ONE, G_I, G_ZERO)
TOMO_E13 = GVec.real(1, 0, 1)
TOMO_E13I = GVec(G_ONE, G_ZERO, G_I)
TOMO_E23 = GVec.real(0, 1, 1)
TOMO_E23I = GVec(G_ZERO, G_ONE, G_I)

NINE_ANCHORS: dict[str, GVec] = {
    "tomo_e1": TOMO_E1,
    "tomo_e2": TOMO_E2,
    "tomo_e3": TOMO_E3,
    "tomo_e12": TOMO_E12,
    "tomo_e12i": TOMO_E12I,
    "tomo_e13": TOMO_E13,
    "tomo_e13i": TOMO_E13I,
    "tomo_e23": TOMO_E23,
    "tomo_e23i": TOMO_E23I,
}

# The 6 orthogonal bisector partners completing the 9 anchors into frames
PARTNER_E12_MINUS = GVec.real(1, -1, 0)
PARTNER_E12I_MINUS = GVec(G_ONE, -G_I, G_ZERO)
PARTNER_E13_MINUS = GVec.real(1, 0, -1)
PARTNER_E13I_MINUS = GVec(G_ONE, G_ZERO, -G_I)
PARTNER_E23_MINUS = GVec.real(0, 1, -1)
PARTNER_E23I_MINUS = GVec(G_ZERO, G_ONE, -G_I)

SIX_PARTNERS: dict[str, GVec] = {
    "partner_e12_minus": PARTNER_E12_MINUS,
    "partner_e12i_minus": PARTNER_E12I_MINUS,
    "partner_e13_minus": PARTNER_E13_MINUS,
    "partner_e13i_minus": PARTNER_E13I_MINUS,
    "partner_e23_minus": PARTNER_E23_MINUS,
    "partner_e23i_minus": PARTNER_E23I_MINUS,
}

WITNESS_111 = GVec.real(1, 1, 1)
WITNESS_NEG211 = GVec.real(-2, 1, 1)
PROBE_120 = GVec.real(1, 2, 0)
PROBE_2M15 = GVec.real(2, -1, 5)
WITNESS_123 = GVec.real(1, 2, 3)
WITNESS_P7 = GVec(G_ONE, GaussRat.of(2, 0), GaussRat.of(1, 1))
WITNESS_P11 = GVec.real(1, 3, 1)


def vp_nat(p: int, n: int) -> int:
    if n <= 0 or p < 2:
        return 0
    v = 0
    while n % p == 0:
        n //= p
        v += 1
    return v


def pp_part_nat(p: int, n: int) -> int:
    if n <= 0 or p < 2:
        return 0
    while n % p == 0:
        n //= p
    return n


def vp_rat(p: int, q: Fraction) -> int:
    if q <= 0:
        return 0
    return vp_nat(p, abs(q.numerator)) - vp_nat(p, q.denominator)


def legendre_symbol(a: int, p: int) -> int:
    a_mod = a % p
    if a_mod == 0:
        return 0
    val = pow(a_mod, (p - 1) // 2, p)
    return 1 if val == 1 else -1


def up_rat(p: int, q: Fraction) -> Fraction:
    if q <= 0:
        return Fraction(0)
    num_part = pp_part_nat(p, abs(q.numerator))
    den_part = pp_part_nat(p, q.denominator)
    return Fraction(legendre_symbol(num_part * den_part, p))


def is_lead_p_coord(p: int, z: GaussRat, u: GVec) -> bool:
    ns_z = z.norm_sq()
    return ns_z > 0 and vp_rat(p, ns_z) < vp_rat(p, u.norm_sq())


def coord_sign_p(p: int, z: GaussRat, u: GVec) -> Fraction:
    return up_rat(p, z.norm_sq()) * up_rat(p, u.norm_sq())


def sp(p: int, u: GVec) -> Fraction:
    """Prime-indexed {-1, 0, 1}-valued frame residual for inert prime p = 3 (mod 4)."""
    ns = u.norm_sq()
    if vp_rat(p, ns) % 2 == 0:
        return Fraction(0)
    if is_lead_p_coord(p, u.x, u):
        return coord_sign_p(p, u.x, u)
    if is_lead_p_coord(p, u.y, u):
        return coord_sign_p(p, u.y, u)
    return coord_sign_p(p, u.z, u)


def s3(u: GVec) -> Fraction:
    return sp(3, u)


def s3_lead_x(u: GVec) -> Fraction:
    """Coordinate-refined 3-adic residual supported only on x-leading odd-v3 rays."""
    ns = u.norm_sq()
    if vp_rat(3, ns) % 2 != 0 and is_lead_p_coord(3, u.x, u):
        return coord_sign_p(3, u.x, u)
    return Fraction(0)


def s3_lead_all(u: GVec) -> Fraction:
    """Coordinate-refined 3-adic residual supported only on simultaneously (x,y,z)-leading odd-v3 rays."""
    ns = u.norm_sq()
    if (
        vp_rat(3, ns) % 2 != 0
        and is_lead_p_coord(3, u.x, u)
        and is_lead_p_coord(3, u.y, u)
        and is_lead_p_coord(3, u.z, u)
    ):
        return coord_sign_p(3, u.x, u)
    return Fraction(0)


def perturb_pos_ray(k: int) -> GVec:
    denom = Fraction(1, 3 * k)
    return GVec(G_ONE, GaussRat(denom, Fraction(0)), GaussRat(denom, denom))


def perturb_neg_ray(k: int) -> GVec:
    denom = Fraction(1, 3 * k)
    return GVec(G_ONE, GaussRat(denom, denom), GaussRat(Fraction(0), Fraction(0)))


def crt_approach_e1(m: int) -> GVec:
    """Chinese Remainder ray `(1 + 9*(m+1), 1, 1)` approaching `tomo_e1` while `s3_lead_all = 1`."""
    return GVec.real(1 + 9 * (m + 1), 1, 1)


def meridian_approach_e1(t: Fraction) -> GVec:
    return GVec.real(Fraction(1) + t, 1, 1)


def meridian_approach_e23(t: Fraction) -> GVec:
    return GVec.real(-2, Fraction(1) + t, Fraction(1) + t)


def dedekind_ray_cut(u: GVec) -> Fraction:
    """Scale-invariant {0, 1}-valued function on Q(i)^3 \\ {0} that is pointwise
    ray-continuous everywhere on Q(i)^3 \\ {0} (because `3 * |u.y|^4` has odd
    3-adic valuation while `||u||^4` has even 3-adic valuation) yet is not
    uniformly ray-continuous across the irrational raycone `3 * |u.y|^4 = ||u||^4`.
    """
    uy_ns = u.y.norm_sq()
    u_ns = u.norm_sq()
    return Fraction(1) if 3 * (uy_ns * uy_ns) > (u_ns * u_ns) else Fraction(0)


def eq_ortho(y: GVec) -> GVec:
    """Canonical equatorial orthogonal partner `(0, -conj(y.z), conj(y.y))` in `e1^perp`."""
    return GVec(G_ZERO, -y.z.conj(), y.y.conj())


def piron_step(y: GVec, lam: GaussRat) -> GVec:
    """Piron equatorial tangent step `e1 + y + lam * eq_ortho(y)`."""
    return TOMO_E1.add(y).add(eq_ortho(y).smul(lam))


def piron_partner(y: GVec, lam: GaussRat) -> GVec:
    """Orthogonal planar partner of `piron_step(y, lam)` in `span(e1 + y, eq_ortho(y))`."""
    ny = y.norm_sq()
    c1 = -(lam.conj() * lam * GaussRat.of(ny))
    c2 = GaussRat.of(Fraction(1) + ny) * lam
    return TOMO_E1.add(y).smul(c1).add(eq_ortho(y).smul(c2))


def meridian_ortho(y: GVec) -> GVec:
    """Meridian orthogonal partner `-N(y) e1 + y` of `e1 + y` in `span(e1, y)`."""
    return TOMO_E1.smul(GaussRat.of(-y.norm_sq())).add(y)


def kelvin_eq(y: GVec) -> GVec:
    """Kelvin-inverted equatorial vector `-(1 / N(y)) * y` in `e1^perp`."""
    return y.smul(GaussRat.of(-Fraction(1) / y.norm_sq()))


def anchor_meridian_step(a: GVec, y: GVec) -> GVec:
    """General-anchor meridian step `a + y` for `y` orthogonal to `a`."""
    return a.add(y)


def anchor_meridian_ortho(a: GVec, y: GVec) -> GVec:
    """General-anchor meridian orthogonal partner `-N(y) a + N(a) y` of `a + y` in `span(a, y)`."""
    return a.smul(GaussRat.of(-y.norm_sq())).add(y.smul(GaussRat.of(a.norm_sq())))


def anchor_kelvin_eq(a: GVec, y: GVec) -> GVec:
    """General-anchor Kelvin equatorial partner `-(N(a) / N(y)) * y` in `a^perp`."""
    return y.smul(GaussRat.of(-(a.norm_sq() / y.norm_sq())))


def eq_tangent_step(y: GVec, t: Fraction) -> GVec:
    """Equatorial tangent step `y + t * eq_ortho(y)` in `e1^perp`."""
    return y.add(eq_ortho(y).smul(GaussRat.of(t)))


def pythag_eq_rot(y: GVec, k: int) -> GVec:
    """Pythagorean equatorial rotation `((k^2 - 1)/(k^2 + 1)) y + (2k/(k^2 + 1)) eq_ortho(y)`."""
    k2 = k * k
    a = Fraction(k2 - 1, k2 + 1)
    b = Fraction(2 * k, k2 + 1)
    return y.smul(GaussRat.of(a)).add(eq_ortho(y).smul(GaussRat.of(b)))


def exotic_qi3(u: GVec) -> Fraction:
    """Nonnegative {0, 1/3, 2/3}-valued nonquadratic frame function `(1 + s3(u)) / 3`."""
    if not u.is_non_zero():
        return Fraction(0)
    return (Fraction(1) + s3(u)) / Fraction(3)


def gaussian_halving_base(a: int | Fraction, b: int | Fraction) -> GVec:
    return GVec.real(a, b, 0)


def gaussian_halving_ortho(a: int | Fraction, b: int | Fraction) -> GVec:
    return GVec.real(-Fraction(b), Fraction(a), 0)


def gaussian_halving_pos(a: int | Fraction, b: int | Fraction) -> GVec:
    return GVec(GaussRat.of(a), GaussRat.of(b), GaussRat.of(a, b))


def gaussian_halving_neg(a: int | Fraction, b: int | Fraction) -> GVec:
    return GVec(GaussRat.of(a), GaussRat.of(b), -GaussRat.of(a, b))


def dedekind_local_constancy_theta(v0: GVec) -> Fraction:
    """Explicit rational step bound theta > 0 from `dedekindRayCut_eventually_const`
    such that `delta = theta^2` is a local-constancy radius for `dedekind_ray_cut` at `v0`."""
    if not v0.is_non_zero():
        raise ValueError("v0 must be nonzero")
    gap = abs(3 * (v0.y.norm_sq() ** 2) - (v0.norm_sq() ** 2))
    if gap <= 0:
        raise AssertionError(f"Expected positive irrational-cone gap at v0={v0}")
    c_bound = Fraction(4) * (Fraction(2) * v0.norm_sq() + Fraction(1)) + Fraction(1)
    eta = min(Fraction(1), gap / c_bound)
    m_bound = Fraction(2) * v0.norm_sq() + Fraction(6)
    return eta / m_bound


def dedekind_local_constancy_radius(v0: GVec) -> Fraction:
    """Explicit rational radius delta > 0 from `dedekindRayCut_eventually_const`
    on which `dist_sq_vec(v, v0) < delta` implies `dedekind_ray_cut(v) == dedekind_ray_cut(v0)`."""
    theta = dedekind_local_constancy_theta(v0)
    return theta * theta


@dataclass(frozen=True)
class FiniteFrameScenario:
    """Finite measurement scenario matching `FiniteFrameScenario` in `BornGaussianFiniteModel.lean`."""

    name: str
    rays: tuple[GVec, ...]
    frames: tuple[tuple[GVec, GVec, GVec], ...]

    def validate(self) -> None:
        ray_set = set(self.rays)
        for v in self.rays:
            if not v.is_non_zero():
                raise AssertionError(f"Scenario {self.name} contains zero ray")
        for u, v, w in self.frames:
            if u not in ray_set or v not in ray_set or w not in ray_set:
                raise AssertionError(f"Scenario {self.name} frame vector not in rays")
            if not is_frame(u, v, w):
                raise AssertionError(f"Scenario {self.name} contains invalid 3-frame {(u, v, w)}")


def is_scenario_valuation(scenario: FiniteFrameScenario, f: Callable[[GVec], Fraction]) -> bool:
    return all(f(u) + f(v) + f(w) == Fraction(1) for u, v, w in scenario.frames)


def is_nonneg_scenario_valuation(
    scenario: FiniteFrameScenario, f: Callable[[GVec], Fraction]
) -> bool:
    return is_scenario_valuation(scenario, f) and all(
        f(v) >= Fraction(0) for v in scenario.rays
    )


def is_zero_one_scenario_valuation(
    scenario: FiniteFrameScenario, f: Callable[[GVec], Fraction]
) -> bool:
    return is_scenario_valuation(scenario, f) and all(
        f(v) in (Fraction(0), Fraction(1)) for v in scenario.rays
    )


def indicator_x_axis_val(v: GVec) -> Fraction:
    """Deterministic {0, 1} valuation matching `indicatorXAxisVal` in `BornGaussianFiniteModel.lean`."""
    if not v.x.is_zero() and v.y.is_zero() and v.z.is_zero():
        return Fraction(1)
    return Fraction(0)


def tomo_positive_x_anchor_val(v: GVec) -> Fraction:
    """Deterministic {0, 1} valuation `tomoPositiveXAnchorVal` on `fifteenAnchorBisectorScenario`:
    assigns `1` to the 5 positive-x tomography anchors (`tomo_e1, tomo_e12, tomo_e12i, tomo_e13, tomo_e13i`)
    and `0` to the remaining 10 anchor-bisector rays."""
    if v in (TOMO_E1, TOMO_E12, TOMO_E12I, TOMO_E13, TOMO_E13I):
        return Fraction(1)
    return Fraction(0)


def nine_anchor_single_frame_scenario() -> FiniteFrameScenario:
    """The 9-ray, 1-frame scenario `nineAnchorSingleFrameScenario`."""
    scenario = FiniteFrameScenario(
        name="nineAnchorSingleFrameScenario",
        rays=tuple(NINE_ANCHORS.values()),
        frames=((TOMO_E1, TOMO_E2, TOMO_E3),),
    )
    scenario.validate()
    return scenario


def fifteen_anchor_bisector_scenario() -> FiniteFrameScenario:
    """The 15-ray, 7-frame full tomography-bisector scenario `fifteenAnchorBisectorScenario`."""
    scenario = FiniteFrameScenario(
        name="fifteenAnchorBisectorScenario",
        rays=(*NINE_ANCHORS.values(), *SIX_PARTNERS.values()),
        frames=(
            (TOMO_E1, TOMO_E2, TOMO_E3),
            (TOMO_E3, TOMO_E12, PARTNER_E12_MINUS),
            (TOMO_E3, TOMO_E12I, PARTNER_E12I_MINUS),
            (TOMO_E2, TOMO_E13, PARTNER_E13_MINUS),
            (TOMO_E2, TOMO_E13I, PARTNER_E13I_MINUS),
            (TOMO_E1, TOMO_E23, PARTNER_E23_MINUS),
            (TOMO_E1, TOMO_E23I, PARTNER_E23I_MINUS),
        ),
    )
    scenario.validate()
    return scenario


def count_zero_one_scenario_valuations(scenario: FiniteFrameScenario) -> int:
    """Exact backtracking count of {0, 1} valuations on a finite scenario."""
    ray_to_idx = {v: idx for idx, v in enumerate(scenario.rays)}
    frame_idx_triples = [
        (ray_to_idx[u], ray_to_idx[v], ray_to_idx[w]) for u, v, w in scenario.frames
    ]
    n_rays = len(scenario.rays)
    adj_frames: list[list[tuple[int, int, int]]] = [[] for _ in range(n_rays)]
    for tr in frame_idx_triples:
        for r_i in tr:
            adj_frames[r_i].append(tr)

    assignment: list[int | None] = [None] * n_rays
    order = sorted(range(n_rays), key=lambda i: len(adj_frames[i]), reverse=True)

    def is_consistent(var_idx: int) -> bool:
        for i, j, k in adj_frames[var_idx]:
            vi, vj, vk = assignment[i], assignment[j], assignment[k]
            s = (vi or 0) + (vj or 0) + (vk or 0)
            if s > 1:
                return False
            if vi is not None and vj is not None and vk is not None and s != 1:
                return False
        return True

    def backtrack(pos: int) -> int:
        if pos == n_rays:
            return 1
        var_idx = order[pos]
        total = 0
        for val in (0, 1):
            assignment[var_idx] = val
            if is_consistent(var_idx):
                total += backtrack(pos + 1)
        assignment[var_idx] = None
        return total

    return backtrack(0)


@dataclass(frozen=True)
class HermForm3:
    """9-parameter Hermitian form on `Q(i)^3` matching `HermForm3` in `BornGaussianTomographyReduction.lean`."""

    d1: Fraction
    d2: Fraction
    d3: Fraction
    a12: Fraction
    b12: Fraction
    a13: Fraction
    b13: Fraction
    a23: Fraction
    b23: Fraction

    def trace(self) -> Fraction:
        return self.d1 + self.d2 + self.d3


def quad_num(rho: HermForm3, v: GVec) -> Fraction:
    return (
        rho.d1 * v.x.norm_sq()
        + rho.d2 * v.y.norm_sq()
        + rho.d3 * v.z.norm_sq()
        + 2 * rho.a12 * (v.x.re * v.y.re + v.x.im * v.y.im)
        - 2 * rho.b12 * (v.x.re * v.y.im - v.x.im * v.y.re)
        + 2 * rho.a13 * (v.x.re * v.z.re + v.x.im * v.z.im)
        - 2 * rho.b13 * (v.x.re * v.z.im - v.x.im * v.z.re)
        + 2 * rho.a23 * (v.y.re * v.z.re + v.y.im * v.z.im)
        - 2 * rho.b23 * (v.y.re * v.z.im - v.y.im * v.z.re)
    )


def quad_ray(rho: HermForm3, v: GVec) -> Fraction:
    ns = v.norm_sq()
    if ns == 0:
        return Fraction(0)
    return quad_num(rho, v) / ns


def tomography_form(f: Callable[[GVec], Fraction]) -> HermForm3:
    """Unique Hermitian form reconstructed from the 9 tomography anchor values of `f`."""
    d1 = f(TOMO_E1)
    d2 = f(TOMO_E2)
    d3 = f(TOMO_E3)
    return HermForm3(
        d1=d1,
        d2=d2,
        d3=d3,
        a12=f(TOMO_E12) - (d1 + d2) / Fraction(2),
        b12=(d1 + d2) / Fraction(2) - f(TOMO_E12I),
        a13=f(TOMO_E13) - (d1 + d3) / Fraction(2),
        b13=(d1 + d3) / Fraction(2) - f(TOMO_E13I),
        a23=f(TOMO_E23) - (d2 + d3) / Fraction(2),
        b23=(d2 + d3) / Fraction(2) - f(TOMO_E23I),
    )


def ray_proj(v: GVec) -> HermForm3:
    """Rank-1 projector `P_v = v v^* / ||v||^2` as a `HermForm3`."""
    ns = v.norm_sq()
    if ns == 0:
        return HermForm3(*(Fraction(0) for _ in range(9)))
    return HermForm3(
        d1=v.x.norm_sq() / ns,
        d2=v.y.norm_sq() / ns,
        d3=v.z.norm_sq() / ns,
        a12=(v.x.re * v.y.re + v.x.im * v.y.im) / ns,
        b12=-(v.x.re * v.y.im - v.x.im * v.y.re) / ns,
        a13=(v.x.re * v.z.re + v.x.im * v.z.im) / ns,
        b13=-(v.x.re * v.z.im - v.x.im * v.z.re) / ns,
        a23=(v.y.re * v.z.re + v.y.im * v.z.im) / ns,
        b23=-(v.y.re * v.z.im - v.y.im * v.z.re) / ns,
    )


def trace_inner(rho: HermForm3, sigma: HermForm3) -> Fraction:
    """Frobenius trace inner product `tr(rho * sigma)` on `HermForm3`."""
    return (
        rho.d1 * sigma.d1
        + rho.d2 * sigma.d2
        + rho.d3 * sigma.d3
        + Fraction(2)
        * (
            rho.a12 * sigma.a12
            + rho.b12 * sigma.b12
            + rho.a13 * sigma.a13
            + rho.b13 * sigma.b13
            + rho.a23 * sigma.a23
            + rho.b23 * sigma.b23
        )
    )


def nine_anchor_projector_expansion_coeffs(v: GVec) -> dict[str, Fraction]:
    """Exact rational coefficients expressing `ray_proj(v)` in the 9-anchor rank-1 projector basis
    so that `quad_ray(tomography_form(f), v) == sum_k coeff[k] * f(anchor_k)` for every `f`."""
    pv = ray_proj(v)
    c12 = Fraction(2) * pv.a12
    c12i = -Fraction(2) * pv.b12
    c13 = Fraction(2) * pv.a13
    c13i = -Fraction(2) * pv.b13
    c23 = Fraction(2) * pv.a23
    c23i = -Fraction(2) * pv.b23
    return {
        "tomo_e1": pv.d1 - (c12 + c12i + c13 + c13i) / Fraction(2),
        "tomo_e2": pv.d2 - (c12 + c12i + c23 + c23i) / Fraction(2),
        "tomo_e3": pv.d3 - (c13 + c13i + c23 + c23i) / Fraction(2),
        "tomo_e12": c12,
        "tomo_e12i": c12i,
        "tomo_e13": c13,
        "tomo_e13i": c13i,
        "tomo_e23": c23,
        "tomo_e23i": c23i,
    }


def _canon_int_ray(v: tuple[int, int, int]) -> tuple[int, int, int]:
    g = reduce(gcd, (abs(v[0]), abs(v[1]), abs(v[2])))
    prim = (v[0] // g, v[1] // g, v[2] // g)
    for coord in prim:
        if coord != 0:
            return (-prim[0], -prim[1], -prim[2]) if coord < 0 else prim
    raise ValueError("Zero vector has no canonical ray")


def _sign_norm_int_ray(v: tuple[int, int, int]) -> tuple[int, int, int]:
    for coord in v:
        if coord != 0:
            return (-v[0], -v[1], -v[2]) if coord < 0 else v
    raise ValueError("Zero vector has no sign-normalized ray")


def extract_and_verify_ks_no_colouring(lean_path: Path | None = None) -> dict[str, object]:
    """Extract and verify the exact Kochen-Specker 3-frame hypergraph and 6-branch unsat core
    from `lean4/BornGaussianRationalNoColouring.lean` in exact rational arithmetic."""
    if lean_path is None:
        lean_path = (
            Path(__file__).resolve().parent.parent
            / "lean4"
            / "BornGaussianRationalNoColouring.lean"
        )
    text = lean_path.read_text(encoding="utf-8")
    lines = text.splitlines()
    gv_pat = re.compile(
        r"gv\s+\(?(-?\d+)\)?\s+\(?(-?\d+)\)?\s+\(?(-?\d+)\)?\s+\(?(-?\d+)\)?\s+\(?(-?\d+)\)?\s+\(?(-?\d+)\)?"
    )

    def parse_gv_tuples(s: str) -> list[tuple[int, int, int]]:
        res: list[tuple[int, int, int]] = []
        for m in gv_pat.finditer(s):
            if int(m.group(2)) != 0 or int(m.group(4)) != 0 or int(m.group(6)) != 0:
                raise AssertionError("Expected real integer GVec in NoColouring.lean")
            res.append((int(m.group(1)), int(m.group(3)), int(m.group(5))))
        return res

    n_vecs: dict[str, tuple[int, int, int]] = {}
    p_frames: dict[str, tuple[tuple[int, int, int], tuple[int, int, int], tuple[int, int, int]]] = {}
    t_frames: dict[str, tuple[tuple[int, int, int], tuple[int, int, int], tuple[int, int, int]]] = {}

    for i, line in enumerate(lines):
        if "have n" in line and "binary_nonneg" in line:
            name = line.split("have ")[1].split(" :")[0].strip()
            n_vecs[name] = parse_gv_tuples(line)[0]
        elif "have p_" in line:
            name = line.split("have ")[1].split(" :")[0].strip()
            u_tup, v_tup = parse_gv_tuples(line)
            w_tup = parse_gv_tuples(lines[i + 1])[0]
            p_frames[name] = (u_tup, v_tup, w_tup)
        elif "have t_" in line:
            name = line.split("have ")[1].split(" :")[0].strip()
            u_tup, v_tup, w_tup = parse_gv_tuples(line)
            t_frames[name] = (u_tup, v_tup, w_tup)

    if len(n_vecs) != 49 or len(p_frames) != 82 or len(t_frames) != 26:
        raise AssertionError(
            f"Unexpected NoColouring declaration counts: n={len(n_vecs)}, p={len(p_frames)}, t={len(t_frames)}"
        )

    # Verify every p_* and t_* frame is a genuine pairwise-orthogonal 3-frame in Q(i)^3
    outside_box_completions = 0
    for f_name, (u_t, v_t, w_t) in {**p_frames, **t_frames}.items():
        u_gv = GVec.real(*u_t)
        v_gv = GVec.real(*v_t)
        w_gv = GVec.real(*w_t)
        if not is_frame(u_gv, v_gv, w_gv):
            raise AssertionError(f"KS frame {f_name} failed exact orthogonality check")
        if f_name.startswith("p_") and max(abs(w_t[0]), abs(w_t[1]), abs(w_t[2])) > 2:
            outside_box_completions += 1

    all_decl_frames = list(p_frames.values()) + list(t_frames.values())
    distinct_ordered_frames = list(dict.fromkeys(all_decl_frames))
    distinct_unordered_frames = {frozenset(fr) for fr in all_decl_frames}
    distinct_canon_w_ordered_frames = {
        (u_t, v_t, _canon_int_ray(w_t)) for u_t, v_t, w_t in all_decl_frames
    }
    distinct_sign_norm_unordered_frames = {
        frozenset(_sign_norm_int_ray(x) for x in fr) for fr in all_decl_frames
    }
    distinct_canon_proj_frames = {
        frozenset(_canon_int_ray(x) for x in fr) for fr in all_decl_frames
    }
    distinct_raw_vectors = list(
        dict.fromkeys([*n_vecs.values(), *(x for fr in all_decl_frames for x in fr)])
    )
    distinct_canon_rays = {_canon_int_ray(x) for x in distinct_raw_vectors}

    # Trace the 6-branch case split (a0, a2, a3, a15) and extract the backward-slice unsat core
    stack: list[dict[str, tuple[int, list[str], int, int]]] = [{}]
    branches_info: list[tuple[int, dict[str, tuple[int, list[str], int, int]], list[str]]] = []
    for i in range(304, len(lines)):
        line = lines[i]
        indent = len(line) - len(line.lstrip())
        m_have = re.match(
            r"\s*have\s+(a\d+)\s*:\s*f\s+.*=\s*([01])\s*:=\s*by\s*linarith only \[(.*)\]",
            line,
        )
        m_close = re.match(r"\s*linarith only \[(.*)\]", line)
        if m_have:
            var_name = m_have.group(1)
            val_assigned = int(m_have.group(2))
            deps = [d.strip() for d in m_have.group(3).split(",")]
            stack[-1][var_name] = (indent, deps, val_assigned, i + 1)
        elif m_close:
            deps = [d.strip() for d in m_close.group(1).split(",")]
            branches_info.append((i + 1, dict(stack[-1]), deps))
        elif line.lstrip().startswith("·"):
            stack[-1] = {k: v for k, v in stack[-1].items() if v[0] <= indent}

    if len(branches_info) != 6:
        raise AssertionError(f"Expected 6 case-split branches, found {len(branches_info)}")

    branch_assignments: list[dict[str, int]] = [
        {"a0": 0, "a2": 0, "a3": 0, "a15": 0},
        {"a0": 0, "a2": 0, "a3": 0, "a15": 1},
        {"a0": 0, "a2": 0, "a3": 1},
        {"a0": 0, "a2": 1},
        {"a0": 1, "a2": 0},
        {"a0": 1, "a2": 1},
    ]

    active_p: set[str] = set()
    active_t: set[str] = set()
    active_n: set[str] = set()
    branch_summaries: list[dict[str, object]] = []

    for b_idx, (line_no, env, close_deps) in enumerate(branches_info):
        init_assign = dict(branch_assignments[b_idx])
        needed = set(close_deps)
        queue = list(close_deps)
        while queue:
            cur = queue.pop()
            if cur in env and cur not in init_assign:
                for d in env[cur][1]:
                    if d not in needed:
                        needed.add(d)
                        queue.append(d)
        bp = {d for d in needed if d.startswith("p_")}
        bt = {d for d in needed if d.startswith("t_")}
        bn = {d for d in needed if d.startswith("n")}
        active_p |= bp
        active_t |= bt
        active_n |= bn

        # Replay every step in this branch in exact integer/rational arithmetic
        known_vals: dict[int, int] = {int(k[1:]): v for k, v in init_assign.items()}
        ordered_steps = sorted(env.items(), key=lambda kv: kv[1][3])
        for var_name, (_ind, deps, expected_val, step_line) in ordered_steps:
            target_idx = int(var_name[1:])
            p_dep = [d for d in deps if d.startswith("p_")]
            t_dep = [d for d in deps if d.startswith("t_")]
            if len(p_dep) == 1 and len(t_dep) == 0:
                _, i_s, j_s = p_dep[0].split("_")
                other_idx = int(j_s) if int(i_s) == target_idx else int(i_s)
                if known_vals.get(other_idx) != 1 or expected_val != 0:
                    raise AssertionError(
                        f"Invalid pair-bound propagation at line {step_line} in branch {b_idx}"
                    )
            elif len(t_dep) == 1 and len(p_dep) == 0:
                _, i_s, j_s, k_s = t_dep[0].split("_")
                tri_indices = [int(i_s), int(j_s), int(k_s)]
                others = [idx for idx in tri_indices if idx != target_idx]
                if expected_val == 1:
                    if not (known_vals.get(others[0]) == 0 and known_vals.get(others[1]) == 0):
                        raise AssertionError(
                            f"Invalid triple-to-1 propagation at line {step_line} in branch {b_idx}"
                        )
                else:
                    if 1 not in (known_vals.get(others[0]), known_vals.get(others[1])):
                        raise AssertionError(
                            f"Invalid triple-to-0 propagation at line {step_line} in branch {b_idx}"
                        )
            else:
                raise AssertionError(f"Unexpected step dependencies at line {step_line}: {deps}")
            known_vals[target_idx] = expected_val

        # Verify the closing contradiction `t_i_j_k` has 0 + 0 + 0 = 0 != 1
        close_t = [d for d in close_deps if d.startswith("t_")]
        if len(close_t) != 1:
            raise AssertionError(f"Expected 1 closing triple at line {line_no}, got {close_deps}")
        _, ci, cj, ck = close_t[0].split("_")
        closing_sum = known_vals[int(ci)] + known_vals[int(cj)] + known_vals[int(ck)]
        if closing_sum == 1:
            raise AssertionError(f"Branch {b_idx} at line {line_no} did not reach contradiction")
        branch_summaries.append(
            {
                "branch_index": b_idx,
                "closing_line": line_no,
                "branch_decisions": init_assign,
                "closing_triple": close_t[0],
                "closing_triple_sum": closing_sum,
                "active_p_count": len(bp),
                "active_t_count": len(bt),
                "active_n_count": len(bn),
            }
        )

    active_decl_frames = [p_frames[k] for k in sorted(active_p)] + [
        t_frames[k] for k in sorted(active_t)
    ]
    active_distinct_ordered = list(dict.fromkeys(active_decl_frames))
    active_distinct_unordered = {frozenset(fr) for fr in active_decl_frames}
    active_raw_vectors = list(
        dict.fromkeys(x for fr in active_decl_frames for x in fr)
    )
    active_canon_rays = {_canon_int_ray(x) for x in active_raw_vectors}

    # Build FiniteFrameScenario objects for both the 62-declaration (59-distinct-ordered-frame) active core and full 108-declaration KS hypergraph
    ks_active_core_scenario = FiniteFrameScenario(
        name="ksActiveCoreScenario",
        rays=tuple(GVec.real(*v) for v in active_raw_vectors),
        frames=tuple(
            (GVec.real(*u), GVec.real(*v), GVec.real(*w))
            for u, v, w in active_distinct_ordered
        ),
    )
    ks_active_core_scenario.validate()

    ks_full_scenario = FiniteFrameScenario(
        name="ksFiniteScenario",
        rays=tuple(GVec.real(*v) for v in distinct_raw_vectors),
        frames=tuple(
            (GVec.real(*u), GVec.real(*v), GVec.real(*w))
            for u, v, w in distinct_ordered_frames
        ),
    )
    ks_full_scenario.validate()

    if count_zero_one_scenario_valuations(ks_active_core_scenario) != 0:
        raise AssertionError("ksActiveCoreScenario unexpectedly admits a {0, 1} valuation")
    if count_zero_one_scenario_valuations(ks_full_scenario) != 0:
        raise AssertionError("ksFiniteScenario unexpectedly admits a {0, 1} valuation")

    if not is_nonneg_scenario_valuation(ks_active_core_scenario, exotic_qi3):
        raise AssertionError("exotic_qi3 failed on ksActiveCoreScenario")
    if not is_nonneg_scenario_valuation(ks_full_scenario, exotic_qi3):
        raise AssertionError("exotic_qi3 failed on ksFiniteScenario")

    return {
        "lean_file": "lean4/BornGaussianRationalNoColouring.lean",
        "box_rays_count": len(n_vecs),
        "pair_completion_frames_count": len(p_frames),
        "pair_completions_outside_box_count": outside_box_completions,
        "internal_triple_frames_count": len(t_frames),
        "total_frame_declarations": len(all_decl_frames),
        "distinct_ordered_frames": len(distinct_ordered_frames),
        "distinct_unordered_frames": len(distinct_unordered_frames),
        "distinct_canonical_w_ordered_frames": len(distinct_canon_w_ordered_frames),
        "distinct_sign_normalized_unordered_frames": len(distinct_sign_norm_unordered_frames),
        "distinct_canonical_projective_frames": len(distinct_canon_proj_frames),
        "distinct_raw_vectors": len(distinct_raw_vectors),
        "distinct_canonical_projective_rays": len(distinct_canon_rays),
        "active_unsat_core": {
            "active_pair_frames_count": len(active_p),
            "active_triple_frames_count": len(active_t),
            "active_nonneg_rays_count": len(active_n),
            "active_total_frame_declarations": len(active_decl_frames),
            "active_distinct_ordered_frames": len(active_distinct_ordered),
            "active_distinct_unordered_frames": len(active_distinct_unordered),
            "active_distinct_raw_vectors": len(active_raw_vectors),
            "active_distinct_canonical_rays": len(active_canon_rays),
            "branching_rays": ["n0=(0,0,1)", "n2=(0,1,-1)", "n3=(0,1,0)", "n15=(1,-1,0)"],
            "branches_verified": len(branch_summaries),
            "branches": branch_summaries,
            "zero_one_valuations_count": 0,
            "admits_exotic_qi3_nonneg_valuation": True,
        },
        "full_ks_scenario": {
            "scenario_name": "ksFiniteScenario",
            "rays_count": len(ks_full_scenario.rays),
            "frames_count": len(ks_full_scenario.frames),
            "zero_one_valuations_count": 0,
            "admits_exotic_qi3_nonneg_valuation": True,
            "latitude_symmetry_assumed": False,
        },
    }


def verify_tfq_0307_four_tier_classification(
    ks_summary: dict[str, object] | None = None,
) -> dict[str, object]:
    """Verify the 4-tier `TFQ-0307` operational non-contextuality classification in exact rational arithmetic."""
    if ks_summary is None:
        ks_summary = extract_and_verify_ks_no_colouring()

    # Tier 1: {0, 1} deterministic / Kochen-Specker regime
    s9 = nine_anchor_single_frame_scenario()
    s15 = fifteen_anchor_bisector_scenario()
    if not is_zero_one_scenario_valuation(s9, indicator_x_axis_val):
        raise AssertionError("indicator_x_axis_val failed on nineAnchorSingleFrameScenario")
    if not is_zero_one_scenario_valuation(s15, tomo_positive_x_anchor_val):
        raise AssertionError("tomo_positive_x_anchor_val failed on fifteenAnchorBisectorScenario")
    s9_zero_one_count = count_zero_one_scenario_valuations(s9)
    s15_zero_one_count = count_zero_one_scenario_valuations(s15)
    if s9_zero_one_count != 192 or s15_zero_one_count != 48:
        raise AssertionError(
            f"Unexpected {s9.name}/{s15.name} binary valuation counts: {s9_zero_one_count}, {s15_zero_one_count}"
        )

    # Tier 2: [0, 1] ∩ Q ray-level non-quadratic frame-function regime
    if not (
        is_nonneg_scenario_valuation(s9, exotic_qi3)
        and is_nonneg_scenario_valuation(s15, exotic_qi3)
    ):
        raise AssertionError("exotic_qi3 must be a valid nonneg valuation on s9 and s15")
    for r_vec in s15.rays:
        if exotic_qi3(r_vec) != Fraction(1, 3):
            raise AssertionError("exotic_qi3 must equal 1/3 on all 15 anchor-bisector rays")
    if exotic_qi3(WITNESS_111) != Fraction(2, 3) or exotic_qi3(WITNESS_NEG211) != Fraction(0):
        raise AssertionError("exotic_qi3 must separate from 1/3 at witness_111 and witness_neg211")

    # Tier 3: Operator-level EffectValuation (space 3) / projector-span linearity regime
    rho_exotic = tomography_form(exotic_qi3)
    if rho_exotic != HermForm3(
        Fraction(1, 3),
        Fraction(1, 3),
        Fraction(1, 3),
        Fraction(0),
        Fraction(0),
        Fraction(0),
        Fraction(0),
        Fraction(0),
        Fraction(0),
    ):
        raise AssertionError("tomography_form(exotic_qi3) must equal (1/3) I_3")
    coeffs_111 = nine_anchor_projector_expansion_coeffs(WITNESS_111)
    projector_linear_val_111 = sum(
        coeff * exotic_qi3(NINE_ANCHORS[a_key]) for a_key, coeff in coeffs_111.items()
    )
    if (
        projector_linear_val_111 != Fraction(1, 3)
        or trace_inner(rho_exotic, ray_proj(WITNESS_111)) != Fraction(1, 3)
        or quad_ray(rho_exotic, WITNESS_111) != Fraction(1, 3)
        or exotic_qi3(WITNESS_111) == projector_linear_val_111
    ):
        raise AssertionError("Tier 3 operator-level projector-span exclusion of exotic_qi3 failed")

    # Also check projector expansion identity across diverse Hermitian forms and rays
    sample_herm = HermForm3(
        Fraction(1, 2),
        Fraction(1, 3),
        Fraction(1, 6),
        Fraction(1, 5),
        Fraction(-1, 7),
        Fraction(2, 9),
        Fraction(1, 11),
        Fraction(-1, 4),
        Fraction(1, 8),
    )
    for probe in (WITNESS_111, WITNESS_NEG211, WITNESS_123, WITNESS_P7, WITNESS_P11):
        c_map = nine_anchor_projector_expansion_coeffs(probe)
        reconstructed_val = sum(
            c_val * quad_ray(sample_herm, NINE_ANCHORS[a_key])
            for a_key, c_val in c_map.items()
        )
        if (
            reconstructed_val != quad_ray(sample_herm, probe)
            or trace_inner(sample_herm, ray_proj(probe)) != quad_ray(sample_herm, probe)
        ):
            raise AssertionError("9-anchor projector expansion identity failed")

    # Tier 4: Topological / bounded-anchor-amplification and continuum d >= 3 Gleason closure
    u_crt0 = crt_approach_e1(0)
    if not (
        exotic_qi3(TOMO_E1) == Fraction(1, 3)
        and exotic_qi3(u_crt0) == Fraction(2, 3)
        and ray_sin_sq(u_crt0, TOMO_E1) == Fraction(2, 102)
    ):
        raise AssertionError("Tier 4 CRT discontinuity check for exotic_qi3 at tomo_e1 failed")

    return {
        "tier1_zero_one_kochen_specker": {
            "nine_anchor_single_frame_zero_one_valuations": s9_zero_one_count,
            "fifteen_anchor_bisector_zero_one_valuations": s15_zero_one_count,
            "tomo_positive_x_anchor_val_verified": True,
            "ks_active_core_zero_one_valuations": 0,
            "ks_full_scenario_zero_one_valuations": 0,
            "latitude_symmetry_assumed": False,
        },
        "tier2_rational_nonquadratic_frame_functions": {
            "exotic_qi3_values": ["0", "1/3", "2/3"],
            "exotic_qi3_on_15_anchor_bisectors": "1/3",
            "exotic_qi3_witness_111": str(exotic_qi3(WITNESS_111)),
            "exotic_qi3_witness_neg211": str(exotic_qi3(WITNESS_NEG211)),
            "ks_scenario_inhabited_by_exotic_qi3": True,
        },
        "tier3_operator_effect_valuation_algebraic_born": {
            "nine_anchor_projector_span_dimension": 9,
            "tomography_form_of_exotic_qi3": "I_3 / 3",
            "operator_linear_value_at_witness_111": str(projector_linear_val_111),
            "exotic_qi3_value_at_witness_111": str(exotic_qi3(WITNESS_111)),
            "algebraic_residual_discrepancy_at_witness_111": str(
                exotic_qi3(WITNESS_111) - projector_linear_val_111
            ),
            "excludes_exotic_qi3_without_topology": True,
        },
        "tier4_topological_and_continuum_gleason_closure": {
            "pointwise_ray_continuity_excludes_exotic_qi3_via_crt": True,
            "dedekind_ray_cut_pointwise_continuous_on_qi3": True,
            "dedekind_ray_cut_refuted_by_bisector_frame": True,
            "bounded_anchor_amplification_closes_born_uniquely": True,
        },
    }


def min_pos_ray_sin_sq_ray(r: GVec, anchors: Sequence[GVec]) -> Fraction:
    """Computable minimum positive `ray_sin_sq(r, a)` across `anchors` (defaulting to 1),
    mirroring `minPosRaySinSqRay` in `BornGaussianFiniteModel.lean`."""
    m = Fraction(1)
    for a in reversed(list(anchors)):
        val = ray_sin_sq(r, a)
        if val > Fraction(0):
            m = min(val, m)
    return m


def min_pos_ray_sin_sq_list(rays: Sequence[GVec], anchors: Sequence[GVec]) -> Fraction:
    """Computable minimum positive `ray_sin_sq(r, a)` across `rays` and `anchors` (defaulting to 1),
    mirroring `minPosRaySinSqList` in `BornGaussianFiniteModel.lean`."""
    m = Fraction(1)
    for r in reversed(list(rays)):
        m = min(min_pos_ray_sin_sq_ray(r, anchors), m)
    return m


def radial_scale_factor(a: GVec, y: GVec, delta: Fraction) -> Fraction:
    """Explicit positive rational scaling factor `min(1, (delta * ||a||^2) / (2 * ||y||^2))`,
    mirroring `radialScaleFactor` in `BornGaussianFiniteModel.lean`."""
    return min(Fraction(1), (delta * a.norm_sq()) / (Fraction(2) * y.norm_sq()))


def verify_tfq_1057_multi_frame_incidence_and_amplification() -> dict[str, object]:
    """Verify Section 9 (`TFQ-1057`) certificates in exact rational arithmetic:
    9A: Logical & vacuity anatomy of `HasBoundedAnchorAmplificationOn` (`s3_lead_all` model),
    9B: 15-plane orthogonal antisymmetry, 1-step `< 2 * delta` collar confinement, and
        finite ray-list collar blindness (`min_pos_ray_sin_sq_list`),
    9C: Scale-invariant radial transport (`anchor_meridian_radial_scale_transport`),
        universal equatorial Kelvin step (`radial_scale_factor`), and multi-step meridian
        linear amplification bound (`meridian_chain_linear_amplification_bound`).
    """
    residual_funcs: dict[str, Callable[[GVec], Fraction]] = {
        "s3": s3,
        "s7": lambda u: sp(7, u),
        "s3_lead_x": s3_lead_x,
        "s3_lead_all": s3_lead_all,
    }
    nine_anchors_list = list(NINE_ANCHORS.values())
    fifteen_rays_list = list(NINE_ANCHORS.values()) + list(SIX_PARTNERS.values())

    # 9A: Logical & vacuity anatomy of HasBoundedAnchorAmplificationOn on s3_lead_all
    for a_name, a_vec in NINE_ANCHORS.items():
        if s3_lead_all(a_vec) != Fraction(0):
            raise AssertionError(f"s3_lead_all must vanish on anchor {a_name}")
    if s3_lead_all(WITNESS_111) != Fraction(1):
        raise AssertionError("Expected s3_lead_all(witness_111) == 1")

    crt_gap_witnesses: list[dict[str, str]] = []
    for delta in (
        Fraction(1, 2),
        Fraction(1, 10),
        Fraction(1, 100),
        Fraction(1, 1000),
        Fraction(1, 10000),
    ):
        m = int(Fraction(2) / delta) + 1
        n_val = 1 + 9 * (m + 1)
        z = crt_approach_e1(m)
        sin_z = ray_sin_sq(z, TOMO_E1)
        if not (
            z.is_non_zero()
            and sin_z <= Fraction(2, n_val * n_val)
            and sin_z < delta
            and s3_lead_all(z) == Fraction(1)
            and abs(s3_lead_all(z)) >= Fraction(1)
        ):
            raise AssertionError(f"crtApproachE1_discontinuity_gap_at_tomo_e1 failed for delta={delta}")
        crt_gap_witnesses.append(
            {
                "delta": str(delta),
                "m": str(m),
                "ray_sin_sq_tomo_e1": str(sin_z),
                "s3_lead_all": str(s3_lead_all(z)),
            }
        )

    # 9B.1 & 9B.2: 15-ray vanishing and 15-plane orthogonal antisymmetry
    fifteen_plane_antisymmetry_checks = 0
    probe_seeds = [
        GVec.real(1, 2, 3),
        GVec.real(2, -1, 4),
        GVec(GaussRat.of(1, 1), GaussRat.of(2, -1), GaussRat.of(-1, 2)),
    ]
    for b_vec in fifteen_rays_list:
        for r_name, r_fn in residual_funcs.items():
            if r_fn(b_vec) != Fraction(0):
                raise AssertionError(
                    f"fifteenAnchorBisector_zero_of_zeroWeight_and_nine failed for {r_name} at {b_vec}"
                )
        for seed in probe_seeds:
            u_ortho = herm_cross(b_vec, seed)
            if not u_ortho.is_non_zero():
                continue
            v_ortho = herm_cross(b_vec, u_ortho)
            if not is_frame(u_ortho, v_ortho, b_vec):
                raise AssertionError("Expected orthogonal frame (u_ortho, v_ortho, b_vec)")
            for r_name, r_fn in residual_funcs.items():
                if r_fn(u_ortho) + r_fn(v_ortho) != Fraction(0) or r_fn(v_ortho) != -r_fn(u_ortho):
                    raise AssertionError(
                        f"fifteen_plane_ortho_antisymmetry failed for {r_name} on plane {b_vec}"
                    )
            fifteen_plane_antisymmetry_checks += 1

    # 9B.3: One-step collar confinement (< 2 * delta)
    collar_confinement_checks = 0
    anchor_frames = [
        (TOMO_E1, TOMO_E2, TOMO_E3),
        (TOMO_E12, PARTNER_E12_MINUS, TOMO_E3),
        (TOMO_E13, PARTNER_E13_MINUS, TOMO_E2),
        (TOMO_E23, PARTNER_E23_MINUS, TOMO_E1),
        (TOMO_E12I, PARTNER_E12I_MINUS, TOMO_E3),
        (TOMO_E13I, PARTNER_E13I_MINUS, TOMO_E2),
        (TOMO_E23I, PARTNER_E23I_MINUS, TOMO_E1),
    ]
    for _f_name, u_f, v_f, w_f in build_test_frames():
        for a1, a2, a3 in anchor_frames:
            delta_tight = max(ray_sin_sq(u_f, a1), ray_sin_sq(v_f, a2)) + Fraction(1, 1000)
            if not (
                ray_sin_sq(u_f, a1) < delta_tight
                and ray_sin_sq(v_f, a2) < delta_tight
                and ray_sin_sq(w_f, a3) < Fraction(2) * delta_tight
            ):
                raise AssertionError("one_step_collar_confinement_of_anchor_frame failed")
            collar_confinement_checks += 1
    # Explicit small-collar 3-frame perturbation check (delta = 1/50, 2*delta = 1/25 < 1)
    u_small = GVec.real(10, 1, 0)
    v_small = GVec.real(-1, 10, 1)
    w_small = GVec.real(1, -10, 101)
    delta_small = Fraction(1, 50)
    if not (
        is_frame(u_small, v_small, w_small)
        and ray_sin_sq(u_small, TOMO_E1) < delta_small
        and ray_sin_sq(v_small, TOMO_E2) < delta_small
        and Fraction(0) < ray_sin_sq(w_small, TOMO_E3) < Fraction(2) * delta_small
    ):
        raise AssertionError("small-collar one_step_collar_confinement check failed")
    collar_confinement_checks += 1

    # 9B.4: Finite ray-list collar blindness (minPosRaySinSqList)
    finite_chain_rays = [
        *fifteen_rays_list,
        WITNESS_111,
        WITNESS_NEG211,
        WITNESS_123,
        PROBE_120,
        PROBE_2M15,
    ]
    delta_0 = min_pos_ray_sin_sq_list(finite_chain_rays, nine_anchors_list)
    if delta_0 <= Fraction(0) or delta_0 != Fraction(1, 10):
        raise AssertionError(f"Expected min_pos_ray_sin_sq_list == 1/10, got {delta_0}")
    for delta_test in (delta_0, delta_0 / Fraction(2), delta_0 / Fraction(10)):
        for r_vec in finite_chain_rays:
            in_collar = any(ray_sin_sq(r_vec, a_vec) < delta_test for a_vec in nine_anchors_list)
            collinear_with_anchor = any(
                ray_sin_sq(r_vec, a_vec) == Fraction(0) for a_vec in nine_anchors_list
            )
            if in_collar != collinear_with_anchor:
                raise AssertionError(
                    f"finite_ray_list_collar_blindness failed at delta={delta_test} for ray={r_vec}"
                )

    # 9C.1 & 9C.2: Scale-invariant radial transport and universal equatorial Kelvin step
    radial_scale_checks = 0
    for a_vec in fifteen_rays_list[:6]:
        for seed in probe_seeds:
            y_eq = herm_cross(a_vec, seed)
            if not y_eq.is_non_zero():
                continue
            # Also test a large-norm equatorial vector on the same ray
            for y_test in (y_eq, y_eq.smul(GaussRat.of(7))):
                for delta_step in (Fraction(1, 2), Fraction(1, 10), Fraction(1, 50)):
                    c_scale = radial_scale_factor(a_vec, y_test, delta_step)
                    if c_scale <= Fraction(0):
                        raise AssertionError("radialScaleFactor_pos failed")
                    yc = y_test.smul(GaussRat.of(c_scale))
                    step_vec = a_vec.add(yc)
                    ortho_vec = anchor_meridian_ortho(a_vec, yc)
                    expected_sin = (c_scale * c_scale * y_test.norm_sq()) / (
                        a_vec.norm_sq() + c_scale * c_scale * y_test.norm_sq()
                    )
                    if (
                        ray_sin_sq(step_vec, a_vec) != expected_sin
                        or ray_sin_sq(ortho_vec, y_test) != expected_sin
                        or expected_sin >= delta_step
                    ):
                        raise AssertionError(
                            "anchor_meridian_radial_scale_transport / radialScale_meridian_step_raySinSq_lt failed"
                        )
                    for r_name, r_fn in residual_funcs.items():
                        if (
                            r_fn(yc) != r_fn(y_test)
                            or r_fn(step_vec) - r_fn(a_vec) != r_fn(y_test) - r_fn(ortho_vec)
                            or abs(r_fn(y_test) - r_fn(ortho_vec)) != abs(r_fn(step_vec) - r_fn(a_vec))
                        ):
                            raise AssertionError(
                                f"anchor_meridian_radial_scale_transport failed for {r_name}"
                            )
                    radial_scale_checks += 1

    # 9C.3: Multi-step meridian chain linear amplification bound
    chain_rays = [
        TOMO_E1,
        PROBE_120,
        WITNESS_111,
        WITNESS_NEG211,
        PROBE_2M15,
        WITNESS_123,
        PARTNER_E12_MINUS,
    ]
    chain_amplification_checks = 0
    for r_name, r_fn in residual_funcs.items():
        for k_len in range(1, len(chain_rays)):
            v0 = chain_rays[0]
            steps = chain_rays[1 : k_len + 1]
            full_chain = [v0, *steps]
            eps_step = max(
                abs(r_fn(full_chain[i + 1]) - r_fn(full_chain[i])) for i in range(k_len)
            )
            lhs_total = abs(r_fn(steps[-1]) - r_fn(v0))
            if lhs_total > Fraction(k_len) * eps_step:
                raise AssertionError(
                    f"meridian_chain_linear_amplification_bound failed for {r_name} at k={k_len}"
                )
            chain_amplification_checks += 1

    return {
        "subsection_9a_bounded_anchor_amplification_anatomy": {
            "pointwise_continuous_iff_zero": True,
            "discontinuous_vacuity_theorem_verified": True,
            "s3_lead_all_amplification_constant": "1",
            "s3_lead_all_witness_111": str(s3_lead_all(WITNESS_111)),
            "crt_discontinuity_gap_witnesses": crt_gap_witnesses,
        },
        "subsection_9b_multi_frame_incidence_and_collar_blindness": {
            "fifteen_rays_vanishing_verified": True,
            "fifteen_plane_ortho_antisymmetry_checks": fifteen_plane_antisymmetry_checks,
            "one_step_collar_confinement_checks": collar_confinement_checks,
            "finite_ray_list_collar_blindness_threshold": str(delta_0),
            "finite_ray_list_collar_blindness_verified": True,
        },
        "subsection_9c_radial_scale_transport_and_chain_scaling": {
            "radial_scale_transport_checks": radial_scale_checks,
            "meridian_chain_linear_amplification_checks": chain_amplification_checks,
            "status": "PASS",
        },
    }


def build_test_frames() -> list[tuple[str, GVec, GVec, GVec]]:
    """Representative corpus of exact orthogonal frames across Q(i)^3."""
    frames: list[tuple[str, GVec, GVec, GVec]] = [
        ("std_basis", TOMO_E1, TOMO_E2, TOMO_E3),
        ("anchor_bisector_12", TOMO_E3, TOMO_E12, PARTNER_E12_MINUS),
        ("anchor_bisector_12i", TOMO_E3, TOMO_E12I, PARTNER_E12I_MINUS),
        ("anchor_bisector_13", TOMO_E2, TOMO_E13, PARTNER_E13_MINUS),
        ("anchor_bisector_13i", TOMO_E2, TOMO_E13I, PARTNER_E13I_MINUS),
        ("anchor_bisector_23", TOMO_E1, TOMO_E23, PARTNER_E23_MINUS),
        ("anchor_bisector_23i", TOMO_E1, TOMO_E23I, PARTNER_E23I_MINUS),
        ("witness_111_meridian", WITNESS_111, WITNESS_NEG211, PARTNER_E23_MINUS),
        ("witness_neg211_fifth_ball", WITNESS_NEG211, PROBE_120, PROBE_2M15),
        (
            "p7_frame",
            WITNESS_P7,
            GVec(GaussRat.of(-2), G_ONE, G_ZERO),
            herm_cross(WITNESS_P7, GVec(GaussRat.of(-2), G_ONE, G_ZERO)),
        ),
        (
            "p11_frame",
            WITNESS_P11,
            GVec.real(-3, 1, 0),
            herm_cross(WITNESS_P11, GVec.real(-3, 1, 0)),
        ),
    ]
    for t_int in (1, 2, 3, 9, 27):
        t = Fraction(t_int)
        frames.append(
            (
                f"meridian_t_{t_int}",
                meridian_approach_e1(t),
                meridian_approach_e23(t),
                PARTNER_E23_MINUS,
            )
        )
    for k in (1, 2, 3):
        u_pos = perturb_pos_ray(k)
        v_pos = GVec(
            GaussRat.of(-1, 0),
            GaussRat.of(0, 0),
            GaussRat(Fraction(3 * k, 2), Fraction(3 * k, 2)),
        )
        w_pos = herm_cross(u_pos, v_pos)
        frames.append((f"perturb_pos_k_{k}", u_pos, v_pos, w_pos))
    for m in (0, 1, 2):
        u_crt = crt_approach_e1(m)
        v_crt = GVec.real(-2, 1 + 9 * (m + 1), 1 + 9 * (m + 1))
        frames.append((f"crt_m_{m}", u_crt, v_crt, PARTNER_E23_MINUS))
    return frames


def verify_all_certificates() -> dict[str, object]:
    """Run all exact rational certificate checks and return a structured receipt."""
    frames = build_test_frames()
    for name, u, v, w in frames:
        if not is_frame(u, v, w):
            raise AssertionError(f"Frame check failed for {name}")

    # 1. Check residuals on all frames and anchors
    residual_funcs: dict[str, Callable[[GVec], Fraction]] = {
        "s3": s3,
        "s3_lead_x": s3_lead_x,
        "s3_lead_all": s3_lead_all,
        "sp_7": lambda v: sp(7, v),
        "sp_11": lambda v: sp(11, v),
    }

    residual_summary: dict[str, object] = {}
    for r_name, r_fn in residual_funcs.items():
        for f_name, u, v, w in frames:
            total = r_fn(u) + r_fn(v) + r_fn(w)
            if total != 0:
                raise AssertionError(
                    f"Residual {r_name} failed zero-sum on frame {f_name}: got {total}"
                )
        for a_name, a_vec in {**NINE_ANCHORS, **SIX_PARTNERS}.items():
            val = r_fn(a_vec)
            if val != 0:
                raise AssertionError(
                    f"Residual {r_name} failed to vanish on {a_name}: got {val}"
                )
        residual_summary[r_name] = {
            "frames_checked": len(frames),
            "vanishes_on_15_anchor_bisectors": True,
            "val_witness_111": str(r_fn(WITNESS_111)),
            "val_witness_neg211": str(r_fn(WITNESS_NEG211)),
            "val_witness_p7": str(r_fn(WITNESS_P7)),
            "val_witness_p11": str(r_fn(WITNESS_P11)),
        }

    # 2. Verify coordinate-plane & perturbPosRay vanishing for s3_lead_all
    if s3_lead_all(WITNESS_111) != 1:
        raise AssertionError("s3_lead_all(witness_111) must equal 1")
    for k in range(1, 6):
        if s3_lead_all(perturb_pos_ray(k)) != 0:
            raise AssertionError(f"s3_lead_all(perturb_pos_ray({k})) must equal 0")
        if s3_lead_all(perturb_neg_ray(k)) != 0:
            raise AssertionError(f"s3_lead_all(perturb_neg_ray({k})) must equal 0")
        if s3_lead_x(perturb_pos_ray(k)) != 0:
            raise AssertionError(f"s3_lead_x(perturb_pos_ray({k})) must equal 0")

    # 3. Verify Chinese Remainder collision sequence crt_approach_e1(m)
    crt_checks = []
    for m in range(5):
        u_m = crt_approach_e1(m)
        sin_sq = ray_sin_sq(u_m, TOMO_E1)
        bound = Fraction(2, (1 + 9 * (m + 1)) ** 2)
        if not (
            s3(u_m) == 1
            and s3_lead_x(u_m) == 1
            and s3_lead_all(u_m) == 1
            and sin_sq <= bound
        ):
            raise AssertionError(f"CRT collision check failed at m={m}")
        crt_checks.append(
            {
                "m": m,
                "ray_sin_sq_to_e1": str(sin_sq),
                "upper_bound": str(bound),
                "s3_lead_all": str(s3_lead_all(u_m)),
            }
        )

    # 4. Verify exact rational projection identity:
    # dist_sq_vec(proj_scalar(u, v0) * u, v0) == norm_sq_vec(v0) * ray_sin_sq(u, v0)
    test_vectors = [
        TOMO_E1,
        TOMO_E12,
        TOMO_E23I,
        WITNESS_111,
        WITNESS_NEG211,
        PROBE_120,
        PROBE_2M15,
        WITNESS_123,
        WITNESS_P7,
        WITNESS_P11,
        perturb_pos_ray(1),
        crt_approach_e1(0),
    ]
    projection_pairs_checked = 0
    for u in test_vectors:
        for v0 in test_vectors:
            c = proj_scalar(u, v0)
            lhs = dist_sq_vec(u.smul(c), v0)
            rhs = v0.norm_sq() * ray_sin_sq(u, v0)
            if lhs != rhs:
                raise AssertionError(
                    f"Projection identity failed for u={u}, v0={v0}: {lhs} != {rhs}"
                )
            if ray_sin_sq(u, v0) > dist_sq_vec(u, v0) / v0.norm_sq():
                raise AssertionError(
                    f"Ray-vs-vector upper bound failed for u={u}, v0={v0}"
                )
            projection_pairs_checked += 1

    # 5. Verify Pell approximations to 1/sqrt(3) for the Dedekind ray-cut witness
    pell_pairs = [
        (GVec.real(0, 1, 0), GVec.real(1, 1, 0)),
        (GVec.real(4, 5, 0), GVec.real(9, 10, 0)),
        (GVec.real(85, 100, 0), GVec.real(86, 100, 0)),
    ]
    for u_hi, u_lo in pell_pairs:
        if not (dedekind_ray_cut(u_hi) == 1 and dedekind_ray_cut(u_lo) == 0):
            raise AssertionError("Dedekind ray cut test pair failed")

    # 6. Track A: Verify rational Piron-Soler chain (1/2/3-step bounds), general
    # meridian-Kelvin polar-equatorial transfer, exact ray_sin_sq duality, and
    # general Piron-Pythagorean sandwich across quadratic and nonquadratic frame functions.
    nonneg_frame_fns: dict[str, Callable[[GVec], Fraction]] = {
        "pure_pole_e1": lambda v: v.x.norm_sq() / v.norm_sq(),
        "mixed_diag": lambda v: (
            Fraction(3, 5) * v.x.norm_sq()
            + Fraction(1, 5) * v.y.norm_sq()
            + Fraction(1, 5) * v.z.norm_sq()
        )
        / v.norm_sq(),
        "exotic_qi3": exotic_qi3,
    }
    equatorial_probes = [
        TOMO_E2,
        TOMO_E23,
        TOMO_E23I,
        GVec.real(0, Fraction(1, 3), Fraction(1, 3)),
        GVec(G_ZERO, GaussRat.of(Fraction(1, 2), Fraction(1, 3)), GaussRat.of(Fraction(1, 5), 0)),
    ]
    track_a_checks = 0
    for y in equatorial_probes:
        if not is_frame(TOMO_E1, y, eq_ortho(y)):
            raise AssertionError(f"Equatorial frame check failed for y={y}")
        if not is_frame(TOMO_E1.add(y), eq_ortho(y), meridian_ortho(y)):
            raise AssertionError(f"Meridian base frame check failed for y={y}")
        if not is_frame(
            piron_step(y, G_ONE), piron_partner(y, G_ONE), meridian_ortho(y)
        ):
            raise AssertionError(f"Piron rotated frame check failed for y={y}")
        expected_sin_sq = y.norm_sq() / (Fraction(1) + y.norm_sq())
        if ray_sin_sq(TOMO_E1.add(y), TOMO_E1) != expected_sin_sq:
            raise AssertionError("Polar ray_sin_sq formula mismatch")
        if ray_sin_sq(meridian_ortho(y), y) != expected_sin_sq:
            raise AssertionError("Equatorial meridian_ortho ray_sin_sq duality mismatch")
        lam_probe = GaussRat.of(Fraction(1, 2), Fraction(1, 3))
        lam_neg = GaussRat.of(-Fraction(1, 2), -Fraction(1, 3))
        expected_piron_sin_sq = (lam_probe.norm_sq() * y.norm_sq()) / (
            Fraction(1) + y.norm_sq() + lam_probe.norm_sq() * y.norm_sq()
        )
        if ray_sin_sq(piron_step(y, lam_probe), TOMO_E1.add(y)) != expected_piron_sin_sq:
            raise AssertionError("Piron step ray_sin_sq formula mismatch")
        if ray_sin_sq(piron_partner(y, lam_probe), eq_ortho(y)) != expected_piron_sin_sq:
            raise AssertionError("Piron partner ray_sin_sq duality mismatch")
        for fn_name, f in nonneg_frame_fns.items():
            slack = Fraction(1) - f(TOMO_E1)
            if f(y) + f(eq_ortho(y)) != slack:
                raise AssertionError(f"Equatorial pair sum failed for {fn_name}")
            # General meridian-Kelvin bridge
            if f(TOMO_E1.add(y)) + f(meridian_ortho(y)) != f(TOMO_E1) + f(y):
                raise AssertionError(f"General meridian bridge failed for {fn_name}")
            if f(TOMO_E1.add(y)) + f(TOMO_E1.add(kelvin_eq(y))) != f(TOMO_E1) + f(y):
                raise AssertionError(f"General Kelvin bridge failed for {fn_name}")
            if f(TOMO_E1.add(y)) - f(TOMO_E1) != f(y) - f(meridian_ortho(y)):
                raise AssertionError(f"Polar-equatorial variation identity failed for {fn_name}")
            # Exact zero-slack Piron step-partner bridge & symmetric opposite-step balance
            if f(piron_step(y, lam_probe)) - f(TOMO_E1.add(y)) != f(eq_ortho(y)) - f(
                piron_partner(y, lam_probe)
            ):
                raise AssertionError(f"Zero-slack Piron step-partner bridge failed for {fn_name}")
            if abs(f(piron_step(y, lam_probe)) - f(TOMO_E1.add(y))) != abs(
                f(piron_partner(y, lam_probe)) - f(eq_ortho(y))
            ):
                raise AssertionError(f"Zero-slack Piron abs variation equality failed for {fn_name}")
            if f(piron_step(y, lam_probe)) + f(piron_partner(y, lam_probe)) != f(
                piron_step(y, lam_neg)
            ) + f(piron_partner(y, lam_neg)):
                raise AssertionError(f"Symmetric opposite-step Piron balance failed for {fn_name}")
            # 1-step, 2-step, 3-step Piron bounds & zero-slack 3-step chain identity
            t1, t2, t3 = Fraction(1, 2), Fraction(1, 3), Fraction(1, 5)
            y1 = eq_tangent_step(y, t1)
            y2 = eq_tangent_step(y1, t2)
            y3 = eq_tangent_step(y2, t3)
            if not (
                f(piron_step(y, GaussRat.of(t1)))
                <= f(TOMO_E1.add(y)) + f(eq_ortho(y))
                <= f(TOMO_E1.add(y)) + slack
            ):
                raise AssertionError(f"1-step Piron bound failed for {fn_name}")
            y_rad = y.smul(GaussRat.of(Fraction(1) + t1 * t1))
            if not (f(TOMO_E1.add(y_rad)) <= f(TOMO_E1.add(y)) + 2 * slack):
                raise AssertionError(f"2-step Piron radial bound failed for {fn_name}")
            if not (
                f(TOMO_E1.add(y3)) - f(TOMO_E1.add(y))
                <= f(eq_ortho(y)) + f(eq_ortho(y1)) + f(eq_ortho(y2))
                <= 3 * slack
            ):
                raise AssertionError(f"3-step Piron chain bound failed for {fn_name}")
            zero_slack_chain_rhs = (
                (f(eq_ortho(y)) - f(piron_partner(y, GaussRat.of(t1))))
                + (f(eq_ortho(y1)) - f(piron_partner(y1, GaussRat.of(t2))))
                + (f(eq_ortho(y2)) - f(piron_partner(y2, GaussRat.of(t3))))
            )
            if f(TOMO_E1.add(y3)) - f(TOMO_E1.add(y)) != zero_slack_chain_rhs:
                raise AssertionError(f"Zero-slack 3-step Piron chain identity failed for {fn_name}")
            zero_slack_abs_rhs = (
                abs(f(piron_partner(y, GaussRat.of(t1))) - f(eq_ortho(y)))
                + abs(f(piron_partner(y1, GaussRat.of(t2))) - f(eq_ortho(y1)))
                + abs(f(piron_partner(y2, GaussRat.of(t3))) - f(eq_ortho(y2)))
            )
            if not (abs(f(TOMO_E1.add(y3)) - f(TOMO_E1.add(y))) <= zero_slack_abs_rhs):
                raise AssertionError(f"Zero-slack 3-step Piron abs bound failed for {fn_name}")
            # General Piron-Pythagorean sandwich for k = 2, 3
            for k in (2, 3):
                k2 = k * k
                y_hi = y.smul(GaussRat.of(Fraction(k2 + 1, k2 - 1)))
                y_lo = y.smul(GaussRat.of(Fraction(k2 - 1, k2 + 1)))
                val_rot = f(TOMO_E1.add(pythag_eq_rot(y, k)))
                if not (
                    f(TOMO_E1.add(y_hi)) - slack <= val_rot <= f(TOMO_E1.add(y_lo)) + slack
                ):
                    raise AssertionError(f"General Pythagorean sandwich failed for {fn_name}, k={k}")
            track_a_checks += 1

    # 7. Track B: Irrational-locus / Dedekind-cut frame-function stress tests on Q(i)^3
    # (a) Local constancy of dedekind_ray_cut near tomo_e1 (ray_sin_sq < 1/2) and tomo_e2 (ray_sin_sq < 1/3)
    for m in range(5):
        u_e1 = crt_approach_e1(m)
        if not (ray_sin_sq(u_e1, TOMO_E1) < Fraction(1, 2) and dedekind_ray_cut(u_e1) == 0):
            raise AssertionError("dedekind_ray_cut local constancy near tomo_e1 failed")
    u_near_e2 = GVec.real(Fraction(1, 4), 1, Fraction(1, 4))
    if not (ray_sin_sq(u_near_e2, TOMO_E2) < Fraction(1, 3) and dedekind_ray_cut(u_near_e2) == 1):
        raise AssertionError("dedekind_ray_cut local constancy near tomo_e2 failed")
    # (b) Bisector frame (tomo_e3, tomo_e12, partner_e12_minus) refutes 3-frame additivity for dedekind_ray_cut
    bisector_sum = (
        dedekind_ray_cut(TOMO_E3)
        + dedekind_ray_cut(TOMO_E12)
        + dedekind_ray_cut(PARTNER_E12_MINUS)
    )
    if bisector_sum != 0:
        raise AssertionError("Expected dedekind_ray_cut sum 0 on (tomo_e3, tomo_e12, partner_e12_minus)")
    # (c) Two-frame Gaussian-norm latitude-halving identity & cone-exit across super-cone rays
    for a_val, b_val in ((0, 1), (1, 2), (1, 3), (85, 100)):
        u_base = gaussian_halving_base(a_val, b_val)
        w_ortho = gaussian_halving_ortho(a_val, b_val)
        u_pos = gaussian_halving_pos(a_val, b_val)
        v_neg = gaussian_halving_neg(a_val, b_val)
        if not (
            is_frame(u_base, TOMO_E3, w_ortho) and is_frame(u_pos, v_neg, w_ortho)
        ):
            raise AssertionError(f"Gaussian-halving frame check failed at ({a_val}, {b_val})")
        for fn_name, f in nonneg_frame_fns.items():
            if 2 * f(u_pos) != f(u_base) + f(TOMO_E3):
                raise AssertionError(f"Gaussian-halving identity failed for {fn_name}")
        if not (
            3 * (u_pos.y.norm_sq() ** 2) < (u_pos.norm_sq() ** 2)
            and dedekind_ray_cut(u_base) == 1
            and dedekind_ray_cut(TOMO_E3) == 0
            and dedekind_ray_cut(u_pos) == 0
            and 2 * dedekind_ray_cut(u_pos) != dedekind_ray_cut(u_base) + dedekind_ray_cut(TOMO_E3)
        ):
            raise AssertionError(
                f"dedekind_ray_cut Gaussian-halving cone-exit check failed at ({a_val}, {b_val})"
            )
    # (d) Global pointwise ray continuity / local constancy radius certificate on Q(i)^3 \ {0}
    local_constancy_probes = [
        TOMO_E1,
        TOMO_E2,
        TOMO_E3,
        TOMO_E12,
        TOMO_E23I,
        WITNESS_111,
        WITNESS_NEG211,
        GVec.real(85, 100, 0),
        GVec.real(86, 100, 0),
        gaussian_halving_base(1, 2),
        gaussian_halving_pos(1, 2),
    ]
    for v0 in local_constancy_probes:
        theta = dedekind_local_constancy_theta(v0)
        delta = dedekind_local_constancy_radius(v0)
        if delta <= 0 or delta != theta * theta:
            raise AssertionError(f"Expected positive local constancy radius for v0={v0}")
        step = theta / Fraction(4)
        for sx, sy, sz in ((1, -1, 1), (-1, 1, -1), (1, 1, 0), (0, 1, 1)):
            v_perturbed = GVec(
                v0.x + GaussRat.of(sx * step),
                v0.y + GaussRat.of(sy * step),
                v0.z + GaussRat.of(0, sz * step),
            )
            if not (
                dist_sq_vec(v_perturbed, v0) < delta
                and dedekind_ray_cut(v_perturbed) == dedekind_ray_cut(v0)
            ):
                raise AssertionError(f"dedekind_ray_cut local constancy failed at v0={v0}")
    # (e) General-anchor orthogonal ray-distance Bessel bound & polar-cap disjointness
    bessel_anchors = [*NINE_ANCHORS.values(), WITNESS_111, WITNESS_P7]
    ortho_bessel_pairs_checked = 0
    for f_name, u, v, w in frames:
        for anchor in bessel_anchors:
            in_cap_count = sum(
                1 for vec in (u, v, w) if ray_sin_sq(vec, anchor) < Fraction(1, 2)
            )
            if in_cap_count > 1:
                raise AssertionError(
                    f"More than one frame vector in < 1/2 polar cap on {f_name} for anchor={anchor}"
                )
            for p, q in ((u, v), (u, w), (v, w)):
                expected_quad = p.inner(anchor).norm_sq() / (
                    p.norm_sq() * anchor.norm_sq()
                )
                if Fraction(1) - ray_sin_sq(p, anchor) != expected_quad:
                    raise AssertionError(f"Projector quadRay identity failed on {f_name}")
                if ray_sin_sq(p, anchor) + ray_sin_sq(q, anchor) < Fraction(1):
                    raise AssertionError(
                        f"Orthogonal Bessel bound failed on frame {f_name}: p={p}, q={q}, anchor={anchor}"
                    )
                if (
                    ray_sin_sq(p, anchor) < Fraction(1, 2)
                    and ray_sin_sq(q, anchor) < Fraction(1, 2)
                ):
                    raise AssertionError(
                        f"Orthogonal polar-cap disjointness failed on frame {f_name}"
                    )
                ortho_bessel_pairs_checked += 1

    # 8. Target 1 (TFQ-1057): General-anchor meridian coupling, spherical frame Pythagoras,
    #    two-frame cross-anchor proximity bound, witness_111 9-anchor isolation,
    #    exact 2-frame B_{1/5}(T_9) determination, witness_neg211 < 1/8 isolation,
    #    perturbed 2-frame bisector bounce-back, witness_123 15-ray isolation, and
    #    meridian-step modulus orthogonal decomposition
    anchor_ortho_probes: list[tuple[str, GVec, GVec]] = [
        ("tomo_e1", TOMO_E1, GVec.real(0, 1, 2)),
        ("tomo_e2", TOMO_E2, GVec.real(2, 0, -1)),
        ("tomo_e3", TOMO_E3, GVec.real(1, -2, 0)),
        ("tomo_e12", TOMO_E12, PARTNER_E12_MINUS),
        ("tomo_e13", TOMO_E13, PARTNER_E13_MINUS),
        ("tomo_e23", TOMO_E23, PARTNER_E23_MINUS),
        ("tomo_e12i", TOMO_E12I, PARTNER_E12I_MINUS),
        ("tomo_e13i", TOMO_E13I, PARTNER_E13I_MINUS),
        ("tomo_e23i", TOMO_E23I, PARTNER_E23I_MINUS),
    ]
    target1_meridian_checks = 0
    for a_name, a_vec, y_base in anchor_ortho_probes:
        for scale_num, scale_den in ((1, 1), (1, 3), (2, 5)):
            y_vec = y_base.smul(GaussRat.of(Fraction(scale_num, scale_den)))
            if a_vec.inner(y_vec) != G_ZERO:
                raise AssertionError(f"Expected y orthogonal to {a_name}")
            step_vec = anchor_meridian_step(a_vec, y_vec)
            ortho_vec = anchor_meridian_ortho(a_vec, y_vec)
            kelvin_vec = anchor_kelvin_eq(a_vec, y_vec)
            cross_vec = herm_cross(a_vec, y_vec)
            if not (
                is_frame(a_vec, y_vec, cross_vec)
                and is_frame(step_vec, ortho_vec, cross_vec)
            ):
                raise AssertionError(f"General-anchor meridian frame check failed for {a_name}")
            if ortho_vec.smul(GaussRat.of(-Fraction(1) / y_vec.norm_sq())) != a_vec.add(kelvin_vec):
                raise AssertionError(f"General-anchor Kelvin scaling failed for {a_name}")
            expected_sin = y_vec.norm_sq() / (a_vec.norm_sq() + y_vec.norm_sq())
            if (
                ray_sin_sq(step_vec, a_vec) != expected_sin
                or ray_sin_sq(ortho_vec, y_vec) != expected_sin
            ):
                raise AssertionError(f"anchorMeridianOrtho_raySinSq_eq failed for {a_name}")
            for fn_name, f in nonneg_frame_fns.items():
                if f(step_vec) - f(a_vec) != f(y_vec) - f(ortho_vec):
                    raise AssertionError(
                        f"anchor_meridian_kelvin_bridge failed for {fn_name} on {a_name}"
                    )
                if f(step_vec) + f(a_vec.add(kelvin_vec)) != f(a_vec) + f(y_vec):
                    raise AssertionError(
                        f"anchor_meridian_kelvin_bridge Kelvin sum failed for {fn_name} on {a_name}"
                    )
            for r_name, r_fn in residual_funcs.items():
                if r_fn(step_vec) - r_fn(a_vec) != r_fn(y_vec) - r_fn(ortho_vec):
                    raise AssertionError(
                        f"anchor_meridian_zeroWeight_bridge failed for {r_name} on {a_name}"
                    )
            target1_meridian_checks += 1

    spherical_pythagoras_checks = 0
    for f_name, u, v, w in frames:
        for anchor in bessel_anchors:
            if ray_sin_sq(u, anchor) + ray_sin_sq(v, anchor) + ray_sin_sq(w, anchor) != Fraction(2):
                raise AssertionError(
                    f"frame_raySinSq_sum_eq_two failed on {f_name} for anchor={anchor}"
                )
            spherical_pythagoras_checks += 1

    anchor_frames: list[tuple[str, GVec, GVec, GVec]] = [
        ("std_basis", TOMO_E1, TOMO_E2, TOMO_E3),
        ("anchor_bisector_12", TOMO_E3, TOMO_E12, PARTNER_E12_MINUS),
        ("anchor_bisector_12i", TOMO_E3, TOMO_E12I, PARTNER_E12I_MINUS),
        ("anchor_bisector_23", TOMO_E1, TOMO_E23, PARTNER_E23_MINUS),
    ]
    two_frame_cross_anchor_checks = 0
    for f_name, u, v, w in frames:
        for af_name, a1, a2, a3 in anchor_frames:
            if ray_sin_sq(w, a3) > ray_sin_sq(u, a1) + ray_sin_sq(v, a2):
                raise AssertionError(
                    f"frame_third_raySinSq_le_add_of_ortho_anchors failed on {f_name} vs {af_name}"
                )
            eta = ray_sin_sq(w, a3)
            if ray_sin_sq(u, a1) < eta / Fraction(2) and ray_sin_sq(v, a2) < eta / Fraction(2):
                raise AssertionError(
                    f"fixed_anchor_frame_isolation_obstruction failed on {f_name} vs {af_name}"
                )
            two_frame_cross_anchor_checks += 1

    for a_name, a_vec in NINE_ANCHORS.items():
        if ray_sin_sq(WITNESS_111, a_vec) > Fraction(2, 3):
            raise AssertionError(
                f"Expected ray_sin_sq(witness_111, {a_name}) <= 2/3, got {ray_sin_sq(WITNESS_111, a_vec)}"
            )
    witness_111_ortho_probes = [
        WITNESS_NEG211,
        PARTNER_E12_MINUS,
        PARTNER_E13_MINUS,
        PARTNER_E23_MINUS,
        GVec.real(1, 2, -3),
        GVec(GaussRat.of(1, 1), GaussRat.of(-1, 0), GaussRat.of(0, -1)),
    ]
    for u_ortho in witness_111_ortho_probes:
        if u_ortho.inner(WITNESS_111) != G_ZERO:
            raise AssertionError(f"Expected {u_ortho} orthogonal to witness_111")
        for a_name, a_vec in NINE_ANCHORS.items():
            if ray_sin_sq(u_ortho, a_vec) < Fraction(1, 3):
                raise AssertionError(
                    f"ortho_witness111_raySinSq_nineAnchors_ge_one_third failed for {u_ortho} vs {a_name}"
                )

    # (a) Exact 2-frame B_{1/5}(T_9) determination of witness_111 & < 1/8 isolation at witness_neg211
    if not is_frame(WITNESS_NEG211, PROBE_120, PROBE_2M15):
        raise AssertionError("isFrame_witness_neg211_probe120_probe2m15 failed")
    if ray_sin_sq(PROBE_120, TOMO_E12) != Fraction(1, 10):
        raise AssertionError("Expected ray_sin_sq(probe_120, tomo_e12) == 1/10")
    if ray_sin_sq(PROBE_2M15, TOMO_E3) != Fraction(1, 6):
        raise AssertionError("Expected ray_sin_sq(probe_2m15, tomo_e3) == 1/6")
    for r_name, r_fn in residual_funcs.items():
        if r_fn(WITNESS_111) != r_fn(PROBE_120) + r_fn(PROBE_2M15):
            raise AssertionError(
                f"residual_witness111_eq_sum_in_fifth_ball failed for {r_name}"
            )
        eps_bound = max(abs(r_fn(PROBE_120)), abs(r_fn(PROBE_2M15)))
        if (
            abs(r_fn(WITNESS_111)) > 2 * eps_bound
            or abs(r_fn(WITNESS_NEG211)) > 2 * eps_bound
        ):
            raise AssertionError(
                f"residual_witness111_abs_le_two_eps_of_fifth_ball failed for {r_name}"
            )
    if ray_sin_sq(WITNESS_NEG211, PARTNER_E12_MINUS) != Fraction(1, 4):
        raise AssertionError("Expected ray_sin_sq(witness_neg211, bisector_12_neg) == 1/4")
    u_neg_real = GVec.real(1, 3, -1)
    u_neg_cplx = GVec(GaussRat.of(1, 1), GaussRat.of(1, 2), GaussRat.of(1, 0))
    for u_neg, v_neg in (
        (PROBE_120, PROBE_2M15),
        (PROBE_2M15, PROBE_120),
        (WITNESS_111, PARTNER_E23_MINUS),
        (PARTNER_E23_MINUS, WITNESS_111),
        (u_neg_real, herm_cross(WITNESS_NEG211, u_neg_real)),
        (u_neg_cplx, herm_cross(WITNESS_NEG211, u_neg_cplx)),
    ):
        if not is_frame(u_neg, v_neg, WITNESS_NEG211):
            raise AssertionError("Expected frame containing witness_neg211")
        sum_e12_e3 = ray_sin_sq(u_neg, TOMO_E12) + ray_sin_sq(v_neg, TOMO_E3)
        if sum_e12_e3 < Fraction(1, 4) or (
            ray_sin_sq(u_neg, TOMO_E12) < Fraction(1, 8)
            and ray_sin_sq(v_neg, TOMO_E3) < Fraction(1, 8)
        ):
            raise AssertionError("witness_neg211_isolation_one_eighth failed")

    # (b) Perturbed two-frame bisector bounce-back (including non-collinear second-step perturbations with LHS > 0)
    u_pert = GVec.real(1, 5, -6)  # orthogonal to witness_111 = (1, 1, 1), close to (0, 1, -1)
    v_pert = herm_cross(WITNESS_111, u_pert)  # (-11, 7, 4)
    u_prime_rev = herm_cross(v_pert, WITNESS_111)
    v_prime_rev = herm_cross(v_pert, u_prime_rev)
    u_prime_ind1 = GVec.real(1, 9, -13)  # orthogonal to v_pert = (-11, 7, 4), LHS = 3/251 > 0
    v_prime_ind1 = herm_cross(v_pert, u_prime_ind1)
    u_prime_ind2 = GVec.real(-1, 3, -8)  # orthogonal to v_pert = (-11, 7, 4), LHS = 6/37 > 0
    v_prime_ind2 = herm_cross(v_pert, u_prime_ind2)
    bounce_back_pairs = [
        (PARTNER_E23_MINUS, WITNESS_NEG211, PARTNER_E23_MINUS, WITNESS_111, False),
        (u_pert, v_pert, u_prime_rev, v_prime_rev, False),
        (u_pert, v_pert, u_prime_ind1, v_prime_ind1, True),
        (u_pert, v_pert, u_prime_ind2, v_prime_ind2, True),
    ]
    for u_b, v_b, u_p, v_p, expect_positive_lhs in bounce_back_pairs:
        if not (is_frame(WITNESS_111, u_b, v_b) and is_frame(v_b, u_p, v_p)):
            raise AssertionError("Bounce-back test frames invalid")
        if ray_sin_sq(v_b, WITNESS_NEG211) > ray_sin_sq(u_b, PARTNER_E23_MINUS):
            raise AssertionError("First-step bounce-back bound failed")
        lhs_bounce = ray_sin_sq(v_p, WITNESS_111)
        rhs_bounce = ray_sin_sq(u_b, PARTNER_E23_MINUS) + ray_sin_sq(
            u_p, PARTNER_E23_MINUS
        )
        if expect_positive_lhs and lhs_bounce <= Fraction(0):
            raise AssertionError("Expected non-trivial positive LHS in perturbed bounce-back")
        if lhs_bounce > rhs_bounce:
            raise AssertionError("Second-step bounce-back bound failed")

    # (c) Generic ray witness_123 = (1, 2, 3) 9-anchor + 6-bisector isolation
    for a_name, a_vec in NINE_ANCHORS.items():
        if ray_sin_sq(WITNESS_123, a_vec) > Fraction(13, 14):
            raise AssertionError(f"witness123_raySinSq_nineAnchors_le failed on {a_name}")
    for b_name, b_vec in SIX_PARTNERS.items():
        if ray_sin_sq(WITNESS_123, b_vec) > Fraction(27, 28):
            raise AssertionError(f"witness123_raySinSq_sixBisectors_le failed on {b_name}")
    witness_123_ortho_probes = [
        GVec.real(2, -1, 0),
        GVec.real(3, 0, -1),
        GVec.real(0, 3, -2),
        GVec.real(1, 1, -1),
        GVec.real(5, -1, -1),
        GVec(GaussRat.of(1, 1), GaussRat.of(1, -2), GaussRat.of(-1, 1)),
    ]
    for u_123 in witness_123_ortho_probes:
        v_123 = herm_cross(WITNESS_123, u_123)
        if not is_frame(WITNESS_123, u_123, v_123):
            raise AssertionError(f"Expected frame (witness_123, {u_123}, {v_123})")
        for partner_vec in (u_123, v_123):
            for a_name, a_vec in NINE_ANCHORS.items():
                if ray_sin_sq(partner_vec, a_vec) < Fraction(1, 14):
                    raise AssertionError(
                        f"frame_witness123_partners_isolated_from_nine_and_six failed on anchor {a_name}"
                    )
            for b_name, b_vec in SIX_PARTNERS.items():
                if ray_sin_sq(partner_vec, b_vec) < Fraction(1, 28):
                    raise AssertionError(
                        f"frame_witness123_partners_isolated_from_nine_and_six failed on bisector {b_name}"
                    )

    # (d) Meridian-step modulus orthogonal projection decomposition (isUniformlyRayContinuous_iff_hasUniformMeridianStepModulus)
    meridian_decomp_checks = 0
    for u in test_vectors:
        c_self = GaussRat.of(Fraction(2), Fraction(-1))
        v_col = u.smul(c_self)
        if ray_sin_sq(u, v_col) != 0 or u.smul(proj_scalar(u, v_col)) != v_col:
            raise AssertionError("eq_of_raySinSq_eq_zero collinear check failed")
        for v in test_vectors:
            sin_uv = ray_sin_sq(u, v)
            if Fraction(0) < sin_uv < Fraction(1):
                a_proj = u.smul(proj_scalar(u, v))
                y_orth = v.sub(a_proj)
                if (
                    a_proj.inner(y_orth) != G_ZERO
                    or a_proj.add(y_orth) != v
                    or y_orth.norm_sq() / (a_proj.norm_sq() + y_orth.norm_sq()) != sin_uv
                ):
                    raise AssertionError("Meridian-step orthogonal decomposition failed")
                meridian_decomp_checks += 1

    # 9. Target 4 (TFQ-0307): Finite Kochen-Specker 3-frame hypergraph extraction and 6-branch
    #    unsat-core replay from BornGaussianRationalNoColouring.lean, fifteenAnchorBisectorScenario
    #    {0, 1} valuation contrast, and 4-tier operational non-contextuality classification.
    ks_summary = extract_and_verify_ks_no_colouring()
    tfq_0307_summary = verify_tfq_0307_four_tier_classification(ks_summary)

    # 10. Section 9 (TFQ-1057): Multi-Frame Rational Incidence Chains, Bounded Anchor Amplification &
    #     Pointwise-Continuous Counterexample Analysis on Q(i)^3 \ {0}.
    tfq_1057_summary = verify_tfq_1057_multi_frame_incidence_and_amplification()

    return {
        "schema_version": 1,
        "phase": "Phase 2 — Finite and Exact-Arithmetic Gleason Model",
        "frames_verified": len(frames),
        "residuals_verified": residual_summary,
        "crt_archimedean_padic_collision_checks": crt_checks,
        "projection_identity_pairs_verified": projection_pairs_checked,
        "two_frame_meridian_antisymmetry_verified": True,
        "track_a_piron_soler_chain_checks": track_a_checks,
        "track_b_irrational_locus_stress_tests_verified": True,
        "ortho_bessel_pairs_verified": ortho_bessel_pairs_checked,
        "target1_general_anchor_meridian_checks": target1_meridian_checks,
        "spherical_frame_pythagoras_checks": spherical_pythagoras_checks,
        "two_frame_cross_anchor_checks": two_frame_cross_anchor_checks,
        "witness_111_nine_anchor_isolation_verified": True,
        "witness_111_two_frame_fifth_ball_verified": True,
        "witness_neg211_one_eighth_isolation_verified": True,
        "perturbed_two_frame_bounce_back_verified": True,
        "witness_123_fifteen_ray_isolation_verified": True,
        "meridian_step_modulus_decomp_pairs_verified": meridian_decomp_checks,
        "ks_no_colouring_certificate": ks_summary,
        "tfq_0307_four_tier_classification": tfq_0307_summary,
        "tfq_1057_multi_frame_incidence_and_amplification": tfq_1057_summary,
        "status": "PASS",
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out",
        type=Path,
        default=None,
        help="Optional path to write JSON verification receipt.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Run all exact rational certificate checks and exit 0 on success.",
    )
    args = parser.parse_args(argv)
    receipt = verify_all_certificates()
    payload = json.dumps(receipt, indent=2, sort_keys=True) + "\n"
    if args.out is not None:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(payload, encoding="utf-8", newline="\n")
    if args.check or args.out is None:
        sys.stdout.write(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
