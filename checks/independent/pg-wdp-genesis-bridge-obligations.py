"""Independent check for the narrowed finite case of PG-WDP-GENESIS-BRIDGE-OBLIGATIONS.

No repository imports. Exact integers only.
"""
from __future__ import annotations

CHECKS = 0
FAILURES = 0


def check(cond: bool, msg: str) -> None:
    global CHECKS, FAILURES
    CHECKS += 1
    if not cond:
        FAILURES += 1
        print(f"FAIL {msg}")


def pair_defect(adj, u: int, v: int) -> bool:
    return adj(u, v) or adj(v, u)


def edge01(u: int, v: int) -> bool:
    return u == 0 and v == 1


def edge10(u: int, v: int) -> bool:
    return u == 1 and v == 0


def main() -> None:
    check(pair_defect(edge01, 0, 1) is True, "pairDefect edge01 (0,1) is true")
    check(pair_defect(edge10, 0, 1) is True, "pairDefect edge10 (0,1) is true")
    check(edge01(0, 1) is True, "directed step edge01 (0,1)")
    check(edge10(0, 1) is False, "no directed step edge10 (0,1)")
    check(edge10(1, 0) is True, "directed step edge10 (1,0)")
    check(edge01(1, 0) is False, "no directed step edge01 (1,0)")
    check(pair_defect(edge01, 0, 1) == pair_defect(edge10, 0, 1), "pair defects agree")
    check(1 * 1 != 2 * (1 * 1), "1*1 != 2*1*1")

    def matches_directed(phi, table) -> bool:
        for u in range(2):
            for v in range(2):
                if phi(table, u, v) is not table[(u, v)]:
                    return False
        return True

    def id_adj(table, u: int, v: int) -> bool:
        return table[(u, v)]

    def constant_true(table, u: int, v: int) -> bool:
        return True

    # Every 2-vertex adjacency: 2^4 = 16 windows. pairDefect is false exactly
    # when both directions are off. The identity function matches the directed
    # step. The constant-true map does not, except on the single full window.
    n_windows = 0
    n_pairs = 0
    n_id_match = 0
    n_constant_miss = 0
    n_defect_iff = 0
    for bits in range(16):
        table = {(i, j): ((bits >> (2 * i + j)) & 1) == 1 for i in range(2) for j in range(2)}
        n_windows += 1
        if matches_directed(id_adj, table):
            n_id_match += 1
        if not matches_directed(constant_true, table):
            n_constant_miss += 1
        for u in range(2):
            for v in range(2):
                n_pairs += 1
                both_off = (not table[(u, v)]) and (not table[(v, u)])
                defect = table[(u, v)] or table[(v, u)]
                if (defect is False) == both_off:
                    n_defect_iff += 1
    check(n_windows == 16, "16 windows on two vertices")
    check(n_pairs == 64, "64 directed pairs")
    check(n_id_match == 16, "identity matches directed steps on all 16 windows")
    check(n_constant_miss == 15, "constant-true misses the 15 windows that are not full")
    check(n_defect_iff == 64, "pairDefect false iff both directions off on all 64 pairs")
    check(
        edge01(0, 1) != edge10(0, 1) and pair_defect(edge01, 0, 1) == pair_defect(edge10, 0, 1),
        "orientation swap separates directed steps and not pair defects",
    )
    check(pair_defect(edge10, 0, 1) is True and edge10(0, 1) is False, "pairDefect is not the directed step")

    # Exact search: no solution of p*p = 2*q*q for 1 <= q <= 200, with p <= 2*q.
    solutions = []
    for q in range(1, 201):
        qq = q * q
        target = 2 * qq
        # p must be even and p*p = target, so p <= floor(sqrt(target)) <= q + q.
        for p in range(1, 2 * q + 1):
            if p * p == target:
                solutions.append((p, q))
    check(solutions == [], f"no solutions for q=1..200, found {solutions[:3]}")

    print(f"checked {CHECKS} claims, failures {FAILURES}")
    if FAILURES:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
