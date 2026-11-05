#!/usr/bin/env python3
"""Independent verification for ADS-HAPPY-TOY-NOT-DUALITY-GAP (TFQ-2212).

AuthorityEffect: None.

Checks the supplied hand-encoded finite model; no tensor-network contraction is derived:
1. Flat stabilizer Renyi spectrum (S_n / S_1 = 1) vs. 2D CFT Calabrese-Cardy /
   Ryu-Takayanagi Renyi scaling S_n^{CFT} / S_1^{CFT} = (1 + 1/n) / 2 over Q.
2. Complete length-resolved census of all 380 proper contiguous boundary intervals on
   the hand-encoded 20-qubit HaPPY-inspired stabilizer fixture (340 exact S(A) = mincut(A) equalities and
   40 strict deficits S(A) = mincut(A) - 1 localized at lengths 8..12 with distribution
   5, 10, 10, 10, 5), including explicit witnesses (start=2, len=8) and (start=2, len=12)
   and the 5-fold rotational orbit start = 4*k + 2.
3. Disconnected boundary-region mutual information jumps on the 20-qubit HaPPY state and
   bulk-to-boundary Hilbert space codimensions across {5,4} pentagon patch layers.
"""

from __future__ import annotations

from fractions import Fraction

# Shared checker infrastructure only; no production implementation is imported.
from pathlib import Path as _Path
import sys as _sys
_sys.path.insert(0, str(_Path(__file__).resolve().parents[1]))
from checker_support.boundary import cli
from checker_support.cases import Cases
from checker_support.domains import rational


def cft_renyi_factor(n: Fraction) -> Fraction:
    n = rational(n, "Renyi order", strictly_positive=True)
    return (Fraction(1) + Fraction(1) / n) / Fraction(2)


def stabilizer_renyi_factor(_n: Fraction) -> Fraction:
    rational(_n, "Renyi order", strictly_positive=True)
    return Fraction(1)


def renyi_spectrum_defect(n: Fraction, s1: Fraction) -> Fraction:
    s1 = rational(s1, "entropy", minimum=0)
    return stabilizer_renyi_factor(n) * s1 - cft_renyi_factor(n) * s1


from checker_support.happy_boundary import build_boundary_gens_20, commutes_20, gf2_rank, interval_entropy, interval_mincut, region_entropy, region_mutual_information


def check_renyi_factors(run: Cases) -> None:
    run.require(cft_renyi_factor(Fraction(1)) == Fraction(1), "cft_renyi_factor(1) == 1")
    run.require(cft_renyi_factor(Fraction(2)) == Fraction(3, 4), "cft_renyi_factor(2) == 3/4")
    run.require(cft_renyi_factor(Fraction(3)) == Fraction(2, 3), "cft_renyi_factor(3) == 2/3")
    run.require(cft_renyi_factor(Fraction(4)) == Fraction(5, 8), "cft_renyi_factor(4) == 5/8")

    for n_int in range(2, 15):
        n_q = Fraction(n_int)
        run.require(
            cft_renyi_factor(n_q) - Fraction(1, 2) == Fraction(1, 2 * n_int),

            f"cft_renyi_factor({n_int}) - 1/2",
        )
        run.require(
            cft_renyi_factor(n_q) < cft_renyi_factor(Fraction(n_int - 1)),

            f"strict anti at {n_int}",
        )
        for s1 in (Fraction(1), Fraction(2), Fraction(5, 3), Fraction(4)):
            defect = renyi_spectrum_defect(n_q, s1)
            expected = Fraction(n_int - 1, 2 * n_int) * s1
            run.require(defect == expected and defect > 0, f"defect({n_int}, {s1})")


def check_interval_census(run: Cases) -> list[int]:
    gens = build_boundary_gens_20()
    run.require(len(gens) == 20, "20 generators")
    run.require(gf2_rank(gens) == 20, "rank 20")
    run.require(
        all(commutes_20(u, v) for u in gens for v in gens),

        "pairwise commutation",
    )

    run.require(
        interval_entropy(gens, 2, 8) == 4 and interval_mincut(2, 8) == 5,

        "witness (2, 8)",
    )
    run.require(
        interval_entropy(gens, 2, 12) == 4 and interval_mincut(2, 12) == 5,

        "witness (2, 12)",
    )
    for k in range(5):
        s_k = 4 * k + 2
        run.require(
            interval_entropy(gens, s_k, 8) == 4 and interval_mincut(s_k, 8) == 5,

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
            run.require(s_val <= m_val, f"S <= mincut at ({start}, {length})")
            if s_val == m_val:
                ex_count += 1
            elif s_val + 1 == m_val:
                def_count += 1
        total_exact += ex_count
        total_deficit += def_count
        run.require(
            def_count == expected_deficits_by_len[length] and ex_count + def_count == 20,

            f"deficit count at len={length}: got {def_count}",
        )

    run.require(total_exact == 340 and total_deficit == 40, "340 exact and 40 deficit")
    return gens


def check_mutual_information_and_codimension(run: Cases, gens: object) -> None:
    run.require(
        region_entropy(gens, [0]) == 1
        and region_entropy(gens, [8]) == 1
        and region_mutual_information(gens, [0], [8]) == 0,

        "I([0] : [8]) == 0",
    )
    p0 = [0, 1, 2, 3]
    p1 = [4, 5, 6, 7]
    p2 = [8, 9, 10, 11]
    run.require(
        region_entropy(gens, p0) == 1
        and region_entropy(gens, p2) == 1
        and region_entropy(gens, p0 + p2) == 2
        and region_mutual_information(gens, p0, p2) == 0,

        "I(P0 : P2) == 0",
    )
    run.require(
        region_entropy(gens, [0, 1]) == 2
        and region_entropy(gens, [2, 3]) == 2
        and region_mutual_information(gens, [0, 1], [2, 3]) == 3,

        "I([0,1] : [2,3]) == 3",
    )
    run.require(
        region_entropy(gens, p0 + p1) == 2
        and region_entropy(gens, p0 + p1 + p2) == 2
        and region_mutual_information(gens, p0 + p1, p2) == 1,

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
        run.require(
            d_bulk == exp_bulk and d_bdry == exp_bdry and codim == exp_codim and codim > 0,

            f"codim({n_bulk}, {n_bdry})",
        )


def main() -> int:
    renyi, mincut, mi_codim = Cases(), Cases(), Cases()
    check_renyi_factors(renyi)
    gens = check_interval_census(mincut)
    check_mutual_information_and_codimension(mi_codim, gens)
    checks = renyi.checks + mincut.checks + mi_codim.checks
    print(f"ads-happy-toy-not-duality-gap independent check: checks={checks} "
          f"renyi={renyi.checks} mincut={mincut.checks} mi_codim={mi_codim.checks} failures=0")
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
    return 0


if __name__ == "__main__":
    raise SystemExit(cli(main))
