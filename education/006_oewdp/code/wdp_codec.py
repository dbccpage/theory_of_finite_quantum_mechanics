"""WDP AST Codec: Serializer and Deserializer linking wdp.ebnf to AST representations.

AuthorityEffect: None. GenesisEffect: None.
Connects wdp.ebnf grammar profiles to typed Python AST nodes representing witnessed differences,
transport events, quotient witnesses, balance matrices, and typed obstruction refusals.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import FrozenSet, Sequence, Union


class WdpCodecError(ValueError):
    """Raised when wire deserialization or AST serialization fails."""


# ---------------------------------------------------------------------------
# Constants & Character Sets
# ---------------------------------------------------------------------------

WITNESS_STATUSES: FrozenSet[str] = frozenset(
    {
        "EXACT_REPAIR",
        "HOMOTOPIC_ZERO",
        "CLOSED_CLASS",
        "OPEN_OBSTRUCTION",
    }
)

REFUSAL_CODES: FrozenSet[str] = frozenset(
    {
        "ERR_FIBER_NON_CONSTANT",
        "ERR_MALFORMED_FILLER",
        "ERR_CAPACITY_EXHAUSTED",
        "ERR_DUAL_IMBALANCE",
    }
)


# ---------------------------------------------------------------------------
# AST Data Structures
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Glyph:
    """Atomic terminal mark over Sigma36 (lower_latin | digit)."""

    char: str

    def __post_init__(self) -> None:
        if len(self.char) != 1 or not (
            (self.char.islower() and self.char.isascii()) or self.char.isdigit()
        ):
            raise WdpCodecError(f"Glyph must be [a-z0-9], got {self.char!r}")

    @property
    def is_digit(self) -> bool:
        return self.char.isdigit()

    @property
    def is_latin(self) -> bool:
        return self.char.isalpha()

    def to_wire(self) -> str:
        return self.char


@dataclass(frozen=True)
class Word:
    """Non-empty sequence of glyphs over Sigma36."""

    text: str

    def __post_init__(self) -> None:
        if not self.text:
            raise WdpCodecError("Word cannot be empty")
        for ch in self.text:
            if not ((ch.islower() and ch.isascii()) or ch.isdigit()):
                raise WdpCodecError(f"Word chars must be [a-z0-9], got {ch!r} in {self.text!r}")

    @classmethod
    def from_glyphs(cls, glyphs: Sequence[Glyph]) -> Word:
        return cls(text="".join(g.to_wire() for g in glyphs))

    @property
    def glyphs(self) -> tuple[Glyph, ...]:
        return tuple(Glyph(c) for c in self.text)

    def to_wire(self) -> str:
        return self.text


# 1. Witnessed Difference Tokens


@dataclass(frozen=True)
class DistinctCut:
    """Witnessed difference cut '<glyph!=glyph>'."""

    first: Glyph
    second: Glyph

    def to_wire(self) -> str:
        return f"<{self.first.to_wire()}!={self.second.to_wire()}>"


@dataclass(frozen=True)
class SimplexPair:
    """Simplex edge pair '<glyph,glyph>'."""

    first: Glyph
    second: Glyph

    def to_wire(self) -> str:
        return f"<{self.first.to_wire()},{self.second.to_wire()}>"


@dataclass(frozen=True)
class MarkedQuotient:
    """Marked quotient token 'quot<glyph/word>'."""

    numerator: Glyph
    fiber: Word

    def to_wire(self) -> str:
        return f"quot<{self.numerator.to_wire()}/{self.fiber.to_wire()}>"


DifferenceItem = Union[DistinctCut, SimplexPair, MarkedQuotient]


# 2. Transport & Homotopy Events


@dataclass(frozen=True)
class D0Map:
    """Boundary d0 map 'd0(glyph)'."""

    target: Glyph

    def to_wire(self) -> str:
        return f"d0({self.target.to_wire()})"


@dataclass(frozen=True)
class D1Map:
    """Boundary d1 map 'd1(glyph,glyph)'."""

    first: Glyph
    second: Glyph

    def to_wire(self) -> str:
        return f"d1({self.first.to_wire()},{self.second.to_wire()})"


@dataclass(frozen=True)
class HHomotopy:
    """Homotopy filler operator 'H(glyph,glyph)'."""

    first: Glyph
    second: Glyph

    def to_wire(self) -> str:
        return f"H({self.first.to_wire()},{self.second.to_wire()})"


TransportEvent = Union[D0Map, D1Map, HHomotopy]


# 3. Quotient Witness & Obstruction Profile


@dataclass(frozen=True)
class QuotientWitness:
    """Quotient witness 'witness<fiber:word,status:witness_status>'."""

    fiber: Word
    status: str

    def __post_init__(self) -> None:
        if self.status not in WITNESS_STATUSES:
            raise WdpCodecError(
                f"Invalid witness status: {self.status!r}, must be one of {sorted(WITNESS_STATUSES)}"
            )

    def to_wire(self) -> str:
        return f"witness<fiber:{self.fiber.to_wire()},status:{self.status}>"


# 4. Balance Matrix & Complex Composite


@dataclass(frozen=True)
class BalanceMatrix:
    """Balance matrix 'balance<sites:digits,trace:digits>'."""

    sites: int
    trace: int

    def __post_init__(self) -> None:
        if self.sites < 0:
            raise WdpCodecError(f"sites must be non-negative, got {self.sites}")
        if self.trace < 0:
            raise WdpCodecError(f"trace must be non-negative, got {self.trace}")

    def to_wire(self) -> str:
        return f"balance<sites:{self.sites},trace:{self.trace}>"


# 5. Typed Refusal Codes


@dataclass(frozen=True)
class WdpRefusal:
    """Typed refusal token 'refusal<refusal_code>'."""

    code: str

    def __post_init__(self) -> None:
        if self.code not in REFUSAL_CODES:
            raise WdpCodecError(
                f"Invalid refusal code: {self.code!r}, must be one of {sorted(REFUSAL_CODES)}"
            )

    def to_wire(self) -> str:
        return f"refusal<{self.code}>"


WdpNode = Union[
    DistinctCut,
    SimplexPair,
    MarkedQuotient,
    D0Map,
    D1Map,
    HHomotopy,
    QuotientWitness,
    BalanceMatrix,
    WdpRefusal,
]


# ---------------------------------------------------------------------------
# Serializer (AST -> Wire String)
# ---------------------------------------------------------------------------


def serialize_wdp(node: WdpNode) -> str:
    """Serialize a WDP AST node to its exact wire encoding string."""
    if hasattr(node, "to_wire"):
        return node.to_wire()
    raise WdpCodecError(f"Unsupported WDP node type: {type(node)}")


# ---------------------------------------------------------------------------
# Deserializer (Wire String -> AST)
# ---------------------------------------------------------------------------

_DISTINCT_CUT_RE = re.compile(r"^<([a-z0-9])!=([a-z0-9])>$")
_SIMPLEX_PAIR_RE = re.compile(r"^<([a-z0-9]),([a-z0-9])>$")
_MARKED_QUOTIENT_RE = re.compile(r"^quot<([a-z0-9])/([a-z0-9]+)>$")

_D0_MAP_RE = re.compile(r"^d0\(([a-z0-9])\)$")
_D1_MAP_RE = re.compile(r"^d1\(([a-z0-9]),([a-z0-9])\)$")
_H_HOMOTOPY_RE = re.compile(r"^H\(([a-z0-9]),([a-z0-9])\)$")

_QUOTIENT_WITNESS_RE = re.compile(r"^witness<fiber:([a-z0-9]+),status:([A-Za-z0-9_]+)>$")
_BALANCE_MATRIX_RE = re.compile(r"^balance<sites:(\d+),trace:(\d+)>$")
_REFUSAL_RE = re.compile(r"^refusal<([A-Za-z0-9_]+)>$")


def deserialize_wdp(wire: str) -> WdpNode:
    """Deserialize a wire string into its corresponding WDP AST node."""
    if not isinstance(wire, str):
        raise WdpCodecError(f"Expected str wire input, got {type(wire)}")

    # 1. Distinct Cut: <a!=b>
    m_dc = _DISTINCT_CUT_RE.fullmatch(wire)
    if m_dc:
        return DistinctCut(first=Glyph(m_dc.group(1)), second=Glyph(m_dc.group(2)))

    # 2. Simplex Pair: <x,y>
    m_sp = _SIMPLEX_PAIR_RE.fullmatch(wire)
    if m_sp:
        return SimplexPair(first=Glyph(m_sp.group(1)), second=Glyph(m_sp.group(2)))

    # 3. Marked Quotient: quot<a/fiber1>
    m_mq = _MARKED_QUOTIENT_RE.fullmatch(wire)
    if m_mq:
        return MarkedQuotient(numerator=Glyph(m_mq.group(1)), fiber=Word(m_mq.group(2)))

    # 4. d0 Map: d0(t)
    m_d0 = _D0_MAP_RE.fullmatch(wire)
    if m_d0:
        return D0Map(target=Glyph(m_d0.group(1)))

    # 5. d1 Map: d1(a,b)
    m_d1 = _D1_MAP_RE.fullmatch(wire)
    if m_d1:
        return D1Map(first=Glyph(m_d1.group(1)), second=Glyph(m_d1.group(2)))

    # 6. Homotopy H: H(a,b)
    m_h = _H_HOMOTOPY_RE.fullmatch(wire)
    if m_h:
        return HHomotopy(first=Glyph(m_h.group(1)), second=Glyph(m_h.group(2)))

    # 7. Quotient Witness: witness<fiber:...,status:...>
    m_qw = _QUOTIENT_WITNESS_RE.fullmatch(wire)
    if m_qw:
        fiber_str, status_str = m_qw.group(1), m_qw.group(2)
        return QuotientWitness(fiber=Word(fiber_str), status=status_str)

    # 8. Balance Matrix: balance<sites:N,trace:M>
    m_bm = _BALANCE_MATRIX_RE.fullmatch(wire)
    if m_bm:
        sites_val, trace_val = int(m_bm.group(1)), int(m_bm.group(2))
        return BalanceMatrix(sites=sites_val, trace=trace_val)

    # 9. Refusal: refusal<code>
    m_ref = _REFUSAL_RE.fullmatch(wire)
    if m_ref:
        code_str = m_ref.group(1)
        return WdpRefusal(code=code_str)

    raise WdpCodecError(f"Unrecognized or invalid WDP wire token: {wire!r}")
