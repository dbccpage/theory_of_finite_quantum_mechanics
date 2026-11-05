"""Bounded exact binary-refinement transport controls over rationals and S3.

AuthorityEffect: None. Complete metric, refinement family and decay hypotheses
are supplied to the separate Lean results; these finite runs do not prove them.
"""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from fractions import Fraction as Q
from itertools import product, permutations
import json
from pathlib import Path as _Path
import sys as _sys
from typing import cast

_sys.path.insert(0, str(_Path(__file__).resolve().parents[1]))
from checker_support.boundary import Violation, cli, evaluate
from checker_support.cases import Cases as CheckRun
from checker_support.domains import binary_word, integer, permutation3, rational
from checker_support.outcome import Outcome

Word = tuple[bool, ...]
Permutation = tuple[int, int, int]
PERMS: tuple[Permutation, ...] = tuple((a, b, c) for a, b, c in permutations(range(3)))
UNIT: Permutation = (0, 1, 2)


def _callback(edge: object) -> Callable[[Word], object]:
    if not callable(edge):
        raise Violation("input", "edge assignment must be a callable")
    return cast(Callable[[Word], object], edge)


@dataclass(frozen=True, slots=True, init=False)
class DyadicCell:
    """Value object owning a little-endian bool word of at most64 bits."""
    word: Word

    def __init__(self, word: object) -> None:
        object.__setattr__(self, "word", binary_word(word))

    def endpoints(self) -> tuple[Q, Q]:
        numerator = sum(int(bit)*2**index for index, bit in enumerate(self.word))
        denominator = 2**len(self.word)
        return Q(numerator, denominator), Q(numerator+1, denominator)

    def _refined_words(self, depth: object) -> tuple[Word, ...]:
        levels = integer(depth, "refinement depth", 0, 12)
        if len(self.word)+levels > 64:
            raise Violation("resource", "refined words are bounded to64 bits")
        return tuple(tuple(reversed(bits))+self.word for bits in product((False, True), repeat=levels))

    def refine(self, depth: object) -> Outcome[tuple[Word, ...]]:
        return evaluate(self._refined_words, depth)

    def _scalar(self, edge: object, depth: object) -> Q:
        function = _callback(edge)
        total = Q(0)
        for leaf in self._refined_words(depth):
            value = rational(function(leaf), "scalar edge value")
            total = rational(total+value, "scalar transport accumulation")
        return total

    def scalar(self, edge: object, depth: object) -> Outcome[Q]:
        return evaluate(self._scalar, edge, depth)

    def _ordered(self, edge: object, depth: object) -> Permutation:
        function = _callback(edge)
        result = UNIT
        for leaf in self._refined_words(depth):
            result = mul(function(leaf), result)
        return result

    def ordered(self, edge: object, depth: object) -> Outcome[Permutation]:
        return evaluate(self._ordered, edge, depth)


def endpoints(word: object) -> tuple[Q, Q]:
    return DyadicCell(word).endpoints()


def leaves(word: object, depth: object) -> list[Word]:
    return list(DyadicCell(word)._refined_words(depth))


def scalar_transport(edge: object, word: object, depth: object) -> Q:
    return DyadicCell(word)._scalar(edge, depth)


def mul(a: object, b: object) -> Permutation:
    left, right = permutation3(a), permutation3(b)
    return left[right[0]], left[right[1]], left[right[2]]


def inv(a: object) -> Permutation:
    value = permutation3(a)
    return value.index(0), value.index(1), value.index(2)


def ordered_transport(edge: object, word: object, depth: object) -> Permutation:
    return DyadicCell(word)._ordered(edge, depth)


def _cases(counter: CheckRun | None) -> CheckRun:
    if counter is None:
        return CheckRun()
    if type(counter) is not CheckRun:
        raise Violation("input", "a Cases recorder is required")
    return counter


def _words() -> tuple[Word, ...]:
    """The fifteen fixed-fixture words of length at most3."""
    return tuple(tuple(word) for length in range(4) for word in product((False, True), repeat=length))


def _scalar_gauge(value: Q) -> Q:
    return 2*value*value-3*value+1


def _geometric_edge(word: Word, q: Q, slope: Q, offset: Q) -> Q:
    return rational(slope/2**len(word)+offset*q**len(word), "geometric fixture edge")


def _scalar_dressed(edge: Callable[[Word], Q], word: Word) -> Q:
    left, right = endpoints(word)
    return edge(word)-_scalar_gauge(right)+_scalar_gauge(left)


def _check_geometric_depth(edge: Callable[[Word], Q], word: Word, depth: int,
                           q: Q, slope: Q, offset: Q, cases: CheckRun) -> None:
    length = len(word)
    bound = abs(offset)*(1-2*q)
    limit = slope/2**length
    value = scalar_transport(edge, word, depth)
    cases.require(value == limit+offset*q**length*(2*q)**depth, "direct leaf sum")
    cases.require(abs(value-limit) == bound*q**length*(2*q)**depth/(1-2*q), "sharp tail bound")
    increment = abs(value-scalar_transport(edge, word, depth+1))
    cases.require(increment == bound*q**length*(2*q)**depth, "binary accumulation factor")
    left, right = endpoints(word)
    dressed: Callable[[Word], Q] = lambda leaf: _scalar_dressed(edge, leaf)
    cases.require(scalar_transport(dressed, word, depth) == value-_scalar_gauge(right)+_scalar_gauge(left),
                  "nonconstant endpoint gauge telescopes")


def _check_geometric_word(word: Word, q: Q, slope: Q, offset: Q, cases: CheckRun) -> None:
    edge: Callable[[Word], Q] = lambda leaf: _geometric_edge(leaf, q, slope, offset)
    bound = abs(offset)*(1-2*q)
    local = abs(edge(word)-edge((True,)+word)-edge((False,)+word))
    cases.require(local <= bound*q**len(word), "split-defect envelope")
    for depth in range(6):
        _check_geometric_depth(edge, word, depth, q, slope, offset, cases)


def _check_geometric_family(cases: CheckRun) -> None:
    for q, slope, offset in product((Q(0), Q(1, 8), Q(1, 4), Q(3, 8)), (Q(-3), Q(0), Q(5, 2)), (Q(-2), Q(0), Q(7, 3))):
        for word in _words():
            _check_geometric_word(word, q, slope, offset, cases)


def _alternating_edge(word: Word, q: Q) -> Q:
    return rational(Q(3, 2**len(word))+(-1)**sum(word)*q**len(word), "alternating fixture edge")


def _check_alternating_word(word: Word, q: Q, cases: CheckRun) -> None:
    edge: Callable[[Word], Q] = lambda leaf: _alternating_edge(leaf, q)
    bound = 1+2*q
    length = len(word)
    cases.require(abs(edge(word)-edge((True,)+word)-edge((False,)+word)) <= bound*q**length,
                  "nonconstant defect bound")
    for depth in range(6):
        cases.require(abs(scalar_transport(edge, word, depth)-Q(3, 2**length)) <=
                      bound*q**length*(2*q)**depth/(1-2*q), "nonconstant tail bound")


def _critical_edge(word: Word) -> Q:
    return Q(len(word), 2**len(word))


def _check_threshold(cases: CheckRun) -> None:
    for depth in range(9):
        cases.require(scalar_transport(_critical_edge, (), depth) == depth, "threshold transports grow as n")
        for word in product((False, True), repeat=depth):
            cases.require(abs(_critical_edge(word)-_critical_edge((True,)+word)-_critical_edge((False,)+word)) == Q(1, 2**depth),
                          "threshold leaf defects shrink")


def scalar_controls(counter: CheckRun | None = None) -> dict[str, object]:
    cases = _cases(counter)
    _check_geometric_family(cases)
    for q in (Q(1, 8), Q(1, 4), Q(3, 8)):
        for word in _words():
            _check_alternating_word(word, q, cases)
    q = Q(1, 4)
    edge: Callable[[Word], Q] = lambda word: q**len(word)
    values = [scalar_transport(edge, (), depth) for depth in range(7)]
    cases.require(abs(values[1]-values[2]) > Q(1, 2)*q, "omitting binary factor must fail")
    _check_threshold(cases)
    return {"sharp_geometric_example": [{"q": str(q), "C": "1/2", "root_transports": list(map(str, values)), "limit": "0"}],
            "threshold_q": "1/2", "threshold_root_transport": "n",
            "negative_controls": ["missing binary factor", "q=1/2 is not convergent"]}


def _permutation_gauge(value: Q) -> Permutation:
    return PERMS[(3*value.numerator+value.denominator) % 6]


def _permutation_edge(word: Word) -> Permutation:
    return PERMS[(len(word)+sum((index+1)*int(bit) for index, bit in enumerate(word))) % 6]


def _permutation_dressed(word: Word) -> Permutation:
    left, right = endpoints(word)
    return mul(mul(inv(_permutation_gauge(right)), _permutation_edge(word)), _permutation_gauge(left))


def _coherent_edge(word: Word) -> Permutation:
    left, right = endpoints(word)
    return mul(_permutation_gauge(right), inv(_permutation_gauge(left)))


def _check_noncommutative_word(word: Word, cases: CheckRun) -> tuple[bool, bool]:
    left, right = endpoints(word)
    order_fault = inverse_fault = False
    for depth in range(5):
        value = ordered_transport(_permutation_edge, word, depth)
        expected = mul(mul(inv(_permutation_gauge(right)), value), _permutation_gauge(left))
        actual = ordered_transport(_permutation_dressed, word, depth)
        cases.require(actual == expected, "noncommutative endpoint covariance")
        reversed_value = UNIT
        for leaf in reversed(leaves(word, depth)):
            reversed_value = mul(_permutation_edge(leaf), reversed_value)
        order_fault |= reversed_value != value
        inverse_fault |= mul(mul(_permutation_gauge(right), value), _permutation_gauge(left)) != actual
    return order_fault, inverse_fault


def noncommutative_controls(counter: CheckRun | None = None) -> dict[str, object]:
    cases = _cases(counter)
    for a, b, c in product(PERMS, repeat=3):
        cases.require(mul(a, mul(b, c)) == mul(mul(a, b), c), "S3 associativity")
    for a in PERMS:
        cases.require(mul(a, inv(a)) == UNIT == mul(inv(a), a), "S3 inverse")
    order_fault = inverse_fault = False
    for word in _words():
        order, inverse = _check_noncommutative_word(word, cases)
        order_fault |= order
        inverse_fault |= inverse
    cases.require(order_fault, "swapping ordered products must be detected")
    cases.require(inverse_fault, "omitting target inverse must be detected")
    for depth in range(7):
        cases.require(ordered_transport(_coherent_edge, (), depth) == _coherent_edge(()), "zero-defect coherent S3 tower")
    return {"group": "S3", "ordered_covariance": "passed", "zero_defect": "passed",
            "negative_controls": ["reversed order", "missing inverse"]}


def main() -> None:
    counter = CheckRun()
    scalar = scalar_controls(counter)
    noncommutative = noncommutative_controls(counter)
    print(json.dumps({"AuthorityEffect": "None", "status": "passed", "checks": counter.checks,
                      "scalar": scalar, "noncommutative": noncommutative,
                      "scope": "Exact finite controls; complete metric, refinement and decay hypotheses are supplied to separate Lean theorems."}, indent=2))


if __name__ == "__main__":
    raise SystemExit(cli(main))
