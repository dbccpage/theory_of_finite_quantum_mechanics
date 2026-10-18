"""Exact finite checks; the infinite Lane E arguments remain analytic proofs."""

from fractions import Fraction

import pytest

from omega_engine_projects.finite_to_continuum.code.presentation_duality import (
    OBSTRUCTION_CHARACTER_DISCONTINUOUS,
    cauchy_tail_level,
    circle_distance,
    dyadic_approximation,
    haar_quadrature,
    integer_character,
    minus_one_third_character,
    minus_one_third_pc_witness,
    minus_one_third_residue,
    scaled_third_in_ball,
    triangle_quadrature,
    triangle_wave,
    verify_integer_characters,
    verify_pc_witness,
)


def test_integer_character_lipschitz():
    assert verify_integer_characters() == 5 * sum(4**n for n in range(9))
    # Wraparound uses the circle metric rather than distance of representatives.
    assert circle_distance(Fraction(255, 256), 0) == Fraction(1, 256)
    assert integer_character(-5, Fraction(255, 256)) == Fraction(5, 256)
    assert integer_character(0, Fraction(255, 256)) == 0


def test_two_adic_minus_one_third_pc_refusal():
    # Arbitrary input is supported by the constructor, not established by this
    # finite list. The all-delta argument uses 4**(-m)<delta and image>=1/4.
    for delta in (
        Fraction(3),
        Fraction(1, 4),
        Fraction(1, 10),
        Fraction(7, 999),
        Fraction(1, 4**100),
        Fraction(1, 10**200),
    ):
        witness = minus_one_third_pc_witness(delta)
        assert verify_pc_witness(witness) is True
        assert witness["obstruction"] == OBSTRUCTION_CHARACTER_DISCONTINUOUS
        assert witness["epsilon"] == Fraction(1, 5)
        assert witness["x"] < delta
        assert witness["image"] >= Fraction(1, 4)
        assert Fraction(1, 3) - witness["image"] == witness["x"] / 3
    # The inequality is strict: x=delta is not an accepted PC counterexample.
    assert minus_one_third_pc_witness(Fraction(1, 4))["m"] == 2


def test_residues_are_compatible_characters_on_finite_levels():
    for level in range(9):
        order = 1 << level
        residue = minus_one_third_residue(level)
        assert (3 * residue + 1) % order == 0
        assert minus_one_third_residue(level + 1) % order == residue
        for k in range(order):
            x = Fraction(k, order)
            assert minus_one_third_character(x) == Fraction(residue * k, order) % 1
            assert (
                minus_one_third_character(x + Fraction(1, order))
                == (minus_one_third_character(x) + minus_one_third_character(Fraction(1, order)))
                % 1
            )


@pytest.mark.parametrize(
    "field,replacement",
    [
        ("m", 0),
        ("m", True),
        ("m", 2.0),
        ("residue", 0),
        ("x", Fraction(1, 3)),
        ("x", 0.0625),
        ("image", Fraction(0)),
        ("image", True),
        ("delta", Fraction(0)),
        ("delta", Fraction(1, 16)),
        ("epsilon", Fraction(1, 6)),
        ("topology", "discrete"),
        ("obstruction", "PASS"),
    ],
)
def test_refusal_verifier_rejects_mutated_witness(field, replacement):
    witness = minus_one_third_pc_witness(Fraction(1, 8))
    witness[field] = replacement
    unchanged = dict(witness)
    assert verify_pc_witness(witness) is False
    assert witness == unchanged


def test_refusal_verifier_rejects_missing_fields():
    witness = minus_one_third_pc_witness(1)
    del witness["image"]
    assert verify_pc_witness(witness) is False


def test_discrete_topology_does_not_inherit_the_circle_refusal():
    # In the discrete source metric, delta=1 forces x=y, so every algebraic
    # character is uniformly continuous. These x_m have discrete distance 1.
    for m in range(1, 20):
        x = Fraction(1, 4**m)
        assert int(x != 0) == 1
        assert circle_distance(x) == x < 1
        assert circle_distance(minus_one_third_character(x)) >= Fraction(1, 4)


def test_colimit_non_locally_compact_witness():
    # a=1/(3*2**s) lies outside D; floors approach a inside every chosen ball.
    # Infinite convergence/noncompactness follow in the analytic derivation,
    # not from declaring this finite prefix compact or noncompact.
    for radius in (
        Fraction(5),
        Fraction(1, 4),
        Fraction(1, 6),
        Fraction(2, 71),
        Fraction(1, 2**80),
    ):
        target = scaled_third_in_ball(radius)
        assert 0 < target < min(radius, Fraction(1, 4))
        assert target.denominator % 3 == 0
        scale = target.denominator // 3
        assert scale & (scale - 1) == 0
        for level in range(100):
            point = dyadic_approximation(target, level)
            assert point.denominator & (point.denominator - 1) == 0
            assert circle_distance(point) < radius
            assert 0 < target - point < Fraction(1, 1 << level)
        for epsilon in (Fraction(1, 3), Fraction(1, 2**30)):
            start = cauchy_tail_level(epsilon)
            points = [dyadic_approximation(target, k) for k in range(start, start + 10)]
            assert all(circle_distance(x, y) < epsilon for x in points for y in points)


def test_haar_quadrature_bandlimited_vs_lipschitz():
    coefficients = {-5: Fraction(2, 3), 0: Fraction(-7, 2), 1: Fraction(1, 9), 5: 4}
    for level in range(7):
        report = haar_quadrature(coefficients, level)
        if (1 << level) > 5:
            assert report["bandlimit_below_order"] is True
            assert report["alias_frequencies"] == ()
            assert report["average"] == report["integral"] == Fraction(-7, 2)
        for slope in (0, 1, Fraction(7, 3)):
            triangle = triangle_quadrature(level, slope)
            assert triangle["average"] == 0
            assert triangle["integral"] == Fraction(slope, 4 * (1 << level))
            assert triangle["error"] == triangle["integral"] <= triangle["bound"]
    assert triangle_quadrature(8, 1)["error"] == Fraction(1, 1024)


def test_strict_bandlimit_and_alias_cancellation_boundaries():
    boundary = haar_quadrature({0: 2, 8: 1}, 3)
    assert boundary["bandlimit_below_order"] is False
    assert boundary["alias_frequencies"] == (8,)
    assert boundary["average"] == 3 and boundary["integral"] == 2
    assert boundary["error"] == 1
    assert haar_quadrature({8: 1}, 4)["error"] == 0
    cancelled = haar_quadrature({-8: -1, 8: 1}, 3)
    assert cancelled["error"] == 0
    assert cancelled["alias_frequencies"] == (-8, 8)
    assert cancelled["bandlimit_below_order"] is False
    assert haar_quadrature({}, 0)["integral"] == 0


def test_triangle_breakpoints_periodicity_and_lipschitz():
    order, slope = 4, Fraction(7, 3)
    points = [Fraction(k, 16) for k in range(-16, 17)]
    assert triangle_wave(order, slope, Fraction(1, 8)) == slope / 8
    assert triangle_wave(order, slope, Fraction(1, 4)) == 0
    for x in points:
        assert triangle_wave(order, slope, x + 1) == triangle_wave(order, slope, x)
        for y in points:
            assert abs(
                triangle_wave(order, slope, x) - triangle_wave(order, slope, y)
            ) <= slope * circle_distance(x, y)


@pytest.mark.parametrize("bad", [True, False, 0.2, complex(1), object()])
def test_rational_boundaries_reject_inexact_or_untyped_inputs(bad):
    for operation in (
        minus_one_third_pc_witness,
        scaled_third_in_ball,
        cauchy_tail_level,
        circle_distance,
        minus_one_third_character,
    ):
        with pytest.raises(TypeError):
            operation(bad)
    with pytest.raises(TypeError):
        haar_quadrature({1: bad}, 2)
    with pytest.raises(TypeError):
        triangle_wave(4, bad, Fraction(1, 8))


@pytest.mark.parametrize("bad", [True, False, 1.0, Fraction(1), "1"])
def test_integer_boundaries_reject_coercion(bad):
    with pytest.raises(TypeError):
        integer_character(bad, Fraction(1, 4))
    with pytest.raises(TypeError):
        minus_one_third_residue(bad)
    with pytest.raises(TypeError):
        haar_quadrature({bad: 1}, 2)
    with pytest.raises(TypeError):
        dyadic_approximation(Fraction(1, 3), bad)
    with pytest.raises(TypeError):
        triangle_wave(bad, 1, 0)


@pytest.mark.parametrize("radius", [0, -1])
def test_nonpositive_radii_are_rejected(radius):
    for operation in (minus_one_third_pc_witness, scaled_third_in_ball, cauchy_tail_level):
        with pytest.raises(ValueError):
            operation(radius)


def test_domain_and_finite_replay_boundaries():
    with pytest.raises(ValueError, match="dyadic"):
        minus_one_third_character(Fraction(1, 3))
    with pytest.raises(ValueError):
        minus_one_third_residue(-1)
    with pytest.raises(ValueError):
        haar_quadrature({1: 1}, 7)
    with pytest.raises(ValueError):
        triangle_quadrature(9, 1)
    with pytest.raises(ValueError):
        triangle_wave(0, 1, 0)
    with pytest.raises(ValueError):
        triangle_wave(1, -1, 0)
