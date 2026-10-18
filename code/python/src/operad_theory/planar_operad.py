"""Planar colored operads, rooted planar trees, grafting, and term hashing.

AuthorityEffect: None.
"""

from __future__ import annotations
from dataclasses import dataclass, field
import hashlib
from typing import List, Optional, Tuple, Union


class OperadError(Exception):
    """Base exception for operadic operations."""
    pass


@dataclass(frozen=True)
class OperadColour:
    """A colour (type) in a colored operad."""
    name: str

    def __str__(self) -> str:
        return self.name


@dataclass(frozen=True)
class Operation:
    """An operation with typed inputs and single typed output."""
    name: str
    inputs: Tuple[OperadColour, ...]
    output: OperadColour

    @property
    def arity(self) -> int:
        return len(self.inputs)


@dataclass(frozen=True)
class OpenLeaf:
    """An open leaf port awaiting grafting."""
    colour: OperadColour

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
    """A rooted planar tree whose vertices are decorated by operadic operations."""
    root: Operation
    children: List[TreeChild] = field(default_factory=list)

    def __post_init__(self):
        if not self.children:
            # Default corolla with open leaves
            self.children = [OpenLeaf(c) for c in self.root.inputs]
        self.validate()

    def validate(self) -> None:
        if len(self.children) != self.root.arity:
            raise OperadError(
                f"Children count {len(self.children)} != root arity {self.root.arity}"
            )
        for idx, child in enumerate(self.children):
            expected = self.root.inputs[idx]
            actual = child.output_colour()
            if actual != expected:
                raise OperadError(
                    f"Child colour mismatch at slot {idx}: expected {expected.name}, got {actual.name}"
                )

    def output_colour(self) -> OperadColour:
        return self.root.output

    @property
    def arity(self) -> int:
        return sum(child.arity for child in self.children)

    @classmethod
    def corolla(cls, op: Operation) -> PlanarTree:
        return cls(root=op, children=[OpenLeaf(c) for c in op.inputs])

    def graft(self, slot_idx: int, subtree: PlanarTree) -> PlanarTree:
        """Graft a subtree into the slot_idx child slot."""
        if slot_idx < 0 or slot_idx >= len(self.children):
            raise OperadError(f"Graft slot index {slot_idx} out of range [0, {len(self.children)})")

        target_slot = self.children[slot_idx]
        if target_slot.output_colour() != subtree.output_colour():
            raise OperadError(
                f"Cannot graft: slot requires colour {target_slot.output_colour().name} "
                f"but subtree produces {subtree.output_colour().name}"
            )

        new_children = list(self.children)
        new_children[slot_idx] = subtree
        return PlanarTree(root=self.root, children=new_children)

    def term_repr(self) -> str:
        child_reprs = ",".join(c.term_repr() for c in self.children)
        return f"{self.root.name}({child_reprs})"

    def term_hash(self) -> str:
        return hashlib.sha256(self.term_repr().encode("utf-8")).hexdigest()
