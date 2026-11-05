from fractions import Fraction

import pytest
from hermitianization.model import GaussianRational
from state_effect_readout.model import (
    BinaryEffectFactor,
    StateFactor,
    born_probability,
    complement_probability,
    depolarized_probability,
    gmatrix,
    phase_scale,
    trace,
    trace_probability,
)
from state_effect_readout.replay import check, produce, reference_problem


def fixture():
    problem = reference_problem()
    state = StateFactor(gmatrix(problem["state_factor"]))
    effect = BinaryEffectFactor(
        gmatrix(problem["accept_factor"]), gmatrix(problem["reject_factor"])
    )
    return problem, state, effect


def test_state_and_binary_effect_are_normalized():
    _, state, effect = fixture()
    assert trace(state.density) == GaussianRational.of(1)
    assert effect.effect[0][0] == GaussianRational.of(1)
    assert effect.complement[1][1] == GaussianRational.of(1)


def test_factor_and_trace_readouts_agree():
    _, state, effect = fixture()
    assert born_probability(state, effect) == Fraction(1, 2)
    assert trace_probability(state, effect) == born_probability(state, effect)


def test_binary_probabilities_are_positive_and_sum_to_one():
    _, state, effect = fixture()
    p = born_probability(state, effect)
    q = complement_probability(state, effect)
    assert 0 <= p <= 1
    assert 0 <= q <= 1
    assert p + q == 1


def test_global_unit_phase_preserves_state_and_readout():
    _, state, effect = fixture()
    phase = GaussianRational.of(Fraction(3, 5), Fraction(4, 5))
    phased = StateFactor(phase_scale(phase, state.factor))
    assert phased.density == state.density
    assert born_probability(phased, effect) == born_probability(state, effect)


def test_zero_state_is_refused():
    with pytest.raises(ValueError, match="positive Frobenius mass"):
        StateFactor(gmatrix([[0, 0], [0, 0]]))


def test_incomplete_effect_is_refused():
    accept = gmatrix([[1, 0], [0, 0]])
    with pytest.raises(ValueError, match="do not resolve"):
        BinaryEffectFactor(accept, accept)


def test_positive_normalized_conditions_do_not_select_readout():
    problem, _, effect = fixture()
    sharp = StateFactor(gmatrix(problem["sharp_state_factor"]))
    base = born_probability(sharp, effect)
    alternate = depolarized_probability(sharp, effect, Fraction(1, 2))
    complement_effect = BinaryEffectFactor(effect.reject, effect.accept)
    alternate_complement = depolarized_probability(sharp, complement_effect, Fraction(1, 2))
    assert base == 1
    assert alternate == Fraction(3, 4)
    assert 0 <= alternate <= 1
    assert alternate + alternate_complement == 1


@pytest.mark.parametrize("weight", [Fraction(0), Fraction(1, 2), Fraction(3, 4), Fraction(1)])
def test_dimension_one_readout_is_independent_of_depolarization(weight):
    state = StateFactor(gmatrix([[2,]]))
    # Three identical Gram rows give the nontrivial scalar effect e=1/3.
    accept = gmatrix([[Fraction(1, 3)]] * 3)
    reject = gmatrix([[Fraction(1, 3)]] * 6)
    effect = BinaryEffectFactor(accept, reject)
    complement = BinaryEffectFactor(reject, accept)
    assert trace(state.density) == GaussianRational.of(1)
    assert born_probability(state, effect) == Fraction(1, 3)
    assert depolarized_probability(state, effect, weight) == Fraction(1, 3)
    assert depolarized_probability(state, complement, weight) == Fraction(2, 3)


@pytest.mark.parametrize("n", [2, 3, 4])
@pytest.mark.parametrize("weight", [Fraction(0), Fraction(1, 2), Fraction(3, 4), Fraction(1)])
def test_nontrivial_dimension_sharp_pair_distinguishes_readouts(n, weight):
    sharp = [[int(i == j == 0) for j in range(n)] for i in range(n)]
    other = [[int(i == j and i != 0) for j in range(n)] for i in range(n)]
    state = StateFactor(gmatrix(sharp))
    effect = BinaryEffectFactor(gmatrix(sharp), gmatrix(other))
    complement = BinaryEffectFactor(effect.reject, effect.accept)
    value = depolarized_probability(state, effect, weight)
    assert value == weight + (1 - weight) / n
    assert (value != born_probability(state, effect)) == (weight != 1)
    assert 0 <= value <= 1
    assert value + depolarized_probability(state, complement, weight) == 1


def test_boolean_matrix_entry_is_refused():
    with pytest.raises(TypeError, match="unsupported rational"):
        gmatrix([[True, 0], [0, 1]])


def test_receipt_replays_and_tamper_is_refused():
    problem = reference_problem()
    receipt = produce(problem)
    check(problem, receipt)
    tampered = {**receipt, "problem_sha256": "0" * 64}
    with pytest.raises(ValueError, match="does not replay"):
        check(problem, tampered)
