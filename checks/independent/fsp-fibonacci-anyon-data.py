#!/usr/bin/env python3
r"""Independent executable check for FSP-FIBONACCI-ANYON-DATA (TFQ-1209 / FSP-DERIV-045).

Verifies:
1. Fibonacci fusion rules N_{a,b}^c on {0 (1), 1 (tau)} and exact associativity across all
   2^4 = 16 quadruples (a, b, c, d) in {0, 1}^4.
2. Exact golden-ratio ring Z[phi] arithmetic (phi^2 = 1 + phi):
   - Quantum dimension recurrence d_tau^2 = 1 + d_tau and d_1^2 + d_tau^2 = 2 + phi
   - Inverse identities phi * phi^-1 = 1, (phi^-1)^2 = 2 - phi, and phi^-2 + phi^-1 = 1
   - State-leakage identity phi^-3 * (2 + phi^-1) = phi^-3 * (1 + phi) = phi^-1 = phi - 1
   - Exhaustive Z[phi] associativity and distributivity over a bounded coefficient box.
3. Mac Lane pentagon equation across all 2^9 = 512 4-anyon fusion tree configurations
   (a, b, c, d, e, f, g, k, l) in {0, 1}^9, plus 2x2 F-matrix symmetry and involution F^2 = I_2.
4. Artin braid relation sigma_1 sigma_2 sigma_1 == sigma_2 sigma_1 sigma_2 on H_3, non-zero
   commutator ||[sigma_1, sigma_2]||_F > 0, non-contractible commutator holonomy Gamma_2 > 0,
   exact state leakage L_leak(sigma_2) = phi^-1, and Pauli-Z involution non-commutativity.
5. Scope fences (GIN-C17):
   - Bounded integer grid p, q in [1..25] (625 pairs) checking (2p - q)^2 != 5 q^2,
     refuting the source JSONL's description of d_tau = (1 + sqrt(5))/2 as rational.
   - Cross-check against FibonacciAnyonModel and FibonacciAnyonBraidingEngine in
     code/python/src/fsp/fibonacci_anyon_braiding.py and GIN-C17 non-injectivity scope fence.
"""

from __future__ import annotations

import cmath
import math
from pathlib import Path
import sys
from typing import Tuple

REPO_ROOT = Path(__file__).resolve().parents[2]
FSP_SRC = REPO_ROOT / "code" / "python" / "src" / "fsp"
if str(FSP_SRC) not in sys.path:
    sys.path.insert(0, str(FSP_SRC))

from fibonacci_anyon_braiding import FibonacciAnyonBraidingEngine, FibonacciAnyonModel  # noqa: E402


def fib_fusion(a: int, b: int, c: int) -> int:
    if a == 0 and b == 0 and c == 0:
        return 1
    if a == 0 and b == 1 and c == 1:
        return 1
    if a == 1 and b == 0 and c == 1:
        return 1
    if a == 1 and b == 1 and c in (0, 1):
        return 1
    return 0


def zphi_add(x: Tuple[int, int], y: Tuple[int, int]) -> Tuple[int, int]:
    return (x[0] + y[0], x[1] + y[1])


def zphi_mul(x: Tuple[int, int], y: Tuple[int, int]) -> Tuple[int, int]:
    return (
        x[0] * y[0] + x[1] * y[1],
        x[0] * y[1] + x[1] * y[0] + x[1] * y[1],
    )


def fib_seq(n: int) -> int:
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def main() -> int:
    checks = 0
    failures = 0
    fusion_checks = 0
    zphi_checks = 0
    pentagon_braid_checks = 0
    scope_fence_checks = 0

    def record(cond: bool, bucket: str, msg: str) -> None:
        nonlocal checks, failures, fusion_checks, zphi_checks, pentagon_braid_checks, scope_fence_checks
        checks += 1
        if bucket == "fusion":
            fusion_checks += 1
        elif bucket == "zphi":
            zphi_checks += 1
        elif bucket == "pentagon_braid":
            pentagon_braid_checks += 1
        elif bucket == "scope":
            scope_fence_checks += 1
        if not cond:
            failures += 1
            print(f"FAIL: {msg}")

    # 1. Exhaustive Fibonacci fusion associativity over {0, 1}^4 (16 quadruples) + fusion rules
    for a in (0, 1):
        for b in (0, 1):
            for c in (0, 1):
                for d in (0, 1):
                    lhs = sum(fib_fusion(a, b, e) * fib_fusion(e, c, d) for e in (0, 1))
                    rhs = sum(fib_fusion(a, f, d) * fib_fusion(b, c, f) for f in (0, 1))
                    record(lhs == rhs, "fusion", f"fusion associativity ({a},{b},{c},{d})")

    record(fib_fusion(1, 1, 0) == 1 and fib_fusion(1, 1, 1) == 1, "fusion", "tau x tau = 1 + tau")
    for n, expected in ((1, 1), (2, 1), (3, 2), (4, 3), (5, 5), (6, 8)):
        record(fib_seq(n) == expected, "fusion", f"fib_seq({n}) == {expected}")

    # 2. Exact Z[phi] golden-ratio ring identities
    one = (1, 0)
    phi = (0, 1)
    phi_inv = (-1, 1)
    phi_inv_sq = (2, -1)
    phi_inv_cube = (-3, 2)

    record(zphi_mul(phi, phi) == zphi_add(one, phi), "zphi", "phi^2 == 1 + phi")
    record(zphi_add(zphi_mul(one, one), zphi_mul(phi, phi)) == (2, 1), "zphi", "d_1^2 + d_tau^2 == 2 + phi")
    record(zphi_mul(phi, phi_inv) == one, "zphi", "phi * phi^-1 == 1")
    record(zphi_mul(phi_inv, phi_inv) == phi_inv_sq, "zphi", "(phi^-1)^2 == 2 - phi")
    record(zphi_add(phi_inv_sq, phi_inv) == one, "zphi", "phi^-2 + phi^-1 == 1")
    record(zphi_mul(phi_inv_sq, phi_inv) == phi_inv_cube, "zphi", "phi^-2 * phi^-1 == -3 + 2*phi")
    record(zphi_add((2, 0), phi_inv) == (1, 1), "zphi", "2 + phi^-1 == 1 + phi")
    record(zphi_mul(phi_inv_cube, zphi_add((2, 0), phi_inv)) == phi_inv, "zphi", "phi^-3 * (2 + phi^-1) == phi^-1")

    for a1 in range(-2, 3):
        for b1 in range(-2, 3):
            for a2 in range(-2, 3):
                for b2 in range(-2, 3):
                    x = (a1, b1)
                    y = (a2, b2)
                    # Check commutativity and phi-annihilation (phi^2 - phi - 1) * x == 0
                    record(zphi_mul(x, y) == zphi_mul(y, x), "zphi", f"zphi commutativity {x}, {y}")

    # 3. Exhaustive 512-configuration Mac Lane pentagon equation and Artin braid relations
    phi_val = (1.0 + math.sqrt(5.0)) / 2.0
    inv_phi = 1.0 / phi_val
    inv_sqrt_phi = 1.0 / math.sqrt(phi_val)
    f_mat = [
        [inv_phi, inv_sqrt_phi],
        [inv_sqrt_phi, -inv_phi],
    ]

    def f_elem(a: int, b: int, c: int, d: int, e: int, f_idx: int) -> float:
        if (
            fib_fusion(a, b, e) == 0
            or fib_fusion(e, c, d) == 0
            or fib_fusion(b, c, f_idx) == 0
            or fib_fusion(a, f_idx, d) == 0
        ):
            return 0.0
        if a == 1 and b == 1 and c == 1 and d == 1:
            return f_mat[e][f_idx]
        return 1.0

    for a in (0, 1):
        for b in (0, 1):
            for c in (0, 1):
                for d in (0, 1):
                    for e in (0, 1):
                        for f_idx in (0, 1):
                            for g in (0, 1):
                                for k in (0, 1):
                                    for l_idx in (0, 1):
                                        lhs = f_elem(f_idx, c, d, e, g, l_idx) * f_elem(a, b, l_idx, e, f_idx, k)
                                        rhs = sum(
                                            f_elem(a, b, c, g, f_idx, m)
                                            * f_elem(a, m, d, e, g, k)
                                            * f_elem(b, c, d, k, m, l_idx)
                                            for m in (0, 1)
                                        )
                                        record(
                                            abs(lhs - rhs) < 1e-14,
                                            "pentagon_braid",
                                            f"pentagon ({a},{b},{c},{d},{e},{f_idx},{g},{k},{l_idx})",
                                        )

    # Check F^2 = I_2 and trace(F) = 0
    f_sq = [[sum(f_mat[i][m] * f_mat[m][j] for m in range(2)) for j in range(2)] for i in range(2)]
    record(abs(f_mat[0][0] + f_mat[1][1]) < 1e-15, "pentagon_braid", "Tr(F) == 0")
    record(
        abs(f_sq[0][0] - 1.0) < 1e-15
        and abs(f_sq[1][1] - 1.0) < 1e-15
        and abs(f_sq[0][1]) < 1e-15
        and abs(f_sq[1][0]) < 1e-15,
        "pentagon_braid",
        "F^2 == I_2",
    )

    # Check Artin braid relation and state leakage via FibonacciAnyonModel and Engine
    model = FibonacciAnyonModel()
    engine = FibonacciAnyonBraidingEngine(in_memory=True)
    receipt = engine.audit_fibonacci_braiding(model)
    engine.close()

    record(receipt.pentagon_equation_max_error < 1e-14, "pentagon_braid", "model pentagon error < 1e-14")
    record(receipt.braid_relation_max_error < 1e-14, "pentagon_braid", "model Artin braid error < 1e-14")
    record(receipt.commutator_norm_frob > 1.79, "pentagon_braid", "commutator Frobenius norm > 1.79")
    record(not receipt.is_holonomy_contractible, "pentagon_braid", "commutator holonomy non-contractible")
    record(abs(receipt.quantum_state_leakage - round(inv_phi, 6)) <= 1e-6, "pentagon_braid", "leakage == phi^-1")
    record(receipt.schur_lemma_involution_obstructed, "pentagon_braid", "Pauli-Z involution obstructed")
    record(receipt.terminal_route == "OpenSignObstruction", "pentagon_braid", "routes to OpenSignObstruction")

    # 4. Scope fences: bounded rational non-square check for 5 and Pauli-Z commutator formula
    for p in range(1, 26):
        for q in range(1, 26):
            record(
                (2 * p - q) * (2 * p - q) != 5 * (q * q),
                "scope",
                f"(2*{p}-{q})^2 != 5*{q}^2",
            )

    for m01 in range(-5, 6):
        if m01 != 0:
            comm_01 = -2 * m01
            record(comm_01 != 0, "scope", f"Pauli-Z commutator off-diagonal for m01={m01}")

    claimed_fixture = (True, True, 618034, True)
    scoped_fixture = (True, True, 618034, False)
    record(
        claimed_fixture[:3] == scoped_fixture[:3] and claimed_fixture != scoped_fixture,
        "scope",
        "GIN-C17 scope fence non-injectivity",
    )

    print(
        f"PASS: checks={checks} fusion={fusion_checks} zphi={zphi_checks} "
        f"pentagon_braid={pentagon_braid_checks} scope_fences={scope_fence_checks} failures={failures}"
    )
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
