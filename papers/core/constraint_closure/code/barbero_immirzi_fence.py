"""SP5a: 4D Barbero-Immirzi Action Runaway Fence.

Track B diagnostic: unconstrained s(k) → -∞ linearly.
Corrected escape barrier: s(8) - s(6) ≈ 4.2916.
MCMC finite-run observation: 80.94% on [3,8] → 0.004% on [3,15] at k=6 (seed 42, 50,000 steps).
Recorded as finite-run observations for the declared action density on finite boxes.

AuthorityEffect: None.
"""

from __future__ import annotations

import math
import numpy as np


THETA_4D = math.acos(0.25)  # ≈ 1.318116 rad
GAMMA_BI = 0.274066


def deficit_4d(k: int) -> float:
    """4D hyper-dihedral deficit angle: ε(k) = 2π - k·arccos(1/4)."""
    return 2 * math.pi - k * THETA_4D


def action_density(k: int, gamma: float = GAMMA_BI) -> float:
    """Barbero-Immirzi action density: s(k) = ε(k) + (1/γ)·sin(ε(k))."""
    eps = deficit_4d(k)
    return eps + (1.0 / gamma) * math.sin(eps)


def flat_packing_limit() -> int:
    """Maximum integer valency for flat 4D Euclidean packing."""
    return int(math.floor(2 * math.pi / THETA_4D))


def compute_action_table(k_min: int = 3, k_max: int = 25) -> dict:
    """Evaluate s(k) across a range of valencies."""
    table = {}
    for k in range(k_min, k_max + 1):
        table[k] = action_density(k)
    return table


def escape_barrier() -> dict:
    """Compute the CORRECTED escape barrier from k*=6 to runaway.

    The true barrier is s(8) - s(6) ≈ 4.2916, not s(7) - s(6) ≈ 1.6076.
    After the barrier peak at k=8, s(k) plunges below s(6) permanently.
    """
    s6 = action_density(6)
    s7 = action_density(7)
    s8 = action_density(8)
    s10 = action_density(10)

    return {
        "s6": s6,
        "s7": s7,
        "s8": s8,
        "s10": s10,
        "barrier_to_k7": s7 - s6,  # ≈ 1.6076
        "barrier_to_k8_peak": s8 - s6,  # ≈ 4.2916
        "runaway_at_k10": s10 - s6,  # < 0: s(10) < s(6)
    }


def mcmc_valency_demo(
    n_steps: int = 50_000,
    k_range: tuple[int, int] = (3, 8),
    beta: float = 1.0,
    seed: int = 42,
) -> dict:
    """Run Metropolis-Hastings over valencies k in [k_min, k_max].

    Returns visit fractions for each k.
    """
    rng = np.random.default_rng(seed)
    k_min, k_max = k_range
    k = 6  # start at expected minimum

    visits = {kv: 0 for kv in range(k_min, k_max + 1)}
    current_s = action_density(k)

    for _ in range(n_steps):
        k_proposal = rng.integers(k_min, k_max + 1)
        s_proposal = action_density(k_proposal)
        delta_s = s_proposal - current_s

        if delta_s <= 0 or rng.random() < math.exp(-beta * delta_s):
            k = k_proposal
            current_s = s_proposal

        visits[k] += 1

    total = sum(visits.values())
    fractions = {kv: visits[kv] / total for kv in visits}

    return {
        "k_range": k_range,
        "n_steps": n_steps,
        "beta": beta,
        "visits": visits,
        "fractions": fractions,
    }
