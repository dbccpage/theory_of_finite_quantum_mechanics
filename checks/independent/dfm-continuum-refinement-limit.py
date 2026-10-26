"""Exact finite controls for the binary-refinement transport limit.

AuthorityEffect: None. No repository code is imported. Finite computations
supplement, and do not establish, the universal convergence theorems in Lean.
"""
from fractions import Fraction as Q
from itertools import product, permutations
import json


class CheckFailure(RuntimeError):
    """A declared identity, error bound or negative control failed."""


checks = 0


def require(condition: bool, message: str) -> None:
    global checks
    checks += 1
    if not condition:
        raise CheckFailure(message)


def endpoints(word: tuple[bool, ...]) -> tuple[Q, Q]:
    numerator = sum(int(bit) * 2**i for i, bit in enumerate(word))
    denominator = 2**len(word)
    return Q(numerator, denominator), Q(numerator + 1, denominator)


def leaves(word: tuple, depth: int) -> list[tuple]:
    if depth == 0:
        return [word]
    return leaves((False,) + word, depth - 1) + leaves((True,) + word, depth - 1)


def scalar_transport(edge, word: tuple, depth: int) -> Q:
    return sum((edge(leaf) for leaf in leaves(word, depth)), Q(0))


def scalar_controls() -> dict:
    examples = []
    for q, slope, offset in product([Q(0), Q(1, 8), Q(1, 4), Q(3, 8)],
                                    [Q(-3), Q(0), Q(5, 2)], [Q(-2), Q(0), Q(7, 3)]):
        c = abs(offset) * (1 - 2*q)
        edge = lambda w: slope / 2**len(w) + offset * q**len(w)
        for k in range(4):
            for word in product([False, True], repeat=k):
                limit = slope / 2**k
                local = abs(edge(word) - edge((True,) + word) - edge((False,) + word))
                require(local <= c*q**k, "split-defect envelope")
                for n in range(6):
                    value = scalar_transport(edge, word, n)
                    require(value == limit + offset*q**k*(2*q)**n, "direct leaf sum")
                    require(abs(value - limit) == c*q**k*(2*q)**n/(1-2*q), "sharp tail bound")
                    increment = abs(value - scalar_transport(edge, word, n+1))
                    require(increment == c*q**k*(2*q)**n, "binary accumulation factor")
                    left, right = endpoints(word)
                    gauge = lambda x: 2*x*x - 3*x + 1
                    dressed = lambda w: edge(w) - gauge(endpoints(w)[1]) + gauge(endpoints(w)[0])
                    require(scalar_transport(dressed, word, n) == value - gauge(right) + gauge(left),
                            "nonconstant endpoint gauge telescopes")
    # Word-dependent perturbations are bounded but do not all saturate the estimate.
    for q in [Q(1, 8), Q(1, 4), Q(3, 8)]:
        edge = lambda w: Q(3, 2**len(w)) + (-1)**sum(w) * q**len(w)
        c = 1 + 2*q
        for k in range(4):
            for word in product([False, True], repeat=k):
                require(abs(edge(word)-edge((True,)+word)-edge((False,)+word)) <= c*q**k,
                        "nonconstant defect bound")
                for n in range(6):
                    require(abs(scalar_transport(edge, word, n)-Q(3, 2**k)) <=
                            c*q**k*(2*q)**n/(1-2*q), "nonconstant tail bound")
    q = Q(1, 4)
    edge = lambda w: q**len(w)
    values = [scalar_transport(edge, (), n) for n in range(7)]
    examples.append({"q": str(q), "C": "1/2", "root_transports": list(map(str, values)), "limit": "0"})
    require(abs(values[1]-values[2]) > Q(1, 2)*q, "omitting binary factor must fail")
    critical = lambda w: Q(len(w), 2**len(w))
    for n in range(9):
        require(scalar_transport(critical, (), n) == n, "threshold transports grow as n")
        for word in product([False, True], repeat=n):
            require(abs(critical(word)-critical((True,)+word)-critical((False,)+word)) == Q(1, 2**n),
                    "threshold leaf defects shrink")
    return {"sharp_geometric_example": examples, "threshold_q": "1/2", "threshold_root_transport": "n",
            "negative_controls": ["missing binary factor", "q=1/2 is not convergent"]}


PERMS = tuple(permutations(range(3)))
UNIT = (0, 1, 2)


def mul(a: tuple, b: tuple) -> tuple:
    return tuple(a[b[i]] for i in range(3))


def inv(a: tuple) -> tuple:
    return tuple(a.index(i) for i in range(3))


def ordered_transport(edge, word: tuple, depth: int) -> tuple:
    result = UNIT
    for leaf in leaves(word, depth):
        result = mul(edge(leaf), result)
    return result


def noncommutative_controls() -> dict:
    for a, b, c in product(PERMS, repeat=3):
        require(mul(a, mul(b, c)) == mul(mul(a, b), c), "S3 associativity")
    for a in PERMS:
        require(mul(a, inv(a)) == UNIT == mul(inv(a), a), "S3 inverse")
    gauge = lambda x: PERMS[(3*x.numerator + x.denominator) % 6]
    edge = lambda w: PERMS[(len(w) + sum((i+1)*int(b) for i,b in enumerate(w))) % 6]
    dressed = lambda w: mul(mul(inv(gauge(endpoints(w)[1])), edge(w)), gauge(endpoints(w)[0]))
    wrong_order_detected = wrong_inverse_detected = False
    for k in range(4):
        for word in product([False, True], repeat=k):
            left, right = endpoints(word)
            for n in range(5):
                value = ordered_transport(edge, word, n)
                expected = mul(mul(inv(gauge(right)), value), gauge(left))
                actual = ordered_transport(dressed, word, n)
                require(actual == expected, "noncommutative endpoint covariance")
                reversed_value = UNIT
                for leaf in reversed(leaves(word, n)):
                    reversed_value = mul(edge(leaf), reversed_value)
                wrong_order_detected |= reversed_value != value
                wrong_inverse_detected |= mul(mul(gauge(right), value), gauge(left)) != actual
    require(wrong_order_detected, "swapping ordered products must be detected")
    require(wrong_inverse_detected, "omitting target inverse must be detected")
    # Exact coherent transports have zero split defect, independently of depth.
    coherent = lambda w: mul(gauge(endpoints(w)[1]), inv(gauge(endpoints(w)[0])))
    for n in range(7):
        require(ordered_transport(coherent, (), n) == coherent(()), "zero-defect coherent S3 tower")
    return {"group": "S3", "ordered_covariance": "passed", "zero_defect": "passed",
            "negative_controls": ["reversed order", "missing inverse"]}


def main() -> None:
    scalar = scalar_controls()
    noncommutative = noncommutative_controls()
    print(json.dumps({"AuthorityEffect": "None", "status": "passed", "checks": checks,
                      "scalar": scalar, "noncommutative": noncommutative,
                      "scope": "Exact finite controls; completeness, convergence and continuity are checked in Lean."}, indent=2))


if __name__ == "__main__":
    main()
