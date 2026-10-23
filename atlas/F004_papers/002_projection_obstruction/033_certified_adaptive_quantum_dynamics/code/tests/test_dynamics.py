"""Tests for exact quantum unitary dynamics and variational product-state mean field.

AuthorityEffect: None.
"""

import pytest
import numpy as np

from caqd.dynamics import evolve_exact, evolve_mean_field, SimulationResult
from caqd.spin_chains import (
    TFIMChain,
    neel_state,
    polarized_x_state,
    staggered_magnetization,
    transverse_magnetization,
)


def test_exact_dynamics_invariants(tfim_n4):
    """Verify trace preservation, Hermiticity, and energy conservation in exact evolution."""
    rho0 = neel_state(4)
    H = tfim_n4.H
    obs = {"H": H, "M_stag": staggered_magnetization(4)}
    
    times = [0.0, 0.1, 0.2, 0.5]
    res = evolve_exact(tfim_n4, rho0, times, obs)
    
    assert len(res.states) == len(times)
    
    # Check energy conservation: <H>(t) == <H>(0)
    e0 = res.expectation("H")[0]
    for e_t in res.expectation("H"):
        assert e_t == pytest.approx(e0, abs=1e-12)
        
    for rho in res.states:
        # Unit trace
        assert np.trace(rho) == pytest.approx(1.0, abs=1e-14)
        # Hermiticity
        np.testing.assert_allclose(rho, rho.conj().T, atol=1e-14)


def test_mean_field_dynamics_invariants(tfim_n4):
    """Verify trace preservation and Hermiticity in product-state mean field."""
    rho0 = polarized_x_state(4)
    obs = {"M_x": transverse_magnetization(4)}
    
    times = [0.0, 0.1, 0.2, 0.4]
    res = evolve_mean_field(tfim_n4, rho0, times, obs)
    
    assert len(res.states) == len(times)
    for rho in res.states:
        assert np.trace(rho) == pytest.approx(1.0, abs=1e-12)
        np.testing.assert_allclose(rho, rho.conj().T, atol=1e-12)


def test_t_span_monotonicity_enforcement(tfim_n4):
    """Verify solver raises ValueError on non-monotonic or empty time sequences."""
    rho0 = neel_state(4)
    with pytest.raises(ValueError):
        evolve_exact(tfim_n4, rho0, [])
    with pytest.raises(ValueError):
        evolve_exact(tfim_n4, rho0, [0.5, 0.2])


def test_simulation_result_expectation_lookup(tfim_n4):
    """Verify SimulationResult expectation method and error handling."""
    rho0 = neel_state(4)
    res = evolve_exact(tfim_n4, rho0, [0.0, 0.1], {"M_stag": staggered_magnetization(4)})
    
    assert len(res.expectation("M_stag")) == 2
    with pytest.raises(KeyError):
        res.expectation("Unknown_Obs")
