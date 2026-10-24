#!/usr/bin/env python3
"""Independent exact rational verifier for TFQ-0107 (FINITE_QG, GAP).

Verifies with Python Fractions (no Lean dependency):
1. Exact rational replay of code/rust/src/general_relativity/field_equation.rs:
   - regge_edge_residual = curvature_grad - lambda * vol_grad
   - flat interior replay (curvature_grad = 0): residual == 0 at lambda = 0, and
     residual == -cosmo_grad != 0 for lambda != 0, vol_grad != 0
   - relaxation step next_sq = current_sq - lr * res fixed-point iff res == 0
2. Exact rational replay of code/rust/src/general_relativity/hamiltonian_constraint.rs:
   - 4-vertex tetrahedral dual volume share 4 * (vol3 / 4) == vol3 and zero-momentum kinetic term == 0
   - DeWitt kinetic form (1/v_vol) * (sum_pi_sq - 1/2 * sum_pi^2): null mode on 2 equal momenta (p, p)
     and negative mode -(3/2)*p^2/v_vol < 0 on 3 equal momenta (p, p, p)
3. Scope fences:
   - Underdetermination of caller-supplied lambda in both Hamiltonian and Regge edge equations
   - 3D spatial rescaling mismatch: s * curv vs s^3 * v_vol leaves residual curv * s * (s^2 - 1)
   - Two-hinge opposite-deficit cancellation kernel: (+delta, -delta) gives curvature_grad = 0
     while eps1^2 + eps2^2 = 2 * delta^2 > 0.
"""

from __future__ import annotations

from fractions import Fraction
import itertools
import sys


def cosmo_grad(lam: Fraction, vol_grad: Fraction) -> Fraction:
    return lam * vol_grad


def regge_edge_residual(curv_grad: Fraction, lam: Fraction, vol_grad: Fraction) -> Fraction:
    return curv_grad - cosmo_grad(lam, vol_grad)


def regge_relaxation_step_sq(curr_sq: Fraction, lr: Fraction, res: Fraction) -> Fraction:
    return curr_sq - lr * res


def vertex_dual_volume_share(vol3: Fraction) -> Fraction:
    return Fraction(1, 4) * vol3


def vertex_kinetic_term(v_vol: Fraction, sum_pi_sq: Fraction, sum_pi: Fraction) -> Fraction:
    return (Fraction(1, 1) / v_vol) * (sum_pi_sq - Fraction(1, 2) * (sum_pi**2))


def vertex_hamiltonian_residual(
    kin: Fraction, curv: Fraction, lam: Fraction, v_vol: Fraction
) -> Fraction:
    return kin - curv + Fraction(2, 1) * lam * v_vol


def main() -> int:
    checks = 0
    regge_checks = 0
    ham_checks = 0
    fence_checks = 0
    failures = 0

    def check(cond: bool, bucket: str, msg: str) -> None:
        nonlocal checks, regge_checks, ham_checks, fence_checks, failures
        checks += 1
        if bucket == "regge":
            regge_checks += 1
        elif bucket == "ham":
            ham_checks += 1
        elif bucket == "fence":
            fence_checks += 1
        if not cond:
            failures += 1
            print(f"FAIL [{bucket}]: {msg}", file=sys.stderr)

    rats = [Fraction(-2, 1), Fraction(-1, 2), Fraction(1, 3), Fraction(1, 2), Fraction(3, 2)]
    pos_rats = [Fraction(1, 3), Fraction(1, 2), Fraction(1, 1), Fraction(2, 1), Fraction(5, 2)]

    # 1. Regge field equation rational replay
    for lam, vg in itertools.product(rats, rats):
        check(
            regge_edge_residual(Fraction(0), Fraction(0), vg) == Fraction(0),
            "regge",
            "flat interior zero lambda vanishes",
        )
        cg = cosmo_grad(lam, vg)
        res_flat = regge_edge_residual(Fraction(0), lam, vg)
        check(
            res_flat == -cg and cg != Fraction(0),
            "regge",
            "flat interior nonzero lambda equals -cosmo_grad != 0",
        )
        check(
            regge_edge_residual(cg, lam, vg) == Fraction(0),
            "regge",
            "residual vanishes at curvature_grad = lambda * vol_grad",
        )

    for l2, lr, res in itertools.product(pos_rats, rats, [Fraction(0)] + rats):
        next_sq = regge_relaxation_step_sq(l2, lr, res)
        check(
            (next_sq == l2) == (res == Fraction(0)),
            "regge",
            "relaxation step fixed point iff res == 0",
        )

    # 2. Simplicial Hamiltonian constraint rational replay
    for v3, v_vol in itertools.product(pos_rats, pos_rats):
        check(
            Fraction(4, 1) * vertex_dual_volume_share(v3) == v3,
            "ham",
            "4 vertex shares sum to tetrahedron volume",
        )
        check(
            vertex_kinetic_term(v_vol, Fraction(0), Fraction(0)) == Fraction(0),
            "ham",
            "zero momenta give zero kinetic term",
        )

    for v_vol, p in itertools.product(pos_rats, rats):
        kin2 = vertex_kinetic_term(v_vol, p * p + p * p, p + p)
        kin3 = vertex_kinetic_term(v_vol, p * p + p * p + p * p, p + p + p)
        check(kin2 == Fraction(0), "ham", "2-edge equal-momentum mode is null")
        check(
            kin3 == -Fraction(3, 2) * (p * p) / v_vol and kin3 < Fraction(0),
            "ham",
            "3-edge equal-momentum mode is strictly negative",
        )

    # 3. Scope fences: Lambda underdetermination, 3D scaling mismatch, and 2-hinge cancellation
    for kin, curv, v_vol in itertools.product(rats, rats, pos_rats):
        lam_sol = (curv - kin) / (Fraction(2, 1) * v_vol)
        check(
            vertex_hamiltonian_residual(kin, curv, lam_sol, v_vol) == Fraction(0),
            "fence",
            "caller-supplied lambda solves Hamiltonian constraint for any (kin, curv, v_vol)",
        )

    for curv_grad, vg in itertools.product(rats, rats):
        lam_edge = curv_grad / vg
        check(
            regge_edge_residual(curv_grad, lam_edge, vg) == Fraction(0),
            "fence",
            "caller-supplied lambda solves Regge edge equation for any (curv_grad, vol_grad)",
        )

    for lam, v_vol, s in itertools.product(rats, pos_rats, [Fraction(1, 2), Fraction(2, 1), Fraction(3, 1)]):
        curv = Fraction(2, 1) * lam * v_vol
        check(
            vertex_hamiltonian_residual(Fraction(0), curv, lam, v_vol) == Fraction(0),
            "fence",
            "unscaled static balance",
        )
        res_scaled = vertex_hamiltonian_residual(Fraction(0), s * curv, lam, (s**3) * v_vol)
        check(
            res_scaled == curv * s * (s * s - Fraction(1, 1)) and res_scaled != Fraction(0),
            "fence",
            "3D rescaling breaks static Hamiltonian balance unless lambda scales as s^-2",
        )
        check(
            vertex_hamiltonian_residual(Fraction(0), s * curv, lam / (s * s), (s**3) * v_vol)
            == Fraction(0),
            "fence",
            "rescaling lambda by s^-2 restores static balance",
        )

    for delta, da, vg in itertools.product(rats, rats, rats):
        cg_two = delta * da + (-delta) * da
        sq_norm = delta * delta + (-delta) * (-delta)
        check(
            cg_two == Fraction(0)
            and regge_edge_residual(cg_two, Fraction(0), vg) == Fraction(0)
            and sq_norm == Fraction(2, 1) * (delta * delta)
            and sq_norm > Fraction(0),
            "fence",
            "two-hinge opposite deficits cancel in curvature_grad while sq_norm > 0",
        )

    print(
        f"checks={checks} regge={regge_checks} ham={ham_checks} "
        f"fence={fence_checks} failures={failures}"
    )
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
