#!/usr/bin/env python3
"""Exact modulo-7 controls; no repository imports or continuum claims.

Integer reduction is independent of the Lean natural-subtraction encoding.
The latter agrees only on the stated residue domain, which is checked fully.
"""
from itertools import product
import json

MOD = 7
GENERATOR = (2, 2)
IDENTITY = (1, 0)
EXPECTED_POWERS = ((1, 0), (2, 2), (0, 1), (5, 2), (6, 0), (5, 5), (0, 6), (2, 5))


def multiply(a, b):
    return ((a[0]*b[0]-a[1]*b[1]) % MOD, (a[0]*b[1]+a[1]*b[0]) % MOD)


def lean_natural_product(a, b):
    return (max(0, a[0]*b[0]+252-a[1]*b[1]) % MOD,
            (a[0]*b[1]+a[1]*b[0]) % MOD)


def main():
    checks = 0

    def require(condition, label):
        nonlocal checks
        checks += 1
        if not condition:
            raise RuntimeError(label)

    candidates = tuple(product(range(MOD), repeat=2))
    solutions = {p for p in candidates if sum(x*x for x in p) % MOD == 1}
    require(len(candidates) == MOD*MOD, 'candidate enumeration')
    for a, b in product(candidates, repeat=2):
        require(lean_natural_product(a, b) == multiply(a, b), 'bounded natural subtraction')
    point = IDENTITY
    powers = []
    for _ in range(MOD+1):
        powers.append(point)
        point = multiply(point, GENERATOR)
    require(tuple(powers) == EXPECTED_POWERS, 'power sequence')
    require(point == IDENTITY, 'return at eighth step')
    require(all(p != IDENTITY for p in powers[1:]), 'no earlier positive return')
    require(len(set(powers)) == len(powers), 'distinct powers')
    require(set(powers) == solutions, 'all and only norm-one residues')
    require(len(solutions) == MOD+1 and len(solutions) != 4, 'solution cardinality')
    require(GENERATOR not in {(0, 1), (0, 6), (1, 0), (6, 0)}, 'non-axis generator')
    for a in solutions:
        inverse = (a[0], -a[1] % MOD)
        require(multiply(a, IDENTITY) == a == multiply(IDENTITY, a), 'identity')
        require(multiply(a, inverse) == IDENTITY == multiply(inverse, a), 'inverse')
    for a, b in product(solutions, repeat=2):
        require(multiply(a, b) in solutions, 'closure')
    for a, b, c in product(solutions, repeat=3):
        require(multiply(multiply(a, b), c) == multiply(a, multiply(b, c)), 'associativity')
    # Negative controls delimit the bounded encoding and the stated solution set.
    require(lean_natural_product((0, 20), (0, 20)) != multiply((0, 20), (0, 20)),
            'natural pad does not justify unrestricted inputs')
    require(set(powers[:-1]) != solutions, 'omitted solution is detected')
    require(set(powers) | {(0, 0)} != solutions, 'non-solution is detected')
    wrong_sign = ((GENERATOR[0]**2+GENERATOR[1]**2) % MOD,
                  2*GENERATOR[0]*GENERATOR[1] % MOD)
    require(wrong_sign != multiply(GENERATOR, GENERATOR), 'wrong real-part sign is detected')
    print(json.dumps({'status': 'passed', 'checks': checks, 'candidate_pairs': len(candidates),
                      'solutions': sorted(solutions), 'powers': powers, 'first_positive_return': len(powers),
                      'return_value': point, 'cardinality': len(solutions), 'negative_controls': 4,
                      'scope': 'Modulo 7 only; no scalar-field or U(1) selection.'}, indent=2))


if __name__ == '__main__':
    main()
