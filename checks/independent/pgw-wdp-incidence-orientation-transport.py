"""Independent check of one incidence-to-WDP triangle transport.

Edge order (01, 02, 12) reorders to (01, 12, 02).
The face column (1, -1, 1) becomes (1, 1, -1).
Does not import repository code.
"""
from __future__ import annotations


def iabs(n):
    return -n if n < 0 else n


def inc_boundary(x01, x02, x12):
    return (-x01 - x02, x01 - x12, x02 + x12)


def reorder(a01, a02, a12):
    return (a01, a12, a02)


def dot3(u, v):
    return u[0] * v[0] + u[1] * v[1] + u[2] * v[2]


def wdp_d0(f0, f1, f2):
    return (f1 - f0, f2 - f1, f2 - f0)


def wdp_d1(x01, x12, x02):
    return x01 + x12 - x02


def residual(f0, f1, f2):
    return (
        iabs(1 - (f1 - f0))
        + iabs(1 - (f2 - f1))
        + iabs(0 - (f2 - f0))
    )


def pairing(f0, f1, f2):
    return (1 - (f1 - f0)) + (1 - (f2 - f1)) - (0 - (f2 - f0))


def main():
    checks = []

    def add(condition):
        checks.append(bool(condition))

    add(inc_boundary(1, 0, 0) == (-1, 1, 0))
    add(inc_boundary(0, 1, 0) == (-1, 0, 1))
    add(inc_boundary(0, 0, 1) == (0, -1, 1))
    add(reorder(1, -1, 1) == (1, 1, -1))
    add(inc_boundary(1, -1, 1) == (0, 0, 0))
    add(wdp_d1(1, 1, 0) == 2)
    add(wdp_d1(1, 1, -1) == 3)
    add(1 + 1 + (-(-1)) == wdp_d1(1, 1, -1))
    for f0 in range(-4, 5):
        for f1 in range(-4, 5):
            for f2 in range(-4, 5):
                vertex = (f0, f1, f2)
                transported = (
                    dot3(inc_boundary(1, 0, 0), vertex),
                    dot3(inc_boundary(0, 0, 1), vertex),
                    dot3(inc_boundary(0, 1, 0), vertex),
                )
                add(transported == wdp_d0(f0, f1, f2))
                add(wdp_d1(*wdp_d0(f0, f1, f2)) == 0)
                add(pairing(f0, f1, f2) == 2)
                add(residual(f0, f1, f2) >= 2)
                x01, x12, x02 = f0, f1, f2
                add(x01 + x12 + (-x02) == wdp_d1(x01, x12, x02))
    add(residual(0, 1, 0) == 2)
    failed = sum(1 for item in checks if not item)
    print(f"checked {len(checks)} conditions, {failed} failures")
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
