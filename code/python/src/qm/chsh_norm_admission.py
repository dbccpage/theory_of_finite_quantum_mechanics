"""Exact CHSH admission controls on two-dimensional norm/dual pairs.

These are finite correlator witnesses, not a reconstruction of a physical
state/effect/composition theory. In particular, l1 geometry does not impose a
nonnegative global joint table. The l2 witness attains 2*sqrt(2); this replay
does not prove a universal norm bound or select Hilbert geometry from primitives.
Only integers, Fraction values, and exact Q(sqrt(2)) values are accepted.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from functools import total_ordering
from itertools import product
from typing import Iterable, Sequence


def rational(value: int | Fraction) -> Fraction:
    if type(value) not in (int, Fraction):
        raise TypeError("an exact integer or Fraction is required")
    return Fraction(value)


@total_ordering
@dataclass(frozen=True, eq=False)
class Qsqrt2:
    """a + b*sqrt(2), ordered at the positive real embedding, without floats."""

    a: Fraction = Fraction(0)
    b: Fraction = Fraction(0)

    def __post_init__(self) -> None:
        object.__setattr__(self, "a", rational(self.a))
        object.__setattr__(self, "b", rational(self.b))

    def __add__(self, other: object) -> Qsqrt2:
        other = exact(other)
        return Qsqrt2(self.a + other.a, self.b + other.b)

    __radd__ = __add__

    def __neg__(self) -> Qsqrt2:
        return Qsqrt2(-self.a, -self.b)

    def __sub__(self, other: object) -> Qsqrt2:
        return self + (-exact(other))

    def __rsub__(self, other: object) -> Qsqrt2:
        return exact(other) - self

    def __mul__(self, other: object) -> Qsqrt2:
        other = exact(other)
        return Qsqrt2(self.a * other.a + 2 * self.b * other.b,
                      self.a * other.b + self.b * other.a)

    __rmul__ = __mul__

    def __truediv__(self, other: object) -> Qsqrt2:
        other = exact(other)
        denominator = other.a * other.a - 2 * other.b * other.b
        if denominator == 0:
            raise ZeroDivisionError("division by zero in Q(sqrt(2))")
        return self * Qsqrt2(other.a / denominator, -other.b / denominator)

    def __rtruediv__(self, other: object) -> Qsqrt2:
        return exact(other) / self

    def sign(self) -> int:
        if self.a == 0:
            return (self.b > 0) - (self.b < 0)
        if self.b == 0:
            return (self.a > 0) - (self.a < 0)
        if self.a > 0 and self.b > 0:
            return 1
        if self.a < 0 and self.b < 0:
            return -1
        difference = self.a * self.a - 2 * self.b * self.b
        # Equality cannot occur for nonzero rational a and b.
        return ((difference > 0) - (difference < 0)) * (1 if self.a > 0 else -1)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Qsqrt2) and type(other) not in (int, Fraction):
            return False
        other = exact(other)
        return self.a == other.a and self.b == other.b

    def __hash__(self) -> int:
        return hash(self.a) if self.b == 0 else hash((self.a, self.b))

    def __lt__(self, other: object) -> bool:
        return (self - other).sign() < 0

    def __abs__(self) -> Qsqrt2:
        return -self if self.sign() < 0 else self

    def serialized(self) -> dict[str, str]:
        return {"rational": str(self.a), "sqrt2_coefficient": str(self.b)}


def exact(value: object) -> Qsqrt2:
    return value if isinstance(value, Qsqrt2) else Qsqrt2(rational(value))


ROOT_TWO = Qsqrt2(0, 1)
OUTCOMES = (-1, 1)
LOCAL_ASSIGNMENTS = tuple(product(OUTCOMES, repeat=4))
DUAL_NORM = {"l1": "linfty", "l2": "l2", "linfty": "l1"}


def vector(values: Iterable[object]) -> tuple[Qsqrt2, Qsqrt2]:
    result = tuple(exact(value) for value in values)
    if len(result) != 2:
        raise ValueError("two coordinates are required")
    return result


def norm_squared(values: Iterable[object], norm: str) -> Qsqrt2:
    u, v = vector(values)
    if norm == "l2":
        return u * u + v * v
    if norm == "l1":
        length = abs(u) + abs(v)
    elif norm == "linfty":
        length = max(abs(u), abs(v))
    else:
        raise ValueError("norm must be l1, l2, or linfty")
    return length * length


def require_unit_ball(values: Iterable[object], norm: str) -> tuple[Qsqrt2, Qsqrt2]:
    result = vector(values)
    if norm_squared(result, norm) > 1:
        raise ValueError(f"vector is outside the {norm} unit ball")
    return result


def parallelogram_defect(u: Iterable[object], v: Iterable[object], norm: str) -> Qsqrt2:
    """Squared-norm parallelogram left side minus right side."""
    u, v = vector(u), vector(v)
    plus = tuple(a + b for a, b in zip(u, v))
    minus = tuple(a - b for a, b in zip(u, v))
    return norm_squared(plus, norm) + norm_squared(minus, norm) - 2 * (
        norm_squared(u, norm) + norm_squared(v, norm))


def require_parallelogram(u: Iterable[object], v: Iterable[object], norm: str) -> None:
    if parallelogram_defect(u, v, norm) != 0:
        raise ValueError("the supplied pair fails the squared-norm parallelogram identity")


def norm_dual_correlations(
    norm: str, states: Sequence[Iterable[object]], effects: Sequence[Iterable[object]],
) -> tuple[Qsqrt2, ...]:
    """E_xy=f_x(b_y); states belong to E, effects to its actual dual ball."""
    if norm not in DUAL_NORM:
        raise ValueError("norm must be l1, l2, or linfty")
    if len(states) != 2 or len(effects) != 2:
        raise ValueError("two settings per party are required")
    states = tuple(require_unit_ball(v, norm) for v in states)
    effects = tuple(require_unit_ball(f, DUAL_NORM[norm]) for f in effects)
    result = tuple(sum((a * b for a, b in zip(f, v)), Qsqrt2())
                   for f in effects for v in states)
    if any(abs(value) > 1 for value in result):
        raise ValueError("correlator outside [-1,1]")
    return result


def chsh(correlations: Iterable[object]) -> Qsqrt2:
    values = tuple(exact(value) for value in correlations)
    if len(values) != 4:
        raise ValueError("four correlators in 00,01,10,11 order are required")
    return values[0] + values[1] + values[2] - values[3]


def validate_behavior(rows: Iterable[Iterable[object]]) -> tuple[tuple[Qsqrt2, ...], ...]:
    """Four contexts; each row ordered (--,-+,+-,++). Check all NS marginals."""
    rows = tuple(tuple(exact(value) for value in row) for row in rows)
    if len(rows) != 4 or any(len(row) != 4 for row in rows):
        raise ValueError("four contexts with four probabilities each are required")
    if any(value < 0 or value > 1 for row in rows for value in row):
        raise ValueError("probabilities must lie in [0,1]")
    if any(sum(row, Qsqrt2()) != 1 for row in rows):
        raise ValueError("each context must be normalized")
    for x in range(2):
        for a in range(2):
            if sum(rows[2*x][2*a:2*a+2], Qsqrt2()) != sum(rows[2*x+1][2*a:2*a+2], Qsqrt2()):
                raise ValueError("Alice marginal signals")
    for y in range(2):
        for b in range(2):
            if rows[y][b] + rows[y][2+b] != rows[2+y][b] + rows[2+y][2+b]:
                raise ValueError("Bob marginal signals")
    return rows


def behavior_from_correlations(correlations: Iterable[object]) -> tuple[tuple[Qsqrt2, ...], ...]:
    """Unbiased binary behavior p(a,b|x,y)=(1+a*b*E_xy)/4."""
    values = tuple(exact(value) for value in correlations)
    if len(values) != 4 or any(abs(value) > 1 for value in values):
        raise ValueError("four correlations in [-1,1] are required")
    return validate_behavior(tuple(tuple((1 + a*b*value) / 4
                                        for a in OUTCOMES for b in OUTCOMES)
                                   for value in values))


def behavior_correlations(rows: Iterable[Iterable[object]]) -> tuple[Qsqrt2, ...]:
    return tuple(row[0] - row[1] - row[2] + row[3] for row in validate_behavior(rows))


def deterministic_correlations(assignment: Sequence[int]) -> tuple[Qsqrt2, ...]:
    if len(assignment) != 4 or any(type(v) is not int or v not in OUTCOMES for v in assignment):
        raise ValueError("four integer signs are required")
    a0, a1, b0, b1 = assignment
    return tuple(exact(v) for v in (a0*b0, a0*b1, a1*b0, a1*b1))


def local_mixture(weights: Iterable[int | Fraction]) -> tuple[tuple[Qsqrt2, ...], ...]:
    """A nonnegative rational global table on the 16 joint assignments."""
    weights = tuple(rational(weight) for weight in weights)
    if len(weights) != 16 or any(weight < 0 for weight in weights) or sum(weights) != 1:
        raise ValueError("16 nonnegative normalized joint weights are required")
    rows = tuple(tuple(sum(weight for assignment, weight in zip(LOCAL_ASSIGNMENTS, weights)
                           if assignment[x] == a and assignment[2+y] == b)
                       for a in OUTCOMES for b in OUTCOMES)
                 for x in range(2) for y in range(2))
    behavior = validate_behavior(rows)
    if abs(chsh(behavior_correlations(behavior))) > 2:
        raise AssertionError("positive joint-table CHSH bound failed")
    return behavior


def replay() -> dict[str, object]:
    """JSON-ready finite evidence, with fields recomputed from the actual witnesses."""
    diagonal = ROOT_TWO / 2
    fixtures = {
        "l1": (((1, 0), (0, 1)), ((1, 1), (1, -1))),
        "l2": (((1, 0), (0, 1)), ((diagonal, diagonal), (diagonal, -diagonal))),
        "linfty": (((1, 1), (1, -1)), ((1, 0), (0, 1))),
    }
    witnesses = {}
    for norm, (states, effects) in fixtures.items():
        correlations = norm_dual_correlations(norm, states, effects)
        behavior = behavior_from_correlations(correlations)
        witnesses[norm] = {
            "dual_norm": DUAL_NORM[norm],
            "states": [[exact(v).serialized() for v in row] for row in states],
            "effects": [[exact(v).serialized() for v in row] for row in effects],
            "state_norm_squared": [norm_squared(v, norm).serialized() for v in states],
            "effect_dual_norm_squared": [norm_squared(f, DUAL_NORM[norm]).serialized() for f in effects],
            "correlations": [v.serialized() for v in correlations],
            "behavior": [[v.serialized() for v in row] for row in behavior],
            "chsh": chsh(correlations).serialized(),
            "basis_parallelogram_defect": parallelogram_defect((1, 0), (0, 1), norm).serialized(),
        }
    local_values = [chsh(deterministic_correlations(a)) for a in LOCAL_ASSIGNMENTS]
    # All vertices and a strictly positive, nonuniform mixture are replayed.
    for i in range(16):
        local_mixture([int(i == j) for j in range(16)])
    weights = [Fraction(i, 136) for i in range(1, 17)]
    mixture = local_mixture(weights)
    return {
        "schema": "chsh-norm-admission/1",
        "scope": "Exact finite norm/dual correlator witnesses; no physical reconstruction or universal norm theorem.",
        "witnesses": witnesses,
        "local_assignments": [list(a) for a in LOCAL_ASSIGNMENTS],
        "local_chsh_values": [v.serialized() for v in local_values],
        "positive_mixture_weights": [str(w) for w in weights],
        "positive_mixture_behavior": [[v.serialized() for v in row] for row in mixture],
        "positive_mixture_chsh": chsh(behavior_correlations(mixture)).serialized(),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(replay(), indent=2, sort_keys=True))
