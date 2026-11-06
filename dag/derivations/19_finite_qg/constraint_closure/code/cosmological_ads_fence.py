"""SP5b: Sign evaluation for a supplied discrete-action fixture.

For the declared formulas, the supplied point k=6 has:
  ε(6) ≈ -1.6255 rad < 0
  s(6) ≈ -5.2688 < 0
Separately, the supplied Friedmann acceleration expression is negative for
the tested nonnegative density and pressure inputs.  These calculations do
not derive an Anti-de Sitter spacetime, a ground state, or a cosmology from
the repository's discrete data.

AuthorityEffect: None.
"""

from __future__ import annotations

import math


THETA_4D = math.acos(0.25)
GAMMA_BI = 0.274066


def discrete_k6_sign_fixture() -> dict:
    """Evaluate the supplied deficit and action formulas at k=6."""
    eps_6 = 2 * math.pi - 6 * THETA_4D
    s_6 = eps_6 + (1.0 / GAMMA_BI) * math.sin(eps_6)

    return {
        "epsilon_6": eps_6,
        "s_6": s_6,
        "epsilon_is_negative": eps_6 < 0,
        "action_is_negative": s_6 < 0,
        "deficit_sign": "negative" if eps_6 < 0 else "nonnegative",
    }


def lambda_residual_unsigned(s_k: float) -> float:
    """Λ_residual = |Φ| as unsigned geometric frustration magnitude.

    This is NOT dark energy. It is a measure of geometric frustration.
    """
    return abs(s_k)


def matter_deceleration(rho: float, p: float, G: float = 1.0) -> dict:
    """Compute Friedmann deceleration for matter with equation of state w = p/ρ.

    ä/a = -(4πG/3)(ρ + 3p)

    For normal matter: ρ > 0, p ≥ 0 ⟹ ä < 0 (deceleration).
    Acceleration requires w < -1/3 (dark energy / negative pressure).
    """
    assert rho >= 0
    assert p >= 0

    q = -(4 * math.pi * G / 3) * (rho + 3 * p)
    w = p / rho if rho > 0 else 0

    return {
        "rho": rho,
        "p": p,
        "w": w,
        "a_ddot_over_a": q,
        "decelerates": q < 0,
        "requires_w_below_minus_third_for_acceleration": True,
    }


def evaluate_declared_sign_cases() -> dict:
    """Evaluate k=6 and three supplied matter cases without physical transport."""
    gc = discrete_k6_sign_fixture()

    matter_cases = [
        {"label": "dust", "rho": 1.0, "p": 0.0},
        {"label": "radiation", "rho": 1.0, "p": 1.0 / 3},
        {"label": "stiff_matter", "rho": 1.0, "p": 1.0},
    ]
    deceleration_results = []
    for case in matter_cases:
        result = matter_deceleration(case["rho"], case["p"])
        result["label"] = case["label"]
        deceleration_results.append(result)

    all_decelerate = all(r["decelerates"] for r in deceleration_results)

    return {
        "k6_fixture": gc,
        "matter_cases": deceleration_results,
        "all_normal_matter_decelerates": all_decelerate,
        "scope": (
            "Arithmetic evaluation of supplied discrete-action and Friedmann "
            "formulas; no spacetime or matter coupling is derived."
        ),
    }
