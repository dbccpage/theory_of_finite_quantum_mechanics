"""Exact countermodels for the E1/E2 hypothesis discussion."""

from fractions import Fraction
from itertools import product

import pytest


@pytest.mark.parametrize("target,expected", [(("a",), 1), (("a", "b"), 2)])
def test_nonsurjective_report_can_have_unique_or_nonunique_extension(target, expected):
    report = {"state": "observed"}
    answer = {"state": "a"}
    report_target = ("observed", "unobserved")
    factors = [dict(zip(report_target, values)) for values in product(target, repeat=2)]
    extensions = [f for f in factors if all(f[report[x]] == answer[x] for x in report)]
    assert len(set(report.values())) < len(report_target)
    assert len(extensions) == expected


def test_negative_weight_can_have_a_finite_attained_minimum():
    # D(x)=(x,x), A(u)=(u,u), w=(-1,2): cancellation leaves a nonnegative norm.
    for x in map(Fraction, (-3, -1, 0, 1, 3)):
        for u in (Fraction(-5), Fraction(1, 3), -x, Fraction(7)):
            coordinates = (x + u, x + u)
            objective = sum(w * abs(v) for w, v in zip((-1, 2), coordinates))
            assert objective == abs(x + u) >= 0
            if u == -x:
                assert objective == 0
    # In contrast, one coordinate of weight -1 has an unbounded negative ray.
    for bound in (1, 10, 100):
        assert -abs(Fraction(bound + 1)) < -bound
