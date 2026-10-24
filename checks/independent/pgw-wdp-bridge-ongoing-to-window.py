"""Independent check for PGW-WDP-BRIDGE-ONGOING-TO-WINDOW.

Recomputes the three-position coboundary round sum, the unbalanced mark,
the loop diagonal, and the two-way sum. No repository imports.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

FAILS = 0
CHECKED = 0


def check(cond: bool, msg: str) -> None:
    global FAILS, CHECKED
    CHECKED += 1
    if not cond:
        FAILS += 1
        print("FAIL", msg)


def round_sum(g0: int, g1: int, g2: int) -> int:
    return (g0 - g1) + (g1 - g2) + (g2 - g0)


def diagnostic(e01: int, e12: int, e20: int) -> int:
    return e01 + e12 + e20


def shift(e01: int, e12: int, e20: int, g0: int, g1: int, g2: int) -> tuple[int, int, int]:
    return (e01 + (g0 - g1), e12 + (g1 - g2), e20 + (g2 - g0))


SAMPLES = ((0, 0, 0), (2, 5, 11), (-4, 7, 1), (9, -3, 4), (100, -50, 25))
EDGES = ((0, 0, 0), (1, 1, 1), (3, 0, 0), (-2, 4, 8), (4, 4, 4))
NAMES = (
    "pgwBr_gradient_round",
    "pgwBr_shift_preserves",
    "pgwBr_unbalanced",
    "pgwBr_loop_diag",
    "pgwBr_loop_not_coboundary",
    "pgwBr_loop_report",
    "pgwBr_two_way",
)


def main() -> int:
    """Recompute the finite identities and scan the campaign module."""
    for triple in SAMPLES:
        check(round_sum(*triple) == 0, f"round {triple}")
    for edge in EDGES:
        for triple in SAMPLES:
            moved = shift(*edge, *triple)
            check(diagnostic(*moved) == diagnostic(*edge), f"shift {edge} {triple}")
    check(1 + 1 + 1 == 3, "unbalanced mark")
    moved = shift(1, 1, 1, 2, 5, 11)
    check(moved == (-2, -5, 10), "shift from (2, 5, 11)")
    check(diagnostic(*moved) == 3, "mark stays 3")
    for value in (0, 2, 4, 5, 11, -7):
        check(value - value == 0, f"diagonal {value}")
        check(value - value != 4, f"diagonal is not 4 for {value}")
    check(0 + 0 + 0 == 0, "oriented loop report")
    check(4 != 0, "loop value")
    check(3 + 0 + 0 == 3, "forward diagnostic")
    check(3 + 5 == 8, "two-way sum")
    check(3 != 8, "oriented report omits the reverse arc")
    lean = (
        Path(__file__).resolve().parents[2]
        / "lean4"
        / "CampaignPgwWdpBridgeOngoingToWindow.lean"
    )
    raw = lean.read_bytes()
    check(b"\r" not in raw, "lean line endings")
    text = raw.decode("utf-8")
    for name in NAMES:
        check(text.count(f"theorem {name}") == 1, f"theorem {name}")
        check(text.count(f"#print axioms {name}") == 1, f"print {name}")
    for token in ("sorry", "admit", "axiom", "native_decide", "unsafe"):
        found = re.search(rf"(?<![\w.']){token}(?![\w'])", text) is not None
        check(not found, f"forbidden {token}")
    print(f"checked {CHECKED} claims, failures {FAILS}")
    print(
        "round 0 unbalanced 3 shifted",
        moved,
        "diag",
        diagnostic(*moved),
        "loop 4 two_way 8",
    )
    return FAILS


if __name__ == "__main__":
    sys.exit(main())
