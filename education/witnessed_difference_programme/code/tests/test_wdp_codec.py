"""Round-trip property tests linking wdp.ebnf AST outputs directly to wire encodings.

AuthorityEffect: None. GenesisEffect: None.
Verifies that:
1. AST -> serialize_wdp -> deserialize_wdp == AST (Lossless AST round-trip).
2. Wire -> deserialize_wdp -> serialize_wdp == Wire (Lossless wire round-trip).
3. Every serialized AST conforms strictly to wdp.ebnf grammar recognizer under "wdp_statement".
4. Conformance cases in wdp_conformance_cases.json deserialize and round-trip or reject cleanly.
5. Generative randomized AST invariant sampling demonstrates round-trip fidelity.
6. Typed refusals reject ill-formed wire tokens.
"""

from __future__ import annotations

import json
import random
import string
import sys
from pathlib import Path

import pytest

MODULE_ROOT = next(
    (
        p
        for p in Path(__file__).resolve().parents
        if (p / "levels").is_dir() or (p / "grammar").is_dir()
    ),
    Path(__file__).resolve().parents[2],
)
REPO_ROOT = next(
    (
        p
        for p in Path(__file__).resolve().parents
        if (p / ".git").exists() or (p / "pixi.toml").exists()
    ),
    Path(__file__).resolve().parents[5],
)
CODE_DIR = MODULE_ROOT / "code"
WDP_EBNF_PATH = MODULE_ROOT / "grammar" / "wdp.ebnf"
CASES_PATH = MODULE_ROOT / "grammar" / "wdp_conformance_cases.json"
GRAMMAR_DIR = next(
    (
        p
        for p in (
            REPO_ROOT / "omega_engine_education" / "documentation" / "004_oepfp" / "grammar",
            REPO_ROOT / "omega_engine_education" / "documentation" / "030_the_symbol_game_proposal_fidelity_protocol_pfp" / "grammar",
            REPO_ROOT / "ow" / "omega_engine_pfp_v0.2" / "grammar",
        )
        if p.is_dir()
    ),
    REPO_ROOT / "omega_engine_education" / "documentation" / "004_oepfp" / "grammar",
)

sys.path.insert(0, str(CODE_DIR))
sys.path.insert(0, str(GRAMMAR_DIR))

from check_grammars import Grammar
from wdp_codec import (
    REFUSAL_CODES,
    WITNESS_STATUSES,
    BalanceMatrix,
    D0Map,
    D1Map,
    DistinctCut,
    Glyph,
    HHomotopy,
    MarkedQuotient,
    QuotientWitness,
    SimplexPair,
    WdpCodecError,
    WdpNode,
    WdpRefusal,
    Word,
    deserialize_wdp,
    serialize_wdp,
)


@pytest.fixture(scope="module")
def wdp_grammar() -> Grammar:
    ebnf = WDP_EBNF_PATH.read_text(encoding="utf-8")
    return Grammar(ebnf)


# ---------------------------------------------------------------------------
# 1. Deterministic Unit & Round-Trip Tests by Production
# ---------------------------------------------------------------------------


def test_distinct_cut_roundtrip(wdp_grammar: Grammar):
    for c1, c2 in [("a", "b"), ("x", "y"), ("0", "1"), ("z", "9")]:
        ast = DistinctCut(first=Glyph(c1), second=Glyph(c2))
        wire = serialize_wdp(ast)
        assert wire == f"<{c1}!={c2}>"
        assert wdp_grammar.accepts("wdp_statement", wire)
        assert wdp_grammar.accepts("distinct_cut", wire)
        assert deserialize_wdp(wire) == ast


def test_simplex_pair_roundtrip(wdp_grammar: Grammar):
    for c1, c2 in [("a", "b"), ("u", "v"), ("2", "3")]:
        ast = SimplexPair(first=Glyph(c1), second=Glyph(c2))
        wire = serialize_wdp(ast)
        assert wire == f"<{c1},{c2}>"
        assert wdp_grammar.accepts("wdp_statement", wire)
        assert wdp_grammar.accepts("simplex_pair", wire)
        assert deserialize_wdp(wire) == ast


def test_marked_quotient_roundtrip(wdp_grammar: Grammar):
    for num, fib in [("a", "fiber1"), ("x", "basis0"), ("1", "c123")]:
        ast = MarkedQuotient(numerator=Glyph(num), fiber=Word(fib))
        wire = serialize_wdp(ast)
        assert wire == f"quot<{num}/{fib}>"
        assert wdp_grammar.accepts("wdp_statement", wire)
        assert wdp_grammar.accepts("marked_quotient", wire)
        assert deserialize_wdp(wire) == ast


def test_d0_map_roundtrip(wdp_grammar: Grammar):
    for ch in ["t", "x", "0", "9"]:
        ast = D0Map(target=Glyph(ch))
        wire = serialize_wdp(ast)
        assert wire == f"d0({ch})"
        assert wdp_grammar.accepts("wdp_statement", wire)
        assert wdp_grammar.accepts("d0_map", wire)
        assert deserialize_wdp(wire) == ast


def test_d1_map_roundtrip(wdp_grammar: Grammar):
    for c1, c2 in [("a", "b"), ("x", "y"), ("5", "6")]:
        ast = D1Map(first=Glyph(c1), second=Glyph(c2))
        wire = serialize_wdp(ast)
        assert wire == f"d1({c1},{c2})"
        assert wdp_grammar.accepts("wdp_statement", wire)
        assert wdp_grammar.accepts("d1_map", wire)
        assert deserialize_wdp(wire) == ast


def test_h_homotopy_roundtrip(wdp_grammar: Grammar):
    for c1, c2 in [("a", "b"), ("u", "w"), ("0", "8")]:
        ast = HHomotopy(first=Glyph(c1), second=Glyph(c2))
        wire = serialize_wdp(ast)
        assert wire == f"H({c1},{c2})"
        assert wdp_grammar.accepts("wdp_statement", wire)
        assert wdp_grammar.accepts("h_homotopy", wire)
        assert deserialize_wdp(wire) == ast


def test_quotient_witness_roundtrip(wdp_grammar: Grammar):
    for status in sorted(WITNESS_STATUSES):
        ast = QuotientWitness(fiber=Word("w1"), status=status)
        wire = serialize_wdp(ast)
        assert wire == f"witness<fiber:w1,status:{status}>"
        assert wdp_grammar.accepts("wdp_statement", wire)
        assert wdp_grammar.accepts("quotient_witness", wire)
        assert deserialize_wdp(wire) == ast


def test_balance_matrix_roundtrip(wdp_grammar: Grammar):
    for sites, trace in [(0, 0), (2, 1), (12, 45), (100, 200)]:
        ast = BalanceMatrix(sites=sites, trace=trace)
        wire = serialize_wdp(ast)
        assert wire == f"balance<sites:{sites},trace:{trace}>"
        assert wdp_grammar.accepts("wdp_statement", wire)
        assert wdp_grammar.accepts("balance_matrix", wire)
        assert deserialize_wdp(wire) == ast


def test_refusal_roundtrip(wdp_grammar: Grammar):
    for code in sorted(REFUSAL_CODES):
        ast = WdpRefusal(code=code)
        wire = serialize_wdp(ast)
        assert wire == f"refusal<{code}>"
        assert wdp_grammar.accepts("wdp_statement", wire)
        assert wdp_grammar.accepts("refusal", wire)
        assert deserialize_wdp(wire) == ast


# ---------------------------------------------------------------------------
# 2. Conformance JSON Cases Validation
# ---------------------------------------------------------------------------


def test_conformance_cases_roundtrip(wdp_grammar: Grammar):
    cases = json.loads(CASES_PATH.read_text(encoding="utf-8"))
    for c in cases:
        text = c["text"]
        expected_accept = c["accept"]

        if expected_accept:
            ast = deserialize_wdp(text)
            wire = serialize_wdp(ast)
            assert wire == text
            assert wdp_grammar.accepts("wdp_statement", wire)
        else:
            with pytest.raises(WdpCodecError):
                deserialize_wdp(text)


# ---------------------------------------------------------------------------
# 3. Generative Property Tests (Randomized Invariant Sampling)
# ---------------------------------------------------------------------------

VALID_GLYPHS = string.ascii_lowercase + string.digits


def _random_glyph(rng: random.Random) -> Glyph:
    return Glyph(rng.choice(VALID_GLYPHS))


def _random_word(rng: random.Random, max_len: int = 8) -> Word:
    length = rng.randint(1, max_len)
    return Word("".join(rng.choice(VALID_GLYPHS) for _ in range(length)))


def _random_ast(rng: random.Random) -> WdpNode:
    tag = rng.randint(0, 8)
    if tag == 0:
        return DistinctCut(first=_random_glyph(rng), second=_random_glyph(rng))
    if tag == 1:
        return SimplexPair(first=_random_glyph(rng), second=_random_glyph(rng))
    if tag == 2:
        return MarkedQuotient(numerator=_random_glyph(rng), fiber=_random_word(rng))
    if tag == 3:
        return D0Map(target=_random_glyph(rng))
    if tag == 4:
        return D1Map(first=_random_glyph(rng), second=_random_glyph(rng))
    if tag == 5:
        return HHomotopy(first=_random_glyph(rng), second=_random_glyph(rng))
    if tag == 6:
        status = rng.choice(sorted(WITNESS_STATUSES))
        return QuotientWitness(fiber=_random_word(rng), status=status)
    if tag == 7:
        return BalanceMatrix(sites=rng.randint(0, 50), trace=rng.randint(0, 50))
    code = rng.choice(sorted(REFUSAL_CODES))
    return WdpRefusal(code=code)


def test_generative_property_roundtrip(wdp_grammar: Grammar):
    """Property: for all generated ASTs, deserialize(serialize(ast)) == ast and grammar accepts."""
    rng = random.Random(20261005)
    for _ in range(300):
        ast = _random_ast(rng)
        wire = serialize_wdp(ast)
        # 1. Grammar accepts
        assert wdp_grammar.accepts("wdp_statement", wire), f"Grammar rejected wire: {wire}"
        # 2. Deserialization produces identical AST
        recovered = deserialize_wdp(wire)
        assert recovered == ast, f"AST mismatch for {wire}: {recovered} != {ast}"
        # 3. Double serialization stability
        assert serialize_wdp(recovered) == wire


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
        "<a=b>",
        "<a!=>",
        "<!=b>",
        "<a!=b!=c>",
        "<a,b,c>",
        "<,>",
        "quot<>",
        "quot<a/>",
        "quot</fiber>",
        "quot<ab/fiber>",
        "d0()",
        "d0(ab)",
        "d1()",
        "d1(a)",
        "d1(a,b,c)",
        "H()",
        "H(a)",
        "H(a,b,c)",
        "witness<fiber:w,status:INVALID_STATUS>",
        "witness<fiber:,status:EXACT_REPAIR>",
        "witness<status:EXACT_REPAIR>",
        "balance<sites:-1,trace:1>",
        "balance<sites:1>",
        "balance<trace:1>",
        "balance<sites:abc,trace:1>",
        "refusal<UNKNOWN_ERROR>",
        "refusal<>",
        "refusal",
        "random_noise",
        "<A!=B>",
        "<X,Y>",
        "d0(Z)",
    ],
)
def test_codec_refusals(bad_wire: str):
    with pytest.raises(WdpCodecError):
        deserialize_wdp(bad_wire)


def test_ast_direct_validation_errors():
    with pytest.raises(WdpCodecError):
        Glyph("ab")
    with pytest.raises(WdpCodecError):
        Glyph("A")
    with pytest.raises(WdpCodecError):
        Glyph("!")
    with pytest.raises(WdpCodecError):
        Word("")
    with pytest.raises(WdpCodecError):
        Word("bad_char!")
    with pytest.raises(WdpCodecError):
        QuotientWitness(fiber=Word("f"), status="NOT_A_STATUS")
    with pytest.raises(WdpCodecError):
        BalanceMatrix(sites=-1, trace=0)
    with pytest.raises(WdpCodecError):
        BalanceMatrix(sites=0, trace=-5)
    with pytest.raises(WdpCodecError):
        WdpRefusal(code="BAD_CODE")
    with pytest.raises(WdpCodecError):
        serialize_wdp("not_an_ast_node")  # type: ignore[arg-type]
