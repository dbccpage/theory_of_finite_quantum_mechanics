"""Enumerate Boolean observer families as partitions, without a computability claim."""
from itertools import combinations, product


def subsets(values):
    return [frozenset(c) for size in range(len(values) + 1)
            for c in combinations(values, size)]


def relation(family):
    signatures = {x: tuple(observer[x] for observer in sorted(family)) for x in (0, 1)}
    return {(x, y) for x, y in product((0, 1), repeat=2)
            if signatures[x] == signatures[y]}


def main() -> None:
    observers = tuple(product((0, 1), repeat=2))
    families = subsets(observers)
    diagonal = {(0, 0), (1, 1)}
    restrictions = 0
    for family in families:
        equivalent = relation(family)
        if not diagonal <= equivalent or any((y, x) not in equivalent for x, y in equivalent):
            raise SystemExit("partition reflexivity/symmetry failed")
        if any((x, z) not in equivalent for x, y in equivalent for yy, z in equivalent if y == yy):
            raise SystemExit("partition transitivity failed")
        for smaller in subsets(tuple(family)):
            if not equivalent <= relation(smaller):
                raise SystemExit("forgetting observers introduced a distinction")
            restrictions += 1
        if relation(family | {(0, 1)}) != diagonal:
            raise SystemExit("identity observer failed to separate")
    empty = relation(frozenset())
    exact = relation(frozenset({(0, 1)}))
    inscriptions = ("<>", "<a>")
    if inscriptions[0] == inscriptions[1]:
        raise SystemExit("exact inscriptions unexpectedly coincide")
    if len(empty) != 4 or len(exact) != 2 or (0, 1) not in empty or (0, 1) in exact:
        raise SystemExit("two conventions did not disagree on novelty")
    if any(answer == ((0, 1) not in empty) == ((0, 1) not in exact) for answer in (False, True)):
        raise SystemExit("a common novelty answer unexpectedly existed")
    print(f"observer_families={len(families)} restrictions={restrictions} "
          f"empty_relation_pairs={len(empty)} exact_relation_pairs={len(exact)} failures=0")


if __name__ == "__main__":
    main()
