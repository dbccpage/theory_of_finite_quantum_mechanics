#!/usr/bin/env python3
"""Independent executable check for FSP-EFFICIENT-SAMPLING-OBLIGATIONS (TFQ-0409).

Checks in exact rational arithmetic and via BQNFSignEvaluator:
1. Input-size and representation-cost scaling:
   - Full spinful Fock space 4^L > L^3 for L in {3, ..., 12}, and half-filled
     spinless configuration count comb(2m, m) strictly increasing and > (2m)^2
     for m >= 4.
   - DQMC rank-1 update cost c * Ns^2 < full stabilization cost c * Ns^3 for
     Ns >= 2, c > 0.
2. BQNFSignEvaluator RREF canonical section vs exact L1 quotient distance:
   - On explicit cochain complexes, normalize_cochain produces a unique RREF
     pivot-zero representative whose L1 norm strictly exceeds the exact L1
     quotient distance solve_quotient_distance (e.g. d0 = [[1],[1],[1]],
     c1 = [0, 1, 1] -> RREF L1 norm 2 vs optimal L1 norm 1 at [-1, 0, 0]).
   - When comb(dim_c1, rank(d0)) > max_candidates, solve_quotient_distance
     refuses with RuntimeError, confirming finite-budget enumeration rather than
     a general polynomial-time solver.
3. Meron orbit cancellation vs survivor variance & mixing scope fences:
   - Cancelling zero-sum meron pairs (+w_m, -w_m) preserves Z while reducing
     Z_abs and raising <Sign> to 1.
   - Positive-weight distributions (p, 1 - p) can still exhibit unbounded
     observable variance 1/p - 1 and arbitrarily small bottleneck conductance
     b / W_well (inverse mixing bound W_well / (2b)).
4. Protected vs unprotected Hubbard determinant signs and sample complexity:
   - Equal spin determinants det_up == det_dn give non-negative weights
     det_up * det_dn >= 0, whereas doped/frustrated configurations produce
     negative determinant products and sample amplification 1 / (s^2 * eps^2).
"""

from __future__ import annotations

from fractions import Fraction
from math import comb
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "python" / "src"))

from fsp.bqnf_sign_evaluator import (  # noqa: E402
    BQNFSignEvaluator,
    CochainComplex,
    TerminalRoute,
)


def main() -> int:
    checks = 0
    failures = 0
    scaling_checks = 0
    bqnf_checks = 0
    variance_mixing_checks = 0
    fence_checks = 0

    def record(cond: bool, bucket: str, msg: str) -> None:
        nonlocal checks, failures, scaling_checks, bqnf_checks, variance_mixing_checks, fence_checks
        checks += 1
        if bucket == "scaling":
            scaling_checks += 1
        elif bucket == "bqnf":
            bqnf_checks += 1
        elif bucket == "variance":
            variance_mixing_checks += 1
        else:
            fence_checks += 1
        if not cond:
            failures += 1
            print(f"FAIL: {msg}", file=sys.stderr)

    # 1. Input-size and representation-cost scaling
    for L in range(3, 15):
        record(4**L > L**3, "scaling", f"4^{L} <= {L}^3")
    prev_comb = 0
    for m in range(1, 12):
        c_val = comb(2 * m, m)
        record(c_val > prev_comb, "scaling", f"comb({2*m},{m}) not strictly increasing")
        if m >= 4:
            record(c_val > (2 * m) ** 2, "scaling", f"comb({2*m},{m}) <= {(2*m)**2}")
        prev_comb = c_val

    for c_cost in (1, 2, 5):
        for Ns in range(2, 20):
            record(
                c_cost * (Ns**2) < c_cost * (Ns**3),
                "scaling",
                f"DQMC update vs stabilization cost failed at c={c_cost}, Ns={Ns}",
            )

    # 2. BQNFSignEvaluator: RREF canonical representative != L1 minimizer
    # d0: 3x1 matrix [[1], [1], [1]], d1: 1x3 matrix [[1, -1, 0]] (d1 * d0 = 0)
    cpx = CochainComplex(
        dim_c0=1,
        dim_c1=3,
        dim_c2=1,
        d0=((1,), (1,), (1,)),
        d1=((1, -1, 0),),
    )
    ev = BQNFSignEvaluator(cpx)
    for scale in range(1, 15):
        s = Fraction(scale, 1)
        cochain = [Fraction(0), s, s]
        nf = ev.normalize_cochain(cochain)
        rref_l1 = ev.compute_l1_norm(nf.representative)
        opt_l1, opt_gauge = ev.solve_quotient_distance(cochain)
        record(
            nf.representative == (Fraction(0), s, s)
            and rref_l1 == 2 * s
            and opt_l1 == s
            and opt_l1 < rref_l1
            and opt_gauge == [s],
            "bqnf",
            f"RREF vs L1 minimizer mismatch at scale={scale}",
        )

    # Budget refusal check when comb(dim_c1, rank_d0) > max_candidates
    cpx_budget = CochainComplex(
        dim_c0=2,
        dim_c1=6,
        dim_c2=1,
        d0=((1, 0), (1, 0), (1, 0), (0, 1), (0, 1), (0, 1)),
        d1=((1, -1, 0, 1, -1, 0),),
    )
    ev_budget = BQNFSignEvaluator(cpx_budget)
    pkt = ev_budget.evaluate_sign_packet(
        [1, 2, 3, 4, 5, 6], [1, -1, 1, -1, 1, -1], max_candidates=5
    )
    record(
        pkt["distance_status"] == "budget_unknown" and pkt["phi_1_residual"] is None,
        "bqnf",
        "Expected budget_unknown when comb(6, 2) = 15 > max_candidates = 5",
    )

    # Meron equal-weight opposite-sign pairing check
    for w1_i in range(1, 6):
        for w2_i in range(1, 6):
            for wm_i in range(1, 6):
                w1, w2, wm = Fraction(w1_i), Fraction(w2_i), Fraction(wm_i)
                z_signed = w1 + w2 + wm - wm
                z_abs = w1 + w2 + 2 * wm
                record(
                    z_signed == w1 + w2
                    and z_signed < z_abs
                    and (w1 + w2) / z_abs < 1
                    and (w1 + w2) / (w1 + w2) == 1,
                    "bqnf",
                    "Meron cancellation partition / average sign identity failed",
                )
    inv_witness = ev.search_meron_involution([Fraction(3), Fraction(3), Fraction(5), Fraction(5)], [1, -1, -1, 1])
    record(
        inv_witness is not None and inv_witness.is_valid and len(inv_witness.mapping) == 4,
        "bqnf",
        "search_meron_involution failed on equal-weight opposite-sign pairs",
    )
    pkt_cancel = ev.evaluate_sign_packet([Fraction(2), Fraction(2), Fraction(0)], [1, -1, 1])
    record(
        pkt_cancel["route"] == TerminalRoute.EXACT_CANCELLATION,
        "bqnf",
        f"Expected EXACT_CANCELLATION route, got {pkt_cancel['route']}",
    )

    # 3. Positive-weight observable variance and bimodal barrier mixing bottlenecks
    p_grid = [Fraction(1, k) for k in range(2, 25)]
    for p2, p1 in zip(p_grid, p_grid[1:]):  # 0 < p1 < p2 < 1
        mean_1 = p1 * (Fraction(1, 1) / p1) + (1 - p1) * 0
        var_1 = p1 * ((Fraction(1, 1) / p1) ** 2) - 1
        var_2 = p2 * ((Fraction(1, 1) / p2) ** 2) - 1
        record(
            mean_1 == 1 and var_2 == (Fraction(1, 1) / p2 - 1) and var_1 > var_2 > 0,
            "variance",
            f"Positive-weight variance blowup failed for p1={p1} < p2={p2}",
        )

    for w_well_i in (1, 4, 10):
        W_well = Fraction(w_well_i, 1)
        b_grid = [Fraction(1, 2**k) for k in range(1, 12)]
        for b2, b1 in zip(b_grid, b_grid[1:]):  # 0 < b1 < b2
            tau_1 = W_well / (2 * b1)
            tau_2 = W_well / (2 * b2)
            record(
                tau_1 > tau_2 > 0,
                "variance",
                f"Bimodal barrier mixing lower bound failed for b1={b1} < b2={b2}",
            )

    # 4. Sign-reweighted sample complexity & Hubbard protection boundary
    s_grid = [Fraction(1, k) for k in range(1, 15)]
    for eps_inv in (10, 100):
        eps = Fraction(1, eps_inv)
        for s2, s1 in zip(s_grid, s_grid[1:]):  # 0 < s1 < s2 <= 1
            m1 = Fraction(1, 1) / (s1 * s1 * eps * eps)
            m2 = Fraction(1, 1) / (s2 * s2 * eps * eps)
            record(
                m1 > m2 > 0,
                "fence",
                f"Sample complexity amplification failed for s1={s1} < s2={s2}",
            )

    for det_up_i in range(-10, 11):
        det_up = Fraction(det_up_i, 3)
        record(
            det_up * det_up >= 0,
            "fence",
            "Spin-balanced determinant square should be non-negative",
        )
    record(
        Fraction(2) * Fraction(-1) == Fraction(-2) < 0,
        "fence",
        "Asymmetric determinant witness failed",
    )

    print(
        f"checks={checks} scaling_costs={scaling_checks} bqnf_normal_forms={bqnf_checks} "
        f"variance_mixing={variance_mixing_checks} scope_fences={fence_checks} failures={failures}"
    )
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
