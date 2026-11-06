"""SP1: L1 Hodge-split calculations on the directed 3-cycle C3.

Implements exact computation of the L1 Hodge split bookkeeping inflation
ratio R_split, representative inflation R_rep, and quotient norm comparison
Phi_1 / Phi_2 on the oriented 3-cycle C3 = partial Delta^2.

Mathematical Reference:
  - R_split(omega) = (||d0 alpha_L2||_1 + ||h_L2||_1) / ||omega||_1
  - Exact fixture: R_split = 7/3 at the six signed basis indicators
  - R_rep(omega) = ||h_L2||_1 / Phi_1([omega]) = 1 for non-coboundaries
  - Phi_1([omega]) / Phi_2([omega]) = sqrt(3) on H^1(C3)
  - On C_n: R_split(e_0) = 3 - 2/n

AuthorityEffect: None.

The sampler below is falsification evidence for the proposed global ceiling,
not a proof of that ceiling.
"""

from __future__ import annotations

import numpy as np


def coboundary_d0_cycle(n: int) -> np.ndarray:
    """Build the n x n coboundary operator d0 for the directed n-cycle C_n."""
    D = np.zeros((n, n), dtype=float)
    for i in range(n):
        D[i, i] = -1.0
        D[i, (i + 1) % n] = 1.0
    return D


def hodge_decomposition_cn(omega: np.ndarray, n: int | None = None) -> dict:
    """Compute the L2 Hodge decomposition on the directed n-cycle.

    Returns dict with keys:
      s: spatial mean
      h_L2: harmonic component (s, s, ..., s)
      exact_L2: exact component omega - h_L2
    """
    if n is None:
        n = len(omega)
    omega = np.asarray(omega, dtype=float)
    s = np.sum(omega) / n
    h = np.full(n, s)
    exact = omega - h
    return {"s": s, "h_L2": h, "exact_L2": exact}


def compute_split_inflation(omega: np.ndarray) -> dict:
    """Compute R_split, R_rep, Phi_1, Phi_2, and their ratio on C3.

    For omega in R^3 (1-cochains on the directed 3-cycle):
      R_split = (||exact||_1 + ||h||_1) / ||omega||_1
      R_rep   = ||h||_1 / Phi_1  (for non-coboundaries)
      Phi_1   = inf_alpha ||omega - d0 alpha||_1 = 3|s|
      Phi_2   = ||h||_2 = sqrt(3)|s|
      ratio   = Phi_1 / Phi_2 = sqrt(3)
    """
    omega = np.asarray(omega, dtype=float)
    assert len(omega) == 3, "omega must be a 3-vector for C3"

    norm1_omega = np.sum(np.abs(omega))
    if norm1_omega == 0:
        return {
            "R_split": float("nan"),
            "R_rep": float("nan"),
            "Phi1": 0.0,
            "Phi2": 0.0,
            "ratio": float("nan"),
        }

    decomp = hodge_decomposition_cn(omega, 3)
    s = decomp["s"]
    h = decomp["h_L2"]
    exact = decomp["exact_L2"]

    norm1_h = np.sum(np.abs(h))
    norm1_exact = np.sum(np.abs(exact))

    R_split = (norm1_exact + norm1_h) / norm1_omega

    Phi1 = 3.0 * abs(s)

    Phi2 = np.sqrt(3.0) * abs(s)

    if abs(s) < 1e-15:
        R_rep = float("nan")
        ratio = float("nan")
    else:
        R_rep = norm1_h / Phi1
        ratio = Phi1 / Phi2

    return {
        "R_split": R_split,
        "R_rep": R_rep,
        "Phi1": Phi1,
        "Phi2": Phi2,
        "ratio": ratio,
    }


def compute_split_inflation_cn(omega: np.ndarray, n: int) -> dict:
    """Compute R_split on the directed n-cycle C_n."""
    omega = np.asarray(omega, dtype=float)
    assert len(omega) == n

    norm1_omega = np.sum(np.abs(omega))
    if norm1_omega == 0:
        return {"R_split": float("nan"), "n": n}

    decomp = hodge_decomposition_cn(omega, n)
    h = decomp["h_L2"]
    exact = decomp["exact_L2"]

    norm1_h = np.sum(np.abs(h))
    norm1_exact = np.sum(np.abs(exact))

    R_split = (norm1_exact + norm1_h) / norm1_omega
    return {"R_split": R_split, "n": n}


def sample_split_bound_c3(n_samples: int = 100_000, seed: int = 42) -> dict:
    """Search random normalized cochains for a counterexample to 7/3."""
    rng = np.random.default_rng(seed)
    max_R = 0.0
    max_omega = None

    for _ in range(n_samples):
        omega = rng.standard_normal(3)
        norm = np.sum(np.abs(omega))
        if norm < 1e-15:
            continue
        omega /= norm

        result = compute_split_inflation(omega)
        if result["R_split"] > max_R:
            max_R = result["R_split"]
            max_omega = omega.copy()

    return {
        "scope": "random_sample_only",
        "n_samples": n_samples,
        "max_R_split": max_R,
        "ceiling_7_3": 7.0 / 3.0,
        "satisfies_bound": max_R <= 7.0 / 3.0 + 1e-10,
        "maximizer": max_omega,
    }
