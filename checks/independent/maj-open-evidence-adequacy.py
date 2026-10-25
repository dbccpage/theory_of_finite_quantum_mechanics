"""Two integer coordinate maps on the readings (1, 0) and (1, 1).

Recomputes the difference (0, -1), the shared first coordinate 1, and
the distinct second coordinates 0 and 1. No repository import.
Integers only.
"""
from __future__ import annotations


def main() -> None:
    checks = 0
    failures = 0

    def expect(condition: bool) -> None:
        nonlocal checks, failures
        checks += 1
        if not condition:
            failures += 1

    topo = (1, 0)
    andreev = (1, 1)
    diff = (topo[0] - andreev[0], topo[1] - andreev[1])
    expect(1 - 1 == 0)
    expect(0 - 1 == -1)
    expect(diff == (0, -1))
    expect(diff[0] == 0)
    expect(topo[0] == 1)
    expect(andreev[0] == 1)
    expect(diff[1] == -1)
    expect(topo[1] == 0)
    expect(andreev[1] == 1)
    expect(topo[1] != andreev[1])
    print(f"checked {checks} conditions, {failures} failures")
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
