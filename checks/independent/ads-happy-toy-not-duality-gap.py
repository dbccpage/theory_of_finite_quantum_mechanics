#!/usr/bin/env python3
"""Independent verification for ADS-HAPPY-TOY-NOT-DUALITY-GAP (TFQ-2212).

AuthorityEffect: None.

Verifies from first principles (using only the Python standard library):
1. Flat stabilizer Renyi spectrum (S_n / S_1 = 1) vs. 2D CFT Calabrese-Cardy /
   Ryu-Takayanagi Renyi scaling S_n^{CFT} / S_1^{CFT} = (1 + 1/n) / 2 over Q.
2. Complete length-resolved census of all 380 proper contiguous boundary intervals on
   the 20-qubit 6-pentagon {5,4} HaPPY patch (340 exact S(A) = mincut(A) equalities and
   40 strict deficits S(A) = mincut(A) - 1 localized at lengths 8..12 with distribution
   5, 10, 10, 10, 5), including explicit witnesses (start=2, len=8) and (start=2, len=12)
   and the 5-fold rotational orbit start = 4*k + 2.
3. Disconnected boundary-region mutual information jumps on the 20-qubit HaPPY state and
   bulk-to-boundary Hilbert space codimensions across {5,4} pentagon patch layers.
"""

from __future__ import annotations

from fractions import Fraction
import sys


def cft_renyi_factor(n: Fraction) -> Fraction:
    return (Fraction(1) + Fraction(1) / n) / Fraction(2)


def stabilizer_renyi_factor(_n: Fraction) -> Fraction:
    return Fraction(1)


def renyi_spectrum_defect(n: Fraction, s1: Fraction) -> Fraction:
    return stabilizer_renyi_factor(n) * s1 - cft_renyi_factor(n) * s1


def set_xz(q: int, x: int, z: int) -> int:
    val = 0
    if x == 1:
        val |= 1 << (2 * q)
    if z == 1:
        val |= 1 << (2 * q + 1)
    return val


LOCAL_BLOCK_3 = [
    [(1, 0), (0, 1), (0, 1), (1, 0)],
    [(0, 1), (1, 1), (1, 1), (0, 1)],
    [(1, 1), (0, 1), (1, 1), (0, 0)],
]

PUSH_X_BLOCK = [(0, 1), (0, 1), (1, 0), (0, 0)]
PUSH_Z_BLOCK = [(1, 0), (0, 0), (1, 0), (0, 1)]

CENTRAL_GENS_5 = [
    [(1, 0), (0, 1), (0, 1), (1, 0), (0, 0)],
    [(0, 0), (1, 0), (0, 1), (0, 1), (1, 0)],
    [(1, 0), (0, 0), (1, 0), (0, 1), (0, 1)],
    [(0, 1), (1, 0), (0, 0), (1, 0), (0, 1)],
    [(0, 1), (0, 1), (0, 1), (0, 1), (0, 1)],
]


def encode_local_gen(k: int, pat: list[tuple[int, int]]) -> int:
    acc = 0
    for j in range(4):
        x, z = pat[j]
        acc ^= set_xz(4 * k + j, x, z)
    return acc


def encode_central_gen(cpat: list[tuple[int, int]]) -> int:
    acc = 0
    for k in range(5):
        cx, cz = cpat[k]
        if cx == 1:
            acc ^= encode_local_gen(k, PUSH_X_BLOCK)
        if cz == 1:
            acc ^= encode_local_gen(k, PUSH_Z_BLOCK)
    return acc


def build_boundary_gens_20() -> list[int]:
    gens: list[int] = []
    for k in range(5):
        for pat in LOCAL_BLOCK_3:
            gens.append(encode_local_gen(k, pat))
    for cpat in CENTRAL_GENS_5:
        gens.append(encode_central_gen(cpat))
    return gens


def commutes_20(u: int, v: int) -> bool:
    s = 0
    for q in range(20):
        ux = (u >> (2 * q)) & 1
        uz = (u >> (2 * q + 1)) & 1
        vx = (v >> (2 * q)) & 1
        vz = (v >> (2 * q + 1)) & 1
        s += (ux * vz) ^ (uz * vx)
    return (s % 2) == 0


def gf2_rank(rows: list[int]) -> int:
    basis: list[tuple[int, int]] = []
    for r in rows:
        cur = r
        for p, b in basis:
            if (cur >> p) & 1:
                cur ^= b
        if cur != 0:
            first_bit = 0
            for b in range(40):
                if (cur >> b) & 1:
                    first_bit = b
                    break
            basis.append((first_bit, cur))
    return len(basis)


def in_contiguous_interval(start: int, length: int, q: int) -> bool:
    return ((q + 20 - start) % 20) < length


def interval_bitmask_40(start: int, length: int) -> int:
    mask = 0
    for q in range(20):
        if in_contiguous_interval(start, length, q):
            mask |= 3 << (2 * q)
    return mask


def interval_entropy(gens: list[int], start: int, length: int) -> int:
    mask = interval_bitmask_40(start, length)
    return gf2_rank([g & mask for g in gens]) - length


def interval_mincut(start: int, length: int) -> int:
    a = [
        sum(1 for j in range(4) if in_contiguous_interval(start, length, 4 * k + j))
        for k in range(5)
    ]

    def cost_for_central(s_c: int) -> int:
        total = 0
        for k in range(5):
            ak = a[k]
            c0 = ak + (1 if 0 != s_c else 0)
            c1 = (4 - ak) + (1 if 1 != s_c else 0)
            total += min(c0, c1)
        return total

    return min(cost_for_central(0), cost_for_central(1))


def region_entropy(gens: list[int], qs: list[int]) -> int:
    mask = 0
    for q in qs:
        mask |= 3 << (2 * q)
    return gf2_rank([g & mask for g in gens]) - len(qs)


def region_mutual_information(gens: list[int], a: list[int], b: list[int]) -> int:
    return region_entropy(gens, a) + region_entropy(gens, b) - region_entropy(gens, a + b)


def main() -> int:
    checks = 0
    renyi_checks = 0
    mincut_checks = 0
    mi_codim_checks = 0
    failures = 0

    def check(cond: bool, bucket: str, msg: str) -> None:
        nonlocal checks, renyi_checks, mincut_checks, mi_codim_checks, failures
        checks += 1
        if bucket == "renyi":
            renyi_checks += 1
        elif bucket == "mincut":
            mincut_checks += 1
        else:
            mi_codim_checks += 1
        if not cond:
            failures += 1
            print(f"FAIL [{bucket}]: {msg}", file=sys.stderr)

    # 1. Renyi spectrum checks over Q
    check(cft_renyi_factor(Fraction(1)) == Fraction(1), "renyi", "cft_renyi_factor(1) == 1")
    check(cft_renyi_factor(Fraction(2)) == Fraction(3, 4), "renyi", "cft_renyi_factor(2) == 3/4")
    check(cft_renyi_factor(Fraction(3)) == Fraction(2, 3), "renyi", "cft_renyi_factor(3) == 2/3")
    check(cft_renyi_factor(Fraction(4)) == Fraction(5, 8), "renyi", "cft_renyi_factor(4) == 5/8")

    for n_int in range(2, 15):
        n_q = Fraction(n_int)
        check(
            cft_renyi_factor(n_q) - Fraction(1, 2) == Fraction(1, 2 * n_int),
            "renyi",
            f"cft_renyi_factor({n_int}) - 1/2",
        )
        check(
            cft_renyi_factor(n_q) < cft_renyi_factor(Fraction(n_int - 1)),
            "renyi",
            f"strict anti at {n_int}",
        )
        for s1 in (Fraction(1), Fraction(2), Fraction(5, 3), Fraction(4)):
            defect = renyi_spectrum_defect(n_q, s1)
            expected = Fraction(n_int - 1, 2 * n_int) * s1
            check(defect == expected and defect > 0, "renyi", f"defect({n_int}, {s1})")

    # 2. HaPPY 6-pentagon 20-qubit boundary state and 380-interval census
    gens = build_boundary_gens_20()
    check(len(gens) == 20, "mincut", "20 generators")
    check(gf2_rank(gens) == 20, "mincut", "rank 20")
    check(
        all(commutes_20(u, v) for u in gens for v in gens),
        "mincut",
        "pairwise commutation",
    )

    check(
        interval_entropy(gens, 2, 8) == 4 and interval_mincut(2, 8) == 5,
        "mincut",
        "witness (2, 8)",
    )
    check(
        interval_entropy(gens, 2, 12) == 4 and interval_mincut(2, 12) == 5,
        "mincut",
        "witness (2, 12)",
    )
    for k in range(5):
        s_k = 4 * k + 2
        check(
            interval_entropy(gens, s_k, 8) == 4 and interval_mincut(s_k, 8) == 5,
            "mincut",
            f"5-fold orbit k={k}",
        )

    expected_deficits_by_len = {
        1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0,
        8: 5, 9: 10, 10: 10, 11: 10, 12: 5,
        13: 0, 14: 0, 15: 0, 16: 0, 17: 0, 18: 0, 19: 0,
    }
    total_exact = 0
    total_deficit = 0
    for length in range(1, 20):
        def_count = 0
        ex_count = 0
        for start in range(20):
            s_val = interval_entropy(gens, start, length)
            m_val = interval_mincut(start, length)
            check(s_val <= m_val, "mincut", f"S <= mincut at ({start}, {length})")
            if s_val == m_val:
                ex_count += 1
            elif s_val + 1 == m_val:
                def_count += 1
        total_exact += ex_count
        total_deficit += def_count
        check(
            def_count == expected_deficits_by_len[length] and ex_count + def_count == 20,
            "mincut",
            f"deficit count at len={length}: got {def_count}",
        )

    check(total_exact == 340 and total_deficit == 40, "mincut", "340 exact and 40 deficit")

    # 3. Disconnected region mutual information and Hilbert codimension checks
    check(
        region_entropy(gens, [0]) == 1
        and region_entropy(gens, [8]) == 1
        and region_mutual_information(gens, [0], [8]) == 0,
        "mi_codim",
        "I([0] : [8]) == 0",
    )
    p0 = [0, 1, 2, 3]
    p1 = [4, 5, 6, 7]
    p2 = [8, 9, 10, 11]
    check(
        region_entropy(gens, p0) == 1
        and region_entropy(gens, p2) == 1
        and region_entropy(gens, p0 + p2) == 2
        and region_mutual_information(gens, p0, p2) == 0,
        "mi_codim",
        "I(P0 : P2) == 0",
    )
    check(
        region_entropy(gens, [0, 1]) == 2
        and region_entropy(gens, [2, 3]) == 2
        and region_mutual_information(gens, [0, 1], [2, 3]) == 3,
        "mi_codim",
        "I([0,1] : [2,3]) == 3",
    )
    check(
        region_entropy(gens, p0 + p1) == 2
        and region_entropy(gens, p0 + p1 + p2) == 2
        and region_mutual_information(gens, p0 + p1, p2) == 1,
        "mi_codim",
        "I(P0 U P1 : P2) == 1",
    )

    for n_bulk, n_bdry, exp_bulk, exp_bdry, exp_codim in [
        (1, 5, 2, 32, 30),
        (6, 20, 64, 1048576, 1048512),
        (11, 25, 2048, 33554432, 33552384),
    ]:
        d_bulk = 1 << n_bulk
        d_bdry = 1 << n_bdry
        codim = d_bdry - d_bulk
        check(
            d_bulk == exp_bulk and d_bdry == exp_bdry and codim == exp_codim and codim > 0,
            "mi_codim",
            f"codim({n_bulk}, {n_bdry})",
        )

    print(
        f"ads-happy-toy-not-duality-gap independent check: "
        f"checks={checks} renyi={renyi_checks} mincut={mincut_checks} "
        f"mi_codim={mi_codim_checks} failures={failures}"
    )
    print(
        "recorded renyi factors: cft(1)=1, cft(2)=3/4 (defect 1/4), "
        "cft(3)=2/3 (defect 1/3), cft(4)=5/8 (defect 3/8)"
    )
    print(
        "recorded happy patch mincut census: 380 intervals -> 340 exact, 40 strict deficits "
        "at lengths 8..12 (5, 10, 10, 10, 5); witness (2,8) and (2,12) have S=4 < 5=mincut"
    )
    print(
        "recorded mi & codim: I([0]:[8])=0, I(P0:P2)=0, I([0,1]:[2,3])=3, I(P0 U P1:P2)=1; "
        "codim(1,5)=30, codim(6,20)=1048512, codim(11,25)=33552384"
    )
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
