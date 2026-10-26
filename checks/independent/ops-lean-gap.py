#!/usr/bin/env python3
"""Four parity constraints on one Boolean box for OPS-LEAN-GAP.

Enumerates all 16 assignments with ordinary Boolean arithmetic.
No repository module is imported. Noncontextual fraction, Vorob'ev,
and any Rust scenario stay outside this check.
"""

from __future__ import annotations


def main() -> None:
    failures = 0
    checks = 0

    def check(cond: bool, label: str) -> None:
        nonlocal failures, checks
        checks += 1
        if not cond:
            failures += 1
            print("FAIL", label)

    hits = 0
    for a in (False, True):
        for ap in (False, True):
            for b in (False, True):
                for bp in (False, True):
                    lhs = (a ^ b) ^ (a ^ bp) ^ (ap ^ b) ^ (ap ^ bp)
                    check(lhs is False, f"lhs {a, ap, b, bp}")
                    sat = (a ^ b) is False and (a ^ bp) is False and (ap ^ b) is False and (ap ^ bp) is True
                    if sat:
                        hits += 1
    check(hits == 0, f"hits {hits}")
    check((False ^ False ^ False ^ True) is True, "rhs")
    check(2 * 2 * 2 * 2 == 16, "sixteen")
    print(
        "bool4 assignments=16 hits=0 lhs_xor=false rhs_xor=true failures="
        + str(failures)
    )
    if failures:
        raise SystemExit(1)
    print("OPS-LEAN-GAP INDEPENDENT CHECKER PASSED: checks=" + str(checks) + " failed=0")


if __name__ == "__main__":
    main()
