"""SP5d: Quadratic-penalty spike-suppression fixture.

Demonstrates that adding the *declared* quadratic penalty S_penalty(k) to the
supplied action suppresses the sampled high-k region and concentrates the
finite-state Markov chain at k=6.  The penalty is not derived from causal
dynamical triangulations or a time foliation.

Unconstrained: S_eff(k) = s(k) ⟹ s(k) → -∞ as k → ∞, visits collapse to < 1% at k=6.
Penalized: S_eff(k) = s(k) + λ * (k - 6)²
           ⟹ k=6 is the minimum on [3, 20], with visits > 70%.

AuthorityEffect: None.
"""

from __future__ import annotations

import math
import numpy as np


THETA_4D = math.acos(0.25)  # ≈ 1.318116 rad
GAMMA_BI = 0.274066


def bare_action_density(k: int, gamma: float = GAMMA_BI) -> float:
    """Bare 4D Barbero-Immirzi action density: s(k) = ε(k) + (1/γ) sin(ε(k))."""
    eps = 2 * math.pi - k * THETA_4D
    return eps + (1.0 / gamma) * math.sin(eps)


def causal_slice_penalty(k: int, lambda_causal: float = 1.5, k_slice: int = 6) -> float:
    """Declared quadratic penalty S_penalty(k) = λ * (k - k_slice)²."""
    return lambda_causal * float((k - k_slice) ** 2)


def effective_causal_action(
    k: int,
    lambda_causal: float = 1.5,
    gamma: float = GAMMA_BI,
) -> float:
    """Effective action S_eff(k) = s(k) + S_causal(k)."""
    return bare_action_density(k, gamma) + causal_slice_penalty(k, lambda_causal)


def compare_action_profiles(k_max: int = 20, lambda_causal: float = 1.5) -> dict:
    """Compare bare vs causally-constrained action profiles for k in [3, k_max]."""
    ks = list(range(3, k_max + 1))
    bare = [bare_action_density(k) for k in ks]
    causal = [effective_causal_action(k, lambda_causal) for k in ks]

    min_bare_k = ks[int(np.argmin(bare))]
    min_causal_k = ks[int(np.argmin(causal))]

    return {
        "ks": ks,
        "bare_actions": bare,
        "causal_actions": causal,
        "bare_minimum_k": min_bare_k,  # = 20 (plunging to infinity)
        "causal_minimum_k": min_causal_k,  # = 6 (stable)
        "bare_plunges": bare[-1] < bare[3],
        "causal_stabilized": min_causal_k == 6,
    }


def mcmc_causal_comparison(
    n_steps: int = 50_000,
    k_range: tuple[int, int] = (3, 20),
    lambda_causal: float = 1.5,
    beta: float = 1.0,
    seed: int = 42,
) -> dict:
    """Run Metropolis-Hastings MCMC comparing unconstrained vs causally-constrained ensembles."""
    k_min, k_max = k_range

    def run_mcmc(is_causal: bool) -> dict[int, float]:
        rng = np.random.default_rng(seed)
        k = 6
        visits = {kv: 0 for kv in range(k_min, k_max + 1)}

        def get_S(kv: int) -> float:
            return (
                effective_causal_action(kv, lambda_causal)
                if is_causal
                else bare_action_density(kv)
            )

        current_S = get_S(k)

        for _ in range(n_steps):
            k_prop = rng.integers(k_min, k_max + 1)
            S_prop = get_S(k_prop)
            delta_S = S_prop - current_S

            if delta_S <= 0 or rng.random() < math.exp(-beta * delta_S):
                k = k_prop
                current_S = S_prop

            visits[k] += 1

        total = sum(visits.values())
        return {kv: visits[kv] / total for kv in visits}

    unconstrained_fracs = run_mcmc(is_causal=False)
    causal_fracs = run_mcmc(is_causal=True)

    k6_unconstrained = unconstrained_fracs[6]
    k6_causal = causal_fracs[6]
    runaway_unconstrained = sum(unconstrained_fracs[k] for k in range(10, k_max + 1))
    runaway_causal = sum(causal_fracs[k] for k in range(10, k_max + 1))

    return {
        "k_range": k_range,
        "n_steps": n_steps,
        "lambda_causal": lambda_causal,
        "unconstrained_k6_fraction": k6_unconstrained,
        "causal_k6_fraction": k6_causal,
        "unconstrained_runaway_fraction": runaway_unconstrained,
        "causal_runaway_fraction": runaway_causal,
        "spike_suppressed": k6_causal > 0.70,
        "runaway_eliminated": runaway_causal < 0.05,
    }
