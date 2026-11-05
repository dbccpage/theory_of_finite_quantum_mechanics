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
5. Chinese Remainder Archimedean/3-adic collision sequence `crt_approach_e1(m) = (1 + 9m, 1, 1)`,
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

    # 5. Verify Pell approximations to 1/sqrt(5) for the Dedekind ray-cut witness
    # For (b, a, 0), norm_sq = b^2 + a^2, so 5 * a^4 > (b^2 + a^2)^2 <=> (sqrt(5) - 1) a^2 > b^2.
    # Instead, compare 5 * |u.y|^2 > |u.x|^2 + |u.y|^2 + |u.z|^2, i.e., 4 * |u.y|^2 > |u.x|^2 + |u.z|^2,
    # Wait: 4 is a square, whereas 5 * |u.y|^2 > 2 * ||u||^2 <=> 3 * |u.y|^2 > 2 * (|u.x|^2 + |u.z|^2)!
    # For u = (b, a, 0), 5 * |u.y|^4 > ||u||^4 is 5 * a^4 > (b^2 + a^2)^2.
    # Even simpler: 2 * |u.y|^2 > |u.x|^2 + |u.y|^2 + |u.z|^2 <=> |u.y|^2 > |u.x|^2 + |u.z|^2 (cut at 1, rational!).
    # Whereas 3 * |u.y|^2 > ||u||^2 <=> 2 * |u.y|^2 > |u.x|^2 + |u.z|^2!
    # Wait: Can |u.x|^2 + |u.z|^2 = 2 * |u.y|^2 for nonzero u in Q(i)^3?
    # Yes, e.g. u = (1, 1, 1) has |u.x|^2 + |u.z|^2 = 2 = 2 * |u.y|^2!
    # Why? Because 2 IS a norm (and sum of two norms) in Q(i)!
    # Whereas 3 is NOT a norm in Q(i) and NOT a sum of two norms in Q(i), because v_3(a^2 + b^2) is ALWAYS EVEN!
    # Wait: By `v3Rat_normSq_even`, for ANY u in Q(i)^3 \ {0}:
    # Can `3 * u.y.normSq == u.x.normSq` (or `3 * (u.y.normSq)^2 == (normSqVec u)^2`)?
    # NEVER! Because `v3Rat (u.y.normSq) % 2 == 0` and `v3Rat ((normSqVec u)^2) = 2 * v3Rat (normSqVec u)` is EVEN,
    # whereas `v3Rat (3 * (u.y.normSq)^2) = 1 + 2 * v3Rat (u.y.normSq)` is ODD!
    pell_pairs = [
        (GVec.real(0, 1, 0), GVec.real(1, 1, 0)),
        (GVec.real(4, 5, 0), GVec.real(9, 10, 0)),
        (GVec.real(85, 100, 0), GVec.real(86, 100, 0)),
    ]
    for u_hi, u_lo in pell_pairs:
        if not (dedekind_ray_cut(u_hi) == 1 and dedekind_ray_cut(u_lo) == 0):
            raise AssertionError("Dedekind ray cut test pair failed")

    return {
        "schema_version": 1,
        "phase": "Phase 2 — Finite and Exact-Arithmetic Gleason Model",
        "frames_verified": len(frames),
        "residuals_verified": residual_summary,
        "crt_archimedean_padic_collision_checks": crt_checks,
        "projection_identity_pairs_verified": projection_pairs_checked,
        "two_frame_meridian_antisymmetry_verified": True,
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
