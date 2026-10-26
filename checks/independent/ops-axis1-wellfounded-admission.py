"""Three-candidate admission chain.

Recomputes the predecessor table, the recurrence, and the two closed base
assignments. No repository imports. Boolean disjunction only; SymPy is unused.
AuthorityEffect: None.

Source labels echoed as text, not arithmetic: WDP-CH14 L035 L035-C1.
"""

from __future__ import annotations


def pred(i: int):
    if i == 0:
        return None
    if i == 1:
        return 0
    if i == 2:
        return 1
    raise AssertionError(i)


def admitted(b: dict[int, bool], i: int) -> bool:
    if i == 0:
        return b[0]
    if i == 1:
        return b[1] or b[0]
    if i == 2:
        return b[2] or (b[1] or b[0])
    raise AssertionError(i)


def main() -> int:
    failures: list[str] = []

    def check(name: str, cond: bool) -> None:
        if not cond:
            failures.append(name)

    check("pred0", pred(0) is None)
    check("pred1", pred(1) == 0)
    check("pred2", pred(2) == 1)

    none_base = {0: False, 1: False, 2: False}
    zero_base = {0: True, 1: False, 2: False}
    check("zb0", zero_base[0] is True)
    check("zb1", zero_base[1] is False)
    check("zb2", zero_base[2] is False)

    for mask in range(8):
        b = {0: bool(mask & 1), 1: bool(mask & 2), 2: bool(mask & 4)}
        a0 = admitted(b, 0)
        a1 = admitted(b, 1)
        a2 = admitted(b, 2)
        check(f"adm0-{mask}", a0 is b[0])
        check(f"adm1-{mask}", a1 is (b[1] or a0))
        check(f"adm2-{mask}", a2 is (b[2] or a1))

    for i in (0, 1, 2):
        check(f"none{i}", admitted(none_base, i) is False)
        check(f"zero{i}", admitted(zero_base, i) is True)

    print(
        "ops-axis1-wellfounded-admission failures="
        + str(len(failures))
        + " bases=8 rows=15"
    )
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
