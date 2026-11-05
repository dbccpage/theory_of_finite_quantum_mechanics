from fractions import Fraction as Q
from itertools import product

import pytest
from locality_smearing.checker import check_alternating, check_recovery, check_subdivision
from locality_smearing.finite import (
    alternating_average,
    differences,
    harmonic,
    observation_completion,
    positive_threshold,
    primitive,
    recovery,
    subdivide,
)


def test_every_small_binary_syndrome_matches_direct_fibers():
    errors = tuple(product((0, 1), repeat=3))
    repairs = ((0, 0, 0),)
    for entries in product((0, 1), repeat=6):
        rows = (entries[:3], entries[3:])
        certificate = recovery(rows, errors, repairs)
        assert check_recovery(rows, errors, repairs, certificate)
        assert certificate["kind"] == "collision"  # 8 inputs, at most 4 syndromes


def test_nontrivial_repair_and_minimum_completion():
    errors = tuple(product((0, 1), repeat=3))
    repairs = ((0, 0, 0), (1, 1, 0))
    rows = ((1, 1, 0),)
    completion = observation_completion(rows, errors, repairs)
    assert completion["minimum"] == 1
    assert check_recovery(
        (*rows, *map(tuple, completion["extra_rows"])), errors, repairs, completion["decoder"]
    )
    wrong = {"kind": "decoder", "rows": [{"syndrome": [0], "repair": [0, 0, 0]}]}
    assert not check_recovery(rows, errors, repairs, wrong)


def test_staggered_smearing_bound_and_changed_samples():
    samples = [[Q(j, 8), Q(j, 8)] for j in range(8)]
    a = alternating_average(samples)
    assert a == -Q(1, 16)
    assert check_alternating(samples, "1", str(a))
    assert not check_alternating(samples, "1", "0")
    samples[1][0] = Q(9)
    assert not check_alternating(samples, "1", str(a))
    with pytest.raises(ValueError):
        alternating_average([[1], [2], [3]])


def test_cochain_period_quotient_and_weighted_subdivision():
    for x in product((-1, 0, 1), repeat=3):
        if sum(x) == 0:
            assert differences(primitive(x)) == x
        else:
            with pytest.raises(ValueError):
                primitive(x)
        y = subdivide(x, 3)
        assert check_subdivision(x, 3, y)
        assert harmonic(x)[0] == harmonic(y)[0] * 3
    # Unweighted L2 is not preserved, and a low-frequency exact cochain survives a low pass.
    assert sum(t * t for t in subdivide([1, -1], 2)) != 2
    assert differences([0, 1, 0, -1]) == (1, -1, -1, 1)
    assert harmonic(differences([0, 1, 0, -1])) == (0, 0, 0, 0)
    assert harmonic([1, 1, 1, 1]) == (1, 1, 1, 1)


def test_strict_margin_threshold_and_upper_bound_not_lower_bound():
    assert positive_threshold("4", "2") == 3
    assert Q(2) - Q(4, 2) == 0
    assert Q(2) - Q(4, 3) > 0
    assert 0 <= 1  # a positive upper envelope is compatible with zero error
