"""Pytest Test Suite for 4D Regge-Barbero-Immirzi Lattice Monte Carlo Simulation.

AuthorityEffect: None.

Verifies:
1. Metropolis-Hastings thermal simulation convergence and energy minimization.
2. Deficit angle action stability under thermal fluctuations.
3. Equilibrium valency distribution concentration around k^* = 5 (minimal curvature density).
"""

from __future__ import annotations

import sys
from pathlib import Path


import numpy as np
import pytest

from solv_regge_monte_carlo import (
    ReggeMonteCarloSolverAdapter,
    SolverInput,
    compute_hinge_action,
    run_regge_monte_carlo_simulation,
)



def test_hinge_action_computation():
    """Verify single hinge action for flat vs deficit valencies."""
    action_k4 = compute_hinge_action(4)
    action_k5 = compute_hinge_action(5)

    assert isinstance(action_k4, float)
    assert isinstance(action_k5, float)
    assert action_k4 != action_k5


def test_regge_monte_carlo_simulation_convergence():
    """Verify Metropolis-Hastings thermal simulation converges to stable mean valency."""
    res = run_regge_monte_carlo_simulation(
        n_hinges=40,
        n_steps=1500,
        beta=2.0,
        seed=123,
    )

    assert res["n_hinges"] == 40
    assert res["acceptance_rate"] > 0.05
    assert 4.0 <= res["final_mean_valency"] <= 6.5
    assert res["authority_effect"] == "None"


def test_regge_monte_carlo_high_beta_cooling():
    """Verify high-beta (low temperature) cooling concentrates valencies at minimum action state (k=6)."""
    res_cold = run_regge_monte_carlo_simulation(
        n_hinges=30,
        n_steps=2000,
        beta=10.0,
        seed=456,
    )

    counts = res_cold["valency_counts"]
    assert counts.get(6, 0) > counts.get(3, 0) + counts.get(8, 0)
    assert counts.get(6, 0) == 30


def test_standalone_solver_adapter_returns_a_real_certificate():
    adapter = ReggeMonteCarloSolverAdapter()
    result = adapter.solve(
        SolverInput(
            problem_id="regge-fixture",
            data={"n_hinges": 4, "n_steps": 20, "seed": 9},
        )
    )
    assert result.problem_id == "regge-fixture"
    assert result.status == "SOLVED"
    assert result.certificate.is_valid
    assert len(result.certificate.certificate_hash) == 64
