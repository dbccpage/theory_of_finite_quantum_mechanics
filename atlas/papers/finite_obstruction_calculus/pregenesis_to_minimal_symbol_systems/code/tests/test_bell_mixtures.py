"""Joint probability checks with exact integer masses and rational arithmetic."""
import itertools
import sys
from fractions import Fraction
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from preservation import bell_mixture, protocol  # noqa: E402


def test_all_vertices_and_two_point_mixtures_obey_both_bell_bounds():
    for first, second in itertools.product(range(16), repeat=2):
        for a, b in itertools.product(range(1, 6), repeat=2):
            weights = [0]*16
            weights[first] += a
            weights[second] += b
            *correlations, score = bell_mixture(weights)
            assert all(-1 <= value <= 1 for value in correlations)
            assert -2 <= score <= 2
            assert tuple(correlations) != (1, 1, -1, 1)


def test_joint_distribution_marginals_independently():
    weights = list(range(1, 17))
    expected = []
    states = list(itertools.product((False, True), repeat=4))
    for left, right in ((0, 2), (0, 3), (1, 2), (1, 3)):
        probabilities = [sum(w for w, s in zip(weights, states, strict=True)
                             if s[left] == a and s[right] == b)
                         for a, b in itertools.product((False, True), repeat=2)]
        assert sum(probabilities) == sum(weights)
        expected.append(Fraction(probabilities[0]-probabilities[1]-probabilities[2]+probabilities[3],
                                 sum(weights)))
    assert bell_mixture(weights)[:4] == tuple(expected)
    assert bell_mixture([1]*16) == (0, 0, 0, 0, 0)


@pytest.mark.parametrize("weights", [[0]*16, [-1]+[1]*15, [1]*15, [1]*17])
def test_invalid_joint_masses_refused(weights):
    with pytest.raises(ValueError):
        bell_mixture(weights)
    assert protocol("v1\tbellmix\t"+",".join(map(str, weights))) == "REFUSE"
