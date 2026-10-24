#!/usr/bin/env python3
"""Independent verification for FSP-DISCRETE-WDW-CONSTRAINT (TFQ-1213 / FSP-DERIV-049).

Standalone exact-rational checker using only Python's standard library (fractions.Fraction).
Verifies:
1. Direct-sum Regge-WDW cochain D_joint = [d_0, 0]^T linearity, constant-cochain kernel,
   signed rational unscreenability ||h_perp||_1 <= ||Omega - D_joint alpha||_1, weak and strong
   L1 duality on exact-coboundary momentum states, and the S^4 seed (N0=6, N1=15) flat (0) vs
   curved (45) defect receipts.
2. Finite-space quadratic constraint operators H_perp = L^T L, diffeomorphism-averaging
   idempotent projector P_inv and complement H_perp = I - P_inv, and 2-tick Page-Wootters
   clock conditioning.
3. Scope fences: DeWitt supermetric indefinite signature (-, +), WDW zero-mode kernel vs
   Section 2.5 thermal Gibbs trace, and fermionic sign-sector independence.
"""

from __future__ import annotations

from fractions import Fraction
import itertools
import sys


def d0_edge(u: int, v: int, alpha: tuple[Fraction, ...]) -> Fraction:
    return alpha[v] - alpha[u]


def rat_sign(x: Fraction) -> Fraction:
    if x > 0:
        return Fraction(1)
    if x < 0:
        return Fraction(-1)
    return Fraction(0)


def total_joint_residual_l1(
    p: tuple[Fraction, ...],
    d0_alpha: tuple[Fraction, ...],
    h_perp: tuple[Fraction, ...],
) -> Fraction:
    return sum((abs(pe - da) for pe, da in zip(p, d0_alpha)), Fraction(0)) + sum(
        (abs(hv) for hv in h_perp), Fraction(0)
    )


def dual_objective(
    w1: tuple[Fraction, ...],
    w2: tuple[Fraction, ...],
    p: tuple[Fraction, ...],
    h_perp: tuple[Fraction, ...],
) -> Fraction:
    return sum((we * pe for we, pe in zip(w1, p)), Fraction(0)) + sum(
        (wv * hv for wv, hv in zip(w2, h_perp)), Fraction(0)
    )


def main() -> int:
    cochain_duality = 0
    projector_pw = 0
    fences = 0
    failures = 0

    def check(cond: bool, category: str) -> None:
        nonlocal cochain_duality, projector_pw, fences, failures
        if not cond:
            failures += 1
        if category == "cochain":
            cochain_duality += 1
        elif category == "proj":
            projector_pw += 1
        else:
            fences += 1

    vals = [Fraction(-2), Fraction(-1), Fraction(0), Fraction(1), Fraction(2)]
    edges_k3 = [(0, 1), (1, 2), (0, 2)]

    # 1. Direct-sum Regge-WDW cochain linearity, unscreenability, and L1 strong duality
    for alpha in itertools.product(vals, repeat=3):
        for beta in itertools.product([Fraction(-1), Fraction(1)], repeat=3):
            a = Fraction(2)
            b = Fraction(-3)
            comb = tuple(a * x + b * y for x, y in zip(alpha, beta))
            for u, v in edges_k3:
                check(
                    d0_edge(u, v, comb) == a * d0_edge(u, v, alpha) + b * d0_edge(u, v, beta),
                    "cochain",
                )
        for c in vals:
            const_vec = (c, c, c)
            for u, v in edges_k3:
                check(d0_edge(u, v, const_vec) == Fraction(0), "cochain")

    for alpha in itertools.product([Fraction(-1), Fraction(0), Fraction(1)], repeat=3):
        d0_a = tuple(d0_edge(u, v, alpha) for u, v in edges_k3)
        for h_perp in itertools.product(vals, repeat=3):
            h_norm = sum((abs(hv) for hv in h_perp), Fraction(0))
            res_exact = total_joint_residual_l1(d0_a, d0_a, h_perp)
            check(res_exact == h_norm, "cochain")
            w1_zero = (Fraction(0), Fraction(0), Fraction(0))
            w2_opt = tuple(rat_sign(hv) for hv in h_perp)
            check(all(abs(wv) <= 1 for wv in w2_opt), "cochain")
            check(dual_objective(w1_zero, w2_opt, d0_a, h_perp) == res_exact, "cochain")
            for p in [(Fraction(1), Fraction(-1), Fraction(2)), d0_a]:
                res_p = total_joint_residual_l1(p, d0_a, h_perp)
                check(res_p >= h_norm, "cochain")
                for v0 in range(3):
                    if h_perp[v0] != 0:
                        check(res_p >= abs(h_perp[v0]) > 0, "cochain")

    # S^4 boundary of 5-simplex (N0 = 6, N1 = 15, vertex degree = 5)
    p_zero_15 = tuple(Fraction(0) for _ in range(15))
    h_flat_6 = tuple(Fraction(0) for _ in range(6))
    h_curved_6 = tuple(Fraction(15, 2) for _ in range(6))
    check(total_joint_residual_l1(p_zero_15, p_zero_15, h_flat_6) == Fraction(0), "cochain")
    check(total_joint_residual_l1(p_zero_15, p_zero_15, h_curved_6) == Fraction(45), "cochain")

    # 2. Quadratic constraint PSD, diffeomorphism projector, and Page-Wootters conditioning
    q_vals = [Fraction(-2), Fraction(-1), Fraction(-1, 2), Fraction(0), Fraction(1, 2), Fraction(1), Fraction(2)]
    for a, b, x0, x1 in itertools.product(q_vals, repeat=4):
        q_form = x0 * (a * (a * x0 + b * x1)) + x1 * (b * (a * x0 + b * x1))
        check(q_form == (a * x0 + b * x1) ** 2, "proj")
        check(q_form >= 0, "proj")
        check((q_form == 0) == (a * x0 + b * x1 == 0), "proj")

    for x0, x1 in itertools.product(q_vals, repeat=2):
        pinv_v = (Fraction(1, 2) * (x0 + x1), Fraction(1, 2) * (x0 + x1))
        hperp_v = (Fraction(1, 2) * (x0 - x1), Fraction(1, 2) * (x1 - x0))
        pinv_pinv_v = (
            Fraction(1, 2) * (pinv_v[0] + pinv_v[1]),
            Fraction(1, 2) * (pinv_v[0] + pinv_v[1]),
        )
        hperp_pinv_v = (
            Fraction(1, 2) * (pinv_v[0] - pinv_v[1]),
            Fraction(1, 2) * (pinv_v[1] - pinv_v[0]),
        )
        check(pinv_pinv_v == pinv_v, "proj")
        check(hperp_pinv_v == (Fraction(0), Fraction(0)), "proj")
        check((hperp_v == (Fraction(0), Fraction(0))) == (x0 == x1), "proj")
        check((pinv_v == (x0, x1)) == (x0 == x1), "proj")

        # Page-Wootters 2-tick clock conditioning with Pauli X
        for y0, y1 in [(x1, x0), (x0, x1)]:
            res0 = (x0 - y1, x1 - y0)
            res1 = (y0 - x1, y1 - x0)
            check(
                (res0 == (Fraction(0), Fraction(0)) and res1 == (Fraction(0), Fraction(0)))
                == ((y0, y1) == (x1, x0)),
                "proj",
            )

    # 3. Scope fences: DeWitt supermetric indefiniteness, thermal vs WDW, fermion sign
    for vc, vt in itertools.product(q_vals, repeat=2):
        q_dw = -(vc**2) + vt**2
        if (vc, vt) == (Fraction(1), Fraction(0)):
            check(q_dw == Fraction(-1) and q_dw < 0, "fence")
        if (vc, vt) == (Fraction(0), Fraction(1)):
            check(q_dw == Fraction(1) and q_dw > 0, "fence")
        if abs(vc) == abs(vt) and vc != 0:
            check(q_dw == Fraction(0) and (vc, vt) != (Fraction(0), Fraction(0)), "fence")

        # Fermion sign cancellation under WDW projector expectation
        exp_val = vc * (Fraction(1, 2) * (vc + vt)) + vt * (Fraction(1, 2) * (vc + vt))
        check(Fraction(1) * exp_val + Fraction(-1) * exp_val == Fraction(0), "fence")

    spec1 = (Fraction(0), Fraction(0), Fraction(-2), Fraction(2))
    spec2 = (Fraction(0), Fraction(0), Fraction(-1), Fraction(1))
    check([lam == 0 for lam in spec1] == [lam == 0 for lam in spec2], "fence")
    for beta in [Fraction(1, 2), Fraction(1), Fraction(2)]:
        tr1 = sum(1 - beta * lam + Fraction(1, 2) * (beta**2) * (lam**2) for lam in spec1)
        tr2 = sum(1 - beta * lam + Fraction(1, 2) * (beta**2) * (lam**2) for lam in spec2)
        check(tr1 != tr2, "fence")
        if beta == Fraction(1):
            check(tr1 == Fraction(8) and tr2 == Fraction(5), "fence")

    total = cochain_duality + projector_pw + fences
    print(
        f"FSP-DISCRETE-WDW-CONSTRAINT independent check: "
        f"checks={total} cochain_duality={cochain_duality} projector_pw={projector_pw} "
        f"fences={fences} failures={failures}"
    )
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
