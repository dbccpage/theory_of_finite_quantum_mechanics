# Status: independent check for TFQ-0385. No repository imports.
"""Two data, one unary instance on the first, then a uniform rule on form 0."""

from __future__ import annotations


def derivable(rule0, inst0, datum):
    return rule0 or (inst0 and datum == 0)


def profile_bit(rule0, inst0, datum):
    return derivable(rule0, inst0, datum)


def class_count(rule0, inst0):
    if profile_bit(rule0, inst0, 0) == profile_bit(rule0, inst0, 1):
        return 1
    return 2


def main():
    failures = 0
    checked = 0

    def expect(cond):
        nonlocal failures, checked
        checked += 1
        if not cond:
            failures += 1

    data = (0, 1)
    expect(len(data) == 2)
    expect(data[0] == 0 and data[1] == 1)
    for datum in data:
        expect(datum == 0 or datum == 1)

    expect(profile_bit(False, True, 0) is True)
    expect(profile_bit(False, True, 1) is False)
    expect(profile_bit(False, True, 0) != profile_bit(False, True, 1))
    expect(class_count(False, True) == 2)

    expect(profile_bit(True, True, 0) is True)
    expect(profile_bit(True, True, 1) is True)
    expect(profile_bit(True, True, 0) == profile_bit(True, True, 1))
    expect(class_count(True, True) == 1)

    expect(class_count(False, True) != class_count(True, True))
    expect(profile_bit(False, True, 0) == profile_bit(True, True, 0))
    expect(profile_bit(False, True, 1) != profile_bit(True, True, 1))

    print(f"checked {checked} conditions, {failures} failures")
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
