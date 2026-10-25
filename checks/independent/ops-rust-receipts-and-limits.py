"""Exact ceiling arithmetic for OPS-RUST-RECEIPTS-AND-LIMITS.

No repository imports. The Rust verifiers are not run.
"""

def main() -> None:
    checks = 0

    def check(ok: bool) -> None:
        nonlocal checks
        checks += 1
        if not ok:
            raise SystemExit(f"failure at check {checks}")

    g = 2**20
    ell = 2**22
    check(g == 1048576)
    check(ell == 4194304)
    check(2**21 == 2097152)
    check(2**64 > g)
    check(2**21 > g)
    check(10 * 2 == 20)
    check(2**10 == 1024)
    check(20 * 1024 == 20480)
    check(1024 < g)
    check(20480 < ell)
    check(2**10 < g)
    check(20 * 1024 < ell)
    print(
        f"checks={checks} failures=0 G={g} L={ell} "
        f"sections21={2**21} rows=20 cols=1024 entries=20480"
    )


if __name__ == "__main__":
    main()
