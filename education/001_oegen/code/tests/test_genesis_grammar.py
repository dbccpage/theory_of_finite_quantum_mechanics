"""Targeted pytest suite for genesis.ebnf conformance verification.

AuthorityEffect: None. GenesisEffect: None.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
STRAND = HERE.parents[1]
REPO = next(
    (p for p in Path(__file__).resolve().parents if (p / ".git").exists()),
    Path(__file__).resolve().parents[4],
)
GENESIS_EBNF_PATH = STRAND / "grammar" / "genesis.ebnf"
CASES_PATH = STRAND / "grammar" / "genesis_conformance_cases.json"
cand_1 = REPO / "omega_engine_education" / "documentation" / "004_oepfp" / "grammar"
cand_2 = REPO / "omega_engine_education" / "documentation" / "030_the_symbol_game_proposal_fidelity_protocol_pfp" / "grammar"
GRAMMAR_DIR = cand_1 if cand_1.is_dir() else cand_2

sys.path.insert(0, str(GRAMMAR_DIR))
from check_grammars import Grammar


@pytest.fixture(scope="module")
def genesis_grammar() -> Grammar:
    ebnf = GENESIS_EBNF_PATH.read_text(encoding="utf-8")
    return Grammar(ebnf)


def test_genesis_conformance(genesis_grammar: Grammar):
    cases = json.loads(CASES_PATH.read_text(encoding="utf-8"))
    for c in cases:
        start = c["start"]
        text = c["text"]
        expected = c["accept"]
        actual = genesis_grammar.accepts(start, text)
        assert actual == expected, (
            f"Case {c['id']} failed: text={text!r}, expected={expected}, got={actual}"
        )
