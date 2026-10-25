"""Independent check for the COMP-C6-TM0-OUTPUT-FORM-OPEN narrowing.

Replays one blank-cell writer and a constant evaluator.
Does not import repository code. This is not M0 or Code.eval.
"""
from __future__ import annotations

failures = 0


def check(cond: bool, msg: str) -> None:
    global failures
    if not cond:
        failures += 1
        print("FAIL", msg)


def write_halt(v: int, halted: bool, value: int) -> tuple[bool, int]:
    if halted:
        return halted, value
    return True, v


def eval_const(v: int, n: int) -> int:
    return v


for v in range(5):
    halted, value = write_halt(v, False, 0)
    check(halted is True and value == v, f"write {v} -> {(halted, value)}")
    for n in range(4):
        check(eval_const(v, n) == value, f"eval {v} {n}")

print(
    "checked writeHalt of v in 0..4 from a blank cell halts with value v; "
    "evalConst(v, n) equals that value for n in 0..3"
)
print(f"failures={failures}")
raise SystemExit(failures)
