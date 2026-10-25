"""Independent check of one two-vertex ongoing-to-window bridge.

Slots are (e00, e11, e01, e10). The mark (0, 1, 0) reads e01 + e10 + e00.
Does not import repository code.
"""
from __future__ import annotations


def cob(g0, g1):
    return (0, 0, g0 - g1, g1 - g0)


def diag(e00, e01, e10):
    return e01 + e10 + e00


def main():
    checks = []

    def add(condition):
        checks.append(bool(condition))

    add(diag(1, 0, -1) == 0)
    add(diag(0, 0, 0) == 0)
    add(diag(0, 1, 0) == 1)
    add(1 + 1 == 2)
    add(1 - 1 == 0)
    add(1 + 1 != 0)
    for g0 in range(-4, 5):
        for g1 in range(-4, 5):
            c00, c11, c01, c10 = cob(g0, g1)
            add(c00 == 0 and c11 == 0 and c01 == g0 - g1 and c10 == g1 - g0)
            add(diag(c00, c01, c10) == 0)
            add(c00 != 1 and c11 != 1)
            for e00 in range(-2, 3):
                for e01 in range(-2, 3):
                    for e10 in range(-2, 3):
                        add(
                            diag(e00 + c00, e01 + c01, e10 + c10)
                            == diag(e00, e01, e10)
                        )
    for b in range(-3, 4):
        if b == 0:
            continue
        for d00 in range(-2, 3):
            for d11 in range(-2, 3):
                for d01 in range(-2, 3):
                    for d10 in range(-2, 3):
                        for n0 in range(-2, 3):
                            for n1 in range(-2, 3):
                                if (
                                    b * d00 == 0
                                    and b * d11 == 0
                                    and b * d01 == n0 - n1
                                    and b * d10 == n1 - n0
                                ):
                                    add((d00, d11, d01, d10) == cob(0, -d01))
    failed = sum(1 for item in checks if not item)
    print(f"checked {len(checks)} conditions, {failed} failures")
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
