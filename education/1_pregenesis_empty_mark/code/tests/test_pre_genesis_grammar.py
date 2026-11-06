"""Pre-genesis grammar conformance and four-state separation tests.

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
for path in (GRAMMAR_DIR, CODE_DIR):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

import check_pre_genesis  # noqa: E402
from check_grammars import Grammar  # noqa: E402


@pytest.fixture(scope="module")
def grammar() -> Grammar:
    return Grammar(check_pre_genesis.EBNF_PATH.read_text(encoding="utf-8"))


def _load_cases() -> list[dict[str, object]]:
    return json.loads(check_pre_genesis.CASES_PATH.read_text(encoding="utf-8"))


@pytest.mark.parametrize(
    "case",
    _load_cases(),
    ids=lambda case: f"{case['id']}_{case['start']}_{case['accept']}",
)
def test_pre_genesis_conformance_case(grammar: Grammar, case: dict[str, object]) -> None:
    assert grammar.accepts(str(case["start"]), str(case["text"])) == bool(case["accept"])


def test_public_starts_and_rules_are_defined(grammar: Grammar) -> None:
    assert set(check_pre_genesis.PUBLIC_STARTS) <= set(grammar.rules)
    assert {"occupied_token", "payload", "payload_glyph"} <= set(grammar.rules)


def test_four_state_separation(grammar: Grammar) -> None:
    for start in check_pre_genesis.PUBLIC_STARTS:
        assert not grammar.accepts(start, ""), start
    assert grammar.accepts("ground_token", "<>")
    assert grammar.accepts("pre_genesis_regime", "{}")
    assert not grammar.accepts("ground_token", "{}")
    assert not grammar.accepts("pre_genesis_regime", "<>")


def test_sigma36_glyphs_and_cuts_are_not_pre_genesis(grammar: Grammar) -> None:
    for glyph in "cdefghijklmnopqrstuvwxyz0123456789":
        assert not grammar.accepts("inscription", f"<{glyph}>"), glyph
    assert not grammar.accepts("inscription", "<a->b>")


def test_checker_main_returns_zero(capsys: pytest.CaptureFixture[str]) -> None:
    assert check_pre_genesis.main() == 0
    assert "PASS" in capsys.readouterr().out


@pytest.mark.parametrize("bad", ["false", 0, 1, None])
def test_expected_verdict_is_not_coerced(bad: object) -> None:
    cases = _load_cases()
    cases[0]["accept"] = bad
    with pytest.raises(ValueError, match="Boolean"):
        check_pre_genesis.validate_cases(cases)


def test_empty_duplicate_and_incomplete_controls_are_refused() -> None:
    cases = _load_cases()
    with pytest.raises(ValueError, match="nonempty"):
        check_pre_genesis.validate_cases([])
    with pytest.raises(ValueError, match="unique"):
        check_pre_genesis.validate_cases(cases + [cases[0]])
    with pytest.raises(ValueError, match="missing positive/negative"):
        check_pre_genesis.validate_cases([case for case in cases if case["accept"]])


def test_invalid_case_file_cannot_print_pass(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    case_path = tmp_path / "cases.json"
    case_path.write_text("[]", encoding="utf-8")
    monkeypatch.setattr(check_pre_genesis, "CASES_PATH", case_path)
    assert check_pre_genesis.main() == 1
    output = capsys.readouterr().out
    assert "FAIL" in output and "PASS" not in output
