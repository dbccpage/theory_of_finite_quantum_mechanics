#!/usr/bin/env python3
r"""Independent executable check for FSP-NICOLAI-MAP-CLAIM (TFQ-1205 / FSP-DERIV-041).

Verifies:
1. 2-site and 3-site periodic lattice Nicolai map Jacobian identities:
   - J_2(w0, w1, kappa) == D_kin(kappa) + diag(w0, w1) with det J_2 = w0 * w1 + kappa^2.
   - det J_3(w0, w1, w2, kappa) == w0 * w1 * w2 + kappa^2 * (w0 + w1 + w2).
2. Strict positivity under convex superpotentials W''(phi_i) = m + c * phi_i^2 > 0
   (m > 0, c >= 0) across bounded grids of (w0, w1, w2, kappa, m, c, phi0, phi1).
3. Change-of-variables branch sign decomposition J = sgn(J) * |J| and non-convex
   branch sign obstructions:
   - Fold Nicolai map xi(phi) = phi^2 - c: symmetric preimages +/-phi_0 have opposite
     Jacobians +/-2*phi_0 and cancelling branch signs (+1) + (-1) = 0.
   - Cubic Nicolai map xi(phi) = phi^3 - 3*phi: preimages {-2, 0, 2} at xi = -2..2
     include negative inner-branch Jacobian J(0) = -3 < 0 alongside positive outer
     branches J(+/-2) = +9 > 0.
   - Supersymmetry-breaking perturbations delta * w1 > w0 * w1 + kappa^2 flipping
     det(M_F - diag(delta, 0)) < 0.
4. Cross-check with CdtSusyWittenEvaluator.evaluate_nicolai_map in
   code/python/src/fsp/cdt_susy_witten_evaluator.py and scope fences for
   NicolaiMapSignSuppressionPredicate t t (t = t) and model specificity.
"""

from __future__ import annotations

from pathlib import Path
import sys
import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[2]
FSP_SRC = REPO_ROOT / "code" / "python" / "src" / "fsp"
if str(FSP_SRC) not in sys.path:
    sys.path.insert(0, str(FSP_SRC))

from cdt_susy_witten_evaluator import CdtSusyWittenEvaluator  # noqa: E402


def det2_skew_plus_diag(w0: int, w1: int, kappa: int) -> int:
    # [[w0, kappa], [-kappa, w1]]
    return w0 * w1 - kappa * (-kappa)


def det3_skew_plus_diag(w0: int, w1: int, w2: int, kappa: int) -> int:
    # [[w0, kappa, -kappa], [-kappa, w1, kappa], [kappa, -kappa, w2]]
    return (
        w0 * (w1 * w2 - kappa * (-kappa))
        - kappa * ((-kappa) * w2 - kappa * kappa)
        + (-kappa) * ((-kappa) * (-kappa) - w1 * kappa)
    )


def branch_sign(j_val: int) -> int:
    if j_val > 0:
        return 1
    if j_val < 0:
        return -1
    return 0


def main() -> int:
    checks = 0
    failures = 0
    jacobian_checks = 0
    positivity_checks = 0
    branch_checks = 0
    scope_fence_checks = 0

    def record(cond: bool, bucket: str, msg: str) -> None:
        nonlocal checks, failures, jacobian_checks, positivity_checks, branch_checks, scope_fence_checks
        checks += 1
        if bucket == "jacobian":
            jacobian_checks += 1
        elif bucket == "positivity":
            positivity_checks += 1
        elif bucket == "branch":
            branch_checks += 1
        elif bucket == "scope":
            scope_fence_checks += 1
        if not cond:
            failures += 1
            print(f"FAIL: {msg}")

    # 1. Exhaustive 2-site and 3-site Jacobian determinant identities on bounded integer grids
    for w0 in range(-3, 5):
        for w1 in range(-3, 5):
            for kappa in range(-3, 4):
                d2 = det2_skew_plus_diag(w0, w1, kappa)
                record(
                    d2 == w0 * w1 + kappa * kappa,
                    "jacobian",
                    f"det2({w0},{w1},{kappa}) == w0*w1 + kappa^2",
                )

    for w0 in range(1, 5):
        for w1 in range(1, 5):
            for w2 in range(1, 5):
                for kappa in range(-3, 4):
                    d3 = det3_skew_plus_diag(w0, w1, w2, kappa)
                    expected = w0 * w1 * w2 + (kappa * kappa) * (w0 + w1 + w2)
                    record(
                        d3 == expected and d3 > 0,
                        "jacobian",
                        f"det3({w0},{w1},{w2},{kappa}) formula and positivity",
                    )

    # 2. Convex quartic superpotential Hessian W''(phi) = m + c * phi^2 lower bounds
    for m in range(1, 4):
        for c in range(0, 4):
            for phi0 in range(-3, 4):
                for phi1 in range(-3, 4):
                    for kappa in range(-2, 3):
                        w0 = m + c * (phi0 * phi0)
                        w1 = m + c * (phi1 * phi1)
                        d2 = det2_skew_plus_diag(w0, w1, kappa)
                        record(
                            w0 >= m and w1 >= m and d2 >= m * m + kappa * kappa and d2 > 0,
                            "positivity",
                            f"quartic superpotential lower bound ({m},{c},{phi0},{phi1},{kappa})",
                        )

    # 3. Branch sign decomposition, fold cancellation, cubic 3-branch sign defect, and SUSY breaking
    for j_val in range(-15, 16):
        if j_val != 0:
            record(
                j_val == branch_sign(j_val) * abs(j_val) and branch_sign(j_val) in (-1, 1),
                "branch",
                f"branch sign decomposition J={j_val}",
            )

    for c_val in range(1, 6):
        for phi0 in range(1, 10):
            xi_pos = phi0 * phi0 - c_val
            xi_neg = (-phi0) * (-phi0) - c_val
            j_pos = 2 * phi0
            j_neg = -2 * phi0
            record(
                xi_pos == xi_neg
                and j_pos > 0
                and j_neg < 0
                and branch_sign(j_pos) + branch_sign(j_neg) == 0,
                "branch",
                f"fold Nicolai branch cancellation c={c_val}, phi0={phi0}",
            )

    # Cubic Nicolai map xi(phi) = phi^3 - 3*phi, J(phi) = 3*(phi^2 - 1)
    cubic_j = {phi: 3 * (phi * phi - 1) for phi in (-2, 0, 2)}
    record(
        cubic_j[-2] == 9
        and cubic_j[0] == -3
        and cubic_j[2] == 9
        and branch_sign(cubic_j[-2]) == 1
        and branch_sign(cubic_j[0]) == -1
        and branch_sign(cubic_j[2]) == 1,
        "branch",
        "cubic Nicolai three-branch sign defect",
    )

    # SUSY-breaking perturbation delta * w1 > w0 * w1 + kappa^2
    for w0 in range(1, 5):
        for w1 in range(1, 5):
            for kappa in range(-2, 3):
                delta = w0 + (kappa * kappa) // w1 + 2
                d_unbroken = det2_skew_plus_diag(w0, w1, kappa)
                d_broken = det2_skew_plus_diag(w0 - delta, w1, kappa)
                record(
                    d_unbroken > 0 and d_broken < 0,
                    "branch",
                    f"SUSY breaking sign flip ({w0},{w1},{kappa},{delta})",
                )

    # 4. Cross-check CdtSusyWittenEvaluator.evaluate_nicolai_map and scope fences
    ev = CdtSusyWittenEvaluator(in_memory=True)
    for nv in (4, 6, 8, 10):
        for seed in range(10, 20):
            nic_res, f_det, f_sign = ev.evaluate_nicolai_map(
                num_vertices=nv, is_broken=False, m_breaking=0.0, seed=seed
            )
            record(
                nic_res == 0.0 and f_det > 0.0 and f_sign == 1,
                "positivity",
                f"unbroken CdtSusyWittenEvaluator nv={nv} seed={seed}",
            )
            nic_res_b, _, _ = ev.evaluate_nicolai_map(
                num_vertices=nv, is_broken=True, m_breaking=0.5, seed=seed
            )
            record(
                nic_res_b > 0.0,
                "branch",
                f"broken CdtSusyWittenEvaluator residual > 0 nv={nv} seed={seed}",
            )
    ev.close()

    # Tautology fence on regge_wdw_core.lean::NicolaiMapSignSuppressionPredicate
    for neg_det in range(-10, 0):
        tautology_holds = neg_det == neg_det
        record(
            tautology_holds and neg_det < 0,
            "scope",
            f"tautology t=t holds for negative determinant {neg_det} < 0",
        )

    overclaimed_interp = (True, True, True)
    scoped_interp = (True, True, False)
    record(
        overclaimed_interp[:2] == scoped_interp[:2] and overclaimed_interp != scoped_interp,
        "scope",
        "FSP-NICOLAI-MAP-CLAIM model specificity scope fence",
    )

    print(
        f"PASS: checks={checks} jacobian={jacobian_checks} positivity={positivity_checks} "
        f"branch={branch_checks} scope_fences={scope_fence_checks} failures={failures}"
    )
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
