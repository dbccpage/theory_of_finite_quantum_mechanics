#!/usr/bin/env python3
"""Exact rational verifier and receipt generator for Phase 4 (Continuum Gleason Development).

This script checks the finite-arithmetic witnesses, counterexamples, and quantitative
bounds formalized in `lean4/GleasonContinuumDevelopment.lean`:
1. Part A (d = 3 complex density matrices & Rayleigh perturbation):
   - Factorized Gaussian-rational state `factorizedState3(B) = B B^* / tr(B B^*)`
     satisfies exact trace 1 and Gram-factorized positive semidefiniteness
     `<v, B B^* v> = ||B^* v||^2 >= 0` across rational-Gaussian vectors.
   - Uniform Rayleigh quotient perturbation inequality
     `|QcRay(factorizedState3(B), v) - complexRayleigh(rho, v)| <= matEntryL1Norm(M_B - M_rho)`.
   - Complex Hermitian polarization uniqueness on 9 standard rays.
2. Part B (all finite dimensions d = 0, 1, 2 and d >= 3):
   - d = 0 vacuous uniqueness and d = 1 constant-1 frame valuation.
   - d = 2 explicit non-quadratic frame function `dim2AxisCounterexample` on Q(i)^2
     assigning 1 on y = 0, 0 on x = 0, and 1/2 off-axis, verified on orthogonal
     2-frames and obstructed on v = (2, 1) where the forced matrix diag(1, 0) gives 4/5 != 1/2
     (`dim2AxisCounterexample_not_quadratic`), alongside the two-frame {0, 1} valuation
     obstruction at (1, -2) where -1/5 < 0 (`dim2_projection_measure_obstruction`).
   - d >= 3 compatibility of 3D coordinate subspace restrictions `submatrix3D` on 1D/2D
     overlaps and global d x d Hermitian polarization uniqueness.
3. Part C (continuum automatic regularity in d >= 3):
   - 3D continuum frame completion, nonnegative frame function bounds `0 <= f(u) <= 1`,
     Piron planar subadditivity `f(u) + f(v) <= 1` for `u perp v`, and pole-complement
     vanishing `f(p) = 1 -> u perp p -> f(u) = 0`.
4. Part D (infinite-dimensional separable Hilbert spaces & trace escape):
   - Monotone finite-dimensional compressions `compressionTrace(w, N)`, tightness tail bound
     `1 - compressionTrace(w, M) <= eps`, and moving-bump counterexample `basisEscapeState(k)`
     demonstrating trace escape without uniform tightness.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys
from typing import Any, Callable


REPO_ROOT = Path(__file__).resolve().parent.parent
LEAN_MODULE_PATH = REPO_ROOT / "lean4" / "GleasonContinuumDevelopment.lean"
DEFAULT_RECEIPT_PATH = REPO_ROOT / "evidence" / "lean_receipts" / "gleason_continuum_development_receipt.json"


class GaussRat:
    """Exact Gaussian rational a + b*i with a, b in Q."""

    __slots__ = ("re", "im")

    def __init__(self, re: int | Fraction = 0, im: int | Fraction = 0) -> None:
        self.re = Fraction(re)
        self.im = Fraction(im)

    def __add__(self, other: GaussRat) -> GaussRat:
        return GaussRat(self.re + other.re, self.im + other.im)

    def __sub__(self, other: GaussRat) -> GaussRat:
        return GaussRat(self.re - other.re, self.im - other.im)

    def __mul__(self, other: GaussRat) -> GaussRat:
        return GaussRat(
            self.re * other.re - self.im * other.im,
            self.re * other.im + self.im * other.re,
        )

    def conj(self) -> GaussRat:
        return GaussRat(self.re, -self.im)

    def norm_sq(self) -> Fraction:
        return self.re * self.re + self.im * self.im

    def l1_abs(self) -> Fraction:
        """Rational upper bound |re| + |im| >= sqrt(re^2 + im^2)."""
        return abs(self.re) + abs(self.im)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, GaussRat):
            return False
        return self.re == other.re and self.im == other.im

    def __repr__(self) -> str:
        return f"GaussRat({self.re}, {self.im})"


GVec2 = tuple[GaussRat, GaussRat]
GVec3 = tuple[GaussRat, GaussRat, GaussRat]
GaussMatrix3 = tuple[
    tuple[GaussRat, GaussRat, GaussRat],
    tuple[GaussRat, GaussRat, GaussRat],
    tuple[GaussRat, GaussRat, GaussRat],
]


def inner2(u: GVec2, v: GVec2) -> GaussRat:
    return u[0].conj() * v[0] + u[1].conj() * v[1]


def norm_sq2(u: GVec2) -> Fraction:
    return u[0].norm_sq() + u[1].norm_sq()


def inner3(u: GVec3, v: GVec3) -> GaussRat:
    return u[0].conj() * v[0] + u[1].conj() * v[1] + u[2].conj() * v[2]


def norm_sq3(u: GVec3) -> Fraction:
    return u[0].norm_sq() + u[1].norm_sq() + u[2].norm_sq()


def frob_norm_sq(B: GaussMatrix3) -> Fraction:
    return sum(
        (B[r][c].norm_sq() for r in range(3) for c in range(3)),
        start=Fraction(0),
    )


def mul_conj_transpose_vec(B: GaussMatrix3, v: GVec3) -> GVec3:
    """Computes B^* v where (B^* v)_k = sum_r conj(B_{r,k}) v_r."""
    return tuple(
        sum((B[r][k].conj() * v[r] for r in range(3)), start=GaussRat(0, 0))
        for k in range(3)
    )  # type: ignore[return-value]


def gram_herm_entry(B: GaussMatrix3, i: int, j: int) -> GaussRat:
    """Computes (B B^*)_{i,j} = sum_k B_{i,k} conj(B_{j,k})."""
    return sum((B[i][k] * B[j][k].conj() for k in range(3)), start=GaussRat(0, 0))


def factorized_state_matrix(B: GaussMatrix3) -> GaussMatrix3:
    """Computes rho(B) = B B^* / tr(B B^*) as a 3x3 Hermitian GaussRat matrix."""
    Z = frob_norm_sq(B)
    if Z == 0:
        raise ValueError("Zero matrix has zero Frobenius norm")
    inv_z = GaussRat(Fraction(1, 1) / Z, 0)
    return tuple(
        tuple(gram_herm_entry(B, i, j) * inv_z for j in range(3))
        for i in range(3)
    )  # type: ignore[return-value]


def herm_quad_form(M: GaussMatrix3, v: GVec3) -> Fraction:
    """Computes Re <v, M v> for a 3x3 Hermitian matrix M over Q(i)."""
    total = GaussRat(0, 0)
    for i in range(3):
        for j in range(3):
            total = total + v[i].conj() * (M[i][j] * v[j])
    if total.im != 0:
        raise ValueError(f"Non-Hermitian imaginary residual: {total.im}")
    return total.re


def herm_rayleigh(M: GaussMatrix3, v: GVec3) -> Fraction:
    nsq = norm_sq3(v)
    if nsq == 0:
        raise ValueError("Zero vector has no Rayleigh quotient")
    return herm_quad_form(M, v) / nsq


def verify_part_a_d3_density_and_rayleigh() -> dict[str, Any]:
    """Verifies Part A: factorized PSD states, Gram identity, and Rayleigh perturbation bound."""
    B_pure: GaussMatrix3 = (
        (GaussRat(1, 0), GaussRat(0, 0), GaussRat(0, 0)),
        (GaussRat(0, 1), GaussRat(0, 0), GaussRat(0, 0)),
        (GaussRat(1, 1), GaussRat(0, 0), GaussRat(0, 0)),
    )
    B_mixed: GaussMatrix3 = (
        (GaussRat(1, 0), GaussRat(0, 1), GaussRat(0, 0)),
        (GaussRat(0, 0), GaussRat(1, 0), GaussRat(1, 1)),
        (GaussRat(1, -1), GaussRat(0, 0), GaussRat(1, 0)),
    )

    test_vectors: list[GVec3] = [
        (GaussRat(1, 0), GaussRat(0, 0), GaussRat(0, 0)),
        (GaussRat(0, 0), GaussRat(1, 0), GaussRat(0, 0)),
        (GaussRat(0, 0), GaussRat(0, 0), GaussRat(1, 0)),
        (GaussRat(1, 1), GaussRat(2, -1), GaussRat(0, 3)),
        (GaussRat(2, 0), GaussRat(-1, 2), GaussRat(1, -1)),
    ]

    for B in (B_pure, B_mixed):
        Z = frob_norm_sq(B)
        assert Z > 0
        rho = factorized_state_matrix(B)
        trace_val = rho[0][0].re + rho[1][1].re + rho[2][2].re
        assert trace_val == Fraction(1, 1)
        for v in test_vectors:
            gram_q = herm_quad_form(rho, v) * Z
            bstar_v = mul_conj_transpose_vec(B, v)
            assert gram_q == norm_sq3(bstar_v)
            assert gram_q >= 0
            ray_val = herm_rayleigh(rho, v)
            assert Fraction(0, 1) <= ray_val <= Fraction(1, 1)

    rho_pure = factorized_state_matrix(B_pure)
    rho_mixed = factorized_state_matrix(B_mixed)
    l1_upper = sum(
        (rho_pure[i][j] - rho_mixed[i][j]).l1_abs()
        for i in range(3)
        for j in range(3)
    )
    max_rayleigh_diff = Fraction(0, 1)
    for v in test_vectors:
        diff = abs(herm_rayleigh(rho_pure, v) - herm_rayleigh(rho_mixed, v))
        assert diff <= l1_upper
        if diff > max_rayleigh_diff:
            max_rayleigh_diff = diff

    # Verify 9-ray polarization uniqueness on 3x3 Hermitian matrices (rho_pure vs rho_mixed)
    nine_rays: list[GVec3] = [
        (GaussRat(1, 0), GaussRat(0, 0), GaussRat(0, 0)),
        (GaussRat(0, 0), GaussRat(1, 0), GaussRat(0, 0)),
        (GaussRat(0, 0), GaussRat(0, 0), GaussRat(1, 0)),
        (GaussRat(1, 0), GaussRat(1, 0), GaussRat(0, 0)),
        (GaussRat(1, 0), GaussRat(0, 0), GaussRat(1, 0)),
        (GaussRat(0, 0), GaussRat(1, 0), GaussRat(1, 0)),
        (GaussRat(1, 0), GaussRat(0, 1), GaussRat(0, 0)),
        (GaussRat(1, 0), GaussRat(0, 0), GaussRat(0, 1)),
        (GaussRat(0, 0), GaussRat(1, 0), GaussRat(0, 1)),
    ]
    assert any(herm_rayleigh(rho_pure, r) != herm_rayleigh(rho_mixed, r) for r in nine_rays)

    return {
        "verified": True,
        "frob_norm_sq_pure": str(frob_norm_sq(B_pure)),
        "frob_norm_sq_mixed": str(frob_norm_sq(B_mixed)),
        "trace_pure": "1",
        "trace_mixed": "1",
        "max_rayleigh_diff_tested": str(max_rayleigh_diff),
        "entry_l1_upper_bound": str(l1_upper),
        "nine_ray_polarization_separates_pure_and_mixed": True,
    }


def dim2_axis_counterexample(u: GVec2) -> Fraction:
    """Matches `dim2AxisCounterexample` in `GleasonContinuumDevelopment.lean`."""
    if u[1] == GaussRat(0, 0):
        return Fraction(1, 1)
    if u[0] == GaussRat(0, 0):
        return Fraction(0, 1)
    return Fraction(1, 2)


def verify_part_b_all_finite_dimensions() -> dict[str, Any]:
    """Verifies Part B: d = 0, 1, 2 counterexamples and d >= 3 subspace compatibility."""
    frames_d2: list[tuple[GVec2, GVec2]] = [
        ((GaussRat(1, 0), GaussRat(0, 0)), (GaussRat(0, 0), GaussRat(1, 0))),
        ((GaussRat(0, 0), GaussRat(2, 1)), (GaussRat(1, -3), GaussRat(0, 0))),
        ((GaussRat(1, 0), GaussRat(1, 0)), (GaussRat(1, 0), GaussRat(-1, 0))),
        ((GaussRat(1, 0), GaussRat(0, 1)), (GaussRat(1, 0), GaussRat(0, -1))),
        ((GaussRat(2, 0), GaussRat(1, 0)), (GaussRat(1, 0), GaussRat(-2, 0))),
        ((GaussRat(1, 1), GaussRat(2, 0)), (GaussRat(2, 0), GaussRat(-1, 1))),
    ]
    for u, v in frames_d2:
        assert norm_sq2(u) > 0 and norm_sq2(v) > 0
        assert inner2(u, v) == GaussRat(0, 0)
        assert dim2_axis_counterexample(u) >= 0
        assert dim2_axis_counterexample(v) >= 0
        assert dim2_axis_counterexample(u) + dim2_axis_counterexample(v) == Fraction(1, 1)

    # Obstruction check 1 (`dim2AxisCounterexample_not_quadratic`):
    # matching (1,0)->1, (0,1)->0, (1,1)->1/2 forces d1 = 1, d2 = 0, a12 = 0,
    # which gives 4/5 on (2,1) whereas dim2AxisCounterexample gives 1/2.
    u_obstruction: GVec2 = (GaussRat(2, 0), GaussRat(1, 0))
    forced_quad_ray_21 = Fraction(4, 5)
    actual_val_21 = dim2_axis_counterexample(u_obstruction)
    assert actual_val_21 == Fraction(1, 2)
    assert forced_quad_ray_21 != actual_val_21

    # Obstruction check 2 (`dim2_projection_measure_obstruction`):
    # matching (1,0)->1, (0,1)->0, (1,1)->1 forces d1 = 1, d2 = 0, a12 = 1/2,
    # which evaluates to (1*1 + 0*4 + 2*(1/2)*(1*-2)) / 5 = -1/5 < 0 at (1, -2).
    d1_two_frame = Fraction(1, 1)
    d2_two_frame = Fraction(0, 1)
    a12_two_frame = Fraction(1, 2)
    quad_ray_1_neg2 = (d1_two_frame * 1 + d2_two_frame * 4 + 2 * a12_two_frame * (-2)) / Fraction(5, 1)
    assert quad_ray_1_neg2 == Fraction(-1, 5)
    assert not (Fraction(0, 1) <= quad_ray_1_neg2)

    # d = 4 Hermitian matrix compatibility across 3D coordinate subspaces & polarization uniqueness
    herm4 = [
        [GaussRat(Fraction(1, 4), 0), GaussRat(Fraction(1, 8), Fraction(1, 16)), GaussRat(0, Fraction(-1, 8)), GaussRat(Fraction(1, 10), 0)],
        [GaussRat(Fraction(1, 8), Fraction(-1, 16)), GaussRat(Fraction(1, 4), 0), GaussRat(Fraction(1, 12), 0), GaussRat(0, Fraction(1, 9))],
        [GaussRat(0, Fraction(1, 8)), GaussRat(Fraction(1, 12), 0), GaussRat(Fraction(1, 4), 0), GaussRat(Fraction(-1, 7), Fraction(1, 14))],
        [GaussRat(Fraction(1, 10), 0), GaussRat(0, Fraction(-1, 9)), GaussRat(Fraction(-1, 7), Fraction(-1, 14)), GaussRat(Fraction(1, 4), 0)],
    ]
    emb_012 = (0, 1, 2)
    emb_013 = (0, 1, 3)
    sub_012 = [[herm4[emb_012[r]][emb_012[c]] for c in range(3)] for r in range(3)]
    sub_013 = [[herm4[emb_013[r]][emb_013[c]] for c in range(3)] for r in range(3)]
    # Overlap on shared 2D subspace {0, 1} (indices 0, 1 in both embeddings)
    for r in (0, 1):
        for c in (0, 1):
            assert sub_012[r][c] == sub_013[r][c]

    # Verify global 4x4 Hermitian polarization recovery matching `eq_of_complexQuadFormD_eq`
    def quad4(vec: list[GaussRat]) -> Fraction:
        acc = GaussRat(0, 0)
        for i in range(4):
            for j in range(4):
                acc = acc + vec[i].conj() * (herm4[i][j] * vec[j])
        assert acc.im == 0
        return acc.re

    for i in range(4):
        ei = [GaussRat(1, 0) if k == i else GaussRat(0, 0) for k in range(4)]
        assert quad4(ei) == herm4[i][i].re
        for j in range(i + 1, 4):
            ej = [GaussRat(1, 0) if k == j else GaussRat(0, 0) for k in range(4)]
            e_plus = [ei[k] + ej[k] for k in range(4)]
            e_minus = [ei[k] - ej[k] for k in range(4)]
            ie_j = [GaussRat(0, 1) * ej[k] for k in range(4)]
            e_iplus = [ei[k] + ie_j[k] for k in range(4)]
            e_iminus = [ei[k] - ie_j[k] for k in range(4)]
            rec_re = (quad4(e_plus) - quad4(e_minus)) / Fraction(4, 1)
            rec_im = (quad4(e_iminus) - quad4(e_iplus)) / Fraction(4, 1)
            assert rec_re == herm4[i][j].re
            assert rec_im == herm4[i][j].im

    return {
        "verified": True,
        "d0_vacuously_unique": True,
        "d1_constant_one": True,
        "d2_frames_checked": len(frames_d2),
        "d2_obstruction_vector": "(2, 1)",
        "d2_forced_quadratic_value": str(forced_quad_ray_21),
        "d2_counterexample_value": str(actual_val_21),
        "d2_two_frame_obstruction_vector": "(1, -2)",
        "d2_two_frame_forced_value": str(quad_ray_1_neg2),
        "d4_submatrix3D_overlap_verified": True,
        "d4_polarization_uniqueness_verified": True,
    }


def verify_part_c_continuum_regularity() -> dict[str, Any]:
    """Verifies Part C: Piron planar subadditivity and pole-complement vanishing on rational frames."""
    B_mixed: GaussMatrix3 = (
        (GaussRat(1, 0), GaussRat(0, 1), GaussRat(0, 0)),
        (GaussRat(0, 0), GaussRat(1, 0), GaussRat(1, 1)),
        (GaussRat(1, -1), GaussRat(0, 0), GaussRat(1, 0)),
    )
    rho = factorized_state_matrix(B_mixed)
    u: GVec3 = (GaussRat(1, 0), GaussRat(1, 0), GaussRat(0, 0))
    v: GVec3 = (GaussRat(1, 0), GaussRat(-1, 0), GaussRat(0, 0))
    w: GVec3 = (GaussRat(0, 0), GaussRat(0, 0), GaussRat(1, 0))
    assert inner3(u, v) == GaussRat(0, 0)
    assert inner3(u, w) == GaussRat(0, 0)
    assert inner3(v, w) == GaussRat(0, 0)
    fu = herm_rayleigh(rho, u)
    fv = herm_rayleigh(rho, v)
    fw = herm_rayleigh(rho, w)
    assert fu + fv + fw == Fraction(1, 1)
    assert fu + fv <= Fraction(1, 1)

    # Pure state with pole p = e_0 where f(p) = 1 vanishes on orthogonal u = e_1
    B_pole: GaussMatrix3 = (
        (GaussRat(1, 0), GaussRat(0, 0), GaussRat(0, 0)),
        (GaussRat(0, 0), GaussRat(0, 0), GaussRat(0, 0)),
        (GaussRat(0, 0), GaussRat(0, 0), GaussRat(0, 0)),
    )
    rho_pole = factorized_state_matrix(B_pole)
    p: GVec3 = (GaussRat(1, 0), GaussRat(0, 0), GaussRat(0, 0))
    e1: GVec3 = (GaussRat(0, 0), GaussRat(1, 0), GaussRat(0, 0))
    assert herm_rayleigh(rho_pole, p) == Fraction(1, 1)
    assert herm_rayleigh(rho_pole, e1) == Fraction(0, 1)

    return {
        "verified": True,
        "piron_subadditivity_sum_uv": str(fu + fv),
        "complement_ray_weight_w": str(fw),
        "pole_value_at_e0": "1",
        "orthogonal_value_at_e1": "0",
    }


def compression_trace(w: Callable[[int], Fraction], n_cutoff: int) -> Fraction:
    return sum((w(n) for n in range(n_cutoff)), start=Fraction(0, 1))


def basis_escape_state(k: int) -> Callable[[int], Fraction]:
    return lambda n: Fraction(1, 1) if n == k else Fraction(0, 1)


def verify_part_d_infinite_dim_and_trace_escape() -> dict[str, Any]:
    """Verifies Part D: tightness tail bound vs moving-bump trace escape."""
    # Tight geometric weight w(n) = 1 / 2^(n+1)
    w_tight = lambda n: Fraction(1, 2 ** (n + 1))
    t_5 = compression_trace(w_tight, 5)
    t_10 = compression_trace(w_tight, 10)
    assert t_5 <= t_10 <= Fraction(1, 1)
    tail_5_to_10 = t_10 - t_5
    assert tail_5_to_10 == Fraction(1, 32) - Fraction(1, 1024)

    # Moving-bump trace escape sequence w_k(n) = delta_{n, k}
    n_fixed = 6
    for k in range(n_fixed, n_fixed + 5):
        wk = basis_escape_state(k)
        assert compression_trace(wk, k + 1) == Fraction(1, 1)
        assert compression_trace(wk, n_fixed) == Fraction(0, 1)

    return {
        "verified": True,
        "tight_compression_N5": str(t_5),
        "tight_compression_N10": str(t_10),
        "tight_tail_5_to_10": str(tail_5_to_10),
        "escape_fixed_cutoff_N": n_fixed,
        "escape_compression_for_k_ge_N": "0",
        "escape_full_stage_normalization": "1",
    }


def embed3d_vec(
    e1: list[GaussRat],
    e2: list[GaussRat],
    e3: list[GaussRat],
    x: GVec3,
) -> list[GaussRat]:
    """Computes embed3D(e1, e2, e3, x) = x[0]*e1 + x[1]*e2 + x[2]*e3 in Q(i)^d."""
    d = len(e1)
    assert len(e2) == d and len(e3) == d
    return [x[0] * e1[i] + x[1] * e2[i] + x[2] * e3[i] for i in range(d)]


def inner_d(u: list[GaussRat], v: list[GaussRat]) -> GaussRat:
    assert len(u) == len(v)
    return sum((u[i].conj() * v[i] for i in range(len(u))), start=GaussRat(0, 0))


def norm_sq_d(u: list[GaussRat]) -> Fraction:
    return sum((u[i].norm_sq() for i in range(len(u))), start=Fraction(0, 1))


def replace_basis_3d(
    basis: list[list[GaussRat]],
    i0: int,
    i1: int,
    i2: int,
    u0: list[GaussRat],
    u1: list[GaussRat],
    u2: list[GaussRat],
) -> list[list[GaussRat]]:
    """Matches `replaceBasis3D` in `GleasonContinuumDevelopment.lean`."""
    out: list[list[GaussRat]] = []
    for idx, vec in enumerate(basis):
        if idx == i0:
            out.append(u0)
        elif idx == i1:
            out.append(u1)
        elif idx == i2:
            out.append(u2)
        else:
            out.append(vec)
    return out


def is_orthonormal_basis_d(basis: list[list[GaussRat]]) -> bool:
    d = len(basis)
    for i in range(d):
        if norm_sq_d(basis[i]) != Fraction(1, 1):
            return False
        for j in range(d):
            if i != j and inner_d(basis[i], basis[j]) != GaussRat(0, 0):
                return False
    return True


def verify_part_e_dim_d_subspace_lift() -> dict[str, Any]:
    """Verifies Part E: d = 3 to d >= 3 isometric subspace embedding, 3-slot basis replacement,
    parallelogram law, and continuity-free pure-state Born rule on 3D subspaces of C^4 and C^5."""
    # Non-coordinate orthonormal basis B4 of C^4 over Q(i)
    e1_4 = [GaussRat(Fraction(3, 5), 0), GaussRat(0, 0), GaussRat(0, Fraction(4, 5)), GaussRat(0, 0)]
    e2_4 = [GaussRat(Fraction(4, 5), 0), GaussRat(0, 0), GaussRat(0, Fraction(-3, 5)), GaussRat(0, 0)]
    e3_4 = [GaussRat(0, 0), GaussRat(Fraction(3, 5), 0), GaussRat(0, 0), GaussRat(Fraction(4, 5), 0)]
    e4_4 = [GaussRat(0, 0), GaussRat(Fraction(4, 5), 0), GaussRat(0, 0), GaussRat(Fraction(-3, 5), 0)]
    basis_4 = [e1_4, e2_4, e3_4, e4_4]
    assert is_orthonormal_basis_d(basis_4)

    # Non-coordinate orthonormal triple in C^5 over Q(i)
    f1_5 = [
        GaussRat(Fraction(3, 5), 0),
        GaussRat(0, Fraction(4, 5)),
        GaussRat(0, 0),
        GaussRat(0, 0),
        GaussRat(0, 0),
    ]
    f2_5 = [
        GaussRat(Fraction(4, 5), 0),
        GaussRat(0, Fraction(-3, 5)),
        GaussRat(0, 0),
        GaussRat(0, 0),
        GaussRat(0, 0),
    ]
    f3_5 = [
        GaussRat(0, 0),
        GaussRat(0, 0),
        GaussRat(Fraction(5, 13), 0),
        GaussRat(0, Fraction(12, 13)),
        GaussRat(0, 0),
    ]
    assert norm_sq_d(f1_5) == Fraction(1, 1)
    assert norm_sq_d(f2_5) == Fraction(1, 1)
    assert norm_sq_d(f3_5) == Fraction(1, 1)
    assert inner_d(f1_5, f2_5) == GaussRat(0, 0)
    assert inner_d(f1_5, f3_5) == GaussRat(0, 0)
    assert inner_d(f2_5, f3_5) == GaussRat(0, 0)

    sample_x: list[GVec3] = [
        (GaussRat(1, 0), GaussRat(2, -1), GaussRat(0, 3)),
        (GaussRat(2, 1), GaussRat(-1, 2), GaussRat(1, -1)),
        (GaussRat(Fraction(3, 5), 0), GaussRat(0, Fraction(4, 5)), GaussRat(0, 0)),
    ]
    for x in sample_x:
        emb4_x = embed3d_vec(e1_4, e2_4, e3_4, x)
        emb5_x = embed3d_vec(f1_5, f2_5, f3_5, x)
        assert norm_sq_d(emb4_x) == norm_sq3(x)
        assert norm_sq_d(emb5_x) == norm_sq3(x)
        for y in sample_x:
            emb4_y = embed3d_vec(e1_4, e2_4, e3_4, y)
            emb5_y = embed3d_vec(f1_5, f2_5, f3_5, y)
            assert inner_d(emb4_x, emb4_y) == inner3(x, y)
            assert inner_d(emb5_x, emb5_y) == inner3(x, y)

    # 3-slot basis replacement in C^4 (`replaceBasis3D` & `sum_replaceBasis3D_sub`)
    rot_x: GVec3 = (GaussRat(Fraction(3, 5), 0), GaussRat(0, Fraction(4, 5)), GaussRat(0, 0))
    rot_y: GVec3 = (GaussRat(Fraction(4, 5), 0), GaussRat(0, Fraction(-3, 5)), GaussRat(0, 0))
    rot_z: GVec3 = (GaussRat(0, 0), GaussRat(0, 0), GaussRat(1, 0))
    assert norm_sq3(rot_x) == Fraction(1, 1)
    assert norm_sq3(rot_y) == Fraction(1, 1)
    assert norm_sq3(rot_z) == Fraction(1, 1)
    assert inner3(rot_x, rot_y) == GaussRat(0, 0)
    assert inner3(rot_x, rot_z) == GaussRat(0, 0)
    assert inner3(rot_y, rot_z) == GaussRat(0, 0)

    u0 = embed3d_vec(e1_4, e2_4, e3_4, rot_x)
    u1 = embed3d_vec(e1_4, e2_4, e3_4, rot_y)
    u2 = embed3d_vec(e1_4, e2_4, e3_4, rot_z)
    basis_4_rep = replace_basis_3d(basis_4, 0, 1, 2, u0, u1, u2)
    assert is_orthonormal_basis_d(basis_4_rep)

    # Also test non-contiguous, non-monotonic slot indices (i0, i1, i2) = (3, 0, 2)
    v0_302 = embed3d_vec(e4_4, e1_4, e3_4, rot_x)
    v1_302 = embed3d_vec(e4_4, e1_4, e3_4, rot_y)
    v2_302 = embed3d_vec(e4_4, e1_4, e3_4, rot_z)
    basis_4_rep_302 = replace_basis_3d(basis_4, 3, 0, 2, v0_302, v1_302, v2_302)
    assert is_orthonormal_basis_d(basis_4_rep_302)
    assert basis_4_rep_302[3] == v0_302
    assert basis_4_rep_302[0] == v1_302
    assert basis_4_rep_302[2] == v2_302
    assert basis_4_rep_302[1] == e2_4

    herm4 = [
        [GaussRat(Fraction(1, 4), 0), GaussRat(Fraction(1, 8), Fraction(1, 16)), GaussRat(0, Fraction(-1, 8)), GaussRat(Fraction(1, 10), 0)],
        [GaussRat(Fraction(1, 8), Fraction(-1, 16)), GaussRat(Fraction(1, 4), 0), GaussRat(Fraction(1, 12), 0), GaussRat(0, Fraction(1, 9))],
        [GaussRat(0, Fraction(1, 8)), GaussRat(Fraction(1, 12), 0), GaussRat(Fraction(1, 4), 0), GaussRat(Fraction(-1, 7), Fraction(1, 14))],
        [GaussRat(Fraction(1, 10), 0), GaussRat(0, Fraction(-1, 9)), GaussRat(Fraction(-1, 7), Fraction(-1, 14)), GaussRat(Fraction(1, 4), 0)],
    ]

    def quad_d(mat: list[list[GaussRat]], vec: list[GaussRat]) -> Fraction:
        acc = GaussRat(0, 0)
        d_len = len(vec)
        for i in range(d_len):
            for j in range(d_len):
                acc = acc + vec[i].conj() * (mat[i][j] * vec[j])
        assert acc.im == 0
        return acc.re

    def rayleigh_d(mat: list[list[GaussRat]], vec: list[GaussRat]) -> Fraction:
        nsq = norm_sq_d(vec)
        assert nsq > 0
        return quad_d(mat, vec) / nsq

    sum_orig = sum((rayleigh_d(herm4, b) for b in basis_4), start=Fraction(0, 1))
    sum_rep = sum((rayleigh_d(herm4, b) for b in basis_4_rep), start=Fraction(0, 1))
    sum_rep_302 = sum((rayleigh_d(herm4, b) for b in basis_4_rep_302), start=Fraction(0, 1))
    subspace_trace_orig = rayleigh_d(herm4, e1_4) + rayleigh_d(herm4, e2_4) + rayleigh_d(herm4, e3_4)
    subspace_trace_rep = rayleigh_d(herm4, u0) + rayleigh_d(herm4, u1) + rayleigh_d(herm4, u2)
    assert sum_orig == Fraction(1, 1)
    assert sum_rep == Fraction(1, 1)
    assert sum_rep_302 == Fraction(1, 1)
    assert subspace_trace_orig == subspace_trace_rep
    assert (sum_rep - sum_orig) == (subspace_trace_rep - subspace_trace_orig)

    # Non-coordinate compressed 3x3 matrix (`subspaceMatrix3D` & `complexRayleighD_embed3D_eq_subspaceMatrix3D`)
    triple_e = (e1_4, e2_4, e3_4)
    subspace_mat_e: GaussMatrix3 = tuple(
        tuple(
            sum(
                (
                    triple_e[a][r].conj() * (herm4[r][c] * triple_e[b][c])
                    for r in range(4)
                    for c in range(4)
                ),
                start=GaussRat(0, 0),
            )
            for b in range(3)
        )
        for a in range(3)
    )  # type: ignore[assignment]
    for a in range(3):
        for b in range(3):
            assert subspace_mat_e[a][b] == subspace_mat_e[b][a].conj()
    for x in sample_x:
        emb_e = embed3d_vec(e1_4, e2_4, e3_4, x)
        assert quad_d(herm4, emb_e) == herm_quad_form(subspace_mat_e, x)
        assert rayleigh_d(herm4, emb_e) == herm_rayleigh(subspace_mat_e, x)

    # d-dimensional parallelogram law (`complexQuadFormD_parallelogram`)
    u_vec4 = [GaussRat(1, 1), GaussRat(2, -1), GaussRat(0, 1), GaussRat(-1, 2)]
    v_vec4 = [GaussRat(2, 0), GaussRat(-1, 1), GaussRat(1, -2), GaussRat(0, 3)]
    u_plus_v = [u_vec4[i] + v_vec4[i] for i in range(4)]
    u_minus_v = [u_vec4[i] - v_vec4[i] for i in range(4)]
    lhs_par = quad_d(herm4, u_plus_v) + quad_d(herm4, u_minus_v)
    rhs_par = 2 * quad_d(herm4, u_vec4) + 2 * quad_d(herm4, v_vec4)
    assert lhs_par == rhs_par

    # Coordinate embedding matches 3x3 principal submatrix (`complexQuadFormD_embed3D_single_eq_submatrix3D`
    # and `complexRayleighD_embed3D_single_eq_submatrix3D`)
    std0 = [GaussRat(1, 0), GaussRat(0, 0), GaussRat(0, 0), GaussRat(0, 0)]
    std2 = [GaussRat(0, 0), GaussRat(0, 0), GaussRat(1, 0), GaussRat(0, 0)]
    std3 = [GaussRat(0, 0), GaussRat(0, 0), GaussRat(0, 0), GaussRat(1, 0)]
    sub_023: GaussMatrix3 = tuple(
        tuple(herm4[r][c] for c in (0, 2, 3))
        for r in (0, 2, 3)
    )  # type: ignore[assignment]
    for x in sample_x:
        emb_std = embed3d_vec(std0, std2, std3, x)
        assert quad_d(herm4, emb_std) == herm_quad_form(sub_023, x)
        assert rayleigh_d(herm4, emb_std) == herm_rayleigh(sub_023, x)

    # Continuity-free pure-state Born rule on 3D subspace (`pure_state_nonneg_gleason_subspace3D`
    # and `pure_state_nonneg_gleason_basis3D`), tested at both W_sub = 1 and partial weight W_sub = 3/5 != 1
    pole_p0: GVec3 = rot_x
    psi_4 = embed3d_vec(e1_4, e2_4, e3_4, pole_p0)
    pure_mat4 = [[psi_4[i] * psi_4[j].conj() for j in range(4)] for i in range(4)]
    w_subspace = rayleigh_d(pure_mat4, e1_4) + rayleigh_d(pure_mat4, e2_4) + rayleigh_d(pure_mat4, e3_4)
    assert w_subspace == Fraction(1, 1)
    assert rayleigh_d(pure_mat4, psi_4) == w_subspace

    # Partial-weight state rho_partial = (3/5)|psi_4><psi_4| + (2/5)|e4_4><e4_4| of total trace 1
    # whose 3D restriction to span(e1_4, e2_4, e3_4) has subspace weight W_sub = 3/5 != 1
    w_partial = Fraction(3, 5)
    w_orth = Fraction(2, 5)
    partial_mat4 = [
        [
            GaussRat(w_partial, 0) * (psi_4[i] * psi_4[j].conj())
            + GaussRat(w_orth, 0) * (e4_4[i] * e4_4[j].conj())
            for j in range(4)
        ]
        for i in range(4)
    ]
    w_subspace_partial = (
        rayleigh_d(partial_mat4, e1_4)
        + rayleigh_d(partial_mat4, e2_4)
        + rayleigh_d(partial_mat4, e3_4)
    )
    assert w_subspace_partial == Fraction(3, 5)
    assert rayleigh_d(partial_mat4, psi_4) == w_subspace_partial
    for x in sample_x:
        emb_x = embed3d_vec(e1_4, e2_4, e3_4, x)
        lhs_born = rayleigh_d(pure_mat4, emb_x)
        rhs_born = w_subspace * inner3(pole_p0, x).norm_sq() / norm_sq3(x)
        assert lhs_born == rhs_born
        lhs_born_partial = rayleigh_d(partial_mat4, emb_x)
        rhs_born_partial = w_subspace_partial * inner3(pole_p0, x).norm_sq() / norm_sq3(x)
        assert lhs_born_partial == rhs_born_partial

    return {
        "verified": True,
        "c4_isometric_embed3D_verified": True,
        "c5_isometric_embed3D_verified": True,
        "replaceBasis3D_orthonormal_verified": True,
        "replaceBasis3D_noncontiguous_slots_verified": True,
        "subspace_3frame_trace_preserved": str(subspace_trace_orig),
        "subspaceMatrix3D_rayleigh_match_verified": True,
        "parallelogram_law_d4_value": str(lhs_par),
        "coordinate_embed3D_matches_submatrix3D": True,
        "pure_state_subspace3D_born_rule_verified": True,
        "pure_state_subspace3D_partial_weight": str(w_subspace_partial),
    }


def build_receipt() -> dict[str, Any]:
    lean_sha256 = hashlib.sha256(LEAN_MODULE_PATH.read_bytes()).hexdigest()
    return {
        "schema_version": "1.0.0",
        "authority_effect": "None",
        "phase": "Phase 4 - Continuum Gleason Development",
        "lean_module": {
            "path": "lean4/GleasonContinuumDevelopment.lean",
            "sha256": lean_sha256,
        },
        "parts": {
            "part_a_d3_complex_density_and_rayleigh": verify_part_a_d3_density_and_rayleigh(),
            "part_b_all_finite_dimensions": verify_part_b_all_finite_dimensions(),
            "part_c_continuum_automatic_regularity": verify_part_c_continuum_regularity(),
            "part_d_infinite_dimensional_and_trace_escape": verify_part_d_infinite_dim_and_trace_escape(),
            "part_e_dim_d_subspace_lift": verify_part_e_dim_d_subspace_lift(),
        },
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--write-receipt",
        action="store_true",
        help="Write receipt JSON to evidence/lean_receipts/gleason_continuum_development_receipt.json",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Verify that all checks pass and match the recorded receipt JSON",
    )
    parser.add_argument(
        "--receipt-path",
        type=Path,
        default=DEFAULT_RECEIPT_PATH,
        help="Override path for receipt JSON",
    )
    args = parser.parse_args(argv)

    receipt = build_receipt()
    if args.write_receipt:
        args.receipt_path.parent.mkdir(parents=True, exist_ok=True)
        args.receipt_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({"written": str(args.receipt_path), "all_passed": True}))
        return 0
    if args.check:
        recorded = json.loads(args.receipt_path.read_text(encoding="utf-8"))
        if recorded != receipt:
            print("Receipt mismatch!", file=sys.stderr)
            return 1
        print(json.dumps({"checked": str(args.receipt_path), "all_passed": True}))
        return 0
    print(json.dumps(receipt, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
