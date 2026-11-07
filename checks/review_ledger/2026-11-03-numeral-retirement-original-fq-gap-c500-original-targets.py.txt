"""Integer check of the C500 block-numeral slice. This file imports no repository code."""

from __future__ import annotations

import sympy as sp


def lo(k: int) -> int:
    return 276 + 25 * k


def hi(k: int) -> int:
    return 300 + 25 * k


def main() -> None:
    failures = 0
    k = sp.symbols("k", integer=True, nonnegative=True)
    symbolic_lo = 276 + 25 * k
    symbolic_hi = 300 + 25 * k
    if sp.expand(symbolic_hi - symbolic_lo + 1 - 25) != 0:
        failures += 1
    if sp.expand(symbolic_hi + 1 - (276 + 25 * (k + 1))) != 0:
        failures += 1
    for sample in range(0, 21):
        if hi(sample) - lo(sample) + 1 != 25:
            failures += 1
        if hi(sample) + 1 != lo(sample + 1):
            failures += 1
    if lo(1) != 301 or hi(10) != 550:
        failures += 1
    cover = hi(10) - lo(1) + 1
    if cover != 250 or 10 * 25 != 250:
        failures += 1
    counts = [0, 2, 4, 2, 4, 1, 1, 1, 1, 5]
    if len(counts) != 10 or sum(counts) != 21 or counts[-1] != 5:
        failures += 1
    if any(item >= 5 for item in counts[:-1]):
        failures += 1
    labels = ["M2", "M5", "M7", "J1", "J2"]
    if len(labels) != 5 or len(set(labels)) != 5:
        failures += 1
    print(
        "checks=8 failures="
        f"{failures} cover={cover} product={10 * 25} clause_sum={sum(counts)} "
        f"last={counts[-1]} labels={len(labels)}"
    )
    raise SystemExit(failures)


if __name__ == "__main__":
    main()
