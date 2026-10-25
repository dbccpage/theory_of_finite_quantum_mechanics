"""Independent check of one six-label guard.

Indices 0 through 5 name the six sealed labels.
A guard with bound 6 refuses 6. A guard with bound 7 accepts 6.
Does not import repository code and does not run a harness.
"""
from __future__ import annotations


NAMES = (
    "supply",
    "admitDatum",
    "admitForm",
    "admitInst",
    "admitRuleAll",
    "impose",
)


def sealed_index(name):
    return NAMES.index(name)


def of_index(index):
    return NAMES[index]


def append_sealed(label):
    return label < 6


def append_amended(label):
    return label < 7


def main():
    checks = []

    def add(condition):
        checks.append(bool(condition))

    for index, name in enumerate(NAMES):
        add(sealed_index(name) == index)
        add(of_index(sealed_index(name)) == name)
        add(sealed_index(of_index(index)) == index)
        add(append_sealed(index) is True)
        add(index != 6)
    add(append_sealed(6) is False)
    add(append_amended(6) is True)
    add(len(NAMES) == 6)
    failed = sum(1 for item in checks if not item)
    print(f"checked {len(checks)} conditions, {failed} failures")
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
