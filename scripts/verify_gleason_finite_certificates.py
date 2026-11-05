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
import json
from pathlib import Path
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
        args.out.write_text(payload, encoding="utf-8")
    if args.check or args.out is None:
        sys.stdout.write(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
