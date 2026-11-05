"""Exact finite reconstruction witnesses; AuthorityEffect: None.

These fixtures verify arithmetic consequences of explicitly declared signed
readouts and Hilbert composition. They do not implement a reconstruction solver.
The reusable general implementations belong to the native Rust owners.
"""
from fractions import Fraction


def signed_readout_countermodel() -> dict[str, object]:
    """Total-positive signed weights fail full-effect classical positivity."""
    weights = (Fraction(2), Fraction(-1))
    return {
        "weights": weights,
        "total": sum(weights),
        "negative_indicator": weights[1],
        "all_reports_classical": all(weight >= 0 for weight in weights),
        "coarse_report_probability": sum(weights),
        "negative_jordan_mass": -weights[1],
    }


def composition_discriminator_witness() -> dict[str, object]:
    """Bell density + rational local directions (3/5, +/-4/5).

    The native tests independently construct the matrices and certify their
    involution/PSD identities. Here we check the resulting scalar certificate.
    The squared bound is necessary for quantum CHSH, not sufficient for quantum
    membership, and imports tensor/trace structure explicitly.
    """
    z_component, x_component = Fraction(3, 5), Fraction(4, 5)
    quantum_chsh = 2 * (z_component + x_component)
    pr_chsh = Fraction(4)
    return {
        "direction_norm_squared": z_component**2 + x_component**2,
        "quantum_chsh": quantum_chsh,
        "quantum_squared": quantum_chsh**2,
        "quantum_bound_slack": 8 - quantum_chsh**2,
        "classical_bound_violated": quantum_chsh > 2,
        "pr_squared": pr_chsh**2,
        "pr_excluded": pr_chsh**2 > 8,
    }
