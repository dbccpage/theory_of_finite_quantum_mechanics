"""Shape of composing a word predicate after a start map.

Two codes only. This script does not decide computability and does not
import repository code.
"""
from __future__ import annotations

failures = 0


def check(cond: bool, msg: str) -> None:
    global failures
    if not cond:
        failures += 1
        print("FAIL", msg)


def start_word(code: int) -> tuple[int, int]:
    return (code, 0)


def word_pred(word: tuple[int, int]) -> bool:
    return word == (1, 0)


check(start_word(0) == (0, 0), "start map on code 0")
check(start_word(1) == (1, 0), "start map on code 1")
check(word_pred((0, 0)) is False, "unmarked word")
check(word_pred((1, 0)) is True, "marked word")
check(word_pred(start_word(0)) is False, "composed predicate on code 0")
check(word_pred(start_word(1)) is True, "composed predicate on code 1")

print("checked two codes: start map then word predicate; code 0 misses (1, 0) and code 1 meets it")
print(f"failures={failures}")
raise SystemExit(failures)
