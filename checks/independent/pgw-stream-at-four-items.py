"""Independent check of one refusal pair and one search flag.

A refusal at item count 3 is not a refusal at item count 4.
The short-circuit flag skips a later target. Does not import
repository code and does not build a stream tree.
"""
from __future__ import annotations


def refuses_at(k, items, refused):
    return items == k and refused


def searched(short_circuit, refusal_at, target):
    if short_circuit:
        return target <= refusal_at
    return True


def main():
    checks = []

    def add(condition):
        checks.append(bool(condition))

    add(refuses_at(3, 3, True))
    add(not refuses_at(4, 3, True))
    add(refuses_at(4, 4, True))
    add(not refuses_at(4, 4, False))
    add(searched(True, 3, 4) is False)
    add(searched(False, 3, 4) is True)
    add(searched(True, 3, 3) is True)
    failed = sum(1 for item in checks if not item)
    print(f"checked {len(checks)} conditions, {failed} failures")
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
