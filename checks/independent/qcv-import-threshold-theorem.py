# Independent integer check for one concatenation-style orbit.
# No repository imports.

def t(n: int) -> int:
    return 2 * n * n


def check() -> int:
    failures = 0
    rows = (
        ("t_spec", t(8), 2 * 8 * 8),
        ("step_zero", t(0), 0),
        ("step_one", t(1), 2),
        ("step_two", t(2), 8),
        ("step_eight", t(8), 128),
        ("orbit_three", t(t(t(1))), 128),
        ("mul_eight", 2 * 8 * 8, 128),
        ("scale_zero", 2 * 0, 0),
        ("scale_one", 2 * 1, 2),
    )
    for name, got, want in rows:
        if got != want:
            failures += 1
            print(f"fail {name} got={got} want={want}")
    print(
        "qcv-import-threshold-theorem"
        f" failures={failures}"
        f" orbit={t(t(t(1)))}"
        f" scale0={2 * 0}"
        f" scale1={2 * 1}"
        f" rows={len(rows)}"
    )
    return failures


if __name__ == "__main__":
    raise SystemExit(check())
