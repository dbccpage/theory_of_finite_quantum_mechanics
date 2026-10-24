"""Independent check for the PGW-DECLARED-INPUT-FLOOR bound record.

Reads the Lean constants and recomputes the finite comparisons. Does not
import repository code and does not claim a floor.
"""
from __future__ import annotations

import re
from pathlib import Path

EXPECTED = {
    "pgwRounds": 15,
    "pgwGuard": 250,
    "pgwDataCeiling": 4,
    "pgwItemBound": 2,
    "pgwInputCount": 2,
    "pgwEngines": 4,
    "pgwReadings": 2,
}
EXPECTED_CANDIDATES = (0, 1, 2, 3, 4)
THEOREM_NAMES = (
    "pgwBounds_values",
    "pgwInput_eq_items",
    "pgwOne_below_input",
    "pgwGuard_above_rounds",
    "pgwEngines_ne_readings",
    "pgwStrictlyBelow_list",
    "pgwStrictlyBelow_length",
    "pgwCeiling_not_below",
)
FORBIDDEN_TOKENS = ("sorry", "native_decide", "unsafe")


def main() -> None:
    failures: list[str] = []
    claims = 0

    def check(name: str, ok: bool) -> None:
        nonlocal claims
        claims += 1
        if not ok:
            failures.append(name)

    root = Path(__file__).resolve().parents[2]
    lean_path = root / "lean4" / "CampaignPgwDeclaredInputFloor.lean"
    lean = lean_path.read_text(encoding="utf-8")
    values: dict[str, int] = {}
    for name in EXPECTED:
        match = re.search(rf"^def {name} : Nat := (\d+)$", lean, re.M)
        check(f"def_{name}", match is not None)
        if match:
            values[name] = int(match.group(1))
            check(f"value_{name}", values[name] == EXPECTED[name])
    cand = re.search(r"^def pgwDataCandidates : List Nat := \[([0-9, ]+)\]$", lean, re.M)
    check("def_candidates", cand is not None)
    candidates = tuple(int(part) for part in cand.group(1).split(",")) if cand else ()
    check("candidates", candidates == EXPECTED_CANDIDATES)

    if len(values) == len(EXPECTED) and candidates:
        ceiling = values["pgwDataCeiling"]
        below = [n for n in candidates if n < ceiling]
        check("input_eq_items", values["pgwInputCount"] == values["pgwItemBound"])
        check("one_below_input", 1 < values["pgwInputCount"])
        check("guard_above_rounds", values["pgwRounds"] < values["pgwGuard"])
        check("engines_ne_readings", values["pgwEngines"] != values["pgwReadings"])
        check("strictly_below_list", below == [0, 1, 2, 3])
        check("strictly_below_length", len(below) == 4)
        check("ceiling_not_below", (ceiling < ceiling) is False)
        check("below_excludes_ceiling", ceiling not in below)
        check("seven_numerals", len(values) == 7)

    for name in THEOREM_NAMES:
        check(f"theorem_{name}", f"theorem {name}" in lean)
    for token in FORBIDDEN_TOKENS:
        check(f"no_{token}", token not in lean)
    check("no_axiom_decl", all(not line.startswith("axiom ") for line in lean.splitlines()))
    check("no_admit_token", "admit" not in lean)
    check("prints_axioms", lean.count("#print axioms ") == len(THEOREM_NAMES))

    print(f"checked {claims} claims, failures {len(failures)}")
    if failures:
        print("failures: " + ", ".join(failures))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
