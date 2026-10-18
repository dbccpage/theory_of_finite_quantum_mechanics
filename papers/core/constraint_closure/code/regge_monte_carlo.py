"""4D Regge-Barbero-Immirzi Lattice Monte Carlo Solver Subsystem.

Conforms strictly to contract specification:
    urn:omega:math:solver:v1.0.0

AuthorityEffect: None.

Executes thermal Metropolis-Hastings sweeps over 4D simplicial block hinge valencies k_i
under the Regge-Barbero-Immirzi discrete action:
    S_{BI}^{(4D)} = sum_i A_i * ( epsilon_i^{(4D)} + (1 / gamma) * sin(epsilon_i^{(4D)}) )
"""

from __future__ import annotations

import hashlib
import json
import math
from dataclasses import dataclass
from typing import Any, Dict, List, Tuple
import numpy as np

try:
    from universe_anomalonica.omega_engine.solver.solver import (
        BaseSolver,
        SolverCertificate,
        SolverInput,
        SolverOutput,
    )
except ImportError:
    # Standalone paper-package fallback.  These are usable value objects, not
    # empty mocks that make an unexercised adapter appear to work.
    @dataclass(frozen=True)
    class SolverCertificate:  # type: ignore[no-redef]
        certificate_type: str
        witness_data: Dict[str, Any]
        is_valid: bool
        certificate_hash: str

    @dataclass(frozen=True)
    class SolverInput:  # type: ignore[no-redef]
        problem_id: str
        category: str = "LatticeMonteCarlo"
        data: Dict[str, Any] | None = None
        parameters: Dict[str, Any] | None = None

    @dataclass(frozen=True)
    class SolverOutput:  # type: ignore[no-redef]
        problem_id: str
        solver_id: str
        status: str
        residual_mass: float
        residual_vector: List[float]
        certificate: SolverCertificate
        metadata: Dict[str, Any]
        authority_effect: str

    class BaseSolver:  # type: ignore[no-redef]
        def __init__(self, solver_id: str, category: str, solver_version: str):
            self.solver_id = solver_id
            self.category = category
            self.solver_version = solver_version


def analytical_boltzmann_distribution(
    beta: float = 1.0,
    immirzi_gamma: float = 0.274066,
    k_range: Sequence[int] = (3, 4, 5, 6, 7, 8),
) -> Dict[int, float]:
    """Exact finite Boltzmann distribution over uncoupled 4D Regge-Barbero-Immirzi hinge valencies.

    Formula:
        p(k) = exp(-beta * s(k)) / sum_{j in k_range} exp(-beta * s(j))
    where s(k) is the single-hinge Barbero-Immirzi action computed via compute_hinge_action.
    """
    weights = {
        k: math.exp(-beta * compute_hinge_action(k, area=1.0, immirzi_gamma=immirzi_gamma))
        for k in k_range
    }
    z = sum(weights.values())
    return {k: float(w / z) for k, w in weights.items()}


def compute_hinge_action(
    k: int,
    area: float = 1.0,
    immirzi_gamma: float = 0.274066,
) -> float:
    """Compute 4D Regge-Barbero-Immirzi action for a single hinge with valency k."""
    theta_hyper = math.acos(0.25)  # arccos(1/4) ~ 1.318116 rad
    epsilon = 2.0 * math.pi - k * theta_hyper
    return area * (epsilon + (1.0 / max(1e-6, immirzi_gamma)) * math.sin(epsilon))


def run_regge_monte_carlo_simulation(
    n_hinges: int = 50,
    n_steps: int = 2000,
    beta: float = 1.0,
    immirzi_gamma: float = 0.274066,
    seed: int = 42,
) -> Dict[str, Any]:
    """Execute Metropolis-Hastings thermal simulation of 4D Regge hinge valencies."""
    np.random.seed(seed)
    # Initialize hinges with random initial valencies k in [3, 7]
    valencies = np.random.randint(3, 8, size=n_hinges)
    areas = np.ones(n_hinges)

    current_actions = np.array([
        compute_hinge_action(k, area, immirzi_gamma)
        for k, area in zip(valencies, areas)
    ])
    total_action = float(np.sum(current_actions))

    valency_history = []
    action_history = []
    n_accepted = 0

    for step in range(n_steps):
        # Pick random hinge
        idx = np.random.randint(0, n_hinges)
        current_k = valencies[idx]

        # Propose step delta_k in {-1, +1} with boundaries in [3, 8]
        delta_k = np.random.choice([-1, 1])
        proposed_k = current_k + delta_k
        if proposed_k < 3 or proposed_k > 8:
            continue

        proposed_action = compute_hinge_action(proposed_k, areas[idx], immirzi_gamma)
        delta_s = proposed_action - current_actions[idx]

        # Metropolis-Hastings acceptance rule
        if delta_s <= 0 or np.random.rand() < math.exp(-beta * delta_s):
            valencies[idx] = proposed_k
            total_action += delta_s
            current_actions[idx] = proposed_action
            n_accepted += 1

        if step % 10 == 0:
            valency_history.append(int(valencies[idx]))
            action_history.append(total_action)

    mean_valency = float(np.mean(valencies))
    valency_counts = {int(k): int(np.sum(valencies == k)) for k in range(3, 9)}
    total_valencies = len(valencies)
    p_analytical = analytical_boltzmann_distribution(beta=beta, immirzi_gamma=immirzi_gamma)
    empirical_dist = {k: valency_counts[k] / total_valencies for k in range(3, 9)}
    tv_distance = 0.5 * sum(abs(empirical_dist[k] - p_analytical[k]) for k in range(3, 9))

    acceptance_rate = n_accepted / max(1, n_steps)
    budget_heuristic_reached = bool(n_steps >= 3 * n_hinges and n_steps > 0)

    return {
        "n_hinges": n_hinges,
        "n_steps": n_steps,
        "beta": beta,
        "acceptance_rate": acceptance_rate,
        "final_mean_valency": mean_valency,
        "valency_counts": valency_counts,
        "empirical_distribution": empirical_dist,
        "analytical_distribution": p_analytical,
        "total_variation_distance": float(tv_distance),
        "final_total_action": total_action,
        "total_action": total_action,
        "mean_action_per_hinge": total_action / max(1, n_hinges),
        "budget_heuristic_reached": budget_heuristic_reached,
        "has_adequate_sampling": budget_heuristic_reached,  # Retained for backward compat, documented as budget heuristic
        "equilibrium_assertion": "NOT_CERTIFIED_BUDGET_HEURISTIC_ONLY",
        "authority_effect": "None",
    }


class ReggeMonteCarloSolverAdapter(BaseSolver):
    """Adapter wrapping 4D Regge-Barbero-Immirzi Lattice Monte Carlo simulation."""

    def __init__(self, solver_id: str = "regge_monte_carlo"):
        super().__init__(
            solver_id=solver_id,
            category="LatticeMonteCarlo",
            solver_version="v1.0.0",
        )

    def solve(self, solver_input: SolverInput) -> SolverOutput:
        data = solver_input.data or solver_input.parameters or {}
        n_hinges = int(data.get("n_hinges", 50))
        n_steps = int(data.get("n_steps", 2000))
        beta = float(data.get("beta", 1.0))
        immirzi_gamma = float(data.get("immirzi_gamma", 0.274066))
        seed = int(data.get("seed", 42))

        if n_steps <= 0:
            cert_bytes = json.dumps({"error": "No sampling steps"}, sort_keys=True).encode("utf-8")
            cert_hash = hashlib.sha256(cert_bytes).hexdigest()
            return SolverOutput(
                problem_id=solver_input.problem_id,
                solver_id=self.solver_id,
                status="NO_SAMPLING",
                residual_mass=1.0,
                residual_vector=[1.0],
                certificate=SolverCertificate(
                    certificate_type="MONTE_CARLO_SAMPLING_RECEIPT",
                    witness_data={"n_steps": 0, "sampling_status": "NO_STEPS"},
                    is_valid=False,
                    certificate_hash=cert_hash,
                ),
                metadata={"n_steps": 0, "total_action": 0.0},
                authority_effect="EvidenceOnly",
            )

        mc_res = run_regge_monte_carlo_simulation(
            n_hinges=n_hinges,
            n_steps=n_steps,
            beta=beta,
            immirzi_gamma=immirzi_gamma,
            seed=seed,
        )

        cert_bytes = json.dumps(mc_res, sort_keys=True, default=str).encode("utf-8")
        cert_hash = hashlib.sha256(cert_bytes).hexdigest()

        is_adequate = mc_res.get("budget_heuristic_reached", False)
        status = "SOLVED" if is_adequate else "SAMPLING_COMPLETED_NOT_EQUILIBRATED"
        tv_dist = float(mc_res.get("total_variation_distance", 0.0))

        output = SolverOutput(
            problem_id=solver_input.problem_id,
            solver_id=self.solver_id,
            status=status,
            residual_mass=tv_dist,
            residual_vector=[tv_dist],
            certificate=SolverCertificate(
                certificate_type="MONTE_CARLO_SAMPLING_RECEIPT",
                witness_data={
                    "sampling_data": mc_res,
                    "budget_heuristic_met": is_adequate,
                    "statistical_assessment": "Finite MCMC sample trajectory, data identity hashed; equilibrium not formally guaranteed.",
                },
                is_valid=is_adequate,
                certificate_hash=cert_hash,
            ),
            metadata=mc_res,
            authority_effect="EvidenceOnly",
        )
        return output


__all__ = [
    "analytical_boltzmann_distribution",
    "compute_hinge_action",
    "run_regge_monte_carlo_simulation",
    "ReggeMonteCarloSolverAdapter",
]
