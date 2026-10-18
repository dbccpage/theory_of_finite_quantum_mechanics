"""Rational path coboundary. Consecutive differences on a closed loop sum to zero.

Origin: papers/derivations/ms_majorana/lean4/MajoranaCore.lean theorem coboundary_is_cocycle
Claim: urn:omega:fqm:ms-majorana:coboundary:telescoping-loop:v1
AuthorityEffect: None
Mutation-Kills: 5 non-equivalent source mutants, executed by papers/derivations/ms_majorana/code/tests/unit/test_l5a_exact_slice.py.
Scope Fence: This file does not certify de Rham cohomology of a smooth manifold.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Mapping, Sequence


class CoboundaryError(ValueError):
    """One violated coboundary invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> CoboundaryError:
    return CoboundaryError(invariant, parameters)


def _rational(value: object, role: str) -> Fraction:
    if isinstance(value, float):
        raise _fail("float refused at the public boundary", role=role, received="float")
    if isinstance(value, bool):
        raise _fail("boolean refused where a rational was required", role=role)
    if isinstance(value, Fraction):
        return value
    if type(value) is int:
        return Fraction(value)
    raise _fail("value is not an exact rational", role=role, received=type(value).__name__)


def _index(value: object, role: str, count: int) -> int:
    if isinstance(value, bool) or type(value) is not int:
        raise _fail("vertex is not an exact index", role=role, received=type(value).__name__)
    if value < 0 or value >= count:
        raise _fail("vertex index is outside the declared set", role=role, index=value, count=count)
    return value


def _values(values: object, count: int) -> tuple[Fraction, ...]:
    if isinstance(values, (str, bytes)) or not isinstance(values, Sequence):
        raise _fail("vertex values must be a sequence", received=type(values).__name__)
    parsed = tuple(_rational(item, f"values[{index}]") for index, item in enumerate(values))
    if len(parsed) != count:
        raise _fail("vertex value length does not match the map", length=len(parsed), expected=count)
    return parsed


@dataclass(frozen=True)
class CoboundaryMap:
    """Exact coboundary (df)(u -> v) = f(v) - f(u) on declared edges."""

    from_degree: int
    to_degree: int
    vertex_count: int
    edges: tuple[tuple[int, int], ...]

    def source_dim(self) -> int:
        return self.vertex_count

    def target_dim(self) -> int:
        return len(self.edges)

    def apply(self, values: object) -> tuple[Fraction, ...]:
        parsed = _values(values, self.vertex_count)
        image: list[Fraction] = []
        for src, dst in self.edges:
            image.append(parsed[dst] - parsed[src])
        return tuple(image)


def _edge(value: object, role: str, count: int) -> tuple[int, int]:
    if isinstance(value, (str, bytes)) or not isinstance(value, Sequence) or len(value) != 2:
        raise _fail("edge must be a pair", role=role, received=type(value).__name__)
    return (_index(value[0], role + "[0]", count), _index(value[1], role + "[1]", count))


def new(vertex_count: object, edges: object) -> CoboundaryMap:
    """Build the degree-0 to degree-1 coboundary of a directed edge list."""
    if isinstance(vertex_count, bool) or type(vertex_count) is not int or vertex_count < 1:
        raise _fail("vertex count is not a positive integer", received=type(vertex_count).__name__)
    if isinstance(edges, (str, bytes)) or not isinstance(edges, Sequence):
        raise _fail("edges must be a sequence", received=type(edges).__name__)
    parsed = tuple(_edge(item, f"edges[{index}]", vertex_count) for index, item in enumerate(edges))
    return CoboundaryMap(0, 1, vertex_count, parsed)


def _loop_sum(values: Sequence[Fraction], loop: Sequence[int]) -> Fraction:
    total = Fraction(0)
    previous = loop[0]
    for vertex in loop[1:]:
        total += values[vertex] - values[previous]
        previous = vertex
    total += values[loop[0]] - values[previous]
    return total


@dataclass(frozen=True)
class TelescopeCertificate:
    """Witness that the coboundary of a vertex function sums to zero around a loop."""

    loop: tuple[int, ...]
    image_sum: Fraction


def certify_closed_loop(coboundary: CoboundaryMap, values: object, loop: object) -> TelescopeCertificate:
    """Recheck that a closed vertex loop has coboundary sum zero."""
    if not isinstance(coboundary, CoboundaryMap):
        raise _fail("coboundary map required", received=type(coboundary).__name__)
    parsed_values = _values(values, coboundary.vertex_count)
    if isinstance(loop, (str, bytes)) or not isinstance(loop, Sequence) or len(loop) < 1:
        raise _fail("loop must be a nonempty vertex sequence", received=type(loop).__name__)
    parsed_loop = tuple(_index(item, f"loop[{index}]", coboundary.vertex_count) for index, item in enumerate(loop))
    image_sum = _loop_sum(parsed_values, parsed_loop)
    if image_sum != 0:
        raise _fail("closed loop coboundary sum is not zero", image_sum=str(image_sum))
    return TelescopeCertificate(parsed_loop, image_sum)


__all__ = [
    "CoboundaryError",
    "CoboundaryMap",
    "TelescopeCertificate",
    "certify_closed_loop",
    "new",
]
