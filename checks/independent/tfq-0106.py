#!/usr/bin/env python3
"""Independent verification script for TFQ-0106 (stage FINITE_QG).

AuthorityEffect: None.
Verifies all three exact rational components and non-equivalence fences in
lean4/CosmologicalCouplingReplay.lean and code/rust/src/general_relativity/cosmological_constant.rs:
1. Exact rational replay of CosmologicalCoupling::evaluate_action and effective_scalar_curvature,
   curvature-volume balance condition evaluate_action == 0 <=> K == 2 * lambda * kappa * V,
   and homogeneous / reciprocal scaling identities.
2. External cell-volume calibration underdetermination fence: 4D length rescaling V_cell -> s^4 * V_cell,
   tautological achievability of any nonzero targetLambda via V_cell = H / targetLambda, injectivity of
   V_cell -> H / V_cell, joint (gamma, V_cell) scale degeneracy, and default valency scaffold spread.
3. Scalar hinge residual vs. 4D tensorial Einstein equation fence: 10 independent symmetric tensor
   components (9 trace-free + 1 trace) in d = 4, and anisotropic diagonal profiles
   (lambda + delta, lambda - delta, lambda, lambda) with zero scalar mean residual and strictly positive
   tensorial squared residual 2 * delta^2.
"""

from __future__ import annotations

from fractions import Fraction
import sys


def effective_scalar_curvature(lam: Fraction, kappa: Fraction) -> Fraction:
    return Fraction(2) * lam * kappa


def evaluate_cosmological_action(
    lam: Fraction, kappa: Fraction, k_hinge: Fraction, vol: Fraction
) -> Fraction:
    if kappa == 0:
        raise ValueError("ZeroCoupling")
    if vol < 0:
        raise ValueError("NegativeVolume")
    return k_hinge / (Fraction(2) * kappa) - lam * vol


def lambda_residual(h_mean: Fraction, v_cell: Fraction) -> Fraction:
    return h_mean / v_cell


def immirzi_lambda_residual(gamma: Fraction, v_cell: Fraction, h0: Fraction) -> Fraction:
    return (gamma * h0) / v_cell


def verify_rust_replay_and_scaling() -> tuple[int, int]:
    checks = 0
    failures = 0

    def check(cond: bool, msg: str) -> None:
        nonlocal checks, failures
        checks += 1
        if not cond:
            failures += 1
            print(f"FAIL [rust_replay]: {msg}", file=sys.stderr)

    # Exact replay of test_cosmological_action in cosmological_constant.rs
    lam0 = Fraction(1, 10)
    kap0 = Fraction(1, 2)
    check(effective_scalar_curvature(lam0, kap0) == Fraction(1, 10), "effective_scalar_curvature")
    check(
        evaluate_cosmological_action(lam0, kap0, Fraction(10), Fraction(20)) == Fraction(8),
        "evaluate_action(10, 20) == 8",
    )

    lambdas = [Fraction(-2, 3), Fraction(0), Fraction(1, 10), Fraction(3, 5), Fraction(5, 2)]
    kappas = [Fraction(1, 4), Fraction(1, 2), Fraction(1), Fraction(3, 2)]
    volumes = [Fraction(1), Fraction(4), Fraction(20)]
    scales = [Fraction(1, 3), Fraction(1, 2), Fraction(2), Fraction(5)]

    for lam in lambdas:
        for kap in kappas:
            eff = effective_scalar_curvature(lam, kap)
            for vol in volumes:
                k_bal = eff * vol
                check(
                    evaluate_cosmological_action(lam, kap, k_bal, vol) == 0,
                    "Balanced curvature K = 2*lambda*kappa*V must give zero action",
                )
                check(
                    evaluate_cosmological_action(lam, kap, k_bal + Fraction(1), vol) != 0,
                    "Perturbed curvature K != 2*lambda*kappa*V must give nonzero action",
                )
                for s in scales:
                    check(
                        evaluate_cosmological_action(lam, kap, s * k_bal, s * vol)
                        == s * evaluate_cosmological_action(lam, kap, k_bal, vol),
                        "Homogeneous scaling in (K, V)",
                    )
                    check(
                        effective_scalar_curvature(lam / s, s * kap) == eff,
                        "Reciprocal invariance of effective_scalar_curvature",
                    )

    return checks, failures


def verify_cell_volume_calibration_fence() -> tuple[int, int]:
    checks = 0
    failures = 0

    def check(cond: bool, msg: str) -> None:
        nonlocal checks, failures
        checks += 1
        if not cond:
            failures += 1
            print(f"FAIL [calibration]: {msg}", file=sys.stderr)

    # Default valency scaffold (3, 4, 5, 6)
    h_default = (Fraction(3) + Fraction(4) + Fraction(5) + Fraction(6)) / Fraction(4)
    check(h_default == Fraction(9, 2), "fourHingeMean(3,4,5,6) == 9/2")
    check(lambda_residual(h_default, Fraction(1)) == Fraction(9, 2), "Vcell=1")
    check(lambda_residual(h_default, Fraction(9, 2)) == Fraction(1), "Vcell=9/2")
    check(lambda_residual(h_default, Fraction(9)) == Fraction(1, 2), "Vcell=9")
    check(lambda_residual(h_default, Fraction(45)) == Fraction(1, 10), "Vcell=45")

    h_vals = [Fraction(1, 2), Fraction(9, 2), Fraction(-3, 4), Fraction(7)]
    targets = [Fraction(1, 1000), Fraction(1, 10), Fraction(1), Fraction(13, 7), Fraction(-5, 3)]
    scales = [Fraction(1, 2), Fraction(2), Fraction(3)]

    for h in h_vals:
        for t in targets:
            v_cal = h / t
            check(v_cal != 0, "Calibrated V_cell != 0")
            check(lambda_residual(h, v_cal) == t, "Any targetLambda reproduced by V_cell = H / targetLambda")
            for s in scales:
                check(
                    lambda_residual(h, (s**4) * v_cal) == (Fraction(1) / (s**4)) * lambda_residual(h, v_cal),
                    "4D lattice spacing rescaling 1/s^4",
                )
                check(
                    immirzi_lambda_residual(s * Fraction(1, 4), s * v_cal, h)
                    == immirzi_lambda_residual(Fraction(1, 4), v_cal, h),
                    "Immirzi and V_cell scale degeneracy",
                )

    return checks, failures


def verify_scalar_vs_tensor_einstein_fence() -> tuple[int, int]:
    checks = 0
    failures = 0

    def check(cond: bool, msg: str) -> None:
        nonlocal checks, failures
        checks += 1
        if not cond:
            failures += 1
            print(f"FAIL [tensor_fence]: {msg}", file=sys.stderr)

    # Symmetric tensor components in d = 1..6
    expected_sym = {1: 1, 2: 3, 3: 6, 4: 10, 5: 15, 6: 21}
    for d, exp_c in expected_sym.items():
        c = d * (d + 1) // 2
        check(c == exp_c, f"symTensorComponents({d}) == {exp_c}")

    lambdas = [Fraction(-1), Fraction(0), Fraction(1, 10), Fraction(3, 2)]
    deltas = [Fraction(-3), Fraction(-1, 2), Fraction(1, 5), Fraction(2), Fraction(7, 3)]
    for lam in lambdas:
        for delta in deltas:
            r = [lam + delta, lam - delta, lam, lam]
            mean_res = sum(r_mu - lam for r_mu in r) / Fraction(4)
            sq_res = sum((r_mu - lam) ** 2 for r_mu in r)
            check(mean_res == 0, "Anisotropic profile has vanishing scalar mean residual")
            check(sq_res == Fraction(2) * (delta**2) > 0, "Anisotropic profile has positive squared residual")
            check(r[0] - lam == delta != 0, "Anisotropic profile violates componentwise Einstein eq")

    return checks, failures


def main() -> int:
    c1, f1 = verify_rust_replay_and_scaling()
    c2, f2 = verify_cell_volume_calibration_fence()
    c3, f3 = verify_scalar_vs_tensor_einstein_fence()
    total_checks = c1 + c2 + c3
    total_failures = f1 + f2 + f3
    print(
        f"checks={total_checks} rust_replay={c1} calibration={c2} tensor_fence={c3} failures={total_failures}"
    )
    return 0 if total_failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
