"""Independent check for one finite reading of PGW-DECLARED-INPUT-FLOOR.

Two named inputs and four stake-only carriers. No repository imports.
"""

from __future__ import annotations


def count(stake: bool, stream: bool) -> int:
    return (1 if stake else 0) + (1 if stream else 0)


def main() -> None:
    failures = 0
    checks = 0

    def expect(cond: bool, label: str) -> None:
        nonlocal failures, checks
        checks += 1
        if not cond:
            failures += 1
            print("fail", label)

    vocabulary = ("stake", "stream")
    engines = ((True, False), (True, False), (True, False), (True, False))
    rounds = 15
    guard = 250
    data_bound = 4
    item_bound = 2

    expect(vocabulary == ("stake", "stream"), "vocabulary")
    expect(len(vocabulary) == 2, "two names")
    expect(vocabulary[0] != vocabulary[1], "names differ")
    expect(len(engines) == 4, "four engines")
    expect(all(pair == (True, False) for pair in engines), "stake not stream")
    expect(all(count(stake, stream) == 1 for stake, stream in engines), "count 1")
    expect(count(True, False) == 1, "stake only")
    expect(count(True, True) == 2, "both inputs")
    expect(count(True, False) < count(True, True), "one below two")
    floor_reading = all(count(stake, stream) >= 2 for stake, stream in engines)
    one_input_reading = any(count(stake, stream) == 1 for stake, stream in engines)
    expect(floor_reading is False, "floor reading false")
    expect(one_input_reading is True, "one-input reading true")
    expect(rounds == 15 and guard == 250 and data_bound == 4 and item_bound == 2, "bounds")
    expect(count(False, False) == 0, "empty count")
    expect(count(False, False) < count(True, False), "empty below stake")
    expect(all(pair != (False, False) for pair in engines), "empty not among four")
    expect(15 < 250, "rounds below guard")
    expect(2 < 4, "item bound below data bound")

    print(f"checked {checks} conditions, {failures} failures")
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
