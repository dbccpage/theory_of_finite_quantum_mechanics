"""Exact finite models for typed histories and contextual compression.

The Lean theorem is unbounded and abstract.  This module supplies an independent
finite replay surface.  A bounded result is labelled bounded; it becomes an
exhaustive result only when the caller supplies an acyclic signature and the
path bound reaches the signature's object count minus one.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Any, Iterable, Mapping


class HistoryError(ValueError):
    """A submitted signature, history, or question is malformed."""


@dataclass(frozen=True)
class Edge:
    name: str
    source: str
    target: str

    def __post_init__(self) -> None:
        if not self.name or not self.source or not self.target:
            raise HistoryError("edge name and endpoints must be nonempty")


@dataclass(frozen=True)
class Signature:
    objects: tuple[str, ...]
    edges: tuple[Edge, ...]

    def __post_init__(self) -> None:
        if len(set(self.objects)) != len(self.objects):
            raise HistoryError("objects must be unique")
        names = [edge.name for edge in self.edges]
        if len(set(names)) != len(names):
            raise HistoryError("edge names must be unique")
        declared = set(self.objects)
        for edge in self.edges:
            if edge.source not in declared or edge.target not in declared:
                raise HistoryError(f"edge {edge.name!r} has an undeclared endpoint")

    @property
    def edge_map(self) -> dict[str, Edge]:
        return {edge.name: edge for edge in self.edges}


@dataclass(frozen=True)
class History:
    source: str
    target: str
    edges: tuple[str, ...] = ()

    def validate(self, signature: Signature) -> None:
        if self.source not in signature.objects or self.target not in signature.objects:
            raise HistoryError("history endpoint is not in the signature")
        current = self.source
        edge_map = signature.edge_map
        for name in self.edges:
            try:
                edge = edge_map[name]
            except KeyError as exc:
                raise HistoryError(f"unknown edge {name!r}") from exc
            if edge.source != current:
                raise HistoryError(
                    f"edge {name!r} starts at {edge.source!r}, expected {current!r}"
                )
            current = edge.target
        if current != self.target:
            raise HistoryError(
                f"history ends at {current!r}, declared target is {self.target!r}"
            )


def compose(signature: Signature, first: History, second: History) -> History:
    first.validate(signature)
    second.validate(signature)
    if first.target != second.source:
        raise HistoryError("history endpoints do not compose")
    result = History(first.source, second.target, first.edges + second.edges)
    result.validate(signature)
    return result


@dataclass(frozen=True)
class Question:
    """A serializable endpoint-typed finite question."""

    name: str
    source: str
    target: str
    kind: str
    argument: Any = None

    def evaluate(self, history: History) -> Any:
        if history.source != self.source or history.target != self.target:
            raise HistoryError(f"question {self.name!r} received the wrong hom-set")
        if self.kind == "exact_word":
            return history.edges == tuple(self.argument)
        if self.kind == "contains":
            return str(self.argument) in history.edges
        if self.kind == "length_mod":
            modulus = self.argument
            if isinstance(modulus, bool) or not isinstance(modulus, int) or modulus <= 0:
                raise HistoryError("length modulus must be a positive integer")
            return len(history.edges) % modulus
        if self.kind == "edge_count":
            return history.edges.count(str(self.argument))
        raise HistoryError(f"unknown question kind {self.kind!r}")


def enumerate_histories(
    signature: Signature, source: str, target: str, max_length: int
) -> tuple[History, ...]:
    if isinstance(max_length, bool) or not isinstance(max_length, int) or max_length < 0:
        raise HistoryError("maximum length must be a nonnegative integer")
    if source not in signature.objects or target not in signature.objects:
        raise HistoryError("enumeration endpoint is not in the signature")
    outgoing: dict[str, list[Edge]] = {obj: [] for obj in signature.objects}
    for edge in signature.edges:
        outgoing[edge.source].append(edge)
    for edges in outgoing.values():
        edges.sort(key=lambda edge: edge.name)

    found: list[History] = []

    def visit(current: str, names: tuple[str, ...], remaining: int) -> None:
        if current == target:
            found.append(History(source, target, names))
        if remaining == 0:
            return
        for edge in outgoing[current]:
            visit(edge.target, names + (edge.name,), remaining - 1)

    visit(source, (), max_length)
    return tuple(found)


def bounded_context_counterexample(
    signature: Signature,
    left: History,
    right: History,
    questions: Iterable[Question],
    max_context_length: int,
) -> Mapping[str, Any] | None:
    """Return the first prefix/question/suffix that distinguishes two paths."""

    left.validate(signature)
    right.validate(signature)
    if (left.source, left.target) != (right.source, right.target):
        raise HistoryError("contextual comparison requires parallel histories")
    typed_questions = tuple(questions)
    for question in sorted(typed_questions, key=lambda item: item.name):
        prefixes = enumerate_histories(
            signature, question.source, left.source, max_context_length
        )
        suffixes = enumerate_histories(
            signature, left.target, question.target, max_context_length
        )
        for prefix in prefixes:
            for suffix in suffixes:
                left_in_context = compose(signature, compose(signature, prefix, left), suffix)
                right_in_context = compose(signature, compose(signature, prefix, right), suffix)
                left_answer = question.evaluate(left_in_context)
                right_answer = question.evaluate(right_in_context)
                if left_answer != right_answer:
                    return {
                        "question": question.name,
                        "prefix": list(prefix.edges),
                        "suffix": list(suffix.edges),
                        "left_answer": left_answer,
                        "right_answer": right_answer,
                    }
    return None


def edge_counts(history: History) -> dict[str, int]:
    return dict(sorted(Counter(history.edges).items()))


def vertex_boundary(signature: Signature, history: History) -> dict[str, int]:
    """Boundary of the signed edge-occurrence chain."""

    history.validate(signature)
    boundary = {obj: 0 for obj in signature.objects}
    edge_map = signature.edge_map
    for name in history.edges:
        edge = edge_map[name]
        boundary[edge.source] -= 1
        boundary[edge.target] += 1
    return boundary


def expected_endpoint_boundary(signature: Signature, history: History) -> dict[str, int]:
    history.validate(signature)
    boundary = {obj: 0 for obj in signature.objects}
    boundary[history.source] -= 1
    boundary[history.target] += 1
    return boundary
