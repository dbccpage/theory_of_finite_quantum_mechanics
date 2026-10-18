"""Positive and separating examples for the stated presentation-closure scope."""
from fractions import Fraction

import pytest

from omega_engine_projects.finite_to_continuum.code.presentation_closure_examples import (
    alternating_character_turns,
    character_average_by_polynomial,
    enclosure_examples,
    profile_examples,
    torus_tent_average,
)


@pytest.mark.parametrize("level", range(6))
def test_original_character_rule_against_actual_polynomial_sum(level):
    from continuous_haar_limit import HaarLimitCharacterPair

    for frequency in range(-6, 7):
        actual = character_average_by_polynomial(level, frequency)
        assert actual == HaarLimitCharacterPair(frequency, 0).discrete_sum_at_level(level)


def test_frequency_four_aliases_then_resolves():
    assert character_average_by_polynomial(2, 4) == 1
    assert character_average_by_polynomial(3, 4) == 0


def test_actual_csq_factor_retains_its_realized_image_boundary():
    example = profile_examples()
    assert example["image_factor_values"] == [-3, 0, 3]
    assert example["unused_profile_refused"]


def test_actual_csq_solver_refuses_a_lipschitz_integral_collision():
    example = profile_examples()
    assert example["sampling_profiles_equal"]
    assert example["sampling_integrals"] == ["0", "1/16"]
    assert not example["sampling_query_factors"]
    assert example["sampling_collision_reported"]


def test_actual_tent_samples_preserve_the_proved_common_target():
    example = enclosure_examples()
    assert example["actual_tent_averages"] == ["0", "1/4", "1/4", "1/4", "1/4"]
    assert example["actual_tent_integral"] == "1/4"
    assert example["tent_target_in_every_enclosure"]
    assert example["tent_finite_contraction_flag"]


def test_original_shrinking_overlap_flag_does_not_check_a_common_target():
    example = enclosure_examples()
    assert example["direct_shrinking_flag"]
    assert example["direct_intersection_empty"]


def test_actual_intersection_wrapper_detects_that_inconsistency():
    assert not enclosure_examples()["accumulated_wrapper_flag"]


def test_haar_flag_requires_observed_stabilized_levels():
    example = enclosure_examples()
    assert example["early_haar_recovery_flag"] is False
    assert example["early_observed_average"] == "1"
    assert example["early_declared_integral"] == "0"
    assert example["early_stabilization_level"] == 3


def test_integer_character_is_separated_by_a_dyadic_compact_test_set():
    for j in range(-32, 33):
        if j:
            v = (abs(j) & -abs(j)).bit_length() - 1
            assert (Fraction(j, 1 << (v + 1)) % 1) == Fraction(1, 2)


def test_alternating_2adic_prefixes_separate_circle_uniformity():
    rows = alternating_character_turns()
    for m, row in enumerate(rows, 1):
        assert Fraction(row["input_turn"]) == Fraction(1, 4 ** m)
        assert Fraction(row["character_turn"]) == Fraction(1, 3) - Fraction(1, 3 * 4 ** m)
        assert Fraction(row["character_turn"]) >= Fraction(1, 4)


def test_source_lipschitz_control_is_lost_by_profile_compression():
    domain = [0, *range(1, 17)]
    p = lambda x: Fraction(1, x) if x else Fraction(0)
    q = lambda x: Fraction(1) if x else Fraction(0)
    for x in domain:
        for y in domain:
            assert abs(q(x) - q(y)) <= int(x != y)
    assert abs(p(16) - p(0)) == Fraction(1, 16)
    assert abs(q(16) - q(0)) == 1


def test_a_zero_threshold_changes_at_the_limit():
    prefix = [Fraction(1, 1 << n) for n in range(8)]
    assert all(x > 0 for x in prefix)
    assert not Fraction(0) > 0


@pytest.mark.parametrize("levels", [(0,), (2,), (2, 1), (1, 2, 0), (1, 1, 1, 1)])
def test_actual_product_grid_samples_obey_the_conditional_torus_error(levels):
    example = torus_tent_average(levels)
    error = abs(Fraction(example["average"]) - Fraction(example["integral"]))
    assert error <= Fraction(example["conditional_error_bound"])
    if levels == (1, 1, 1, 1):
        assert example["node_count"] == 16
        assert example["average"] == example["integral"] == "5/2"


def test_product_grid_refuses_excess_resources_before_enumeration():
    with pytest.raises(ValueError, match="4096"):
        torus_tent_average((6, 6, 6, 6))


@pytest.mark.parametrize("level,frequency,exception", [
    (True, 1, TypeError), (1.0, 1, TypeError),
    (1, False, TypeError), (1, 0.5, TypeError), (7, 1, ValueError),
])
def test_exact_scalar_and_finite_resource_boundaries(level, frequency, exception):
    with pytest.raises(exception):
        character_average_by_polynomial(level, frequency)
