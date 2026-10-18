"""Exact signed incidence matrix of a finite directed graph. Each row sums to zero.

Origin: eb88d0892bd5501c7065a1dab39eede2b657f1ca:papers/derivations/ms_majorana/code/incidence.py
Claim: urn:omega:fqm:ms-majorana:incidence:row-sum-zero:v1
AuthorityEffect: None
Mutation-Kills: 4 non-equivalent source mutants, executed by papers/derivations/ms_majorana/code/tests/unit/test_l5a_exact_slice.py.
Scope Fence: The matrix is the graph coboundary. It is not a continuum exterior derivative.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Mapping, Protocol, Sequence


class IncidenceError(ValueError):
    """One violated incidence invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> IncidenceError:
    return IncidenceError(invariant, parameters)


class _Directed(Protocol):
    nodes: Sequence[object]
    edges: Sequence[object]


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


def _row_sum(row: Sequence[Fraction]) -> Fraction:
    total = Fraction(0)
    for entry in row:
        total += entry
    return total


@dataclass(frozen=True)
class IncidenceCertificate:
    """Witness that every incidence row sums to zero."""

    matrix: tuple[tuple[Fraction, ...], ...]
    node_index: tuple[tuple[str | int, int], ...]
    edges: tuple[tuple[str | int, str | int], ...]


def _index_map(nodes: object) -> dict[str | int, int]:
    if isinstance(nodes, (str, bytes)) or not isinstance(nodes, Sequence) or len(nodes) == 0:
        raise _fail("nodes must be a nonempty sequence", received=type(nodes).__name__)
    index: dict[str | int, int] = {}
    for position, item in enumerate(nodes):
        node = _node(item, f"nodes[{position}]")
        if node in index:
            raise _fail("node is repeated", node=str(node))
        index[node] = position
    return index


def build_incidence_matrix(poset: object) -> tuple[tuple[tuple[Fraction, ...], ...], dict[str | int, int], tuple[tuple[str | int, str | int], ...]]:
    """Return the signed incidence matrix, the node index, and the admitted edges."""
    certificate = certify_incidence(poset)
    return certificate.matrix, dict(certificate.node_index), certificate.edges


def _one_row(
    index: Mapping[str | int, int],
    item: object,
    position: int,
) -> tuple[tuple[Fraction, ...], tuple[str | int, str | int]]:
    src, dst = _pair(item, f"edges[{position}]")
    if src == dst:
        raise _fail("loop edge refused", node=str(src))
    if src not in index or dst not in index:
        raise _fail("edge endpoint is not a declared node", src=str(src), dst=str(dst))
    row = [Fraction(0) for _ in range(len(index))]
    row[index[src]] = Fraction(-1)
    row[index[dst]] = Fraction(1)
    frozen = tuple(row)
    if _row_sum(frozen) != 0:
        raise _fail("incidence row sum is not zero", edge=position, row_sum=str(_row_sum(frozen)))
    return frozen, (src, dst)


def certify_incidence(poset: object) -> IncidenceCertificate:
    """Build B with B[e, src] = -1 and B[e, dst] = +1, then recheck each row sum."""
    if not hasattr(poset, "nodes") or not hasattr(poset, "edges"):
        raise _fail("poset must declare nodes and edges", received=type(poset).__name__)
    index = _index_map(getattr(poset, "nodes"))
    edges_raw = getattr(poset, "edges")
    if isinstance(edges_raw, (str, bytes)) or not isinstance(edges_raw, Sequence):
        raise _fail("edges must be a sequence", received=type(edges_raw).__name__)
    rows: list[tuple[Fraction, ...]] = []
    edges: list[tuple[str | int, str | int]] = []
    for position, item in enumerate(edges_raw):
        row, edge = _one_row(index, item, position)
        rows.append(row)
        edges.append(edge)
    return IncidenceCertificate(tuple(rows), tuple(index.items()), tuple(edges))


__all__ = ["IncidenceCertificate", "IncidenceError", "build_incidence_matrix", "certify_incidence"]
