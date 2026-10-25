#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Independent check for one exact coboundary on PGW-WDP-HANDOFF-TO-L1.

AuthorityEffect: None.

Recomputes the coboundary of vertex values (0, 1, 0) in slot order (01, 12, 02),
its L1 norm, the residual after subtracting that coboundary, and the oriented sum.
No repository imports.
"""
from __future__ import annotations

import pathlib
import re
import sys


def coboundary(f0: int, f1: int, f2: int) -> tuple[int, int, int]:
    return (f1 - f0, f2 - f1, f2 - f0)


def l1(slots: tuple[int, int, int]) -> int:
    return abs(slots[0]) + abs(slots[1]) + abs(slots[2])


def main() -> int:
    claims: list[tuple[str, bool]] = []

    def add(name: str, ok: bool) -> None:
        claims.append((name, ok))

    values = (0, 1, 0)
    slots = coboundary(values[0], values[1], values[2])
    add("coboundary", slots == (1, -1, 0))
    leakage = l1(slots)
    add("leakage", leakage == 2)
    residual = (
        slots[0] - (values[1] - values[0]),
        slots[1] - (values[2] - values[1]),
        slots[2] - (values[2] - values[0]),
    )
    add("residual", residual == (0, 0, 0))
    residual_l1 = l1(residual)
    add("residual_l1", residual_l1 == 0)
    add("zero_lower_bound_sample", all(0 <= n for n in (0, 1, 2, 5, 10)))
    add("leakage_not_residual", leakage != residual_l1)
    oriented = slots[0] + slots[1] - slots[2]
    add("oriented", oriented == 0)

    lean_path = pathlib.Path(__file__).resolve().parents[2] / "lean4" / "CampaignPgwWdpHandoffToL1.lean"
    raw = lean_path.read_bytes()
    text = raw.decode("utf-8")
    add("lean_lf", b"\r" not in raw)
    names = (
        "pgwHo_coboundary",
        "pgwHo_leakage",
        "pgwHo_repair",
        "pgwHo_residual_l1",
        "pgwHo_zero_le",
        "pgwHo_leakage_not_min",
        "pgwHo_oriented",
    )
    add(
        "one_theorem_each",
        all(re.search(r"(?m)^theorem " + name + r"\b", text) is not None for name in names),
    )
    add(
        "one_print_each",
        all(
            re.search(r"(?m)^#print axioms CampaignPgwWdpHandoffToL1\." + name + r"$", text) is not None
            for name in names
        ),
    )
    add("zero_le_statement", "theorem pgwHo_zero_le (n : Nat) : 0 ≤ n := Nat.zero_le n" in text)
    forbidden = re.search(r"(?m)^\s*axiom\b|\b(sorry|admit|native_decide|unsafe)\b", text)
    add("no_forbidden_token", forbidden is None)

    failed = [name for name, ok in claims if not ok]
    print(f"checked {len(claims)} claims, failures {len(failed)}")
    if failed:
        print("failed: " + ", ".join(failed))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
