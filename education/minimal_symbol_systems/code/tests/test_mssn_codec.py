"""Targeted round-trip and refusal tests against the independent EBNF recognizer.

AuthorityEffect: None. GenesisEffect: None.
Verifies that:
1. AST -> serialize_mssn -> deserialize_mssn == AST (Lossless AST round-trip).
2. Wire -> deserialize_mssn -> serialize_mssn == Wire (Lossless wire round-trip).
3. Every serialized AST conforms strictly to mssn.ebnf grammar recognizer.
4. Typed refusals reject ill-formed wire tokens.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
CODE_DIR = HERE.parent
REPO = HERE.parents[4]
MSSN_EBNF_PATH = (
    REPO
    / "omega_engine_education"
    / "documentation"
    / "003_minimal_symbol_system_n_mssn"
    / "grammar"
    / "mssn.ebnf"
)
GRAMMAR_DIR = (
    REPO
    / "omega_engine_education"
    / "documentation"
    / "030_the_symbol_game_proposal_fidelity_protocol_pfp"
    / "grammar"
)

sys.path.insert(0, str(CODE_DIR))
sys.path.insert(0, str(GRAMMAR_DIR))

from check_grammars import Grammar
from mssn_codec import (
    Bitstream,
    EdgeWeightPath,
    Glyph,
    GlyphPath,
    HeadApp,
    HeadAtom,
    Incidence,
    IncidenceItem,
    MssnCodecError,
    NestedGroup,
    NestedLeaf,
    Octets,
    PostfixTree,
    PrefixBranch,
    PrefixLeaf,
    RewriteRule,
    Scalar,
    ScalarPath,
    ScalarVertex,
    SuffixPath,
    SuffixVertex,
    VectorPath,
    VectorVertex,
    Word,
    deserialize_mssn,
    serialize_mssn,
)


@pytest.fixture(scope="module")
def mssn_grammar() -> Grammar:
    ebnf = MSSN_EBNF_PATH.read_text(encoding="utf-8")
    return Grammar(ebnf)


# ---------------------------------------------------------------------------
# 1. Conformance Cases Round-Trip
# ---------------------------------------------------------------------------


def test_mssn_conformance_cases_roundtrip(mssn_grammar: Grammar):
    cases_path = CODE_DIR.parent / "grammar" / "mssn_conformance_cases.json"
    cases = json.loads(cases_path.read_text(encoding="utf-8"))

    # Every public start has a codec representation, including raw inscriptions.
    ast_starts = {
        "raw_glyphs",
        "word",
        "glyph_path",
        "label_path",
        "suffix_path",
        "path_list",
        "suffix_list",
        "scalar_path",
        "vector_path",
        "edge_weight_path",
        "labelled_path",
        "prefix_tree",
        "postfix_tree",
        "sequence",
        "nested_tree",
        "head_term",
        "incidence",
        "unicode_path",
        "arrow_path",
        "bitstream",
        "octets",
        "rewrite_rule",
    }

    for c in cases:
        start = c["start"]
        if start not in ast_starts:
            continue
        text = c["text"]
        accept = c["accept"]

        if accept:
            ast = deserialize_mssn(start, text)
            wire = serialize_mssn(ast)
            assert wire == text
            assert mssn_grammar.accepts(start, wire)
        else:
            with pytest.raises(MssnCodecError):
                deserialize_mssn(start, text)


# ---------------------------------------------------------------------------
# 2. Detailed AST Profile Round-Trips
# ---------------------------------------------------------------------------


def test_word_profile(mssn_grammar: Grammar):
    ast = Word(chars=(Glyph("h"), Glyph("e"), Glyph("l"), Glyph("l"), Glyph("o")))
    wire = serialize_mssn(ast)
    assert wire == "hello"
    assert mssn_grammar.accepts("word", wire)
    assert deserialize_mssn("word", wire) == ast


def test_glyph_path_profile(mssn_grammar: Grammar):
    ast = GlyphPath(head=Glyph("a"), steps=((">", Glyph("b")), ("<", Glyph("c"))))
    wire = serialize_mssn(ast)
    assert wire == "a>b<c"
    assert mssn_grammar.accepts("glyph_path", wire)
    assert deserialize_mssn("glyph_path", wire) == ast


def test_suffix_profile(mssn_grammar: Grammar):
    ast = SuffixPath(
        head=SuffixVertex("a", "0"),
        steps=((">", SuffixVertex("b", "12")), ("<", SuffixVertex("c", "3"))),
    )
    wire = serialize_mssn(ast)
    assert wire == "a0>b12<c3"
    assert mssn_grammar.accepts("suffix_path", wire)
    assert deserialize_mssn("suffix_path", wire) == ast


def test_scalar_profile(mssn_grammar: Grammar):
    ast = ScalarPath(
        head=ScalarVertex("a", Scalar(sign="+", whole="1", frac_or_ratio=(".", "5"))),
        steps=((">", ScalarVertex("b", Scalar(sign="-", whole="2", frac_or_ratio=("/", "3")))),),
    )
    wire = serialize_mssn(ast)
    assert wire == "a:+1.5>b:-2/3"
    assert mssn_grammar.accepts("scalar_path", wire)
    assert deserialize_mssn("scalar_path", wire) == ast


def test_vector_profile(mssn_grammar: Grammar):
    ast = VectorPath(
        head=VectorVertex("a", (Scalar(None, "1", None), Scalar(None, "2", None))),
        steps=((">", VectorVertex("b", (Scalar(None, "3", None), Scalar(None, "4", None)))),),
    )
    wire = serialize_mssn(ast)
    assert wire == "a[1,2]>b[3,4]"
    assert mssn_grammar.accepts("vector_path", wire)
    assert deserialize_mssn("vector_path", wire) == ast


def test_edge_weight_profile(mssn_grammar: Grammar):
    ast = EdgeWeightPath(
        head="a",
        steps=((">", Scalar(None, "2", (".", "5")), "b"), ("<", Scalar(None, "1", None), "c")),
    )
    wire = serialize_mssn(ast)
    assert wire == "a>2.5>b<1<c"
    assert mssn_grammar.accepts("edge_weight_path", wire)
    assert deserialize_mssn("edge_weight_path", wire) == ast


def test_trees_profile(mssn_grammar: Grammar):
    # Prefix tree: >ab
    ast_p = PrefixBranch(">", PrefixLeaf(Glyph("a")), PrefixLeaf(Glyph("b")))
    wire_p = serialize_mssn(ast_p)
    assert wire_p == ">ab"
    assert mssn_grammar.accepts("prefix_tree", wire_p)
    assert deserialize_mssn("prefix_tree", wire_p) == ast_p

    # Postfix tree: ab>
    ast_post = PostfixTree(head=Glyph("a"), steps=((PostfixTree(head=Glyph("b"), steps=()), ">"),))
    wire_post = serialize_mssn(ast_post)
    assert wire_post == "ab>"
    assert mssn_grammar.accepts("postfix_tree", wire_post)
    assert deserialize_mssn("postfix_tree", wire_post) == ast_post

    # Nested tree: (a,(b,c))
    ast_n = NestedGroup(
        (
            NestedLeaf(Glyph("a")),
            NestedGroup((NestedLeaf(Glyph("b")), NestedLeaf(Glyph("c")))),
        )
    )
    wire_n = serialize_mssn(ast_n)
    assert wire_n == "(a,(b,c))"
    assert mssn_grammar.accepts("nested_tree", wire_n)
    assert deserialize_mssn("nested_tree", wire_n) == ast_n


def test_head_term_profile(mssn_grammar: Grammar):
    # f(x,g(y))
    ast = HeadApp(
        word=Word((Glyph("f"),)),
        args=(
            HeadAtom(Word((Glyph("x"),))),
            HeadApp(word=Word((Glyph("g"),)), args=(HeadAtom(Word((Glyph("y"),))),)),
        ),
    )
    wire = serialize_mssn(ast)
    assert wire == "f(x,g(y))"
    assert mssn_grammar.accepts("head_term", wire)
    assert deserialize_mssn("head_term", wire) == ast


def test_incidence_profile(mssn_grammar: Grammar):
    ast = Incidence((IncidenceItem(src=(Glyph("a"), Glyph("b")), tgt=(Glyph("c"), Glyph("d"))),))
    wire = serialize_mssn(ast)
    assert wire == "[a,b]>[c,d]"
    assert mssn_grammar.accepts("incidence", wire)
    assert deserialize_mssn("incidence", wire) == ast


def test_bitstream_and_octets_profile(mssn_grammar: Grammar):
    bs = Bitstream("10011010")
    wire_bs = serialize_mssn(bs)
    assert mssn_grammar.accepts("bitstream", wire_bs)
    assert deserialize_mssn("bitstream", wire_bs) == bs

    oc = Octets("deadbeef")
    wire_oc = serialize_mssn(oc)
    assert mssn_grammar.accepts("octets", wire_oc)
    assert deserialize_mssn("octets", wire_oc) == oc


def test_rewrite_rule_profile(mssn_grammar: Grammar):
    rule = RewriteRule(lhs=(Glyph("a"),), rhs=(Glyph("b"),))
    wire_r = serialize_mssn(rule)
    assert wire_r == "a=>b"
    assert mssn_grammar.accepts("rewrite_rule", wire_r)
    assert deserialize_mssn("rewrite_rule", wire_r) == rule


@pytest.mark.parametrize("digit", ["²", "٢", "９"])
@pytest.mark.parametrize("start,template", [
    ("word", "a{}"), ("glyph_path", "a>{}"),
    ("suffix_path", "a{}"), ("scalar_path", "a:{}"),
    ("vector_path", "a[{}]"), ("prefix_tree", ">a{}"),
    ("postfix_tree", "a{}>"), ("nested_tree", "(a,{})"),
    ("head_term", "f({})"), ("rewrite_rule", "a=>{}"),
])
def test_ascii_grammar_refuses_unicode_digits(mssn_grammar, digit, start, template):
    wire = template.format(digit)
    assert not mssn_grammar.accepts(start, wire)
    with pytest.raises(MssnCodecError):
        deserialize_mssn(start, wire)


@pytest.mark.parametrize("wire", ["", "a", "αβ", "α→", "👩💻", "α→🙂", "α\n"])
def test_unicode_profile_refuses_undeclared_tokens(mssn_grammar, wire):
    assert not mssn_grammar.accepts("unicode_path", wire)
    with pytest.raises(MssnCodecError):
        deserialize_mssn("unicode_path", wire)


@pytest.mark.parametrize("wire", ["α", "α→β←👩‍💻", "𓀀→𓂀", "□←●"])
def test_declared_unicode_tokens_roundtrip(mssn_grammar, wire):
    assert mssn_grammar.accepts("unicode_path", wire)
    assert serialize_mssn(deserialize_mssn("unicode_path", wire)) == wire


@pytest.mark.parametrize("wire", ["", "<>", "a0><z", "<<<"])
def test_raw_glyphs_roundtrip(mssn_grammar, wire):
    assert mssn_grammar.accepts("raw_glyphs", wire)
    assert serialize_mssn(deserialize_mssn("raw_glyphs", wire)) == wire


def test_serializer_refuses_invalid_ast_direction():
    malformed = GlyphPath(Glyph("a"), (("=", Glyph("b")),))
    with pytest.raises(MssnCodecError):
        serialize_mssn(malformed)


@pytest.mark.parametrize("wire", ["ab>c>", "abc>>", "ab>cd><", "abcd><>"])
def test_postfix_branch_structure_roundtrip(mssn_grammar, wire):
    assert mssn_grammar.accepts("postfix_tree", wire)
    ast = deserialize_mssn("postfix_tree", wire)
    assert serialize_mssn(ast) == wire
    assert deserialize_mssn("postfix_tree", serialize_mssn(ast)) == ast
