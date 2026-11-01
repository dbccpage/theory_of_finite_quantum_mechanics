"""Unit and property tests for FQ-GLEASON-QI3-FRAME-FUNCTIONS (Record TFQ-1055).

Governing DAG target nodes:
  - FQ-GLEASON-QI3-FRAME-FUNCTIONS (TFQ-1055)
  - FQ-GAP-BORN-UNIQUENESS-GLEASON (TFQ-0307)
AuthorityEffect: None
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import importlib.util
import itertools
from pathlib import Path
import subprocess
import sys
from typing import Callable

import pytest


REPO_ROOT = Path(__file__).resolve().parents[3]
CHECKS_DIR = REPO_ROOT / "checks" / "independent"
LEAN_TOMOGRAPHY_FILE = REPO_ROOT / "lean4" / "BornGaussianTomographyReduction.lean"


@dataclass(frozen=True)
class GaussRat:
    """Exact Gaussian rational re + im * i over Q."""

    re: Fraction
    im: Fraction = Fraction(0)

    @staticmethod
    def of_ints(re: int, im: int = 0) -> "GaussRat":
        return GaussRat(Fraction(re), Fraction(im))

    def conj(self) -> "GaussRat":
        return GaussRat(self.re, -self.im)

    def norm_sq(self) -> Fraction:
        return self.re * self.re + self.im * self.im

    def __add__(self, other: "GaussRat") -> "GaussRat":
        return GaussRat(self.re + other.re, self.im + other.im)

    def __sub__(self, other: "GaussRat") -> "GaussRat":
        return GaussRat(self.re - other.re, self.im - other.im)

    def __mul__(self, other: "GaussRat") -> "GaussRat":
        return GaussRat(
            self.re * other.re - self.im * other.im,
            self.re * other.im + self.im * other.re,
        )


@dataclass(frozen=True)
class GVec:
    """Three-component vector in Q(i)^3."""

    x: GaussRat
    y: GaussRat
    z: GaussRat

    def dot(self, other: "GVec") -> GaussRat:
        return (
            self.x.conj() * other.x
            + self.y.conj() * other.y
            + self.z.conj() * other.z
        )

    def norm_sq(self) -> Fraction:
        return self.x.norm_sq() + self.y.norm_sq() + self.z.norm_sq()


@dataclass(frozen=True)
class HermForm3:
    """Nine-parameter Hermitian form on Q(i)^3 matching BornGaussianTomographyReduction.lean."""

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


E1 = GVec(GaussRat.of_ints(1, 0), GaussRat.of_ints(0, 0), GaussRat.of_ints(0, 0))
E2 = GVec(GaussRat.of_ints(0, 0), GaussRat.of_ints(1, 0), GaussRat.of_ints(0, 0))
E3 = GVec(GaussRat.of_ints(0, 0), GaussRat.of_ints(0, 0), GaussRat.of_ints(1, 0))
U12_PLUS = GVec(GaussRat.of_ints(1, 0), GaussRat.of_ints(1, 0), GaussRat.of_ints(0, 0))
U12_I = GVec(GaussRat.of_ints(1, 0), GaussRat.of_ints(0, 1), GaussRat.of_ints(0, 0))
U13_PLUS = GVec(GaussRat.of_ints(1, 0), GaussRat.of_ints(0, 0), GaussRat.of_ints(1, 0))
U13_I = GVec(GaussRat.of_ints(1, 0), GaussRat.of_ints(0, 0), GaussRat.of_ints(0, 1))
U23_PLUS = GVec(GaussRat.of_ints(0, 0), GaussRat.of_ints(1, 0), GaussRat.of_ints(1, 0))
U23_I = GVec(GaussRat.of_ints(0, 0), GaussRat.of_ints(1, 0), GaussRat.of_ints(0, 1))
NINE_RAYS = [E1, E2, E3, U12_PLUS, U12_I, U13_PLUS, U13_I, U23_PLUS, U23_I]


def quad_num(rho: HermForm3, v: GVec) -> Fraction:
    """Rational quadratic numerator <v, rho v> matching quadNum in Lean 4."""
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
    """Normalized ray quotient <v, rho v> / <v, v> matching quadRay in Lean 4."""
    denom = v.norm_sq()
    if denom == 0:
        return Fraction(0)
    return quad_num(rho, v) / denom


def tomography_form(f: Callable[[GVec], Fraction]) -> HermForm3:
    """Reconstruct the unique Hermitian form matching f on the 9 tomography rays."""
    d1 = f(E1)
    d2 = f(E2)
    d3 = f(E3)
    return HermForm3(
        d1=d1,
        d2=d2,
        d3=d3,
        a12=f(U12_PLUS) - (d1 + d2) / 2,
        b12=(d1 + d2) / 2 - f(U12_I),
        a13=f(U13_PLUS) - (d1 + d3) / 2,
        b13=(d1 + d3) / 2 - f(U13_I),
        a23=f(U23_PLUS) - (d2 + d3) / 2,
        b23=(d2 + d3) / 2 - f(U23_I),
    )


HERM_ZERO = HermForm3(
    Fraction(0), Fraction(0), Fraction(0),
    Fraction(0), Fraction(0), Fraction(0),
    Fraction(0), Fraction(0), Fraction(0),
)
HERM_ID = HermForm3(
    Fraction(1), Fraction(1), Fraction(1),
    Fraction(0), Fraction(0), Fraction(0),
    Fraction(0), Fraction(0), Fraction(0),
)


def herm_add(rho: HermForm3, sigma: HermForm3) -> HermForm3:
    return HermForm3(
        d1=rho.d1 + sigma.d1,
        d2=rho.d2 + sigma.d2,
        d3=rho.d3 + sigma.d3,
        a12=rho.a12 + sigma.a12,
        b12=rho.b12 + sigma.b12,
        a13=rho.a13 + sigma.a13,
        b13=rho.b13 + sigma.b13,
        a23=rho.a23 + sigma.a23,
        b23=rho.b23 + sigma.b23,
    )


def herm_smul(c: Fraction, rho: HermForm3) -> HermForm3:
    return HermForm3(
        d1=c * rho.d1,
        d2=c * rho.d2,
        d3=c * rho.d3,
        a12=c * rho.a12,
        b12=c * rho.b12,
        a13=c * rho.a13,
        b13=c * rho.b13,
        a23=c * rho.a23,
        b23=c * rho.b23,
    )


def trace_inner(rho: HermForm3, sigma: HermForm3) -> Fraction:
    """Rational Frobenius trace pairing tr(rho sigma) matching traceInner in Lean 4."""
    return (
        rho.d1 * sigma.d1
        + rho.d2 * sigma.d2
        + rho.d3 * sigma.d3
        + 2
        * (
            rho.a12 * sigma.a12
            + rho.a13 * sigma.a13
            + rho.a23 * sigma.a23
            + rho.b12 * sigma.b12
            + rho.b13 * sigma.b13
            + rho.b23 * sigma.b23
        )
    )


def ray_proj(v: GVec) -> HermForm3:
    """Normalized rank-1 ray projector T(v) = v v* / <v, v> matching rayProj in Lean 4."""
    denom = v.norm_sq()
    if denom == 0:
        return HERM_ZERO
    return HermForm3(
        d1=v.x.norm_sq() / denom,
        d2=v.y.norm_sq() / denom,
        d3=v.z.norm_sq() / denom,
        a12=(v.x.re * v.y.re + v.x.im * v.y.im) / denom,
        b12=-(v.x.re * v.y.im - v.x.im * v.y.re) / denom,
        a13=(v.x.re * v.z.re + v.x.im * v.z.im) / denom,
        b13=-(v.x.re * v.z.im - v.x.im * v.z.re) / denom,
        a23=(v.y.re * v.z.re + v.y.im * v.z.im) / denom,
        b23=-(v.y.re * v.z.im - v.y.im * v.z.re) / denom,
    )



def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def tomography_mod():
    return _load_module(
        "fq_gleason_qi3_tomography",
        CHECKS_DIR / "fq-gleason-qi3-tomography.py",
    )


@pytest.fixture(scope="module")
def frame_functions_mod():
    return _load_module(
        "fq_gleason_qi3_frame_functions",
        CHECKS_DIR / "fq-gleason-qi3-frame-functions.py",
    )


def test_nine_ray_tomography_reconstruction_and_uniqueness() -> None:
    """Verify exact 9-ray Hermitian tomography reconstruction and uniqueness over Q(i)^3."""
    sample_forms = [
        HermForm3(
            d1=Fraction(1, 2),
            d2=Fraction(1, 3),
            d3=Fraction(1, 6),
            a12=Fraction(2, 5),
            b12=Fraction(-1, 7),
            a13=Fraction(-3, 11),
            b13=Fraction(4, 9),
            a23=Fraction(5, 13),
            b23=Fraction(-2, 3),
        ),
        HermForm3(
            d1=Fraction(5, 4),
            d2=Fraction(-1, 2),
            d3=Fraction(1, 4),
            a12=Fraction(0),
            b12=Fraction(3, 8),
            a13=Fraction(-7, 6),
            b13=Fraction(0),
            a23=Fraction(1, 9),
            b23=Fraction(5, 12),
        ),
        HermForm3(
            d1=Fraction(1, 3),
            d2=Fraction(1, 3),
            d3=Fraction(1, 3),
            a12=Fraction(0),
            b12=Fraction(0),
            a13=Fraction(0),
            b13=Fraction(0),
            a23=Fraction(0),
            b23=Fraction(0),
        ),
    ]

    probe_vectors = [
        GVec(GaussRat.of_ints(1, 2), GaussRat.of_ints(-3, 1), GaussRat.of_ints(2, -1)),
        GVec(GaussRat.of_ints(1, 0), GaussRat.of_ints(1, 0), GaussRat.of_ints(1, 1)),
        GVec(GaussRat.of_ints(1, 2), GaussRat.of_ints(1, 0), GaussRat.of_ints(1, 1)),
        GVec(GaussRat.of_ints(0, 3), GaussRat.of_ints(2, -5), GaussRat.of_ints(-1, 4)),
    ]

    for rho in sample_forms:
        assert rho.trace() == Fraction(1)
        reconstructed = tomography_form(lambda v, r=rho: quad_ray(r, v))
        assert reconstructed == rho
        assert reconstructed.trace() == Fraction(1)
        for ray in NINE_RAYS:
            assert quad_ray(reconstructed, ray) == quad_ray(rho, ray)
        for vec in probe_vectors:
            assert quad_ray(reconstructed, vec) == quad_ray(rho, vec)
            for scalar in [GaussRat.of_ints(2, -1), GaussRat.of_ints(-1, 3)]:
                scaled = GVec(scalar * vec.x, scalar * vec.y, scalar * vec.z)
                assert quad_ray(rho, scaled) == quad_ray(rho, vec)

    # Negative control: flipping the sign of b12 breaks evaluation on U12_I
    rho0 = sample_forms[0]
    wrong_sign_rho = HermForm3(
        d1=rho0.d1,
        d2=rho0.d2,
        d3=rho0.d3,
        a12=rho0.a12,
        b12=-rho0.b12,
        a13=rho0.a13,
        b13=rho0.b13,
        a23=rho0.a23,
        b23=rho0.b23,
    )
    assert quad_ray(wrong_sign_rho, U12_I) != quad_ray(rho0, U12_I)


def test_quadray_frame_sum_on_non_unit_orthogonal_frames() -> None:
    """Verify quadRay_frame_sum on non-unit orthogonal frames in Q(i)^3, including norm-4 and norm-8 primitive rays."""

    def gv(a: int, b: int, c: int, d: int, e: int, g: int) -> GVec:
        return GVec(
            GaussRat.of_ints(a, b),
            GaussRat.of_ints(c, d),
            GaussRat.of_ints(e, g),
        )

    orthogonal_frames = [
        (gv(0, 0, 0, 0, 1, 0), gv(1, 0, 1, 0, 0, 0), gv(1, 0, -1, 0, 0, 0)),
        (gv(0, 0, 0, 0, 1, 0), gv(0, 1, 1, 0, 0, 0), gv(0, 1, -1, 0, 0, 0)),
        (gv(1, 0, 1, 0, 0, 0), gv(1, 0, -1, 0, 1, 1), gv(1, 0, -1, 0, -1, -1)),
        (gv(1, 0, 0, 0, 1, 0), gv(1, 0, 1, 1, -1, 0), gv(1, 0, -1, -1, -1, 0)),
        (gv(0, 0, 1, 0, 1, 0), gv(1, 1, 1, 0, -1, 0), gv(-1, -1, 1, 0, -1, 0)),
        # Frame containing (1+i)-primitive vector (1, 1, 1+i) of Hermitian norm 4
        (gv(1, 0, 1, 0, 1, 1), gv(1, 0, -1, 0, 0, 0), gv(1, 0, 1, 0, -1, -1)),
        # Frame containing (1+i)-primitive vector (1+2i, 1, 1+i) of Hermitian norm 8
        (gv(1, 2, 1, 0, 1, 1), gv(1, 0, -1, 2, 0, 0), gv(3, 1, 1, -1, -6, 0)),
    ]

    rho = HermForm3(
        d1=Fraction(3, 7),
        d2=Fraction(5, 14),
        d3=Fraction(3, 14),
        a12=Fraction(4, 9),
        b12=Fraction(-5, 6),
        a13=Fraction(-1, 3),
        b13=Fraction(7, 11),
        a23=Fraction(2, 5),
        b23=Fraction(-3, 8),
    )
    assert rho.trace() == Fraction(1)

    for u, v, w in orthogonal_frames:
        assert u.norm_sq() > 0 and v.norm_sq() > 0 and w.norm_sq() > 0
        assert u.dot(v) == GaussRat(Fraction(0), Fraction(0))
        assert u.dot(w) == GaussRat(Fraction(0), Fraction(0))
        assert v.dot(w) == GaussRat(Fraction(0), Fraction(0))
        assert quad_ray(rho, u) + quad_ray(rho, v) + quad_ray(rho, w) == rho.trace()
        assert herm_add(herm_add(ray_proj(u), ray_proj(v)), ray_proj(w)) == HERM_ID

    # Negative control: non-orthogonal triple does not sum to trace(rho) or HERM_ID
    u_bad, v_bad, w_bad = gv(1, 0, 1, 0, 0, 0), gv(1, 0, 0, 0, 0, 0), gv(0, 0, 0, 0, 1, 0)
    assert u_bad.dot(v_bad) != GaussRat(Fraction(0), Fraction(0))
    assert quad_ray(rho, u_bad) + quad_ray(rho, v_bad) + quad_ray(rho, w_bad) != rho.trace()
    assert herm_add(herm_add(ray_proj(u_bad), ray_proj(v_bad)), ray_proj(w_bad)) != HERM_ID


def test_operator_space_ray_projector_duality_and_zero_normalization() -> None:
    """Verify Section 5 operator-space Frobenius trace pairing, rayProj duality, 9-ray spanning, and zero normalization."""
    rho = HermForm3(
        d1=Fraction(3, 7),
        d2=Fraction(5, 14),
        d3=Fraction(3, 14),
        a12=Fraction(4, 9),
        b12=Fraction(-5, 6),
        a13=Fraction(-1, 3),
        b13=Fraction(7, 11),
        a23=Fraction(2, 5),
        b23=Fraction(-3, 8),
    )
    assert trace_inner(HERM_ZERO, HERM_ZERO) == Fraction(0)
    assert trace_inner(rho, rho) > Fraction(0)
    assert trace_inner(rho, HERM_ID) == rho.trace()

    zero_vec = GVec(GaussRat.of_ints(0, 0), GaussRat.of_ints(0, 0), GaussRat.of_ints(0, 0))
    assert quad_ray(rho, zero_vec) == Fraction(0)
    assert ray_proj(zero_vec) == HERM_ZERO
    assert trace_inner(rho, ray_proj(zero_vec)) == quad_ray(rho, zero_vec)

    for a, b, c, d in itertools.product([-2, -1, 0, 1, 2], repeat=4):
        vec = GVec(
            GaussRat.of_ints(a, b),
            GaussRat.of_ints(c, d),
            GaussRat.of_ints(1, 1),
        )
        proj = ray_proj(vec)
        assert proj.trace() == Fraction(1)
        assert trace_inner(rho, proj) == quad_ray(rho, vec)
        for scalar in [GaussRat.of_ints(2, -1), GaussRat.of_ints(-1, 2)]:
            scaled = GVec(scalar * vec.x, scalar * vec.y, scalar * vec.z)
            assert ray_proj(scaled) == proj

    # Explicit 9-ray basis expansion (rayProj_nine_rays_span_hermForm3)
    spanned = herm_add(
        herm_add(
            herm_add(
                herm_add(
                    herm_add(
                        herm_add(
                            herm_add(
                                herm_add(
                                    herm_smul(rho.d1 - rho.a12 - rho.a13 + rho.b12 + rho.b13, ray_proj(E1)),
                                    herm_smul(rho.d2 - rho.a12 - rho.a23 + rho.b12 + rho.b23, ray_proj(E2)),
                                ),
                                herm_smul(rho.d3 - rho.a13 - rho.a23 + rho.b13 + rho.b23, ray_proj(E3)),
                            ),
                            herm_smul(2 * rho.a12, ray_proj(U12_PLUS)),
                        ),
                        herm_smul(2 * rho.a13, ray_proj(U13_PLUS)),
                    ),
                    herm_smul(2 * rho.a23, ray_proj(U23_PLUS)),
                ),
                herm_smul(-2 * rho.b12, ray_proj(U12_I)),
            ),
            herm_smul(-2 * rho.b13, ray_proj(U13_I)),
        ),
        herm_smul(-2 * rho.b23, ray_proj(U23_I)),
    )
    assert spanned == rho


def test_signed_and_nonnegative_residual_reduction_equivalences() -> None:
    """Verify residual zero-weight, 9-ray vanishing, quadRay bound, and one-sided-to-two-sided bound."""
    rho = HermForm3(
        d1=Fraction(2, 5),
        d2=Fraction(1, 5),
        d3=Fraction(2, 5),
        a12=Fraction(1, 8),
        b12=Fraction(-1, 9),
        a13=Fraction(1, 10),
        b13=Fraction(-1, 12),
        a23=Fraction(1, 7),
        b23=Fraction(1, 11),
    )

    quad_ray_bound = (
        abs(rho.d1)
        + abs(rho.d2)
        + abs(rho.d3)
        + 2
        * (
            abs(rho.a12)
            + abs(rho.b12)
            + abs(rho.a13)
            + abs(rho.b13)
            + abs(rho.a23)
            + abs(rho.b23)
        )
    )

    for a, b, c, d in itertools.product([-2, -1, 0, 1, 2], repeat=4):
        vec = GVec(
            GaussRat.of_ints(a, b),
            GaussRat.of_ints(c, d),
            GaussRat.of_ints(1, -1),
        )
        val = quad_ray(rho, vec)
        assert abs(val) <= quad_ray_bound

    f_quad = lambda v: quad_ray(rho, v)
    reconstructed = tomography_form(f_quad)
    residual = lambda v: f_quad(v) - quad_ray(reconstructed, v)

    for ray in NINE_RAYS:
        assert residual(ray) == Fraction(0)

    bound_b = Fraction(3, 4)
    for r_v, r_w in [
        (Fraction(-3, 4), Fraction(-3, 4)),
        (Fraction(-1, 2), Fraction(1, 8)),
        (Fraction(0), Fraction(-3, 4)),
    ]:
        r_u = -(r_v + r_w)
        assert r_v >= -bound_b and r_w >= -bound_b
        assert r_u <= 2 * bound_b

    r_v_bad, r_w_bad = Fraction(-2), Fraction(-1)
    r_u_bad = -(r_v_bad + r_w_bad)
    assert r_u_bad > 2 * bound_b


def is_one_plus_i_primitive(a: int, b: int, c: int, d: int, e: int, g: int) -> bool:
    """Whether a Gaussian-integer 3-vector (a+bi, c+di, e+gi) is not divisible by (1+i) in Z[i]^3."""
    return not (((a + b) % 2 == 0) and ((c + d) % 2 == 0) and ((e + g) % 2 == 0))


def test_one_plus_i_adic_norm_parity_witnesses_and_mod_four_iff() -> None:
    """Exhaustively check (1+i)-adic norm-parity witnesses and primitive_gaussian_norm_mod_four_iff."""

    def norm_sq(a: int, b: int, c: int, d: int, e: int, g: int) -> int:
        return a * a + b * b + c * c + d * d + e * e + g * g

    assert is_one_plus_i_primitive(1, 0, 1, 0, 1, 1)
    assert norm_sq(1, 0, 1, 0, 1, 1) == 4

    assert is_one_plus_i_primitive(1, 2, 1, 0, 1, 1)
    assert norm_sq(1, 2, 1, 0, 1, 1) == 8

    for x, y in itertools.product(range(-4, 5), repeat=2):
        assert (x * x) % 4 == x % 2
        assert (x * x + y * y) % 4 == (x % 2) + (y % 2)
        assert (x * x + y * y) % 2 == (x + y) % 2
        c_mod4 = (x * x + y * y) % 4
        c_mod2 = (x * x + y * y) % 2
        assert c_mod4 in (0, 1, 2)
        assert ((x + y) % 2 == 0) == (c_mod2 == 0)
        assert (c_mod2 == 1) == (c_mod4 == 1)
        assert ((x % 2 == 0) and (y % 2 == 0)) == (c_mod4 == 0)
        assert ((x % 2 != 0) and (y % 2 != 0)) == (c_mod4 == 2)

    primitive_div4_count = 0
    for a, b, c, d, e, g in itertools.product(range(4), repeat=6):
        if not is_one_plus_i_primitive(a, b, c, d, e, g):
            continue
        n_ab = a * a + b * b
        n_cd = c * c + d * d
        n_eg = e * e + g * g
        total_div4 = ((n_ab + n_cd + n_eg) % 4) == 0
        pattern_match = (
            (n_ab % 2 == 1 and n_cd % 2 == 1 and n_eg % 4 == 2)
            or (n_ab % 2 == 1 and n_cd % 4 == 2 and n_eg % 2 == 1)
            or (n_ab % 4 == 2 and n_cd % 2 == 1 and n_eg % 2 == 1)
        )
        assert total_div4 == pattern_match
        if total_div4:
            primitive_div4_count += 1
    assert primitive_div4_count > 0

    for a, c, e in itertools.product(range(4), repeat=3):
        if is_one_plus_i_primitive(a, 0, c, 0, e, 0):
            assert norm_sq(a, 0, c, 0, e, 0) % 4 != 0


def _v3_int(n: int) -> int:
    n = abs(n)
    if n == 0:
        return 0
    k = 0
    while n % 3 == 0:
        n //= 3
        k += 1
    return k


def _p3_part_int(n: int) -> int:
    n = abs(n)
    if n == 0:
        return 0
    while n % 3 == 0:
        n //= 3
    return n


def v3_rat(q: Fraction) -> int:
    """Exact 3-adic valuation v_3(q) on Q matching v3Rat in Lean 4."""
    if q <= 0:
        return 0
    return _v3_int(q.numerator) - _v3_int(q.denominator)


def u3_rat(q: Fraction) -> Fraction:
    """Exact 3-adic unit residue sign in {-1, +1} for q > 0 (0 if q <= 0) matching u3Rat in Lean 4."""
    if q <= 0:
        return Fraction(0)
    rem = (_p3_part_int(q.numerator) * _p3_part_int(q.denominator)) % 3
    return Fraction(1) if rem == 1 else Fraction(-1)


def is_lead3_coord(c_norm: Fraction, vec_norm: Fraction) -> bool:
    """Whether c_norm > 0 and v_3(c_norm) < v_3(vec_norm) (isLead3Coord in Lean 4)."""
    return c_norm > 0 and v3_rat(c_norm) < v3_rat(vec_norm)


def coord_sign3(c_norm: Fraction, vec_norm: Fraction) -> Fraction:
    """The 3-adic contribution u3Rat(c_norm) * u3Rat(vec_norm) matching coordSign3 in Lean 4."""
    return u3_rat(c_norm) * u3_rat(vec_norm)


def s3(u: GVec) -> Fraction:
    """Global {-1, 0, +1}-valued zero-weight 3-adic residual frame function matching s3 in Lean 4."""
    vn = u.norm_sq()
    if v3_rat(vn) % 2 == 0:
        return Fraction(0)
    if is_lead3_coord(u.x.norm_sq(), vn):
        return coord_sign3(u.x.norm_sq(), vn)
    if is_lead3_coord(u.y.norm_sq(), vn):
        return coord_sign3(u.y.norm_sq(), vn)
    return coord_sign3(u.z.norm_sq(), vn)


def exotic_qi3(u: GVec) -> Fraction:
    """Global {0, 1/3, 2/3}-valued nonnegative non-quadratic frame function (1 + s3(u)) / 3."""
    return (Fraction(1) + s3(u)) / 3


def _v7_int(n: int) -> int:
    n = abs(n)
    if n == 0:
        return 0
    k = 0
    while n % 7 == 0:
        n //= 7
        k += 1
    return k


def _p7_part_int(n: int) -> int:
    n = abs(n)
    if n == 0:
        return 0
    while n % 7 == 0:
        n //= 7
    return n


def v7_rat(q: Fraction) -> int:
    """Exact 7-adic valuation v_7(q) on Q matching v7Rat in Lean 4."""
    if q <= 0:
        return 0
    return _v7_int(q.numerator) - _v7_int(q.denominator)


def u7_rat(q: Fraction) -> Fraction:
    """Exact 7-adic unit Legendre residue sign (q / 7) in {-1, +1} for q > 0 matching u7Rat in Lean 4."""
    if q <= 0:
        return Fraction(0)
    rem = (_p7_part_int(q.numerator) * _p7_part_int(q.denominator)) % 7
    return Fraction(1) if rem in (1, 2, 4) else Fraction(-1)


def is_lead7_coord(c_norm: Fraction, vec_norm: Fraction) -> bool:
    """Whether c_norm > 0 and v_7(c_norm) < v_7(vec_norm) (isLead7Coord in Lean 4)."""
    return c_norm > 0 and v7_rat(c_norm) < v7_rat(vec_norm)


def coord_sign7(c_norm: Fraction, vec_norm: Fraction) -> Fraction:
    """The 7-adic contribution u7Rat(c_norm) * u7Rat(vec_norm) matching coordSign7 in Lean 4."""
    return u7_rat(c_norm) * u7_rat(vec_norm)


def s7(u: GVec) -> Fraction:
    """Global {-1, 0, +1}-valued zero-weight 7-adic residual frame function matching s7 in Lean 4."""
    vn = u.norm_sq()
    if v7_rat(vn) % 2 == 0:
        return Fraction(0)
    if is_lead7_coord(u.x.norm_sq(), vn):
        return coord_sign7(u.x.norm_sq(), vn)
    if is_lead7_coord(u.y.norm_sq(), vn):
        return coord_sign7(u.y.norm_sq(), vn)
    return coord_sign7(u.z.norm_sq(), vn)


def exotic_qi7(u: GVec) -> Fraction:
    """Global {0, 1/3, 2/3}-valued nonnegative non-quadratic frame function (1 + s7(u)) / 3 matching exoticQi7."""
    return (Fraction(1) + s7(u)) / 3


def comb_residual_37(c3: Fraction, c7: Fraction, u: GVec) -> Fraction:
    """Two-parameter linear combination c3 * s3(u) + c7 * s7(u) matching combResidual37 in Lean 4."""
    return c3 * s3(u) + c7 * s7(u)


def exotic_comb_37(c3: Fraction, c7: Fraction, u: GVec) -> Fraction:
    """Two-parameter frame function (1 + combResidual37(c3, c7, u)) / 3 matching exoticComb37 in Lean 4."""
    return (Fraction(1) + comb_residual_37(c3, c7, u)) / 3


def _vp_int(n: int, p: int) -> int:
    n = abs(n)
    if n == 0 or p < 2:
        return 0
    k = 0
    while n % p == 0:
        n //= p
        k += 1
    return k


def _pp_part_int(n: int, p: int) -> int:
    n = abs(n)
    if n == 0 or p < 2:
        return 0
    while n % p == 0:
        n //= p
    return n


def vp_rat(q: Fraction, p: int) -> int:
    """Exact p-adic valuation v_p(q) on Q matching vpRat in Lean 4."""
    if q <= 0:
        return 0
    return _vp_int(q.numerator, p) - _vp_int(q.denominator, p)


def up_rat(q: Fraction, p: int) -> Fraction:
    """Exact p-adic unit Euler-criterion Legendre sign (q / p) in {-1, +1} for q > 0 matching upRat in Lean 4."""
    if q <= 0:
        return Fraction(0)
    rem = (_pp_part_int(q.numerator, p) * _pp_part_int(q.denominator, p)) % p
    return Fraction(1) if pow(rem, (p - 1) // 2, p) == 1 else Fraction(-1)


def is_leadp_coord(c_norm: Fraction, vec_norm: Fraction, p: int) -> bool:
    """Whether c_norm > 0 and v_p(c_norm) < v_p(vec_norm) (isLeadPCoord in Lean 4)."""
    return c_norm > 0 and vp_rat(c_norm, p) < vp_rat(vec_norm, p)


def coord_signp(c_norm: Fraction, vec_norm: Fraction, p: int) -> Fraction:
    """The p-adic contribution upRat(c_norm, p) * upRat(vec_norm, p) matching coordSignP in Lean 4."""
    return up_rat(c_norm, p) * up_rat(vec_norm, p)


def sp(u: GVec, p: int) -> Fraction:
    """Uniform prime-indexed {-1, 0, +1}-valued residual s_p(u) matching sp p u in Lean 4."""
    vn = u.norm_sq()
    if vp_rat(vn, p) % 2 == 0:
        return Fraction(0)
    if is_leadp_coord(u.x.norm_sq(), vn, p):
        return coord_signp(u.x.norm_sq(), vn, p)
    if is_leadp_coord(u.y.norm_sq(), vn, p):
        return coord_signp(u.y.norm_sq(), vn, p)
    return coord_signp(u.z.norm_sq(), vn, p)


def fin_comb_residual(primes: list[int], coeffs: list[Fraction], u: GVec) -> Fraction:
    """Finite m-prime residual linear combination sum_i c_i * s_{p_i}(u) matching finCombResidual in Lean 4."""
    return sum((c * sp(u, p) for p, c in zip(primes, coeffs)), Fraction(0))


def fin_exotic_comb(primes: list[int], coeffs: list[Fraction], u: GVec) -> Fraction:
    """Finite m-parameter frame function (1 + finCombResidual) / 3 matching finExoticComb in Lean 4."""
    return (Fraction(1) + fin_comb_residual(primes, coeffs, u)) / 3



def herm_cross(u: GVec, v: GVec) -> GVec:
    """Hermitian cross product conj(u x v) orthogonal to both u and v in Q(i)^3."""
    return GVec(
        (u.y * v.z - u.z * v.y).conj(),
        (u.z * v.x - u.x * v.z).conj(),
        (u.x * v.y - u.y * v.x).conj(),
    )


def det_gvec(u: GVec, v: GVec, w: GVec) -> GaussRat:
    """3x3 determinant of [u, v, w] over Q(i) matching detGVec in Lean 4."""
    return (
        u.x * (v.y * w.z - v.z * w.y)
        - u.y * (v.x * w.z - v.z * w.x)
        + u.z * (v.x * w.y - v.y * w.x)
    )


def test_s3_global_bounded_zero_weight_residual_and_exotic_qi3() -> None:
    """Verify Section 8 global bounded residual s3, exoticQi3, 3-adic frame invariants, and negative controls."""

    def gv(a: int, b: int, c: int, d: int, e: int, g: int) -> GVec:
        return GVec(
            GaussRat.of_ints(a, b),
            GaussRat.of_ints(c, d),
            GaussRat.of_ints(e, g),
        )

    # 1. Every nonzero Gaussian rational z in Q(i)^x has even v_3(|z|^2) (v3Rat_normSq_even)
    for num_re, num_im in itertools.product(range(-6, 7), repeat=2):
        if num_re == 0 and num_im == 0:
            continue
        for den in (1, 2, 3, 6, 9):
            z = GaussRat(Fraction(num_re, den), Fraction(num_im, den))
            assert v3_rat(z.norm_sq()) % 2 == 0
            assert u3_rat(z.norm_sq()) in (Fraction(-1), Fraction(1))
            assert u3_rat(z.norm_sq()) * u3_rat(z.norm_sq()) == Fraction(1)

    # 2. s3 vanishes on 0 and on all 9 tomography rays; exotic_qi3 equals 1/3 on all 9 rays
    zero_vec = gv(0, 0, 0, 0, 0, 0)
    assert s3(zero_vec) == Fraction(0)
    for ray in NINE_RAYS:
        assert s3(ray) == Fraction(0)
        assert exotic_qi3(ray) == Fraction(1, 3)

    reconstructed_s3 = tomography_form(s3)
    assert reconstructed_s3 == HERM_ZERO
    reconstructed_exotic = tomography_form(exotic_qi3)
    assert reconstructed_exotic == herm_smul(Fraction(1, 3), HERM_ID)

    # 3. Nonzero witnesses across norm shells (norm 3, norm 12 with 4|N, norm 24 with 8|N)
    #    and explicit (1+i)-primitivity checks distinguishing higher-shell rays from scalar multiples
    witness_111 = gv(1, 0, 1, 0, 1, 0)
    witness_div4 = gv(1, 2, 1, 2, 1, 1)
    witness_div8 = gv(1, 4, 1, 2, 1, 1)

    assert is_one_plus_i_primitive(1, 0, 1, 0, 1, 0)
    assert witness_111.norm_sq() == Fraction(3)
    assert s3(witness_111) == Fraction(1)
    assert exotic_qi3(witness_111) == Fraction(2, 3)
    assert exotic_qi3(witness_111) != quad_ray(reconstructed_exotic, witness_111)

    assert is_one_plus_i_primitive(1, 2, 1, 2, 1, 1)
    assert witness_div4.norm_sq() == Fraction(12)
    assert witness_div4.norm_sq() % 4 == 0
    assert s3(witness_div4) == Fraction(-1)
    assert exotic_qi3(witness_div4) == Fraction(0)

    assert is_one_plus_i_primitive(1, 4, 1, 2, 1, 1)
    assert witness_div8.norm_sq() == Fraction(24)
    assert witness_div8.norm_sq() % 8 == 0
    assert s3(witness_div8) == Fraction(1)
    assert exotic_qi3(witness_div8) == Fraction(2, 3)

    # Negative control for (1+i)-primitivity: scalar multiples (1+i)^2*(1,1,1) = (2i,2i,2i) (norm 12)
    # and 2*(1+i)*(1,1,1) = (2+2i,2+2i,2+2i) (norm 24) lie on the same ray as (1,1,1) and fail primitivity
    assert not is_one_plus_i_primitive(0, 2, 0, 2, 0, 2)
    assert gv(0, 2, 0, 2, 0, 2).norm_sq() == Fraction(12)
    assert s3(gv(0, 2, 0, 2, 0, 2)) == s3(witness_111) == Fraction(1) != s3(witness_div4)
    assert not is_one_plus_i_primitive(2, 2, 2, 2, 2, 2)
    assert gv(2, 2, 2, 2, 2, 2).norm_sq() == Fraction(24)

    # 3b. Constructive 7-ray operator-space projector kernel decomposition & separation (Section 5)
    proj_111_rhs = herm_add(
        herm_smul(
            Fraction(-1, 3),
            herm_add(herm_add(ray_proj(E1), ray_proj(E2)), ray_proj(E3)),
        ),
        herm_smul(
            Fraction(2, 3),
            herm_add(herm_add(ray_proj(U12_PLUS), ray_proj(U13_PLUS)), ray_proj(U23_PLUS)),
        ),
    )
    assert ray_proj(witness_111) == proj_111_rhs

    sample_rho = HermForm3(
        Fraction(2, 7),
        Fraction(3, 7),
        Fraction(2, 7),
        Fraction(1, 5),
        Fraction(-2, 9),
        Fraction(4, 11),
        Fraction(-3, 8),
        Fraction(5, 13),
        Fraction(-1, 6),
    )
    quad_kernel_lhs = (
        quad_ray(sample_rho, witness_111)
        + Fraction(1, 3) * (quad_ray(sample_rho, E1) + quad_ray(sample_rho, E2) + quad_ray(sample_rho, E3))
        - Fraction(2, 3)
        * (quad_ray(sample_rho, U12_PLUS) + quad_ray(sample_rho, U13_PLUS) + quad_ray(sample_rho, U23_PLUS))
    )
    assert quad_kernel_lhs == Fraction(0)

    s3_kernel_lhs = (
        s3(witness_111)
        + Fraction(1, 3) * (s3(E1) + s3(E2) + s3(E3))
        - Fraction(2, 3) * (s3(U12_PLUS) + s3(U13_PLUS) + s3(U23_PLUS))
    )
    exotic_kernel_lhs = (
        exotic_qi3(witness_111)
        + Fraction(1, 3) * (exotic_qi3(E1) + exotic_qi3(E2) + exotic_qi3(E3))
        - Fraction(2, 3) * (exotic_qi3(U12_PLUS) + exotic_qi3(U13_PLUS) + exotic_qi3(U23_PLUS))
    )
    assert s3_kernel_lhs == Fraction(1)
    assert exotic_kernel_lhs == Fraction(1, 3)

    # 4. Ray-scaling invariance s3(l * u) == s3(u) and boundedness |s3(u)| <= 1
    scalars = [
        GaussRat.of_ints(3, 0),
        GaussRat.of_ints(1, 1),
        GaussRat.of_ints(2, -3),
        GaussRat(Fraction(3, 5), Fraction(-6, 5)),
        GaussRat(Fraction(-1, 9), Fraction(2, 9)),
    ]
    probe_vecs = [
        witness_111,
        witness_div4,
        witness_div8,
        gv(1, 0, -1, 0, 0, 0),
        gv(1, 0, 1, 0, -2, 0),
        gv(1, 1, 1, 0, 0, 0),
        gv(0, 0, 1, 1, 1, 0),
        gv(1, 0, 0, 0, 1, 1),
    ]
    for u in probe_vecs:
        assert s3(u) in (Fraction(-1), Fraction(0), Fraction(1))
        assert abs(s3(u)) <= Fraction(1)
        assert exotic_qi3(u) in (Fraction(0), Fraction(1, 3), Fraction(2, 3))
        for l in scalars:
            lu = GVec(l * u.x, l * u.y, l * u.z)
            assert s3(lu) == s3(u)
            assert exotic_qi3(lu) == exotic_qi3(u)

    # 5. Frame valuation parity, ortho_coord_identity_x, and zero-weight / weight-1 frame additivity
    ortho_pairs = [
        (E1, E2),
        (E1, U23_PLUS),
        (E3, U12_I),
        (witness_111, gv(1, 0, -1, 0, 0, 0)),
        (witness_111, gv(1, 0, 1, 0, -2, 0)),
        (witness_111, gv(0, 0, 1, 0, -1, 0)),
        (witness_111, gv(-2, 0, 1, 0, 1, 0)),
        (gv(1, 1, 1, 0, 0, 0), gv(1, 1, -2, 0, 0, 0)),
        (gv(0, 0, 1, 1, 1, 0), gv(0, 0, 1, 1, -2, 0)),
        (gv(1, 0, 0, 0, 1, 1), gv(-2, 0, 0, 0, 1, 1)),
        (witness_div4, gv(1, 0, -1, 0, 0, 0)),
        (witness_div4, gv(1, 2, 1, 2, -5, -5)),
        (witness_div8, gv(0, 0, 2, 4, -5, -5)),
        (witness_div8, gv(1, 4, -3, -6, -1, -1)),
    ]
    for u, v in ortho_pairs:
        w = herm_cross(u, v)
        assert u.norm_sq() > 0 and v.norm_sq() > 0 and w.norm_sq() > 0
        assert u.dot(v) == GaussRat.of_ints(0, 0)
        assert u.dot(w) == GaussRat.of_ints(0, 0)
        assert v.dot(w) == GaussRat.of_ints(0, 0)

        # Verify detGVec_normSq_of_frame: |det[u,v,w]|^2 == N(u) N(v) N(w)
        assert det_gvec(u, v, w).norm_sq() == u.norm_sq() * v.norm_sq() * w.norm_sq()

        # Verify frame_v3Rat_sum_even
        v3_sum = v3_rat(u.norm_sq()) + v3_rat(v.norm_sq()) + v3_rat(w.norm_sq())
        assert v3_sum % 2 == 0

        # Verify ortho_coord_identity_x on all pairs in the frame
        for p, q in ((u, v), (u, w), (v, w)):
            lhs = (
                p.x.norm_sq() * q.norm_sq()
                + q.x.norm_sq() * p.norm_sq()
                + (p.y * q.z - q.y * p.z).norm_sq()
            )
            assert lhs == p.norm_sq() * q.norm_sq()

        # Verify s3 is a zero-weight frame function and exotic_qi3 is a weight-1 frame function
        assert s3(u) + s3(v) + s3(w) == Fraction(0)
        assert exotic_qi3(u) + exotic_qi3(v) + exotic_qi3(w) == Fraction(1)

    # 6. Multi-prime inert residual s7 (p = 7 == 3 mod 4 via Legendre symbol (./7)):
    #    linearly independent of s3 and vanishes on all 49 real primitive rays in [-2, 2]^3
    witness_p7 = gv(1, 0, 2, 0, 1, 1)  # norm 1 + 4 + 2 = 7
    assert is_one_plus_i_primitive(1, 0, 2, 0, 1, 1)
    assert witness_p7.norm_sq() == Fraction(7)
    assert s3(witness_111) == Fraction(1) and s7(witness_111) == Fraction(0)
    assert s3(witness_p7) == Fraction(0) and s7(witness_p7) == Fraction(1)
    for ray in NINE_RAYS:
        assert s7(ray) == Fraction(0)

    # Verify s7 vanishes on all real vectors in [-2, 2]^3 (since max norm is 12 and 7 != a^2+b^2+c^2)
    for a, c, e in itertools.product(range(-2, 3), repeat=3):
        if a == 0 and c == 0 and e == 0:
            continue
        assert s7(gv(a, 0, c, 0, e, 0)) == Fraction(0)

    for v7_ortho in (gv(2, 0, -1, 0, 0, 0), gv(2, 0, 2, 0, -3, -3)):
        w7 = herm_cross(witness_p7, v7_ortho)
        assert witness_p7.dot(v7_ortho) == GaussRat.of_ints(0, 0)
        assert (v7_rat(witness_p7.norm_sq()) + v7_rat(v7_ortho.norm_sq()) + v7_rat(w7.norm_sq())) % 2 == 0
        assert s7(witness_p7) + s7(v7_ortho) + s7(w7) == Fraction(0)

    # 7. Negative Control A: mutating the u3 == 2 (mod 3) sign from -1 to +1 breaks zero-weight additivity
    def bad_unsigned_s3(u: GVec) -> Fraction:
        return abs(s3(u))

    u0, v0 = witness_111, gv(1, 0, -1, 0, 0, 0)
    w0 = herm_cross(u0, v0)
    assert bad_unsigned_s3(u0) + bad_unsigned_s3(v0) + bad_unsigned_s3(w0) == Fraction(2) != Fraction(0)

    # 8. Negative Control B: using non-inert prime p = 5 == 1 (mod 4) breaks even norm valuation parity
    def v5_int(n: int) -> int:
        n = abs(n)
        if n == 0:
            return 0
        k = 0
        while n % 5 == 0:
            n //= 5
            k += 1
        return k

    z_split = GaussRat.of_ints(2, 1)  # 2 + i has norm 5
    assert v5_int(int(z_split.norm_sq())) == 1  # odd 5-adic valuation!
    u_split = GVec(z_split, GaussRat.of_ints(0, 0), GaussRat.of_ints(0, 0))
    assert (
        v5_int(int(u_split.norm_sq()))
        + v5_int(int(E2.norm_sq()))
        + v5_int(int(E3.norm_sq()))
    ) % 2 == 1


def test_archimedean_discontinuity_and_field_extension_elimination() -> None:
    """Verify Section 9 archimedean oscillation near tomo_e1, Q(i, sqrt(3))^3 even-norm frame, and projector linearity."""
    for k in range(1, 15):
        inv3k = Fraction(1, 3 * k)
        pos_int = GVec(GaussRat.of_ints(3 * k, 0), GaussRat.of_ints(1, 0), GaussRat.of_ints(1, 1))
        neg_int = GVec(GaussRat.of_ints(3 * k, 0), GaussRat.of_ints(1, 1), GaussRat.of_ints(1, 0))
        pos_ray = GVec(GaussRat.of_ints(1, 0), GaussRat(inv3k, Fraction(0)), GaussRat(inv3k, inv3k))
        neg_ray = GVec(GaussRat.of_ints(1, 0), GaussRat(inv3k, inv3k), GaussRat(inv3k, Fraction(0)))

        assert pos_int.norm_sq() == Fraction(9 * k * k + 3)
        assert neg_int.norm_sq() == Fraction(9 * k * k + 3)
        assert v3_rat(pos_int.norm_sq()) == 1
        assert u3_rat(pos_int.norm_sq()) == Fraction(1)
        assert s3(pos_int) == Fraction(1) and s3(pos_ray) == Fraction(1)
        assert s3(neg_int) == Fraction(-1) and s3(neg_ray) == Fraction(-1)
        assert exotic_qi3(pos_ray) == Fraction(2, 3)
        assert exotic_qi3(neg_ray) == Fraction(0)

        dist_pos = (
            (pos_ray.x - E1.x).norm_sq()
            + (pos_ray.y - E1.y).norm_sq()
            + (pos_ray.z - E1.z).norm_sq()
        )
        dist_neg = (
            (neg_ray.x - E1.x).norm_sq()
            + (neg_ray.y - E1.y).norm_sq()
            + (neg_ray.z - E1.z).norm_sq()
        )
        assert dist_pos == Fraction(1, 3 * k * k)
        assert dist_neg == Fraction(1, 3 * k * k)

    # Positive control (archimedeanContinuousAt_quadRay_tomo_e1):
    # Every Hermitian form quad_ray(rho, v) converges to quad_ray(rho, E1) == rho.d1 at O(1/k^2).
    rho_sample = HermForm3(
        d1=Fraction(2, 5),
        d2=Fraction(1, 5),
        d3=Fraction(2, 5),
        a12=Fraction(1, 7),
        b12=Fraction(-1, 9),
        a13=Fraction(2, 11),
        b13=Fraction(-1, 13),
        a23=Fraction(1, 6),
        b23=Fraction(1, 8),
    )
    coeff_norm = (
        abs(rho_sample.d1)
        + abs(rho_sample.d2)
        + abs(rho_sample.d3)
        + abs(rho_sample.a12)
        + abs(rho_sample.b12)
        + abs(rho_sample.a13)
        + abs(rho_sample.b13)
        + abs(rho_sample.a23)
        + abs(rho_sample.b23)
    )
    assert quad_ray(rho_sample, E1) == rho_sample.d1
    for k in range(1, 15):
        inv3k = Fraction(1, 3 * k)
        pos_ray = GVec(GaussRat.of_ints(1, 0), GaussRat(inv3k, Fraction(0)), GaussRat(inv3k, inv3k))
        neg_ray = GVec(GaussRat.of_ints(1, 0), GaussRat(inv3k, inv3k), GaussRat(inv3k, Fraction(0)))
        theta = Fraction(1, 3 * k * k)
        assert abs(quad_ray(rho_sample, pos_ray) - rho_sample.d1) <= 8 * coeff_norm * theta
        assert abs(quad_ray(rho_sample, neg_ray) - rho_sample.d1) <= 8 * coeff_norm * theta

    # Exact biquadratic arithmetic over Q(i, sqrt(p)) matching GaussRatSqrt3 / GVecSqrt3 in Lean 4
    def gr_p_add(z, w):
        return (z[0] + w[0], z[1] + w[1])

    def gr_p_mul(p_val: int, z, w):
        p_gr = GaussRat.of_ints(p_val, 0)
        return (z[0] * w[0] + p_gr * (z[1] * w[1]), z[0] * w[1] + z[1] * w[0])

    def gr_p_conj(z):
        return (z[0].conj(), z[1].conj())

    def gv_p_inner(p_val: int, u, v):
        acc = (GaussRat.of_ints(0, 0), GaussRat.of_ints(0, 0))
        for cu, cv in zip(u, v):
            acc = gr_p_add(acc, gr_p_mul(p_val, gr_p_conj(cu), cv))
        return acc

    def four_square_partner_p(v0: GVec, w0: GVec, alpha: GaussRat, beta: GaussRat):
        return (
            (beta * w0.x, alpha * v0.x),
            (beta * w0.y, alpha * v0.y),
            (beta * w0.z, alpha * v0.z),
        )

    def four_square_partner_q(v0: GVec, w0: GVec, alpha: GaussRat, beta: GaussRat):
        neg_one = GaussRat.of_ints(-1, 0)
        return (
            (neg_one * (alpha.conj() * w0.x), beta.conj() * v0.x),
            (neg_one * (alpha.conj() * w0.y), beta.conj() * v0.y),
            (neg_one * (alpha.conj() * w0.z), beta.conj() * v0.z),
        )

    zero_gr3 = (GaussRat.of_ints(0, 0), GaussRat.of_ints(0, 0))
    one_gr3 = (GaussRat.of_ints(1, 0), GaussRat.of_ints(0, 0))
    inv_sqrt3 = (GaussRat.of_ints(0, 0), GaussRat(Fraction(1, 3), Fraction(0)))

    u_111_s3 = (
        (GaussRat.of_ints(1, 0), GaussRat.of_ints(0, 0)),
        (GaussRat.of_ints(1, 0), GaussRat.of_ints(0, 0)),
        (GaussRat.of_ints(1, 0), GaussRat.of_ints(0, 0)),
    )
    u_111_unit = tuple(gr_p_mul(3, inv_sqrt3, c) for c in u_111_s3)
    assert gv_p_inner(3, u_111_unit, u_111_unit) == one_gr3
    assert v3_rat(gv_p_inner(3, u_111_unit, u_111_unit)[0].re) % 2 == 0

    p_s3 = (
        (GaussRat.of_ints(1, 1), GaussRat.of_ints(1, 0)),
        (GaussRat.of_ints(1, 1), GaussRat.of_ints(-1, 0)),
        (GaussRat.of_ints(-2, -2), GaussRat.of_ints(0, 0)),
    )
    q_s3 = (
        (GaussRat.of_ints(-1, 0), GaussRat.of_ints(1, -1)),
        (GaussRat.of_ints(-1, 0), GaussRat.of_ints(-1, 1)),
        (GaussRat.of_ints(2, 0), GaussRat.of_ints(0, 0)),
    )
    assert gv_p_inner(3, u_111_s3, p_s3) == zero_gr3
    assert gv_p_inner(3, u_111_s3, q_s3) == zero_gr3
    assert gv_p_inner(3, p_s3, q_s3) == zero_gr3
    assert gv_p_inner(3, u_111_s3, u_111_s3) == (GaussRat.of_ints(3, 0), GaussRat.of_ints(0, 0))
    assert gv_p_inner(3, p_s3, p_s3) == (GaussRat.of_ints(18, 0), GaussRat.of_ints(0, 0))
    assert gv_p_inner(3, q_s3, q_s3) == (GaussRat.of_ints(18, 0), GaussRat.of_ints(0, 0))
    assert v3_rat(Fraction(3)) == 1
    assert v3_rat(Fraction(18)) == 2
    assert (v3_rat(Fraction(3)) + v3_rat(Fraction(18)) + v3_rat(Fraction(18))) % 2 == 1

    # Parameterized four-square SU(2) completion at p = 7 matching isFrameSqrt7_witness_p7_norms in Lean 4:
    u7_vec = GVec(GaussRat.of_ints(1, 0), GaussRat.of_ints(2, 0), GaussRat.of_ints(1, 1))
    v7_0 = GVec(GaussRat.of_ints(2, 0), GaussRat.of_ints(-1, 0), GaussRat.of_ints(0, 0))
    w7_0 = GVec(GaussRat.of_ints(1, -1), GaussRat.of_ints(2, -2), GaussRat.of_ints(-5, 0))
    alpha7 = GaussRat.of_ints(1, 1)
    beta7 = GaussRat.of_ints(2, 1)
    assert alpha7.norm_sq() + beta7.norm_sq() == Fraction(7)
    u7_s7 = (
        (u7_vec.x, GaussRat.of_ints(0, 0)),
        (u7_vec.y, GaussRat.of_ints(0, 0)),
        (u7_vec.z, GaussRat.of_ints(0, 0)),
    )
    inv_sqrt7 = (GaussRat.of_ints(0, 0), GaussRat(Fraction(1, 7), Fraction(0)))
    u7_unit = tuple(gr_p_mul(7, inv_sqrt7, c) for c in u7_s7)
    assert gv_p_inner(7, u7_unit, u7_unit) == one_gr3
    p_s7 = four_square_partner_p(v7_0, w7_0, alpha7, beta7)
    q_s7 = four_square_partner_q(v7_0, w7_0, alpha7, beta7)
    assert gv_p_inner(7, u7_s7, p_s7) == zero_gr3
    assert gv_p_inner(7, u7_s7, q_s7) == zero_gr3
    assert gv_p_inner(7, p_s7, q_s7) == zero_gr3
    assert gv_p_inner(7, u7_s7, u7_s7) == (GaussRat.of_ints(7, 0), GaussRat.of_ints(0, 0))
    assert gv_p_inner(7, p_s7, p_s7) == (GaussRat.of_ints(245, 0), GaussRat.of_ints(0, 0))
    assert gv_p_inner(7, q_s7, q_s7) == (GaussRat.of_ints(245, 0), GaussRat.of_ints(0, 0))


def test_multi_prime_s3_s7_linear_independence_and_joint_elimination() -> None:
    """Verify Subsection 9D: s7, exoticQi7, combResidual37, exoticComb37, witness_p7 projector kernel, selective oscillation near tomo_e1, and joint elimination."""

    def gv(a: int, b: int, c: int, d: int, e: int, g: int) -> GVec:
        return GVec(
            GaussRat.of_ints(a, b),
            GaussRat.of_ints(c, d),
            GaussRat.of_ints(e, g),
        )

    witness_111 = gv(1, 0, 1, 0, 1, 0)
    witness_p7 = gv(1, 0, 2, 0, 1, 1)

    # 1. Dual Kronecker-delta evaluation on (witness_111, witness_p7) (s3_s7_dual_on_witnesses)
    assert s3(witness_111) == Fraction(1) and s7(witness_111) == Fraction(0)
    assert s3(witness_p7) == Fraction(0) and s7(witness_p7) == Fraction(1)
    assert exotic_qi7(witness_111) == Fraction(1, 3)
    assert exotic_qi7(witness_p7) == Fraction(2, 3)

    reconstructed_exotic7 = tomography_form(exotic_qi7)
    assert reconstructed_exotic7 == herm_smul(Fraction(1, 3), HERM_ID)
    assert exotic_qi7(witness_p7) != quad_ray(reconstructed_exotic7, witness_p7)

    # 2. Constructive 9-ray projector expansion for witness_p7 = (1, 2, 1 + i)
    #    (rayProj_witness_p7_decomp, quadRay_witness_p7_kernel_relation, s7_witness_p7_kernel_separation)
    def witness_p7_kernel_eval(f) -> Fraction:
        return (
            f(witness_p7)
            + Fraction(3, 7) * f(E1)
            + Fraction(2, 7) * f(E2)
            + Fraction(4, 7) * f(E3)
            - Fraction(4, 7) * f(U12_PLUS)
            - Fraction(2, 7) * f(U13_PLUS)
            - Fraction(4, 7) * f(U23_PLUS)
            - Fraction(2, 7) * f(U13_I)
            - Fraction(4, 7) * f(U23_I)
        )

    p_wp7 = ray_proj(witness_p7)
    p_wp7_rhs = herm_add(
        herm_add(
            herm_add(
                herm_add(
                    herm_smul(Fraction(-3, 7), ray_proj(E1)),
                    herm_smul(Fraction(-2, 7), ray_proj(E2)),
                ),
                herm_add(
                    herm_smul(Fraction(-4, 7), ray_proj(E3)),
                    herm_smul(Fraction(4, 7), ray_proj(U12_PLUS)),
                ),
            ),
            herm_add(
                herm_smul(Fraction(2, 7), ray_proj(U13_PLUS)),
                herm_smul(Fraction(4, 7), ray_proj(U23_PLUS)),
            ),
        ),
        herm_add(
            herm_smul(Fraction(2, 7), ray_proj(U13_I)),
            herm_smul(Fraction(4, 7), ray_proj(U23_I)),
        ),
    )
    assert p_wp7 == p_wp7_rhs

    rho_sample = HermForm3(
        d1=Fraction(2, 5),
        d2=Fraction(1, 5),
        d3=Fraction(2, 5),
        a12=Fraction(1, 7),
        b12=Fraction(-1, 9),
        a13=Fraction(2, 11),
        b13=Fraction(-1, 13),
        a23=Fraction(1, 6),
        b23=Fraction(1, 8),
    )
    assert witness_p7_kernel_eval(lambda u: quad_ray(rho_sample, u)) == Fraction(0)
    assert witness_p7_kernel_eval(s7) == Fraction(1)
    assert witness_p7_kernel_eval(s3) == Fraction(0)

    # 3. 2D space combResidual37 and 2-parameter nonnegative family exoticComb37
    #    (exoticComb37_isNonnegFrameFunction, exoticComb37_quadratic_iff)
    coeff_samples = [
        (Fraction(0), Fraction(0)),
        (Fraction(1), Fraction(0)),
        (Fraction(0), Fraction(1)),
        (Fraction(-1), Fraction(0)),
        (Fraction(0), Fraction(-1)),
        (Fraction(2, 5), Fraction(-3, 7)),
        (Fraction(-4, 9), Fraction(5, 11)),
        (Fraction(1, 2), Fraction(1, 2)),
        (Fraction(-1, 3), Fraction(2, 3)),
    ]
    ortho_pairs = [
        (E1, E2),
        (witness_111, gv(1, 0, -1, 0, 0, 0)),
        (witness_p7, gv(2, 0, -1, 0, 0, 0)),
        (witness_p7, gv(2, 0, 2, 0, -3, -3)),
        (gv(1, 1, 2, 1, 0, 0), gv(2, -1, -1, -1, 0, 0)),
    ]
    for c3, c7 in coeff_samples:
        assert abs(c3) + abs(c7) <= Fraction(1)
        assert witness_p7_kernel_eval(lambda u: comb_residual_37(c3, c7, u)) == c7
        for ray in NINE_RAYS:
            assert comb_residual_37(c3, c7, ray) == Fraction(0)
            assert exotic_comb_37(c3, c7, ray) == Fraction(1, 3)
        for u, v in ortho_pairs:
            w = herm_cross(u, v)
            assert comb_residual_37(c3, c7, u) + comb_residual_37(c3, c7, v) + comb_residual_37(c3, c7, w) == Fraction(0)
            assert exotic_comb_37(c3, c7, u) + exotic_comb_37(c3, c7, v) + exotic_comb_37(c3, c7, w) == Fraction(1)
            for vec in (u, v, w):
                assert abs(comb_residual_37(c3, c7, vec)) <= abs(c3) + abs(c7)
                assert Fraction(0) <= exotic_comb_37(c3, c7, vec) <= Fraction(2, 3)
        # Linear independence (s3_s7_linearIndependent) and quadratic iff (exoticComb37_quadratic_iff)
        vanishes_on_both = (
            comb_residual_37(c3, c7, witness_111) == Fraction(0)
            and comb_residual_37(c3, c7, witness_p7) == Fraction(0)
        )
        assert vanishes_on_both == (c3 == Fraction(0) and c7 == Fraction(0))
        reconstructed = tomography_form(lambda u: exotic_comb_37(c3, c7, u))
        assert reconstructed == herm_smul(Fraction(1, 3), HERM_ID)
        matches_reconstructed = (
            exotic_comb_37(c3, c7, witness_111) == quad_ray(reconstructed, witness_111)
            and exotic_comb_37(c3, c7, witness_p7) == quad_ray(reconstructed, witness_p7)
        )
        assert matches_reconstructed == (c3 == Fraction(0) and c7 == Fraction(0))

    # 4. Selective cross-prime oscillation near tomo_e1 = (1, 0, 0)
    #    (s3_s7_selective_oscillation_near_tomo_e1, exoticComb37_archimedeanContinuousAt_tomo_e1_iff)
    for k in range(1, 12):
        inv21k = Fraction(1, 21 * k)
        u3_pos = GVec(GaussRat.of_ints(1, 0), GaussRat(inv21k, Fraction(0)), GaussRat(inv21k, inv21k))
        u3_neg = GVec(GaussRat.of_ints(1, 0), GaussRat(inv21k, inv21k), GaussRat(inv21k, Fraction(0)))

        inv7k = Fraction(1, 7 * k)
        u7_pos = GVec(GaussRat.of_ints(1, 0), GaussRat(inv7k, inv7k), GaussRat(2 * inv7k, inv7k))
        u7_neg = GVec(GaussRat.of_ints(1, 0), GaussRat(2 * inv7k, inv7k), GaussRat(inv7k, inv7k))

        dist_u3_pos = (u3_pos.x - E1.x).norm_sq() + (u3_pos.y - E1.y).norm_sq() + (u3_pos.z - E1.z).norm_sq()
        dist_u3_neg = (u3_neg.x - E1.x).norm_sq() + (u3_neg.y - E1.y).norm_sq() + (u3_neg.z - E1.z).norm_sq()
        dist_u7_pos = (u7_pos.x - E1.x).norm_sq() + (u7_pos.y - E1.y).norm_sq() + (u7_pos.z - E1.z).norm_sq()
        dist_u7_neg = (u7_neg.x - E1.x).norm_sq() + (u7_neg.y - E1.y).norm_sq() + (u7_neg.z - E1.z).norm_sq()

        assert dist_u3_pos == Fraction(1, 147 * k * k)
        assert dist_u3_neg == Fraction(1, 147 * k * k)
        assert dist_u7_pos == Fraction(1, 7 * k * k)
        assert dist_u7_neg == Fraction(1, 7 * k * k)

        # Selective cross-prime evaluation:
        assert s3(u3_pos) == Fraction(1) and s7(u3_pos) == Fraction(0)
        assert s3(u3_neg) == Fraction(-1) and s7(u3_neg) == Fraction(0)
        assert s3(u7_pos) == Fraction(0) and s7(u7_pos) == Fraction(1)
        assert s3(u7_neg) == Fraction(0) and s7(u7_neg) == Fraction(-1)
        assert exotic_qi7(u7_pos) == Fraction(2, 3) and exotic_qi7(u7_neg) == Fraction(0)
        for c3, c7 in coeff_samples:
            assert exotic_comb_37(c3, c7, u3_pos) - exotic_comb_37(c3, c7, u3_neg) == Fraction(2, 3) * c3
            assert exotic_comb_37(c3, c7, u7_pos) - exotic_comb_37(c3, c7, u7_neg) == Fraction(2, 3) * c7

    # 5. Joint {3, 7}-even-valuation partner norms in Q(i, sqrt(3))^3 and Q(i, sqrt(7))^3
    #    (cross_prime_frame_partner_norm_valuations_even, joint_sqrt3_sqrt7_even_valuation_eliminates_combResidual37)
    for norm_s3 in (Fraction(3), Fraction(18)):
        assert v7_rat(norm_s3) == 0 and v7_rat(norm_s3) % 2 == 0
    for norm_s7 in (Fraction(7), Fraction(245)):
        assert v3_rat(norm_s7) == 0 and v3_rat(norm_s7) % 2 == 0
    assert v3_rat(Fraction(18)) == 2 and v7_rat(Fraction(18)) == 0
    assert v3_rat(Fraction(245)) == 0 and v7_rat(Fraction(245)) == 2
    assert v3_rat(Fraction(18)) % 2 == 0 and v7_rat(Fraction(18)) % 2 == 0
    assert v3_rat(Fraction(245)) % 2 == 0 and v7_rat(Fraction(245)) % 2 == 0

    # 6. Negative control: a residual that only vanishes on even-v3 vectors (e.g. c3=0, c7=1)
    #    vanishes on witness_111 and its Q(i, sqrt(3))^3 partners (norms 3, 18, 18 have v7 = 0),
    #    requiring the second extension Q(i, sqrt(7))^3 to eliminate c7!
    assert comb_residual_37(Fraction(0), Fraction(1), witness_111) == Fraction(0)
    assert comb_residual_37(Fraction(0), Fraction(1), witness_p7) == Fraction(1) != Fraction(0)


def test_uniform_sp_family_p11_and_finite_inert_residual_system() -> None:
    """Verify Subsection 9E: uniform prime-indexed sp family, p = 11 == 3 (mod 4) witness_p11 = (1, 3, 1), 3x3 Kronecker-delta duality, 7-ray projector kernel, Q(i, sqrt(11))^3 four-square frame, and m-prime InertPrimeResidualSystem theorems."""

    def gv(a: int, b: int, c: int, d: int, e: int, g: int) -> GVec:
        return GVec(
            GaussRat.of_ints(a, b),
            GaussRat.of_ints(c, d),
            GaussRat.of_ints(e, g),
        )

    witness_111 = gv(1, 0, 1, 0, 1, 0)
    witness_p7 = gv(1, 0, 2, 0, 1, 1)
    witness_p11 = gv(1, 0, 3, 0, 1, 0)

    # 1. Exact agreement sp(u, 3) == s3(u) and sp(u, 7) == s7(u) (sp_three_eq_s3, sp_seven_eq_s7)
    probe_vecs = [
         *NINE_RAYS,
        witness_111,
        witness_p7,
        witness_p11,
        gv(1, 2, 1, 2, 1, 1),
        gv(1, 4, 1, 2, 1, 1),
        gv(3, 0, -1, 0, 0, 0),
        gv(1, 0, 3, 0, -10, 0),
    ]
    for u in probe_vecs:
        assert sp(u, 3) == s3(u)
        assert sp(u, 7) == s7(u)
        for p in (3, 7, 11, 19, 23):
            assert sp(u, p) in (Fraction(-1), Fraction(0), Fraction(1))
            assert abs(sp(u, p)) <= Fraction(1)

    for p in (3, 7, 11, 19, 23):
        for ray in NINE_RAYS:
            assert sp(ray, p) == Fraction(0)

    def is_qr_mod_p(p: int, m: int) -> bool:
        return pow(m % p, (p - 1) // 2, p) == 1

    def check_inert_prime_spec(p: int) -> bool:
        if p < 3:
            return False
        for a in range(1, p):
            for b in range(1, p):
                if (a * b) % p == 0:
                    return False
                if is_qr_mod_p(p, a * b) != (is_qr_mod_p(p, a) == is_qr_mod_p(p, b)):
                    return False
                if (a + b) % p == 0 and is_qr_mod_p(p, a) != (not is_qr_mod_p(p, b)):
                    return False
        for x in range(p):
            for y in range(p):
                if (x * x + y * y) % p == 0 and (x != 0 or y != 0):
                    return False
        return True

    for p_inert in (3, 7, 11, 19, 23):
        assert check_inert_prime_spec(p_inert)
    for p_bad in (2, 4, 5, 9, 13, 15, 17):
        assert not check_inert_prime_spec(p_bad)

    # 2. Third inert prime p = 11 == 3 (mod 4): witness_p11 = (1, 3, 1) of norm 11
    #    and 3x3 Kronecker-delta duality (witness_p11_primitive, s3_s7_sp11_dual_on_three_witnesses)
    assert is_one_plus_i_primitive(1, 0, 3, 0, 1, 0)
    assert witness_p11.norm_sq() == Fraction(11)
    primes_3 = [3, 7, 11]
    witnesses_3 = [witness_111, witness_p7, witness_p11]
    for i, p_i in enumerate(primes_3):
        for j, w_j in enumerate(witnesses_3):
            assert sp(w_j, p_i) == (Fraction(1) if i == j else Fraction(0))

    # Verify odd-v11 orthogonal frame cancellation and scalar invariance for sp(u, 11)
    # (sp_orthogonal_odd_cancel, sp_isZeroWeightFrameFunction, sp_smul, sp11_isZeroWeightFrameFunction)
    for v11_ortho in (gv(3, 0, -1, 0, 0, 0), gv(1, 0, 0, 0, -1, 0), gv(3, 0, -2, 0, 3, 0)):
        w11 = herm_cross(witness_p11, v11_ortho)
        assert witness_p11.dot(v11_ortho) == GaussRat.of_ints(0, 0)
        assert (
            vp_rat(witness_p11.norm_sq(), 11)
            + vp_rat(v11_ortho.norm_sq(), 11)
            + vp_rat(w11.norm_sq(), 11)
        ) % 2 == 0
        assert sp(witness_p11, 11) + sp(v11_ortho, 11) + sp(w11, 11) == Fraction(0)
        for scalar in (GaussRat.of_ints(2, 3), GaussRat.of_ints(-1, 4)):
            scaled_w11 = GVec(scalar * witness_p11.x, scalar * witness_p11.y, scalar * witness_p11.z)
            assert sp(scaled_w11, 11) == sp(witness_p11, 11)

    # 3. Constructive 7-ray projector expansion for purely real witness_p11 = (1, 3, 1)
    #    (rayProj_witness_p11_decomp, quadRay_witness_p11_kernel_relation, sp11_witness_p11_kernel_separation)
    def witness_p11_kernel_eval(f) -> Fraction:
        return (
            f(witness_p11)
            + Fraction(3, 11) * f(E1)
            - Fraction(3, 11) * f(E2)
            + Fraction(3, 11) * f(E3)
            - Fraction(6, 11) * f(U12_PLUS)
            - Fraction(2, 11) * f(U13_PLUS)
            - Fraction(6, 11) * f(U23_PLUS)
        )

    p_wp11_rhs = herm_add(
        herm_add(
            herm_add(
                herm_smul(Fraction(-3, 11), ray_proj(E1)),
                herm_smul(Fraction(3, 11), ray_proj(E2)),
            ),
            herm_add(
                herm_smul(Fraction(-3, 11), ray_proj(E3)),
                herm_smul(Fraction(6, 11), ray_proj(U12_PLUS)),
            ),
        ),
        herm_add(
            herm_smul(Fraction(2, 11), ray_proj(U13_PLUS)),
            herm_smul(Fraction(6, 11), ray_proj(U23_PLUS)),
        ),
    )
    assert ray_proj(witness_p11) == p_wp11_rhs

    rho_sample = HermForm3(
        d1=Fraction(2, 5),
        d2=Fraction(1, 5),
        d3=Fraction(2, 5),
        a12=Fraction(1, 7),
        b12=Fraction(-1, 9),
        a13=Fraction(2, 11),
        b13=Fraction(-1, 13),
        a23=Fraction(1, 6),
        b23=Fraction(1, 8),
    )
    assert witness_p11_kernel_eval(lambda u: quad_ray(rho_sample, u)) == Fraction(0)
    assert witness_p11_kernel_eval(lambda u: sp(u, 11)) == Fraction(1)
    assert witness_p11_kernel_eval(s3) == Fraction(0)
    assert witness_p11_kernel_eval(s7) == Fraction(0)

    # 4. General m-prime finite combinations finCombResidual and finExoticComb
    #    (finExoticComb_isNonnegFrameFunction, inertPrimeResidualSystem_linearIndependent,
    #     finExoticComb_quadratic_iff, factorsThroughRayProjLinear_finCombResidual_iff)
    coeff_triples = [
        [Fraction(0), Fraction(0), Fraction(0)],
        [Fraction(1), Fraction(0), Fraction(0)],
        [Fraction(0), Fraction(1), Fraction(0)],
        [Fraction(0), Fraction(0), Fraction(1)],
        [Fraction(1, 4), Fraction(-1, 3), Fraction(5, 12)],
        [Fraction(-2, 9), Fraction(4, 9), Fraction(-1, 3)],
        [Fraction(1, 5), Fraction(2, 5), Fraction(-2, 5)],
    ]
    ortho_pairs_3 = [
        (E1, E2),
        (witness_111, gv(1, 0, -1, 0, 0, 0)),
        (witness_p7, gv(2, 0, -1, 0, 0, 0)),
        (witness_p11, gv(3, 0, -1, 0, 0, 0)),
        (witness_p11, gv(1, 0, 3, 0, -10, 0)),
    ]
    for c_vec in coeff_triples:
        assert sum(abs(c) for c in c_vec) <= Fraction(1)
        assert witness_p11_kernel_eval(lambda u: fin_comb_residual(primes_3, c_vec, u)) == c_vec[2]
        for ray in NINE_RAYS:
            assert fin_comb_residual(primes_3, c_vec, ray) == Fraction(0)
            assert fin_exotic_comb(primes_3, c_vec, ray) == Fraction(1, 3)
        for u, v in ortho_pairs_3:
            w = herm_cross(u, v)
            assert (
                fin_comb_residual(primes_3, c_vec, u)
                + fin_comb_residual(primes_3, c_vec, v)
                + fin_comb_residual(primes_3, c_vec, w)
                == Fraction(0)
            )
            assert (
                fin_exotic_comb(primes_3, c_vec, u)
                + fin_exotic_comb(primes_3, c_vec, v)
                + fin_exotic_comb(primes_3, c_vec, w)
                == Fraction(1)
            )
            for vec in (u, v, w):
                assert abs(fin_comb_residual(primes_3, c_vec, vec)) <= sum(abs(c) for c in c_vec)
                assert Fraction(0) <= fin_exotic_comb(primes_3, c_vec, vec) <= Fraction(2, 3)

        vanishes_on_all_three = all(
            fin_comb_residual(primes_3, c_vec, w_j) == Fraction(0) for w_j in witnesses_3
        )
        assert vanishes_on_all_three == all(c == Fraction(0) for c in c_vec)
        reconstructed = tomography_form(lambda u: fin_exotic_comb(primes_3, c_vec, u))
        assert reconstructed == herm_smul(Fraction(1, 3), HERM_ID)
        matches_reconstructed = all(
            fin_exotic_comb(primes_3, c_vec, w_j) == quad_ray(reconstructed, w_j)
            for w_j in witnesses_3
        )
        assert matches_reconstructed == all(c == Fraction(0) for c in c_vec)

    # 5. Selective 3-prime product-scaled oscillation near tomo_e1 = (1, 0, 0)
    #    (finCombResidual_coeffs_zero_of_archimedeanContinuousAt_tomo_e1,
    #     quadRay_add_finCombResidual_archimedeanContinuousAt_tomo_e1_iff,
    #     finExoticComb_archimedeanContinuousAt_tomo_e1_iff)
    for k in range(1, 8):
        inv231k = Fraction(1, 231 * k)
        u3_pos_11 = GVec(GaussRat.of_ints(1, 0), GaussRat(inv231k, Fraction(0)), GaussRat(inv231k, inv231k))
        u3_neg_11 = GVec(GaussRat.of_ints(1, 0), GaussRat(inv231k, inv231k), GaussRat(inv231k, Fraction(0)))
        u7_pos_11 = GVec(GaussRat.of_ints(1, 0), GaussRat(inv231k, inv231k), GaussRat(2 * inv231k, inv231k))
        u7_neg_11 = GVec(GaussRat.of_ints(1, 0), GaussRat(2 * inv231k, inv231k), GaussRat(inv231k, inv231k))
        u11_pos = GVec(GaussRat.of_ints(1, 0), GaussRat(3 * inv231k, Fraction(0)), GaussRat(inv231k, inv231k))
        u11_neg = GVec(GaussRat.of_ints(1, 0), GaussRat(inv231k, inv231k), GaussRat(3 * inv231k, Fraction(0)))

        assert [sp(u3_pos_11, p) for p in primes_3] == [Fraction(1), Fraction(0), Fraction(0)]
        assert [sp(u3_neg_11, p) for p in primes_3] == [Fraction(-1), Fraction(0), Fraction(0)]
        assert [sp(u7_pos_11, p) for p in primes_3] == [Fraction(0), Fraction(1), Fraction(0)]
        assert [sp(u7_neg_11, p) for p in primes_3] == [Fraction(0), Fraction(-1), Fraction(0)]
        assert [sp(u11_pos, p) for p in primes_3] == [Fraction(0), Fraction(0), Fraction(1)]
        assert [sp(u11_neg, p) for p in primes_3] == [Fraction(0), Fraction(0), Fraction(-1)]

        for c_vec in coeff_triples:
            assert (
                fin_exotic_comb(primes_3, c_vec, u3_pos_11)
                - fin_exotic_comb(primes_3, c_vec, u3_neg_11)
                == Fraction(2, 3) * c_vec[0]
            )
            assert (
                fin_exotic_comb(primes_3, c_vec, u7_pos_11)
                - fin_exotic_comb(primes_3, c_vec, u7_neg_11)
                == Fraction(2, 3) * c_vec[1]
            )
            assert (
                fin_exotic_comb(primes_3, c_vec, u11_pos)
                - fin_exotic_comb(primes_3, c_vec, u11_neg)
                == Fraction(2, 3) * c_vec[2]
            )

    # 6. Parameterized four-square SU(2) completion at p = 11 in Q(i, sqrt(11))^3
    #    matching isFrameSqrt11_witness_p11_norms and three_prime_frame_partner_norm_valuations_even
    v11_0 = gv(3, 0, -1, 0, 0, 0)  # norm 10
    w11_0 = gv(1, 0, 3, 0, -10, 0)  # norm 110
    alpha11 = GaussRat.of_ints(3, 0)
    beta11 = GaussRat.of_ints(1, 1)
    assert alpha11.norm_sq() + beta11.norm_sq() == Fraction(11)
    assert v11_0.norm_sq() == Fraction(10) and w11_0.norm_sq() == Fraction(110)
    partner_norm_11 = Fraction(1210)  # 10 * 11^2
    for norm_val in (Fraction(18), Fraction(245), partner_norm_11):
        for p in primes_3:
            assert vp_rat(norm_val, p) % 2 == 0
    assert vp_rat(partner_norm_11, 3) == 0
    assert vp_rat(partner_norm_11, 7) == 0
    assert vp_rat(partner_norm_11, 11) == 2


def test_independent_check_scripts_pass(tomography_mod, frame_functions_mod) -> None:
    """Run all three independent check scripts for FQ-GLEASON-QI3-FRAME-FUNCTIONS."""
    tomography_mod.main()
    frame_functions_mod.main()

    ext_proc = subprocess.run(
        [sys.executable, str(CHECKS_DIR / "fq-gleason-qi3-extension.py"), "--self-test"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert ext_proc.returncode == 0, ext_proc.stderr or ext_proc.stdout
    assert "Exact certificate: 0 = 32" in ext_proc.stdout
    assert "Negative control rejected: Boolean coordinate" in ext_proc.stdout


def test_fq_gleason_qi3_frame_functions_end_to_end() -> None:
    """Verify that Lean 4 formalization BornGaussianTomographyReduction.lean declares all required theorems."""
    assert LEAN_TOMOGRAPHY_FILE.is_file(), f"Missing {LEAN_TOMOGRAPHY_FILE}"
    content = LEAN_TOMOGRAPHY_FILE.read_text(encoding="utf-8")

    required_theorems = [
        "theorem inner_applyVec_im_zero",
        "theorem inner_applyVec_re_eq_quadNum",
        "theorem quadRay_smul",
        "theorem quadNum_orthogonal_weighted_sum",
        "theorem quadRay_frame_sum",
        "theorem quadRay_isFrameFunction",
        "theorem tomography_matches_nine_rays",
        "theorem tomography_trace_one",
        "theorem tomography_isFrameFunction",
        "theorem tomography_unique",
        "theorem tomographyForm_quadRay",
        "theorem residual_is_zero_weight",
        "theorem residual_vanishes_on_nine_rays",
        "theorem signed_rigidity_iff_zero_residual",
        "theorem nonneg_frameFunction_bounds",
        "theorem abs_quadRay_le",
        "theorem nonneg_residual_is_bounded",
        "theorem one_sided_lower_bound_implies_upper_bound",
        "theorem nonneg_rigidity_iff_bounded_zero_residual",
        "theorem gaussian_norm_div_four_witness",
        "theorem gaussian_norm_eight_primitive_witness",
        "theorem gaussian_coord_norm_mod_four",
        "theorem primitive_gaussian_norm_mod_four_iff",
        "theorem eq_quadRay_all_of_zero_at_zero",
        "theorem traceInner_self_eq_zero_iff",
        "theorem traceInner_ext",
        "theorem traceInner_rayProj",
        "theorem rayProj_smul",
        "theorem rayProj_tr",
        "theorem rayProj_frame_sum",
        "theorem rayProj_nine_rays_span_hermForm3",
        "theorem v3Rat_normSq_even",
        "theorem detGVec_normSq_of_frame",
        "theorem frame_v3Rat_sum_even",
        "theorem ortho_coord_identity_x",
        "theorem s3_orthogonal_odd_cancel",
        "theorem s3_isZeroWeightFrameFunction",
        "theorem s3_smul",
        "theorem s3_isBoundedOnRays",
        "theorem s3_vanishes_on_nine_rays",
        "theorem witness_111_primitive",
        "theorem witness_div_four_shell_primitive",
        "theorem witness_div_eight_shell_primitive",
        "theorem exists_nonzero_bounded_zero_residual",
        "theorem not_signed_quadratic_rigidity",
        "theorem not_nonneg_quadratic_rigidity",
        "theorem exoticQi3_isNonnegFrameFunction",
        "theorem exoticQi3_not_quadratic",
        "theorem rayProj_witness_111_decomp",
        "theorem quadRay_witness_111_kernel_relation",
        "theorem s3_witness_111_kernel_separation",
        "theorem s3_perturbPosRay",
        "theorem s3_perturbNegRay",
        "theorem distSqVec_perturbPosRay_tomo_e1",
        "theorem distSqVec_perturbNegRay_tomo_e1",
        "theorem s3_oscillates_near_tomo_e1",
        "theorem not_archimedeanContinuousAt_s3_tomo_e1",
        "theorem not_archimedeanContinuousAt_exoticQi3_tomo_e1",
        "theorem s3_coeff_zero_of_archimedeanContinuousAt_tomo_e1",
        "theorem archimedeanContinuousAt_quadRay_tomo_e1",
        "theorem quadRay_add_smul_s3_archimedeanContinuousAt_tomo_e1_iff",
        "theorem no_unit_norm_smul_witness_111_in_qi3",
        "theorem witness_111_unit_sqrt3_normSq",
        "theorem isFrameSqrt3_witness_111_even_norms",
        "theorem zero_on_witness_111_of_sqrt3_even_v3_vanishing",
        "theorem no_s3_even_v3_extension_to_sqrt3",
        "theorem unit_norm_in_sqrtP_of_normSqVec_eq",
        "theorem fourSquarePartner_ortho_and_normSqRatP",
        "theorem isFrameSqrt7_witness_p7_norms",
        "theorem zero_of_vanishesOnNineRays_and_factorsThroughRayProjLinear",
        "theorem not_factorsThroughRayProjLinear_s3",
        "theorem quadratic_rigidity_iff_factorsThroughRayProjLinear",
        "theorem v7Rat_normSq_even",
        "theorem frame_v7Rat_sum_even",
        "theorem s7_orthogonal_odd_cancel",
        "theorem s7_isZeroWeightFrameFunction",
        "theorem s7_smul",
        "theorem s7_isBoundedOnRays",
        "theorem s7_vanishes_on_nine_rays",
        "theorem witness_p7_primitive",
        "theorem s3_s7_dual_on_witnesses",
        "theorem exoticQi7_isNonnegFrameFunction",
        "theorem exoticQi7_not_quadratic",
        "theorem combResidual37_isZeroWeightFrameFunction",
        "theorem combResidual37_vanishes_on_nine_rays",
        "theorem combResidual37_isBoundedOnRays",
        "theorem s3_s7_linearIndependent",
        "theorem s7_perturb7PosRay",
        "theorem s7_perturb7NegRay",
        "theorem s3_perturb7PosRay",
        "theorem s3_perturb7NegRay",
        "theorem s7_perturbPosRay_seven_mul",
        "theorem s7_perturbNegRay_seven_mul",
        "theorem distSqVec_perturb7PosRay_tomo_e1",
        "theorem distSqVec_perturb7NegRay_tomo_e1",
        "theorem s3_s7_selective_oscillation_near_tomo_e1",
        "theorem not_archimedeanContinuousAt_s7_tomo_e1",
        "theorem not_archimedeanContinuousAt_exoticQi7_tomo_e1",
        "theorem combResidual37_coeffs_zero_of_archimedeanContinuousAt_tomo_e1",
        "theorem quadRay_add_combResidual37_archimedeanContinuousAt_tomo_e1_iff",
        "theorem no_unit_norm_smul_witness_p7_in_qi3",
        "theorem zero_on_witness_p7_of_sqrt7_even_v7_vanishing",
        "theorem no_s7_even_v7_extension_to_sqrt7",
        "theorem joint_sqrt3_sqrt7_even_valuation_eliminates_combResidual37",
        "theorem not_factorsThroughRayProjLinear_s7",
        "theorem factorsThroughRayProjLinear_combResidual37_iff",
        "theorem rayProj_witness_p7_decomp",
        "theorem quadRay_witness_p7_kernel_relation",
        "theorem s7_witness_p7_kernel_separation",
        "theorem cross_prime_frame_partner_norm_valuations_even",
        "theorem exoticComb37_isNonnegFrameFunction",
        "theorem exoticComb37_quadratic_iff",
        "theorem exoticComb37_archimedeanContinuousAt_tomo_e1_iff",
        "theorem sp_three_eq_s3",
        "theorem sp_seven_eq_s7",
        "theorem sp_isBoundedOnRays",
        "theorem sp_vanishes_on_nine_rays",
        "theorem inertPrimeSpec_eleven",
        "theorem vpRat_normSq_even",
        "theorem frame_vpRat_sum_even",
        "theorem sp_orthogonal_odd_cancel",
        "theorem sp_isZeroWeightFrameFunction",
        "theorem sp_smul",
        "theorem sp11_isZeroWeightFrameFunction",
        "theorem combResidual3_7_11_isZeroWeightFrameFunction",
        "theorem witness_p11_primitive",
        "theorem s3_s7_sp11_dual_on_three_witnesses",
        "theorem s3_s7_sp11_linearIndependent",
        "theorem factorsThroughRayProjLinear_combResidual3_7_11_iff",
        "theorem rayProj_witness_p11_decomp",
        "theorem quadRay_witness_p11_kernel_relation",
        "theorem sp11_witness_p11_kernel_separation",
        "theorem isFrameSqrt11_witness_p11_norms",
        "theorem three_prime_frame_partner_norm_valuations_even",
        "theorem finExoticComb_isNonnegFrameFunction",
        "theorem inertPrimeResidualSystem_linearIndependent",
        "theorem finExoticComb_quadratic_iff",
        "theorem finCombResidual_coeffs_zero_of_archimedeanContinuousAt_tomo_e1",
        "theorem quadRay_add_finCombResidual_archimedeanContinuousAt_tomo_e1_iff",
        "theorem finExoticComb_archimedeanContinuousAt_tomo_e1_iff",
        "theorem factorsThroughRayProjLinear_finCombResidual_iff",
        "theorem joint_field_extension_eliminates_finCombResidual",
        "theorem finCombResidual_inertSystem37_eq_combResidual37",
    ]
    for decl in required_theorems:
        assert decl in content, f"Missing declaration {decl!r} in {LEAN_TOMOGRAPHY_FILE}"


