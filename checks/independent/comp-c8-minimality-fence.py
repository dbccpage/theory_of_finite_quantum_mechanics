"""Independent check for the closed COMP-C8 tape.

Recomputes one word of two marks followed by one blank cell.
Does not import repository code. No machine and no minimality sentence.
"""
from __future__ import annotations

mark_a = 1
mark_b = 2
blank = 0


def append_blank(word: list[int]) -> list[int]:
    return word + [blank]


failures = 0


def check(name: str, cond: bool) -> None:
    global failures
    print(f"{name}: {cond}")
    if not cond:
        failures += 1


got = append_blank([mark_a, mark_b])
check("mark_a_is_1", mark_a == 1)
check("mark_b_is_2", mark_b == 2)
check("blank_is_0", blank == 0)
check("one_word_then_blank", got == [1, 2, 0])
check("length_3", len(got) == 3)
check("blank_differs_from_mark_a", blank != mark_a)
check("blank_differs_from_mark_b", blank != mark_b)
print(f"failures={failures}")
raise SystemExit(failures)
