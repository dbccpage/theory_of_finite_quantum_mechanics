"""Independent check for one letter, no rewrite step, and length bound 1.

No repository imports.
"""


def length(word: tuple[int, ...]) -> int:
    return len(word)


def in_bound(word: tuple[int, ...], bound: int = 1) -> bool:
    return length(word) <= bound


def reaches(source: tuple[int, ...], target: tuple[int, ...]) -> bool:
    return source == target


def main() -> None:
    failures = 0
    start = (0,)
    empty: tuple[int, ...] = ()
    long = (0, 0)
    bound = 1
    if length(start) != 1 or length(empty) != 0 or length(long) != 2:
        failures += 1
    if not in_bound(start, bound) or not in_bound(empty, bound) or in_bound(long, bound):
        failures += 1
    if not reaches(start, start):
        failures += 1
    if reaches(start, long) or reaches(start, empty):
        failures += 1
    inside = [word for word in (empty, start, long) if in_bound(word, bound)]
    reached = [word for word in inside if reaches(start, word)]
    if inside != [empty, start] or reached != [start]:
        failures += 1
    print(f"failures={failures}")
    print("bound 1")
    print("lengths start empty long are 1 0 2")
    print("inside the bound: empty and (0)")
    print("reached from (0): (0)")
    print("one letter and no rewrite step; this is not a normal-form search")
    raise SystemExit(failures)


if __name__ == "__main__":
    main()
