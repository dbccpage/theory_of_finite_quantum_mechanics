"""Independent integer check for the narrowed sector-weight witness."""


def main():
    weight_a = (2, 0)
    weight_b = (0, 2)
    failures = 0
    checks = 0

    def expect(cond):
        nonlocal failures, checks
        checks += 1
        if not cond:
            failures += 1

    expect(weight_a[0] + weight_a[1] == 2)
    expect(weight_b[0] + weight_b[1] == 2)
    expect(weight_a != weight_b)
    expect(4 * 0 != 2)
    expect(4 * 1 != 2)
    expect(4 * 2 == 8)
    expect(8 > 2)
    expect(4 * 1 == 4)
    print(f"checked {checks} conditions, {failures} failures")
    return failures


if __name__ == "__main__":
    raise SystemExit(main())
