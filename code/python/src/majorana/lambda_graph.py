"""A declared strict poset presentation is a directed acyclic graph.

Origin: eb88d0892bd5501c7065a1dab39eede2b657f1ca:papers/derivations/ms_majorana/code/lambda_graph.py
Claim: urn:omega:fqm:ms-majorana:lambda-graph:acyclic-presentation:v1
AuthorityEffect: None
Mutation-Kills: 4 non-equivalent source mutants, executed by papers/derivations/ms_majorana/code/tests/unit/test_l5a_exact_slice.py.
Scope Fence: Acyclicity of the supplied relations is not a theorem that every lambda-term is normalizing.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence


class LambdaGraphError(ValueError):
    """One violated poset-graph invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> LambdaGraphError:
    return LambdaGraphError(invariant, parameters)


def _node(value: object, role: str) -> str:
    if isinstance(value, float):
        raise _fail("float refused at the public boundary", role=role, received="float")
    if isinstance(value, bool) or not isinstance(value, str) or value == "":
        raise _fail("node must be a nonempty string", role=role, received=type(value).__name__)
    return value


def _nodes(values: object) -> tuple[str, ...]:
    if isinstance(values, (str, bytes)) or not isinstance(values, Sequence) or len(values) == 0:
        raise _fail("nodes must be a nonempty sequence", received=type(values).__name__)
    found: list[str] = []
    for index, item in enumerate(values):
        node = _node(item, f"nodes[{index}]")
        if node in found:
            raise _fail("node is repeated", node=node)
        found.append(node)
    return tuple(found)


def _pair(value: object, role: str) -> tuple[str, str]:
    if isinstance(value, (str, bytes)) or not isinstance(value, Sequence) or len(value) != 2:
        raise _fail("relation must be a pair", role=role, received=type(value).__name__)
    return (_node(value[0], role + "[0]"), _node(value[1], role + "[1]"))


def _relations(values: object, known: set[str]) -> tuple[tuple[str, str], ...]:
    if isinstance(values, (str, bytes)) or not isinstance(values, Sequence):
        raise _fail("relations must be a sequence", received=type(values).__name__)
    found: list[tuple[str, str]] = []
    for index, item in enumerate(values):
        lower, upper = _pair(item, f"relations[{index}]")
        if lower == upper:
            raise _fail("reflexive relation refused", node=lower)
        if lower not in known or upper not in known:
            raise _fail("relation endpoint is not a declared node", lower=lower, upper=upper)
        found.append((lower, upper))
    return tuple(found)


def _indegree(nodes: Sequence[str], relations: Sequence[tuple[str, str]]) -> dict[str, int]:
    degree = {node: 0 for node in nodes}
    for _lower, upper in relations:
        degree[upper] += 1
    return degree


def _order(nodes: Sequence[str], relations: Sequence[tuple[str, str]]) -> tuple[str, ...]:
    degree = _indegree(nodes, relations)
    ready = [node for node in nodes if degree[node] == 0]
    ordered: list[str] = []
    outgoing: dict[str, list[str]] = {node: [] for node in nodes}
    for lower, upper in relations:
        outgoing[lower].append(upper)
    while len(ready) != 0:
        current = ready.pop(0)
        ordered.append(current)
        for upper in outgoing[current]:
            degree[upper] -= 1
            if degree[upper] == 0:
                ready.append(upper)
    return tuple(ordered)


@dataclass(frozen=True)
class AcyclicCertificate:
    """Witness that Kahn's algorithm ordered every declared node."""

    order: tuple[str, ...]
    relation_count: int


def graph_from_poset(nodes: object, relations: object) -> AcyclicCertificate:
    """Admit a strict relation list only when it is acyclic."""
    declared = _nodes(nodes)
    parsed = _relations(relations, set(declared))
    ordered = _order(declared, parsed)
    if len(ordered) != len(declared):
        raise _fail("relation graph contains a directed cycle", ordered=len(ordered), nodes=len(declared))
    return AcyclicCertificate(ordered, len(parsed))


__all__ = ["AcyclicCertificate", "LambdaGraphError", "graph_from_poset"]
