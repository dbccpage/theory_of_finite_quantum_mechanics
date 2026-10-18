"""Undirected handshaking certificate for a declared node set.

Origin: eb88d0892bd5501c7065a1dab39eede2b657f1ca:papers/derivations/ms_majorana/code/adjacency.py
Claim: urn:omega:fqm:ms-majorana:adjacency:handshaking:v1
AuthorityEffect: None
Mutation-Kills: 6 non-equivalent source mutants, executed by papers/derivations/ms_majorana/code/tests/unit/test_l5a_exact_slice.py.
Scope Fence: This file does not certify directed homology, embedding dimension, or a physical lattice.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence


class AdjacencyError(ValueError):
    """One violated adjacency invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> AdjacencyError:
    return AdjacencyError(invariant, parameters)


def _node(value: object, role: str) -> str | int:
    if isinstance(value, float):
        raise _fail("float refused at the public boundary", role=role, received="float")
    if isinstance(value, bool):
        raise _fail("boolean refused where a node was required", role=role)
    if type(value) is int:
        return value
    if isinstance(value, str) and value != "":
        return value
    raise _fail("node is not an exact identifier", role=role, received=type(value).__name__)


def _pair(value: object, role: str) -> tuple[str | int, str | int]:
    if isinstance(value, (str, bytes)) or not isinstance(value, Sequence) or len(value) != 2:
        raise _fail("edge must be a pair", role=role, received=type(value).__name__)
    return (_node(value[0], role + "[0]"), _node(value[1], role + "[1]"))


def _nodes(values: object) -> tuple[str | int, ...]:
    if isinstance(values, (str, bytes)) or not isinstance(values, Sequence):
        raise _fail("nodes must be a sequence", received=type(values).__name__)
    found: list[str | int] = []
    for index, item in enumerate(values):
        node = _node(item, f"nodes[{index}]")
        if node in found:
            raise _fail("node is repeated", node=str(node))
        found.append(node)
    return tuple(found)


def _degree_sum(adjacency: Mapping[str | int, Sequence[str | int]]) -> int:
    total = 0
    for neighbors in adjacency.values():
        total += len(neighbors)
    return total


@dataclass(frozen=True)
class HandshakingCertificate:
    """Witness that the degree sum is twice the undirected edge count."""

    adjacency: tuple[tuple[str | int, tuple[str | int, ...]], ...]
    edge_count: int
    degree_sum: int


def _undirected_key(left: str | int, right: str | int) -> tuple[str, str]:
    first = str(type(left).__name__) + ":" + str(left)
    second = str(type(right).__name__) + ":" + str(right)
    if first <= second:
        return (first, second)
    return (second, first)


def _admit_edge(
    known: set[str | int],
    neighbors: dict[str | int, list[str | int]],
    seen: set[tuple[str, str]],
    item: object,
    role: str,
) -> None:
    left, right = _pair(item, role)
    if left == right:
        raise _fail("loop edge refused", node=str(left))
    if left not in known or right not in known:
        raise _fail("edge endpoint is not a declared node", left=str(left), right=str(right))
    key = _undirected_key(left, right)
    if key in seen:
        raise _fail("undirected edge is repeated", left=str(left), right=str(right))
    seen.add(key)
    neighbors[left].append(right)
    neighbors[right].append(left)


def certify_handshaking(nodes: object, edges: object) -> HandshakingCertificate:
    """Build an undirected adjacency list and recheck the handshaking identity."""
    declared = _nodes(nodes)
    if isinstance(edges, (str, bytes)) or not isinstance(edges, Sequence):
        raise _fail("edges must be a sequence", received=type(edges).__name__)
    neighbors: dict[str | int, list[str | int]] = {node: [] for node in declared}
    seen: set[tuple[str, str]] = set()
    known = set(declared)
    for index, item in enumerate(edges):
        _admit_edge(known, neighbors, seen, item, f"edges[{index}]")
    frozen = tuple((node, tuple(neighbors[node])) for node in declared)
    degree_sum = _degree_sum(dict(frozen))
    edge_count = len(seen)
    if degree_sum != edge_count * 2:
        raise _fail("handshaking degree sum is not twice the edge count", degree_sum=degree_sum, edges=edge_count)
    return HandshakingCertificate(frozen, edge_count, degree_sum)


def build_adjacency(nodes: object, edges: object) -> dict[str | int, list[str | int]]:
    """Return the neighbor lists of a certified undirected graph."""
    certificate = certify_handshaking(nodes, edges)
    return {node: list(neighbors) for node, neighbors in certificate.adjacency}


__all__ = ["AdjacencyError", "HandshakingCertificate", "build_adjacency", "certify_handshaking"]
