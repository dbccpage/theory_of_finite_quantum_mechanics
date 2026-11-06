"""MSS-N AST codec for the 22 declared starts of mssn.ebnf.

AuthorityEffect: None. GenesisEffect: None.
The separate Lean syntax sketches do not prove this Python parser correct.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Optional


class MssnCodecError(ValueError):
    """Raised when wire deserialization or AST serialization fails."""


# ---------------------------------------------------------------------------
# AST Data Structures
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class RawGlyphs:
    text: str

    def __post_init__(self) -> None:
        if any(c not in "abcdefghijklmnopqrstuvwxyz0123456789<>" for c in self.text):
            raise MssnCodecError("Raw glyphs must belong to the declared 38-glyph alphabet")

    def to_wire(self) -> str:
        return self.text


@dataclass(frozen=True)
class Glyph:
    char: str

    def __post_init__(self) -> None:
        if len(self.char) != 1 or not (
            self.char in "abcdefghijklmnopqrstuvwxyz0123456789"
        ):
            raise MssnCodecError(f"Glyph must be [a-z0-9], got {self.char!r}")

    def to_wire(self) -> str:
        return self.char


@dataclass(frozen=True)
class Word:
    chars: tuple[Glyph, ...]

    def __post_init__(self) -> None:
        if not self.chars:
            raise MssnCodecError("Word cannot be empty")

    def to_wire(self) -> str:
        return "".join(g.to_wire() for g in self.chars)


@dataclass(frozen=True)
class GlyphPath:
    head: Glyph
    steps: tuple[tuple[str, Glyph], ...]  # (dir, glyph) where dir in (">", "<")

    def to_wire(self) -> str:
        return self.head.to_wire() + "".join(d + g.to_wire() for d, g in self.steps)


@dataclass(frozen=True)
class LabelPath:
    head: Word
    steps: tuple[tuple[str, Word], ...]

    def to_wire(self) -> str:
        return self.head.to_wire() + "".join(d + w.to_wire() for d, w in self.steps)


@dataclass(frozen=True)
class SuffixVertex:
    label: str
    digits: str

    def __post_init__(self) -> None:
        if len(self.label) != 1 or not (self.label.islower() and self.label.isascii()):
            raise MssnCodecError(f"SuffixVertex label must be lower_latin, got {self.label!r}")
        if not self.digits or not (self.digits.isascii() and self.digits.isdigit()):
            raise MssnCodecError(
                f"SuffixVertex digits must be non-empty digits, got {self.digits!r}"
            )

    def to_wire(self) -> str:
        return self.label + self.digits


@dataclass(frozen=True)
class SuffixPath:
    head: SuffixVertex
    steps: tuple[tuple[str, SuffixVertex], ...]

    def to_wire(self) -> str:
        return self.head.to_wire() + "".join(d + v.to_wire() for d, v in self.steps)


@dataclass(frozen=True)
class PathList:
    paths: tuple[GlyphPath, ...]

    def __post_init__(self) -> None:
        if not self.paths:
            raise MssnCodecError("PathList cannot be empty")

    def to_wire(self) -> str:
        return ";".join(p.to_wire() for p in self.paths)


@dataclass(frozen=True)
class SuffixList:
    paths: tuple[SuffixPath, ...]

    def __post_init__(self) -> None:
        if not self.paths:
            raise MssnCodecError("SuffixList cannot be empty")

    def to_wire(self) -> str:
        return ";".join(p.to_wire() for p in self.paths)


@dataclass(frozen=True)
class Scalar:
    sign: Optional[str]
    whole: str
    frac_or_ratio: Optional[tuple[str, str]]  # ('.', digits) or ('/', digits)

    def __post_init__(self) -> None:
        if self.sign is not None and self.sign not in ("+", "-"):
            raise MssnCodecError(f"Scalar sign must be '+' or '-', got {self.sign!r}")
        if not (self.whole.isascii() and self.whole.isdigit()):
            raise MssnCodecError(f"Scalar whole must be digits, got {self.whole!r}")
        if self.frac_or_ratio is not None:
            sep, d = self.frac_or_ratio
            if sep not in (".", "/"):
                raise MssnCodecError(f"Fraction separator must be '.' or '/', got {sep!r}")
            if not (d.isascii() and d.isdigit()):
                raise MssnCodecError(f"Fraction part must be digits, got {d!r}")

    def to_wire(self) -> str:
        res = self.sign or ""
        res += self.whole
        if self.frac_or_ratio is not None:
            res += self.frac_or_ratio[0] + self.frac_or_ratio[1]
        return res


@dataclass(frozen=True)
class ScalarVertex:
    label: str
    scalar: Scalar

    def __post_init__(self) -> None:
        if len(self.label) != 1 or not (self.label.islower() and self.label.isascii()):
            raise MssnCodecError(f"ScalarVertex label must be lower_latin, got {self.label!r}")

    def to_wire(self) -> str:
        return f"{self.label}:{self.scalar.to_wire()}"


@dataclass(frozen=True)
class ScalarPath:
    head: ScalarVertex
    steps: tuple[tuple[str, ScalarVertex], ...]

    def to_wire(self) -> str:
        return self.head.to_wire() + "".join(d + v.to_wire() for d, v in self.steps)


@dataclass(frozen=True)
class VectorVertex:
    label: str
    coords: tuple[Scalar, ...]

    def __post_init__(self) -> None:
        if len(self.label) != 1 or not (self.label.islower() and self.label.isascii()):
            raise MssnCodecError(f"VectorVertex label must be lower_latin, got {self.label!r}")
        if not self.coords:
            raise MssnCodecError("VectorVertex coords cannot be empty")

    def to_wire(self) -> str:
        return f"{self.label}[{','.join(c.to_wire() for c in self.coords)}]"


@dataclass(frozen=True)
class VectorPath:
    head: VectorVertex
    steps: tuple[tuple[str, VectorVertex], ...]

    def to_wire(self) -> str:
        return self.head.to_wire() + "".join(d + v.to_wire() for d, v in self.steps)


@dataclass(frozen=True)
class EdgeWeightPath:
    head: str
    steps: tuple[tuple[str, Scalar, str], ...]  # (dir, weight, next_latin)

    def to_wire(self) -> str:
        res = self.head
        for d, w, lat in self.steps:
            res += f"{d}{w.to_wire()}{d}{lat}"
        return res


@dataclass(frozen=True)
class LabelledPath:
    head: str
    steps: tuple[tuple[Word, str], ...]  # (word, next_latin)

    def to_wire(self) -> str:
        res = self.head
        for w, lat in self.steps:
            res += f"-{w.to_wire()}>{lat}"
        return res


@dataclass(frozen=True)
class PrefixLeaf:
    glyph: Glyph

    def to_wire(self) -> str:
        return self.glyph.to_wire()


@dataclass(frozen=True)
class PrefixBranch:
    dir: str
    left: Any
    right: Any

    def to_wire(self) -> str:
        return f"{self.dir}{self.left.to_wire()}{self.right.to_wire()}"


@dataclass(frozen=True)
class PostfixTree:
    head: Glyph
    steps: tuple[tuple[PostfixTree, str], ...] = ()  # (child_tree, dir) where dir in (">", "<")

    def to_wire(self) -> str:
        return self.head.to_wire() + "".join(t.to_wire() + d for t, d in self.steps)


@dataclass(frozen=True)
class Sequence:
    glyphs: tuple[Glyph, ...]

    def __post_init__(self) -> None:
        if not self.glyphs:
            raise MssnCodecError("Sequence cannot be empty")

    def to_wire(self) -> str:
        return ",".join(g.to_wire() for g in self.glyphs)


@dataclass(frozen=True)
class NestedLeaf:
    glyph: Glyph

    def to_wire(self) -> str:
        return self.glyph.to_wire()


@dataclass(frozen=True)
class NestedGroup:
    children: tuple[Any, ...]

    def to_wire(self) -> str:
        return f"({','.join(c.to_wire() for c in self.children)})"


@dataclass(frozen=True)
class HeadAtom:
    word: Word

    def to_wire(self) -> str:
        return self.word.to_wire()


@dataclass(frozen=True)
class HeadApp:
    word: Word
    args: tuple[Any, ...]

    def to_wire(self) -> str:
        return f"{self.word.to_wire()}({','.join(a.to_wire() for a in self.args)})"


@dataclass(frozen=True)
class IncidenceItem:
    src: tuple[Glyph, ...]
    tgt: tuple[Glyph, ...]

    def __post_init__(self) -> None:
        if not self.src or not self.tgt:
            raise MssnCodecError("Incidence group cannot be empty")

    def to_wire(self) -> str:
        s = ",".join(g.to_wire() for g in self.src)
        t = ",".join(g.to_wire() for g in self.tgt)
        return f"[{s}]>[{t}]"


@dataclass(frozen=True)
class Incidence:
    items: tuple[IncidenceItem, ...]

    def __post_init__(self) -> None:
        if not self.items:
            raise MssnCodecError("Incidence items cannot be empty")

    def to_wire(self) -> str:
        return ";".join(it.to_wire() for it in self.items)


@dataclass(frozen=True)
class UnicodePath:
    head: str
    steps: tuple[tuple[str, str], ...]  # (dir, glyph)

    def __post_init__(self) -> None:
        glyphs = {"α", "β", "γ", "□", "●", "𓀀", "𓂀", "👩‍💻"}
        if self.head not in glyphs or any(
            d not in ("→", "←") or g not in glyphs for d, g in self.steps
        ):
            raise MssnCodecError("Unicode path uses an undeclared glyph or direction")

    def to_wire(self) -> str:
        return self.head + "".join(d + g for d, g in self.steps)


@dataclass(frozen=True)
class ArrowPath:
    head: Glyph
    steps: tuple[tuple[str, Glyph], ...]

    def to_wire(self) -> str:
        return self.head.to_wire() + "".join(d + g.to_wire() for d, g in self.steps)


@dataclass(frozen=True)
class Bitstream:
    bits: str

    def __post_init__(self) -> None:
        if not self.bits or not set(self.bits).issubset({"0", "1"}):
            raise MssnCodecError(f"Bitstream must be non-empty '0' and '1', got {self.bits!r}")

    def to_wire(self) -> str:
        return self.bits


@dataclass(frozen=True)
class Octets:
    hex_str: str

    def __post_init__(self) -> None:
        if len(self.hex_str) < 2 or len(self.hex_str) % 2 != 0:
            raise MssnCodecError(f"Octets must be even length >= 2, got {self.hex_str!r}")
        if not all(c in "0123456789abcdef" for c in self.hex_str):
            raise MssnCodecError(f"Octets must be lowercase hex, got {self.hex_str!r}")

    def to_wire(self) -> str:
        return self.hex_str


@dataclass(frozen=True)
class RewriteRule:
    lhs: tuple[Glyph, ...]
    rhs: tuple[Glyph, ...]

    def to_wire(self) -> str:
        return (
            "".join(g.to_wire() for g in self.lhs) + "=>" + "".join(g.to_wire() for g in self.rhs)
        )


# ---------------------------------------------------------------------------
# Serializer (AST -> Wire Encoding)
# ---------------------------------------------------------------------------


def serialize_mssn(node: Any) -> str:
    """Serialize a public-profile AST, refusing malformed direct constructions.

    ``to_wire`` methods only render fields. This checked entry point additionally
    parses their output under the node's own profile; it never normalizes it.
    """
    profiles = {
        RawGlyphs: "raw_glyphs", Word: "word", GlyphPath: "glyph_path",
        LabelPath: "label_path", SuffixPath: "suffix_path", PathList: "path_list",
        SuffixList: "suffix_list", ScalarPath: "scalar_path", VectorPath: "vector_path",
        EdgeWeightPath: "edge_weight_path", LabelledPath: "labelled_path",
        PrefixLeaf: "prefix_tree", PrefixBranch: "prefix_tree", PostfixTree: "postfix_tree",
        Sequence: "sequence", NestedLeaf: "nested_tree", NestedGroup: "nested_tree",
        HeadAtom: "head_term", HeadApp: "head_term", Incidence: "incidence",
        UnicodePath: "unicode_path", ArrowPath: "arrow_path", Bitstream: "bitstream",
        Octets: "octets", RewriteRule: "rewrite_rule",
    }
    profile = profiles.get(type(node))
    if profile is None:
        raise MssnCodecError(f"Unsupported MSS-N node: {type(node)}")
    wire = node.to_wire()
    reconstructed = deserialize_mssn(profile, wire)
    if reconstructed != node:
        raise MssnCodecError(f"AST is not a valid canonical {profile} construction")
    return wire


# ---------------------------------------------------------------------------
# Deserializers for Public Starts
# ---------------------------------------------------------------------------

_SCALAR_RE = re.compile(r"^([+-]?)([0-9]+)(?:([./])([0-9]+))?$")


def parse_scalar(text: str) -> Scalar:
    m = _SCALAR_RE.fullmatch(text)
    if not m:
        raise MssnCodecError(f"Invalid scalar: {text!r}")
    sign = m.group(1) or None
    whole = m.group(2)
    sep = m.group(3)
    frac = m.group(4)
    frac_or_ratio = (sep, frac) if sep and frac else None
    return Scalar(sign=sign, whole=whole, frac_or_ratio=frac_or_ratio)


def parse_prefix_tree(text: str, pos: int = 0) -> tuple[Any, int]:
    if pos >= len(text):
        raise MssnCodecError("Unexpected end in prefix_tree")
    ch = text[pos]
    if ch in (">", "<"):
        left, pos2 = parse_prefix_tree(text, pos + 1)
        right, pos3 = parse_prefix_tree(text, pos2)
        return PrefixBranch(dir=ch, left=left, right=right), pos3
    if ch in "abcdefghijklmnopqrstuvwxyz0123456789":
        return PrefixLeaf(glyph=Glyph(ch)), pos + 1
    raise MssnCodecError(f"Unexpected token in prefix tree: {ch!r}")


def parse_postfix_tree(text: str, pos: int = 0) -> tuple[PostfixTree, int]:
    if pos >= len(text):
        raise MssnCodecError("Unexpected end in postfix_tree")
    ch = text[pos]
    if not (ch in "abcdefghijklmnopqrstuvwxyz0123456789"):
        raise MssnCodecError(f"Expected glyph at {pos}, got {ch!r}")
    head = Glyph(ch)
    pos += 1
    steps = []
    while pos < len(text) and (
        text[pos] in "abcdefghijklmnopqrstuvwxyz0123456789"
    ):
        saved = pos
        try:
            child, p2 = parse_postfix_tree(text, pos)
            if p2 < len(text) and text[p2] in (">", "<"):
                steps.append((child, text[p2]))
                pos = p2 + 1
            else:
                pos = saved
                break
        except MssnCodecError:
            pos = saved
            break
    return PostfixTree(head=head, steps=tuple(steps)), pos


def parse_nested_tree(text: str, pos: int = 0) -> tuple[Any, int]:
    if pos >= len(text):
        raise MssnCodecError("Unexpected end in nested_tree")
    if text[pos] == "(":
        pos += 1
        if pos < len(text) and text[pos] == ")":
            return NestedGroup(children=()), pos + 1
        children = []
        child, pos = parse_nested_tree(text, pos)
        children.append(child)
        while pos < len(text) and text[pos] == ",":
            pos += 1
            child, pos = parse_nested_tree(text, pos)
            children.append(child)
        if pos >= len(text) or text[pos] != ")":
            raise MssnCodecError(f"Expected ')' in nested_tree at {pos}")
        return NestedGroup(children=tuple(children)), pos + 1
    ch = text[pos]
    if ch in "abcdefghijklmnopqrstuvwxyz0123456789":
        return NestedLeaf(glyph=Glyph(ch)), pos + 1
    raise MssnCodecError(f"Unexpected token in nested tree: {ch!r}")


def parse_head_term(text: str, pos: int = 0) -> tuple[Any, int]:
    # word start
    start = pos
    while pos < len(text) and (
        text[pos] in "abcdefghijklmnopqrstuvwxyz0123456789"
    ):
        pos += 1
    if pos == start:
        raise MssnCodecError(f"Expected word at {pos}")
    w = Word(chars=tuple(Glyph(c) for c in text[start:pos]))
    if pos < len(text) and text[pos] == "(":
        pos += 1
        if pos < len(text) and text[pos] == ")":
            return HeadApp(word=w, args=()), pos + 1
        args = []
        arg, pos = parse_head_term(text, pos)
        args.append(arg)
        while pos < len(text) and text[pos] == ",":
            pos += 1
            arg, pos = parse_head_term(text, pos)
            args.append(arg)
        if pos >= len(text) or text[pos] != ")":
            raise MssnCodecError(f"Expected ')' at {pos}")
        return HeadApp(word=w, args=tuple(args)), pos + 1
    return HeadAtom(word=w), pos


def deserialize_mssn(start: str, wire: str) -> Any:
    """Deserialize a wire string according to a declared MSS-N start profile."""
    if not isinstance(wire, str):
        raise MssnCodecError(f"Expected string, got {type(wire)}")

    if start == "raw_glyphs":
        return RawGlyphs(wire)

    if start == "word":
        if not wire:
            raise MssnCodecError("Empty word rejected")
        return Word(chars=tuple(Glyph(c) for c in wire))

    if start == "glyph_path":
        parts = re.split(r"([><])", wire)
        if len(parts) % 2 != 1:
            raise MssnCodecError(f"Invalid glyph path: {wire!r}")
        head = Glyph(parts[0])
        steps = []
        for i in range(1, len(parts), 2):
            steps.append((parts[i], Glyph(parts[i + 1])))
        return GlyphPath(head=head, steps=tuple(steps))

    if start == "label_path":
        parts = re.split(r"([><])", wire)
        if len(parts) % 2 != 1:
            raise MssnCodecError(f"Invalid label path: {wire!r}")
        head = Word(chars=tuple(Glyph(c) for c in parts[0]))
        steps = []
        for i in range(1, len(parts), 2):
            w = Word(chars=tuple(Glyph(c) for c in parts[i + 1]))
            steps.append((parts[i], w))
        return LabelPath(head=head, steps=tuple(steps))

    if start == "suffix_path":
        parts = re.split(r"([><])", wire)
        if len(parts) % 2 != 1:
            raise MssnCodecError(f"Invalid suffix path: {wire!r}")

        def parse_sv(s: str) -> SuffixVertex:
            m = re.fullmatch(r"([a-z])([0-9]+)", s)
            if not m:
                raise MssnCodecError(f"Invalid suffix vertex: {s!r}")
            return SuffixVertex(label=m.group(1), digits=m.group(2))

        head = parse_sv(parts[0])
        steps = [(parts[i], parse_sv(parts[i + 1])) for i in range(1, len(parts), 2)]
        return SuffixPath(head=head, steps=tuple(steps))

    if start == "path_list":
        segments = wire.split(";")
        return PathList(paths=tuple(deserialize_mssn("glyph_path", s) for s in segments))

    if start == "suffix_list":
        segments = wire.split(";")
        return SuffixList(paths=tuple(deserialize_mssn("suffix_path", s) for s in segments))

    if start == "scalar_path":
        parts = re.split(r"([><])", wire)
        if len(parts) % 2 != 1:
            raise MssnCodecError(f"Invalid scalar path: {wire!r}")

        def parse_scv(s: str) -> ScalarVertex:
            idx = s.find(":")
            if idx == -1:
                raise MssnCodecError(f"Expected ':' in scalar vertex: {s!r}")
            label = s[:idx]
            sc = parse_scalar(s[idx + 1 :])
            return ScalarVertex(label=label, scalar=sc)

        head = parse_scv(parts[0])
        steps = [(parts[i], parse_scv(parts[i + 1])) for i in range(1, len(parts), 2)]
        return ScalarPath(head=head, steps=tuple(steps))

    if start == "vector_path":
        parts = re.split(r"([><])", wire)
        if len(parts) % 2 != 1:
            raise MssnCodecError(f"Invalid vector path: {wire!r}")

        def parse_vv(s: str) -> VectorVertex:
            m = re.fullmatch(r"([a-z])\[(.*)\]", s)
            if not m:
                raise MssnCodecError(f"Invalid vector vertex: {s!r}")
            label = m.group(1)
            raw_coords = m.group(2).split(",")
            coords = tuple(parse_scalar(c) for c in raw_coords)
            return VectorVertex(label=label, coords=coords)

        head = parse_vv(parts[0])
        steps = [(parts[i], parse_vv(parts[i + 1])) for i in range(1, len(parts), 2)]
        return VectorPath(head=head, steps=tuple(steps))

    if start == "edge_weight_path":
        m = re.fullmatch(r"([a-z])((?:[><][^><]+[><][a-z])*)", wire)
        if not m:
            raise MssnCodecError(f"Invalid edge weight path: {wire!r}")
        head = m.group(1)
        rest = m.group(2)
        step_matches = re.findall(r"([><])([^><]+)([><])([a-z])", rest)
        steps = []
        for d1, sc_str, d2, lat in step_matches:
            if d1 != d2:
                raise MssnCodecError(f"Mismatched link directions: {d1} != {d2}")
            steps.append((d1, parse_scalar(sc_str), lat))
        # Ensure full string was consumed
        reconstructed = head + "".join(f"{d}{w.to_wire()}{d}{lat}" for d, w, lat in steps)
        if reconstructed != wire:
            raise MssnCodecError(f"Failed to fully parse edge weight path: {wire!r}")
        return EdgeWeightPath(head=head, steps=tuple(steps))

    if start == "labelled_path":
        m = re.fullmatch(r"([a-z])((?:-[a-z0-9]+>[a-z])*)", wire)
        if not m:
            raise MssnCodecError(f"Invalid labelled path: {wire!r}")
        head = m.group(1)
        rest = m.group(2)
        step_matches = re.findall(r"-([a-z0-9]+)>([a-z])", rest)
        steps = [(Word(tuple(Glyph(c) for c in w)), lat) for w, lat in step_matches]
        return LabelledPath(head=head, steps=tuple(steps))

    if start == "prefix_tree":
        tree, consumed = parse_prefix_tree(wire, 0)
        if consumed != len(wire):
            raise MssnCodecError(f"Unconsumed tokens in prefix tree: {wire[consumed:]!r}")
        return tree

    if start == "postfix_tree":
        tree, consumed = parse_postfix_tree(wire, 0)
        if consumed != len(wire):
            raise MssnCodecError(f"Unconsumed tokens in postfix tree: {wire[consumed:]!r}")
        return tree

    if start == "sequence":
        parts = wire.split(",")
        return Sequence(glyphs=tuple(Glyph(p) for p in parts))

    if start == "nested_tree":
        tree, consumed = parse_nested_tree(wire, 0)
        if consumed != len(wire):
            raise MssnCodecError(f"Unconsumed tokens in nested tree: {wire[consumed:]!r}")
        return tree

    if start == "head_term":
        term, consumed = parse_head_term(wire, 0)
        if consumed != len(wire):
            raise MssnCodecError(f"Unconsumed tokens in head term: {wire[consumed:]!r}")
        return term

    if start == "incidence":
        items = []
        for segment in wire.split(";"):
            m = re.fullmatch(r"\[([a-z0-9](?:,[a-z0-9])*)\]>\[([a-z0-9](?:,[a-z0-9])*)\]", segment)
            if not m:
                raise MssnCodecError(f"Invalid incidence item: {segment!r}")
            src = tuple(Glyph(c) for c in m.group(1).split(","))
            tgt = tuple(Glyph(c) for c in m.group(2).split(","))
            items.append(IncidenceItem(src=src, tgt=tgt))
        return Incidence(items=tuple(items))

    if start == "unicode_path":
        parts = re.split(r"([→←])", wire)
        if len(parts) % 2 != 1:
            raise MssnCodecError(f"Invalid unicode path: {wire!r}")
        head = parts[0]
        steps = [(parts[i], parts[i + 1]) for i in range(1, len(parts), 2)]
        return UnicodePath(head=head, steps=tuple(steps))

    if start == "arrow_path":
        parts = re.split(r"([→←])", wire)
        if len(parts) % 2 != 1:
            raise MssnCodecError(f"Invalid arrow path: {wire!r}")
        head = Glyph(parts[0])
        steps = [(parts[i], Glyph(parts[i + 1])) for i in range(1, len(parts), 2)]
        return ArrowPath(head=head, steps=tuple(steps))

    if start == "bitstream":
        return Bitstream(bits=wire)

    if start == "octets":
        return Octets(hex_str=wire)

    if start == "rewrite_rule":
        if "=>" not in wire:
            raise MssnCodecError(f"Expected '=>' in rewrite rule: {wire!r}")
        lhs_str, rhs_str = wire.split("=>", 1)
        lhs = tuple(Glyph(c) for c in lhs_str)
        rhs = tuple(Glyph(c) for c in rhs_str)
        return RewriteRule(lhs=lhs, rhs=rhs)

    raise MssnCodecError(f"Unsupported MSS-N start profile: {start!r}")
