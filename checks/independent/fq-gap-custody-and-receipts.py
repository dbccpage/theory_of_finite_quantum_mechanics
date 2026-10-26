"""Integer check of the named custody numerals. This file imports no repository code."""

from __future__ import annotations


def main() -> None:
    failures = 0
    gap = 48 - 24
    remainder = 53 - 22
    proper = 22 < 53
    if gap != 24:
        failures += 1
    if remainder != 31:
        failures += 1
    if not proper:
        failures += 1
    print(
        f"checks=3 failures={failures} gap={gap} remainder={remainder} proper={proper}"
    )
    raise SystemExit(failures)


if __name__ == "__main__":
    main()
