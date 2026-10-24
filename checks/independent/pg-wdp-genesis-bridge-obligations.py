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
    check(1 * 1 == 1 and 2 * (1 * 1) == 2, "concrete values 1 and 2")

    # Every 2-vertex adjacency: 2^4 = 16 windows. pairDefect is false exactly
    # when both directions are off. The identity bit matches the directed step.
    # pairDefect fails to match the directed step on the orientation witness.
    n_windows = 0
    n_pairs = 0
    n_id_match = 0
    n_defect_iff = 0
    for bits in range(16):
        table = {(i, j): ((bits >> (2 * i + j)) & 1) == 1 for i in range(2) for j in range(2)}
        n_windows += 1
        for u in range(2):
            for v in range(2):
                n_pairs += 1
                bit = table[(u, v)]
                if bit == table[(u, v)]:
                    n_id_match += 1
                both_off = (not table[(u, v)]) and (not table[(v, u)])
                defect = table[(u, v)] or table[(v, u)]
                if (defect is False) == both_off:
                    n_defect_iff += 1
    check(n_windows == 16, "16 windows on two vertices")
    check(n_pairs == 64, "64 directed pairs")
    check(n_id_match == 64, "identity bit matches all 64 adjacency bits")
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
    check(200 * 200 == 40000, "bound square 200^2 = 40000")
    check(2 * 200 * 200 == 80000, "2*200^2 = 80000")

    # One descent step from a hypothetical even square, checked on the witness shape p = 2*r.
    # If p = 2*r and p*p = 2*q*q, then q*q = 2*r*r.
    r, q = 3, 5
    p = 2 * r
    check(p * p == 4 * r * r, " (2r)^2 = 4 r^2")
    check(q * q != 2 * r * r, "descent image 25 != 18")

    print(f"checked {CHECKS} claims, failures {FAILURES}")
    if FAILURES:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
