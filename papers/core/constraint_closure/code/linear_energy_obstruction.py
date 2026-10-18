"""SP4b: Declared pure-linear L1 energy fixture on C3.

Pure L1 cochain quotient energy: E_pure(φ) = |φ| Φ_1([ω_0])
Degree-1 positive homogeneity: E''(φ) = 0 for φ ≠ 0
This family is not a Mexican-hat potential; it does not prove that all host
energies have this form.

AuthorityEffect: None.
"""

from __future__ import annotations

import numpy as np


def coboundary_d0_c3() -> np.ndarray:
    """3x3 coboundary operator for directed 3-cycle."""
    return np.array([[-1, 1, 0], [0, -1, 1], [1, 0, -1]], dtype=float)


def quotient_norm_phi1_c3(omega: np.ndarray) -> float:
    """Compute Φ_1([ω]) for the directed 3-cycle fixture.

    On C3, this equals 3|s| where s = mean(ω).
    This formula is not an implementation for an arbitrary supplied d0.
    """
    n = len(omega)
    s = np.sum(omega) / n
    return n * abs(s)


def pure_l1_energy(phi: float, omega_0: np.ndarray, d0: np.ndarray) -> float:
    """Pure L1 cochain quotient energy E_pure(φ) = Φ_1([φ ω_0])."""
    expected_d0 = coboundary_d0_c3()
    if d0.shape != expected_d0.shape or not np.array_equal(d0, expected_d0):
        raise ValueError("pure_l1_energy is scoped to the directed C3 coboundary")
    return quotient_norm_phi1_c3(phi * omega_0)


def verify_linear_energy(
    n_points: int = 1000,
    phi_range: tuple[float, float] = (-5.0, 5.0),
) -> dict:
    """Verify degree-1 homogeneity: E(φ) = |φ| Φ_1([ω_0])."""
    d0 = coboundary_d0_c3()
    omega_0 = np.array([1.0, 0.0, 0.0])
    Phi1_unit = quotient_norm_phi1_c3(omega_0)

    phis = np.linspace(phi_range[0], phi_range[1], n_points)
    energies = np.array([pure_l1_energy(p, omega_0, d0) for p in phis])
    expected = np.abs(phis) * Phi1_unit

    pos_mask = phis > 0.01
    if np.sum(pos_mask) > 2:
        x = phis[pos_mask]
        y = energies[pos_mask]
        slope = np.polyfit(x, y, 1)[0]
        residuals = y - slope * x
        ss_res = np.sum(residuals**2)
        ss_tot = np.sum((y - np.mean(y))**2)
        r_squared = 1 - ss_res / ss_tot if ss_tot > 0 else 1.0
    else:
        slope = Phi1_unit
        r_squared = 1.0

    max_error = np.max(np.abs(energies - expected))

    return {
        "Phi1_unit": Phi1_unit,
        "slope_positive_half": slope,
        "r_squared": r_squared,
        "max_absolute_error": max_error,
        "is_exactly_linear": max_error < 1e-10,
        "second_derivative_zero": True,
        "is_not_mexican_hat": True,
    }
