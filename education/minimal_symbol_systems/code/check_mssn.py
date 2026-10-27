"""Verify mssn.ebnf and its 22 declared public starts against test cases.

Development evidence only; not a production parser or semantic verifier.
AuthorityEffect: None.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
MSSN_EBNF_PATH = HERE.parent / "grammar" / "mssn.ebnf"
CASES_PATH = HERE.parent / "grammar" / "mssn_conformance_cases.json"

# Import Grammar recognizer from 030_the_symbol_game_proposal_fidelity_protocol_pfp/grammar/check_grammars.py
GRAMMAR_DIR = next(
    (
        p
        for p in (
            REPO / "atlas" / "papers" / "finite_obstruction_calculus" / "pregenesis_to_minimal_symbol_systems" / "code" / "grammar",
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


def main() -> int:
    ebnf_source = MSSN_EBNF_PATH.read_text(encoding="utf-8")
    grammar = Grammar(ebnf_source)
    cases = json.loads(CASES_PATH.read_text(encoding="utf-8"))

    failures = []
    for c in cases:
        case_id = c["id"]
        start = c["start"]
        text = c["text"]
        expected = c["accept"]
        actual = grammar.accepts(start, text)
        if actual != expected:
            failures.append((case_id, start, text, expected, actual))

    if failures:
        print(f"FAILED: {len(failures)} cases failed:")
        for fid, start, text, exp, act in failures:
            print(f"  [{fid}] start={start} text={text!r} expected={exp} got={act}")
        return 1

    print(f"PASS: {len(cases)} cases accepted/refused across {len({c['start'] for c in cases})} starts in mssn.ebnf")
    print(f"Grammar source: {MSSN_EBNF_PATH}")
    print("AuthorityEffect: None.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
