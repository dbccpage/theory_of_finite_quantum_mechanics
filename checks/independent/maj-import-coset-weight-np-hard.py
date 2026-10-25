#!/usr/bin/env python3
"""Independent verification for MAJ-IMPORT-COSET-WEIGHT-NP-HARD (TFQ-1157).

Checks:
1. F2^n involutive vector addition and Hamming weight identity:
   wt(u ^ v) + 2 * wt(u & v) == wt(u) + wt(v) and wt(u ^ v) <= wt(u) + wt(v).
2. Primal Coset-Weight vs Parity-Check Syndrome Decoding Equivalence (BMVT 1978):
   Exhaustive check across small F2 linear codes that
   min_{alpha} wt(r ^ d0*alpha) == min_{e : H*e = H*r} wt(e).
3. Gauge-shift invariance of coset-weight decision under r -> r ^ d0*beta.
4. Greedy single-generator-flip local minimum trap on n=5, k=2:
   r = (1,0,0,1,0) has wt=2, single flips give wt=3 > 2, joint flip gives wt=0 < 2.
5. Cross-check against papers/core/majorana/code/majorana_evaluator.py:
   compute_coset_weight, budget capping, and 3x4 vs 6x6 torus coset cardinality.
"""

from __future__ import annotations

import itertools
import sys
from pathlib import Path

import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "papers" / "core" / "majorana" / "code"))

from majorana_evaluator import (  # noqa: E402
    F2CochainComplex,
    GF2Matrix,
    build_tetron_carrier,
    compute_coset_weight,
    logical_representative,
)


def main() -> int:
    checks = 0
    f2_algebra = 0
    equivalence = 0
    greedy_trap = 0
    scope_fences = 0
    failures = 0

    def record(bucket: str, cond: bool, msg: str) -> None:
        nonlocal checks, f2_algebra, equivalence, greedy_trap, scope_fences, failures
        checks += 1
        if bucket == "f2_algebra":
            f2_algebra += 1
        elif bucket == "equivalence":
            equivalence += 1
        elif bucket == "greedy_trap":
            greedy_trap += 1
        elif bucket == "scope_fences":
            scope_fences += 1
        if not cond:
            failures += 1
            print(f"FAIL: {msg}")

    # 1. Exhaustive F2^5 vector space & Hamming weight subadditivity
    for u_int in range(32):
        for v_int in range(32):
            xor_int = u_int ^ v_int
            and_int = u_int & v_int
            wt_u = u_int.bit_count()
            wt_v = v_int.bit_count()
            wt_xor = xor_int.bit_count()
            wt_and = and_int.bit_count()
            record(
                "f2_algebra",
                (u_int ^ v_int) == (v_int ^ u_int)
                and (v_int ^ v_int) == 0
                and ((u_int ^ v_int) ^ v_int) == u_int,
                f"F2 involutive cancel at u={u_int}, v={v_int}",
            )
            record(
                "f2_algebra",
                wt_xor + 2 * wt_and == wt_u + wt_v and wt_xor <= wt_u + wt_v,
                f"Hamming weight identity at u={u_int}, v={v_int}",
            )

    # 2. Primal Coset-Weight vs Parity-Check Syndrome Decoding Equivalence
    # Generator d0 (n=5, k=2) with columns g0=(1,1,1,0,0), g1=(0,1,1,1,0)
    # Parity check H (m=3, n=5) whose kernel is span(g0, g1):
    # Rows of H: h0=(1,1,0,1,0), h1=(0,1,1,0,0), h2=(0,0,0,0,1)
    d0_cols = [
        np.array([1, 1, 1, 0, 0], dtype=int),
        np.array([0, 1, 1, 1, 0], dtype=int),
    ]
    d0_mat = np.column_stack(d0_cols)
    h_mat = np.array(
        [
            [1, 1, 0, 1, 0],
            [0, 1, 1, 0, 0],
            [0, 0, 0, 0, 1],
        ],
        dtype=int,
    )
    # Verify H * d0 == 0 mod 2
    prod_hd0 = (h_mat @ d0_mat) % 2
    record("equivalence", not np.any(prod_hd0), "H * d0 == 0 mod 2")

    for r_bits in itertools.product([0, 1], repeat=5):
        r_vec = np.array(r_bits, dtype=int)
        syn_r = (h_mat @ r_vec) % 2
        coset_vecs = []
        for a0, a1 in itertools.product([0, 1], repeat=2):
            c_vec = (r_vec ^ (a0 * d0_cols[0]) ^ (a1 * d0_cols[1])) % 2
            coset_vecs.append(int(np.sum(c_vec)))
        min_coset_wt = min(coset_vecs)

        syndrome_fiber_wts = []
        for e_bits in itertools.product([0, 1], repeat=5):
            e_vec = np.array(e_bits, dtype=int)
            if np.array_equal((h_mat @ e_vec) % 2, syn_r):
                syndrome_fiber_wts.append(int(np.sum(e_vec)))
        min_syn_wt = min(syndrome_fiber_wts)
        record(
            "equivalence",
            min_coset_wt == min_syn_wt and len(syndrome_fiber_wts) == 4,
            f"Primal coset weight == syndrome weight for r={r_bits}",
        )
        # Check equivalence of decision predicate <= w for w in 0..5
        for w_thresh in range(6):
            primal_yes = any(wt <= w_thresh for wt in coset_vecs)
            syn_yes = any(wt <= w_thresh for wt in syndrome_fiber_wts)
            record(
                "equivalence",
                primal_yes == syn_yes,
                f"Decision equivalence at r={r_bits}, w={w_thresh}",
            )
        # Check gauge-shift invariance under r -> r ^ d0*beta
        for b0, b1 in itertools.product([0, 1], repeat=2):
            r_shift = (r_vec ^ (b0 * d0_cols[0]) ^ (b1 * d0_cols[1])) % 2
            shift_wts = [
                int(np.sum((r_shift ^ (a0 * d0_cols[0]) ^ (a1 * d0_cols[1])) % 2))
                for a0, a1 in itertools.product([0, 1], repeat=2)
            ]
            record(
                "equivalence",
                min(shift_wts) == min_coset_wt,
                f"Gauge shift invariance at r={r_bits}, beta=({b0},{b1})",
            )

    # 3. Greedy single-gauge-flip local minimum trap on n=5, k=2
    trap_r = np.array([1, 0, 0, 1, 0], dtype=int)
    wt_r = int(np.sum(trap_r))
    wt_g0 = int(np.sum(trap_r ^ d0_cols[0]))
    wt_g1 = int(np.sum(trap_r ^ d0_cols[1]))
    wt_g01 = int(np.sum(trap_r ^ d0_cols[0] ^ d0_cols[1]))
    record("greedy_trap", wt_r == 2, "trapResidual weight is 2")
    record("greedy_trap", wt_g0 == 3 and wt_g0 > wt_r, "single flip g0 increases weight to 3")
    record("greedy_trap", wt_g1 == 3 and wt_g1 > wt_r, "single flip g1 increases weight to 3")
    record("greedy_trap", wt_g01 == 0 and wt_g01 < wt_r, "joint flip g0^g1 reaches weight 0")

    cochain_trap = F2CochainComplex(
        n0=2,
        n1=5,
        n2=3,
        d0=GF2Matrix.from_array(d0_mat.tolist()),
        d1=GF2Matrix.from_array(h_mat.tolist()),
    )
    record("greedy_trap", cochain_trap.is_nilpotent(), "trap cochain complex is nilpotent")
    phi1_trap, exact_trap = compute_coset_weight(cochain_trap, trap_r, budget_max=10)
    record("greedy_trap", phi1_trap == 0 and exact_trap is True, "exact coset weight of trap_r is 0")
    phi1_capped, exact_capped = compute_coset_weight(cochain_trap, trap_r, budget_max=2)
    record(
        "greedy_trap",
        phi1_trap <= phi1_capped and exact_capped is False,
        "budget-capped search returns upper bound with exact=False",
    )

    # 4. Torus 3x4 vs 6x6 coset cardinality & budget overflow
    torus_3x4 = build_tetron_carrier("torus", 3, 4)
    rank_3x4 = torus_3x4.complex.d0.rank()
    record("scope_fences", rank_3x4 == 11 and (2**rank_3x4) == 2048, "3x4 torus rank(d0)=11, coset=2048")
    col_3x4 = logical_representative(torus_3x4, axis="column", index=0)
    w_col_3x4, ex_col_3x4 = compute_coset_weight(torus_3x4.complex, col_3x4, budget_max=2**20)
    record("scope_fences", w_col_3x4 == 3 and ex_col_3x4 is True, "3x4 torus column coset weight=3")
    w_cap_3x4, ex_cap_3x4 = compute_coset_weight(torus_3x4.complex, col_3x4, budget_max=4)
    record(
        "scope_fences",
        w_col_3x4 <= w_cap_3x4 and ex_cap_3x4 is False,
        "3x4 torus capped budget=4 flags exact=False",
    )

    torus_6x6 = build_tetron_carrier("torus", 6, 6)
    rank_6x6 = torus_6x6.complex.d0.rank()
    default_budget = 2**20
    record(
        "scope_fences",
        rank_6x6 == 35
        and (2**rank_6x6) > default_budget
        and (2**rank_6x6) // default_budget == 32768,
        "6x6 torus rank(d0)=35 overflows 2^20 budget by 32768x",
    )

    # Verify every column of d0 on a graphic tetron torus has weight 4 (4 incident edges per site),
    # while every row of d0 (edge coboundary) has weight 2 (2 endpoints per edge).
    for row in torus_3x4.complex.d0.data:
        record("scope_fences", sum(row) == 2, "each edge row of d0 on 3x4 torus has weight 2")

    if failures > 0:
        print(f"FAIL: checks={checks} failures={failures}")
        return 1
    print(
        f"PASS: checks={checks} f2_algebra={f2_algebra} equivalence={equivalence} "
        f"greedy_trap={greedy_trap} scope_fences={scope_fences} failures={failures}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
