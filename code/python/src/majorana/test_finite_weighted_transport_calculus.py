"""Regression coverage for the legacy finite weighted transport helpers."""

import numpy as np
import pytest

from omega_engine.crates.functional.quantum_gaps import TransportAmplitude
from omega_engine.crates.homology_theory import finite_transport
from omega_engine.crates.linear_algebra_theory.transport import MinimalCyclicTransport


def test_weighted_path_sum_and_legacy_normalized_shift_are_concrete() -> None:
    weights = np.array([[0.0, 0.0, 5.0], [2.0, 0.0, 0.0], [0.0, 3.0, 0.0]])
    assert np.array_equal(
        finite_transport.path_sum(weights, 2),
        np.array([[0.0, 15.0, 0.0], [0.0, 0.0, 10.0], [6.0, 0.0, 0.0]]),
    )
    assert not finite_transport.is_column_stochastic(weights)

    shift = MinimalCyclicTransport(3).shift_operator()
    assert np.array_equal(TransportAmplitude.get_physical_transport_operator(3), shift / np.pi)


@pytest.mark.parametrize("dimension", [0, -1, True, "3"])
def test_legacy_cyclic_shift_refuses_invalid_dimensions(dimension: object) -> None:
    with pytest.raises(ValueError, match="positive integer"):
        MinimalCyclicTransport(dimension)
