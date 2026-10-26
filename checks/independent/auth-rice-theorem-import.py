# Independent check of one three-code behavior table.
# No repository imports.
# External witness version labels, not arithmetic: 4.33.1 and 4.35.0.


def beh(code: int, index: int) -> int:
    return {
        (0, 0): 0,
        (0, 1): 1,
        (1, 0): 0,
        (1, 1): 1,
        (2, 0): 0,
        (2, 1): 0,
    }[(code, index)]


def id_bit(code: int) -> bool:
    return beh(code, 0) == 0 and beh(code, 1) == 1


def code_zero(code: int) -> bool:
    return code == 0


def check() -> int:
    failures = 0
    rows = (
        ("beh00", beh(0, 0), 0),
        ("beh01", beh(0, 1), 1),
        ("beh10", beh(1, 0), 0),
        ("beh11", beh(1, 1), 1),
        ("beh20", beh(2, 0), 0),
        ("beh21", beh(2, 1), 0),
        ("id0", id_bit(0), True),
        ("id1", id_bit(1), True),
        ("id2", id_bit(2), False),
        ("z0", code_zero(0), True),
        ("z1", code_zero(1), False),
        ("z2", code_zero(2), False),
    )
    for name, got, want in rows:
        if got != want:
            failures += 1
            print(f"fail {name} got={got} want={want}")
    print(
        "auth-rice-theorem-import"
        f" failures={failures}"
        f" codes=3"
        f" rows={len(rows)}"
        f" id_true={sum(1 for c in (0, 1, 2) if id_bit(c))}"
        f" code_zero_true={sum(1 for c in (0, 1, 2) if code_zero(c))}"
    )
    return failures


if __name__ == "__main__":
    raise SystemExit(check())
