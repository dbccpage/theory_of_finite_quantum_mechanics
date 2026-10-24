"""Independent check for the TFQ-0177 open-fence boundary.

Recomputes the Segre pieces at (1, 1, 1, 1) and reads the deposit texts.
Imports no repository code.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
README = ROOT / "papers" / "core" / "mub6" / "README.md"
MAIN = ROOT / "papers" / "core" / "mub6" / "code" / "src" / "main.rs"
REGISTRY = ROOT / "papers" / "core" / "mub6" / "research" / "mub6_gap_registry.json"
PROGRAM = ROOT / "lean4" / "research_programs" / "mub6"

FAILURES: list[str] = []
CHECKED = 0


def check(name: str, ok: bool) -> None:
    global CHECKED
    CHECKED += 1
    if not ok:
        FAILURES.append(name)


def main() -> None:
    quadric = (1 - 1) * (1 - 1) - (1 - 1) * (1 - 1)
    squares = (1 * 1 - 1) + (1 * 1 - 1) + (1 * 1 - 1) + (1 * 1 - 1)
    check("point_quadric", quadric == 0)
    check("point_squares", squares == 0)
    check("guard_cleared", 0 * 1000 - 1 == -1)
    check("collar_sign", -1 < 0 and 0 < 1000)
    # Cross-multiplication of -1/1000 against 0: -1 * 1 < 0 * 1000.
    check("fraction_below_zero", -1 * 1 < 0 * 1000)
    readme = README.read_text(encoding="utf-8")
    check("readme_title", "# MUB(6): exact reductions, conditional interfaces and open gaps" in readme)
    check("readme_open", "dimension six is open" in readme)
    check("readme_unset", "This deposit does not settle it." in readme)
    check("readme_g1", "Gap G1 is OPEN" in readme)
    check("readme_count_sentence", "185 `.lean` files" in readme and "imports 180" in readme)
    check("program_dir_absent", not PROGRAM.exists())
    main_rs = MAIN.read_text(encoding="utf-8")
    check("banner_comment", "This binary prints a banner. It does not run a solver." in main_rs)
    check("banner_line", "This binary prints a banner and does not run a solver." in main_rs)
    check("banner_fence", "Gap G1 stays OPEN. R6 and R7 stay NOT_A_CERTIFICATE." in main_rs)
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    g1 = next(gap for gap in registry["gaps"] if gap["id"] == "G1")
    residuals = {row["id"]: row for row in registry["open_residuals"]}
    check("g1_status", g1["status"] == "OPEN")
    check("r6_status", residuals["R6"]["status"] == "NOT_A_CERTIFICATE")
    check("r7_status", residuals["R7"]["status"] == "NOT_A_CERTIFICATE")
    check("r7_fraction", "-1/1000" in residuals["R7"]["note"])
    print(f"checked {CHECKED} claims, failures {len(FAILURES)}")
    if FAILURES:
        for name in FAILURES:
            print("FAIL", name)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
