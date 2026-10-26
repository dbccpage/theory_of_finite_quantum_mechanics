# -*- coding: utf-8 -*-
"""Exact rational companion for metric completion and midpoint enclosure.

Finite nested intervals, Cauchy-modulus checks, and a two-signal sample
collision. Arithmetic is exact rational. Floats and booleans in scalar
position raise TypeError.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from types import MappingProxyType
from typing import Any, Dict, Mapping, Sequence, Tuple

from continuum import Enclosure, sqrt2_enclosure


def _validate_exact_rational(val: Any, name: str) -> Fraction:
    """Accept int/Fraction/digit-string; refuse floats and booleans."""
    if isinstance(val, bool):
        raise TypeError(f"{name} must be an exact rational or integer, got bool")
    if isinstance(val, float) or (
        getattr(val, "dtype", None) is not None and "float" in str(val.dtype).lower()
    ):
        raise TypeError(
            f"{name} must be an exact rational or integer, got float (floats strictly forbidden)"
        )
    if isinstance(val, Fraction):
        return val
    if isinstance(val, int):
        return Fraction(val)
    if isinstance(val, str):
        try:
            return Fraction(val)
        except (ValueError, ZeroDivisionError) as exc:
            raise TypeError(
                f"{name} string could not be converted to exact rational: {exc}"
            ) from exc
    raise TypeError(f"{name} must be an exact rational or integer, got {type(val).__name__}")


def _validate_exact_int(val: Any, name: str) -> int:
    """Accept a nonnegative int; refuse floats, booleans, and negatives."""
    if isinstance(val, bool):
        raise TypeError(f"{name} must be an integer, got bool")
    val_dtype = getattr(val, "dtype", None)
    if not isinstance(val, int) or (val_dtype is not None and "float" in str(val_dtype)):
        raise TypeError(f"{name} must be an integer, got {type(val).__name__}")
    if val < 0:
        raise ValueError(f"{name} must be non-negative, got {val}")
    return val


def midpoint(lo: Any, hi: Any) -> Fraction:
    """Midpoint (lo + hi) / 2 of an ordered pair."""
    left = _validate_exact_rational(lo, "lo")
    right = _validate_exact_rational(hi, "hi")
    if left > right:
        raise ValueError("lo must be ≤ hi")
    return (left + right) / 2


def enclosure_error_bound(lo: Any, hi: Any) -> Fraction:
    """Half-width (hi - lo) / 2."""
    left = _validate_exact_rational(lo, "lo")
    right = _validate_exact_rational(hi, "hi")
    if left > right:
        raise ValueError("lo must be ≤ hi")
    return (right - left) / 2


def enclosure_error(lo: Any, hi: Any, x: Any) -> Fraction:
    """|x - (lo + hi) / 2| for x in [lo, hi].

    Matches Coda.Q.enclosure_error on rationals. The bound
    enclosure_error(...) ≤ enclosure_error_bound(...) always holds
    for a well-formed interval.
    """
    left = _validate_exact_rational(lo, "lo")
    right = _validate_exact_rational(hi, "hi")
    point = _validate_exact_rational(x, "x")
    if left > right:
        raise ValueError("lo must be ≤ hi")
    if not (left <= point <= right):
        raise ValueError("x must lie in [lo, hi]")
    return abs(point - (left + right) / 2)


def sqrt_step(lo: Any, hi: Any) -> Tuple[Fraction, Fraction]:
    """One rational bisection step for √2, matching Coda.Q.sqrtStep.

    Requires 0 ≤ lo ≤ hi. Keeps [m, hi] when m² ≤ 2, else [lo, m].
    """
    left = _validate_exact_rational(lo, "lo")
    right = _validate_exact_rational(hi, "hi")
    if left < 0:
        raise ValueError("lo must be nonnegative")
    if left > right:
        raise ValueError("lo must be ≤ hi")
    mid = (left + right) / 2
    if mid * mid <= 2:
        return mid, right
    return left, mid


@dataclass(frozen=True)
class RationalSequence:
    """A finite list of rationals, used for Cauchy-modulus checks."""

    terms: Tuple[Fraction, ...]

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "terms",
            tuple(_validate_exact_rational(t, f"terms[{i}]") for i, t in enumerate(self.terms)),
        )

    def distance_at(self, other: "RationalSequence", index: int) -> Fraction:
        n = _validate_exact_int(index, "index")
        if n >= len(self.terms) or n >= len(other.terms):
            raise ValueError("index out of range")
        return abs(self.terms[n] - other.terms[n])


def is_cauchy_from(seq: RationalSequence, start: Any, epsilon: Any) -> bool:
    """True when |x_m - x_n| < epsilon for all m, n ≥ start in the finite list."""
    n0 = _validate_exact_int(start, "start")
    eps = _validate_exact_rational(epsilon, "epsilon")
    if eps <= 0:
        raise ValueError("epsilon must be positive")
    if n0 >= len(seq.terms):
        raise ValueError("start out of range")
    terms = seq.terms
    for i in range(n0, len(terms)):
        for j in range(i, len(terms)):
            if abs(terms[i] - terms[j]) >= eps:
                return False
    return True


def sequences_close_from(
    xs: RationalSequence, ys: RationalSequence, start: Any, epsilon: Any
) -> bool:
    """True when |x_n - y_n| < epsilon for all n ≥ start in both finite lists."""
    n0 = _validate_exact_int(start, "start")
    eps = _validate_exact_rational(epsilon, "epsilon")
    if eps <= 0:
        raise ValueError("epsilon must be positive")
    limit = min(len(xs.terms), len(ys.terms))
    if n0 >= limit:
        raise ValueError("start out of range")
    for n in range(n0, limit):
        if abs(xs.terms[n] - ys.terms[n]) >= eps:
            return False
    return True


def nested_sqrt2_enclosures(steps: Any) -> Tuple[Enclosure, ...]:
    """Enclosures of √2 after 0, 1, ..., steps bisections."""
    n = _validate_exact_int(steps, "steps")
    return tuple(sqrt2_enclosure(k) for k in range(n + 1))


def enclosure_endpoint_sequence(steps: Any, which: str = "lower") -> RationalSequence:
    """Lower, upper, or midpoint sequence of nested √2 enclosures."""
    if which not in ("lower", "upper", "midpoint"):
        raise ValueError("which must be 'lower', 'upper', or 'midpoint'")
    encs = nested_sqrt2_enclosures(steps)
    if which == "lower":
        terms = tuple(e.lower for e in encs)
    elif which == "upper":
        terms = tuple(e.upper for e in encs)
    else:
        terms = tuple(e.midpoint for e in encs)
    return RationalSequence(terms=terms)


def reproduce_sqrt2_picture(steps: Any = 5) -> Dict[str, Any]:
    """Running enclosure after ``steps`` bisections from [1, 2]."""
    n = _validate_exact_int(steps, "steps")
    enc = sqrt2_enclosure(n)
    err = enclosure_error(enc.lower, enc.upper, enc.midpoint)
    return {
        "lower": enc.lower,
        "upper": enc.upper,
        "midpoint": enc.midpoint,
        "error_bound": enc.error_bound,
        "midpoint_self_distance": err,
        "verifies": enc.verifies_sqrt2(),
        "width": enc.upper - enc.lower,
        "steps": n,
    }


@dataclass(frozen=True)
class SampledSignal:
    """A signal known only through finitely many exact sample values."""

    signal_id: str
    samples: Mapping[Fraction, Fraction]

    def __post_init__(self) -> None:
        frozen: Dict[Fraction, Fraction] = {}
        for key, val in self.samples.items():
            k = _validate_exact_rational(key, "sample node")
            v = _validate_exact_rational(val, "sample value")
            frozen[k] = v
        object.__setattr__(self, "samples", MappingProxyType(frozen))

    def evaluate_at(self, t: Any) -> Fraction:
        node = _validate_exact_rational(t, "sample_coordinate")
        if node not in self.samples:
            raise KeyError(f"Signal {self.signal_id} has no sample at {node}")
        return self.samples[node]


def profile_values(signal: SampledSignal, nodes: Sequence[Any]) -> Tuple[Fraction, ...]:
    """Sample list of a signal on a declared node list."""
    return tuple(signal.evaluate_at(n) for n in nodes)


def same_profile(left: SampledSignal, right: SampledSignal, nodes: Sequence[Any]) -> bool:
    """True when the two signals agree on every declared node."""
    return profile_values(left, nodes) == profile_values(right, nodes)


def query_collides_on_profile(
    left: SampledSignal,
    right: SampledSignal,
    profile_nodes: Sequence[Any],
    query_node: Any,
) -> bool:
    """Same profile, different query value.

    A finite replay of the CS / CS-Q fibre collision, not a Q theorem.
    """
    if not same_profile(left, right, profile_nodes):
        return False
    return left.evaluate_at(query_node) != right.evaluate_at(query_node)


def two_signal_sample_collision() -> Dict[str, Any]:
    """f(t)=0 and g(t)=t(t-1) agree on {0,1} and disagree at 1/2."""
    zero = Fraction(0)
    one = Fraction(1)
    half = Fraction(1, 2)
    f = SampledSignal(
        signal_id="zero",
        samples={zero: zero, one: zero, half: zero},
    )
    g = SampledSignal(
        signal_id="t(t-1)",
        samples={zero: zero, one: zero, half: half * (half - one)},
    )
    nodes = (zero, one)
    collides = query_collides_on_profile(f, g, nodes, half)
    return {
        "profile": profile_values(f, nodes),
        "query_f": f.evaluate_at(half),
        "query_g": g.evaluate_at(half),
        "collides": collides,
    }
