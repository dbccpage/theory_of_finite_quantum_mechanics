# Independent integer check for three keep-and-scale steps.
# No repository imports.


def check() -> int:
    u = 1
    v = 1
    w = 1
    rows = [(0, u, v, w)]
    for _ in range(3):
        u = 3 * u
        v = 4 * v
        w = 3 * w + 0
        rows.append((len(rows), u, v, w))
    expected = (
        (0, 1, 1, 1),
        (1, 3, 4, 3),
        (2, 9, 16, 9),
        (3, 27, 64, 27),
    )
    failures = 0
    if rows != list(expected):
        failures += 1
        print(f"fail rows got={rows}")
    for step, uu, vv, ww in rows[1:]:
        if not uu < vv or ww != uu:
            failures += 1
            print(f"fail step={step} u={uu} v={vv} w={ww}")
    if 3 * 9 != 27 or 4 * 16 != 64:
        failures += 1
        print("fail products")
    print(
        "qcv-import-noisy-reversible-limits"
        f" failures={failures}"
        f" steps=3"
        f" u3={rows[3][1]}"
        f" v3={rows[3][2]}"
        f" rows={len(rows)}"
    )
    return failures


if __name__ == "__main__":
    raise SystemExit(check())
