"""Countermodel for a Phi_1-decreasing repair policy on two finite windows.

Degree-1 data over Q. The one-cell window has d0 = 0 and d1 = id. The filled
triangle is the WDP-CH04-P08 complex, scaled by the same dyadic coefficient and
certified on its own edges. Checked steps strictly decrease Phi_1, keep R_cl at
the operator-norm bound, and stay off ExactClass. No continuum limit, discrete
rank, or uniform additive drop is admitted.
"""

from __future__ import annotations

from collections.abc import Callable
from fractions import Fraction
from typing import NamedTuple

PREFIX = (0, 1, 2)
SUCCESSOR = 3
FAR_N = 10
EXACT_CLASS = 0
CLOSED_RESIDUAL = 1
ACTIVE_CLOSURE_FAILURE = 2
ZERO = Fraction(0)
ONE = Fraction(1)
UNIT_CIRCULATION = (ONE, ONE, -ONE)

Cochain = tuple[Fraction, Fraction, Fraction]
WitnessValue = int | Fraction | tuple[int, ...] | tuple[Fraction, ...]


class State(NamedTuple):
    phi: Fraction
    gamma: Fraction
    r_cl: Fraction
    kind: int


class TriangleState(NamedTuple):
    phi: Fraction
    gamma: Fraction
    r_cl: Fraction
    kind: int
    delta: Cochain


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def _nat(value: int) -> int:
    if not (isinstance(value, int) and not isinstance(value, bool)) or value < 0:
        raise ValueError("index must be a nonnegative int")
    return value


def one_cell_d0() -> Fraction:
    return ZERO


def one_cell_d1(value: Fraction) -> Fraction:
    return value


def one_cell_d0_star(_circulation: Fraction) -> Fraction:
    return ZERO


def d0_triangle(potential: Cochain) -> Cochain:
    vertex_0, vertex_1, vertex_2 = potential
    return (vertex_1 - vertex_0, vertex_2 - vertex_1, vertex_2 - vertex_0)


def d1_triangle(cochain: Cochain) -> Fraction:
    edge_01, edge_12, edge_02 = cochain
    return edge_01 + edge_12 - edge_02


def d0_star(circulation: Cochain) -> Cochain:
    edge_01, edge_12, edge_02 = circulation
    return (-edge_01 - edge_02, edge_01 - edge_12, edge_12 + edge_02)


def l1(cochain: Cochain) -> Fraction:
    return abs(cochain[0]) + abs(cochain[1]) + abs(cochain[2])


def pairing(left: Cochain, right: Cochain) -> Fraction:
    return left[0] * right[0] + left[1] * right[1] + left[2] * right[2]


def closure_ratio(gamma: Fraction, phi: Fraction) -> Fraction:
    if phi == 0:
        raise ValueError("R_cl is undefined when Phi_1 is zero")
    if phi < 0 or gamma < 0:
        raise ValueError("masses are nonnegative")
    return gamma / phi


def diagnostic_class(phi: Fraction, gamma: Fraction) -> int:
    if phi < 0 or gamma < 0:
        raise ValueError("masses are nonnegative")
    if phi == 0:
        if gamma != 0:
            raise RuntimeError("Phi_1 vanished while Gamma_2 did not")
        return EXACT_CLASS
    if gamma == 0:
        return CLOSED_RESIDUAL
    return ACTIVE_CLOSURE_FAILURE


def one_cell_operator_norm() -> Fraction:
    return abs(one_cell_d1(ONE))


def triangle_operator_norm() -> Fraction:
    basis = (
        (ONE, ZERO, ZERO),
        (ZERO, ONE, ZERO),
        (ZERO, ZERO, ONE),
    )
    return max(abs(d1_triangle(vector)) for vector in basis)


def triangle_composition() -> tuple[Fraction, Fraction, Fraction]:
    basis = (
        (ONE, ZERO, ZERO),
        (ZERO, ONE, ZERO),
        (ZERO, ZERO, ONE),
    )
    extra = (Fraction(1, 2), Fraction(1, 3), Fraction(1, 5))
    _require(d1_triangle(d0_triangle(extra)) == 0, "d1 d0 failed off the vertex basis")
    values = tuple(d1_triangle(d0_triangle(vertex)) for vertex in basis)
    _require(values == (ZERO, ZERO, ZERO), "d1 d0 failed on the vertex basis")
    return values


def _certify_circulation(circulation: Cochain) -> None:
    _require(all(abs(coord) <= 1 for coord in circulation), "circulation leaves the unit weights")
    _require(d0_star(circulation) == (ZERO, ZERO, ZERO), "net inflow is not zero")
    samples = ((ONE, ZERO, ZERO), (ZERO, ONE, ZERO), (ZERO, ZERO, ONE))
    for potential in samples:
        _require(
            pairing(circulation, d0_triangle(potential)) == 0,
            "circulation meets a coboundary",
        )


def one_cell_state(n: int) -> State:
    value = Fraction(1, 2 ** _nat(n))
    phi = abs(value - one_cell_d0())
    gamma = abs(one_cell_d1(value))
    _require(abs(ONE) <= 1, "one-cell weight was left")
    _require(one_cell_d0_star(ONE) == 0, "one-cell adjoint left the zero space")
    _require(ONE * value == phi, "one-cell pairing missed the repaired mass")
    return State(phi, gamma, closure_ratio(gamma, phi), diagnostic_class(phi, gamma))


def triangle_state(n: int) -> TriangleState:
    # Run coefficient on the three triangle edges, not the one-cell mass copied into a sum.
    scale = Fraction(1, 2 ** _nat(n))
    delta = (scale, scale, ZERO)
    coboundary = d0_triangle((ZERO, scale, ZERO))
    residual = (
        delta[0] - coboundary[0],
        delta[1] - coboundary[1],
        delta[2] - coboundary[2],
    )
    _certify_circulation(UNIT_CIRCULATION)
    matched = pairing(UNIT_CIRCULATION, delta)
    _require(matched == l1(residual), "triangle certificate missed the repaired mass")
    _require(matched != scale, "filled-triangle Phi_1 collapsed to the one-cell mass")
    gamma = abs(d1_triangle(delta))
    return TriangleState(
        matched,
        gamma,
        closure_ratio(gamma, matched),
        diagnostic_class(matched, gamma),
        delta,
    )


def step_accepted(
    phi: Fraction,
    phi_next: Fraction,
    r_cl: Fraction,
    r_next: Fraction,
    bound: Fraction,
) -> bool:
    if phi <= 0 or phi_next <= 0:
        return False
    return phi_next < phi and r_cl <= bound and r_next <= bound


def one_cell_step_is_coboundary(n: int) -> bool:
    index = _nat(n)
    return Fraction(1, 2 ** (index + 1)) - Fraction(1, 2**index) == one_cell_d0()


def triangle_step_adds_coboundary(n: int) -> bool:
    current = triangle_state(n).delta
    nxt = triangle_state(n + 1).delta
    difference = (nxt[0] - current[0], nxt[1] - current[1], nxt[2] - current[2])
    return d1_triangle(difference) == 0


def coboundary_edit_drop() -> Fraction:
    original = triangle_state(0).phi
    added = d0_triangle((ZERO, ONE, ZERO))
    edited = (ONE + added[0], ONE + added[1], ZERO + added[2])
    _require(edited == (Fraction(2), ZERO, ZERO), "coboundary edit left (2, 0, 0)")
    _certify_circulation(UNIT_CIRCULATION)
    matched = pairing(UNIT_CIRCULATION, edited)
    _require(matched == l1(edited), "edited representative was not certified")
    _require(closure_ratio(abs(d1_triangle(edited)), matched) == ONE, "edited R_cl left 1")
    drop = original - matched
    _require(drop == 0, "coboundary edit changed Phi_1")
    return drop


def first_drop_below(epsilon: Fraction) -> tuple[int, Fraction]:
    if isinstance(epsilon, float):
        raise TypeError("float tolerance is not a claim")
    if not isinstance(epsilon, Fraction):
        raise TypeError("epsilon must be a positive rational")
    if epsilon <= 0:
        raise ValueError("epsilon must be positive")
    limit = epsilon.denominator.bit_length() + 2
    n = 0
    while n <= limit:
        drop = one_cell_state(n).phi - one_cell_state(n + 1).phi
        if drop < epsilon:
            return n, drop
        n += 1
    raise RuntimeError("no dyadic drop fell below the rational epsilon")


def first_phi_outside_grid(denominator: int) -> tuple[int, Fraction]:
    if not (isinstance(denominator, int) and not isinstance(denominator, bool)) or denominator <= 0:
        raise ValueError("denominator must be a positive int")
    limit = denominator.bit_length() + 1
    n = 0
    while n <= limit:
        phi = one_cell_state(n).phi
        if (denominator * phi).denominator != 1:
            return n, phi
        n += 1
    raise RuntimeError("dyadic masses stayed on the declared grid")


def _accept_prefix(
    states: dict[int, State] | dict[int, TriangleState],
    bound: Fraction,
    adds_coboundary: Callable[[int], bool],
) -> tuple[tuple[Fraction, Fraction], int]:
    for n in PREFIX:
        current = states[n]
        nxt = states[n + 1]
        _require(current.kind == ACTIVE_CLOSURE_FAILURE, "checked state left ActiveClosureFailure")
        _require(current.r_cl == bound, "R_cl left the operator-norm bound")
        accepted = step_accepted(current.phi, nxt.phi, current.r_cl, nxt.r_cl, bound)
        _require(accepted, "strict-decrease and R_cl gates rejected a dyadic step")
        _require(current.phi - nxt.phi == nxt.phi, "dyadic drop is not half the current mass")
        _require(nxt.phi > 0, "dyadic step reached zero")
        _require(not adds_coboundary(n), "dyadic step was addition of a coboundary")
    successor = states[SUCCESSOR]
    _require(successor.kind == ACTIVE_CLOSURE_FAILURE, "successor left ActiveClosureFailure")
    _require(successor.r_cl == bound, "successor R_cl left the operator-norm bound")
    drops = (states[0].phi - states[1].phi, states[1].phi - states[2].phi)
    still_accepted = step_accepted(
        states[2].phi,
        successor.phi,
        states[2].r_cl,
        successor.r_cl,
        bound,
    )
    return drops, 1 if still_accepted else 0


def _far_step(
    n: int,
    one_bound: Fraction,
    triangle_bound: Fraction,
) -> tuple[Fraction, Fraction, int, int]:
    one_now = one_cell_state(n)
    one_next = one_cell_state(n + 1)
    tri_now = triangle_state(n)
    tri_next = triangle_state(n + 1)
    one_ok = step_accepted(one_now.phi, one_next.phi, one_now.r_cl, one_next.r_cl, one_bound)
    tri_ok = step_accepted(tri_now.phi, tri_next.phi, tri_now.r_cl, tri_next.r_cl, triangle_bound)
    _require(one_ok and tri_ok, "far dyadic step was rejected")
    _require(
        one_now.phi - one_next.phi == one_next.phi,
        "far one-cell drop left the halving relation",
    )
    _require(
        tri_now.phi - tri_next.phi == tri_next.phi,
        "far triangle drop left the halving relation",
    )
    _require(one_next.phi > 0 and tri_next.phi > 0, "far step reached zero")
    _require(one_now.phi != tri_now.phi, "far masses collapsed the two windows")
    _require(not one_cell_step_is_coboundary(n), "far one-cell step was a coboundary")
    _require(not triangle_step_adds_coboundary(n), "far triangle step was a coboundary")
    _require(one_now.r_cl == one_bound and tri_now.r_cl == triangle_bound, "far R_cl left 1")
    return one_now.phi, tri_now.phi, 1 if one_ok else 0, 1 if tri_ok else 0


def witness() -> dict[str, WitnessValue]:
    one_composition = one_cell_d1(one_cell_d0())
    _require(one_composition == 0, "one-cell composition left 0")
    composition = triangle_composition()
    one_bound = one_cell_operator_norm()
    triangle_bound = triangle_operator_norm()
    _require(one_bound == ONE and triangle_bound == ONE, "operator norm left 1")

    one_states: dict[int, State] = {n: one_cell_state(n) for n in range(SUCCESSOR + 1)}
    triangle_states: dict[int, TriangleState] = {
        n: triangle_state(n) for n in range(SUCCESSOR + 1)
    }
    one_drops, one_accepted = _accept_prefix(one_states, one_bound, one_cell_step_is_coboundary)
    triangle_drops, triangle_accepted = _accept_prefix(
        triangle_states,
        triangle_bound,
        triangle_step_adds_coboundary,
    )
    distinct = 1
    reached = 0
    for n in range(SUCCESSOR + 1):
        if one_states[n].phi == triangle_states[n].phi:
            distinct = 0
        if one_states[n].phi == 0 or triangle_states[n].phi == 0:
            reached = 1
    _require(distinct == 1, "same-index masses collapsed the two windows")
    _require(reached == 0, "a checked state reached zero")
    _require(one_accepted == 1 and triangle_accepted == 1, "prefix successor was rejected")

    edit_drop = coboundary_edit_drop()
    coboundary_accepted = 1 if edit_drop > 0 else 0
    _require(coboundary_accepted == 0, "strict gate accepted a coboundary edit")

    epsilon = Fraction(1, 4)
    drop_n, drop_value = first_drop_below(epsilon)
    _require(drop_n == PREFIX[-1], "undershooting step left the prefix end")
    _require(drop_value == one_states[SUCCESSOR].phi, "undershooting drop left the successor mass")
    _require(drop_n + 1 in one_states, "undershooting index left the checked successor")

    grid_n, grid_phi = first_phi_outside_grid(4)
    _require(grid_phi == one_states[grid_n].phi, "grid escape left the one-cell run")
    _require(grid_phi == one_states[SUCCESSOR].phi, "grid escape is not the positive successor")

    one_far_phi, triangle_far_phi, one_far_accepted, triangle_far_accepted = _far_step(
        FAR_N,
        one_bound,
        triangle_bound,
    )
    return {
        "one_cell_composition": one_composition,
        "triangle_composition": composition,
        "one_cell_operator_norm": one_bound,
        "triangle_operator_norm": triangle_bound,
        "one_cell_phi": (one_states[0].phi, one_states[1].phi, one_states[2].phi),
        "one_cell_gamma": (one_states[0].gamma, one_states[1].gamma, one_states[2].gamma),
        "one_cell_r_cl": (one_states[0].r_cl, one_states[1].r_cl, one_states[2].r_cl),
        "one_cell_class": (one_states[0].kind, one_states[1].kind, one_states[2].kind),
        "one_cell_drops": one_drops,
        "one_cell_successor_phi": one_states[SUCCESSOR].phi,
        "one_cell_successor_r_cl": one_states[SUCCESSOR].r_cl,
        "one_cell_successor_class": one_states[SUCCESSOR].kind,
        "one_cell_successor_accepted": one_accepted,
        "triangle_phi": (triangle_states[0].phi, triangle_states[1].phi, triangle_states[2].phi),
        "triangle_gamma": (
            triangle_states[0].gamma,
            triangle_states[1].gamma,
            triangle_states[2].gamma,
        ),
        "triangle_r_cl": (
            triangle_states[0].r_cl,
            triangle_states[1].r_cl,
            triangle_states[2].r_cl,
        ),
        "triangle_class": (
            triangle_states[0].kind,
            triangle_states[1].kind,
            triangle_states[2].kind,
        ),
        "triangle_drops": triangle_drops,
        "triangle_successor_phi": triangle_states[SUCCESSOR].phi,
        "triangle_successor_r_cl": triangle_states[SUCCESSOR].r_cl,
        "triangle_successor_class": triangle_states[SUCCESSOR].kind,
        "triangle_successor_accepted": triangle_accepted,
        "windows_distinct": distinct,
        "coboundary_drop": edit_drop,
        "coboundary_accepted": coboundary_accepted,
        "reaches_zero": reached,
        "termination_admitted": 0,
        "undershooting_epsilon": epsilon,
        "undershooting_drop_n": drop_n,
        "undershooting_drop": drop_value,
        "grid_denominator": 4,
        "grid_escape_n": grid_n,
        "grid_escape_phi": grid_phi,
        "far_n": FAR_N,
        "one_cell_far_phi": one_far_phi,
        "one_cell_far_r_cl": ONE,
        "one_cell_far_accepted": one_far_accepted,
        "triangle_far_phi": triangle_far_phi,
        "triangle_far_r_cl": ONE,
        "triangle_far_accepted": triangle_far_accepted,
    }


def refuse_one_cell_mass_as_triangle(n: object, claimed_phi: object) -> None:
    if isinstance(n, float) or isinstance(claimed_phi, float):
        raise TypeError("float tolerance is not a claim")
    if not (isinstance(n, int) and not isinstance(n, bool)) or n < 0:
        raise ValueError("n must be a nonnegative int")
    if isinstance(claimed_phi, bool) or not isinstance(claimed_phi, (int, Fraction)):
        raise TypeError("exact int or Fraction required")
    claimed = Fraction(claimed_phi)
    if claimed == one_cell_state(n).phi:
        raise ValueError("one-cell Phi_1 is not the filled-triangle signature")
    if claimed != triangle_state(n).phi:
        raise ValueError("claimed value is not Phi_1 of the scaled filled triangle")


def refuse_limit_zero(claimed: object) -> None:
    if isinstance(claimed, float):
        raise TypeError("float tolerance is not a claim")
    if isinstance(claimed, bool) or not isinstance(claimed, (int, Fraction)):
        raise TypeError("exact int or Fraction required")
    if Fraction(claimed) == 0:
        raise ValueError("the limit value 0 is not a state of the run and not a repair")
