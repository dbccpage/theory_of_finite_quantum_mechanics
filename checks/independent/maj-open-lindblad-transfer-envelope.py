"""Integer envelope f(T) = 4 + T*T*T against 3*T*T at T = 1, 2, 3.

Recomputes the narrowed comparisons and the separation of reading 0
from envelope value 12. No repository import. Integers only.
"""
from __future__ import annotations


def f(t: int) -> int:
    return 4 + t * t * t


def comparison(t: int) -> int:
    return 3 * t * t


def main() -> None:
    checks = 0
    failures = 0

    def expect(condition: bool) -> None:
        nonlocal checks, failures
        checks += 1
        if not condition:
            failures += 1

    expect(f(1) == 5)
    expect(comparison(1) == 3)
    expect(f(1) > comparison(1))
    expect(f(2) == 12)
    expect(comparison(2) == 12)
    expect(f(2) == comparison(2))
    expect(f(3) == 31)
    expect(comparison(3) == 27)
    expect(f(3) > comparison(3))
    expect(f(2) == 12 and 12 > 0)
    expect(0 < f(2))
    expect(2 * 2 == 4)
    expect(2 * 2 * 2 == 8)
    expect(4 + 1 == 5)
    expect(4 + 8 == 12)
    expect(3 * 4 == 12)
    expect(2 * 4 == 8)
    expect(3 * 3 * 3 == 27)
    expect(4 + 27 == 31)
    print(f"checked {checks} conditions, {failures} failures")
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
