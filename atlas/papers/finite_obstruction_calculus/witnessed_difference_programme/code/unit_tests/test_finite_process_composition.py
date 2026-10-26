from fractions import Fraction

import pytest

from process_composition.model import (
    EnsembleState,
    KrausProcess,
    apply_process,
    branch_probability,
    compose_process,
    exact_standard_real_hadamard_available,
    identity_instrument_single,
    identity_instrument_split,
    phase_s_gate,
    tensor_process,
    unitary_process,
    x_gate,
)
from process_composition.replay import check, produce, reference_problem
from state_effect_readout.model import gmatrix, identity


def test_unitary_process_preserves_mass_and_is_reversible_by_composition():
    state = EnsembleState((gmatrix([[1, 0], [0, 0]]),))
    x = unitary_process(x_gate())
    once = apply_process(state, x)
    twice = apply_process(once, x)
    assert once.total_mass == state.total_mass
    assert twice.density == state.density


def test_sequential_and_composite_processes_agree():
    state = EnsembleState((gmatrix([[1, 0], [0, 0]]),))
    x = unitary_process(x_gate())
    s = unitary_process(phase_s_gate())
    assert apply_process(apply_process(state, x), s).density == apply_process(
        state, compose_process(x, s)
    ).density


def test_measurement_probabilities_and_updates():
    problem = reference_problem()
    state = EnsembleState((gmatrix(problem["plus_factor"]),))
    measurement = KrausProcess(tuple(gmatrix(x) for x in problem["measurement_operators"]))
    probabilities = [branch_probability(state, measurement, i) for i in range(2)]
    assert probabilities == [Fraction(1, 2), Fraction(1, 2)]


def test_same_unconditioned_channel_can_have_different_labelled_instrument():
    state = EnsembleState((gmatrix([[1, 1], [0, 0]]),))
    single = identity_instrument_single(2)
    split = identity_instrument_split(2)
    assert apply_process(state, single).density == apply_process(state, split).density
    assert [branch_probability(state, split, i) for i in range(2)] == [
        Fraction(9, 25), Fraction(16, 25)
    ]


def test_tensor_product_of_unitaries_is_complete_and_mass_preserving():
    tensor = tensor_process(unitary_process(x_gate()), unitary_process(identity(2)))
    state = EnsembleState((gmatrix([
        [1, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ]),))
    assert apply_process(state, tensor).total_mass == 1


def test_incomplete_process_is_refused():
    with pytest.raises(ValueError, match="do not resolve"):
        KrausProcess((gmatrix([[1, 0], [0, 0]]),))


def test_standard_hadamard_is_not_exact_over_gaussian_rationals():
    assert not exact_standard_real_hadamard_available()


def test_receipt_replays_and_tamper_is_refused():
    problem = reference_problem()
    receipt = produce(problem)
    check(problem, receipt)
    tampered = {**receipt, "problem_sha256": "0" * 64}
    with pytest.raises(ValueError, match="does not replay"):
        check(problem, tampered)
