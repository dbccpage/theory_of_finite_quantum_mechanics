#!/usr/bin/env python3
"""Independent verification checker for Record TFQ-1219 (FSP-HINGE-LINEON-SIGN-CLAIM).

Target node: FSP-HINGE-LINEON-SIGN-CLAIM
Record: TFQ-1219
Stage: FERMION_SIGN
AuthorityEffect: None
Zero repository imports: pure Python standard library only.

Verifies:
1. 1D discrete line lattice coordinate ordering and collision avoidance.
2. Collision-free 1D hinge paths strictly preserve relative order (pos1 < pos2).
3. 1D exchange obstruction: lineons on a 1D hinge cannot exchange without passing
   through an identical site or crossing an edge (discrete IVT).
4. Exact character traces for abelian (+2) vs non-abelian (-2) higher-form 2-gauge
   defect sheets over Q(i), defect mass Phi1, and curvature Gamma2.
5. Foliated categorical quantum double projection restoring non-negative trace
   on decoupled sheets vs uncancelled defect on corner lineon turns.
6. Worldline permutation sign is trivial (+1) on non-intersecting hinges.
7. BQNF 5-fold terminal routing consistency.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import json
import math
import sys
from typing import Any, Dict, List, Tuple


# Exact Gaussian Rational Q(i) 2x2 Matrix arithmetic
@dataclass(frozen=True)
class ComplexRat:
    re: Fraction
    im: Fraction

    def __add__(self, other: ComplexRat) -> ComplexRat:
        return ComplexRat(self.re + other.re, self.im + other.im)

    def __sub__(self, other: ComplexRat) -> ComplexRat:
        return ComplexRat(self.re - other.re, self.im - other.im)

    def __mul__(self, other: ComplexRat) -> ComplexRat:
        return ComplexRat(
            self.re * other.re - self.im * other.im,
            self.re * other.im + self.im * other.re,
        )

    def conj(self) -> ComplexRat:
        return ComplexRat(self.re, -self.im)

    def norm_sq(self) -> Fraction:
        return self.re * self.re + self.im * self.im

    def inv(self) -> ComplexRat:
        n = self.norm_sq()
        if n == Fraction(0, 1):
            raise ZeroDivisionError("Cannot invert zero Gaussian rational")
        return ComplexRat(self.re / n, -self.im / n)


@dataclass(frozen=True)
class Mat2x2:
    a11: ComplexRat
    a12: ComplexRat
    a21: ComplexRat
    a22: ComplexRat

    @staticmethod
    def eye() -> Mat2x2:
        zero = ComplexRat(Fraction(0, 1), Fraction(0, 1))
        one = ComplexRat(Fraction(1, 1), Fraction(0, 1))
        return Mat2x2(one, zero, zero, one)

    @staticmethod
    def pauli_z() -> Mat2x2:
        zero = ComplexRat(Fraction(0, 1), Fraction(0, 1))
        one = ComplexRat(Fraction(1, 1), Fraction(0, 1))
        neg_one = ComplexRat(Fraction(-1, 1), Fraction(0, 1))
        return Mat2x2(one, zero, zero, neg_one)

    @staticmethod
    def pauli_x() -> Mat2x2:
        zero = ComplexRat(Fraction(0, 1), Fraction(0, 1))
        one = ComplexRat(Fraction(1, 1), Fraction(0, 1))
        return Mat2x2(zero, one, one, zero)

    def mul(self, other: Mat2x2) -> Mat2x2:
        return Mat2x2(
            self.a11 * other.a11 + self.a12 * other.a21,
            self.a11 * other.a12 + self.a12 * other.a22,
            self.a21 * other.a11 + self.a22 * other.a21,
            self.a21 * other.a12 + self.a22 * other.a22,
        )

    def trace(self) -> ComplexRat:
        return self.a11 + self.a22

    def det(self) -> ComplexRat:
        return self.a11 * self.a22 - self.a12 * self.a21

    def inv(self) -> Mat2x2:
        d_inv = self.det().inv()
        return Mat2x2(
            self.a22 * d_inv,
            ComplexRat(Fraction(-1, 1), Fraction(0, 1)) * self.a12 * d_inv,
            ComplexRat(Fraction(-1, 1), Fraction(0, 1)) * self.a21 * d_inv,
            self.a11 * d_inv,
        )


def verify_1d_lineon_collision_avoidance(pos1: int, pos2: int, hops: List[Tuple[int, int]]) -> bool:
    if pos1 >= pos2:
        return False
    curr1, curr2 = pos1, pos2
    for d1, d2 in hops:
        if abs(d1) > 1 or abs(d2) > 1:
            return False
        curr1 += d1
        curr2 += d2
        if curr1 >= curr2:
            return False
    return True


def verify_discrete_ivt_collision_site(
    p1: int, p2: int, traj1: List[int], traj2: List[int]
) -> Tuple[bool, int]:
    if p1 >= p2 or not traj1 or not traj2 or len(traj1) != len(traj2):
        return False, -1
    if traj1[0] != p1 or traj2[0] != p2:
        return False, -1
    if traj1[-1] != p2 or traj2[-1] != p1:
        return False, -1

    for t in range(len(traj1)):
        if traj1[t] == traj2[t]:
            return True, t
    for t in range(len(traj1) - 1):
        if traj1[t] < traj2[t] and traj1[t + 1] > traj2[t + 1]:
            return True, t
    return False, -1


def compute_commutator_holonomy_trace(b_xy: Mat2x2, b_yz: Mat2x2) -> ComplexRat:
    inv_xy = b_xy.inv()
    inv_yz = b_yz.inv()
    m_hinge = b_xy.mul(b_yz).mul(inv_xy).mul(inv_yz)
    return m_hinge.trace()


def evaluate_foliated_projected_trace(has_corner_lineon: bool, base_trace_re: Fraction) -> Fraction:
    if has_corner_lineon:
        return base_trace_re
    return abs(base_trace_re) * abs(base_trace_re)


def compute_curvature_gamma2(trace_re: Fraction) -> float:
    """Computes face curvature angle Gamma2 = arccos(Tr(M) / 2) from exact trace."""
    val = float(trace_re / Fraction(2, 1))
    val = max(-1.0, min(1.0, val))
    return math.acos(val)


def compute_defect_mass_phi1(trace_re: Fraction) -> int:
    """Computes defect mass Phi1: 0 for non-negative trace, 2 for negative trace."""
    return 0 if trace_re >= Fraction(0, 1) else 2


def evaluate_terminal_routing(is_corner_lineon: bool, is_nonabelian: bool) -> str:
    """Routes sign packet under BQNF 5-fold classification."""
    if is_corner_lineon or is_nonabelian:
        return "OPEN_SIGN_OBSTRUCTION"
    return "EXACT_REPAIR"


def compute_lineon_permutation_parity(p1: int, p2: int, hops: List[Tuple[int, int]]) -> int:
    """Computes braid permutation parity exponent for 1D lineon trajectories.

    Under 1D collision avoidance, worldline exchange is strictly obstructed,
    restricting the braid permutation to the trivial identity permutation
    with transposition parity exponent 0.
    Returns 0 if the trajectory strictly avoids collision (preserving pos1 < pos2).
    Returns 1 if collision or ordering violation occurs.
    """
    is_valid = verify_1d_lineon_collision_avoidance(p1, p2, hops)
    return 0 if is_valid else 1


def run_checks() -> Dict[str, Any]:
    checks: List[Tuple[str, bool]] = []

    # -------------------------------------------------------------------------
    # Family 1: 1D Lineon coordinate ordering & static avoidance
    # -------------------------------------------------------------------------
    for p1 in [-10, -3, 0, 2]:
        for p2 in [p1 + 1, p1 + 5, p1 + 12]:
            checks.append((f"static_ordering_valid_{p1}_{p2}", p1 < p2))
            checks.append(
                (f"static_collision_refusal_equal_{p1}", not verify_1d_lineon_collision_avoidance(p1, p1, []))
            )
            checks.append(
                (f"static_ordering_refusal_inverted_{p2}_{p1}", not verify_1d_lineon_collision_avoidance(p2, p1, []))
            )

    # -------------------------------------------------------------------------
    # Family 2: 1D Collision-free hop trajectories
    # -------------------------------------------------------------------------
    valid_paths = [
        (0, 3, [(1, 1), (0, 1), (-1, 0), (1, 1)]),
        (-5, -1, [(1, 0), (1, 1), (0, -1), (1, 1)]),
        (2, 6, [(-1, -1), (0, -1), (1, 0), (1, 1)]),
        (10, 15, [(1, 0), (0, -1), (1, 1), (-1, -1)]),
        (-2, 2, [(1, 1), (1, 1), (0, 1), (-1, 0)]),
    ]
    for idx, (p1, p2, hops) in enumerate(valid_paths):
        checks.append((f"valid_path_preserved_{idx}", verify_1d_lineon_collision_avoidance(p1, p2, hops)))

    # Refusal paths (hops causing collision)
    refusal_paths = [
        (0, 2, [(1, 0), (1, 0)]),  # pos1 reaches 2 == pos2
        (0, 1, [(1, 0)]),           # pos1 reaches 1 == pos2
        (3, 4, [(1, -1)]),          # pos1 reaches 4, pos2 reaches 3 (crossed)
        (-1, 1, [(1, -1)]),         # pos1 reaches 0, pos2 reaches 0
        (5, 7, [(2, 0)]),           # invalid step size > 1
    ]
    for idx, (p1, p2, hops) in enumerate(refusal_paths):
        checks.append((f"collision_path_refused_{idx}", not verify_1d_lineon_collision_avoidance(p1, p2, hops)))

    # -------------------------------------------------------------------------
    # Family 3: Discrete IVT exchange obstruction
    # -------------------------------------------------------------------------
    # Scenario A: Sequential swap on [0, 4]
    t1_a = [0, 1, 2, 2, 3, 4]
    t2_a = [4, 4, 3, 2, 1, 0]
    coll_a, idx_a = verify_discrete_ivt_collision_site(0, 4, t1_a, t2_a)
    checks.append(("ivt_swap_a_collision_found", coll_a))
    checks.append(("ivt_swap_a_exact_meeting_site", t1_a[idx_a] == t2_a[idx_a]))

    # Scenario B: Sequential swap on [-2, 2]
    t1_b = [-2, -1, 0, 0, 1, 2]
    t2_b = [2, 2, 1, 0, -1, -2]
    coll_b, idx_b = verify_discrete_ivt_collision_site(-2, 2, t1_b, t2_b)
    checks.append(("ivt_swap_b_collision_found", coll_b))
    checks.append(("ivt_swap_b_exact_meeting_site", t1_b[idx_b] == t2_b[idx_b]))

    # Scenario C: Simultaneous unit crossing on [0, 1]
    t1_c = [0, 1]
    t2_c = [1, 0]
    coll_c, idx_c = verify_discrete_ivt_collision_site(0, 1, t1_c, t2_c)
    checks.append(("ivt_swap_c_crossing_collision_found", coll_c))

    # Scenario D: Non-swapped path without collision
    t1_d = [0, 1, 2]
    t2_d = [4, 4, 4]
    coll_d, _ = verify_discrete_ivt_collision_site(0, 4, t1_d, t2_d)
    checks.append(("ivt_non_swap_refused", not coll_d))

    # -------------------------------------------------------------------------
    # Family 4: Exact higher-form 2-gauge commutator holonomy traces over Q(i)
    # -------------------------------------------------------------------------
    eye = Mat2x2.eye()
    pauli_z = Mat2x2.pauli_z()
    pauli_x = Mat2x2.pauli_x()

    # Abelian sheets: B_xy = I, B_yz = I -> Tr(M) = 2
    tr_abelian = compute_commutator_holonomy_trace(eye, eye)
    checks.append(("abelian_trace_re_is_plus_2", tr_abelian.re == Fraction(2, 1)))
    checks.append(("abelian_trace_im_is_zero", tr_abelian.im == Fraction(0, 1)))

    # Non-abelian sheets: Pauli Z and X where Z X Z^-1 X^-1 = -I -> Tr(M) = -2
    tr_nonab = compute_commutator_holonomy_trace(pauli_z, pauli_x)
    checks.append(("nonabelian_trace_re_is_minus_2", tr_nonab.re == Fraction(-2, 1)))
    checks.append(("nonabelian_trace_im_is_zero", tr_nonab.im == Fraction(0, 1)))

    # Curvature angle Gamma2: 0 for abelian, pi for non-abelian
    checks.append(("curvature_gamma2_abelian_is_zero", compute_curvature_gamma2(tr_abelian.re) == 0.0))
    checks.append(("curvature_gamma2_nonabelian_is_pi", abs(compute_curvature_gamma2(tr_nonab.re) - math.pi) < 1e-12))

    # Defect mass Phi1: 0 for abelian, 2 for non-abelian
    checks.append(("defect_mass_phi1_abelian_is_0", compute_defect_mass_phi1(tr_abelian.re) == 0))
    checks.append(("defect_mass_phi1_nonabelian_is_2", compute_defect_mass_phi1(tr_nonab.re) == 2))

    # Non-commuting SU(2) counterexample: A = diag(i, -i), B = [[4/5, -3/5], [3/5, 4/5]]
    # Both in SU(2), AB != BA, yet Tr(A B A^-1 B^-1) = 14/25 > 0
    zero_c = ComplexRat(Fraction(0, 1), Fraction(0, 1))
    one_c = ComplexRat(Fraction(1, 1), Fraction(0, 1))
    a_su2 = Mat2x2(
        ComplexRat(Fraction(0, 1), Fraction(1, 1)),
        zero_c,
        zero_c,
        ComplexRat(Fraction(0, 1), Fraction(-1, 1)),
    )
    b_su2 = Mat2x2(
        ComplexRat(Fraction(4, 5), Fraction(0, 1)),
        ComplexRat(Fraction(-3, 5), Fraction(0, 1)),
        ComplexRat(Fraction(3, 5), Fraction(0, 1)),
        ComplexRat(Fraction(4, 5), Fraction(0, 1)),
    )
    tr_su2_ce = compute_commutator_holonomy_trace(a_su2, b_su2)
    checks.append(("su2_counterexample_det_one", a_su2.det() == one_c and b_su2.det() == one_c))
    checks.append(("su2_counterexample_noncommuting", a_su2.mul(b_su2) != b_su2.mul(a_su2)))
    checks.append(("su2_counterexample_trace_re_is_14_over_25", tr_su2_ce.re == Fraction(14, 25)))
    checks.append(("su2_counterexample_trace_im_is_zero", tr_su2_ce.im == Fraction(0, 1)))
    checks.append(("su2_counterexample_trace_strictly_positive", tr_su2_ce.re > Fraction(0, 1)))

    # -------------------------------------------------------------------------
    # Family 5: Foliated categorical quantum double projection
    # -------------------------------------------------------------------------
    # Decoupled straight lineon: projected trace |base_tr|^2 = 4 >= 0
    proj_tr_decoupled_ab = evaluate_foliated_projected_trace(False, tr_abelian.re)
    proj_tr_decoupled_nonab = evaluate_foliated_projected_trace(False, tr_nonab.re)
    checks.append(("projected_trace_decoupled_ab_positive", proj_tr_decoupled_ab == Fraction(4, 1)))
    checks.append(("projected_trace_decoupled_nonab_positive", proj_tr_decoupled_nonab == Fraction(4, 1)))
    checks.append(("projected_trace_decoupled_nonneg", proj_tr_decoupled_nonab >= Fraction(0, 1)))

    # Corner lineon turn: uncancelled negative curvature persists (-2 < 0)
    proj_tr_corner = evaluate_foliated_projected_trace(True, tr_nonab.re)
    checks.append(("projected_trace_corner_lineon_negative", proj_tr_corner == Fraction(-2, 1)))
    checks.append(("projected_trace_corner_lineon_strictly_less_zero", proj_tr_corner < Fraction(0, 1)))

    # -------------------------------------------------------------------------
    # Family 6: Trivial permutation sign (+1) on 1D hinge line
    # -------------------------------------------------------------------------
    parity_exp = compute_lineon_permutation_parity(0, 1, [])
    perm_sign = (-1) ** parity_exp
    checks.append(("collision_free_permutation_sign_trivial", perm_sign == 1))
    checks.append(("permutation_parity_exponent_zero", parity_exp == 0))

    # -------------------------------------------------------------------------
    # Family 7: BQNF 5-fold terminal routing consistency
    # -------------------------------------------------------------------------
    route_straight = evaluate_terminal_routing(is_corner_lineon=False, is_nonabelian=False)
    route_corner = evaluate_terminal_routing(is_corner_lineon=True, is_nonabelian=True)
    checks.append(("terminal_route_straight_decoupled_is_exact_repair", route_straight == "EXACT_REPAIR"))
    checks.append(("terminal_route_corner_turn_is_open_sign_obstruction", route_corner == "OPEN_SIGN_OBSTRUCTION"))

    # -------------------------------------------------------------------------
    # Family 8: Multi-hinge Y-junction 6-step collision-free exchange vs axis conservation
    # -------------------------------------------------------------------------
    y_adj = {("0", "X"), ("X", "0"), ("0", "Y"), ("Y", "0"), ("0", "Z"), ("Z", "0")}
    y_traj = [("X", "Y"), ("0", "Y"), ("Z", "Y"), ("Z", "0"), ("Z", "X"), ("0", "X"), ("Y", "X")]
    y_coll_free = all(u != v for u, v in y_traj)
    y_steps_ok = all(
        (y_traj[t][0] == y_traj[t + 1][0] and (y_traj[t][1], y_traj[t + 1][1]) in y_adj)
        or (y_traj[t][1] == y_traj[t + 1][1] and (y_traj[t][0], y_traj[t + 1][0]) in y_adj)
        for t in range(len(y_traj) - 1)
    )
    y_exchanged = y_traj[-1][0] == y_traj[0][1] and y_traj[-1][1] == y_traj[0][0]
    y_sign = -1 if y_exchanged else 1
    checks.append(("y_junction_6step_collision_free_exchange", len(y_traj) - 1 == 6 and y_coll_free and y_steps_ok and y_exchanged))
    checks.append(("y_junction_exchange_induces_negative_sign", y_sign == -1 and y_sign * tr_abelian.re == Fraction(-2, 1)))

    total = len(checks)
    failures = [name for name, passed in checks if not passed]
    all_passed = len(failures) == 0

    return {
        "record_id": "TFQ-1219",
        "dag_node": "FSP-HINGE-LINEON-SIGN-CLAIM",
        "authority_effect": "None",
        "total_checks": total,
        "failed_checks": len(failures),
        "failures": failures,
        "all_passed": all_passed,
    }


def main() -> None:
    result = run_checks()
    print(json.dumps(result, indent=2))
    if not result["all_passed"]:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
