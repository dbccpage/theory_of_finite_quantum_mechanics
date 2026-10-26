#!/usr/bin/env python3
"""Exact four-variable parity census with independent integer parity controls.

No repository module is imported. This finite box is not a proof of the
noncontextual-fraction equivalences, Vorob'ev theorem or a Rust refinement.
"""
from itertools import product, combinations
import json

EDGES = ((0, 2), (0, 3), (1, 2), (1, 3))
TARGET = (0, 0, 0, 1)


def parities(assignment):
    return tuple((assignment[i]+assignment[j]) % 2 for i, j in EDGES)


def main():
    checks = 0

    def require(condition, label):
        nonlocal checks
        checks += 1
        if not condition:
            raise RuntimeError(label)

    assignments = tuple(product((0, 1), repeat=4))
    hits = []
    satisfied_counts = []
    for values in assignments:
        actual = parities(values)
        a, ap, b, bp = map(bool, values)
        direct = (a ^ b, a ^ bp, ap ^ b, ap ^ bp)
        require(tuple(map(int, direct)) == actual, 'integer and Boolean routes agree')
        require(sum(actual) % 2 == 0, 'even left parity')
        require((direct[0] ^ direct[1] ^ direct[2] ^ direct[3]) is False, 'Boolean left parity')
        if actual == TARGET:
            hits.append(values)
        satisfied_counts.append(sum(x == y for x, y in zip(actual, TARGET)))
    require(len(assignments) == 2**4 == 16, 'actual assignment cardinality')
    require(sum(TARGET) % 2 == 1, 'odd right parity')
    require(not hits, 'no common assignment')
    # Every three equations are satisfiable: an omitted constraint must change the result.
    triple_counts = []
    for indices in combinations(range(4), 3):
        count = sum(all(parities(v)[i] == TARGET[i] for i in indices) for v in assignments)
        triple_counts.append(count)
        require(count == 2, 'each three-constraint subsystem has two solutions')
    consistent = sum(parities(v) == (0, 0, 0, 0) for v in assignments)
    require(consistent == 2, 'changing the odd right side makes the box satisfiable')
    require(max(satisfied_counts) == 3, 'at most three original constraints hold')
    print(json.dumps({'status': 'passed', 'checks': checks, 'assignments': len(assignments),
                      'solutions': len(hits), 'left_parity': 0, 'right_parity': sum(TARGET) % 2,
                      'three_constraint_solution_counts': triple_counts,
                      'consistent_variant_solutions': consistent,
                      'scope': 'One finite parity box; the broader OPS Lean obligations remain open.'}, indent=2))


if __name__ == '__main__':
    main()
