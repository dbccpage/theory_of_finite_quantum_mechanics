"""
density_builder.py
FORGE-S1 Feature Projection phi(x), State Feature Matrix F, and Density Matrix rho Builder.
AuthorityEffect: None.
"""

import math
from typing import List
from omega_engine.crates.linear_algebra_theory.density import (
    NumericalDensityMatrix,
    DensityMatrixCandidate,
    DensityMatrixConfig,
)


def phi_binning(features: List[float], num_bins: int = 8) -> List[complex]:
    """Map raw feature values x onto complex phase unit vectors exp(i * theta_k).

    Empty features pad to ``max(num_bins, 1)`` ones (parity with Rust FORGE-S4).
    Negative feature values use Euclidean remainder into [0, 1) for the phase.
    """
    if num_bins < 0:
        raise ValueError("num_bins must be non-negative")
    bins = max(num_bins, 1)
    if not features:
        return [complex(1.0, 0.0)] * bins

    phases: List[complex] = []
    for x in features:
        if not math.isfinite(x):
            frac = 0.0
        else:
            frac = float(x) % 1.0
        theta = 2.0 * math.pi * frac
        phase = complex(math.cos(theta), math.sin(theta))
        phases.append(phase)

    target = bins if num_bins == 0 else num_bins
    if len(phases) > target:
        phases = phases[:target]
    elif len(phases) < target:
        phases.extend([complex(1.0, 0.0)] * (target - len(phases)))

    return phases


def build_state_feature_matrix(
    samples: List[List[float]], num_bins: int = 8
) -> List[List[complex]]:
    """
    Construct state feature matrix F = [phi(x_1), phi(x_2), ..., phi(x_N)]
    where F has shape (M_bins, N_samples).
    """
    if not samples:
        bins = max(num_bins, 1)
        return [[complex(1.0, 0.0)] for _ in range(bins)]

    cols = [phi_binning(sample, num_bins=num_bins) for sample in samples]
    num_rows = len(cols[0])
    num_cols = len(cols)

    matrix_F = []
    for r in range(num_rows):
        row = [cols[c][r] for c in range(num_cols)]
        matrix_F.append(row)

    return matrix_F


def build_density_matrix_from_matrix(
    matrix_F: List[List[complex]],
) -> NumericalDensityMatrix:
    r"""
    Construct density matrix rho = (F * F^\dagger) / Tr(F * F^\dagger).
    Returns a normalized NumericalDensityMatrix with Tr(rho) == 1.0.
    """
    num_rows = len(matrix_F)
    num_cols = len(matrix_F[0])

    rho_data = [[complex(0.0, 0.0) for _ in range(num_rows)] for _ in range(num_rows)]

    for i in range(num_rows):
        for j in range(num_rows):
            val = complex(0.0, 0.0)
            for k in range(num_cols):
                val += matrix_F[i][k] * complex(
                    matrix_F[j][k].real, -matrix_F[j][k].imag
                )
            rho_data[i][j] = val

    trace_val = sum(rho_data[i][i].real for i in range(num_rows))
    if trace_val <= 1e-15:
        trace_val = 1.0

    data_vec = []
    for i in range(num_rows):
        for j in range(num_rows):
            data_vec.append(rho_data[i][j] / trace_val)

    config = DensityMatrixConfig.default()
    candidate = DensityMatrixCandidate.from_raw(num_rows, data_vec)
    candidate.diagnostic_hermitian_project()
    return candidate.validate(config)



