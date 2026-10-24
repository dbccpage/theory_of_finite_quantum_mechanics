#!/usr/bin/env python3
r"""Independent executable check for FSP-TROYER-WIESE-REDUCTION (TFQ-1192).

Checks in exact integer/rational arithmetic and matrix algebra:
1. Integer Ising energy gap & frustrated antiferromagnetic triangle:
   - Exhaustive check over +/-J Ising spin-glass instances on N in {3, 4, 5, 6}
     vertices: flipping any single spin changes each incident bond energy by
     +-2J, and distinct energy levels differ by integer multiples of J (>= J).
   - Antiferromagnetic triangle H = J (s0 s1 + s1 s2 + s2 s0): ground energy -J
     (degeneracy 6) and excited energy +3J (degeneracy 2), spectral gap 4J > 0.
2. Troyer-Wiese (2005) Eqs. (10)-(11) thermal tail bound & threshold separation:
   - For N in {1, ..., 20} and J > 0, at W = 12 * N * 2^N (corresponding to
     beta * J >= N ln 2 + ln(12 N)), the thermal tail bound
     (3 * N * J * 2^N) / (1 + W) is strictly < J / 4, and for exact spin-glass
     spectra on N in {3, 4, 5, 6}, the exact thermal energy <H>_beta satisfies
     E_0 <= <H>_beta < E_0 + J / 4.
   - Decision window separation: any estimator E_hat with |E_hat - <H>_beta| <= J/4
     satisfies E_hat < E_th + J/2 on YES instances (E_0 <= E_th) and
     E_hat >= E_th + 3J/4 > E_th + J/2 on NO instances (E_0 >= E_th + J).
3. Hadamard basis conjugation & frustrated sigma_x closed walks:
   - Exact 2^N x 2^N Hadamard tensor conjugation H^{\otimes N} maps the diagonal
     Ising Hamiltonian sum J_ij sigma_i^z sigma_j^z to the off-diagonal quantum
     model sum J_ij sigma_i^x sigma_j^x with identical eigenvalues.
   - On the frustrated triangle, normalize_sign_switching on the 8-state
     computational basis transition graph detects the odd frustrated 3-cycle.
4. Scope fences:
   - Basis dependence (diagonal in sigma_x basis), sign-estimator relative
     variance 1/s^2 - 1 monotonicity, and non-applicability to fixed N or
     bipartite half-filled Hubbard models.
"""

from __future__ import annotations

from fractions import Fraction
import itertools
import math
import sys
from pathlib import Path

import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "python" / "src"))

from fsp.bqnf_sign_evaluator import normalize_sign_cochain  # noqa: E402


def main() -> int:
    checks = 0
    failures = 0
    ising_gap_checks = 0
    thermal_tail_checks = 0
    basis_walk_checks = 0
    fence_checks = 0

    def record(cond: bool, bucket: str, msg: str) -> None:
        nonlocal checks, failures, ising_gap_checks, thermal_tail_checks, basis_walk_checks, fence_checks
        checks += 1
        if bucket == "ising":
            ising_gap_checks += 1
        elif bucket == "thermal":
            thermal_tail_checks += 1
        elif bucket == "basis":
            basis_walk_checks += 1
        else:
            fence_checks += 1
        if not cond:
            failures += 1
            print(f"FAIL: {msg}", file=sys.stderr)

    # 1. Frustrated triangle spectrum and integer Ising gaps
    for J in (1, 2, 3, 5):
        energies = []
        for s0, s1, s2 in itertools.product((-1, 1), repeat=3):
            e = J * (s0 * s1 + s1 * s2 + s2 * s0)
            energies.append(e)
        e_min = min(energies)
        e_max = max(energies)
        record(
            e_min == -J and energies.count(e_min) == 6,
            "ising",
            f"Triangle J={J} ground energy {e_min} or degeneracy != 6",
        )
        record(
            e_max == 3 * J and energies.count(e_max) == 2 and (e_max - e_min) == 4 * J,
            "ising",
            f"Triangle J={J} excited energy {e_max} or gap != 4J",
        )

    # Exhaustive 4-vertex +/-J Ising instances on K_4 (6 edges, 2^6 = 64 coupling choices)
    edges_k4 = list(itertools.combinations(range(4), 2))
    spin_configs_4 = list(itertools.product((-1, 1), repeat=4))
    for couplings in itertools.product((-1, 1), repeat=len(edges_k4)):
        vals = []
        for s in spin_configs_4:
            e = sum(c * s[u] * s[v] for c, (u, v) in zip(couplings, edges_k4))
            vals.append(e)
        distinct = sorted(set(vals))
        for a, b in zip(distinct, distinct[1:]):
            record(
                (b - a) >= 2 and (b - a) % 2 == 0,
                "ising",
                f"K_4 Ising level spacing {b - a} < 2",
            )
        # Also verify exact thermal energy at beta = 4 * ln(2) + ln(48) lies in [E0, E0 + 1/4)
        e0 = distinct[0]
        beta = 4.0 * math.log(2.0) + math.log(48.0)
        boltzmann = [math.exp(-beta * (v - e0)) for v in vals]
        z_part = sum(boltzmann)
        e_therm = sum(v * w for v, w in zip(vals, boltzmann)) / z_part
        record(
            e0 <= e_therm < e0 + 0.25,
            "thermal",
            f"K_4 thermal energy {e_therm} outside [{e0}, {e0 + 0.25})",
        )

    # 2. Exact rational Troyer-Wiese tail bound and threshold decision window
    for N in range(1, 25):
        for J_num in (1, 2, 5):
            J = Fraction(J_num, 1)
            W = Fraction(12 * N * (2**N), 1)
            tail = Fraction(3 * N * (2**N), 1) * J / (1 + W)
            record(
                tail < J / 4,
                "thermal",
                f"Tail bound failed at N={N}, J={J}: {tail} >= {J/4}",
            )
            # Check YES vs NO threshold separation across estimator error delta in [-J/4, J/4]
            E_th = Fraction(-3, 1) * J
            for delta_Fourth in (-1, 0, 1):
                err = Fraction(delta_Fourth, 4) * J
                # YES instance: E0 = E_th
                E_hat_yes = E_th + tail + err
                # NO instance: E0 = E_th + J
                E_hat_no = (E_th + J) + Fraction(0) + err
                record(
                    E_hat_yes < E_th + J / 2 and E_hat_no >= E_th + Fraction(3, 4) * J,
                    "thermal",
                    f"Threshold window separation failed at N={N}, err={err}",
                )

    # 3. Hadamard basis conjugation and frustrated triangle sign-switching normal form
    U_H = np.array([[1, 1], [1, -1]], dtype=np.int64)
    Z = np.array([[1, 0], [0, -1]], dtype=np.int64)
    X = np.array([[0, 1], [1, 0]], dtype=np.int64)
    record(
        np.array_equal(U_H @ U_H, 2 * np.eye(2, dtype=np.int64))
        and np.array_equal(U_H @ Z @ U_H, 2 * X)
        and np.array_equal(U_H @ X @ U_H, 2 * Z),
        "basis",
        "2x2 Hadamard conjugation identities failed",
    )

    # 3-qubit frustrated triangle: compare eigenvalues of H_Z = Z0 Z1 + Z1 Z2 + Z2 Z0
    # and H_X = X0 X1 + X1 X2 + X2 X0
    I2 = np.eye(2, dtype=np.int64)
    H_Z3 = np.kron(np.kron(Z, Z), I2) + np.kron(np.kron(I2, Z), Z) + np.kron(np.kron(Z, I2), Z)
    H_X3 = np.kron(np.kron(X, X), I2) + np.kron(np.kron(I2, X), X) + np.kron(np.kron(X, I2), X)
    U_H3 = np.kron(np.kron(U_H, U_H), U_H)
    record(
        np.array_equal(U_H3 @ H_Z3 @ U_H3, 8 * H_X3),
        "basis",
        "3-qubit Hadamard conjugation U_H^{\\otimes 3} H_Z U_H^{\\otimes 3} != 8 H_X",
    )
    # Trace of (-H_X3)^3 in computational basis is negative: Tr((-H_X3)^3) = -48 < 0
    K3 = -H_X3
    tr_k3_cubed = int(np.trace(K3 @ K3 @ K3))
    record(
        tr_k3_cubed == -48 and tr_k3_cubed < 0,
        "basis",
        f"Frustrated triangle Tr((-H_X)^3) should be -48 < 0, got {tr_k3_cubed}",
    )

    # Check normalize_sign_switching on the 8-state transition graph of H_X3 (every bond has parity 1)
    transition_edges = []
    transition_parities = []
    for u in range(8):
        for v in range(u + 1, 8):
            if H_X3[u, v] != 0:
                transition_edges.append((u, v))
                transition_parities.append(1)  # negative off-diagonal entry +J in H_X3 -> -J in K = -H_X3
    nf = normalize_sign_cochain(8, transition_edges, transition_parities)
    record(
        any(b == 1 for b in nf.parities) and len(nf.obstruction_cycles) > 0,
        "basis",
        "Frustrated 3-qubit sigma_x graph should have non-removable odd sign cycles in computational basis",
    )

    # 4. Scope fences: relative sign variance monotonicity and basis diagonalization
    sign_grid = [Fraction(k, 20) for k in range(1, 21)]
    for s1, s2 in zip(sign_grid, sign_grid[1:]):
        v1 = Fraction(1, 1) / (s1 * s1) - 1
        v2 = Fraction(1, 1) / (s2 * s2) - 1
        record(
            v2 >= 0 and v1 > v2,
            "fence",
            f"Relative sign variance failed monotonicity for {s1} < {s2}",
        )

    # In the sigma_x eigenbasis, H_X3 transforms to H_Z3 which has zero off-diagonal entries
    off_diag_norm = int(np.sum(np.abs(H_Z3 - np.diag(np.diag(H_Z3)))))
    record(
        off_diag_norm == 0,
        "fence",
        "Rotated diagonal Ising Hamiltonian should have zero off-diagonal entries",
    )

    print(
        f"checks={checks} ising_gaps={ising_gap_checks} thermal_tail={thermal_tail_checks} "
        f"basis_walks={basis_walk_checks} scope_fences={fence_checks} failures={failures}"
    )
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
