"""Independent integer check for the narrowed GTH-LANG-CORE carrier."""


def slot_sum(data, forms, instances, rules, requirements):
    return data + forms + instances + rules + requirements


def reach(v):
    return 0


def main():
    carrier = (1, 0, 0, 0, 0)
    with_rule = (1, 0, 0, 1, 0)
    failures = 0
    checks = 0

    def expect(cond):
        nonlocal failures, checks
        checks += 1
        if not cond:
            failures += 1

    expect(carrier[0] == 1)
    expect(carrier[1] == 0)
    expect(carrier[2] == 0)
    expect(carrier[3] == 0)
    expect(carrier[4] == 0)
    expect(slot_sum(*carrier) == 1)
    expect(with_rule != carrier)
    expect(with_rule[0] == 1)
    expect(with_rule[1] == 0)
    expect(with_rule[2] == 0)
    expect(with_rule[3] == 1)
    expect(with_rule[4] == 0)
    expect(slot_sum(*with_rule) == 2)
    expect(reach(0) == 0)
    expect(reach(1) == 0)
    print(f"checked {checks} conditions, {failures} failures")
    return failures


if __name__ == "__main__":
    raise SystemExit(main())
