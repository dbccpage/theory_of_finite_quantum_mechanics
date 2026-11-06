"""GR-002 compatibility exports for the paper-local Regge Monte Carlo fixture.

AuthorityEffect: None.
"""

from __future__ import annotations

from regge_monte_carlo import (
    ReggeMonteCarloSolverAdapter,
    SolverInput,
    analytical_boltzmann_distribution,
    compute_hinge_action,
    run_regge_monte_carlo_simulation,
)

__all__ = [
    "analytical_boltzmann_distribution",
    "compute_hinge_action",
    "run_regge_monte_carlo_simulation",
    "ReggeMonteCarloSolverAdapter",
    "SolverInput",
]
