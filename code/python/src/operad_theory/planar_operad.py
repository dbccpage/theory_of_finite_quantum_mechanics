"""Planar partial composition: grafting changes arity by arity(child) - 1.

Origin: dag/derivation_dag_operads.binding.yaml schema omega_operad_binding_v1.
The binding locks each derivation family to a Code slot, a Proof slot, and an
Audit codomain. This module is the planar-tree composition control.
Claim: urn:omega:fqm:operad:disjoint-graft-witness:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/src/operad_theory/test_operad_control.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 6; AST Sonar cognitive complexity max 4; AST nesting depth max 2; lizard 1.24.1 cyclomatic complexity max 6.
Scope Fence: disjoint_graft_witness checks that grafting two unary operations
into distinct leaves of a binary corolla is order-independent and raises the
leaf count by arity(child) - 1. This file does not audit the derivation DAG
and does not prove an operad axiom in Lean.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from typing import Mapping, Union


class OperadError(ValueError):
    """One violated operad invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> OperadError:
    return OperadError(invariant, parameters)


def _require_name(value: object, role: str) -> str:
    if isinstance(value, str) and value != "":
        return value
    raise _fail("operad name is not a non-empty string", role=role, received=type(value).__name__)


def _require_slot(value: object, width: int) -> int:
    if isinstance(value, float):
        raise _fail("float refused where a graft slot was required", received="float")
    if isinstance(value, bool):
        raise _fail("boolean refused where a graft slot was required")
    if not isinstance(value, int):
        raise _fail("graft slot is not an integer", received=type(value).__name__)
    if value < 0 or value >= width:
        raise _fail("graft slot is outside the tree", slot=value, width=width)
    return value


@dataclass(frozen=True)
class OperadColour:
    """A colour in a coloured operad."""

    name: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "name", _require_name(self.name, "colour"))

    def __str__(self) -> str:
        return self.name


@dataclass(frozen=True)
class Operation:
    """One operation with a tuple of input colours and one output colour."""

    name: str
    inputs: tuple[OperadColour, ...]
    output: OperadColour

    def __post_init__(self) -> None:
        object.__setattr__(self, "name", _require_name(self.name, "operation"))
        object.__setattr__(self, "inputs", _require_colours(self.inputs))
        if not isinstance(self.output, OperadColour):
            raise _fail("operation output is not a colour", received=type(self.output).__name__)

    @property
    def arity(self) -> int:
        return len(self.inputs)


def _require_colours(values: object) -> tuple[OperadColour, ...]:
    if isinstance(values, (str, bytes)) or not isinstance(values, tuple):
        raise _fail("operation inputs are not a tuple", received=type(values).__name__)
    colours: list[OperadColour] = []
    for index, item in enumerate(values):
        if not isinstance(item, OperadColour):
            raise _fail("operation input is not a colour", index=index, received=type(item).__name__)
        colours.append(item)
    return tuple(colours)


@dataclass(frozen=True)
class OpenLeaf:
    """An open input leaf."""

    colour: OperadColour

    def __post_init__(self) -> None:
        if not isinstance(self.colour, OperadColour):
            raise _fail("leaf colour is not a colour", received=type(self.colour).__name__)

    @property
    def arity(self) -> int:
        return 1

    def output_colour(self) -> OperadColour:
        return self.colour

    def term_repr(self) -> str:
        return f"leaf:{self.colour.name}"


TreeChild = Union[OpenLeaf, "PlanarTree"]


@dataclass
class PlanarTree:
    """Rooted planar tree decorated by one operation at the root."""

    root: Operation
    children: list[TreeChild] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not isinstance(self.root, Operation):
            raise _fail("tree root is not an operation", received=type(self.root).__name__)
        if not self.children:
            self.children = [OpenLeaf(colour) for colour in self.root.inputs]
        self.validate()

    def validate(self) -> None:
        if len(self.children) != self.root.arity:
            raise _fail("child count is not the root arity", children=len(self.children), arity=self.root.arity)
        for index, child in enumerate(self.children):
            _check_child(self.root, index, child)

    def output_colour(self) -> OperadColour:
        return self.root.output

    @property
    def arity(self) -> int:
        total = 0
        for child in self.children:
            total += _child_arity(child)
        return total

    @classmethod
    def corolla(cls, operation: Operation) -> PlanarTree:
        if not isinstance(operation, Operation):
            raise _fail("corolla root is not an operation", received=type(operation).__name__)
        return cls(root=operation, children=[OpenLeaf(colour) for colour in operation.inputs])

    def graft(self, slot_idx: object, subtree: PlanarTree) -> PlanarTree:
        slot = _require_slot(slot_idx, len(self.children))
        branch = _require_tree(subtree)
        target = self.children[slot]
        if _output(target) != branch.output_colour():
            raise _fail(
                "graft colour does not match the slot",
                slot=slot,
                expected=_output(target).name,
                received=branch.output_colour().name,
            )
        children = list(self.children)
        children[slot] = branch
        return PlanarTree(root=self.root, children=children)

    def term_repr(self) -> str:
        rendered = ",".join(_term(child) for child in self.children)
        return f"{self.root.name}({rendered})"

    def term_hash(self) -> str:
        return hashlib.sha256(self.term_repr().encode("utf-8")).hexdigest()


def _check_child(root: Operation, index: int, child: object) -> None:
    if not isinstance(child, (OpenLeaf, PlanarTree)):
        raise _fail("tree child has the wrong type", index=index, received=type(child).__name__)
    actual = _output(child)
    expected = root.inputs[index]
    if actual != expected:
        raise _fail("child colour does not match the input", index=index, expected=expected.name, received=actual.name)


def _output(child: OpenLeaf | PlanarTree) -> OperadColour:
    return child.output_colour()


def _child_arity(child: OpenLeaf | PlanarTree) -> int:
    return child.arity


def _term(child: OpenLeaf | PlanarTree) -> str:
    return child.term_repr()


def _require_tree(value: object) -> PlanarTree:
    if isinstance(value, PlanarTree):
        return value
    raise _fail("graft subtree is not a planar tree", received=type(value).__name__)


def disjoint_graft_witness() -> int:
    """Return 2 when the two graft orders of eta and theta into mu agree."""
    colour = OperadColour("V")
    output = OperadColour("W")
    binary = Operation("mu", (colour, colour), output)
    eta = Operation("eta", (colour,), colour)
    theta = Operation("theta", (colour,), colour)
    left = PlanarTree.corolla(binary).graft(0, PlanarTree.corolla(eta)).graft(1, PlanarTree.corolla(theta))
    right = PlanarTree.corolla(binary).graft(1, PlanarTree.corolla(theta)).graft(0, PlanarTree.corolla(eta))
    if left.term_repr() != right.term_repr():
        raise _fail("disjoint grafts disagree", left=left.term_repr(), right=right.term_repr())
    if left.arity != binary.arity - 1 + eta.arity - 1 + theta.arity:
        raise _fail("graft arity formula failed", arity=left.arity)
    if left.term_repr() != "mu(eta(leaf:V),theta(leaf:V))":
        raise _fail("graft term has the wrong name", term=left.term_repr())
    return left.arity


def main() -> int:
    """Print the disjoint-graft certificate."""
    try:
        print(disjoint_graft_witness())
    except OperadError as error:
        print(error.invariant)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
