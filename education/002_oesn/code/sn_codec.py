"""Flat S(n) AST codec for the declared ASCII grammar.

AuthorityEffect: None. GenesisEffect: None.
The Lean syntax uses corresponding constructors; a cross-language proof is
not provided. Stage numerals normalize leading zeroes.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Union


class SnCodecError(ValueError):
    """Raised when wire deserialization or AST serialization fails."""


# ---------------------------------------------------------------------------
# AST Data Structures (Mirroring SnSyntax.lean)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Glyph:
    char: str

    def __post_init__(self) -> None:
        if type(self.char) is not str or len(self.char) != 1:
            raise SnCodecError(f"Glyph must be single character, got {self.char!r}")
        if self.char not in "abcdefghijklmnopqrstuvwxyz0123456789":
            raise SnCodecError(f"Glyph must be lowercase ASCII or digit, got {self.char!r}")

    @property
    def is_digit(self) -> bool:
        return self.char.isdigit()

    @property
    def is_latin(self) -> bool:
        return self.char.isalpha()

    def to_wire(self) -> str:
        return self.char


@dataclass(frozen=True)
class GroundToken:
    """Stage S(0): Ground token '<>'."""

    def to_wire(self) -> str:
        return "<>"


@dataclass(frozen=True)
class SuppliedToken:
    """Stage S(1): Supplied lone mark '<glyph>'."""

    mark: Glyph

    def to_wire(self) -> str:
        return f"<{self.mark.to_wire()}>"


@dataclass(frozen=True)
class RetainedPair:
    """Stage S(2): Retained pair '<g1 g2>'."""

    first: Glyph
    second: Glyph

    def to_wire(self) -> str:
        return f"<{self.first.to_wire()}{self.second.to_wire()}>"


@dataclass(frozen=True)
class DirectedCut:
    """Stage S(3): Directed cut '<src->tgt>'."""

    src: Glyph
    tgt: Glyph

    def to_wire(self) -> str:
        return f"<{self.src.to_wire()}->{self.tgt.to_wire()}>"


@dataclass(frozen=True)
class SimplexCut:
    """Stage S(3): Simplex cut '[v0,v1]'."""

    v0: Glyph
    v1: Glyph

    def to_wire(self) -> str:
        return f"[{self.v0.to_wire()},{self.v1.to_wire()}]"


RelationToken = Union[RetainedPair, DirectedCut, SimplexCut]


@dataclass(frozen=True)
class InnerBodyArrow:
    src: Glyph
    tgt: Glyph

    def to_wire(self) -> str:
        return f"{self.src.to_wire()}->{self.tgt.to_wire()}"


@dataclass(frozen=True)
class InnerBodyPair:
    first: Glyph
    second: Glyph

    def to_wire(self) -> str:
        return f"{self.first.to_wire()},{self.second.to_wire()}"


@dataclass(frozen=True)
class InnerBodyGlyphs:
    glyphs: tuple[Glyph, ...]

    def to_wire(self) -> str:
        return "".join(g.to_wire() for g in self.glyphs)


InnerBody = Union[InnerBodyArrow, InnerBodyPair, InnerBodyGlyphs]


@dataclass(frozen=True)
class SectionLift:
    """Stage S(6): Section lift 'u_N<inner_body>'."""

    stage: int
    body: InnerBody

    def __post_init__(self) -> None:
        if type(self.stage) is not int or self.stage < 0:
            raise SnCodecError(f"Stage must be non-negative, got {self.stage}")

    def to_wire(self) -> str:
        return f"u_{self.stage}<{self.body.to_wire()}>"


@dataclass(frozen=True)
class RetractionMap:
    """Stage S(6): Retraction down-map 'r_N<inner_body>'."""

    stage: int
    body: InnerBody

    def __post_init__(self) -> None:
        if type(self.stage) is not int or self.stage < 0:
            raise SnCodecError(f"Stage must be non-negative, got {self.stage}")

    def to_wire(self) -> str:
        return f"r_{self.stage}<{self.body.to_wire()}>"


@dataclass(frozen=True)
class NonDescent:
    """Stage S(6): Typed refusal token 'NON_DESCENT'."""

    def to_wire(self) -> str:
        return "NON_DESCENT"


SnNode = Union[
    GroundToken,
    SuppliedToken,
    RetainedPair,
    DirectedCut,
    SimplexCut,
    SectionLift,
    RetractionMap,
    NonDescent,
]


# ---------------------------------------------------------------------------
# Serializer (AST -> Lean 4 Wire Encoding)
# ---------------------------------------------------------------------------


def serialize_sn(node: SnNode) -> str:
    """Serialize an S(n) AST node to its exact Lean 4 wire encoding string."""
    if hasattr(node, "to_wire"):
        return node.to_wire()
    raise SnCodecError(f"Unsupported S(n) node type: {type(node)}")


# ---------------------------------------------------------------------------
# Deserializer (Lean 4 Wire Encoding -> AST)
# ---------------------------------------------------------------------------

_LIFT_RE = re.compile(r"^u_([0-9]+)<(.*)>$")
_RETRACT_RE = re.compile(r"^r_([0-9]+)<(.*)>$")
_ARROW_RE = re.compile(r"^([a-z0-9])->([a-z0-9])$")
_PAIR_RE = re.compile(r"^([a-z0-9]),([a-z0-9])$")
_SIMPLEX_RE = re.compile(r"^\[([a-z0-9]),([a-z0-9])\]$")
_DIRECTED_CUT_RE = re.compile(r"^<([a-z0-9])->([a-z0-9])>$")


def _parse_inner_body(text: str) -> InnerBody:
    m_arr = _ARROW_RE.fullmatch(text)
    if m_arr:
        return InnerBodyArrow(src=Glyph(m_arr.group(1)), tgt=Glyph(m_arr.group(2)))
    m_pr = _PAIR_RE.fullmatch(text)
    if m_pr:
        return InnerBodyPair(first=Glyph(m_pr.group(1)), second=Glyph(m_pr.group(2)))
    # Glyphs: zero or more glyphs
    for ch in text:
        if ch not in "abcdefghijklmnopqrstuvwxyz0123456789":
            raise SnCodecError(f"Invalid glyph in inner body: {ch!r}")
    return InnerBodyGlyphs(glyphs=tuple(Glyph(ch) for ch in text))


def deserialize_sn(wire: str) -> SnNode:
    """Deserialize a wire string into its corresponding S(n) AST node."""
    if not isinstance(wire, str):
        raise SnCodecError(f"Expected str wire input, got {type(wire)}")

    # 1. Ground token
    if wire == "<>":
        return GroundToken()

    # 2. NonDescent
    if wire == "NON_DESCENT":
        return NonDescent()

    # 3. Simplex cut: [a,b]
    m_sx = _SIMPLEX_RE.fullmatch(wire)
    if m_sx:
        return SimplexCut(v0=Glyph(m_sx.group(1)), v1=Glyph(m_sx.group(2)))

    # 4. Directed cut: <a->b>
    m_dc = _DIRECTED_CUT_RE.fullmatch(wire)
    if m_dc:
        return DirectedCut(src=Glyph(m_dc.group(1)), tgt=Glyph(m_dc.group(2)))

    # 5. Section lift: u_N<...>
    m_lift = _LIFT_RE.fullmatch(wire)
    if m_lift:
        stage = int(m_lift.group(1))
        body = _parse_inner_body(m_lift.group(2))
        return SectionLift(stage=stage, body=body)

    # 6. Retraction map: r_N<...>
    m_ret = _RETRACT_RE.fullmatch(wire)
    if m_ret:
        stage = int(m_ret.group(1))
        body = _parse_inner_body(m_ret.group(2))
        return RetractionMap(stage=stage, body=body)

    # 7. Angle-bracketed tokens: <a> or <ab>
    if wire.startswith("<") and wire.endswith(">"):
        inner = wire[1:-1]
        if len(inner) == 1:
            return SuppliedToken(mark=Glyph(inner))
        if len(inner) == 2:
            return RetainedPair(first=Glyph(inner[0]), second=Glyph(inner[1]))
        raise SnCodecError(f"Unsupported enclosed wire token length: {wire!r}")

    raise SnCodecError(f"Unrecognized S(n) wire token: {wire!r}")
