"""Shared fixtures for CAQD test suite.

AuthorityEffect: None.
"""

import pytest
import numpy as np

from caqd.spin_chains import (
    TFIMChain,
    XXZChain,
    neel_state,
    polarized_x_state,
    all_up_state,
    staggered_magnetization,
    center_correlation,
    transverse_magnetization,
)


@pytest.fixture
def tfim_n4():
    """4-site open-boundary TFIM chain (J=1.0, h=1.0)."""
    return TFIMChain(num_sites=4, J=1.0, h=1.0, periodic=False)


@pytest.fixture
def xxz_n4():
    """4-site open-boundary XXZ Heisenberg chain (J=1.0, delta=1.0, h=0.2)."""
    return XXZChain(num_sites=4, J=1.0, delta=1.0, h=0.2, periodic=False)


@pytest.fixture
def tfim_n6():
    """6-site open-boundary TFIM chain (J=1.0, h=0.5)."""
    return TFIMChain(num_sites=6, J=1.0, h=0.5, periodic=False)


@pytest.fixture
def standard_observables_n4():
    """Standard observables for N=4 chain."""
    return {
        "M_stag": staggered_magnetization(4),
        "C_mid": center_correlation(4),
        "M_x": transverse_magnetization(4),
    }


@pytest.fixture
def initial_states_n4():
    """Collection of initial pure density matrices for N=4."""
    return {
        "neel": neel_state(4),
        "polarized_x": polarized_x_state(4),
        "all_up": all_up_state(4),
    }
