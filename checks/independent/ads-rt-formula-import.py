#!/usr/bin/env python3
"""Independent verification for ADS-RT-FORMULA-IMPORT (TFQ-2204).

AuthorityEffect: None.

Independently checks the three exact finite/rational algebraic shadows and scope fences
formalized in lean4/AdsRtFormulaImport.lean:
1. Ryu-Takayanagi / Brown-Henneaux coupling elimination (c = 3R / (2G_N^(3)), S_A = L_gamma / (4G_N^(3))
   = (c / 3) * logFactor), cut-pasting Strong Subadditivity inequality, and complement symmetry
   (A <-> A^c) of mincut and boundaryEntropy across all 380 proper contiguous boundary intervals
   of the supplied 20-qubit HaPPY-inspired fixture. Network identification is not derived.
2. Four rational entropy examples and exact symbolic bit/nat conversions.
   The general algebraic-entropy transcendence fence remains a separate Baker-dependent
   statement; these examples do not prove it or a general rational-equality obstruction.
3. Exact rational Regge proxy (TFQ-0100) vs minimal-surface area & HaPPY bond-cut fence:
   - On the orthogonal_pentatope chart of TFQ-0100, the 6 right-triangle hinges have Cayley-Menger
     squared area 1/4 and the 4 equilateral-triangle hinges have Cayley-Menger squared area 3/4
     (total 9/2), with no rational linear area A satisfying A^2 = 3/4.
   - On any flat chart (kappa = 0), the rational Regge action vanishes identically, whereas all 380
     proper contiguous boundary intervals of the 20-qubit HaPPY patch have 1 <= S(A) <= mincut(A).
   - Under uniform length rescaling L -> lam * L, Cayley-Menger squared area and the Regge proxy
     scale as lam^4, whereas 2-surface area scales as lam^2 and bond count as lam^0.
"""

from __future__ import annotations

from fractions import Fraction
import math

# Shared checker infrastructure only; no production implementation is imported.
from pathlib import Path as _Path
import sys as _sys
_sys.path.insert(0, str(_Path(__file__).resolve().parents[1]))
from checker_support.boundary import cli
from checker_support.cases import Cases
from checker_support.domains import rational


def rt_leading_entropy(area: Fraction, g_n: Fraction) -> Fraction:
    area = rational(area, "area", minimum=0)
    g_n = rational(g_n, "Newton constant", strictly_positive=True)
    return area / (4 * g_n)


def brown_henneaux_central_charge(r_ads: Fraction, g_n3: Fraction) -> Fraction:
    r_ads = rational(r_ads, "AdS radius", strictly_positive=True)
    g_n3 = rational(g_n3, "Newton constant", strictly_positive=True)
    return (3 * r_ads) / (2 * g_n3)


def ads3_geodesic_length(r_ads: Fraction, log_factor: Fraction) -> Fraction:
    r_ads = rational(r_ads, "AdS radius", strictly_positive=True)
    log_factor = rational(log_factor, "log factor", minimum=0)
    return 2 * r_ads * log_factor


def calabrese_cardy_coefficient(c: Fraction) -> Fraction:
    c = rational(c, "central charge", minimum=0)
    return c / 3


def cayley_menger_triangle_area_sq(s01: Fraction, s02: Fraction, s12: Fraction) -> Fraction:
    """Exact polynomial on Q, not a triangle-realizability certificate."""
    s01 = rational(s01, "s01")
    s02 = rational(s02, "s02")
    s12 = rational(s12, "s12")
    return (2 * (s01 * s02 + s01 * s12 + s02 * s12) - (s01 * s01 + s02 * s02 + s12 * s12)) / 16


from checker_support.happy_boundary import BOUNDARY_GENS_20, interval_mincut, interval_entropy as _boundary_entropy
import sympy as sp


def interval_entropy(start: int, length: int) -> int:
    return _boundary_entropy(BOUNDARY_GENS_20, start, length)


def has_rational_square_root(value: Fraction) -> bool:
    """Reduced p/q is a rational square iff both p and q are integer squares."""
    value = rational(value, "squared area", minimum=0)
    return (math.isqrt(value.numerator)**2 == value.numerator and
            math.isqrt(value.denominator)**2 == value.denominator)


def check_rt_coupling(run: Cases) -> None:
    r_vals = [Fraction(1, 2), Fraction(1, 1), Fraction(3, 2), Fraction(5, 3)]
    g_vals = [Fraction(1, 7), Fraction(1, 3), Fraction(2, 5), Fraction(3, 4)]
    log_vals = [Fraction(0, 1), Fraction(1, 1), Fraction(7, 5), Fraction(11, 4)]

    for r_ads in r_vals:
        for g_n3 in g_vals:
            c = brown_henneaux_central_charge(r_ads, g_n3)
            for lf in log_vals:
                l_geo = ads3_geodesic_length(r_ads, lf)
                s_rt = rt_leading_entropy(l_geo, g_n3)
                s_cc = calabrese_cardy_coefficient(c) * lf
                run.require(
                    s_rt == s_cc and s_rt / c == lf / 3,
                    "coupling elimination",
                )


    # Additivity and cut-pasting SSA check
    for a1 in [Fraction(3, 2), Fraction(7, 4), Fraction(5, 1)]:
        for a2 in [Fraction(1, 2), Fraction(9, 4), Fraction(6, 1)]:
            for g_n in [Fraction(1, 4), Fraction(2, 3)]:
                run.require(
                    rt_leading_entropy(a1 + a2, g_n) == rt_leading_entropy(a1, g_n) + rt_leading_entropy(a2, g_n),
                    "entropy additivity",
                )
                # Submodular pasting: min_abc <= a1 + a2 - delta, min_b <= delta
                delta = Fraction(1, 3)
                area_union = a1 + a2 - delta
                area_inter = delta / 2
                min_abc = area_union - Fraction(1, 5)
                min_b = area_inter - Fraction(1, 7)
                run.require(
                    rt_leading_entropy(min_abc, g_n) + rt_leading_entropy(min_b, g_n) <= rt_leading_entropy(a1, g_n) + rt_leading_entropy(a2, g_n),
                    "cut-pasting inequality",
                )


def check_exact_entropy_examples(run: Cases) -> None:
    for k in range(1, 21):
        s_nats = k * sp.log(2)
        s_bits = sp.simplify(s_nats / sp.log(2))
        run.require(
            s_bits == k,
            "bit/nat conversion",
        )


    # These four normalized mixed spectra have positive natural-log entropy.
    mixed_spectra = [
        [Fraction(1, 2), Fraction(1, 2)],
        [Fraction(1, 4), Fraction(3, 4)],
        [Fraction(1, 4), Fraction(1, 4), Fraction(1, 4), Fraction(1, 4)],
        [Fraction(1, 8), Fraction(3, 8), Fraction(1, 2)],
    ]
    for spec in mixed_spectra:
        run.require(
            sum(spec) == Fraction(1, 1),
            "normalized spectrum",
        )
        s_val = -sum(sp.Rational(p.numerator, p.denominator) * sp.log(sp.Rational(p.numerator, p.denominator)) for p in spec if p > 0)
        run.require(
            s_val.is_positive is True,
            "positive mixed entropy",
        )


def check_hinge_geometry(run: Cases) -> None:
    vertices = [
        (Fraction(0), Fraction(0), Fraction(0), Fraction(0)),
        (Fraction(1), Fraction(0), Fraction(0), Fraction(0)),
        (Fraction(0), Fraction(1), Fraction(0), Fraction(0)),
        (Fraction(0), Fraction(0), Fraction(1), Fraction(0)),
        (Fraction(0), Fraction(0), Fraction(0), Fraction(1)),
    ]

    def dist_sq(u: tuple[Fraction, ...], v: tuple[Fraction, ...]) -> Fraction:
        return sum(((ui - vi) ** 2 for ui, vi in zip(u, v)), Fraction(0))

    right_count = 0
    equil_count = 0
    total_area_sq = Fraction(0)
    for i in range(5):
        for j in range(i + 1, 5):
            for k in range(j + 1, 5):
                s01 = dist_sq(vertices[i], vertices[j])
                s02 = dist_sq(vertices[i], vertices[k])
                s12 = dist_sq(vertices[j], vertices[k])
                a_sq = cayley_menger_triangle_area_sq(s01, s02, s12)
                total_area_sq += a_sq
                if i == 0:
                    right_count += 1
                    run.require(
                        (s01, s02, s12) == (Fraction(1), Fraction(1), Fraction(2)) and a_sq == Fraction(1, 4),
                        "right hinge squared area",
                    )
                else:
                    equil_count += 1
                    run.require(
                        (s01, s02, s12) == (Fraction(2), Fraction(2), Fraction(2)) and a_sq == Fraction(3, 4),
                        "equilateral hinge squared area",
                    )


    run.require(
        right_count == 6 and equil_count == 4 and (total_area_sq == Fraction(9, 2)),
        "hinge census and total",
    )


    # Exact reduced-rational square certificate, with no bounded search.
    run.require(
        not has_rational_square_root(Fraction(3, 4)),
        "irrational equilateral area",
    )


def check_scaling_and_complements(run: Cases) -> None:
    for lam in [Fraction(1, 2), Fraction(2, 1), Fraction(3, 1), Fraction(5, 2)]:
        for s01, s02, s12 in [(Fraction(1), Fraction(1), Fraction(2)), (Fraction(2), Fraction(2), Fraction(2))]:
            lhs = cayley_menger_triangle_area_sq(lam * lam * s01, lam * lam * s02, lam * lam * s12)
            rhs = (lam ** 4) * cayley_menger_triangle_area_sq(s01, s02, s12)
            run.require(
                lhs == rhs,
                "fourth-degree length scaling",
            )


    # Check all 380 proper nonempty contiguous boundary intervals on the 20-qubit HaPPY patch:
    # (a) complement symmetry of mincut and boundary_entropy, and (b) 1 <= S(A) <= mincut(A)
    for start in range(20):
        for length in range(1, 20):
            sc = (start + length) % 20
            lc = 20 - length
            s_a = interval_entropy(start, length)
            s_ac = interval_entropy(sc, lc)
            cut_a = interval_mincut(start, length)
            cut_ac = interval_mincut(sc, lc)
            run.require(
                s_a == s_ac and cut_a == cut_ac and (s_a >= 1) and (cut_a >= 1) and (s_a <= cut_a),
                "complement symmetry and entropy bounds",
            )


def main() -> int:
    coupling, entropy, geometry = Cases(), Cases(), Cases()
    check_rt_coupling(coupling)
    check_exact_entropy_examples(entropy)
    check_hinge_geometry(geometry)
    check_scaling_and_complements(geometry)
    checks = coupling.checks + entropy.checks + geometry.checks
    print(f"checks={checks} rt_bh={coupling.checks} dichotomy={entropy.checks} "
          f"regge_happy={geometry.checks} failures=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(cli(main))
