import random
from fractions import Fraction
from itertools import product

import pytest
from witnessed_difference.interference import (
    Readout,
    ReadoutKind,
    additive_readout,
    bilinear_readout,
    cross_term,
    power_readout,
    quadratic_readout,
    readout_value,
    sorkin_alternating_sum,
    unit_amplitude,
)
from witnessed_difference.outcomes import Accepted, AuthorityEffect, RefusalCode, Refused
from witnessed_difference.projective import GaussianRational
from witnessed_difference.state_spaces import (
    ConvexDecomposition,
    StateSpace,
    decompositions_of,
    is_simplex,
    is_simplex_decomposition_unique,
    make_state_space,
    square_state_space,
    triangle_state_space,
)

HALF = Fraction(1, 2)


def accepted(outcome):
    assert isinstance(outcome, Accepted), outcome
    assert outcome.authority_effect is AuthorityEffect.NONE
    return outcome.value


def refused(outcome, code: RefusalCode, fragment: str = "") -> Refused:
    assert isinstance(outcome, Refused), outcome
    assert outcome.code is code, outcome
    assert fragment in outcome.detail, outcome.detail
    return outcome


def g(real, imag=0) -> GaussianRational:
    return GaussianRational(Fraction(real), Fraction(imag))


def test_square_centre_has_two_disjoint_extreme_decompositions() -> None:
    square = square_state_space()
    family = accepted(decompositions_of(square, (0, 0)))
    assert set(family.decompositions) == {
        ConvexDecomposition((HALF, 0, HALF, 0)),
        ConvexDecomposition((0, HALF, 0, HALF)),
    }
    assert not family.unique
    supports = {decomposition.support for decomposition in family.decompositions}
    assert supports == {(0, 2), (1, 3)}
    for t in (Fraction(0), Fraction(1, 4), Fraction(1, 3), HALF):
        mixture = [t * a + t * c + (HALF - t) * b + (HALF - t) * d for a, b, c, d in zip(*square.extreme_points)]
        assert mixture == [0, 0]
    verdict = accepted(is_simplex_decomposition_unique(square, (0, 0)))
    assert (verdict.simplex, verdict.unique, verdict.decompositions) == (False, False, 2)
    assert accepted(is_simplex(square)) is False


def test_square_edge_points_decompose_uniquely_but_interior_points_do_not() -> None:
    square = square_state_space()
    edge = accepted(decompositions_of(square, (HALF, HALF)))
    assert edge.unique and edge.decompositions[0].weights == (HALF, HALF, 0, 0)
    for x, y in product((Fraction(-1, 4), Fraction(1, 4)), repeat=2):
        assert not accepted(decompositions_of(square, (x, y))).unique
    refused(decompositions_of(square, (1, 1)), RefusalCode.OUTSIDE_CARRIER, "convex hull")


def test_simplex_points_decompose_uniquely_on_a_grid() -> None:
    triangle = triangle_state_space()
    assert accepted(is_simplex(triangle)) is True
    for i, j in product(range(5), repeat=2):
        if i + j > 4:
            refused(decompositions_of(triangle, (Fraction(i, 4), Fraction(j, 4))), RefusalCode.OUTSIDE_CARRIER)
            continue
        point = (Fraction(i, 4), Fraction(j, 4))
        verdict = accepted(is_simplex_decomposition_unique(triangle, point))
        assert verdict.simplex and verdict.unique and verdict.decompositions == 1
        (decomposition,) = accepted(decompositions_of(triangle, point)).decompositions
        assert decomposition.weights == (1 - point[0] - point[1], point[0], point[1])


def test_state_space_admission_refuses_non_extreme_and_malformed_points() -> None:
    assert accepted(make_state_space(((1, 0), (0, 1), (-1, 0), (0, -1)))) == square_state_space()
    assert accepted(make_state_space(((3,),))).dimension == 1
    refused(make_state_space(((1, 0), (0, 1), (HALF, HALF))), RefusalCode.INVALID_INPUT, "not extreme")
    refused(make_state_space(()), RefusalCode.INVALID_INPUT, "distinct")
    refused(make_state_space(((), ())), RefusalCode.INVALID_INPUT, "distinct")
    refused(make_state_space(((1, 0), (1, 0))), RefusalCode.INVALID_INPUT, "distinct")
    refused(make_state_space(((0.5, 0),)), RefusalCode.INVALID_INPUT, "exact")
    refused(make_state_space(tuple((k, k * k) for k in range(11))), RefusalCode.BUDGET_EXHAUSTED)
    refused(decompositions_of("square", (0, 0)), RefusalCode.INVALID_INPUT, "state space")
    refused(decompositions_of(square_state_space(), (0,)), RefusalCode.INVALID_INPUT, "length 2")
    refused(is_simplex("square"), RefusalCode.INVALID_INPUT)
    refused(is_simplex_decomposition_unique(square_state_space(), (2, 2)), RefusalCode.OUTSIDE_CARRIER)
    tampered = StateSpace(((Fraction(1), Fraction(0)), (HALF, Fraction(0)), (Fraction(0), Fraction(0))))
    refused(decompositions_of(tampered, (HALF, 0)), RefusalCode.INVALID_INPUT, "not extreme")


def test_audit_instance_i2_is_six_fifths_for_the_quadratic_readout() -> None:
    a = accepted(unit_amplitude(1, 0))
    b = accepted(unit_amplitude(Fraction(3, 5), Fraction(4, 5)))
    quadratic = quadratic_readout()
    assert readout_value(quadratic, (a,)) == readout_value(quadratic, (b,)) == 1
    assert readout_value(quadratic, (a, b)) == Fraction(16, 5)
    assert accepted(sorkin_alternating_sum((a, b), (0, 1), quadratic)) == Fraction(6, 5)
    assert accepted(cross_term(quadratic, a, b)) == Fraction(6, 5)
    assert accepted(sorkin_alternating_sum((a, b), (0,), quadratic)) == 1
    assert accepted(sorkin_alternating_sum((a, b), (), quadratic)) == 0


def _random_amplitude(rng: random.Random) -> GaussianRational:
    return g(Fraction(rng.randint(-9, 9), rng.randint(1, 7)), Fraction(rng.randint(-9, 9), rng.randint(1, 7)))


def test_higher_sorkin_sums_vanish_for_every_declared_biadditive_readout() -> None:
    rng = random.Random(20260929)
    forms = [quadratic_readout()] + [
        accepted(bilinear_readout(tuple(tuple(rng.randint(-3, 3) for _ in range(2)) for _ in range(2)))) for _ in range(4)
    ]
    for readout in forms:
        for size in range(3, 7):
            for _ in range(6):
                amplitudes = tuple(_random_amplitude(rng) for _ in range(size))
                assert accepted(sorkin_alternating_sum(amplitudes, tuple(range(size)), readout)) == 0
        a, b = _random_amplitude(rng), _random_amplitude(rng)
        assert accepted(sorkin_alternating_sum((a, b), (0, 1), readout)) == accepted(cross_term(readout, a, b))


def test_quartic_readout_gives_i3_thirty_six_and_additive_readout_gives_zero() -> None:
    ones = (1, 1, 1)
    quartic = accepted(power_readout(2))
    assert accepted(sorkin_alternating_sum(ones, (0, 1, 2), quartic)) == 36
    assert accepted(sorkin_alternating_sum(ones, (0, 1, 2), accepted(power_readout(1)))) == 0
    additive = additive_readout()
    a, b = g(1), g(Fraction(3, 5), Fraction(4, 5))
    assert accepted(sorkin_alternating_sum((a, b), (0, 1), additive)) == 0
    assert accepted(sorkin_alternating_sum((a, b, g(2)), (0, 1, 2), additive)) == 0
    refused(cross_term(additive, a, b), RefusalCode.SCOPE_VIOLATION, "biadditive")
    refused(cross_term(quartic, a, b), RefusalCode.SCOPE_VIOLATION, "biadditive")


def test_sorkin_sum_refusals() -> None:
    quadratic = quadratic_readout()
    refused(sorkin_alternating_sum((0.5,), (0,), quadratic), RefusalCode.INVALID_INPUT)
    refused(sorkin_alternating_sum((1j,), (0,), quadratic), RefusalCode.INVALID_INPUT)
    refused(sorkin_alternating_sum((1, 1), [0, 1], quadratic), RefusalCode.INVALID_INPUT, "distinct integer")
    refused(sorkin_alternating_sum((1, 1), (0, 0), quadratic), RefusalCode.INVALID_INPUT, "distinct integer")
    refused(sorkin_alternating_sum((1, 1), (True,), quadratic), RefusalCode.INVALID_INPUT, "distinct integer")
    refused(sorkin_alternating_sum((1, 1), (0, 2), quadratic), RefusalCode.OUTSIDE_CARRIER)
    refused(sorkin_alternating_sum((1,) * 13, tuple(range(13)), quadratic), RefusalCode.BUDGET_EXHAUSTED)
    for bad in ("quadratic", Readout("quadratic"), Readout(ReadoutKind.POWER, 0), Readout(ReadoutKind.BILINEAR, 1, None)):
        refused(sorkin_alternating_sum((1,), (0,), bad), RefusalCode.INVALID_INPUT, "declared exact readout")
        refused(cross_term(bad, 1, 1), RefusalCode.INVALID_INPUT, "declared exact readout")
    refused(cross_term(quadratic, 0.5, 1), RefusalCode.INVALID_INPUT)
    for exponent in (0, -1, 1.0, True):
        refused(power_readout(exponent), RefusalCode.INVALID_INPUT, "exponent")
    refused(bilinear_readout(((1, 0),)), RefusalCode.INVALID_INPUT, "shape")
    refused(bilinear_readout(((0.5, 0), (0, 1))), RefusalCode.INVALID_INPUT)
    refused(unit_amplitude(1, 1), RefusalCode.NON_UNIT_PHASE)
    refused(unit_amplitude(0.6, 0.8), RefusalCode.INVALID_INPUT, "exact")


@pytest.mark.parametrize("exponent", [1, 2, 3])
def test_power_readouts_match_explicit_values(exponent) -> None:
    readout = accepted(power_readout(exponent))
    assert readout_value(readout, (g(1), g(0, 1))) == Fraction(2) ** exponent


def test_a_bilinear_readout_is_used_in_its_admitted_exact_form() -> None:
    from witnessed_difference.interference import (
        Readout,
        ReadoutKind,
        cross_term,
        sorkin_alternating_sum,
    )

    raw = Readout(ReadoutKind.BILINEAR, form=(("1", "0"), ("0", "1")))
    assert accepted(sorkin_alternating_sum((1, 1), (0, 1), raw)) == 2
    assert accepted(cross_term(raw, 1, 1)) == 2
    broken = Readout(ReadoutKind.BILINEAR, form=("10", "01"))
    refused(cross_term(broken, 1, 1), RefusalCode.INVALID_INPUT, "declared exact readout")


# Executable finite evidence; AuthorityEffect: None.
