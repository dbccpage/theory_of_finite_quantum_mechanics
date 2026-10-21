"""Regression coverage for finite cyclic path sums and composition."""

import numpy as np
import pytest

from omega_engine.crates.homology_theory import finite_transport
from omega_engine.crates.linear_algebra_theory.transport import MinimalCyclicTransport


def test_cyclic_path_sums_wrap_and_compose_without_authority_effect() -> None:
    shift = MinimalCyclicTransport(3).shift_operator()
    basis_zero = np.array([1.0, 0.0, 0.0])

    assert np.array_equal(
        shift,
        np.array([[0.0, 0.0, 1.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]),
    )
    assert np.array_equal(finite_transport.path_sum(shift, 0), np.eye(3))
    assert np.array_equal(finite_transport.path_sum(shift, 3), np.eye(3))
    assert np.array_equal(finite_transport.path_sum(shift, 2) @ basis_zero, np.array([0.0, 0.0, 1.0]))

    report = finite_transport.chapman_kolmogorov(shift, 1, 2)
    assert report == {
        "p": 1,
        "q": 2,
        "max_abs_deviation": 0.0,
        "holds": True,
        "authority_effect": "None",
    }


def test_negative_path_length_is_refused() -> None:
    with pytest.raises(ValueError, match="nonnegative"):
        finite_transport.path_sum(MinimalCyclicTransport(3).shift_operator(), -1)
