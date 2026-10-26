"""Targeted pytest suite for S(n) presentation grammar conformance.

Verifies sn.ebnf rules against sn_conformance_cases.json using Grammar from check_grammars.py.
AuthorityEffect: None.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
CODE_DIR = HERE.parent
REPO = HERE.parents[4]
SN_EBNF_PATH = CODE_DIR.parent / "grammar" / "sn.ebnf"
CASES_PATH = CODE_DIR.parent / "grammar" / "sn_conformance_cases.json"

GRAMMAR_DIR = next(
    (
        p
        for p in (
            REPO / "omega_engine_education" / "documentation" / "004_oepfp" / "grammar",
            REPO / "omega_engine_education" / "documentation" / "030_the_symbol_game_proposal_fidelity_protocol_pfp" / "grammar",
            REPO / "ow" / "omega_engine_pfp_v0.2" / "grammar",
        )
        if p.is_dir()
    ),
    REPO / "omega_engine_education" / "documentation" / "004_oepfp" / "grammar",
)
sys.path.insert(0, str(GRAMMAR_DIR))
from check_grammars import Grammar


@pytest.fixture(scope="module")
def sn_grammar() -> Grammar:
    ebnf_source = SN_EBNF_PATH.read_text(encoding="utf-8")
    return Grammar(ebnf_source)


def _load_cases():
    return json.loads(CASES_PATH.read_text(encoding="utf-8"))


@pytest.mark.parametrize(
    "case", _load_cases(), ids=lambda c: f"{c['id']}_{c['start']}_{c['text']}_{c['accept']}"
)
def test_sn_conformance_case(sn_grammar: Grammar, case: dict):
    actual = sn_grammar.accepts(case["start"], case["text"])
    assert actual == case["accept"], (
        f"Failed case {case['id']}: start={case['start']!r}, text={case['text']!r}, "
        f"expected={case['accept']}, got={actual}"
    )


def test_sn_grammar_all_rules_defined(sn_grammar: Grammar):
    assert len(sn_grammar.rules) >= 15
    assert "sn_presentation" in sn_grammar.rules
    assert "ground_token" in sn_grammar.rules
    assert "supplied_token" in sn_grammar.rules
    assert "relation_token" in sn_grammar.rules
    assert "section_lift" in sn_grammar.rules
    assert "retraction_map" in sn_grammar.rules
    assert "non_descent" in sn_grammar.rules


def test_multi_adapter_receipt_packet_conformance(sn_grammar: Grammar):
    """Validate multi-adapter receipt packets for example levels E10-E21."""
    sys.path.insert(0, str(CODE_DIR))
    from sn_codec import RetractionMap, SectionLift, deserialize_sn

    multi_adapter_packets = [
        ("u_10<a>", 10, True),
        ("u_11<a->b>", 11, True),
        ("r_12<a->b>", 12, True),
        ("u_13<ab>", 13, True),
        ("r_14<a,b>", 14, True),
        ("u_15<a->b>", 15, True),
        ("r_16<ab>", 16, True),
        ("u_17<a->b>", 17, True),
        ("u_18<a,b>", 18, True),
        ("r_19<a->b>", 19, True),
        ("u_20<a,b>", 20, True),
        ("u_21<a->b>", 21, True),
    ]

    for wire, expected_stage, should_accept in multi_adapter_packets:
        assert sn_grammar.accepts("sn_presentation", wire) == should_accept, f"EBNF failed for wire {wire!r}"
        ast_node = deserialize_sn(wire)
        assert isinstance(ast_node, (SectionLift, RetractionMap))
        assert ast_node.stage == expected_stage

