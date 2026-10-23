"""Exact finite examples for coda.md; no operational authority is issued.

The linear evaluator is the three-coordinate packet in section 4, not a
general linear-programming solver. All arithmetic inputs are exact.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import product
from typing import Callable, Hashable, Iterable, Mapping, TypeVar

X = TypeVar("X", bound=Hashable)
P = TypeVar("P", bound=Hashable)
Y = TypeVar("Y")


def rational(value: int | Fraction) -> Fraction:
    if isinstance(value, bool) or not isinstance(value, (int, Fraction)):
        raise TypeError("Use an int or Fraction, never approximate arithmetic")
    return Fraction(value)


@dataclass(frozen=True)
class Collision:
    left: Hashable
    right: Hashable
    observation: Hashable
    left_value: object
    right_value: object


def factor_or_collision(
    states: Iterable[X], observe: Callable[[X], P], query: Callable[[X], Y]
) -> dict[P, Y] | Collision:
    """Return a factor on the enumerated image or an actual separating pair.

    Caller supplies the whole declared finite domain and pure, total maps.
    An empty domain has the empty image factor. No values off the image are
    invented, and this routine makes no claim about unenumerated states.
    """
    representatives: dict[P, X] = {}
    factor: dict[P, Y] = {}
    for state in states:
        observed, value = observe(state), query(state)
        if observed in factor and factor[observed] != value:
            return Collision(
                representatives[observed], state, observed, factor[observed], value
            )
        representatives[observed] = state
        factor[observed] = value
    return factor


@dataclass(frozen=True)
class MenuResult:
    status: str
    repairs: tuple[str, ...]
    minima: tuple[str, ...]
    checked: int
    declared: int


def evaluate_menu(
    menu: Mapping[str, int | Fraction],
    works: Callable[[str], bool],
    budget: int | None = None,
) -> MenuResult:
    """Evaluate a declared menu, retaining every tied least-cost repair.

    Enumeration order is insertion order. With an incomplete search, found
    repairs are witnesses, but minima are withheld: an unchecked repair may
    be cheaper. Exhaustion is relative to this exact menu, even if empty.
    """
    if budget is not None and (type(budget) is not int or budget < 0):
        raise ValueError("budget must be a nonnegative integer or None")
    costs = {name: rational(cost) for name, cost in menu.items()}
    if any(cost < 0 for cost in costs.values()):
        raise ValueError("costs must be nonnegative")
    names = tuple(costs)
    selected = names if budget is None else names[:budget]
    successes = []
    for name in selected:
        verdict = works(name)
        if type(verdict) is not bool:
            raise TypeError("repair predicates must return bool")
        if verdict:
            successes.append(name)
    if len(selected) < len(names):
        return MenuResult(
            "BudgetUnknown", tuple(successes), (), len(selected), len(names)
        )
    if not successes:
        return MenuResult("ExhaustedDeclaredMenu", (), (), len(selected), len(names))
    least = min(costs[name] for name in successes)
    minima = tuple(name for name in successes if costs[name] == least)
    return MenuResult(
        "RepairsFound", tuple(successes), minima, len(selected), len(names)
    )


@dataclass(frozen=True)
class LinearCertificate:
    state: tuple[Fraction, Fraction, Fraction]
    repair: Fraction
    residual: tuple[Fraction, Fraction, Fraction]
    dual: tuple[Fraction, Fraction, Fraction]
    phi: Fraction
    gamma: Fraction
    grade: str


def coordinate_packet(values: Iterable[int | Fraction]) -> LinearCertificate:
    """Solve d0(t)=(t,0,0), d1(a,b,c)=c, a2=0, all weights one."""
    state = tuple(rational(value) for value in values)
    if len(state) != 3:
        raise ValueError("the coordinate packet requires exactly three coordinates")
    a, b, c = state
    phi, gamma = abs(b) + abs(c), abs(c)
    def sign(x: Fraction) -> Fraction:
        return Fraction((x > 0) - (x < 0))
    grade = (
        "ExactRepair"
        if phi == 0
        else ("CoherentResidual" if gamma == 0 else "NonclosedDefect")
    )
    return LinearCertificate(
        state,
        -a,
        (Fraction(0), b, c),
        (Fraction(0), sign(b), sign(c)),
        phi,
        gamma,
        grade,
    )


def verify_coordinate_certificate(cert: LinearCertificate) -> bool:
    """Check feasibility and a matching dual bound, independently of the solver."""
    if not all(len(v) == 3 for v in (cert.state, cert.residual, cert.dual)):
        return False
    try:
        for value in (
            *cert.state,
            cert.repair,
            *cert.residual,
            *cert.dual,
            cert.phi,
            cert.gamma,
        ):
            rational(value)
    except TypeError:
        return False
    a, b, c = cert.state
    y0, y1, y2 = cert.dual
    norm = sum(abs(r) for r in cert.residual)
    bound = sum(x * y for x, y in zip(cert.state, cert.dual))
    grade = (
        "ExactRepair"
        if cert.phi == 0
        else ("CoherentResidual" if cert.gamma == 0 else "NonclosedDefect")
    )
    return (
        cert.residual == (a + cert.repair, b, c)
        and y0 == 0
        and all(abs(y) <= 1 for y in (y0, y1, y2))
        and norm == bound == cert.phi
        and cert.gamma == abs(c)
        and cert.grade == grade
    )


def parity_sections(
    vertices: int,
    constraints: Iterable[tuple[int, int, int]],
) -> tuple[tuple[int, ...], ...]:
    """All sections of a declared finite binary edge-constraint system."""
    if type(vertices) is not int or not 0 <= vertices <= 16:
        raise ValueError("explicit enumerator supports 0 through 16 vertices")
    edges = tuple(constraints)
    if any(
        type(i) is not int
        or type(j) is not int
        or type(bit) is not int
        or not 0 <= i < vertices
        or not 0 <= j < vertices
        or bit not in (0, 1)
        for i, j, bit in edges
    ):
        raise ValueError("each constraint needs valid endpoints and a bit")
    return tuple(
        state
        for state in product((0, 1), repeat=vertices)
        if all(state[i] ^ state[j] == bit for i, j, bit in edges)
    )


def affine_quadrature(n: int) -> dict[str, Fraction]:
    """Exact sums for f(x)=x on [0,10], with n equal panels."""
    if type(n) is not int or n <= 0:
        raise ValueError("panel count must be a positive integer")
    width = Fraction(10, n)
    left = sum(((i * width) * width for i in range(n)), start=Fraction(0))
    right = sum(((i * width) * width for i in range(1, n + 1)), start=Fraction(0))
    trapezoid = (left + right) / Fraction(2)
    return {
        "left": left,
        "right": right,
        "trapezoid": trapezoid,
        "integral": Fraction(50),
        "error": Fraction(50, n),
    }


def polynomial_product(
    a: Iterable[Fraction], b: Iterable[Fraction]
) -> tuple[Fraction, ...]:
    aa, bb = tuple(a), tuple(b)
    out = [Fraction(0)] * (len(aa) + len(bb) - 1)
    for i, x in enumerate(aa):
        for j, y in enumerate(bb):
            out[i + j] += rational(x) * rational(y)
    return tuple(out)


def sample_collision() -> dict[str, object]:
    """f(x)=x and f(x)+[u(u-1/2)(u-1)]^2, u=x/10, agree at 0,5,10."""
    roots = (Fraction(0), Fraction(1, 2), Fraction(1))
    polynomial: tuple[Fraction, ...] = (Fraction(1),)
    for root in roots:
        polynomial = polynomial_product(polynomial, (-root, Fraction(1)))
    squared = polynomial_product(polynomial, polynomial)
    values = tuple(
        sum(coef * t**power for power, coef in enumerate(squared)) for t in roots
    )
    area = 10 * sum(coef / (power + 1) for power, coef in enumerate(squared))
    return {
        "nodes": (0, 5, 10),
        "perturbation_at_nodes": values,
        "perturbation_coefficients_in_u": squared,
        "area_difference": area,
        "base_integral": Fraction(50),
        "perturbed_integral": Fraction(50) + area,
    }


def standing(evidence: bool, grant: bool) -> bool:
    """A declared logical policy model; no identity, signing, or grant service."""
    if type(evidence) is not bool or type(grant) is not bool:
        raise TypeError("the policy model takes Boolean assumptions")
    return evidence and grant


def example_results() -> dict[str, object]:
    states = tuple(product((0, 1), repeat=2))
    collision = factor_or_collision(states, lambda x: x[0], lambda x: x[1])
    packets = [coordinate_packet(x) for x in ((2, 0, 0), (2, 3, 0), (2, 3, 5))]
    edges = ((0, 1, 0), (1, 2, 0), (2, 0, 1))
    return {
        "authority_effect": "None",
        "scope": "Declared finite examples only",
        "image_factor": factor_or_collision(states, lambda x: x[0], lambda x: 2 * x[0]),
        "collision": collision.__dict__ if isinstance(collision, Collision) else None,
        "incomplete_menu": evaluate_menu(
            {"r0": 0, "r1": 1}, lambda x: x == "r1", 1
        ).__dict__,
        "tied_repairs": evaluate_menu({"a": 1, "b": 1}, lambda _: True).__dict__,
        "linear_packets": [p.__dict__ for p in packets],
        "dual_certificates_valid": all(
            verify_coordinate_certificate(p) for p in packets
        ),
        "single_edge_section_counts": [
            len(parity_sections(3, [edge])) for edge in edges
        ],
        "global_sections": parity_sections(3, edges),
        "quadrature_n10": affine_quadrature(10),
        "sample_collision": sample_collision(),
        "evidence_without_grant": standing(True, False),
    }
