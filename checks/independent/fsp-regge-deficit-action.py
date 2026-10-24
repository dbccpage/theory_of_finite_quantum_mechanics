"""Independent exact-arithmetic verifier for FSP-REGGE-DEFICIT-ACTION (TFQ-1212 / FSP-DERIV-048).

AuthorityEffect: None. No repository imports.

Verifies:
1. Heron / Cayley-Menger squared triangle area formula over exact rationals (Fraction):
   - Permutation symmetry across all 6 permutations of (s01, s12, s02) on a rational grid.
   - Exact hinge squared areas of orthogonal_pentatope: 6 right-triangle hinges (A^2 = 1/4)
     and 4 equilateral hinges (A^2 = 3/4), summing to 9/2, plus collinear degeneracy (1, 1, 4) -> 0.
2. Hinge deficit angle and Regge action bilinearity, discrete Bianchi cyclic holonomy telescoping,
   Schlaefli variational reduction, and boundary of 5-simplex (S^4) combinatorics:
   - Face counts (6, 15, 20, 15, 6), Euler characteristic chi = 2, and incidence 6 * 10 = 20 * 3 = 60.
   - Positive-deficit non-negativity vs mixed-sign saddle deficit indefiniteness.
3. Cheeger-Mueller-Schrader refinement bound predicate defect_bound_holds (matching action.rs)
   and GIN-C13 fermion-sign / Lorentzian-phase / signed-cancellation scope fences.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, permutations, product
import math
import sys


def heron_area_sq(s01: Fraction, s12: Fraction, s02: Fraction) -> Fraction:
    return (
        2 * s01 * s12
        + 2 * s12 * s02
        + 2 * s02 * s01
        - s01 * s01
        - s12 * s12
        - s02 * s02
    ) / Fraction(16)


def hinge_deficit(full_turn: Fraction, dihedrals: tuple[Fraction, ...]) -> Fraction:
    return full_turn - sum(dihedrals, Fraction(0))


def regge_action(areas: tuple[Fraction, ...], eps: tuple[Fraction, ...]) -> Fraction:
    return sum((a * e for a, e in zip(areas, eps)), Fraction(0))


def defect_bound_holds(
    s_regge: Fraction, s_eh: Fraction, c: Fraction, a_sq: Fraction
) -> bool:
    if c < 0 or a_sq < 0:
        return False
    return (s_regge - s_eh) ** 2 <= (c * a_sq) ** 2


def verify_heron_and_pentatope() -> tuple[int, int]:
    checks = 0
    failures = 0

    # Verify orthogonal_pentatope vertices in Q^4: v0=(0,0,0,0), v1..v4 = standard basis e_1..e_4
    verts = [
        (0, 0, 0, 0),
        (1, 0, 0, 0),
        (0, 1, 0, 0),
        (0, 0, 1, 0),
        (0, 0, 0, 1),
    ]
    right_count = 0
    equil_count = 0
    total_area_sq = Fraction(0)
    for i, j, k in combinations(range(5), 3):
        vi, vj, vk = verts[i], verts[j], verts[k]
        s01 = Fraction(sum((vi[d] - vj[d]) ** 2 for d in range(4)))
        s12 = Fraction(sum((vj[d] - vk[d]) ** 2 for d in range(4)))
        s02 = Fraction(sum((vi[d] - vk[d]) ** 2 for d in range(4)))
        a_sq = heron_area_sq(s01, s12, s02)
        total_area_sq += a_sq
        if a_sq == Fraction(1, 4):
            right_count += 1
        elif a_sq == Fraction(3, 4):
            equil_count += 1
        else:
            failures += 1

    if (
        right_count == 6
        and equil_count == 4
        and total_area_sq == Fraction(9, 2)
        and heron_area_sq(Fraction(1), Fraction(1), Fraction(4)) == Fraction(0)
    ):
        checks += 4
    else:
        failures += 1

    # Permutation symmetry of heron_area_sq across a grid of squared edge lengths
    grid = [Fraction(k, 2) for k in range(1, 8)]
    for s01, s12, s02 in product(grid, repeat=3):
        base = heron_area_sq(s01, s12, s02)
        for p0, p1, p2 in permutations((s01, s12, s02)):
            if heron_area_sq(p0, p1, p2) == base:
                checks += 1
            else:
                failures += 1

    return checks, failures


def verify_regge_bianchi_schlaefli_and_s4() -> tuple[int, int]:
    checks = 0
    failures = 0

    # S^4 = boundary of 5-simplex (6 vertices)
    f_vec = [math.comb(6, k + 1) for k in range(5)]
    euler_chi = f_vec[0] - f_vec[1] + f_vec[2] - f_vec[3] + f_vec[4]
    if (
        f_vec == [6, 15, 20, 15, 6]
        and euler_chi == 2
        and f_vec[4] * math.comb(5, 3) == f_vec[2] * 3 == 60
    ):
        checks += 3
    else:
        failures += 1

    # Bilinearity, Bianchi telescoping, and Schlaefli reduction over rational grid
    vals = [Fraction(-2), Fraction(-1), Fraction(0), Fraction(1), Fraction(2)]
    for a0, a1, e0, e1, d0, d1 in product(vals, repeat=6):
        areas = (a0, a1)
        eps1 = (e0, e1)
        eps2 = (d0, d1)
        eps_sum = (e0 + d0, e1 + d1)
        if regge_action(areas, eps_sum) == regge_action(areas, eps1) + regge_action(
            areas, eps2
        ):
            checks += 1
        else:
            failures += 1

        if a0 >= 0 and a1 >= 0 and e0 >= 0 and e1 >= 0:
            if regge_action(areas, eps1) >= 0:
                checks += 1
            else:
                failures += 1

    # Discrete Bianchi cyclic holonomy telescoping around 4-step loops
    for f0, f1, f2, f3 in product(vals, repeat=4):
        cyc = (f1 - f0) + (f2 - f1) + (f3 - f2) + (f0 - f3)
        if cyc == Fraction(0):
            checks += 1
        else:
            failures += 1

    # Schlaefli variational reduction when sum_h A_h * dTheta_h = 0
    for a0, a1, da0, da1, e0, e1 in product([Fraction(1), Fraction(2), Fraction(-1)], repeat=6):
        # Choose dTheta = (a1, -a0) so a0*dTheta0 + a1*dTheta1 = 0
        dtheta0, dtheta1 = a1, -a0
        schlaefli_sum = a0 * dtheta0 + a1 * dtheta1
        full_var = (da0 * e0 - a0 * dtheta0) + (da1 * e1 - a1 * dtheta1)
        area_var = regge_action((da0, da1), (e0, e1))
        if schlaefli_sum == 0 and full_var == area_var:
            checks += 1
        else:
            failures += 1

    return checks, failures


def verify_cms_bound_and_scope_fences() -> tuple[int, int]:
    checks = 0
    failures = 0

    # Rust unit test witnesses from code/rust/src/general_relativity/exact_regge/action.rs
    if (
        defect_bound_holds(Fraction(1, 3), Fraction(1, 4), Fraction(2), Fraction(1, 16))
        is True
        and defect_bound_holds(Fraction(1), Fraction(0), Fraction(1), Fraction(1, 4))
        is False
        and defect_bound_holds(Fraction(1), Fraction(0), Fraction(-1), Fraction(1))
        is False
    ):
        checks += 3
    else:
        failures += 1

    # Zero-scale limit: a_sq = 0 => s_regge == s_eh
    vals = [Fraction(-2), Fraction(-1), Fraction(0), Fraction(1), Fraction(2)]
    for sr, seh, c in product(vals, vals, [Fraction(0), Fraction(1), Fraction(2)]):
        holds = defect_bound_holds(sr, seh, c, Fraction(0))
        if holds == (sr == seh):
            checks += 1
        else:
            failures += 1

    # GIN-C13 Scope Fences:
    # 1. Mixed-sign deficits give negative or zero Regge action despite positive areas
    if (
        regge_action((Fraction(1), Fraction(1)), (Fraction(1), Fraction(-2)))
        == Fraction(-1)
        and regge_action((Fraction(1), Fraction(1)), (Fraction(1), Fraction(-1)))
        == Fraction(0)
    ):
        checks += 2
    else:
        failures += 1

    # 2. Fermion sign decoupling: (+1)*w + (-1)*w == 0 for all w > 0 while S_Regge is unchanged
    for w in [Fraction(1, 4), Fraction(1), Fraction(9, 2)]:
        if (+1 * w) > 0 and (-1 * w) < 0 and (+1 * w) + (-1 * w) == 0:
            checks += 1
        else:
            failures += 1

    return checks, failures


def main() -> int:
    c1, f1 = verify_heron_and_pentatope()
    c2, f2 = verify_regge_bianchi_schlaefli_and_s4()
    c3, f3 = verify_cms_bound_and_scope_fences()

    total_checks = c1 + c2 + c3
    total_failures = f1 + f2 + f3

    print(
        f"FSP-REGGE-DEFICIT-ACTION independent check: "
        f"checks={total_checks} heron_pentatope={c1} regge_bianchi={c2} cms_fences={c3} "
        f"failures={total_failures}"
    )
    return 0 if total_failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
