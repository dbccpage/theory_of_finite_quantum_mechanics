"""MSS-N Extended 100-Glyph Horizon Codec: Inclusion, Retraction, and Compression.

AuthorityEffect: None. GenesisEffect: None.

An explicit old-alphabet inclusion and word substitution retraction from
Gamma_100 to Gamma_38. The retraction is not injective on extended words;
for example both α and alpha map to alpha. Logarithms below are ideal
uniform-symbol information rates, not measured byte compression.
"""

from __future__ import annotations

import math
import re
from typing import Final, Mapping

# ---------------------------------------------------------------------------
# Alphabet Partition Definitions
# ---------------------------------------------------------------------------

# Gamma_38: 26 lower latin + 10 decimal digits + 2 boundary delimiters
GAMMA_38_LOWER_LATIN: Final[tuple[str, ...]] = tuple("abcdefghijklmnopqrstuvwxyz")
GAMMA_38_DIGITS: Final[tuple[str, ...]] = tuple("0123456789")
GAMMA_38_DELIMITERS: Final[tuple[str, ...]] = ("<", ">")

GAMMA_38: Final[tuple[str, ...]] = (
    GAMMA_38_LOWER_LATIN + GAMMA_38_DIGITS + GAMMA_38_DELIMITERS
)
assert len(GAMMA_38) == 38, f"Gamma_38 must have 38 glyphs, got {len(GAMMA_38)}"

# Extended glyphs in Gamma_100 (62 additional glyphs)

# 1. Operational Punctuation (12 glyphs)
SIGMA_PUNCT: Final[tuple[str, ...]] = (
    "!", "=", "+", "-", "*", "/", "[", "]", "(", ")", ":", ";"
)
assert len(SIGMA_PUNCT) == 12

# 2. Greek Mathematical Alphabet (24 glyphs: 20 lowercase + 4 uppercase/operators)
SIGMA_GREEK: Final[tuple[str, ...]] = (
    "α", "β", "γ", "δ", "ε", "ζ", "η", "θ", "λ", "μ",
    "ν", "ξ", "π", "ρ", "σ", "τ", "φ", "χ", "ψ", "ω",
    "Ω", "Δ", "∇", "∂",
)
assert len(SIGMA_GREEK) == 24

# 3. Semantic Emojis & Pictograms (26 glyphs)
# Note: Emojis with variation selectors (like ⚖️, 🛡️, 🏷️) are matched as exact declared code-point sequences; no normalization is applied.
SIGMA_EMOJI: Final[tuple[str, ...]] = (
    "🎯", "🔒", "📦", "⚖️", "🧭", "🧩", "⚡", "🛡️", "🔍", "📜",
    "🛑", "🚪", "🔑", "🔗", "🏷️", "📐", "🔬", "🧪", "🔮", "💡",
    "💎", "⏳", "🏁", "🚀", "🌟", "⚙️",
)
assert len(SIGMA_EMOJI) == 26

# Gamma_100: Total 100 glyphs
GAMMA_100_EXTENDED: Final[tuple[str, ...]] = (
    SIGMA_PUNCT + SIGMA_GREEK + SIGMA_EMOJI
)
assert len(GAMMA_100_EXTENDED) == 62

GAMMA_100: Final[tuple[str, ...]] = GAMMA_38 + GAMMA_100_EXTENDED
assert len(GAMMA_100) == 100, f"Gamma_100 must have 100 glyphs, got {len(GAMMA_100)}"

SET_GAMMA_38: Final[frozenset[str]] = frozenset(GAMMA_38)
SET_GAMMA_100: Final[frozenset[str]] = frozenset(GAMMA_100)

# ---------------------------------------------------------------------------
# Canonical Codec Retraction Mapping r_100_38(g) for g in Gamma_100 \ Gamma_38
# ---------------------------------------------------------------------------

RETRACTION_TABLE: Final[Mapping[str, str]] = {
    # Punctuation
    "!": "bang",
    "=": "eq",
    "+": "add",
    "-": "sub",
    "*": "mul",
    "/": "div",
    "[": "<lbrak>",
    "]": "<rbrak>",
    "(": "<lparen>",
    ")": "<rparen>",
    ":": "<colon>",
    ";": "<semi>",
    # Greek
    "α": "alpha",
    "β": "beta",
    "γ": "gamma",
    "δ": "delta",
    "ε": "eps",
    "ζ": "zeta",
    "η": "eta",
    "θ": "theta",
    "λ": "lambda",
    "μ": "mu",
    "ν": "nu",
    "ξ": "xi",
    "π": "pi",
    "ρ": "rho",
    "σ": "sigma",
    "τ": "tau",
    "φ": "phi",
    "χ": "chi",
    "ψ": "psi",
    "ω": "omega",
    "Ω": "<omega>",
    "Δ": "<delta>",
    "∇": "<nabla>",
    "∂": "<del>",
    # Emojis
    "🎯": "<goal>",
    "🔒": "<lock>",
    "📦": "<pack>",
    "⚖️": "<eqv>",
    "🧭": "<dir>",
    "🧩": "<comp>",
    "⚡": "<step>",
    "🛡️": "<guard>",
    "🔍": "<wit>",
    "📜": "<trace>",
    "🛑": "<halt>",
    "🚪": "<gate>",
    "🔑": "<key>",
    "🔗": "<link>",
    "🏷️": "<tag>",
    "📐": "<geom>",
    "🔬": "<obs>",
    "🧪": "<trial>",
    "🔮": "<pred>",
    "💡": "<idea>",
    "💎": "<pure>",
    "⏳": "<wait>",
    "🏁": "<term>",
    "🚀": "<lift>",
    "🌟": "<lead>",
    "⚙️": "<engine>",
}

assert set(RETRACTION_TABLE.keys()) == set(GAMMA_100_EXTENDED)

# Verify all retraction outputs are strictly in Gamma_38*
for k, v in RETRACTION_TABLE.items():
    assert all(c in SET_GAMMA_38 for c in v), (
        f"Retraction output {v!r} for glyph {k!r} contains characters outside Gamma_38"
    )

# ---------------------------------------------------------------------------
# Core Codec Operations
# ---------------------------------------------------------------------------


def is_in_gamma38(text: str) -> bool:
    """Return True iff every character in text belongs to Gamma_38."""
    return all(c in SET_GAMMA_38 for c in text)


def tokenize_gamma100(text: str) -> list[str]:
    """Segment a Gamma_100 string into its constituent atomic glyphs.

    Handles variation-selector emojis (e.g. ⚖️ = U+2696 U+FE0F) as single glyphs.
    """
    # Build regex pattern matching emojis and multi-codepoint symbols first
    emoji_patterns = sorted(SIGMA_EMOJI, key=len, reverse=True)
    pattern = (
        "|".join(re.escape(e) for e in emoji_patterns)
        + "|"
        + "|".join(re.escape(g) for g in SIGMA_GREEK)
        + "|"
        + "|".join(re.escape(p) for p in SIGMA_PUNCT)
        + "|."
    )
    tokens = re.findall(pattern, text, flags=re.DOTALL)
    return tokens


def is_in_gamma100(text: str) -> bool:
    """Return True iff text consists strictly of glyphs in Gamma_100."""
    tokens = tokenize_gamma100(text)
    return all(t in SET_GAMMA_100 for t in tokens)


def inclusion_38_to_100(wire38: str) -> str:
    """Inclusion homomorphism iota : Gamma_38* -> Gamma_100*.

    Every word in Gamma_38* is identically a word in Gamma_100*.
    """
    if not is_in_gamma38(wire38):
        invalid = [c for c in wire38 if c not in SET_GAMMA_38]
        raise ValueError(f"Input contains characters outside Gamma_38: {invalid[:5]}")
    return wire38


def retraction_100_to_38(wire100: str) -> str:
    """Retraction map r_100_38 : Gamma_100* -> Gamma_38*.

    Maps every glyph g in Gamma_38 to itself (identity), and every extended
    glyph g in Gamma_100 \\ Gamma_38 to its canonical composite Gamma_38* encoding.
    """
    tokens = tokenize_gamma100(wire100)
    result = []
    for t in tokens:
        if t in SET_GAMMA_38:
            result.append(t)
        elif t in RETRACTION_TABLE:
            result.append(RETRACTION_TABLE[t])
        else:
            raise ValueError(f"Character {t!r} is not in Gamma_100")
    return "".join(result)


# ---------------------------------------------------------------------------
# Information Theoretic Bounds
# ---------------------------------------------------------------------------


def entropy_gamma38() -> float:
    """Maximum Shannon entropy per symbol of Gamma_38: log2(38)."""
    return math.log2(38)


def entropy_gamma100() -> float:
    """Maximum Shannon entropy per symbol of Gamma_100: log2(100)."""
    return math.log2(100)


def theoretical_compression_ratio_100_over_38() -> float:
    """Theoretical compression factor log2(100) / log2(38)."""
    return entropy_gamma100() / entropy_gamma38()
