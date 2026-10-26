"""Conformance checker for the pre-genesis inscription grammar.

AuthorityEffect: None. GenesisEffect: None.

Replays ``grammar/pre_genesis_conformance_cases.json`` against
``grammar/pre_genesis.ebnf`` with the shared EBNF-subset recognizer from the
030 grammar directory. Exit code 0 on PASS, 1 on any divergence. Dual
invocation: run the file directly or import it and call ``main()``.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import TypedDict

HERE = Path(__file__).resolve().parent
STRAND = HERE.parent
REPO = HERE.parents[3]
EBNF_PATH = STRAND / "grammar" / "pre_genesis.ebnf"
CASES_PATH = STRAND / "grammar" / "pre_genesis_conformance_cases.json"
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
if str(GRAMMAR_DIR) not in sys.path:
    sys.path.insert(0, str(GRAMMAR_DIR))

from check_grammars import Grammar  # noqa: E402

PUBLIC_STARTS: tuple[str, ...] = ("ground_token", "inscription", "pre_genesis_regime")


class GrammarCase(TypedDict):
    id: str
    start: str
    text: str
    accept: bool


def load_grammar() -> Grammar:
    return Grammar(EBNF_PATH.read_text(encoding="utf-8"))


def validate_cases(payload: object) -> list[GrammarCase]:
    if not isinstance(payload, list) or not payload:
        raise ValueError("conformance cases must be a nonempty list")
    cases: list[GrammarCase] = []
    seen: set[str] = set()
    coverage: set[tuple[str, bool]] = set()
    for index, case in enumerate(payload):
        if not isinstance(case, dict) or set(case) != {"id", "start", "text", "accept"}:
            raise ValueError(f"case {index}: expected id, start, text and accept fields")
        case_id, start, text, accept = (
            case["id"], case["start"], case["text"], case["accept"]
        )
        if not isinstance(case_id, str) or not case_id or case_id in seen:
            raise ValueError(f"case {index}: id must be a unique nonempty string")
        if not isinstance(start, str) or start not in PUBLIC_STARTS:
            raise ValueError(f"case {case_id}: unknown public start")
        if not isinstance(text, str) or type(accept) is not bool:
            raise ValueError(f"case {case_id}: text must be a string and accept a Boolean")
        cases.append({"id": case_id, "start": start, "text": text, "accept": accept})
        seen.add(case_id)
        coverage.add((start, accept))
    missing = {(start, accept) for start in PUBLIC_STARTS for accept in (False, True)} - coverage
    if missing:
        raise ValueError(f"missing positive/negative public-start controls: {sorted(missing)}")
    return cases


def load_cases() -> list[GrammarCase]:
    return validate_cases(json.loads(CASES_PATH.read_text(encoding="utf-8")))


def main() -> int:
    try:
        grammar = load_grammar()
        cases = load_cases()
    except (OSError, ValueError) as error:
        print(f"FAIL: cannot load conformance inputs: {error}")
        return 1
    failures: list[str] = []
    starts_covered: set[str] = set()
    for case in cases:
        start = case["start"]
        text = case["text"]
        expected = case["accept"]
        if start not in PUBLIC_STARTS:
            failures.append(f"{case['id']}: start {start!r} is not a public start")
            continue
        starts_covered.add(start)
        actual = grammar.accepts(start, text)
        if actual != expected:
            failures.append(
                f"{case['id']}: start={start} text={text!r} expected={expected} actual={actual}"
            )
    if failures:
        print(f"FAIL: {len(failures)} divergence(s) in pre_genesis.ebnf")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print(
        f"PASS: {len(cases)} cases accepted/refused across {len(starts_covered)} starts "
        "in pre_genesis.ebnf"
    )
    print(f"Grammar source: {EBNF_PATH}")
    print("AuthorityEffect: None.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
