"""Exact input-dependent checks for the five formerly recorded quantum anchors."""

from dataclasses import replace
from fractions import Fraction
from itertools import product
from math import factorial, prod

import pytest
from witnessed_difference.projective import GaussianRational
from witnessed_difference.quantum import (
    CABELLO_CONTEXTS,
    CABELLO_RAYS,
    H020,
    H015_collapse_no_isometry,
    H015CollapseDilations,
    H016_no_report_half_step,
    H017Fin,
    collapse_dilations,
    finite_matrix_recovery_fixture,
    report_square_roots,
)


def test_collapse_gram_changes_for_a_reversible_basis_action():
    assert H015_collapse_no_isometry((0, 0)) is True
    assert H015_collapse_no_isometry((1, 1)) is True
    assert H015_collapse_no_isometry((0, 1)) is False
    assert H015_collapse_no_isometry((1, 0)) is False
    assert H015_collapse_no_isometry((0,)) is False


def test_dilation_census_retains_each_actual_permutation():
    permutations = collapse_dilations()
    assert len(permutations) == len(set(permutations)) == H015CollapseDilations() == 4
    for permutation in permutations:
        assert sorted(permutation) == list(range(4))
        assert permutation[0] in (0, 1) and permutation[2] in (0, 1)
    assert H015CollapseDilations(environment_size=1) == 0
    assert H015CollapseDilations((0, 1), environment_size=1) == 1
    assert H015CollapseDilations(prepared=1) == 4


def test_dilation_enumeration_agrees_with_independent_counting_formula():
    # For each target value choose distinct environment images for its fiber;
    # then freely permute the remaining composite states. This is independent
    # of the implementation's exhaustive permutation enumeration.
    for size in (1, 2, 3):
        for mapping in product(range(size), repeat=size):
            fibers = [mapping.count(target) for target in range(size)]
            expected = 0 if max(fibers) > 2 else prod(
                factorial(2) // factorial(2 - count) for count in fibers
            ) * factorial(size)
            assert H015CollapseDilations(mapping) == expected


def test_half_step_changes_with_actual_report_map():
    assert H016_no_report_half_step() is True
    assert report_square_roots() == ()
    assert report_square_roots((0, 1)) == ((0, 1), (1, 0))
    assert report_square_roots((1, 2, 0)) == ((2, 0, 1),)
    assert H016_no_report_half_step((0, 0)) is False
    assert H016_no_report_half_step((1, 0, 3, 2)) is False


@pytest.mark.parametrize("mapping", [(), [0, 0], (0, True), (0, 0.0), (0, 2), (-1, 0)])
def test_map_admission_rejects_malformed_or_inexact_carriers(mapping):
    for anchor in (H015_collapse_no_isometry, H015CollapseDilations, H016_no_report_half_step):
        with pytest.raises(ValueError):
            anchor(mapping)


def test_census_limits_refuse_instead_of_silently_omitting_candidates():
    with pytest.raises(ValueError, match="eight"):
        H015CollapseDilations((0, 1, 2), environment_size=3)
    with pytest.raises(ValueError, match="six"):
        H016_no_report_half_step(tuple(range(7)))
    with pytest.raises(ValueError, match="positive integer"):
        H015CollapseDilations(environment_size=True)
    with pytest.raises(ValueError, match="prepared"):
        H015CollapseDilations(prepared=2)


def test_finite_matrix_recovery_computes_supplied_instance():
    fixture = finite_matrix_recovery_fixture()
    assert H017Fin() is True
    assert H017Fin(fixture) is True
    zero = GaussianRational(0)
    zmat = ((zero, zero), (zero, zero))
    assert H017Fin(replace(fixture, basis_images=zmat)) is False
    assert H017Fin(replace(fixture, matrix=zmat)) is False
    assert H017Fin(replace(fixture, adjoint=zmat)) is False
    assert H017Fin(replace(fixture, other_matrix=zmat)) is False
    assert H017Fin(replace(fixture, composition=zmat)) is False
    # Consistent changed data is a new valid instance, not a replay of the old one.
    assert H017Fin(replace(fixture, basis_images=zmat, matrix=zmat, adjoint=zmat,
                          composition=zmat)) is True


def test_finite_matrix_adjoint_is_conjugate_transpose_not_transpose():
    fixture = finite_matrix_recovery_fixture()
    plain_transpose = tuple(zip(*fixture.matrix))
    assert H017Fin(replace(fixture, adjoint=plain_transpose)) is False
    # Multiplication is noncommutative: supplying BA for the declared AB fails.
    g = GaussianRational
    ba = ((g(2), g(0, -1)), (g(1), g(0, -2)))
    assert H017Fin(replace(fixture, composition=ba)) is False


@pytest.mark.parametrize("entry", [1, 1.0, True, 1j, GaussianRational(Fraction(1, 2))])
def test_matrix_anchor_rejects_values_outside_declared_gaussian_integer_ring(entry):
    fixture = finite_matrix_recovery_fixture()
    with pytest.raises(TypeError, match="Gaussian integers"):
        H017Fin(replace(fixture, matrix=((entry, fixture.matrix[0][1]), fixture.matrix[1])))


def test_matrix_anchor_rejects_wrong_shape_and_empty_basis():
    fixture = finite_matrix_recovery_fixture()
    with pytest.raises(ValueError, match="dimension"):
        H017Fin(replace(fixture, adjoint=fixture.adjoint[:1]))
    with pytest.raises(ValueError, match="nonempty"):
        H017Fin(replace(fixture, basis_images=()))


def test_contextuality_binds_eighteen_rays_nine_contexts_and_incidence():
    assert H020() is True
    assert H020(CABELLO_RAYS, CABELLO_CONTEXTS) is True
    assert sum(len(context) for context in CABELLO_CONTEXTS) == 36
    assert [sum(index in context for context in CABELLO_CONTEXTS) for index in range(18)] == [2] * 18
    # A corruption leaves nine contexts and 36 entries: oddness alone misses it.
    changed_contexts = (CABELLO_CONTEXTS[1],) + CABELLO_CONTEXTS[1:]
    assert H020(CABELLO_RAYS, changed_contexts) is False


@pytest.mark.parametrize("replacement", [(0, 0, 0, 0), (1, 0, 0, 1), (1, 0, 0, 2)])
def test_contextuality_rejects_zero_parallel_or_nonorthogonal_rays(replacement):
    assert H020((replacement,) + CABELLO_RAYS[1:], CABELLO_CONTEXTS) is False


def test_contextuality_rejects_changed_incidence_and_accepts_valid_coordinate_change():
    bad_context = (0, 0, 2, 3)
    assert H020(CABELLO_RAYS, (bad_context,) + CABELLO_CONTEXTS[1:]) is False
    # Independent nonzero rational scaling leaves every projective ray unchanged.
    scaled = tuple(tuple(Fraction(index + 1, 3) * value for value in ray)
                   for index, ray in enumerate(CABELLO_RAYS))
    assert H020(scaled, CABELLO_CONTEXTS) is True
    # Reordering every ambient coordinate is a distinct valid supplied table.
    permuted = tuple(tuple(reversed(ray)) for ray in CABELLO_RAYS)
    assert H020(permuted, CABELLO_CONTEXTS) is True


@pytest.mark.parametrize("entry", [True, 0.0, "0"])
def test_contextuality_rejects_inexact_and_type_confused_coordinates(entry):
    with pytest.raises(TypeError, match="exact rational"):
        H020(((entry, 0, 0, 1),) + CABELLO_RAYS[1:], CABELLO_CONTEXTS)


def test_contextuality_rejects_missing_ray_context_or_outside_index():
    with pytest.raises(ValueError, match="eighteen"):
        H020(CABELLO_RAYS[:-1])
    with pytest.raises(ValueError, match="nine"):
        H020(contexts=CABELLO_CONTEXTS[:-1])
    with pytest.raises(ValueError, match="outside"):
        H020(contexts=((18, 1, 2, 3),) + CABELLO_CONTEXTS[1:])
