#!/usr/bin/env python3
"""Independent executable check for FSP-HINGE-LINEON-SIGN-CLAIM (TFQ-1219).

Checks in exact integer/rational arithmetic:
1. Open 1D hinge chain (L in {4, 5, 6, 7}, N in {2, 3, 4}):
   - Every non-colliding, non-crossing nearest-neighbor step preserves strict
     site ordering x_1 < x_2 < ... < x_N.
   - In the canonical ordered Fock basis |x_1 < ... < x_N>, every nearest-neighbor
     hop on an open chain passes over 0 occupied intermediate sites, so every
     off-diagonal matrix element of (-H_open) is >= 0 and every closed worldline
     walk has positive sign +1.
2. Scope Fence 1 — Periodic 1D hinge ring (L in {4, 5, 6, 7}):
   - On a closed 1D hinge loop with boundary bond (L-1, 0), hopping a fermion
     between site 0 and site L-1 passes over (N - 1) intermediate fermions;
     for even N in {2, 4}, (-1)^(N-1) = -1 < 0, producing negative closed-loop
     worldline weights.
3. Scope Fence 2 — Intersecting 1D hinges (T-junction and 3D cubic 6-valent junction):
   - In the exact 2-fermion Fock basis on a 4-vertex T-junction {0, 1, 2, 3}
     (center 1 joined to 0, 2, 3), the 6-step exchange loop exchanging two
     fermions via branch vertex 3 has product of Jordan-Wigner hop signs equal
     to -1 < 0.
4. Scope Fence 3 & 4 — Corner lineon turn & non-abelian 2-gauge hinge commutator:
   - Exact 2x2 matrix group commutator J D J^{-1} D^{-1} = -I_2 has trace -2 < 0
     and defect mass Phi_1 = 2 > 0, matching FoliatedFractonEngine.
"""

from __future__ import annotations

import itertools
import sys
from pathlib import Path

import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "python" / "src"))

from fsp.foliated_fracton_2gauge_defects import (  # noqa: E402
    FoliatedFractonConfig,
    FoliatedFractonEngine,
)


def jw_hop_sign(state: tuple[int, ...], u: int, v: int) -> tuple[tuple[int, ...] | None, int]:
    """Apply fermion hop from occupied site u to empty site v in canonical ordered tuple state."""
    if u not in state or v in state:
        return None, 0
    lo, hi = (u, v) if u < v else (v, u)
    between = sum(1 for s in state if lo < s < hi)
    sign = -1 if (between % 2 == 1) else 1
    new_state = tuple(sorted(s if s != u else v for s in state))
    return new_state, sign


def main() -> int:
    checks = 0
    failures = 0
    open_chain_checks = 0
    ring_checks = 0
    junction_checks = 0
    holonomy_checks = 0

    def record(cond: bool, bucket: str, msg: str) -> None:
        nonlocal checks, failures, open_chain_checks, ring_checks, junction_checks, holonomy_checks
        checks += 1
        if bucket == "open":
            open_chain_checks += 1
        elif bucket == "ring":
            ring_checks += 1
        elif bucket == "junction":
            junction_checks += 1
        else:
            holonomy_checks += 1
        if not cond:
            failures += 1
            print(f"FAIL: {msg}", file=sys.stderr)

    # 1. Open 1D chain: order preservation and positive JW nearest-neighbor hop signs
    for L in (4, 5, 6, 7):
        open_bonds = [(i, i + 1) for i in range(L - 1)] + [(i + 1, i) for i in range(L - 1)]
        for N in (2, 3, 4):
            if N >= L:
                continue
            states = list(itertools.combinations(range(L), N))
            for st in states:
                for u, v in open_bonds:
                    new_st, sgn = jw_hop_sign(st, u, v)
                    if new_st is not None:
                        record(
                            sgn == 1 and list(new_st) == sorted(new_st),
                            "open",
                            f"Open chain L={L} N={N} state={st} hop ({u}->{v}) gave sign {sgn}",
                        )

    # Exhaustive check of two-particle simultaneous nearest-neighbor steps on Z in [-4, 4]
    for x1 in range(-4, 4):
        for x2 in range(x1 + 1, 5):
            for d1 in (-1, 0, 1):
                for d2 in (-1, 0, 1):
                    y1, y2 = x1 + d1, x2 + d2
                    if y1 == y2:
                        continue
                    if y1 == x2 and y2 == x1:
                        continue
                    record(
                        y1 < y2,
                        "open",
                        f"Order violated for ({x1},{x2}) + ({d1},{d2}) -> ({y1},{y2})",
                    )

    # 2. Scope Fence 1: Periodic 1D hinge ring cyclic winding sign (-1)^(N-1)
    for L in (4, 5, 6, 7):
        for N in (2, 3, 4):
            if N >= L:
                continue
            # Start at state (0, 1, ..., N-1)
            # Move particle at N-1 to L-1 in (L - N) open-bond steps, then hop L-1 -> 0, etc.
            # Specifically, boundary hop from u = L-1 to v = 0 when {1, ..., N-1} are occupied:
            b_state = tuple(range(1, N)) + (L - 1,)
            after_b, b_sgn = jw_hop_sign(b_state, L - 1, 0)
            expected_sgn = -1 if ((N - 1) % 2 == 1) else 1
            record(
                after_b == tuple(range(N)) and b_sgn == expected_sgn,
                "ring",
                f"Periodic ring L={L} N={N} boundary hop sign {b_sgn} != {expected_sgn}",
            )
            if N % 2 == 0:
                record(
                    b_sgn == -1,
                    "ring",
                    f"Even N={N} on periodic ring L={L} should give negative sign -1",
                )

    # 3. Scope Fence 2: Intersecting 1D hinges (T-junction and 6-valent cubic vertex)
    # T-junction vertices {0, 1, 2, 3} with center 1 connected to 0, 2, 3
    # Sequence of single-fermion hops executing a 2-fermion exchange loop from (0, 2) back to (0, 2):
    t_hops = [
        (0, 1),  # (0, 2) -> (1, 2), sign +1
        (1, 3),  # (1, 2) -> (2, 3), sign -1 (passes over occupied site 2!)
        (2, 1),  # (2, 3) -> (1, 3), sign +1
        (1, 0),  # (1, 3) -> (0, 3), sign +1
        (3, 1),  # (0, 3) -> (0, 1), sign +1
        (1, 2),  # (0, 1) -> (0, 2), sign +1
    ]
    cur = (0, 2)
    loop_sign = 1
    for u, v in t_hops:
        nxt, sgn = jw_hop_sign(cur, u, v)
        record(nxt is not None, "junction", f"Invalid T-junction hop {u}->{v} from {cur}")
        assert nxt is not None
        loop_sign *= sgn
        cur = nxt
    record(
        cur == (0, 2) and loop_sign == -1,
        "junction",
        f"T-junction 6-step closed exchange loop should return to (0,2) with sign -1, got {cur}, {loop_sign}",
    )

    # Also test all 4-tuples of vertices (a < center < b < branch) in a 3D cubic lattice junction (7 vertices: center + 6 neighbors)
    for center in range(1, 5):
        for a in range(center):
            for b in range(center + 1, 6):
                for branch in range(b + 1, 7):
                    hops = [(a, center), (center, branch), (b, center), (center, a), (branch, center), (center, b)]
                    c_st = (a, b)
                    c_sgn = 1
                    for u, v in hops:
                        nxt, s = jw_hop_sign(c_st, u, v)
                        assert nxt is not None
                        c_sgn *= s
                        c_st = nxt
                    record(
                        c_st == (a, b) and c_sgn == -1,
                        "junction",
                        f"Junction loop ({a},{center},{b},{branch}) failed negative sign check",
                    )

    # 4. Scope Fence 3 & 4: Corner lineon turn & non-abelian 2-gauge hinge commutator
    J = np.array([[0, 1], [-1, 0]], dtype=np.int64)
    D = np.array([[1, 0], [0, -1]], dtype=np.int64)
    J_inv = -J
    D_inv = D
    comm = J @ D @ J_inv @ D_inv
    record(
        np.array_equal(comm, -np.eye(2, dtype=np.int64)) and int(np.trace(comm)) == -2,
        "holonomy",
        "2x2 group commutator J D J^-1 D^-1 != -I_2 or trace != -2",
    )

    engine = FoliatedFractonEngine(
        FoliatedFractonConfig(lx=6, ly=6, lz=6, kappa_subsystem_penalty=2.0)
    )
    ab_res = engine.evaluate_intersecting_2gauge_defects(is_nonabelian=False)
    nab_res = engine.evaluate_intersecting_2gauge_defects(is_nonabelian=True)
    record(
        ab_res.details["trace"] == 2.0 and ab_res.average_sign == 1.0,
        "holonomy",
        "Abelian 2-gauge hinge trace should be +2.0",
    )
    record(
        nab_res.details["trace"] == -2.0
        and nab_res.defect_mass_phi1 == 2.0
        and nab_res.average_sign == -1.0
        and not nab_res.is_foliated_projection_successful,
        "holonomy",
        "Non-abelian 2-gauge hinge trace should be -2.0 with defect mass 2.0",
    )

    corner_ok = engine.evaluate_foliated_categorical_projection(has_corner_lineon_turn=False)
    corner_bad = engine.evaluate_foliated_categorical_projection(has_corner_lineon_turn=True)
    record(
        corner_ok.details["projected_trace"] == 4.0 and corner_ok.is_foliated_projection_successful,
        "holonomy",
        "Decoupled foliated projection trace should be +4.0",
    )
    record(
        corner_bad.details["projected_trace"] == -2.0
        and corner_bad.defect_mass_phi1 == 2.0
        and not corner_bad.is_foliated_projection_successful,
        "holonomy",
        "Corner lineon turn projection trace should be -2.0",
    )

    print(
        f"checks={checks} open_chain={open_chain_checks} periodic_ring={ring_checks} "
        f"intersecting_junctions={junction_checks} holonomy_fences={holonomy_checks} failures={failures}"
    )
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
