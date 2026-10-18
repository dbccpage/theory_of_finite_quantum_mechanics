"""L1 proximity of a finite cochain host to named SM-gauge and SUSY extras.

AuthorityEffect: None.

This module does not derive SU(3)×SU(2)×U(1) or supersymmetry.
It measures ℓ¹ distance from host-constructible discrete shadows to a
declared extra vector, and it kills 3-2-1 uniqueness.

Stdlib only. No numpy, scipy, universe_anomalonica, or omega_engine.
"""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass
from itertools import product


def l1(v: tuple[int, ...]) -> int:
    return sum(abs(x) for x in v)


def vec_sub(a: tuple[int, ...], b: tuple[int, ...]) -> tuple[int, ...]:
    if len(a) != len(b):
        raise ValueError("feature length mismatch")
    return tuple(x - y for x, y in zip(a, b))


@dataclass(frozen=True)
class FiniteGroup:
    name: str
    order: int
    abelian: bool
    generators: int


# Declared finite menu. Lie groups are not on this list because they
# are not constructed on the host.
FINITE_MENU: tuple[FiniteGroup, ...] = (
    FiniteGroup("1", 1, True, 0),
    FiniteGroup("Z2", 2, True, 1),
    FiniteGroup("Z3", 3, True, 1),
    FiniteGroup("Z4", 4, True, 1),
    FiniteGroup("Z2xZ2", 4, True, 2),
    FiniteGroup("S3", 6, False, 2),
    FiniteGroup("D4", 8, False, 2),
    FiniteGroup("Q8", 8, False, 2),
    FiniteGroup("A4", 12, False, 2),
    FiniteGroup("S4", 24, False, 2),
)


def group_by_name(name: str) -> FiniteGroup:
    for g in FINITE_MENU:
        if g.name == name:
            return g
    raise KeyError(name)


# Feature layout (all integers):
# 0 n_slots
# 1 size of 2-slot (finite order, or Lie adjoint dim for the named extra)
# 2 size of 1-slot
# 3 size of 0-slot
# 4 number of abelian factors
# 5 number of nonabelian factors
# 6 compact-connected Lie extra (1 only for the named SM target)
# 7 Z2 grading present
# 8 odd generator with square even (superbracket shadow)
# 9 equal even/odd counting extra
FEATURE_LEN = 10


def features(
    g2: FiniteGroup,
    g1: FiniteGroup,
    g0: FiniteGroup,
    *,
    lie_extra: int = 0,
    grading: int = 0,
    superbracket: int = 0,
    equal_bf: int = 0,
) -> tuple[int, ...]:
    abelian = int(g2.abelian) + int(g1.abelian) + int(g0.abelian)
    nonabelian = 3 - abelian
    return (
        3,
        g2.order,
        g1.order,
        g0.order,
        abelian,
        nonabelian,
        lie_extra,
        grading,
        superbracket,
        equal_bf,
    )


# Declared extras of ordinary SM gauge. Not a theorem of the host.
# Sizes are adjoint dimensions 8, 3, 1.
SM_GAUGE_EXTRAS: tuple[int, ...] = (3, 8, 3, 1, 1, 2, 1, 0, 0, 0)

# Declared extras of a supersymmetry-like structure on top of a host.
# Grading, superbracket, equal boson/fermion counting. Not a superalgebra.
SUSY_EXTRAS: tuple[int, ...] = (0, 0, 0, 0, 0, 0, 0, 1, 1, 1)


def sm_distance(feat: tuple[int, ...]) -> int:
    return l1(vec_sub(feat, SM_GAUGE_EXTRAS))


def susy_extra_distance(grading: int, superbracket: int, equal_bf: int) -> int:
    host = (grading, superbracket, equal_bf)
    target = (SUSY_EXTRAS[7], SUSY_EXTRAS[8], SUSY_EXTRAS[9])
    return l1(vec_sub(host, target))


def all_321_assignments() -> Iterator[tuple[FiniteGroup, FiniteGroup, FiniteGroup]]:
    yield from product(FINITE_MENU, FINITE_MENU, FINITE_MENU)


def discrete_321_census() -> list[tuple[str, str, str, int]]:
    """Every 3-2-1 assignment from the declared finite menu, with L1 to SM extras."""
    rows: list[tuple[str, str, str, int]] = []
    for g2, g1, g0 in all_321_assignments():
        feat = features(g2, g1, g0, lie_extra=0)
        rows.append((g2.name, g1.name, g0.name, sm_distance(feat)))
    return rows


def min_sm_distance() -> tuple[int, list[tuple[str, str, str]]]:
    rows = discrete_321_census()
    m = min(d for _, _, _, d in rows)
    winners = [(a, b, c) for a, b, c, d in rows if d == m]
    return m, winners


def simplex_shadow() -> tuple[FiniteGroup, FiniteGroup, FiniteGroup]:
    """Constructible discrete shadow of a filled 2-simplex: Z3, Z2, 1."""
    return group_by_name("Z3"), group_by_name("Z2"), group_by_name("1")


def uniqueness_killed() -> bool:
    """At least two non-isomorphic 3-2-1 assignments exist, and none has L1 0 to SM."""
    rows = discrete_321_census()
    names = {(a, b, c) for a, b, c, _ in rows}
    distances = {d for _, _, _, d in rows}
    return len(names) > 1 and 0 not in distances


# --- Class A: ℓ¹ residual on the boundary of a 2-simplex ---

# Oriented edges of a triangle: 01, 12, 20.
# d0 maps vertex values (a,b,c) to edge differences (b-a, c-b, a-c).


def d0_vertex(alpha: tuple[int, int, int]) -> tuple[int, int, int]:
    a, b, c = alpha
    return (b - a, c - b, a - c)


def phi_triangle(omega: tuple[int, int, int]) -> int:
    """Exact integer quotient residual on the oriented triangle.

    The image of ``d0_vertex`` is exactly the integer triples whose
    oriented sum is zero.  Every residual therefore has the same sum as
    ``omega``, so its L1 norm is at least ``abs(sum(omega))``.  That bound
    is attained by moving all residual mass to one edge.
    """
    return abs(sum(omega))


def opposite_signs_do_not_cancel() -> bool:
    return l1((1, -1)) == 2


def closed_loop_sum_zero(omega: tuple[int, int, int]) -> bool:
    """On the triangle, exact 1-cochains have sum of oriented edges 0."""
    return sum(omega) == 0


def exact_implies_loop_sum_zero(bound: int = 2) -> bool:
    for alpha in product(range(-bound, bound + 1), repeat=3):
        w = d0_vertex(alpha)
        if not closed_loop_sum_zero(w):
            return False
    return True


# Cochain grading: even = vertex 0-cochains, odd = edge 1-cochains.
# This is the closest host object to a boson/fermion split. It is not SUSY.


@dataclass(frozen=True)
class CochainGrading:
    even_dim: int
    odd_dim: int
    d_raises_degree: bool
    superbracket: bool
    equal_counting: bool


def triangle_grading() -> CochainGrading:
    even_dim = 3
    odd_dim = 3
    return CochainGrading(
        even_dim=even_dim,
        odd_dim=odd_dim,
        d_raises_degree=True,
        superbracket=False,
        equal_counting=(even_dim == odd_dim),
    )


def grading_is_not_susy(g: CochainGrading) -> bool:
    return (not g.superbracket) or (not g.d_raises_degree)


def proximity_report() -> dict[str, object]:
    g2, g1, g0 = simplex_shadow()
    shadow = features(g2, g1, g0, lie_extra=0)
    d_sm = sm_distance(shadow)
    min_d, winners = min_sm_distance()
    gr = triangle_grading()
    d_susy = susy_extra_distance(
        grading=1 if gr.d_raises_degree else 0,
        superbracket=int(gr.superbracket),
        equal_bf=int(gr.equal_counting),
    )
    ungraded_susy = susy_extra_distance(0, 0, 0)
    return {
        "authority_effect": "None",
        "simplex_shadow": (g2.name, g1.name, g0.name),
        "simplex_shadow_sm_l1": d_sm,
        "min_sm_l1_over_finite_menu": min_d,
        "min_sm_l1_winners_count": len(winners),
        "sm_l1_zero_exists": min_d == 0,
        "uniqueness_killed": uniqueness_killed(),
        "assignment_count": len(FINITE_MENU) ** 3,
        "phi_exact_zero": phi_triangle((1, 1, -2)) == 0,
        "phi_inexact_example": phi_triangle((1, 0, 0)),
        "opposite_signs_l1": l1((1, -1)),
        "grading_even_odd": (gr.even_dim, gr.odd_dim),
        "grading_equal_counting": gr.equal_counting,
        "grading_superbracket": gr.superbracket,
        "susy_extra_l1_graded": d_susy,
        "susy_extra_l1_ungraded": ungraded_susy,
        "graded_closer_than_ungraded": d_susy < ungraded_susy,
        "is_sm": False,
        "is_susy": False,
    }
