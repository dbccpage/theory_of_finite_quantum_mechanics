"""Targeted pytest suite for wdp.ebnf conformance verification.

AuthorityEffect: None. GenesisEffect: None.
"""

from __future__ import annotations

import json
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

sys.path.insert(0, str(GRAMMAR_DIR))
from check_grammars import Grammar


@pytest.fixture(scope="module")
def wdp_grammar() -> Grammar:
    ebnf = WDP_EBNF_PATH.read_text(encoding="utf-8")
    return Grammar(ebnf)


def test_wdp_conformance(wdp_grammar: Grammar):
    cases = json.loads(CASES_PATH.read_text(encoding="utf-8"))
    for c in cases:
        start = c["start"]
        text = c["text"]
        expected = c["accept"]
        actual = wdp_grammar.accepts(start, text)
        assert actual == expected, (
            f"Case {c['id']} failed: text={text!r}, expected={expected}, got={actual}"
        )


def test_wdp_grammar_rules_defined(wdp_grammar: Grammar):
    assert "wdp_statement" in wdp_grammar.rules
    assert "difference_item" in wdp_grammar.rules
    assert "transport_event" in wdp_grammar.rules
    assert "quotient_witness" in wdp_grammar.rules
    assert "balance_matrix" in wdp_grammar.rules
    assert "refusal" in wdp_grammar.rules
