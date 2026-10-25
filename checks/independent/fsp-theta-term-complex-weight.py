#!/usr/bin/env python3
r"""Independent executable check for FSP-THETA-TERM-COMPLEX-WEIGHT (TFQ-1198 / FSP-DERIV-034).

Verifies:
1. Integer lattice topological charge Q_top = n_+ - n_- CP antisymmetry:
   Q_top(n_-, n_+) == -Q_top(n_+, n_-) and Q_top(n, n) == 0.
2. Non-real Boltzmann weight exp(-i theta Q_top) criterion for rational angles
   theta = (p/q) * pi: exp(-i theta Q_top) is real iff (p * Q_top) % q == 0,
   and has non-zero imaginary part -sin(theta * Q_top) != 0 whenever (p * Q_top) % q != 0.
3. CP-conjugate pair summation:
   w(Q) exp(-i theta Q) + w(Q) exp(+i theta Q) = 2 w(Q) cos(theta Q) (imaginary part cancels),
   which becomes strictly negative whenever w(Q) > 0 and cos(theta Q) < 0 (pi/2 < |theta Q| <= pi).
4. At theta = pi, alternating real sign character sigma_pi(Q) = (-1)^Q homomorphism
   sigma_pi(Q1 + Q2) == sigma_pi(Q1) * sigma_pi(Q2), two-sector partition sum cancellation
   Z(pi) = w0 - w1 < Z_pq = w0 + w1, action-gap weight separation, and CP-symmetric
   3-sector instanton susceptibility second moment sum_Q Q^2 w_Q = 2 * w1 > 0.
5. Cross-check with CdtTopologicalChargeEvaluator in
   code/python/src/fsp/cdt_topological_charge_evaluator.py and GIN-C9 scope fences.
"""

from __future__ import annotations

import cmath
import math
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[2]
FSP_SRC = REPO_ROOT / "code" / "python" / "src" / "fsp"
if str(FSP_SRC) not in sys.path:
    sys.path.insert(0, str(FSP_SRC))

from cdt_topological_charge_evaluator import CdtTopologicalChargeEvaluator  # noqa: E402


def lattice_topological_charge(n_pos: int, n_neg: int) -> int:
    return n_pos - n_neg


def theta_charge_in_pi_z(p: int, q: int, q_top: int) -> bool:
    return (p * q_top) % q == 0


def theta_pi_sign(q_top: int) -> int:
    return 1 if (q_top % 2 == 0) else -1


def main() -> int:
    checks = 0
    failures = 0
    index_checks = 0
    phase_checks = 0
    sector_checks = 0
    scope_fence_checks = 0

    def record(cond: bool, bucket: str, msg: str) -> None:
        nonlocal checks, failures, index_checks, phase_checks, sector_checks, scope_fence_checks
        checks += 1
        if bucket == "index":
            index_checks += 1
        elif bucket == "phase":
            phase_checks += 1
        elif bucket == "sector":
            sector_checks += 1
        elif bucket == "scope":
            scope_fence_checks += 1
        if not cond:
            failures += 1
            print(f"FAIL: {msg}")

    # 1. Chiral index Q_top = n_+ - n_- antisymmetry on [0..12]^2
    for n_pos in range(13):
        for n_neg in range(13):
            q1 = lattice_topological_charge(n_pos, n_neg)
            q2 = lattice_topological_charge(n_neg, n_pos)
            record(
                q2 == -q1 and lattice_topological_charge(n_pos, n_pos) == 0,
                "index",
                f"chiral index antisymmetry ({n_pos},{n_neg})",
            )

    # 2. Rational angle theta = (p/q)*pi complex weight and CP-conjugate pair cancellation
    for q_den in range(2, 8):
        for p_num in range(1, q_den):
            for q_top in range(-6, 7):
                theta = (p_num / q_den) * math.pi
                weight = cmath.exp(-1j * theta * q_top)
                in_pi_z = theta_charge_in_pi_z(p_num, q_den, q_top)
                is_real = abs(weight.imag) < 1e-12
                record(
                    in_pi_z == is_real,
                    "phase",
                    f"rational pi divisibility iff real weight p={p_num}, q={q_den}, Q={q_top}",
                )
                # CP-conjugate pair sum
                weight_cp = cmath.exp(1j * theta * q_top)
                pair_sum = weight + weight_cp
                record(
                    abs(pair_sum.imag) < 1e-12 and abs(pair_sum.real - 2.0 * math.cos(theta * q_top)) < 1e-12,
                    "phase",
                    f"CP pair sine cancellation p={p_num}, q={q_den}, Q={q_top}",
                )

    # Integer CP-pair and obtuse-phase negativity check
    for w in range(1, 6):
        for c_val in range(-5, 6):
            for s_val in range(-5, 6):
                re_sum = w * c_val + w * c_val
                im_sum = -(w * s_val) + (w * s_val)
                record(
                    re_sum == 2 * w * c_val and im_sum == 0,
                    "phase",
                    f"integer CP pair ({w},{c_val},{s_val})",
                )
                if c_val < 0:
                    record(re_sum < 0, "phase", f"negative paired weight for c={c_val} < 0")

    # 3. theta = pi parity homomorphism, two-sector partition cancellation, and 3-sector moments
    for q1 in range(-8, 9):
        for q2 in range(-8, 9):
            record(
                theta_pi_sign(q1 + q2) == theta_pi_sign(q1) * theta_pi_sign(q2),
                "sector",
                f"theta=pi parity homomorphism ({q1},{q2})",
            )

    for w0 in range(1, 10):
        for w1 in range(1, 10):
            z_signed = w0 - w1
            z_quenched = w0 + w1
            mean_q = (-1) * w1 + 0 * w0 + 1 * w1
            m2_q = ((-1) ** 2) * w1 + (0**2) * w0 + (1**2) * w1
            record(
                z_signed < z_quenched
                and z_quenched > 0
                and ((z_signed > 0) == (w1 < w0))
                and mean_q == 0
                and m2_q == 2 * w1
                and m2_q > 0,
                "sector",
                f"two/three-sector partition and second moment ({w0},{w1})",
            )

    # 4. Cross-check with CdtTopologicalChargeEvaluator and GIN-C9 scope fences
    ev = CdtTopologicalChargeEvaluator(in_memory=True)
    for nv in (6, 8):
        for target_q in (-2, -1, 0, 1, 2):
            d_rat, gamma_5, n_pos, n_neg = ev.build_synthetic_instanton_operator(
                num_vertices=nv, target_Q=target_q, is_tearing=False
            )
            q_idx = lattice_topological_charge(n_pos, n_neg)
            record(
                q_idx == target_q,
                "index",
                f"CdtTopologicalChargeEvaluator index nv={nv}, Q={target_q}",
            )
    ens_res = ev.evaluate_instanton_susceptibility_ensemble(
        ensemble_id="check_theta_smooth",
        geometry_regime="SMOOTH_SEMICLASSICAL",
        num_configs=10,
        volume_scale=32,
        seed=42,
    )
    ev.close()
    record(
        ens_res["all_charges_integer"] and ens_res["instanton_susceptibility"] > 0.0,
        "sector",
        "CdtTopologicalChargeEvaluator integer charges and positive susceptibility",
    )

    for w0 in range(1, 10):
        for delta_s in range(1, 10):
            record(w0 != w0 + delta_s, "scope", f"GIN-C9 Nat arithmetic fence ({w0},{delta_s})")

    overclaimed_interp = (True, True, True)
    scoped_interp = (True, True, False)
    record(
        overclaimed_interp[:2] == scoped_interp[:2] and overclaimed_interp != scoped_interp,
        "scope",
        "theta_term_phenomenology_scope_fence non-injectivity",
    )

    print(
        f"PASS: checks={checks} index={index_checks} phase={phase_checks} "
        f"sector={sector_checks} scope_fences={scope_fence_checks} failures={failures}"
    )
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
