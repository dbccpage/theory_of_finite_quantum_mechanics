"""F2 cycle certificate: an edge chain is a cycle when every vertex boundary bit is zero.

Origin: papers/derivations/ms_majorana/lean4/MajoranaCore.lean theorem coboundary_is_cocycle
Claim: urn:omega:fqm:ms-majorana:cycle:f2-boundary-zero:v1
AuthorityEffect: None
Mutation-Kills: 5 non-equivalent source mutants, executed by papers/derivations/ms_majorana/code/tests/unit/test_l5a_exact_slice.py.
Scope Fence: This file does not compute homology rank and does not accept rational weights.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence


class CycleError(ValueError):
    """One violated cycle invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> CycleError:
    return CycleError(invariant, parameters)


def _bit(value: object, role: str) -> int:
    if isinstance(value, float):
        raise _fail("float refused at the public boundary", role=role, received="float")
    if isinstance(value, bool) or type(value) is not int:
        raise _fail("boolean or non-bit refused", role=role, received=type(value).__name__)
    if value not in (0, 1):
        raise _fail("F2 coordinate is not 0 or 1", role=role, received=value)
    return value


def _vertex(value: object, role: str, count: int) -> int:
    if isinstance(value, bool) or type(value) is not int:
        raise _fail("vertex is not an exact index", role=role, received=type(value).__name__)
    if value < 0 or value >= count:
        raise _fail("vertex index is outside the declared set", role=role, index=value, count=count)
    return value


def _edge(value: object, role: str, count: int) -> tuple[int, int]:
    if isinstance(value, (str, bytes)) or not isinstance(value, Sequence) or len(value) != 2:
        raise _fail("edge must be a pair", role=role, received=type(value).__name__)
    return (_vertex(value[0], role + "[0]", count), _vertex(value[1], role + "[1]", count))


def _boundary(edges: Sequence[tuple[int, int]], chain: Sequence[int], count: int) -> tuple[int, ...]:
    boundary = [0 for _ in range(count)]
    for (src, dst), bit in zip(edges, chain):
        boundary[src] = (boundary[src] + bit) % 2
        boundary[dst] = (boundary[dst] + bit) % 2
    return tuple(boundary)


@dataclass(frozen=True)
class Cycle:
    """Witness that the F2 boundary of the edge chain is the zero vertex vector."""

    chain: tuple[int, ...]
    boundary: tuple[int, ...]


def _count(value: object) -> int:
    if isinstance(value, bool) or type(value) is not int or value < 0:
        raise _fail("vertex count is not a nonnegative integer", received=type(value).__name__)
    return value


def _edge_list(edges: object, count: int) -> tuple[tuple[int, int], ...]:
    if isinstance(edges, (str, bytes)) or not isinstance(edges, Sequence):
        raise _fail("edges must be a sequence", received=type(edges).__name__)
    return tuple(_edge(item, f"edges[{index}]", count) for index, item in enumerate(edges))


def _chain_bits(chain: object) -> tuple[int, ...]:
    if isinstance(chain, (str, bytes)) or not isinstance(chain, Sequence):
        raise _fail("chain must be a sequence", received=type(chain).__name__)
    return tuple(_bit(item, f"chain[{index}]") for index, item in enumerate(chain))


def try_cycle(vertex_count: object, edges: object, chain: object) -> Cycle:
    """Accept the chain only when every vertex has even incident support."""
    count = _count(vertex_count)
    parsed_edges = _edge_list(edges, count)
    parsed_chain = _chain_bits(chain)
    if len(parsed_edges) != len(parsed_chain):
        raise _fail("chain length does not match the edge set", edges=len(parsed_edges), chain=len(parsed_chain))
    boundary = _boundary(parsed_edges, parsed_chain, count)
    if boundary != tuple(0 for _ in range(count)):
        raise _fail("chain is not an F2 cycle", boundary=boundary)
    return Cycle(parsed_chain, boundary)


__all__ = ["Cycle", "CycleError", "try_cycle"]
