"""Tier 4 Real-World Application Scenarios for Paper 1 (R1).

End-to-end quench dynamics simulations on TFIM and XXZ spin chains
comparing sampled residual estimates and fixture-specific observable errors.

AuthorityEffect: None.
"""

import pytest
import numpy as np

from caqd.spin_chains import (
    TFIMChain,
    XXZChain,
    neel_state,
    polarized_x_state,
    staggered_magnetization,
    center_correlation,
    transverse_magnetization,
)
from caqd.dynamics import evolve_exact, evolve_mean_field
from caqd.adaptive import evolve_adaptive
from caqd.bounds import verify_bound_honesty, compute_cumulative_bounds


def test_e2e_tfim_quench_dynamics_n4():
    """Scenario 1: TFIM quench dynamics verifying certificate honesty across all observables."""
    chain = TFIMChain(num_sites=4, J=1.0, h=1.0)
    rho0 = polarized_x_state(4)
    obs = {
        "M_stag": staggered_magnetization(4),
        "C_mid": center_correlation(4),
        "M_x": transverse_magnetization(4),
    }
    times = np.linspace(0.0, 0.4, 9)
    
    exact = evolve_exact(chain, rho0, times, obs)
    adapt = evolve_adaptive(chain, rho0, obs, times, tol=0.1, max_bond=4)
    
    report = verify_bound_honesty(exact, adapt, obs)
    for name, v in report.items():
        assert v.is_honest, f"Certificate violated for {name} with min margin {v.min_margin}"
        assert v.min_margin >= -1e-12
        # Error must be strictly within [0, 1]
        assert np.all(v.true_errors <= 1.0 + 1e-12)


def test_e2e_xxz_heisenberg_quench_n4():
    """Scenario 2: XXZ Heisenberg chain quench dynamics starting from pure Néel state."""
    chain = XXZChain(num_sites=4, J=1.0, delta=1.0, h=0.2)
    rho0 = neel_state(4)
    obs = {
        "M_stag": staggered_magnetization(4),
        "C_mid": center_correlation(4),
    }
    times = np.linspace(0.0, 0.3, 7)
    
    exact = evolve_exact(chain, rho0, times, obs)
    adapt = evolve_adaptive(chain, rho0, obs, times, tol=0.08, max_bond=4)
    
    report = verify_bound_honesty(exact, adapt, obs)
    for name, v in report.items():
        assert v.is_honest, f"XXZ certificate violated for {name}"
        assert np.all(v.margins >= -1e-12)
        # Tightness ratio must be in [0, 1]
        assert np.all(v.tightness_ratios <= 1.0 + 1e-7)


def test_e2e_adaptive_vs_mean_field_fixture():
    """Compare terminal errors for this fixture; parameter budgets differ."""
    chain = TFIMChain(num_sites=4, J=1.0, h=1.0)
    rho0 = polarized_x_state(4)
    obs = {"C_mid": center_correlation(4)}
    times = np.linspace(0.0, 0.3, 7)
    
    exact = evolve_exact(chain, rho0, times, obs)
    mf = evolve_mean_field(chain, rho0, times, obs)
    adapt = evolve_adaptive(chain, rho0, obs, times, tol=0.01, max_bond=4, refine_threshold=0.01)
    
    # Evaluate terminal error |<C_mid>_exact - <C_mid>_approx| at t_end
    err_mf = abs(exact.expectation("C_mid")[-1] - mf.expectation("C_mid")[-1])
    err_adapt = abs(exact.expectation("C_mid")[-1] - adapt.expectation("C_mid")[-1])
    
    # This chosen fixture improves or matches the mean-field reference error.
    assert err_adapt <= err_mf + 1e-10


def test_e2e_n6_simulation_scalability():
    """Verify simulation executes cleanly on N=6 spin chain."""
    chain = TFIMChain(num_sites=6, J=1.0, h=1.0)
    rho0 = polarized_x_state(6)
    obs = {"M_stag": staggered_magnetization(6)}
    times = [0.0, 0.1, 0.2]
    
    exact = evolve_exact(chain, rho0, times, obs)
    adapt = evolve_adaptive(chain, rho0, obs, times, tol=0.2, max_bond=4)
    
    report = verify_bound_honesty(exact, adapt, obs)
    assert report["M_stag"].is_honest
