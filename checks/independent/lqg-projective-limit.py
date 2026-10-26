"""Exact finite checks for a supplied projective spin-label probability family.

AuthorityEffect: None. No repository imports. Infinite extension/uniqueness is
proved separately in Lean. This correlated label model is not an LQG amplitude.
"""
from collections import defaultdict
from fractions import Fraction as Q
from itertools import combinations, product
import json


class CheckFailure(RuntimeError):
    """A probability, marginal, constraint or negative control failed."""


checks = 0


def require(condition: bool, message: str) -> None:
    global checks
    checks += 1
    if not condition:
        raise CheckFailure(message)


K = ((Q(1, 2), Q(1, 3), Q(1, 6)),
     (Q(1, 4), Q(1, 2), Q(1, 4)),
     (Q(1, 6), Q(1, 3), Q(1, 2)))
INITIAL = (Q(1, 2), Q(1, 3), Q(1, 6))


def probability(law: dict[tuple, Q]) -> bool:
    return all(isinstance(x, Q) and x >= 0 for x in law.values()) and sum(law.values(), Q(0)) == 1


def paths(blocks: int, initial=INITIAL) -> dict[tuple, Q]:
    require(1 <= blocks <= 4, "finite audit depth envelope")
    result = {}
    for states in product(range(3), repeat=blocks):
        weight = initial[states[0]]
        for a, b in zip(states, states[1:]):
            weight *= K[a][b]
        # Three labels per supplied local triangle. No manifold incidence is claimed.
        labels = tuple(label for state in states for label in (state, state, 0))
        result[labels] = weight
    return result


def marginal(law: dict[tuple, Q], indices: tuple[int, ...]) -> dict[tuple, Q]:
    result = defaultdict(Q)
    for state, weight in law.items():
        result[tuple(state[i] for i in indices)] += weight
    return dict(result)


def admissible(a: int, b: int, c: int) -> bool:
    return (all(0 <= x <= 2 for x in (a, b, c)) and a <= b+c and b <= a+c and c <= a+b
            and (a+b+c) % 2 == 0 and a+b+c <= 4)


def matrix_mul(a: tuple, b: tuple) -> tuple:
    return tuple(tuple(sum((a[i][k]*b[k][j] for k in range(3)), Q(0)) for j in range(3)) for i in range(3))


def matrix_power(n: int) -> tuple:
    result = tuple(tuple(Q(i == j) for j in range(3)) for i in range(3))
    for _ in range(n):
        result = matrix_mul(result, K)
    return result


def main() -> None:
    require(sum(INITIAL) == 1 and all(x > 0 for x in INITIAL), "initial probability")
    for row in K:
        require(sum(row) == 1 and all(x > 0 for x in row), "Markov row probability")
    require(sum(admissible(*t) for t in product(range(3), repeat=3)) == 10, "level-two admissibility census")
    laws = {n: paths(n) for n in range(1, 5)}
    cases = []
    for n, law in laws.items():
        require(probability(law), "normalized nonnegative joint law")
        require(len(law) == 3**n, "explicit support count")
        for m in range(1, n+1):
            require(marginal(law, tuple(range(3*m))) == laws[m], "full earlier-level marginal")
        tested_subsets = 0
        for size in range(4):
            for indices in combinations(range(3*n), size):
                short = marginal(law, indices)
                require(probability(short), "arbitrary-coordinate marginal probability")
                # Marginalize a finer joint law directly; no recursive projection reuse.
                require(short == marginal(laws[4], indices), "projective consistency on arbitrary coordinate subsets")
                tested_subsets += 1
        for block in range(n):
            mass = sum((weight for state, weight in law.items() if admissible(*state[3*block:3*block+3])), Q(0))
            require(mass == 1, "each supplied triangle constraint has full mass")
        require(sum((weight for state, weight in law.items()
                     if all(admissible(*state[3*i:3*i+3]) for i in range(n))), Q(0)) == 1,
                "finite conjunction has full mass")
        # A separate transfer-matrix computation checks long-range correlations.
        pair = marginal(law, (0, 3*(n-1)))
        transition = matrix_power(n-1)
        for a, b in product(range(3), repeat=2):
            require(pair.get((a, b), Q(0)) == INITIAL[a]*transition[a][b], "transfer matrix versus full path enumeration")
        cases.append({"blocks": n, "label_coordinates": 3*n, "positive_support": len(law),
                      "tested_coordinate_subsets_size_at_most_three": tested_subsets, "total_mass": "1"})
    joint = marginal(laws[2], (0, 3));first=marginal(laws[2], (0,));second=marginal(laws[2], (3,))
    require(any(joint[a,b] != first[a,]*second[b,] for a,b in product(range(3),repeat=2)),
            "the example really is correlated")
    incompatible = {tuple([0]*6): Q(1)}
    require(probability(incompatible), "negative control remains normalized")
    require(marginal(incompatible, (0,)) != marginal(laws[1], (0,)), "normalization does not imply compatibility")
    signed = {(0,): Q(2), (1,): Q(-1)}
    require(sum(signed.values()) == 1 and not probability(signed), "signed total one is not a probability law")
    bad_constraint = {(0, 0, 1): Q(1)}
    require(probability(bad_constraint) and not admissible(0, 0, 1), "a constraint needs its own full-mass premise")
    alternative = paths(4, (Q(1, 3),)*3)
    require(probability(alternative) and set(alternative) == set(laws[4]), "same finite support, second law")
    require(marginal(alternative, (0,)) != marginal(laws[4], (0,)), "finite counts do not select the law")
    print(json.dumps({"AuthorityEffect": "None", "status": "passed", "checks": checks,
                      "method": "rational Markov path enumeration and independent transfer matrices", "cases": cases,
                      "negative_controls": ["normalized incompatible marginals", "negative weights with unit total",
                                            "missing constraint premise", "same support does not determine weights"],
                      "scope": "Finite controls for the declared correlated model; no physical LQG or continuum spacetime claim."}, indent=2))


if __name__ == "__main__":
    main()
