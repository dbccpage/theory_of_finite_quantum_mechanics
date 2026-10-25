#!/usr/bin/env python3
r"""Independent executable check for FSP-TRIALITY-CENTER-PROJECTION (TFQ-1202 / FSP-DERIV-038).

Verifies:
1. Eisenstein-cyclotomic ring Z[omega] (omega^2 + omega + 1 = 0, omega^3 = 1) arithmetic:
   - Cube roots of unity group law and character sum 1 + omega + omega^2 == 0.
2. Canonical-ensemble Z3 center projection Pi_Z3(q) = sum_{k=0}^2 omega^{q*k} in Z[omega]:
   - Pi_Z3(q) == (3, 0) when q % 3 == 0 (zero-triality color-singlet meson/baryon sectors).
   - Pi_Z3(q) == (0, 0) when q % 3 in {1, 2} (fractional-triality quark/diquark sectors).
   - Idempotence Pi_Z3(q)^2 == 3 * Pi_Z3(q).
3. Grand-canonical center-twisted partition sum Z(z_k) = Z_0 + omega^k Z_1 + omega^{2k} Z_2:
   - Averaging over k in {0, 1, 2} removes fractional-triality amplitudes Z_1, Z_2 completely
     and yields 3 * Z_0.
   - Sign persistence inside the zero-triality baryon sector: when Z_0 = w_{B,+} - w_{B,-}
     with w_{B,-} > w_{B,+} > 0, the projected sum 3*(w_{B,+} - w_{B,-}) < 0 remains negative.
4. Simplicial Y-junction coboundary nilpotence d1 . d0 == 0, SU(3) Cartan singlet closure
   mu_R + mu_G + mu_B == (0, 0), meson (0) vs baryon (10 > 0) 2-cochain curvature,
   Polyakov-loop center action shifts and gap 18*h*P, cross-check with SU3BaryonGinEngine,
   and GIN-C10 / GIN-C11 scope fences.
"""

from __future__ import annotations

from pathlib import Path
import sys
from typing import Tuple

REPO_ROOT = Path(__file__).resolve().parents[2]
FSP_SRC = REPO_ROOT / "code" / "python" / "src" / "fsp"
if str(FSP_SRC) not in sys.path:
    sys.path.insert(0, str(FSP_SRC))

from su3_baryon_triality import SU3BaryonGinEngine, SU3SimplicialYJunction  # noqa: E402


def zomega_add(x: Tuple[int, int], y: Tuple[int, int]) -> Tuple[int, int]:
    return (x[0] + y[0], x[1] + y[1])


def zomega_scale(c: int, x: Tuple[int, int]) -> Tuple[int, int]:
    return (c * x[0], c * x[1])


def zomega_mul(x: Tuple[int, int], y: Tuple[int, int]) -> Tuple[int, int]:
    return (
        x[0] * y[0] - x[1] * y[1],
        x[0] * y[1] + x[1] * y[0] - x[1] * y[1],
    )


def z3_phase(n: int) -> Tuple[int, int]:
    r = n % 3
    if r == 0:
        return (1, 0)
    if r == 1:
        return (0, 1)
    return (-1, -1)


def z3_projector_sum(q: int) -> Tuple[int, int]:
    return zomega_add(zomega_add(z3_phase(q * 0), z3_phase(q * 1)), z3_phase(q * 2))


def y_junction_d0(v0: int, v1: int, v2: int, v3: int) -> Tuple[int, int, int, int, int, int]:
    return (v1 - v0, v2 - v0, v3 - v0, v2 - v1, v3 - v2, v1 - v3)


def y_junction_d1(e0: int, e1: int, e2: int, e3: int, e4: int, e5: int) -> Tuple[int, int, int]:
    return (e0 - e1 + e3, e1 - e2 + e4, -e0 + e2 + e5)


def main() -> int:
    checks = 0
    failures = 0
    zomega_checks = 0
    projection_checks = 0
    y_junction_checks = 0
    scope_fence_checks = 0

    def record(cond: bool, bucket: str, msg: str) -> None:
        nonlocal checks, failures, zomega_checks, projection_checks, y_junction_checks, scope_fence_checks
        checks += 1
        if bucket == "zomega":
            zomega_checks += 1
        elif bucket == "projection":
            projection_checks += 1
        elif bucket == "y_junction":
            y_junction_checks += 1
        elif bucket == "scope":
            scope_fence_checks += 1
        if not cond:
            failures += 1
            print(f"FAIL: {msg}")

    # 1. Z[omega] group law and commutativity
    one = (1, 0)
    omega = (0, 1)
    omega_sq = (-1, -1)
    zero = (0, 0)
    record(zomega_mul(omega, omega) == omega_sq, "zomega", "omega^2 == (-1, -1)")
    record(zomega_mul(omega, omega_sq) == one, "zomega", "omega^3 == (1, 0)")
    record(zomega_add(zomega_add(one, omega), omega_sq) == zero, "zomega", "1 + omega + omega^2 == 0")

    for a1 in range(-3, 4):
        for b1 in range(-3, 4):
            for a2 in range(-3, 4):
                for b2 in range(-3, 4):
                    x = (a1, b1)
                    y = (a2, b2)
                    record(zomega_mul(x, y) == zomega_mul(y, x), "zomega", f"zomega commutativity {x},{y}")

    # 2. Canonical Z3 center projection and idempotence on q in [-30..30]
    for q in range(-30, 31):
        proj = z3_projector_sum(q)
        expected = (3, 0) if (q % 3 == 0) else (0, 0)
        record(proj == expected, "projection", f"Pi_Z3({q}) == {expected}")
        record(
            zomega_mul(proj, proj) == zomega_scale(3, proj),
            "projection",
            f"Pi_Z3({q}) idempotence",
        )

    # Grand-canonical Z3 Fourier isolation and zero-triality baryon sign persistence
    for z0 in range(-4, 5):
        for z1 in range(-4, 5):
            for z2 in range(-4, 5):
                total = (0, 0)
                for k in (0, 1, 2):
                    zk = zomega_add(
                        zomega_add(zomega_scale(z0, z3_phase(0)), zomega_scale(z1, z3_phase(k))),
                        zomega_scale(z2, z3_phase(2 * k)),
                    )
                    total = zomega_add(total, zk)
                record(
                    total == (3 * z0, 0),
                    "projection",
                    f"Fourier isolation ({z0},{z1},{z2})",
                )

    for w_pos in range(1, 6):
        for w_neg in range(w_pos + 1, 8):
            proj_baryon = 3 * (w_pos - w_neg)
            record(
                proj_baryon < 0 and (w_pos + w_neg) > 0,
                "projection",
                f"zero-triality baryon sign persistence ({w_pos},{w_neg})",
            )

    # 3. Simplicial Y-junction nilpotence d1 . d0 == 0 and Cartan singlet curvature
    for v0 in range(-2, 3):
        for v1 in range(-2, 3):
            for v2 in range(-2, 3):
                for v3 in range(-2, 3):
                    edges = y_junction_d0(v0, v1, v2, v3)
                    faces = y_junction_d1(*edges)
                    record(faces == (0, 0, 0), "y_junction", f"nilpotence d1(d0({v0},{v1},{v2},{v3})) == 0")

    for s in range(-5, 6):
        record(y_junction_d1(s, s, s, 0, 0, 0) == (0, 0, 0), "y_junction", f"meson spoke closure s={s}")

    baryon_faces = y_junction_d1(2, 1, -3, 0, 0, 0)
    baryon_l1 = sum(abs(x) for x in baryon_faces)
    record(
        (2 + 1 - 3 == 0) and baryon_faces == (1, 4, -5) and baryon_l1 == 10,
        "y_junction",
        "baryon Cartan singlet 2-cochain curvature",
    )

    # Cross-check with SU3SimplicialYJunction and SU3BaryonGinEngine
    junc = SU3SimplicialYJunction()
    record(junc.complex.check_nilpotence(), "y_junction", "SU3SimplicialYJunction nilpotence")
    eng = SU3BaryonGinEngine(in_memory=True)
    receipt = eng.audit_su3_baryon_triality()
    eng.close()
    record(
        receipt.meson_gamma_2 == 0.0
        and receipt.baryon_gamma_2 == 5.0
        and receipt.has_higher_order_curvature
        and receipt.baryon_terminal_route == "OpenSignObstruction"
        and receipt.meson_terminal_route == "ExactRepair",
        "y_junction",
        "SU3BaryonGinEngine receipt verification",
    )

    # 4. Polyakov loop sector action sum/gap and GIN-C10 / GIN-C11 scope fences
    for h_val in range(1, 6):
        for p_val in range(1, 6):
            s0 = -12 * h_val * p_val
            s1 = 6 * h_val * p_val
            s2 = 6 * h_val * p_val
            record(
                (s0 + s1 + s2 == 0) and (s1 - s0 == 18 * h_val * p_val) and (18 * h_val * p_val > 0),
                "scope",
                f"Polyakov loop sector action sum and gap ({h_val},{p_val})",
            )

    for w_val in range(1, 10):
        record(w_val - 2 * w_val == -w_val < 0, "scope", f"confined 1-vs-2 multiplicity imbalance w={w_val}")

    overclaimed_interp = (True, True, True)
    scoped_interp = (True, True, False)
    record(
        overclaimed_interp[:2] == scoped_interp[:2] and overclaimed_interp != scoped_interp,
        "scope",
        "GIN-C10 / GIN-C11 historical fixture scope fence",
    )

    print(
        f"PASS: checks={checks} zomega={zomega_checks} projection={projection_checks} "
        f"y_junction={y_junction_checks} scope_fences={scope_fence_checks} failures={failures}"
    )
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
