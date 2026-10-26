#!/usr/bin/env python3
"""Profile exact bit-length growth under projective coordinate scaling (homogeneous integer arithmetic).

Evaluates whether clearing denominators avoids Phase 1 common denominator swell.
AuthorityEffect: None.
"""

from __future__ import annotations

import json
import random
import sys
import time
from fractions import Fraction
from pathlib import Path

# Add code/ to sys.path
CODE_DIR = Path(__file__).resolve().parent.parent / "code"
if str(CODE_DIR) not in sys.path:
    sys.path.insert(0, str(CODE_DIR))

from witnessed_difference.cochains import FiniteComplex
from witnessed_difference.obstruction import (
    DEFAULT_PIVOT_BUDGET,
    d0_matrix,
    solve_standard_lp,
    verify_standard_lp,
)
from witnessed_difference.outcomes import Accepted


def max_matrix_bitlength(matrix: list[list[Fraction]]) -> int:
    max_b = 0
    for row in matrix:
        for val in row:
            if val != 0:
                max_b = max(max_b, val.numerator.bit_length(), val.denominator.bit_length())
    return max_b


def run_projective_profile(n: int, bit_len: int, seed: int = 42) -> dict:
    rng = random.Random(seed + n * 1000 + bit_len)
    vertices = tuple(f"v{i}" for i in range(n))
    edges = tuple((f"v{i}", f"v{j}") for i in range(n) for j in range(i + 1, n))
    comp = FiniteComplex(vertices, edges)
    m = len(edges)
    width = len(vertices)
    w = (Fraction(1),) * m

    cochain = [
        Fraction(rng.randint(-(1 << bit_len), 1 << bit_len), rng.randint(1, 1 << bit_len))
        for _ in edges
    ]
    d = d0_matrix(comp)

    # 1. Standard formulation
    rows_std = [
        list(row) + [-entry for entry in row] + [Fraction(int(i == k)) for k in range(m)]
        + [-Fraction(int(i == k)) for k in range(m)]
        for i, row in enumerate(d)
    ]
    costs = [Fraction(0)] * (2 * width) + list(w) + list(w)

    std_phase1_sum = sum((abs(x) for x in cochain), start=Fraction(0))
    std_phase1_bits = max(std_phase1_sum.numerator.bit_length(), std_phase1_sum.denominator.bit_length())

    # 2. Projective row-wise denominator clearing
    rows_proj = []
    cochain_proj = []
    for i in range(m):
        q_i = cochain[i].denominator
        rows_proj.append([q_i * val for val in rows_std[i]])
        cochain_proj.append(cochain[i].numerator)

    proj_phase1_sum = sum((abs(b.numerator) for b in cochain), start=0)
    proj_phase1_bits = proj_phase1_sum.bit_length()

    # Time and solve both
    t0_std = time.perf_counter()
    sol_std = solve_standard_lp(costs, rows_std, cochain, max_pivots=DEFAULT_PIVOT_BUDGET)
    t1_std = time.perf_counter()

    t0_proj = time.perf_counter()
    sol_proj = solve_standard_lp(costs, rows_proj, cochain_proj, max_pivots=DEFAULT_PIVOT_BUDGET)
    t1_proj = time.perf_counter()

    assert isinstance(sol_std, Accepted)
    assert isinstance(sol_proj, Accepted)
    assert verify_standard_lp(costs, rows_std, cochain, sol_std.value)
    assert verify_standard_lp(costs, rows_proj, cochain_proj, sol_proj.value)
    assert sol_std.value.value == sol_proj.value.value

    return {
        "n": n,
        "edges_m": m,
        "input_bits": bit_len,
        "std_phase1_bits": std_phase1_bits,
        "proj_phase1_bits": proj_phase1_bits,
        "reduction_factor": round(std_phase1_bits / max(1, proj_phase1_bits), 2),
        "std_pivots": sol_std.value.pivots,
        "proj_pivots": sol_proj.value.pivots,
        "std_time_sec": round(t1_std - t0_std, 4),
        "proj_time_sec": round(t1_proj - t0_proj, 4),
        "exact_match": True,
    }


def main():
    print("# Exact Projective Coordinate Scaling Bit-Length Growth Profile")
    print("AuthorityEffect: None.\n")

    test_configs = [
        (4, 16), (4, 32), (4, 64),
        (6, 16), (6, 32), (6, 64),
        (8, 16), (8, 32), (8, 64),
        (10, 16), (10, 32), (10, 64),
        (12, 16), (12, 32), (12, 64),
    ]

    print("| n | Edges (m) | Input Bits | Std Phase 1 Bits | Proj Phase 1 Bits | Reduction Factor | Std Pivots | Proj Pivots | Std Time (s) | Proj Time (s) |")
    print("|---|-----------|------------|------------------|-------------------|------------------|------------|-------------|--------------|---------------|")

    records = []
    for n, bits in test_configs:
        res = run_projective_profile(n, bits)
        records.append(res)
        print(
            f"| {res['n']:2d} | {res['edges_m']:9d} | {res['input_bits']:10d} | "
            f"{res['std_phase1_bits']:16d} | {res['proj_phase1_bits']:17d} | "
            f"{res['reduction_factor']:15.1f}x | {res['std_pivots']:10d} | "
            f"{res['proj_pivots']:11d} | {res['std_time_sec']:12.4f} | {res['proj_time_sec']:13.4f} |"
        )

    out_path = Path(__file__).resolve().parent.parent / "evidence" / "projective_scaling_profile.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "authority_effect": "None",
                "claim": "WDP-CH04-P04",
                "description": "Projective row-wise denominator clearing eliminates Phase 1 common denominator swell",
                "records": records,
            },
            f,
            indent=2,
        )
    print(f"\nProfile evidence written to: {out_path}")


if __name__ == "__main__":
    main()
