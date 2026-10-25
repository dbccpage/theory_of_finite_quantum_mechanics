"""Independent check for the COMP-C7-FIXED-TARGET-OPEN narrowing.

Replays two erasures to the fixed word [0].
Does not import repository code. These words are not the rule set R0'.
"""
from __future__ import annotations

failures = 0


def check(cond: bool, msg: str) -> None:
    global failures
    if not cond:
        failures += 1
        print("FAIL", msg)


def hole(word, left, lhs, rhs, right):
    check(word == left + lhs + right, f"split {word}")
    return left + rhs + right


fixed = [0]
got = hole([1, 0], [], [1], [], [0])
check(got == fixed, f"erase 1 gave {got}")
got = hole([2, 0], [], [2], [], [0])
check(got == fixed, f"erase 2 gave {got}")

print("checked [1, 0] erases [1] to [0]; [2, 0] erases [2] to [0]; both results are [0]")
print(f"failures={failures}")
raise SystemExit(failures)
