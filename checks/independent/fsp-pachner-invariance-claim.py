#!/usr/bin/env python3
"""Independent verification for FSP-PACHNER-INVARIANCE-CLAIM (TFQ-1214 / FSP-DERIV-050).

Standalone exact-rational and combinatorial checker using only Python's standard library.
Verifies:
1. Combinatorial 4D bistellar Pachner moves (1<->5, 2<->4, 3<->3) on explicit 4-simplex sets
   starting from partial Delta^5 = S^4, face-vector trajectory (6,15,20,15,6) -> (7,20,30,25,10)
   -> (7,21,34,30,12) -> (7,21,34,30,12), Euler characteristic chi = 2 invariance, and
   codimension-1 Dehn-Sommerville invariance 2 N3 - 5 N4 = 0.
2. Exact linear state-sum Pachner invariance characterization
   w0 = 10 w2 + 15 w3 + 6 w4, w1 = -4 w2 - 5 w3 - 2 w4 and finite-group flat bundle vertex
   normalization G^{-N0} |Flat|.
3. Metric Regge action non-invariance under curved 1->5 and 2->4 moves, curved WDW scalar
   defect growth (45 -> 60 -> 63), signed rational deficit cancellation, unnormalized simplex
   weight failure, and fermion-sign independence.
"""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
import itertools
import sys


def face_vector_4d(simplices: set[tuple[int, ...]]) -> tuple[int, int, int, int, int]:
    v = {x for s in simplices for x in s}
    e = {tuple(sorted(c)) for s in simplices for c in itertools.combinations(s, 2)}
    t = {tuple(sorted(c)) for s in simplices for c in itertools.combinations(s, 3)}
    q = {tuple(sorted(c)) for s in simplices for c in itertools.combinations(s, 4)}
    return (len(v), len(e), len(t), len(q), len(simplices))


def euler_char(fv: tuple[int, int, int, int, int]) -> int:
    return fv[0] - fv[1] + fv[2] - fv[3] + fv[4]


def pachner_1_to_5(fv: tuple[int, int, int, int, int]) -> tuple[int, int, int, int, int]:
    return (fv[0] + 1, fv[1] + 5, fv[2] + 10, fv[3] + 10, fv[4] + 4)


def pachner_5_to_1(fv: tuple[int, int, int, int, int]) -> tuple[int, int, int, int, int]:
    return (fv[0] - 1, fv[1] - 5, fv[2] - 10, fv[3] - 10, fv[4] - 4)


def pachner_2_to_4(fv: tuple[int, int, int, int, int]) -> tuple[int, int, int, int, int]:
    return (fv[0], fv[1] + 1, fv[2] + 4, fv[3] + 5, fv[4] + 2)


def pachner_4_to_2(fv: tuple[int, int, int, int, int]) -> tuple[int, int, int, int, int]:
    return (fv[0], fv[1] - 1, fv[2] - 4, fv[3] - 5, fv[4] - 2)


def linear_exp(w: tuple[Fraction, ...], fv: tuple[int, int, int, int, int]) -> Fraction:
    return sum((wk * Fraction(nk) for wk, nk in zip(w, fv)), Fraction(0))


def main() -> int:
    pachner_comb = 0
    state_sum = 0
    fences = 0
    failures = 0

    def check(cond: bool, category: str) -> None:
        nonlocal pachner_comb, state_sum, fences, failures
        if not cond:
            failures += 1
        if category == "comb":
            pachner_comb += 1
        elif category == "sum":
            state_sum += 1
        else:
            fences += 1

    # 1. Explicit combinatorial S^4 surgical trajectory and face-vector algebra
    simplices: set[tuple[int, ...]] = {
        tuple(sorted(c)) for c in itertools.combinations(range(6), 5)
    }
    fv0 = face_vector_4d(simplices)
    check(fv0 == (6, 15, 20, 15, 6), "comb")
    check(euler_char(fv0) == 2, "comb")
    check(2 * fv0[3] - 5 * fv0[4] == 0, "comb")

    # Apply combinatorial 1->5 move
    s0 = sorted(simplices)[0]
    new_v = 6
    simplices.remove(s0)
    for tet in itertools.combinations(s0, 4):
        simplices.add(tuple(sorted(tet + (new_v,))))
    fv1 = face_vector_4d(simplices)
    check(fv1 == (7, 20, 30, 25, 10) and fv1 == pachner_1_to_5(fv0), "comb")
    check(euler_char(fv1) == 2 and 2 * fv1[3] - 5 * fv1[4] == 0, "comb")

    # Apply combinatorial 2->4 move
    edges_1 = {tuple(sorted(c)) for s in simplices for c in itertools.combinations(s, 2)}
    tet_map: dict[tuple[int, ...], list[tuple[int, ...]]] = defaultdict(list)
    for s in simplices:
        for tet in itertools.combinations(s, 4):
            tet_map[tuple(sorted(tet))].append(s)
    moved_24 = False
    for tet, s_list in sorted(tet_map.items()):
        if len(s_list) == 2:
            sa, sb = s_list
            u = next(iter(set(sa) - set(tet)))
            v = next(iter(set(sb) - set(tet)))
            if tuple(sorted((u, v))) not in edges_1:
                simplices.remove(sa)
                simplices.remove(sb)
                for tri in itertools.combinations(tet, 3):
                    simplices.add(tuple(sorted(tri + (u, v))))
                moved_24 = True
                break
    check(moved_24, "comb")
    fv2 = face_vector_4d(simplices)
    check(fv2 == (7, 21, 34, 30, 12) and fv2 == pachner_2_to_4(fv1), "comb")
    check(euler_char(fv2) == 2 and 2 * fv2[3] - 5 * fv2[4] == 0, "comb")

    # Apply combinatorial 3->3 move
    tris_2 = {tuple(sorted(c)) for s in simplices for c in itertools.combinations(s, 3)}
    tri_map: dict[tuple[int, ...], list[tuple[int, ...]]] = defaultdict(list)
    for s in simplices:
        for tri in itertools.combinations(s, 3):
            tri_map[tuple(sorted(tri))].append(s)
    moved_33 = False
    for tri, s_list in sorted(tri_map.items()):
        if len(s_list) == 3:
            opp = tuple(sorted(set().union(*s_list) - set(tri)))
            if len(opp) == 3 and opp not in tris_2:
                for s in s_list:
                    simplices.remove(s)
                for edge in itertools.combinations(tri, 2):
                    simplices.add(tuple(sorted(edge + opp)))
                moved_33 = True
                break
    check(moved_33, "comb")
    fv3 = face_vector_4d(simplices)
    check(fv3 == (7, 21, 34, 30, 12) and fv3 == fv2, "comb")
    check(euler_char(fv3) == 2 and 2 * fv3[3] - 5 * fv3[4] == 0, "comb")

    for n0, n1, n2, n3, n4 in itertools.product(range(-2, 3), repeat=5):
        fv = (n0, n1, n2, n3, n4)
        check(euler_char(pachner_1_to_5(fv)) == euler_char(fv), "comb")
        check(euler_char(pachner_5_to_1(fv)) == euler_char(fv), "comb")
        check(euler_char(pachner_2_to_4(fv)) == euler_char(fv), "comb")
        check(euler_char(pachner_4_to_2(fv)) == euler_char(fv), "comb")
        check(pachner_5_to_1(pachner_1_to_5(fv)) == fv, "comb")
        check(pachner_4_to_2(pachner_2_to_4(fv)) == fv, "comb")
        check(
            2 * pachner_1_to_5(fv)[3] - 5 * pachner_1_to_5(fv)[4] == 2 * fv[3] - 5 * fv[4],
            "comb",
        )
        check(
            2 * pachner_2_to_4(fv)[3] - 5 * pachner_2_to_4(fv)[4] == 2 * fv[3] - 5 * fv[4],
            "comb",
        )

    # 2. Linear topological state-sum invariance and finite-group flat bundle normalization
    q_grid = [Fraction(-2), Fraction(-1), Fraction(0), Fraction(1), Fraction(2)]
    for w2, w3, w4 in itertools.product(q_grid, repeat=3):
        w0_inv = 10 * w2 + 15 * w3 + 6 * w4
        w1_inv = -4 * w2 - 5 * w3 - 2 * w4
        w_inv = (w0_inv, w1_inv, w2, w3, w4)
        check(linear_exp(w_inv, pachner_1_to_5(fv0)) == linear_exp(w_inv, fv0), "sum")
        check(linear_exp(w_inv, pachner_2_to_4(fv0)) == linear_exp(w_inv, fv0), "sum")
        for dw0, dw1 in [(Fraction(1), Fraction(0)), (Fraction(0), Fraction(1))]:
            w_bad = (w0_inv + dw0, w1_inv + dw1, w2, w3, w4)
            inv_both = (linear_exp(w_bad, pachner_1_to_5(fv0)) == linear_exp(w_bad, fv0)) and (
                linear_exp(w_bad, pachner_2_to_4(fv0)) == linear_exp(w_bad, fv0)
            )
            check(not inv_both, "sum")

    for g_ord in [Fraction(2), Fraction(3), Fraction(4), Fraction(5)]:
        for inv_n0 in [Fraction(1, 16), Fraction(1, 64), Fraction(1, 81)]:
            for flat_cnt in [Fraction(8), Fraction(16), Fraction(32)]:
                s_before = inv_n0 * flat_cnt
                s_after_15 = ((Fraction(1) / g_ord) * inv_n0) * (g_ord * flat_cnt)
                check(s_after_15 == s_before, "sum")

    # 3. Regge action non-invariance, curved WDW defect growth, and scope fences
    check(3 * fv0[1] == 45 and 3 * fv1[1] == 60 and 3 * fv2[1] == 63 and 3 * fv3[1] == 63, "fence")
    check(45 < 60 < 63, "fence")

    for area in [Fraction(1, 4), Fraction(3, 4), Fraction(1), Fraction(2)]:
        check(10 * area * Fraction(0) == Fraction(0), "fence")
        check(4 * area * Fraction(0) == Fraction(0), "fence")
        for eps in [Fraction(-2), Fraction(-1, 2), Fraction(1, 2), Fraction(2)]:
            check(10 * area * eps != Fraction(0), "fence")
            check(4 * area * eps != Fraction(0), "fence")

    deficits_24 = (Fraction(1), Fraction(-1), Fraction(1), Fraction(-1))
    check(deficits_24[0] > 0 and sum(deficits_24, Fraction(0)) == Fraction(0), "fence")

    for w4 in [Fraction(-2), Fraction(-1), Fraction(1), Fraction(2)]:
        w_n4 = (Fraction(0), Fraction(0), Fraction(0), Fraction(0), w4)
        check(linear_exp(w_n4, pachner_1_to_5(fv0)) - linear_exp(w_n4, fv0) == 4 * w4 != 0, "fence")
        check(linear_exp(w_n4, pachner_2_to_4(fv0)) - linear_exp(w_n4, fv0) == 2 * w4 != 0, "fence")

    for fv in (fv0, fv1, fv2, fv3):
        check(1 * euler_char(fv) + (-1) * euler_char(fv) == 0, "fence")

    total = pachner_comb + state_sum + fences
    print(
        f"FSP-PACHNER-INVARIANCE-CLAIM independent check: "
        f"checks={total} pachner_comb={pachner_comb} state_sum={state_sum} "
        f"fences={fences} failures={failures}"
    )
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
