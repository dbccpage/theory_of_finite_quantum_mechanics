"""Independent check for the COMP-C2-STEP3-NOT-WORD-STEP narrowing.

Replays three concrete one-hole list replacements and the map that sends 1 to 0.
Does not import repository code. These lists are not every Genesis Step3 state.
"""
from __future__ import annotations

failures = 0


def check(cond: bool, msg: str) -> None:
    global failures
    if not cond:
        failures += 1
        print("FAIL", msg)


def hole(word: list[int], left: list[int], lhs: list[int], rhs: list[int], right: list[int]) -> list[int]:
    check(word == left + lhs + right, f"split {word}")
    return left + rhs + right


got = hole([0], [0], [], [1], [])
check(got == [0, 1], f"append 1 gave {got}")

got = hole([0, 1], [0, 1], [], [0, 1], [])
check(got == [0, 1, 0, 1], f"append block gave {got}")

got = hole([0, 1], [0], [1], [], [])
check(got == [0], f"delete final 1 gave {got}")


def merge01(t: int) -> int:
    return 0 if t == 1 else t


check(merge01(0) == 0 and merge01(1) == 0 and 0 != 1, "merge01")
check(merge01(2) == 2, "merge01 fixes 2")

print(
    "checked [0] -> [0, 1] by replacing an empty block with [1]; "
    "[0, 1] -> [0, 1, 0, 1] by replacing an empty block with [0, 1]; "
    "[0, 1] -> [0] by replacing [1] with an empty block; "
    "merge01 sends 0 and 1 to 0 and fixes 2"
)
print(f"failures={failures}")
raise SystemExit(failures)
