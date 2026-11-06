"""Round-trip tests for the Python AST and EBNF recognizer (no Lean invocation).

AuthorityEffect: None. GenesisEffect: None.
Verifies that:
1. AST -> serialize_sn -> deserialize_sn == AST (Lossless AST round-trip).
2. Canonical wire -> deserialize_sn -> serialize_sn == wire; numeric leading zeroes normalize.
3. The well-typed sampled ASTs conform to sn.ebnf grammar recognizer.
4. Typed refusals reject ill-formed wire tokens.
"""

from __future__ import annotations

import json
import random
import string
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
CODE_DIR = HERE.parent
REPO = HERE.parents[4]
SN_EBNF_PATH = REPO / "omega_engine_education" / "documentation" / "002_s_n" / "grammar" / "sn.ebnf"
GRAMMAR_DIR = (
    REPO
    / "omega_engine_education"
    / "documentation"
    / "030_the_symbol_game_proposal_fidelity_protocol_pfp"
    / "grammar"
)
if not GRAMMAR_DIR.is_dir():
    GRAMMAR_DIR = REPO / "ow" / "omega_engine_pfp_v0.2" / "grammar"

sys.path.insert(0, str(CODE_DIR))
sys.path.insert(0, str(GRAMMAR_DIR))

from check_grammars import Grammar
from sn_codec import (
    DirectedCut,
    Glyph,
    GroundToken,
    InnerBody,
    InnerBodyArrow,
    InnerBodyGlyphs,
    InnerBodyPair,
    NonDescent,
    RetainedPair,
    RetractionMap,
    SectionLift,
    SimplexCut,
    SnCodecError,
    SnNode,
    SuppliedToken,
    deserialize_sn,
    serialize_sn,
)


@pytest.fixture(scope="module")
def sn_grammar() -> Grammar:
    ebnf = SN_EBNF_PATH.read_text(encoding="utf-8")
    return Grammar(ebnf)


# ---------------------------------------------------------------------------
# 1. Deterministic Unit & Conformance Tests
# ---------------------------------------------------------------------------


def test_ground_roundtrip(sn_grammar: Grammar):
    ast = GroundToken()
    wire = serialize_sn(ast)
    assert wire == "<>"
    assert sn_grammar.accepts("sn_presentation", wire)
    assert deserialize_sn(wire) == ast


def test_supplied_roundtrip(sn_grammar: Grammar):
    for ch in ["a", "z", "0", "9"]:
        ast = SuppliedToken(mark=Glyph(ch))
        wire = serialize_sn(ast)
        assert wire == f"<{ch}>"
        assert sn_grammar.accepts("sn_presentation", wire)
        assert deserialize_sn(wire) == ast


def test_retained_pair_roundtrip(sn_grammar: Grammar):
    ast = RetainedPair(first=Glyph("a"), second=Glyph("b"))
    wire = serialize_sn(ast)
    assert wire == "<ab>"
    assert sn_grammar.accepts("sn_presentation", wire)
    assert deserialize_sn(wire) == ast


def test_directed_cut_roundtrip(sn_grammar: Grammar):
    ast = DirectedCut(src=Glyph("a"), tgt=Glyph("b"))
    wire = serialize_sn(ast)
    assert wire == "<a->b>"
    assert sn_grammar.accepts("sn_presentation", wire)
    assert deserialize_sn(wire) == ast


def test_simplex_cut_roundtrip(sn_grammar: Grammar):
    ast = SimplexCut(v0=Glyph("a"), v1=Glyph("b"))
    wire = serialize_sn(ast)
    assert wire == "[a,b]"
    assert sn_grammar.accepts("sn_presentation", wire)
    assert deserialize_sn(wire) == ast


def test_section_lift_roundtrip(sn_grammar: Grammar):
    bodies = [
        InnerBodyArrow(src=Glyph("a"), tgt=Glyph("b")),
        InnerBodyPair(first=Glyph("x"), second=Glyph("y")),
        InnerBodyGlyphs(glyphs=()),
        InnerBodyGlyphs(glyphs=(Glyph("a"),)),
        InnerBodyGlyphs(glyphs=(Glyph("a"), Glyph("b"), Glyph("c"))),
    ]
    for stage in [0, 1, 6, 42]:
        for b in bodies:
            ast = SectionLift(stage=stage, body=b)
            wire = serialize_sn(ast)
            assert sn_grammar.accepts("sn_presentation", wire)
            assert deserialize_sn(wire) == ast


def test_retraction_map_roundtrip(sn_grammar: Grammar):
    bodies = [
        InnerBodyArrow(src=Glyph("c"), tgt=Glyph("d")),
        InnerBodyPair(first=Glyph("0"), second=Glyph("1")),
        InnerBodyGlyphs(glyphs=()),
        InnerBodyGlyphs(glyphs=(Glyph("z"),)),
    ]
    for stage in [0, 1, 3, 10]:
        for b in bodies:
            ast = RetractionMap(stage=stage, body=b)
            wire = serialize_sn(ast)
            assert sn_grammar.accepts("sn_presentation", wire)
            assert deserialize_sn(wire) == ast


def test_nondescent_roundtrip(sn_grammar: Grammar):
    ast = NonDescent()
    wire = serialize_sn(ast)
    assert wire == "NON_DESCENT"
    assert sn_grammar.accepts("sn_presentation", wire)
    assert deserialize_sn(wire) == ast


# ---------------------------------------------------------------------------
# 2. Conformance JSON Cases Validation
# ---------------------------------------------------------------------------


def test_conformance_cases_roundtrip(sn_grammar: Grammar):
    cases_path = CODE_DIR.parent / "grammar" / "sn_conformance_cases.json"
    cases = json.loads(cases_path.read_text(encoding="utf-8"))

    for c in cases:
        if c["start"] == "sn_presentation":
            text = c["text"]
            if c["accept"]:
                ast = deserialize_sn(text)
                wire = serialize_sn(ast)
                assert wire == text
                assert sn_grammar.accepts("sn_presentation", wire)
            else:
                with pytest.raises(SnCodecError):
                    deserialize_sn(text)


# ---------------------------------------------------------------------------
# 3. Generative Property Tests (Randomized Invariant Sampling)
# ---------------------------------------------------------------------------

VALID_CHARS = string.ascii_lowercase + string.digits


def _random_glyph(rng: random.Random) -> Glyph:
    return Glyph(rng.choice(VALID_CHARS))


def _random_inner_body(rng: random.Random) -> InnerBody:
    choice = rng.randint(0, 2)
    if choice == 0:
        return InnerBodyArrow(src=_random_glyph(rng), tgt=_random_glyph(rng))
    if choice == 1:
        return InnerBodyPair(first=_random_glyph(rng), second=_random_glyph(rng))
    k = rng.randint(0, 5)
    return InnerBodyGlyphs(glyphs=tuple(_random_glyph(rng) for _ in range(k)))


def _random_ast(rng: random.Random) -> SnNode:
    tag = rng.randint(0, 7)
    if tag == 0:
        return GroundToken()
    if tag == 1:
        return SuppliedToken(mark=_random_glyph(rng))
    if tag == 2:
        return RetainedPair(first=_random_glyph(rng), second=_random_glyph(rng))
    if tag == 3:
        return DirectedCut(src=_random_glyph(rng), tgt=_random_glyph(rng))
    if tag == 4:
        return SimplexCut(v0=_random_glyph(rng), v1=_random_glyph(rng))
    if tag == 5:
        return SectionLift(stage=rng.randint(0, 20), body=_random_inner_body(rng))
    if tag == 6:
        return RetractionMap(stage=rng.randint(0, 20), body=_random_inner_body(rng))
    return NonDescent()


def test_generative_property_roundtrip(sn_grammar: Grammar):
    """For the seeded generated sample, deserialize(serialize(ast)) == ast and grammar accepts."""
    rng = random.Random(20261005)
    for _ in range(200):
        ast = _random_ast(rng)
        wire = serialize_sn(ast)
        # 1. Grammar accepts
        assert sn_grammar.accepts("sn_presentation", wire), f"Grammar rejected wire: {wire}"
        # 2. Deserialization produces identical AST
        recovered = deserialize_sn(wire)
        assert recovered == ast, f"AST mismatch for {wire}: {recovered} != {ast}"
        # 3. Double serialization stability
        assert serialize_sn(recovered) == wire


# ---------------------------------------------------------------------------
# 4. Negative / Refusal Tests
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "bad_wire",
    [
        "",
        "   ",
        "<",
        ">",
        "<abc>",
        "<a->>",
        "<->b>",
        "[a]",
        "[a,b,c]",
        "u_<abc>",
        "u_-1<a>",
        "r_<a>",
        "NON_DESCENT_EXTRA",
        "Op<1>",
        "<A>",
        "<a-b>",
    ],
)
def test_codec_refusals(bad_wire: str):
    with pytest.raises(SnCodecError):
        deserialize_sn(bad_wire)


@pytest.mark.parametrize("bad_wire", ["<١>", "<²>", "u_١<a>", "r_１<a>", "u_1<١>"])
def test_codec_rejects_unicode_digits_outside_the_ascii_grammar(bad_wire):
    with pytest.raises(SnCodecError):
        deserialize_sn(bad_wire)


@pytest.mark.parametrize("stage", [True, 1.5, "1", -1])
def test_stage_requires_an_actual_nonnegative_integer(stage):
    with pytest.raises(SnCodecError):
        SectionLift(stage, InnerBodyGlyphs(()))
