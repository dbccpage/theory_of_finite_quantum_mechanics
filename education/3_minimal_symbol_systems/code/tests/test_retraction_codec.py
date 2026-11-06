"""Test Suite for MSS-N Retraction Codec between Gamma_38 and Gamma_100.

AuthorityEffect: None. GenesisEffect: None.

Verifies:
1. Theorem 9.1: Retraction identity r_100_38 ∘ ι = id on Gamma_38*.
2. Conservative alphabet transport: all Gamma_38 words are preserved without modification.
3. Extended glyph retraction: operational punctuation, Greek alphabet, and semantic emojis.
4. Entropy metrics and theoretical compression bounds.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
CODE_DIR = HERE.parent
sys.path.insert(0, str(CODE_DIR))

from mssn_extended_codec import (
    GAMMA_38,
    GAMMA_100,
    GAMMA_100_EXTENDED,
    RETRACTION_TABLE,
    SET_GAMMA_38,
    SET_GAMMA_100,
    entropy_gamma38,
    entropy_gamma100,
    inclusion_38_to_100,
    is_in_gamma38,
    is_in_gamma100,
    retraction_100_to_38,
    theoretical_compression_ratio_100_over_38,
    tokenize_gamma100,
)



def test_alphabet_cardinalities() -> None:
    """Check exact mathematical cardinalities of declared alphabets."""
    assert len(GAMMA_38) == 38
    assert len(SET_GAMMA_38) == 38
    assert len(GAMMA_100) == 100
    assert len(SET_GAMMA_100) == 100
    assert len(GAMMA_100_EXTENDED) == 62
    assert SET_GAMMA_38.issubset(SET_GAMMA_100)


def test_retraction_table_well_formed() -> None:
    """Verify that every extended glyph retracts to a non-empty string in Gamma_38*."""
    assert len(RETRACTION_TABLE) == 62
    for glyph, replacement in RETRACTION_TABLE.items():
        assert len(replacement) > 0
        assert is_in_gamma38(replacement), (
            f"Replacement {replacement!r} for {glyph!r} must be in Gamma_38*"
        )


@pytest.mark.parametrize(
    "wire38",
    [
        "",
        "a",
        "z",
        "0",
        "9",
        "<>",
        "<ab>",
        "a>b>c>a",
        "a0>b2>c1>a0",
        "op<<10010><1><11><10>>",
        "node1<step>node2",
        "10011010",
        "deadbeef",
        "<packet<nested<value42>>>",
    ],
)
def test_theorem_9_1_retraction_identity(wire38: str) -> None:
    """Verify Theorem 9.1: r_100_38(ι(w)) == w for any w in Gamma_38*."""
    assert is_in_gamma38(wire38)
    lifted = inclusion_38_to_100(wire38)
    assert lifted == wire38  # Inclusion is identity on string representation
    retracted = retraction_100_to_38(lifted)
    assert retracted == wire38, f"Retraction failed for {wire38!r}: got {retracted!r}"


def test_extended_glyph_tokenization() -> None:
    """Verify that multi-codepoint emojis and Greek symbols are tokenized atomically."""
    sample = "a=b!+α>β🎯📦⚖️"
    tokens = tokenize_gamma100(sample)
    expected = ["a", "=", "b", "!", "+", "α", ">", "β", "🎯", "📦", "⚖️"]
    assert tokens == expected
    assert is_in_gamma100(sample)


def test_extended_glyphs_retraction_mapping() -> None:
    """Test retraction of punctuation, Greek symbols, and emojis."""
    # Equality and bang
    assert retraction_100_to_38("a=b!") == "aeqbbang"
    # Arithmetic and brackets
    assert retraction_100_to_38("x[1]+y[2]") == "x<lbrak>1<rbrak>addy<lbrak>2<rbrak>"
    # Greek categorical symbols
    assert retraction_100_to_38("α>β") == "alpha>beta"
    assert retraction_100_to_38("∂Ω=0") == "<del><omega>eq0"
    # Semantic emojis
    assert retraction_100_to_38("🎯<goal>📦") == "<goal><goal><pack>"
    assert retraction_100_to_38("🔒<lock>") == "<lock><lock>"


def test_refusal_on_invalid_glyphs() -> None:
    """Verify fail-closed refusal when characters are outside Gamma_100."""
    # Inclusion refusal
    with pytest.raises(ValueError, match="outside Gamma_38"):
        inclusion_38_to_100("a=b")  # '=' is in Gamma_100 but not Gamma_38

    # Retraction refusal on characters outside Gamma_100
    with pytest.raises(ValueError, match="not in Gamma_100"):
        retraction_100_to_38("hello @ world")  # '@' is not in Gamma_100

    with pytest.raises(ValueError, match="not in Gamma_100"):
        retraction_100_to_38("price $100")  # '$' is not in Gamma_100


def test_entropy_and_compression_bounds() -> None:
    """Verify Theorem 9.2 information-theoretic calculations."""
    h38 = entropy_gamma38()
    h100 = entropy_gamma100()
    assert 5.24 < h38 < 5.25  # log2(38) ≈ 5.2479
    assert 6.64 < h100 < 6.65  # log2(100) ≈ 6.6439

    ratio = theoretical_compression_ratio_100_over_38()
    assert 1.26 < ratio < 1.27  # ≈ 1.266 symbols per equal-information block ratio
    assert 0.20 < 1 - 1 / ratio < 0.22  # Ideal symbol-count reduction is ≈21%.


@pytest.mark.parametrize("wire", ["\n", "a\nb", "α\r\nβ", "a\t", "a\u2028b"])
def test_tokenizer_does_not_discard_invalid_layout(wire: str) -> None:
    assert "".join(tokenize_gamma100(wire)) == wire
    assert not is_in_gamma100(wire)
    with pytest.raises(ValueError, match="not in Gamma_100"):
        retraction_100_to_38(wire)


def test_retraction_is_not_a_lossless_encoding_of_new_words() -> None:
    assert "α" != "alpha"
    assert retraction_100_to_38("α") == retraction_100_to_38("alpha")
