"""Independent finite counts for the declared ceiling examples.

Binomial sums count binary choices; explicit products count the small table.
The Rust verifiers and their configured limits are not exercised here.
"""
from itertools import product
from math import comb


def binary_choices(size: int) -> int:
    return sum(comb(size, selected) for selected in range(size + 1))


def main() -> None:
    global_limit = binary_choices(20)
    lp_limit = binary_choices(22)
    sections21 = binary_choices(21)
    rows = tuple(product(range(10), (0, 1)))
    assignments = tuple(product((0, 1), repeat=10))
    entries = sum(1 for _ in product(rows, assignments))
    checks = {
        "global power": global_limit == 1 << 20,
        "global decimal": global_limit == 1048576,
        "LP power": lp_limit == 1 << 22,
        "LP decimal": lp_limit == 4194304,
        "64 choices exceed global": binary_choices(64) > global_limit,
        "21 choices decimal": sections21 == 2097152,
        "21 choices exceed global": sections21 > global_limit,
        "ten binary rows": len(rows) == 20,
        "ten binary assignments": len(assignments) == 1024,
        "table entries": entries == 20480,
        "assignments below global": len(assignments) < global_limit,
        "entries below LP": entries < lp_limit,
    }
    failures = [name for name, passed in checks.items() if not passed]
    for name in failures:
        print("FAIL", name)
    print(
        f"checks={len(checks)} failures={len(failures)} G={global_limit} L={lp_limit} "
        f"sections21={sections21} rows={len(rows)} cols={len(assignments)} entries={entries}"
    )
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
