"""Verify wdp.ebnf against conformance test cases.

AuthorityEffect: None. GenesisEffect: None.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
STRAND_DIR = HERE.parent
WDP_EBNF_PATH = STRAND_DIR / "grammar" / "wdp.ebnf"
CASES_PATH = STRAND_DIR / "grammar" / "wdp_conformance_cases.json"

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
from check_grammars import Grammar


def main() -> int:
    ebnf_source = WDP_EBNF_PATH.read_text(encoding="utf-8")
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

    print(f"PASS: {len(cases)} cases accepted/refused across starts in wdp.ebnf")
    print(f"Grammar source: {WDP_EBNF_PATH}")
    print("AuthorityEffect: None.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
