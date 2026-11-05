#!/usr/bin/env python3
"""Independent verification checker for Record TFQ-1219 (FSP-HINGE-LINEON-SIGN-CLAIM).

Target node: FSP-HINGE-LINEON-SIGN-CLAIM
Record: TFQ-1219
Stage: FERMION_SIGN
AuthorityEffect: None
Imports checker infrastructure only; no production implementation.

Verifies:
1. 1D discrete line lattice coordinate ordering and collision avoidance.
2. Collision-free 1D hinge paths strictly preserve relative order (pos1 < pos2).
3. 1D exchange obstruction: lineons on a 1D hinge cannot exchange without passing
   through an identical site or crossing an edge (discrete IVT).
4. Exact traces for supplied commuting (+2) and Pauli (-2) matrix examples,
   plus a noncommuting SU(2) example with positive trace. No general implication
   from noncommutation to negative trace is asserted. Phi1 is a sign indicator;
   Gamma2 is a symbolic scalar angle, not a certificate of matrix membership.
5. Toy trace-squaring map restoring non-negative trace
   on decoupled sheets vs uncancelled defect on corner lineon turns.
6. Worldline permutation sign is trivial (+1) on non-intersecting hinges.
7. Two-label routing fixture (not the BQNF five-way classifier).
"""

from __future__ import annotations

from fractions import Fraction
import json
import sympy as sp
from dataclasses import dataclass
from typing import Literal

# Shared checker infrastructure only; no production implementation is imported.
from pathlib import Path as _Path
import sys as _sys
_sys.path.insert(0, str(_Path(__file__).resolve().parents[1]))
from checker_support.boundary import cli, evaluate
from checker_support.domains import integer, rational, sequence
from checker_support.boundary import Violation
from checker_support.cases import Cases


# Exact Gaussian Rational Q(i) 2x2 Matrix arithmetic
from checker_support.gaussian_rational import GaussianRational as ComplexRat


from checker_support.gaussian_matrix2 import GaussianMatrix2 as Mat2x2


def _position(value: object) -> int:
    admitted = integer(value, "lattice position")
    if admitted.bit_length() > 4096:
        raise Violation("resource", "lattice position exceeds 4096 bits")
    return admitted


def _flag(value: object, name: str) -> bool:
    if type(value) is not bool:
        raise Violation("input", name + " requires an exact bool")
    return value


@dataclass(frozen=True, slots=True, init=False)
class LineonPath:
    """Two labelled particles on one line, with immutable simultaneous unit hops.

    Initial positions have at most 4096 bits and there are at most 4096 steps.
    Colliding/unordered paths are admitted descriptions, not defined parities.
    """

    first: int
    second: int
    hops: tuple[tuple[int, int], ...]

    def __init__(self, first: object, second: object, hops: object) -> None:
        first, second = _position(first), _position(second)
        pairs = []
        for hop in sequence(hops, "hops"):
            left, right = sequence(hop, "simultaneous hop", 2)
            pairs.append((integer(left, "unit hop", -1, 1), integer(right, "unit hop", -1, 1)))
        object.__setattr__(self, "first", first)
        object.__setattr__(self, "second", second)
        object.__setattr__(self, "hops", tuple(pairs))

    def preserves_order(self) -> bool:
        distance = self.second - self.first
        if distance <= 0:
            return False
        for left, right in self.hops:
            distance += right - left
            if distance <= 0:
                return False
        return True


def verify_1d_lineon_collision_avoidance(pos1: int, pos2: int, hops: list[tuple[int, int]] | tuple[tuple[int, int], ...]) -> bool:
    return LineonPath(pos1, pos2, hops).preserves_order()


def validate_unit_trajectory(trajectory: object) -> tuple[int, ...]:
    """Return a detached trajectory with exact bounded positions and unit steps."""
    positions = tuple(_position(position) for position in sequence(trajectory, "trajectory"))
    for left, right in zip(positions, positions[1:]):
        integer(right-left, "unit hop", -1, 1)
    return positions


def verify_discrete_ivt_collision_site(
    p1: int, p2: int, traj1: list[int] | tuple[int, ...], traj2: list[int] | tuple[int, ...]
) -> tuple[bool, int]:
    """Legacy witness pair: first site meeting, else left-to-right edge start; -1 means no exchange.

    Trajectories must describe swapped endpoints and have equal nonzero lengths.
    A site witness is preferred even if an edge crossing occurred earlier.
    """
    p1, p2 = _position(p1), _position(p2)
    first = validate_unit_trajectory(traj1)
    second = validate_unit_trajectory(traj2)
    if len(first) != len(second) or not first:
        raise Violation("input", "trajectories require equal nonzero lengths")
    if p1 >= p2:
        return False, -1
    if first[0] != p1 or second[0] != p2:
        return False, -1
    if first[-1] != p2 or second[-1] != p1:
        return False, -1

    for t in range(len(first)):
        if first[t] == second[t]:
            return True, t
    for t in range(len(first) - 1):
        if first[t] < second[t] and first[t + 1] > second[t + 1]:
            return True, t
    return False, -1


def compute_commutator_holonomy_trace(b_xy: Mat2x2, b_yz: Mat2x2) -> ComplexRat:
    if type(b_xy) is not Mat2x2 or type(b_yz) is not Mat2x2:
        raise Violation("input", "commutator requires exact GaussianMatrix2 operands")
    inv_xy = b_xy.inv()
    inv_yz = b_yz.inv()
    m_hinge = b_xy.mul(b_yz).mul(inv_xy).mul(inv_yz)
    return m_hinge.trace()


def evaluate_foliated_projected_trace(has_corner_lineon: bool, base_trace_re: Fraction) -> Fraction:
    has_corner_lineon = _flag(has_corner_lineon, "corner-lineon flag")
    base_trace_re = rational(base_trace_re, "base trace")
    if has_corner_lineon:
        return base_trace_re
    return base_trace_re * base_trace_re


def compute_curvature_gamma2(trace_re: Fraction) -> sp.Expr:
    """Exact symbolic acos(trace/2); no SU(2) certificate or numeric approximation.

    Only the five integral traces are simplified. Other admitted rationals use
    an unevaluated expression, avoiding an implicit symbolic simplification job.
    """
    trace_re = rational(trace_re, "trace", minimum=-2)
    if trace_re > 2:
        raise Violation("input", "trace must lie in [-2,2]")
    if trace_re.denominator == 1:
        return {-2: sp.pi, -1: 2 * sp.pi / 3, 0: sp.pi / 2,
                1: sp.pi / 3, 2: sp.Integer(0)}[trace_re.numerator]
    return sp.acos(sp.Rational(trace_re.numerator, 2 * trace_re.denominator), evaluate=False)


def compute_defect_mass_phi1(trace_re: Fraction) -> int:
    """Computes defect mass Phi1: 0 for non-negative trace, 2 for negative trace."""
    trace_re = rational(trace_re, "defect trace")
    return 0 if trace_re >= Fraction(0, 1) else 2


def evaluate_terminal_routing(is_corner_lineon: bool, is_nonabelian: bool) -> Literal["OPEN_SIGN_OBSTRUCTION", "EXACT_REPAIR"]:
    """Returns one of two fixture labels, not a BQNF five-way classification."""
    is_corner_lineon = _flag(is_corner_lineon, "corner-lineon flag")
    is_nonabelian = _flag(is_nonabelian, "nonabelian flag")
    if is_corner_lineon or is_nonabelian:
        return "OPEN_SIGN_OBSTRUCTION"
    return "EXACT_REPAIR"


def compute_lineon_permutation_parity(p1: int, p2: int, hops: list[tuple[int, int]] | tuple[tuple[int, int], ...]) -> int:
    """Computes braid permutation parity exponent for 1D lineon trajectories.

    Under 1D collision avoidance, worldline exchange is strictly obstructed,
    restricting the braid permutation to the trivial identity permutation
    with transposition parity exponent 0.
    Returns 0 if the trajectory strictly avoids collision (preserving pos1 < pos2).
    Refuses malformed, colliding or unordered paths; no odd parity is inferred.
    """
    is_valid = verify_1d_lineon_collision_avoidance(p1, p2, hops)
    if not is_valid:
        raise Violation("input", "parity is undefined for colliding or unordered trajectories")
    return 0


def check_lineon_paths(checks: Cases) -> None:
    for p1 in [-10, -3, 0, 2]:
        for p2 in [p1 + 1, p1 + 5, p1 + 12]:
            checks.append((f"static_ordering_valid_{p1}_{p2}", p1 < p2))
            checks.append(
                (f"static_collision_refusal_equal_{p1}_case_{p2}", not verify_1d_lineon_collision_avoidance(p1, p1, []))
            )
            checks.append(
                (f"static_ordering_refusal_inverted_{p2}_{p1}", not verify_1d_lineon_collision_avoidance(p2, p1, []))
            )

    # Family 2: 1D Collision-free hop trajectories
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
    ]
    for idx, (p1, p2, hops) in enumerate(refusal_paths):
        checks.append((f"collision_path_refused_{idx}", not verify_1d_lineon_collision_avoidance(p1, p2, hops)))

    # Family 3: Discrete IVT exchange obstruction
    checks.append(("invalid_unit_hop_refused", not evaluate(verify_1d_lineon_collision_avoidance, 5, 7, [(2, 0)]).ok))
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


def check_holonomy_examples(checks: Cases) -> tuple[ComplexRat, ComplexRat]:
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
    checks.append(("curvature_gamma2_abelian_is_zero", compute_curvature_gamma2(tr_abelian.re) == 0))
    checks.append(("curvature_gamma2_nonabelian_is_pi", compute_curvature_gamma2(tr_nonab.re) == sp.pi))

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
    checks.append(("su2_counterexample_unitary", a_su2.is_unitary() and b_su2.is_unitary()))
    checks.append(("su2_counterexample_det_one", a_su2.det() == one_c and b_su2.det() == one_c))
    checks.append(("su2_counterexample_noncommuting", a_su2.mul(b_su2) != b_su2.mul(a_su2)))
    checks.append(("su2_counterexample_trace_re_is_14_over_25", tr_su2_ce.re == Fraction(14, 25)))
    checks.append(("su2_counterexample_trace_im_is_zero", tr_su2_ce.im == Fraction(0, 1)))
    checks.append(("su2_counterexample_trace_strictly_positive", tr_su2_ce.re > Fraction(0, 1)))
    return tr_abelian, tr_nonab


def check_toy_projection_and_routing(checks: Cases, tr_abelian: ComplexRat, tr_nonab: ComplexRat) -> None:
    proj_tr_decoupled_ab = evaluate_foliated_projected_trace(False, tr_abelian.re)
    proj_tr_decoupled_nonab = evaluate_foliated_projected_trace(False, tr_nonab.re)
    checks.append(("projected_trace_decoupled_ab_positive", proj_tr_decoupled_ab == Fraction(4, 1)))
    checks.append(("projected_trace_decoupled_nonab_positive", proj_tr_decoupled_nonab == Fraction(4, 1)))
    checks.append(("projected_trace_decoupled_nonneg", proj_tr_decoupled_nonab >= Fraction(0, 1)))

    # Corner lineon turn: uncancelled negative curvature persists (-2 < 0)
    proj_tr_corner = evaluate_foliated_projected_trace(True, tr_nonab.re)
    checks.append(("projected_trace_corner_lineon_negative", proj_tr_corner == Fraction(-2, 1)))
    checks.append(("projected_trace_corner_lineon_strictly_less_zero", proj_tr_corner < Fraction(0, 1)))

    # Family 6: Trivial permutation sign (+1) on 1D hinge line
    parity_exp = compute_lineon_permutation_parity(0, 1, [])
    perm_sign = (-1) ** parity_exp
    checks.append(("collision_free_permutation_sign_trivial", perm_sign == 1))
    checks.append(("permutation_parity_exponent_zero", parity_exp == 0))

    # Family 7: Two-label routing fixture (not the BQNF five-way classifier)
    route_straight = evaluate_terminal_routing(is_corner_lineon=False, is_nonabelian=False)
    route_corner = evaluate_terminal_routing(is_corner_lineon=True, is_nonabelian=True)
    checks.append(("terminal_route_straight_decoupled_is_exact_repair", route_straight == "EXACT_REPAIR"))
    checks.append(("terminal_route_corner_turn_is_open_sign_obstruction", route_corner == "OPEN_SIGN_OBSTRUCTION"))


def check_y_junction_convention(checks: Cases, tr_abelian: ComplexRat) -> None:
    y_adj = {("0", "X"), ("X", "0"), ("0", "Y"), ("Y", "0"), ("0", "Z"), ("Z", "0")}
    y_traj = [("X", "Y"), ("0", "Y"), ("Z", "Y"), ("Z", "0"), ("Z", "X"), ("0", "X"), ("Y", "X")]
    y_coll_free = all(u != v for u, v in y_traj)
    y_steps_ok = all(
        (y_traj[t][0] == y_traj[t + 1][0] and (y_traj[t][1], y_traj[t + 1][1]) in y_adj)
        or (y_traj[t][1] == y_traj[t + 1][1] and (y_traj[t][0], y_traj[t + 1][0]) in y_adj)
        for t in range(len(y_traj) - 1)
    )
    y_exchanged = y_traj[-1][0] == y_traj[0][1] and y_traj[-1][1] == y_traj[0][0]
    # Supplied fermionic sign convention, not a derivation of physical statistics.
    y_sign = -1 if y_exchanged else 1
    checks.append(("y_junction_6step_collision_free_exchange", len(y_traj) - 1 == 6 and y_coll_free and y_steps_ok and y_exchanged))
    checks.append(("y_junction_exchange_sign_by_convention", y_sign == -1 and y_sign * tr_abelian.re == Fraction(-2, 1)))


def run_checks() -> dict[str, object]:
    checks = Cases()

    # Family 1: 1D Lineon coordinate ordering & static avoidance
    check_lineon_paths(checks)

    # Family 4: Exact higher-form 2-gauge commutator holonomy traces over Q(i)
    tr_abelian, tr_nonab = check_holonomy_examples(checks)

    # Family 5: Toy trace-squaring rule; no categorical construction
    # Decoupled straight lineon: projected trace |base_tr|^2 = 4 >= 0
    check_toy_projection_and_routing(checks, tr_abelian, tr_nonab)

    # Family 8: Multi-hinge Y-junction 6-step collision-free exchange vs axis conservation
    check_y_junction_convention(checks, tr_abelian)

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


def main() -> int:
    result = run_checks()
    print(json.dumps(result, indent=2))
    if not result["all_passed"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(cli(main))
